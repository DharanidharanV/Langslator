import json
import boto3

s3 = boto3.client('s3')

translate = boto3.client('translate')

client = boto3.client('s3')

def lambda_handler(event, context):
    
    try:
        global SourceFileLanguage, TargetFileLanguage
        
        InputBucket = event['currentIntent']['slots']['InputBucket']
    
        Inputkey = event['currentIntent']['slots']['Inputkey']
    
        OutputBucket = event['currentIntent']['slots']['OutputBucket']
    
        OutputKey = event['currentIntent']['slots']['OutputKey']
    
        SourceFileLanguage = event['currentIntent']['slots']['SourceFileLanguage']
    
        TargetFileLanguage = event['currentIntent']['slots']['TargetFileLanguage']
        
        
        ################# Read the File From S3 Bucket #################
        
        file = readfilefroms3(InputBucket, Inputkey)
        
        data = file.decode("utf-8")
        
        ################# Split File into Small Paragraph and put in List #################
        
        listofdata = splittopara(data)
        
        TranslatedData = []              #List for Storing the TranslatedData
        
        ################# Language Translator #################
        
        for para in listofdata:
            if (para!=''):
                #print(para)
                Transtext = translator(para)
                TranslatedData.append(Transtext)
        
        #print('#### After TranslatedData ')
        
        #print('TranslatedData',TranslatedData)
        
        TransText=''                      #String for Storing the Translated Data
        
        for transpara in TranslatedData:
            TransText+=transpara+'\n'
            
        #print('TransText',TransText)
        
        ################# Write the Output to S3 Bucket #################
            
        writefiletos3(TransText, OutputBucket, OutputKey)
        
        #comment = 'Langslator Task Successfully Completed...! \n You can see the Translated Output \n Bucket :: '+Output_Bucket+',\n Key :: '+Output_Key+''
        
        response = {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Langslator Task Completed Successfully :). Please check the {output_file} in the {output_bucket} Bucket Location.".format(output_file=OutputKey,output_bucket=OutputBucket)
            },
        }
    }
        
        return response

    except Exception as e:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "SSML",
                    "content": "Exception Occured = {error}.".format(error=e)
                    
                },
                
            }
            
        }
        return response
        
#---------------------------------------------------------------------------------------
        
#----------------------------------------------------------
# Read the Input File From S3 Bucket
#----------------------------------------------------------
        
def readfilefroms3(InputBucket, Inputkey):
    try:
        response = s3.get_object(Bucket=InputBucket, Key=Inputkey)
        file = response['Body'].read()
        return file
    
    except Exception as e:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "SSML",
                    "content": "Exception Occured = {error}.".format(error=e)
                    
                },
                
            }
            
        }
        return response
#------------------------------------------------------------

#------------------------------------------------------------
# Split File into Small Paragraph and put in List
#------------------------------------------------------------
        
def splittopara(data):
    try:
                
        List=[]
        splat = data.split("\n")
        for paragraph in splat:
            List.append(paragraph)
            
        return List
        
    except Exception as e:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "SSML",
                    "content": "Exception Occured = {error}.".format(error=e)
                    
                },
                
            }
            
        }
        return response

#------------------------------------------------------------


#------------------------------------------------------------
# Language Translator
#------------------------------------------------------------    
    
def translator(file):
    try:
        
        result = translate.translate_text(Text=file,SourceLanguageCode=SourceFileLanguage,TargetLanguageCode=TargetFileLanguage)
        
        #print(f'TranslatedText: {result["TranslatedText"]}')
        #print(f'SourceLanguageCode: {result["SourceLanguageCode"]}')
        #print(f'TargetLanguageCode: {result["TargetLanguageCode"]}')
        
        return (result["TranslatedText"])
    
    except Exception as e:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "SSML",
                    "content": "Exception Occured = {error}.".format(error=e)
                    
                },
                
            }
            
        }
        return response
#------------------------------------------------------------


#------------------------------------------------------------
# Write the Output To S3 Bucket
#------------------------------------------------------------
    
def writefiletos3(TranslatedData, OutputBucket, OutputKey):
    try:
        
        client = boto3.client('s3')
        client.put_object(Body=TranslatedData, Bucket=OutputBucket, Key=OutputKey)
        
    except Exception as e:
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "SSML",
                    "content": "Exception Occured = {error}.".format(error=e)
                    
                },
                
            }
            
        }
        return response
#------------------------------------------------------------
