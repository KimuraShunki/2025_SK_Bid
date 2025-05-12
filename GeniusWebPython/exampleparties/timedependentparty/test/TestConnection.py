from typing import List, Optional
from tudelft.utilities.listener.DefaultListenable import DefaultListenable
from geniusweb.actions.Action import Action
from geniusweb.inform.Inform import Inform
from geniusweb.connection.ConnectionEnd import ConnectionEnd
from geniusweb.references.Reference import Reference
from uri.uri import URI

class TestConnection(DefaultListenable[Inform], ConnectionEnd[Inform, Action]):
	'''
	A "real" connection object, because the party is going to subscribe etc, and
	without a real connection we would have to do a lot of mocks that would make
	the test very hard to read.
	'''
	
	def __init__(self):
		super().__init__()
		self.actions: List[Action]  = []

	#Override
	def send(self , action:Action ):
		self.actions.append(action)

	#Override
	def getReference(self)-> Reference :
		return None #type:ignore

	#Override
	def getRemoteURI(self) -> URI :
		return None #type:ignore

	def  close(self):
		pass
	 
	#Override
	def getError(self)->Optional[Exception] :
		return None

	def getActions(self) -> List[Action] :
		return self.actions
