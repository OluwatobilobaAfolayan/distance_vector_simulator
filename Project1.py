#Emmnauel Oluwatobiloba Afolayan
#CS4310-FALL2017
#Description: Program to simulate Distance Vector routing for a given network topology

import sys
from collections import defaultdict

nodes = [] #array to hold all distinct nodes
neighbours = []
routingTable = {} #routing table of all the nodes in the topology
num_of_dvp = 0 #Number of DV messages sent
rounds = 0; #number of rounds

class Graph:
    def __init__(self, vertices):
        self.nodeCount = vertices
        self.graph = []

    def add_graph(self, src, dest, cost):  #add to graph
        self.graph.append([src, dest, cost])

    def createRoutingTable(self, src, dest, cost):  #create routing table for each node
        if src not in routingTable.keys(): #checks if src is already in graph
            routingTable[src] = [[ dest, cost, dest ]]
        else:
            routingTable[src].append([dest, cost, dest])

        if dest not in routingTable.keys():
            routingTable[dest] = [[ src, cost, src ]]
        else:
            routingTable[dest].append([src, cost, src])

if __name__ == '__main__':
    with open(sys.argv[1], "r") as f: #read file from command line
      lines = f.readlines()
    g = Graph(100)

    for x in lines:
      line = x.split()
      g.add_graph(line[0], line[1], line[2])
    for row in g.graph:
        g.createRoutingTable(row[0], row[1], row[2]) #calls graph function to create routing table

    for i in routingTable.keys():
         nodes.append(i)
    for key, value in routingTable.items():  #add non-neighbours of node to its routing tgable
         neighbours = []
         for j in value:
             neighbours.append(j[2])
         for k in nodes:
             if k not in neighbours and key != k:
                 routingTable[key].append([k, sys.maxint, 'x'])

    print('***********************************************************************')
    print('BEFORE CONVERGENCE')
    print('***********************************************************************')
    for r, v in routingTable.items():
        print('Node: ' + str(r) + ', Routing table:' + str(v))

    convergence = False
    while convergence is False:
        convergence = True
        complete_dv_packet = {}
        for n, rt in routingTable.items(): #prepare DV Packet for every node in topology
            dvPacket_per_node = {}
            for j in rt:  #prepares DV Packet
                if j[1] is not sys.maxint:  #checks if it is a neighbour or not
                    dvPacket_per_node[j[0]] = j[1]
            complete_dv_packet[n] = dvPacket_per_node
            num_of_dvp+=1

        for node, rt2 in routingTable.items():  #share DV Packet with its neighbours
            for x in rt2:
                cost_to_node = 0
                if x[1] is not sys.maxint and x[0] is x[2]: #checks node is a neighbour
                    neighbour = x[0]
                    rt_neighbour = routingTable.get(neighbour, 0) #get routing table of neighbour node
                    for a in rt_neighbour: #get cost to node from neighbour
                        if a[0] == node:
                            cost_to_node = a[1]
                    node_dv_packet = complete_dv_packet[node]   #retrieve dv packet of current node

                    for dest, advertised_cost in node_dv_packet.items():
                        initial_cost = 0
                        pos = 5.9 #arbitrary value
                        for n1 in rt_neighbour:
                            if dest == n1[0]:
                                pos = rt_neighbour.index(n1)
                                initial_cost = int(n1[1])

                        if int(advertised_cost) + int(cost_to_node) < int(initial_cost) and pos is not 5.9:
                            convergence = False
                            rt_neighbour[pos][1] = str(int(advertised_cost) + int(cost_to_node))
                            rt_neighbour[pos][2] = str(node)
                            last_node_to_converge = rt_neighbour[pos][0]
        rounds+=1


    print('***********************************************************************')
    print('AFTER CONVERGENCE')
    print('***********************************************************************')

    for r, v in routingTable.items():
        print('Node: ' + str(r) + ', Routing table:' + str(v))

    print('***********************************************************************')
    print('The number of rounds it took to converge is ' + str(rounds))
    print('The last node to converge in the network is '+ str(last_node_to_converge))
    print('The number of DV messages sent in total is ' + str(num_of_dvp))
    print('***********************************************************************')

    if sys.argv[1] == 'topology1.txt': #find path from 0 to 3
        path = []
        src = str(0)
        path.append(src)
        reachDest = False
        while reachDest is False:
            for x, j in routingTable.items():
                if x is str(src):
                    rt = j
            for z in rt:
                if z[0] == str(3):
                    if z[2] == str(3):
                       reachDest = True
                       path.append(z[2])
                    elif z[2] != str(3):
                       src = z[2]
                       path.append(z[2])
        print('Path from 0 to 3 is ' + str(path))

    if sys.argv[1] == 'topology2.txt': #find path from 0 to 7
        path = []
        src = str(0)
        path.append(src)
        reachDest = False
        while reachDest is False:
            for x, j in routingTable.items():
                if x is str(src):
                    rt = j
                    break;
            for z in rt:
                if z[0] == str(7):
                    if z[2] == str(7):
                        reachDest = True
                        path.append(z[2])
                    elif z[2] != str(7):
                        src = z[2]
                        path.append(z[2])
                    break
        print('Path from 0 to 7 is ' + str(path))

    if sys.argv[1] == 'topology3.txt': #find path from 0 to 23
        path = []
        src = str(0)
        path.append(src)
        reachDest = False
        while reachDest is False:
            for x, j in routingTable.items():
                if x is str(src):
                    rt = j
                    break;
            for z in rt:
                if z[0] == str(23):
                    if z[2] == str(23):
                        reachDest = True
                        path.append(z[2])
                    elif z[2] != str(23):
                        src = z[2]
                        path.append(z[2])
                    break
        print('Path from 0 to 23 is ' + str(path))

    print('***********************************************************************')
