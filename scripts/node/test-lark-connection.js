// Test Lark API Connection
// Quick test to verify credentials and base access

const https = require('https');

// Your Lark credentials
const APP_ID = 'cli_a860785f5078100d';
const APP_SECRET = 'sfH5BBpCd6tTeqfPB1FRlhV3JQ6M723A';
const BASE_ID = 'Qr40bFHf8aKpBosZjXbcjF4rnXe';

// Step 1: Get access token
function getAccessToken() {
    return new Promise((resolve, reject) => {
        const postData = JSON.stringify({
            app_id: APP_ID,
            app_secret: APP_SECRET
        });

        const options = {
            hostname: 'open.larksuite.com',
            port: 443,
            path: '/open-apis/auth/v3/app_access_token/internal',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                const response = JSON.parse(data);
                if (response.code === 0) {
                    console.log('✅ Successfully obtained access token');
                    resolve(response.app_access_token);
                } else {
                    console.error('❌ Failed to get access token:', response);
                    reject(response);
                }
            });
        });

        req.on('error', (e) => {
            console.error('❌ Request error:', e);
            reject(e);
        });

        req.write(postData);
        req.end();
    });
}

// Step 2: Test base access
function testBaseAccess(accessToken) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'open.larksuite.com',
            port: 443,
            path: `/open-apis/bitable/v1/apps/${BASE_ID}/tables`,
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                const response = JSON.parse(data);
                if (response.code === 0) {
                    console.log('✅ Successfully accessed base');
                    console.log('📊 Existing tables:', response.data.items.map(t => t.name));
                    resolve(response.data.items);
                } else {
                    console.error('❌ Failed to access base:', response);
                    reject(response);
                }
            });
        });

        req.on('error', (e) => {
            console.error('❌ Request error:', e);
            reject(e);
        });

        req.end();
    });
}

// Run the test
async function runTest() {
    try {
        console.log('🔍 Testing Lark API connection...');
        console.log(`📍 Base ID: ${BASE_ID}`);

        const accessToken = await getAccessToken();
        const tables = await testBaseAccess(accessToken);

        console.log('\n🎉 Connection test successful!');
        console.log('✅ Ready to create tables');

        return { accessToken, tables };
    } catch (error) {
        console.error('\n❌ Connection test failed:', error);
        throw error;
    }
}

// Export for use in other scripts
module.exports = { getAccessToken, testBaseAccess, APP_ID, APP_SECRET, BASE_ID };

// Run test if called directly
if (require.main === module) {
    runTest();
}