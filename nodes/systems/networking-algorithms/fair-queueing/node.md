---
tag: YH4B2M
kind: algorithm
slug: fair-queueing
name: Fair queueing
aliases:
- fair queuing
- FQ
- Demers-Keshav-Shenker fair queueing
area: systems/networking-algorithms
level: advanced
summary: "Give each packet the finish number it would have under bit-by-bit round robin, F = max(F_prev, R(t)) + P, and send the queued packet with the least F."
solves: [packet-scheduling]
model: word-ram
complexity:
  vars: {n: the number of packets}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [packet-scheduling, round-robin, priority-queue]
see_also: [weighted-fair-queueing, generalized-processor-sharing, deficit-round-robin, max-min-fairness, active-queue-management, codel, stride-scheduling, completely-fair-scheduler]
sources:
  - paper: doi:10.1145/75246.75248
    title: Alan Demers, Srinivasan Keshav and Scott Shenker, Analysis and simulation of a fair queueing algorithm, ACM SIGCOMM (1989)
    locator: pp. 1 to 12, Section 2 (bit-by-bit round robin, the round number R(t), the finish number F = max(F_prev, R(t)) + P, and the bid with the parameter delta) and Section 3 (the simulations against FIFO)
  - paper: "Alan Demers, Srinivasan Keshav and Scott Shenker, Analysis and simulation of a fair queueing algorithm, Internetworking, Research and Experience 1(1), 1990, pp. 3 to 26"
    locator: the journal version of the SIGCOMM paper
  - paper: doi:10.1109/TCOM.1987.1096782
    title: John Nagle, On packet switches with infinite storage, IEEE Transactions on Communications 35(4) (1987)
    locator: pp. 435 to 438 (one queue per source host, served in round robin, so that a source that sends too much only fills its own queue)
  - paper: doi:10.1109/90.234856
    title: Abhay K. Parekh and Robert G. Gallager, A generalized processor sharing approach to flow control in integrated services networks, the single-node case, IEEE/ACM Transactions on Networking 1(3) (1993)
    locator: pp. 344 to 357, Section III (the packet-by-packet form of GPS and the bound of one maximum packet time, which covers equal weights)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2012
    locator: Chapter 6, Section 6.2 (fair queuing and the finish time F = max(F_prev, A) + P)
---

Fair queueing (FQ) is a [packet scheduling](/packet-scheduling/) algorithm by Demers, Keshav and Shenker (1989). It keeps one queue per flow and imitates *bit-by-bit round robin*, an ideal scheduler that sends one bit from each backlogged flow in turn. In that ideal, the *round number* $R(t)$ counts the rounds done so far, and it grows at rate $r/N_{active}$ on a link of rate $r$ with $N_{active}$ active flows. A packet of $P$ bits of flow $i$ that arrives at time $t$ gets the finish number

$$F = \max(F_{prev}, R(t)) + P,$$

where $F_{prev}$ is the finish number of the packet of flow $i$ before it. FQ sends the queued packet with the least $F$ and does not preempt. Each packet then finishes at most one maximum packet time after it would finish in the ideal, so each flow gets an equal share of the link and a flow that sends too much fills only its own queue.

## In plain words

Picture a polite gate that lets one bit pass from each sender in turn. Every sender with data gets the same part of the link, and a sender with big packets gets no more than a sender with small ones. But a real link cannot cut packets into bits.

Fair queueing works out, for each packet, when the polite gate would let its last bit through. It writes that time on the packet as a number. When the link is free, it sends the waiting packet with the smallest number, whole.

A sender that floods the link only makes its own numbers grow, so its packets wait in its own line, and the other senders still get their turns.

## The problem

A link of rate $r$ is shared by flows. The aim, as on the [packet scheduling](/packet-scheduling/) page, is to share the link equally among the flows that have data, to bound the delay of each flow whatever the others do, and to keep the link busy. Packet [round robin](/round-robin/), proposed by Nagle in 1987, gives equal packet counts, so a flow with large packets gets more bytes. FIFO gives each flow a share that grows with how much it sends. FQ aims at the [max-min fair](/max-min-fairness/) share in bits.

## The algorithm

A flow is *active* when its last finish number is above the round number, $F_{last}[i] > R$. In the ideal, these are exactly the flows that still have bits to send. The scheduler keeps the round number $R$, the time $clock$ at which $R$ was last brought up to date, the number $N_{active}$ of active flows, and a [priority queue](/priority-queue/) of the queued packets keyed by $F$.

```pseudo id=main
ARRIVE(packet p of flow i, P bits, time t)
L1  ADVANCE(t)
L2  F ← max(F_last[i], R) + P
L3  F_last[i] ← F;  if i was not active then N_active ← N_active + 1
L4  insert p with key F into the priority queue

ADVANCE(t)                                       ▷ R grows at rate r / N_active
L5  while N_active > 0 and R reaches m = min{F_last[i] : i active} by time t:
        clock ← clock + (m − R)·N_active / r;  R ← m;  the flows with F_last = m become inactive
L6  if N_active > 0 then R ← R + (t − clock)·r / N_active
L7  clock ← t

SEND-NEXT()                                      ▷ when the link is free
L8  if the priority queue is not empty then extract the packet with the least F and send it
```

Line L5 is needed because $N_{active}$ changes inside the time interval: each time a flow finishes in the ideal, the other flows speed up. The finish numbers of one flow increase, so its packets leave in FIFO order. A packet that arrives when its flow is idle in the ideal starts at the current round, so an idle flow cannot save up credit.

## Example

A link sends 1 byte per time unit. At time 0, flow A has two packets of 4 bytes and flow B one packet of 2 bytes. At time 1, a packet of 6 bytes of flow C arrives.

| packet | arrives | $R$ at arrival | $F$ | FQ sends | ideal finish |
|---|---|---|---|---|---|
| B1 | 0 | 0 | 2 | 0 to 2 | 5.5 |
| A1 | 0 | 0 | 4 | 2 to 6 | 9.5 |
| C1 | 1 | 0.5 | 6.5 | 6 to 12 | 14.5 |
| A2 | 0 | 0 | 8 | 12 to 16 | 16 |

At time 0, two flows are active, so $R$ grows at rate $1/2$ and $R(1) = 0.5$. From time 1 three flows share the link, so $R$ grows at rate $1/3$ and reaches 2, the finish number of B1, at time $1 + 3 \cdot 1.5 = 5.5$. The last column is the time at which $R$ reaches $F$, which is the finish time in the ideal. FQ finishes B1, A1 and C1 earlier than the ideal here, because it sends whole packets at the full rate, and it finishes A2 at the same time. No packet finishes more than $L_{max}/r = 6$ after the ideal.

**Isolation.** On a link of 1 byte per time unit, flow H sends 1500 bytes every 750 time units, twice the link rate, and flow L sends 100 bytes every 1000 time units. Under FIFO, the queue of H grows without bound, and after 300 packets of L the last one waits 329,493 time units. Under FQ, the largest delay of an L packet is 1593, within the bound of $200 + 1500$: the ideal time of 100 bytes at half the link plus one packet of H.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **The finish number is the ideal finish.** In the fluid limit of bit-by-bit round robin, where each active flow is served at rate $r / N_{active}$, packet $p$ finishes at the first time $d_p$ at which $R(t) = F_p$. So a smaller finish number means an earlier ideal finish.
2. **One packet of lag.** Let $\hat d_p$ be the time at which FQ finishes packet $p$. Then for every packet,

$$\hat d_p \le d_p + \frac{L_{max}}{r},$$

where $L_{max}$ is the largest packet. This is the theorem of Parekh and Gallager for packet-by-packet GPS, in the case of equal weights.
3. **Fair shares.** In the ideal, two flows that are both backlogged over an interval get the same number of bits. By property 2, FQ differs from the ideal by at most a few maximum packets over any interval.

## Complexity

Each arrival does one insertion into the priority queue and each departure one extraction, which take $O(\log n)$ time with a [binary heap](/binary-heap/). Each pass of the loop of line L5 makes one flow inactive, and each arrival makes at most one flow active, so over the whole run the loop makes at most $n$ passes. With a heap of active flows, each pass costs $O(\log n)$. So $n$ packets cost $O(n \log n)$ time in total. One arrival may make many flows inactive at once, so one call of ADVANCE can cost $O(N \log n)$ for $N$ flows. The space is $\Theta(n)$ for the queued packets plus $O(N)$ for the flow state. The cost of tracking $R$ led to simpler schemes such as SCFQ and [deficit round robin](/deficit-round-robin/).

## Properties

- **Work conserving.** The link is never idle while a packet waits.
- **Isolation.** A flow that sends faster than its share only lengthens its own queue.
- **Fair in bits, not packets.** A flow of small packets gets the same bit rate as a flow of large packets.
- **No credit for idle time.** A flow that was idle starts at the current round number, so it cannot later take more than its share.
- **Not worst-case fair.** FQ can send a flow's packets ahead of the ideal by many packets, then serve the flow nothing for a while. WF2Q fixes this.

## Variants and improvements

- **[Weighted fair queueing](/weighted-fair-queueing/).** Give flow $i$ a weight $\varphi_i$ and use $F = \max(F_{prev}, V(t)) + P/\varphi_i$, with a virtual time that grows at rate $r/\sum \varphi$ over the backlogged flows. Parekh and Gallager analysed this as packetized [GPS](/generalized-processor-sharing/).
- **Promptness.** Demers, Keshav and Shenker also proposed a bid $B = P + \max(F_{prev}, R(t) - \delta)$, which lets a flow that has been idle get a small delay advantage, at the cost of fairness in the short term.
- **A buffer policy.** When the buffer is full, they drop a packet of the flow that uses the most buffer space, so that a flood cannot push out the packets of other flows.
- **Stochastic fairness queueing.** McKenney (1990) hashes flows into a fixed number of queues served in round robin, so the state does not grow with the number of flows.
- **Cheaper approximations.** SCFQ uses the finish number of the packet in service in place of $R(t)$. [Deficit round robin](/deficit-round-robin/) gives fairness in bytes with $O(1)$ work per packet.
- **Flow queueing with AQM.** FQ-CoDel serves hashed flow queues by deficit round robin and runs [CoDel](/codel/) on each queue.

## When to use it

Use fair queueing, or one of its approximations, when many flows share a bottleneck and no flow should be able to take the link from the others: router ports, home gateways and host network stacks. When per-packet work must be $O(1)$, use [deficit round robin](/deficit-round-robin/). When flows need different shares or delay guarantees, use [weighted fair queueing](/weighted-fair-queueing/) or WF2Q.

## Pitfalls

- **A round number that counts time.** $R$ grows at rate $r/N_{active}$, not at rate $r$. Using the wall clock in place of $R$ turns FQ into Virtual Clock, which can punish a flow for using idle capacity.
- **Counting the wrong flows.** $N_{active}$ counts the flows that are active in the ideal ($F_{last} > R$), not the flows that have packets in the real queue. The two sets differ, because the real scheduler can be ahead of or behind the ideal.
- **Forgetting the events inside an interval.** If ADVANCE uses one rate for a whole interval in which flows become inactive, $R$ comes out too small.
- **Tie-breaking.** Packets with equal finish numbers need a fixed rule, such as the arrival order, or the results depend on the heap.
- **Preemption.** FQ never stops a packet in service. The bound of one packet time is the price of that, and a large maximum packet makes it large.

## Implementations

## History

John Nagle proposed in 1987 that a packet switch keep a separate queue for each source and serve the queues in round robin, so that a badly behaved source fills only its own queue. Alan Demers, Srinivasan Keshav and Scott Shenker presented fair queueing at SIGCOMM 1989. Their algorithm made the shares fair in bits, by imitating bit-by-bit round robin with the round number and finish numbers, and they showed by simulation that it protects well-behaved TCP flows from aggressive ones. In 1993, Parekh and Gallager generalized the ideal to weighted fluid sharing, GPS, and proved the bound of one maximum packet time for the packet scheduler, which covers fair queueing as the case of equal weights.

## References
