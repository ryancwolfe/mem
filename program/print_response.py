import time
def correct_answer():
      print '''
    
      **************************
      *                        *
      *   C O R R E C T ! ! !  *
      *                        *
      **************************
      '''
      time.sleep(.5)

def wrong():
      print '''

      ************
      *  Wrong!  *
      ************
    
        Try again...
    
      '''
      time.sleep (1)


def giveup(answer,frequency_low_watermark):
      print '\n'*50
      raw_input( '''
      Previous frequency: %s
      
      The correct answer is:
      
      ***********************************************************************
      *
      *  %s
      *
      ***********************************************************************
        
      Press <ENTER> to try again.
      
          > '''%(frequency_low_watermark,answer))
      
        
def rescore(answer,frequency_low_watermark):
      print '\n'*10+"The correct answer is:\n\t" + answer + \
            '\n'*10+'Previous frequency: '+str(frequency_low_watermark)+ \
            '\n\n\nWhat would you like the frequency to be?'

def tally():
      ag_score = 0
      for _question in all_questions:
        number = ioQuestion2frequency[_question]
        ag_score += number
        print '  %4d'%number + '    ' + _question[:75]
      print ' Total:   '+str(len(facts))
      print ' Average: %2.2f'%(float(ag_score) / len(facts) )
      raw_input('press <ENTER> to continue')

def sorted_tally():
      ag_score = 0
      for _question in sorted(all_questions,key=lambda x:ioQuestion2frequency[x]):
        number = ioQuestion2frequency[_question]
        ag_score += number
        print '  %4d'%number + '   ' + '%-75s'%_question[:75]+'   '+questions2answers[_question]
      print ' Total:   '+str(len(facts))
      print ' Average: %2.2f'%(float(ag_score) / len(facts) )
      raw_input('press <ENTER> to continue')

