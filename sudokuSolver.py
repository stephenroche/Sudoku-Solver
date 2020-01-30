import numpy as np
# import math

class BoardState:
	def __init__(self, assignment, domains):
		self.assignment = np.array(assignment)
		self.domains = np.array(domains)
		self.size = int(np.sqrt(len(assignment)))

	def assignVariable(self, variable, value):
		self.assignment[variable] = value
		self.domains[variable] = set([value])

		# Call arc consistency starting from variable

	def arcConsistency(self, varaible):
		queue = 

	def solveCSP(self):
		if self.isComplete():
			return self.assignment

		# Choose next variable to set
		mrv = 10
		for row in range(9):
			for column in range(9):
				if not self.assignment[row][column] and len(self.domains[row][column]) < mrv:
					mrv = len(self.domains[row][column])
					nextVariable = (row, column)
					for value in self.domains[nextVariable]:
						nextState = self.copy()
						nextState.assignVariable(nextVariable, value)
						result = nextState.solveCSP()
						# Success - found solution
						if result != False:
							return nextState.assignment

					# Return failure
					return False


	def isComplete(self):
		return all(all(row) for row in self.assignment)

	def getVariableAssignment(self, variable):
		return self.assignment[variable]

	def getDomainSize(self, variable):
		return len(self.domains[variable])

	def boardImage(self, valueFunction):
		size = self.size
		string = ''
		string += ('+' + '-' * 2 * size) * size + '+' + '\n'
		for bigRow in range(size):
			for littleRow in range(size):
				string += '|'
				for bigColumn in range(size):
					for littleColumn in range(size):
						value = valueFunction( (size * bigRow + littleRow, size * bigColumn + littleColumn) )
						# value = self.assignment[size * bigRow + littleRow][size * bigColumn + littleColumn]
						string += '%2d' % value if value else ' ' * 2
					string += '|'
				string += '\n'
			string += ('+' + '-' * 2 * size) * size + '+' + '\n'

		return string

	def __str__(self):
		return self.boardImage(self.getVariableAssignment)

	def printDomainSizes(self):
		print(self.boardImage(self.getDomainSize))

size = 2
assignment = np.full((size**2, size**2), None)
assignment[1][2] = 9
assignment[0][3] = 12
fullDomains = np.full((size**2, size**2), set(range(1, size**2 + 1)))
board = BoardState(assignment, fullDomains)
board.assignVariable((3, 0), 1)
print(board)
board.printDomainSizes()