from navpoints import NavPoint
from navsegments import NavSegment
from navairports import NavAirport

class AirSpace:
    def __init__(self):
        self.navpoints = []
        self.navsegments = []
        self.navairports = []

def AddNavPoint(airspace,navpoint):
    airspace.navpoints.append(navpoint)

def AddNavSegment(airspace, navsegment):
    airspace.navsegments.append(navsegment)

def AddAirport(airspace, airport):
    airspace.navairports.append(airport)

def Navpoint(airspace, number):
    for navpoint in airspace.navpoints:
        if navpoint.number == number:
             return navpoint
    return None

def Airport(airspace, name):
    for airport in airspace.navairports:
        if airport.name == name:
            return airport
    return None

def CreateGraph4(navpoint_file, navsegment_file, airport_file):
    airspace = AirSpace()

    with open(navpoint_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 4:
                number, name, lat, lon = parts
                navpoint = NavPoint(int(number), name, float(lat), float(lon))
                AddNavPoint(airspace,navpoint)

    with open(navsegment_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 3:
                origin, dest, dist = parts
                navsegment = NavSegment(int(origin), int(dest), float(dist))
                AddNavSegment(airspace,navsegment)

    with open(airport_file, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3:
                name = parts[0]
                sids = [int(n) for n in parts[1].split(",") if n]
                stars = [int(n) for n in parts[2].split(",") if n]
                airport = NavAirport(name)
                airport.sids = [AddNavPoint(airspace,n) for n in sids]
                airport.stars = [AddNavPoint(airspace,n) for n in stars]
                AddAirport(airspace,airport)

    return airspace


