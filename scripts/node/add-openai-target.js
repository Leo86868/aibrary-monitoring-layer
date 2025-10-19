// Add @openai as first competitor monitoring target
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

// Get table ID by name
async function getTableId(accessToken, tableName) {
    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
        'GET',
        null,
        accessToken
    );

    const table = result.items.find(t => t.name === tableName);
    if (!table) {
        throw new Error(`Table ${tableName} not found`);
    }
    return table.table_id;
}

// Add OpenAI monitoring target
async function addOpenAITarget(accessToken, tableId) {
    console.log('📝 Adding @openai as competitor intelligence target...');

    const targetRecord = {
        fields: {
            "target_value": "@openai",
            "platform": "tiktok",
            "target_type": "profile",
            "active": true,
            "results_limit": 20,
            "team_notes": "Primary competitor - monitor their TikTok content strategy and engagement patterns"
        }
    };

    try {
        const result = await makeLarkRequest(
            `/open-apis/bitable/v1/apps/${BASE_ID}/tables/${tableId}/records`,
            'POST',
            targetRecord,
            accessToken
        );
        console.log('✅ @openai target added successfully!');
        console.log('📍 Record ID:', result.record.record_id);
        console.log('📊 Target details:');
        console.log('   Platform: TikTok');
        console.log('   Type: Competitor Intelligence (Profile)');
        console.log('   Target: @openai');
        console.log('   Limit: 20 posts per run');
        console.log('   Status: Active');

        return result.record;
    } catch (error) {
        throw error;
    }
}

// Main function
async function testOpenAITarget() {
    try {
        console.log('🎯 Adding first competitor monitoring target...');

        const accessToken = await getAccessToken();

        // Get monitoring table ID
        const monitoringTableId = await getTableId(accessToken, 'Monitoring_Targets_Simple');
        console.log(`📍 Monitoring_Targets_Simple table ID: ${monitoringTableId}`);

        // Add OpenAI target
        const targetRecord = await addOpenAITarget(accessToken, monitoringTableId);

        console.log('\n🎉 First target added successfully!');
        console.log('✅ Table functionality confirmed working');
        console.log('✅ Ready to build TikTok processor');
        console.log('✅ Your team can now see this target in Lark');

        console.log('\n📋 Next: Check your Lark Base to see the @openai target');
        console.log('🚀 Then we can build the TikTok scraping processor');

        return targetRecord;

    } catch (error) {
        console.error('❌ Failed to add OpenAI target:', error);
        throw error;
    }
}

// Run if called directly
if (require.main === module) {
    testOpenAITarget();
}

module.exports = { testOpenAITarget };