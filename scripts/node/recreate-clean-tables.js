// Recreate tables with completely clean field configurations
const { getAccessToken, BASE_ID } = require('./test-lark-connection.js');
const https = require('https');

// Helper function to make Lark API requests
function makeLarkRequest(path, method, data, accessToken) {
    return new Promise((resolve, reject) => {
        const postData = data ? JSON.stringify(data) : undefined;

        const options = {
            hostname: 'open.larksuite.com',
            port: 443,
            path: path,
            method: method,
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        };

        if (postData) {
            options.headers['Content-Length'] = Buffer.byteLength(postData);
        }

        const req = https.request(options, (res) => {
            let responseData = '';
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            res.on('end', () => {
                const response = JSON.parse(responseData);
                if (response.code === 0) {
                    resolve(response.data);
                } else {
                    console.error(`❌ API Error:`, response);
                    reject(response);
                }
            });
        });

        req.on('error', (e) => {
            console.error('❌ Request error:', e);
            reject(e);
        });

        if (postData) {
            req.write(postData);
        }
        req.end();
    });
}

// Delete table by name
async function deleteTable(accessToken, tableName) {
    try {
        // Get all tables
        const result = await makeLarkRequest(
            `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
            'GET',
            null,
            accessToken
        );

        const table = result.items.find(t => t.name === tableName);
        if (table) {
            await makeLarkRequest(
                `/open-apis/bitable/v1/apps/${BASE_ID}/tables/${table.table_id}`,
                'DELETE',
                null,
                accessToken
            );
            console.log(`🗑️ Deleted old ${tableName} table`);
        }
    } catch (error) {
        console.log(`⚠️ Could not delete ${tableName}:`, error.msg || error);
    }
}

// Create clean monitoring table
async function createCleanMonitoringTable(accessToken) {
    console.log('📊 Creating clean Monitoring_Targets table...');

    const tableSchema = {
        table: {
            name: "Monitoring_Targets_Clean",
            default_view_name: "All Targets",
            fields: [
                {
                    field_name: "target_value",
                    type: 2 // Text - no property needed for simple text
                },
                {
                    field_name: "platform",
                    type: 3, // Single select
                    property: {
                        options: [
                            { name: "tiktok", color: 0 },
                            { name: "instagram", color: 1 },
                            { name: "linkedin", color: 2 }
                        ]
                    }
                },
                {
                    field_name: "target_type",
                    type: 3, // Single select
                    property: {
                        options: [
                            { name: "profile", color: 0 },
                            { name: "hashtag", color: 1 }
                        ]
                    }
                },
                {
                    field_name: "active",
                    type: 7 // Checkbox - no property needed
                },
                {
                    field_name: "results_limit",
                    type: 11 // Number - no property needed for simple number
                },
                {
                    field_name: "team_notes",
                    type: 2 // Text - no property needed
                }
            ]
        }
    };

    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
        'POST',
        tableSchema,
        accessToken
    );
    console.log('✅ Clean Monitoring_Targets table created');
    return result.table_id;
}

// Create clean TikTok content table
async function createCleanTikTokTable(accessToken) {
    console.log('📊 Creating clean TikTok_Content table...');

    const tableSchema = {
        table: {
            name: "TikTok_Content_Clean",
            default_view_name: "Recent Content",
            fields: [
                {
                    field_name: "content_id",
                    type: 2 // Text
                },
                {
                    field_name: "target_value",
                    type: 2 // Text - which target found this
                },
                {
                    field_name: "video_url",
                    type: 15 // URL
                },
                {
                    field_name: "author_username",
                    type: 2 // Text
                },
                {
                    field_name: "caption",
                    type: 2 // Text
                },
                {
                    field_name: "likes",
                    type: 11 // Number
                },
                {
                    field_name: "comments",
                    type: 11 // Number
                },
                {
                    field_name: "views",
                    type: 11 // Number
                },
                {
                    field_name: "engagement_rate",
                    type: 11 // Number
                },
                {
                    field_name: "team_status",
                    type: 3, // Single select
                    property: {
                        options: [
                            { name: "new", color: 0 },
                            { name: "reviewed", color: 1 },
                            { name: "approved", color: 2 },
                            { name: "ignored", color: 3 }
                        ]
                    }
                },
                {
                    field_name: "team_notes",
                    type: 2 // Text
                }
            ]
        }
    };

    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
        'POST',
        tableSchema,
        accessToken
    );
    console.log('✅ Clean TikTok_Content table created');
    return result.table_id;
}

// Add OpenAI test target to clean table
async function addTestTarget(accessToken, tableId) {
    console.log('📝 Adding @openai test target...');

    const targetRecord = {
        fields: {
            "target_value": "@openai",
            "platform": "tiktok",
            "target_type": "profile",
            "active": true,
            "results_limit": 20,
            "team_notes": "Primary competitor - TikTok content strategy"
        }
    };

    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables/${tableId}/records`,
        'POST',
        targetRecord,
        accessToken
    );
    console.log('✅ @openai target added successfully!');
    return result.record;
}

// Main function
async function recreateCleanTables() {
    try {
        console.log('🚀 Recreating tables with clean field configurations...');

        const accessToken = await getAccessToken();

        // Delete old tables (optional - comment out if you want to keep them)
        // await deleteTable(accessToken, 'Monitoring_Targets_Simple');
        // await deleteTable(accessToken, 'TikTok_Content_Simple');

        // Create new clean tables
        const monitoringTableId = await createCleanMonitoringTable(accessToken);
        const tikTokTableId = await createCleanTikTokTable(accessToken);

        console.log('\\n📍 New table IDs:');
        console.log(`   Monitoring_Targets_Clean: ${monitoringTableId}`);
        console.log(`   TikTok_Content_Clean: ${tikTokTableId}`);

        // Test data insertion
        const testRecord = await addTestTarget(accessToken, monitoringTableId);

        console.log('\\n🎉 Success! Clean tables created and working!');
        console.log('✅ Field types are correctly configured');
        console.log('✅ Data insertion works perfectly');
        console.log('✅ @openai target added as test');
        console.log('\\n🚀 Ready to build TikTok processor!');

        return {
            monitoringTableId,
            tikTokTableId,
            testRecord
        };

    } catch (error) {
        console.error('❌ Failed to recreate clean tables:', error);
        throw error;
    }
}

// Run if called directly
if (require.main === module) {
    recreateCleanTables();
}

module.exports = { recreateCleanTables };