---
tag: 74M4VC
kind: algorithm
slug: codel
name: CoDel
aliases:
- controlled delay
- CoDel AQM
area: systems/networking-algorithms
level: advanced
summary: "Drop at dequeue when the sojourn time of packets has stayed above a target (5 ms) for an interval (100 ms), and space the next drops by interval over the square root of the count."
model: word-ram
complexity:
  vars: {n: the number of arriving packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [active-queue-management]
see_also: [red-random-early-detection, pie-aqm, ecn, fair-queueing, deficit-round-robin, tcp-reno, congestion-control]
sources:
  - paper: doi:10.1145/2208917.2209336
    title: Kathleen Nichols and Van Jacobson, Controlling queue delay, ACM Queue 10(5) (2012)
    locator: pp. 20 to 34 (good and bad queue, the sojourn time, the minimum over an interval, and the control law); also in Communications of the ACM 55(7), 2012, pp. 42 to 50
  - url: https://www.rfc-editor.org/rfc/rfc8289
    title: Kathleen Nichols, Van Jacobson, Andrew McGregor and Jana Iyengar, Controlled Delay Active Queue Management, RFC 8289, 2018
    locator: Section 3 (the building blocks), Section 4.3 and Section 4.4 (TARGET and INTERVAL), Section 5 (the pseudocode, with dodequeue in Section 5.6 and the dropping state in Section 5.5)
  - url: https://www.rfc-editor.org/rfc/rfc8290
    title: Toke Høiland-Jørgensen, Paul McKenney, Dave Taht, Jim Gettys and Eric Dumazet, The Flow Queue CoDel Packet Scheduler and Active Queue Management Algorithm, RFC 8290, 2018
    locator: Section 4 (CoDel on each flow queue of a deficit round-robin scheduler)
  - url: https://www.rfc-editor.org/rfc/rfc7567
    title: Fred Baker and Godred Fairhurst, IETF Recommendations Regarding Active Queue Management, RFC 7567 (BCP 197), 2015
    locator: Section 4 (an AQM should not need tuning)
---

CoDel (controlled delay) is an [active queue management](/active-queue-management/) algorithm that Nichols and Jacobson published in 2012 and that RFC 8289 specifies. It measures the *sojourn time* of each packet, the time from its arrival in the queue to its departure. When the sojourn time has stayed at or above a target of 5 ms for a full interval of 100 ms, CoDel enters a dropping state. In that state it drops a packet at dequeue, and it sets the time of the next drop to the last drop time plus $\text{interval}/\sqrt{count}$, so drops come faster until the delay falls below the target. The two constants are in units of time, so the same values work on links of very different rates. CoDel is a heuristic: it has no worst-case bound on the delay, and it relies on senders that respond to drops.

## In plain words

Think of a line at a counter. A line that forms when a crowd arrives and then goes away is fine. A line that never gets short is a problem: people wait for no gain.

CoDel watches how long each packet waited when it leaves the line. If every packet in the last tenth of a second waited more than five thousandths of a second, the line is not going away. CoDel then throws away one packet, so that its sender slows down. If the line still does not go away, CoDel throws away the next packet a little sooner, and the next one sooner again. As soon as a packet leaves with a short wait, CoDel stops.

So a short crowd passes without any loss, and a line that stays long is cut back.

## The problem

A FIFO [queue](/queue/) feeds a link. The queue stamps each packet with its arrival time. The link asks for a packet each time it is free. At each dequeue the AQM may drop the head packet instead of sending it. The aim is to remove a standing queue (bad queue) and to keep the short queues that bursts make (good queue), as described on the [active queue management](/active-queue-management/) page. The time is in milliseconds; the constants are

- TARGET $= 5$ ms, the acceptable standing delay;
- INTERVAL $= 100$ ms, about one worst-case round-trip time of the flows;
- MAXPACKET, the size of the largest packet, in bytes.

## The algorithm

The state is the time $first\_above$ (or none), the dropping flag, the next drop time $drop\_next$, the drop $count$ and the $lastcount$ of the previous dropping state. DODEQUEUE pops the head packet and tells whether the queue is in the "above target for a full interval" condition.

```pseudo id=main
DODEQUEUE(now)
L1  if the queue is empty then first_above ← none;  return (none, false)
L2  p ← pop the head;  s ← now − p.stamp                    ▷ the sojourn time
L3  if s < TARGET or bytes left ≤ MAXPACKET then first_above ← none;  return (p, false)
L4  if first_above = none then first_above ← now + INTERVAL;  return (p, false)
L5  return (p, now ≥ first_above)

DEQUEUE(now)
L6  (p, ok) ← DODEQUEUE(now)
L7  if p = none then dropping ← false;  return none
L8  if dropping then
L9      if not ok then dropping ← false
L10     while dropping and now ≥ drop_next do
L11         drop p;  count ← count + 1;  (p, ok) ← DODEQUEUE(now)
L12         if not ok then dropping ← false  else drop_next ← drop_next + INTERVAL/√count
L13 else if ok then
L14     drop p;  (p, ok) ← DODEQUEUE(now);  dropping ← true
L15     delta ← count − lastcount;  count ← 1
L16     if delta > 1 and now − drop_next < 16·INTERVAL then count ← delta
L17     drop_next ← now + INTERVAL/√count;  lastcount ← count
L18 return p
```

Lines L3 and L4 implement the minimum of the sojourn time over a sliding interval: $first\_above$ is reset whenever one packet leaves with a sojourn time below the target, so $ok$ becomes true only when every packet for INTERVAL has been above it. The test on MAXPACKET keeps CoDel from dropping when at most one packet is left, since such a queue cannot be a standing queue. Lines L10 to L12 are the control law: the gap between drops is INTERVAL$/\sqrt{count}$. The `while` loop can drop several packets at one dequeue when the next drop time is already past. Lines L15 and L16 come from the Linux code: if CoDel enters the dropping state again soon after it left, it starts from the number of drops of the last state, not from 1, because the old drop rate was probably close to right.

## Example

**The control law.** 1000 packets of 1500 bytes arrive at time 0 at a link that sends one packet per millisecond (12 Mbit/s). A packet that leaves at time $t$ has sojourn time $t$.

| time (ms) | event | count | next drop at |
|---|---|---|---|
| 5 | first sojourn time at TARGET; $first\_above = 105$ | 0 | |
| 105 | enter the dropping state, drop | 1 | $105 + 100 = 205$ |
| 205 | drop | 2 | $205 + 100/\sqrt 2 = 275.71$ |
| 276 | drop | 3 | $275.71 + 57.74 = 333.45$ |
| 334 | drop | 4 | $333.45 + 50 = 383.45$ |
| 384 | drop | 5 | $383.45 + 44.72 = 428.17$ |
| 429 | drop | 6 | $428.17 + 40.82 = 468.99$ |

The drops happen at the first dequeue at or after each time of the last column, so they come at 105, 205, 276, 334, 384, 429, 469 and 507 ms. The next time is computed from the planned time $drop\_next$, not from the dequeue time, so rounding to the dequeue times does not add up.

**Good queue and bad queue.** On the same link, bursts of 50 packets every 200 ms drain in 50 ms. Over 20 bursts, the largest sojourn time is 49 ms and CoDel drops nothing: no packet waits above TARGET for a full INTERVAL. Bursts of 150 packets every 300 ms keep the sojourn time above 5 ms for about 145 ms, and CoDel drops one packet in each of the 20 bursts.

**Traffic that does not respond.** Poisson arrivals at 1.2 packets per ms (seed 5) for 60 s give 72,053 packets at a link of 1 packet per ms. CoDel dropped 11,828 of them, 16.4 percent, close to the excess $1 - 1/1.2 \approx 16.7$ percent. It entered the dropping state 22 times, and some entries started with a count above 1 by line L16. In the second half of the run the mean sojourn time was 99 ms and the largest was 255 ms. A FIFO without drops would grow by about 0.2 ms per ms, to seconds of delay. CoDel bounds the queue here, but it does not hold the delay near 5 ms, because the senders do not slow down when they lose packets.

## Correctness

CoDel is a heuristic. The properties below hold for all inputs, and the proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **No drop without a standing queue.** If CoDel drops a packet at time $now$, then every packet that left the queue in the time interval $[now - \text{INTERVAL}, now]$ had sojourn time at least TARGET and left more than MAXPACKET bytes behind it. So a burst whose sojourn times stay above TARGET for less than INTERVAL is never cut.
2. **The control law.** In a dropping state that starts at time $e$ with count $c_0$, the $j$-th planned drop after the entry is at

$$D_j = e + \text{INTERVAL} \sum_{i=0}^{j-1} \frac{1}{\sqrt{c_0 + i}},$$

and the drop happens at the first dequeue at or after $D_j$. For $c_0 = 1$, $2(\sqrt{j+1} - 1) \le (D_j - e)/\text{INTERVAL} \le 2\sqrt{j}$. So about $(\tau / 2\,\text{INTERVAL})^2$ packets are dropped in the first $\tau$ ms of a long dropping state, and the drop rate grows linearly in time.
3. **Every packet is sent or dropped once.** Each call of DODEQUEUE pops one packet, and each popped packet is either returned or dropped.

RFC 8289 explains the square root as follows: for a [Reno](/tcp-reno/)-like sender the throughput is about inverse to the square root of the drop rate, so a drop rate that grows with the square root of the count gives a sending rate that falls about linearly with the number of drops.

## Complexity

Each packet is popped once by line L2 and either sent or dropped, so $n$ arrivals cost $\Theta(n)$ time in total. One DEQUEUE call may drop many packets in the loop of lines L10 to L12, so a single call is not $O(1)$ in the worst case, but the cost is $O(1)$ amortized per packet. The square root of line L12 is one operation, or a Newton step on an inverse square root, as the RFC suggests for kernels. The state is five numbers, plus the arrival stamp of each queued packet, so the extra space is $\Theta(1)$ per queue apart from the stamps.

## Properties

- **No parameters to tune for the link.** TARGET and INTERVAL are times. A queue of 5 ms is 5 ms of delay on any link, while a queue length in packets is not.
- **Works at dequeue.** CoDel decides when a packet leaves, so it uses the real waiting time, and it works with a link whose rate changes, such as Wi-Fi.
- **Keeps good queue.** By property 1, a burst that drains within INTERVAL loses no packet.
- **A heuristic.** There is no theorem that the sojourn time converges to TARGET. With responsive TCP flows it stays near TARGET in the simulations and measurements of Nichols and Jacobson; with traffic that does not respond, as in the example, it does not.
- **No flow isolation.** One FIFO with CoDel drops from all flows alike. FQ-CoDel puts CoDel on each flow queue of a [deficit round robin](/deficit-round-robin/) scheduler.

## Variants and improvements

- **FQ-CoDel (RFC 8290).** Hash the flows into many queues, serve them by [deficit round robin](/deficit-round-robin/) with priority for new flows, and run CoDel on each queue. Low-rate flows then see almost no queue at all.
- **ECN marks.** In the dropping state, CoDel can mark an [ECN](/ecn/)-capable packet in place of a drop, as RFC 8289 allows.
- **Other targets.** In a data center, where round-trip times are tens of microseconds, TARGET and INTERVAL are scaled down together. RFC 8289 suggests keeping TARGET at 5 to 10 percent of INTERVAL.
- **Other delay controllers.** [PIE](/pie-aqm/) also controls the delay, but it drops at enqueue with a probability that a proportional-integral controller sets.

## When to use it

Use CoDel on a queue that feeds a bottleneck link with TCP-like traffic, when you want a low delay without tuning: home gateways, Wi-Fi drivers and the egress of servers. Prefer FQ-CoDel when flows of different kinds share the link, because it also isolates them. Do not expect CoDel to control traffic that does not respond to drops; police such traffic with a [token bucket](/token-bucket/) or isolate it with [fair queueing](/fair-queueing/).

## Pitfalls

- **Measuring the queue length.** CoDel needs the sojourn time of each packet, so the queue must stamp packets at enqueue. A queue length divided by a nominal rate is wrong on links whose rate changes.
- **Setting drop_next from the dequeue time.** Line L12 adds to the planned time $drop\_next$, not to $now$. Using $now$ makes the drops slower than the control law.
- **Dropping the last packet.** Without the MAXPACKET test of line L3, CoDel can drop when the queue holds only one packet, and the link can go idle.
- **A wrong INTERVAL.** INTERVAL should be on the order of the worst round-trip time of the flows. If it is much shorter, CoDel drops before the senders could react to the last drop.
- **Using CoDel as a buffer limit.** CoDel does not bound the buffer. The queue still needs a hard limit for the case of traffic that does not respond.

## Implementations

## History

Kathleen Nichols and Van Jacobson published CoDel in ACM Queue in May 2012, with a version in Communications of the ACM in July 2012, as a response to the bufferbloat problem that Gettys and Nichols had described in 2011. Their key choices were the sojourn time as the measure and the minimum over an interval as the test of a standing queue. CoDel went into Linux in 2012, together with fq_codel. RFC 8289 (Nichols, Jacobson, McGregor and Iyengar, January 2018) gives the algorithm as an experimental RFC, and RFC 8290 gives FQ-CoDel.

## References
