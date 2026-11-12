---
tag: RHGNKB
kind: algorithm
slug: dimension-order-routing
name: Dimension-order routing
aliases:
- XY routing
- e-cube routing
area: systems/networking-algorithms
level: intro
summary: "Route a packet along one dimension at a time, in a fixed order. Paths are shortest on meshes and hypercubes, and no deadlock is possible there; a torus needs two virtual channels."
solves: [routing-problem]
model: word-ram
complexity:
  vars: {n: the number of dimensions}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1987
  people: [Herbert Sullivan, T. R. Bashkow, William J. Dally, Charles L. Seitz]
  note: Sullivan and Bashkow described e-cube routing for hypercube machines in 1977. Dally and Seitz proved in 1987 that it is deadlock-free and showed how virtual channels make it deadlock-free on tori.
prereqs: [routing-problem, deadlock]
see_also: [wormhole-routing, virtual-cut-through, deadlock-prevention, valiant-routing, oblivious-routing, permutation-routing, store-and-forward, benes-network-routing]
sources:
  - paper: doi:10.1109/TC.1987.1676939
    title: "William J. Dally and Charles L. Seitz, Deadlock-free message routing in multiprocessor interconnection networks, IEEE Transactions on Computers C-36(5) (1987), 547-553"
    locator: the channel dependency graph, the theorem that a deterministic routing function is deadlock-free if and only if its dependency graph is acyclic, e-cube routing on the hypercube, and virtual channels for the torus
  - paper: "Herbert Sullivan and T. R. Bashkow, A large scale, homogeneous, fully distributed parallel machine, I, Proceedings of the 4th Annual Symposium on Computer Architecture (1977), 105-117"
    locator: the e-cube routing rule for the binary hypercube
  - paper: doi:10.1145/185675.185682
    title: "Christopher J. Glass and Lionel M. Ni, The turn model for adaptive routing, Journal of the ACM 41(5) (1994), 874-902"
    locator: dimension-order routing as the routing that forbids all turns from a higher to a lower dimension, and partially adaptive deadlock-free alternatives such as west-first
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 8, routing basics (dimension-order routing on tori and meshes), and Chapter 14, deadlock and livelock (channel dependency graphs, dateline virtual channels)
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Section 1.7, packet routing on arrays (the greedy row-first algorithm), and Chapter 3, routing on the hypercube by bit-fixing
---

Dimension-order routing sends a packet through a grid-shaped network one dimension at a time, in a fixed order. On a two-dimensional mesh this is **XY routing**: first move along the row until the column of the destination, then along the column. On a hypercube it is **e-cube routing**: flip the differing address bits in a fixed order. Each route is a shortest path, the router needs only a few comparisons per hop, and the routing is [oblivious](/oblivious-routing/): the path depends only on the source and the destination. Its key property is that it cannot [deadlock](/deadlock/) on a mesh or hypercube, even with [wormhole routing](/wormhole-routing/) and small buffers, because the order of dimensions puts the channels in an order that every packet climbs. On a torus the wrap-around links break this order, and two virtual channels per link restore it.

## In plain words

Think of a city laid out in a grid. To reach an address, first drive east or west until you reach the right street, then drive north or south until you reach the right house. Never turn back to east or west after you start going north or south.

This rule makes every route as short as possible. It also stops a traffic jam that goes in a circle. In such a jam, each car waits for the car in front, all the way around a block. A full circle around a block needs some car to turn from north or south back to east or west, and the rule forbids that turn. So the line of waiting cars always ends at a car that can move.

## The problem

The network is a $k$-ary $n$-dimensional mesh: nodes are vectors $(x_0, \ldots, x_{n-1})$ with $0 \le x_d < k$, and a link joins nodes that differ by 1 in one coordinate. A **torus** adds wrap-around links between coordinate $k - 1$ and 0. A **hypercube** is the mesh with $k = 2$. Each router must decide, from the packet's current node $c$ and destination $t$, which output link to use next, so that every packet reaches its destination and no set of packets can block each other forever.

## The algorithm

```pseudo id=main
DOR-NEXT-HOP(c, t)                        ▷ current node c, destination t, n dimensions
L1  for d ← 0 to n − 1 do                  ▷ the fixed order of dimensions
L2      if c[d] ≠ t[d] then
L3          if c[d] < t[d] then return the link of dimension d in the + direction
L4          else return the link of dimension d in the − direction
L5  return DELIVER                          ▷ c = t
```

On a hypercube, lines L3 and L4 both mean "flip bit $d$". On a torus, line L3 changes: go in the + direction when $(t[d] - c[d]) \bmod k \le k/2$, else in the − direction, so the route takes the shorter way around each ring (ties go +). On a torus, each link also has two virtual channels: a packet uses VC 0 when it starts in a dimension and VC 1 after it crosses the **dateline**, the wrap-around link of that ring.

## Example

On a $4 \times 4$ mesh, a packet from $(0, 0)$ to $(3, 2)$ takes $+X, +X, +X, +Y, +Y$: three hops along dimension 0, then two along dimension 1. That is 5 hops, the distance. A packet from $(3, 2)$ to $(0, 0)$ takes $-X$ three times, then $-Y$ twice.

**Why the order matters.** On a $3 \times 3$ mesh, suppose some packets use XY and others use YX. Then four packets can sit around one unit square: one holds $+X$ out of $(0,0)$ and wants $+Y$ out of $(1,0)$; one holds that and wants $-X$ out of $(1,1)$; one holds that and wants $-Y$ out of $(0,1)$; and one holds that and wants $+X$ out of $(0,0)$. The [channel dependency graph](/deadlock-prevention/) of the mixed routing has this 4-cycle, and with full buffers it is a deadlock. With XY alone, the turns $+Y \to -X$ and $-Y \to +X$ never happen, and the graph has no cycle. For the $4 \times 4$ mesh the graph has 48 channels and 68 dependencies, and no cycle.

**The torus.** On a ring of 4 nodes with minimal routing, the packet from 0 to 2 holds the channel $0 \to 1$ and wants $1 \to 2$; the packet from 1 to 3 holds $1 \to 2$ and wants $2 \to 3$; and so on around the ring. These four dependencies form a cycle, so four packets can deadlock. The implementation finds such a cycle for rings of 4, 5 and 6 nodes. On a ring of 3 nodes every minimal route has one hop, so there is no cycle. With the dateline rule, the $4 \times 4$ torus has 72 channels in use and no cycle, and the same holds for $5 \times 5$, $6 \times 6$ and $7 \times 7$.

## Correctness

**Delivery on a shortest path.** Each hop moves the first differing coordinate one step toward its target, so the sum $\sum_d |c[d] - t[d]|$ falls by 1 per hop. The packet arrives after exactly that many hops, which is the distance in the mesh.

**No deadlock on a mesh.** Number the channels of dimension $d$ in the range $[2kd, 2kd + 2k)$: the + channel out of coordinate $x$ gets $2kd + x$, the − channel gets $2kd + k + (k - 1 - x)$. Along every route the numbers strictly increase: within a dimension the packet moves one way, and later dimensions have higher ranges. Suppose a set of packets is deadlocked, each waiting for its next channel, which is full of packets of the set. A packet waits for a channel with a higher number than any channel it holds. Following the waits from packet to packet then gives strictly increasing channel numbers forever, which is impossible with finitely many packets. This is the "if" direction of the Dally-Seitz theorem: a deterministic routing function whose channel dependency graph has no cycle is deadlock-free. The dateline numbering for the torus is in the proof below.

## Complexity

- **Per hop.** The router compares at most $n$ coordinate pairs: $O(n)$ time, $O(1)$ extra space. In hardware the comparisons run in parallel, and the decision is a few gate delays. Routers often precompute the output port at the previous hop (lookahead routing).
- **Path length.** Exactly the mesh distance $\sum_d |s[d] - t[d]|$, at most $n(k-1)$. On a torus, the ring distance in each dimension, at most $n \lfloor k/2 \rfloor$.
- **Resources.** No routing tables: the router needs only its own coordinates. A torus needs two virtual channels per physical link.

## Properties

- **Deterministic and oblivious.** One fixed path per source and destination, which keeps packets of a flow in order.
- **Minimal.** Every route is a shortest path.
- **Deadlock-free on meshes and hypercubes** with any buffer size, and on tori with two virtual channels.
- **No path diversity.** It cannot route around a busy or broken link. On some permutations, such as transpose on a mesh or bit reversal on a hypercube, many routes share a few links and throughput drops.

## Variants and improvements

- **Turn model.** Glass and Ni (1994) showed that forbidding one turn in each cycle of a 2-D mesh, rather than all turns from Y to X, is enough. West-first, north-last and negative-first routing allow some adaptivity and stay deadlock-free.
- **Duato's protocol.** Dimension-order routing on an escape virtual channel, plus fully adaptive routing on other virtual channels, gives adaptive routing that is still deadlock-free.
- **O1TURN.** Pick XY or YX at random for each packet, each on its own virtual channel, which balances load better than one fixed order.
- **[Valiant's routing](/valiant-routing/).** Route by dimension order to a random intermediate node, then to the destination, to remove the bad cases of fixed order.
- **Hypercube bit-fixing order.** Fixing bits from the most significant down, or from the least significant up, are both dimension-order routing with different orders; the bad permutations change with the order.

## When to use it

Use dimension-order routing in mesh and torus networks of parallel computers and in networks on chip, where routers must be small and fast and packets of a flow must stay in order. It is the default in many on-chip meshes. Add a randomized or adaptive scheme when the traffic has hot spots or adversarial patterns, or when links can fail.

## Pitfalls

- **Wrap-around links without virtual channels.** On a torus with rings of 4 or more nodes, plain dimension-order routing can deadlock. Use the dateline rule with two virtual channels, or avoid the wrap links.
- **Mixing orders on the same channels.** XY for some packets and YX for others creates cycles in the dependency graph. Each order needs its own virtual channels.
- **Ties on a torus.** When the two ways around a ring are equally long, the choice must be deterministic (for example, always +), or the analysis of the dependency graph must include both.
- **Deadlock at the endpoints.** The proof assumes that destinations consume packets. If a node can refuse a packet until it sends a reply, request and reply traffic need separate virtual networks.
- **Reading deadlock-free as fast.** Freedom from deadlock says nothing about congestion. Dimension-order routing has poor worst-case throughput on adversarial permutations.

## Implementations

## History

Sullivan and Bashkow described e-cube routing for the hypercube computers they proposed in 1977, and hypercube machines such as the Cosmic Cube and the Intel iPSC used it. Dally and Seitz (1987) introduced channel dependency graphs, proved that a deterministic routing function is deadlock-free exactly when its graph is acyclic, and used virtual channels to make dimension-order routing deadlock-free on tori, in the design of the Torus Routing Chip. Glass and Ni's turn model (1992 conference, 1994 journal) and Duato's theory of escape channels (1993) built adaptive routing on the same ideas.

## References
