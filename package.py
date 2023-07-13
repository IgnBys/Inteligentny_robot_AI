class Package():
    def __init__(self,id,size,type):
        self.size=size
        self.id=id
        self.type=type

    def get_size(self):
        return self.size

    def get_id(self):
        return self.id

    def get_type(self):
       return self.type