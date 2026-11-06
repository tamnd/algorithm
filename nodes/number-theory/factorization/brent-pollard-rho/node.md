---
tag: ES28TA
kind: algorithm
slug: brent-pollard-rho
name: Brent's variant of Pollard's rho
aliases:
- Brent's cycle-finding rho
area: number-theory/factorization
level: advanced
summary: Pollard's rho with Brent's cycle detection, which needs only one sequence, and with m differences multiplied before each gcd. Heuristically O(p^(1/2)) steps, about a quarter faster than Floyd's.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, p: the smallest prime factor of N, m: the number of differences per gcd}
  time: {worst: O(N), heuristic: O(p^(1/2))}
  space: {extra: O(1)}
  gcds: {heuristic: O(p^(1/2) / m + m)}
  bit_operations: {heuristic: O(p^(1/2) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [pollard-rho, brent-cycle-detection, greatest-common-divisor]
see_also: [floyd-cycle-detection, birthday-paradox, pollard-p-minus-1, elliptic-curve-factorization, montgomery-multiplication, integer-factorization]
sources:
  - paper: "Richard P. Brent, An improved Monte Carlo factorization algorithm, BIT Numerical Mathematics 20(2), 1980"
    locator: pages 176 to 184 (the cycle-finding method, the factorization algorithm with the product of m differences, and the comparison with Floyd's method)
  - paper: "Richard P. Brent and J. M. Pollard, Factorization of the eighth Fermat number, Mathematics of Computation 36(154), 1981"
    locator: pages 627 to 630
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.2.1, Pollard rho method for factoring, pages 229 to 231 (the delayed gcd, the backtrack when the gcd is n, and the remark on Brent's faster cycle finding)
---

Brent's variant of [Pollard's rho](/pollard-rho/) finds a factor of a composite $N$ with the same random walk $x \mapsto x^2 + c \bmod N$, but it detects the cycle modulo the unknown prime $p$ with [Brent's cycle detection](/brent-cycle-detection/) instead of [Floyd's](/floyd-cycle-detection/). It keeps one saved value $x$ and moves a single sequence $y$ forward, so each comparison costs one evaluation of the map instead of three. It also multiplies $m$ differences together modulo $N$ before it takes one gcd, and backtracks in the rare case that the product is $0 \bmod N$. Brent reported that this makes the method about 24% faster on average, and it is the form of rho used in practice.

## In plain words

Pollard's rho walks along a sequence of numbers and waits for two of them to agree modulo a hidden prime factor. Floyd's way runs a slow and a fast walker, so every step moves the sequence three times.

Brent's way uses one walker. It saves its position at index $0$, $2$, $6$, $14$, and so on, each saved point roughly twice as far as the last. After each save, it walks on and compares every new value with the saved one. Once the saved point is inside the loop and the walk past it is longer than the loop, the walker meets the saved value again.

Each comparison needs a gcd, which is slow. So multiply about a hundred differences together and take one gcd of the product. If that gcd is the whole number, go back and redo the last batch one step at a time.

## The problem

**Input.** An integer $N \ge 2$, a constant $c$, a start value $s$ with $0 \le s < N$, and a batch size $m \ge 1$. In practice $N$ is odd and composite, $c \notin \{0, -2\}$, and $m$ is about $100$.

**Output.** A divisor $g > 1$ of $N$. The method succeeds when $g < N$; for $g = N$ it is run again with a new $c$. This is a step of [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, a multiplication modulo $N$ and a gcd cost $O(1)$. For an arbitrary-precision $N$ with $n$ binary digits, each costs $O(n^2)$ bit operations with schoolbook arithmetic. The cost is counted in evaluations of $f(x) = (x^2 + c) \bmod N$, multiplications modulo $N$ and gcds.

## The algorithm

Write $x_0 = s$ and $x_{i+1} = f(x_i)$. The value $x$ is the saved point, $y$ walks along the sequence, $r$ is the length of the current block (a power of two), $q$ is the running product of the differences, and $y_s$ remembers $y$ at the start of the last batch.

```pseudo id=main
BRENT-RHO(N, c, s, m)                     ▷ N ≥ 2, 0 ≤ s < N, m ≥ 1; returns a divisor g > 1 of N (g = N is a failure)
L1  y ← s, r ← 1, q ← 1, g ← 1
L2  while g = 1 do
L3      x ← y; repeat r times: y ← f(y)
L4      k ← 0
L5      while k < r and g = 1 do
L6          y_s ← y
L7          repeat min(m, r − k) times: y ← f(y), q ← q · |x − y| mod N
L8          g ← gcd(q, N), k ← k + m
L9      r ← 2r
L10 if g = N then
L11     repeat y_s ← f(y_s), g ← gcd(|x − y_s|, N) until g > 1
L12 return g
```

In the block with length $r$, line L3 saves $x = x_{2r-2}$ and moves $y$ on to $x_{3r-2}$ without comparisons. Lines L5 to L8 compare $x$ with $x_j$ for $3r - 1 \le j \le 4r - 2$, so the differences of indices are $r + 1, \dots, 2r$. Line L8 takes one gcd per batch of $m$ comparisons. If the batch product is divisible by every prime of $N$, line L11 repeats the last batch with a gcd at each step.

## Example

Let $N = 8051 = 83 \cdot 97$, $c = 1$, $s = 2$ and $m = 1$. The sequence is $x_0, x_1, \dots = 2, 5, 26, 677, 7474, 2839, 871, \dots$

| block $r$ | saved $x$ | compared with | $\gcd(\lvert x - x_j \rvert, N)$ |
|---|---|---|---|
| 1 | $x_0 = 2$ | $x_2 = 26$ | 1 |
| 2 | $x_2 = 26$ | $x_5 = 2839$ | 97 |

The method returns $97$ after computing $x_1, \dots, x_5$: five evaluations of $f$ and two gcds. Modulo $97$ the sequence is $2, 5, 26, 95, 5, 26, 95, \dots$, with tail $\mu = 1$ and cycle $\lambda = 3$, and indeed $x_5 - x_2$ has index difference $3$. Floyd's version finds the same factor at its third pass, with nine evaluations of $f$ (see [Pollard's rho](/pollard-rho/)). With $m = 128$ the result is the same, because the first batches are shorter than $m$.

## Correctness

The returned $g$ is a gcd with $N$ and is greater than $1$, so it is a divisor of $N$ with $g > 1$. In the block of length $r$, the saved value is $x_{2r-2}$ and the comparisons use the index differences $r + 1, \dots, 2r$. Let $\mu$ and $\lambda$ be the tail and cycle lengths of the sequence modulo $N$. Once $r \ge \max(\lambda, \mu, 2)$, the saved index is at least $\mu$, and the $r$ consecutive differences contain a multiple of $\lambda$, so some factor of $q$ is $0 \bmod N$ and the outer loop ends. If the gcd of a batch is $N$, then the product before the batch was coprime to $N$, so one term of the batch has a gcd above $1$ with $N$, and line L11 finds it within $m$ steps. The full proof is below.

## Complexity

- **Per comparison.** Brent's version needs one evaluation of $f$ and one multiplication into $q$ per comparison, plus the $r$ evaluations of line L3 per block without comparisons. Floyd's version needs three evaluations of $f$ per comparison. With batching, the gcds cost one per $m$ comparisons.
- **Heuristic time.** If the map modulo $p$ behaves like a random map, the tail and cycle are $O(\sqrt p)$ long, the method stops in the first block with $r \ge \max(\lambda_p, \mu_p)$, and the index reached is less than $4r = O(\sqrt p)$. So the cost is $O(p^{1/2})$ evaluations on the word RAM and $O(p^{1/2} n^2)$ bit operations for an arbitrary-precision $N$, with $O(p^{1/2}/m + m)$ gcds (the term $m$ is the backtrack). For the full factorization this is $O(N^{1/4})$ per split. As for Pollard's rho, these bounds are heuristic; no proof is known for the maps $x^2 + c$.
- **Measured gain.** Brent found that the expected number of evaluations for the cycle detection is lower than for Floyd's method, and that the factoring algorithm as a whole is about 24% faster on average.
- **Proved bound.** The loop ends by the block with $r \ge \max(\lambda_N, \mu_N, 2)$, so after $O(N)$ evaluations.
- **Space.** $O(1)$ numbers: $x$, $y$, $y_s$, $q$, $g$.

## Properties

- **The same answer as rho, faster.** Both versions find a factor once the walk modulo $p$ closes its cycle. Brent's version detects it a little later in index, but with far fewer operations.
- **Deterministic for fixed $c$, $s$ and $m$.** The randomness is in the choice of $c$.
- **Batching is safe.** A product of differences is $0 \bmod p$ if and only if one of them is, so no factor is missed; only the case where all primes appear in one batch needs the backtrack.
- **One sequence.** No second copy of the walk is needed.

## Variants and improvements

- **No early comparisons.** Line L3 makes no comparisons for the first $r$ steps of each block, so it saves the multiplications into $q$ there; the index differences that remain, $r + 1$ to $2r$, still cover every cycle length up to $r$.
- **Montgomery arithmetic.** Use [Montgomery multiplication](/montgomery-multiplication/) for $f$ and for the product $q$, which removes the divisions.
- **Other maps.** As with Pollard's rho, maps $x^{k} + c$ help when the prime factors are known to be $1 \bmod k$. Brent and Pollard factored the Fermat number $F_8 = 2^{256} + 1$ this way, with a map of degree $2^{10}$, and found the factor $1238926361552897$.
- **Multiple walks.** Several values of $c$ can run side by side, and their differences can share one product and one gcd.

## When to use it

Use Brent's variant wherever Pollard's rho is the right method: for 64-bit integers after [trial division](/trial-division/) and a [Miller-Rabin](/miller-rabin/) test, and to find factors up to about 20 digits. For larger factors use the [elliptic curve method](/elliptic-curve-factorization/), which also runs a short [p - 1](/pollard-p-minus-1/) stage first.

## Pitfalls

- **Forgetting the backtrack.** Without lines L10 and L11, a batch that contains all prime factors returns $N$ and the method looks like a failure. With large $m$ on a small $N$ this is common.
- **Saving $y_s$ in the wrong place.** Line L6 must save $y$ at the start of each batch, not of each block, or the backtrack replays too much and can miss the batch with the factor.
- **A prime $N$.** The loop only ends when the walk modulo $N$ closes, after about $\sqrt N$ steps, and then returns $N$. Test primality first.
- **Overflow.** For $N$ near $2^{64}$, both $y^2$ and $q \cdot \lvert x - y \rvert$ need 128-bit products.

## Implementations

## History

Richard Brent published the method in 1980, with his cycle-finding algorithm and a comparison against Floyd's. In 1980 Brent and Pollard used it, with a high-degree map, to factor the eighth Fermat number $F_8$; the paper appeared in 1981. Brent's version, with batched gcds, became the standard rho in computer algebra systems and in the first stage of factoring programs.

## References
