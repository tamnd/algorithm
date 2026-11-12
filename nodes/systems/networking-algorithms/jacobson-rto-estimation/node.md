---
tag: CNHXD2
kind: algorithm
slug: jacobson-rto-estimation
name: Jacobson's RTO estimation
aliases:
- Jacobson-Karels algorithm
- RFC 6298 retransmission timer
area: systems/networking-algorithms
level: advanced
summary: Keep a moving average of the RTT and of its mean deviation, and set the retransmission timeout to SRTT + 4 RTTVAR. Double it on each timeout.
solves: [round-trip-time-estimation]
model: word-ram
complexity:
  vars: {n: the number of RTT samples}
  time: {best: Θ(n), worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Van Jacobson, Michael J. Karels]
  note: Jacobson added the mean deviation of the RTT to the timeout in Congestion Avoidance and Control (SIGCOMM 1988). RFC 2988 (2000) and RFC 6298 (2011) made it the TCP standard.
prereqs: [round-trip-time-estimation, exponential-moving-average]
see_also: [karn-algorithm, exponential-backoff, slow-start, congestion-control, phi-accrual-failure-detector, peak-ewma]
sources:
  - paper: doi:10.1145/52324.52356
    title: Van Jacobson, Congestion avoidance and control, Proceedings of SIGCOMM 1988, 314-329
    locator: Section 2, Round-trip timing, and Appendix A, A fast algorithm for RTT mean and variation
  - url: https://www.rfc-editor.org/rfc/rfc6298
    title: RFC 6298, Computing TCP's Retransmission Timer, 2011
    locator: Section 2, rules 2.1 to 2.5; Section 3, Taking RTT Samples; Section 5, rule 5.5 and rule 5.7
  - url: https://www.rfc-editor.org/rfc/rfc2988
    title: RFC 2988, Computing TCP's Retransmission Timer, 2000
    locator: Section 2, the initial RTO of 3 seconds
  - url: https://www.rfc-editor.org/rfc/rfc793
    title: RFC 793, Transmission Control Protocol, 1981
    locator: Section 3.7, Retransmission Timeout (the earlier rule with ALPHA and BETA)
  - book: isbn:9780136681557
    title: James F. Kurose and Keith W. Ross, Computer Networking, A Top-Down Approach, eighth edition
    locator: Section 3.5.3, Round-Trip Time Estimation and Timeout
  - book: isbn:9780123850591
    title: Larry L. Peterson and Bruce S. Davie, Computer Networks, A Systems Approach, fifth edition
    locator: Section 5.2.6, Adaptive Retransmission (the Jacobson/Karels algorithm)
---

Jacobson's RTO estimation is the rule that TCP uses to set its retransmission timeout (RTO), a solution of the [round-trip time estimation](/round-trip-time-estimation/) problem. It keeps two [exponential moving averages](/exponential-moving-average/): SRTT of the round-trip time samples, and RTTVAR of their absolute deviation from SRTT. The timeout is $\mathrm{SRTT} + 4\,\mathrm{RTTVAR}$, so it follows the spread of the delay as well as its mean. On a timeout the RTO doubles. Van Jacobson proposed it in 1988, and RFC 6298 specifies it.

## In plain words

You want to know how long to wait for a reply before you ask again. You measure each reply time. You keep a running average of the times, and you also keep a running average of how far each time was from the average.

You then wait for the average plus four times the typical miss. If the replies come at very regular times, you wait a little more than the average. If they jump around, you wait much longer, so a slow reply does not make you ask again for nothing.

If you must ask again, you double the wait each time, because the path may be much slower than you thought.

## The problem

A sender measures round-trip times $R_1, R_2, \ldots$ of segments that were sent once (see [Karn's algorithm](/karn-algorithm/)). It must choose a timeout that is rarely shorter than the next round trip, because a spurious retransmission wastes the link, and not much longer, because a real loss is repaired only when the timer expires.

The earlier rule of RFC 793 set $\mathrm{SRTT} \leftarrow \alpha\,\mathrm{SRTT} + (1-\alpha) R$ with $\alpha$ from 0.8 to 0.9, and $\mathrm{RTO} = \min(\mathrm{UBOUND}, \max(\mathrm{LBOUND}, \beta\,\mathrm{SRTT}))$ with $\beta$ from 1.3 to 2.0. A fixed multiple of the mean is too small when the delay varies much, and too large when it varies little.

## The algorithm

The rule uses $\alpha = 1/8$, $\beta = 1/4$, $K = 4$ and the clock granularity $G$. All times are in seconds.

```pseudo id=main
JACOBSON-RTO
L1  RTO ← 1                                   ▷ before the first sample (rule 2.1)
L2  on an RTT sample R from a segment that was sent once:
        if this is the first sample then
L3          SRTT ← R
L4          RTTVAR ← R/2
        else
L5          RTTVAR ← (1 − β)·RTTVAR + β·|SRTT − R|   ▷ uses the old SRTT
L6          SRTT ← (1 − α)·SRTT + α·R
L7      RTO ← SRTT + max(G, K·RTTVAR)
L8      if RTO < 1 then RTO ← 1                ▷ rule 2.4; an upper bound of at least 60 s may apply
L9  on a timeout: RTO ← 2·RTO                  ▷ rule 5.5, with the same bounds
```

Line L5 must run before line L6. A new sample after a timeout replaces the doubled value of line L9 by the value of line L7.

## Example

Samples of 0.5, 0.6, 0.4, 1.2 and 0.5 s, with $G = 0$ and without the 1 s lower bound, give these exact values:

| sample $R$ | RTTVAR | SRTT | RTO |
|---|---|---|---|
| 0.5 | 1/4 = 0.25 | 1/2 = 0.5 | 3/2 = 1.5 |
| 0.6 | 17/80 = 0.2125 | 41/80 = 0.5125 | 109/80 = 1.3625 |
| 0.4 | 3/16 = 0.1875 | 319/640 ≈ 0.4984 | 799/640 ≈ 1.2484 |
| 1.2 | 809/2560 ≈ 0.3160 | 3001/5120 ≈ 0.5861 | 9473/5120 ≈ 1.8502 |
| 0.5 | 1059/4096 ≈ 0.2585 | 23567/40960 ≈ 0.5754 | 65927/40960 ≈ 1.6095 |

For the second row, $\mathrm{RTTVAR} = \frac34 \cdot \frac14 + \frac14 |0.5 - 0.6| = 0.2125$ and $\mathrm{SRTT} = \frac78 \cdot 0.5 + \frac18 \cdot 0.6 = 0.5125$. If SRTT were updated first, RTTVAR would be $67/320 \approx 0.2094$.

The spike of 1.2 s raises RTTVAR from 0.19 to 0.32, so the RTO grows from 1.25 to 1.85 s, while SRTT grows by only 0.09 s.

On a trace of four samples of 0.1 s and one of 0.4 s, repeated 20 times, the RFC 793 rule with $\alpha = 0.9$ and $\beta = 2$ never gets above $2 \cdot 0.174$, so all 20 spikes are late. This rule, without the 1 s bound, is late only for the spikes at the indices 4, 9 and 14; after these, RTTVAR stays large enough.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). SRTT is a weighted mean of the samples with positive weights $\frac18 (\frac78)^{n-i}$ (and $(\frac78)^{n-1}$ for the first), so it lies between the smallest and the largest sample. RTTVAR is the same kind of mean of the deviations. For constant samples $R$, $\mathrm{RTTVAR}_n = (3/4)^{n-1} R/2$, so the RTO falls geometrically to $R + G$. If a sample exceeds SRTT by $d$, then $4\,\mathrm{RTTVAR} \ge d$ after it, so the next RTO is at least the sample plus $d/8$, and the same delay is not late twice in a row. The doubling of line L9 reaches any round-trip time $D$ below the upper bound after at most $\lceil \log_2 D \rceil + 1$ timeouts.

## Complexity

Each sample costs $O(1)$ arithmetic operations and the state is three numbers. Jacobson's original code uses integers: it stores $8\,\mathrm{SRTT}$ and $4\,\mathrm{RTTVAR}$, so the updates need only additions and shifts.

## Properties

- **Online.** One pass over the samples, constant memory.
- **Adapts to the spread.** The timeout uses the mean deviation, which is a cheap stand-in for the standard deviation and needs no square root.
- **Conservative start.** The first sample gives $\mathrm{RTO} = R + 2R = 3R$.
- **Lower bound.** RFC 6298 says that the RTO SHOULD be rounded up to 1 s, to avoid spurious timeouts. Some stacks use a lower bound; Linux uses 200 ms.
- **Initial value.** The RTO before the first sample is 1 s; RFC 2988 had 3 s. If the SYN or its answer times out, the RTO is set back to 3 s for data (rule 5.7).

## Variants and improvements

- **Timestamps.** The TCP timestamps option (RFC 7323) gives a sample for almost every ACK, also for retransmitted segments. Then RFC 7323 scales $\alpha$ and $\beta$ down, so that one round trip has about the same weight as before.
- **Linux.** Linux keeps a separate mean deviation that falls more slowly, and a lower bound of 200 ms on the RTO.
- **Other K.** A larger $K$ gives fewer spurious timeouts and slower repair of real losses.
- **RFC 793 rule.** $\beta\,\mathrm{SRTT}$ with UBOUND and LBOUND. It is simpler, but it fails when the delay varies, as in the example.
- **Outside TCP.** The same average and deviation set timeouts in QUIC (RFC 9002, which uses the smallest RTT too), in RPC systems, and in [failure detectors](/failure-detector/).

## When to use it

Use it to set a retransmission or request timeout from measured round-trip times when the delay changes over time. Take samples only from requests that were sent once, and use [exponential backoff](/exponential-backoff/) for timeouts in a row.

## Pitfalls

- **Samples from retransmissions.** The ACK may belong to any copy, so the sample can be much too short or too long. Use [Karn's algorithm](/karn-algorithm/).
- **Wrong order of the updates.** Line L5 uses the SRTT from before the sample.
- **Coarse clocks.** With a 500 ms tick, RTTVAR can fall to 0. The term $\max(G, K\,\mathrm{RTTVAR})$ keeps one tick of margin.
- **No upper bound and no reset.** After many backoffs the RTO can be very large; the next valid sample must replace it.
- **Floating point in tests.** The exact values above need fractions; with floating point, compare with a tolerance.

## Implementations

## History

RFC 793 (1981) used a fixed multiple of the smoothed RTT. In the congestion collapses of 1986, Van Jacobson saw that this timeout fired too early when the load made the delay vary. His paper Congestion Avoidance and Control (SIGCOMM 1988) added the mean deviation to the timeout and gave a fast integer version. The revised version of the paper has Michael J. Karels as a second author. It went into 4.3BSD Tahoe, together with [slow start](/slow-start/) and Karn's algorithm. RFC 1122 (1989) required it for hosts. RFC 2988 (2000) wrote down the exact rules with an initial RTO of 3 s, and RFC 6298 (2011) changed the initial RTO to 1 s.

## References
