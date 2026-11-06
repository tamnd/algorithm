---
tag: 44F174
kind: problem
slug: divisor-summatory-function
name: Divisor summatory function
aliases:
- Dirichlet divisor sum
- D(n) = sum of tau(k)
area: number-theory/divisibility-and-gcd
level: advanced
summary: Compute D(n) = sum of tau(k) for k from 1 to n, the sum of divisor counts.
prereqs: [divisor-function, harmonic-series, floor-division]
see_also: [dirichlet-hyperbola-method, dirichlets-divisor-problem, lattice-point-counting, divisor-count-sieve, divisor-function-up-to-n, counting-coprime-pairs, lucy-hedgehog-prime-counting, dirichlet-convolution]
sources:
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Chapter 18, Section 18.2, The average order of d(n) (Theorem 320 and the lattice-point proof)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 3, Section 3.5, The average order of d(n) (Theorem 3.3, Dirichlet's asymptotic formula)
  - paper: "Richard Sladkey, A successive approximation algorithm for computing the divisor summatory function, arXiv:1206.3369, 2012"
    locator: abstract (the claim of O(n^(1/3)) time and O(log n) space)
  - url: "https://oeis.org/A006218"
    locator: OEIS A006218, a(n) = Sum_{k=1..n} floor(n/k), also Sum_{k=1..n} d(k)
  - url: "https://oeis.org/A057494"
    locator: OEIS A057494, the values D(10^n)
---

The divisor summatory function is $D(n) = \sum_{k=1}^{n} d(k)$, where $d(k)$ is the number of positive divisors of $k$ (the [divisor function](/divisor-function/) $\tau$). The problem is to compute $D(n)$ for a given $n$, usually for $n$ far too large to list the divisors of every $k \le n$. Each pair $(a, b)$ of positive integers with $ab \le n$ is counted once, so $D(n) = \sum_{k \le n} \lfloor n/k \rfloor$, the number of lattice points under the hyperbola $xy = n$. This gives an $O(n)$ algorithm, the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) brings it to $O(n^{1/2})$, and a convex-hull method reaches $O(n^{1/3})$. Dirichlet's formula $D(n) = n \ln n + (2\gamma - 1)n + O(\sqrt n)$ describes its size, and the true order of the error is the open [Dirichlet divisor problem](/dirichlets-divisor-problem/).

## In plain words

Take every whole number from one up to some limit, count how many divisors each one has, and add up all those counts. That total is the divisor summatory function.

Counting divisors one number at a time is slow. There is a better way to see the total: every divisor of every number comes from a pair of whole numbers whose product stays within the limit. So the total is the number of such pairs. For each first number, the possible second numbers are easy to count with one division. Because the pairs are symmetric, only the first numbers up to the square root of the limit need to be visited, and the rest follows from the symmetry. Even faster methods trace the edge of the region with straight segments.

## Definition

**Input.** An integer $n \ge 0$.

**Output.** The integer

$$D(n) = \sum_{k=1}^{n} d(k), \qquad d(k) = \#\{ a \ge 1 : a \mid k \},$$

with $D(0) = 0$. For $n < 0$ the sum is empty and $D(n) = 0$ by convention.

**Equivalent forms.** Grouping the pairs $(a, b)$ with $ab = k \le n$ by $a$ instead of by $k$ gives

$$D(n) = \#\{ (a, b) \in \mathbb{Z}_{\ge 1}^2 : ab \le n \} = \sum_{a=1}^{n} \left\lfloor \frac{n}{a} \right\rfloor.$$

So $D(n)$ is the number of points with positive integer coordinates on or below the hyperbola $xy = n$. With $s = \lfloor \sqrt n \rfloor$, the region is symmetric in $x$ and $y$, and the points with $a \le s$ or $b \le s$ cover all of it, with the square $a, b \le s$ counted twice:

$$D(n) = 2 \sum_{a=1}^{s} \left\lfloor \frac{n}{a} \right\rfloor - s^2.$$

**Cost model.** For $n$ that fits in a machine word, each [floor division](/floor-division/) $\lfloor n/a \rfloor$ is one unit-cost operation on the word RAM, and $D(n) < n(\ln n + 1)$ fits in two words. For $n$ of $\beta$ binary digits in arbitrary precision, each division costs $O(\beta^2)$ with schoolbook arithmetic, which multiplies the bounds below.

## Variants

- **All prefix values.** Output $D(1), D(2), \ldots, D(n)$. Compute $d(k)$ for all $k \le n$ with a [divisor count sieve](/divisor-count-sieve/) or a linear sieve and take [prefix sums](/prefix-sums/); $\Theta(n)$ outputs force $\Omega(n)$ time.
- **Sum of divisors.** $\sum_{k \le n} \sigma(k) = \sum_{a \le n} a \lfloor n/a \rfloor$, and more generally $\sum_{k \le n} \sigma_t(k)$. The same hyperbola split works, with sums of powers over ranges of $a$.
- **Piltz divisor functions.** $D_m(n) = \sum_{k \le n} d_m(k)$, where $d_m(k)$ counts ordered factorizations $k = a_1 \cdots a_m$. $D_m(n)$ counts lattice points under $x_1 \cdots x_m \le n$; $D_3(n)$ can be computed in $O(n^{2/3})$ steps by the same symmetry.
- **Modular and interval versions.** $D(n) \bmod m$ for large $n$, or $D(n) - D(m)$, the divisor count of an interval.
- **General multiplicative weights.** $\sum_{ab \le n} f(a) g(b)$, the summatory function of a [Dirichlet convolution](/dirichlet-convolution/) $f * g$, given fast prefix sums of $f$ and $g$.

## Examples

The first values are

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $d(n)$ | 1 | 2 | 2 | 3 | 2 | 4 | 2 | 4 | 3 | 4 | 2 | 6 |
| $D(n)$ | 1 | 3 | 5 | 8 | 10 | 14 | 16 | 20 | 23 | 27 | 29 | 35 |

**$D(10)$ three ways.** By divisor counts, $1 + 2 + 2 + 3 + 2 + 4 + 2 + 4 + 3 + 4 = 27$. By the floor sum, $10 + 5 + 3 + 2 + 2 + 1 + 1 + 1 + 1 + 1 = 27$. By the hyperbola symmetry, $s = 3$ and $2(10 + 5 + 3) - 9 = 27$, using three divisions instead of ten.

**Large values and the error term.** Write $\Delta(n) = D(n) - n \ln n - (2\gamma - 1) n$, where $\gamma = 0.5772\ldots$ is the Euler-Mascheroni constant.

| $n$ | $D(n)$ | $\Delta(n)$ | $\Delta(n) / n^{1/4}$ |
|---|---|---|---|
| $10$ | 27 | 2.43 | 1.37 |
| $10^2$ | 482 | 6.04 | 1.91 |
| $10^3$ | 7069 | 6.81 | 1.21 |
| $10^4$ | 93668 | 20.28 | 2.03 |
| $10^6$ | 13970034 | 92.11 | 2.91 |
| $10^9$ | 20877697634 | 467.25 | 2.63 |
| $10^{12}$ | 27785452449086 | 3354.39 | 3.35 |
| $10^{14}$ | 3239062263181054 | 9083.47 | 2.87 |

The main term $n \ln n$ is already $3.2 \cdot 10^{15}$ at $n = 10^{14}$, while the error stays near $n^{1/4}$ in size, far below the elementary bound $\sqrt n = 10^7$.

## Known algorithms

| method | time | space | idea |
|---|---|---|---|
| divisor counts | $O(n \log n)$ | $O(n)$ | sieve $d(k)$ for all $k \le n$, then add |
| floor sum | $\Theta(n)$ | $O(1)$ | $\sum_{a \le n} \lfloor n/a \rfloor$ |
| [hyperbola method](/dirichlet-hyperbola-method/) | $\Theta(n^{1/2})$ | $O(1)$ | $2 \sum_{a \le s} \lfloor n/a \rfloor - s^2$ |
| convex-hull walk (Sladkey) | $O(n^{1/3})$ | $O(\log n)$ | follow the hyperbola with lattice segments |

**Sieve.** The loop "for $a \le n$, for each multiple $k$ of $a$, add one to $d(k)$" runs exactly $D(n)$ times, so it takes $\Theta(n \log n)$ steps, a direct instance of the [harmonic series](/harmonic-series/). It is the right choice when all prefix values are needed and $n$ fits in memory.

**Floor sum and block decomposition.** The value $\lfloor n/a \rfloor$ takes fewer than $2\sqrt n$ distinct values as $a$ runs from $1$ to $n$: for $a \le \sqrt n$ the $a$ are few, and for $a > \sqrt n$ the quotients are below $\sqrt n$. Grouping equal quotients, $\lfloor n/a \rfloor = q$ for $a$ from $\lfloor n/(q+1) \rfloor + 1$ to $\lfloor n/q \rfloor$, gives another $O(\sqrt n)$ algorithm, and the same grouping is the basis of [Lucy Hedgehog prime counting](/lucy-hedgehog-prime-counting/) and other prefix sums of multiplicative functions.

**Hyperbola method.** The symmetric formula above, with $s = \lfloor \sqrt n \rfloor$ computed by an integer square root. It costs $s$ divisions and is exact; see [Dirichlet hyperbola method](/dirichlet-hyperbola-method/).

**Convex-hull walk.** The points under the hyperbola between $x = n^{1/3}$ and $x = \sqrt n$ are counted by moving along the boundary in straight steps with rational slopes chosen by successive approximation, counting the lattice points under each segment with a closed formula. The boundary in that range has $O(n^{1/3})$ such segments, up to logarithmic factors in the analysis, and the remaining $x \le n^{1/3}$ are summed directly. Sladkey (2012) states the bound $O(n^{1/3})$ time and $O(\log n)$ space, with arithmetic on numbers of $O(\log n)$ binary digits.

## Bounds

**Size of the answer.** Dirichlet's theorem gives

$$D(n) = n \ln n + (2\gamma - 1) n + \Delta(n), \qquad \Delta(n) = O(\sqrt n).$$

*Proof sketch.* In the hyperbola formula, $\lfloor n/a \rfloor = n/a - \{n/a\}$, so $2 \sum_{a \le s} \lfloor n/a \rfloor = 2n H_s - O(s)$, where $H_s = \ln s + \gamma + O(1/s)$. With $s = \sqrt n - \theta$, $0 \le \theta < 1$, we get $2n \ln s = n \ln n + O(\sqrt n)$ and $s^2 = n + O(\sqrt n)$, which together give the formula. So $d(k)$ is $\ln k$ on average, although $d(k) = 2$ for every prime.

**Error term.** Voronoi (1903) improved the bound to $\Delta(n) = O(n^{1/3} \log n)$, Hardy (1916) proved that $\Delta(n) = O(n^{1/4})$ is false, and the true exponent between $1/4$ and $1/3$ is the open [Dirichlet divisor problem](/dirichlets-divisor-problem/).

**Algorithmic bounds.** The input has $\Theta(\log n)$ binary digits and the output $\Theta(\log n)$ as well, so the only known lower bound is the trivial $\Omega(\log n)$. The best published upper bound is $O(n^{1/3})$ up to logarithmic factors. No algorithm with time polynomial in $\log n$ is known, and it is open whether $D(n)$ can be computed in time $n^{o(1)}$.

## Reductions

- **Lattice points.** $D(n)$ is the number of lattice points in $\{x, y \ge 1, xy \le n\}$; this is the hyperbola case of [lattice point counting](/lattice-point-counting/) under a monotone curve.
- **From prefix sums of $1$.** Since $d = 1 * 1$ as a [Dirichlet convolution](/dirichlet-convolution/), $D(n) = \sum_{ab \le n} 1 \cdot 1$, and the general hyperbola identity $\sum_{ab \le n} f(a) g(b) = \sum_{a \le s} f(a) G(n/a) + \sum_{b \le s} g(b) F(n/b) - F(s) G(s)$ with $F, G$ the prefix sums reduces it to $O(\sqrt n)$ evaluations of $F(x) = G(x) = \lfloor x \rfloor$.
- **Factorization is not needed.** Unlike $d(n)$ for one $n$, which needs the factorization of $n$, the sum $D(n)$ needs no factoring at all.
- **To coprime pair counts.** Counting pairs $(a, b)$ with $ab \le n$ and $\gcd(a, b) = 1$ gives $\sum_{k \le n} 2^{\omega(k)}$, which [Möbius inversion](/mobius-inversion-formula/) reduces to $\sum_{m} \mu(m) D(n/m^2)$; compare [counting coprime pairs](/counting-coprime-pairs/).

## Applications

- **Running time of harmonic loops.** Any double loop over $a \le n$ and multiples of $a$ up to $n$, as in the divisor count sieve or [the divisor function up to n](/divisor-function-up-to-n/), does exactly $D(n) = n \ln n + O(n)$ inner steps.
- **Average order of $d(n)$.** $D(n)/n = \ln n + 2\gamma - 1 + O(n^{-1/2})$ is the classic first theorem of analytic number theory on average values.
- **Numerical study of the divisor problem.** Exact values of $D(n)$ for large $n$ give $\Delta(n)$ and test conjectures on its growth and distribution.
- **Prefix sums of multiplicative functions.** The hyperbola split and the block decomposition of $\lfloor n/a \rfloor$ are the building blocks of sublinear algorithms for sums of $\varphi$, $\mu$ and the [prime counting function](/prime-counting-function/).
- **Programming contests.** Sums such as $\sum_{k \le n} d(k)$ or $\sum_{k \le n} \lfloor n/k \rfloor \, k$ for $n$ up to $10^{12}$ or more are standard exercises for the $O(\sqrt n)$ technique.

## References
