class BaseResponse(object):
    def __init__(self,code=1000,data=None,error=None):
        self.code = code
        self.data = data
        self.error = error
    @property
    def dict(self):
        return self.__dict__
