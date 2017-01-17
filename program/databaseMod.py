from pprint import pformat
class Database():
  def __init__(self,ioQuestion2frequency):
    self.allQuestion2frequency=dict(ioQuestion2frequency)
  def __dict__(self):
    return self.allQuestion2frequency
  def rescore(self,fact):
    self.allQuestion2frequency[str(fact.question)]=int(fact.question.frequency)
  def store(self):
    open('localdb','w').write('ioQuestion2frequency='+pformat(self.allQuestion2frequency))
  def update(self,fact):
    self.rescore(fact)
    self.store()
