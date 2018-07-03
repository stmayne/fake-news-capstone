import tldextract as tlde
import sys
import json
import boto3
import requests

def parseUrl(url, suffix=False):
    extracted = tlde.extract(url)
    domain = [extracted.domain + '.' + extracted.suffix]
    if suffix:
        domain.append(extracted.suffix)

    return domain


def getBsType(domain):
    s3 = boto3.resource('s3')
    object = s3.Object('fakenewstest','bs.json')

    data = json.load(object.get()['Body'])

    try:
        type = data[domain]['type']
    except:
        type = ""
    finally:
        return type

def getWebHoseData(domain):
    apitoken = '<Private API Token Here>'
    sizeofresponse = '1'
    requeststring = 'http://webhose.io/filterWebContent?token=%s&format=json&size=%s&q=site:%s' % (apitoken, sizeofresponse, domain)
    try:
        response = requests.get(requeststring)
        data = response.json()
    except:
        print('Exception occured when requesting from webhose.io, check domain name')
    finally:
        return data['posts'][0]['thread']['domain_rank']

if __name__ == "__main__":
    #domain = parseUrl(str(sys.argv[1]))
    #bstype = getBsType(domain)
    #domain = parseUrl('https://www.nytimes.com/2018/07/02/nyregion/michael-cohen-trump.html?rref=collection%2Fsectioncollection%2Fpolitics&action=click&contentCollection=politics&region=stream&module=stream_unit&version=latest&contentPlacement=2&pgtype=sectionfront')
    #print(bstype)
    print(getWebHoseData('nytimes.com'))
