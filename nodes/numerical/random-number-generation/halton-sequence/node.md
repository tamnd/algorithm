---
tag: MKABDE
kind: algorithm
slug: halton-sequence
name: Halton sequence
aliases:
- Halton low-discrepancy sequence
- Halton points
area: numerical/random-number-generation
level: advanced
summary: A low-discrepancy sequence in [0, 1)^d whose i-th point mirrors the base-b_k digits of i about the radix point in each coordinate, for pairwise coprime bases such as the first d primes.
model: word-ram
complexity:
  vars: {n: the number of points, d: the dimension}
  time: {worst: O(d n log n)}
  space: {extra: Θ(d)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1960
  people: [J. H. Halton]
  note: Halton extended van der Corput's 1935 base-2 digit reversal to several coprime bases, one per coordinate, and proved the discrepancy bound O((log N)^d / N).
prereqs: [discrepancy, quasi-monte-carlo-integration, equidistribution]
see_also: [sobol-sequence, koksma-hlawka-inequality, monte-carlo-integration, latin-hypercube-sampling, chinese-remainder-theorem, prime-number, pseudorandom-number-generator]
sources:
  - paper: "J. H. Halton, On the efficiency of certain quasi-random sequences of points in evaluating multi-dimensional integrals, Numerische Mathematik 2, 1960, 84-90"
    locator: the definition of the sequence in coprime bases and the bound on its discrepancy
  - book: isbn:9780898712957
    title: Harald Niederreiter, Random Number Generation and Quasi-Monte Carlo Methods, SIAM, CBMS-NSF Regional Conference Series in Applied Mathematics 63, 1992
    locator: Chapter 2, Theorem 2.6 (the exact one-dimensional star discrepancy) and Theorem 2.11 (Koksma-Hlawka); Chapter 3, Section 3.1 (the radical inverse function, van der Corput and Halton sequences, Theorem 3.6)
  - paper: "J. G. van der Corput, Verteilungsfunktionen, Proceedings of the Koninklijke Akademie van Wetenschappen te Amsterdam 38, 1935"
    locator: the one-dimensional sequence obtained by reversing the binary digits of the index
  - paper: "Eric Braaten and George Weller, An improved low-discrepancy sequence for multidimensional quasi-Monte Carlo integration, Journal of Computational Physics 33(2), 1979, 249-258"
    locator: the digit permutations that remove the correlations between coordinates with large bases
  - paper: "Ladislav Kocis and William J. Whiten, Computational investigations of low-discrepancy sequences, ACM Transactions on Mathematical Software 23(2), 1997, 266-294"
    locator: the comparison of Halton, leaped Halton and scrambled variants, and the plots of correlated coordinate pairs
---

The Halton sequence is a deterministic sequence of points in the unit cube $[0, 1)^d$ that fills space far more evenly than independent random points. Its $i$-th point is built from the digits of $i$: in coordinate $k$, write $i$ in base $b_k$ and mirror the digits about the radix point, so that $i = 6 = 110_2$ gives $0.011_2 = 3/8$. With pairwise coprime bases, usually the first $d$ primes, every block of consecutive points hits each small box of a matching grid about equally often, which gives star [discrepancy](/discrepancy/) $O((\log N)^d / N)$ against $O(N^{-1/2})$ for random points. It is the simplest sequence for [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/), and it works best in low dimension.

## In plain words

To spread points along a line without bunching, take the counting numbers $0, 1, 2, 3, \ldots$, write them in binary, and read the digits backwards after a point: $0, 0.1, 0.01, 0.11, 0.001, \ldots$ in binary, that is $0, \tfrac12, \tfrac14, \tfrac34, \tfrac18, \ldots$ Each new point lands in the middle of the largest gap left so far. For a square, do the same in base 2 for the first coordinate and in base 3 for the second; for a cube add base 5, and so on with prime bases. Because the bases share no factor, the coordinates do not line up with each other, and the points cover the square evenly.

The points are not random. They are designed to be more even than random points, which makes averages of a smooth function over them converge faster.

## The problem

Given a dimension $d$, produce points $u_0, u_1, \ldots \in [0, 1)^d$ such that for every $N$ the first $N$ points have small star discrepancy
$$D_N^* = \sup_{y \in [0,1]^d} \left| \frac{\#\{ i < N : u_i \in [0, y) \}}{N} - \operatorname{vol}[0, y) \right|,$$
where $[0, y) = \prod_k [0, y_k)$. By the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/), the error of the average $\frac1N \sum_{i<N} h(u_i)$ as an estimate of $\int_{[0,1)^d} h$ is at most $V(h)\, D_N^*$, where $V(h)$ is the variation of $h$ in the sense of Hardy and Krause. The sequence must be extensible: adding more points must not change the earlier ones. In the notation of generators, the state is the index, $s_{i+1} = s_i + 1$, and the output is $u_i = g(i)$; the cost model counts word operations per point.

**Radical inverse.** For a base $b \ge 2$ and $i = \sum_{j \ge 0} a_j b^j$ with digits $0 \le a_j < b$, the radical inverse is
$$\varphi_b(i) = \sum_{j \ge 0} a_j\, b^{-j-1} \in [0, 1).$$
The van der Corput sequence in base $b$ is $\varphi_b(0), \varphi_b(1), \ldots$, and the Halton sequence in pairwise coprime bases $b_1, \ldots, b_d$ is $u_i = (\varphi_{b_1}(i), \ldots, \varphi_{b_d}(i))$.

## The algorithm

```pseudo id=main
HALTON(i, b_1, ..., b_d)            ▷ pairwise coprime bases, usually the first d primes
L1  for k ← 1 to d
L2      x ← 0; f ← 1 / b_k; n ← i
L3      while n > 0
L4          x ← x + f · (n mod b_k)  ▷ digit j of i goes to position j + 1 after the point
L5          n ← ⌊n / b_k⌋; f ← f / b_k
L6      u_k ← x
L7  return (u_1, ..., u_d)
```

In floating point, $x$ is a sum of at most $\lceil \log_{b_k}(i+1) \rceil$ terms. For exact output, accumulate the integer $\sum_j a_j b^{L-1-j}$ by Horner's rule and divide by $b^L$ once, as the reference implementation does.

## Example

Bases 2 and 3, first six points:

| $i$ | base 2 | $\varphi_2(i)$ | base 3 | $\varphi_3(i)$ | point |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | $(0, 0)$ |
| 1 | 1 | $0.1_2$ | 1 | $0.1_3$ | $(1/2, 1/3)$ |
| 2 | 10 | $0.01_2$ | 2 | $0.2_3$ | $(1/4, 2/3)$ |
| 3 | 11 | $0.11_2$ | 10 | $0.01_3$ | $(3/4, 1/9)$ |
| 4 | 100 | $0.001_2$ | 11 | $0.11_3$ | $(1/8, 4/9)$ |
| 5 | 101 | $0.101_2$ | 12 | $0.21_3$ | $(5/8, 7/9)$ |

For $i = 11$ the run of L1 to L7 with bases $(2, 3, 5)$ gives: $11 = 1011_2$, so $\varphi_2(11) = 0.1101_2 = 13/16$; $11 = 102_3$, so $\varphi_3(11) = 0.201_3 = 19/27$; $11 = 21_5$, so $\varphi_5(11) = 0.12_5 = 7/25$.

**Stratification.** The first 72 points in bases (2, 3) put exactly one point in each of the $8 \times 9$ boxes $[a/8, (a+1)/8) \times [c/9, (c+1)/9)$, and the same holds for any 72 consecutive indices. Exact star discrepancies, computed by checking every critical box, are $D_{16}^* = 29/144 \approx 0.201$, $D_{64}^* = 5/96 \approx 0.052$ and $D_{128}^* \approx 0.0367$; 128 independent uniform points typically have $D^*$ around 0.08 to 0.15. For $N = 4$ the value is $1/2$: the closed box $[0, 3/4] \times [0, 2/3]$ holds all four points but has area $1/2$.

**Integration.** The average of $x y$ over the 4096 points $u_1, \ldots, u_{4096}$ in bases (2, 3) differs from the true value $1/4$ by $3.75 \times 10^{-4}$. Plain Monte Carlo with 4096 points has standard error $\sigma / 64 \approx 0.0034$ for this integrand ($\sigma^2 = 1/9 - 1/16$).

## Correctness

**The algorithm computes $\varphi_b(i)$.** After $j$ passes through L3 to L5, $n = \lfloor i / b^j \rfloor$, $f = b^{-j-1}$ and $x = \sum_{t<j} a_t b^{-t-1}$, because $n \bmod b$ at pass $t$ is the digit $a_t$. The loop stops when $n = 0$, after the last nonzero digit.

**Elementary boxes.** Call $E = \prod_k [c_k b_k^{-e_k}, (c_k + 1) b_k^{-e_k})$ an elementary box, of volume $1/M$ with $M = \prod_k b_k^{e_k}$. In one coordinate, $\varphi_b(i) \in [c\, b^{-e}, (c+1) b^{-e})$ if and only if the first $e$ digits of $\varphi_b(i)$ after the point are the base-$b$ digits of $c$, that is, if and only if $i \bmod b^e$ equals the digit reversal of $c$. So $u_i \in E$ is a system of congruences $i \equiv r_k \pmod{b_k^{e_k}}$, and since the moduli are pairwise coprime, the [Chinese remainder theorem](/chinese-remainder-theorem/) makes it a single class $i \equiv r \pmod M$. Any $N$ consecutive indices contain $\lfloor N / M \rfloor$ or $\lceil N / M \rceil$ members of that class, so the count in $E$ differs from $N \operatorname{vol}(E)$ by less than 1.

**Discrepancy bound.** Split each $[0, y_k)$ by the base-$b_k$ digits of $y_k$ into at most $(b_k - 1) L_k$ elementary intervals plus a remainder inside one interval of length $b_k^{-L_k}$, with $L_k = \lceil \log_{b_k} N \rceil$. Products of these pieces sandwich $[0, y)$ between two unions of at most $\prod_k ((b_k - 1) L_k + 1)$ elementary boxes whose volumes differ by at most $\sum_k b_k^{-L_k} \le d / N$. Adding the errors of less than 1 per box gives
$$D_N^* \le \frac{1}{N}\left( d + \prod_{k=1}^{d} \big( (b_k - 1) \lceil \log_{b_k} N \rceil + 1 \big) \right) = O\!\left( \frac{(\log N)^d}{N} \right),$$
for every $N \ge 1$ and every block of $N$ consecutive points. The full proofs are on the proof page. This bound is cruder than Halton's and Niederreiter's (Theorem 3.6 has constants $(b_k - 1) / (2 \log b_k)$ in place of $(b_k - 1) / \log b_k$), but has the same order.

## Complexity

Coordinate $k$ of point $i$ takes $\lceil \log_{b_k}(i+1) \rceil$ passes of the loop, each a constant number of word operations, so the first $n$ points cost $O(d\, n \log n)$ in total and $O(d \log n)$ each. The incremental variant below keeps the digits of the current index in each base and adds 1 with carry, which costs $O(1)$ amortized digit operations per coordinate (a carry past position $j$ happens once in $b^j$ steps), so $\Theta(d n)$ for $n$ points. Extra space is $\Theta(d)$ words, or $\Theta(d \log n)$ digits for the incremental form. Point $i$ can be computed directly without the earlier ones, which makes the sequence easy to split across processors.

## Properties

- **Proved:** star discrepancy $O((\log N)^d / N)$ for every $N$, with the explicit bound above; every block of $\prod_k b_k^{e_k}$ consecutive points is perfectly stratified in the matching elementary boxes.
- **Each coordinate is a van der Corput sequence**, so every one-dimensional projection is as even as possible up to a constant: $N D_N^* = O(\log N)$.
- **Extensible and indexable.** $u_i$ depends only on $i$; adding points never moves earlier ones.
- **Not random.** Consecutive points are strongly dependent: $\varphi_2(2i+1) = \varphi_2(2i) + 1/2$. The sequence must not be used where independence matters, such as in a simulation that draws several values per step from one stream. It is $1$-[equidistributed](/equidistribution/) in each coordinate and fails $k$-distribution of consecutive values by design.
- **Error estimates need randomization.** A deterministic point set gives no variance estimate; randomized versions (random shift or digit scrambling, repeated with independent randomizations) do.

## Variants and improvements

- **Hammersley point set.** For a fixed $N$, use $(i / N, \varphi_{b_1}(i), \ldots, \varphi_{b_{d-1}}(i))$, $0 \le i < N$; this saves one logarithmic factor in the discrepancy but is not extensible.
- **Incremental generation.** Keep the base-$b_k$ digits of $i$ and add 1 with carry; update the coordinate by the changed digits only.
- **Scrambled Halton.** Apply a permutation $\pi_j$ of $\{0, \ldots, b-1\}$ with $\pi_j(0) = 0$ to digit $j$ before mirroring. Braaten and Weller (1979) chose permutations to reduce the correlation between coordinates with large bases; random permutations give a randomized QMC method with unbiased estimates.
- **Leaped Halton.** Use the indices $0, L, 2L, \ldots$ for an integer $L$ coprime to all bases; Kocis and Whiten (1997) report that suitable leaps reduce the correlations.
- **Random start.** Begin at a random index; the stratification property holds for every block of consecutive indices, so the bounds are unchanged.
- **Digital nets and sequences.** The [Sobol sequence](/sobol-sequence/) and Niederreiter sequences use one base for all coordinates and achieve stronger uniformity (all elementary boxes of the same volume in base 2), which makes them the usual choice in higher dimensions.

## When to use it

Use it for numerical integration and sampling in low to moderate dimension (up to about 10 to 20) when the integrand is reasonably smooth and the number of points is not fixed in advance: option pricing with few time steps, rendering (sampling pixel areas and lens positions), design of computer experiments and global optimization start points. In higher dimensions prefer scrambled Halton or [Sobol](/sobol-sequence/) points, and use [pseudorandom numbers](/pseudorandom-number-generator/) for simulation of stochastic processes where independence matters.

## Pitfalls

- **Large bases in high dimension.** For bases 29 and 31, the first 29 points are $(i/29, i/31)$ and lie on one line through the origin; long stretches of the sequence in neighbouring large prime bases fall on a few parallel lines. The bound $(\log N)^d / N$ is smaller than $N^{-1/2}$ only when $N$ is astronomically large for $d = 20$. Scramble the digits, or use a digital sequence.
- **Common bases.** Bases that share a factor, or the same base twice, destroy the construction: with bases 2 and 4, $\varphi_4(i)$ is determined by the binary digits of $i$ and the pairs correlate. Use the first $d$ primes.
- **Dropping point 0.** $u_0 = (0, \ldots, 0)$ lies on the boundary; integrands with a singularity at the origin need it skipped, which is safe because blocks of consecutive points keep the bounds.
- **Using it as a random number generator.** The values are highly correlated in sequence; feeding them to code that expects independent draws gives biased results.
- **Floating-point accumulation.** For very large $i$ and small bases, summing $f \cdot a_j$ in floating point loses the last bits; integer accumulation followed by one division avoids it.

## Implementations

## History

Van der Corput introduced the one-dimensional sequence in 1935 in his study of distribution functions. Halton (1960) took one coprime base per coordinate, proved that the discrepancy is $O((\log N)^d / N)$ and compared the error of integration with that of random points; Hammersley proposed the fixed-size point set in the same year. Braaten and Weller (1979) introduced digit permutations to break the correlations that appear in higher dimensions. Niederreiter's monograph (1992) gives the general theory together with digital nets, and later work by Kocis and Whiten, Wang and Hickernell, and Owen developed leaped, randomly started and randomly scrambled forms for randomized quasi-Monte Carlo.

## References
