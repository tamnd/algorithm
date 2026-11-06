---
tag: GZCF2N
kind: algorithm
slug: fermat-factorization
name: Fermat's factorization method
aliases:
- Fermat's method
- difference of squares factorization
area: number-theory/factorization
level: core
summary: Writes an odd N as x^2 - y^2 = (x - y)(x + y) by trying x = ceil(N^(1/2)), ceil(N^(1/2)) + 1, ... It is very fast when the two factors are close and Θ(N) in the worst case.
solves: [integer-factorization]
model: word-ram
complexity:
  vars: {N: the odd integer to factor, n: the number of binary digits of N, a: the largest divisor of N that is at most N^(1/2), b: the cofactor N/a}
  time: {worst: O(N), best: O(1)}
  space: {extra: O(1)}
  iterations: {worst: "O((b^(1/2) - a^(1/2))^2 + 1)"}
  bit_operations: {worst: O(N n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [divisibility, integer-square-root, trial-division]
see_also: [congruence-of-squares, lehman-factorization, hart-one-line-factorization, shanks-squfof, quadratic-sieve, knuth-schroeppel-multiplier, integer-factorization, rsa-cryptosystem]
sources:
  - book: isbn:9780387252827
    title: Richard Crandall and Carl Pomerance, Prime Numbers, A Computational Perspective, second edition, Springer, 2005
    locator: Section 5.1.1, Fermat method, pages 225 to 227 (Algorithm 5.1.1, the examples 8051 and 2581, the worst case n = 3p, residue filters and multipliers)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.5.4, Factoring into primes (Algorithm C, factoring by addition and subtraction, and the sieve tests for squares)
  - paper: "Carl Pomerance, A tale of two sieves, Notices of the American Mathematical Society 43(12), 1996"
    locator: pages 1473 to 1485 (the section on Fermat's method and Kraitchik's improvement)
  - url: https://en.wikipedia.org/wiki/Fermat%27s_factorization_method
    title: Fermat's factorization method, Wikipedia
    locator: the example N = 5959 and Fermat's factorization of 2027651281
---

Fermat's factorization method splits an odd integer $N$ by writing it as a difference of two squares, $N = x^2 - y^2 = (x - y)(x + y)$. It tries $x = \lceil \sqrt N \rceil, \lceil \sqrt N \rceil + 1, \dots$ until $x^2 - N$ is a perfect square $y^2$. When $N$ has two factors close to $\sqrt N$, the first trial value already succeeds, so the method is the standard check for badly chosen [RSA](/rsa-cryptosystem/) moduli. In the worst case, $N = 3p$, it takes about $N/6$ steps, much more than [trial division](/trial-division/).

## In plain words

Take an odd number. If it is the product of two numbers, it sits exactly in the middle between their average squared and their half difference squared. So look for a square that is larger than the number by another square.

Start at the smallest square that is not less than the number. Subtract the number. If the rest is a square, you are done: the two factors are the sum and the difference of the two square roots. If not, go to the next square and try again.

When the two factors are close to each other, the first or second try works, even for very large numbers. When one factor is small, you need a very long walk. Trial division finds small factors fast, so the two methods help each other.

## The problem

**Input.** An odd integer $N \ge 1$.

**Output.** A pair $(a, b)$ with $ab = N$ and $a \le b$, where $a$ is the largest divisor of $N$ that is at most $\sqrt N$. So $a = 1$ exactly when $N$ is $1$ or a [prime](/prime-number/), and otherwise $a$ is a nontrivial factor. Applied again to $a$ and $b$, the method gives the full [integer factorization](/integer-factorization/).

**Cost model.** On the [word RAM](/word-ram/), with $N < 2^w$, an addition, a multiplication and an [integer square root](/integer-square-root/) cost $O(1)$, and the time is the number of loop steps. For an arbitrary-precision $N$ with $n$ binary digits, one step is an addition of $O(n)$ bit operations plus a perfect-square test, which costs $O(n^2)$ bit operations with schoolbook arithmetic and Newton's method.

## The algorithm

$x$ is the trial value and $r = x^2 - N$ is kept up to date by an addition: $(x + 1)^2 - N = r + 2x + 1$.

```pseudo id=main
FERMAT(N)                                 ▷ N odd, N ≥ 1; returns (a, b) with ab = N, a the largest divisor ≤ √N
L1  x ← ⌈√N⌉
L2  r ← x² − N
L3  while r is not a perfect square do
L4      r ← r + 2x + 1, x ← x + 1
L5  y ← √r
L6  return (x − y, x + y)
```

Line L1 starts at the smallest $x$ with $x^2 \ge N$. Line L3 asks if $r$ is a perfect square. A fast program first looks at $r \bmod 64$: squares take only 12 of the 64 residues, so most $r$ are rejected with one table look-up, and only the rest need an integer square root. Line L4 moves to the next $x$ with one addition. Line L6 uses $N = x^2 - y^2 = (x - y)(x + y)$.

## Example

Factor $N = 5959$. Here $\sqrt{5959} \approx 77.2$, so line L1 sets $x = 78$.

| $x$ | $r = x^2 - N$ | square? |
|---|---|---|
| 78 | 125 | no |
| 79 | 282 | no |
| 80 | 441 | yes, $21^2$ |

Line L5 sets $y = 21$, and line L6 returns $(80 - 21, 80 + 21) = (59, 101)$. Indeed $59 \cdot 101 = 5959$, and both factors are prime. Crandall and Pomerance give a shorter example: for $N = 8051$ the first value $x = 90$ gives $r = 49 = 7^2$, so $8051 = 83 \cdot 97$.

## Correctness

Each factorization $N = uv$ with $1 \le u \le v$ gives a pair $x = (u + v)/2$, $y = (v - u)/2$ of integers (both $u$ and $v$ are odd) with $x^2 - y^2 = N$, and each such pair with $y \ge 0$ comes from one factorization. By the inequality of the means, $x \ge \sqrt N$, so the search starts low enough. The map $u \mapsto (u + N/u)/2$ decreases as $u$ grows up to $\sqrt N$, so the smallest $x$ that works belongs to the largest $u \le \sqrt N$. The invariant of line L3 is $r = x^2 - N$, and no smaller $x' \ge \lceil \sqrt N \rceil$ gives a square. The loop ends by $x = (N + 1)/2$ at the latest, from the factorization $N = 1 \cdot N$. The full proof is below.

## Complexity

**The exact count.** The loop ends at $x = (a + b)/2$, so the number of executions of line L4 is
$$\frac{a + b}{2} - \lceil \sqrt N \rceil \le \frac{a + b}{2} - \sqrt{ab} = \frac{(\sqrt b - \sqrt a)^2}{2}.$$

- **Best case.** If $b - a < 2\sqrt 2\, N^{1/4}$, then $(\sqrt b - \sqrt a)^2 = (b - a)^2 / (\sqrt b + \sqrt a)^2 \le (b - a)^2/(4\sqrt N) < 2$, so the count is $0$ and the first $x$ succeeds. The time is $O(1)$ on the word RAM. Factors that agree in their upper half of digits are found at once.
- **Worst case.** For $N = 3p$ with $p$ prime, $a = 3$ and the loop ends at $x = (p + 3)/2 = (N + 9)/6$, after about $N/6 - \sqrt N$ steps. For $N$ prime, $a = 1$ and the loop runs to $x = (N + 1)/2$. The time is $O(N)$ on the word RAM, which is worse than the $O(N^{1/2})$ of trial division.
- **Bit operations.** With $O(n^2)$ bit operations per step for an arbitrary-precision $N$, the worst case is $O(N n^2)$ bit operations.
- **Extra space** is $O(1)$ words, or $O(n)$ bits.

**After trial division.** If trial division first removes all prime factors up to $N^{1/3}$, then the rest is $1$, a prime, or a product $pq$ of two primes with $N^{1/3} < p \le q < N^{2/3}$. Then the count is at most $q/2 < N^{2/3}/2$, so the combined method takes $O(N^{2/3})$ steps. To prove that $N$ is prime, it is better to stop Fermat's method once $x$ passes this bound than to run it to $(N + 1)/2$.

## Properties

- **Deterministic and exact.** The output is a true factorization, and the first split it finds is the one with the two factors closest together.
- **A primality proof, at a high price.** For prime $N$ it returns $(1, N)$ after about $N/2$ steps.
- **Only odd numbers, or multiples of 4.** A number $N \equiv 2 \pmod 4$ is never a difference of two squares, because $x^2 - y^2 \bmod 4$ is $0$, $1$ or $3$. So remove the factors $2$ first.
- **Complementary to trial division.** Trial division is fast when one factor is small. Fermat's method is fast when the factors are close to $\sqrt N$.
- **Additions only in the loop.** Line L4 needs no multiplication, which made the method practical by hand and on early machines.

## Variants and improvements

- **Residue filters.** If $N \equiv 1 \pmod 4$, then $x$ must be odd; if $N \equiv 2 \pmod 3$, then $x$ must be a multiple of $3$ (Crandall and Pomerance). Tables of the squares modulo several small numbers, for example $64$, $63$, $65$ and $11$, exclude most $x$ before any square root, as in Knuth's sieve for Algorithm C.
- **Multipliers.** Apply the method to $kN$ for a small $k$ and take $\gcd(x - y, N)$. For $N = 2581 = 29 \cdot 89$ the plain method needs nine values of $x$, but $3N = 7743 = 87 \cdot 89$ succeeds at the first value $x = 88$. Lehman's method runs over all $k \le N^{1/3}$ and so factors any $N$ in $O(N^{1/3})$ steps; see [Lehman factorization](/lehman-factorization/). [Hart's one line factoring algorithm](/hart-one-line-factorization/) is a simpler heuristic form of the same idea.
- **Congruences instead of equations.** It is enough to find $x^2 \equiv y^2 \pmod N$ with $x \not\equiv \pm y$. This [congruence of squares](/congruence-of-squares/) idea, from Kraitchik, leads to [Dixon's method](/dixon-random-squares/) and the [quadratic sieve](/quadratic-sieve/), whose polynomial $x^2 - N$ is Fermat's.
- **[SQUFOF](/shanks-squfof/).** Shanks's square form factorization looks for squares in the continued fraction expansion of $\sqrt N$, where the values are of size $O(\sqrt N)$ instead of growing.

## When to use it

Use Fermat's method as a cheap test when the factors may be close, for example on an [RSA](/rsa-cryptosystem/) modulus made from two primes chosen near each other. A few hundred steps of the loop cost little and break such keys at once. As a general method, use it only after trial division to $N^{1/3}$, and then prefer [Lehman's method](/lehman-factorization/), [Pollard's rho](/pollard-rho/) or [SQUFOF](/shanks-squfof/), which have better bounds.

## Pitfalls

- **Even input.** For $N = 2 \cdot$ odd, no $x$ gives a square, and the loop never ends. Remove the factors $2$ first, or treat $N \equiv 2 \pmod 4$ separately.
- **A floating-point square root.** For $N > 2^{53}$, a double does not hold $\sqrt N$ or $\sqrt r$ exactly, so line L1 can start one too low and line L3 can miss a square. Use an exact [integer square root](/integer-square-root/) and check $y \cdot y = r$.
- **Overflow.** $x^2$ is about $N$, and $2x + 1$ is added each step. With $N$ close to $2^{64}$, keep $r$ and $x$ in a wider type.
- **Expecting a prime factor.** The output $a$ is the largest divisor at most $\sqrt N$, which need not be prime: for $N = 3 \cdot 5 \cdot 7 = 105$ the first $x$ is $11$, with $r = 16$, and the output is $(7, 15)$. Split both parts again.
- **Small factors.** Without trial division first, $N = 3p$ needs about $N/6$ steps. For $N = 3 \cdot (2^{61} - 1)$ this is more than $10^{18}$ steps.

## Implementations

## History

Pierre de Fermat described the method in a letter of about 1643, in which he factored $2027651281 = 44021 \cdot 46061$; the method needs 12 values of $x$ for this number. In the 1920s Maurice Kraitchik replaced the equation $x^2 - y^2 = N$ by the congruence $x^2 \equiv y^2 \pmod N$ and combined several values of $x^2 - N$ to make a square, which is the root of the modern sieve methods. R. Sherman Lehman made the method rigorous with multipliers in 1974.

## References
