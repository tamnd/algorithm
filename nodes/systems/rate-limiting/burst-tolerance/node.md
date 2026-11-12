---
tag: C0TBFM
kind: definition
slug: burst-tolerance
name: Burst tolerance
aliases:
- maximum burst size
- bucket depth
area: systems/rate-limiting
level: intro
summary: How much traffic a limit lets pass at once, above its long-term rate. For a token bucket it is the depth b; at a peak rate R it allows about b R / (R - r).
prereqs: [token-bucket]
see_also: [gcra, leaky-bucket-meter, traffic-shaping, traffic-policing, single-rate-three-color-marker, fixed-window-counter, sliding-window-log, rate-limiter]
sources:
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.2 (arrival curves, Corollary 1.2.1 on GCRA and the leaky bucket), Section 1.4 (Theorem 1.4.1 on backlog and Theorem 1.4.2 on delay, and the example of a leaky bucket served by a rate-latency service curve)
  - paper: ATM Forum, Traffic Management Specification Version 4.0, af-tm-0056.000, 1996
    locator: the sustainable cell rate, the burst tolerance and the maximum burst size in the traffic contract
  - url: "https://www.rfc-editor.org/rfc/rfc2212"
    title: Scott Shenker, Craig Partridge and Roch Guerin, RFC 2212, Specification of Guaranteed Quality of Service, 1997
    locator: the sections on policing (the bound M+min[pT, rT+b-M]) and on end-to-end behavior (the delay bound with the term (b-M)/R)
---

Burst tolerance is the amount of traffic that a rate limit lets pass at once, or in a short time, on top of its long-term rate. For a [token bucket](/token-bucket/) with rate $r$ and depth $b$, it is $b$: a source that was quiet long enough can send $b$ units at the same instant. ATM traffic contracts state it in two forms: the burst tolerance $\tau_s$ of a [GCRA](/gcra/), which is a time, and the maximum burst size, the number of cells that may be sent back to back at the peak cell rate. The burst tolerance sets the buffer and the delay that the network must plan for.

## Definition

Let a limit be given by an arrival curve $\alpha$, so that each interval of length $\tau$ may hold at most $\alpha(\tau)$ units of passed traffic. The **burst tolerance** of the limit is

$$B = \lim_{\tau \to 0^+} \alpha(\tau),$$

the most traffic that can pass in an arbitrarily short time. For the token bucket curve $\alpha(\tau) = r\tau + b$, $B = b$, the *bucket depth*.

For a [GCRA](/gcra/) with emission interval $T_s$ (the inverse of the sustainable cell rate) and tolerance $\tau_s$, ATM calls $\tau_s$ the **burst tolerance** (BT). It is a time: how early a cell may come with respect to its theoretical arrival time. In cells, a quiet connection may send $1 + \lfloor \tau_s / T_s \rfloor$ cells at the same instant.

The **maximum burst size** at a peak rate is the largest number of units that can pass when they come back to back at that peak rate, starting from a quiet state.

- For unit cells with peak spacing $T < T_s$ and the test GCRA$(T_s, \tau_s)$, cell $i = 0, 1, 2, \ldots$ comes at time $iT$, and its theoretical arrival time is $iT_s$. It conforms if $iT \ge iT_s - \tau_s$, that is $i(T_s - T) \le \tau_s$. So

$$\text{MBS} = 1 + \left\lfloor \frac{\tau_s}{T_s - T} \right\rfloor, \qquad \text{and conversely} \qquad \tau_s = (\text{MBS} - 1)(T_s - T)$$

is the smallest tolerance that allows a burst of MBS cells.

- For a token bucket $(r, b)$ and unit requests at peak rate $R > r$, the first $k$ requests come in a time $(k-1)/R$ and conform while $k \le b + r(k-1)/R$, so the largest burst is

$$k_{\max} = \left\lfloor \frac{b - r/R}{1 - r/R} \right\rfloor = 1 + \left\lfloor \frac{b - 1}{1 - r/R} \right\rfloor.$$

With $b = 1 + \tau_s/T_s$, $r = 1/T_s$ and $R = 1/T$ this gives the ATM formula. In the fluid limit, a source at rate $R$ empties a full bucket in time $b/(R - r)$ and sends $bR/(R - r)$ units.

## Examples and non-examples

- **An API limit.** A token bucket with $r = 10$ requests per second and $b = 20$ lets a quiet client send 20 requests at once. If the client sends at a peak rate of $R = 100$ per second, $k_{\max} = \lfloor 19.9 / 0.9 \rfloor = 22$: the 22 requests take 0.21 seconds, in which 2.1 tokens drip in.
- **An ATM contract.** A sustainable cell rate of 1000 cells per second ($T_s = 1$ ms), a peak cell rate of 5000 cells per second ($T = 0.2$ ms) and a maximum burst size of 100 cells give $\tau_s = 99 \times 0.8$ ms $= 79.2$ ms.
- **GCRA$(10, 2)$.** Here $\tau_s/T_s = 0.2$, so only $1 + \lfloor 0.2 \rfloor = 1$ cell may come at one instant. The tolerance lets a cell come up to 2 time units early, but not a second cell at once. As a token bucket it has depth $b = 1.2$.
- **Dual bucket.** In the Integrated Services Guaranteed Service of RFC 2212, a flow has a peak rate $p$, a maximum packet size $M$, a rate $r$ and a bucket depth $b$, and "over all time periods, the amount of data sent cannot exceed M+min[pT, rT+b-M]". The burst tolerance at an instant is $M$, and the bound $pT + M$ meets $rT + b$ at $T^* = (b - M)/(p - r)$, so the largest burst at the peak rate is $M + p(b - M)/(p - r)$.
- **Window limits.** A [sliding window log](/sliding-window-log/) with limit $n$ has burst tolerance $n$. A [fixed window counter](/fixed-window-counter/) with limit $n$ has burst tolerance $2n$: $n$ requests just before a window edge and $n$ just after pass within an arbitrarily short time.
- **Not the peak rate.** A peak rate bounds the speed during a burst; burst tolerance bounds how much the burst holds. A limit with a peak rate and no sustained bucket has burst tolerance one packet.
- **Not the queue size.** A [leaky bucket queue](/leaky-bucket-queue/) with room for $K$ packets accepts $K$ packets at once, but its output has a burst of one packet, because it sends at a constant rate. The burst tolerance of its output is one packet, not $K$.

## Related definitions

- **Arrival curve.** The function $\alpha$ above. The burst tolerance is its value just after 0.
- **Buffer and delay.** By network calculus, traffic with the curve $r\tau + b$ through a server with rate $R \ge r$ and latency $T$ needs a buffer of $b + rT$ and has a delay of at most $T + b/R$ (Le Boudec and Thiran, Theorems 1.4.1 and 1.4.2). So the delay grows linearly with the burst tolerance. The delay bound of RFC 2212 for $p > R \ge r$, "[(b-M)/R*(p-R)/(p-r)]+(M+Ctot)/R+Dtot", has the same shape: its first term grows with $b - M$.
- **Cell delay variation tolerance.** The tolerance $\tau$ of the GCRA on the peak cell rate. It allows jitter at the peak rate, not a burst above the sustained rate.
- **Committed and excess burst size.** The two bucket depths of the [single-rate three-color marker](/single-rate-three-color-marker/); traffic within the first is green, within the second yellow.
- **Shaping a burst away.** A [traffic shaper](/traffic-shaping/) with a smaller depth lowers the burst tolerance of a flow at the cost of delay; a [policer](/traffic-policing/) lowers it by dropping.

## References
