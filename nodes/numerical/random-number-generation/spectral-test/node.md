---
tag: 81HMHG
kind: algorithm
slug: spectral-test
name: Spectral test
aliases:
- spectral test for LCGs
- Coveyou-MacPherson test
area: numerical/random-number-generation
level: advanced
summary: Measures the lattice-structure quality of an LCG's multiplier and modulus in each dimension.
model: word-ram
complexity:
  vars: {T: the largest dimension tested, m: the modulus of the generator}
  time: {worst: 2^(O(T^2)) poly(log m)}
  space: {extra: O(T^2)}
properties: {deterministic: true, in_place: false, recursive: true}
prereqs: [linear-congruential-generator, lll-algorithm, marsaglia-hyperplane-theorem]
see_also: [randu, park-miller-minimal-standard, dual-lattice, fincke-pohst-enumeration, hermite-constant, multiple-recursive-generator, lecuyer-combined-generator, statistical-tests-for-randomness]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.3.4, The spectral test (the definition of ν_t, Algorithm S, the figure of merit μ_t with the thresholds 0.1 and 1, and Table 1 of multipliers)
  - paper: doi:10.1145/321371.321379
    title: R. R. Coveyou and R. D. MacPherson, Fourier analysis of uniform random number generators, Journal of the ACM 14(1), 1967, pages 100 to 119
    locator: the introduction of the test through the Fourier coefficients of the joint distribution of successive outputs
  - paper: doi:10.1007/BF01457454
    title: A. K. Lenstra, H. W. Lenstra and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261, 1982, pages 515 to 534
    locator: the basis reduction algorithm used here to prepare the dual basis before enumeration
  - paper: "George S. Fishman and Louis R. Moore, An exhaustive analysis of multiplicative congruential random number generators with modulus 2^31 - 1, SIAM Journal on Scientific and Statistical Computing 7(1), 1986, pages 24 to 45"
    locator: the spectral and lattice figures of merit for all primitive multipliers of 2^31 - 1, and the recommendation of 48271 and 69621 among others
  - paper: "Pierre L'Ecuyer and Raymond Couture, An implementation of the lattice and spectral tests for multiple recursive linear random number generators, INFORMS Journal on Computing 9(2), 1997, pages 206 to 217"
    locator: the dual lattice construction for MRGs and combined generators, and the use of reduction followed by branch-and-bound enumeration
---

The spectral test measures how badly the outputs of a [linear congruential generator](/linear-congruential-generator/) fail to fill space. By [Marsaglia's theorem](/marsaglia-hyperplane-theorem/), the points $(x_n, x_{n+1}, \ldots, x_{n+t-1})/m$ formed by $t$ consecutive outputs all lie on a family of parallel hyperplanes. The spectral test computes, for each dimension $t = 2, 3, \ldots, T$, the largest distance $1/\nu_t$ between adjacent hyperplanes over all such families. A small $1/\nu_t$ means many planes, close together, which is good; a large one means the points sit on a few widely spaced planes, which is the flaw of [RANDU](/randu/). Computing $\nu_t$ is a shortest vector problem in the [dual lattice](/dual-lattice/), solved exactly here by [LLL reduction](/lll-algorithm/) and [Fincke-Pohst enumeration](/fincke-pohst-enumeration/). Knuth calls it the most powerful test known for LCGs, because every good generator passes it and every known bad one fails it.

## In plain words

Take a generator and plot each output against the next one, or each triple of outputs as a point in a cube. For a generator of this kind, the points are not scattered like dust: they line up in rows, and in three dimensions they lie on stacked flat sheets. That is unavoidable. What matters is how far apart the sheets are. If they are packed tightly, the gaps are too thin to matter in a simulation. If there are only a handful of sheets with wide empty slabs between them, results that depend on triples of numbers can be badly wrong.

The spectral test finds, for each number of dimensions, the widest possible gap between sheets. It does this by finding the shortest arrow in a related grid of whole-number points. A good multiplier keeps the gap small in every dimension tested.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The generator is $x_{n+1} = (a x_n + c) \bmod m$ with $\gcd(a, m) = 1$, and the outputs are normalized to $u_n = x_n / m \in [0, 1)$. For a dimension $t \ge 2$, let

$$L^*_t = \{ s \in \mathbb{Z}^t : s_1 + s_2 a + \cdots + s_t a^{t-1} \equiv 0 \pmod m \}, \qquad \nu_t = \min \{ |s| : s \in L^*_t, s \ne 0 \},$$

with $|s|$ the Euclidean length. Given $a$, $m$ and $T$, compute $\nu_t$ and a vector $s$ attaining it for $t = 2, \ldots, T$, together with the normalized figure of merit

$$\mu_t = \frac{\pi^{t/2} \nu_t^t}{\Gamma(t/2 + 1)\, m},$$

the volume of the $t$-ball of radius $\nu_t$ divided by $m$. The increment $c$ does not enter: it only shifts the point set.

## The algorithm

```pseudo id=main
SPECTRAL-TEST(a, m, T)                  ▷ gcd(a, m) = 1, T ≥ 2
L1  for t ← 2 to T
L2      B ← rows (m, 0, ..., 0) and e_j − (a^(j−1) mod m) e_1 for j = 2..t   ▷ a basis of L*_t
L3      B ← LLL-REDUCE(B)                ▷ same lattice, shorter and more orthogonal rows
L4      (ν_t², s_t) ← SHORTEST-VECTOR(B) ▷ exact Fincke-Pohst enumeration
L5      μ_t ← π^(t/2) ν_t^t / (Γ(t/2 + 1) m)
L6  return (ν_t², s_t, μ_t) for t = 2..T
```

Line L4 enumerates all integer combinations $\sum x_i b_i$ whose length is at most the best found so far, level by level over the Gram-Schmidt decomposition of the reduced basis; the bound shrinks whenever a shorter vector appears. All arithmetic is exact, with integers and rationals, so the result is $\nu_t^2$ itself and not an approximation. Knuth's Algorithm S computes the same quantity with a different reduction (pairwise reductions in the style of Dieter) before the enumeration.

## Example

**RANDU.** For $a = 65539$, $m = 2^{31}$, the test gives $\nu_2^2 = 2147221514$, which is fine, but $\nu_3^2 = 118$ with $s = (9, -6, 1)$. Indeed $a = 2^{16} + 3$ gives $a^2 \equiv 6a - 9 \pmod{2^{31}}$, so $9 x_n - 6 x_{n+1} + x_{n+2} \equiv 0$. Every triple therefore satisfies $9 u_n - 6 u_{n+1} + u_{n+2} \in \{-5, \ldots, 9\}$: all points lie on 15 planes, $1/\sqrt{118} \approx 0.092$ apart. Marsaglia's bound for $m = 2^{31}$ and $t = 3$ allows up to about 2344 planes. The figure of merit is $\mu_3 \approx 2.5 \times 10^{-6}$, far below Knuth's threshold of 0.1.

**The minimal standard and its replacement.** For $m = 2^{31} - 1$:

| $t$ | $\nu_t^2$, $a = 16807$ | $\mu_t$ | $\nu_t^2$, $a = 48271$ | $\mu_t$ |
|---|---|---|---|---|
| 2 | 282475250 | 0.413 | 1990735345 | 2.912 |
| 3 | 408197 | 0.509 | 1433881 | 3.349 |
| 4 | 21682 | 1.080 | 47418 | 5.167 |
| 5 | 4439 | 3.218 | 4404 | 3.155 |
| 6 | 895 | 1.725 | 1402 | 6.632 |

For 16807, $\nu_2^2 = 16807^2 + 1$ from $s = (-16807, 1)$: with a small multiplier, the pairs $(u_n, u_{n+1})$ lie on lines of slope about 16807, and $\mu_2$ is below 1. Both multipliers pass Knuth's criterion $\mu_t \ge 0.1$ for $t \le 6$, but 48271 scores higher in almost every dimension, which is why Park, Miller and Stockmeyer recommended it in 1993 ([minimal standard](/park-miller-minimal-standard/)). The multiplier 69069 with $m = 2^{32}$ scores well up to $t = 5$ but has $\nu_6^2 = 242$ and $\mu_6 \approx 0.017$. The tests of this page reproduce all these values.

## Correctness

The full proof is in the proof file; the outline is as follows.

1. **Duality.** The tuples $(x_n, \ldots, x_{n+t-1})/m$ lie in a shift of the lattice $\Lambda_t = \mathbb{Z}^t + \mathbb{Z}\,(1, a, \ldots, a^{t-1})/m$, and $L^*_t$ is exactly its dual lattice, with determinant $m$.
2. **Hyperplanes.** Each non-zero $s \in L^*_t$ defines a family of parallel hyperplanes $s \cdot u = k + \text{const}$ that contains all points, with spacing $1/|s|$. Conversely, any family of parallel hyperplanes with spacing $d$ containing all points gives a dual vector of length $1/d$. So $1/\nu_t$ is the largest spacing.
3. **Basis.** The rows of line L2 form a basis of $L^*_t$, and LLL reduction changes it only by unimodular operations.
4. **Exact enumeration.** The squared length of $\sum x_i b_i$ is a sum of non-negative terms over the Gram-Schmidt vectors; pruning a branch only when its partial sum already exceeds the current bound never discards a shorter vector, so the search ends at $\nu_t^2$.

The tests check the result against exhaustive search over a box that is large enough by the [Hermite bound](/hermite-constant/) $\nu_t^2 \le \gamma_t m^{2/t}$, for every multiplier of three small moduli in dimension 2 and several in dimension 3, and against [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) in dimension 2.

## Complexity

The input is the numbers $a$ and $m$, of $O(\log m)$ digits, and the dimension bound $T$. For each $t$, building the basis costs $O(t)$ modular multiplications. LLL reduction takes a number of arithmetic operations polynomial in $t$ and $\log m$. The enumeration of line L4 on an LLL-reduced basis visits at most $2^{O(t^2)}$ nodes, each costing $O(t)$ operations on rationals of $O(t \log m)$ digits. Over $t = 2, \ldots, T$ the total is $2^{O(T^2)}\,\mathrm{poly}(\log m)$ operations. In practice $T \le 8$ and the cost is negligible: the tests compute all five dimensions for a 31-bit modulus in a fraction of a second. Stronger reductions (BKZ, or Dieter's pairwise reductions) lower the enumeration cost in higher dimensions. The space is $O(T^2)$ numbers for the basis and Gram-Schmidt data.

## Properties

- **Exact, not statistical.** The test uses no samples; it computes a property of the whole period from $a$ and $m$.
- **Monotone in $t$.** $\nu_{t+1} \le \nu_t$, since appending a zero to a dual vector gives a dual vector of the next dimension. The spacing $1/\nu_t$ therefore grows with the dimension.
- **Upper bound.** By Hermite's theorem, $\nu_t^2 \le \gamma_t m^{2/t}$, with $\gamma_t^t = 4/3, 2, 4, 8, 64/3$ for $t = 2, \ldots, 6$. So $\mu_t$ is bounded by a constant depending on $t$ only, and $1/\nu_t$ is at least about $m^{-1/t}$ for every multiplier. No LCG has fine structure in high dimensions.
- **Knuth's criterion.** A multiplier passes if $\mu_t \ge 0.1$ for $2 \le t \le 6$, and passes with flying colors if $\mu_t \ge 1$ for all of them. These thresholds are conventions, not theorems.
- **Covers more than LCGs.** The same computation applies to [multiple recursive generators](/multiple-recursive-generator/) and [combined generators](/lecuyer-combined-generator/), whose output vectors also lie on lattices, and to lattice rules for numerical integration.

## Variants and improvements

- **Lattice test (Beyer ratio).** Instead of only the shortest dual vector, compare the lengths of the shortest and longest vectors in a Minkowski-reduced basis of $\Lambda_t$; a ratio near 1 means a nearly cubic lattice.
- **Counting planes.** The number of hyperplanes that cover the unit cube, rather than their spacing, uses the $\ell_1$ norm $\sum |s_i|$ in place of $|s|$. RANDU's 15 planes come from this count.
- **Lacunary indices.** Test the vectors $(u_{n+i_1}, \ldots, u_{n+i_t})$ for chosen lags, which gives the dual lattice for $(1, a^{i_2 - i_1}, \ldots)$.
- **Normalized figures of merit.** L'Ecuyer's $S_t = \nu_t / (\gamma_t^{1/2} m^{1/t})$, the ratio of $\nu_t$ to its Hermite bound, lies in $(0, 1]$; generators are chosen to maximize $\min_t S_t$ over a range of $t$.
- **Dieter's algorithm.** Knuth's Algorithm S, based on Dieter (1975), uses pairwise reductions and a bounded search; it is simpler to implement in fixed precision than exact LLL.

## When to use it

Use the spectral test when choosing or checking the multiplier of an LCG, an MRG or a combined generator. It is the first filter in every published search for multipliers, and published tables (Knuth Table 1, Fishman and Moore, L'Ecuyer) list its results. Run it for $t$ up to 6 or 8. A generator that fails it should not be used; one that passes still has to be checked with [empirical tests](/statistical-tests-for-randomness/), and still has the hyperplane structure that Marsaglia's theorem forces, so for large simulations a generator with a much longer period is preferable.

## Pitfalls

- **Floating-point arithmetic.** The basis entries are of size $m$ and squared lengths of size $m^2$; with $m$ near $2^{64}$, double precision loses the answer. Use exact integers and rationals, as here, or carefully bounded fixed-point arithmetic.
- **Dimension 2 is not enough.** RANDU has an excellent $\nu_2$ and a disastrous $\nu_3$. Test every dimension up to at least 6.
- **Low-order digits.** The test is about the full outputs $x_n / m$. With a power-of-two modulus, the low-order digits of $x_n$ have much shorter periods, which the spectral test does not reveal.
- **Approximate shortest vectors.** LLL alone gives a vector within a factor $2^{(t-1)/2}$ of the shortest, which overestimates $\nu_t$ and can make a bad multiplier look good; the enumeration step is required.

## Implementations

## History

R. R. Coveyou and R. D. MacPherson introduced the test in 1967, through the Fourier analysis of the joint distribution of successive outputs; the name "spectral" comes from there. The following year George Marsaglia showed that LCG points lie on few hyperplanes ("Random numbers fall mainly in the planes"), which made the geometric meaning of the test clear. Ulrich Dieter (1975) gave an efficient algorithm for the shortest vector, which Knuth adopted as Algorithm S in The Art of Computer Programming, together with the figure of merit $\mu_t$ and a table of multipliers. Fishman and Moore (1986) applied the test to every primitive multiplier of $2^{31} - 1$. With the LLL algorithm (1982) and better enumeration, L'Ecuyer and Couture (1997) extended the test to multiple recursive and combined generators, and it remains the main criterion in the design of generators such as [MRG32k3a](/mrg32k3a/).

## References
