import random

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

def getDecrementDictionary(decrement_array):
  decrement_array = list(reversed(sorted(list(set(decrement_array)))))
  decrement_dictionary = {}
  for i,d in enumerate(decrement_array):
    if len(decrement_array) == i+1: decrement_dictionary[d] = d
    else: decrement_dictionary[d] = decrement_array[i+1]
  return decrement_dictionary

MAX_NUMBER = decrement_array[0]

class Frequency():
  def __init__(self,frequency=MAX_NUMBER):
    self.set_to(frequency)
    self.low_watermark = frequency
  def decrement(self):
    decrement_dictionary = getDecrementDictionary(decrement_array)
    new_value = decrement_dictionary[self.value]
    self.set_to( new_value )
    self.low_watermark = new_value
  def set_to(self,frequency):
    self.value=frequency
  def __int__(self):  return int(self.value)
  def __str__(self):  return str(self.value)
  def reset(self):
    self.set_to(MAX_NUMBER)

class Question():
  def __init__(self,question,_freq=MAX_NUMBER):
    self.value=question
    self.frequency = Frequency(_freq)
  def __str__(self):
    return str(self.value)

class Fact():
  def __init__(self,question,answer):
    self.question = Question(question)
    self.answer = answer
    
  def render_pick3(self):
    question = list(self.question.value.split()[1:])
    i = random.randrange(len(question)-2)
    while (question[i]).startswith('~'): 
      i = random.randrange(len(question)-2)
    question = 'Reference: "'+question[i]+' '+question[i+1]+' '+question[i+2]+'"'
    question = question.replace('~','')
    return question,self.answer
    
  def render_blanks(self):
    print self.question
    question = list(self.question.split())
    title=''
    if question[0].endswith(':'):
      title=question[0]+' '
      question=question[1:]
    how_many_blanks=int(round(len(question)/3.5))
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
    answer = (', '.join(wordsInCorrectAnswer)).lower()
    
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
            ew_word=word[1]+new_word
          new_word=word[0]+new_word
      newQuestion.append(new_word)
    #--------------------------
    # (B) Handle double blanks
    if self.answer.lower() == 'blanks':
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
    return question,answer
    
  def render(self):
    #-----------------------------------------------------------------------------
    # Handle the "Pick 3"s
    #-----------------------------------------------------------------------------
    if self.question.value.lower().startswith('pick3:'):
      return self.render_pick3()
    
    #-----------------------------------------------------------------------------
    # Handle the "fill in the blank questions"
    #-----------------------------------------------------------------------------
    if self.answer.lower() in ['list','blanks']:
      return self.render_blanks()
    
    return self.question.value,self.answer

class Facts():
  def __init__(self,facts):
    self.population = Population(facts)
    self.facts=facts
  def __list__(self):
    return self.facts

class Population():
  def __init__(self,facts):
    self.facts = facts
    self.repopulate()
  def repopulate(self):
    self.value=[]
    for i,fact in enumerate(self.facts):
      frequency=fact.question.frequency
      for _ in range(frequency):
        self.value.append(i)
  def __len__(self): return len(self.value)

  
#facts=[Fact('What is your name?','George'),Fact('What is down there?','hippos')]
#population=Population(facts)
#facts[0].question.frequency.decrement()
#population.repopulate()

#population = getFactArray(facts,ioQuestion2frequency)