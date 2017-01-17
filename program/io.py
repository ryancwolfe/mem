import factMod
import sys, csv, os

def json2facts(json_path = 'facts.json'):
  '''
   input:  json_path is the path to the json file.
   
   output: array of Facts. (Each fact is an instance of the Fact
            class.)
  '''
  
  facts_array = []
  
  # Open the existing json file
  with open(json_path, 'rb') as jsonfile:
  
    json_contents = eval(json_path)
    
    for i, fact in enumerate(json_contents):
    
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
      

class Population_Frequencies():
  '''
    Program interface to the frequencies.json file.
  
  '''
  
  def __init__(self):
    '''
      Dependency is the 'frequencies.json' file.
      
      Contents of the file is a dictionary or tuple like:
              Dicionary:
                 {'Some question text': 200,
                  'Some other text': 175}
              Tuple array:
                 [('Some question text', 200),
                  ('Some other text', 175)]
    '''
    
    # If the file exists
    if os.access('frequencies.json', os.R_OK):
      
      # Load it as the baseline
      self.allQuestion2frequency=eval(open("frequencies.json").read())

    else:
    
      ans=raw_input ( """
       It appears that the local database either hasn't been created or
       has been been corrupted.  Do you want to create a new local database?
       WARNING: This will erase the current database if it exists.
         Y - Create a new file:
         N - Abort
       > """)
       
      # Handle the "Abort" option
      if ans.lower().startswith('n'): raise ExceptionError('Aborting!')
      
      # Create a blank history record
      else: self.allQuestion2frequency={} 
    
  def __dict__(self):
    # Treat the instance as, basically, a dicionary
    return self.allQuestion2frequency
  
  def rescore(self,fact):
    '''
     Input: 
        fact
          is a Fact instance, which should have its question frequency set.
          
     Operation:
        Updates the dictionary to have the new value added here.
    '''
    self.allQuestion2frequency[str(fact.question)] = int(fact.question.frequency)
  
  def store(self):
    # Dump the dictionary to the json file
    with open('frequencies.json, 'wb') as f:

      # write JSON to file; note the ensure_ascii parameter
      json.dump(self.allQuestion2frequency, f, indent = 2, ensure_ascii = True)
  
  def update(self,fact):
    '''
      Sequence of the two main class operations
    '''
    self.rescore(fact)
    self.store()
      

facts = json2facts()


