import pandas as pd
import boto3
import json
import os
import configparser
from botocore.exceptions import ClientError
import psycopg2



class S3_file_retriever :
    
    def __init__(self, config_file, bucket_name, aws_region_name):
        self.config_file = config_file
        config = configparser.ConfigParser()
        config.read_file(open(self.config_file))
        self.KEY=config.get('AWS','KEY')
        self.SECRET= config.get('AWS','SECRET')
        
        self.bucket_name = bucket_name
        self.aws_region_name = aws_region_name
    

    def get_file_names_in_S3(self, prefix) :
        s3 = boto3.resource(
            's3',
            region_name=self.aws_region_name,
            aws_access_key_id=self.KEY,
            aws_secret_access_key=self.SECRET
        )

        sampleDbBucket =  s3.Bucket(self.bucket_name)

        file_names = []

        for obj in sampleDbBucket.objects.filter(Prefix=prefix):
            file_names.append(obj)

        return file_names
    


    def download_file_from_S3(self, file_name_to_create, file_path) :
        s3 = boto3.client(    
            's3',
            region_name=self.aws_region_name,
            aws_access_key_id=self.KEY,
            aws_secret_access_key=self.SECRET
        )

        with open(file_name_to_create, 'wb') as f:
            s3.download_fileobj(self.bucket_name, file_path, f)
        
    
    
if __name__ == "__main__" :
    
    config_file = 'dwh.cfg'
    
    bucket_name = "udacity-labs"
    aws_region_name = "us-west-2"
    S3_f_r = S3_file_retriever(config_file, bucket_name, aws_region_name)    
    prefix = "tickets"
    file_names_in_S3 = S3_f_r.get_file_names_in_S3(prefix)
    print(file_names_in_S3)
    
    
    bucket_name = 'udacity-dend'
    file_path = 'log_data/2018/11/2018-11-01-events.json'
    file_name_to_create = 'log_data_file'
    S3_f_r = S3_file_retriever(config_file, bucket_name, aws_region_name) 
    S3_f_r.download_file_from_S3(file_name_to_create, file_path) 
    
    file_path = 'song_data/A/A/A/TRAAAAK128F9318786.json'
    file_name_to_create = 'song_data_file'
    S3_f_r.download_file_from_S3(file_name_to_create, file_path) 