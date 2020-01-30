import numpy as np
import util
import copy
import re

class BoardState:
	def __init__(self, assignment, domains=None):
		if isinstance(assignment, str):
			f = open(assignment, 'r')
			assignment = re.findall(r'\.|\d+', f.read())
			assignment = np.array([int(x) if x != '.' else None for x in assignment])
			sizeSquared = int(np.sqrt(len(assignment)))
			assignment = np.reshape(assignment, (sizeSquared, sizeSquared))
			print(assignment)

		self.size = int(np.sqrt(len(assignment)))
		if domains is not None:
			self.domains = copy.deepcopy(domains)
			self.assignment = np.array(assignment)

		else:
			self.domains = np.full((self.size**2, self.size**2), None)
			for row in range(self.size**2):
				for column in range(self.size**2):
					self.domains[row, column] = set(range(1, self.size**2 + 1))

			self.assignment = np.full((self.size**2, self.size**2), None)
			for row in range(self.size**2):
				for column in range(self.size**2):
					if assignment[row][column]:
						self.assignVariable( (row, column), assignment[row][column])

	def assignVariable(self, variable, value):
		self.assignment[variable] = value
		self.domains[variable] = set([value])

		# Remove value from domains of neighbours
		return self.forwardChecking(variable, value)

		# Call arc consistency starting from variable

	def forwardChecking(self, variable, value):
		size = self.size
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
		mrv = self.size**2 + 1
		for row in range(self.size**2):
			for column in range(self.size**2):
				if not self.assignment[row][column] and len(self.domains[row][column]) < mrv:
					mrv = len(self.domains[row][column])
					nextVariable = (row, column)
		for value in self.domains[nextVariable]:
			nextState = self.copy()
			nextState.assignVariable(nextVariable, value)
			result = nextState.solveCSP()
			# Success - found solution
			if result is not False:
				self.assignment = result
				return result

		# Return failure
		return False


	def isComplete(self):
		return all(all(row) for row in self.assignment)

	def copy(self):
		return BoardState(self.assignment, self.domains)

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

# size = 2
# assignment = np.full((size**2, size**2), None)
# assignment[1][2] = 2
# assignment[0][3] = 3
# board = BoardState(assignment)
# board.assignVariable((3, 2), 1)
# a1 = np.array(board.assignment)
# a1[3, 3] = 5
# print(board)
# a2 = np.array(board.domains)
# a2[3, 3] = set([1,2,3,4,5])
# board.printDomainSizes()

# # a = np.array([5,6,7])
# # b = np.array(a)
# # c = a
# # a[1] = 9
# # print(b)
# # print(c)
# print(board.domains[0, 2])

# print(board.solveCSP())
# print(board)

# size = 3
# board = BoardState(np.full((size**2, size**2), None))
# print(board.solveCSP())
# # print(board)

# # size = 4
# # board = BoardState(np.full((size**2, size**2), None))
# # print(board.solveCSP())
# # print(board)
# # board.printBlank()

board = BoardState('first_test.txt')
board.solveCSP()
print(board)