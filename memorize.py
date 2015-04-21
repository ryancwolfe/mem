
import time, random, re, bannerMod
from pprint import pformat
from io import facts,ioQuestion2frequency
from databaseMod import Database
from factMod import Population
from print_introduction import Introduction
# Add any new facts to the dictionary
#for fact in facts:
#  if fact.question not in ioQuestion2frequency: 
#    ioQuestion2frequency[question]=decrement_array[0]

database=Database(ioQuestion2frequency)

population=Population(facts)

# Class Instantiation
introduction=Introduction(facts)

def getAnInteger():
  # Crazy construction for in case the user doesn't type an integer.
  user_return = ''
  while not re.compile(r'\d+').match(user_return):
    user_return = raw_input('Please return an integer.\n  > ').strip()
  return int(user_return)

def getUserAnswer(fact):
    user_answer=raw_input('    > ').strip().lower()
    
    # For "set" answers, the order shouldn't matter.  So, sort the answers alphabetically
    if fact.question.lower().startswith('set:'):
      user_answer = ', '.join(sorted([x.strip() for x in user_answer.split(',')]))
      fact.answer = ', '.join(sorted([x.strip() for x in fact.answer.split(',')]))
    
    return user_answer

while 1:
  population.repopulate()
  i=random.randrange(len(population))
  fact=facts[population.value[i]]

  question,answer = fact.render()
  
  given_answer = ''
  while given_answer not in ['skip',answer,'giveup','skip','remove', 'rescore']:
  
    introduction._print(fact)
    answer,fact.question.frequency.low_watermark
    
    given_answer = getUserAnswer(fact)
    
    if given_answer.lower()=='skip':
      continue
    
    #
    # If they got the right answer, then decrease the frequency (aka "score")
    #  with which the question is asked.
    #
    if given_answer == correct_answer:
      fact.question.frequency.decrement()
      print_response.correct_answer()
    
    #
    # Handle a request to change the score/frequency of a given question
    #
    elif given_answer == 'rescore':
      print_response.rescore(answer,fact.question.frequency.low_watermark)
      fact.question.frequency.set_to(getAnInteger())
    
    #
    # Handle a request to give up and see the answer
    # (This also resets the score/frequency.)
    #
    elif given_answer == 'giveup':
      fact.question.frequency.reset()
      print_response.giveup(answer,fact.question.frequency.low_watermark)
    
    #
    # Allow the user to print out tallies if they want
    #  
    elif given_answer == 'tally':
      print_response.tally()
    
    elif given_answer == 'sorted tally':
      print_response.sorted_tally()
    
    #
    # Handle the wrong answers
    # 
    else: 
      fact.question.frequency.reset()
      print_response.wrong()

  database.update(fact)

