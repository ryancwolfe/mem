# To do list:
#  - Back it up by 3
#  - When it is under a certain score:
#     - Move the "blanks" function into a separate "def" statement.
#     - Have it be run until the "blanks" occur only 1 in every 7 words.  Or have the x in "1 in every x words" grow with the score.
#     - Maybe also have the blanks frequency increase
#     - Actually, just having the blanks frequency increase may be the best way...  May not need to have both
#
#  - Print out the estimated number of answers needed to get back to 50%.  (Calculate by using random?)
#
#  - Print the number of questions answered in the last 5 minutes.
#

#Change the numbers below to control the relative frequency of the numbers
decrement_array = map(int, \
 '''
200
175
150
120
110
100 
 90 
 80 
 70 
 60 
 50
 40
 30
 20
 10
  5
  3
  2
  1
    
 '''.split())

def nBlanksMap(score):
  if (score>119): return 3.5
  if (score>109): return 3 
  if (score> 99): return 2.5
  if (score> 89): return 2.2
  if (score> 79): return 1.7
  if (score> 69): return 1.5
  if (score> 59): return 1.4
  return 1.3
 
def getDecrement(decrement_array):
  decrement_array = list(reversed(sorted(list(set(decrement_array)))))
  decrement = {}
  for i,d in enumerate(decrement_array):
    if len(decrement_array) == i+1: decrement[d] = d
    else: decrement[d] = decrement_array[i+1]
  return decrement

decrement = getDecrement(decrement_array)

MAX_NUMBER = decrement_array[0]
last_frequency = MAX_NUMBER
import time, random, os, csv, sys, re
from pprint import pformat
fname=sys.argv[1]

facts=[]
with open(fname, 'rb') as csvfile:
   facts_file = csv.reader(csvfile, delimiter=',', quotechar='"')
   first_yet=False
   for fact in facts_file:
     if not first_yet:
       first_yet = True
       continue
     if (''.join(fact)).strip() == '': continue # skip it if it's a blank row
     if not (fact[2]==fact[3]):  continue #this field determines whether or not it should be asked...
     if fact[0].startswith('#'): continue #this also determines whether or not it should be asked...
     if fact[1].lower()=='title': continue #this also determines whether or not it should be asked.
     facts.append([fact[0].strip(),fact[1].strip().lower(),fact[4].strip()])

if os.access("localdb", os.R_OK):  execfile('localdb')
else: history={}

def getFactArray(facts,history):
  fact_array=[]
  for fact in facts:
    question,correct_answer,query = fact
    if question not in history: history[question]=decrement_array[0]
    for null in range(history[question]): fact_array.append(fact)
  return fact_array

fact_array = getFactArray(facts,history)
all_questions=[x[0] for x in facts]
questions2answers=dict([(x[0],x[1]) for x in facts])
while 1:
  i=random.randrange(len(fact_array))
  
  question,correct_answer,query = fact_array[i]
  original_question = question
  
  #-----------------------------------------------------------------------------
  # Handle the "Pick 3"s
  #-----------------------------------------------------------------------------
  if question.lower().startswith('pick3:'):
    question = question.split()[1:]
    iLocal = random.randrange(len(question)-2)
    while (question[iLocal]).startswith('~'): iLocal = random.randrange(len(question)-2)
    question = 'Reference: "'+question[iLocal]+' '+question[iLocal+1]+' '+question[iLocal+2]+'"'
    question = question.replace('~','')
  
  
  #-----------------------------------------------------------------------------
  # Handle the "fill in the blank questions"
  #-----------------------------------------------------------------------------

  if correct_answer.lower() in ['list','blanks']:
  
    prev_correct_answer = str(correct_answer)
    
    question = question.split()
    title=''
    if question[0].endswith(':'):
      title=question[0]+' '
      question=question[1:]
    
    score=history[original_question]
    how_many_blanks=int(round(float(len(question))/nBlanksMap(score)))
    listOfListIndexes=[]
    for null in range(how_many_blanks):
      iList=random.choice(range(len(question)))
      while iList in listOfListIndexes: iList=random.choice(range(len(question)))
      listOfListIndexes.append(iList)
    listOfListIndexes=sorted(listOfListIndexes)
    
    
    #Get correct answer
    characters='''  .;,:"'!?-()  ''' #'
    wordsInCorrectAnswer=[]
    for iList in listOfListIndexes:
      correct_word=question[iList]
      while correct_word[-1] in characters:
        correct_word = correct_word[:-1]
      while correct_word[0] in characters:
        correct_word = correct_word[1:]
      wordsInCorrectAnswer.append(correct_word)
    correct_answer = (', '.join(wordsInCorrectAnswer)).lower()
    
    #-------------
    # Get question
    #-------------
    # (A) Apply blanks and characters to all blank words
    newQuestion=[]
    for i,word in enumerate(question):
      new_word=str(word)
      if i in listOfListIndexes:
        new_word='____'
        if word[-1] in characters:
          if word[-2] in characters:
            new_word+=word[-2]
          new_word+=word[-1]
        if word[0] in characters:
          if word[1] in characters:
            new_word=word[1]+new_word
          new_word=word[0]+new_word
      newQuestion.append(new_word)
    #--------------------------
    # (B) Handle double blanks
    if prev_correct_answer.lower() == 'blanks':
      # (B.1) apply first character to subsequent blanks
      for i,word in enumerate(newQuestion):
        if '_' in word:
          new_i = int(i) + 1
          while new_i in range(len(newQuestion)):
            if '_' not in newQuestion[new_i]: break
            newQuestion[new_i] = word[0] + newQuestion[new_i][1:]
            new_i+=1
      # (B.2) replace blanks sequences with just the last blank
      local_f = lambda i,listOfListIndexes: (i in listOfListIndexes and i+1 not in listOfListIndexes) or (i not in listOfListIndexes)
      newQuestion = [word for i,word in enumerate(newQuestion) if local_f(i,listOfListIndexes)]
    #---------
    # (C) Turn into string
    question=title+' '.join(newQuestion)
  
  if correct_answer.lower() == 'persons':
    pass
  
  
  given_answer = ''
  while given_answer not in [correct_answer,'giveup','skip','remove', 'rescore']:

    
    
    print '\n'*50
    print '''
    
  o---------------------------------------------------------------------------o
  | M E M O R I Z E
  o---------------------------------------------------------------------------o
  |
  |    Other options include:
  |      "giveup"        - Gives the answer (but also resets its frequency)
  |      "skip"          - Skips the question (doesn\'t reset its frequency)
  |      "tally"         - Shows the frequency each question is set for.
  |      "sorted tally"  - Like "tally" but ordered by frequency with answers.
  |      "remove"        - Removes the question from the (temporary) database.
  |      "rescore"       - Allows user to set the question frequency.
  |      "how many"      - Gives number of Qs needed until a given Average.
  |
  o---------------------------------------------------------------------------o
    '''
    
    ag_score=sum([history[_question] for _question in all_questions])
    avg= '%2.2f'%(float(ag_score) / len(facts) )
    print '   Frequency of this question = %d / %d.  (Average is %s.)'%(history[original_question],len(fact_array),avg)
    
    
    all_freqs=dict([(history[x],1) for x in all_questions]).keys()
    print '    All Frequencies: ',
    ninetyMinusSum=0
    for freq in list(reversed(sorted(all_freqs))):
      QsInF=len([x for x in all_questions if history[x]==freq])
      if freq>90: print '%d: %d,'%(freq,QsInF),
      else: ninetyMinusSum+=QsInF
    print '90-: '+str(ninetyMinusSum)
    
    #print '     Questions with:  200: %d, 175: %d, 150: %d'%(len([x for x in all_questions if history[x]==200]), \
    #                                                         len([x for x in all_questions if history[x]==175]), \
    #                                                         len([x for x in all_questions if history[x]==150]))
    print '\n'*14
    print question
    
    given_answer=raw_input('    > ').strip().lower()
    
    if question.lower().startswith('set:'):
      given_answer = ', '.join(sorted([x.strip() for x in given_answer.split(',')]))
      correct_answer = ', '.join(sorted([x.strip() for x in correct_answer.split(',')]))
    

      
    if given_answer == correct_answer:
      decrement = getDecrement (decrement_array + [history[original_question]])
      history[original_question]=decrement[history[original_question]]
      fact_array = getFactArray(facts,history)
      print '''
    
      **************************
      *                        *
      *   C O R R E C T ! ! !  *
      *                        *
      **************************
      '''
      time.sleep(.5)
    elif given_answer == 'skip': continue
    elif given_answer == 'tally':
      ag_score = 0
      for _question in all_questions:
        number = history[_question]
        ag_score += number
        print '  %4d'%number + '    ' + _question[:75]
      print ' Total:   '+str(len(facts))
      print ' Average: %2.2f'%(float(ag_score) / len(facts) )
      raw_input('press <ENTER> to continue')
    elif given_answer == 'how many':
      goal_freq = int(raw_input('What is your goal frequency?\n  >'))
      ag_score = 0
      for _question in all_questions:
        number = history[_question]
        ag_score += number
      Current_Average = float(ag_score) / len(facts) 
      Mock_all_questions = list(all_questions)
      Mock_history = dict(history)
      Mock_current_average = float(Current_Average)
      Mock_fact_array = list(fact_array)
      i_Counter = 0
      while Mock_current_average > goal_freq:
        #print Mock_current_average, goal_freq
        mock_i = random.randrange(len(Mock_all_questions))
        mock_question = Mock_all_questions[mock_i]
        mock_decrement = getDecrement (decrement_array + [Mock_history[mock_question]])
        Mock_history[mock_question]=mock_decrement[Mock_history[mock_question]]
        mock_fact_array = getFactArray(facts,Mock_history)
        ag_score = 0
        for _Mquestion in Mock_all_questions:
          number = Mock_history[_Mquestion]
          ag_score += number
        Mock_current_average = float(ag_score) / len(facts) 
        i_Counter += 1
      raw_input(str( i_Counter))
      
      
      
    elif given_answer == 'sorted tally':
      ag_score = 0
      for _question in sorted(all_questions,key=lambda x:history[x]):
        number = history[_question]
        ag_score += number
        print '  %4d'%number + '   ' + '%-75s'%_question[:75]+'   '+questions2answers[_question]
      print ' Total:   '+str(len(facts))
      print ' Average: %2.2f'%(float(ag_score) / len(facts) )
      raw_input('press <ENTER> to continue')
    elif given_answer == 'remove':
      facts = [fact for fact in facts if fact[0] != question]
      fact_array = getFactArray(facts,history)
    elif given_answer == 'giveup':
      history[original_question] = MAX_NUMBER
      fact_array = getFactArray(facts,history)
      prompt= '\n'*50+'Previous frequency: '+str(last_frequency)+'\n'
      prompt+= '  (To rescore, type "rescore".)\n\n'
      prompt+= 'To skip to the next question, type "next question".\n\n'
      prompt+= 'Otherwise, press <ENTER> to try again.\n\n'
      prompt+='  The correct answer is:\n  '+'*'*20+'\n  * '+correct_answer+'\n  '+'*'*20+'\n  > '
      prompt_ans=raw_input(prompt).lower()
      if 'next question' not in prompt_ans:
        given_answer = ''
      if 'rescore' in prompt_ans:
        #try: printed_frequency
        #except: printed_fre
        printed_frequency = history[original_question] if history[original_question]!=200 else last_frequency
        print '\n'*10+'Previous frequency: '+str(printed_frequency)+ \
              '\n\n\nWhat would you like the frequency to be? (Please provide an integer...)'
        sN = raw_input(' > ').strip()
        while not re.compile(r'^\d+$').match(sN): sN = raw_input('Wrong format.  Needs to be an integer:\n > ').strip()
        frequency = int(sN)        
        decrement = getDecrement (decrement_array + [frequency])
        history[original_question] = frequency
        fact_array = getFactArray(facts,history)
      
    elif given_answer == 'rescore':
      print '\n'*10+"The correct answer is:\n\t" + correct_answer
      
      print '\n'*10+'Previous frequency: '+str(last_frequency)+ \
            '\n\n\nWhat would you like the frequency to be? (Please provide an integer...)'
      # Crazy construction for in case the user doesn't type an integer.
      local_v=raw_input(' > ').strip()
      while not re.compile(r'^\d+$').match(local_v): local_v=raw_input('Wrong format. Needs to be an integer:\n > ').strip()
      frequency = int(local_v)
      decrement = getDecrement (decrement_array + [frequency])
      history[original_question] = frequency
      fact_array = getFactArray(facts,history)
    elif query == '1':
      print '\n'*50
      ans=raw_input( '''

  Do you consider your answer correct?
    Correct Answer: %s
    Your Answer:    %s

  type "Y" if so, "N" if not.

  Or type "try again" to try again.
  
  Then press <ENTER>.
   > '''%(correct_answer,given_answer))
      if ans.lower().startswith('y'):
        history[original_question]=decrement[history[original_question]]
        fact_array = getFactArray(facts,history)
        print '''
        
   counting this answer as...
   
   
        
      **************************
      *                        *
      *   C O R R E C T ! ! !  *
      *                        *
      **************************
        
        '''
        time.sleep(.5)
        given_answer = correct_answer
      else:
        history[original_question] = MAX_NUMBER
        fact_array = getFactArray(facts,history)
        print '''
        
        counting this answer as...
        
         ***************
         * INCORRECT!  *
         ***************
        
        '''
        time.sleep(.5)
        if 'try again' not in ans.lower():
          given_answer = correct_answer
    else:
      last_frequency = history[original_question]
      history[original_question] = MAX_NUMBER
      fact_array = getFactArray(facts,history)
      print '''

      ************
      *  Wrong!  *
      ************
    
        Try again...
    
      '''
      time.sleep (1)

  open('localdb','w').write('history='+pformat(history))