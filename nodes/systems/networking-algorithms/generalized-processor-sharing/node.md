---
tag: REWV62
kind: model
slug: generalized-processor-sharing
name: Generalized processor sharing
aliases:
- weighted fluid fair sharing
area: systems/networking-algorithms
level: advanced
summary: "An ideal fluid server in which each backlogged flow i gets the share phi_i / (sum of phi over the backlogged flows) of the link at every instant; the reference for fair packet schedulers."
history:
  year: 1993
  people: [Abhay K. Parekh, Robert G. Gallager]
  note: Parekh and Gallager defined GPS and analysed its packet form in IEEE/ACM Transactions on Networking in 1993 and 1994.
prereqs: [packet-scheduling]
see_also: [weighted-fair-queueing, fair-queueing, deficit-round-robin, token-bucket, max-min-fairness, stride-scheduling, completely-fair-scheduler, work-conserving-scheduling]
sources:
  - paper: doi:10.1109/90.234856
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the single-node case, IEEE/ACM Transactions on Networking 1(3) (1993)
    locator: pp. 344 to 357, Section II (the definition of GPS and the guaranteed rate), Section III (virtual time, PGPS and the bounds of one maximum packet) and Section IV onward (the delay and backlog bounds for leaky-bucket flows)
  - paper: doi:10.1109/90.298432
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the multiple node case, IEEE/ACM Transactions on Networking 2(2) (1994)
    locator: pp. 137 to 150 (end-to-end bounds, and rate-proportional processor sharing)
  - paper: doi:10.1145/75246.75248
    title: Alan Demers, Srinivasan Keshav and Scott Shenker, Analysis and simulation of a fair queueing algorithm, ACM SIGCOMM (1989)
    locator: Section 2 (bit-by-bit round robin, the equal-weight form of the fluid ideal)
  - paper: doi:10.1109/INFCOM.1996.497885
    title: Jon C. R. Bennett and Hui Zhang, WF2Q, worst-case fair weighted fair queueing, IEEE INFOCOM (1996)
    locator: pp. 120 to 128 (the difference between PGPS and GPS, and the worst-case fair index)
  - paper: doi:10.1109/INFCOM.1994.337677
    title: S. Jamaloddin Golestani, A self-clocked fair queueing scheme for broadband applications, IEEE INFOCOM (1994)
    locator: pp. 636 to 646 (the cost of tracking the GPS virtual time, and a self-clocked substitute)
---

Generalized processor sharing (GPS) is an ideal model of a shared link, defined by Parekh and Gallager in 1993. The link of rate $r$ serves traffic as a fluid. Each flow $i$ has a weight $\varphi_i > 0$, and at every instant each backlogged flow is served at rate

$$r_i(t) = \frac{\varphi_i}{\sum_{j \in B(t)} \varphi_j}\, r,$$

where $B(t)$ is the set of backlogged flows. GPS cannot be built, because a real link sends one packet at a time. It is the reference that fair [packet schedulers](/packet-scheduling/) try to follow: [weighted fair queueing](/weighted-fair-queueing/) finishes each packet within one maximum packet time of its GPS finish. In GPS, a flow with weight $\varphi_i$ always gets at least the guaranteed rate $g_i = \varphi_i r / \sum_j \varphi_j$, so a flow shaped by a [token bucket](/token-bucket/) has a delay bound that the other flows cannot break.

## The machine

- **The server.** One link of rate $r$ bits per second. It is work conserving: it serves at rate $r$ whenever some flow has bits.
- **The flows.** $N$ flows with fixed weights $\varphi_1, \dots, \varphi_N > 0$. Each flow has its own FIFO queue. A packet of $L$ bits of flow $i$ enters its queue in full at its arrival time.
- **The rule.** The service is a fluid: in each short time interval, the server splits its capacity among the backlogged flows in proportion to their weights. Formally, let $S_i(\tau, t)$ be the bits of flow $i$ served in $(\tau, t]$. For every interval in which flow $i$ is backlogged all the time,

$$\frac{S_i(\tau, t)}{S_j(\tau, t)} \ge \frac{\varphi_i}{\varphi_j} \quad \text{for all flows } j,$$

with equality when $j$ is also backlogged all the time.
- **Virtual time.** Parekh and Gallager track the progress of GPS by a virtual time $V(t)$, with $V = 0$ at the start of a busy period and

$$\frac{dV}{dt} = \frac{r}{\sum_{j \in B(t)} \varphi_j}$$

while the system is busy. Each backlogged flow receives $\varphi_i\, dV$ bits while $V$ grows by $dV$.

With all weights equal, GPS is the fluid limit of the bit-by-bit round robin of [fair queueing](/fair-queueing/), and $V$ is its round number up to a constant factor.

**Example.** A link of rate 1 serves flow A with $\varphi_A = 1$ and flow B with $\varphi_B = 3$. At time 0, a packet of 4 bits of A and a packet of 6 bits of B arrive. A gets $1/4$ of the link and B $3/4$. B finishes at time $6 / (3/4) = 8$, when A has received 2 bits. A then has the whole link and finishes its other 2 bits at time 10. The virtual time grows at rate $1/4$ up to time 8, where $V = 2$, and at rate 1 after that, so $V(10) = 4$. These are the tags $6/3 = 2$ and $4/1 = 4$ that the packet schedulers compute.

## What it counts

- **Service and backlog.** $S_i(\tau, t)$ and the backlog $Q_i(t)$ of each flow, in bits.
- **Delay.** The time $D_i$ from the arrival of a bit of flow $i$ to its departure. For a flow that conforms to a token bucket of depth $\sigma_i$ and rate $\rho_i$, the model gives bounds on the worst $D_i$ and $Q_i$.
- **Fairness.** How close a real scheduler comes to GPS: the gap between its finish times and the GPS finish times, and the gap between its service $\hat S_i$ and $S_i$.
- **The cost of emulation.** A packet scheduler that follows GPS must compute $V(t)$, which changes slope each time a flow empties in GPS. The number of such events between two arrivals can be as large as the number of flows.

## Relation to other models

- **Processor sharing in queueing theory.** With equal weights, GPS is the processor sharing discipline of queueing theory, applied to flows instead of jobs. Discriminatory processor sharing gives jobs of different classes different weights, as GPS does for flows.
- **Fair queueing.** Bit-by-bit round robin, the ideal of [fair queueing](/fair-queueing/) by Demers, Keshav and Shenker, is GPS with equal weights. [WFQ](/weighted-fair-queueing/), also called packet-by-packet GPS (PGPS), sends the packets in the order of their GPS finish times.
- **Other packet schedulers.** WF2Q also follows GPS but sends a packet only if it has started in GPS. SCFQ replaces $V(t)$ by the tag of the packet in service. [Deficit round robin](/deficit-round-robin/) gets long-run GPS shares with a byte quantum and no virtual time.
- **Processor scheduling.** The same fluid ideal underlies proportional-share schedulers of processors: [stride scheduling](/stride-scheduling/) uses pass values like virtual finish tags, and the [completely fair scheduler](/completely-fair-scheduler/) of Linux tracks a weighted virtual runtime per task.
- **Fair allocation.** At each instant, GPS gives the weighted [max-min fair](/max-min-fairness/) split of one link among flows that want more than their share.
- **Work conservation.** As a [work-conserving](/work-conserving-scheduling/) server, GPS has the same busy periods and the same total backlog as FIFO on the same arrivals; it only moves delay between flows.

## Known results in the model

**Guaranteed rate.** Since $B(t)$ is a subset of all flows, a backlogged flow $i$ is always served at rate at least $g_i = \varphi_i r / \sum_{j=1}^{N} \varphi_j$. This holds whatever the other flows send.

**Fair shares.** Over an interval in which flows $i$ and $j$ are both backlogged all the time, $S_i / \varphi_i = S_j / \varphi_j$ exactly. Both receive $\varphi\, dV$ bits for each step $dV$ of the virtual time.

**Single-node delay bound (Parekh and Gallager 1993).** Suppose that flow $i$ conforms to a token bucket: its arrivals in any interval of length $\ell$ are at most $\sigma_i + \rho_i \ell$ bits, with $\rho_i \le g_i$. Then under GPS its backlog is at most $\sigma_i$ and the delay of each bit is at most $\sigma_i / g_i$. The proof is short. Let $\tau$ be the start of a backlogged period of flow $i$ that contains $t$. Then $Q_i(t) = A_i(\tau, t) - S_i(\tau, t) \le \sigma_i + \rho_i (t - \tau) - g_i (t - \tau) \le \sigma_i$. A bit that arrives at $t$ has left once $S_i(\tau, t + d) \ge A_i(\tau, t)$, and this holds when $g_i (t + d - \tau) \ge \sigma_i + \rho_i (t - \tau)$, so for every $d \ge \sigma_i / g_i$. The bound is tight: a flow that sends its whole burst $\sigma_i$ at once, while all other flows are backlogged, waits exactly $\sigma_i / g_i$ for its last bit. For example, in seeded random runs with $g = 1$ and $\sigma = 8$ for one flow and $g = 2$ and $\sigma = 15$ for another, beside a greedy third flow, the largest delays were exactly 8 and 7.5.

**Virtual finish times.** Give the $k$-th packet of flow $i$, of length $L$ and arrival time $a$, the tags

$$S = \max(F_{prev}, V(a)), \qquad F = S + \frac{L}{\varphi_i},$$

where $F_{prev}$ is the tag $F$ of the packet of flow $i$ before it (0 at the start). Then in GPS the packet is served while $V$ runs from $S$ to $F$, and it finishes at the first time at which $V(t) = F$. The reason is that a backlogged flow receives $\varphi_i\, dV$ bits for each $dV$, so $L$ bits take $L / \varphi_i$ units of virtual time, and the packet starts when the packet before it ends ($V = F_{prev}$) or at its arrival, whichever is later. Since $V$ never decreases, the GPS finish order is the order of the tags $F$.

**Packet-by-packet GPS (Parekh and Gallager 1993).** Let PGPS (that is, [WFQ](/weighted-fair-queueing/)) send, each time the link is free, the queued packet with the least GPS finish tag. Then for every packet, $\hat F_p \le F_p + L_{max}/r$, where $\hat F_p$ and $F_p$ are its finish times under PGPS and GPS and $L_{max}$ is the largest packet. Also $S_i(0, t) - \hat S_i(0, t) \le L_{max}$ for every flow and every time: PGPS is never behind GPS by more than one packet. So the token-bucket flow above has delay at most $\sigma_i / g_i + L_{max}/r$ under PGPS.

**PGPS can run ahead.** The converse fails. Bennett and Zhang showed that PGPS can send many packets of one flow far ahead of GPS, then starve it. Their WF2Q is never ahead of GPS by more than one packet either.

**Multiple nodes (Parekh and Gallager 1994).** In a network of GPS servers, if each flow has the same weight at every node in proportion to its reserved rate (rate-proportional processor sharing), then the end-to-end delay of a token-bucket flow is bounded independently of the other flows, by about $\sigma_i / g_i$ plus a packet term for each hop. The burst is paid only once, not once per hop.

## References
