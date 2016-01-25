import operator
from collections import defaultdict
from cs176.basics import *

class DVRouter(Entity):
    __SPACE = "  "

    """ Default constructor """
    def __init__(self):
        # key: destination
        # value: {next hop, latency}
        self.routing_table = defaultdict(lambda: None)

        # key: destination
        # value: {via neighbor, latency}
        # self.forwarding_table = defaultdict(lambda: {"neighbor":None, "latency":float('inf')})
        self.forwarding_table = defaultdict(lambda: defaultdict(lambda: float('inf')))

        # key: port
        # value: neighbor
        self.port_table = {}

    """ Handle packets sent to the router """
    def handle_rx(self, packet, port):
        if type(packet) is DiscoverPackets:
            self.__update_port_table(packet, port)
            self.__handle_discover_packet(packet, port)
        elif type(packet) is UpdateRouting:
            self.__handle_update_routing_packet(packet)
        else:
            self.__handle_data_packet(packet)

    """ Handles what to do when a router receives a Discover Packet """
    def __handle_discover_packet(self, packet, packet_port):

        self.forwarding_table[packet.src][packet.src] = packet.latency

        if packet.is_link_up is False:
            poisonPacket = UpdateRouting()
            poisonPacket.add_destination(packet.src, float('inf'))
            for port, destination in self.port_table.iteritems():
                if type(destination) is not BasicHost:
                    self.send(poisonPacket, port, False)
            for dest in self.forwarding_table:
                self.forwarding_table[dest][packet.src] = float('inf')
            for dest in self.routing_table:
                self.routing_table[dest] = self.__get_minimum_latency(self.forwarding_table[dest])

        else:
            oldValue = self.routing_table[packet.src]
            self.routing_table[packet.src] = self.__get_minimum_latency(self.forwarding_table[packet.src])
            update_packet = UpdateRouting()
            if oldValue != self.routing_table[packet.src]:
                update_packet.add_destination(self.routing_table[packet.src][0], self.routing_table[packet.src][1])

            # If the source of the Discover Packet is a BasicHost, then
            # send update to distance vector to every router in the port table
            if type(packet.src) is BasicHost and bool(update_packet.paths) == True:
                for port, destination in self.port_table.iteritems():
                    if type(destination) is not BasicHost:
                        self.send(update_packet, port, False)

            # Else if the source of the Discover Packet is a DVRouter, then do the following:
            # (1) Send entire distance vector to the source of the Discover Packet
            # (2) Send distance vector update to everyone except hosts and source of Discover Packet
            else: #type(packet.src) is DVRouter:
                # Send whole distance vector in packet to port of DiscoverPacket source
                distance_vector_packet = UpdateRouting()
                #adding everything in self's routing table
                for tuple in self.routing_table.values():
                    #if dest != packet.src:
                    distance_vector_packet.add_destination(tuple[0], tuple[1])
                self.send(distance_vector_packet, packet_port, False)
                if bool(update_packet.paths) == True:
                    # Send distance vector update to everyone except hosts and DiscoverPacket source
                    for port, destination in self.port_table.iteritems():
                        if type(destination) is DVRouter and packet.src is not destination:
                            self.send(update_packet, port, False)



    """ Handles what to do when a router receives a Update Routing Packet """
    def __handle_update_routing_packet(self, packet):

        update_packet = UpdateRouting()

        # if self.name == 'r2':
        #     print str(packet.paths) + " from " + packet.src.name

        ### if we arw getting from neghbors

        for dest, latency in packet.paths.iteritems():
            if dest == self:
                continue
            self.forwarding_table[dest][packet.src] = latency + self.routing_table[packet.src][1]
            old_state = self.routing_table[dest]
            self.routing_table[dest] = self.__get_minimum_latency(self.forwarding_table[dest])


            if old_state != self.routing_table[dest]:
                update_packet.add_destination(dest, self.routing_table[dest][1])

        if bool(update_packet.paths) is True:
            for port, neighbor in self.port_table.iteritems():
                self.send(update_packet, port, False)

        # split horizon
            """ a get G to 1"""

    """ Handles actions when a router receives a data (Ping) packet """
    def __handle_data_packet(self, packet):
        nextHopLat = self.routing_table[packet.dst]
        print "packet.src: " + str(packet.src) + " Next Hop and Latency: " + str(nextHopLat)
        if(nextHopLat is not None and nextHopLat[1] != float('inf')):
            for port, neighbor in self.port_table.iteritems():
                if nextHopLat[0] == neighbor:
                    self.send(packet, port, False)
                    break


    """ Updates the port table """
    def __update_port_table(self, packet, port):
        # If the link is alive, then add port to tables
        if packet.is_link_up is True:
            self.port_table[port] = packet.src
        # Else link is dead, so remove port from tables
        else:
            if port in self.port_table.keys():
                del self.port_table[port]


    def __get_minimum_latency(self, vector):
        if len(vector) > 0:
            sorted_vector = sorted(vector.items(), key=operator.itemgetter(1))
            return sorted_vector[0]

    """ Prints the routing table """
    def print_routing_table(self):
        self.__print_title("Routing Table(" + self.name + ")")
        for destination, tuple in sorted(self.routing_table.iteritems()):
            if destination is not self:
                print (self.__SPACE + destination.name + "->"),
                print ("(" + tuple[0].name + "," + str(tuple[1]) + ")")
        print

    """ Prints the title for a function call in command line """
    def __print_title(self, title):
        print "\n" + self.__SPACE + title + "\n" + self.__SPACE + ("-" * len(title))

    def print_forwarding_table(self):
        self.__print_title("Forwarding Table(" + self.name + ")")
        for destination, link_info in self.forwarding_table.iteritems():
            if destination is not self:
                print (self.__SPACE + destination.name + "->"),
                for neighbor, latency in sorted(link_info.iteritems()):
                    print (self.__SPACE + neighbor.name + "," + str(latency)),
                print
        print

