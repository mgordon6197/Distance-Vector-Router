import cs176
from cs176.core import CreateEntity, topoOf
from cs176.basics import BasicHost
from hub import Hub
from the_router import DVRouter as router
import cs176.topo as topo
from time import sleep


def create ():

    r1 = router.create('r1')
    r2 = router.create('r2')
    r3 = router.create('r3')

    topo.link(r1, r2, 14)
    topo.link(r1, r3, 1)
    topo.link(r3, r2, 1)


    #r1 = router.create('r1')
    #r2 = router.create('r2')
    #r3 = router.create('r3')
    #topo.link(r1,r2,3)
    #topo.link(r1,r3,2)

    #h1 = BasicHost.create('h1')
    #h2 = BasicHost.create('h2')

    #h1.linkTo(r1)
    #h2.linkTo(r2)

