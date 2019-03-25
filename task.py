class task:
    ip =""
    port = ""
    intrested = False
    chocked = True #If chocked no data will be recieved from the peer

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

