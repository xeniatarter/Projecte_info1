import math

class Node:
    def __init__(self,name:str, x:float, y:float, node_type="NAV"): #Asigna el valor 1 a self.name, el valor 2 a self.x y el valor 3 a self.y.
        self.name = name
        self.x = float(x)
        self.y = float(y)
        self.node_type= node_type
        self.neighbors = []

    def AddNeighbor(self,n2): #Permite agregar nodos a la lista neighbors
        if n2 in self.neighbors:
            return False
        self.neighbors.append(n2)
        return True

    def Distance(self, n2):
        return math.sqrt((n2.x-self.x)**2+(n2.y-self.y)**2)

    def __repr__(self): #Imprime los datos de nodos de forma 'bonita'
        return f"Node({self.name}, x={self.x}, y={self.y})"

