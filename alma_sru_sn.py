'''
This script searches a list of ISBNs in Alma's standard number index via SRU, 
and generates an output files of found ISBNs with MMS IDs.
'''

import csv
from csv import reader
import requests
import pandas as pd
import re

def sn_sru(fname):


	'''
	Searches a list of ISBNs in Alma's standard number index via SRU. Writes .pkl and .csv files of found ISBNs with Alma MMS IDs.	Returns two counts: number of ISBNs searched, 
	and number of ISBNs found. Required input: txt or csv file of values to be searched.
	'''

	count = 0
	found_count = 0
	
	with open(fname) as infile:
		
		if str(fname).endswith('.csv'):
			isbns = csv.reader(infile, delimiter=' ', quotechar='|')
		elif str(fname).endswith('.txt'):
			isbns = infile.read().split('\n')
		else:
			print('Error: Input file must be .csv or .txt. Quitting.')
			quit()

		foundlist = {}
		foundfile = open("isbns_found.txt", "w+")
		results = []
		count = 0

		for isbn in isbns:
	
			isbn = str(isbn).strip("['']")
		
			#insert your Alma SRU base URL here
			search_url = f'https://xxxx.alma.exlibrisgroup.com/view/sru/XXXXXX?version=1.2&operation=searchRetrieve&recordSchema=marcxml&query=alma.standard_number={isbn} and alma.mms_tagSuppressed=false'
			query_isbn = requests.get(search_url)

			record = query_isbn.text
		
			found_re = re.compile(r'.*<numberOfRecords>[1-9]<.*')
			found = found_re.search(record)
		
			mmsid_re = 'tag="001">(.*?)<'
		
			if found:
		
				print('found')
				mmsids = re.findall(mmsid_re, record)
				print(mmsids)
				for mmsid in mmsids:
					foundlist[mmsid] = isbn
					found_count += 1
			
					df_result = pd.DataFrame(data={'MMSID': [mmsid], 'ISBN': [isbn]})
					results.append(df_result)
			else:
				print('not found')
				df_result = pd.DataFrame(data={'MMSID': 'none', 'ISBN': [isbn]})
			
			results.append(df_result)
			count += 1
			if count % 10 == 0:
				print(count)
				
			df_partial = pd.concat(results)
			df_partial.to_pickle('isbns_found_partial.pkl')
	
		df_results = pd.concat(results)
		df_results.to_pickle('isbns_found_all.pkl')
		df_results.to_csv('isbns_found_all.csv')

	return count, found_count

def main():


	'''
	Gets user input for txt or csv filename, calls 
	sn_sru(), prints found and not found counts to the console.
	'''

	isbn_file = input("Enter filename: ")
	count, found_count = sn_sru(isbn_file)
	print (count, "ISBNs queried")
	print (found_count, "ISBNs found")
	print ("Queries complete.")

if __name__ == '__main__':
	main()