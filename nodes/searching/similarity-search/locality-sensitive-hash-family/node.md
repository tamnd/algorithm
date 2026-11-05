---
tag: PVBNHA
kind: definition
slug: locality-sensitive-hash-family
name: Locality-sensitive hash family
aliases:
- LSH family
area: searching/similarity-search
level: core
summary: A family of hash functions in which near points collide with higher probability than far points.
prereqs: [c-approximate-nearest-neighbor, hash-function, metric-space]
see_also: [locality-sensitive-hashing, lsh-amplification, bit-sampling-lsh, minhash, random-hyperplane-lsh, e2lsh, p-stable-distribution, asymmetric-lsh]
sources:
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (the definition of a locality-sensitive family and the family of bit samples for the Hamming cube)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Section 3 (locality-sensitive families, the exponent ρ and the bit-sampling family with ρ ≤ 1/c)
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: Section 2 (a locality-sensitive hashing scheme for a similarity, and the fact that 1 − sim must then satisfy the triangle inequality)
  - paper: doi:10.1145/2578221
    title: Ryan O'Donnell, Yi Wu and Yuan Zhou, Optimal lower bounds for locality-sensitive hashing (except when q is tiny), ACM Transactions on Computation Theory 6(1), article 5, 2014
    locator: the main theorem (ρ ≥ 1/c − o(1) for the Hamming cube, and ρ ≥ 1/c² − o(1) for ℓ2, when p2 is not exponentially small in the dimension)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the table of known families and exponents, and the ball-carving family for ℓ2 with ρ = 1/c² + o(1))
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.6 The Theory of Locality-Sensitive Functions (the (d1, d2, p1, p2)-sensitive families) and Section 3.7 LSH Families for Other Distance Measures
---

A locality-sensitive hash family is a random [hash function](/hash-function/) whose chance of giving two points the same value goes down as the distance between them goes up: points within distance $r_1$ collide with probability at least $p_1$, and points at distance at least $r_2$ collide with probability at most $p_2 < p_1$. Indyk and Motwani defined it in 1998 as the building block of [locality-sensitive hashing](/locality-sensitive-hashing/), which solves the [$(c, r)$-near neighbor](/c-approximate-nearest-neighbor/) problem in time about $n^\rho$ with $\rho = \ln(1/p_1)/\ln(1/p_2)$. Each distance needs its own family: bit sampling for the Hamming distance, MinHash for the Jaccard distance, random hyperplanes for the angle, and random projections for the Euclidean distance.

## Definition

Let $(M, \delta)$ be a [metric space](/metric-space/), $U$ a set, and $\mathcal{H}$ a family of functions $h : M \to U$ with a probability distribution on it. Let $0 \le r_1 < r_2$ and $0 \le p_2 < p_1 \le 1$.

**Sensitive family.** $\mathcal{H}$ is $(r_1, r_2, p_1, p_2)$-*sensitive* if for all $x, y \in M$, with $h$ drawn from $\mathcal{H}$:

$$\delta(x, y) \le r_1 \implies \Pr[h(x) = h(y)] \ge p_1, \qquad \delta(x, y) \ge r_2 \implies \Pr[h(x) = h(y)] \le p_2.$$

Nothing is required for $r_1 < \delta(x, y) < r_2$. For the $(c, r)$-near neighbor problem one takes $r_1 = r$ and $r_2 = c r$ with $c > 1$.

**The exponent.** The quality of the family is

$$\rho = \frac{\ln(1/p_1)}{\ln(1/p_2)},$$

with $p_2 > 0$. Since $p_2 < p_1 \le 1$, $0 \le \rho < 1$. A smaller $\rho$ is better: [LSH](/locality-sensitive-hashing/) built from the family uses $O(n^{\rho}/p_1)$ hash tables and a query time of the same order, up to the cost of one hash.

**Similarity form.** For a similarity $\mathrm{sim} : M \times M \to [0, 1]$, Charikar calls $\mathcal{H}$ an *LSH scheme for* $\mathrm{sim}$ if $\Pr[h(x) = h(y)] = \mathrm{sim}(x, y)$ for all $x, y$. Such a scheme is $(r_1, r_2, 1 - r_1, 1 - r_2)$-sensitive for the distance $1 - \mathrm{sim}$.

**Asymmetric form.** For problems such as [maximum inner product search](/maximum-inner-product-search/), the data point and the query are hashed by two different functions $h$ and $g$, and the rules are on $\Pr[h(x) = g(q)]$. See [asymmetric LSH](/asymmetric-lsh/).

### A necessary condition

**Proposition.** If $\mathcal{H}$ is an LSH scheme for $\mathrm{sim}$, then $D(x, y) = 1 - \mathrm{sim}(x, y)$ satisfies the triangle inequality.

*Proof.* $D(x, y) = \Pr[h(x) \ne h(y)]$. If $h(x) \ne h(z)$, then $h(x) \ne h(y)$ or $h(y) \ne h(z)$. By the [union bound](/union-bound/), $\Pr[h(x) \ne h(z)] \le \Pr[h(x) \ne h(y)] + \Pr[h(y) \ne h(z)]$. $\square$

So a similarity such as the Dice coefficient, whose distance $1 - D$ breaks the triangle inequality (see [Jaccard similarity](/jaccard-similarity/)), has no LSH scheme in this exact form.

### Lower bounds on the exponent

For the Hamming cube $\{0, 1\}^d$ with $r_2 = c\, r_1$, O'Donnell, Wu and Zhou proved that each family has $\rho \ge 1/c - o(1)$, when $p_2$ is not exponentially small in $d$. Bit sampling has $\rho \le 1/c$, so it is optimal. For $\ell_2$ the same work gives $\rho \ge 1/c^2 - o(1)$, and Andoni and Indyk gave a family with $\rho = 1/c^2 + o(1)$. These bounds hold for data-independent families. Methods that adapt the hash to the data set reach smaller exponents.

## Examples and non-examples

| family | space and distance | $\Pr[h(x) = h(y)]$ | $\rho$ for $r_2 = c\,r_1$ |
|---|---|---|---|
| [bit sampling](/bit-sampling-lsh/): $h(x) = x_i$, $i$ uniform | $\{0,1\}^d$, Hamming $H$ | $1 - H(x,y)/d$ | at most $1/c$ |
| [MinHash](/minhash/): first element in a random order | sets, Jaccard distance $d_J$ | $1 - d_J(A, B)$ | depends on $r_1$ |
| [random hyperplane](/random-hyperplane-lsh/): $h(x) = \mathrm{sign}(g \cdot x)$, $g$ Gaussian | $\mathbb{R}^d$, angle $\theta$ | $1 - \theta(x,y)/\pi$ | depends on $r_1$ |
| [p-stable projection](/e2lsh/): $h(x) = \lfloor (a \cdot x + b)/w \rfloor$ | $\mathbb{R}^d$, $\ell_2$ | a decreasing function of $\|x - y\|$ | below $1/c$ for a good $w$ |

**Numbers.** In $\{0, 1\}^{100}$ with $r_1 = 10$ and $r_2 = 20$, bit sampling gives $p_1 = 0.9$, $p_2 = 0.8$ and $\rho = \ln(1/0.9)/\ln(1/0.8) \approx 0.4722 \le 1/2$. For angles $\pi/6$ and $\pi/3$, random hyperplanes give $p_1 = 5/6$, $p_2 = 2/3$ and $\rho \approx 0.4497$. For MinHash with $r_1 = 0.2$ and $r_2 = 0.6$ (similarity at least $0.8$ against at most $0.4$), $p_1 = 0.8$, $p_2 = 0.4$ and $\rho \approx 0.2435$.

**A random shift on the line.** On $\mathbb{R}$ let $h_b(x) = \lfloor (x + b)/w \rfloor$ with $b$ uniform in $[0, w)$. Two points at distance $u$ collide exactly when no multiple of $w$ falls between $x + b$ and $y + b$. Such a multiple falls in the interval with probability $\min(1, u/w)$, so $\Pr[h_b(x) = h_b(y)] = \max(0, 1 - u/w)$. For $r_1 = 1$, $r_2 = 2$ and $w = 4$ the family is $(1, 2, 0.75, 0.5)$-sensitive, with $\rho \approx 0.4150$.

**Non-example: a fixed grid.** Without the random shift, $h(x) = \lfloor x/w \rfloor$ puts $x = w - \varepsilon$ and $y = w$ in different cells for each $\varepsilon > 0$. So the collision probability of close points is 0, and the family is not $(r_1, r_2, p_1, p_2)$-sensitive for any $r_1 > 0$ and $p_1 > 0$. The randomness must be in the choice of the function, for each pair.

**Non-example: a random hash.** A universal hash family $\mathcal{H}$ gives $\Pr[h(x) = h(y)] \le 1/|U|$ for all $x \ne y$, near or far. Then $p_1 \le p_2$, so the family is not sensitive. [Universal hashing](/universal-hashing/) spreads keys apart on purpose; an LSH family keeps near keys together on purpose.

## Related definitions

- **[c-approximate nearest neighbor](/c-approximate-nearest-neighbor/)**: the problem that a sensitive family with $r_2 = c\, r_1$ solves through LSH.
- **[LSH amplification](/lsh-amplification/)**: the AND of $k$ functions gives a family with probabilities $(p_1^k, p_2^k)$ and the same $\rho$, since $\ln(1/p_1^k) / \ln(1/p_2^k) = \rho$; the OR of $L$ such functions then gives $(1 - (1 - p_1^k)^L, 1 - (1 - p_2^k)^L)$.
- **[p-stable distribution](/p-stable-distribution/)**: the distribution of the projection vector $a$ that makes the projection family work for $\ell_p$.
- **[Universal hashing](/universal-hashing/)**: the opposite goal, small collision probability for all distinct pairs.

## References
