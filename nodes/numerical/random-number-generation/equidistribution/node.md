---
tag: BAB267
kind: definition
slug: equidistribution
name: Equidistribution
aliases:
- k-distribution
- k-distributed to v-bit accuracy
- equidistributed sequence
area: numerical/random-number-generation
level: advanced
summary: A sequence is k-distributed when its k-tuples of consecutive values fill the cube evenly; for a generator, every pattern of the top v bits of k outputs occurs equally often per period.
prereqs: [uniform-distribution, generator-period, linear-feedback-shift-register]
see_also: [mersenne-twister, marsaglia-hyperplane-theorem, discrepancy, well-rng, xorshift, spectral-test, statistical-tests-for-randomness]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.5, What is a random sequence? (equidistributed, k-distributed and infinitely distributed sequences)
  - paper: "Makoto Matsumoto and Takuji Nishimura, Mersenne twister: a 623-dimensionally equidistributed uniform pseudo-random number generator, ACM Transactions on Modeling and Computer Simulation 8(1), 1998, pages 3 to 30"
    locator: the definition of k-distribution to v-bit accuracy, the bound k(v) at most the floor of the state dimension over v, and the result that MT19937 is 623-distributed to 32-bit accuracy
  - paper: "Pierre L'Ecuyer, Maximally equidistributed combined Tausworthe generators, Mathematics of Computation 65(213), 1996, pages 203 to 213"
    locator: the definition of maximally equidistributed generators and the resolution-wise test
  - paper: "François Panneton, Pierre L'Ecuyer and Makoto Matsumoto, Improved long-period generators based on linear recurrences modulo 2, ACM Transactions on Mathematical Software 32(1), 2006, pages 1 to 16"
    locator: the dimension gaps and their sum as a figure of merit
  - paper: "Hermann Weyl, Über die Gleichverteilung von Zahlen mod. Eins, Mathematische Annalen 77, 1916, pages 313 to 352"
    locator: the definition of uniform distribution modulo one and the criterion by exponential sums
---

Equidistribution measures how evenly a sequence of numbers fills space, one dimension at a time. A sequence in $[0, 1)$ is equidistributed when each interval gets its fair share of points, and $k$-distributed when the $k$-tuples of consecutive values fill the cube $[0, 1)^k$ evenly. For a periodic generator with $w$-bit outputs, the exact finite version asks that every pattern of the leading $v$ bits of $k$ consecutive outputs occur equally often over one [period](/generator-period/). For generators that are linear over $\mathbb{F}_2$ this property is decided by the rank of a binary matrix, which is how the Mersenne Twister's "623-dimensional equidistribution" is proved.

## Definition

**Real sequences (Weyl 1916; Knuth, Section 3.5).** A sequence $u_0, u_1, \ldots$ in $[0, 1)$ is *equidistributed* if for all $0 \le \alpha < \beta \le 1$,
$$\lim_{n \to \infty} \frac{1}{n} \#\{ i < n : \alpha \le u_i < \beta \} = \beta - \alpha.$$
It is *$k$-distributed* if the points $(u_i, u_{i+1}, \ldots, u_{i+k-1})$ are equidistributed in $[0, 1)^k$, that is, the limiting fraction of points in every box $\prod_j [\alpha_j, \beta_j)$ is $\prod_j (\beta_j - \alpha_j)$. It is *$\infty$-distributed* if it is $k$-distributed for every $k$. A $k$-distributed sequence is $j$-distributed for every $j \le k$.

**Periodic generators to $v$-bit accuracy (Matsumoto and Nishimura 1998).** Let $y_0, y_1, \ldots$ be a purely periodic sequence of $w$-bit integers with period $\rho$, and for $1 \le v \le w$ let $\operatorname{trunc}_v(y) = \lfloor y / 2^{w-v} \rfloor$ be the leading $v$ bits. The sequence is *$k$-distributed to $v$-bit accuracy* if each of the $2^{kv}$ tuples in $\{0, \ldots, 2^v - 1\}^k$ occurs as
$$\big(\operatorname{trunc}_v(y_i), \operatorname{trunc}_v(y_{i+1}), \ldots, \operatorname{trunc}_v(y_{i+k-1})\big), \quad 0 \le i < \rho,$$
the same number of times, except that the all-zero tuple may occur once fewer. The exception is there for generators whose state space $S = \mathbb{F}_2^e$ has the zero state removed, so that $\rho = 2^e - 1$. Write $k(v)$ for the largest such $k$.

**Bound and gaps.** If the generator has $e$ bits of state, then $k(v) \le \lfloor e / v \rfloor$, because $2^{kv} - 1$ distinct tuples must fit into at most $2^e$ states. The *dimension gap* at resolution $v$ is $\delta_v = \lfloor e / v \rfloor - k(v)$. A generator is *maximally equidistributed* if $\delta_v = 0$ for every $v = 1, \ldots, w$, and the sum $\Delta = \sum_v \delta_v$ is used as a figure of merit.

**Linear generators over $\mathbb{F}_2$.** Suppose $s_{i+1} = A s_i$ on $\mathbb{F}_2^e$ with period $2^e - 1$ (so $A$ cycles through all nonzero states), and $y_i = B s_i$ is linear. Let $M_{k,v}$ be the $kv \times e$ matrix sending $s_i$ to the leading $v$ bits of $y_i, \ldots, y_{i+k-1}$. Then the sequence is $k$-distributed to $v$-bit accuracy if and only if $M_{k,v}$ has rank $kv$. Indeed, if the rank is $kv$, every tuple has exactly $2^{e - kv}$ preimages in $\mathbb{F}_2^e$, and running over the nonzero states removes one preimage of the zero tuple; if the rank is smaller, some tuple has no preimage at all.

## Examples and non-examples

- **A maximal-length LFSR bit stream.** The [LFSR](/linear-feedback-shift-register/) with $P(x) = x^4 + x^3 + 1$ outputs the period-15 bit sequence `100010011010111`. Each of the 15 nonzero 4-bit windows occurs once and `0000` never does, so $k(1) = 4 = e$: maximally equidistributed at 1-bit resolution.
- **A gap.** Take the Galois form of the same LFSR and output the whole 4-bit state: $1, 2, 4, 8, 9, 11, 15, 7, 14, 5, 10, 13, 3, 6, 12$. Here $k(4) = 1$, $k(3) = 1$, $k(1) = 4$, but $k(2) = 1$ while the bound is $\lfloor 4/2 \rfloor = 2$: pairs of leading 2-bit values are not balanced. The gaps are $\delta_2 = 1$ and zero elsewhere, so $\Delta = 1$.
- **A full-period LCG is 1-distributed and no more.** The [LCG](/linear-congruential-generator/) $s_{i+1} = (5 s_i + 3) \bmod 16$ from seed 7 runs through $7, 6, 1, 8, 11, 10, 5, 12, 15, 14, 9, 0, 3, 2, 13, 4$, every 4-bit value once, so $k(4) = 1$. Already the leading bit fails in two dimensions: over the period the pairs $(0,0)$ and $(1,1)$ occur 5 times each and $(0,1)$ and $(1,0)$ only 3 times, so $k(1) = 1$. The [Hull-Dobell theorem](/hull-dobell-theorem/) guarantees 1-distribution, and [Marsaglia's theorem](/marsaglia-hyperplane-theorem/) explains why higher dimensions fail for any LCG with a modulus this small.
- **MT19937.** The Mersenne Twister has $e = 19937$ and is 623-distributed to 32-bit accuracy, which equals the bound $\lfloor 19937 / 32 \rfloor = 623$. It is not maximally equidistributed: Matsumoto and Nishimura report gaps at several lower resolutions $v$, and the WELL generators were designed to remove them.
- **Weyl sequence, equidistributed but not 2-distributed.** For irrational $\theta$, $u_i = i \theta \bmod 1$ is equidistributed (Weyl), but $u_{i+1} = (u_i + \theta) \bmod 1$, so the pairs lie on two line segments in the unit square. With $\theta = \sqrt 2$ and $10^5$ terms, the pairs of leading bits $(0,1)$ and $(1,0)$ each occur 41421 times and $(0,0)$ and $(1,1)$ about 8580 times each, far from the 25000 each that 2-distribution would give.
- **Non-example.** The sequence $0, \tfrac12, 0, \tfrac12, \ldots$ is not equidistributed: the interval $[\tfrac14, \tfrac12)$ gets no points.

## Related definitions

- **[Uniform distribution](/uniform-distribution/)** of a random variable is the probabilistic model; equidistribution is the deterministic property of a fixed sequence that makes it look like independent samples of that model, one marginal at a time.
- **[Discrepancy](/discrepancy/)** quantifies how far the empirical measure is from equidistribution in finitely many points. A sequence is equidistributed if and only if its star discrepancy tends to 0. Low-discrepancy sequences, such as the [Halton sequence](/halton-sequence/), are equidistributed in a fixed dimension but are deliberately not $k$-distributed for consecutive tuples.
- **Weyl's criterion.** A sequence is equidistributed if and only if $\frac1n \sum_{j<n} e^{2\pi i h u_j} \to 0$ for every nonzero integer $h$.
- **[Spectral test](/spectral-test/)** is the analogue for linear generators modulo a large integer: it measures the gaps between the hyperplanes that hold the $k$-tuples, instead of counting bit patterns.
- **Empirical tests.** Equidistribution is a provable property of the full period. [Statistical tests](/statistical-tests-for-randomness/) look at much shorter stretches and detect other defects; MT19937 is 623-distributed and still fails the linear complexity tests of TestU01.

## References
