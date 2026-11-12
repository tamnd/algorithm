---
tag: NC11TV
kind: algorithm
slug: tcp-cubic
name: TCP CUBIC
aliases:
- CUBIC
- CUBIC congestion control
area: systems/networking-algorithms
level: advanced
summary: A loss-based TCP congestion control that grows the window as a cubic function of the time since the last loss, with a plateau at the last loss window and a Reno-friendly lower bound.
solves: [congestion-control]
model: asynchronous-model
complexity:
  vars: {a: the number of ACKs}
  time: {worst: Θ(a)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2008
  people: [Sangtae Ha, Injong Rhee, Lisong Xu]
  note: Ha, Rhee and Xu published CUBIC in 2008 as a simpler successor of BIC TCP. The IETF published it as RFC 8312 in 2018 and as the Standards Track RFC 9438 in 2023.
prereqs: [tcp-reno, aimd]
see_also: [congestion-control, bbr-congestion-control, tcp-vegas, slow-start, fast-retransmit-fast-recovery, ecn, codel, red-random-early-detection]
sources:
  - url: "https://www.rfc-editor.org/rfc/rfc9438"
    title: Lisong Xu, Sangtae Ha, Injong Rhee, Vidhi Goel and Lars Eggert, RFC 9438, CUBIC for Fast and Long-Distance Networks, 2023
    locator: Section 1 (deployment), Section 4.2 (the window increase function), Section 4.3 (the Reno-friendly region), Sections 4.4 and 4.5 (the concave and convex regions), Section 4.6 (multiplicative decrease) and Section 4.7 (fast convergence)
  - paper: doi:10.1145/1400097.1400105
    title: Sangtae Ha, Injong Rhee and Lisong Xu, CUBIC, a new TCP-friendly high-speed TCP variant, ACM SIGOPS Operating Systems Review 42(5), 2008
    locator: pages 64 to 74 (the cubic function, its relation to BIC TCP, and the response function)
  - url: "https://www.rfc-editor.org/rfc/rfc8312"
    title: Injong Rhee, Lisong Xu, Sangtae Ha, Alexander Zimmermann, Lars Eggert and Richard Scheffenegger, RFC 8312, CUBIC for Fast Long-Distance Networks, 2018
    locator: Section 4 (the CUBIC congestion control)
  - paper: doi:10.1145/263932.264023
    title: Matthew Mathis, Jeffrey Semke, Jamshid Mahdavi and Teunis Ott, The macroscopic behavior of the TCP congestion avoidance algorithm, ACM SIGCOMM Computer Communication Review 27(3), 1997
    locator: pages 67 to 82 (the periodic sawtooth model used for the Reno-friendly increase)
---

TCP CUBIC is a loss-based TCP [congestion control](/congestion-control/) for paths with a large bandwidth-delay product. After a loss it reduces the window to $\beta = 0.7$ times its value, and then the window follows the cubic function $W_{\text{cubic}}(t) = C(t - K)^3 + W_{\max}$ of the time $t$ since the loss, with $C = 0.4$. The curve rises fast, flattens at $W_{\max}$, the window at the last loss, and then rises fast again to probe for more bandwidth. Below the curve, CUBIC never grows more slowly than [TCP Reno](/tcp-reno/) would. RFC 9438 is the standard.

## In plain words

Reno adds one packet to its window per round trip. On a fast path that spans the world, the window can be tens of thousands of packets, and after one loss Reno needs hours to grow back.

CUBIC remembers the window it had at the last loss. After the loss it first grows quickly, because that window was safe until just now. As it gets close to the old value, it slows down and waits there for a while, because that is where the loss happened. If no loss comes, it speeds up again, slowly first and then quickly, to find out whether the path now has more room. The growth depends on the time since the loss, not on the number of round trips, so flows with short and long round trips grow at the same speed.

## The problem

A sender must find and share the bandwidth of the path, and keep its rate high on paths where the bandwidth-delay product is large. [AIMD](/aimd/) with an increase of one segment per round trip takes $\Theta(w)$ round trips to regain a window of $w$, and its rate falls as one over the round-trip time. The problem is to grow faster on such paths, to stay stable near the last window that caused a loss, and to stay fair to Reno where Reno does well. The model here is one sender in congestion avoidance with windows in segments, one ACK per segment, time in seconds, and losses that come from the network.

## The algorithm

The state is cwnd, $W_{\max}$, $\text{cwnd}_{\text{prior}}$, ssthresh, $t_{\text{epoch}}$, $K$ and $W_{\text{est}}$. Constants: $C = 0.4$, $\beta = 0.7$ and $\alpha_{\text{cubic}} = 3(1 - \beta)/(1 + \beta)$.

```pseudo id=main
ON-ACK(now, acked)                                    ▷ in congestion avoidance
L1  t ← now − t_epoch
L2  W_next ← C (t + RTT − K)³ + W_max                  ▷ the curve one round trip ahead
L3  target ← min(max(W_next, cwnd), 1.5 · cwnd)
L4  W_est ← W_est + α · acked / cwnd                   ▷ α = α_cubic, or 1 once W_est ≥ cwnd_prior
L5  if C (t − K)³ + W_max < W_est then cwnd ← W_est    ▷ the Reno-friendly region
L6  else cwnd ← cwnd + (target − cwnd) / cwnd           ▷ the concave or the convex region

ON-CONGESTION(now)                                    ▷ three duplicate ACKs, or ECN
L7  if fast convergence and cwnd < W_max then W_max ← cwnd · (1 + β) / 2 else W_max ← cwnd
L8  cwnd_prior ← cwnd, ssthresh ← β · cwnd, cwnd ← max(ssthresh, 2)
L9  t_epoch ← now, W_est ← cwnd, K ← ∛((W_max − cwnd) / C)
```

Line L9 chooses $K$ so that the curve starts at the reduced window at $t = 0$ and is back at $W_{\max}$ at $t = K$. Line L2 looks one round trip ahead, and line L6 spreads the gap to that target over the ACKs of one round trip. Line L3 keeps each step between 0 and one half of the window per round trip. Line L4 tracks the window that an AIMD flow with the increase $\alpha_{\text{cubic}} \approx 0.529$ and the decrease 0.7 would have. That flow has the same average rate as Reno, and line L5 uses its window whenever the curve is below it. Line L7 is fast convergence: if the window at the loss is below the old $W_{\max}$, another flow probably joined, so CUBIC sets the plateau lower and leaves room. A timeout still sets cwnd to one segment and starts [slow start](/slow-start/), as in Reno.

## Example

**The curve.** Take $W_{\max} = 100$, a round trip of 0.1 s and no loss after time 0. Line L8 gives $\text{cwnd} = 70$, and line L9 gives $K = \sqrt[3]{30/0.4} = \sqrt[3]{75} \approx 4.217$ s.

| $t$ (s) | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $W_{\text{cubic}}(t)$ | 70 | 86.68 | 95.64 | 99.28 | 100.00 | 100.19 | 102.27 | 108.62 | 121.65 |
| cwnd | 70 | 86.64 | 95.61 | 99.26 | 99.99 | 100.20 | 102.82 | 112.70 | 122.60 |
| $W_{\text{est}}$ | 70 | 75.21 | 80.44 | 85.70 | 90.95 | 96.23 | 102.82 | 112.70 | 122.60 |
| region | | concave | concave | concave | concave | convex | Reno-friendly | Reno-friendly | Reno-friendly |

The window gains 16.6 segments in the first second and only 0.7 in the fourth. It stays near 100 from about 3 s to 5 s. On this short path the Reno-friendly estimate passes the curve at about 6 s, since it grows by one segment per round trip after it reaches 100. With $W_{\max} = 1000$ the curve gives $K \approx 9.09$ s, and it is above the estimate for longer.

**The time between losses.** If the path holds 1000 segments and every round with a larger window loses one, the losses come every 8.4 to 9.0 s, close to $K$, whatever the round-trip time. Reno would need 300 round trips to grow from 700 to 1000: 30 s with a round trip of 0.1 s.

**Rates against Reno.** In the periodic loss model, the mean window of the cubic curve is about $1.054\,(\text{RTT}/p)^{3/4}$, and that of Reno is $\sqrt{3/(2p)}$, both in segments:

| round trip | loss rate $p$ | cubic curve | Reno |
|---|---|---|---|
| 10 ms | $10^{-4}$ | 33.3 | 122.5 |
| 10 ms | $10^{-6}$ | 1053.8 | 1224.7 |
| 100 ms | $10^{-4}$ | 187.4 | 122.5 |
| 100 ms | $10^{-6}$ | 5926.1 | 1224.7 |
| 300 ms | $10^{-6}$ | 13508.6 | 1224.7 |

Where the Reno column is larger, CUBIC is in the Reno-friendly region and behaves like Reno. On long, fast paths the curve gives several times the Reno window.

## Correctness

The curve starts at the reduced window, reaches $W_{\max}$ exactly at $t = K$, and has slope 0 there. Its derivative $3C(t - K)^2$ is never negative, so the curve only grows, and its second derivative $6C(t - K)$ makes it concave before $K$ and convex after. Each ACK adds between 0 and 0.5 segments. For an AIMD sawtooth with increase $\alpha$ and decrease factor $\beta$, the rate $B$ and the loss rate $p$ satisfy $B^2 p = \alpha(1 + \beta)/(2(1 - \beta))$, so $\alpha_{\text{cubic}} = 3(1 - \beta)/(1 + \beta)$ gives the Reno value $3/2$. The proof also derives the mean window of the cubic region in the periodic model.

## Complexity

Each ACK costs $\Theta(1)$ time, with one cube and the cube root of line L9 at each loss. The state is a few numbers. One epoch from a loss to the window at the last loss lasts $K = \sqrt[3]{W_{\max}(1 - \beta)/C}$ seconds, so it grows only as the cube root of the window and does not depend on the round-trip time. In the cubic region, the rate falls as $\text{RTT}^{-1/4}$, against $\text{RTT}^{-1}$ for Reno, so flows with different round-trip times share a link more evenly.

## Properties

- **Loss-based.** CUBIC reacts to losses and to [ECN](/ecn/) marks, so like Reno it fills the bottleneck buffer.
- **Plateau at the last loss window.** The flat part near $W_{\max}$ keeps the window stable where the network had its last loss.
- **Gentler decrease.** $\beta = 0.7$ cuts less than Reno's one half, which helps on long paths.
- **Reno-friendly.** Where Reno would get more, CUBIC uses the Reno-friendly estimate.
- **Fast convergence.** Line L7 lets an older flow with a large window give up bandwidth faster to a new flow.

## Variants and improvements

- **BIC TCP**, the predecessor, used a binary search for the window between the last loss window and the reduced window. CUBIC replaces it with one cubic function, which is simpler to analyze.
- **Slow start with HyStart.** Linux uses hybrid slow start with CUBIC to leave [slow start](/slow-start/) before the first loss, when the round-trip time starts to grow.
- **Model-based control.** [BBR](/bbr-congestion-control/) does not use losses as the main signal, and keeps a short queue.
- **Active queue management.** [CoDel](/codel/) or [RED](/red-random-early-detection/) at the bottleneck, with ECN, keeps the queue of loss-based flows such as CUBIC short.

## When to use it

CUBIC is the default choice for TCP and QUIC on general Internet paths, in particular paths with a large bandwidth-delay product. It is fair to Reno where Reno does well. On paths with a deep buffer it gives a long queueing delay, and on paths with random losses that do not come from congestion it gets less than the capacity. In those cases a model-based control such as BBR, or AQM at the bottleneck, can do better.

## Pitfalls

- **Time in the wrong unit.** $C = 0.4$ is for windows in segments and $t$ in seconds. With time in milliseconds the curve is off by a factor of $10^9$.
- **Restarting the epoch at the wrong time.** $t$ must count from the congestion event, and an idle period of the application must not count as growth time. Otherwise the first ACKs after the idle period make a large jump.
- **Leaving out the clamp of line L3.** Without it a single round trip far into the convex region can more than double the window.
- **Setting $W_{\max}$ after the reduction.** Line L7 must store the window before line L8 reduces it. If it stores the reduced window, the plateau is too low and $K$ is wrong.
- **Expecting RTT fairness against Reno.** In the Reno-friendly region CUBIC acts like Reno, with the same bias against long round trips.

## Implementations

## History

Ha, Rhee and Xu presented CUBIC in 2008 as a simpler version of their BIC TCP, which used a binary search for the window. The IETF published CUBIC as the informational RFC 8312 in 2018, and RFC 9438 made it a Standards Track protocol in 2023. RFC 9438 states that CUBIC is the default in the TCP stacks of Linux, Windows and Apple.

## References
