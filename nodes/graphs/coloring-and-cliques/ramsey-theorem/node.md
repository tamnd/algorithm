---
tag: 43816V
kind: theorem
slug: ramsey-theorem
name: Ramsey's theorem
aliases:
- Ramsey theory
area: graphs/coloring-and-cliques
level: core
summary: Every sufficiently large graph contains a clique or an independent set of a given size.
prereqs: [clique, independent-set, pigeonhole-principle]
see_also: [clique-number, independence-number, turan-theorem, probabilistic-method, erdos-szekeres-theorem, maximum-clique]
sources:
  - paper: doi:10.1112/plms/s2-30.1.264
    title: F. P. Ramsey, On a problem of formal logic, Proceedings of the London Mathematical Society s2-30(1), 264 to 286 (1930)
    locator: the theorem on colorings of the r-subsets of a set (finite and infinite forms)
  - paper: "P. Erdős and G. Szekeres, A combinatorial problem in geometry, Compositio Mathematica 2, 463 to 470 (1935)"
    locator: the bound R(s, t) ≤ C(s + t - 2, s - 1)
  - paper: doi:10.1090/S0002-9904-1947-08785-1
    title: P. Erdős, Some remarks on the theory of graphs, Bulletin of the American Mathematical Society 53(4), 292 to 294 (1947)
    locator: the lower bound R(k, k) > 2^(k/2)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 9.1, Ramsey's original theorems
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Section 1.1, The basic method (the lower bound for R(k, k))
  - paper: doi:10.37236/21
    title: Stanisław P. Radziszowski, Small Ramsey numbers, Electronic Journal of Combinatorics, Dynamic Survey DS1
    locator: Section 2, the values and bounds of R(k, l) for two colors
---

Ramsey's theorem says that for all positive integers $s$ and $t$ there is a number $R(s, t)$ such that every graph with at least $R(s, t)$ vertices contains a [clique](/clique/) of $s$ vertices or an [independent set](/independent-set/) of $t$ vertices. The least such number is the Ramsey number $R(s, t)$. The proof gives $R(s, t) \le \binom{s + t - 2}{s - 1}$, so $R(k, k) < 4^k$, and Erdős showed with the [probabilistic method](/probabilistic-method/) that $R(k, k) > 2^{k/2}$. Exact values are known only for small cases, such as $R(3, 3) = 6$ and $R(4, 4) = 18$.

## Statement

Let $s, t \ge 1$ be integers. Write $\omega(G)$ for the [clique number](/clique-number/) and $\alpha(G)$ for the [independence number](/independence-number/) of a finite simple graph $G$.

**Theorem (Ramsey 1930, Erdős and Szekeres 1935).** There is an integer $N$ such that every graph $G$ with at least $N$ vertices has $\omega(G) \ge s$ or $\alpha(G) \ge t$. The least such $N$, the Ramsey number $R(s, t)$, satisfies

$$R(s, 1) = R(1, t) = 1, \qquad R(s, 2) = s, \quad R(2, t) = t,$$

$$R(s, t) \le R(s - 1, t) + R(s, t - 1) \quad (s, t \ge 2), \qquad R(s, t) \le \binom{s + t - 2}{s - 1}.$$

**Lower bound (Erdős 1947).** For $k \ge 3$, $R(k, k) > \lfloor 2^{k/2} \rfloor$.

**Multicolor form.** For integers $r \ge 1$ and $k_1, \ldots, k_r \ge 1$ there is $N$ such that each coloring of the edges of $K_N$ with $r$ colors has, for some $i$, a set of $k_i$ vertices whose edges all have color $i$. The two-color case with edges for color 1 and non-edges for color 2 is the theorem above.

## In plain words

In any group of six people, there are three who all know each other or three who are all strangers. Ramsey's theorem says that this is not luck about the number six. For any sizes you choose, a large enough group always contains a set of mutual friends of the first size or a set of mutual strangers of the second size.

Total disorder is impossible in a large structure: some regular piece is always inside. The catch is that "large enough" grows very fast, and the exact threshold is known only for small sizes.

## Proof

**Base cases.** Every graph with at least one vertex has a clique and an independent set of one vertex, and the graph with no vertex has neither, so $R(s, 1) = R(1, t) = 1$. A graph on $s$ vertices is either complete, and then it is a clique of $s$ vertices, or it has two non-adjacent vertices, which form an independent set of 2. The complete graph $K_{s-1}$ has neither, so $R(s, 2) = s$. The same argument with the roles of edges and non-edges swapped gives $R(2, t) = t$.

**The recurrence.** Let $s, t \ge 2$ and assume that $a = R(s - 1, t)$ and $b = R(s, t - 1)$ exist. Let $G$ have $n \ge a + b$ vertices, and let $v$ be a vertex. The other $n - 1 \ge a + b - 1$ vertices split into the neighbors $N$ of $v$ and the non-neighbors $M$. Since $|N| + |M| \ge a + b - 1$, either $|N| \ge a$ or $|M| \ge b$.

- If $|N| \ge a$, the induced graph $G[N]$ has a clique of $s - 1$ vertices, and adding $v$ gives a clique of $s$ vertices in $G$, or $G[N]$ has an independent set of $t$ vertices.
- If $|M| \ge b$, the graph $G[M]$ has a clique of $s$ vertices, or an independent set of $t - 1$ vertices, and adding $v$ gives an independent set of $t$ vertices.

So $R(s, t)$ exists and $R(s, t) \le a + b$. Induction on $s + t$ proves existence for all $s, t$.

**The binomial bound.** By induction on $s + t$: the base cases satisfy $R(s, 1) = 1 = \binom{s-1}{s-1}$, $R(1, t) = 1 = \binom{t-1}{0}$. For $s, t \ge 2$, the recurrence and Pascal's rule give $R(s, t) \le \binom{s + t - 3}{s - 2} + \binom{s + t - 3}{s - 1} = \binom{s + t - 2}{s - 1}$. For $s = t = k$ this is $\binom{2k-2}{k-1} < 4^{k-1}$.

**The lower bound.** Let $n = \lfloor 2^{k/2} \rfloor$ and color each edge of $K_n$ red or blue independently with probability $1/2$ each (red for an edge of $G$, blue for a non-edge). A fixed set of $k$ vertices is all red or all blue with probability $2 \cdot 2^{-\binom{k}{2}}$. By the [union bound](/union-bound/), the probability that some $k$-set is one-colored is at most

$$\binom{n}{k}\, 2^{1 - \binom{k}{2}} < \frac{n^k}{k!}\, 2^{1 - k(k-1)/2} \le \frac{2^{k^2/2}}{k!}\, 2^{1 - k^2/2 + k/2} = \frac{2^{1 + k/2}}{k!} < 1 \quad (k \ge 3).$$

So some graph on $n$ vertices has $\omega < k$ and $\alpha < k$, and $R(k, k) > n$. The proof shows that such a graph exists but gives no fast way to build one.

**Multicolor form.** By induction on $r$. For $r = 1$ take $N = k_1$. For $r \ge 2$, merge the colors $r - 1$ and $r$ into one color. By the induction hypothesis with $r - 1$ colors and the targets $k_1, \ldots, k_{r-2}, R(k_{r-1}, k_r)$, a large enough $K_N$ has a $k_i$-set of color $i$ for some $i \le r - 2$, or a set of $R(k_{r-1}, k_r)$ vertices whose edges use only the colors $r - 1$ and $r$. In the second case, the two-color theorem gives a $k_{r-1}$-set of color $r - 1$ or a $k_r$-set of color $r$. $\blacksquare$

## Consequences

- **Cliques or independent sets of logarithmic size.** Each graph on $n$ vertices has $\max(\omega, \alpha) \ge \frac12 \log_2 n$, from $R(k, k) < 4^k$. The Erdős bound shows that some graphs have $\max(\omega, \alpha) < 2 \log_2 n$. So the order $\log n$ is right.
- **Erdős-Szekeres.** Each sequence of more than $(r - 1)(s - 1)$ distinct numbers has an increasing subsequence of length $r$ or a decreasing one of length $s$; see the [Erdős-Szekeres theorem](/erdos-szekeres-theorem/) and [longest increasing subsequence](/longest-increasing-subsequence/). Ramsey's theorem gives a weaker bound of the same kind, and the 1935 paper also proved that each large enough set of points in general position in the plane has $k$ points in convex position.
- **Ramsey graphs and explicit constructions.** A graph with $\omega$ and $\alpha$ both of order $\log n$ is a *Ramsey graph*. Building one explicitly, without randomness, is a hard problem in pseudorandomness, linked to extractors and to lower bounds in complexity.
- **Lower bounds in computing.** Ramsey arguments show that some decision trees and comparison-based procedures must behave in a uniform way on a large subset of inputs, which is then used for a lower bound.

## Tightness

- **$R(3, 3) = 6$.** The 5-cycle $C_5$ has no triangle and no independent set of 3 vertices, so $R(3, 3) > 5$, and the bound $\binom{4}{2} = 6$ gives equality. Every one of the $2^{15}$ graphs on the vertex set $\{1, \ldots, 6\}$ has a triangle or an independent triple.
- **$R(4, 4) = 18$.** The Paley graph on $\mathbb{Z}_{17}$, where $i$ and $j$ are adjacent when $i - j$ is a nonzero square modulo 17 (the squares are $1, 2, 4, 8, 9, 13, 15, 16$), has no clique and no independent set of 4 vertices. So $R(4, 4) > 17$. Greenwood and Gleason proved $R(4, 4) = 18$ in 1955. The binomial bound gives only $20$.
- **Other known values.** $R(3, 4) = 9$, $R(3, 5) = 14$, $R(3, 6) = 18$, $R(3, 7) = 23$, $R(3, 8) = 28$, $R(3, 9) = 36$ and $R(4, 5) = 25$. The value of $R(5, 5)$ is unknown; its lower bound is 43. The survey of Radziszowski keeps the current list.
- **Asymptotics.** The bounds $2^{k/2} < R(k, k) < 4^k$ leave a gap in the base of the exponent. The lower base $\sqrt 2$ has not been improved since 1947, apart from a factor of 2 in front. Campos, Griffiths, Morris and Sahasrabudhe (2023) proved $R(k, k) \le (4 - \varepsilon)^k$ for a fixed $\varepsilon > 0$, the first exponential improvement of the upper bound.

## History

Frank Ramsey proved the theorem in 1930 as a lemma in a paper on the decision problem of logic; he stated it for colorings of the $r$-element subsets of a set, in finite and infinite forms. Erdős and Szekeres rediscovered it in 1935 in a problem on convex polygons and proved the binomial bound. Erdős gave the lower bound in 1947, one of the first uses of the probabilistic method. Greenwood and Gleason found $R(3, 3)$, $R(3, 4)$, $R(3, 5)$ and $R(4, 4)$ in 1955.

## References
