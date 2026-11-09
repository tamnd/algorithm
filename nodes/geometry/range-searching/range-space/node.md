---
tag: YHGFS8
kind: definition
slug: range-space
name: Range space
aliases:
- set system
- hypergraph of ranges
- shatter function
- primal shatter function
area: geometry/range-searching
level: advanced
summary: Pair (X, R) of a point set and a family of ranges, the abstraction behind range searching and sampling bounds.
prereqs: [orthogonal-range-searching, binomial-coefficient]
see_also: [vc-dimension, sauer-shelah-lemma, epsilon-net-theorem, geometric-cutting, radon-theorem, hypergraph, discrepancy-method, pac-learning]
sources:
  - book: isbn:9780387953748
    title: Jiří Matoušek, Lectures on Discrete Geometry, Graduate Texts in Mathematics 212, Springer, 2002
    locator: Chapter 10, Sections 10.1 (set systems, VC dimension, shatter functions) and 10.2 (the shatter function lemma and its proof)
  - paper: doi:10.1007/BF02187876
    title: David Haussler and Emo Welzl, Epsilon-nets and simplex range queries, Discrete and Computational Geometry 2, 1987, pages 127 to 151
    locator: Section 2, range spaces and their VC dimension, with the geometric examples
  - paper: doi:10.1137/1116025
    title: Vladimir N. Vapnik and Alexey Ya. Chervonenkis, On the uniform convergence of relative frequencies of events to their probabilities, Theory of Probability and its Applications 16(2), 1971, pages 264 to 280
    locator: the growth function and the polynomial bound on it (DOI to be checked)
  - paper: doi:10.1016/0097-3165(72)90019-2
    title: Norbert Sauer, On the density of families of sets, Journal of Combinatorial Theory, Series A 13(1), 1972, pages 145 to 147
    locator: the bound sum of binomial coefficients on the number of sets in a family of VC dimension d (DOI to be checked)
  - paper: doi:10.2140/pjm.1972.41.247
    title: Saharon Shelah, A combinatorial problem, stability and order for models and theories in infinitary languages, Pacific Journal of Mathematics 41(1), 1972, pages 247 to 261
    locator: the same bound, found independently (DOI to be checked)
---

A range space is a pair $(X, \mathcal{R})$ of a ground set $X$ and a family $\mathcal{R}$ of subsets of $X$, called ranges. In range searching, $X = \mathbb{R}^d$ and the ranges are boxes, halfspaces, simplices or balls; a query asks about $P \cap r$ for a stored finite set $P$ and a range $r$. Two numbers measure how complex a range space is: the **VC dimension**, the size of the largest set on which the ranges cut out every subset, and the **shatter function**, the largest number of distinct subsets the ranges cut out of $m$ points. The Sauer-Shelah lemma ties them: if the VC dimension is $\delta$, then $m$ points are cut into at most $\sum_{i \le \delta} \binom{m}{i} = O(m^{\delta})$ subsets, not $2^m$. This polynomial bound is what makes the [epsilon-net theorem](/epsilon-net-theorem/), [cuttings](/geometric-cutting/) and the lower and upper bounds of range searching work.

## Definition

**Notation.** $X$ is a set, $\mathcal{R}$ a family of subsets of $X$, $A$ a finite subset of $X$, $m = |A|$, and $\delta$ a VC dimension. For a finite point set $P$ of the plane, $\mathrm{orient}$ is the [orientation test](/orientation-test/); $\mathrm{incircle}$ is not used.

**Range space.** A *range space*, or *set system*, is a pair $\Sigma = (X, \mathcal{R})$ with $\mathcal{R} \subseteq 2^X$. The members of $\mathcal{R}$ are its *ranges*. When $X$ is finite, $\Sigma$ is a [hypergraph](/hypergraph/) with vertex set $X$ and hyperedges $\mathcal{R}$.

**Projection (trace).** For $A \subseteq X$, the *projection* of $\mathcal{R}$ on $A$ is
$$\mathcal{R}|_A = \{ r \cap A : r \in \mathcal{R} \},$$
a set, so equal intersections count once. $(A, \mathcal{R}|_A)$ is the *induced* range space. For a range searching problem on a stored set $P$, $\mathcal{R}|_P$ is exactly the set of possible answers to reporting queries.

**Shattering.** $A$ is *shattered* by $\mathcal{R}$ if $\mathcal{R}|_A = 2^A$, that is, every subset of $A$ equals $r \cap A$ for some range $r$.

**VC dimension.** The *Vapnik-Chervonenkis dimension* of $\Sigma$ is the largest size of a finite set $A \subseteq X$ shattered by $\mathcal{R}$, or $\infty$ if there are shattered sets of every finite size. For $\mathcal{R} \ne \emptyset$ the empty set is shattered, so the VC dimension is at least $0$. See also [VC dimension](/vc-dimension/) in learning theory.

**Shatter function.** The *(primal) shatter function* of $\Sigma$ is
$$\pi_{\mathcal{R}}(m) = \max \{ |\mathcal{R}|_A| : A \subseteq X, |A| = m \},$$
the largest number of distinct subsets that ranges cut out of $m$ points. Always $\pi_{\mathcal{R}}(m) \le 2^m$, with equality exactly when some $m$-point set is shattered, so the VC dimension is the largest $m$ with $\pi_{\mathcal{R}}(m) = 2^m$. In learning theory $\pi_{\mathcal{R}}$ is the *growth function*.

**Sauer-Shelah lemma.** Let $\Phi_{\delta}(m) = \sum_{i=0}^{\delta} \binom{m}{i}$. If $\Sigma$ has VC dimension at most $\delta$, then for every $m \ge 0$,
$$\pi_{\mathcal{R}}(m) \le \Phi_{\delta}(m), \qquad \text{and} \qquad \Phi_{\delta}(m) \le \left( \frac{e m}{\delta} \right)^{\delta} \text{ for } m \ge \delta \ge 1.$$

*Proof.* It is enough to show that every family $\mathcal{F}$ of subsets of an $m$-element set $A$ that shatters no set of size $\delta + 1$ has $|\mathcal{F}| \le \Phi_{\delta}(m)$; apply this to $\mathcal{F} = \mathcal{R}|_A$, since a subset of $A$ shattered by $\mathcal{R}|_A$ is shattered by $\mathcal{R}$. Induction on $m + \delta$. If $m = 0$, then $|\mathcal{F}| \le 1 = \Phi_{\delta}(0)$. If $\delta = 0$, no single element is shattered; two different members of $\mathcal{F}$ would differ at some $x$, and then $\{x\}$ would be shattered, so $|\mathcal{F}| \le 1 = \Phi_0(m)$. Otherwise fix $x \in A$ and let $A' = A \setminus \{x\}$,
$$\mathcal{F}_1 = \{ S \setminus \{x\} : S \in \mathcal{F} \}, \qquad \mathcal{F}_2 = \{ S \subseteq A' : S \in \mathcal{F} \text{ and } S \cup \{x\} \in \mathcal{F} \}.$$
The map $S \mapsto S \setminus \{x\}$ from $\mathcal{F}$ onto $\mathcal{F}_1$ is two to one exactly on the pairs $\{S, S \cup \{x\}\}$ with $S \in \mathcal{F}_2$ and one to one elsewhere, so $|\mathcal{F}| = |\mathcal{F}_1| + |\mathcal{F}_2|$. A set shattered by $\mathcal{F}_1$ is shattered by $\mathcal{F}$, so $|\mathcal{F}_1| \le \Phi_{\delta}(m - 1)$. If $B \subseteq A'$ is shattered by $\mathcal{F}_2$, then $B \cup \{x\}$ is shattered by $\mathcal{F}$, because each $T \subseteq B$ is $S \cap B$ for some $S \in \mathcal{F}_2$, and both $S$ and $S \cup \{x\}$ are in $\mathcal{F}$. So $\mathcal{F}_2$ shatters no set of size $\delta$, and $|\mathcal{F}_2| \le \Phi_{\delta - 1}(m - 1)$. By Pascal's rule $\binom{m-1}{i} + \binom{m-1}{i-1} = \binom{m}{i}$, $\Phi_{\delta}(m - 1) + \Phi_{\delta - 1}(m - 1) = \Phi_{\delta}(m)$. For the second bound, with $0 < \delta / m \le 1$,
$$\left( \frac{\delta}{m} \right)^{\delta} \Phi_{\delta}(m) \le \sum_{i=0}^{\delta} \binom{m}{i} \left( \frac{\delta}{m} \right)^{i} \le \left( 1 + \frac{\delta}{m} \right)^{m} \le e^{\delta}. \qquad \blacksquare$$

The bound $\Phi_{\delta}(m)$ is attained, for example by the family of all subsets of size at most $\delta$ of an $m$-set, and by intervals on the line (below). The lemma also has a converse direction: if $\pi_{\mathcal{R}}(m) < 2^m$ for some $m$, the VC dimension is less than $m$. See [the Sauer-Shelah lemma](/sauer-shelah-lemma/) for its use in learning theory.

## Examples and non-examples

Ranges are closed throughout. The counts for the eight-point set $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ were found by enumerating all ranges by script.

| ground set and ranges | VC dimension | shatter function or count | reason |
|---|---|---|---|
| $\mathbb{R}$, closed intervals | 2 | $\pi(m) = 1 + m + \binom{m}{2} = \Phi_2(m)$ | two points are shattered; of three points $a < b < c$, no interval contains $a$ and $c$ but not $b$ |
| $\mathbb{R}^2$, closed halfplanes | 3 | $m(m - 1) + 2$ for $m \ge 2$ points with no three collinear; $56$ for $P$ | three points in general position are shattered; four points cannot be, by [Radon's theorem](/radon-theorem/) |
| $\mathbb{R}^2$, axis-parallel boxes | 4 | $73$ for $P$, against $\Phi_4(8) = 163$ | the four points of a diamond are shattered; for five points, every box that holds a leftmost, a rightmost, a lowest and a highest point holds all five, so those at most four points are never cut out alone |
| $\mathbb{R}^d$, halfspaces | $d + 1$ | $O(m^{d})$ | Radon's theorem in $\mathbb{R}^d$ |
| $\mathbb{R}^d$, balls | $d + 1$ | $O(m^{d+1})$ by Sauer-Shelah | lifting turns balls into halfspaces of $\mathbb{R}^{d+1}$ |
| $\mathbb{R}^2$, simplices (triangles) | 7 | polynomial | a known exact value; finite because triangles are intersections of $3$ halfplanes |
| $\mathbb{R}^2$, convex sets | $\infty$ (non-example) | $\pi(m) = 2^m$ | any $m$ points on a circle are shattered: each subset is cut out by its own convex hull |
| $\mathbb{R}$, finite unions of intervals | $\infty$ (non-example) | $\pi(m) = 2^m$ | every finite set of reals is a union of degenerate intervals |

**The halfplanes on $P$.** The points $(5,4)$, $(8,1)$, $(7,2)$ lie on the line $x + y = 9$, and a closed halfplane that contains $(5,4)$ and $(8,1)$ contains the point $(7,2)$ between them. So this triple is not shattered, and $P$ has $56$ halfplane traces instead of the $8 \cdot 7 + 2 = 58$ of a set in general position. The other $55$ triples of $P$ are shattered. For four points in convex position, such as the corners of a square, the halfplanes cut $14$ of the $16$ subsets; the two missing ones are the diagonal pairs.

**The boxes on $P$.** Exactly four of the $70$ four-point subsets of $P$ are shattered by boxes, for example $\{(2,3), (9,6), (4,7), (8,1)\}$, whose points are extreme in four different directions.

**Why the polynomial bound matters.** For halfplanes and $m = 8$, $\Phi_3(8) = 93 < 256 = 2^8$; for $m = 20$, $\Phi_3(20) = 1351$ against $2^{20} = 1048576$. A structure for halfplane queries on $n$ points has only $O(n^3)$ possible answers to distinguish, and a random sample hits all large ranges once a union bound over $O(m^{\delta})$ traces is affordable; this is the core of the [epsilon-net theorem](/epsilon-net-theorem/).

## Related definitions

- **Dual range space.** For $(X, \mathcal{R})$, the dual has ground set $\mathcal{R}$ and, for each $x \in X$, the range $\{ r \in \mathcal{R} : x \in r \}$. Its shatter function, the *dual shatter function*, counts the cells of the arrangement of $m$ ranges; for halfplanes it is $O(m^2)$. If the primal VC dimension is $\delta$, the dual VC dimension is less than $2^{\delta + 1}$.
- **$\varepsilon$-net.** For a finite $X$ and $0 < \varepsilon < 1$, a set $N \subseteq X$ such that every range $r$ with $|r \cap X| \ge \varepsilon |X|$ meets $N$. See the [epsilon-net theorem](/epsilon-net-theorem/).
- **$\varepsilon$-approximation.** A set $A \subseteq X$ with $\left| \frac{|r \cap A|}{|A|} - \frac{|r \cap X|}{|X|} \right| \le \varepsilon$ for every range $r$; every $\varepsilon$-approximation is an $\varepsilon$-net.
- **Discrepancy.** The smallest, over 2-colorings of $X$, of the largest imbalance of a range; it bounds the size of $\varepsilon$-approximations and drives lower bounds, see the [discrepancy method](/discrepancy-method/).
- **Range searching.** A range searching problem is a range space with a finite stored set $P$; the [orthogonal](/orthogonal-range-searching/), [halfspace](/halfspace-range-searching/) and [simplex](/simplex-range-searching/) problems use the range spaces above.
- **PAC learning.** A hypothesis class of finite VC dimension is learnable to error $\varepsilon$ with failure probability $\eta$ from $O((\delta \log(1/\varepsilon) + \log(1/\eta)) / \varepsilon)$ examples; see [PAC learning](/pac-learning/).

## References
