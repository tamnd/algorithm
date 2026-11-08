---
tag: 9VVSW8
kind: theorem
slug: marsaglia-hyperplane-theorem
name: Marsaglia's theorem on lattice structure
aliases:
- hyperplane theorem for LCGs
- random numbers fall mainly in the planes
area: numerical/random-number-generation
level: advanced
summary: For any LCG with modulus m, all overlapping d-tuples of consecutive outputs lie on at most (d! m)^(1/d) parallel hyperplanes of the unit cube.
prereqs: [linear-congruential-generator, lattice, minkowski-theorem]
see_also: [spectral-test, randu, hull-dobell-theorem, lattice-basis-reduction, shortest-vector-problem, equidistribution, multiple-recursive-generator]
sources:
  - paper: "George Marsaglia, Random numbers fall mainly in the planes, Proceedings of the National Academy of Sciences 61(1), 1968, pages 25 to 28"
    locator: the theorem bounding the number of parallel hyperplanes by (n! m)^(1/n), and the table of bounds for m = 2^32
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.3.4, The spectral test (the lattice of points, the distance 1/ν_t between hyperplanes, and the discussion of RANDU)
  - paper: "Pierre L'Ecuyer, Uniform random number generation, Annals of Operations Research 53, 1994, pages 77 to 120"
    locator: the section on the lattice structure of linear congruential and multiple recursive generators
---

Marsaglia's theorem says that the points formed by $d$ consecutive outputs of a [linear congruential generator](/linear-congruential-generator/) are not spread through the unit cube: they all lie on a small family of parallel hyperplanes, at most $(d!\, m)^{1/d}$ of them, where $m$ is the modulus. For $m = 2^{32}$ and $d = 3$ the bound is 2953 planes, and for $d = 10$ it is 41. The proof is a short application of [Minkowski's theorem](/minkowski-theorem/) to a lattice of index $m$. The theorem holds for every multiplier, so no choice of $a$ removes the structure; a choice of $a$ can only make the planes more numerous and closer together, which is what the [spectral test](/spectral-test/) measures.

## Statement

Fix integers $m \ge 2$, $a$ and $c$, and a dimension $d \ge 1$. Let $s_{i+1} = (a s_i + c) \bmod m$ with any seed $s_0 \in \{0, \ldots, m-1\}$, let $u_i = s_i / m$, and let $P_i = (u_i, u_{i+1}, \ldots, u_{i+d-1}) \in [0, 1)^d$ be the overlapping $d$-tuples.

**Theorem (Marsaglia 1968).** There is a nonzero integer vector $k = (k_1, \ldots, k_d)$ with
$$K = |k_1| + \cdots + |k_d| \le (d!\, m)^{1/d}$$
such that every point $P_i$, for every $i \ge 0$, lies on one of at most $K$ parallel hyperplanes $k_1 x_1 + \cdots + k_d x_d = \beta$. The hyperplanes are those of this form that meet $[0,1)^d$ with $\beta$ in a fixed residue class $\beta \equiv \beta_0 \pmod 1$, so consecutive ones are at Euclidean distance $1 / \lVert k \rVert_2$.

The key fact is the lattice $L = \{ k \in \mathbb{Z}^d : k_1 + k_2 a + \cdots + k_d a^{d-1} \equiv 0 \pmod m \}$: every $k \in L \setminus \{0\}$ gives such a family, and the theorem is the statement that $L$ has a nonzero vector of small 1-norm.

## In plain words

Take three numbers in a row from a linear congruential generator and use them as the coordinates of a point in a cube. Do this many times. The points do not fill the cube like a fine mist. They lie on a stack of flat parallel sheets, with empty space between the sheets. The theorem says how few sheets can be enough: the count grows only like the cube root of the modulus when the points have three coordinates, and like a smaller root in more dimensions.

The reason is that each output is a fixed multiple of the one before, up to a wrap-around. So a small whole-number combination of consecutive outputs can only take a few values, and each value is one sheet.

## Proof

**Step 1: $L$ is a lattice of index $m$.** The map $\varphi(k) = (k_1 + k_2 a + \cdots + k_d a^{d-1}) \bmod m$ is a group homomorphism from $\mathbb{Z}^d$ onto $\mathbb{Z}/m\mathbb{Z}$; it is onto because $\varphi(t, 0, \ldots, 0) = t \bmod m$. Its kernel is $L$, so $L$ is a full-rank sublattice of $\mathbb{Z}^d$ with $[\mathbb{Z}^d : L] = m$, and $\det L = m$.

**Step 2: a short vector exists.** The cross-polytope $B_R = \{ x \in \mathbb{R}^d : |x_1| + \cdots + |x_d| \le R \}$ is convex, compact and symmetric about 0, with volume $2^d R^d / d!$. Take $R = (d!\, m)^{1/d}$, so the volume is $2^d m = 2^d \det L$. Minkowski's convex body theorem gives a nonzero point of $L$ in the interior of $(1 + \varepsilon) B_R$ for every $\varepsilon > 0$, since that body has volume larger than $2^d \det L$. There are finitely many lattice points in $2 B_R$, so one of them lies in $(1 + \varepsilon) B_R$ for a sequence of $\varepsilon \to 0$, hence in $B_R$. So some $k \in L$, $k \ne 0$, has $K = \sum_j |k_j| \le (d!\, m)^{1/d}$.

**Step 3: the tuples satisfy a linear congruence.** By induction, $s_{i+j} \equiv a^j s_i + c\, S_j(a) \pmod m$, where $S_j(a) = 1 + a + \cdots + a^{j-1}$ and $S_0 = 0$. For $k \in L$:
$$\sum_{j=1}^{d} k_j s_{i+j-1} \equiv s_i \sum_{j=1}^{d} k_j a^{j-1} + c \sum_{j=1}^{d} k_j S_{j-1}(a) \equiv \gamma \pmod m,$$
where $\gamma = c \sum_j k_j S_{j-1}(a) \bmod m$ does not depend on $i$. So $k \cdot (s_i, \ldots, s_{i+d-1}) = \gamma + t_i m$ for some integer $t_i$, which means $k \cdot P_i = \gamma / m + t_i$.

**Step 4: few values of $t_i$.** Let $N = \sum_{k_j < 0} |k_j|$ and $Q = \sum_{k_j > 0} k_j$, so $N + Q = K$. Since $0 \le s \le m - 1$, the integer $k \cdot (s_i, \ldots, s_{i+d-1})$ lies in $[-(m-1) N, (m-1) Q]$, a closed interval of length $(m-1) K$. Integers of the form $\gamma + t m$ in an interval of length $\ell$ are at most $\lfloor \ell / m \rfloor + 1$ in number, and $\lfloor (m-1) K / m \rfloor + 1 \le K$ because $(m-1) K / m < K$. So $t_i$ takes at most $K$ values, and each value is one hyperplane $k \cdot x = \gamma/m + t$. Two hyperplanes $k \cdot x = \beta$ and $k \cdot x = \beta + 1$ are $1 / \lVert k \rVert_2$ apart. $\blacksquare$

The proof uses nothing about $a$, $c$ or the seed. It does not need full period, and it covers every overlapping tuple, so it holds for the whole output stream, not only for a sample.

## Consequences

- **Bounds for common moduli.** The values of $\lfloor (d!\, m)^{1/d} \rfloor$ are:

  | $m$ | $d = 2$ | $d = 3$ | $d = 4$ | $d = 5$ | $d = 6$ | $d = 8$ | $d = 10$ |
  |---|---|---|---|---|---|---|---|
  | $2^{31}$ | 65536 | 2344 | 476 | 191 | 107 | 55 | 38 |
  | $2^{32}$ | 92681 | 2953 | 566 | 220 | 120 | 60 | 41 |
  | $2^{48}$ | 23726566 | 119086 | 9065 | 2021 | 766 | 240 | 126 |
  | $2^{64}$ | 6074000999 | 4801279 | 145055 | 18578 | 4866 | 963 | 382 |

  A simulation that uses outputs in groups of 10 from a 32-bit LCG gets points on at most 41 hyperplanes of the 10-dimensional cube, with gaps that no choice of multiplier can close.
- **RANDU.** For $a = 65539 = 2^{16} + 3$ and $m = 2^{31}$, $a^2 \equiv 6a - 9 \pmod{2^{31}}$, so $k = (9, -6, 1) \in L$ with $K = 16$. Every triple satisfies $9 u_i - 6 u_{i+1} + u_{i+2} = t$ with $t$ an integer in the open interval $(-6, 10)$, so the triples lie on the 15 planes $t = -5, \ldots, 9$, about $1/\sqrt{118} \approx 0.092$ apart. A run of 200000 triples from seed 1 meets all 15. See [RANDU](/randu/).
- **The spectral test.** The theorem gives an upper bound on the number of hyperplanes in the best family. The quantity that matters for a given $a$ is the maximal distance between adjacent hyperplanes over all families, $1/\nu_d$, where $\nu_d$ is the length of the shortest nonzero vector of $L$ in the Euclidean norm. The [spectral test](/spectral-test/) computes $\nu_d$ by [lattice basis reduction](/lattice-basis-reduction/), and good multipliers are chosen to make $\nu_d$ large for $d$ up to 8 or so.
- **Other linear generators.** The same argument applies to [multiple recursive generators](/multiple-recursive-generator/) and to combined LCGs, whose tuples also lie in a shifted lattice; a larger modulus makes the bound, and the actual gaps, smaller. It does not apply to generators that are linear over $\mathbb{F}_2$ such as the Mersenne Twister, whose analogue is the theory of [equidistribution](/equidistribution/).
- **What it rules out.** An LCG with modulus $m$ cannot give good $d$-dimensional uniformity at a resolution finer than about $(d!\, m)^{-1/d}$ along some direction. For $m = 2^{64}$ and $d = 6$ this resolution is about $1/4866$.

## Tightness

- **The bound is nearly attained in two dimensions.** Over all multipliers $2 \le a < m$, the largest value of the least $K$ is 44 for $m = 1009$ (bound 44.9), 90 for $m = 4096$ (bound 90.5) and 361 for $m = 65537$ (bound 362.04), found by exhaustive search. So the constant $(d!)^{1/d}$ cannot be lowered much for $d = 2$, and the exponent $1/d$ is the right one: good multipliers are the ones that come close to the bound.
- **Bad multipliers do much worse than the bound.** RANDU has 15 planes in dimension 3 where the bound allows 2344. The multiplier $a = 1$ puts all pairs on the $2$ lines $x_2 - x_1 = \beta$ for $c \ne 0$.
- **A small case.** For $m = 101$, $a = 10$, $c = 0$, the pairs $(s_i, s_{i+1})$ satisfy $10 s_i - s_{i+1} = 101\, t$ with $t \in \{0, \ldots, 9\}$, so all 100 nonzero states give pairs on 10 lines. The best vector in $L$ has $K = 11$ (for example $k = (10, -1)$), and the theorem's bound is $\lfloor \sqrt{202} \rfloor = 14$.
- **The count $K$ can exceed the number of planes used.** Step 4 counts the possible values of $t_i$; the generator may use fewer of them, as both examples above show.

## History

Marsaglia published the theorem in 1968 under the title "Random numbers fall mainly in the planes", as a warning about multiplicative congruential generators then in wide use for Monte Carlo work in several dimensions. RANDU became the standard illustration of the effect. The lattice view had been developed in the spectral test of Coveyou and MacPherson (1967), which Knuth treats in Section 3.3.4. Since then, LCG multipliers have been published with their spectral test figures rather than with full-period conditions alone.

## References
