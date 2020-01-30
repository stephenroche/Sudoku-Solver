import numpy as np
import util
import copy

class BoardState:
	def __init__(self, assignment, domains=None):
		self.size = int(np.sqrt(len(assignment)))
		if domains is not None:
			self.assignment = np.array(assignment)
			self.domains = copy.deepcopy(domains)
		else:
			self.assignment = np.full((self.size**2, self.size**2), None)
			self.domains = np.full((self.size**2, self.size**2), set())
			for row in range(self.size**2):
				for column in range(self.size**2):
					self.domains[row, column] = set(range(1, size**2 + 1))

	def assignVariable(self, variable, value):
		self.assignment[variable] = value
		self.domains[variable] = set([value])

		# Remove value from domains of neighbours
		return self.forwardChecking(variable, value)

		# Call arc consistency starting from variable

	def forwardChecking(self, variable, value):
		row, column = variable
		neighbours = []
		for x in range(size**2):
			if x != column:
				neighbours.append( (row, x) )

		for y in range(size**2):
			if y != row:
				neighbours.append( (y, column) )

		for y in range(size * (row // size), size * (row // size + 1)):
			for x in range(size * (column // size), size * (column // size + 1)):
				if y != row and x != column:
					neighbours.append( (y, x) )

		print(len(neighbours), 'neighbours')

		for neighbour in neighbours:
			self.domains[neighbour].discard(value)
			if len(self.domains[neighbour]) == 0:
				return False


		for group in self.domains[row, :], self.domains[:, column], self.domains[size * (row // size):size * (row // size + 1), size * (column // size):size * (column // size + 1)].flatten():
			for n in range(1, size**2 + 1):
				if not any(n in domain for domain in group):
					return False

		return True
		

	# def arcConsistency(self, variable):
	# 	queue = util.Queue()


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
board = BoardState(assignment)
board.assignVariable((3, 0), 1)
a1 = np.array(board.assignment)
a1[3, 3] = 5
print(board)
a2 = np.array(board.domains)
a2[3, 3] = set([1,2,3,4,5])
fullDomains[3, 3].add(88)
board.printDomainSizes()

# a = np.array([5,6,7])
# b = np.array(a)
# c = a
# a[1] = 9
# print(b)
# print(c)