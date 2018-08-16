class Permissions(object):
    def __init__(self,code_list):
        self.code_list=code_list
    def list(self):
        return "list" in self.code_list
    def add(self):
        return "add" in self.code_list
    def delete(self):
        return "delete" in self.code_list
    def edit(self):
        return "edit" in self.code_list