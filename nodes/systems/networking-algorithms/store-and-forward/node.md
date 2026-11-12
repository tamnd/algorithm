---
tag: TC3XFV
kind: technique
slug: store-and-forward
name: Store-and-forward switching
aliases:
- store-and-forward
- store-and-forward packet switching
area: systems/networking-algorithms
level: intro
summary: "Each node receives a whole packet, checks it, then sends it on. Over h links of rate R, a packet of L bits takes h L / R plus propagation and queueing; n packets in a row take (h + n - 1) L / R."
prereqs: [routing-problem, queue]
see_also: [virtual-cut-through, wormhole-routing, permutation-routing, packet-scheduling, switch-scheduling, flow-control, congestion-control, fair-queueing]
sources:
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2021
    locator: Chapter 1, Section 1.3.1 (store-and-forward transmission, the delay (h + n - 1) L / R) and Section 1.4 (processing, queueing, transmission and propagation delay)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Chapter 2, the discussion of packet and message switching and the choice of packet length (section number not checked)
  - paper: "Parviz Kermani and Leonard Kleinrock, Virtual cut-through, a new computer communication switching technique, Computer Networks 3(4), 1979, pages 267 to 286"
    locator: the comparison of the delay of virtual cut-through with store-and-forward message and packet switching (page numbers not checked)
  - book: isbn:9780122007514
    title: William James Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: the chapters on flow control, packet-buffer flow control (store-and-forward and cut-through) against flit-buffer flow control (wormhole) (chapter numbers not checked)
  - paper: "Paul Baran, On distributed communications, RAND Corporation memorandum series RM-3420-PR and following, 1964"
    locator: the proposal of a network of nodes that store message blocks and forward them hop by hop (volume and page not checked)
---

Store-and-forward switching is the rule that a switch or router must receive the whole of a packet before it starts to send it on the next link. While the packet arrives, the node stores it in a buffer; when the last bit is in, the node can check the packet, choose the output link and queue it there. The rule is simple and safe: corrupt packets are dropped at the first hop, links of different speeds can be joined, and a packet that must wait does not hold any link. The cost is delay. Over $h$ links of rate $R$, a packet of $L$ bits pays the full transmission time $L / R$ at every hop, so it needs $h L / R$ plus propagation, processing and queueing delays. A stream of $n$ such packets is pipelined across the links and needs $(h + n - 1) L / R$. This is the reason to cut long messages into packets, and the reason that [virtual cut-through](/virtual-cut-through/) and [wormhole routing](/wormhole-routing/) start to forward before the tail arrives.

## In plain words

Think of a relay of post offices. A post office does not pass on a parcel until the whole parcel has arrived and has been checked. Only then does it put the parcel on the next truck.

That makes each step safe and simple, but slow for big parcels, because every office must wait for the whole parcel. So big shipments are cut into small parcels. While the second office sends parcel one onward, the first office already sends parcel two. All the trucks work at the same time, and the whole shipment arrives much sooner than one huge parcel would.

## When it applies

- Links have different speeds, or a packet may have to wait for an output link, so the node must be able to hold whole packets.
- Packets must be checked before they go on, for example by their checksum, so that bad packets do not waste capacity further on.
- The packet length is small compared with the bandwidth-delay product of the path, so the per-hop delay $L / R$ is small next to propagation and queueing.
- The node must look at the whole packet to decide, as with deep packet inspection, encryption at each hop, or a store-carry-forward link that is not always up.

## The template

```pseudo
when the last bit of packet P has arrived at node x:
    check P (length, checksum) and drop it if it is bad
    choose the output link ℓ for P's destination (routing table)
    append P to the queue of ℓ, or drop P if that buffer is full
when link ℓ is idle and its queue is not empty:
    take the first packet P and send its L bits at the link rate R    ▷ this takes L / R
    the next node has the last bit after a further propagation delay
```

**The delay of one packet.** On a path of $h$ links with rates $R_1, \dots, R_h$ and propagation delays $d_1, \dots, d_h$, with no other traffic, a packet of $L$ bits arrives after

$$T_1 = \sum_{i=1}^{h} \Bigl( \frac{L}{R_i} + d_i \Bigr),$$

plus the processing time at each node and the time it waits in queues. With equal rates this is $h L / R + \sum_i d_i$.

**The delay of a stream.** If $n$ packets of $L$ bits leave the source back to back on links of equal rate, packet $k$ (from 1) leaves link $i$ at time $(i + k - 1) L / R$ plus the propagation delays, because each link sends one packet per $L / R$ and the packets move in step. So the last packet arrives at

$$T_n = (h + n - 1)\frac{L}{R} + \sum_i d_i .$$

With unequal rates, the slowest link sets the pace: $T_n = \sum_i L / R_i + (n - 1) L / \min_i R_i + \sum_i d_i$.

**The best packet size.** To send a message of $M$ bits as packets of $p$ payload bits, each with an $H$-bit header, over $h$ equal links,

$$T(p) = \Bigl(h - 1 + \frac{M}{p}\Bigr)\frac{p + H}{R}.$$

Large packets lose time to store-and-forward at every hop; small packets lose capacity to headers. Setting the derivative to zero gives $p^* = \sqrt{M H / (h - 1)}$. One packet of $M$ bits ($n = 1$) is never better than the best split when $h > 1$.

## Classic examples

- **A small path.** Three links of 10 Mb/s, packets of 1500 bytes ($L = 12000$ bits, $L / R = 1.2$ ms), no propagation delay. One packet needs $3 \times 1.2 = 3.6$ ms. Four packets in a row need $(3 + 4 - 1) \times 1.2 = 7.2$ ms, while one message of $48000$ bits sent whole would need $3 \times 4.8 = 14.4$ ms. With 40-byte headers, the best payload for this message is $p^* = \sqrt{48000 \cdot 320 / 2} \approx 2771$ bits, so packets of a few hundred bytes are best here.
- **Internet routers.** IP routers receive each packet, check its header, decrement the TTL, look up the next hop by [longest-prefix match](/longest-prefix-match/), and queue it at the output. Queue management and [packet scheduling](/packet-scheduling/) decide the order in which queued packets leave.
- **Ethernet switches.** Most switches work in store-and-forward mode, and drop frames with a bad check sequence. Some low-latency switches offer cut-through mode, which forwards after the destination address and so passes bad frames on.
- **The ARPANET.** The first packet network used store-and-forward IMPs, after the designs of Baran and of Davies. Earlier telegraph and message-switching systems stored whole messages at each relay.
- **Packet routing models.** The theory of [permutation routing](/permutation-routing/) and of routing on fixed paths in $O(C + D)$ steps assumes store-and-forward: in each step, a packet moves at most one whole edge.
- **Delay-tolerant networks.** Store-carry-forward networks hold a bundle at a node for minutes or days until a contact to the next node opens; the bundle protocol of the IETF works this way.

## Variations

- **Message switching against packet switching.** Message switching stores whole messages at each hop, so its delay grows with the message length times the hop count. Packet switching cuts messages into packets and pipelines them, as in the formula for $T_n$.
- **Cut-through switching.** A switch starts to send as soon as it has read the header, so the per-hop delay is about the header time, not $L / R$. If the output is busy, virtual cut-through stores the whole packet as store-and-forward does; see [virtual cut-through](/virtual-cut-through/).
- **Wormhole routing.** The packet is split into flits, and each node buffers only a few flits; a blocked packet stays spread over several links and holds them. See [wormhole routing](/wormhole-routing/).
- **Buffer management.** A node needs room for at least one whole packet per input, and usually much more. How the buffer is shared between inputs and outputs is the subject of [switch scheduling](/switch-scheduling/) and [flow control](/flow-control/).

## Pitfalls

- **Delay grows with hops times packet size.** Jumbo frames or a long chain of switches add $L / R$ at every hop. On slow links this can dominate the delay.
- **Store-and-forward deadlock.** With finite buffers, a cycle of nodes whose buffers are all full of packets for the next node in the cycle can never move. Buffer classes ordered by hop count, as studied by Merlin and Schweitzer (1980), or dropping packets, break such cycles.
- **Big buffers cause big queueing delay.** Queues absorb bursts, but a full queue of $B$ bits adds $B / R$ of delay at that hop, which is known as bufferbloat when buffers are much larger than needed. [Congestion control](/congestion-control/) and active queue management limit it.
- **Forgetting the other delays.** The formula $h L / R$ is only the transmission part. Propagation delay does not depend on the packet size and dominates on long links, and queueing delay depends on the load.
- **Header overhead in the packet size choice.** Smaller packets lower the pipeline delay but add headers and per-packet processing, so the best size depends on $M$, $H$ and $h$, not on the delay alone.

## References
