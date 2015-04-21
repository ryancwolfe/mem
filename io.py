import factMod

def csv2facts():
  import sys, csv
  fname=r'C:\me\devos\mem\facts.csv'
  ret_val=[]
  with open(fname, 'rb') as csvfile:
    facts_file = csv.reader(csvfile, delimiter=',', quotechar='"')
    for i,fact in enumerate(facts_file):
      if i==0:continue
      fields = [field.strip() for field in fact[:4]]
      question,answer,category,category_to_ask=fields
      # Filter out unwanted rows
      if (not (category==category_to_ask)) or \
          question.startswith('#') or \
         (answer.lower()=='title'):
            continue # Filter out unwanted rows
      if question=='' or answer=='':continue
      ret_val.append(factMod.Fact(question,answer))
      
  return ret_val
      
      
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
