class Introduction():
  def __init__(self,facts):
    self.facts=facts
    self.header='\n'*50 +'''
    
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
  |
  o----------------------------------------------------------------------------o
    '''
  
  def get_histogram(self):
    histogram=[]
    ninetyMinusSum=0
    for freq in reversed(sorted(list(self.all_freqs))):
      questions_with_this_frequency=len([fact.question.value for fact in self.facts if fact.question.frequency==freq])
      if freq>90: 
        histogram.append( (freq,questions_with_this_frequency) )
      else: 
        ninetyMinusSum += questions_with_this_frequency
    histogram.append( ( '90-',ninetyMinusSum ) )
    return histogram
    
    
  def _print(self,fact):
    self.all_freqs=set([fact.question.frequency.value for fact in self.facts])
    population_size = sum(self.all_freqs)
    
    avg= '%2.2f'%(float(population_size) / len(self.facts) )
    s=self.header+'\n'
    s+='   Frequency of this question = %d / %d.  (Average is %s.)\n'%(fact.question.frequency.value,len(self.facts),avg)
    s+= str(fact.question.frequency.low_watermark)
    s+='    All Frequencies: '
    for freq, questions_with_this_frequency in self.get_histogram():
      s+= str(freq)+':'+str(questions_with_this_frequency)
    s+='\n'*14
    s+=fact.question.value
    print s
    