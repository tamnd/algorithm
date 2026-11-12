---
tag: RVRJVD
kind: algorithm
slug: fast-retransmit-fast-recovery
name: Fast retransmit and fast recovery
aliases:
- fast retransmit
- fast recovery
- NewReno fast recovery
area: systems/networking-algorithms
level: intro
summary: Resend a segment after three duplicate ACKs, without waiting for the timer, and halve the window instead of restarting slow start. NewReno also repairs several losses in one window.
solves: [congestion-control]
model: asynchronous-model
complexity:
  vars: {k: the number of lost segments in one window, R: the round-trip time}
  time: {worst: Θ(k R)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Van Jacobson]
  note: Fast retransmit came with the 4.3BSD Tahoe TCP in 1988. Fast recovery came with 4.3BSD Reno in 1990.
prereqs: [slow-start, aimd]
see_also: [tcp-reno, tcp-tahoe, selective-repeat, go-back-n, round-trip-time-estimation, karn-algorithm, jacobson-rto-estimation]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Section 2 (the definition of a duplicate ACK) and Section 3.2 (fast retransmit and fast recovery, steps 1 to 6)
  - url: "https://www.rfc-editor.org/rfc/rfc6582"
    title: Tom Henderson, Sally Floyd, Andrei Gurtov and Yoshifumi Nishida, RFC 6582, The NewReno Modification to TCP's Fast Recovery Algorithm, 2012
    locator: Section 3 (the recover variable, full and partial acknowledgments)
  - paper: doi:10.1145/235160.235162
    title: Kevin Fall and Sally Floyd, Simulation-based comparisons of Tahoe, Reno and SACK TCP, ACM SIGCOMM Computer Communication Review 26(3), 1996
    locator: pages 5 to 21 (the behavior of Tahoe, Reno, NewReno and SACK with one to four losses in a window)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.5.4 (fast retransmit) and Section 3.7.1 (fast recovery)
---

Fast retransmit and fast recovery are the two loss-repair steps of TCP [congestion control](/congestion-control/). *Fast retransmit* resends a segment as soon as three duplicate ACKs show that it is lost, without waiting for the retransmission timer. *Fast recovery* then cuts the window to one half and keeps the data flowing, instead of going back to a window of one segment and [slow start](/slow-start/). RFC 5681, Section 3.2, gives the standard steps, and the NewReno change of RFC 6582 repairs several losses of one window in one recovery.

## In plain words

The receiver confirms data in order: "I have everything up to here". If one packet is lost, every later packet makes the receiver repeat the same confirmation. When the sender sees the same confirmation four times (the first one and three repeats), it knows that one packet is missing and that the later packets did arrive. So it sends the missing packet again at once.

The repeats also show that the network still delivers packets, so there is no reason to stop. The sender halves its sending window, because a loss means that the network is full. Then it sends one new packet for each repeat that comes back, since each repeat means that one packet left the network. When the missing packet is confirmed, the sender continues with the halved window.

## The problem

A TCP sender uses a [sliding window](/sliding-window-protocol/) with cumulative ACKs. A lost segment is found by the retransmission timer at the latest. The timer is set to well above the round-trip time, so a timeout wastes much more than one round trip, and after a timeout the window restarts at one segment. The problem is to find a single loss faster, to repair it, and to reduce the window by the [AIMD](/aimd/) factor of one half, without emptying the pipe. The model here is a sender with windows in segments, a receiver that sends one cumulative ACK per arriving segment, a network that keeps the order, and losses that the caller chooses.

## The algorithm

The sender keeps snd_una (the oldest unacknowledged segment), snd_nxt (the next new segment), cwnd, ssthresh, a counter dupacks and a flag in_recovery. NewReno also keeps recover, the highest segment sent when fast recovery started. An ACK $a$ names the next segment that the receiver expects.

```pseudo id=main
ON-ACK(a)                                           ▷ windows count segments
L1  if a = snd_una and snd_nxt > snd_una then         ▷ a duplicate ACK
L2      if in_recovery then cwnd ← cwnd + 1           ▷ one segment has left the network
L3      else
L4          dupacks ← dupacks + 1
L5          if dupacks = 3 and (not NewReno or a > recover) then
L6              ssthresh ← max(⌊(snd_nxt − snd_una) / 2⌋, 2)
L7              recover ← snd_nxt − 1
L8              resend segment snd_una                ▷ fast retransmit
L9              cwnd ← ssthresh + 3, in_recovery ← true    ▷ fast recovery
L10 else if a > snd_una then                          ▷ new data is acknowledged
L11     acked ← a − snd_una, snd_una ← a, dupacks ← 0
L12     if in_recovery and NewReno and a ≤ recover then    ▷ a partial ACK
L13         resend segment snd_una
L14         cwnd ← max(cwnd − acked + 1, 1)
L15     else if in_recovery then
L16         cwnd ← ssthresh, in_recovery ← false      ▷ deflate and leave
L17     else grow cwnd by slow start or congestion avoidance
L18 send new segments while snd_nxt − snd_una < cwnd
```

Line L6 is equation 4 of RFC 5681, with FlightSize $= \text{snd\_nxt} - \text{snd\_una}$. Line L9 adds 3 because the three duplicate ACKs mean that three segments have left the network. Line L2 inflates the window by one for each further duplicate ACK, so line L18 can send one new segment for each segment that leaves. Line L16 deflates the window to ssthresh when the retransmission is acknowledged. A timeout still works as in [slow start](/slow-start/): ssthresh from the flight, cwnd to 1, and resend from snd_una.

NewReno changes lines L5 and L12 to L14. A *partial ACK* acknowledges the retransmitted segment but not all the data up to recover, so another segment of the same window is lost. NewReno resends it at once and stays in fast recovery. Line L14 deflates the window by the acknowledged data and adds back one segment. The test $a > \text{recover}$ in line L5 stops a second halving for losses of the same window.

## Example

The time unit below is the round trip $R$. The sender has 40 segments, starts with $\text{cwnd} = \text{ssthresh} = 8$, and the first transmission of segment 20 is lost. When the ACK for segment 19 arrives, the window is $W = 10$ and segments 20 to 29 are in flight.

| event | cwnd | ssthresh | sent |
|---|---|---|---|
| new ACK 20 | 10 | 8 | 29 |
| duplicate ACKs 1 and 2 | 10 | 8 | nothing |
| duplicate ACK 3 | 8 | 5 | resend 20 |
| duplicate ACKs 4 and 5 | 9, 10 | 5 | nothing |
| duplicate ACKs 6 to 9 | 11 to 14 | 5 | 30, 31, 32, 33 |
| new ACK 30 | 5 | 5 | 34 |

The 9 duplicate ACKs come from segments 21 to 29. The flight is 10 until the window passes 10, and then the sender sends one new segment per duplicate ACK. When segment 20 arrives, the receiver has 20 to 29 and acknowledges 30. The sender deflates to 5 and has 30 to 34 in flight: exactly one half of the old window. The transfer ends after $6R$, against $5R$ with no loss.

Several losses in the same window, with the same start:

| lost segments | Reno | NewReno |
|---|---|---|
| 20 | one fast recovery, done at $6R$ | the same |
| 20 and 22 | two fast recoveries, ssthresh halved twice, done at $8R$ | one recovery with one partial ACK, done at $7R$ |
| 20, 22 and 24 | a timeout, done at $12R$ | one recovery with two partial ACKs, done at $7R$ |

With two losses, Reno leaves fast recovery on the partial ACK for 22. It needs three new duplicate ACKs to start again, and it halves a window that is already halved. With three losses, too few segments are in flight after the second halving to make three duplicate ACKs, and Reno waits for the timer.

## Correctness

The receiver hands the data over in order, and with finitely many losses the sender ends: in each bounded time after the last loss, either a new ACK comes or the timer resends snd_una. For one loss in a window of $W \ge 4$ segments, the $W - 1$ later segments make $W - 1$ duplicate ACKs. Then lines L6 to L9 and L2 let the sender send $\lfloor W/2 \rfloor - 1$ new segments during recovery, the retransmission is acknowledged after one round trip, and line L16 leaves exactly $\lfloor W/2 \rfloor$ segments in flight. For $k$ losses in one window, NewReno resends one hole per round trip at the partial ACKs and needs no timeout. The proof gives the conditions, including a retransmission timeout above two round trips.

## Complexity

Each ACK costs $\Theta(1)$ time, and the state is a few integers. The repair of one loss takes one round trip after the third duplicate ACK, against a retransmission timeout of at least one second in RFC 6298. NewReno repairs $k$ losses of one window in $k$ round trips, because it finds the next hole only at the next partial ACK. With selective acknowledgments (SACK, RFC 2018) the sender knows all holes and can repair them in about one round trip.

## Properties

- **Needs three duplicate ACKs.** Fast retransmit works only when at least three segments after the lost one arrive. A window of fewer than 4 segments, or a loss at the end of a transfer, still needs the timer.
- **Packet conservation.** During fast recovery, one new segment enters the network for each segment that leaves, so the ACK clock keeps running.
- **Multiplicative decrease.** Lines L6 and L16 halve the window, the decrease of [AIMD](/aimd/).
- **Robust to reordering of up to two places.** A segment that arrives one or two places late makes at most two duplicate ACKs, which do not trigger line L5.

## Variants and improvements

- **Limited transmit (RFC 3042).** On the first and second duplicate ACK, send one new segment each, so that a small window still makes three duplicate ACKs.
- **SACK-based recovery (RFC 6675).** The receiver reports the blocks that it has, and the sender resends all holes and counts the data in flight exactly.
- **Proportional rate reduction (RFC 6937).** Spreads the reduction of the window over the recovery, instead of the pause and the burst of lines L9 and L16.
- **RACK-TLP (RFC 8985).** Finds losses from the send times instead of from a count of duplicate ACKs, which works better with reordering.
- **[TCP Tahoe](/tcp-tahoe/)** has fast retransmit but no fast recovery: after line L8 it sets cwnd to 1 and goes back to slow start. **[TCP Reno](/tcp-reno/)** has both.

## When to use it

Every TCP sender that follows RFC 5681 uses fast retransmit and fast recovery, and NewReno is the base when SACK is not available. Use SACK-based recovery when both ends support it. The three-duplicate rule is a poor fit for paths that reorder packets a lot, such as some multipath links. There, use a time-based detection such as RACK.

## Pitfalls

- **Counting the wrong duplicates in line L1.** RFC 5681 counts an ACK as a duplicate only when it carries no data, does not change the receiver window, and repeats the highest ACK while data is outstanding. A window update or a data segment with the same ACK number is not a duplicate.
- **Forgetting to deflate in line L16.** If cwnd stays at ssthresh plus the inflation, the sender sends a burst of about one half a window on the first new ACK.
- **Leaving fast recovery on a partial ACK.** Plain Reno does this at line L15, and with several losses in one window it halves the window more than once or falls back to a timeout. Use the NewReno test with recover in lines L5 and L12.
- **Using cwnd instead of the flight in line L6.** A sender limited by the application can have a cwnd far above the data in flight. RFC 5681 uses FlightSize.

## Implementations

## History

Jacobson's 1988 TCP for 4.3BSD Tahoe resent a segment after three duplicate ACKs but then restarted slow start. Fast recovery came with 4.3BSD Reno in 1990. Stevens wrote both steps into RFC 2001 in 1997, and RFC 2581 and RFC 5681 kept them. Janey Hoe proposed the use of partial ACKs, and the NewReno change was published in RFC 2582 in 1999, RFC 3782 in 2004 and RFC 6582 in 2012. Fall and Floyd compared Tahoe, Reno, NewReno and SACK in simulation in 1996.

## References
