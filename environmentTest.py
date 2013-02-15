import unittest
from environment import Environment

class EnvironmentTestCase(unittest.TestCase):
	def runTest(self):
		environment = Environment()
		assert environment.width > 0 and environment.height > 0, 'Environment has no dimensions'
		environment.debug_output()
