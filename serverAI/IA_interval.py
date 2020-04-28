import portion as P

'''This class allows to manage a certain number of segments equal to the number of wifi terminals present in the system. 
These segments are defined according to the maximum capacities of the access point and allow, thanks to an evaluation 
function, to determine the number of access points required for a given configuration. '''


def calc_heuristic(param1, param2):
    return 0.6 * param1 + 0.4 * param2


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
nbrOfAP = 5
capacity_bandwith_per_AP = 50
capacity_client_per_AP = 20
nbr_client = 4
bandwith = 20
heuritic = 0.6 * nbr_client + 0.4 * bandwith
interval1 = Interval(0, 20)
interval1.addSegment(1, 3)
interval1.addSegment(2, 6)
print(interval1.getListOfSegment())
print(calc_heuristic(nbr_client,bandwith))
