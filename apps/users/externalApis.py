import requests
import json
from django.conf import settings

def status_transaction(id_transaction):

	if settings.WOMPI_DEBUG == False:
		url = 'https://production.wompi.co/v1/transactions/'+id_transaction
		authorization = "Bearer pub_prod_Vlm7zuJTqCvBkhezWQZhGr8mhbVcKonm"
	else:
		url = 'https://sandbox.wompi.co/v1/transactions/'+id_transaction
		authorization = "Bearer pub_test_3nY5Jqlp0rLB99qB2BcWrCwsyf721Wp6"
	headers = {
		"authorization": authorization,
		"Content-Type": "application/json"
	}
	
	r = requests.get(url=url, headers=headers)
	return r