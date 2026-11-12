---
tag: 52M6P4
kind: problem
slug: switch-scheduling
name: Switch scheduling
aliases:
- input-queued switch scheduling
- crossbar scheduling problem
area: systems/networking-algorithms
level: advanced
summary: "In each time slot, pick a matching of inputs to outputs of an input-queued crossbar switch, so that the switch carries every admissible traffic load with bounded queues."
prereqs: [bipartite-matching, maximal-matching, maximum-weight-matching]
see_also: [parallel-iterative-matching, islip, birkhoff-von-neumann-decomposition, hungarian-algorithm, backpressure-routing, packet-scheduling, wireless-link-scheduling, konig-theorem]
sources:
  - paper: doi:10.1109/TCOM.1987.1096719
    title: "Mark J. Karol, Michael G. Hluchyj and Samuel P. Morgan, Input versus output queueing on a space-division packet switch, IEEE Transactions on Communications 35(12) (1987), 1347-1356"
    locator: the saturation throughput of FIFO input queueing under uniform Bernoulli traffic, 2 - sqrt(2) as N tends to infinity, and the table of values for small N
  - paper: doi:10.1109/26.780463
    title: "Nick McKeown, Adisak Mekkittikul, Venkat Anantharam and Jean Walrand, Achieving 100% throughput in an input-queued switch, IEEE Transactions on Communications 47(8) (1999), 1260-1267"
    locator: virtual output queues, the admissibility condition, and the stability of the longest-queue-first maximum-weight matching for all admissible i.i.d. traffic, by a quadratic Lyapunov function
  - paper: doi:10.1109/49.772430
    title: "Shang-Tse Chuang, Ashish Goel, Nick McKeown and Balaji Prabhakar, Matching output queueing with a combined input/output-queued switch, IEEE Journal on Selected Areas in Communications 17(6) (1999), 1030-1039"
    locator: a CIOQ switch with speedup 2 emulates an output-queued switch exactly, with the most urgent cell first algorithm
  - paper: "J. G. Dai and Balaji Prabhakar, The throughput of data switches with and without speedup, Proceedings of IEEE INFOCOM 2000"
    locator: the fluid-model proof that maximum-weight matching gives 100% throughput, and that any maximal matching with speedup 2 does too
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 13, switching (crossbars, head-of-line blocking, virtual output queues, PIM and iSLIP)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Chapter 4, Scheduling in packet switches (Section 4.1 on head-of-line blocking and virtual output queues, Section 4.2 on the capacity region and MaxWeight, Section 4.3 on maximal matching and load-balanced switches)
---

Switch scheduling is the problem of choosing, in each time slot, which inputs of an input-queued crossbar switch send a cell to which outputs. Each input sends at most one cell and each output takes at most one cell, so each choice is a [matching](/bipartite-matching/) in the bipartite graph of inputs and outputs. The goal is throughput: the queues must stay bounded for every traffic load that the ports can carry. A plain FIFO queue at each input fails this goal because of head-of-line blocking, and it saturates near $2 - \sqrt2 \approx 0.586$ of the line rate; virtual output queues with a [maximum-weight matching](/maximum-weight-matching/) reach 100%.

## In plain words

A switch has a set of input ports and a set of output ports, and a crossbar in the middle that can connect each input to any output. Packets are cut into cells of the same size, and time is cut into slots. In one slot, an input can send one cell, and an output can receive one cell.

When two inputs have cells for the same output, only one can go. The other cell waits. If each input keeps one line of cells, the cell at the front can block the cells behind it, even when their outputs are free. That wastes about 40% of the capacity. The fix is to keep a separate line at each input for each output. Then the switch must decide in each slot which input talks to which output. That decision is the problem on this page.

## Definition

**The model.** An $N \times N$ crossbar with time slots $t = 0, 1, 2, \ldots$ and fixed-size cells. At most one cell leaves each input and at most one cell reaches each output in each slot. A *schedule* for slot $t$ is a matrix $S(t) \in \{0, 1\}^{N \times N}$ with at most one 1 in each row and each column: a matching, or a sub-permutation matrix.

**Queues.** With *virtual output queues* (VOQs), input $i$ keeps a queue $Q_{ij}(t)$ of the cells for output $j$. Let $A_{ij}(t) \in \{0, 1\}$ be the arrivals. Then

$$Q_{ij}(t+1) = \max\bigl(Q_{ij}(t) - S_{ij}(t), 0\bigr) + A_{ij}(t).$$

With a *FIFO input queue*, input $i$ keeps one queue in arrival order, and only its head-of-line (HOL) cell can be scheduled.

**Traffic.** The arrivals are stationary with rates $\lambda_{ij} = \mathbb{E}[A_{ij}(t)]$. The standard case is i.i.d. Bernoulli: in each slot, a cell arrives at input $i$ with probability $\rho$, and its output is uniform on the $N$ outputs, so $\lambda_{ij} = \rho/N$.

**Admissible load.** The rate matrix $\Lambda = (\lambda_{ij})$ is *admissible* when no port is overloaded:

$$\sum_{j} \lambda_{ij} < 1 \text{ for each input } i, \qquad \sum_{i} \lambda_{ij} < 1 \text{ for each output } j.$$

No schedule can keep the queues bounded when a row or column sum is above 1, since that port gets more than one cell per slot on average.

**The task.** Find a rule that picks $S(t)$ from the queue state, such that the queues are stable (for example, $\limsup_{T \to \infty} \frac1T \sum_{t < T} \mathbb{E}[\sum_{ij} Q_{ij}(t)] < \infty$) for every admissible $\Lambda$. Such a rule has *100% throughput*. A second goal is to compute $S(t)$ in one slot time, which is a few nanoseconds in a fast router.

## Variants

- **FIFO input queueing.** Only the HOL cell of each input competes. This is simple but suffers HOL blocking (below).
- **VOQ with a matching per slot.** The page's main problem. The rule can be a maximum-weight matching (slow, optimal), a [maximal matching](/maximal-matching/) found by an iterative hardware arbiter ([PIM](/parallel-iterative-matching/), [iSLIP](/islip/)), or a fixed sequence of permutations computed from known rates ([Birkhoff-von Neumann](/birkhoff-von-neumann-decomposition/)).
- **Speedup and CIOQ.** A switch with speedup $s$ runs the crossbar $s$ times per slot and keeps queues at both the inputs and the outputs (combined input and output queueing, CIOQ). An output-queued switch is the ideal: each cell goes straight to its output queue, which needs speedup $N$.
- **Emulation.** A CIOQ switch *emulates* an output-queued switch if, for each arrival sequence, each cell leaves at the same time as in the output-queued switch.
- **Variable-length packets.** The switch schedules whole packets, or cuts them into cells and puts them back together at the output.
- **Multicast.** A cell can go to several outputs in one slot (fanout splitting).

## Examples

**HOL blocking with two ports.** Let $N = 2$, and let both inputs always have cells, each with a uniform random output. If the two HOL cells want different outputs, both go. If they want the same output, one goes and the other stays. In both cases the next pair of HOL cells wants the same output with probability $1/2$: after a collision, the loser keeps its output and the winner's new cell picks one of two outputs at random. So half the slots carry two cells and half carry one, and the throughput is $(\frac12 \cdot 2 + \frac12 \cdot 1)/2 = 3/4$ per port.

**The saturation throughput of FIFO for larger N.** With every input always backlogged and uniform outputs, a seeded simulation (seed 1, 20000 slots after 1000 slots of warm-up) gives these throughputs per port. Karol, Hluchyj and Morgan give 0.6553 for $N = 4$ and 0.6184 for $N = 8$ by exact analysis.

| $N$ | 2 | 4 | 8 | 16 | 32 | $\infty$ |
| --- | --- | --- | --- | --- | --- | --- |
| throughput | 0.7493 | 0.6557 | 0.6187 | 0.6007 | 0.5939 | $2 - \sqrt2 = 0.5858$ |

**FIFO against VOQ at load 0.95.** With $N = 16$, Bernoulli arrivals of rate 0.95 per input, uniform outputs and 2000 slots (seed 2), the FIFO switch receives 30481 cells and sends 19213, which is 0.600 per port per slot. Its backlog grows by about 5.6 cells per slot. The VOQ switch with a maximum-weight matching (weight $Q_{ij}$) receives 30430 cells and sends 30297; 133 cells, about 8 per input, are queued at the end.

**A load that is not admissible.** $\Lambda = \begin{pmatrix} 1/2 & 1/2 \\ 0 & 0 \end{pmatrix}$ has row sum 1 at input 1, so no rule keeps its queues stable: the queue grows like a random walk with no drift. Any $\Lambda$ with a row sum or column sum above 1 makes a queue grow linearly.

## Known algorithms

- **Maximum-weight matching (LQF).** Pick the matching that maximizes $\sum_{ij} Q_{ij}(t) S_{ij}$. It has 100% throughput for all admissible i.i.d. traffic (McKeown, Mekkittikul, Anantharam and Walrand 1999). The [Hungarian algorithm](/hungarian-algorithm/) finds it in $O(N^3)$ time, which is too slow for one slot of a fast switch.
- **Maximum-size matching.** A matching with the most edges, for example by [Hopcroft-Karp](/hopcroft-karp/) in $O(N^{2.5})$ time. It does not give 100% throughput for all admissible loads: McKeown et al. give a $3 \times 3$ example with nonuniform rates that is admissible but unstable under it.
- **[Parallel iterative matching](/parallel-iterative-matching/).** Random request, grant and accept steps. It finds a maximal matching in $O(\log N)$ iterations on average.
- **[iSLIP](/islip/).** Round-robin grant and accept pointers that move only on an accepted first-iteration grant. 100% throughput under uniform i.i.d. Bernoulli traffic, simple in hardware.
- **[Birkhoff-von Neumann scheduling](/birkhoff-von-neumann-decomposition/).** For known rates, decompose a doubly stochastic matrix above $\Lambda$ into permutation matrices and play them in proportion. 100% throughput with no per-slot matching.
- **Most urgent cell first with speedup 2.** Chuang, Goel, McKeown and Prabhakar (1999): a CIOQ switch with speedup 2 emulates an output-queued switch exactly. Dai and Prabhakar (2000) proved that any maximal matching with speedup 2 has 100% throughput.

## Bounds

**HOL blocking (Karol, Hluchyj and Morgan 1987).** Under uniform i.i.d. traffic with every input backlogged, the saturation throughput $\rho_0$ of FIFO input queueing tends to $2 - \sqrt2$ as $N \to \infty$. Their argument, in outline: there is one HOL cell per input, so on average one HOL cell per output, of which a fraction $\rho_0$ is served each slot and $1 - \rho_0$ waits. As $N \to \infty$, the HOL cells that wait for one output form a discrete-time queue with Poisson arrivals of rate $\rho_0$ and deterministic unit service, whose mean number waiting is $\rho_0^2 / (2(1 - \rho_0))$. Setting this equal to $1 - \rho_0$ gives $\rho_0^2 = 2(1-\rho_0)^2$, so $\rho_0 = \sqrt2/(1 + \sqrt2) = 2 - \sqrt2$. The finite values in the table above approach the limit from above.

**Admissibility is necessary.** If $\sum_j \lambda_{ij} > 1$, input $i$ gets more than one cell per slot on average and sends at most one, so $\sum_j Q_{ij}(t)$ grows linearly. The same holds for a column. So no rule has a larger stability region than the admissible set.

**Max-weight is throughput optimal (McKeown et al. 1999).** For i.i.d. arrivals with an admissible $\Lambda$, the max-weight rule keeps the queues stable. The proof uses the Lyapunov function $V(Q) = \sum_{ij} Q_{ij}^2$. The one-step drift is

$$\mathbb{E}[V(Q(t+1)) - V(Q(t)) \mid Q(t)] \le 2\sum_{ij} Q_{ij}(t)\bigl(\lambda_{ij} - S_{ij}(t)\bigr) + 2N,$$

since each $A_{ij}$ and $S_{ij}$ is 0 or 1 and each input has at most one arrival per slot. An admissible $\Lambda$ satisfies $\Lambda \le (1 - \varepsilon) D$ entrywise for some $\varepsilon > 0$ and some doubly stochastic $D$. By the [Birkhoff-von Neumann theorem](/birkhoff-von-neumann-decomposition/), $D$ is a convex combination of permutation matrices, so $\sum_{ij} Q_{ij}\lambda_{ij} \le (1-\varepsilon)\max_{P}\sum_{ij} Q_{ij}P_{ij}$, and the max-weight $S(t)$ attains that maximum. A maximum over permutations is at least the average over the $N$ cyclic shifts, which is $\frac1N\sum_{ij}Q_{ij}$. So the drift is at most $-\frac{2\varepsilon}{N}\sum_{ij}Q_{ij}(t) + 2N$, which is negative outside a finite set, and the Foster-Lyapunov criterion gives stability.

**Maximal matchings without speedup.** A maximal matching has at least half the size of a maximum matching. Without speedup, a maximal matching does not in general give 100% throughput for all admissible loads; with speedup 2 it does (Dai and Prabhakar 2000).

**Time per slot.** A maximum-weight matching costs $O(N^3)$ time with the Hungarian algorithm. PIM and iSLIP run $O(\log N)$ iterations, and each iteration is a parallel step of $N$ arbiters, each a priority encoder of depth $O(\log N)$.

## Reductions

- **To bipartite matching.** One slot of VOQ scheduling is a matching problem in the bipartite graph with an edge $(i, j)$ when $Q_{ij} > 0$. Maximum size is [bipartite matching](/bipartite-matching/); maximum weight is the [assignment problem](/assignment-problem/).
- **To edge coloring, offline.** If all arrivals of a frame of $T$ slots are known and each port has at most $T$ cells, the cells form a bipartite multigraph of maximum degree at most $T$. By [König's edge-coloring theorem](/edge-coloring/) its edges split into $T$ matchings, so the frame can be sent in exactly $T$ slots. This is the integer form of the Birkhoff-von Neumann decomposition.
- **As a case of max-weight scheduling.** The max-weight rule is the switch case of the [backpressure](/backpressure-routing/) rule of Tassiulas and Ephremides, with one hop and the matchings as the feasible schedules. [Wireless link scheduling](/wireless-link-scheduling/) is the same problem with independent sets of an interference graph in place of matchings.

## Applications

- **Router and switch fabrics.** High-speed routers use input-queued crossbars with VOQs, because the memory of an output-queued switch must run $N$ times faster than the line. The arbiters run iSLIP or a related round-robin scheme. The Tiny Tera and the Cisco GSR 12000 used iSLIP-like schedulers, according to McKeown.
- **Local-area network switches.** The AN2 switch of DEC SRC used PIM (Anderson et al. 1993).
- **Data center and optical circuit switches.** A circuit switch reconfigures slowly, so it plays a short list of permutations for long periods. This is a Birkhoff-von Neumann schedule with a cost per reconfiguration.
- **Interconnects inside a chip or a supercomputer.** Router allocators assign input virtual channels to output ports with the same separable request, grant and accept structure.

## References
