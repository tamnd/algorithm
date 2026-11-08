---
tag: 3EWTJP
kind: algorithm
slug: mrg32k3a
name: MRG32k3a
aliases:
- MRG32k3a combined generator
- RngStreams
- "L'Ecuyer-CMRG"
area: numerical/random-number-generation
level: advanced
summary: A combined pair of MRGs with period about 2^191, used in simulation and parallel streams.
model: word-ram
complexity:
  vars: {m: "the two prime moduli, just below 2^32"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: true, recursive: false}
prereqs: [multiple-recursive-generator, lecuyer-combined-generator, jump-ahead]
see_also: [spectral-test, statistical-tests-for-randomness, matrix-exponentiation, primitive-polynomial, philox, xoshiro-xoroshiro, monte-carlo-integration, park-miller-minimal-standard]
sources:
  - paper: doi:10.1287/opre.47.1.159
    title: Pierre L'Ecuyer, Good parameters and implementations for combined multiple recursive random number generators, Operations Research 47(1), 1999, pages 159 to 164
    locator: the parameter set MRG32k3a with moduli 2^32 - 209 and 2^32 - 22853, its period near 2^191, the selection by the spectral test, and the C implementation in double precision
  - paper: doi:10.1287/opre.50.6.1073.358
    title: Pierre L'Ecuyer, Richard Simard, E. Jack Chen and W. David Kelton, An object-oriented random-number package with many long streams and substreams, Operations Research 50(6), 2002, pages 1073 to 1075
    locator: the RngStreams package built on MRG32k3a, with streams 2^127 steps apart, substreams 2^76 steps apart, and jumps by precomputed matrix powers
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007, Article 22
    locator: the summary table of results for widely used generators, where MRG32k3a passes SmallCrush, Crush and BigCrush
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.2, linear recurrences modulo a prime, the period p^k - 1 for a primitive polynomial and the three conditions for primitivity
---

MRG32k3a runs two [multiple recursive generators](/multiple-recursive-generator/) of order 3 side by side, with prime moduli $m_1 = 2^{32} - 209$ and $m_2 = 2^{32} - 22853$, and outputs the difference of their newest values modulo $m_1$, scaled into $(0, 1)$. Pierre L'Ecuyer chose the parameters in 1999 with the [spectral test](/spectral-test/). The state is six 32-bit integers, the state period is about $2^{191}$, and all arithmetic fits exactly in IEEE double precision, so the same code gives the same numbers on every machine. With the RngStreams package, which cuts the period into $2^{64}$ streams of $2^{127}$ values, it is a standard generator for stochastic simulation and parallel Monte Carlo work.

## In plain words

Imagine two counters that each update by mixing their last three values with a few fixed multipliers, and then wrap around at a prime number just below four billion. Each counter alone is a decent generator with a very long cycle. The generator takes the newest value of each, subtracts one from the other, wraps the result into range and divides, which gives a number strictly between 0 and 1.

The two cycles have different lengths, so the pair repeats only when both line up again, which takes about $2^{191}$ steps. Because the update is a fixed linear rule, the generator can also jump far ahead in one go, so each part of a parallel program can get its own long, separate piece of the sequence.

## The problem

We use the notation of the [pseudorandom number generator](/pseudorandom-number-generator/) page. The task is to produce a sequence $u_0, u_1, \ldots$ in $U(0,1)$ that passes statistical tests, with a period far beyond any simulation, a theory that explains its lattice structure, the same output on every platform, and cheap jumps so that many disjoint streams can be handed out. The state space is $S = (\mathbb{Z}_{m_1}^3 \setminus \{0\}) \times (\mathbb{Z}_{m_2}^3 \setminus \{0\})$, the transition $f$ advances both components, and the output function $g$ combines them.

## The algorithm

The two components are

$$x_{1,n} = (1403580\, x_{1,n-2} - 810728\, x_{1,n-3}) \bmod m_1, \qquad x_{2,n} = (527612\, x_{2,n-1} - 1370589\, x_{2,n-3}) \bmod m_2,$$

and the output is $z_n = (x_{1,n} - x_{2,n}) \bmod m_1$, mapped to $u_n = z_n \cdot \mathit{norm}$ if $z_n > 0$ and to $m_1 \cdot \mathit{norm}$ if $z_n = 0$, with $\mathit{norm} = 2.328306549295728 \cdot 10^{-10} \approx 1/(m_1 + 1)$. Each state $X_j = (x_{j,n-3}, x_{j,n-2}, x_{j,n-1})$ is kept oldest first.

```pseudo id=main
MRG32K3A-NEXT(X1, X2)                      ▷ X1 in [0, m1)^3, X2 in [0, m2)^3, neither all zero
L1  p1 ← (1403580 · X1[1] − 810728 · X1[0]) mod m1
L2  X1 ← (X1[1], X1[2], p1)
L3  p2 ← (527612 · X2[2] − 1370589 · X2[0]) mod m2
L4  X2 ← (X2[1], X2[2], p2)
L5  if p1 > p2 then return (p1 − p2) · norm
L6  return (p1 − p2 + m1) · norm           ▷ includes p1 = p2, which gives m1 · norm < 1
```

Each component has a zero coefficient, so each step needs two multiplications per component. In L'Ecuyer's reference code the values are doubles: every product is below $2^{53}$, so the arithmetic is exact. The implementation on this page uses Python integers and returns the same doubles bit for bit.

**Streams and substreams.** Since each component is $X_j \leftarrow A_j X_j \bmod m_j$ for a $3 \times 3$ matrix $A_j$, the state $2^e$ steps ahead is $A_j^{2^e} X_j \bmod m_j$, by [matrix exponentiation](/matrix-exponentiation/) ([jump ahead](/jump-ahead/)). RngStreams stores $A_j^{2^{127}}$ and $A_j^{2^{76}}$: a new stream starts $2^{127}$ steps after the previous one, and each stream is split into substreams $2^{76}$ steps apart.

## Example

From the default seed, 12345 in all six places, the first three steps are:

| $n$ | $p_1$ | $p_2$ | $p_1 - p_2$ | $u_n$ |
|---|---|---|---|---|
| 1 | 3023790853 | 2478282264 | 545508589 | 0.12701112204657714 |
| 2 | 3023790853 | 1655725443 | 1368065410 | 0.3185275653967945 |
| 3 | 3385359573 | 2057415812 | 1327943761 | 0.3091860155832701 |

The first two values of $p_1$ agree because the first component reads $x_{1,n-2}$ and $x_{1,n-3}$, which are both 12345 in the first two steps. The next outputs are $0.82584686292711362$ and $0.2216299157820229$, as printed by the reference C code. The second RngStreams stream, $2^{127}$ steps on, starts with $0.7595818622487196$, $0.97831057326137083$, $0.68513580819318265$; the tests check these values and the four jump matrices printed in RngStream.c.

## Correctness

Correctness here has three parts, proved in full in the proof file.

1. **Period.** The characteristic polynomials $z^3 - 1403580 z + 810728$ modulo $m_1$ and $z^3 - 527612 z^2 + 1370589$ modulo $m_2$ are [primitive](/primitive-polynomial/), which the tests check with Knuth's three conditions in exact arithmetic. So each component, from any non-zero seed, has period $m_j^3 - 1$. The pair repeats exactly when both do, so its period is $\operatorname{lcm}(m_1^3 - 1, m_2^3 - 1) = (m_1^3 - 1)(m_2^3 - 1)/2$, since the gcd is 2. This number lies between $2^{190}$ and $2^{191}$.
2. **Exact arithmetic.** Each product is below $1403580 \cdot m_1 < 2^{53}$, so double precision computes the integers $p_1, p_2$ exactly, and the output is a single rounded product.
3. **Range.** The integer multiplied by $\mathit{norm}$ lies in $[1, m_1]$, so $u_n \in [\mathit{norm}, m_1 \cdot \mathit{norm}] \subset (0, 1)$. The generator never returns 0 or 1, which matters for $-\ln u$ and similar transformations.

The output is a function of the state, so its period divides the state period. That it is exactly the state period is L'Ecuyer's statement, not proved on this page.

## Complexity

Each output costs four multiplications, two reductions modulo a prime, one comparison and one floating-point multiplication: $\Theta(1)$ word operations. The state is six words. A jump by $2^e$ steps costs two $3 \times 3$ matrix-vector products with precomputed matrices, or $O(e)$ matrix squarings, 27 multiplications each, without them.

## Properties

- **Proved:** state period $(m_1^3 - 1)(m_2^3 - 1)/2 \approx 2^{191}$; outputs in $(0, 1)$; identical results on any machine with IEEE doubles.
- **Lattice structure.** The combination behaves like one MRG of order 3 with modulus $m_1 m_2$, as on the [L'Ecuyer combined generator](/lecuyer-combined-generator/) page, and L'Ecuyer selected the multipliers so that the spectral test of this large recurrence is good over many dimensions. This is a design criterion, measured, not a proof of randomness.
- **Empirical:** L'Ecuyer and Simard (2007) report that MRG32k3a passes SmallCrush, Crush and BigCrush of TestU01 ([statistical tests for randomness](/statistical-tests-for-randomness/)).
- **Resolution.** Each output carries about 32 bits; for full 53-bit doubles, combine two outputs.
- **Not secure.** The state follows linearly from a handful of outputs, so the sequence is predictable.

## Variants and improvements

- **MRG31k3p.** L'Ecuyer and Touzin (2000) gave a variant with moduli $2^{31} - 1$ and $2^{31} - 21069$ and multipliers that are sums or differences of powers of 2, so the steps use shifts and additions on 32-bit integers.
- **MRG32k5a.** The same 1999 paper gives order-5 components with a longer period, for users who want more.
- **Integer implementations.** With 64-bit integers, the products fit easily and the reduction can use [Barrett](/barrett-reduction/) or plain `%`, as in this page's code.
- **Library versions.** MRG32k3a with streams is built into many simulation and numerical systems, including R's `"L'Ecuyer-CMRG"` generator in the parallel package, MATLAB's `mrg32k3a` stream, NVIDIA cuRAND and Intel MKL.
- **Counter-based alternatives.** [Philox](/philox/) gives random access by a counter instead of jump matrices.

## When to use it

Use MRG32k3a for discrete-event simulation and other stochastic models where you need reproducible, independent streams and substreams, a published theory and the same numbers on every platform; for example to give each simulated entity its own stream so that changing one part of the model does not shift the random numbers of another (common random numbers). For raw speed with 64-bit integers, [xoshiro256**](/xoshiro-xoroshiro/) or [PCG](/pcg-random/) are faster; for massively parallel work on GPUs, [Philox](/philox/) is simpler to split. Never use it for keys or tokens; use a [cryptographically secure generator](/cryptographically-secure-prng/).

## Pitfalls

- **Overflow in 32-bit code.** The products reach about $6 \cdot 10^{15}$. Use doubles or 64-bit integers; 32-bit integer code overflows silently.
- **Zero seeds.** A component seed of three zeros stays zero forever, and seed values must be below their modulus ($m_2 < m_1$, so a value valid for the first component may be invalid for the second).
- **Wrong state order.** The coefficients apply to $x_{n-2}$ and $x_{n-3}$ in the first component and to $x_{n-1}$ and $x_{n-3}$ in the second. Swapping the order of the stored values gives a different and untested generator.
- **Overlapping streams by seeding.** Starting parallel streams from seeds such as $1, 2, 3, \ldots$ gives no guarantee that they do not overlap or correlate. Use the jump matrices so that streams are $2^{127}$ steps apart.
- **Comparison direction.** The reference code returns $(p_1 - p_2 + m_1) \cdot \mathit{norm}$ when $p_1 \le p_2$. Testing $p_1 \ge p_2$ in line L5 instead returns 0 when the two values are equal, which breaks code that takes $\ln u$.

## Implementations

## History

Combined generators with several small prime moduli go back to Wichmann and Hill (1982) and L'Ecuyer (1988). L'Ecuyer and Tezuka (1991) showed that such combinations behave like a single generator with the product modulus, which made their lattice structure analysable. In 1999 L'Ecuyer published a search for combined MRGs whose arithmetic is exact in double precision, and MRG32k3a was the recommended 32-bit set. The RngStreams package of L'Ecuyer, Simard, Chen and Kelton (2002) added streams and substreams on top of it, and it was later adopted by many simulation tools and numerical libraries.

## References
