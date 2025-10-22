"""
AIbrary TikTok Monitoring System - Lark Client
Client for interacting with Lark Base API
"""

import requests
import time
from typing import List, Dict, Any, Optional
from core import (
    MonitoringTarget, TikTokContent,
    LARK_APP_ID, LARK_APP_SECRET, LARK_BASE_ID,
    MONITORING_TARGETS_TABLE, TIKTOK_CONTENT_TABLE
)


class LarkClient:
    """Client for interacting with Lark Base API"""

    def __init__(self):
        self.app_id = LARK_APP_ID
        self.app_secret = LARK_APP_SECRET
        self.base_id = LARK_BASE_ID
        self.access_token = None
        self.token_expires_at = 0

    def _get_access_token(self) -> str:
        """Get or refresh access token"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token

        url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        if data["code"] != 0:
            raise Exception(f"Failed to get access token: {data}")

        self.access_token = data["tenant_access_token"]
        self.token_expires_at = time.time() + data["expire"] - 60

        return self.access_token

    def _make_request(self, method: str, path: str, payload: Optional[Dict] = None) -> Dict[str, Any]:
        """Make authenticated request to Lark API"""
        token = self._get_access_token()

        url = f"https://open.larksuite.com/open-apis{path}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.request(method, url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data["code"] != 0:
            raise Exception(f"Lark API error: {data}")

        return data["data"]

    def _get_table_id(self, table_name: str) -> str:
        """Get table ID by name"""
        path = f"/bitable/v1/apps/{self.base_id}/tables"
        data = self._make_request("GET", path)

        for table in data["items"]:
            if table["name"] == table_name:
                return table["table_id"]

        raise Exception(f"Table '{table_name}' not found")

    def get_active_targets(self) -> List[MonitoringTarget]:
        """Get all active monitoring targets"""
        table_id = self._get_table_id(MONITORING_TARGETS_TABLE)
        path = f"/bitable/v1/apps/{self.base_id}/tables/{table_id}/records"

        data = self._make_request("GET", path)
        targets = []

        for item in data["items"]:
            fields = item["fields"]

            # Only include active targets
            if not fields.get("active", False):
                continue

            # Decode monitoring_strategy from Lark single-select field
            raw_strategy = fields.get("monitoring_strategy", None)
            strategy_text = None
            if raw_strategy and isinstance(raw_strategy, list) and len(raw_strategy) > 0:
                # Lark returns single-select as list with text value
                strategy_text = raw_strategy[0].get("text") if isinstance(raw_strategy[0], dict) else raw_strategy[0]

            target = MonitoringTarget(
                record_id=item["record_id"],
                target_value=fields.get("target_value", ""),
                platform=fields.get("platform", ""),
                target_type=fields.get("target_type", ""),
                active=fields.get("active", False),
                results_limit=int(fields.get("results_limit", 10)),
                monitoring_strategy=strategy_text,
                team_notes=fields.get("team_notes", "")
            )
            targets.append(target)

        return targets

    def content_exists(self, content_id: str) -> Optional[str]:
        """
        Check if content already exists in database
        Returns record_id if exists, None otherwise
        """
        table_id = self._get_table_id(TIKTOK_CONTENT_TABLE)
        path = f"/bitable/v1/apps/{self.base_id}/tables/{table_id}/records"

        try:
            data = self._make_request("GET", path)
            for item in data["items"]:
                if str(item["fields"].get("content_id")) == str(content_id):
                    return item["record_id"]
            return None
        except Exception:
            return None

    def update_content(self, record_id: str, content: TikTokContent) -> bool:
        """
        Update existing content record with new analysis data (Phase 5)
        """
        table_id = self._get_table_id(TIKTOK_CONTENT_TABLE)
        path = f"/bitable/v1/apps/{self.base_id}/tables/{table_id}/records/{record_id}"

        # Build update fields (only AI analysis fields)
        fields = {}

        if content.ai_analysis_result:
            fields["Analysis"] = str(content.ai_analysis_result)

        if content.strategic_score is not None:
            fields["strategic_score"] = float(content.strategic_score)

        if content.content_type:
            fields["content_type"] = str(content.content_type)

        if content.strategic_insights:
            fields["strategic_insights"] = str(content.strategic_insights)

        if content.niche_category:
            fields["niche_category"] = str(content.niche_category)

        if not fields:
            print(f"⚠️ No fields to update for content {content.content_id}")
            return False

        update_data = {"fields": fields}

        try:
            self._make_request("PUT", path, update_data)
            print(f"✅ Updated content: {content.content_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to update content {content.content_id}: {e}")
            return False

    def save_content(self, content_list: List[TikTokContent], target_record_id: str = None) -> bool:
        """
        Save or update TikTok content to Lark table with target linkage
        Phase 5: Check if exists, update if so, create if not
        """
        if not content_list:
            return True

        table_id = self._get_table_id(TIKTOK_CONTENT_TABLE)
        path = f"/bitable/v1/apps/{self.base_id}/tables/{table_id}/records"

        success_count = 0

        for content in content_list:
            # Phase 5: Check if content already exists
            existing_record_id = self.content_exists(content.content_id)

            if existing_record_id:
                # Update existing record
                if self.update_content(existing_record_id, content):
                    success_count += 1
                continue

            # Create new record
            # Calculate engagement rate
            content.engagement_rate = content.calculate_engagement_rate()

            # Build fields dict, omitting empty URL fields
            fields = {
                "content_id": str(content.content_id),  # Text field - preserves full TikTok ID precision
                "Target": [target_record_id] if target_record_id else [],  # Two-way link field - expects array of strings
                "video_url": {"link": str(content.video_url)},  # URL field
                "author_username": str(content.author_username) if content.author_username else "",  # Text field
                "caption": str(content.caption[:500]) if content.caption else "",  # Text field
                "likes": float(content.likes) if content.likes is not None else 0.0,  # Number field
                "comments": float(content.comments) if content.comments is not None else 0.0,  # Number field
                "views": float(content.views) if content.views is not None else 0.0,  # Number field
                "engagement_rate": float(round(content.engagement_rate, 2)) if content.engagement_rate is not None else 0.0,  # Number field
                "Analysis": str(content.ai_analysis_result) if content.ai_analysis_result else "",  # Text field for AI results
            }

            # Add simplified strategic AI analysis fields if available
            if content.strategic_score is not None:
                fields["strategic_score"] = float(content.strategic_score)
            if content.content_type:
                fields["content_type"] = str(content.content_type)
            if content.strategic_insights:
                fields["strategic_insights"] = str(content.strategic_insights)
            if content.niche_category:
                fields["niche_category"] = str(content.niche_category)

            # Only add URL fields if they have valid URLs
            if content.video_download_url:
                fields["video_downlaod_url"] = {"link": str(content.video_download_url)}  # Note: field name has typo in Lark Base
            if content.subtitle_url:
                fields["subtitle_url"] = {"link": str(content.subtitle_url)}

            record_data = {"fields": fields}

            try:
                self._make_request("POST", path, record_data)
                success_count += 1
                print(f"✅ Saved content: {content.content_id}")
            except Exception as e:
                print(f"❌ Failed to save content {content.content_id}: {e}")

        print(f"📊 Saved {success_count}/{len(content_list)} content items")
        return success_count == len(content_list)
