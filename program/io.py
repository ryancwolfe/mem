import factMod
import sys, csv

def csv2facts(csv_path = 'facts.csv'):
  '''
   input:  csv_path is the path to the csv file.
   
   output: array of Facts. (Each fact is an instance of the Fact
            class.)
  '''
  
  facts_array = []
  
  # Open the existing csv file
  with open(csv_path, 'rb') as csvfile:
  
    csv_contents = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    for i, fact in enumerate(csv_contents):
    
      # Skip the first (title) row
      if i == 0: continue
      
      # Get the four elements of each fact
      fields = [field.strip() for field in fact[:4]]
      question, answer, field_3, field_4 = fields
      
      # Rules in filtering out unwanted rows:
      
      #  1. Fields 3 and 4 should match
      #     (This was invented as an easy / fast way of
      #      retaining questions but filtering them out)
      if field_3 != field_4: continue
      
      #  2. Questions must not start with "#"
      if question.startswith('#'): continue
      
      #  3. Must have at least a question and an answer
      if question == '' or answer == '':continue
  
      facts_array.append(factMod.Fact(question, answer))
      
  return facts_array
      
      
def loadQuestion2Frequency():
  import os
  if os.access("db\\question2frequency.localdatabase", os.R_OK): # If the file exists
    question2frequency=eval(open("db\\question2frequency.localdatabase").read()) # Load the "history" variable from it
  else:
    ans=raw_input= """
     It appears that the local database either hasn't been created or
     has been been corrupted.  Do you want to create a new local database?
     WARNING: This will erase the current database if it exists.
       Y - Create a new file:
       N - Abort
     > """
    if ans.lower().startswith('n'): raise ExceptionError('Aborting!')
    else: question2frequency={} # Create a blank history record
  return question2frequency

facts = csv2facts()

ioQuestion2frequency = loadQuestion2Frequency()
