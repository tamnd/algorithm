---
tag: 5WH9D0
kind: algorithm
slug: gcra
name: Generic cell rate algorithm
aliases:
- GCRA
- virtual scheduling algorithm
area: systems/rate-limiting
level: advanced
summary: Tracks a theoretical arrival time per flow; equivalent to the leaky bucket meter, stored as one timestamp (ITU-T I.371).
solves: [rate-limiting-problem]
model: word-ram
complexity:
  vars: {n: the number of cells on one connection}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [token-bucket, leaky-bucket-meter]
see_also: [token-bucket, leaky-bucket-meter, burst-tolerance, traffic-policing, traffic-shaping, rate-limiter, leaky-bucket-queue]
sources:
  - url: "https://www.itu.int/rec/T-REC-I.371"
    title: ITU-T Recommendation I.371, Traffic control and congestion control in B-ISDN, 2004
    locator: Annex A, the generic cell rate algorithm, its virtual scheduling form and its continuous-state leaky bucket form
  - book: isbn:9783540421849
    title: Jean-Yves Le Boudec and Patrick Thiran, Network Calculus, A Theory of Deterministic Queuing Systems for the Internet, Springer LNCS 2050, 2001
    locator: Section 1.2.2, Definition 1.2.3 (GCRA(T, tau)), Table 1.1 (examples for GCRA(10, 2)), Proposition 1.2.4 (GCRA and stair arrival curves) and Corollary 1.2.1 (equivalence with the leaky bucket, b = (tau/T + 1) delta and r = delta/T)
  - paper: ATM Forum, Traffic Management Specification Version 4.0, af-tm-0056.000, 1996
    locator: the GCRA in the traffic contract, with the peak cell rate, the sustainable cell rate, the cell delay variation tolerance and the burst tolerance
---

The generic cell rate algorithm, GCRA$(T, \tau)$, is the conformance test of ATM networks. It keeps one timestamp per connection, the *theoretical arrival time* $tat$, which is the time at which the next cell would be due if the cells came exactly every $T$ seconds. A cell that comes more than $\tau$ before $tat$ is nonconforming; any other cell conforms and moves $tat$ forward by $T$. GCRA$(T, \tau)$ makes the same decisions as a [token bucket](/token-bucket/), or a [leaky bucket meter](/leaky-bucket-meter/), with rate $1/T$ and depth $1 + \tau/T$ cells. It is also a popular way to write a [rate limiter](/rate-limiter/) for web APIs, because the state is one number that needs no refill arithmetic.

## In plain words

Picture a train timetable for a client. If the client is allowed one request each second, the timetable says when its next request is due. When a request comes on time or late, it is fine, and the next due time is one second after the later of the old due time and now. A request that comes early is also fine if it is only a little early. A request that is too early is refused, and the timetable does not change.

How early "a little early" may be sets the burst size. If a request may be up to five seconds early, a quiet client can send six requests at once, and then one per second. The limiter stores only the due time of the next request.

## The problem

The input is a sequence of cells (or requests) at times $t_1 \le t_2 \le \cdots$. A connection has an *emission interval* $T > 0$, the inverse of its rate, and a *tolerance* $\tau \ge 0$, both in units of time. The test decides each cell at its arrival. It must pass a cell if and only if the passed cells, with it, still fit the $(r, b)$ arrival curve of the [rate limiting problem](/rate-limiting-problem/) with $r = 1/T$ and $b = 1 + \tau/T$ cells. The arrival model is adversarial. In ATM, $\tau$ is the cell delay variation tolerance when $T$ is the peak cell interval, and the [burst tolerance](/burst-tolerance/) when $T$ is the sustainable cell interval.

## The algorithm

The *virtual scheduling* form keeps $tat$, which starts at the time of the first cell (or at $-\infty$).

```pseudo id=main
GCRA(G, t)                           ▷ a cell arrives at time t
L1  if t < G.tat − τ then return NONCONFORM   ▷ too early: tat does not change
L2  G.tat ← max(t, G.tat) + T
L3  return CONFORM
```

The *continuous-state leaky bucket* form keeps a level $X$, in units of time, and the last conformance time $lct$. The level starts at 0.

```pseudo id=leaky
GCRA-LEAKY-BUCKET(G, t)              ▷ the same test, written as a leaky bucket meter
L4  X′ ← max(0, G.X − (t − G.lct))           ▷ the bucket leaks one unit per unit of time
L5  if X′ > τ then return NONCONFORM
L6  G.X ← X′ + T, G.lct ← t                  ▷ each conforming cell pours T units
L7  return CONFORM
```

The two forms agree because $X + lct = tat$ after each conforming cell. The second form is a [leaky bucket meter](/leaky-bucket-meter/) in which each cell pours $T$ and the bucket holds $\tau + T$. In both forms a nonconforming cell changes nothing.

**Requests of many units.** A rate limiter often asks for $n$ units at once. Then the test is: let $tat' = \max(t, tat) + nT$; pass if $tat' - t \le \tau + T$, and then set $tat \leftarrow tat'$. For $n = 1$ this is line L1. A refused request can retry at time $tat + (n - 1)T - \tau$, which is the value to put in an HTTP `Retry-After` header.

## Example

Take GCRA$(10, 2)$, the first example of Le Boudec and Thiran (Table 1.1), with four more cells. The equivalent token bucket has $r = 1/10$ and $b = 1.2$ cells. The column "tokens" is $b - \max(0, tat - t)/T$, the tokens of that bucket at the arrival, and $X'$ is the level of line L4.

| arrival $t$ | $tat$ before | $X'$ | tokens | result | $tat$ after |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 1.2 | conform | 10 |
| 10 | 10 | 0 | 1.2 | conform | 20 |
| 18 | 20 | 2 | 1 | conform | 30 |
| 28 | 30 | 2 | 1 | conform | 40 |
| 38 | 40 | 2 | 1 | conform | 50 |
| 48 | 50 | 2 | 1 | conform | 60 |
| 57 | 60 | 3 | 0.9 | nonconform | 60 |
| 60 | 60 | 0 | 1.2 | conform | 70 |
| 61 | 70 | 9 | 0.3 | nonconform | 70 |

The cells from 18 to 48 are each 2 time units early, which $\tau = 2$ allows. They cannot add up: the cell at 57 would be 3 units early, so it fails, though it is 9 units after the cell before it. In each row a cell conforms exactly when $X' \le 2$, and exactly when the token bucket holds at least one token.

## Correctness

The full proof is below. Write $D = \max(0, tat - t)$ at an arrival. By induction on the cells, the token bucket with $r = 1/T$ and $b = 1 + \tau/T$, full at the start, holds

$$x = b - \frac{D}{T}$$

tokens at each arrival. The token test $x \ge 1$ is then $D \le \tau$, which is the test of line L1, and the update of line L2 takes one token. The same algebra covers requests of $n$ units. So the GCRA inherits the three properties proved for the [token bucket](/token-bucket/):

- **Soundness.** The conforming cells fit the arrival curve $\tau'/T + 1 + \tau/T$. In the form of Le Boudec and Thiran (Proposition 1.2.4): if two conforming cells are $k$ conforming cells apart, their times differ by at least $kT - \tau$.
- **Greedy.** A cell fails only if passing it would break that bound.
- **Tightness.** If the whole input fits the bound, every cell conforms.

For cells of $\delta$ data units this is Corollary 1.2.1 of Le Boudec and Thiran: GCRA$(T, \tau)$ is the leaky bucket with $r = \delta/T$ and $b = (\tau/T + 1)\delta$.

## Complexity

In the [word RAM](/word-ram/), with times in words:

- **Time.** One comparison and one update per cell: $\Theta(1)$ in the worst case, $\Theta(n)$ for $n$ cells.
- **Space.** One timestamp per connection in the virtual scheduling form, two numbers in the leaky bucket form. A key with $tat \le t$ is in the same state as a new key, so a key-value store can let it expire at time $tat$.

## Properties

- **Online and immediate.** It is a policer: it decides at once and holds no cell.
- **Integer friendly.** With times in integer ticks and $T$ an integer number of ticks, every value is an integer. No fractional tokens appear, and no refill is computed.
- **Largest burst.** A quiet connection can send $\lfloor \tau/T \rfloor + 1$ cells at the same instant. At a peak spacing $T_p < T$ it can send $1 + \lfloor \tau/(T - T_p) \rfloor$ cells, the ATM maximum burst size; see [burst tolerance](/burst-tolerance/).
- **No trace of failures.** A nonconforming cell changes no state.

## Variants and improvements

- **Dual GCRA.** The ATM variable bit rate service checks each cell against two GCRAs: GCRA$(T_p, \tau_p)$ for the peak cell rate and GCRA$(T_s, \tau_s)$ for the sustainable cell rate.
- **Cell tagging.** A nonconforming cell can be passed with its cell loss priority bit set, so that it is dropped first later on. See [traffic policing](/traffic-policing/).
- **Shaping.** A sender can delay each cell until $tat - \tau$, so that all its cells conform. This turns the test into a shaper; see [traffic shaping](/traffic-shaping/).
- **Variable sizes.** The test for $n$ units above handles packets of any size, with $T$ the time per unit of data.

## When to use it

Use the GCRA when you want token bucket behavior with the smallest possible state, or when your store holds one timestamp per key more easily than two numbers. It suits a key-value store with expiring keys, since the key can expire when the bucket would be full again. Use the [token bucket](/token-bucket/) form when you need to show users a token count. Use a [sliding window log](/sliding-window-log/) if the rule must be "at most $n$ in any window" with no refill inside the window.

## Pitfalls

- **Reject test on the wrong side.** The test is $t < tat - \tau$, with $tat$ before the update. Testing the updated value, $\max(t, tat) + T$, against $t + \tau$ rejects every burst one cell too early. The test for $n$ units compares $tat' - t$ with $\tau + T$, not with $\tau$.
- **Updating on a reject.** If line L2 runs for a nonconforming cell, a client that keeps sending pushes $tat$ forward for ever and is never served. Change $tat$ only on a pass, unless you want rejected requests to count.
- **Starting $tat$ in the past.** A $tat$ of 0 with times from a Unix clock is fine, because $\max(t, tat)$ resets it. A $tat$ far in the future, from a clock that jumped, blocks the key until the clock catches up.
- **Confusing $\tau$ and $b$.** The tolerance $\tau$ is a time; the burst $b = 1 + \tau/T$ is a number of cells. With $\tau = 0$ the GCRA still passes one cell at a time, at spacing $T$.

## Implementations

The Python version has both forms and the test for $n$ units, with times as `int` or `Fraction`. The tests reproduce the table above, check that the two forms agree and that $X + lct = tat$ after every cell, check that the decisions equal those of a token bucket with $r = 1/T$ and $b = 1 + \tau/T$ on random inputs (cells and requests of 1 to 4 units), check the retry time, and check the bound $t_{m+k} \ge t_m + kT - \tau$ on the output.

## History

The GCRA comes from the ATM standards of the 1990s, the ITU-T Recommendation I.371 and the ATM Forum traffic management specification, which define conformance of a cell stream to a traffic contract by the GCRA. Recommendation I.371 gives it in the virtual scheduling form and in the continuous-state leaky bucket form, as two equivalent ways to state one test. Le Boudec and Thiran prove that the GCRA and the leaky bucket controller give the same constraint for cells of a fixed size.

## References
