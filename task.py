class peer:
    ip =""
    port = ""
    intrested = False
    chocked = True #If chocked no data will be recieved from the peer
    piecesAvaliable =[]

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

