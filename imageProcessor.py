import json
import boto3
import json
import requests

url_p = "https://vpc-photo-6r6is2fk5nvktuptrbsvyzmskq.us-east-1.es.amazonaws.com"
host = 'vpc-photo-6r6is2fk5nvktuptrbsvyzmskq.us-east-1.es.amazonaws.com' # For example, search-mydomain-id.us-west-1.es.amazonaws.com
index = 'photos/photo'
url = 'https://' + host + '/' + index + '/_search'
prefix = 'https://photosalbums.s3.amazonaws.com/'

def searcher_handler(name):
    ret = []
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    query = {
        "query":{
            # "match_all":{}
            "match":{
                "labels": name
            }
        }
    }

    # ES 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    print('before get')
    response = requests.get(url, headers=headers, data=json.dumps(query))
    # print(type(response))
    print(response)
    res = response.json()
    print(res)
    if 'status' in res.keys() and res['status'] == 404:
        print('404')
        return ret
    # print(type(res['hits']))
    # print(res)
    print("_________")
    # print(res['hits']['hits'])
    for xx in res['hits']['hits']:
        print(xx['_source']['objectKey'])
        print("***********")
        ret.append(xx['_source']['objectKey'])
    # id = 'testtestpng'
    # getResponse = requests.get(url_p+"/_search?q="+id)
    # print('after get')
    # print(getResponse.json())
    print('end')
    return ret
    # r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    # response = {
    #     "statusCode": 200,
    #     "headers": {
    #         "Access-Control-Allow-Origin": '*'
    #     },
    #     "isBase64Encoded": False
    # }

    # Add the search results to the response
    # response['body'] = r.text
    # return response

def lambda_handler(event, context):
    # TODO implement
    boto3.setup_default_session(region_name='us-east-1')
    client = boto3.client('lex-runtime')
    
    query = event['q']
    # query = event.split('=')[1]

    response = client.post_text(
        botName='imageSearch',
        inputText=query,
        userId='11',
        botAlias='parseBot'
    )
    print("response is:")
    print(response)

    
    # return {
    #     'statusCode': 200,
    #     # 'body': ans
    # }

    # print("111")
    # print(event)
    # # sessionAttributes = event["sessionAttributes"]
    
    if 'slots' not in response.keys():
        return {
            'status': '4xx',
            'results': []
        }
    slots = response['slots']
    search_obj = slots['object']
    
    # print(event)
    
    ret = searcher_handler(search_obj)
    
    print(ret)
    
    # attr_dic = {}
    # for i, xx in enumerate(ret):
    #     attr_dic[i] = prefix + xx
    
    res = []
    for xx in ret:
        dic = {}
        dic['url'] = prefix+xx
        dic['labels'] = [search_obj]
        res.append(dic)
    
    print(res)
    # headers = {
    #     "Access-Control-Allow-Origin": "*",
    #     "Access-Control-Allow-Credentials": True
    # }
    return {
        "results": res,
        'statusCode': 200
    }
    
    # return {
    #     "url": "hh"
    #     # "sessionAttributes": attr_dic,
    #     # "dialogAction": {
    #     #     "type": "Close",
    #     #     "fulfillmentState": "Fulfilled",
    #     #     "message": {
    #     #         "contentType": "PlainText",
    #     #         "content": "Okay, We will find {} from es".format(search_obj),
    #     #     }
    #     # }
    # }
