---
tag: 88G93M
kind: technique
slug: wormhole-routing
name: Wormhole routing
aliases:
- wormhole switching
- wormhole flow control
area: systems/networking-algorithms
level: intro
summary: "Split a packet into flits and send each flit on as soon as the head has its next channel. Buffers hold a few flits, so a blocked packet holds channels across several nodes."
prereqs: [store-and-forward, deadlock]
see_also: [virtual-cut-through, store-and-forward, dimension-order-routing, deadlock-prevention, lock-ordering, valiant-routing, flow-control, livelock]
sources:
  - paper: doi:10.1007/BF01660031
    title: "William J. Dally and Charles L. Seitz, The torus routing chip, Distributed Computing 1(4) (1986), 187-196"
    locator: wormhole routing in a self-timed router chip for a torus, with two virtual channels per link to break the cycles of the rings
  - paper: doi:10.1109/TC.1987.1676939
    title: "William J. Dally and Charles L. Seitz, Deadlock-free message routing in multiprocessor interconnection networks, IEEE Transactions on Computers C-36(5) (1987), 547-553"
    locator: the channel dependency graph and the theorem that a deterministic routing function is deadlock-free if and only if the graph is acyclic, stated for wormhole routing
  - paper: doi:10.1109/71.127260
    title: "William J. Dally, Virtual-channel flow control, IEEE Transactions on Parallel and Distributed Systems 3(2) (1992), 194-205"
    locator: several virtual channels with separate flit buffers on one physical link, so that a blocked packet does not stop the link, and the throughput gain over plain wormhole flow control
  - paper: "Lionel M. Ni and Philip K. McKinley, A survey of wormhole routing techniques in direct networks, IEEE Computer 26(2) (1993), 62-76"
    locator: the latency of wormhole routing against store-and-forward, deadlock, and routing algorithms for meshes and hypercubes
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 12, buffered flow control (store-and-forward, cut-through, wormhole and virtual-channel flow control), Chapter 13, flow control mechanics (credits), and Chapter 14, deadlock and livelock
---

**Wormhole routing** is a way to move packets through a network of routers with very little buffer space. The packet is cut into **flits** (flow control digits), a few bits to a few bytes each. The first flit, the **head**, carries the destination. Each router routes the head as soon as it arrives and sends it on; the body flits follow the head in a line, and the last flit, the **tail**, frees each channel as it passes. A router needs buffers for only a few flits per channel, not for whole packets. Without contention, the latency is about the number of hops plus the packet length, not their product as in [store-and-forward](/store-and-forward/) switching. The cost is that a packet whose head is blocked stays spread over several routers and holds all the channels under it, which can block other packets and can cause [deadlock](/deadlock/). [Virtual cut-through](/virtual-cut-through/) has the same latency without contention but buffers a blocked packet in one router.

## In plain words

Think of a long train on a track that is cut into short blocks. Each block can hold only two cars. The engine goes ahead as soon as the next block is free, and the cars follow. When the engine must stop, the cars stop too, and the train stays spread over many blocks. No other train can use those blocks until this train moves on.

Compare a train that must stop fully inside each station before it may go on. That train is slow, because it must wait for its last car at every station. The long train in short blocks is fast when the track is clear, but it can jam the track when it is not.

## When it applies

- The network has many small routers, as in multicomputers, supercomputers and networks on chip, where buffer memory is the main cost and latency must be low.
- Packets are short or medium, so a packet spread over a few routers is acceptable.
- The routing function can be made deadlock-free, for example with [dimension-order routing](/dimension-order-routing/) on a mesh, or with virtual channels on a torus.
- The links have link-level flow control (credits or on/off signals), so a flit is sent only when the next buffer has room. This is [flow control](/flow-control/) applied to one link, at flit level.

## The template

The holes are ROUTE, the routing function that gives the next channel for a head flit, and ARBITRATE, the rule that picks one packet when several heads want the same free channel.

```pseudo id=main
WORMHOLE-ROUTER-CYCLE()                    ▷ runs in every router in every cycle
L1  for each input channel c whose front flit is a head that has waited t_r cycles do
L2      o ← ROUTE(the destination in the head, this node)
L3      if channel o is free and ARBITRATE picks c then give o to the packet in c
L4  for each input channel c whose packet holds an output channel o do
L5      if o has a credit (a free flit slot in the next router) then
L6          send the front flit of c on o; use one credit
L7          if this flit is the tail then free o
L8  for each flit that left an input buffer, send a credit back to the router upstream
```

**Walk-through.** Lines L1 to L3 handle the head: after a routing delay of $t_r$ cycles, the router finds the next channel and gives it to the packet if no other packet holds it. The packet then holds that channel until its tail has crossed it (L7). Lines L4 to L6 move one flit per channel per cycle, and only when the next buffer has room. Line L8 is credit-based flow control: each router knows how many free slots the next buffer has, so no flit is ever dropped. A packet blocked at its head simply stops: its flits stay in the buffers along its path, and its channels stay held.

**Latency without contention.** Let a packet of $L$ flits cross $H$ links, one flit per link per cycle, with a routing delay of $t_r$ cycles at each of the $H - 1$ routers on the way. The head crosses the last link at cycle $H + (H - 1) t_r$, and the tail follows $L - 1$ cycles later, so

$$T_{\text{wormhole}} = H + (H - 1)\,t_r + L - 1, \qquad T_{\text{store-and-forward}} = H L + (H - 1)\,t_r.$$

Store-and-forward waits for all $L$ flits at each hop, so it pays $L$ per hop. The difference is exactly $(H - 1)(L - 1)$ cycles. For $H = 4$, $L = 16$, $t_r = 1$: wormhole takes 22 cycles and store-and-forward 67, a saving of $3 \cdot 15 = 45$ cycles. A flit-level simulation for this page gave these numbers, and it matched both formulas for every case we tried.

## Classic examples

- **[Dimension-order routing](/dimension-order-routing/) on meshes and hypercubes.** E-cube routing with wormhole switching was the network of the second generation of hypercube and mesh multicomputers. The order of dimensions gives a channel numbering that grows along each route, so a packet spread over many channels cannot be part of a cycle of waits.
- **Tori with virtual channels.** On a ring, wormhole packets can wait for each other in a circle. In our simulation of a 4-node one-way ring where each node sends an 8-flit packet two hops ahead, with 2-flit buffers, all four packets held their first channel and waited for the next one forever. With two virtual channels and the dateline rule of [dimension-order routing](/dimension-order-routing/), the same packets were delivered after 11, 19, 27 and 35 cycles. The Torus Routing Chip of Dally and Seitz used this method.
- **[Deadlock prevention](/deadlock-prevention/) by channel order.** The channel dependency graph of Dally and Seitz is the resource-allocation view of wormhole routing: channels are resources, and a packet holds some while it asks for the next. A global numbering of channels is [lock ordering](/lock-ordering/) for the network.
- **[Valiant's routing](/valiant-routing/) with wormhole switching.** Randomized two-phase routing spreads the load, and wormhole switching keeps the latency low. Each phase needs its own set of virtual channels, or the two phases can form cycles of waits.
- **Networks on chip.** Most on-chip meshes in many-core processors use wormhole or virtual-channel flow control with XY routing, because buffers take chip area and power.

## Variations

- **Virtual-channel flow control** (Dally 1992). Each physical link has several virtual channels, each with its own small flit buffer. A blocked packet holds only one virtual channel, and other packets pass it on the same wire. Virtual channels also break deadlock cycles (datelines, escape channels) and separate traffic classes.
- **[Virtual cut-through](/virtual-cut-through/).** Each channel buffer holds a whole packet, and a head takes the next channel only if the next buffer can take the whole packet. A blocked packet then collapses into one router and frees the channels behind it.
- **Adaptive wormhole routing.** The turn model, Duato's escape channels and other methods let a head choose among several channels and stay deadlock-free.
- **Circuit switching** reserves the whole path first with a probe, then sends data. Wormhole routing reserves the path flit by flit, as the head moves.
- **Pipelined circuit switching and scouting switching** let the head move ahead of the data by a few links, so that it can back off from faults.

## Pitfalls

- **Blocking spreads.** In our simulation on the line $0 - 1 - 2 - 3 - 4$, a long packet held the link $3 \to 4$ until cycle 41, an 8-flit packet A from 0 to 4 waited behind it, and a packet B from 1 to 2 was injected at cycle 30. Alone, B needs 9 cycles. With wormhole routing and 2-flit buffers, A's flits sat in the channels $0 \to 1$, $1 \to 2$ and $2 \to 3$, and B left the network at cycle 57; with 4-flit buffers, at cycle 55. With virtual cut-through, A sat in one buffer at node 3, and B left at cycle 39, with no delay. Each extra flit of buffer cut B's finish time by only one cycle, until at 8 flits one buffer held all of A and the wormhole router behaved like virtual cut-through.
- **Deadlock.** Store-and-forward networks deadlock only when buffers fill, but wormhole packets hold channels while they wait for others, so any cycle in the channel dependency graph can deadlock. Make the routing function acyclic, or add virtual channels with an acyclic escape network.
- **Protocol deadlock.** A node that must send a reply before it can accept a request ties two packet types together. Requests and replies need separate virtual networks.
- **Head-of-line blocking at a channel.** With one buffer per link, a blocked packet stops every packet behind it on that link, even packets for free outputs. Virtual channels fix this.
- **Livelock with adaptive or misrouting variants.** A packet that may take non-minimal links can move forever. Limit misroutes, or use age-based priority. See [livelock](/livelock/).
- **Long packets.** The latency gain falls as $L$ grows against $H$, and a long blocked packet holds many channels. Split long messages into several packets.

## Exercises

1. Show that the formulas above give the same latency for wormhole routing and store-and-forward when $H = 1$ or $L = 1$, and explain why.
2. On a one-way ring of 4 nodes, each node sends a packet of 8 flits two hops ahead, and each buffer holds 2 flits. Show that wormhole routing can deadlock, and that two virtual channels with the dateline rule remove the deadlock.
3. On a one-way ring of 4 nodes, find two packets with minimal routes that can deadlock under wormhole routing with 2-flit buffers.

## References
