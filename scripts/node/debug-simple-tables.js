// Debug the simple table schemas
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

// Debug both simple tables
async function debugSimpleTables() {
    try {
        console.log('🔍 Debugging simple table schemas...');

        const accessToken = await getAccessToken();

        // Get all tables first
        const tablesResult = await makeLarkRequest(
            `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
            'GET',
            null,
            accessToken
        );

        console.log('📋 Available tables:', tablesResult.items.map(t => t.name));

        // Debug Monitoring_Targets_Simple
        const monitoringTableId = await getTableId(accessToken, 'Monitoring_Targets_Simple');
        console.log(`\n📊 MONITORING_TARGETS_SIMPLE (${monitoringTableId}):`);

        const monitoringFields = await getTableSchema(accessToken, monitoringTableId);
        monitoringFields.forEach((field, index) => {
            console.log(`${index + 1}. ${field.field_name}`);
            console.log(`   Type: ${field.type} (${getFieldTypeName(field.type)})`);
            console.log(`   Property:`, field.property);
            console.log('');
        });

        // Debug TikTok_Content_Simple
        const contentTableId = await getTableId(accessToken, 'TikTok_Content_Simple');
        console.log(`\n📱 TIKTOK_CONTENT_SIMPLE (${contentTableId}):`);

        const contentFields = await getTableSchema(accessToken, contentTableId);
        contentFields.forEach((field, index) => {
            console.log(`${index + 1}. ${field.field_name}`);
            console.log(`   Type: ${field.type} (${getFieldTypeName(field.type)})`);
            console.log(`   Property:`, field.property);
            console.log('');
        });

        return {
            monitoringFields,
            contentFields
        };

    } catch (error) {
        console.error('❌ Debug failed:', error);
        throw error;
    }
}

// Helper to get field type names
function getFieldTypeName(typeNumber) {
    const types = {
        1: 'Auto Number',
        2: 'Text',
        3: 'Single Select',
        4: 'Multi Select',
        5: 'Date/DateTime',
        7: 'Checkbox',
        11: 'Number',
        15: 'URL',
        18: 'Link to other table'
    };
    return types[typeNumber] || 'Unknown';
}

// Run if called directly
if (require.main === module) {
    debugSimpleTables();
}

module.exports = { debugSimpleTables };