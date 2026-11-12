---
tag: M9FPKM
kind: algorithm
slug: single-rate-three-color-marker
name: Single rate three color marker
aliases:
- srTCM
- RFC 2697 meter
- single-rate three-color marker
area: systems/rate-limiting
level: advanced
summary: "RFC 2697 meter: buckets C (depth CBS) and E (depth EBS) fill at one rate CIR, E only from the overflow of C. A packet is green if C covers it, else yellow if E does, else red."
model: word-ram
complexity:
  vars: {n: the number of packets}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [token-bucket]
see_also: [two-rate-three-color-marker, traffic-policing, traffic-shaping, leaky-bucket-meter, gcra, burst-tolerance, red-random-early-detection, rate-limiter]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc2697
    title: "Juha Heinanen and Roch Guerin, RFC 2697, A Single Rate Three Color Marker, September 1999 (Informational)"
    locator: "Section 1 (use for ingress policing when only the burst length matters), Section 2 (CIR, CBS and EBS), Section 3 (metering: the token update and the color-blind and color-aware rules), Section 4 (marking) and Section 5 (service example)"
  - url: https://www.rfc-editor.org/rfc/rfc2698
    title: "Juha Heinanen and Roch Guerin, RFC 2698, A Two Rate Three Color Marker, September 1999 (Informational)"
    locator: "Section 1 and Section 3 (the companion meter with a separate peak rate)"
  - url: https://www.rfc-editor.org/rfc/rfc2475
    title: "Steven Blake, David Black, Mark Carlson, Elwyn Davies, Zheng Wang and Walter Weiss, RFC 2475, An Architecture for Differentiated Services, December 1998"
    locator: "Section 2.3.3 (traffic conditioners), Section 2.3.3.1 (meters) and Section 2.3.3.2 (markers)"
  - url: https://www.rfc-editor.org/rfc/rfc2597
    title: "Juha Heinanen, Fred Baker, Walter Weiss and John Wroclawski, RFC 2597, Assured Forwarding PHB Group, June 1999"
    locator: "Section 2 (four AF classes, each with three levels of drop precedence)"
---

The single rate three color marker (srTCM) is the traffic meter of RFC 2697 that colors each packet green, yellow or red, for [traffic policing](/traffic-policing/) at the edge of a network. It has one rate, the committed information rate CIR, and two [token buckets](/token-bucket/): C of depth CBS and E of depth EBS. Tokens go into C at rate CIR, and only the overflow of a full C goes into E. A packet is green if C holds enough tokens for it, else yellow if E does, else red; a red packet takes no tokens. The green packets fit the curve $CBS + CIR \cdot \tau$ and the green and yellow packets together fit $CBS + EBS + CIR \cdot \tau$, at $\Theta(1)$ time per packet.

## In plain words

Think of two jars of coins and one tap that drips coins at a fixed pace. The tap fills the first jar. When the first jar is full, the coins that spill over fall into the second jar. When both jars are full, extra coins are lost.

Each packet must pay with coins, one coin per byte, and it must pay the full price from one jar. If the first jar can pay, the packet is green: it is inside the contract. If not, but the second jar can pay, the packet is yellow: it is over the contract, but only in a burst that the customer earned by being quiet before. If neither jar can pay, the packet is red. Red packets pay nothing.

The meter only writes the color into the packet. A later stage drops red packets first and yellow packets next.

## The problem

The input is a stream of IP packets, packet $j$ with arrival time $t_j$ (non-decreasing) and size $B_j$ bytes, and in color-aware mode a color $p_j$ that an earlier node gave it. The parameters are $CIR > 0$ in bytes of IP packets per second, and $CBS \ge 0$ and $EBS \ge 0$ in bytes, with $CBS + EBS > 0$. The RFC recommends that a nonzero burst size be at least the largest IP packet of the stream.

The output is one color per packet, decided online at the arrival time and without delay, such that the green traffic conforms to the token bucket $(CIR, CBS)$ of the [rate limiting problem](/rate-limiting-problem/), and the yellow traffic is the part of the rest that an excess burst of size EBS can carry. The arrival model is adversarial: no assumption is made on the times or sizes.

## The algorithm

The meter state is $T_c$, $T_e$ and the time $last$ of the last update. At the start, $T_c = CBS$, $T_e = EBS$ and $last$ is the start time. In color-blind mode, call METER with $pre$ = green for every packet.

```pseudo id=main
SRTCM-REFILL(M, t)                       ▷ lazy update: CIR · (t − last) new tokens
L1  a ← CIR · (t − M.last); M.last ← t
L2  f ← min(a, CBS − M.Tc)                ▷ the part that fits into C
L3  M.Tc ← M.Tc + f
L4  M.Te ← min(EBS, M.Te + (a − f))       ▷ only the overflow of C reaches E

SRTCM-METER(M, t, B, pre)                ▷ packet of B bytes at time t, precolor pre
L5  SRTCM-REFILL(M, t)
L6  if pre = green and M.Tc − B ≥ 0 then
L7      M.Tc ← M.Tc − B; return green
L8  if pre ∈ {green, yellow} and M.Te − B ≥ 0 then
L9      M.Te ← M.Te − B; return yellow
L10 return red                            ▷ red takes no tokens
```

The RFC describes the token update as a process that adds one token CIR times per second: to C if $T_c < CBS$, else to E if $T_e < EBS$, else nowhere. Lines L1 to L4 do the same work at once, only when a packet comes. Lines L6 to L10 are the rules of RFC 2697, Section 3. With $pre$ = green they are the color-blind rules: green if $T_c - B \ge 0$, else yellow if $T_e - B \ge 0$, else red. With the real precolor they are the color-aware rules: a precolored yellow packet is never tested against C, and a precolored red packet stays red.

## Example

Let $CIR = 1000$ bytes per second, $CBS = 2000$ and $EBS = 2000$ bytes, in color-blind mode. The counts are written $T_c, T_e$.

| time (s) | size $B$ | after refill (L5) | color | after the packet |
|---|---|---|---|---|
| 0 | 1500 | 2000, 2000 | green | 500, 2000 |
| 0 | 1500 | 500, 2000 | yellow | 500, 500 |
| 0 | 1500 | 500, 500 | red | 500, 500 |
| 1 | 1500 | 1500, 500 | green | 0, 500 |
| 1.5 | 1000 | 500, 500 | red | 500, 500 |
| 5 | 1500 | 2000, 2000 | green | 500, 2000 |
| 5 | 1500 | 500, 2000 | yellow | 500, 500 |
| 5 | 1000 | 500, 500 | red | 500, 500 |

At time 1 the 1000 new tokens all go to C, because C is not full. At time 5 the refill brings 3500 tokens: 1500 fill C, 1500 fill E, and the last 500 are lost. The packet at time 1.5 is red although the two buckets hold 1000 tokens together, because a packet must be paid from one bucket. On $[0, 5]$ the green and yellow packets carry 7500 bytes, below the bound $CBS + EBS + 5 \cdot CIR = 9000$.

In color-aware mode, give the eight packets the precolors green, green, yellow, green, green, yellow, green, green. The first five packets get the same colors as before. At time 5 the first packet is precolored yellow, so it is yellow and takes 1500 tokens from E, while C stays full at 2000. The next packet is then green and leaves $T_c = 500$, and the last packet is red. The counts end at 500 and 500 again, but the green packet is now a different one.

## Correctness

The proof is below. It has four parts.

- **The RFC rules.** The lazy refill of lines L1 to L4 gives the counts $T_c' = \min(CBS, T_c + a)$ and $T_e' = \min(EBS, T_e + \max(0, a - (CBS - T_c)))$, which is what the RFC token process gives after $a$ tokens. Lines L6 to L10 are the RFC rules, in both modes. The counts stay in $[0, CBS]$ and $[0, EBS]$, so the RFC's "decremented by B down to the minimum value of 0" never needs the floor.
- **No upgrade.** In color-aware mode a packet never leaves with a better color than it came with.
- **Green is a token bucket.** $T_c$ does not depend on $T_e$, so in color-blind mode the green packets are exactly the packets that a [token bucket](/token-bucket/) with rate CIR and depth CBS passes. In color-aware mode they are the packets that this token bucket passes when it sees only the precolored green packets.
- **Interval bounds.** In every interval of length $\tau$, the green bytes are at most $CBS + CIR\tau$, the yellow bytes are at most $EBS + CIR\tau$, and the green and yellow bytes together are at most $CBS + EBS + CIR\tau$. All three bounds are reached. So the long-term rate of non-red traffic is at most CIR: the excess bucket buys burst size, not rate.

## Complexity

In the [word RAM](/word-ram/), with the times and the counts in words:

- **Time.** Each packet runs lines L1 to L10 at most once, with no loop: $\Theta(1)$ in the worst case, and $\Theta(n)$ for $n$ packets.
- **Space.** Three numbers per metered stream: $T_c$, $T_e$ and $last$. A router with $k$ metered streams keeps $\Theta(k)$ words.

## Properties

- **Online and without delay.** Each color depends only on the packets so far, and no packet waits.
- **Marks, does not drop.** The meter only sets a color, for example the drop precedence of an Assured Forwarding class of RFC 2597. The dropping policy is a separate stage.
- **No peak rate.** A burst of up to $CBS + EBS$ bytes can leave green or yellow at line rate. The srTCM limits the size of a burst, not its rate; that is why RFC 2697 suggests it for services where "only the length, not the peak rate, of the burst determines service eligibility".
- **Not one bucket of depth CBS + EBS.** A token bucket with rate CIR and depth $CBS + EBS$ passes a packet when $T_c + T_e \ge B$. The srTCM needs $T_c \ge B$ or $T_e \ge B$, so it can color a packet red that this bucket would pass, as at time 1.5 above. The two meters share only the interval bound.
- **Red is free.** A red packet takes no tokens, so a flood of red packets does not hurt the next packet.

## Variants and improvements

- **Color-blind and color-aware modes.** Both are in the RFC. Color-aware mode lets a chain of meters keep the colors that an upstream meter gave.
- **[Two rate three color marker](/two-rate-three-color-marker/).** RFC 2698 replaces the excess bucket with a peak bucket that fills at its own rate PIR and is charged by both green and yellow packets. It limits the peak rate as well as the committed rate.
- **Two rates with green charged once.** RFC 4115 gives E its own rate EIR, with no overflow from C, and charges a green packet only to C. A yellow packet is charged only to E.
- **Discrete or fluid tokens.** The RFC adds whole tokens CIR times per second. Most implementations compute the tokens from the elapsed time, as lines L1 to L4 do. The two agree at packet times that fall on the token grid.
- **Policer.** Drop the red packets at once and the srTCM becomes a [traffic policer](/traffic-policing/) whose output fits $CBS + EBS + CIR\tau$, with the yellow packets marked for early drop downstream.

## When to use it

Use an srTCM at the edge of a network or a service when a customer buys one committed rate and you want to allow, but mark, occasional bursts above it. A later queue can use the colors, for example by dropping yellow packets earlier than green ones with an [active queue management](/active-queue-management/) scheme such as [RED](/red-random-early-detection/). Use the [two-rate marker](/two-rate-three-color-marker/) when the contract also caps the peak rate. Use a plain [token bucket](/token-bucket/) when two classes, pass and drop, are enough.

## Pitfalls

- **Feeding E at its own rate.** E gets only the overflow of C. If E also fills at CIR on its own, the long-term rate of green plus yellow traffic can reach $2 \cdot CIR$, which is not the srTCM.
- **Refilling E first.** Lines L2 to L4 must fill C before E. The other order sends tokens to E while C is not full.
- **Splitting a packet across the buckets.** RFC 2697 requires that one bucket hold the whole packet. Taking part of the size from C and the rest from E gives a different meter.
- **Charging red packets.** A red packet must leave both counts unchanged. Charging it makes the meter punish the stream for traffic that was already marked as excess.
- **Upgrading in color-aware mode.** A precolored yellow packet must never be tested against C. Testing it there would let a downstream meter turn yellow traffic green.
- **Burst sizes below the packet size.** If CBS is smaller than the largest packet, such packets can never be green. The RFC recommends that a nonzero CBS or EBS be at least the largest IP packet.
- **Wrong units.** CIR counts bytes of IP packets per second, with the IP header but without link-layer headers. A meter that counts link-layer bytes or bits gives a different rate.

## Implementations

The Python version keeps times and counts as `int` or `Fraction`, so the tests are exact. A reference follows RFC 2697 literally: it adds the tokens one at a time with the rule of Section 3 and then applies the text of the color-blind or color-aware rules. The tests compare the colors and the counts of the lazy meter with this reference on every trace of up to three packets with small parameters, and on seeded random traces. They also check, on random traces with fractional times, that the green packets are the output of a token bucket $(CIR, CBS)$, that no color improves in color-aware mode, and the three interval bounds over every pair of packets.

## History

Juha Heinanen and Roch Guerin published the srTCM as RFC 2697 in September 1999, together with the two-rate marker of RFC 2698. Both are Informational RFCs of the Differentiated Services work of the IETF, whose architecture (RFC 2475, 1998) splits a traffic conditioner into meters, markers, shapers and droppers. The three colors fit the three drop precedences of the Assured Forwarding group of RFC 2597.

## References
