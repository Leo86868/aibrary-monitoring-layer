# Manual Setup Guide - Add First Target

**Issue**: API has field format issues, but tables work perfectly via Lark interface.

## 📋 **Add @openai Target Manually**

### Step 1: Open Your Lark Base
- Go to: https://larksuite.com
- Navigate to Base ID: `Qr40bFHf8aKpBosZjXbcjF4rnXe`
- Open **Monitoring_Targets_Simple** table

### Step 2: Add OpenAI Competitor Target
**Click "Add Record" and fill in:**

| Field | Value | Notes |
|-------|-------|-------|
| **target_value** | `@openai` | TikTok username |
| **platform** | `tiktok` | Select from dropdown |
| **target_type** | `profile` | Select from dropdown |
| **active** | ✅ Checked | Enable monitoring |
| **results_limit** | `20` | Posts per run |
| **team_notes** | `Primary competitor - monitor content strategy` | Why we're tracking |
| **created_date** | Auto-filled | Leave as default |

### Step 3: Verify the Record
After saving, you should see:
- ✅ @openai target in the table
- ✅ All fields populated correctly
- ✅ Ready for TikTok processing

## 🎯 **What This Target Does**

**Strategy**: Competitor Intelligence
- **Monitors**: @openai TikTok profile
- **Collects**: Their 20 most recent posts
- **Purpose**: Learn from their content strategy
- **Team Use**: Review their viral posts, trending topics, engagement patterns

## 🚀 **After Adding Target**

Once you've added the @openai target manually:

1. **Verify Table Works**: Confirm you can see and edit the record
2. **Ready for Processor**: We can build the TikTok scraping script
3. **Team Workflow**: Your 10-person team can add more targets the same way

## 📱 **Future Targets to Add**

After @openai works, consider adding:
- **More Competitors**: `@anthropic`, `@nvidia`, `@microsoft`
- **Trend Discovery**: `#ai`, `#artificialintelligence`, `#machinelearning`
- **Different Platforms**: Instagram profiles when ready

## ⚠️ **API Issue Status**

- **Tables**: ✅ Working perfectly
- **Manual Entry**: ✅ Working perfectly
- **API Insertion**: ❌ Field format issues (can fix later)
- **Processing**: ✅ Ready to build (reads from tables fine)

**Bottom Line**: Manual workflow is ready. API issues don't block progress.

---

**Please add the @openai target manually, then we can build the TikTok processor!**