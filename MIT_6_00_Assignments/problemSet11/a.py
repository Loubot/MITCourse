# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class MITNode(Node):
    def __hash__(self):
        return hash(self.name)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class MITEdge(Edge):
    def __init__(self, src,dest,dist,outDist):
        Edge.__init__(self,src,dest)
        self.dist = dist
        self.outDist = outDist
    def getDistance(self):
        return int(self.dist)
    def getOutDist(self):
        return int(self.outDist)
    def __str__(self):
        return str(self.src)+'->' + str(self.dest)+' Distance: ' + self.dist + ' OutDistance: '+ self.outDist

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]

class MITMap(Digraph):
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(edge)
    def __str__(self):
        res = ''
        for node, edge in self.edges.iteritems():
            for e in edge:
                res = res + str(e) + '\n'
        return res

mapFileName = 'mit_map.txt'
##mapFileName = 'practise_map.txt'
#
# Problem 2: Building up the Campus Map
#
# Write a couple of sentences describing how you will model the
# problem as a graph)
#

def load_map(mapFileName):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    #TODO
    graph = MITMap()
    print "Loading map from file..."
    dataFile = open(mapFileName)
    for line in dataFile:
        src,dest,dist,outDist = line.split()
        node1 = MITNode(src)
        node2 = MITNode(dest)
        edge = MITEdge(node1,node2,dist,outDist)
        try:
            graph.addNode(node1)
        except:
            pass
        try:
            graph.addNode(node2)
        except:
            pass
        try:
            graph.addEdge(edge)
        except ValueError as e:
            print e
    return graph


d =load_map(mapFileName)
for edge in d.childrenOf(MITNode('57')):
    print edge

def recurseList(d,start,end,visited = []):
   path =[str(start)]

   if MITNode(start) == MITNode(end):
      return path
   shortest = None
   for edge in d.childrenOf(MITNode(start)):
      if edge.getDestination() not in visited:
         visited = visited + [edge.getDestination()]
         newPath = recurseList(d,edge.getDestination(),end,visited)
##         print visited
         if newPath == None:
            continue
         if (shortest == None or len(newPath) < len(shortest)):
            shortest = newPath
##            print '%%%%%%%%%%%%%%%%%%',shortest

   if shortest != None:
##       print '£££££££££££'
       path = path + shortest
   else:
##       print '**********'
       path = None
   return path
         
                                  
##c = d.childrenOf(MITNode('32'))
##for edge in c:
##   print str(edge)
a =recurseList(d,'32','56')
print 'ans',a
