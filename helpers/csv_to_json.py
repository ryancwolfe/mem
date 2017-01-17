'''
  The Facts.csv file was the old way of storing the data.
  (It was originally just maintained in a spreadsheet and exported 
    to the csv file.)

  This fast python script was used to migrate the data format
   over to json.
   
  Usage:
    > python csv_to_json.py

'''

import json, sys, csv

def csv2json( csv_path = 'facts.csv', json_path = 'facts.json' ):
  '''
   inputs: 
      csv_path:    path to the csv file which is read from
      json_path:   path to the json file which is written to
  '''
  
  # This will be dumped into the json file
  facts_array = []
  
  # Open the existing csv file
  with open(csv_path, 'rb') as csvfile:
  
    csv_contents = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    for i,fact in enumerate(csv_contents):
    
      # Skip the first (title) row
      if i==0:continue
      
      # Get the four elements of each fact
      fact = [field.strip() for field in fact[:4]]
      
      facts_array.append(fact)
  
  # Dump the facts to the json file
  with open(json_path, 'wb') as f:

    # write JSON to file; note the ensure_ascii parameter
    json.dump(facts_array, f, indent = 2, ensure_ascii = True)

# Entry point
csv2json()