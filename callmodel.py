

class CallModel():
    
    def __init__(self):
        self.incoming = False
        self.sipA = ""
        self.sipB = ""
        callid = ""
        packets = []
        internalnode = ""
        externalnode = ""
        sequence = []
    
    def setIncoming(self, incoming):
        self.incoming = incoming
    
    def getIncoming(self):
        return self.incoming
    
    def setSipA(self, sipuri):
        self.sipA = sipuri
    
    def getSipA(self):
        return self.sipA
    
    def setSipB(self, sipuri):
        self.sipB = sipuri
    
    def getSipB(self, sipuri):
        return self.sipB
    
    def setCallID(self, callid):
        self.callid = callid
    
    def getCallID(self):
        return self.callid
    
    def getPackets(self):
        return packets
    
    def setPackets(self, packets):
        self.packets = packets
    
    def appendPackets(self, packet):
        self.packets.append(packet)
    
    def setInternalNode(self, node):
        self.internalnode = node
    
    def getInternalNode(self):
        return self.internalnode
    
    def setExternalNode(self, node):
        self.externalnode = node
    
    def getExternalNode(self):
        return self.externalnode
    
    def setSequence(self, sequence):
        self.sequence = sequence
    
    def appendSequence(self, sequence):
        self.sequence.append(sequence)
    
    def getSequence(self):
        return self.sequence