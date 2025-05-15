from navairports import NavAirport
n1 = NavAirport('LEAL')
n2 = NavAirport ('LEBL')
n3 = NavAirport()
print(Node.Distance(n1,n1)) #Distància de n1 a si mateix
print(Node.Distance(n1,n2)) #Distància de n1 a n2
print(Node.AddNeighbor(n1,n2)) #Afageix n2 a la llista de veïns True
print(Node.AddNeighbor(n1,n2)) #Afageix n2 a la llista de veïns False, perq ja hi era
print(n1.__dict__) #Es guarden les característiques de cada node a un diccionari que es __dict__
for n in n1.neighbors:
    print(n.__dict__) #Mostra els atributs/característiques de n2

    LEGE
    GIR.D
    GIR.A
    LEIB
    IZA.D
    IZA.A