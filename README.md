# Creating_Item_Records
Creating item records in batch

Creating the item records in batch can save lots of time of technical services librarians. The Ex Libris API provided the convenience and capability to fulfill it.

Creating the item records involved creating the holding record first. It is impossible to create an item record without affiliating with any holding records. It means that when you desire to create an item record, the holding record either exists already or need to be created first.

This procedure is suitable to process the items creation in batch for the contributed books or gift books which you would like to put them into one library location. If you had the books for different locations, you either divided them to different groups then make use of the code to process them, or modify the code to add the capability putting the items into the different locations. Here, I merely talked about the situation to put all gift books into one location.

The PO line we used here is mega type PO Line (Print book –standing order) which is easy for affiliating thousands of items records directly, or attaching the PO line to each item precisely.

One of the prerequisites to run this code was that you already imported bib records from the OCLC Connexion into ALMA.

The flow chart of the code logic was as follows.



When using this code, please change the API key into the one your library employed, shown like below.



The PO line in the code should be changed to the one employed in your library, shown as follows. If you would like to change any attributes in the item data, please do it according to the corresponding XML tags.



In windows command processor, enter “python Main11.py” to run the code.



The first step, enter the location code by which you would like to create the holding record. The second step, add the item policy code for your item. The third step, click the “Locate the MMS ID file” button and select the text file containing the MMS IDs and barcodes.

The location code in your library should be obtained by clicking Fulfillment>Locations>Physical Locations



The item policy code in your library should be acquired by clicking Fulfillment>Physical Fulfillment>Item Policy.



The MMS ID text file format in 3r step is as follows. It is easy to create it by using notepad.



The code was written in Python and located in Github https://github.com/andytang2008/Creating_Item_Records

The running environment is in windows 10 and Python 3.8.6

I hope it helps.
