from node import Node
class Segment:
    def __init__(self,name:str,origin: Node, destination: Node):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Node.Distance(origin,destination)
    def __repr__(self): #Ens retorna la informació ben presentada
        return f"Segment({self.name}: {self.origin.name}-{self.destination.name}, cost={self.cost})" #La f permet incluir variables dins el text
