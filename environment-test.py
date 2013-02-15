import unittest

class EnvironmentTestCase:
	def runTest(self):
		environment = Environment()
		assert environment.width > 0 && environment.height > 0, 'Environment has no dimensions'
