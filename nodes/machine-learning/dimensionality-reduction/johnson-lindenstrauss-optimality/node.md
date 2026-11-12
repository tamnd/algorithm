---
tag: SJBGY3
kind: theorem
slug: johnson-lindenstrauss-optimality
name: Optimality of the Johnson-Lindenstrauss lemma
aliases:
- Johnson-Lindenstrauss lower bound
- Larsen-Nelson lower bound
area: machine-learning/dimensionality-reduction
level: research
summary: "Some n-point sets need Omega(eps^-2 log n) dimensions for distortion 1 + eps under any map, so the Johnson-Lindenstrauss bound is tight up to a constant."
prereqs: [johnson-lindenstrauss-lemma]
see_also: [embedding, random-projection, sparse-random-projection, fast-johnson-lindenstrauss-transform, probabilistic-method, restricted-isometry-property]
sources:
  - paper: arxiv:1609.02094
    title: Kasper Green Larsen and Jelani Nelson, Optimality of the Johnson-Lindenstrauss lemma, Proceedings of the 58th IEEE Symposium on Foundations of Computer Science (FOCS), 2017
    locator: Theorem 1 (for n, d >= 2 and 1/min(n, d)^0.4999 < eps < 1, some n-point set in R^d needs m = Omega(eps^-2 lg n) for every map, linear or not)
  - paper: doi:10.1016/S0012-365X(03)00227-9
    title: Noga Alon, Problems and results in extremal combinatorics I, Discrete Mathematics 273(1-3), 2003, pages 31 to 53
    locator: the section on low rank matrices with a large diagonal, which gives Omega(eps^-2 log n / log(1/eps)) for the simplex
  - paper: arxiv:1411.2404
    title: Kasper Green Larsen and Jelani Nelson, The Johnson-Lindenstrauss lemma is optimal for linear dimensionality reduction, Proceedings of the 43rd International Colloquium on Automata, Languages and Programming (ICALP), LIPIcs 55, 2016
    locator: the main theorem (an n^O(1)-point subset of R^n on which every linear map with distortion 1 + eps needs m = Omega(min(n, eps^-2 log n)))
  - book: isbn:9780387953731
    title: Jiří Matoušek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 15, Section 15.2 (the flattening lemma) and Section 15.3 (lower bounds by counting)
---

The [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/) maps any $n$ points into $k = O(\varepsilon^{-2} \log n)$ dimensions with distortion $1 + \varepsilon$. The optimality results show that this target dimension cannot be lowered by more than a constant factor. Alon (2003) proved a bound that is short by a factor $\log(1/\varepsilon)$ and holds for every map. Larsen and Nelson first closed the gap for linear maps (2016) and then for all maps (2017), for every $\varepsilon$ that is not tiny compared with $n$ and $d$. This page states the three results and proves Alon's bound in full.

## Statement

A map $f : X \to \mathbb{R}^k$ on a finite set $X \subset \mathbb{R}^d$ is an $\varepsilon$-embedding if for all $u, v \in X$

$$(1 - \varepsilon)\,\|u - v\|^2 \;\le\; \|f(u) - f(v)\|^2 \;\le\; (1 + \varepsilon)\,\|u - v\|^2 .$$

The map need not be linear, and it need not be defined outside $X$. Write $\log$ for any fixed base; the bounds hold up to constant factors.

**Theorem A (Larsen and Nelson 2017).** For all integers $n, d \ge 2$ and all $\varepsilon$ with $1/\min(n, d)^{0.4999} < \varepsilon < 1$, there is a set $X$ of $n$ points in $\mathbb{R}^d$ such that every $\varepsilon$-embedding of $X$ into $\mathbb{R}^k$ has $k = \Omega(\varepsilon^{-2} \log n)$.

**Theorem B (Alon 2003).** Let $X = \{0, e_1, \ldots, e_n\} \subset \mathbb{R}^n$, the standard simplex with its corner at the origin. For $n^{-1/2}/4 \le \varepsilon \le 1/16$, every $\varepsilon$-embedding of $X$ into $\mathbb{R}^k$ has $k = \Omega\big(\varepsilon^{-2} \log n / \log(1/\varepsilon)\big)$; explicitly,

$$k \;\ge\; \frac{\ln n}{256\, e\, \varepsilon^2 \ln(1/(4\varepsilon))} .$$

**Theorem C (Larsen and Nelson 2016).** For $n > 1$ and $0 < \varepsilon < 1/2$ there is a set of $n^{O(1)}$ points in $\mathbb{R}^n$ such that every linear $\varepsilon$-embedding into $\mathbb{R}^k$ has $k = \Omega(\min(n, \varepsilon^{-2} \log n))$.

The constants in Theorem B are the ones of the proof below; Alon states the bound up to a constant factor. The exponent $0.4999$ in Theorem A can be any constant below $1/2$.

## In plain words

The Johnson-Lindenstrauss lemma says that a fixed number of new coordinates, about the log of the number of points divided by the square of the allowed error, is always enough. These results show that you cannot do much better. There are point sets for which no map at all, simple or complex, can keep every distance within the error with fewer coordinates.

The simplest bad set is a corner of a cube: the origin and the unit points on each axis. All these points are at the same distance from each other, so their images must be almost at right angles. Space with few coordinates does not have room for many vectors that are all almost at right angles. Counting this room carefully gives a bound that misses the best one only by a small log factor.

## Proof

This is a full proof of Theorem B. Theorem A needs a longer argument; an outline follows the proof.

**Step 1 (almost orthogonal unit vectors).** Let $f$ be an $\varepsilon$-embedding of $X = \{0, e_1, \ldots, e_n\}$ with $\varepsilon \le 1/2$. Translate so that $f(0) = 0$; this keeps all differences. Let $z_i = f(e_i)$. Since $\|e_i\| = 1$ and $\|e_i - e_j\|^2 = 2$ for $i \ne j$,

$$1 - \varepsilon \le \|z_i\|^2 \le 1 + \varepsilon, \qquad 2(1 - \varepsilon) \le \|z_i - z_j\|^2 \le 2(1 + \varepsilon).$$

From $\langle z_i, z_j \rangle = \frac{1}{2}(\|z_i\|^2 + \|z_j\|^2 - \|z_i - z_j\|^2)$ we get $|\langle z_i, z_j \rangle| \le \frac{1}{2}\big(2(1 + \varepsilon) - 2(1 - \varepsilon)\big) = 2\varepsilon$. Let $w_i = z_i / \|z_i\|$. Then $|\langle w_i, w_j \rangle| \le 2\varepsilon/(1 - \varepsilon) \le 4\varepsilon$. Write $\delta = 4\varepsilon$.

So it suffices to bound the dimension $k$ of a space that holds $n$ unit vectors with all pairwise inner products at most $\delta$ in absolute value. Let $G$ be their Gram matrix, $G_{ij} = \langle w_i, w_j \rangle$. It is symmetric, $G_{ii} = 1$, $|G_{ij}| \le \delta$ for $i \ne j$, and $\operatorname{rank} G \le k$.

**Step 2 (rank lemma).** For a real symmetric matrix $A \ne 0$, $\operatorname{rank} A \ge (\operatorname{tr} A)^2 / \operatorname{tr}(A^2)$. Proof: let $\lambda_1, \ldots, \lambda_r$ be the nonzero eigenvalues, with $r = \operatorname{rank} A$. Then $\operatorname{tr} A = \sum \lambda_i$ and $\operatorname{tr}(A^2) = \sum \lambda_i^2$, and by the Cauchy-Schwarz inequality $(\sum \lambda_i)^2 \le r \sum \lambda_i^2$.

**Step 3 (entrywise powers have small rank).** For an integer $t \ge 1$ let $G^{\circ t}$ be the matrix with entries $G_{ij}^t$. Then $G_{ij}^t = \langle w_i^{\otimes t}, w_j^{\otimes t} \rangle$, where $w^{\otimes t}$ is the $t$-fold tensor power. Each $w_i^{\otimes t}$ is a symmetric tensor over $\mathbb{R}^k$, and the space of symmetric $t$-tensors has dimension $\binom{k + t - 1}{t}$, the number of monomials of degree $t$ in $k$ variables. A Gram matrix of vectors in a space of dimension $D$ has rank at most $D$, so

$$\operatorname{rank} G^{\circ t} \le \binom{k + t - 1}{t} \le \Big(\frac{e (k + t - 1)}{t}\Big)^t .$$

**Step 4 (entrywise powers have large rank).** $G^{\circ t}$ has diagonal 1 and off-diagonal entries of absolute value at most $\delta^t$. So $\operatorname{tr} G^{\circ t} = n$ and $\operatorname{tr}((G^{\circ t})^2) = \sum_{i,j} G_{ij}^{2t} \le n + n^2 \delta^{2t}$. By Step 2,

$$\operatorname{rank} G^{\circ t} \ge \frac{n^2}{n + n^2 \delta^{2t}} = \frac{n}{1 + n \delta^{2t}} .$$

Choose $t = \lfloor \ln n / (2 \ln(1/\delta)) \rfloor$. Then $\delta^{2t} \ge \delta^{\ln n / \ln(1/\delta)} = 1/n$, so $n \delta^{2t} \ge 1$ and the bound is at least $n / (2 n \delta^{2t}) = \delta^{-2t}/2$.

**Step 5 (combine).** Steps 3 and 4 give $\big(e(k + t - 1)/t\big)^t \ge \delta^{-2t}/2$. Take the $t$-th root and use $2^{-1/t} \ge 1/2$:

$$\frac{e (k + t - 1)}{t} \ge \frac{\delta^{-2}}{2}, \qquad\text{so}\qquad k \ge t \Big(\frac{\delta^{-2}}{2e} - 1\Big) + 1 .$$

**Step 6 (the constants).** Assume $n^{-1/2}/4 \le \varepsilon \le 1/16$, so $n^{-1/2} \le \delta \le 1/4$. Let $x = \ln n / (2 \ln(1/\delta))$. From $\delta \ge n^{-1/2}$ we get $x \ge 1$, and $\lfloor x \rfloor \ge x/2$ for every $x \ge 1$, so $t \ge \ln n / (4 \ln(1/\delta))$. From $\delta \le 1/4$ we get $\delta^{-2} \ge 16 \ge 4e$, so $\delta^{-2}/(2e) - 1 \ge \delta^{-2}/(4e)$. Hence

$$k \ge \frac{\ln n}{4 \ln(1/\delta)} \cdot \frac{1}{4 e \delta^2} = \frac{\ln n}{256\, e\, \varepsilon^2 \ln(1/(4\varepsilon))} . \qquad \square$$
**Outline of Theorem A (not a proof).** Larsen and Nelson use an encoding argument. They define a large family of point sets: the origin, basis vectors, and further points built as sparse combinations of the basis vectors. From an $\varepsilon$-embedding of such a set into $\mathbb{R}^k$, with the image vectors rounded to a fine grid, a decoder can find which basis vectors each further point uses, from the approximate inner products. So the rounded images, which take a number of bits proportional to $n k$ times a logarithmic factor, must tell apart all sets of the family. Counting the sets and comparing gives $k = \Omega(\varepsilon^{-2} \log n)$ when $\varepsilon$ is not too small. The paper gives the details.

## Consequences

- **Random projection is optimal.** A Gaussian or $\pm 1$ [random projection](/random-projection/) with $k = O(\varepsilon^{-2} \log n)$ dimensions meets the best possible bound up to a constant factor, even compared with nonlinear maps that see all the data. Data-dependent methods such as [principal component analysis](/principal-component-analysis/) cannot beat it on worst-case point sets.
- **Faster maps must keep $k$.** Work on [sparse random projection](/sparse-random-projection/) and the [fast Johnson-Lindenstrauss transform](/fast-johnson-lindenstrauss-transform/) lowers the time per point, not the target dimension, because the target dimension is already optimal.
- **Almost orthogonal vectors.** Steps 1 to 6 alone give a geometric fact: $n$ unit vectors in $\mathbb{R}^k$ with all pairwise inner products at most $\delta$ in absolute value need $k = \Omega(\delta^{-2} \log n / \log(1/\delta))$. Random unit vectors show that $k = O(\delta^{-2} \log n)$ suffices. This is the same counting that limits the coherence of matrices in [compressed sensing](/compressed-sensing/).
- **Linear maps on a fixed set.** Theorem C shows that a linear map cannot gain over the Gaussian map, even when it is chosen after seeing the points.

## Tightness

- **Upper and lower bounds match.** The lemma gives $k \le 4 (\varepsilon^2/2 - \varepsilon^3/3)^{-1} \ln n \approx 8 \varepsilon^{-2} \ln n$, and Theorem A gives $k \ge c\, \varepsilon^{-2} \log n$ for a constant $c > 0$. The best constant is not known.
- **Theorem A needs a richer set.** The rank argument loses the factor $\log(1/\varepsilon)$ on the simplex. Theorem A removes it with a different family of point sets and a counting argument, not with a sharper rank bound.
- **Small $\varepsilon$.** When $\varepsilon < 1/\sqrt{\min(n, d)}$, the term $\varepsilon^{-2} \log n$ exceeds $\min(n, d)$. Then the trivial map into the span of the points, of dimension at most $\min(n - 1, d)$, is exact and better. So the condition on $\varepsilon$ in Theorem A is close to necessary.
- **Distributional form.** For an oblivious random map that must keep the norm of each fixed vector with failure probability $\delta$, the dimension $\Theta(\varepsilon^{-2} \log(1/\delta))$ is needed and suffices (Jayram and Woodruff 2013; Kane, Meka and Nelson 2011). This is a different statement from Theorem A, which allows a map built for the specific set.

## History

Bounds on almost orthogonal vectors by Welch (1974) and Levenshtein (1983) imply limits of the same form as Theorem B. Alon (2003) gave the rank argument above and the bound $\Omega(\varepsilon^{-2} \log n / \log(1/\varepsilon))$ for every map, which left a factor $\log(1/\varepsilon)$ between the upper and lower bounds. Larsen and Nelson removed the factor for linear maps at ICALP 2016 and for all maps at FOCS 2017; the second paper settled the question for $\varepsilon \ge \min(n, d)^{-0.4999}$.

## References
