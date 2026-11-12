---
tag: DKHAZZ
kind: technique
slug: direct-server-return
name: Direct server return
aliases:
- DSR
area: systems/load-balancing-and-hashing
level: advanced
summary: "The balancer forwards each request packet to a backend without changing its IP addresses; the backend owns the VIP too and replies straight to the client, so replies bypass the balancer."
prereqs: [layer-4-load-balancing]
see_also: [maglev-hashing, ecmp-hashing, consistent-hashing, health-checking, connection-draining, layer-7-load-balancing, load-balancer]
sources:
  - url: http://www.linuxvirtualserver.org/VS-DRouting.html
    title: The Linux Virtual Server project, Virtual Server via Direct Routing
    locator: the whole page (the balancer changes only the destination MAC address; the real servers have the VIP on a non-ARP alias device and reply to the client directly; the balancer and the servers must be on one LAN segment)
  - url: http://www.linuxvirtualserver.org/VS-IPTunneling.html
    title: The Linux Virtual Server project, Virtual Server via IP Tunneling
    locator: the whole page (the request is encapsulated in IP to the real server, which decapsulates it and replies to the client directly; the real servers can be in any network)
  - url: https://docs.kernel.org/networking/ip-sysctl.html
    title: Linux kernel documentation, IP Sysctl
    locator: the entries arp_ignore (1, reply only if the target address is configured on the incoming interface) and arp_announce (2, always use the best local address for this target)
  - paper: "Daniel E. Eisenbud, Cheng Yi, Carlo Contavalli, Cody Smith, Roman Kononov, Eric Mann-Hielscher, Ardas Cilingiroglu, Bin Cheyney, Wentao Shang and Jinnah Dylan Hosein, Maglev: a fast and reliable software network load balancer, 13th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2016), pages 523 to 535"
    locator: the system overview (packets are encapsulated in GRE to the service endpoint, and the replies go directly to the client, not through Maglev)
  - paper: "Parveen Patel, Deepak Bansal, Lihua Yuan, Ashwin Murthy, Albert Greenberg, David A. Maltz, Randy Kern, Hemant Kumar, Marios Zikos, Hongyu Wu, Changhoon Kim and Naveen Karri, Ananta: cloud scale load balancing, ACM SIGCOMM 2013, pages 207 to 218"
    locator: the design sections on the multiplexer and the host agent (inbound packets are encapsulated to the host, and the host agent sends the replies without the multiplexer); the exact section numbers are not checked
  - url: https://github.com/facebookincubator/katran
    title: Katran, README
    locator: the section on limitations (katran works only in DSR mode, uses IPIP encapsulation, does not fragment, and recommends a smaller advertised TCP MSS)
---

*Direct server return* (DSR) is a way to forward traffic in a [layer 4 load balancer](/layer-4-load-balancing/) so that only the requests pass through the balancer. The balancer picks a backend for each flow as usual, but it does not rewrite the IP addresses of the packet: it either changes only the destination MAC address, or it wraps the whole packet in an outer IP header addressed to the backend. The backend also owns the service's virtual IP (VIP), on a device that does not answer ARP, so it accepts the packet as its own and sends the reply from the VIP straight to the client. Since responses are often much larger than requests, the balancer carries a small part of the bytes and can serve many more connections. The cost is that the balancer never sees the replies, and the backends need special network setup.

## In plain words

A normal balancer is like a front desk that takes each question, passes it to an expert, waits for the answer and hands it back. Every answer goes through the desk, and answers are often long.

With direct server return, the desk only passes the question on. The expert answers the customer directly, and signs the answer with the shop's name, not their own, so the customer believes the shop answered. The desk handles only short questions, so it can serve many more customers.

For this to work, every expert must accept mail addressed to the shop, but must never tell the post office "the shop lives here", or the post office would send all mail to that one expert.

## When it applies

- The traffic is asymmetric: responses are much larger than requests, as for web pages, video and file downloads. Then the bytes through the balancer fall to about the request bytes.
- The balancer works at [layer 4](/layer-4-load-balancing/): it does not need to see or change the replies. A [layer 7](/layer-7-load-balancing/) balancer that reads responses, retries or compresses cannot use DSR.
- The backends can be set up to accept the VIP: the VIP on a loopback or dummy device, ARP replies for it turned off, and, for the tunnel forms, a tunnel device that unwraps IP-in-IP or GRE.
- For the MAC form, the balancer and the backends share one LAN segment. The tunnel forms work across routers.
- The return path from the backend to the client does not pass a stateful firewall or NAT that expects to see both directions.

## The template

The balancer runs FORWARD on each packet to the VIP; the backend runs RECEIVE.

```pseudo id=main
FORWARD(pkt)                                   ▷ on the balancer; pkt.dst = VIP
L1  key ← the 5-tuple of pkt
L2  if key is not in table then
L3      table[key] ← POLICY()                  ▷ e.g. round robin, least connections, a consistent hash
L4  b ← table[key]; if mode = MAC then
L5      pkt.dst_mac ← mac(b)                   ▷ IP addresses unchanged
L6  else wrap pkt in an outer IP header from the balancer to ip(b)   ▷ IP-in-IP or GRE
L7  send pkt

RECEIVE(pkt)                                    ▷ on backend b
L8  if pkt is wrapped then unwrap it
L9  if pkt.dst is not a local address (the VIP on loopback) then drop pkt
L10 handle the request; send the reply from VIP:port to the client by the normal route
```

**Why it works.** In both forms, the packet that reaches the TCP stack of the backend is the one the client sent: source the client, destination the VIP. Line L9 accepts it because the VIP is a local address. The reply at line L10 has source VIP and destination the client, which is exactly what the client's TCP connection expects, so the client cannot tell that the reply came from another machine. The flow affinity of [layer 4 balancing](/layer-4-load-balancing/) comes from lines L1 to L3: all packets of one 5-tuple reach the same backend while the table entry lives.

**The ARP rule.** In the MAC form, the backends sit on the same LAN as the router. If a backend answered ARP requests for the VIP, the router could learn the backend's MAC address for the VIP and send all client traffic to that backend, past the balancer. On Linux the usual settings are `arp_ignore = 1` (answer only for addresses configured on the interface that gets the request, so not for a VIP on loopback) and `arp_announce = 2` (never use the VIP as the source of the backend's own ARP requests).

**What is guaranteed.** Flows arrive online and in any order. DSR keeps flow affinity as above and does not change the choice of the policy, so the balance of load is that of the policy. What DSR changes is the cost: the balancer handles only the client-to-server packets.

## Classic examples

**Bytes through the balancer.** A request is one 300-byte packet and the response is 30,000 bytes. With NAT, the balancer receives and sends each request and each response, so it moves $2 \cdot (300 + 30000) = 60600$ bytes per request. With DSR by MAC rewrite it moves $2 \cdot 300 = 600$ bytes, about 0.99 percent of that. With IP-in-IP it sends 20 more bytes per packet, 620 in all, and with GRE 24 more, 624.

**MTU and MSS.** On an Ethernet link with an MTU of 1500 bytes, TCP over IPv4 can send segments of $1500 - 20 - 20 = 1460$ bytes of data. A full packet of 1500 bytes wrapped in IP-in-IP becomes 1520 bytes and no longer fits. So the backends should advertise an MSS of at most $1500 - 20 - 40 = 1440$ for IP-in-IP and $1436$ for GRE, or the network between the balancer and the backends needs a larger MTU. The MAC form adds no header. The Katran README states that it does not fragment and recommends advertising a smaller MSS.

**The LVS modes.** The Linux Virtual Server offers three forwarding modes. NAT rewrites the destination address and port, and the replies must come back through the balancer to be rewritten. Direct routing changes the MAC address only. Tunneling wraps the packet in IP. The last two are DSR; the servers in tunneling mode can be in another network.

**Large balancers.** Maglev wraps packets in GRE to the service endpoints, and the replies go directly to the client. Katran uses IP-in-IP and works only in DSR mode. Ananta's host agents receive encapsulated packets and send the replies without the multiplexer.

## Variations

- **MAC rewrite (direct routing).** No extra header, no MTU cost, but one LAN segment and careful ARP settings.
- **IP-in-IP or GRE tunnel.** Works across routed networks and lets the backends be anywhere, at the cost of 20 or 24 bytes per packet and an MTU or MSS change. Some balancers vary the outer source address per flow so that the receiving network cards spread the flows over their queues.
- **Destination address on the host.** In Ananta, an agent on each host does the address work, so the service sees a normal address and the reply leaves without the multiplexer.
- **Stateless or hash-based tables.** With many balancer instances behind [ECMP](/ecmp-hashing/), each instance can use [Maglev hashing](/maglev-hashing/) or another [consistent hash](/consistent-hashing/) so that a flow keeps its backend when it moves to another instance.

## Pitfalls

- **ARP for the VIP.** A backend that answers ARP for the VIP can take all traffic of the LAN. Set `arp_ignore = 1` and `arp_announce = 2`, or put the VIP on a device that does not do ARP.
- **No view of the replies.** The balancer cannot measure response times, see the end of a response, or count bytes sent. Policies such as [least response time](/least-response-time/) do not apply, and [least connections](/least-connections/) must guess the end of a connection from the client's FIN or from a timeout, so the counts lag.
- **Health and draining.** The balancer does not see a backend that stops replying. It needs active [health checks](/health-checking/), and [draining](/connection-draining/) must wait for the table entries to expire.
- **Fragments and MTU.** A wrapped packet that exceeds the MTU is dropped or fragmented; fragments after the first carry no port numbers, so a hash on the 5-tuple can send them to another backend.
- **Reverse path filters.** A router or host that checks that the source of a packet is reachable through the interface it came in on can drop the replies with the VIP as the source.
- **Port rewriting is not possible.** The backend must listen on the same port as the VIP, since the balancer does not change the port.

## Exercises

1. A balancer has a 10 Gb/s link. Requests are 400 bytes and responses 40,000 bytes. How many requests per second can it carry with NAT, and with DSR by MAC rewrite?
2. Why does DSR by MAC rewrite need the balancer and the backends on one LAN segment, while the tunnel form does not?
3. Explain what happens when a backend in direct routing mode has `arp_ignore = 0` and the router sends an ARP request for the VIP.
4. A backend advertises an MSS of 1460 behind a GRE tunnel with a path MTU of 1500. Which packets are affected, and what are two fixes?
5. Least connections in DSR mode counts a connection as closed when it sees the client's FIN. Give a case where the count is too high for a long time, and one where it is too low.

## References
