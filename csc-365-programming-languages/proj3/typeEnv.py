
class TypeEnv(object):
    def __init__(self) :
        self.scopes = [{}]
        
    def __len__(self):
        return reduce(lambda a, b : a + len(b), self.scopes, 0)
    
    def numLevels(self):
        return len(self.scopes)
    
    def __setitem__(self, address, value):
        self.scopes[0][address] = value
 
    def __getitem__(self, key):
        for scope in self.scopes :
            if key in scope :
                return scope[key]
        return None
        
    def __delitem__(self, key):
        del self.scopes[0][key]
    
    def keys(self):
        return [k for scope in self.scopes for k in scope]
        
    def __iter__(self):
        return iter(self.keys())

    def __contains__(self, key):
        #return reduce(lambda a, b : a or item in b, self.scopes, False)
        return any([key in scope for scope in self.scopes])

    def isGlobal(self, key):
        return key in self.scopes[-1]

    def push(self):
        self.scopes = [{}] + self.scopes
        
    def pop(self):
        self.scopes = self.scopes[1:]
    
    
    