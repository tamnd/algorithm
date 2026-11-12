---
tag: A9935B
kind: algorithm
slug: red-random-early-detection
name: Random early detection
aliases:
- RED
- random early detection
- RED gateway
area: systems/networking-algorithms
level: intro
summary: "A router marks or drops each arriving packet with a probability that rises with the average queue length, so that marks are spread out and spaced almost evenly."
model: word-ram
complexity:
  vars: {n: the number of arriving packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: false, recursive: false}
prereqs: [active-queue-management, exponential-moving-average]
see_also: [codel, pie-aqm, ecn, congestion-control, aimd, tcp-reno, fair-queueing]
sources:
  - paper: doi:10.1109/90.251892
    title: Sally Floyd and Van Jacobson, Random early detection gateways for congestion avoidance, IEEE/ACM Transactions on Networking 1(4) (1993)
    locator: pp. 397 to 413; Section 4 (the algorithm), Section 6 (the queue weight w_q and the ramp example), Section 7 (the marking probability, Method 1 against Method 2 and the uniform gap)
  - url: https://www.rfc-editor.org/rfc/rfc2309
    title: Bob Braden et al., Recommendations on Queue Management and Congestion Avoidance in the Internet, RFC 2309, 1998
    locator: Section 3 (the problems of drop-tail queues) and Section 4 (the recommendation of active queue management, with RED as the example)
  - url: https://www.rfc-editor.org/rfc/rfc7567
    title: Fred Baker and Godred Fairhurst, IETF Recommendations Regarding Active Queue Management, RFC 7567 (BCP 197), 2015
    locator: Section 1 and Section 4 (RFC 2309 is obsoleted, AQM is still recommended, and the AQM must not need tuning of its parameters)
  - url: https://www.icir.org/floyd/red/gentle.html
    title: Sally Floyd, Recommendation on using the gentle variant of RED, 2000
    locator: the whole note (the marking probability rises from max_p to 1 as the average goes from max_th to twice max_th)
  - url: https://www.icir.org/floyd/papers/adaptiveRed.pdf
    title: Sally Floyd, Ramakrishna Gummadi and Scott Shenker, Adaptive RED, an algorithm for increasing the robustness of RED's active queue management, technical report, ICSI, 2001
    locator: the algorithm that adapts max_p
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition, Morgan Kaufmann, 2012
    locator: Chapter 6, Section 6.4 (congestion-avoidance mechanisms, random early detection)
---

Random early detection (RED) is an [active queue management](/active-queue-management/) algorithm for a router queue. Floyd and Jacobson proposed it in 1993. For each arriving packet, RED updates an [exponential moving average](/exponential-moving-average/) of the queue length. When the average lies between two thresholds, RED marks the packet with a probability that grows with the average; above the upper threshold it marks every packet. A mark is a drop, or an [ECN](/ecn/) mark when the flow supports it. A count of the unmarked packets since the last mark makes the gaps between marks close to uniform rather than geometric. Each decision takes $O(1)$ time.

## In plain words

A router has a waiting line of packets. If the line stays long, the senders send too fast. RED warns them early, before the line is full. It does not look at the line length at one moment, because short bursts are normal. It keeps a slow running average of the length.

When the average is small, RED lets every packet in. When the average is between a low mark and a high mark, RED picks some packets at random and drops them (or marks them). The higher the average, the more packets it picks. A sender that loses a packet slows down. Because the picks are random, the senders slow down at different times, not all at once. RED also makes sure that the picks do not come in clumps or leave long gaps.

## The problem

A router port has a FIFO queue in front of a link. Packets arrive at the queue at times that RED does not control. The input to RED is, for each arriving packet, the queue length $q$ in packets (or bytes) at its arrival and the time. The output is a decision for each packet: enqueue it, or mark it. A marked packet is dropped, or carries an [ECN](/ecn/) congestion mark. The aims are those of [active queue management](/active-queue-management/): a small average queue and so a small delay, high use of the link, no bias against bursty flows, and no global synchronization of the [TCP](/tcp-reno/) senders.

The parameters are the queue weight $w_q \in (0, 1]$, the thresholds $0 \le min_{th} < max_{th}$, the maximum probability $max_p \in (0, 1]$, and the time $s$ to send a typical small packet.

## The algorithm

RED keeps three values: the average $avg$, the count $count$ of unmarked packets since the last mark, and the time $q_{time}$ when the queue last became empty. At the start, $avg = 0$ and $count = 0$.

```pseudo id=main
RED-ARRIVAL(q, now)                         ▷ q: the queue length when the packet arrives
L1  if q > 0 then avg ← (1 − w_q)·avg + w_q·q
L2  else m ← (now − q_time)/s;  avg ← (1 − w_q)^m · avg     ▷ decay over the idle time
L3  if avg < min_th then count ← 0;  return ENQUEUE
L4  if avg ≥ max_th then count ← 0;  return MARK
L5  p_b ← max_p · (avg − min_th)/(max_th − min_th)
L6  p_a ← p_b / (1 − count·p_b)                              ▷ 1 if the result is not in (0, 1)
L7  with probability p_a:  count ← 0;  return MARK
L8  count ← count + 1;  return ENQUEUE
```

Line L1 is the low-pass filter. Line L2 handles an idle period: the router acts as if $m$ small packets had arrived to an empty queue, so a long idle time pulls the average down. Lines L3 and L4 are the two regions where the answer is fixed. Line L5 gives the base probability $p_b$, which rises in a straight line from 0 at $min_{th}$ to $max_p$ at $max_{th}$. Line L6 is the count correction: the probability grows with each unmarked packet, and reaches 1 when $count \ge 1/p_b - 1$.

In byte mode, line L5 scales $p_b$ by the size of the packet over the maximum size, so that a large packet is more likely to be marked than a small one.

## Example

**The probability as the count grows.** Take $min_{th} = 5$, $max_{th} = 15$ and $max_p = 0.1$, and let the average stay at $avg = 10$. Then $p_b = 0.1 \cdot 5/10 = 0.05$, and line L6 gives:

| count | 0 | 5 | 10 | 15 | 18 | 19 |
|---|---|---|---|---|---|---|
| $p_a$ | 0.05 | 0.0667 | 0.1 | 0.2 | 0.5 | 1 |

So the 20th packet after a mark is always marked, and the gap $X$ between marks is uniform on $\{1, \ldots, 20\}$ with mean $10.5$. Without the correction, $X$ is geometric with mean 20, and $\Pr[X > 20] = 0.95^{20} \approx 0.358$.

**A seeded run of the gap law.** With $avg$ frozen so that $p_b = 0.1$, 50,000 arrivals (seed 7) gave 9,098 marks. Each gap length from 1 to 10 occurred between 866 and 947 times, and no gap was longer than 10. With a plain coin of probability 0.1 and the same seed, 35.5 percent of the gaps were longer than 10, against $0.9^{10} \approx 0.349$ in theory.

**The slow average.** Let the queue grow by one packet at each arrival, from 1 to 100, with $w_q = 0.001$. The average after the 100th arrival is

$$avg_{100} = \sum_{k=1}^{100} w_q (1 - w_q)^{100-k} k = 101 + \frac{(1 - w_q)^{101} - 1}{w_q} \approx 4.89.$$

So a burst of 100 packets moves the average by less than 5 packets. This is the example of Floyd and Jacobson, Section 6. The time constant of the filter is about $1/w_q = 1000$ arrivals.

**A loaded queue.** A queue serves one packet per slot. Each slot brings one packet, or two with probability 0.05, so the load is 1.05. With $w_q = 0.002$, the thresholds 5 and 15, $max_p = 0.1$ and a buffer of 40 (seeds 3 and 4), over 20,000 slots RED dropped 1,032 packets early and none by overflow, which is 4.9 percent of the arrivals. The average in the second half was 7.39 packets, and the queue never held more than 22. The excess load needs a drop rate of $0.05/1.05 \approx 4.8$ percent. At $avg = 7.39$, $p_b \approx 0.024$, and with uniform gaps the rate of marks is $2p_b/(1 + p_b) \approx 4.7$ percent, which matches.

## Correctness

RED does not compute a function, so "correct" here means that it has the properties that it was designed for. The proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **The gap law.** If $avg$ stays fixed with $p_b$ in $(0, 1)$, the number $X$ of packets from one mark to the next (the marked packet included) has $\Pr[X = n] = p_b$ for $n = 1, \ldots, \lfloor 1/p_b \rfloor$, and the rest of the mass on $n = \lfloor 1/p_b \rfloor + 1$. When $1/p_b$ is an integer, $X$ is uniform on $\{1, \ldots, 1/p_b\}$ with $E[X] = (1/p_b + 1)/2$. This is Method 2 of Floyd and Jacobson, Section 7.
2. **The average.** After arrivals with queue lengths $q_1, \ldots, q_k$ and no idle period, $avg_k = (1 - w_q)^k avg_0 + \sum_{j=1}^{k} w_q (1 - w_q)^{k-j} q_j$. The weights add up to 1, so $avg$ always lies between the least and the largest of $avg_0, q_1, \ldots, q_k$.
3. **No bias against a flow.** The decision of lines L3 to L8 depends on $avg$, $count$ and a coin, not on the flow of the packet. So two packets that arrive in the same state have the same chance of a mark, whatever their flows send.

## Complexity

Each arrival takes $O(1)$ time: a multiply and an add for the average, two compares, and one random number when the average is between the thresholds. The power $(1 - w_q)^m$ of line L2 is one call of a power function, or a lookup in a small table when $m$ is rounded. For $n$ arrivals the time is $\Theta(n)$. The state is three numbers, so the extra space is $\Theta(1)$ per queue. RED needs no state per flow.

## Properties

- **A heuristic with no worst-case guarantee.** No theorem bounds the queue or the delay that RED gives. Its behavior depends on the load, the number of flows and their round-trip times. What holds is the gap law and the fixed relation between $avg$ and $p_b$.
- **The average moves slowly.** A burst passes through without marks if it is short compared with $1/w_q$ arrivals. A queue that stays long raises the average and so the marks.
- **Random marks break synchronization.** Different flows get marks at different times, so they do not all halve their windows at once. This is the global synchronization that drop-tail queues cause.
- **Marks are about twice as frequent as $p_b$.** With uniform gaps the rate of marks is $1/E[X] = 2p_b/(1 + p_b)$, not $p_b$.
- **The average queue depends on the load.** For a fixed set of parameters, more flows need a higher drop rate, and so a higher average. The operator cannot set a target delay.

## Variants and improvements

- **Gentle RED.** Between $max_{th}$ and $2\,max_{th}$, the probability rises in a line from $max_p$ to 1, in place of the jump to 1 at $max_{th}$. Floyd recommended this change in 2000.
- **Adaptive RED.** Floyd, Gummadi and Shenker (2001) adapt $max_p$ slowly, so that the average stays between the thresholds when the load changes.
- **Weighted RED.** Routers keep separate thresholds for different classes of traffic in one queue.
- **RED with ECN.** The router sets the congestion bit in place of a drop when the flow supports [explicit congestion notification](/ecn/).
- **Delay-based successors.** [CoDel](/codel/) controls the time that packets spend in the queue, with no thresholds to tune. [PIE](/pie-aqm/) controls an estimate of the queueing delay with a proportional-integral controller.

## When to use it

Use RED where a router has a single FIFO queue and the traffic is many TCP flows that respond to loss or ECN marks. Set $max_{th}$ to at least twice $min_{th}$, as Floyd and Jacobson suggest, and set $min_{th}$ high enough to keep the link busy. When you cannot tune the parameters for the link rate and the traffic, prefer [CoDel](/codel/) or [PIE](/pie-aqm/), whose targets are in units of time. When flows must be isolated from each other, put an AQM behind a [fair queueing](/fair-queueing/) scheduler.

## Pitfalls

- **Off by one in the count.** Line L6 must use the number of unmarked packets before this one. If $count$ also counts the arriving packet, the gap is uniform on $\{1, \ldots, 1/p_b - 1\}$, each value with probability $p_b/(1 - p_b)$.
- **Using the current queue length.** Without the average, RED marks packets in every burst, and becomes a random form of drop-tail.
- **Forgetting the idle period.** Without line L2, the average stays high after the queue empties, and the first packets after the idle time are marked for no reason.
- **The jump at max_th.** With plain RED, the drop rate jumps from $max_p$ to 1 when the average passes $max_{th}$. This can cause oscillation; gentle RED removes the jump.
- **Parameters that depend on the link.** Thresholds in packets mean different delays at 10 Mbit/s and at 10 Gbit/s. Many deployments left RED switched off because it was hard to tune; RFC 7567 asks that an AQM work without such tuning.
- **Treating RED as fair.** RED drops from each flow in proportion to its arrivals, so a flow that does not respond to drops still takes a large share of the link.

## Implementations

## History

Floyd and Jacobson published RED in the IEEE/ACM Transactions on Networking in August 1993. They built on the earlier Random Drop and Early Random Drop gateways and on the DECbit scheme, and they added the average queue length and the count-based spacing of marks. RFC 2309 (Braden et al., 1998) recommended active queue management for the Internet, with RED as its example. RFC 7567 (Baker and Fairhurst, 2015) replaced RFC 2309. It keeps the recommendation of AQM, but it no longer names RED, because RED was hard to tune and was seldom switched on.

## References
