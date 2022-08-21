#!/usr/bin/env python

#########################################################
### Script name: ExpirationDates.py
### Author: Adrián Payol Montero
### Department: WAF Telefónica
### Versión: 4.0
########################################################

import requests
import argparse
import warnings
import datetime
import json

#Credentials
IMPERVA_API_ID = "XXXX"
IMPERVA_API_KEY = "XXXXXXXXXXXXXXXXX"

IMPERVA_headers = {
	"x-API-key": IMPERVA_API_KEY,
	"x-API-id": IMPERVA_API_ID,
	"Content-Type" : "application/json"
}

#--------------------------------------------------------
print("Entity, Site, Custom Certificate, Expiration Date Custom Certificate, Scheduled Renewal Custom Certificate, Imperva Certificate, Status Imperva Certificate, Expiration Date GlobalSign Imperva Certificate, Host where TXT must be added, TXT Certificate Imperva, Expiration Date TXT")
parser = argparse.ArgumentParser()
parser.add_argument("--accountid", type=str, help="ID of the account in Imperva")
args = parser.parse_args()

def getAccountName (accountid):
	payload = ""
	url = "https://my.imperva.com/api/prov/v1/account?account_id=" + str(accountid)
	try:
		response = requests.post(url, headers=IMPERVA_headers, data=payload, verify=False)
		jsonresp = json.dumps(response.json())
		response_dict = json.loads(jsonresp)
		return response_dict["account"]["account_name"]
	except:
		print("API interaction error: GetAccountName" + str(response))

def getImpervaCertInfo (siteid):
	payload = ""
	url = "https://api.imperva.com/certificates/v3/certificates?extSiteId=" + str(siteid)

	try:
		response = requests.get(url, headers=IMPERVA_headers, data=payload, verify=False)
		jsonresp = json.dumps(response.json())
		response_dict = json.loads(jsonresp)

		if response_dict["data"]:
			#Esta llamada de API tiene doble valor en profundidad, por lo que los recorro con dos bucles (i,z de 0 a longitud de parámetros)
			for i in range(len(response_dict["data"])):
				for z in range(len(response_dict["data"][i]["sans"])):
					# Obtengo TODA LA INFO DEL IMPERVA CERT (según su estado guardo ciertos parámetros)
					if response_dict["data"][i]["sans"][z]["status"]=="PUBLISHED":
						impervaCert = "Active"
						impervaCertStatus = "Published"
						expDateImperva = response_dict["data"][i]["sans"][z]["expirationDate"]
						expDateImperva = datetime.datetime.fromtimestamp(int(expDateImperva / 1000)).strftime('%d/%m/%Y %H:%M:%S')
						hostTxt = response_dict["data"][0]["sans"][0]["approverFqdn"]
						txt = response_dict["data"][0]["sans"][0]["verificationCode"]
						txtDate = "-"
					elif response_dict["data"][i]["sans"][z]["status"]=="PENDING_USER_ACTION":
						impervaCert = "Active"
						impervaCertStatus = "TXT must be added in DNS"
						expDateImperva = "-"
						hostTxt = response_dict["data"][0]["sans"][0]["approverFqdn"]
						txt = response_dict["data"][0]["sans"][0]["verificationCode"]
						txtDate = "txtexpdate"
					else:
						#Estado de certificado de Imperva distinto de 'Published' y 'Pending_User_Action' (chequear manualmente)
						impervaCert = "Unknown"
						impervaCertStatus = "Unknown Imperva Status"
						expDateImperva = "-"
						hostTxt = "-"
						txt = "-"
						txtDate = "-"
				# Salida de función que imprimiré en la función ppal a continuación del resto de info (no imprimo aquí por formato)
				impervaCertInfo = impervaCert + "," + impervaCertStatus + "," + str(expDateImperva) + "," + hostTxt + "," + txt + "," + txtDate
				return impervaCertInfo
		else:
			# Sin ningún certificado (datos vacíos, salida None)
			impervaCert = "Not active"
			impervaCertStatus = "Not published"
			expDateImperva = "-"
			hostTxt = "-"
			txt = "-"
			txtDate = "-"
			impervaCertInfo = impervaCert + "," + impervaCertStatus + "," + str(expDateImperva) + "," + hostTxt + "," + txt + "," + txtDate
			return impervaCertInfo

	except:
		# Certificado de Imperva sin generar (s7 = not published)
		return str("Not Active,Not Published,-,-,-,-")

def listSitesforAccount (account_id):
	payload=""
	page_id=0
	count_item_per_page = 20
	finished_pagination = False

	while not finished_pagination:
		url = "https://my.imperva.com/api/prov/v1/sites/list?page_size=" + str(count_item_per_page) + "&page_num=" + str(page_id) + "&account_id=" + str(account_id)
		response = requests.post(url, headers=IMPERVA_headers, data=payload, verify=False)
		jsonresp = json.dumps(response.json())
		response_dict = json.loads(jsonresp)

		if response_dict["sites"] == []:
			finished_pagination = True
			break

		for i in range(len(response_dict["sites"])):
			try:
				# Obtengo Nombre_de_subcuenta (s1)
				accountName = getAccountName(response_dict["sites"][i]["account_id"])
				# Obtengo Nombre_de_dominio (s2)
				domainName = response_dict["sites"][i]["domain"]
				# Obtengo si existe certificado custom (s3) y dentro obtengo la fecha de caducidad (s4) y el campo vacío scheduledRenewal (s5) = TODA LA INFO DEL CUSTOM
				customIsActive = response_dict["sites"][i]['ssl']['custom_certificate']['active']
				if customIsActive:
					customCertStatus = "Activated"
					expDateCustom = response_dict["sites"][i]['ssl']['custom_certificate']['expirationDate']
					# Convierto de int a formato fecha
					expDateCustom = datetime.datetime.fromtimestamp(int(expDateCustom / 1000)).strftime('%d/%m/%Y %H:%M:%S')
					scheduledRenewal = "-"
				else:
					customCertStatus = "Not Activated"
					expDateCustom = "-"
					scheduledRenewal = "-"

				# Obtengo el Site_id para usarlo al llamar a getImpervaCertInfo
				site_id = response_dict["sites"][i]["site_id"]

				#Imprimo salida
				print(accountName + "," + domainName + "," + customCertStatus + "," + str(expDateCustom) + "," + scheduledRenewal + "," + str(getImpervaCertInfo(site_id)))

			except:
				print("Fallo con: " + str(site_id))
				pass

		page_id += 1

def main():
	warnings.filterwarnings("ignore")
	listSitesforAccount(args.accountid)

if __name__ == '__main__':
	main()