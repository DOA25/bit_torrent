import asyncio
from builtins import str
import socket
import aiohttp
from aiohttp import web
import bencode
from task import peer
from urllib import parse
import random
import struct
import codecs
import socket
import binascii as bin
import hashlib
import time
import re
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
    for x in peerList:
        print("{}: {}".format(int(x),str(x)))
    while i < len(peerList):
        binIp = struct.unpack_from('!i',peerList,i)[0]
        ip = socket.inet_ntoa(struct.pack("!i", binIp))
        i = i+4
        binPeer = struct.unpack_from('!H', peerList,i)[0]
        peers.append([ip, binPeer])
        i = i+2
    print(peers)
    return peers

async def breakPieces(metainfo):
    pecies = []
    offset = 0
    print(metainfo)
    while (offset<len(metainfo)):
        pecies.append(bin.hexlify(metainfo[offset: offset + 19]))
        offset = offset + 20
    return pecies


async def downloadFile(torrent_file, peerList, peerid):
    fileInfo = torrent_file['info']
    jobs = await createTasks(peerList, await breakPieces(fileInfo['pieces']))
    f= open(fileInfo['name'], "wb")
    downloadedPieces = []
    for i in jobs:
        print("{}:{} {}".format(i.ip,i.port, i.piece))

async def requestPeerList(torrent_file, peerid):
    async with aiohttp.ClientSession() as session:
        response = bencode.bdecode(await getClients(session, torrent_file, peerid))
        return response


async def createTasks(peerList, peices):
    jobs = []
    for i in peerList:
        for piece in peices:
            jobs.append(peer(i[0], i[1], piece))
    return jobs


async def main():
    f = open("torrentFiles/Mob_Psycho_100_S2-01.torrent", 'rb')
    peerid = await generatePeerID()
    torrent_file = f.read()
    f.close()
    torrent_file = bencode.bdecode(torrent_file)
    response = await requestPeerList(torrent_file, peerid)
    peer_list = await decodePeerBinary(response['peers'])
    await downloadFile(torrent_file, peer_list, peerid)





loop = asyncio.get_event_loop()
loop.run_until_complete(main())

