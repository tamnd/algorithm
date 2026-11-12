---
tag: XAQ195
kind: algorithm
slug: weighted-fair-queueing
name: Weighted fair queueing
aliases:
- WFQ
- packetized GPS
- PGPS
- packet-by-packet generalized processor sharing
area: systems/networking-algorithms
level: advanced
summary: "Track the GPS virtual time V, tag each packet with F = max(F_prev, V(a)) + L/phi, and send the least tag; each packet ends within L_max/r of its GPS finish."
solves: [packet-scheduling]
model: word-ram
complexity:
  vars: {n: the number of packets}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [generalized-processor-sharing, fair-queueing, priority-queue]
see_also: [deficit-round-robin, packet-scheduling, token-bucket, calendar-queue, stride-scheduling, completely-fair-scheduler, max-min-fairness, active-queue-management]
sources:
  - paper: doi:10.1109/90.234856
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the single-node case, IEEE/ACM Transactions on Networking 1(3) (1993)
    locator: pp. 344 to 357, Section III (virtual time, the tags S and F, PGPS, and Theorem 1, that each packet finishes at most L_max/r after its GPS finish)
  - paper: doi:10.1109/90.298432
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the multiple node case, IEEE/ACM Transactions on Networking 2(2) (1994)
    locator: pp. 137 to 150 (end-to-end delay bounds for PGPS networks)
  - paper: doi:10.1145/75246.75248
    title: Alan Demers, Srinivasan Keshav and Scott Shenker, Analysis and simulation of a fair queueing algorithm, ACM SIGCOMM (1989)
    locator: Section 2 (the equal-weight scheme, and weights as a generalization)
  - paper: doi:10.1109/INFCOM.1996.497885
    title: Jon C. R. Bennett and Hui Zhang, WF2Q, worst-case fair weighted fair queueing, IEEE INFOCOM (1996)
    locator: pp. 120 to 128 (the example in which WFQ runs far ahead of GPS, and WF2Q, which sends only packets that have started in GPS)
  - paper: doi:10.1109/INFCOM.1994.337677
    title: S. Jamaloddin Golestani, A self-clocked fair queueing scheme for broadband applications, IEEE INFOCOM (1994)
    locator: pp. 636 to 646 (SCFQ, which uses the tag of the packet in service as the virtual time, and its fairness bound)
  - paper: doi:10.1145/99508.99525
    title: Lixia Zhang, VirtualClock, a new traffic control algorithm for packet switching networks, ACM SIGCOMM (1990)
    locator: pp. 19 to 29 (tags computed from real time and the reserved rate); also ACM Transactions on Computer Systems 9(2), 1991, doi:10.1145/103720.103721
  - book: isbn:9781107036055
    title: R. Srikant and Lei Ying, Communication Networks, An Optimization, Control, and Stochastic Networks Perspective, Cambridge University Press, 2014
    locator: Section 3.5 (fair queueing and weighted fair queueing)
---

Weighted fair queueing (WFQ), which Parekh and Gallager call packet-by-packet generalized processor sharing (PGPS), is the [packet scheduler](/packet-scheduling/) that sends packets in the order in which they would finish under [generalized processor sharing](/generalized-processor-sharing/) (GPS). It tracks the GPS virtual time $V(t)$, which grows at rate

$$\frac{dV}{dt} = \frac{r}{\sum_{j \in B(t)} \varphi_j}$$

over the set $B(t)$ of flows that are backlogged in GPS. A packet of $L$ bits of flow $i$ that arrives at time $a$ gets the tags

$$S = \max(F_{prev}, V(a)), \qquad F = S + \frac{L}{\varphi_i},$$

and when the link is free, WFQ sends the queued packet with the least $F$. Parekh and Gallager proved that each packet then finishes at most $L_{max}/r$ after it would finish under GPS, so each flow gets its weighted share and the delay bounds of GPS, up to one maximum packet time. With equal weights, WFQ is the [fair queueing](/fair-queueing/) of Demers, Keshav and Shenker.

## In plain words

Imagine a perfect link that serves all waiting senders at once, each at a speed set by its weight. A sender with weight 3 gets three times the speed of a sender with weight 1. A real link cannot do this, because it sends one whole packet at a time.

Weighted fair queueing runs the perfect link in its head. It works out, for each arriving packet, at what point the perfect link would finish it, and writes that point on the packet. When the real link is free, it sends the waiting packet with the earliest point.

So the real link sends packets in nearly the same order as the perfect link, and each packet leaves at most one long packet later than it would have.

## The problem

A link of rate $r$ serves $N$ flows. Flow $i$ has weight $\varphi_i$ and is promised the guaranteed rate $g_i = \varphi_i r / \sum_j \varphi_j$. The aim, as on the [packet scheduling](/packet-scheduling/) page, is to give each backlogged flow its weighted share, to keep the delay bounds of GPS for flows shaped by a [token bucket](/token-bucket/), and to isolate the flows from each other, with non-preemptive transmission of whole packets.

## The algorithm

A flow is backlogged in GPS when its last tag is above the virtual time, $F_{last}[i] > V$. The scheduler keeps $V$, the time $clock$ at which $V$ was last brought up to date, the sum $\Phi$ of the weights of the flows backlogged in GPS, and a [priority queue](/priority-queue/) of the queued packets keyed by $F$.

```pseudo id=main
ARRIVE(packet p of flow i, L bits, time a)
L1  ADVANCE(a)
L2  S ← max(F_last[i], V)
L3  F ← S + L / φ_i;  if F_last[i] ≤ V then Φ ← Φ + φ_i;  F_last[i] ← F
L4  insert p with key F into the priority queue

ADVANCE(t)                                          ▷ V grows at rate r / Φ
L5  while Φ > 0 and V reaches m = min{F_last[i] : i backlogged in GPS} by time t:
        clock ← clock + (m − V)·Φ / r;  V ← m;  remove the weights of the flows with F_last = m from Φ
L6  if Φ > 0 then V ← V + (t − clock)·r / Φ
L7  clock ← t

SEND-NEXT()                                         ▷ when the link is free
L8  if the priority queue is not empty then extract the packet with the least F and send it
```

Line L5 is the iterated deletion of the GPS departures: each time a flow empties in GPS, $\Phi$ falls and $V$ speeds up. The GPS departures depend only on the tags and the arrivals, not on what the real link sends, which is why WFQ can simulate GPS beside the real link. While the system is empty, $V$ stays constant.

## Example

**Tags by hand.** A link of rate 1 serves flow A with $\varphi_A = 1$ and flow B with $\varphi_B = 3$. At time 0, A sends 4 bits and B sends 6 bits. The tags are $F_A = 0 + 4/1 = 4$ and $F_B = 0 + 6/3 = 2$, so WFQ sends B first (times 0 to 6) and then A (6 to 10). In GPS, $V$ grows at rate $1/(1+3) = 1/4$ and reaches $F_B = 2$ at time 8, when B finishes, and then at rate 1, so $V(9) = 3$. A second packet of 3 bits of B that arrives at time 9 gets $S = \max(2, 3) = 3$ and $F = 3 + 3/3 = 4$: B had emptied in GPS, so it starts from the current virtual time and gets no credit for its idle time.

**WFQ can run ahead of GPS.** The example of Bennett and Zhang: flow 0 has weight 10 and 11 packets of 1 bit, and ten other flows have weight 1 and one packet each, all at time 0, on a link of rate 1. GPS gives flow 0 half the link, so its packets finish at times 2, 4, ..., 20. Their tags are $0.1, 0.2, \dots, 1.1$, while each other flow has tag 1. So WFQ sends ten packets of flow 0 in the time interval $[0, 10]$, five more than GPS, then the ten other packets in $[10, 20]$, while flow 0 waits. No packet is late by more than one packet time, but flow 0 gets bursty service.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **The tags are the GPS finish points.** Under GPS, the packet is served while $V$ runs from $S$ to $F$, and it finishes at the first time $d_p$ at which $V(t) = F_p$. So the order of the tags is the GPS finish order.
2. **Theorem of Parekh and Gallager.** For every packet $p$, with $\hat d_p$ its finish time under WFQ,

$$\hat d_p \le d_p + \frac{L_{max}}{r}.$$

3. **Delay bound.** If flow $i$ conforms to a token bucket $(\sigma_i, \rho_i)$ with $\rho_i \le g_i$, each of its packets leaves within $\sigma_i / g_i + L_{max} / r$ of its arrival, since GPS gives the bound $\sigma_i / g_i$.

Parekh and Gallager also show that WFQ is never behind GPS by more than $L_{max}$ bits in the service of any flow. The example above shows that it can be far ahead.

## Complexity

ARRIVE does one insertion into the priority queue and SEND-NEXT one extraction, $O(\log n)$ each with a [binary heap](/binary-heap/). Each pass of the loop of line L5 removes a flow from the GPS-backlogged set, and a flow enters that set at most once per arrival, so the loop makes at most $n$ passes over the run, each $O(\log n)$ with a heap of the last tags. So $n$ packets cost $O(n \log n)$ time, $O(\log n)$ amortized per packet. One arrival can still cause $\Theta(N)$ GPS departures for $N$ flows, so the worst case of one operation is $O(N \log n)$. The space is $\Theta(n)$ for the queued packets and $O(N)$ for the flow state. The tags can also go into a [calendar queue](/calendar-queue/) or a bucket structure for hardware.

## Properties

- **Within one packet of GPS.** The finish time bound $L_{max}/r$ is the best that any non-preemptive scheduler can guarantee, since a packet that arrives just after a maximum packet has started must wait for it.
- **Isolation.** The guaranteed rate $g_i$ holds whatever the other flows send.
- **Not worst-case fair.** As the example shows, WFQ can serve a flow far ahead of GPS and then stop serving it for a long time.
- **Weights, not rates.** The shares adapt: when some flows are idle, the backlogged flows share the rest in proportion to their weights.
- **Exact with a known rate.** The virtual time needs the link rate $r$. On a link whose rate changes, the GPS simulation is wrong.

## Variants and improvements

- **WF2Q (Bennett and Zhang, 1996).** Among the queued packets that have already started service in GPS ($S \le V(t)$), send the one with the least $F$. This keeps the service within one packet of GPS in both directions, so it is worst-case fair. WF2Q+ simplifies the virtual time.
- **SCFQ (Golestani, 1994).** Self-clocked fair queueing uses the tag $F$ of the packet in service in place of $V(a)$. It needs no GPS simulation, so the cost is one heap operation per packet, and the fairness measure is at most $L_i/\varphi_i + L_j/\varphi_j$. The delay bound grows with the number of flows.
- **Virtual Clock (Zhang, 1990).** Tags use real time in place of virtual time: $F = \max(F_{prev}, a) + L/\rho_i$ for a reserved rate $\rho_i$. It gives the same delay bound as WFQ for flows within their reservation, but a flow that used idle capacity in the past is punished later.
- **Start-time tags.** Schedulers that send the least start tag $S$ are also used, and they suit links whose rate changes.
- **Constant-time approximations.** [Deficit round robin](/deficit-round-robin/) gives the long-run weighted shares with $O(1)$ work per packet, at the cost of weaker delay bounds.
- **Processor schedulers.** [Stride scheduling](/stride-scheduling/) applies the same tags to processes, and the [completely fair scheduler](/completely-fair-scheduler/) runs the task with the least weighted virtual runtime.

## When to use it

Use WFQ, or better WF2Q, when flows need guaranteed rates and delay bounds, as in integrated services and in the scheduling of reserved traffic classes. When the number of flows is large and the per-packet budget is a few operations, use [deficit round robin](/deficit-round-robin/) or SCFQ. When only priority between a few classes matters, a priority scheduler is simpler.

## Pitfalls

- **Using the wall clock as the virtual time.** That is Virtual Clock, with its different behaviour, not WFQ.
- **Counting backlog in the real queue.** $\Phi$ sums the weights of the flows backlogged in GPS, not of the flows with packets in the real queue.
- **Skipping the GPS departures in ADVANCE.** Using one rate for the whole interval since the last arrival makes $V$ too small, and newly active flows get too early tags.
- **Resetting $V$ too late or never.** $V$ should stay constant while the system is empty. Letting it grow with time gives an idle flow tags that are too large compared with old tags.
- **Overflow of tags.** In fixed-point hardware the tags grow without bound. Implementations reset $V$ and the tags at the end of each busy period, or compare them modulo a large number.

## Implementations

## History

Demers, Keshav and Shenker introduced fair queueing in 1989 and noted that weights can be added. Abhay Parekh and Robert Gallager defined GPS and its packet form PGPS in 1993, and proved that PGPS finishes each packet within one maximum packet time of GPS, and that a network of PGPS servers gives end-to-end delay bounds to token-bucket flows (1994). These bounds became a basis of the guaranteed service of the IETF integrated services. Lixia Zhang's Virtual Clock (1990) and Golestani's SCFQ (1994) offered cheaper tags, and Bennett and Zhang's WF2Q (1996) removed the burstiness of WFQ. Router vendors later shipped forms of WFQ and of class-based WFQ.

## References
