---
tag: E6QYBH
kind: theorem
slug: johnson-lindenstrauss-lemma
name: Johnson-Lindenstrauss lemma
aliases:
- JL lemma
- Johnson-Lindenstrauss flattening
- Johnson-Lindenstrauss flattening lemma
area: machine-learning/dimensionality-reduction
level: core
summary: "Any n points in Euclidean space map linearly into k = O(log n / eps^2) dimensions with all squared distances kept within a factor 1 +/- eps."
prereqs: [concentration-of-measure, union-bound, moment-generating-function, markov-inequality]
see_also: [random-projection, sparse-random-projection, fast-johnson-lindenstrauss-transform, johnson-lindenstrauss-optimality, embedding, approximate-nearest-neighbor, ams-sketch, principal-component-analysis]
sources:
  - paper: doi:10.1090/conm/026/737400
    title: William B. Johnson and Joram Lindenstrauss, Extensions of Lipschitz mappings into a Hilbert space, Contemporary Mathematics 26, American Mathematical Society, 1984, pages 189 to 206
    locator: the lemma on the projection of n points to a random subspace of dimension O(log n / eps^2), used to extend Lipschitz maps
  - paper: doi:10.1002/rsa.10073
    title: Sanjoy Dasgupta and Anupam Gupta, An elementary proof of a theorem of Johnson and Lindenstrauss, Random Structures and Algorithms 22(1), 2003, pages 60 to 65
    locator: Theorem 2.1 (k >= 4 (eps^2/2 - eps^3/3)^(-1) ln n, success probability at least 1/n) and Lemma 2.2 (the tail bounds)
  - book: isbn:9780387953731
    title: Jiří Matoušek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 15, Section 15.2 (the Johnson-Lindenstrauss flattening lemma)
  - paper: doi:10.1016/0095-8956(88)90043-3
    title: Peter Frankl and Hiroshi Maehara, The Johnson-Lindenstrauss lemma and the sphericity of some graphs, Journal of Combinatorial Theory, Series B 44(3), 1988, pages 355 to 362
    locator: a shorter proof with an explicit constant
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998, pages 604 to 613
    locator: the dimension reduction with a matrix of independent Gaussian entries
---

The Johnson-Lindenstrauss lemma states that any $n$ points in the Euclidean space $\mathbb{R}^d$ can be mapped into $\mathbb{R}^k$ with $k = O(\varepsilon^{-2} \log n)$ so that each pairwise distance changes by a factor of at most $1 \pm \varepsilon$. The target dimension $k$ does not depend on $d$. A random linear map, a [random projection](/random-projection/), has this property with positive probability, and the proof below gives the explicit constant $k \ge 4(\varepsilon^2/2 - \varepsilon^3/3)^{-1} \ln n$ of Dasgupta and Gupta. The bound on $k$ is optimal up to a constant factor; see [Johnson-Lindenstrauss optimality](/johnson-lindenstrauss-optimality/).

## Statement

Notation: $n$ is the number of points, $d$ is the input dimension, $k$ is the target dimension, $\|\cdot\|$ is the Euclidean norm, and $\ln$ is the natural logarithm. There is no learning model here: the points are fixed and arbitrary, and the only randomness is in the map.

**Theorem (Johnson and Lindenstrauss 1984; constant of Dasgupta and Gupta 2003).** Let $0 < \varepsilon < 1$, let $n \ge 2$, and let $k$ be an integer with

$$k \ge \frac{4 \ln n}{\varepsilon^2/2 - \varepsilon^3/3}.$$

For every set $V$ of $n$ points in $\mathbb{R}^d$ there is a linear map $f : \mathbb{R}^d \to \mathbb{R}^k$ such that for all $u, v \in V$

$$(1 - \varepsilon)\,\|u - v\|^2 \;\le\; \|f(u) - f(v)\|^2 \;\le\; (1 + \varepsilon)\,\|u - v\|^2 .$$

Moreover, let $R$ be a $k \times d$ matrix of independent standard normal entries and $f(x) = R x / \sqrt{k}$. Then $f$ has this property with probability at least $1/n$.

**Distributional form.** For each fixed $x \in \mathbb{R}^d$, the same random $f$ satisfies

$$\Pr\big[\, \big|\, \|f(x)\|^2 - \|x\|^2 \,\big| > \varepsilon \|x\|^2 \,\big] \;\le\; 2 \exp\!\Big(-\frac{k}{2}\Big(\frac{\varepsilon^2}{2} - \frac{\varepsilon^3}{3}\Big)\Big).$$

The statement is about squared distances. Since $\sqrt{1 - \varepsilon} \ge 1 - \varepsilon$ and $\sqrt{1 + \varepsilon} \le 1 + \varepsilon$, the distances themselves change by a factor in $[1 - \varepsilon, 1 + \varepsilon]$ as well.

## In plain words

You have a set of points described by very many numbers each. You want to describe each point with far fewer numbers, and you still want the distance between any two points to stay almost the same. The lemma says this is always possible. The number of new coordinates you need grows only with the logarithm of the number of points, and it does not depend on how many coordinates the points had at the start.

A random map does the job. Each new coordinate is a random weighted sum of the old coordinates. For one fixed pair of points, the new distance is close to the old one with a probability very near one. Because the failure chance for each pair is tiny, all pairs are fine at the same time with positive probability.

## Proof

The proof is the Gaussian form of the argument of Dasgupta and Gupta. Write $c_\varepsilon = \varepsilon^2/2 - \varepsilon^3/3$. For $0 < \varepsilon < 1$ we have $\varepsilon/3 < 1/2$, so $c_\varepsilon > 0$.

**Step 1 (reduce to one unit vector).** The map $f$ is linear, so $f(u) - f(v) = f(u - v)$. For $w \ne 0$, linearity also gives $\|f(w)\|^2 / \|w\|^2 = \|f(w / \|w\|)\|^2$. So the pair $u, v$ is good exactly when the unit vector $x = (u - v)/\|u - v\|$ satisfies $1 - \varepsilon \le \|f(x)\|^2 \le 1 + \varepsilon$. (Equal points are always good.)

**Step 2 (the law of the image).** Fix a unit vector $x$. The $i$-th coordinate of $Rx$ is $Z_i = \sum_{j} R_{ij} x_j$, a sum of independent normal variables, so $Z_i \sim N(0, \sum_j x_j^2) = N(0, 1)$. Different coordinates use different rows of $R$, so $Z_1, \ldots, Z_k$ are independent. Hence $k \|f(x)\|^2 = \sum_{i=1}^k Z_i^2$ is a chi-square variable with $k$ degrees of freedom, with mean $k$.

**Step 3 (the moment generating function).** For $Z \sim N(0, 1)$ and $t < 1/2$,

$$\mathbb{E}\, e^{t Z^2} = \int_{-\infty}^{\infty} \frac{1}{\sqrt{2\pi}}\, e^{-(1 - 2t) z^2 / 2}\, dz = (1 - 2t)^{-1/2},$$

by the substitution $z' = \sqrt{1 - 2t}\, z$. By independence, $\mathbb{E}\, e^{t \sum Z_i^2} = (1 - 2t)^{-k/2}$.

**Step 4 (two facts about the logarithm).**
(a) $\ln(1 + \varepsilon) \le \varepsilon - \varepsilon^2/2 + \varepsilon^3/3$ for $\varepsilon \ge 0$. Let $g(\varepsilon)$ be the right side minus the left side. Then $g(0) = 0$ and $g'(\varepsilon) = 1 - \varepsilon + \varepsilon^2 - \frac{1}{1 + \varepsilon} = \frac{\varepsilon^3}{1 + \varepsilon} \ge 0$.
(b) $\ln(1 - \varepsilon) \le -\varepsilon - \varepsilon^2/2$ for $0 \le \varepsilon < 1$. Let $h(\varepsilon) = -\varepsilon - \varepsilon^2/2 - \ln(1 - \varepsilon)$. Then $h(0) = 0$ and $h'(\varepsilon) = -1 - \varepsilon + \frac{1}{1 - \varepsilon} = \frac{\varepsilon^2}{1 - \varepsilon} \ge 0$.

**Step 5 (upper tail).** Let $S = \sum_{i=1}^k Z_i^2$. For $0 < t < 1/2$, [Markov's inequality](/markov-inequality/) applied to $e^{tS}$ gives

$$\Pr[S \ge (1 + \varepsilon) k] \le \frac{\mathbb{E}\, e^{tS}}{e^{t(1 + \varepsilon)k}} = \Big( (1 - 2t)^{-1/2} e^{-t(1 + \varepsilon)} \Big)^k .$$

Take $t = \frac{\varepsilon}{2(1 + \varepsilon)}$, so $1 - 2t = \frac{1}{1 + \varepsilon}$. The bound becomes $\big((1 + \varepsilon)^{1/2} e^{-\varepsilon/2}\big)^k = \exp\big(\frac{k}{2}(\ln(1 + \varepsilon) - \varepsilon)\big)$, and by fact (a) this is at most $\exp(-\frac{k}{2} c_\varepsilon)$.

**Step 6 (lower tail).** For $t > 0$, Markov's inequality applied to $e^{-tS}$, with $\mathbb{E}\, e^{-tZ^2} = (1 + 2t)^{-1/2}$ from Step 3, gives

$$\Pr[S \le (1 - \varepsilon) k] \le \Big( (1 + 2t)^{-1/2} e^{t(1 - \varepsilon)} \Big)^k .$$

Take $t = \frac{\varepsilon}{2(1 - \varepsilon)}$, so $1 + 2t = \frac{1}{1 - \varepsilon}$. The bound becomes $\exp\big(\frac{k}{2}(\ln(1 - \varepsilon) + \varepsilon)\big)$, and by fact (b) this is at most $\exp(-k\varepsilon^2/4) \le \exp(-\frac{k}{2} c_\varepsilon)$, because $\varepsilon^3/3 > 0$. Steps 5 and 6 prove the distributional form.

**Step 7 (union bound).** If $k \ge 4 \ln n / c_\varepsilon$, then $\exp(-\frac{k}{2} c_\varepsilon) \le \exp(-2 \ln n) = n^{-2}$. So one pair is bad with probability at most $2/n^2$. There are $n(n-1)/2$ pairs, and by the [union bound](/union-bound/) some pair is bad with probability at most $\frac{n(n-1)}{2} \cdot \frac{2}{n^2} = 1 - \frac{1}{n}$. So all pairs are good with probability at least $1/n > 0$, and a map $f$ with the property exists. $\square$

The same computation with $k \ge (4 + 2\beta)\, c_\varepsilon^{-1} \ln n$ for some $\beta > 0$ makes each tail at most $n^{-2-\beta}$, so all pairs are good with probability at least $1 - n^{-\beta}$.

## Consequences

**The numbers.** The table gives the least $k$ of the theorem, $\lceil 4 \ln n / c_\varepsilon \rceil$.

| $n$ | $\varepsilon = 0.1$ | $\varepsilon = 0.2$ | $\varepsilon = 0.3$ | $\varepsilon = 0.5$ |
|---|---|---|---|---|
| 100 | 3948 | 1063 | 512 | 222 |
| 1000 | 5921 | 1595 | 768 | 332 |
| $10^6$ | 11842 | 3189 | 1536 | 664 |
| $10^9$ | 17763 | 4783 | 2303 | 995 |

For small $\varepsilon$ the bound is about $8 \varepsilon^{-2} \ln n$. It pays off only when $k$ is well below both $d$ and $n - 1$: any $n$ points already lie in an affine subspace of dimension $n - 1$, where an exact isometric map exists. For $n = 1000$ and $\varepsilon = 0.1$ the lemma asks for 5921 dimensions, more than the 999 that suffice exactly.

**A seeded check.** Take 30 points with independent $N(0,1)$ coordinates in $\mathbb{R}^{300}$ (Python `random.Random(42)`), and $\varepsilon = 0.5$, so $k = \lceil 163.26 \rceil = 164$. With $R$ drawn from `random.Random(7)`, the ratio $\|f(u) - f(v)\|^2 / \|u - v\|^2$ over all 435 pairs lies between 0.755 and 1.216, inside $[0.5, 1.5]$. With the smaller $k = 100$ and $\varepsilon = 0.3$ (points from seed 43, $R$ from seed 8), 4 of the 435 pairs, 0.92%, fall outside $[0.7, 1.3]$. The distributional form bounds the expected fraction of bad pairs by $2 e^{-50 c_{0.3}} = 0.331$, so the bound is loose but valid.

**Inner products.** For unit vectors $u, v$, the identity $\langle a, b \rangle = (\|a + b\|^2 - \|a - b\|^2)/4$ and the distributional form applied to $u + v$ and $u - v$ give $|\langle f(u), f(v) \rangle - \langle u, v \rangle| \le \varepsilon (\|u + v\|^2 + \|u - v\|^2)/4 = \varepsilon$ when both events hold. So angles and dot products are kept up to an additive $\varepsilon$, which is what kernel methods, linear classifiers and [nearest neighbor search](/nearest-neighbor-search/) use.

**Uses.**
- The map is oblivious: it does not look at the points. So it can be drawn before the data arrive, applied to a stream, or applied to a query point that was not known in advance. This is the base of [random projection](/random-projection/) in machine learning and of the [AMS sketch](/ams-sketch/) view of the second moment.
- The cost of computing $Rx$ is $O(kd)$ per point. [Sparse random projection](/sparse-random-projection/) and the [fast Johnson-Lindenstrauss transform](/fast-johnson-lindenstrauss-transform/) lower this cost and keep the guarantee.
- Algorithms whose cost grows with the dimension, such as [approximate nearest neighbor](/approximate-nearest-neighbor/) search, clustering and least squares, can first reduce $d$ to $O(\varepsilon^{-2} \log n)$ and then run in the small space.
- Unlike [principal component analysis](/principal-component-analysis/), the lemma promises every pairwise distance, not the average squared error. PCA can be much better on data with a few strong directions, and much worse for some pairs.

## Tightness

- **The order $\varepsilon^{-2} \log n$ is optimal.** Larsen and Nelson (2017) found, for $\varepsilon$ larger than about $\min(n, d)^{-1/2}$, sets of $n$ points for which every map with this distortion, linear or not, needs $k = \Omega(\varepsilon^{-2} \log n)$. The details and the earlier bounds are on the page [Johnson-Lindenstrauss optimality](/johnson-lindenstrauss-optimality/).
- **The constant is not tight.** The constant 4 and the term $\varepsilon^3/3$ come from the proof. For one fixed vector, the chi-square tails decay like $e^{-k\varepsilon^2/4}$ for small $\varepsilon$, so the leading constant $8$ in $8 \varepsilon^{-2} \ln n$ is what this union bound method gives. A smaller constant needs a different argument.
- **The success probability $1/n$ is low.** The theorem only promises probability $1/n$ at the smallest $k$. Either check all pairs and draw again (expected $n$ draws at most), or take a slightly larger $k$ as in the remark after the proof.
- **Only Euclidean distances.** No such reduction holds for $\ell_1$: Brinkman and Charikar (2005) showed that some $n$-point subsets of $\ell_1$ need dimension $n^{\Omega(1/c^2)}$ for distortion $c$. The lemma is a property of $\ell_2$.

## History

Johnson and Lindenstrauss proved the lemma in 1984 as a step in a question about the extension of Lipschitz maps into a Hilbert space. Their map was the projection onto a uniformly random subspace of dimension $k$, scaled by $\sqrt{d/k}$. Frankl and Maehara (1988) gave a shorter proof with an explicit constant. Indyk and Motwani (1998) used a matrix of independent Gaussian entries, which is easier to sample than a random subspace, for approximate nearest neighbor search. Dasgupta and Gupta (1999 report, 2003 journal) gave the elementary proof with the constant $4 (\varepsilon^2/2 - \varepsilon^3/3)^{-1}$ that is used above. Achlioptas (2003) then showed that entries of $\pm 1$ suffice, which led to the [sparse random projections](/sparse-random-projection/).

## References
