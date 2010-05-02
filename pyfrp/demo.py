from frp import *

a = TimerE(.5)
printE(WithTimeE(sinET(a)))

#a = TimerB(100)
#printB(sinB(a)+100)

runtime.run()
