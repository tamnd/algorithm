---
tag: MC25MW
kind: problem
slug: permutation-routing
name: Permutation routing
aliases:
- permutation routing on networks
- permutation packet routing
area: systems/networking-algorithms
level: advanced
summary: "Each node of a network sends one packet and receives one. Route all of them in few steps when each link carries one packet per step. A path set needs at least max(C, D) steps; O(C + D) suffice."
prereqs: [permutation, routing-problem, store-and-forward]
see_also: [valiant-routing, benes-network-routing, oblivious-routing, dimension-order-routing, bit-reversal-permutation, birkhoff-von-neumann-decomposition, sorting-network, mesh-sorting-problem]
sources:
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Section 1.7 (packet routing on linear and two-dimensional arrays, the greedy algorithm and its queue sizes) and Chapter 3 (routing on hypercubes and butterflies, the Beneš network, and randomized routing)
  - paper: doi:10.1137/0211027
    title: "Leslie G. Valiant, A scheme for fast parallel communication, SIAM Journal on Computing 11(2) (1982), 350-361"
    locator: randomized two-phase routing of any permutation on the hypercube in O(log N) steps with high probability
  - paper: doi:10.1016/0022-0000(85)90008-X
    title: "Allan Borodin and John E. Hopcroft, Routing, merging, and sorting on parallel models of computation, Journal of Computer and System Sciences 30(1) (1985), 130-145"
    locator: the lower bound for deterministic oblivious routing on networks of bounded degree
  - paper: doi:10.1007/BF02090400
    title: "Christos Kaklamanis, Danny Krizanc and Thanasis Tsantilas, Tight bounds for oblivious routing in the hypercube, Mathematical Systems Theory 24(4) (1991), 223-232"
    locator: the improved lower bound Ω(√N/d) on networks of degree d and an algorithm on the hypercube that meets it
  - paper: doi:10.1007/BF01215349
    title: "F. Thomson Leighton, Bruce M. Maggs and Satish B. Rao, Packet routing and job-shop scheduling in O(congestion + dilation) steps, Combinatorica 14(2) (1994), 167-186"
    locator: the existence of a schedule with O(C + D) steps and constant queues for any set of paths
  - paper: "F. Thomson Leighton, Fillia Makedon and Ioannis G. Tollis, A 2n-2 step algorithm for routing in an n x n array with constant-size queues, Algorithmica 14(4) (1995), 291-304"
    locator: permutation routing on the two-dimensional mesh in the distance bound of 2n - 2 steps with queues of constant size
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 4, the section Application, packet routing in sparse networks (permutation routing on the hypercube and the butterfly)
---

Permutation routing is the basic test of a communication network. Every node holds one packet, every node is the destination of exactly one packet, so the destinations form a [permutation](/permutation/), and all packets must reach their destinations. In the standard model time runs in synchronous steps and each link carries at most one packet per step. The question is how few steps are needed, how small the queues can stay, and whether the route of a packet may depend on the other packets. The answers differ by network: on the hypercube, plain bit-fixing needs about $\sqrt{N}/2$ steps on some permutations, but [Valiant's random intermediate nodes](/valiant-routing/) give $O(\log N)$. In a switching network such as the [Beneš network](/benes-network-routing/), the same problem asks for a setting of switches that gives every packet its own path.

## In plain words

Picture a group of towns joined by roads. Each town sends one truck, and each town gets one truck. A road can take only one truck at a time in each direction, and a trip on a road takes one hour. Trucks that want the same road must wait in line.

The task is to choose a road plan for every truck so that the last truck arrives soon. A plan that looks good for each truck alone can be bad for the group, because many trucks may want the same road. Good plans spread the trucks out, often with a random detour.

## Definition

**Network.** A directed graph $G = (V, E)$ with $N = |V|$ nodes. Usually each undirected link is two directed edges, one in each direction.

**Input.** A permutation $\pi$ of $V$. Node $v$ holds one packet with destination $\pi(v)$.

**Model (store-and-forward packet routing).** Time runs in synchronous steps. In each step each directed edge carries at most one packet. A packet at a node that cannot move yet waits in a queue there. Packets are not split or combined. This is the [store-and-forward](/store-and-forward/) model in which a whole packet crosses a link in one step.

**Output.** A schedule: for each packet, a path from $v$ to $\pi(v)$ and the step at which it crosses each edge, with at most one packet per edge per step.

**Measures.** The main measure is the number of steps $T$ until the last packet arrives. Secondary measures are the largest queue at a node, and the work of computing the schedule.

**Two parameters of a path set.** For a chosen set of paths, the **dilation** $D$ is the length of the longest path and the **congestion** $C$ is the largest number of paths that use one edge. Any schedule on those paths needs at least $\max(C, D)$ steps: the packet on the longest path needs $D$ steps, and the edge with $C$ paths can pass only one packet per step.

## Variants

- **Oblivious routing.** The path of each packet depends only on its source, its destination and, for randomized schemes, its own random bits. [Dimension-order routing](/dimension-order-routing/) is deterministic and oblivious; [Valiant's scheme](/valiant-routing/) is randomized and oblivious. See [oblivious routing](/oblivious-routing/).
- **Adaptive routing.** A packet may choose its next edge from the queues it sees.
- **Offline routing.** The whole permutation is known in advance, and a central algorithm computes the schedule.
- **Bounded queues.** Each node can hold only a constant number of packets.
- **Circuit switching.** Each packet needs a path of its own for its whole lifetime, with no shared edges. In a switching network this means setting the switches so that the paths are disjoint; a network that can do this for every permutation is *rearrangeable*. The [Beneš network](/benes-network-routing/) is the classic example.
- **Partial permutations and $h$-relations.** Some nodes send nothing, or each node sends and receives up to $h$ packets.
- **Wormhole and cut-through.** Long packets are split into flits that move in a pipeline, as in [wormhole routing](/wormhole-routing/) and [virtual cut-through](/virtual-cut-through/). The step count then depends on packet length as well as on path length.

## Examples

**Bit reversal on the hypercube.** On the $n$-dimensional hypercube with $N = 2^n$ nodes, node $x$ sends to the node whose address is $x$ with its bits in reverse order (the [bit-reversal permutation](/bit-reversal-permutation/)). Plain bit-fixing, which fixes the address bits from left to right, sends all packets that start at $a\,0^{n/2}$ with $a$ odd through one edge into node $0^n$. There are $\sqrt{N}/2$ of them, so this scheme needs at least $\sqrt{N}/2$ steps, while the diameter is only $n$. Measured with FIFO queues, it takes 21 steps for $N = 1024$ and 136 for $N = 65536$. Valiant's two-phase scheme takes 20 and 33 steps on the same inputs (seed 0). The transpose permutation, which swaps the two halves of the address, behaves the same way.

**Transpose on a mesh.** On a $\sqrt{N} \times \sqrt{N}$ mesh, the packet at $(i, j)$ goes to $(j, i)$. The packet at $(\sqrt{N}-1, 0)$ goes to $(0, \sqrt{N}-1)$, which is $2(\sqrt{N}-1)$ links away, so every algorithm needs $2\sqrt{N} - 2$ steps on this input. Row-first [dimension-order routing](/dimension-order-routing/) with farthest-first priority finishes within $2\sqrt{N} - 2$ steps on every permutation, but its queues can grow with $\sqrt{N}$.

**Beneš network, $N = 8$.** The permutation $(5, 7, 2, 4, 0, 6, 1, 3)$ is routed through the 20 switches of the 8-line Beneš network with no two packets on one link. The looping algorithm finds the settings in one pass over a single cycle of constraints, then recurses on two networks with 4 lines each. The details are on the [Beneš network routing](/benes-network-routing/) page.

## Known algorithms

| network | algorithm | steps | notes |
| --- | --- | --- | --- |
| hypercube, $N = 2^n$ | greedy bit-fixing | at least $\sqrt{N}/2$ on bit reversal and transpose | deterministic, oblivious; $n$ steps on the random permutations we measured |
| hypercube | [Valiant's two-phase routing](/valiant-routing/) | $O(n)$ with high probability | randomized, oblivious; at most $14n$ with probability $1 - 1/N$ |
| hypercube | deterministic oblivious routing of Kaklamanis, Krizanc and Tsantilas | $O(\sqrt{N}/n)$ | meets the lower bound for its class |
| hypercube | route by [sorting](/sorting-network/) on destination (Batcher's bitonic sort) | $O(n^2)$ | deterministic, not oblivious |
| $\sqrt{N} \times \sqrt{N}$ mesh | greedy [dimension-order routing](/dimension-order-routing/), farthest first | $2\sqrt{N} - 2$ | queues up to $\Theta(\sqrt{N})$ |
| $\sqrt{N} \times \sqrt{N}$ mesh | Leighton, Makedon and Tollis | $2\sqrt{N} - 2$ | constant queues; complex |
| any network, given paths | Leighton, Maggs and Rao | $O(C + D)$ | the schedule exists; later work made it constructive |
| Beneš network (circuit switched) | [looping algorithm](/benes-network-routing/) | one pass through $2\log_2 N - 1$ switch columns | offline set-up in $O(N \log N)$ time |

## Bounds

- **Distance and bisection.** On any network, $T \ge$ the largest distance $\mathrm{dist}(v, \pi(v))$, and $T \ge$ (number of packets that must cross a cut) / (number of edges across the cut). On the $\sqrt{N} \times \sqrt{N}$ mesh, the transpose gives $T \ge 2\sqrt{N} - 2$.
- **Path sets.** For a fixed set of paths, $\max(C, D) \le T$, and Leighton, Maggs and Rao (1994) proved that a schedule with $T = O(C + D)$ and constant queues always exists. So, for a given path set, the problem is to find paths with small $C + D$.
- **Deterministic oblivious routing.** Borodin and Hopcroft (1985) proved that every deterministic oblivious algorithm on a network of $N$ nodes and degree $d$ needs many steps on some permutation, about $\sqrt{N}$ divided by a power of $d$. Kaklamanis, Krizanc and Tsantilas (1991) improved the bound to $\Omega(\sqrt{N}/d)$, which on the hypercube ($d = n$) is $\Omega(\sqrt{N}/\log N)$, and gave an algorithm that matches it.
- **Randomized oblivious routing.** Valiant's scheme gives $O(\log N)$ on the hypercube with high probability, which matches the diameter up to a constant factor.
- **Circuit switching.** A rearrangeable network of $2 \times 2$ switches needs at least $\log_2 N! = N \log_2 N - O(N)$ switches, because it must have at least $N!$ settings. The Beneš network has $N \log_2 N - N/2$.

## Reductions

- **Sorting gives routing.** Sort the packets by destination address on the network; since the destinations form a permutation, after sorting each packet is at its destination. So a sorting algorithm on a network, such as [bitonic sort](/bitonic-sort/) on the hypercube or a [mesh sort](/mesh-sorting-problem/), is a deterministic permutation routing algorithm.
- **Any permutation to two random ones.** Valiant's scheme reduces a worst-case permutation to two routing problems with random destinations or random sources, which are easy for oblivious routing.
- **$h$-relations to permutations.** Any traffic pattern in which each node sends and receives at most $h$ packets splits into $h$ partial permutations, by [Kőnig's edge coloring theorem](/konig-theorem/), which is the integer form of the [Birkhoff-von Neumann decomposition](/birkhoff-von-neumann-decomposition/). So an algorithm for permutations handles $h$-relations with a factor $h$.
- **Scheduling.** For given paths, finding the schedule is a job-shop scheduling problem in which packets are jobs and edges are machines; Leighton, Maggs and Rao used this view.

## Applications

- **Parallel computers.** Data movement in parallel algorithms (matrix transpose, the fast Fourier transform, sorting) and the emulation of shared memory on a distributed-memory machine are permutation routing or $h$-relation routing.
- **Collective communication.** All-to-all exchange in message passing libraries is a sequence of permutations.
- **Interconnection networks and on-chip networks.** Router designers test networks with permutation traffic such as bit reversal, transpose and shuffle, which are the bad cases of simple routing functions.
- **Switch fabrics.** Each time slot of an input-queued [switch](/switch-scheduling/) is a partial permutation, and multistage fabrics such as the Beneš network realize it with few crosspoints.
- **Data center and backbone networks.** Valiant load balancing splits traffic over intermediate points to handle any traffic matrix in the network's capacity.

## References
