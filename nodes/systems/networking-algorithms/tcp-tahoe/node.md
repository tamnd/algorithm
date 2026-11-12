---
tag: TX7EHD
kind: algorithm
slug: tcp-tahoe
name: TCP Tahoe
aliases:
- Tahoe TCP
- 4.3BSD Tahoe TCP
area: systems/networking-algorithms
level: intro
summary: The first TCP congestion control, from 4.3BSD Tahoe in 1988. It uses slow start, congestion avoidance and fast retransmit, and goes back to a window of one segment after every loss.
solves: [congestion-control]
model: asynchronous-model
complexity:
  vars: {w: the window in segments before the loss, R: the round-trip time}
  time: {worst: Θ(R log w)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Van Jacobson]
  note: The 4.3BSD Tahoe release of 1988 carried Jacobson's slow start, congestion avoidance and fast retransmit.
prereqs: [slow-start, aimd, fast-retransmit-fast-recovery]
see_also: [tcp-reno, congestion-control, go-back-n, round-trip-time-estimation, jacobson-rto-estimation, karn-algorithm]
sources:
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, ACM SIGCOMM 1988
    locator: pages 314 to 329 (conservation of packets, slow start, the round-trip timer and congestion avoidance)
  - paper: doi:10.1145/235160.235162
    title: Kevin Fall and Sally Floyd, Simulation-based comparisons of Tahoe, Reno and SACK TCP, ACM SIGCOMM Computer Communication Review 26(3), 1996
    locator: pages 5 to 21 (the description of Tahoe and its behavior with one to four losses in a window)
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Section 3.1 (slow start, congestion avoidance and the loss window) and Section 3.2 (fast retransmit)
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 6.3 (TCP congestion control)
---

TCP Tahoe is the TCP [congestion control](/congestion-control/) that came with the 4.3BSD Tahoe release in 1988. It joins three of Jacobson's algorithms: [slow start](/slow-start/), congestion avoidance with the [AIMD](/aimd/) increase of one segment per round trip, and fast retransmit after three duplicate ACKs. On every loss, found by the timer or by three duplicate ACKs, it sets the threshold to one half of the flight and starts again from a window of one segment. [TCP Reno](/tcp-reno/) later kept the window at one half after a fast retransmit.

## In plain words

Tahoe has one simple rule for bad news. While all goes well, the sender grows its window: fast at the start (it doubles each round trip) and then slowly (one more packet each round trip). When it finds a lost packet, either because a timer runs out or because the receiver repeats the same confirmation three times, the sender remembers one half of its window as a limit. Then it starts again with one packet, doubles up to that limit, and grows slowly from there.

This is safe: after a loss the sender almost stops, so the network can empty its queues. The price is speed. After each loss the sender must spend several round trips to grow its window back.

## The problem

A TCP sender with a [sliding window](/sliding-window-protocol/) must choose how many segments to keep in flight, without knowledge of the path, and must react to losses so that the network does not reach congestion collapse. In 1988 the problem was urgent: the Internet had collapses from October 1986, and TCP sent a full receiver window at once. The model on this page is one sender with windows in segments, one cumulative ACK per arriving segment, a fixed round-trip time $R$, a network that keeps the order, and losses that the caller chooses.

## The algorithm

The state is snd_una, snd_nxt, cwnd, ssthresh and a counter of duplicate ACKs. An ACK $a$ names the next segment that the receiver expects.

```pseudo id=main
ON-ACK(a)
L1  if a = snd_una and snd_nxt > snd_una then      ▷ a duplicate ACK
L2      dupacks ← dupacks + 1
L3      if dupacks = 3 then LOSS()                  ▷ fast retransmit
L4  else if a > snd_una then                        ▷ new data is acknowledged
L5      snd_una ← a, dupacks ← 0
L6      if cwnd < ssthresh then cwnd ← cwnd + 1     ▷ slow start
L7      else add 1 to cwnd once per cwnd ACKs       ▷ congestion avoidance
L8  send new segments while snd_nxt − snd_una < cwnd

LOSS()                                              ▷ also run on a timeout
L9  ssthresh ← max(⌊(snd_nxt − snd_una) / 2⌋, 2)
L10 cwnd ← 1
L11 snd_nxt ← snd_una                               ▷ resend from the oldest unacknowledged segment
```

Lines L6 and L7 are [slow start](/slow-start/) and congestion avoidance. Line L3 is fast retransmit, and the remaining lines show the main difference from Reno: a fast retransmit runs the same LOSS as a timeout. Line L9 halves the flight, which is the multiplicative decrease. Line L10 empties the pipe. Line L11 makes the sender go back to the oldest unacknowledged segment. Then line L8 resends it, and later segments go out again as the window grows, unless a cumulative ACK shows that the receiver already has them. Duplicate ACKs after the third do nothing. A second timeout of the same segment keeps ssthresh, as RFC 5681 asks.

## Example

The sender has 40 segments and starts with $\text{cwnd} = \text{ssthresh} = 8$. The table gives the highest ACK and the window at the end of each round trip.

| round trip | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| no loss: ACK | 8 | 17 | 27 | 38 | 40 | | |
| no loss: cwnd | 9 | 10 | 11 | 12 | 12 | | |
| segment 20 lost: ACK | 8 | 17 | 20 | 30 | 32 | 36 | 40 |
| segment 20 lost: cwnd | 9 | 10 | 1 | 2 | 4 | 5 | 6 |

In round trip 3, segment 20 is lost with a flight of 10 segments. Three duplicate ACKs come, so ssthresh becomes 5 and cwnd becomes 1. Only the retransmission of 20 is in flight for one round trip. Its ACK is 30, because segments 21 to 29 arrived, so nothing of the old window is sent again. Then the window grows 2, 4, 5 and enters congestion avoidance. The transfer ends after $7R$. [TCP Reno](/tcp-reno/) ends the same transfer after $6R$ and no loss after $5R$.

With more losses in the same window, Tahoe can do better than Reno. With segments 20 and 22 lost, Tahoe ends after $8R$, the same as Reno, with 43 transmissions. With 20, 22 and 24 lost, Tahoe ends after $9R$ with 46 transmissions and no timeout, while Reno waits for a timeout and ends after $12R$. The go-back of line L11 resends each hole on the way, so Tahoe never needs more duplicate ACKs.

**Long-run rate.** The same model with an unlimited transfer and every $m$-th transmission lost gives these rates in segments per round trip, measured from time $1000R$ to $2000R$, with the formula of Mathis et al. for Reno for comparison:

| $m$ | Tahoe | Reno | $\sqrt{3m/2}$ |
|---|---|---|---|
| 50 | 5.44 | 7.00 | 8.66 |
| 200 | 12.46 | 15.92 | 17.32 |
| 800 | 28.50 | 33.31 | 34.64 |
| 1600 | 42.12 | 47.43 | 48.99 |

## Correctness

The receiver hands the data over in order, also when line L11 makes the sender resend data that the receiver has. With finitely many losses the sender ends, because in each bounded time after the last loss either a new ACK comes or the timer resends snd_una. For one loss in a window of $W \ge 4$ segments, the fast retransmit comes at most one round trip after the last new ACK, the retransmission is acknowledged one round trip later with no timeout, and the window is back at $\lfloor W/2 \rfloor$ after $\lceil \log_2 \lfloor W/2 \rfloor \rceil$ round trips. The proof has the details.

## Complexity

Each ACK costs $\Theta(1)$ time, and the state is a few integers. The cost of a loss is in round trips. After one loss from a window of $w$ segments, Tahoe needs about $\log_2(w/2)$ round trips of slow start to return to the halved window, and it sends almost nothing in the first of them. [TCP Reno](/tcp-reno/) keeps one half of the window in flight during the repair. For large windows the slow start is short against the linear growth that follows, which is why the rates in the table get closer as $m$ grows.

## Properties

- **One reaction to every loss.** A timeout and three duplicate ACKs both lead to a window of one segment.
- **Self-clocked restart.** After a loss the sender rebuilds the ACK clock with slow start instead of a burst.
- **AIMD in the long run.** Between losses the window grows by about one segment per round trip, and ssthresh halves at each loss, so Tahoe has the fairness of [AIMD](/aimd/) between flows with the same round-trip time.
- **Robust to several losses.** Because it resends from snd_una, it does not need duplicate ACKs for the second and later holes of a window.

## Variants and improvements

- **[TCP Reno](/tcp-reno/)** adds fast recovery: after a fast retransmit the window becomes one half of the flight, not one segment.
- **NewReno and SACK** repair several holes of one window without a timeout and without the restart from one segment. See [fast retransmit and fast recovery](/fast-retransmit-fast-recovery/).
- **Round-trip timer.** Tahoe also brought Jacobson's estimate of the mean and the variation of the round-trip time for the retransmission timer. See [Jacobson's RTO estimation](/jacobson-rto-estimation/) and [Karn's algorithm](/karn-algorithm/).

## When to use it

Tahoe is of historical and teaching value. It shows the base of all loss-based TCP controls in its plainest form. Current systems use Reno, NewReno, [CUBIC](/tcp-cubic/) or [BBR](/bbr-congestion-control/). A Tahoe-like restart to one segment is still the standard reaction to a retransmission timeout in RFC 5681.

## Pitfalls

- **The same reaction to two different signals.** Duplicate ACKs show that the path still delivers, and a timeout does not. Line L3 runs the full LOSS on duplicate ACKs, so the pipe drains for no reason. This is the main loss of rate that Reno fixed.
- **Resending data that arrived.** The go-back of line L11 resends segments that the receiver may have. In the model a cumulative ACK skips them, but with several holes some segments are sent twice.
- **Halving the window instead of the flight in line L9.** The threshold must come from the data in flight.
- **Fast retransmit with a small window.** With fewer than 4 segments in flight, three duplicate ACKs cannot come, and the sender waits for the timer.

## Implementations

## History

Jacobson's paper Congestion avoidance and control (SIGCOMM 1988) described slow start, congestion avoidance and the new round-trip timer, and the code went into the 4.3BSD Tahoe release in 1988. Fall and Floyd describe Tahoe as the TCP with slow start, congestion avoidance and fast retransmit, and they compare it with Reno, NewReno and SACK. The name of the algorithm is the name of the BSD release.

## References
