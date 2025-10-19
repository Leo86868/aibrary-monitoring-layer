// Check current Lark base setup
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

// Get table records
async function getTableRecords(accessToken, tableId) {
    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables/${tableId}/records`,
        'GET',
        null,
        accessToken
    );
    return result.items;
}

// Get table schema
async function getTableSchema(accessToken, tableId) {
    const result = await makeLarkRequest(
        `/open-apis/bitable/v1/apps/${BASE_ID}/tables/${tableId}/fields`,
        'GET',
        null,
        accessToken
    );
    return result.items;
}

// Check current setup
async function checkCurrentSetup() {
    try {
        console.log('🔍 Checking current Lark base setup...');

        const accessToken = await getAccessToken();

        // Get all tables first
        const tablesResult = await makeLarkRequest(
            `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
            'GET',
            null,
            accessToken
        );

        console.log('📋 Available tables:', tablesResult.items.map(t => t.name));

        // Check Monitoring_Targets table
        const monitoringTableId = await getTableId(accessToken, 'Monitoring_Targets');
        console.log(`\\n📊 MONITORING_TARGETS (${monitoringTableId}):`);

        const monitoringRecords = await getTableRecords(accessToken, monitoringTableId);
        console.log(`📝 Records found: ${monitoringRecords.length}`);

        if (monitoringRecords.length > 0) {
            monitoringRecords.forEach((record, index) => {
                console.log(`\\n${index + 1}. Record ${record.record_id}:`);
                Object.entries(record.fields).forEach(([key, value]) => {
                    console.log(`   ${key}: ${JSON.stringify(value)}`);
                });
            });
        }

        // Check TikTok_Content table
        const tikTokTableId = await getTableId(accessToken, 'TikTok_Content');
        console.log(`\\n📱 TIKTOK_CONTENT (${tikTokTableId}):`);

        const tikTokRecords = await getTableRecords(accessToken, tikTokTableId);
        console.log(`📝 Records found: ${tikTokRecords.length}`);

        // Verify @openai target setup
        const openaiTarget = monitoringRecords.find(r =>
            r.fields.target_value === '@openai' ||
            r.fields.target_value === 'openai'
        );

        if (openaiTarget) {
            console.log('\\n✅ @openai target found!');
            console.log('📋 Configuration:');
            console.log(`   target_value: ${openaiTarget.fields.target_value}`);
            console.log(`   platform: ${openaiTarget.fields.platform}`);
            console.log(`   target_type: ${openaiTarget.fields.target_type}`);
            console.log(`   active: ${openaiTarget.fields.active}`);
            console.log(`   results_limit: ${openaiTarget.fields.results_limit}`);
            console.log(`   team_notes: ${openaiTarget.fields.team_notes}`);

            // Validation
            let isValid = true;
            if (!openaiTarget.fields.target_value) {
                console.log('❌ Missing target_value');
                isValid = false;
            }
            if (!openaiTarget.fields.platform) {
                console.log('❌ Missing platform');
                isValid = false;
            }
            if (!openaiTarget.fields.target_type) {
                console.log('❌ Missing target_type');
                isValid = false;
            }
            if (openaiTarget.fields.active !== true) {
                console.log('❌ Target not active');
                isValid = false;
            }
            if (!openaiTarget.fields.results_limit || openaiTarget.fields.results_limit <= 0) {
                console.log('❌ Missing or invalid results_limit');
                isValid = false;
            }

            if (isValid) {
                console.log('\\n🎉 @openai target setup is PERFECT!');
                console.log('✅ All required fields configured');
                console.log('✅ Ready to build TikTok scraper');
                console.log('🚀 Can proceed with Apify integration');
            } else {
                console.log('\\n⚠️ @openai target needs fixes before proceeding');
            }
        } else {
            console.log('\\n❌ @openai target not found');
            console.log('Please add @openai target manually in Lark base');
        }

        return {
            tables: tablesResult.items,
            monitoringRecords,
            tikTokRecords,
            openaiTarget,
            isReady: !!openaiTarget
        };

    } catch (error) {
        console.error('❌ Setup check failed:', error);
        throw error;
    }
}

// Run if called directly
if (require.main === module) {
    checkCurrentSetup();
}

module.exports = { checkCurrentSetup };