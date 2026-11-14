---
tag: KTPTAC
kind: technique
slug: latency-insensitive-design
name: Latency-insensitive design
aliases:
- relay station insertion
- Carloni latency-insensitive protocol
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Carloni, McMillan and Sangiovanni-Vincentelli's method that wraps blocks in shells with valid and stop signals so long wires can take relay stations without changing behaviour.
prereqs: [finite-state-machine-with-datapath, petri-net, minimum-mean-cycle-problem]
see_also: [karp-minimum-mean-cycle, minimum-ratio-problem, timed-event-graph, interface-synthesis, iteration-bound, retiming, queue, synchronous-dataflow]
sources:
  - paper: doi:10.1109/43.945302
    title: Luca P. Carloni, Kenneth L. McMillan and Alberto L. Sangiovanni-Vincentelli, Theory of latency-insensitive design, IEEE Transactions on Computer-Aided Design 20(9), 1059 to 1076, 2001
    locator: whole paper (patient processes, shells and relay stations, and the equivalence of a latency-insensitive system with the original one up to stalling)
  - paper: doi:10.1145/337292.337441
    title: Luca P. Carloni and Alberto L. Sangiovanni-Vincentelli, Performance analysis and optimization of latency insensitive systems, Proceedings of the 37th Design Automation Conference, 2000
    locator: whole paper (the throughput of a system with relay stations on its cycles)
  - paper: "Rebecca L. Collins and Luca P. Carloni, Topology-based performance analysis and optimization of latency-insensitive systems, IEEE Transactions on Computer-Aided Design 27(12), 2008"
    locator: whole paper (marked graph models with finite queues and back pressure, and queue sizing)
  - paper: "C. V. Ramamoorthy and Gary S. Ho, Performance evaluation of asynchronous concurrent systems using Petri nets, IEEE Transactions on Software Engineering SE-6(5), 440 to 449, 1980"
    locator: whole paper (the cycle time of a timed marked graph is the largest ratio of delay to tokens over its cycles)
---

Latency-insensitive design is a way to build a synchronous chip so that the wires between its blocks may take any number of clock cycles without changing what the chip computes. Carloni, McMillan and Sangiovanni-Vincentelli (2001) wrap each block, a *pearl*, in a *shell* that passes data with a valid bit and stalls the pearl when an input is missing or an output is blocked, using a *stop* signal that flows backwards. A long wire can then be cut by *relay stations*, small two-place buffers that add one cycle each, after placement and routing, when the wire delays are known. The data streams stay the same, only shifted in time. The price is throughput: on a cycle of the block graph with $S$ shells and $R$ relay stations, only $S$ valid data circulate in $S + R$ stages, and the system throughput is the least of $S/(S + R)$ over all cycles, a minimum cycle ratio.

## In plain words

On a big chip, a signal may need more than one clock tick to cross from one block to another, and this is often found out only at the end of the design. Latency-insensitive design plans for it. Each block gets a wrapper that only lets the block work when all its inputs have fresh data and its outputs have room. Every wire carries a flag that says whether the data on it is real or empty. If a wire is too long, we cut it with small holding stations that add one tick. The blocks still see the same numbers in the same order, just later. In a loop of blocks, the empty slots added by the stations slow the whole loop down.

## When it applies

- A synchronous design whose blocks are *patient*: a block can be stalled for a cycle and resume with the same state, for example by gating its clock or by a hold enable on its registers.
- The communication between blocks is point to point, through channels that carry data and could tolerate extra delay if the receiver waits for it.
- Wire delays are known only after placement and routing, or change between technology versions, and redesigning the blocks for each change is too costly.
- The loss of throughput on the cycles of the block graph is acceptable, or the design has few cycles.

## The template

Model the design as a directed graph whose vertices are the pearls and whose arcs are the channels.

```pseudo id=main
LATENCY-INSENSITIVE(G, the clock period T, the wire delays)
L1  for each pearl P: make P patient, so that a stall input freezes its state for one cycle
L2  wrap P in a shell: a queue on each input channel, a valid bit on each output, and a stop signal back to each sender
L3  the shell fires P in a cycle exactly when every input queue has a valid datum and no output receives stop
L4  place and route the design and measure the delay of each channel
L5  for each channel of delay D > T, insert ⌈D / T⌉ − 1 relay stations, each a two-place buffer with valid and stop
L6  build the marked graph of the system and compute θ = the minimum over cycles of tokens / stages
L7  if θ is too low then move relay stations off the critical cycles, enlarge queues, or change the floorplan, and go to L4
L8  return the system
```

The holes are the shell protocol of L2 and L3, the size of the queues, and the choices of L7.

**Why the behaviour does not change.** A shell fires its pearl only on valid inputs, and a relay station passes valid data in order and only drops the empty slots. So each pearl sees, on each input, the same sequence of valid data as in the original design, with empty cycles in between, and produces the same sequence of valid outputs. Carloni, McMillan and Sangiovanni-Vincentelli call two such systems *latency equivalent*: they agree on the valid data of every signal, in order, and differ only in the timing.

**The marked graph.** Each shell and each relay station is a stage that takes one cycle. Each channel segment between two stages is an arc with tokens: an arc out of a shell starts with 1 token, the valid datum in the shell's output register, and an arc out of a relay station starts with 0 tokens, since relay stations start empty. A stage fires when every incoming arc has a token. Firing removes one token from each incoming arc and, one cycle later, adds one to each outgoing arc. Each stage fires at most once per cycle, which is a self-loop with 1 token. With unbounded queues this is a timed [marked graph](/petri-net/), a Petri net in which each place has one input and one output transition, also called a [timed event graph](/timed-event-graph/).

**Theorem (throughput).** Let the graph be strongly connected, and for a cycle $C$ let $M(C)$ be its tokens and $L(C)$ its number of stages. In the schedule in which every stage fires as soon as it can, every stage fires $\theta T' + O(1)$ times in the first $T'$ cycles, with
$$\theta = \min_C \frac{M(C)}{L(C)}.$$
For a cycle of $S$ shells and $R$ relay stations, $M(C) = S$ and $L(C) = S + R$.

*Proof.* The total of the tokens on a cycle never changes, since each firing of a stage on the cycle takes one token from its incoming arc on the cycle and puts one on its outgoing arc on the cycle. Let $N_v(t)$ be the number of firings of stage $v$ in cycles $0, \ldots, t$. For an arc $(u, v)$ with $m$ initial tokens, the firings of $v$ up to cycle $t$ use tokens that were there at the start or produced by $u$ up to cycle $t - 1$, so $N_v(t) \le N_u(t - 1) + m$. Adding this around a cycle $C$ through $v$ gives $N_v(t) \le N_v(t - L(C)) + M(C)$, so $v$ fires at most $M(C)$ times in any $L(C)$ consecutive cycles, and the rate is at most $M(C)/L(C)$ for every cycle, hence at most $\theta$.

For the other direction, give each arc the weight $m(u, v) - \theta$. Every cycle has weight $M(C) - \theta L(C) \ge 0$, so there is no negative cycle and shortest path potentials $d$ exist with $d(v) \le d(u) + m(u, v) - \theta$ on every arc. Set $\pi = -d$ and fire $v$ for the $k$-th time, $k \ge 1$, in cycle $\tau_v(k) = \lceil (k + \pi(v)) / \theta \rceil + c$, with a constant $c$ that makes all these times nonnegative. On an arc $(u, v)$, the $k$-th firing of $v$ needs the $(k - m)$-th firing of $u$ to happen at least one cycle earlier when $k > m$. From $\pi(u) - \pi(v) \le m - \theta$ we get $(k + \pi(v))/\theta \ge (k - m + \pi(u))/\theta + 1$, and taking ceilings keeps the gap of 1. The self-loops give $\theta \le 1$, so successive firings of one stage are at least one cycle apart. So this periodic schedule is feasible, and it fires every stage about $\theta T'$ times in $T'$ cycles. The as-soon-as-possible schedule fires every stage no later than any feasible schedule, by induction on the firings, so it reaches at least the same count. $\square$

Since every stage takes one cycle, $L(C)$ is the number of arcs of $C$, and $\theta$ is the least mean token count per arc over all cycles. It is computed by [Karp's minimum mean cycle algorithm](/karp-minimum-mean-cycle/) in $O(nm)$ time, or by the search of the [minimum ratio problem](/minimum-ratio-problem/). If the graph has no cycle except the self-loops, $\theta = 1$: relay stations on an acyclic design add latency but cost no throughput.

**Finite queues.** With a queue of capacity $q$ on a channel, the stop signal blocks the sender when the queue is full. In the marked graph this is a reverse arc from the receiver to the sender with $q - m$ tokens, the free places, where $m$ is the initial tokens of the forward arc. The theorem applies to the graph with the reverse arcs, which is strongly connected even when the design is acyclic.

## Classic examples

**A ring of three shells.** Shells $A$, $B$ and $C$ form a ring $A \to B \to C \to A$, and routing puts one relay station on $A \to B$ and one on $B \to C$. The only cycle has $S = 3$ and $R = 2$, so $\theta = 3/5$: in every 5 cycles, each shell does 3 cycles of useful work. A simulation of the as-soon-as-possible firing gives exactly 3 firings per 5 cycles in steady state. Both wires are long, so neither relay station can be removed. A ring of 6 shells with the same two relay stations would have $\theta = 6/8 = 3/4$.

**Reconvergent paths and queue size.** Shell $A$ sends to shell $B$ on two channels, one direct and one through a relay station $R$. With unbounded queues the design is acyclic and $\theta = 1$. With queues of capacity $q$, the reverse arcs create cycles. The cycle $A \to R \to B \to A$, using the forward arcs through $R$ and the reverse arc of the direct channel, has $1 + 0 + (q - 1) = q$ tokens on 3 arcs. The other cycles, such as $A \to B \to A$ with $q$ tokens on 2 arcs, give $q/2$ or more. So $\theta = \min(1, q/3)$: $1/3$ for $q = 1$, $2/3$ for $q = 2$ and $1$ for $q = 3$. The short path fills its queue while $B$ waits for the datum on the long path, and the stop signal then stalls $A$. Simulation of the firing gives the same three values.

**A pipeline.** A chain of shells with any number of relay stations and queues of capacity 2 has, on each pair of forward and reverse arcs, $2$ tokens on 2 arcs, so $\theta = 1$. This is why relay stations hold two places: a one-place station on a channel would give a cycle of 1 token on 2 arcs and halve the throughput.

## Variations

- **Synchronous elastic circuits.** Later work by Cortadella, Kishinevsky and others uses the same valid and stop handshake at the level of single registers, with simpler controllers.
- **Queue sizing.** Choose the queue capacities to reach $\theta = 1$ on all cycles created by back pressure, with the least total size, as in Collins and Carloni (2008).
- **Recycling.** Add relay stations on short paths of reconvergent structures to balance them, which can raise the throughput when queues are small, at the cost of latency.
- **Pipelining the pearls.** Combine relay station insertion with [retiming](/retiming/), which moves registers across the logic to spread the delay of long paths.
- **Dataflow view.** Shells with valid and stop signals implement a dataflow network, close to [synchronous dataflow](/synchronous-dataflow/) graphs with unit rates and to the [iteration bound](/iteration-bound/) of DSP loops.

## Pitfalls

- **Pearls that are not patient.** A block with internal timing assumptions, such as a memory with a fixed read latency, breaks when stalled unless its shell handles it.
- **Combinational stop paths.** The stop signal runs backwards through the shells. If each shell passes it on without a register, it forms a long combinational path that defeats the purpose. Relay stations with two places break it.
- **Relay stations on tight cycles.** One relay station on a cycle of two shells drops the throughput to $2/3$. Place blocks so that the critical cycles have short wires.
- **Initial tokens.** A cycle with no valid token at the start never fires. Every cycle of the original design passes through a register, which gives it a token.
- **Off-chip interfaces.** The environment must follow the protocol too, or a [protocol converter](/interface-synthesis/) is needed at the chip boundary.

## Exercises

1. A ring of 4 shells has relay stations on 3 of its channels. What is $\theta$, and how many relay stations can a ring of 4 shells take before the throughput falls below $1/2$?
2. Prove that in a marked graph the token count of every cycle is constant over time.
3. In the reconvergent example, put a second relay station on the long path. Find $\theta$ as a function of $q$, and the least $q$ that gives $\theta = 1$.
4. Show that for an acyclic design with unbounded queues, the latency from input to output grows by the number of relay stations on the longest path, while $\theta$ stays 1.

## References
