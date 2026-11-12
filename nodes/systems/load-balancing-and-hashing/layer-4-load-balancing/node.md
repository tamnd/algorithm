---
tag: DZ9K42
kind: concept
slug: layer-4-load-balancing
name: Layer 4 load balancing
aliases:
- transport-layer load balancing
area: systems/load-balancing-and-hashing
level: intro
summary: "Balancing by TCP or UDP flow: the balancer reads only addresses and ports, picks a backend once per flow and sends every later packet of that flow to the same backend."
prereqs: [load-balancer, hash-function]
see_also: [layer-7-load-balancing, direct-server-return, maglev-hashing, ecmp-hashing, consistent-hashing, source-ip-hash, least-connections, connection-draining]
sources:
  - url: http://www.linuxvirtualserver.org/VS-NAT.html
    title: The Linux Virtual Server project, Virtual Server via NAT
    locator: the whole page (the destination address and port are rewritten to those of the chosen server, the connection is kept in a hash table, replies are rewritten back to the virtual service)
  - url: http://www.linuxvirtualserver.org/VS-IPTunneling.html
    title: The Linux Virtual Server project, Virtual Server via IP Tunneling
    locator: the whole page (the request is encapsulated to the real server, which replies to the client directly)
  - url: http://www.linuxvirtualserver.org/VS-DRouting.html
    title: The Linux Virtual Server project, Virtual Server via Direct Routing
    locator: the whole page (the balancer changes the destination MAC address; the balancer and the servers must share one LAN segment)
  - paper: "Daniel E. Eisenbud, Cheng Yi, Carlo Contavalli, Cody Smith, Roman Kononov, Eric Mann-Hielscher, Ardas Cilingiroglu, Bin Cheyney, Wentao Shang and Jinnah Dylan Hosein, Maglev: a fast and reliable software network load balancer, 13th USENIX Symposium on Networked Systems Design and Implementation (NSDI 2016), pages 523 to 535"
    locator: the sections on the system overview (routers spread packets over Maglev machines with ECMP, GRE encapsulation to the service endpoints, direct return) and on consistent hashing with connection tracking
  - paper: "Parveen Patel, Deepak Bansal, Lihua Yuan, Ashwin Murthy, Albert Greenberg, David A. Maltz, Randy Kern, Hemant Kumar, Marios Zikos, Hongyu Wu, Changhoon Kim and Naveen Karri, Ananta: cloud scale load balancing, ACM SIGCOMM 2013, pages 207 to 218"
    locator: the design sections (a layer 4 balancer in a cloud data center, with a router tier, a software multiplexer tier and a host agent that does the NAT)
  - url: https://nginx.org/en/docs/stream/ngx_stream_upstream_module.html
    title: nginx documentation, Module ngx_stream_upstream_module
    locator: the upstream directive and its balancing methods for TCP and UDP (hash, least_conn, random)
---

A layer 4 [load balancer](/load-balancer/) chooses a backend for each transport flow, a TCP connection or a stream of UDP datagrams, and reads only the IP and TCP or UDP headers: the addresses, the ports and the protocol. It picks the backend once, when the flow starts, and then sends every packet of the flow to that backend. It never parses the bytes that the application sends, so it cannot route by URL or cookie, but it is cheap per packet and works for any protocol on top of TCP or UDP. The name refers to the transport layer, layer 4 of the OSI model. Balancing by request content is [layer 7 load balancing](/layer-7-load-balancing/).

## In plain words

A layer 4 balancer is like a receptionist who sends each visitor to a desk but never reads the visitor's papers. It looks only at the envelope: who sends, to which door. When a new visitor comes, it picks a desk. Every later letter from the same visitor in the same conversation goes to the same desk, because the desk has the start of the story.

So the balancer is fast and works for any kind of traffic. But it sees only conversations, not the questions in them. If one visitor asks a thousand questions in one long conversation, they all go to one desk.

## The idea

**The flow and its key.** A flow is identified by its *5-tuple*: source address, source port, destination address, destination port and protocol. The destination address is the *virtual IP* (VIP) of the service, which the balancer announces. Each packet of a flow carries the same 5-tuple, so the balancer can find the flow of each packet without state from the application.

**Flow affinity.** The one rule that every layer 4 balancer must keep is that all packets of a flow reach the same backend. A TCP connection has state only on the backend that accepted it; a packet that reaches another backend is answered with a reset. The balancer keeps the rule in one of two ways, often both:

- A **connection table** maps the 5-tuple to the chosen backend. The first packet (a TCP SYN) runs the policy, and later packets look up the table. LVS keeps this table as a hash table.
- A **hash of the 5-tuple** picks the backend, so any balancer that knows the same list of backends picks the same one without a table. With modulo hashing, a change of the list moves most flows; [consistent hashing](/consistent-hashing/) and [Maglev hashing](/maglev-hashing/) move few.

**Policies.** Any per-connection policy can run on the first packet: [round robin](/round-robin-load-balancing/), [weighted round robin](/weighted-round-robin/), [least connections](/least-connections/), [weighted least connections](/weighted-least-connections/), [source IP hash](/source-ip-hash/) or a consistent hash. The unit of balance is the connection, not the request, so the balancer cannot know how much work a connection will bring.

**How the packets get to the backend.** There are four common forms.

| form | what the balancer does to a request packet | path of the reply | what the backend needs |
|---|---|---|---|
| proxy | ends the client's TCP connection and opens its own to the backend | through the balancer | nothing |
| NAT | rewrites the destination address and port to the backend | through the balancer, which rewrites the source back to the VIP | the balancer as its gateway |
| tunnel | wraps the packet in an IP-in-IP or GRE header to the backend | from the backend to the client | to unwrap the packet and accept the VIP |
| MAC rewrite | changes only the destination MAC address | from the backend to the client | the same LAN segment, the VIP on a device that does not answer ARP |

The last two are [direct server return](/direct-server-return/): the replies, which are often much larger than the requests, bypass the balancer.

**Scaling out.** One balancer machine is a limit and a single point of failure. Large systems run many balancer instances behind routers that spread packets with [ECMP](/ecmp-hashing/). A router change can send the packets of one flow to another instance, which has no table entry for it. If every instance uses the same consistent hash over the same backend list, the new instance makes the same choice. Maglev combines a connection table with Maglev hashing for this reason.

**What is guaranteed.** Flows arrive online and in any order. Flow affinity holds for each flow as long as its table entry lives, or as long as the backend list does not change. The balance of load depends on the policy and on the arrival model of each policy page; a layer 4 balancer adds no guarantee on the work per backend, because it does not see the work.

## Examples

**Modulo hashing on a change.** Take a hash $h$ of the 5-tuple and the backend $h \bmod n$. When a fifth backend joins four, a flow keeps its backend only if $h \bmod 4 = h \bmod 5$. Over one period of 20 hash values, that holds for $h = 0, 1, 2, 3$ only, so 4 of 20 flows, or 20 percent, keep their backend. The other 80 percent of the open connections break if no table holds them. In general, going from $n$ to $n + 1$ backends keeps exactly $1/(n+1)$ of the hash values. A consistent hash moves only about $1/(n+1)$ of the flows, those that the new backend takes.

**Long connections.** Three clients each open one HTTP/2 connection and send 100, 10 and 10 requests per second over it. A layer 4 round robin over three backends gives each backend one connection, so the backends see 100, 10 and 10 requests per second. A layer 7 balancer that picks a backend for each request can give each backend 40. This is the common reason to move gRPC and HTTP/2 traffic to layer 7, or to make clients open several connections.

**A connection table.** A balancer has backends A and B and runs least connections. A SYN from 10.0.0.1 port 5000 arrives; both backends have 0 connections, so it picks A and stores the 5-tuple with A. A SYN from 10.0.0.2 port 6000 goes to B. A data packet from 10.0.0.1 port 5000 finds the table entry and goes to A, whatever the counts are now. A FIN or a timeout removes the entry.

## Where it is used

- **Linux Virtual Server (IPVS).** The Linux kernel module of the LVS project, with NAT, tunnel and direct routing modes and schedulers such as round robin, WLC and SED. Kubernetes can use it for Service traffic in the IPVS mode of kube-proxy.
- **Large cloud and web balancers.** Google's Maglev (NSDI 2016), Microsoft's Ananta for Azure (SIGCOMM 2013) and Facebook's Katran run in software on ordinary servers behind ECMP routers and return traffic directly from the backends.
- **Proxies in TCP mode.** HAProxy in `mode tcp` and the nginx `stream` module end the client's connection and open one to the backend, with policies such as least_conn and hash.
- **Cloud network balancers.** Managed services that work per flow, often the first tier in front of a [layer 7](/layer-7-load-balancing/) tier.

Layer 4 balancing is the transport-layer cousin of [ECMP hashing](/ecmp-hashing/) in routers. ECMP spreads flows over equal-cost paths; a layer 4 balancer spreads them over servers behind one address, and it must also track the health of those servers.

## References
