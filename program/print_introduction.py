class Introduction():
  def __init__(self,facts):
    self.facts=facts
    self.header='\n'*50 +'''
  
    O P T I O N S 
     #------------------------------------------------------------------------#
     #
     #   "giveup"        - Gives the answer (but also resets its frequency)
     #   "skip"          - Skips the question (doesn\'t reset its frequency)
     #   "tally"         - Shows the frequency each question is set for.
     #   "sorted tally"  - Like "tally" but ordered by frequency with answers.
     #   "remove"        - Removes the question from the (temporary) database.
     #   "rescore"       - Allows user to set the question frequency.
     #
     #------------------------------------------------------------------------#
    '''
  
  def get_histogram(self):
    histogram=[]
    ninetyMinusSum=0
    for freq in reversed(sorted(list(self.all_freqs))):
      questions_with_this_frequency=len([fact for fact in self.facts if fact.question.frequency.value==freq])
      if freq>90: 
        histogram.append( (freq,questions_with_this_frequency) )
      else: 
        ninetyMinusSum += questions_with_this_frequency
    if ninetyMinusSum: histogram.append( ( '90-',ninetyMinusSum ) )
    return histogram
  
  def get_stats(self,fact):
    Low_Watermark = fact.question.frequency.low_watermark
    Frequency = fact.question.frequency.value
    All_Frequencies = [_fact.question.frequency.value for _fact in self.facts]
    self.all_freqs = set(All_Frequencies)
    population_size = sum(All_Frequencies)
    Average = '%2.2f'%(float(population_size) / len(self.facts) )
  
    self.stats = r'''
    S T A T S:    
     #-------------------- # -----------------------#
     # Q U E S T I O N     #  P O P U L A T I O N   #
     #-------------------- # -----------------------#
     # Low-         Frequ  #    Aver       Size     
     # Watermark     ency  #     age                
     #   %3s         %3s   #   %3s       %3s     
     #-------------------- # -----------------------#
    
    '''%(str(Low_Watermark),str(Frequency),str(Average),str(population_size))
    
  def _print(self,fact):
    s= self.header
    self.get_stats(fact)
    h = self.get_histogram()
    s+=self.stats
    print h
    for freq, questions_with_this_frequency in self.get_histogram():
      s+= ' '+str(freq)+':'+str(questions_with_this_frequency)
    s+='\n'*14
    s+=fact.question.value
    print s
    