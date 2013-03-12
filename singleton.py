class Singleton(object):
	_instance = None
	"""
	Used by __new__ to return the unique singleton instance and by
	__init__ to determine if it has been called yet.
	"""

	def __new__(cls, *args, **kwargs):
		"""
		Create a new object on the first call. Return it on every 
		subsequent call without creating any more objects.
		"""
		if not cls._instance:
			return super(Singleton, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, *args):
		"""
		First call: Save the unique singleton instance to a class
		  variable _instance. Then call init_once, passing any args.
		Thereafter: Just checks that the argument list is empty to ensure 
		  that the caller is not attempting reinitialization.
		"""
		#print "init:", id(self) #should print many times with the same id 
		if self._instance is None:
			if len(args) < 2:
				raise BaseException("Not enough arguments on first call to " + self.__class__.__name__ + " constructor.")
			self.__class__._instance = self
			self.init_once(*args)
		elif len(args) > 0:
			raise BaseException("Too many arguments to " + self.__class__.__name__ + " constructor.")
