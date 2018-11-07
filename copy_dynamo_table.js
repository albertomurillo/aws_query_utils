var copy = require('copy-dynamodb-table').copy

var globalAWSConfig = { // AWS Configuration object http://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/Config.html#constructor-property
    accessKeyId: 'AKID',
    secretAccessKey: 'SECRET',
    region: 'us-east-1'
}

var sourceAWSConfig = {
    accessKeyId: 'AKID',
    secretAccessKey: 'SECRET',
    region: 'us-east-1'
}

var destinationAWSConfig = {
    accessKeyId: 'AKID',
    secretAccessKey: 'SECRET',
    region: 'us-east-1' // support cross zone copying
}

copy({
    config: globalAWSConfig,
    source: {
        tableName: 'TABLE_NAME', // required
        config: sourceAWSConfig // optional , leave blank to use globalAWSConfig
    },
    destination: {
        tableName: 'TABLE_NAME', // required
        config: destinationAWSConfig // optional , leave blank to use globalAWSConfig
    },
    log: true,// default false
    create: true // create destination table if not exist
},
    function (err, result) {
        if (err) {
            console.log(err)
        }
        console.log(result)
    })
