---
tag: AW3RN4
kind: algorithm
slug: brent-cycle-detection
name: Brent's cycle detection algorithm
aliases:
- Brent's algorithm
- power-of-two cycle finding
area: data-structures/linear-structures
level: advanced
summary: Cycle detection using a teleporting pointer, typically fewer function evaluations than Floyd's.
solves: [floyd-cycle-detection]
prereqs: [floyd-cycle-detection]
see_also: [floyd-cycle-detection, brent-pollard-rho, pollard-rho, functional-graph, cycle-detection, linked-list, list-reversal, hash-table]
sources:
  - paper: "Richard P. Brent, An improved Monte Carlo factorization algorithm, BIT 20 (1980)"
    locator: Section 2 (the cycle-finding algorithm), its analysis, and the comparison with Floyd's method on random mappings
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 3.1, exercises 6 and 7 and their answers, on cycle finding with bounded memory; Section 4.5.4, Algorithm B (Pollard rho factorization with Brent's improvements)
  - paper: "Michael Beeler, R. William Gosper and Richard Schroeppel, HAKMEM, MIT Artificial Intelligence Laboratory Memo 239 (1972)"
    locator: item 132, Gosper's loop detector
---

Brent's algorithm finds the cycle of an eventually periodic sequence $x_0, x_1 = f(x_0), x_2 = f(x_1), \ldots$ with $O(1)$ memory, like Floyd's tortoise and hare, but with fewer evaluations of $f$. It keeps one saved value and one walking pointer. The pointer moves one step at a time and is compared with the saved value; after $1, 2, 4, 8, \ldots$ steps, the saved value jumps forward to the pointer's place. As soon as the saved value lies on the cycle and the power of two is at least the cycle length $\lambda$, the pointer returns to it after exactly $\lambda$ steps, so $\lambda$ is found directly. A second walk then finds the tail length $\mu$. Each step evaluates $f$ once, and Brent reported about 36% fewer evaluations than Floyd's method on random functions; his variant of [Pollard's rho](/brent-pollard-rho/) factoring is built on it.

## In plain words

You walk along a path that may end in a loop, and you want to know how long the loop is. You leave a marker where you stand and walk on, counting your steps. If you come back to the marker, the count is the length of the loop.

But the marker may be on the path before the loop, where you will never come back to it. So after 1 step, then 2 more, then 4 more, then 8 more, you pick the marker up and put it down where you are now, and you start counting again. Each new stretch is twice as long as the last one, so soon the marker is on the loop and the stretch is long enough to go all the way round. Then you meet the marker, and your count is the loop length.

## The problem

**Input.** A function $f : S \to S$ that can be evaluated, values that can be compared for equality, and a start value $x_0$. The sequence $x_{i+1} = f(x_i)$ is eventually periodic, which always holds when $S$ is finite.

**Output.** The tail length $\mu$, the least index whose value appears again, and the cycle length $\lambda$, the least $\lambda \ge 1$ with $x_{\mu + \lambda} = x_\mu$. This is the [cycle detection](/floyd-cycle-detection/) problem. Then $x_i = x_j$ for $i < j$ exactly when $i \ge \mu$ and $\lambda$ divides $j - i$.

## The algorithm

```pseudo id=main
BRENT(f, x₀)
L1  power ← 1, λ ← 1
L2  t ← x₀, h ← f(x₀)
L3  while t ≠ h
L4      if power = λ then
L5          t ← h, power ← 2 · power, λ ← 0
L6      h ← f(h), λ ← λ + 1
L7  t ← x₀, h ← x₀
L8  repeat λ times: h ← f(h)
L9  μ ← 0
L10 while t ≠ h: t ← f(t), h ← f(h), μ ← μ + 1
L11 return (λ, μ)
```

Lines L1 to L6 find $\lambda$. The saved value $t$ sits at $x_{2^k - 1}$ during round $k$, and $h$ walks through $x_{2^k}, \ldots, x_{2^{k+1} - 1}$, with $\lambda$ counting the steps from $t$. When a round of $2^k$ steps ends without a match, line L5 moves $t$ to $h$ and doubles the length of the next round.

Lines L7 to L10 find $\mu$. They start two pointers at $x_0$ and $x_\lambda$, a fixed distance $\lambda$ apart, and step them together. Two values at distance $\lambda$ are equal exactly when both are on the cycle, so the pointers first meet at $x_\mu$, after $\mu$ steps.

## Example

The list of the [cycle detection](/floyd-cycle-detection/) page: nodes $0, \ldots, 7$ with $i \to i + 1$ and $7 \to 3$, so $\mu = 3$ and $\lambda = 5$. Each row shows the state after line L6, and $i$ is the index of $h$.

| $i$ | $t$ | $h$ | power | $\lambda$ |
|---|---|---|---|---|
| 1 | 0 | 1 | 1 | 1 |
| 2 | 1 | 2 | 2 | 1 |
| 3 | 1 | 3 | 2 | 2 |
| 4 | 3 | 4 | 4 | 1 |
| 5 | 3 | 5 | 4 | 2 |
| 6 | 3 | 6 | 4 | 3 |
| 7 | 3 | 7 | 4 | 4 |
| 8 | 7 | 3 | 8 | 1 |
| 9 | 7 | 4 | 8 | 2 |
| 10 | 7 | 5 | 8 | 3 |
| 11 | 7 | 6 | 8 | 4 |
| 12 | 7 | 7 | 8 | 5 |

The saved value takes the values $x_0, x_1, x_3, x_7$. In round 3 it is node 7, on the cycle, and the pointer comes back to it after 5 steps, so $\lambda = 5$. The first row is the state after line L2. Then line L8 moves $h$ 5 steps from node 0 to node 5, and line L10 steps the pair $(0, 5) \to (1, 6) \to (2, 7) \to (3, 3)$, so $\mu = 3$. The run uses $12 + 5 + 6 = 23$ evaluations of $f$, against 26 for Floyd's method on the same list; for $\lambda$ alone, 12 against 15.

## Correctness

Round $k = 0, 1, 2, \ldots$ compares $x_{2^k - 1}$ with $x_{2^k - 1 + j}$ for $j = 1, \ldots, 2^k$. These are equal exactly when $2^k - 1 \ge \mu$ and $\lambda$ divides $j$. So no round stops while $2^k - 1 < \mu$ or $2^k < \lambda$, and the first round with $2^k \ge \max(\mu + 1, \lambda)$ stops at $j = \lambda$, the least positive multiple of $\lambda$. Line L3 then exits with the counter equal to $\lambda$. In the second part, $x_i = x_{i + \lambda}$ exactly when $i \ge \mu$, so line L10 stops after $\mu$ steps. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $2^K$ be the least power of two with $2^K \ge \max(\mu + 1, \lambda)$, so $2^K < 2\max(\mu + 1, \lambda)$.

| part | evaluations of $f$ | comparisons |
|---|---|---|
| lines L1 to L6, find $\lambda$ | $2^K - 1 + \lambda < 2\max(\mu + 1, \lambda) + \lambda$ | the same number |
| lines L7 to L10, find $\mu$ | $\lambda + 2\mu$ | $\mu + 1$ |
| total | less than $2\max(\mu + 1, \lambda) + 2\lambda + 2\mu \le 4(\mu + \lambda) + 2$ | |
| memory | 2 values and 3 counters | |

Floyd's method uses three evaluations per step of its first phase and needs up to about $3(\mu + \lambda)$ evaluations to find a point on the cycle, then $\lambda$ more for $\lambda$. Brent's first part uses one evaluation per step. For a random function on $N$ points, where $\mu$ and $\lambda$ are both about $0.63\sqrt{N}$, Brent found that his first part needs on average about 36% fewer evaluations than Floyd's.

## Properties

- **Constant memory.** Two values of $S$ and a few counters, as in Floyd's method.
- **Equality tests only.** No order on $S$ and no hashing is needed.
- **Finds $\lambda$ first.** When only the period is needed, as in testing a random number generator, lines L7 to L10 can be left out.
- **One evaluation per step.** The pointer $h$ is the only one that moves in the first part, so $f$ is evaluated once per comparison. Floyd's method evaluates $f$ three times per comparison.
- **Deterministic.** The same input always gives the same sequence of evaluations.

## Variants and improvements

- **[Brent-Pollard rho](/brent-pollard-rho/).** In [Pollard's rho](/pollard-rho/) factorization, the equality test becomes $\gcd(\lvert h - t \rvert, n) > 1$. Brent also multiplies many differences modulo $n$ and takes one gcd of the product, and leaves out some of the early comparisons in each round, which saves gcd computations.
- **Other growth factors.** Any factor $r > 1$ in place of 2 works. A larger factor wastes more evaluations after the cycle is entered, and a smaller one moves the saved value more often. Brent analysed the choice; the best factor for random functions is a little above 2, and 2 is close to it in cost.
- **Gosper's loop detector.** Keep about $\log_2 i$ saved values, the $x_j$ chosen by the binary expansion of the index, and compare each new value with all of them. It notices the cycle within a small constant of $\mu + \lambda$ steps, at the cost of $O(\log(\mu + \lambda))$ memory.
- **Stack algorithm.** Nivasch's method keeps a stack of values that increase from the bottom, and stops after at most $\mu + 2\lambda$ steps, using an order on $S$.
- **Distinguished points.** For very long cycles on many processors, save only values with a rare easy property in a shared table; a repeat of a saved value shows a cycle or a collision.

## When to use it

Use Brent's algorithm when $f$ is expensive and memory must stay constant: in Pollard's rho methods, when testing the period of a generator, or when iterating a map whose values are large numbers. If $f$ is cheap, as for a linked list, Floyd's method is as fast in practice and a little simpler to write correctly. If memory for $\mu + \lambda$ values is available and $S$ can be hashed, a [hash table](/hash-table/) of visited values finds the cycle with exactly $\mu + \lambda$ evaluations.

## Pitfalls

- **Resetting the counter in the wrong place.** Line L5 sets $\lambda$ to 0 and line L6 then adds 1, so the counter is the distance from $t$ to $h$. Setting it to 1 in line L5 makes $\lambda$ one too large.
- **Starting with $h = x_0$.** Then the first comparison is $x_0 = x_0$, and the loop stops at once with $\lambda = 1$. Line L2 must start $h$ one step ahead.
- **Using $\lambda$ from the first part as $\mu + \lambda$.** The counter measures only the distance between $t$ and $h$. The tail length needs the second part.
- **Linked lists with NIL.** For a list without a cycle, $f$ reaches NIL. Test $h = $ NIL in line L6 and stop with "no cycle"; evaluating $f(\text{NIL})$ fails.
- **Overflow of the power.** With fixed-width counters, `power` doubles; for cycles longer than half the counter range, it overflows. Use a 64-bit counter.

## Implementations

## History

Brent published the algorithm in 1980, as the cycle-finding part of his improvement of Pollard's rho method of factorization. Pollard's 1975 method had used Floyd's two-pointer method, which Knuth credits to Floyd in the exercises of Section 3.1. Gosper's loop detector, in the HAKMEM memo of 1972, is an earlier method that also saves values at power-of-two positions, but it keeps a logarithmic number of them. Brent and Pollard used the improved method in 1981 to factor the eighth Fermat number.

## References
