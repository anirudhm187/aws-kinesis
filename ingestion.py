
import boto3
import json
import random
import json
import datetime
 
 
 
def generate_click_data():
    x = random.randint(1,5)
    x = x*50
    y = x+30
    data = {}
    data['user_id'] = random.randint(x,y)
    data['device_id'] = random.choice(['mobile','computer', 'tablet', 'mobile','computer'])
    data['client_event'] = random.choice(['beer_vitrine_nav','beer_checkout','beer_product_detail',
                                          'beer_products','beer_selection','beer_cart'])
    now = datetime.datetime.now()
    str_now = now.isoformat()
    data['client_timestamp'] = str_now
    return data
 
 
class KinesisSettings(object):
    def __init__(self):
        self.aws_access_key = "XXXXXXXXXXXXXXXXXXXXX"
        self.aws_secret_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.aws_region = "us-east-1"
        self.stream_name = "XXXXXXXXXXXXXXXXXXXXXX"
 
 
class KinesisFireHose(KinesisSettings):
 
    def __init__(self):
        KinesisSettings.__init__(self)
        self.client = boto3.client(
            "firehose",
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region,
        )
 
    def insert_item(self, json_data):
 
        response = self.client.put_record(
            DeliveryStreamName=self.stream_name,
            Record={
                'Data': bytes(
                    "{}\n".format(
                        json.dumps(
                            json_data
                        )
                    ).encode("UTF-8")
                ),
            }
        )
        print(response)
        return response
 
 
def main():
    for i in range(1, 30):
 
        json_data = generate_click_data()
        print(json_data)
        helper = KinesisFireHose()
        helper.insert_item(json_data=json_data)
 
main()
