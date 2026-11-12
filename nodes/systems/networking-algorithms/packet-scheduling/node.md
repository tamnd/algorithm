---
tag: SYFHKA
kind: problem
slug: packet-scheduling
name: Packet scheduling
aliases:
- queue scheduling
- packet scheduling discipline
area: systems/networking-algorithms
level: intro
summary: "Choose which queued packet a link sends next, so that the link stays busy, flows get fair shares and delay bounds hold, and one flow cannot harm the others."
prereqs: [queue, work-conserving-scheduling]
see_also: [fair-queueing, weighted-fair-queueing, deficit-round-robin, generalized-processor-sharing, active-queue-management, switch-scheduling, round-robin, priority-queue]
sources:
  - paper: doi:10.1145/75246.75248
    title: Alan Demers, Srinivasan Keshav and Scott Shenker, Analysis and simulation of a fair queueing algorithm, ACM SIGCOMM (1989)
    locator: Section 1 and Section 2 (the goals of a queueing algorithm, the critique of FIFO and the fair queueing algorithm)
  - paper: doi:10.1109/90.234856
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the single-node case, IEEE/ACM Transactions on Networking 1(3) (1993)
    locator: pp. 344 to 357 (GPS, PGPS, the bound of one maximum packet time, and the delay bounds for leaky-bucket flows)
  - paper: doi:10.1109/90.502236
    title: M. Shreedhar and George Varghese, Efficient fair queuing using deficit round-robin, IEEE/ACM Transactions on Networking 4(3) (1996)
    locator: pp. 375 to 385 (the fairness measure and the O(1) work per packet)
  - paper: doi:10.1109/INFCOM.1994.337677
    title: S. Jamaloddin Golestani, A self-clocked fair queueing scheme for broadband applications, IEEE INFOCOM (1994)
    locator: pp. 636 to 646 (the relative fairness measure over intervals in which two flows are backlogged)
  - paper: doi:10.1109/TCOM.1987.1096782
    title: John Nagle, On packet switches with infinite storage, IEEE Transactions on Communications 35(4) (1987)
    locator: pp. 435 to 438 (one queue per source, served in round robin)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition, Pearson, 2020
    locator: Chapter 4, Section 4.2 (packet scheduling, FIFO, priority queueing, round robin and weighted fair queueing)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2012
    locator: Chapter 6, Section 6.2 (queuing disciplines, FIFO and fair queuing)
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control, and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Section 3.5 (providing priorities and fair queueing)
---

Packet scheduling is the problem of choosing, each time an output link becomes free, which of the queued packets it sends next. The packets belong to flows, and the choice decides how the capacity of the link is shared, how long each packet waits, and whether a flow that sends too much can harm the others. The main goals are to keep the link busy (work conservation), to share it fairly or in given proportions, to give bounds on delay, and to isolate flows from each other, all at a cost of a few operations per packet. The answers range from FIFO and strict priority to [round robin](/round-robin/) and the [fair queueing](/fair-queueing/) family, whose ideal is the fluid model of [generalized processor sharing](/generalized-processor-sharing/).

## In plain words

A router port sends one packet at a time. While it sends, more packets arrive and wait. Each time the port is free, a rule must pick the next packet. This rule is the packet scheduler.

The simplest rule takes the oldest packet. Then one sender that floods the port makes every other sender wait. A second rule gives some packets priority, which helps urgent traffic, but low-priority traffic can starve. A third rule keeps one line per sender and takes turns between the lines, so each sender gets a fair part of the port.

Good rules never leave the port idle while packets wait, share the port in a fair way, promise each sender a bound on its wait, and do all of this with very little work per packet.

## Definition

A link of rate $r$ (bits per second) serves packets. Packet $p$ arrives at time $a_p$, has length $L_p$ bits and belongs to flow $f(p)$ among $N$ flows. Flow $i$ may have a weight $\varphi_i > 0$. A *schedule* gives each packet a start time $s_p \ge a_p$. Transmission is non-preemptive, so packet $p$ finishes at $d_p = s_p + L_p / r$, and the transmission intervals of two packets do not overlap. A *scheduler* is an online rule: the packet it starts at time $t$ depends only on the packets that arrived by $t$.

Let $W_i(t_1, t_2)$ be the bits of flow $i$ sent in $[t_1, t_2]$. A flow is *backlogged* at $t$ if it has a packet that has arrived and has not finished. The usual goals are:

- **Work conservation.** The link is never idle while some packet waits.
- **Fairness.** Over any interval in which flows $i$ and $j$ are both backlogged, $|W_i/\varphi_i - W_j/\varphi_j|$ stays below a constant that does not grow with the interval. Golestani called the least such constant the fairness measure. With equal weights, the ideal is the [max-min fair](/max-min-fairness/) share of the link.
- **Delay bounds.** If flow $i$ is shaped by a [token bucket](/token-bucket/) of depth $\sigma_i$ and rate $\rho_i$, every packet of flow $i$ leaves within a bound $D_i$ that depends only on $\sigma_i$, $\rho_i$, the weights and the packet sizes.
- **Isolation.** The guarantees of flow $i$ hold whatever the other flows send.
- **Cost.** The work and memory per packet, as a function of $N$.

## Variants

- **Work conserving or not.** A non-work-conserving scheduler may hold a packet back to shape the output, as a rate-controlled scheduler or a [traffic shaper](/traffic-shaping/) does. This wastes capacity but bounds the burstiness at the next hop.
- **Classes or flows.** A scheduler may serve a few traffic classes (as in DiffServ) or thousands of flows. Many systems hash flows into a fixed number of queues.
- **Weighted or equal shares.** Weights $\varphi_i$ give flow $i$ the share $\varphi_i / \sum_{j \in B} \varphi_j$ of the link, where $B$ is the set of backlogged flows.
- **Hierarchical.** Shares are given to a tree of classes, and the scheduler serves each level in turn.
- **Deadline-based.** Each packet has a deadline, and the aim is to meet the deadlines, as in [earliest deadline first](/earliest-deadline-first/).
- **Multiple links.** A switch with many inputs and outputs must choose a [matching](/switch-scheduling/) of inputs to outputs in each slot, and a wireless network must choose [links that do not interfere](/wireless-link-scheduling/). These are packet scheduling problems with a combinatorial constraint.

## Examples

**A bulk flow and a voice flow.** A link of 1 Mbit/s carries flow A, a file transfer with 1500-byte packets (12 ms each) and 50 packets queued, and flow B, a voice call with a 200-byte packet (1.6 ms) every 20 ms.

| scheduler | wait of a voice packet | effect on A |
|---|---|---|
| FIFO | behind the 50 queued A packets, about 600 ms | none |
| strict priority for B | at most the A packet in service, 12 ms | A gets what B leaves; a flood of B would starve A |
| fair queueing | at most the fluid time of 3.2 ms plus one maximum packet time of 12 ms, 15.2 ms | A keeps at least half the link |

The bound for fair queueing comes from the theorem of Parekh and Gallager: in the fluid model, B gets at least half the link, so its 1600 bits finish within 3.2 ms, and the packet scheduler [WFQ](/weighted-fair-queueing/) finishes each packet at most $L_{max}/r = 12$ ms after the fluid model does.

**Round robin over packets.** Serve one packet from each backlogged flow in turn. If flow A sends 1500-byte packets and flow C sends 100-byte packets, A gets 15 times the bytes of C. [Deficit round robin](/deficit-round-robin/) fixes this with a byte quantum.

## Known algorithms

| algorithm | work per packet | fairness | delay bound for a token-bucket flow |
|---|---|---|---|
| FIFO (first come, first served) | $O(1)$ | none | none per flow; the sum of the bursts of all flows over $r$ |
| strict priority | $O(1)$ for a fixed number of classes | none | only for the top class |
| packet round robin (Nagle 1987) | $O(1)$ | fair in packets, not in bytes | none in general |
| [deficit round robin](/deficit-round-robin/) (1995) | $O(1)$ when the quantum is at least the largest packet | measure at most $Q + 2L_{max}$ for equal quanta $Q$ | grows with the number of flows |
| [fair queueing](/fair-queueing/) (DKS 1989) | $O(\log N)$ with a heap, plus the round number | close to bit-by-bit round robin | as WFQ with equal weights |
| [WFQ / PGPS](/weighted-fair-queueing/) (Parekh and Gallager 1993) | $O(\log N)$ amortized with a heap; the virtual time can cost $O(N)$ in one step | within one maximum packet of GPS | $\sigma_i / g_i + L_{max} / r$ |
| WF2Q (Bennett and Zhang 1996) | as WFQ | worst-case fair: its service stays within one maximum packet of GPS, ahead or behind | as WFQ |
| SCFQ (Golestani 1994) | $O(\log N)$ | measure at most $L_i/\varphi_i + L_j/\varphi_j$ | grows with the number of flows |
| Virtual Clock (Zhang 1990) | $O(\log N)$ | not fair over intervals; a flow can be punished for past use | as WFQ for a reserved rate |

Here $g_i = \varphi_i r / \sum_j \varphi_j$ is the guaranteed rate of flow $i$, and $L_{max}$ is the largest packet. The tags of WFQ and SCFQ are kept in a [priority queue](/priority-queue/), such as a [binary heap](/binary-heap/) or a [calendar queue](/calendar-queue/).

## Bounds

- **Conservation.** All work-conserving schedulers have the same busy periods and the same total backlog in bits at every time, since the link sends at rate $r$ whenever there is work. A scheduler can only move delay between flows, not remove it.
- **The cost of non-preemption.** No non-preemptive scheduler can always finish each packet by its fluid finish time. If a packet of $L_{max}$ bits starts just before a small packet of another flow arrives, the small packet waits about $L_{max}/r$ more than in the fluid model. WFQ meets this lower bound: Parekh and Gallager prove that each packet finishes at most $L_{max}/r$ after its finish under GPS.
- **Delay under GPS.** If flow $i$ is shaped by a token bucket $(\sigma_i, \rho_i)$ and $\rho_i \le g_i$, then under GPS its backlog is at most $\sigma_i$ and its delay at most $\sigma_i / g_i$, whatever the other flows do. With WFQ, the delay is at most $\sigma_i / g_i + L_{max}/r$.
- **FIFO.** If all flows are shaped and $\sum_j \rho_j \le r$, FIFO bounds every delay by $\sum_j \sigma_j / r$ plus one packet time. One flow with a large burst raises the delay of all.

## Reductions

- **To a priority queue.** WFQ, SCFQ and Virtual Clock compute a tag for each packet at arrival and send the packet with the least tag. So they reduce packet scheduling to the [priority queue](/priority-queue/) operations insert and extract-min, plus the computation of a virtual time.
- **To CPU scheduling.** Proportional share of a link is the same problem as proportional share of a processor, with packet lengths in place of time slices. [Stride scheduling](/stride-scheduling/) is the processor form of WFQ, [lottery scheduling](/lottery-scheduling/) a randomized form, and the virtual runtime of the [completely fair scheduler](/completely-fair-scheduler/) plays the role of the virtual finish time. The difference is that packets cannot be cut, while time slices can.
- **From fair sharing.** The fluid ideal, [generalized processor sharing](/generalized-processor-sharing/), gives each backlogged flow its weighted share at each instant, which is the weighted max-min fair allocation of one link.

## Applications

- **Router and switch ports.** Each output port of a router has a scheduler, often DRR or a priority scheduler over a few classes, with an [AQM](/active-queue-management/) on each queue.
- **Home gateways and hosts.** FQ-CoDel and other flow-queueing schedulers in Linux keep interactive traffic fast when a large transfer runs.
- **Quality of service.** Integrated services used WFQ to give delay guarantees to shaped flows. Differentiated services use priority and weighted queues for classes.
- **Data centers and the cloud.** Schedulers in network cards and virtual switches share links between tenants and flows.
- **Wireless and cellular links.** The [proportional fair scheduler](/proportional-fair-scheduling/) picks a user per slot by its channel quality and its past throughput.

## References
