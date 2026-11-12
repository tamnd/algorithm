---
tag: 2FQ2DX
kind: algorithm
slug: two-rate-three-color-marker
name: Two rate three color marker
aliases:
- trTCM
- RFC 2698 meter
- two-rate three-color marker
area: systems/rate-limiting
level: advanced
summary: "RFC 2698 meter: bucket P fills at the peak rate PIR up to PBS, bucket C at the committed rate CIR up to CBS. A packet is red if P cannot cover it, else yellow if C cannot, else green."
model: word-ram
complexity:
  vars: {n: the number of packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [token-bucket, single-rate-three-color-marker]
see_also: [traffic-policing, traffic-shaping, burst-tolerance, gcra, leaky-bucket-meter, red-random-early-detection, rate-limiter]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc2698
    title: "Juha Heinanen and Roch Guerin, RFC 2698, A Two Rate Three Color Marker, September 1999 (Informational)"
    locator: "Section 1 (use for ingress policing with a separate peak rate), Section 2 (PIR, PBS, CIR and CBS, with PIR at least CIR), Section 3 (metering: the token update and the color-blind and color-aware rules) and Section 5 (service example)"
  - url: https://www.rfc-editor.org/rfc/rfc2697
    title: "Juha Heinanen and Roch Guerin, RFC 2697, A Single Rate Three Color Marker, September 1999 (Informational)"
    locator: "Section 3 (the single-rate meter with an excess bucket fed by overflow)"
  - url: https://www.rfc-editor.org/rfc/rfc4115
    title: "Osama Aboul-Magd and Sameh Rabie, RFC 4115, A Differentiated Service Two-Rate, Three-Color Marker with Efficient Handling of in-Profile Traffic, July 2005 (Informational)"
    locator: "Section 1 (the differences from RFC 2698) and Section 3 (the meter with rates CIR and EIR, where green packets are charged only to the committed bucket)"
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Chapter 1, Section 1.2 (arrival curves, and the affine curves of token buckets)
---

The two rate three color marker (trTCM) is the traffic meter of RFC 2698 that colors each packet green, yellow or red against two rates: a peak information rate PIR and a committed information rate CIR. It runs two independent [token buckets](/token-bucket/): P fills at PIR up to depth PBS, and C fills at CIR up to depth CBS. A packet that P cannot cover is red; otherwise it is yellow if C cannot cover it and green if C can. Green packets pay both buckets and yellow packets pay only P, so the non-red traffic fits $PBS + PIR\tau$ and the green traffic fits $CBS + CIR\tau$, at $\Theta(1)$ time per packet.

## In plain words

There are two jars of coins, each with its own tap. The fast tap fills the peak jar, and the slow tap fills the committed jar. Each jar has its own size, and coins that do not fit are lost.

A packet first asks the peak jar for one coin per byte. If the peak jar cannot pay the full price, the packet is red: it is above the fastest speed the customer may send. If the peak jar can pay, the packet then asks the committed jar. If the committed jar can also pay, the packet is green and both jars pay. If not, the packet is yellow, and only the peak jar pays.

So green traffic stays within the committed speed, green and yellow traffic together stay within the peak speed, and everything above the peak speed is red.

## The problem

The input is a stream of IP packets, packet $j$ with arrival time $t_j$ (non-decreasing) and size $B_j$ bytes, and in color-aware mode a color $p_j$ that an earlier node gave it. The parameters are the rates $PIR$ and $CIR$ in bytes of IP packets per second, with $PIR \ge CIR > 0$, and the depths $PBS > 0$ and $CBS > 0$ in bytes. The RFC recommends depths of at least the largest IP packet of the stream.

The output is one color per packet, decided online at the arrival time and without delay, such that the green traffic conforms to the token bucket $(CIR, CBS)$ and the green and yellow traffic together conform to the token bucket $(PIR, PBS)$, in the sense of the [rate limiting problem](/rate-limiting-problem/). The arrival model is adversarial.

## The algorithm

The meter state is $T_p$, $T_c$ and the time $last$ of the last update. At the start, $T_p = PBS$, $T_c = CBS$ and $last$ is the start time. In color-blind mode, call METER with $pre$ = green for every packet.

```pseudo id=main
TRTCM-METER(M, t, B, pre)                ▷ packet of B bytes at time t, precolor pre
L1  M.Tp ← min(PBS, M.Tp + PIR · (t − M.last))
L2  M.Tc ← min(CBS, M.Tc + CIR · (t − M.last))
L3  M.last ← t
L4  if pre = red or M.Tp − B < 0 then return red     ▷ red takes no tokens
L5  if pre = yellow or M.Tc − B < 0 then
L6      M.Tp ← M.Tp − B; return yellow
L7  M.Tp ← M.Tp − B; M.Tc ← M.Tc − B
L8  return green
```

Lines L1 to L3 replace the RFC's process that adds one token to P PIR times per second and one token to C CIR times per second, each up to its depth. Lines L4 to L8 are the rules of RFC 2698, Section 3. With $pre$ = green they are the color-blind rules: red if $T_p - B < 0$, else yellow if $T_c - B < 0$, else green. With the real precolor they are the color-aware rules: a precolored red packet stays red, and a precolored yellow packet is yellow if P can cover it.

## Example

Let $PIR = 2000$ and $CIR = 1000$ bytes per second, $PBS = 3000$ and $CBS = 2000$ bytes, in color-blind mode. The counts are written $T_p, T_c$.

| time (s) | size $B$ | after refill (L3) | color | after the packet |
|---|---|---|---|---|
| 0 | 1000 | 3000, 2000 | green | 2000, 1000 |
| 0 | 1000 | 2000, 1000 | green | 1000, 0 |
| 0 | 1000 | 1000, 0 | yellow | 0, 0 |
| 0 | 1000 | 0, 0 | red | 0, 0 |
| 0.5 | 1000 | 1000, 500 | yellow | 0, 500 |
| 1 | 1000 | 1000, 1000 | green | 0, 0 |
| 1.25 | 500 | 500, 250 | yellow | 0, 250 |
| 3 | 1500 | 3000, 2000 | green | 1500, 500 |
| 3 | 1500 | 1500, 500 | yellow | 0, 500 |

On $[0, 1.25]$ the green and yellow packets carry 5500 bytes, which is exactly the peak bound $PBS + PIR \cdot 1.25 = 3000 + 2500$, and the green packets carry 3000 bytes, below $CBS + CIR \cdot 1.25 = 3250$.

Compare the [single rate marker](/single-rate-three-color-marker/) with $CIR = 1000$, $CBS = 2000$ and $EBS = 1000$ on the same trace. It gives green, green, yellow, red, red, green, red, green, red. The packets at times 0.5 and 1.25 are red there, because its excess bucket fills only when C is full. Under steady traffic above CIR, the trTCM keeps marking up to $PIR - CIR$ bytes per second yellow, while the srTCM marks this traffic red.

In color-aware mode, give the nine packets the precolors green, yellow, green, green, green, green, green, yellow, green. The colors are green, yellow, green, red, yellow, green, yellow, yellow, green. The second packet is yellow and pays only P, so C still holds 1000 tokens for the third packet, which is now green. At time 3 the first packet is precolored yellow, so C stays full and the next packet is green.

## Correctness

The proof is below. It has four parts.

- **The RFC rules.** Lines L1 to L3 give the counts of the RFC token process, and lines L4 to L8 are its rules, in both modes. The counts stay in $[0, PBS]$ and $[0, CBS]$.
- **No upgrade.** In color-aware mode no packet leaves with a better color than it came with.
- **Non-red is a token bucket.** $T_p$ is charged exactly by the packets that are not red, so in color-blind mode the non-red packets are exactly the packets that a [token bucket](/token-bucket/) with rate PIR and depth PBS passes. The green packets are not the output of one token bucket: C sees only the packets that P let through.
- **Interval bounds.** In every interval of length $\tau$, the green bytes are at most $CBS + CIR\tau$, and the green and yellow bytes together are at most $PBS + PIR\tau$. Both bounds are reached on one trace when $PBS \ge CBS$. Green packets also pay P, so a green burst at one instant is at most $\min(CBS, PBS)$ bytes.

## Complexity

In the [word RAM](/word-ram/), with the times and the counts in words:

- **Time.** Each packet runs lines L1 to L8 at most once, with no loop: $\Theta(1)$ in the worst case, and $\Theta(n)$ for $n$ packets.
- **Space.** Three numbers per metered stream: $T_p$, $T_c$ and $last$.

## Properties

- **Online and without delay.** Each color depends only on the packets so far, and no packet waits.
- **Two rates.** The long-term rate of green traffic is at most CIR, and that of green and yellow traffic together is at most PIR. The srTCM has only the first limit.
- **Independent buckets.** No tokens move from one bucket to the other. Tokens that do not fit are lost.
- **Red is free.** A red packet takes no tokens.
- **Marks, does not drop.** As with the srTCM, the colors feed a later dropper, for example the drop precedences of RFC 2597.

## Variants and improvements

- **Color-blind and color-aware modes.** Both are in the RFC. In color-aware mode the meter respects the colors of an upstream meter.
- **[Single rate three color marker](/single-rate-three-color-marker/).** RFC 2697 has one rate, and its excess bucket fills only from the overflow of C. It limits the size of a burst, not its peak rate.
- **RFC 4115.** It uses a committed rate CIR and an excess rate EIR. A green packet is charged only to the committed bucket, and a yellow packet only to the excess bucket. In-profile traffic is then never cut by a small peak bucket, and the green and yellow traffic together can reach $CIR + EIR$.
- **A dual token bucket policer.** Drop the red packets and pass the rest: the output fits $PBS + PIR\tau$. This is the peak part of the dual bucket of [burst tolerance](/burst-tolerance/), with the committed bucket used only for marking.
- **Shaping at the peak rate.** A sender can shape its traffic to PIR with a [traffic shaper](/traffic-shaping/) before the meter, so that no packet is red.

## When to use it

Use a trTCM at the edge of a network when the contract has two rates: a committed rate that the provider guarantees, and a peak rate above which traffic is not accepted at all. Typical Differentiated Services setups drop red packets, forward yellow packets as best effort, and forward green packets with the committed service, as in the service example of RFC 2698. Use the [srTCM](/single-rate-three-color-marker/) when only the burst length matters.

## Pitfalls

- **PIR below CIR.** RFC 2698 requires $PIR \ge CIR$. With a smaller PIR, the peak bucket, not the committed bucket, decides how much traffic is green.
- **PBS below CBS.** Green packets also pay P, so a green burst is at most PBS bytes. RFC 4115 notes that this can force a customer to shape its traffic to PIR.
- **Charging a yellow packet to C.** A yellow packet pays only P. Charging C as well makes the green rate fall below CIR under load.
- **Charging green only to C.** In RFC 2698 a green packet pays both buckets. Charging it only to C gives the meter of RFC 4115, which allows more than PIR in total.
- **Upgrading in color-aware mode.** A precolored yellow packet must never be tested against C, and a precolored red packet must not take tokens.
- **Wrong units.** The rates count bytes of IP packets per second, with the IP header but without link-layer headers.

## Implementations

The Python version keeps times and counts as `int` or `Fraction`. A reference follows RFC 2698 literally: it adds the tokens of each bucket one at a time, up to the depth, and then applies the text of the color-blind or color-aware rules. The tests compare the colors and the counts with this reference on every trace of up to three packets for five parameter sets, and on seeded random traces, in both modes. They also check that the non-red packets are the output of a token bucket $(PIR, PBS)$, that no color improves in color-aware mode, and both interval bounds over every pair of packets.

## History

Juha Heinanen and Roch Guerin published the trTCM as RFC 2698 in September 1999, together with the single-rate marker of RFC 2697, as Informational RFCs of the Differentiated Services work of the IETF. In 2005 RFC 4115 by Aboul-Magd and Rabie gave a two-rate marker that charges green packets only to the committed bucket, to handle in-profile traffic better.

## References
