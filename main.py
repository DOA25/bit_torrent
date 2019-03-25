import asyncio
from builtins import str

import aiohttp
from aiohttp import web
import bcoding as bencode
from urllib import parse
import random
import struct
import codecs
import socket
import hashlib
import time
import re
import ujson
import sys
import collections
from yarl import URL


async def getClients(session,meta, peer_id):
    print("Requesting clients from {}".format(meta['announce']))
    info = meta['info']
    m = hashlib.sha1()
    m.update(bencode.bencode(info))
    print(bencode.bencode(info))
    byte = m.digest()
    hash = parse.quote_from_bytes(byte).strip()
    payload = {"info_hash": hash,
                "peer_id": peer_id,
                "downloaded": 0}
    time.sleep(3)
    async with session.get(URL(meta['announce'], encoded=True).with_query(payload)) as res:
        print(res.url)
        if res.status != 200:
            print("Failure")
            print(await res.text())
            exit()
        return await res.read()




async def generatePeerID():
    sha = hashlib.sha1()
    stime = bytes(random.randint(1, 9999))
    sha.update(stime)
    return parse.quote_from_bytes(sha.digest())

async def decodePeerBinary(peerList):
    i = 0
    peers =[]
    while i < len(peerList):
        #ip = "{}".format(peerList[i])
        #for p in range(i+1, i+4):
        #    ip = ip + "." + str(peerList[p])
        binIp = struct.unpack_from('!i',peerList,i)[0]
        ip = socket.inet_ntoa(struct.pack("!i", binIp))
        i = i+4
        binPeer = struct.unpack_from('!H', peerList,i)[0]
        peers.append([ip, binPeer])
        i = i+3
    print(peers)




async def main():
    f = open("torrentFiles/[HorribleSubs] Mob Psycho 100 S2 - 01 [1080p].mkv (1).torrent",'rb')
    peerid = await generatePeerID()
    torrent_file = f.read()
    f.close()
    torrent_file = bencode.bdecode(torrent_file)
    async with aiohttp.ClientSession() as session:
        peers = bencode.bdecode(await getClients(session, torrent_file, peerid))
        print(peers)
        #peer_list = re.findall('......', peers['peers'])
        chunk_size = 6
        peer = ""
        peer_list = await decodePeerBinary(peers['peers'])




loop = asyncio.get_event_loop()
loop.run_until_complete(main())

