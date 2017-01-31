var JDBC = require('jdbc');
var jinst = require('jdbc/lib/jinst');
var moment = require('moment');

// Initialize a the jdbc only once per JVM
if (!jinst.isJvmCreated()) {
    jinst.addOption("-Xrs");

    // Specify path to athena JDBC driver
    jinst.setupClasspath(['./AthenaJDBC41-1.0.0.jar']);
}

console.log(process.env['AWS_KEY'],process.env['AWS_SECRET'])

var config = {
    // Athena JDBC connection string incl. region name
    url: 'jdbc:awsathena://athena.us-east-1.amazonaws.com:443',
    drivername: 'com.amazonaws.athena.jdbc.AthenaDriver',
    properties: {
        // Athena staging S3 path
        "s3_staging_dir": "s3://srfrnk-doit/result/",
        //AWS Access Key
        "user": process.env['AWS_KEY'],
        //AWS Access Key Secret
        "password": process.env['AWS_SECRET']
    }
};

function getDailyTotals(date, callback) {
    var jdbc = new JDBC(config);

    // Connect to jdbc driver
    jdbc.initialize(function (err) {
        if (!!err) {
            callback(err, null);
        }
    });

    // Access a connection from the connection pool
    jdbc.reserve(function (err, connObj) {
        if (connObj) {
            var conn = connObj.conn;
            // Create the statement to execute over the connection
            conn.createStatement(function (err, statement) {
                if (!!err) {
                    callback(err, null);
                } else {
                    // Format the start and end date for the query
                    var startDate=moment(date).format('YYYY-MM-DD');
                    var endDate=moment(date).add(1,'d').format('YYYY-MM-DD');

                    // Execute the query to Athena
                    statement.executeQuery("select vendor_id as vendor,sum(total_amount) as total " +
                        "from (" +
                        "select date_trunc('day',from_unixtime(pickup_timestamp)) as pickup_date,*" +
                        "from srfrnk.yellow_trips_parquet limit 10000" +
                        ") " +
                        "where pickup_date between timestamp '"+startDate+"' and timestamp '"+endDate+"' "+
                        "group by vendor_id;",
                        function (err, resultset) {
                            if (!!err) {
                                callback(err, null);
                            } else {
                                // Convert result-set into an array for easier processing
                                resultset.toObjArray(function (err, results) {
                                    // Release the connection back to the pool
                                    jdbc.release(connObj, function (err) {
                                        if (!!err) {
                                            callback(err, null);
                                        }
                                        else {
                                            // Return the results array
                                            callback(null, results);
                                        }
                                    });
                                });
                            }
                        });
                }
            });
        }
    });
}

// Print today's totals at the console
getDailyTotals(new Date(2009,4,12), function (err, results) {
    if (!err) {
        console.log("Results: " + JSON.stringify(results));
    }
    else {
        console.error(err);
    }
});