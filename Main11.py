#######################################################
#  Creating the item records by using Ex Libris item API
#   Andy Tang 03/2023
#######################################################
import requests
import xml.etree.ElementTree as ET
from tkinter import *
#it will open a file open box
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
#This code successfully detects whether the bibs had the holding with location already existed. If not, create holdings records. 
#gui = tk.Tk(className='Python Examples - Window Size')
# set window size
#gui.geometry("500x200")
top = tk.Tk()
top.geometry("500x200")
L1 = Label(top, text="Location code:")
L1.place(x = 35,y = 30)

E1 = Entry(top, bd =5)
E1.place(x = 155,y = 30)


IP = Label(top, text="Item policy code:")
IP.place(x = 35,y = 70)
E2 = Entry(top, bd =5)
E2.place(x = 155,y = 70)

global location
global itemPolicy
global apiKey
apiKey='Put your library API key here'

def locateFile():
	#messagebox.showinfo( "Hello Python", "Hello World")
	top.file_path = filedialog.askopenfilename()
	print(top.file_path)
	#location=E1.get()
	#print(location)
	#print(E1.get())
	
	top.location=E1.get()
	top.itemPolicy=E2.get()
	print(top.location)
	print(top.itemPolicy)
	top.destroy()

	

B = tk.Button(top, text ="Locate the MMS ID file!", command = locateFile)
E = tk.Button(top, text="Quit", command=top.destroy)  #.pack() is commented at the end of this line.
B.place(x = 35,y = 110)
E.place(x = 260,y = 110)

#print(top.location)
#print(E1.get())
top.mainloop()

mms_ID_File=top.file_path
locationCode=top.location
IP_Code=top.itemPolicy
print(mms_ID_File);
print(locationCode);
print(IP_Code);   #added by andy 03-2023

global callNumberLostList
callNumberLostList=[]

#B.pack()

def api_createHoldings(mms_id):
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	data = ' <holding> <suppress_from_publishing>false</suppress_from_publishing> <record> <leader>     nx  a22     1n 4500</leader> <controlfield tag="008">1011252u    8   4001uueng0000000</controlfield> <datafield ind1="0" ind2=" " tag="852"> <subfield code="b">UNLVLAW</subfield> <subfield code="i"></subfield> <subfield code="c">nnve</subfield> <subfield code="h"></subfield> </datafield> </record> </holding>'
	mms_ID=mms_id
	response = requests.post('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mms_ID+'/holdings?apikey='+apiKey, headers=headers, data=data)
	print(response.content)
	myroot = ET.fromstring(response.text)
	print('myroot in api_createHoldings:'+myroot.tag)
	
	holdingId = myroot.find('holding_id').text
	print("holding_id value:"+holdingId)
	return holdingId


			
def api_getHoldings(mms_id):
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	mms_ID=mms_id
	response = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mms_ID+'/holdings?apikey='+apiKey, headers=headers)
	print(response.content)
	
	myroot = ET.fromstring(response.text)
	#print(myroot)
	print(myroot.tag)
	i=0
	for x in myroot.findall('holding'):  #if there is no holding at all, all code in for cycle will not run.
		i=i+1
		holdingId = x.find("holding_id").text
		locationValue =x.find('location').text
		#callNumver=x.find('call_number').text
		print('xxxxlocationValue:   '+locationValue)
		print('xxxxholdingId:   '+holdingId)
		print(i)
		if x.find('call_number') is None:#21Instead of checking if x.find('call_number').text is not None, you should make sure that x.find('call_number') is not None first.
			callNumberLostList.append(mms_id)  #call number didn't exist, this record mms id is saved into callNumberLostList
		if locationValue==locationCode:
			return locationValue,holdingId
	return '',''

def api_createItem(mmsID, holdingID, data):
	headers = {
		'accept': 'application/xml',
		'Content-Type': 'application/xml',
	}
	response = requests.post('https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs/'+mmsID+'/holdings/'+holdingID+'/items?generate_description=false&apikey='+apiKey, headers=headers, data=data)
	print(response.content)
	print('**********The item was created!***********')

	print('')
def createItem(mmsID, holdingID, barcode, item_policy): ##IP_Code/item_policy is the item policy from the box value in gui
		
	print('')   
#Gift books pol 4879. 
	data='<item link=\"string\"><holding_data link=\"string\"><holding_id>'+holdingID+'</holding_id><copy_id>1</copy_id><in_temp_location>false</in_temp_location><temp_library><xml_value></xml_value></temp_library><temp_location><xml_value></xml_value></temp_location><temp_call_number_type><xml_value>0</xml_value></temp_call_number_type><temp_call_number></temp_call_number><temp_call_number_source></temp_call_number_source><temp_policy><xml_value>0</xml_value></temp_policy></holding_data><item_data><barcode>'+barcode+'</barcode><physical_material_type><xml_value>BOOK</xml_value></physical_material_type><policy><xml_value>'+item_policy+'</xml_value></policy><provenance><xml_value></xml_value></provenance><po_line>POL-4879</po_line><is_magnetic>false</is_magnetic><arrival_date>2022-08-01Z</arrival_date><year_of_issue></year_of_issue><enumeration_a></enumeration_a><enumeration_b></enumeration_b><enumeration_c></enumeration_c><enumeration_d></enumeration_d><enumeration_e></enumeration_e><enumeration_f></enumeration_f><enumeration_g></enumeration_g><enumeration_h></enumeration_h><chronology_i></chronology_i><chronology_j></chronology_j><chronology_k></chronology_k><chronology_l></chronology_l><chronology_m></chronology_m><break_indicator><xml_value>G</xml_value></break_indicator><pattern_type><xml_value></xml_value></pattern_type><linking_number>1</linking_number><description></description><replacement_cost></replacement_cost><receiving_operator></receiving_operator><inventory_number></inventory_number><inventory_price></inventory_price><receive_number></receive_number><weeding_number></weeding_number><alternative_call_number></alternative_call_number><alternative_call_number_type><xml_value>0</xml_value></alternative_call_number_type><alt_number_source></alt_number_source><storage_location_id></storage_location_id><pages></pages><pieces></pieces><public_note></public_note><fulfillment_note></fulfillment_note><internal_note_1></internal_note_1><internal_note_2></internal_note_2><internal_note_3></internal_note_3><statistics_note_1></statistics_note_1><statistics_note_2></statistics_note_2><statistics_note_3></statistics_note_3><physical_condition><xml_value></xml_value></physical_condition><committed_to_retain><xml_value>false</xml_value></committed_to_retain><retention_reason><xml_value></xml_value></retention_reason><retention_note></retention_note></item_data></item>'
	api_createItem(mmsID, holdingID, data)

#f = open("mms_id_books.txt", "r")
f = open(mms_ID_File, "r")

lines = f.read().splitlines() # lines is an array, each element in array contains the format like 991008836536904082|31166002949495
#barcode='31166002949495'


for x in lines:
	if len(x)>1:  # avoid the empty element such as CR in lines.
		mmsID,barcode = x.split('|') # x is the each element in lines array
		print ("mmsID:"+mmsID)
		print ("barcode:"+barcode)
		location, holdingId=api_getHoldings(mmsID)
		print ("location + holding id:")
		print ('location :'+location)
		print ('holding id:'+holdingId)
		if location==locationCode:
			print('')
		else:
			holdingId=api_createHoldings(mmsID)
			location, holdingId=api_getHoldings(mmsID)

		print ("location + holding id:")
		print ('location :'+location)
		print ('holding id:'+holdingId)
		print ('mmsID id:'+mmsID)
		print ('barcode id:'+barcode)
		createItem(mmsID, holdingId, barcode,IP_Code);  #IP_Code is the item policy from the box value in gui
		
f = open("The_records_with_lost_call_number.txt", "a")  # If there are some bib records not having call number in 050 and 090 field, output the mmsID of those records into a file named The_records_with_lost_call_number.txt
print('The records with lost call number:',file=f)
for p in callNumberLostList: 
	print (p,file=f)
f.close()
