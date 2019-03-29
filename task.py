class peer:
    ip = ""
    port = ""
    intrested = False
    chocked = True  #If chocked no data will be recieved from the peer
    piece = ""

    def __init__(self, ip, port, piece):
        self.ip = ip
        self.port = port
        self.piece = piece

    def handshake(self):

    def setIntrest(self, isIntrested):
        if isIntrested:
            self.intrested = True
        else:
            self.intrested = False

    def chokePeer(self):
        self.chocked = True

    def unchokePeer(self):
        self.chocked = False

    def  __del__(self):
        print("piece {} has been downloaded".format(self.piece))
