import portion as P

'''This class allows to manage a certain number of segments equal to the number of wifi terminals present in the system. 
These segments are defined according to the maximum capacities of the access point and allow, thanks to an evaluation 
function, to determine the number of access points required for a given configuration. '''


class Interval:
    def __init__(self, minA, maxB):
        self.min = minA
        self.max = maxB
        self.listOfSegment = []

    def addSegment(self, fromA, toB):
        if fromA == self.min:
            tmp = P.closed(fromA, toB)
        else:
            tmp = P.openclosed(fromA, toB)
        self.listOfSegment.append(tmp)

    def getListOfSegment(self):
        return self.listOfSegment

# nb de borne +  capacité
nbrOfAP= 5
capacity_bandwith=50
capacity_client=20

interval1 = Interval(1, 4)
interval1.addSegment(2, 3)
print(interval1.getListOfSegment())
