import json
def cleanUp():
    #sometimes, consecutive runs of Lambda doesn't clean up temp files & throws memory error
    import os
    import sys
    print("The dir is: %s" %os.listdir('/tmp/'))

    # listing directories after removing path
    print("The dir after removal of path : %s" %os.listdir('/tmp/'))

    print('Clearing up temp space.')
    import shutil
    os.chdir('/tmp/')
    listdirs  = os.listdir()   
    for dirname in listdirs:
        try:
            shutil.rmtree(dirname)
        except:
            os.remove(dirname) #prob a file, remove it
   
   
    os.chdir('..')
    print("The dir after removal of path : %s" %os.listdir('/tmp/'))
    return   


def grabLib(BUCKET_NAME = 'YOUR_BUCKET_HERE', # replace with your bucket name
                   KEY = 'YOUR_OBJECT_KEY_FOR_YOUR_CUSTOM_LIBRARY_HERE', # replace with your object key,
                  FILENAME ='PGF.py'):
    #function I wrote to mannually import into AWS Lambda's temp env from wherever in S3
    import boto3
    import botocore
    s3 = boto3.resource('s3')

    try:
        s3.Bucket(BUCKET_NAME).download_file(KEY, '/tmp/'+FILENAME)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print(FILENAME + "  cannot be found.")
        else:
            raise
       
def lambda_handler(event, context):
    cleanUp()
    #Grab Pythena Library (all in one python file)
    grabLib(KEY = 'YOUR_OBJECT_KEY_FOR_YOUR_CUSTOM_LIBRARY_HERE', # replace with your object key,
        FILENAME ='PGF.py')
       
    #GRAB REQUIRED FILES -- zipped non-supported python libraries
    grabLib(KEY = 'OBJECT_KEY_FOR_ZIP_PACKAGE_CONTAINING_LIBRARIES_YOURS_IS_DEPENDENT_ON.zip', # replace with your object key,
        FILENAME ='PRL.zip')
   

    import os
    import zipfile
    #We can only modify/downoad to in the /tmp/ folder -- that's fine
    path_to_zip_file = '/tmp/PRL.zip'
    directory_to_extract_to  = '/tmp/'
    zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
    zip_ref.extractall(directory_to_extract_to)
    zip_ref.close()
    print(os.path)

    #we can just add the tmp to our system envirnment
    import sys
    sys.path.append(os.path.abspath('/tmp'))
    import PGF
    # import test
    # test.main()
   
    #PUT IN PARAMATERS RIGHT HERE - AWS LAMBDA BENDS TO MY WILL MUAHAHAHA
    import PGF
    PGF.YOUR_FUNCTION_FROM_YOUR_LIBRARY_HERE()

    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }