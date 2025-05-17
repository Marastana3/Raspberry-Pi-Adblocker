from dnslib.server import DNSServer, DNSHandler, BaseResolver
from dnslib import DNSRecord, RR, QTYPE, A
import socket

BLOCKLIST = {"doubleclick.net", "ads.example.com"}

class BlocklistResolver(BaseResolver):
    def resolve(self, request, handler):
        qname = str(request.q.qname).rstrip(".")
        print(f"Request for: {qname}")

        if any(domain in qname for domain in BLOCKLIST):
            reply = request.reply()
            reply.add_answer(RR(qname, QTYPE.A, rdata=A("0.0.0.0"), ttl=60))
            print("Blocked:", qname)
            return reply

        try:
            proxy_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            proxy_sock.settimeout(2)
            proxy_sock.sendto(request.pack(), ("1.1.1.1", 53))
            response, _ = proxy_sock.recvfrom(4096)
            return DNSRecord.parse(response)
        except Exception as e:
            print("Error forwarding:", e)
            return request.reply()

resolver = BlocklistResolver()
server = DNSServer(resolver, port=53, address="0.0.0.0")
server.start_thread()

print("DNS Proxy running on port 53...")
import time; time.sleep(1_000_000)
