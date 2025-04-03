from node import Node
from segment import Segment
n1 = Node('BCN','2','6')
n2 = Node('MAD', '4','13')
n3 = Node('SEV', '9','14')

s1 = Segment("S1",n1,n2)
s2 = Segment("S2",n2,n3)

print(n1)
print(n2)
print(n3)
print(s1)
print(s2)