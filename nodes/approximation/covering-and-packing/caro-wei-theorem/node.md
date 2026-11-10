---
tag: 1BDTJZ
kind: theorem
slug: caro-wei-theorem
name: Caro-Wei theorem
aliases:
- Caro-Wei bound
- Caro-Wei inequality
area: approximation/covering-and-packing
level: core
summary: Each graph has an independent set with at least the sum over all vertices of 1/(deg(v) + 1) vertices; a random order proves it, and the minimum-degree greedy finds such a set.
prereqs: [independent-set, independence-number, linearity-of-expectation, probabilistic-method]
see_also: [greedy-independent-set, turan-theorem, independence-number, maximum-independent-set, probabilistic-method, method-of-conditional-expectations, linearity-of-expectation]
sources:
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition
    locator: The Probabilistic Lens, Turán's theorem (after Chapter 6; the random-order proof of the bound and of Turán's theorem)
  - title: Yair Caro, New results on the independence number, Technical report, Tel Aviv University, 1979
    locator: the main theorem
  - title: Victor K. Wei, A lower bound on the stability number of a simple graph, Bell Laboratories Technical Memorandum 81-11217-9, 1981
    locator: the main theorem
  - paper: doi:10.1007/BF02523693
    title: Magnús M. Halldórsson and Jaikumar Radhakrishnan, Greed is good, approximating independent sets in sparse and bounded-degree graphs, Algorithmica 18(1), 1997
    locator: pages 145 to 163 (the minimum-degree greedy reaches the bound)
---

The Caro-Wei theorem gives a lower bound on the [independence number](/independence-number/) of a graph from its degrees alone: $\alpha(G) \ge \sum_v 1/(\deg(v) + 1)$. Each vertex counts for one over its closed neighbourhood size, so vertices of small degree count more. The proof with a random order of the vertices is a standard example of the [probabilistic method](/probabilistic-method/). The [minimum-degree greedy algorithm](/greedy-independent-set/) finds an independent set at least this large in near-linear time. By convexity the bound implies the Turán bound $\alpha(G) \ge n/(\bar d + 1)$, which is the complement form of [Turán's theorem](/turan-theorem/).

## Statement

Let $G = (V, E)$ be a finite simple graph with $n$ vertices and $m$ edges, and let $\deg(v)$ be the degree of $v$. An independent set is a set of vertices with no edge between any two of them, and $\alpha(G)$ is the largest size of one.

**Theorem (Caro 1979, Wei 1981).**

$$\alpha(G) \ge \sum_{v \in V} \frac{1}{\deg(v) + 1}.$$

**Corollary (Turán bound).** With the average degree $\bar d = 2m/n$, $\alpha(G) \ge \dfrac{n}{\bar d + 1} = \dfrac{n^2}{2m + n}$.

## In plain words

Put the points of a network in a random order. Keep each point that comes before all of its linked points. Two kept points can never be linked, because then each would have to come before the other.

A point with few links has a good chance to be first among itself and its linked points. With three links, there are four points in the race and the chance is one in four. Add these chances over all points: this is the expected number of kept points. Some order keeps at least that many, so a set of that size with no links inside always exists.

## Proof

Let $\pi$ be a uniformly random ordering of $V$. For each vertex $v$, let $N[v]$ be the set of $v$ and its neighbours, of size $\deg(v) + 1$. Let

$$I = \{ v \in V : v \text{ comes before each of its neighbours in } \pi \}.$$

*$I$ is independent.* Suppose $u, v \in I$ and $\{u, v\} \in E$. Since $u \in I$ and $v$ is a neighbour of $u$, $u$ comes before $v$. Since $v \in I$, $v$ comes before $u$. Both cannot hold, so no edge joins two vertices of $I$.

*The expected size.* The vertex $v$ is in $I$ exactly when $v$ is the first vertex of $N[v]$ in $\pi$. The order that $\pi$ induces on $N[v]$ is uniform over the $(\deg(v) + 1)!$ orders of $N[v]$, so each of its $\deg(v) + 1$ vertices is first with the same probability. So $\Pr[v \in I] = 1/(\deg(v) + 1)$. By [linearity of expectation](/linearity-of-expectation/),

$$\mathbb{E}[|I|] = \sum_{v \in V} \Pr[v \in I] = \sum_{v \in V} \frac{1}{\deg(v) + 1}.$$

*Conclusion.* A random variable takes a value at least its mean with positive probability, so some ordering gives an independent set $I$ with $|I| \ge \sum_v 1/(\deg(v) + 1)$. So $\alpha(G)$ is at least this sum. $\blacksquare$

*Proof of the corollary.* The function $g(x) = 1/(x + 1)$ is convex on $x \ge 0$. By Jensen's inequality, $\frac{1}{n}\sum_v g(\deg(v)) \ge g\left(\frac{1}{n}\sum_v \deg(v)\right) = g(\bar d)$, and $\sum_v \deg(v) = 2m$. Multiply by $n$. $\square$

**Examples.** The values below are exact.

| graph | $n$ | Caro-Wei sum | $\alpha$ |
|---|---|---|---|
| $K_n$ | $n$ | $1$ | $1$ |
| $t$ disjoint copies of $K_r$ | $tr$ | $t$ | $t$ |
| cycle $C_5$ | 5 | $5/3$ | 2 |
| Petersen graph | 10 | $5/2$ | 4 |
| star $K_{1,n-1}$ | $n$ | $1/n + (n-1)/2$ | $n - 1$ |
| $K_{3,3}$ | 6 | $3/2$ | 3 |
| the graph with edges 0-1, 0-2, 1-2, 1-3, 2-3, 3-4, 4-5, 4-6, 5-6 | 7 | 2 | 3 |

The sum is exact for disjoint cliques, and it can be weak for dense graphs with large independent sets, such as $K_{3,3}$ or the star.

## Consequences

- **An algorithm.** The [minimum-degree greedy algorithm](/greedy-independent-set/) returns an independent set of at least this size, in $O((n + m) \log n)$ time. Each pick of a vertex $v$ of least degree deletes $\deg(v) + 1$ vertices, each worth at most $1/(\deg(v) + 1)$ in the sum, and the rest only gain. So it is a deterministic form of the proof.
- **Derandomization.** The [method of conditional expectations](/method-of-conditional-expectations/) also turns the random order into a deterministic algorithm, by fixing the order one position at a time.
- **Turán's theorem.** Apply the corollary to the complement $\bar G$: a graph on $n$ vertices with no clique of $r + 1$ vertices has $\alpha(\bar G) \le r$, and the bound gives at most $(1 - 1/r)n^2/2$ edges, which is [Turán's theorem](/turan-theorem/).
- **Bounded degree.** If each degree is at most $\Delta$, then $\alpha(G) \ge n/(\Delta + 1)$. A maximal independent set already reaches this, and it gives the ratio $\Delta + 1$ for approximating $\alpha$.
- **Weighted form.** The same proof with weights $w(v) \ge 0$ gives an independent set of weight at least $\sum_v w(v)/(\deg(v) + 1)$.
- **Distributed algorithms.** The random-order rule is local: each vertex compares its random rank with those of its neighbours. One round of it is the first step of Luby-type algorithms for maximal independent sets.

## Tightness

- **Equality.** The bound holds with equality for each disjoint union of cliques: each clique $K_r$ adds $r \cdot 1/r = 1$ to the sum, and an independent set takes at most one vertex of each clique.
- **The Turán bound.** The corollary $n/(\bar d + 1)$ holds with equality for a disjoint union of cliques of equal size, because all degrees are equal and Jensen's inequality is then an equality.
- **Gap.** The bound can be far from $\alpha$. On the star $K_{1,n-1}$ the sum is about $n/2$, but $\alpha = n - 1$; on $K_{k,k}$ the sum is $2k/(k + 1) < 2$, but $\alpha = k$.
- **Hardness.** No bound computable in polynomial time can be close to $\alpha$ on all graphs, because approximating $\alpha$ within $n^{1 - \varepsilon}$ is NP-hard; see [maximum independent set](/maximum-independent-set/).

## History

Caro (1979) and Wei (1981) found the bound independently. The short proof by a random order is in Alon and Spencer's book, as a Probabilistic Lens on Turán's theorem. Griggs (1983) and later Halldórsson and Radhakrishnan (1997) noted that the minimum-degree greedy algorithm always reaches the bound.

## References
