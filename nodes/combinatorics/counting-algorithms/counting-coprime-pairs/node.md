---
tag: H3W1XV
kind: problem
slug: counting-coprime-pairs
name: Counting coprime pairs
aliases:
- Number of coprime pairs
- counting pairs with gcd one
- visible lattice points counting
area: combinatorics/counting-algorithms
level: core
summary: Counting pairs of integers in a range with gcd equal to one, using inclusion-exclusion over squarefree divisors.
model: word-ram
complexity:
  vars: {N: the upper end of the range}
  time: {worst: "O(N^(2/3))"}
prereqs: [mobius-inversion, euler-totient]
see_also: [mobius-inversion, mobius-function, euler-totient, totient-values-up-to-n, mobius-sieve, farey-sequence, coprime-integers, inclusion-exclusion-principle]
sources:
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory, Springer, 1976
    locator: Chapter 3, Averages of Arithmetical Functions (Section 3.7, The average order of φ(n), and Section 3.8, lattice points visible from the origin)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition, Oxford University Press, 2008
    locator: Chapter XVIII, The Order of Magnitude of Arithmetical Functions (Section 18.5, the average order of φ(n))
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.9, Phi and Mu (the sum Φ(x) of φ(k) and its recurrence)
---

Counting coprime pairs asks for the number $Q(N)$ of ordered pairs $(a, b)$ with $1 \le a, b \le N$ and $\gcd(a, b) = 1$. [Möbius inversion](/mobius-inversion/) gives $Q(N) = \sum_{d \le N} \mu(d) \lfloor N/d \rfloor^2$, which a sieve evaluates in $O(N)$ time, and grouping equal values of $\lfloor N/d \rfloor$ brings the time below $N$. The answer is about $\frac{6}{\pi^2}N^2$, so two random integers are coprime with probability close to $6/\pi^2 \approx 0.6079$.

## In plain words

Take all pairs of whole numbers from 1 to N and ask how many pairs have no common factor larger than one. Checking every pair is slow when N is large.

A faster way counts the opposite. Pairs where both numbers are even are easy to count, and so are pairs where both are multiples of 3. Take these away from the total. Pairs where both are multiples of 6 were taken away twice, so add them back. Continue over all numbers built from different primes. The sign for each number comes from a fixed rule, and many terms share the same size, so the sum is short.

A second way counts, for each number, the smaller numbers that share no factor with it, and adds these counts.

## Definition

Notation: $[N] = \{1, \ldots, N\}$, $\gcd$ is the [greatest common divisor](/greatest-common-divisor/), $\mu$ is the [Möbius function](/mobius-function/) ($\mu(1) = 1$, $\mu(d) = (-1)^r$ if $d$ is a product of $r$ distinct primes, and $\mu(d) = 0$ if a square larger than 1 divides $d$), and $\varphi$ is [Euler's totient](/euler-totient/).

**Input.** An integer $N \ge 1$.

**Output.** $Q(N) = \bigl|\{(a, b) \in [N]^2 : \gcd(a, b) = 1\}\bigr|$.

**Cost model.** $Q(N) \le N^2$, so the answer has at most $2\log_2 N + 1$ bits, which fits in two machine words when $N$ fits in one. Each arithmetic operation on numbers of $O(\log N)$ bits costs $O(1)$ on the [word RAM](/word-ram/), and the time bounds count these operations. Space counts words.

**Theorem.** For $N \ge 1$,
$$Q(N) = \sum_{d=1}^{N} \mu(d) \Bigl\lfloor \frac{N}{d} \Bigr\rfloor^2 = 2\sum_{n=1}^{N} \varphi(n) - 1.$$

*Proof of the first form.* For $d \ge 1$, the pairs in $[N]^2$ with $d \mid a$ and $d \mid b$ number $\lfloor N/d \rfloor^2$. The basic identity of the Möbius function is $\sum_{d \mid m} \mu(d) = [m = 1]$. So
$$Q(N) = \sum_{a, b \le N} \bigl[\gcd(a, b) = 1\bigr] = \sum_{a, b \le N} \sum_{d \mid \gcd(a, b)} \mu(d) = \sum_{d \le N} \mu(d) \cdot \bigl|\{(a, b) : d \mid a,\ d \mid b\}\bigr|,$$
which is the formula. It is [inclusion-exclusion](/inclusion-exclusion-principle/) over the events "$p$ divides both", one event per prime $p \le N$: the terms with $\mu(d) = 0$ are the ones that no set of distinct primes produces. $\square$

*Proof of the second form.* Split the pairs into $a < b$, $a = b$ and $a > b$. The only coprime pair with $a = b$ is $(1, 1)$. For fixed $b \ge 2$, the pairs $(a, b)$ with $a < b$ and $\gcd(a, b) = 1$ number $\varphi(b)$, and for $b = 1$ there are none, while $\varphi(1) = 1$. So the pairs with $a < b$ number $\sum_{n \le N} \varphi(n) - 1$, by symmetry so do the pairs with $a > b$, and $Q(N) = 2\bigl(\sum_{n \le N}\varphi(n) - 1\bigr) + 1$. $\square$

## Variants

- **Unordered pairs.** The pairs $a < b \le N$ with $\gcd(a, b) = 1$ number $(Q(N) - 1)/2 = \sum_{n=2}^{N} \varphi(n)$.
- **Rectangle.** For $(a, b) \in [N] \times [M]$, the same proof gives $\sum_{d \le \min(N, M)} \mu(d)\lfloor N/d \rfloor\lfloor M/d \rfloor$.
- **Range.** For $L \le a, b \le R$, let $f(x, y)$ be the rectangle count, with $f = 0$ if $x = 0$ or $y = 0$. Then the count is $f(R, R) - 2f(L - 1, R) + f(L - 1, L - 1)$, by inclusion-exclusion on the two lower limits.
- **A fixed gcd.** The pairs in $[N]^2$ with $\gcd(a, b) = g$ are $(ga', gb')$ with $\gcd(a', b') = 1$ and $a', b' \le \lfloor N/g \rfloor$, so they number $Q(\lfloor N/g \rfloor)$.
- **Pairs from a list.** Given integers $x_1, \ldots, x_n \le V$, the pairs $i < j$ with $\gcd(x_i, x_j) = 1$ number $\sum_{d \le V} \mu(d)\binom{c_d}{2}$, where $c_d$ is the number of $x_i$ divisible by $d$. The counts $c_d$ for all $d$ cost $O(V \log V)$ by a harmonic loop over multiples.
- **More coordinates.** The $k$-tuples in $[N]^k$ with gcd 1 number $\sum_d \mu(d)\lfloor N/d \rfloor^k$.
- **Gcd sums.** $\sum_{a, b \le N} \gcd(a, b) = \sum_{d \le N} \varphi(d)\lfloor N/d \rfloor^2$, by $g = \sum_{d \mid g} \varphi(d)$; see [the totient divisor sum](/totient-divisor-sum/).

## Examples

**1. $N = 10$ by the Möbius sum.** The nonzero terms are:

| $d$ | 1 | 2 | 3 | 5 | 6 | 7 | 10 |
|---|---|---|---|---|---|---|---|
| $\mu(d)$ | $1$ | $-1$ | $-1$ | $-1$ | $1$ | $-1$ | $1$ |
| $\lfloor 10/d \rfloor^2$ | 100 | 25 | 9 | 4 | 1 | 1 | 1 |

The terms for $d = 4, 8, 9$ are $0$. The sum is $100 - 25 - 9 - 4 + 1 - 1 + 1 = 63$.

**2. $N = 10$ by the totient sum.** $\varphi(1), \ldots, \varphi(10)$ are $1, 1, 2, 2, 4, 2, 6, 4, 6, 4$, with sum $32$, so $Q(10) = 2 \cdot 32 - 1 = 63$. There are $31$ unordered coprime pairs $a < b \le 10$, and the [Farey sequence](/farey-sequence/) of order 10 has $1 + 32 = 33$ terms.

**3. Small values and the density.** $Q(N)$ for $N = 1, \ldots, 5$ is $1, 3, 7, 11, 19$. Further values are $Q(100) = 6087$, $Q(1000) = 608383$ and $Q(10^6) = 607927104783$, a number of 40 bits. The ratio $Q(10^6)/10^{12} = 0.6079271047\ldots$ agrees with $6/\pi^2 = 0.6079271018\ldots$ to eight decimal places.

**4. Rectangle and range.** For $[10] \times [6]$ the count is $38$. For $5 \le a, b \le 15$ it is $72$, both by the formulas of the variants and by a direct check.

**5. A list.** For the list $2, 3, 4, 5, 6, 9$, nine of the fifteen pairs are coprime. The formula gives $\binom{6}{2} - \binom{3}{2} - \binom{3}{2} - \binom{1}{2} + \binom{1}{2} = 15 - 3 - 3 - 0 + 0 = 9$, with $c_1 = 6$, $c_2 = 3$ ($2, 4, 6$), $c_3 = 3$ ($3, 6, 9$), $c_5 = 1$ and $c_6 = 1$.

**6. A fixed gcd.** In $[100]^2$, the pairs with gcd $1, 2, 3, 5$ number $6087$, $1547 = Q(50)$, $687 = Q(33)$ and $255 = Q(20)$.

## Known algorithms

| method | time | space | idea |
|---|---|---|---|
| all pairs | $O(N^2 \log N)$ | $O(1)$ | one [gcd](/gcd-of-two-integers/) per pair |
| totient sieve | $O(N \log\log N)$ | $O(N)$ | $\varphi(1..N)$, then $2\sum\varphi - 1$ |
| Möbius sieve | $O(N)$ | $O(N)$ | [linear sieve](/linear-sieve/) for $\mu$, then the sum |
| grouped sum | $O(\sqrt N)$ terms | $O(\sqrt N)$ | needs the Mertens values $M(N/v)$ |
| sublinear | $O(N^{2/3})$ | $O(N^{2/3})$ | sieve to $N^{2/3}$, recursion above it |

**Sieves.** [Computing the totients up to $N$](/totient-values-up-to-n/) takes $O(N \log\log N)$ with the sieve of Eratosthenes, or $O(N)$ with a linear sieve, which also gives $\mu$; see the [Möbius sieve](/mobius-sieve/). Either sum then costs $O(N)$.

**Grouping.** The value $v = \lfloor N/d \rfloor$ takes fewer than $2\sqrt N$ distinct values as $d$ runs over $[N]$: for $d \le \sqrt N$ there are at most $\sqrt N$ values of $d$, and for $d > \sqrt N$ the value $v$ is less than $\sqrt N$. For $N = 10^6$ there are $1999$ values. The $d$ with $\lfloor N/d \rfloor = v$ form one interval $[d_0, d_1]$ with $d_1 = \lfloor N/v \rfloor$, so
$$Q(N) = \sum_{\text{intervals}} \bigl(M(d_1) - M(d_0 - 1)\bigr)\,v^2, \qquad M(x) = \sum_{d \le x} \mu(d).$$

**Sublinear time.** The Mertens function satisfies $\sum_{d \le x} M(\lfloor x/d \rfloor) = 1$ for $x \ge 1$, from $\sum_{d \mid m}\mu(d) = [m = 1]$. So $M(x) = 1 - \sum_{d = 2}^{x} M(\lfloor x/d \rfloor)$, and with the same grouping this costs $O(\sqrt x)$ given the smaller values. Only the values $M(\lfloor N/v \rfloor)$ are needed, since $\lfloor\lfloor N/a \rfloor/b\rfloor = \lfloor N/(ab) \rfloor$. Sieving $\mu$ up to $N^{2/3}$ and using the recursion with memoization above it gives $O(N^{2/3})$ time. The same scheme works for $\Phi(x) = \sum_{n \le x}\varphi(n)$ with $\sum_{d \le x}\Phi(\lfloor x/d \rfloor) = x(x+1)/2$ (Concrete Mathematics, Section 4.9); the [Dirichlet hyperbola method](/dirichlet-hyperbola-method/) is the general form.

## Bounds

- **Asymptotic size.** $\sum_{n \le N}\varphi(n) = \frac{3}{\pi^2}N^2 + O(N\log N)$ (Mertens, 1874; Apostol, Section 3.7), so $Q(N) = \frac{6}{\pi^2}N^2 + O(N\log N)$. The constant is $1/\zeta(2) = \prod_p (1 - p^{-2})$: a pair is coprime when no prime divides both, and each prime $p$ divides both with probability about $p^{-2}$.
- **Error size.** For $N = 10^6$ the error $Q(N) - \frac{6}{\pi^2}N^2$ is about $2929$, much less than $N\log N$.
- **Trivial bounds.** $2N - 1 \le Q(N) \le N^2$ for $N \ge 1$: all pairs with $a = 1$ or $b = 1$ are coprime.
- **Lower bound on time.** Reading $N$ and writing the answer take $\Omega(\log N)$ bit operations. No algorithm with time polynomial in $\log N$ is known; all the methods above take time that grows as a power of $N$.
- **Cancellation.** The Möbius sum has terms up to $N^2$ in size with both signs; it is exact in integer arithmetic, but floating point loses digits.

## Reductions

- **To the Mertens function.** With the grouping, $Q(N)$ needs only $M(\lfloor N/v \rfloor)$ for $O(\sqrt N)$ values; so an algorithm for $M$ at these points gives $Q(N)$ in the same time plus $O(\sqrt N)$.
- **To totient sums.** $Q(N) = 2\Phi(N) - 1$, and conversely $\Phi(N) = (Q(N) + 1)/2$, so the two problems are equivalent.
- **To lattice points.** A pair $(a, b)$ with $\gcd(a, b) = 1$ is a lattice point visible from the origin: no other lattice point lies on the segment between them. So $Q(N)$ counts the visible points in the square $[1, N]^2$ (Apostol, Section 3.8); see [lattice point counting](/lattice-point-counting/).
- **From fixed gcd counts.** Counts by exact gcd reduce to $Q$ of a smaller argument, as in the variants, and so do sums of $F(\gcd(a, b))$ for any function $F$.

## Applications

- **Farey sequences.** The Farey sequence of order $N$ has $1 + \Phi(N) = (Q(N) + 3)/2$ terms, which bounds the number of distinct slopes and fractions with small denominators.
- **Probability.** Two integers drawn uniformly from $[N]$ are coprime with probability $Q(N)/N^2 \to 6/\pi^2$. So a random input to [Euclid's algorithm](/euclidean-algorithm/) ends with gcd 1 in about 61 percent of the cases.
- **Geometry.** The number of distinct directions from the origin to the points of the grid $[N]^2$ is $Q(N)$, because each direction has exactly one point $(a, b)$ with $\gcd(a, b) = 1$.
- **Programming contests.** Sums of $\gcd(a, b)$, $\operatorname{lcm}(a, b)$ or $[\gcd(a, b) = g]$ over ranges are reduced to $Q$ and its rectangle variant with [Möbius inversion](/mobius-inversion-formula/).

## References
