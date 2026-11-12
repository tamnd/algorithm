---
tag: 97E1GT
kind: algorithm
slug: pie-aqm
name: PIE
aliases:
- proportional integral controller enhanced
- PIE AQM
area: systems/networking-algorithms
level: advanced
summary: "Every 15 ms, change a drop probability by alpha times the delay error plus beta times the delay change, and drop each arriving packet with that probability."
model: word-ram
complexity:
  vars: {n: the number of arriving packets, u: the number of updates}
  time: {worst: Θ(n + u)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: false, recursive: false}
prereqs: [active-queue-management]
see_also: [codel, red-random-early-detection, ecn, congestion-control, exponential-moving-average, tcp-reno, aimd]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc8033
    title: Rong Pan, Preethi Natarajan, Fred Baker and Greg White, Proportional Integral Controller Enhanced (PIE), A Lightweight Control Scheme to Address the Bufferbloat Problem, RFC 8033, 2017
    locator: Section 4.1 (random dropping and its safeguards), Section 4.2 (the update with QDELAY_REF 15 ms, T_UPDATE 15 ms and the auto-tuning table), Section 4.3 (the delay estimate), Section 4.4 (the burst allowance of 150 ms), Section 5 (ECN, the dequeue rate, derandomization and the cap) and Appendix A (alpha 0.125 and beta 1.25 per second)
  - paper: doi:10.1109/HPSR.2013.6602305
    title: Rong Pan, Preethi Natarajan, Chiara Piglione, Mythili Suryanarayana Prabhu, Vijay Subramanian, Fred Baker and Bill VerSteeg, PIE, A lightweight control scheme to address the bufferbloat problem, IEEE HPSR (2013)
    locator: pp. 148 to 155 (the design, the control analysis and the simulations)
  - url: https://www.rfc-editor.org/rfc/rfc8034
    title: Greg White and Rong Pan, Active Queue Management (AQM) Based on Proportional Integral Controller Enhanced (PIE) for Data-Over-Cable Service Interface Specifications (DOCSIS) Cable Modems, RFC 8034, 2017
    locator: Section 1 and Section 4 (the DOCSIS-PIE form in cable modems)
  - url: https://www.rfc-editor.org/rfc/rfc7567
    title: Fred Baker and Godred Fairhurst, IETF Recommendations Regarding Active Queue Management, RFC 7567 (BCP 197), 2015
    locator: Section 4 (an AQM should work with default parameters and should control delay)
---

PIE (Proportional Integral controller Enhanced) is an [active queue management](/active-queue-management/) algorithm by Pan and others (2013), specified in RFC 8033. It keeps one number, the drop probability. Every $T_{update} = 15$ ms it estimates the queueing delay $q$ and changes the probability by

$$\Delta p = \alpha\,(q - q_{ref}) + \beta\,(q - q_{old}),$$

with $q_{ref} = 15$ ms, $\alpha = 0.125$ and $\beta = 1.25$ per second, where $q_{old}$ is the estimate of the update before. Each arriving packet is dropped (or [ECN](/ecn/)-marked) with this probability. The first term adds up the delay error over time (the integral part), and the second reacts to the change of the delay (the proportional part). PIE scales $\Delta p$ down when the probability is small, lets bursts of up to 150 ms pass, and never drops when the queue is short.

## In plain words

PIE keeps one dial: the chance that an arriving packet is thrown away. Many times a second, it looks at how long packets now wait in the line.

If they wait longer than the goal, it turns the dial up a little. If they wait less, it turns the dial down a little. It also looks at the change since the last look: if the wait grows fast, it turns the dial up more; if the wait shrinks fast, it turns it down more.

When the dial is near zero, PIE turns it in very small steps, so that it does not jump at the first sign of a line.

A short burst after a quiet time passes with no loss. A line of one or two packets is never cut.

## The problem

A FIFO [queue](/queue/) feeds a link. The aim of an AQM, as on the [active queue management](/active-queue-management/) page, is to keep the queueing delay near a target while the link stays busy. PIE drops at enqueue, so it needs no time stamp on each packet. It estimates the delay of the queue as the number of bytes in it divided by the departure rate (Little's law), or it uses time stamps when the queue has them. The constants are those of RFC 8033: $q_{ref} = 15$ ms (QDELAY_REF), $T_{update} = 15$ ms, $\alpha = 0.125$ and $\beta = 1.25$ in units of 1 per second with delays in seconds, MAX_BURST $= 150$ ms and a mean packet size of 1500 bytes.

## The algorithm

The state is $drop\_prob$, $qdelay\_old$ and $burst\_allowance$, which starts at MAX_BURST. ENQUEUE runs for each arriving packet. UPDATE runs every $T_{update}$.

```pseudo id=main
ENQUEUE(packet)
L1  if drop_prob = 0 and qdelay < q_ref/2 and qdelay_old < q_ref/2 then burst_allowance ← MAX_BURST
L2  if burst_allowance > 0 then accept the packet;  return
L3  if (qdelay_old < q_ref/2 and drop_prob < 0.2) or queue bytes ≤ 2·MEAN_PKTSIZE then accept;  return
L4  with probability drop_prob drop the packet, else accept it

UPDATE()                                   ▷ every T_update
L5  qdelay ← queue bytes / departure rate
L6  p ← α·(qdelay − q_ref) + β·(qdelay − qdelay_old)
L7  divide p by 2048, 512, 128, 32, 8 or 2 if drop_prob < 10⁻⁶, 10⁻⁵, 10⁻⁴, 10⁻³, 10⁻² or 0.1
L8  drop_prob ← drop_prob + p
L9  if qdelay = 0 and qdelay_old = 0 then drop_prob ← 0.98 · drop_prob
L10 drop_prob ← min(1, max(0, drop_prob))
L11 qdelay_old ← qdelay;  burst_allowance ← max(0, burst_allowance − T_update)
```

Line L1 gives a fresh burst allowance after a calm time. Line L3 holds two safeguards: no drops while the last delay was below half the target and the probability is below 0.2, and no drops when the queue holds at most two packets, so the link does not go idle. Lines L6 and L8 are a discrete proportional-integral controller. Line L7 is the auto-tuning of RFC 8033: a fixed step that suits a probability near 0.1 would be far too large near 0.0001, so the step shrinks with the probability. Line L9 lets the probability decay when the queue stays empty.

RFC 8033 lists optional parts that the pseudocode leaves out: [ECN](/ecn/) marks in place of drops while $drop\_prob \le 0.1$, an estimate of the departure rate measured over $2^{14}$ bytes, derandomization that drops by a counter in place of a coin, and a cap of 0.02 on the step when $drop\_prob \ge 0.1$.

## Example

**One update.** Start from $drop\_prob = 0$ and $qdelay\_old = 0$, and let the queue hold 30 ms of data. Line L6 gives $p = 0.125 \cdot (0.030 - 0.015) + 1.25 \cdot (0.030 - 0) = 0.001875 + 0.0375 = 0.039375$. Since $drop\_prob < 10^{-6}$, line L7 divides by 2048, so $drop\_prob = 1.92 \cdot 10^{-5}$. Without the scaling, one update would give a probability of almost 4 percent.

**A long burst.** A link of 10 Mbit/s sends a 1500-byte packet in 1.2 ms. Packets arrive at twice that rate for 1 s, so the delay grows by about 15 ms per update. The probability after each update is

| time (ms) | 15 | 60 | 105 | 150 | 195 | 240 | 285 |
|---|---|---|---|---|---|---|---|
| $drop\_prob$ | $10^{-5}$ | 0.00097 | 0.0091 | 0.049 | 0.10 | 0.22 | 0.32 |

The auto-tuning gives about one factor of 10 per three updates while the probability is small. The burst allowance runs out after 10 updates, so the first drop is at 171 ms. In total PIE drops 831 of the 1666 packets, and the largest delay is 256 ms. A burst of 50 packets at the same rate (60 ms) gets no drop at all, and its largest delay is 29 ms.

**Traffic that does not respond.** Poisson arrivals at 1.2 times the link rate for 60 s (seed 1) give 59,587 packets, of which PIE drops 9,941 (16.7 percent, the excess $1 - 1/1.2$). The probability passes 0.1 at 0.57 s and then stays near 0.2. After that time the mean of the delay samples is 15.4 ms, and the mean delay of the packets that arrive in the second half is 14.0 ms. So PIE holds the delay at its target even when the senders do not respond, because the integral term moves the probability until the delay error is zero on average. [CoDel](/codel/) on the same kind of load lets the delay grow to about 100 ms.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). PIE is a controller, so the statements are about its state, not a bound on the delay for every input.

1. **The probability stays in $[0, 1]$.** Line L10 clamps it after each update, and nothing else changes it.
2. **The burst allowance.** If line L1 resets the allowance at time $t_0$, then no packet that arrives before $t_0 + \text{MAX\_BURST} - T_{update}$ (135 ms) is dropped. Packets that find at most two packets in the queue are never dropped.
3. **Integral action.** Over a run of updates $1, \dots, K$ in which $drop\_prob \ge 0.1$ and lines L9 and L10 do not change it,

$$drop\_prob_K - drop\_prob_0 = \alpha \sum_{k=1}^{K} (q_k - q_{ref}) + \beta\,(q_K - q_0),$$

so if the delay samples are at most $Q$, the mean sample is within $(1 + \beta Q) / (\alpha K)$ of $q_{ref}$. A long run with a steady probability therefore has a mean delay sample equal to the target, whatever the traffic.

The analysis of Pan and others picks $\alpha$ and $\beta$ from a linear model of TCP flows and the queue so that the loop is stable. That analysis is an approximation and is not reproduced here.

## Complexity

ENQUEUE does $O(1)$ work, one comparison chain and one random number. UPDATE does $O(1)$ work, at most six comparisons for line L7. So $n$ arrivals and $u$ updates cost $\Theta(n + u)$ time. The state is three numbers plus the byte count of the queue, $\Theta(1)$ extra space. No per-packet time stamp is needed when the delay comes from Little's law, and the controller runs on a timer, not on the fast path.

## Properties

- **Delay target.** Like [CoDel](/codel/), PIE controls the delay, not the queue length, so the target means the same on links of different rates.
- **Enqueue drops.** PIE decides at arrival, so a dropped packet never takes buffer space, and it is simple to put in hardware.
- **Randomized.** Line L4 uses a coin. With traffic that does not respond, the drop rate settles where the arrival rate after drops equals the link rate.
- **Heavier tuning than CoDel.** It has more constants: $q_{ref}$, $T_{update}$, $\alpha$, $\beta$, MAX_BURST and the table of line L7. RFC 8033 gives defaults that are meant to work without change.
- **No flow isolation.** One queue with PIE treats all flows alike.

## Variants and improvements

- **DOCSIS-PIE (RFC 8034).** A form for cable modems, with its own constants and a burst allowance adapted to the DOCSIS uplink.
- **PI and PI2.** PIE grows out of the PI controller of Hollot, Misra, Towsley and Gong (2001), which controls the queue length. PI2 drops with the square of a probability that a PI controller sets, which suits Reno-like senders, and lets scalable senders use the probability directly.
- **FQ-PIE.** PIE on each queue of a flow-queueing scheduler, as FQ-CoDel does with [CoDel](/codel/).
- **Delay from time stamps.** When the queue stamps packets, the delay of the head packet can replace line L5. The RFC allows either.

## When to use it

Use PIE where packets must be dropped at enqueue or where per-packet time stamps are costly, such as in switch hardware and cable modems, and where a fixed delay target is wanted. Prefer [CoDel](/codel/) or FQ-CoDel in software queues that already stamp packets, since CoDel has fewer constants. Prefer [RED](/red-random-early-detection/) only where a queue length is the only signal at hand.

## Pitfalls

- **Wrong units.** $\alpha$ and $\beta$ are per second, with the delay in seconds. With the delay in milliseconds, the steps are 1000 times too large.
- **Leaving out the auto-tuning.** Without line L7, the first update after a burst sets a large probability, and the queue swings between full and empty.
- **A bad rate estimate.** Line L5 needs the departure rate. On a link whose rate changes, a stale estimate gives a wrong delay. RFC 8033 measures the rate over large blocks of departures, or uses time stamps.
- **Reading the target as a bound.** The target is a mean. Single packets can wait much longer, as in the burst example.
- **Forgetting the safeguards.** Without line L3, PIE can drop when the queue holds one packet, and the link goes idle.

## Implementations

## History

Rong Pan and her coworkers at Cisco presented PIE at IEEE HPSR in 2013 as a light-weight answer to bufferbloat, at the same time as CoDel. The design adds the delay estimate, the auto-tuning and the burst allowance to the earlier PI controller for AQM. CableLabs chose a form of PIE for DOCSIS 3.1 cable modems. The IETF AQM working group published PIE as RFC 8033 and DOCSIS-PIE as RFC 8034 in February 2017. Linux has a pie queue discipline.

## References
