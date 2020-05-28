import portion as P

'''This class allows to manage a certain number of segments equal to the number of wifi terminals present in the system. 
These segments are defined according to the maximum capacities of the access point and allow, thanks to an evaluation 
function, to determine the number of access points required for a given configuration. '''


class Interval:
    def __init__(self, nbAP, maxClient, maxBandwidth):
        self.ap = nbAP
        self.client = maxClient
        self.bandwidth = maxBandwidth
        self.listOfSegment = []
        self.maxIter = 0

    def addSegment(self, fromA, toB):
        tmp = P.open(fromA, toB)
        self.listOfSegment.append(tmp)

    def build(self):
        for i in range(1, self.ap+1):
            print("Minumum value nb_ap : "+str(i)+" expected value :" + str(self.maxIter * (i - 1)))
            print("Maximum value nb_ap : " + str(i) + " expected value :" + str(self.maxIter * i))
            self.listOfSegment.append(P.open(self.maxIter * (i - 1), self.maxIter * i))
        print(self.listOfSegment)

    def config(self):
        self.maxIter = 0.6 * self.client + 0.4 * self.bandwidth
        print("Segment created : l = " + str(self.maxIter))

    def getListOfSegm(self):
        return self.listOfSegment

    def define(self, bandwidth, nbClient):
        return 0.6 * nbClient + 0.4 * bandwidth

    def expect(self, value):
        for s in self.listOfSegment:
            if value in s:
                return self.listOfSegment.index(s) + 1



'''# nb de borne +  capacité
nbrOfAP = 5
capacity_bandwith_per_AP = 50
capacity_client_per_AP = 20
nbr_client = 4
bandwith = 20
heuritic = 0.6 * nbr_client + 0.4 * bandwith
interval1 = Interval(nbrOfAP, capacity_client_per_AP, capacity_bandwith_per_AP)
interval1.config()
interval1.build()
print(interval1.getListOfSegm())
print(interval1.expect(80.16))'''