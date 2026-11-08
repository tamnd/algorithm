---
tag: 9FJDDG
kind: algorithm
slug: lecuyer-combined-generator
name: L'Ecuyer combined generator
aliases:
- combined multiple recursive generator
- combined linear congruential generator
- combined MRG
area: numerical/random-number-generation
level: advanced
summary: Runs several multiple recursive generators with distinct prime moduli and outputs their weighted sum modulo the first modulus; the result is close to one MRG with the product modulus.
model: word-ram
complexity:
  vars: {n: the number of outputs, J: the number of components, k: the largest component order}
  time: {worst: Θ(n J k)}
  space: {extra: Θ(J k)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1988
  people: [Pierre L'Ecuyer]
  note: L'Ecuyer combined two multiplicative LCGs with moduli near 2^31 into a portable generator with period about 2.3 * 10^18, and later extended the method to MRGs, leading to MRG32k3a in 1999.
prereqs: [multiple-recursive-generator, linear-congruential-generator, chinese-remainder-theorem, primitive-polynomial]
see_also: [mrg32k3a, park-miller-minimal-standard, marsaglia-hyperplane-theorem, spectral-test, jump-ahead, generator-period, primitive-root]
sources:
  - paper: "Pierre L'Ecuyer, Efficient and portable combined random number generators, Communications of the ACM 31(6), 1988, pages 742 to 749"
    locator: the combination of two multiplicative LCGs with m1 = 2147483563, a1 = 40014, m2 = 2147483399, a2 = 40692, output (x1 - x2) mod (m1 - 1), and its period
  - paper: "Pierre L'Ecuyer and Shu Tezuka, Structural properties for two classes of combined random number generators, Mathematics of Computation 57(196), 1991, pages 735 to 746"
    locator: the theorem that a combined LCG is close to one LCG whose modulus is the product of the component moduli
  - paper: "Pierre L'Ecuyer, Combined multiple recursive random number generators, Operations Research 44(5), 1996, pages 816 to 822"
    locator: the extension to MRG components, the equivalent MRG modulo the product, and the bound on the difference between the two outputs
  - paper: "Pierre L'Ecuyer, Good parameters and implementations for combined multiple recursive random number generators, Operations Research 47(1), 1999, pages 159 to 164"
    locator: the parameters of MRG32k3a, chosen by the spectral test, and its period of about 2^191
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.2, Other methods (combining generators by addition modulo m)
---

L'Ecuyer's combined generator runs $J$ small linear generators side by side, each with its own prime modulus $m_j$, and outputs a weighted sum of their states modulo $m_1$. Each component is cheap and fits in a machine word, but the combination behaves almost exactly like one [multiple recursive generator](/multiple-recursive-generator/) whose modulus is the product $m_1 m_2 \cdots m_J$: its period is the least common multiple of the component periods, and its lattice structure is that of the big generator, which can be checked with the [spectral test](/spectral-test/). The 1988 version combines two LCGs with moduli near $2^{31}$ and has period about $2.3 \cdot 10^{18}$; [MRG32k3a](/mrg32k3a/) combines two order-3 MRGs and has period about $2^{191}$.

## In plain words

One small generator has a short cycle and a visible pattern. Run two or three of them at once, each counting in its own modular arithmetic, and add their outputs, wrapping around at the end. The sum only repeats when all the small generators are back at their starting points together, which takes as long as the product of their cycle lengths, roughly.

The surprise is that the sum is not a messy mixture. It is almost exactly the output of one big generator of the same simple kind, with a huge modulus, so the same mathematics that measures the quality of a simple generator also measures the combination.

## The problem

A generator is a tuple $(S, f, g, s_0)$ with state space $S$, transition $f$ ($s_{i+1} = f(s_i)$), output $u_i = g(s_i)$ and seed $s_0$. We want outputs close to $U(0, 1)$ with a long period $\rho$ and a good lattice structure, using only arithmetic on numbers below $2^{53}$ or $2^{64}$. A single MRG $x_n = (a_1 x_{n-1} + \cdots + a_k x_{n-k}) \bmod m$ with $m$ near $2^{32}$ has period at most $m^k - 1$, and its $d$-tuples lie on few hyperplanes when $m$ is small ([Marsaglia's theorem](/marsaglia-hyperplane-theorem/)). The combined generator uses components

$$x_{j,n} = (a_{j,1} x_{j,n-1} + \cdots + a_{j,k} x_{j,n-k}) \bmod m_j, \qquad j = 1, \ldots, J,$$

with distinct primes $m_j$ and integer weights $\delta_j$ coprime to $m_j$. The state is the concatenation of the component states, and the output is

$$z_n = \Big( \sum_{j=1}^{J} \delta_j x_{j,n} \Big) \bmod m_1, \qquad u_n = z_n / m_1.$$

Implementations often use $u_n = z_n / (m_1 + 1)$ and map $z_n = 0$ to $m_1 / (m_1 + 1)$, so that $u_n$ is never 0 or 1.

## The algorithm

```pseudo id=main
COMBINED-NEXT()                        ▷ components j = 1..J, each with state (x_(j,n−k), ..., x_(j,n−1))
L1  z ← 0
L2  for j ← 1 to J
L3      x ← (a_(j,1) x_(j,n−1) + ... + a_(j,k) x_(j,n−k)) mod m_j
L4      shift the state of component j and store x as x_(j,n)
L5      z ← z + δ_j · x
L6  z ← z mod m_1
L7  if z > 0 then return z / (m_1 + 1) else return m_1 / (m_1 + 1)
```

Line L3 needs products of up to about $2^{53}$ in floating-point implementations or a 64-bit integer product; MRG32k3a's coefficients are below $2^{21}$ so that $a \cdot x < 2^{53}$ holds in double precision. Schrage's method or 128-bit products serve when the coefficients are larger.

**The equivalent generator.** Let $m = m_1 \cdots m_J$, and let $w_n = \big(\sum_j \delta_j x_{j,n} / m_j\big) \bmod 1$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), choose $a_i \equiv a_{j,i} \pmod{m_j}$ for all $j$. Then $X_n = m w_n$ is an integer and satisfies the single MRG $X_n = (a_1 X_{n-1} + \cdots + a_k X_{n-k}) \bmod m$ (L'Ecuyer and Tezuka 1991 for $k = 1$, L'Ecuyer 1996 in general). The proof page derives it. The actual output $u_n = z_n/m_1$ differs from $w_n$ by an amount that is small when the moduli are close: for $J = 2$ and $\delta = (1, -1)$, $u_n - w_n \equiv x_{2,n} (m_1 - m_2) / (m_1 m_2) \pmod 1$, of size less than $(m_1 - m_2)/m_1$.

## Example

Take two LCGs, $x_{1,n} = 3 x_{1,n-1} \bmod 31$ and $x_{2,n} = 2 x_{2,n-1} \bmod 29$, with seeds 1 and 5 and $\delta = (1, -1)$. Here 3 is a [primitive root](/primitive-root/) modulo 31 and 2 is one modulo 29, so the components have periods 30 and 28. The equivalent LCG has modulus $899 = 31 \cdot 29$ and multiplier $a = 437$, since $437 \equiv 3 \pmod{31}$ and $437 \equiv 2 \pmod{29}$; it is seeded with $X_0 = (29 \cdot 1 - 31 \cdot 5) \bmod 899 = 773$.

| $n$ | $x_{1,n}$ | $x_{2,n}$ | $z_n$ | $z_n / 31$ | $X_n = 437 X_{n-1} \bmod 899$ | $w_n = X_n / 899$ |
|---|---|---|---|---|---|---|
| 1 | 3 | 10 | 24 | 0.7742 | 676 | 0.7519 |
| 2 | 9 | 20 | 20 | 0.6452 | 540 | 0.6007 |
| 3 | 27 | 11 | 16 | 0.5161 | 442 | 0.4917 |
| 4 | 19 | 22 | 28 | 0.9032 | 768 | 0.8543 |
| 5 | 26 | 15 | 11 | 0.3548 | 289 | 0.3215 |
| 6 | 16 | 1 | 15 | 0.4839 | 433 | 0.4816 |

In every row $w_n$ is exactly $(x_{1,n}/31 - x_{2,n}/29) \bmod 1$; for example at $n = 1$, $3/31 - 10/29 = -223/899$, and $-223/899 + 1 = 676/899$. The combined state returns to its start after $\operatorname{lcm}(30, 28) = 420$ steps. With these tiny moduli $z_n/31$ and $w_n$ differ by up to $2/31$; with $m_1 - m_2 = 164$ as in the 1988 generator the difference is below $10^{-7}$.

**The 1988 generator.** $m_1 = 2147483563$, $a_1 = 40014$, $m_2 = 2147483399$, $a_2 = 40692$, output $z = (x_1 - x_2) \bmod (m_1 - 1)$ with 0 replaced by $m_1 - 1$. Both multipliers are primitive roots (the prime factors of $m_1 - 1$ are 2, 3, 7, 631, 81031, and those of $m_2 - 1$ are 2, 19, 31, 1019, 1789), and $\gcd(m_1 - 1, m_2 - 1) = 2$, so the period is $(m_1 - 1)(m_2 - 1)/2 = 2305842648436451838 \approx 2.3 \cdot 10^{18}$.

**MRG32k3a.** $m_1 = 2^{32} - 209$, $x_{1,n} = (1403580\, x_{1,n-2} - 810728\, x_{1,n-3}) \bmod m_1$; $m_2 = 2^{32} - 22853$, $x_{2,n} = (527612\, x_{2,n-1} - 1370589\, x_{2,n-3}) \bmod m_2$; $z_n = (x_{1,n} - x_{2,n}) \bmod m_1$. Both characteristic polynomials are primitive, $\gcd(m_1^3 - 1, m_2^3 - 1) = 2$, and the period is $(m_1^3 - 1)(m_2^3 - 1)/2 \approx 3.1 \cdot 10^{57} \approx 2^{191}$. From the seed with all six values 12345, exact integer arithmetic gives $z_1 = 545508589$, so $u_1 \approx 0.1270111220$.

## Correctness

The proof page shows three facts. First, each component computes its MRG and the output is the stated sum, by direct reading of lines L1 to L6. Second, $X_n = m w_n$ satisfies one MRG modulo $m = \prod m_j$: $X_n \equiv \delta_j (m/m_j) x_{j,n} \pmod{m_j}$, so modulo each $m_j$ it obeys the recurrence of component $j$, and by the Chinese remainder theorem it obeys the recurrence with the combined coefficients modulo $m$. Third, the combined state sequence is purely periodic with period $\operatorname{lcm}_j \rho_j$, where $\rho_j$ is the period of component $j$; when each component has a primitive characteristic polynomial and a nonzero seed, $\rho_j = m_j^k - 1$. These are all even, so the period is at most $\prod_j (m_j^k - 1) / 2^{J-1}$, with equality when the numbers $(m_j^k - 1)/2$ are pairwise coprime.

## Complexity

Each output costs, for each of the $J$ components, $k$ multiplications and a reduction modulo $m_j$, plus $J$ additions and one reduction modulo $m_1$: $\Theta(J k)$ word operations, a constant for a fixed design ($J = 2$, $k = 3$ for MRG32k3a, with two of the six coefficients zero). Space is $J k$ words. MRG32k3a is several times slower than xorshift-type generators but fast enough for most simulations.

## Properties

- **Period.** The period is $\operatorname{lcm}$ of the component periods, about $2^{191}$ for MRG32k3a with words of 32 bits.
- **Analyzable lattice.** Because the output is close to that of one MRG modulo $\prod m_j$, its $d$-tuples lie in a lattice with determinant of order $\prod m_j$; MRG32k3a's parameters were chosen by the spectral test over many dimensions.
- **Streams.** Each component is linear, so [jump-ahead](/jump-ahead/) by a matrix power modulo $m_j$ moves the combined state; RngStreams spaces streams $2^{127}$ apart.
- **Statistical tests.** MRG32k3a passes the batteries of TestU01, including BigCrush (L'Ecuyer and Simard 2007). This is an empirical result, not a theorem.
- **Not cryptographic.** The equivalent MRG is linear; a few outputs determine the state.

## Variants and improvements

- **Wichmann-Hill (1982).** Three multiplicative LCGs with moduli 30269, 30307 and 30323, combined by $u_n = (x_1/m_1 + x_2/m_2 + x_3/m_3) \bmod 1$, the exact $w_n$ form; by the same theorem it is an LCG modulo their product, about $2.8 \cdot 10^{13}$.
- **MRG31k3p, MRG32k5a, MRG63k3a.** Other combined MRGs by L'Ecuyer and coauthors with different word sizes and orders.
- **Combined Tausworthe generators.** The same idea over $\mathbb{F}_2$: exclusive-or of several LFSR generators gives an $\mathbb{F}_2$-linear generator whose characteristic polynomial is the product of the components' polynomials when these are pairwise coprime (L'Ecuyer 1996 for maximally equidistributed versions).
- **Shuffling.** Bays-Durham shuffling of one LCG's output by another generator, used in Numerical Recipes' ran2 together with the 1988 combination, is a different and less analyzable way to combine.

## When to use it

MRG32k3a remains a standard choice for simulation software that needs many reproducible, provably long, independent streams, such as discrete-event simulation packages and the RngStreams library. Choose it when the generator's structure must be documented and analyzable and speed is secondary. For raw speed choose [xoshiro](/xoshiro-xoroshiro/) or [PCG](/pcg-random/); for parallel work in random order, [Philox](/philox/); for anything security-related, a [cryptographic generator](/cryptographically-secure-prng/).

## Pitfalls

- **Combining is not automatically good.** The theorem says the combination is one big linear generator; its quality depends on the combined coefficients, which must be checked by the spectral test. Arbitrary components can give a poor lattice.
- **Weights and moduli.** The moduli must be distinct primes (pairwise coprime at least) and each $\delta_j$ coprime to $m_j$; otherwise the CRT argument and the period formula fail.
- **Overflow.** In double precision, $a \cdot x$ must stay below $2^{53}$, which is why MRG32k3a's coefficients are small; changing a coefficient without checking the bound breaks exactness.
- **Zero output.** $z_n = 0$ occurs; map it inside $(0, 1)$ when the output feeds a logarithm or an inverse distribution function.
- **Seeding.** Each component's seed must not be the zero vector, and must be below its modulus; seeds of the form all-12345 are conventional defaults, not random.

## Implementations

## History

Wichmann and Hill published a three-component combination in 1982. L'Ecuyer (1988) gave a portable combination of two LCGs near $2^{31}$ with period about $2.3 \cdot 10^{18}$. L'Ecuyer and Tezuka (1991) proved that such combinations are close to one LCG with the product modulus, which explained both their good behavior and their limits. L'Ecuyer (1996) extended the theory to MRG components, and L'Ecuyer (1999) published MRG32k3a, chosen with the spectral test; with the RngStreams package of 2002 it became one of the most used generators in simulation software.

## References
