---
tag: 8GH0FX
kind: technique
slug: virtual-cut-through
name: Virtual cut-through
aliases:
- virtual cut-through routing
- virtual cut-through switching
area: systems/networking-algorithms
level: intro
summary: "Forward a packet as soon as its head is routed, as in wormhole routing, but take the next channel only when its buffer can hold the whole packet. A blocked packet waits in one router."
prereqs: [store-and-forward, wormhole-routing]
see_also: [wormhole-routing, store-and-forward, dimension-order-routing, deadlock-prevention, switch-scheduling, flow-control, valiant-routing, permutation-routing]
sources:
  - paper: doi:10.1016/0376-5075(79)90032-1
    title: "Parviz Kermani and Leonard Kleinrock, Virtual cut-through: a new computer communication switching technique, Computer Networks 3(4) (1979), 267-286"
    locator: the definition of virtual cut-through, and the queueing analysis of its delay against store-and-forward (equal at heavy load, much lower at light load)
  - paper: doi:10.1109/71.127260
    title: "William J. Dally, Virtual-channel flow control, IEEE Transactions on Parallel and Distributed Systems 3(2) (1992), 194-205"
    locator: the comparison of flit-buffer flow control with virtual channels against packet-buffer flow control
  - paper: "Valentin Puente, Ramón Beivide, José A. Gregorio, J. M. Prellezo, José Duato and Cruz Izu, Adaptive bubble router: a design to improve performance in torus networks, Proceedings of the International Conference on Parallel Processing (ICPP 1999), 58-67"
    locator: bubble flow control, which keeps a torus with virtual cut-through deadlock-free with one virtual channel by asking for room for two packets when a packet enters a ring
  - paper: "Lionel M. Ni and Philip K. McKinley, A survey of wormhole routing techniques in direct networks, IEEE Computer 26(2) (1993), 62-76"
    locator: the comparison of store-and-forward, virtual cut-through, circuit switching and wormhole routing
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 12, buffered flow control (packet-buffer flow control, store-and-forward and cut-through, and their latency), and Chapter 14, deadlock and livelock
---

**Virtual cut-through** (VCT) is a switching method in which a router starts to send a packet on before it has received all of it, as soon as the head is routed and the next channel is free. So, without contention, a packet crosses the network with the low latency of [wormhole routing](/wormhole-routing/): about the number of hops plus the packet length. The difference is in the buffers and the rule for taking a channel. Each channel has a buffer for at least one whole packet, and a packet takes the next channel only when that buffer has room for all of it. If the head is blocked, the rest of the packet keeps flowing into the router where the head waits, and the packet then sits there whole, like a packet under [store-and-forward](/store-and-forward/) switching. A blocked packet holds one buffer, not a chain of channels. Kermani and Kleinrock proposed it in 1979 for computer networks; it is used in many torus networks of supercomputers and in cut-through Ethernet switches.

## In plain words

A train goes through a station without stopping if the track ahead is clear. Each station has a siding that is long enough for a full train. If the track ahead is busy, the whole train pulls into the siding of the station where it had to stop, and the track behind it is clear again for others.

So when traffic is light, the train is as fast as one that never stops. When traffic is heavy, it waits in one place and does not block the track behind it. The price is that each station needs a siding for a full train.

## When it applies

- Latency at light load matters, as in wormhole routing, but a blocked packet must not block other traffic over several routers.
- Packets have a bounded and fairly small length, so a router can afford a buffer for one or a few whole packets per channel.
- The analysis or the hardware wants packet-level behavior: in the worst case each router holds whole packets, so queueing and deadlock arguments for store-and-forward networks carry over.
- Switches whose input and output links have the same speed, where the switch can look at the header and start to transmit before the frame has arrived.

## The template

The holes are ROUTE, the routing function for a head, and ARBITRATE, the rule that picks one packet when several want the same channel. Buffers are counted in flits, and each holds at least one packet of the largest size $L$.

```pseudo id=main
VCT-ROUTER-CYCLE()                         ▷ runs in every router in every cycle
L1  for each input buffer c whose front flit is a head that has waited t_r cycles do
L2      o ← ROUTE(the destination in the head, this node)
L3      if channel o is free and the buffer at the far end of o has room for the whole packet
L4          and ARBITRATE picks c then give o to the packet in c
L5  for each input buffer c whose packet holds an output channel o do
L6      send the front flit of c on o              ▷ room is sure: it was checked at L3
L7      if this flit is the tail then free o
L8  each input buffer keeps taking the flits that arrive for it, even while its head waits
```

**Walk-through.** The only change from the [wormhole](/wormhole-routing/) template is the test at L3: wormhole routing needs one free flit slot, virtual cut-through needs room for the whole packet. Because of that test, once a packet holds channel $o$, all its flits can enter the next buffer, so the flits behind a blocked head do not stall in the routers upstream (L8). The packet frees each channel as its tail crosses it (L7). A blocked packet ends up whole in the buffer where its head waits, and every channel behind it is free.

**Latency.** Without contention, let a packet of $L$ flits cross $H$ links, one flit per link per cycle, with a routing delay of $t_r$ at each of the $H - 1$ routers on the way. Then

$$T_{\text{VCT}} = H + (H - 1)\,t_r + L - 1, \qquad T_{\text{store-and-forward}} = H L + (H - 1)\,t_r,$$

the same as wormhole routing, with a saving of $(H - 1)(L - 1)$ cycles over store-and-forward. If the head is blocked at a router for at least $L$ cycles, the whole packet arrives there, and from that router on the packet starts again as if it were new. If the packet is blocked at every router, VCT behaves exactly like store-and-forward. Kermani and Kleinrock's queueing analysis gives the same picture for whole networks: at light load the delay is much lower than with store-and-forward, and as the load grows the delay of VCT tends to that of store-and-forward.

## Classic examples

- **Contrast with [wormhole routing](/wormhole-routing/).** On the line $0 - 1 - 2 - 3 - 4$, a long packet holds the link $3 \to 4$ until cycle 41, and an 8-flit packet A from 0 to 4 waits behind it. A packet B from 1 to 2 enters at cycle 30; alone it needs 9 cycles. A flit-level simulation for this page gave: with virtual cut-through and 8-flit buffers, A sat whole in the buffer at node 3, and B left the network at cycle 39, with no delay. With wormhole routing and 2-flit buffers, A held the channels $0 \to 1$, $1 \to 2$ and $2 \to 3$, and B left at cycle 57. The same simulation gave 22 cycles for $H = 4$, $L = 16$, $t_r = 1$ without contention under both methods, and 67 cycles under [store-and-forward](/store-and-forward/).
- **Torus networks with [dimension-order routing](/dimension-order-routing/).** VCT needs fewer deadlock tools than wormhole routing. On a 4-node one-way ring, two packets with 3-hop routes, from 0 to 3 and from 2 to 1, each with 8 flits, deadlocked under wormhole routing with 2-flit buffers, but under VCT each packet waited whole in one buffer and both were delivered after 19 cycles. Four packets that each go two hops ahead, one from each node, still deadlocked under VCT, because every buffer on the ring was full. Two virtual channels with the dateline rule fixed it: the packets were delivered after 17, 25, 33 and 41 cycles. Bubble flow control is a cheaper fix for VCT tori: a packet may enter a ring only if the buffer there has room for two packets, so the ring is never full.
- **Cut-through Ethernet and data center switches.** A cut-through switch reads the destination address, looks it up, and starts to send the frame on the output while the rest still arrives. When the output is busy, the frame is stored in the switch, as in VCT. This lowers the latency per switch from the frame time to the header time, which matters in low-latency data center and trading networks. The scheduler of an [input-queued switch](/switch-scheduling/) must then match inputs to outputs while frames are still arriving.
- **[Deadlock prevention](/deadlock-prevention/) for packet buffers.** Because a VCT packet holds only buffers, not chains of channels, the deadlock analysis is the one for store-and-forward networks: number the buffer classes so that every packet asks for buffers in increasing order, or keep an empty buffer in each cycle of the dependency graph.

## Variations

- **Store-and-forward** is VCT with the cut-through removed: the head may take the next channel only when the tail has arrived.
- **[Wormhole routing](/wormhole-routing/)** is VCT with flit-sized buffers: the head may take the next channel when one flit slot is free, and a blocked packet stays spread over several routers.
- **Buffered wormhole and partial cut-through.** Buffers between one flit and one packet; a blocked packet holds fewer channels as buffers grow. A packet of $L$ flits frees the channels behind it only when one buffer holds all $L$ flits.
- **Virtual channels with packet buffers.** Several packet-sized buffers per link, used as virtual channels to break deadlock cycles (datelines) or to separate traffic classes.
- **Bubble flow control.** On a ring, a packet may enter or change dimension only if the next buffer has room for two packets; packets that stay in the ring need room for one. This keeps one free packet buffer in every ring and avoids deadlock without a second virtual channel.
- **Adaptive routing with an escape channel.** Packets route adaptively on some buffers and fall back to a deadlock-free routing, such as dimension-order routing with bubble flow control, on an escape buffer.

## Pitfalls

- **Buffers must hold the largest packet.** If a packet can be longer than the buffer, the method is no longer VCT: a blocked long packet spreads over several routers as in wormhole routing, and the deadlock analysis for packet buffers no longer holds. Limit the packet size, or split long messages.
- **VCT is not deadlock-free by itself.** It removes the cycles that come from packets spread over several routers, but packets can still fill all buffers in a cycle. The 4-node ring above is an example. Use an acyclic buffer order, virtual channels, or bubble flow control.
- **Heavy load.** When most packets block, VCT has the latency of store-and-forward. The gain is at light and medium load.
- **Error checks.** A cut-through router sends the start of a packet before it has seen the checksum at the end, so a damaged packet travels on. The destination must check it. A switch that finds a bad checksum at the end of a frame can only count it, or mark the frame as bad on its way out; it cannot drop a frame whose start it has already sent.
- **Speed mismatch.** If the output link is faster than the input link, the output would run out of data in the middle of a packet. Such a switch must buffer the whole packet, or wait until enough of it has arrived.

## Exercises

1. Show that VCT never has a larger latency than store-and-forward for the same packet, the same route and the same sequence of channel grants.
2. In the line example, packet B is delayed under wormhole routing with buffers of 2 to 7 flits, and not delayed with 8-flit buffers. Explain the value 8.
3. On a one-way ring of $k$ nodes with one packet buffer per channel, show that $k$ packets can deadlock under VCT, and that $k - 1$ packets cannot.

## References
