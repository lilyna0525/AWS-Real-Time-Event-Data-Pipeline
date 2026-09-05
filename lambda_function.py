import base64
import json
import os

import mysql.connector


def lambda_handler(event, context):
    db_config = {
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "host": os.environ["DB_HOST"],
        "database": os.environ["DB_NAME"],
    }

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    processed_count = 0

    try:
        for record in event["Records"]:
            record_data = base64.b64decode(
                record["kinesis"]["data"]
            ).decode("utf-8")

            data = json.loads(record_data)

            if data.get("user_type") == "new_user":
                insert_query = '''
                    INSERT INTO channel_marketing_tb
                    (
                        serviceType,
                        gtmLongTime,
                        base_dt,
                        channel_name,
                        conversion_name,
                        platform,
                        user_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''

                values = (
                    data.get("serviceType"),
                    data.get("gtmLongTime"),
                    data.get("base_dt"),
                    data.get("channel_name"),
                    data.get("conversion_name"),
                    data.get("platform"),
                    data.get("user_type"),
                )

                cursor.execute(insert_query, values)
                processed_count += 1

        connection.commit()

    finally:
        cursor.close()
        connection.close()

    return {
        "statusCode": 200,
        "body": json.dumps(
            f"Processed and saved {processed_count} records to MySQL"
        ),
    }
