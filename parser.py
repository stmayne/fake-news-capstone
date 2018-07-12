import tldextract as tlde
import sys
import json
import boto3
import requests

#function to extract domain name (ex. www.nytimes.com -> nytimes.com)
#returns list with domain name as string
#suffix parameter true if you want the list to include the suffix
def parseUrl(url, suffix=False):
    extracted = tlde.extract(url)
    domain = [extracted.domain + '.' + extracted.suffix]
    if suffix:
        domain.append(extracted.suffix)

    return domain

#function to pull data from bs detector dataset stored in S3
#takes a domain name and checks the database for a match and returns dict as one-hot vector
def getBsType(domain):
    #pulling from s3
    s3 = boto3.resource('s3')
    object = s3.Object('fakenewstest','bs.json')

    data = json.load(object.get()['Body'])
    type_dict = {'bias':0, 'bias ':0, 'fake':0, 'conspiracy':0, 'unreliable':0, 'rumor':0, 'satire':0,'satirical':0, 'clickbait':0, 'political':0, 'credible':0, 'unknown':0, 'junkscience':0, 'junksci':0, 'hate':0}
    #set type to 1 if found in bs data
    try:
        domain_data = data[domain]
        types = [domain_data['type'], domain_data['2nd type'], domain_data['3rd type']]
        for type in types:
            if type in type_dict:
                type_dict[type] = 1
    except:
        print('failed to find domain in bs')

    #cleaning up data
    if type_dict['bias '] == 1:
        type_dict['bias'] = 1
    if type_dict['junkscience'] == 1:
        type_dict['junksci'] = 1
    type_dict.pop('bias ')
    type_dict.pop('junkscience')

    return type_dict

#find all types in bs dataset
def findBSTypes():
    s3 = boto3.resource('s3')
    object = s3.Object('fakenewstest','bs.json')
    data = json.load(object.get()['Body'])
    type_dict = {}

    for domain in data:
        for type in data[domain]:
            if type == 'Source Notes (things to know?)':
                break
            type_dict[data[domain][type]] = 1

    print(type_dict)
#function to get data from the webhose.io apitoken
#currently takes domain name and returns domain rank, lots of other options available
def getWebHoseData(domain):
    #must include your api token here
    #TODO apitoken =  <Put API token here>

    #how many threads you want back, currently only doing site level params so only need one thread
    sizeofresponse = '1'
    try:
        requeststring = 'http://webhose.io/filterWebContent?token=%s&size=%s&format=json&q=site:%s' % (apitoken, sizeofresponse, domain)
    except:
        print('Exception occured when requesting from webhose.io, check domain name')
        return '0'
    #get json from webhose.io api
    try:
        response = requests.get(requeststring)
        data = response.json()
        #webhose.io returns a dictionary of lists of dictionaries
        return data['posts'][0]['thread']['domain_rank']
    except:
        print('Exception occured when parsing data, check domain name')
        return '0'


if __name__ == "__main__":
    #domain = parseUrl(str(sys.argv[1]))
    #bstype = getBsType(domain)
    #domain = parseUrl('https://www.nytimes.com/2018/07/02/nyregion/michael-cohen-trump.html?rref=collection%2Fsectioncollection%2Fpolitics&action=click&contentCollection=politics&region=stream&module=stream_unit&version=latest&contentPlacement=2&pgtype=sectionfront')
    #print(bstype)
    print(getBsType('dcclothesline.com'))
    #print(getWebHoseData('cnn.com'))
