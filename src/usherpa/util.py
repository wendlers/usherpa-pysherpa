from functools import wraps

def synchronized(tlockname):
	"""A decorator to place an instance based lock around a method """

	def _synced(func):

		@wraps(func)
		def _synchronizer(self,*args, **kwargs):

			tlock = self.__getattribute__(tlockname)
			tlock.acquire()

			try:
				return func(self, *args, **kwargs)
			finally:
				tlock.release()

		return _synchronizer

	return _synced
