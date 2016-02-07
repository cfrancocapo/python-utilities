import time
import requests
import random
import hashlib
import argparse
import numpy

__author__="cfrancocapo"
 
apikey = "gfhpht2ffsfejd88g7pcnexe"
apisecret = "e7Af9xbEtm"
requests.packages.urllib3.disable_warnings()
parser = argparse.ArgumentParser()
parser.add_argument('--target', choices=['proxy', 'direct'], default='direct')
parser.add_argument('--total', type=int, default=4)
args = parser.parse_args()

def buildApiSignature():
    """Generate Signature from Api Key and Shared Secret"""
    authHash = hashlib.sha256();
    temp = str.encode(apikey + apisecret + repr(int(time.time())))
    authHash.update(temp)
    return authHash.hexdigest()

def buildHeaders():
	# build headers 	
	headers = {'Accept':'application/xml'}
	headers['Api-Key'] = apikey
	headers['X-Signature'] = buildApiSignature()
	headers['Content-Type'] = 'application/xml;charset=UTF-8'
	headers['Host'] = 'api.test.hotelbeds.com'
	return headers
	
if __name__ == "__main__":
	counter = args.total
	success = 0
	total_perf = 0	
	if args.target == 'direct':
		url = direct = "apps.test.hotelbeds.com"
	else:
		url = "api.test.hotelbeds.com"
	
	url = "https://" + url + "/hotel-api/1.0/hotels"
	print("target:", url)
	
	payload = '<availabilityRQ xmlns="http://www.hotelbeds.com/schemas/messages" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ><stay checkIn="2016-10-19" checkOut="2016-10-21"/><occupancies> <occupancy rooms="1" adults="1" children="0"/></occupancies><destination code="MCO"/><debug><provider>ACE</provider></debug></availabilityRQ>'
	total = []

	for x in range(1, counter + 1):
		myheaders=buildHeaders()		
		t_start = time.time()
		response = requests.post(url, data=payload, headers=myheaders, verify=False)
		perf_time = 0
		#print (response.request.body)
		if response.status_code == 200:
			success = success + 1
			perf_time = round((time.time() - t_start) * 1000)
			total.append(perf_time)
			total_perf = total_perf + perf_time
		else:
			print(perf_time = response.text)
		print(x, response.status_code, perf_time)
	avg_response = round(total_perf / success, 2)
	print(str(args.total) + " requests to " + url + " response times [s]:")
	print("  Avg   : " + str(avg_response))
	print("  Pct95 : " + str(numpy.percentile(total, 95)))
	print("  Median: " + str(numpy.percentile(total, 50)))
	