---
tag: WM4RDM
kind: algorithm
slug: tcp-reno
name: TCP Reno
aliases:
- Reno TCP
area: systems/networking-algorithms
level: intro
summary: The TCP congestion control of 4.3BSD Reno (1990). It adds fast recovery to Tahoe, so one loss found by three duplicate ACKs halves the window instead of restarting slow start.
solves: [congestion-control]
model: asynchronous-model
complexity:
  vars: {w: the window in segments just before a loss, R: the round-trip time}
  time: {worst: Θ(w R)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1990
  people: [Van Jacobson]
  note: Fast recovery came with the 4.3BSD Reno release of 1990. The four algorithms were written down as a standard in RFC 2001 (1997), RFC 2581 and RFC 5681.
prereqs: [tcp-tahoe, fast-retransmit-fast-recovery]
see_also: [congestion-control, tcp-cubic, tcp-vegas, bbr-congestion-control, ecn, round-trip-time-estimation, jacobson-rto-estimation, red-random-early-detection]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc5681"
    title: Mark Allman, Vern Paxson and Ethan Blanton, RFC 5681, TCP Congestion Control, 2009
    locator: Section 3.1 (slow start and congestion avoidance) and Section 3.2 (fast retransmit and fast recovery)
  - paper: doi:10.1145/235160.235162
    title: Kevin Fall and Sally Floyd, Simulation-based comparisons of Tahoe, Reno and SACK TCP, ACM SIGCOMM Computer Communication Review 26(3), 1996
    locator: pages 5 to 21 (Reno with one, two, three and four losses in one window)
  - paper: doi:10.1145/263932.264023
    title: Matthew Mathis, Jeffrey Semke, Jamshid Mahdavi and Teunis Ott, The macroscopic behavior of the TCP congestion avoidance algorithm, ACM SIGCOMM Computer Communication Review 27(3), 1997
    locator: pages 67 to 82 (the periodic sawtooth model and the constant sqrt(3/2))
  - paper: doi:10.1145/285237.285291
    title: Jitendra Padhye, Victor Firoiu, Don Towsley and Jim Kurose, Modeling TCP throughput, a simple model and its empirical validation, ACM SIGCOMM 1998
    locator: pages 303 to 314 (the throughput model with triple-duplicate losses and timeouts)
  - url: "https://www.rfc-editor.org/rfc/rfc6582"
    title: Tom Henderson, Sally Floyd, Andrei Gurtov and Yoshifumi Nishida, RFC 6582, The NewReno Modification to TCP's Fast Recovery Algorithm, 2012
    locator: Section 3 (partial acknowledgments)
  - url: "https://www.rfc-editor.org/rfc/rfc9002"
    title: Jana Iyengar and Ian Swett, RFC 9002, QUIC Loss Detection and Congestion Control, 2021
    locator: Section 7 (a congestion controller similar to TCP NewReno)
---

TCP Reno is the TCP [congestion control](/congestion-control/) of the 4.3BSD Reno release of 1990. It is [TCP Tahoe](/tcp-tahoe/) with one change: after a fast retransmit it uses [fast recovery](/fast-retransmit-fast-recovery/), so the window drops to one half and the data keeps flowing. Only a retransmission timeout still sets the window to one segment. In the long run Reno is [AIMD](/aimd/) with an increase of one segment per round trip and a decrease by one half, and its rate follows the square-root law of Mathis et al.: about $\sqrt{3/(2p)}$ segments per round trip at loss rate $p$.

## In plain words

Reno grows its sending window the same way as Tahoe: it doubles each round trip at the start, and later it adds one packet per round trip. The difference is what it does when a packet is lost.

If the receiver repeats the same confirmation three times, the later packets did arrive, so the network still works. Reno then sends the lost packet again, halves its window and continues at that speed. Only when nothing comes back and the timer runs out does it start again from one packet.

Over a long transfer the window goes up slowly and drops by one half at each loss. This makes a sawtooth pattern.

## The problem

A TCP sender with a [sliding window](/sliding-window-protocol/) must choose how many segments to keep in flight, and it must react to each loss so that the network does not reach congestion collapse. Tahoe reacts to every loss with a window of one segment, which leaves the path almost empty for several round trips. The problem is to keep the decrease by one half that the [AIMD](/aimd/) fairness argument needs, without that restart. The model on this page is one sender with windows in segments, one cumulative ACK per arriving segment, a fixed round-trip time $R$, a network that keeps the order, and losses that the caller chooses.

## The algorithm

The state is snd_una, snd_nxt, cwnd, ssthresh, a counter dupacks and a flag in_recovery. An ACK $a$ names the next segment that the receiver expects.

```pseudo id=main
ON-ACK(a)
L1  if a = snd_una and snd_nxt > snd_una then          ▷ a duplicate ACK
L2      if in_recovery then cwnd ← cwnd + 1             ▷ inflate
L3      else dupacks ← dupacks + 1
L4          if dupacks = 3 then
L5              ssthresh ← max(⌊(snd_nxt − snd_una) / 2⌋, 2)
L6              resend segment snd_una                  ▷ fast retransmit
L7              cwnd ← ssthresh + 3, in_recovery ← true ▷ fast recovery
L8  else if a > snd_una then                            ▷ new data is acknowledged
L9      snd_una ← a, dupacks ← 0
L10     if in_recovery then cwnd ← ssthresh, in_recovery ← false   ▷ deflate
L11     else if cwnd < ssthresh then cwnd ← cwnd + 1    ▷ slow start
L12     else add 1 to cwnd once per cwnd ACKs           ▷ congestion avoidance
L13 send new segments while snd_nxt − snd_una < cwnd

ON-TIMEOUT()
L14 ssthresh ← max(⌊(snd_nxt − snd_una) / 2⌋, 2)        ▷ kept on a repeated timeout
L15 cwnd ← 1
L16 snd_nxt ← snd_una                                   ▷ go back to the oldest unacknowledged segment
```

Lines L11 and L12 are [slow start](/slow-start/) and congestion avoidance, as in Tahoe. Lines L4 to L7 and L2 are fast retransmit and fast recovery from RFC 5681, Section 3.2. Line L10 is the main difference from Tahoe: any new ACK ends fast recovery and leaves the window at ssthresh, one half of the flight before the loss. Lines L14 to L16 are the Tahoe reaction, which Reno keeps for timeouts only. A second timeout of the same segment keeps ssthresh, as RFC 5681 asks.

## Example

The sender has 40 segments and starts with $\text{cwnd} = \text{ssthresh} = 8$. The first transmission of segment 20 is lost when the window is 10. The third duplicate ACK starts fast recovery with $\text{ssthresh} = 5$ and $\text{cwnd} = 8$. The ACK of the retransmission is 30, the window deflates to 5, and the transfer ends after $6R$, against $5R$ with no loss and $7R$ for Tahoe.

More losses in the same window show the weak point of line L10:

| lost segments | fast retransmits | timeouts | done at |
|---|---|---|---|
| 20 | 1 | 0 | $6R$ |
| 20 and 22 | 2 | 0 | $8R$ |
| 20, 22 and 24 | 1 | 1 | $12R$ |

With 20 and 22 lost, the ACK of the retransmission of 20 is 22. It is new data, so line L10 ends the recovery. The sender then needs three more duplicate ACKs for 22 and halves the window a second time. With three losses, the halved window is too small to make three duplicate ACKs for the second hole, and Reno waits for the timer. Tahoe ends the same case after $9R$.

**Long-run rate.** In the same model with an unlimited transfer and every $m$-th transmission lost, the rate from time $1000R$ to $2000R$ is:

| $m$ | Reno (segments per round trip) | $\sqrt{3m/2}$ | ratio |
|---|---|---|---|
| 50 | 7.00 | 8.66 | 0.81 |
| 100 | 10.42 | 12.25 | 0.85 |
| 200 | 15.92 | 17.32 | 0.92 |
| 400 | 22.60 | 24.49 | 0.92 |
| 800 | 33.31 | 34.64 | 0.96 |
| 1600 | 47.43 | 48.99 | 0.97 |

The ratio goes up to 1 as $p = 1/m$ goes down. At high loss rates the windows are small and losses fall more often outside the clean sawtooth, so the formula is too high.

## Correctness

The receiver hands the data over in order, and with finitely many losses the sender ends: after the last loss, either a new ACK comes or the timer resends snd_una. For one loss in a window of $W \ge 4$ segments, Reno repairs the loss with no timeout, and one round trip after the retransmission it has exactly $\lfloor W/2 \rfloor$ segments in flight. For the long-run rate, the proof uses the periodic sawtooth from $w/2$ to $w$: one loss per $\frac{3w}{4}(\frac{w}{2} + 1)$ segments gives a rate times $\sqrt{p}$ of $\sqrt{3/2} \sqrt{w/(w+2)}$, which goes to $\sqrt{3/2} \approx 1.2247$. For $w = 20$, $100$ and $1000$ the factor is $1.1677$, $1.2127$ and $1.2235$.

## Complexity

Each ACK and each timeout costs $\Theta(1)$ time, and the state is a few integers. A single loss costs about one round trip of repair. After the loss, the window needs $w/2$ round trips to grow from $w/2$ back to $w$, so one sawtooth cycle lasts $\Theta(wR)$. For a path with a large bandwidth-delay product this is long: at 10 Gbit/s, 100 ms and 1500-byte segments, $w$ is about 83000 segments, and one cycle lasts more than an hour. This is the reason for [CUBIC](/tcp-cubic/) and other controls for fast long paths.

## Properties

- **Loss-based.** Reno sees congestion only through losses, so it fills the buffer of the bottleneck before it slows down. Drop-tail buffers of one bandwidth-delay product keep the link busy through the halvings.
- **Fair between equal round-trip times.** Flows with the same round-trip time converge to equal shares by the AIMD argument.
- **Unfair to long round-trip times.** The rate is inversely proportional to the round-trip time, so a flow with twice the round-trip time gets about one half of the rate at the same loss rate.
- **The square-root law.** The rate is about $\frac{\text{MSS}}{R} \sqrt{3/(2p)}$, so a 4 times lower loss rate gives twice the rate.
- **TCP-friendly reference.** Other controls use this rate as a reference. For example, in its Reno-friendly region CUBIC grows at least as fast as Reno would.

## Variants and improvements

- **NewReno (RFC 6582).** A partial ACK keeps the sender in fast recovery and resends the next hole, which fixes the multi-loss cases of the example. See [fast retransmit and fast recovery](/fast-retransmit-fast-recovery/).
- **SACK-based recovery.** The receiver reports which blocks it has, and the sender repairs all holes of a window in about one round trip.
- **Explicit signals.** With [ECN](/ecn/), routers mark packets instead of dropping them, and the sender halves its window once per round trip without a loss.
- **Delay-based and model-based controls.** [TCP Vegas](/tcp-vegas/) and [BBR](/bbr-congestion-control/) react before the buffer is full.
- **Faster growth.** [CUBIC](/tcp-cubic/) replaces the linear increase with a cubic function of the time since the last loss and keeps a Reno-friendly region.

## When to use it

Reno with the NewReno change is the reference congestion control of the IETF, and QUIC (RFC 9002) describes a NewReno-like control. It is a good choice when simplicity and fairness to other Reno flows matter more than the rate. Do not use it alone on paths with a large bandwidth-delay product, on wireless paths with losses that do not come from congestion, or when a low queueing delay is important.

## Pitfalls

- **Ending fast recovery on a partial ACK.** Line L10 does this, and with several losses in a window it gives several halvings or a timeout. Use NewReno or SACK.
- **Confusing losses from bit errors with congestion.** On a lossy radio link the square-root law gives a low rate even on an empty path.
- **A small buffer at the bottleneck.** With a buffer much smaller than one bandwidth-delay product, each halving leaves the link idle for part of the cycle.
- **Taking the Mathis formula as exact.** It holds for the sawtooth without timeouts. At higher loss rates, timeouts dominate, and the model of Padhye et al. is closer.

## Implementations

## History

Jacobson's 1988 algorithms in 4.3BSD Tahoe had slow start, congestion avoidance and fast retransmit, and the 4.3BSD Reno release of 1990 added fast recovery. Stevens wrote the four algorithms into RFC 2001 in 1997, later replaced by RFC 2581 and RFC 5681. Fall and Floyd showed in 1996 that Reno does badly with several losses in one window, which led to NewReno and SACK. Mathis, Semke, Mahdavi and Ott gave the square-root law in 1997, and Padhye, Firoiu, Towsley and Kurose added timeouts in 1998.

## References
