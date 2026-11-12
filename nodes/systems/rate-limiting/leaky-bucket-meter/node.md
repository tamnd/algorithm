---
tag: JQZSX6
kind: algorithm
slug: leaky-bucket-meter
name: Leaky bucket (meter)
aliases:
- leaky bucket as a meter
- leaky bucket counter
area: systems/rate-limiting
level: intro
summary: A counter that drains at rate r and admits a request if adding it keeps the level at or below capacity.
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {n: the number of requests on one key}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1986
  people: [Jonathan S. Turner]
  note: Turner described the leaky bucket for packet networks in 1986. The ATM standards later defined the GCRA, whose second form is a leaky bucket meter.
prereqs: [token-bucket]
see_also: [token-bucket, gcra, leaky-bucket-queue, traffic-policing, burst-tolerance, rate-limiter, sliding-window-log]
sources:
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.2.2, Definition 1.2.2 (leaky bucket controller), Lemma 1.2.2 (content of a buffer served at constant rate) and Proposition 1.2.3 (the controller enforces the arrival curve r t + b)
  - paper: doi:10.1109/MCOM.1986.1092946
    title: Jonathan S. Turner, New directions in communications (or which way to the information age?), IEEE Communications Magazine 24(10), 1986
    locator: the leaky bucket as a way to control the rate and the burstiness of a virtual circuit
  - url: "https://www.itu.int/rec/T-REC-I.371"
    title: ITU-T Recommendation I.371, Traffic control and congestion control in B-ISDN, 2004
    locator: Annex A, the generic cell rate algorithm in its continuous-state leaky bucket form
  - book: isbn:9780132126953
    title: Andrew S. Tanenbaum and David J. Wetherall, Computer Networks, fifth edition
    locator: Chapter 5, Section 5.4.2 (traffic shaping, leaky and token buckets)
---

A leaky bucket meter is a [rate limiter](/rate-limiter/) that keeps one counter, the level of a bucket of size $b$ that leaks at rate $r$. A packet of size $L$ conforms if pouring $L$ into the bucket does not make it overflow; then the level goes up by $L$. A nonconforming packet is dropped or marked at once, and the bucket does not change. The meter is the mirror image of the [token bucket](/token-bucket/): its level is always $b$ minus the tokens, so it makes the same decisions and gives the same guarantee, the arrival curve $r\tau + b$. It is not the same as the [leaky bucket queue](/leaky-bucket-queue/), which holds the packets and sends them out at a constant rate.

## In plain words

Think of a bucket with a small hole in the bottom. Water runs out of the hole at a steady pace while there is water in it. Each request must pour its own amount of water into the bucket. If the water fits, the request goes through. If the bucket would overflow, the request is refused, and it pours nothing.

A client that was quiet for a while finds an empty bucket, so it can send a short burst. A client that sends all the time can only go as fast as the water runs out. The program does not let the water run out drop by drop. When a request comes, it looks at the clock, works out how much water ran out since the last request, and takes it off in one step.

## The problem

The input is a sequence of packets (or requests) at times $t_1 \le t_2 \le \cdots$ with sizes $L_k > 0$; for request counting, $L_k = 1$. The meter decides each packet at its arrival, with no delay. The passed packets must fit the $(r, b)$ arrival curve of the [rate limiting problem](/rate-limiting-problem/): each interval of length $\tau$ holds at most $r\tau + b$ units of passed packets. The arrival model is adversarial: no assumption on the times or sizes. We assume $b \ge \max_k L_k$, because a larger packet can never pass.

## The algorithm

Each key has a bucket with the parameters $r$ and $b$, the level $X$ and the time $last$ of the last update. At the start, $X = 0$: the bucket is empty.

```pseudo id=main
LEAKY-BUCKET-METER(B, t, L)          ▷ a packet of size L arrives at time t ≥ B.last
L1  B.X ← max(0, B.X − r · (t − B.last))     ▷ lazy leak, never below empty
L2  B.last ← t
L3  if B.X + L ≤ b then
L4      B.X ← B.X + L
L5      return CONFORM
L6  return NONCONFORM
```

Line L1 does the work of the hole: the level falls by $r$ units per second, but it stops at zero. Line L3 is the overflow test. A packet that fails line L3 pours nothing, so it does not hurt the packets after it. The level counts fluid, not data: no packet waits in this bucket.

**Compared with the token bucket.** Write $x = b - X$. Line L1 becomes $x \leftarrow \min(b, x + r(t - last))$, line L3 becomes $x \ge L$, and line L4 becomes $x \leftarrow x - L$. These are the lines of the [token bucket](/token-bucket/). So the two are one algorithm: the meter counts the fluid in the bucket, and the token bucket counts the room that is left. The meter starts empty exactly when the token bucket starts full.

## Example

Let $r = 1000$ bytes per second and $b = 3000$ bytes. The column "level" is the value after line L1, and the last two columns are the level and the tokens $b - X$ after the decision.

| time (s) | size (bytes) | level after leak | decision | level after | tokens after |
|---|---|---|---|---|---|
| 0 | 1500 | 0 | pass | 1500 | 1500 |
| 0 | 1500 | 1500 | pass | 3000 | 0 |
| 0 | 500 | 3000 | reject | 3000 | 0 |
| 0.5 | 1000 | 2500 | reject | 2500 | 500 |
| 1 | 1500 | 2000 | reject | 2000 | 1000 |
| 1.5 | 1500 | 1500 | pass | 3000 | 0 |
| 2 | 500 | 2500 | pass | 3000 | 0 |
| 4 | 1500 | 1000 | pass | 2500 | 500 |
| 4 | 1500 | 2500 | reject | 2500 | 500 |
| 4 | 1500 | 2500 | reject | 2500 | 500 |

The first two packets fill the bucket. At time 0.5 the 1000-byte packet fails, because 500 bytes have leaked and $2500 + 1000 > 3000$. At time 2 a small packet fits where a large one would not. The passed packets in $[0, 2]$ add up to 5000 bytes, and $r \cdot 2 + b = 5000$: the bound is met with equality, and no more could pass.

## Correctness

The proof is in full below. Its key step is a closed form for the level after line L1 at packet $j$, with $A$ the set of passed packets:

$$X_j = \max\Big(0,\ \max_{i \in A,\ i < j}\big(\textstyle\sum_{k \in A,\ i \le k < j} L_k - r(t_j - t_i)\big)\Big).$$

It is the discrete form of the buffer content $\sup_{s \le t}\,(R(t) - R(s) - r(t - s))$ of Le Boudec and Thiran (Lemma 1.2.2). It holds by induction, and the rejected packets do not appear in it. From it:

- **Soundness.** For passed packets $i \le j$, the passed size from $i$ to $j$ is at most $r(t_j - t_i) + b$. So each interval of length $\tau$ gets at most $r\tau + b$ units.
- **Greedy.** A packet passes if and only if it, with the passed packets before it, still fits the curve.
- **Tightness.** If the whole input fits $(r, b)$, every packet passes.
- **Mirror.** At each packet the level is $b$ minus the tokens of a token bucket that started full, so the decisions agree packet for packet.

## Complexity

In the [word RAM](/word-ram/), with the level and the times held in words:

- **Time.** Each call runs lines L1 to L6 once: $\Theta(1)$ in the worst case, and $\Theta(n)$ for $n$ requests on one key.
- **Space.** Two numbers per key, $X$ and $last$. A key whose level has leaked to zero can be deleted, because a new bucket starts empty.

## Properties

- **Online and immediate.** Each decision uses only the past, and no packet waits.
- **Same output as the token bucket.** Any statement about the token bucket with $(r, b)$ holds for the meter with leak rate $r$ and size $b$.
- **Size matters.** A small packet can pass at a moment when a large one fails, as at time 2 in the example.
- **Work at arrivals only.** No timer runs between packets.

## Variants and improvements

- **[GCRA](/gcra/).** Its continuous-state leaky bucket form is this meter for fixed-size cells, with the level kept in units of time: each cell adds $T$, the level leaks one unit per unit of time, and the limit is $\tau + T$. Its other form stores one timestamp instead of the level.
- **Leaky bucket as a queue.** Put the packets themselves in the bucket and send them out at rate $r$. That is a shaper, not a meter: see [leaky bucket queue](/leaky-bucket-queue/) for how the two differ.
- **Markers.** Instead of dropping a nonconforming packet, mark it (for example, set the ATM cell loss priority bit or a lower DiffServ code point). See [traffic policing](/traffic-policing/) and the [single-rate three-color marker](/single-rate-three-color-marker/).
- **Counting attempts.** Some limiters pour on every request, even a rejected one, and cap the level at $b$. Then a client that keeps sending stays blocked. The output still fits $r\tau + b$, but the greedy property is lost.

## When to use it

Use the meter, or the token bucket, which is the same thing, when you want a long-term rate with a bounded burst and an answer at once. Choose the form that reads best in your system: the level form is natural when the limit is a "backlog" (bytes that a downstream link at rate $r$ would still have to send), and the token form when the limit is a "budget". If you must smooth the traffic and can delay it, use a shaper such as the [leaky bucket queue](/leaky-bucket-queue/).

## Pitfalls

- **Two meanings of "leaky bucket".** Some texts mean this meter, and some mean the [leaky bucket queue](/leaky-bucket-queue/). The meter passes bursts of up to $b$ at once; the queue never sends faster than $r$. Say which one you mean.
- **Update the time only on a pass.** If line L2 runs only after a pass, the next leak counts the same seconds twice. Run line L2 at each call.
- **Floor at zero.** Without the $\max(0, \cdot)$ of line L1, a long quiet period makes the level negative, and the client can then send a burst larger than $b$.
- **Integer levels.** With an integer level and a small $r$, the leak $r(t - last)$ rounds to 0 at each call, and a client that calls often is blocked for ever. Keep the level in small units or in fractions.
- **Clock going back.** A wall clock can jump back; use a monotonic clock, and treat a negative difference as 0.

## Implementations

The Python version keeps the level and the time as `int` or `Fraction`, so the tests check the arrival curve exactly. The tests compare the meter with a token bucket on random inputs (same decisions, and level equal to $b$ minus the tokens after each call), and check soundness, the greedy rule and tightness on every sequence of up to four packets of size 1 or 2 at integer times 0 to 4.

## History

Turner described the leaky bucket in 1986 as a way to bound the rate and the bursts of the traffic that a user sends into a packet network. The ATM standards of the ITU-T define the generic cell rate algorithm in two equivalent forms, and one of them, the continuous-state leaky bucket, is this meter in units of time. Le Boudec and Thiran define the leaky bucket controller as this meter and prove that it enforces the arrival curve $r\tau + b$.

## References
