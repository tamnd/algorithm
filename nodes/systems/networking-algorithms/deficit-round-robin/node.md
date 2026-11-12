---
tag: 4F8MEF
kind: algorithm
slug: deficit-round-robin
name: Deficit round robin
aliases:
- DRR
- deficit round-robin scheduler
area: systems/networking-algorithms
level: advanced
summary: "Visit the flow queues in round robin; at each turn add a byte quantum to the flow's deficit counter and send head packets while they fit, for O(1) work per packet."
solves: [packet-scheduling]
model: word-ram
complexity:
  vars: {n: the number of packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [fair-queueing, round-robin]
see_also: [weighted-fair-queueing, generalized-processor-sharing, packet-scheduling, codel, stride-scheduling, lottery-scheduling, max-min-fairness, queue]
sources:
  - paper: doi:10.1109/90.502236
    title: M. Shreedhar and George Varghese, Efficient fair queuing using deficit round-robin, IEEE/ACM Transactions on Networking 4(3) (1996)
    locator: pp. 375 to 385 (the algorithm, the fairness measure FM at most 2 Max + Q, the O(1) work when Quantum is at least Max, and the latency)
  - paper: "M. Shreedhar and George Varghese, Efficient fair queuing using deficit round robin, ACM SIGCOMM 1995, pp. 231 to 242"
    locator: Section 3 (the algorithm and its pseudocode), Section 4 (Lemma 4.1, that 0 is at most DeficitCounter which is less than Max after a turn; Theorem 4.2, that after K rounds the bytes sent differ from K times Quantum by at most Max; Theorem 4.5, O(1) work per packet)
  - paper: doi:10.1109/TCOM.1987.1096782
    title: John Nagle, On packet switches with infinite storage, IEEE Transactions on Communications 35(4) (1987)
    locator: pp. 435 to 438 (round robin over per-source queues, the packet form that DRR corrects for sizes)
  - url: https://www.rfc-editor.org/rfc/rfc8290
    title: Toke Høiland-Jørgensen, Paul McKenney, Dave Taht, Jim Gettys and Eric Dumazet, The Flow Queue CoDel Packet Scheduler and Active Queue Management Algorithm, RFC 8290, 2018
    locator: Section 4 (a DRR scheduler over hashed flow queues, with a list for new flows)
  - book: isbn:9780120884773
    title: George Varghese, Network Algorithmics, Morgan Kaufmann, 2005
    locator: Chapter 14 (scheduling packets, deficit round robin)
---

Deficit round robin (DRR) is a [packet scheduling](/packet-scheduling/) algorithm by Shreedhar and Varghese (1995). It serves the flow queues in [round robin](/round-robin/) order, like Nagle's packet round robin, but it counts bytes, not packets. Each flow $i$ has a quantum $Q_i$ in bytes and a deficit counter $DC_i$. At its turn, the flow adds $Q_i$ to $DC_i$ and sends head packets as long as the head packet is no larger than $DC_i$, subtracting each size. The rest of the counter carries over to the next turn, so a flow whose packet did not fit gets the bytes later. Over any interval in which two flows stay backlogged, the bytes they send differ by less than $Q + 2\,Max$ when both have quantum $Q$, where $Max$ is the largest packet. When $Q_i \ge Max$, every turn sends at least one packet, so the work is $O(1)$ per packet.

## In plain words

Several lines of packets share one link. Plain round robin takes one packet from each line in turn. That is unfair when one line has big packets and another has small ones: the line with big packets gets more of the link.

Deficit round robin gives each line an allowance of bytes at each turn. A line may send packets as long as they fit in its allowance. If the next packet is too big, the line keeps the unused allowance and tries again at its next turn, with more allowance added.

Over time every line sends about the same number of bytes per turn. The work per packet stays small, because the scheduler only visits lines in a fixed order and never sorts anything.

## The problem

A link serves $N$ flows, each with its own FIFO [queue](/queue/). The aim is the same as for [fair queueing](/fair-queueing/): share the link among the backlogged flows in proportion to given weights, measured in bytes, and isolate the flows. Fair queueing and [WFQ](/weighted-fair-queueing/) need a priority queue and a virtual time, so they cost $O(\log n)$ per packet or more. DRR aims at fairness over the long run with a constant number of operations per packet.

## The algorithm

The scheduler keeps the ActiveList, a FIFO list of the flows with packets, and for each flow its queue, quantum $Q_i$ and counter $DC_i$. The pseudocode returns one packet per call of DEQUEUE and keeps the turn in progress between calls.

```pseudo id=main
ENQUEUE(packet p of flow i)
L1  append p to queue i
L2  if i is not in the ActiveList then add i at the tail;  DC_i ← 0

DEQUEUE()
L3  while the ActiveList is not empty:
L4      i ← the head of the ActiveList
L5      if the turn of i has not started then DC_i ← DC_i + Q_i;  start the turn
L6      if size(head of queue i) ≤ DC_i then
L7          remove the head p of queue i;  DC_i ← DC_i − size(p)
L8          if queue i is empty then DC_i ← 0;  remove i from the ActiveList;  end the turn
L9          return p
L10     move i to the tail of the ActiveList;  end the turn
L11 return none
```

Line L8 resets the counter of a flow that empties, so a flow cannot save up credit while it is idle. Line L10 ends a turn when the head packet does not fit; the counter keeps what is left.

## Example

Three flows have quantum 500 bytes. Flow A has packets of 200, 750 and 300 bytes, flow B two packets of 500, and flow C one packet of 1000.

| turn | flow | $DC$ after adding $Q$ | sends | $DC$ at the end |
|---|---|---|---|---|
| 1 | A | 500 | 200 | 300 (750 does not fit) |
| 2 | B | 500 | 500 | 0 |
| 3 | C | 500 | nothing | 500 |
| 4 | A | 800 | 750 | 50 |
| 5 | B | 500 | 500 | 0, B leaves |
| 6 | C | 1000 | 1000 | 0, C leaves |
| 7 | A | 550 | 300 | 0, A leaves |

C's first turn sends nothing, because its packet is larger than the quantum. This is the only empty turn, and it happens because $Q < Max$.

**Packet round robin against DRR.** Flow "big" sends 1500-byte packets and flow "small" sends 100-byte packets, both always backlogged. Packet round robin gives "big" 15 times the bytes of "small". DRR with quantum 1500 for both sends one big packet or 15 small packets per turn, and after 3000 packets the byte counts differ by at most 1500.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). Let $M$ be the largest packet size.

1. **The counter stays small.** At the end of a turn of a flow that stays backlogged, $0 \le DC_i < M$ (Lemma 4.1 of the paper). During a turn, $DC_i < Q_i + M$.
2. **Fairness over any interval.** Let flows $i$ and $j$ stay in the ActiveList over an interval, and let $s_i$ and $s_j$ be the bytes they send in it. Then

$$\left| \frac{s_i}{Q_i} - \frac{s_j}{Q_j} \right| < 1 + \frac{M}{Q_i} + \frac{M}{Q_j}.$$

With equal quanta $Q$, this is $|s_i - s_j| < Q + 2M$, the bound $FM \le 2\,Max + Q$ of Shreedhar and Varghese.
3. **Long-run shares.** After $K$ turns of a backlogged flow $i$, the bytes it has sent are within $M$ of $K Q_i$ (Theorem 4.2 of the paper), so backlogged flows get bytes in proportion to their quanta.
4. **Constant work.** If $Q_i \ge M$ for every flow, every turn sends at least one packet (Theorem 4.5 of the paper).

## Complexity

Each packet is handled once at line L1 and once at lines L6 to L9. Each turn costs $O(1)$ apart from the packets it sends. If every $Q_i \ge M$, each turn sends at least one packet, so the number of turns is at most the number of packets and $n$ packets cost $\Theta(n)$ time, $O(1)$ per packet. If some $Q_i < M$, a flow may need up to $\lceil M / Q_i \rceil$ turns to send one packet, so the work per packet is $O(M / Q_{min})$. The space is $\Theta(n)$ for the queued packets and $O(N)$ for the counters and the list. No priority queue and no virtual time are needed.

## Properties

- **Fair in bytes over the long run.** Unlike packet round robin, the shares do not depend on packet sizes.
- **Weighted shares.** Quanta in the ratio of the weights give weighted shares, as in [WFQ](/weighted-fair-queueing/).
- **Coarse in the short run.** Within a round, a flow sends up to $Q_i + M$ bytes at once. The delay of a packet can grow with the number of flows times the quantum, which is worse than the delay bound of WFQ.
- **No credit for idle time.** Line L8 resets the counter when a flow empties.
- **Simple to build.** The state is a counter per flow and one list, which suits hardware and kernels.

## Variants and improvements

- **FQ-CoDel (RFC 8290).** A DRR scheduler over hashed flow queues, with a separate list for new flows so that short flows go first, and [CoDel](/codel/) on each queue. It is the default queue discipline of many Linux systems.
- **Surplus round robin.** Let a flow send its last packet even if it does not fit, and carry the surplus as a negative counter. This avoids empty turns when the quantum is small.
- **DRR+.** Shreedhar and Varghese also describe a form with a priority list for latency-critical flows that keep within an agreed rate.
- **Hashed flows.** With many flows, hash them into a fixed number of queues, as in stochastic fairness queueing, and run DRR over the buckets.
- **Weighted round robin.** Sending a fixed number of packets per turn in proportion to the weights is fair only when the packet sizes are known and equal.

## When to use it

Use DRR when many flows must share a link fairly in bytes and the per-packet budget is a few operations: router line cards, software routers and host queue disciplines. Use [WFQ](/weighted-fair-queueing/) or WF2Q when tight delay bounds per flow matter more than the cost. Set every quantum to at least the largest packet, so that each turn sends a packet.

## Pitfalls

- **A quantum below the largest packet.** The algorithm stays fair, but turns that send nothing waste work, and the $O(1)$ bound is lost.
- **Not resetting the counter.** If line L8 keeps $DC_i$ when the queue empties, an idle flow saves up credit and later sends a large burst.
- **Restarting the turn.** When DEQUEUE returns one packet at a time, the scheduler must remember that the turn of the head flow has started, or it adds the quantum again on each call.
- **Reading the bound as a delay bound.** The fairness bound is about bytes sent, not about the delay of one packet, which can be large when there are many flows.

## Implementations

## History

John Nagle proposed packet round robin over per-source queues in 1987. Demers, Keshav and Shenker made the shares fair in bits in 1989, at the cost of sorted tags. M. Shreedhar and George Varghese presented deficit round robin at SIGCOMM 1995, with a journal version in IEEE/ACM Transactions on Networking in 1996, and showed that a counter per flow gives fairness in bytes with constant work per packet. DRR became one of the most used fair schedulers in routers. In 2012, FQ-CoDel combined it with CoDel, and RFC 8290 described that combination in 2018.

## References
