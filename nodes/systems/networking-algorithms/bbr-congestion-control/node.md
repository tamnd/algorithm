---
tag: BBWT9S
kind: algorithm
slug: bbr-congestion-control
name: BBR congestion control
aliases:
- BBR
- Bottleneck Bandwidth and Round-trip propagation time
area: systems/networking-algorithms
level: advanced
summary: A model-based congestion control from Google. It estimates the bottleneck bandwidth with a max filter and the propagation delay with a min filter, and paces at the estimated bandwidth.
solves: [congestion-control]
model: synchronous-model
complexity:
  vars: {r: the number of round trips}
  time: {worst: Θ(r)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2016
  people: [Neal Cardwell, Yuchung Cheng, C. Stephen Gunn, Soheil Hassas Yeganeh, Van Jacobson]
  note: Cardwell, Cheng, Gunn, Hassas Yeganeh and Jacobson described BBR in ACM Queue in 2016 and in Communications of the ACM in 2017.
prereqs: [congestion-control, round-trip-time-estimation]
see_also: [tcp-cubic, tcp-reno, tcp-vegas, slow-start, active-queue-management, codel, ecn, token-bucket]
sources:
  - paper: doi:10.1145/3012426.3022184
    title: Neal Cardwell, Yuchung Cheng, C. Stephen Gunn, Soheil Hassas Yeganeh and Van Jacobson, BBR, congestion-based congestion control, ACM Queue 14(5), 2016
    locator: pages 20 to 53 (the BtlBw and RTprop estimates, the operating point of Kleinrock, the state machine, the gains and the PROBE_RTT state)
  - paper: doi:10.1145/3009824
    title: Neal Cardwell, Yuchung Cheng, C. Stephen Gunn, Soheil Hassas Yeganeh and Van Jacobson, BBR, congestion-based congestion control, Communications of the ACM 60(2), 2017
    locator: pages 58 to 66 (the same design, the pacing gain cycle and the results from Google)
  - paper: doi:10.1145/3355369.3355604
    title: Ranysha Ware, Matthew K. Mukerjee, Srinivasan Seshan and Justine Sherry, Modeling BBR's interactions with loss-based congestion control, ACM Internet Measurement Conference 2019
    locator: pages 137 to 143 (the in-flight cap sets the share of BBR against Reno and CUBIC)
  - url: "https://datatracker.ietf.org/doc/draft-ietf-ccwg-bbr/"
    title: Neal Cardwell, Ian Swett and Joseph Beshay, BBR Congestion Control, IETF Internet-Draft draft-ietf-ccwg-bbr
    locator: the later version of the algorithm, with loss and ECN signals
---

BBR is a model-based [congestion control](/congestion-control/) from Google. Loss-based controls such as [Reno](/tcp-reno/) and [CUBIC](/tcp-cubic/) treat a loss as the sign of congestion, so they keep the bottleneck buffer full. BBR instead builds a model of the path from two numbers: the bottleneck bandwidth BtlBw, the maximum delivery rate of the last 10 round trips, and the round-trip propagation time RTprop, the minimum round-trip time of the last 10 seconds. It paces packets at about BtlBw and keeps about $\text{BtlBw} \cdot \text{RTprop}$ data in flight, so the link stays busy and the queue stays short. BBR is a heuristic: it has no general proof of convergence or fairness, and the code on this page is a model of BBR version 1, not the Linux code.

## In plain words

Every path has a narrowest link, and that link sets the highest speed. The path also has a shortest round-trip time, which a packet gets when no queue is in its way. If a sender knows these two numbers, it knows how much data it can keep in flight: the speed times the time. Less leaves the link idle. More only makes a queue.

BBR measures both numbers as it sends. The fastest delivery it saw recently is its speed estimate, and the shortest round trip it saw recently is its time estimate. It sends at that speed. From time to time it sends a little faster to see whether the path got faster, and then a little slower to empty the queue it made. If it has not seen a short round trip for a while, it almost stops for a moment to measure the empty path again.

## The problem

A sender must use the bottleneck fully without building a long queue. The best point is where the data in flight equals the bandwidth-delay product: there the delivery rate is already at its maximum, and the round-trip time is still at its minimum. Cardwell et al. call this the operating point of Kleinrock. The difficulty is that one measurement cannot show both numbers: the bandwidth shows only when the pipe is full, and the propagation time shows only when the queue is empty. The model on this page has one flow on one link of capacity $c$ packets per second and propagation time $d$, in rounds of one round-trip time, with an unlimited buffer unless stated.

## The algorithm

The state is BtlBw with the last 10 rate samples, RTprop with the time of its last update, the state of the machine (STARTUP, DRAIN, PROBE_BW or PROBE_RTT) and the phase of the gain cycle.

```pseudo id=main
ON-ROUND(rate, rtt, now, inflight)
L1  BtlBw ← max of the rate samples of the last 10 rounds
L2  if rtt ≤ RTprop or RTprop is older than 10 s then RTprop ← rtt, stamp ← now
L3  if STARTUP and BtlBw grew by less than 25% in 3 rounds then state ← DRAIN
L4  if DRAIN and inflight ≤ BtlBw · RTprop then state ← PROBE_BW
L5  else if PROBE_BW then phase ← (phase + 1) mod 8
L6  if RTprop expired then state ← PROBE_RTT for 200 ms, then back
L7  choose the gains: STARTUP 2/ln 2, DRAIN ln 2/2 (pacing), PROBE_BW gains[phase], PROBE_RTT 1
L8  pacing_rate ← pacing_gain · BtlBw
L9  cwnd ← max(cwnd_gain · BtlBw · RTprop, 4)    ▷ 4 packets in PROBE_RTT
```

Lines L1 and L2 are the two filters. The max filter for the bandwidth and the min filter for the delay both ignore the noise that queues and ACK compression add in only one direction. Line L3 ends STARTUP when three rounds in a row do not raise BtlBw by 25%, so the pipe is full. STARTUP uses the gain $2/\ln 2 \approx 2.885$, which Cardwell et al. give as the smallest gain that doubles the sending rate in each round, like [slow start](/slow-start/). Line L4 runs DRAIN with the inverse gain until the queue made by STARTUP is gone. In PROBE_BW the pacing gain cycles through $1.25, 0.75, 1, 1, 1, 1, 1, 1$ and the window gain is 2: the round at 1.25 tests for more bandwidth, the round at 0.75 removes the queue that the test made, and the six rounds at 1 cruise. Line L6 enters PROBE_RTT when RTprop has not been refreshed for 10 s. For 200 ms the window is 4 packets, so the queue empties and the flow can measure the propagation time again.

## Example

A link of $c = 1000$ packets per second with $d = 40$ ms has a bandwidth-delay product of 40 packets. The flow starts with BtlBw at 250 packets per second.

| round | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|
| state | STARTUP | STARTUP | STARTUP | STARTUP | STARTUP | DRAIN | PROBE_BW | PROBE_BW | PROBE_BW |
| delivered (packets/s) | 721.3 | 1000 | 1000 | 864.2 | 1000 | 1000 | 1000 | 1000 | 950 |
| queue at the end (packets) | 0 | 43.3 | 110.2 | 0 | 75.4 | 0 | 0 | 10 | 0 |
| round-trip time (ms) | 40 | 40 | 83.3 | 150.2 | 40 | 115.4 | 40 | 40 | 50 |

In round 0 the flow paces at $2.885 \cdot 250 = 721.3$ packets per second, and in round 1 it already reaches the capacity. Rounds 2, 3 and 4 do not raise BtlBw by 25%, so DRAIN starts in round 5 and empties the queue. From round 6 the flow is in PROBE_BW. In each cycle of 8 rounds one round at gain 1.25 leaves a queue of 10 packets, a quarter of the bandwidth-delay product, and the next round at 0.75 delivers 950 packets per second and empties it. The other rounds run at 1000 packets per second with no queue.

**A route change.** After 100 rounds the propagation time grows to 60 ms. Every round-trip sample is now above RTprop, so line L2 does not refresh it, and about 10.08 s later RTprop expires. The flow enters PROBE_RTT, sends 4 packets per round (66.7 packets per second for 0.24 s), takes 60 ms as the new RTprop and returns to PROBE_BW. Here the old RTprop did not slow the flow, because the window of $2 \cdot 40 = 80$ packets is above the new bandwidth-delay product of 60.

**A small buffer.** With a buffer of 20 packets the STARTUP rounds lose packets, but BBR v1 does not react to loss, and the filters still find 1000 packets per second and 40 ms.

## Correctness

BBR does not compute a defined output, so the proof shows what each part does in the round model. The rate samples are never above $c$ and the round-trip samples never below $d$, so BtlBw can only be too low, and RTprop can only be too low after the path got longer. With exact estimates, the PROBE_BW cycle has a queue of at most $cd/4$, empties it in the round at gain 0.75, and delivers $8.1875/8.25 > 99\%$ of the capacity, while both filters keep their values. After a route change to a longer path, PROBE_RTT starts within 10 s and one round, and the new RTprop is the new propagation time. The proof does not cover convergence from every start or fairness between flows.

## Complexity

Each round, or each ACK in a real stack, costs $\Theta(1)$ time, because the max filter keeps at most 10 samples. STARTUP needs about $\log_2$ of the ratio between the bandwidth-delay product and the initial window in round trips, like slow start. The steady cycle costs one round with a queue of $cd/4$ every 8 rounds, and PROBE_RTT costs 200 ms at low rate every 10 s when no short round-trip sample comes. When the flow sees an empty queue often, as in the example, PROBE_RTT is not needed.

## Properties

- **Model-based.** BBR reacts to the measured rate and delay, not to loss. A random loss on a radio link does not lower its rate.
- **Short queue.** At the steady point the queue is close to zero, with a short peak in each probe round.
- **Pacing.** The sender spaces packets at the pacing rate, so it sends no bursts.
- **Window as a cap.** The window of 2 bandwidth-delay products only limits the data in flight. The pacing rate sets the speed.
- **Not fair to loss-based flows.** Ware et al. showed that against Reno and CUBIC, the share of BBR is set by its in-flight cap, not by the number of flows, so one BBR flow can take much more than a fair share from many loss-based flows. With a shallow buffer, BBR v1 can also cause many losses, since it does not react to them.

## Variants and improvements

- **BBR version 2 and later.** The later versions, described in the IETF draft, also use loss and [ECN](/ecn/) marks as signals, set a limit on the data in flight after losses, and change the probing to be fairer to loss-based flows.
- **Delay-based control.** [TCP Vegas](/tcp-vegas/) also uses the minimum round-trip time, but it moves the window by one packet per round trip and does not estimate the bandwidth.
- **Active queue management.** [CoDel](/codel/) uses the minimum queueing delay over a window, the same kind of min filter, to decide when to drop at the router.

## When to use it

BBR fits paths where losses do not mean congestion, such as radio links, and paths with deep buffers where loss-based controls give long delays. It is less suitable when it shares a bottleneck with many loss-based flows and fairness to them matters, and when the path has a very shallow buffer and BBR v1 is used. Test the version that the stack offers, because the versions differ a lot.

## Pitfalls

- **Taking the model as the algorithm.** The code here has a simple round model and no losses. Real BBR runs on every ACK, uses delivery-rate samples per packet, handles application-limited periods and has many more rules.
- **Counting application-limited samples.** When the application sends less than the path allows, the delivery rate is low. A real BBR must not let these samples lower BtlBw. The max filter of line L1 helps, but the samples must also be marked.
- **A stale RTprop after a route change.** If the path gets longer and the queue never empties, RTprop is too low until line L6 expires it, and the window of line L9 can then be too small.
- **Ignoring loss in a shallow buffer.** BBR v1 keeps sending at BtlBw when the buffer overflows. Use a version that reacts to loss when the buffers are shallow.
- **Expecting fairness to CUBIC.** See Properties. A mix of BBR and loss-based flows can give very unequal shares.

## Implementations

## History

Cardwell, Cheng, Gunn, Hassas Yeganeh and Jacobson described BBR in ACM Queue in 2016 and in Communications of the ACM in 2017. They based it on the operating point that Kleinrock described in 1979, where the data in flight equals the bandwidth-delay product, and they reported its use for Google traffic. Ware, Mukerjee, Seshan and Sherry modeled its competition with loss-based flows at IMC 2019. Later versions of BBR are described in an IETF Internet-Draft.

## References
