class NavAirport:
    def __init__(self, name):
        self.name = name
        self.sids = []
        self.stars = []

    def AddSid(self, navpoint):
        self.sids.append(navpoint)

    def AddStar(self, navpoint):
        self.stars.append(navpoint)

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs: {len(self.sids)}, STARs: {len(self.stars)})"
