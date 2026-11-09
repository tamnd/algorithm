---
tag: 8Z79BR
kind: definition
slug: pareto-dominance
name: Pareto dominance
aliases:
- dominance
- domination relation
- Pareto order
- componentwise order
area: optimization/multi-objective
level: intro
summary: A vector dominates another when it is no worse in every objective and strictly better in at least one. Dominance is a strict partial order, so two vectors can be incomparable.
prereqs: [multi-objective-optimization]
see_also: [pareto-optimality, pareto-front, non-dominated-sorting, pareto-ranking, epsilon-dominance, kung-algorithm]
sources:
  - book: isbn:9783540213987
    title: Matthias Ehrgott, Multicriteria Optimization, second edition, Springer, 2005
    locator: Chapter 1 (binary relations and the componentwise orders on the objective space) and Chapter 2 (efficiency and nondominance)
  - book: isbn:9780471873396
    title: Kalyanmoy Deb, Multi-Objective Optimization Using Evolutionary Algorithms, Wiley, 2001
    locator: Chapter 2, the definition of dominance and its properties
  - paper: doi:10.1145/322092.322095
    title: Jon L. Bentley, H. T. Kung, Mario Schkolnick and Clark D. Thompson, On the average number of maxima in a set of vectors and applications, Journal of the ACM 25(4), 1978
    locator: pages 536 to 543, the recurrence for the expected number of maxima
---

Pareto dominance is the order that multi-objective optimization uses to compare two solutions: one solution dominates another when it is at least as good in every objective and strictly better in at least one. It is a strict partial order, so two solutions often do not dominate each other. The solutions that nothing dominates are the [Pareto optimal](/pareto-optimality/) ones, and their images form the [Pareto front](/pareto-front/).

## Definition

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$. A solution $x$ of the feasible set $X$ has the image $y = f(x) = (f_1(x), \ldots, f_p(x)) \in \mathbb{R}^p$.

For two vectors $y, y' \in \mathbb{R}^p$ define three relations:

| name | notation | meaning |
|---|---|---|
| weak dominance | $y \leqq y'$ | $y_i \le y'_i$ for all $i = 1, \ldots, p$ |
| dominance | $y \prec y'$ | $y \leqq y'$ and $y \ne y'$, so $y_i \le y'_i$ for all $i$ and $y_j < y'_j$ for some $j$ |
| strict dominance | $y < y'$ | $y_i < y'_i$ for all $i$ |

A solution $x$ *dominates* a solution $x'$ when $f(x) \prec f(x')$. The vectors $y$ and $y'$ are *incomparable* when $y \ne y'$ and neither dominates the other. For maximization, reverse every inequality, or replace each $f_i$ by $-f_i$.

**Properties.** On $\mathbb{R}^p$:

1. $\leqq$ is a partial order: it is reflexive, antisymmetric and transitive.
2. $\prec$ is a strict partial order: it is irreflexive and transitive, and so it is also asymmetric.
3. $<$ is a strict partial order, and $y < y'$ implies $y \prec y'$.
4. For $p = 1$, all three agree with the usual order of $\mathbb{R}$. For $p \ge 2$, none of them is total.

*Proof.* Each property of $\leqq$ holds in each coordinate, so it holds for the vector. For $\prec$: $y \prec y$ is false, because it needs $y \ne y$. If $y \prec y'$ and $y' \prec y''$, then $y \leqq y''$ by transitivity of $\leqq$. If $y = y''$, then $y \leqq y'$ and $y' \leqq y$, so $y = y'$ by antisymmetry, which contradicts $y \prec y'$. So $y \ne y''$ and $y \prec y''$. Asymmetry follows: $y \prec y'$ and $y' \prec y$ would give $y \prec y$. Property 3 is the same argument with strict inequalities. For property 4, the vectors $(1, 2, 0, \ldots, 0)$ and $(2, 1, 0, \ldots, 0)$ are not comparable under any of the three relations. $\square$

On solutions, the relation "$f(x) \leqq f(x')$" is only a preorder: two different solutions can have the same image, and then each weakly dominates the other. Dominance between solutions is still a strict partial order, because it is defined through the images.

A dominance test costs at most $p$ comparisons of numbers, and it can stop at the first coordinate where $y_i > y'_i$.

## Examples and non-examples

**Examples.** With $p = 2$:

- $(1, 2) \prec (1, 3)$: equal in the first objective, better in the second. But $(1, 2) < (1, 3)$ is false.
- $(1, 2) < (2, 3)$, so also $(1, 2) \prec (2, 3)$.
- $(1, 2)$ and $(2, 1)$ are incomparable.
- $(1, 2)$ does not dominate $(1, 2)$. Equal vectors are never in the relation $\prec$, but each weakly dominates the other.

In the seven points $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$ of the example on the [multi-objective optimization](/multi-objective-optimization/) page, the dominance pairs are $b \prec c$, $d \prec f$ and $e \prec f$. All other pairs of distinct points are incomparable. So $\{a, b, d, e, g\}$ is the set of nondominated points.

**Comparable pairs become rare as $p$ grows.** Let $u$ and $v$ be independent random vectors whose $2p$ coordinates are independent with one continuous distribution. Ties then have probability 0, and each coordinate gives $u_i < v_i$ with probability $1/2$, independently. So

$$\Pr[u \prec v \text{ or } v \prec u] = 2 \cdot 2^{-p} = 2^{1-p}.$$

For $p = 2, 3, 4, 5$ this is $0.5, 0.25, 0.125, 0.0625$. In the same model, let $A(N, p)$ be the expected number of nondominated vectors among $N$ such vectors. Then $A(N, 1) = 1$ and

$$A(N, p) = \sum_{k=1}^{N} \frac{A(k, p - 1)}{k}.$$

*Proof.* Sort the vectors by the first coordinate. The vector of rank $k$ can be dominated only by a vector of smaller rank, and then only through coordinates $2$ to $p$. The last $p - 1$ coordinates of the $k$ vectors of rank at most $k$ are independent of the ranks, so by symmetry the vector of rank $k$ is nondominated among them with probability $A(k, p - 1)/k$. Linearity of expectation gives the sum. $\square$

So $A(N, 2) = H_N$, the harmonic number, and $A(N, p) = \Theta(\ln^{p-1} N)$ for fixed $p$ (Bentley, Kung, Schkolnick and Thompson, 1978). The exact values:

| $N$ | $p = 2$ | $p = 3$ | $p = 4$ | $p = 5$ |
|---|---|---|---|---|
| 10 | 2.93 | 5.06 | 6.86 | 8.13 |
| 100 | 5.19 | 14.27 | 27.91 | 43.85 |
| 1000 | 7.49 | 28.84 | 76.46 | 157.45 |

With many objectives, a large part of a random set is nondominated, so dominance alone gives little selection pressure. This is one reason for the reference points of [NSGA-III](/nsga-iii/) and for the decomposition of [MOEA/D](/moea-d/).

**Non-examples.**

- *A weighted sum is not dominance.* The rule "$y$ is better when $y_1 + y_2 < y'_1 + y'_2$" is a total preorder. It ranks $(0, 10)$ before $(6, 5)$, but neither dominates the other. The [weighted sum method](/weighted-sum-method/) uses such a rule to pick one point; it does not define the front.
- *"Better in more objectives" is not an order.* Let $u = (1, 2, 3)$, $v = (2, 3, 1)$ and $w = (3, 1, 2)$. Then $u$ beats $v$ in two of three objectives, $v$ beats $w$ in two, and $w$ beats $u$ in two. The relation has a cycle, so it is not transitive.
- *Dominance with a strict inequality in every coordinate is not Pareto dominance.* The relation $<$ ignores improvements in only some objectives. A point that only $<$ cannot beat is [weakly Pareto optimal](/pareto-optimality/), which is a weaker property than Pareto optimality.

## Related definitions

- [Pareto optimality](/pareto-optimality/): a solution is Pareto optimal when no feasible solution dominates it. The [Pareto front](/pareto-front/) is the set of their images.
- [Epsilon-dominance](/epsilon-dominance/) relaxes dominance by a factor or an additive margin, to get a small approximate front.
- [Non-dominated sorting](/non-dominated-sorting/) and [Pareto ranking](/pareto-ranking/) split a finite set into layers by repeated removal of the nondominated points.
- [Kung's algorithm](/kung-algorithm/) finds the nondominated vectors of a finite set with fewer than the $\binom{N}{2}$ pairwise tests of the brute force.
- **Cone dominance.** For a closed convex pointed cone $C$, $y$ dominates $y'$ when $y' - y \in C \setminus \{0\}$. Pareto dominance is the case $C = \mathbb{R}^p_{\ge 0}$, the nonnegative orthant.
- **Lexicographic order.** $y$ is lexicographically smaller than $y'$ when $y_j < y'_j$ at the first index $j$ where they differ. It is a total order, and $y \prec y'$ implies that $y$ is lexicographically smaller. [Lexicographic optimization](/lexicographic-optimization/) uses it.

## References
