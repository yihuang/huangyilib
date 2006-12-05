class Action(object):
        reg_after = {}
        reg_before = {}
        def __init__(self,func):
                self.internal = func
        def __call__(self):
                '''excute all actions registered to excute before self,
                then excute self,
                last excute all actions registered to excute after self.'''
                if self.reg_before.has_key(self):
                        acs = self.reg_before[self]
                        for a in acs:
                                a()
                self.internal()
                if self.reg_after.has_key(self):
                        acs = self.reg_after[self]
                        for a in acs:
                                a()
        def before(self,action):
                'register self take place before action'
                self.register(action,self,self.reg_before)
        def after(self,action):
                'register self take place after action'
                self.register(action,self,self.reg_after)
        @staticmethod
        def register(ac1,ac2,reg):
                if reg.has_key(ac1):
                        reg[ac1].append(ac2)
                else:reg[ac1]=[ac2]

class Door(object):
        def __init__(self,no):
                self.no = no
                self.Open = Action(self.ac_Open)
        def ac_Open(self):
                print 'door',self.no,'open'

class Player(object):
        def __init__(self,name):
                self.name = name
                self.Die = Action(self.ac_Die)
        def ac_Die(self):
                print self.name,'player die'

class Beer(object):
        def __init__(self,no):
                self.no = no
                self.Start = Action(self.ac_Start)
        def ac_Start(self):
                print 'beer',self.no,'start'

if __name__ =='__main__':
        player = Player('hy')
        door = Door(1)
        beer = Beer(1)
        door.Open.before(player.Die)
        beer.Start.after(door.Open)
        player.Die()