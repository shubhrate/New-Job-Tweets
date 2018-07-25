import boto3
ssm = boto3.client('ssm')

def put_secret(name, value):
    res = ssm.put_parameter(Name=name, Value=value, Type="SecureString", Overwrite=True)
    if res:
        return 'success'
    else: 
        return 'fail'

def get_secret(name):
    res = ssm.get_parameter(Name=name, WithDecryption=True)
    return res['Parameter']['Value']
