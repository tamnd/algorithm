---
tag: 5PHMAQ
kind: theorem
slug: steiner-ratio
name: Steiner ratio
aliases:
- Gilbert-Pollak ratio
- Gilbert-Pollak conjecture
- Steiner ratio conjecture
area: geometry/geometric-optimization
level: advanced
summary: The worst case ratio of Steiner minimal tree to minimum spanning tree length. It is at least 1/2 in every metric and 2/3 in the L1 plane; in the Euclidean plane √3/2 is open.
prereqs: [euclidean-steiner-tree-problem, minimum-spanning-tree, fermat-point]
see_also: [euclidean-steiner-tree-problem, rectilinear-steiner-tree-problem, steiner-tree-problem, euclidean-minimum-spanning-tree, fermat-point, approximation-ratio, steiner-tree-inapproximability, minimum-spanning-tree]
sources:
  - paper: "E. N. Gilbert and H. O. Pollak, Steiner minimal trees, SIAM Journal on Applied Mathematics 16(1), 1968, 1 to 29"
    locator: the definition of the Steiner ratio, the bound 1/2, and the conjecture that the Euclidean plane ratio is √3/2
  - paper: doi:10.1137/0130013
    title: "F. K. Hwang, On Steiner minimal trees with rectilinear distance, SIAM Journal on Applied Mathematics 30(1), 1976"
    locator: the rectilinear Steiner ratio 2/3
  - paper: "F. R. K. Chung and R. L. Graham, A new bound for Euclidean Steiner minimal trees, Annals of the New York Academy of Sciences 440, 1985"
    locator: the lower bound 0.824 for the Euclidean plane
  - paper: "D. Z. Du and F. K. Hwang, A proof of the Gilbert-Pollak conjecture on the Steiner ratio, Algorithmica 7, 1992"
    locator: the claimed proof of the conjecture by a minimax theorem and characteristic areas
  - paper: "A. O. Ivanov and A. A. Tuzhilin, The Steiner ratio Gilbert-Pollak conjecture is still open, Algorithmica 62, 2012"
    locator: the gap in the Du and Hwang proof, and the statement that the conjecture is open
  - paper: "J. H. Rubinstein and D. A. Thomas, The Steiner ratio conjecture for six points, Journal of Combinatorial Theory, Series A 58, 1991"
    locator: the conjecture for six terminals
  - paper: "Frank K. Hwang, Dana S. Richards and Pawel Winter, The Steiner Tree Problem, Annals of Discrete Mathematics 53, North-Holland, 1992"
    locator: Part I, the section on the Steiner ratio and the history of its lower bounds
---

The *Steiner ratio* of a metric space is the largest factor by which a Steiner minimal tree can be shorter than a minimum spanning tree: the infimum, over finite terminal sets, of $\mathrm{SMT}/\mathrm{MST}$. It measures how much extra junction points can save, and its inverse is the approximation factor of the spanning tree heuristic for the Steiner tree problem. In every metric space the ratio is at least $1/2$, and that is tight for graphs. In the rectilinear plane it is exactly $2/3$ (Hwang 1976). In the Euclidean plane it lies between $0.824$ (Chung and Graham 1985) and $\sqrt{3}/2 \approx 0.866$. Gilbert and Pollak (1968) conjectured that $\sqrt{3}/2$ is the exact value. Du and Hwang published a proof in 1990 and 1992, but Ivanov and Tuzhilin (2012) found a gap, and the conjecture is now regarded as open.

## Statement

Notation: $(M, d)$ is a metric space and $T \subseteq M$ a finite set of at least two terminals. $\mathrm{MST}(T)$ is the length of a minimum spanning tree on $T$ with edge weights $d$. $\mathrm{SMT}(T)$ is the infimum of the lengths of trees whose vertex set contains $T$ and may contain other points of $M$, the Steiner points. The Steiner ratio is

$$\rho(M) = \inf_T \frac{\mathrm{SMT}(T)}{\mathrm{MST}(T)}.$$

**Theorem.**

1. For every metric space $M$ and every $T$ with $n \ge 2$ terminals, $\mathrm{SMT}(T) \ge \frac{n}{2(n-1)}\, \mathrm{MST}(T)$. Hence $\rho(M) \ge \frac{1}{2}$, and the constant $\frac{1}{2}$ is attained in the limit by some graph metrics.
2. In the Euclidean plane, $\mathrm{SMT}(T)/\mathrm{MST}(T) = \sqrt{3}/2$ for the vertices of an equilateral triangle, so $\rho(\mathbb{R}^2, L_2) \le \sqrt{3}/2$.
3. (Hwang 1976.) In the plane with the $L_1$ metric, $\rho = 2/3$.
4. (Chung and Graham 1985.) In the Euclidean plane, $\rho \ge 0.824$.

**Conjecture (Gilbert and Pollak 1968).** In the Euclidean plane, $\rho = \sqrt{3}/2$.

**Status.** Proved for $n = 3$ (Gilbert and Pollak), $n = 4$ (Pollak 1978), $n = 5$ (Du, Yao and Hwang 1982) and $n = 6$ (Rubinstein and Thomas 1991). The general case is open: the 1992 proof of Du and Hwang has a gap that Ivanov and Tuzhilin described in 2012, and the conjecture is regarded as open. Parts 1 and 2 are proved below; parts 3 and 4 are cited.

## In plain words

To connect some points, you can join them directly, point to point, or you can add new junction points to share road. Junctions never make the network longer, but how much shorter can they make it?

The answer depends on how distance is measured. With any distance at all, junctions can at most halve the length. On a grid where roads go only left-right and up-down, they can save at most a third. For ordinary straight-line distance, three points at the corners of an equal-sided triangle give a saving of about 13 percent. Most people believe no set of points does better, but nobody has a complete proof. What is proved is that the saving is never more than about 18 percent.

## Proof

**Part 1.** Let $S$ be a Steiner tree for $T$ of length $L$, with any Steiner points. Double every edge of $S$. Every vertex now has even degree, so there is a closed walk that uses each doubled edge once; its length is $2L$ and it visits every terminal. List the terminals in the order of their first visit, $t_1, \ldots, t_n$, and close the list with $t_1$. By the triangle inequality, $d(t_i, t_{i+1})$ is at most the length of the walk between those visits, so the cycle $t_1, \ldots, t_n, t_1$ has length at most $2L$. Remove its longest edge. The rest is a spanning path on $T$, so

$$\mathrm{MST}(T) \le \left(1 - \frac{1}{n}\right) 2L.$$

Take the infimum over $S$: $\mathrm{SMT}(T) \ge \frac{n}{2(n-1)} \mathrm{MST}(T) > \frac{1}{2}\mathrm{MST}(T)$.

*Tightness.* In the star graph with center $c$ and leaves $t_1, \ldots, t_n$, with every edge of length 1 and the shortest path metric, take $T$ as the leaves. Then $d(t_i, t_j) = 2$, so $\mathrm{MST}(T) = 2(n - 1)$, while the star itself gives $\mathrm{SMT}(T) = n$. The ratio $n/(2(n-1))$ equals the bound of part 1 and tends to $\frac{1}{2}$.

**Part 2.** Let $T$ be the vertices of an equilateral triangle with side 1. Then $\mathrm{MST}(T) = 2$. A Steiner minimal tree for three terminals has at most one Steiner point (Gilbert and Pollak), so it is either two sides, of length 2, or a star from one point $x$, of length $\sum_i |x - t_i|$. The least such sum is reached at the [Fermat point](/fermat-point/), here the center, at distance $1/\sqrt{3}$ from each vertex. So $\mathrm{SMT}(T) = 3/\sqrt{3} = \sqrt{3}$ and the ratio is $\sqrt{3}/2$. $\blacksquare$

## Consequences

- **Spanning tree heuristic.** A minimum spanning tree is a $1/\rho$ approximation of the Steiner minimal tree. This gives the factor 2 for graphs, $3/2$ in the $L_1$ plane, and at most $1/0.824 \approx 1.214$ in the Euclidean plane. If the conjecture holds, the Euclidean factor is $2/\sqrt{3} \approx 1.155$.
- **Fast bounds.** Since the Euclidean minimum spanning tree takes $O(n \log n)$ time, it gives a quick estimate of the Steiner tree length within these factors.
- **Approximation in graphs.** In graphs, better approximation algorithms than the spanning tree exist, but the problem has no polynomial time approximation scheme unless P = NP; see [Steiner tree inapproximability](/steiner-tree-inapproximability/).

## Tightness

- **General metrics.** The star example shows that $\frac{1}{2}$ cannot be improved.
- **Rectilinear plane.** The four terminals $(1,0), (0,1), (2,1), (1,2)$ have $\mathrm{MST} = 6$ and $\mathrm{SMT} = 4$, ratio $2/3$, which matches Hwang's bound.
- **Euclidean plane.** The equilateral triangle gives $\sqrt{3}/2$.
- **Higher dimensions.** The natural extension, that the regular simplex is the worst case in $\mathbb{R}^d$, fails for $d \ge 3$ (Du and Smith 1996), and the exact Euclidean Steiner ratio is not known in any dimension $d \ge 2$.

## History

Gilbert and Pollak (1968) defined the ratio, proved $\rho \ge \frac{1}{2}$, and stated the conjecture $\rho = \sqrt{3}/2$ for the Euclidean plane. Lower bounds then rose step by step: $1/\sqrt{3} \approx 0.577$ (Graham and Hwang 1976), $0.743$ (Chung and Hwang 1978), $0.8$ (Du and Hwang 1983), and $0.824$ (Chung and Graham 1985), the best bound known. Hwang (1976) found the rectilinear value $2/3$. Du and Hwang announced a proof of the full conjecture at FOCS 1990 and published it in Algorithmica in 1992, and for about twenty years it was cited as a theorem. In 2012 Ivanov and Tuzhilin showed that a step in that proof does not hold, and the conjecture returned to open status. The cases $n \le 6$ have separate proofs that do not depend on it.

## References
