---
tag: NPTDBB
kind: algorithm
slug: tcp-vegas
name: TCP Vegas
aliases:
- Vegas TCP
area: systems/networking-algorithms
level: advanced
summary: A delay-based TCP congestion control. Once per round trip it compares the expected and the actual rate and keeps between alpha and beta of its packets in the bottleneck queue.
solves: [congestion-control]
model: synchronous-model
complexity:
  vars: {t: the number of round trips}
  time: {worst: Θ(t)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Lawrence S. Brakmo, Sean W. O'Malley, Larry L. Peterson]
  note: Brakmo, O'Malley and Peterson presented TCP Vegas at SIGCOMM 1994. Low, Peterson and Wang gave its equilibrium as a utility maximization in 2002.
prereqs: [tcp-reno, round-trip-time-estimation]
see_also: [congestion-control, bbr-congestion-control, tcp-cubic, proportional-fairness, network-utility-maximization, aimd, active-queue-management, ecn]
sources:
  - paper: doi:10.1145/190314.190317
    title: Lawrence S. Brakmo, Sean W. O'Malley and Larry L. Peterson, TCP Vegas, new techniques for congestion detection and avoidance, ACM SIGCOMM 1994
    locator: pages 24 to 35 (the congestion avoidance mechanism with Expected, Actual, Diff, alpha and beta)
  - paper: doi:10.1109/49.464716
    title: Lawrence S. Brakmo and Larry L. Peterson, TCP Vegas, end to end congestion avoidance on a global Internet, IEEE Journal on Selected Areas in Communications 13(8), 1995
    locator: pages 1465 to 1480 (the mechanism, alpha = 1 and beta = 3 extra buffers, and the modified slow start)
  - paper: doi:10.1145/506147.506152
    title: Steven H. Low, Larry L. Peterson and Limin Wang, Understanding TCP Vegas, a duality model, Journal of the ACM 49(2), 2002
    locator: pages 207 to 235 (Vegas as a distributed algorithm for utility maximization with logarithmic utilities, and the effect of a wrong base RTT)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 6.4 (congestion-avoidance mechanisms, source-based congestion avoidance)
---

TCP Vegas is a delay-based TCP [congestion control](/congestion-control/) by Brakmo, O'Malley and Peterson (1994). Loss-based controls such as [TCP Reno](/tcp-reno/) grow the window until the bottleneck buffer overflows. Vegas instead watches the round-trip time. Once per round trip it compares the rate it would get with an empty queue to the rate it measures, and it turns the difference into an estimate of its own packets in the queue. It adds one segment to the window when that estimate is below $\alpha$, takes one away when it is above $\beta$, and otherwise keeps the window. The usual values are $\alpha = 1$ and $\beta = 3$ packets.

## In plain words

When a router is not busy, a packet goes and comes back in the shortest time the path allows. When the router has a queue, the packet waits, so the trip takes longer. Vegas remembers the shortest trip it has seen and compares it with the current trip.

From the two times it computes how many of its own packets wait in the queue. If fewer than one waits, the path has room, and Vegas sends a little more. If more than three wait, the queue grows, and Vegas sends a little less. Between one and three, it keeps its speed. So the link stays busy, the queue stays short, and Vegas does not need to lose a packet to find the limit.

## The problem

A sender must find the rate of the bottleneck and share it with other flows. A loss-based sender finds the rate only when the buffer overflows, so it keeps the buffer full and adds a queueing delay to every packet of every flow. The problem here is to keep the link busy with a short, stable queue, using only the round-trip times that the sender measures. The model on this page is a fluid one: one link of rate $c$, flows with propagation round-trip times $d_i$, one queueing delay $q$ for all flows, and one step per round trip for every flow.

## The algorithm

The state of a flow is cwnd and BaseRTT, the smallest round-trip time it has measured. Windows count packets, and Diff is in packets.

```pseudo id=main
ON-ROUND()                                       ▷ once per round trip
L1  RTT ← the round-trip time measured in this round
L2  BaseRTT ← min(BaseRTT, RTT)
L3  Expected ← cwnd / BaseRTT                     ▷ the rate with an empty queue
L4  Actual ← cwnd / RTT                           ▷ the rate now
L5  Diff ← (Expected − Actual) · BaseRTT          ▷ packets of this flow in the queue
L6  if Diff < α then cwnd ← cwnd + 1
L7  else if Diff > β then cwnd ← max(cwnd − 1, 2)
L8  else keep cwnd
```

Line L5 is the key step. With $\text{BaseRTT} = d$ and $\text{RTT} = d + q$, the flow sends at $x = \text{cwnd}/(d + q)$, and

$$\text{Diff} = \frac{\text{cwnd}\; q}{d + q} = x\, q,$$

which is the rate of the flow times the time that each packet waits: the number of its packets in the queue. Lines L6 and L7 change the window by one packet per round trip in either direction, so the increase and the decrease are both additive. A loss is still handled as in Reno, by [fast retransmit](/fast-retransmit-fast-recovery/) or a timeout.

## Example

Two flows share a link of $c = 1$ packet per ms, and both have $d = 20$ ms. They start with windows of 2.

| round | 0 | 1 | ... | 8 | 9 | 10 and later |
|---|---|---|---|---|---|---|
| windows | 2, 2 | 3, 3 | ... | 10, 10 | 11, 11 | 11, 11 |
| queueing delay $q$ (ms) | 0 | 0 | ... | 0 | 2 | 2 |
| Diff of each flow | 0 | 0 | ... | 0 | 1 | 1 |

Until round 8 the windows fit in the pipe of 20 packets, $q = 0$, so $\text{Diff} = 0 < \alpha$ and each window grows. In round 9 the total window is 22, so 2 packets wait and $q = 2$ ms. Each flow measures $\text{RTT} = 22$ ms and gets $\text{Diff} = 11 \cdot 2/22 = 1$, which is in $[1, 3]$. Both windows stay. The link is full, each flow gets 0.5 packets per ms, and the queue holds 2 packets.

**Different round-trip times.** With $d = 10$ and $40$ ms on the same link, the windows settle at 9 and 14, with $q = 3.3$ ms and rates 0.677 and 0.323. The Diffs are 2.23 and 1.07. The rate ratio is 2.1, below the limit $\beta/\alpha = 3$. By the square-root law of Reno, two Reno flows with the same loss rate would have a rate ratio equal to the ratio of their round-trip times, here about 3.3.

**A late flow.** Four flows with $d = 20$ ms settle at windows of 7 and $q = 8$ ms. A fifth flow joins and sees a round-trip time of 30 ms in its first round. It takes 30 ms as its BaseRTT, though its true $d$ is 20 ms. The system settles at windows 6, 6, 6, 6 and 10 with $q = 14$ ms. The new flow gets 0.294 packets per ms and the others 0.176 each. Its measured Diff is 1.18, but its true backlog is $0.294 \cdot 14 = 4.1$ packets.

## Correctness

Vegas has no single correct output, so the proof states what its fixed points are in the fluid model. If BaseRTT equals the propagation delay, Diff is exactly the backlog of the flow in the queue. The windows stay fixed only when every Diff is in $[\alpha, \beta]$ or a window is at the floor of 2. No fixed point has an empty queue, so at every fixed point the link is fully used and the queue holds between $n\alpha$ and $n\beta$ packets for $n$ flows. With $\alpha = \beta$, the rates solve the maximization of $\sum_i \alpha \log x_i$ under the link capacity, with $q$ as the Lagrange multiplier. Low, Peterson and Wang prove the general network form of this result. The proof does not show that the windows reach a fixed point from every start.

## Complexity

Each round costs $\Theta(1)$ time per flow, and the state is cwnd and BaseRTT. Because the window changes by at most one packet per round trip, a flow that starts with a window of $w_0$ needs about $w - w_0$ round trips to reach a window of $w$ in congestion avoidance. For a large bandwidth-delay product this is slow, which is why the original Vegas also has a slow start that stops when Diff grows.

## Properties

- **Delay-based.** Vegas reacts to the queue before a loss, so it has few losses and a short queue: at most $\beta$ packets per flow.
- **Little bias against long round-trip times.** The rates of two flows differ by at most $\beta/\alpha$ in the fluid model, whatever their round-trip times.
- **Proportional fairness.** The equilibrium is a weighted [proportionally fair](/proportional-fairness/) allocation, an instance of [network utility maximization](/network-utility-maximization/) with queueing delay as the price.
- **Additive changes only.** The window moves by one packet per round trip in both directions.

## Variants and improvements

- **Modified slow start.** The original Vegas doubles the window only every other round trip, and it leaves slow start when Expected and Actual differ by more than a threshold.
- **FAST TCP** keeps the same equilibrium idea but moves the window in larger steps, for fast long paths.
- **Hybrid controls.** Some later controls use delay only as an extra signal and keep a loss-based mode to compete with Reno and CUBIC.
- **Model-based control.** [BBR](/bbr-congestion-control/) also estimates the minimum round-trip time and aims for a short queue, but it also measures the bottleneck rate and paces at that rate.

## When to use it

Vegas works well when all flows on the bottleneck are delay-based, for example inside one network that one operator controls. It keeps the queue and the delay short. On the open Internet it shares links with loss-based flows, and it usually loses: a Reno or [CUBIC](/tcp-cubic/) flow fills the buffer, Vegas sees a Diff above $\beta$, and it lowers its window round after round.

## Pitfalls

- **A wrong BaseRTT.** A flow that starts while a queue is present takes a round-trip time with queueing as its BaseRTT. It then underestimates its backlog and keeps more packets in the queue than $\beta$, as the late flow in the example. The same happens after a route change to a longer path, when the old BaseRTT is too small: Vegas then reads the new path as a queue and lowers its rate.
- **Persistent queues.** Each new flow adds $\alpha$ to $\beta$ packets to the queue for good, so with many flows the queue is long.
- **Noise in the round-trip time.** Delayed ACKs, cross traffic and timer granularity add noise to line L1. Use a filtered value, such as the minimum of the round, not one sample.
- **Mixing with loss-based flows.** See When to use it. In such a mix Vegas gets far less than its share.

## Implementations

## History

Brakmo, O'Malley and Peterson presented TCP Vegas at SIGCOMM 1994. Next to the congestion avoidance on this page, it changed the retransmission rules and slow start. Brakmo and Peterson gave the full version in the IEEE Journal on Selected Areas in Communications in 1995, with $\alpha = 1$ and $\beta = 3$. Low, Peterson and Wang showed in 2002 that Vegas is a distributed method for a utility maximization in which the queueing delay is the price, and they explained the problems with a wrong base round-trip time.

## References
