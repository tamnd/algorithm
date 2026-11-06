---
tag: ZGK3CY
kind: algorithm
slug: pollard-rho
name: Pollard's rho algorithm
aliases:
- Pollard rho
- rho method
area: number-theory/factorization
level: core
summary: Iterates x -> x^2 + c mod N and uses Floyd's cycle finding to detect a collision modulo an unknown prime p | N, which gcd(x - y, N) reveals. Heuristically O(p^(1/2)) steps, so O(N^(1/4)).
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the integer to factor, n: the number of binary digits of N, p: the smallest prime factor of N}
  time: {worst: O(N), heuristic: O(p^(1/2))}
  space: {extra: O(1)}
  multiplications_mod_N: {heuristic: O(p^(1/2))}
  bit_operations: {heuristic: O(p^(1/2) n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [greatest-common-divisor, floyd-cycle-detection, birthday-paradox, functional-graph]
see_also: [brent-pollard-rho, pollard-rho-discrete-logarithm, pollard-rho-collision-search, brent-cycle-detection, pollard-p-minus-1, trial-division, miller-rabin, integer-factorization]
sources:
  - paper: "J. M. Pollard, A Monte Carlo method for factorization, BIT Numerical Mathematics 15(3), 1975"
    locator: pages 331 to 334
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.2.1, Pollard rho method for factoring, pages 229 to 231 (Algorithm 5.2.1, the delayed gcd, and the poor choices x^2 and x^2 - 2)
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 31.9, Integer factorization (procedure POLLARD-RHO and the example n = 1387)
  - paper: "Richard P. Brent and J. M. Pollard, Factorization of the eighth Fermat number, Mathematics of Computation 36(154), 1981"
    locator: pages 627 to 630
---

Pollard's rho algorithm finds a factor of a composite integer $N$ by iterating a simple map, $x \mapsto x^2 + c \bmod N$, until two values agree modulo an unknown [prime](/prime-number/) factor $p$ of $N$. Then $p$ divides their difference, and $\gcd(x - y, N)$ reveals it. If the map behaves like a random function, the [birthday paradox](/birthday-paradox/) gives such a pair after about $\sqrt p$ steps, and [Floyd's cycle detection](/floyd-cycle-detection/) finds one with $O(1)$ memory. So the method finds a factor of size $p$ in about $\sqrt p$ multiplications, which is the square root of the cost of [trial division](/trial-division/). This bound is a heuristic; it is not proved for any explicit map.

## In plain words

Pick a starting number and a rule that makes a new number from the old one: square it, add a constant, and take the remainder modulo $N$. Repeat.

Look at the same numbers modulo a secret prime factor $p$ of $N$. There are only $p$ possible remainders, so after a while the remainders repeat, and from then on they go round a cycle. The shape of the path, a tail that runs into a loop, looks like the Greek letter rho.

You cannot see the remainders modulo $p$, but you can test if two numbers have the same one: then their difference and $N$ have a common factor. Run one copy of the sequence at single speed and one at double speed. Once both are in the loop, the fast one catches the slow one, and the common factor appears.

## The problem

**Input.** An integer $N \ge 2$, a constant $c$, and a start value $s$ with $0 \le s < N$. In practice $N$ is odd and composite (a [Miller-Rabin](/miller-rabin/) test first rules out a prime $N$), and $c \notin \{0, -2\}$.

**Output.** A divisor $g > 1$ of $N$. The method succeeds when $g < N$. If $g = N$, it is run again with a new $c$. Applied in a loop to the factors, it gives the full [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/) with $N < 2^w$, one multiplication modulo $N$ and one gcd cost $O(1)$ (a gcd of word-size numbers takes $O(w)$ steps, which is a constant for fixed $w$). For an arbitrary-precision $N$ with $n$ binary digits, a multiplication modulo $N$ and a gcd each cost $O(n^2)$ bit operations with schoolbook arithmetic.

## The algorithm

Let $f(x) = (x^2 + c) \bmod N$. The slow value $x$ is $x_i = f^{(i)}(s)$ and the fast value $y$ is $x_{2i}$, after $i$ passes of the loop.

```pseudo id=main
POLLARD-RHO(N, c, s)                      ▷ N ≥ 2, 0 ≤ s < N; returns a divisor g > 1 of N (g = N is a failure)
L1  x ← s, y ← s, g ← 1
L2  while g = 1 do
L3      x ← f(x)
L4      y ← f(f(y))
L5      g ← gcd(|x − y|, N)
L6  return g
```

Line L3 moves the slow value one step and line L4 moves the fast value two steps, so after pass $i$ we have $x = x_i$ and $y = x_{2i}$. Line L5 asks if $x_i \equiv x_{2i}$ modulo some prime factor of $N$. Each pass costs three multiplications modulo $N$ and one gcd. A program can multiply the differences $|x - y|$ together modulo $N$ for about 100 passes and take one gcd of the product, which makes the gcd cost negligible.

## Example

Let $N = 8051$, $c = 1$ and $s = 2$.

| pass $i$ | $x = x_i$ | $y = x_{2i}$ | $\lvert x - y \rvert$ | $\gcd(\lvert x - y \rvert, 8051)$ |
|---|---|---|---|---|
| 1 | 5 | 26 | 21 | 1 |
| 2 | 26 | 7474 | 7448 | 1 |
| 3 | 677 | 871 | 194 | 97 |

The method returns $97$, and $8051 = 83 \cdot 97$. Modulo $97$ the sequence is $2, 5, 26, 95, 5, 26, 95, \dots$: a tail of length $1$ and a cycle of length $3$. The first $i \ge 1$ that is a multiple of $3$ is $i = 3$, and indeed $x_3 = 677 \equiv 95$ and $x_6 = 871 \equiv 95 \pmod{97}$. Modulo $83$ the values are $13$ and $41$, so the gcd is $97$ and not $N$. CLRS give a second example, $N = 1387 = 19 \cdot 73$ with $f(x) = x^2 - 1$, where the factor $19$ appears in the same way.

## Correctness

The output $g$ is a gcd with $N$, and the loop exits only when $g \ne 1$, so $g$ is a divisor of $N$ with $g > 1$. Now consider any modulus $m \mid N$, and the sequence $x_i \bmod m$. It is defined by $x_{i+1} \equiv x_i^2 + c \pmod m$, so it eventually repeats with a tail of length $\mu$ and a cycle of length $\lambda$, and $x_i \equiv x_{2i} \pmod m$ exactly when $i \ge \mu$ and $\lambda \mid i$. For $m = N$ this happens at some $i \le \mu + \lambda \le N$, where $\gcd(0, N) = N$, so the loop ends. If it happens for a prime $p \mid N$ at an earlier $i$ than for $N$, then $p \mid g$ and $g < N$. The full proof is below.

## Complexity

**The heuristic.** Let $p$ be the smallest prime factor of $N$. If $x \mapsto x^2 + c \bmod p$ were a random map on $p$ elements, then the expected number of distinct values before the first repeat is about $\sqrt{\pi p / 2} \approx 1.25 \sqrt p$ (the birthday paradox), and the tail $\mu$ and the cycle $\lambda$ each have expected length about $\sqrt{\pi p / 8}$. Floyd's method stops at the first multiple of $\lambda$ that is at least $\mu$, so at some $i \le \mu + \lambda$. This gives $O(\sqrt p)$ passes, and since $p \le \sqrt N$ for a composite $N$, $O(N^{1/4})$ passes.

- **Heuristic time.** $O(p^{1/2})$ on the word RAM, and $O(p^{1/2} n^2)$ bit operations for an arbitrary-precision $N$. To find the full factorization, the heuristic cost is $O(N^{1/4})$ multiplications modulo $N$ times $O(\log N)$ splits.
- **Proved bound.** The loop always stops within $\mu_N + \lambda_N \le N$ passes. For the maps $x^2 + c$, nothing much better is proved: the $O(\sqrt p)$ bound rests on the model of a random map, which these quadratic maps are not. Eric Bach proved a lower bound of order $k^2/p$ on the chance of success within $k$ steps, averaged over $c$ and $s$, for $k$ small compared to $\sqrt p$; this supports the heuristic but does not prove it.
- **Extra space.** $O(1)$ words, or $O(n)$ bits: only $x$, $y$ and $g$.

**In practice.** The cost does not depend on $N$ except through the cost of arithmetic modulo $N$. A 64-bit $N$ has $p < 2^{32}$, so rho needs at most about $2^{16}$ to $2^{17}$ passes, which is why it is the standard method for numbers of that size.

## Properties

- **Deterministic for fixed $c$ and $s$.** The randomness lies in the choice of $c$; for a fixed choice the output is fixed. The result, when $g < N$, is always a true factor, so the method never gives a wrong answer, only a slow one or a failure.
- **Not a prime factor in general.** The result $g$ is a product of the primes $p \mid N$ whose cycles closed at the same pass. It is usually prime, but a full factorization must test it and split it again.
- **Constant memory.** Only three numbers are stored, unlike the deterministic [Pollard-Strassen method](/pollard-strassen/), which needs about $N^{1/4}$ numbers in memory.
- **Finds small factors first.** The expected cost depends on the smallest prime factor, so a 20 digit factor of a 100 digit number takes about $10^{10}$ steps.
- **The same idea elsewhere.** The rho shape and the collision search serve also for [discrete logarithms](/pollard-rho-discrete-logarithm/) and for [collision search](/pollard-rho-collision-search/) in hash functions.

## Variants and improvements

- **[Brent's variant](/brent-pollard-rho/).** Replace Floyd's method by [Brent's cycle detection](/brent-cycle-detection/), which saves one of the three multiplications per step, and take the gcd of a product of about 100 differences. Brent reported about 24% fewer operations in practice.
- **Other maps.** Any polynomial map of degree at least 2 works. If all primes $p \mid N$ are known to be $1 \bmod k$, a map $x^k + c$ with $k \mid p - 1$ walks through a smaller set of values, and Crandall and Pomerance estimate the gain for $k = 2^{j}$ as a factor of about $\sqrt{k/2}$. Brent and Pollard used a map of the form $x^{2^{10}} + c$ to factor the Fermat number $F_8 = 2^{256} + 1$, whose prime factors are all $1 \bmod 2^{10}$.
- **Parallel rho.** Many machines run the method with different $c$; the speed-up is only about the square root of the number of machines. Methods with distinguished points, as in [collision search](/pollard-rho-collision-search/), do better for discrete logarithms but not for factoring, because the collision must be found modulo an unknown $p$.
- **The rho idea in other groups.** Pollard's rho for [discrete logarithms](/pollard-rho-discrete-logarithm/) and the [kangaroo method](/pollard-kangaroo/) use the same random walk and collision argument.

## When to use it

Use rho for $N$ up to about $10^{20}$, or more generally to find factors of up to about 20 digits. It is the usual method for 64-bit integers, after [trial division](/trial-division/) to a few hundred and a [Miller-Rabin](/miller-rabin/) test. For factors of 20 to 60 digits, the [elliptic curve method](/elliptic-curve-factorization/) is much faster. For a number made of two primes of the same size beyond about 30 digits each, use the [quadratic sieve](/quadratic-sieve/) or the [number field sieve](/general-number-field-sieve/).

## Pitfalls

- **A prime $N$.** For prime $N$ the loop runs until $x_i = x_{2i}$ modulo $N$ and returns $N$ after about $\sqrt N$ steps. Test primality first, or the program retries forever with new $c$.
- **Even $N$ or a prime power.** For $N = 4$ and $s = 2$, every $c$ fails. Remove the factors $2$ first, and give up and use trial division after many failures for small $N$.
- **Bad constants.** With $c = 0$, the sequence is $s^{2^i}$, whose cycle length is a multiplicative order, often large. With $c = -2$, the values $y + y^{-1}$ map to $y^2 + y^{-2}$, which has the same defect (Crandall and Pomerance). Use $c \notin \{0, -2\}$.
- **The gcd is $N$.** This means the cycles modulo all primes closed at the same pass. It is rare, but more likely with batched gcds. Go back to the last saved $x, y$ and take a gcd at each step, or change $c$.
- **Overflow in $x^2$.** For 64-bit $N$, the product $x \cdot x$ needs 128 bits. Use a 128-bit product or [Montgomery multiplication](/montgomery-multiplication/).
- **Expecting a prime output.** For $N = 3 \cdot 5 \cdot 7 \cdots$ the result can be a composite factor. Split again.

## Implementations

## History

John Pollard published the method in 1975 under the title "A Monte Carlo method for factorization". Richard Brent made it about a quarter faster in 1980 with a different cycle detection, and Brent and Pollard used a version with a map of degree $2^{10}$ to find the factor $1238926361552897$ of the Fermat number $F_8$, published in 1981. The same random walk idea gave Pollard's methods for discrete logarithms in 1978.

## References
