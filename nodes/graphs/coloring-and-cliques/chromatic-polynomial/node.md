---
tag: H9AF9P
kind: concept
slug: chromatic-polynomial
name: Chromatic polynomial
aliases:
- Birkhoff polynomial
area: graphs/coloring-and-cliques
level: advanced
summary: Polynomial P(G,k) that counts the proper k-colorings of G.
prereqs: [graph-coloring, chromatic-number, inclusion-exclusion-principle]
see_also: [deletion-contraction, counting-graph-colorings, chromatic-number, graph-coloring, four-color-theorem, inclusion-exclusion-principle, bjorklund-chromatic-number, k-coloring]
sources:
  - paper: doi:10.2307/1967597
    title: George D. Birkhoff, A determinant formula for the number of ways of coloring a map, Annals of Mathematics 14(1-4), 42 to 46 (1912)
    locator: the whole paper (the number of colorings of a map as a polynomial in the number of colors)
  - paper: doi:10.1090/S0002-9904-1932-04768-6
    title: Hassler Whitney, A logical expansion in mathematics, Bulletin of the American Mathematical Society 38(8), 572 to 579 (1932)
    locator: the expansion over edge subsets and the broken circuit theorem for the coefficients
  - paper: doi:10.1016/S0021-9800(68)80087-0
    title: Ronald C. Read, An introduction to chromatic polynomials, Journal of Combinatorial Theory 4(1), 52 to 71 (1968)
    locator: the whole paper (the basic properties, deletion-contraction, and the conjecture on the coefficients)
  - paper: doi:10.1016/0012-365X(73)90108-8
    title: Richard P. Stanley, Acyclic orientations of graphs, Discrete Mathematics 5(2), 171 to 178 (1973)
    locator: Corollary 1.3 ((-1)^n P(G,-1) is the number of acyclic orientations)
  - paper: doi:10.1090/S0894-0347-2012-00731-0
    title: June Huh, Milnor numbers of projective hypersurfaces and the chromatic polynomial of graphs, Journal of the American Mathematical Society 25(3), 907 to 927 (2012)
    locator: the main theorem (the absolute values of the coefficients form a log-concave sequence)
  - paper: doi:10.1017/S0963548300000705
    title: Bill Jackson, A zero-free interval for chromatic polynomials of graphs, Combinatorics, Probability and Computing 2(3), 325 to 336 (1993)
    locator: the main theorem (no real roots in (1, 32/27], and 32/27 is best possible)
---

The chromatic polynomial $P(G, k)$ of a graph $G$ is the number of proper colorings of the vertices of $G$ with at most $k$ colors, taken from a fixed set of $k$ colors. Birkhoff showed in 1912 that this number is a polynomial in $k$, of degree $n$, whose coefficients encode facts about $G$: the number of edges, triangles and components. The [chromatic number](/chromatic-number/) is the smallest positive integer $k$ with $P(G, k) > 0$. Computing $P(G, k)$ is #P-hard, and the standard tools are [deletion-contraction](/deletion-contraction/) and inclusion-exclusion over edge sets.

## In plain words

Take a network and a box of $k$ crayons. Count the ways to color every point so that two joined points never get the same crayon. That count changes with $k$, and it always follows a fixed polynomial formula in $k$.

For three points all joined to each other, the first point has $k$ choices, the second $k - 1$, the third $k - 2$. So the count is $k(k-1)(k-2)$. For a line of points, each point after the first only has to avoid one neighbor, so the count is $k$ times $(k-1)$ for each further point.

The formula tells you a lot. If it is zero for some $k$, the network cannot be colored with $k$ crayons.

## The idea

Let $G = (V, E)$ be a finite graph without loops, with $n$ vertices and $m$ edges, and let $[k] = \{1, \ldots, k\}$. Define

$$P(G, k) = \big|\{ c : V \to [k] \ \text{with}\ c(u) \ne c(v) \text{ for every edge } uv \}\big|, \qquad k = 0, 1, 2, \ldots$$

Parallel edges do not change $P$, and a loop makes it 0.

**It is a polynomial (Whitney's expansion).** For $S \subseteq E$, let $A_S$ be the set of maps $V \to [k]$ that are constant on both ends of every edge of $S$. Such a map is constant on each component of the spanning subgraph $(V, S)$, so $|A_S| = k^{c(S)}$, where $c(S)$ is the number of components of $(V, S)$. By the [inclusion-exclusion principle](/inclusion-exclusion-principle/) over the edges that are violated,

$$P(G, k) = \sum_{S \subseteq E} (-1)^{|S|}\, k^{c(S)}.$$

The right side is a polynomial in $k$ with integer coefficients. It agrees with the count at every non-negative integer $k$, so it defines $P(G, k)$ for all real or complex $k$.

**Deletion-contraction.** For an edge $e = uv$, the proper colorings of $G - e$ split into those with $c(u) \ne c(v)$, which are the proper colorings of $G$, and those with $c(u) = c(v)$, which correspond to the proper colorings of the contraction $G / e$. So

$$P(G, k) = P(G - e, k) - P(G / e, k).$$

Repeating this until no edge is left, where $P(\overline{K_r}, k) = k^r$, computes $P$. See [deletion-contraction](/deletion-contraction/).

**Properties.** For a graph $G$ with $n \ge 1$ vertices, $m$ edges and $c$ components:

1. $P(G, k)$ has degree $n$ and leading coefficient 1, from the term $S = \emptyset$.
2. The coefficient of $k^{n-1}$ is $-m$: the terms with $c(S) = n - 1$ are the single edges.
3. For a simple graph, the coefficient of $k^{n-2}$ is $\binom{m}{2} - t$, where $t$ is the number of triangles.
4. The coefficients alternate in sign, and the lowest non-zero term is $k^c$. So $k = 0$ is a root of multiplicity exactly $c$, and $P(G, 0) = 0$.
5. For disjoint graphs, $P(G \cup H, k) = P(G, k)\, P(H, k)$. If $G$ and $H$ meet in a clique $K_r$, then $P = P(G, k)\, P(H, k) / P(K_r, k)$.
6. $\chi(G) = \min \{ k \ge 1 : P(G, k) > 0 \}$, and $P(G, k) > 0$ for every integer $k \ge \chi(G)$.
7. $(-1)^n P(G, -1)$ is the number of acyclic orientations of $G$ (Stanley 1973).

Properties 1, 2 and 4 follow by induction from deletion-contraction: $G - e$ and $G / e$ have $m - 1$ edges, $G / e$ has $n - 1$ vertices, and the alternation is kept because the subtraction combines coefficients of opposite signs.

**Whitney's broken circuit theorem.** Fix an order of the edges. A *broken circuit* is a cycle with its largest edge removed. The coefficient of $k^{n-i}$ is $(-1)^i$ times the number of $i$-edge subsets of $E$ that contain no broken circuit. This gives a direct combinatorial meaning to each coefficient.

**Roots.** $P(G, k)$ has no real root in $(-\infty, 0)$ or in $(0, 1)$, and none in $(1, 32/27]$ (Jackson 1993); the value $32/27$ is best possible. The [four color theorem](/four-color-theorem/) says that $P(G, 4) > 0$ for every planar loopless $G$, which is how Birkhoff hoped to attack it.

**Coefficients.** Read (1968) conjectured that the absolute values of the coefficients are unimodal. Huh (2012) proved the stronger statement that they form a log-concave sequence.

## Examples

| graph | $P(G, k)$ | $P(G, 3)$ | $P(G, 4)$ | $(-1)^n P(G, -1)$ |
|---|---|---|---|---|
| $\overline{K_n}$, no edges | $k^n$ | $3^n$ | $4^n$ | 1 |
| $K_n$ | $k(k-1)\cdots(k-n+1)$ | 0 for $n \ge 4$ | $24$ for $n = 4$ | $n!$ |
| tree with $n$ vertices | $k(k-1)^{n-1}$ | $3 \cdot 2^{n-1}$ | $4 \cdot 3^{n-1}$ | $2^{n-1}$ |
| cycle $C_n$ | $(k-1)^n + (-1)^n (k-1)$ | $2^n + (-1)^n 2$ | $3^n + (-1)^n 3$ | $2^n - 2$ |
| triangle strip $S$ | $k(k-1)(k-2)^4$ | 6 | 192 | 162 |
| Petersen graph | degree 10, see below | 120 | 12960 | 16680 |

Here $S$ is the graph on $0, \ldots, 5$ with edges $01, 02, 12, 13, 23, 24, 34, 35, 45$. It is built from a triangle by adding 3 vertices, each joined to an edge, so property 5 gives the factor $(k-2)$ three times beyond $k(k-1)(k-2)$.

**Worked expansion.** For $C_4$, $P(C_4, k) = k^4 - 4k^3 + 6k^2 - 3k$:

- the coefficient $-4$ is $-m$;
- $6 = \binom{4}{2} - 0$, as $C_4$ has no triangle;
- the constant term is 0, and the coefficient of $k$ is non-zero, since $C_4$ is connected;
- $P(C_4, 2) = 16 - 32 + 24 - 6 = 2$, the two alternating colorings, and $P(C_4, -1) = 1 + 4 + 6 + 3 = 14 = 2^4 - 2$, the number of acyclic orientations of $C_4$.

**The Petersen graph.**

$$P = k^{10} - 15k^9 + 105k^8 - 455k^7 + 1353k^6 - 2861k^5 + 4275k^4 - 4305k^3 + 2606k^2 - 704k.$$

For $i \le 3$ the coefficient of $k^{10 - i}$ is $(-1)^i \binom{15}{i}$: in Whitney's expansion, a set $S$ with $c(S) = 10 - i$ that is not a forest would need a cycle of length at most $i + 1 \le 4$, and the graph has girth 5. The coefficient of $k^6$ is $\binom{15}{4} - 12 = 1353$, because each of the 12 five-cycles of the Petersen graph contributes one broken circuit of 4 edges. The values $P(3) = 120$ and $P(4) = 12960$ agree with a direct count over all $3^{10}$ and $4^{10}$ maps.

**Non-uniqueness.** All trees on $n$ vertices have the same polynomial $k(k-1)^{n-1}$, so $P(G, k)$ does not determine $G$. Graphs with the same polynomial are called *chromatically equivalent*.

## Where it is used

- **Exact chromatic number.** Evaluating $P(G, k)$ for $k = 1, 2, \ldots$ until it is positive gives $\chi(G)$. Björklund, Husfeldt and Koivisto compute $P(G, k)$ for one $k$ in $O^*(2^n)$ time by inclusion-exclusion over independent sets; see [Björklund's algorithm](/bjorklund-chromatic-number/) and [counting graph colorings](/counting-graph-colorings/).
- **Statistical physics.** $P(G, k)$ is the zero-temperature limit of the antiferromagnetic Potts model partition function with $k$ states, and it is the specialization $(-1)^{n - c} k^c\, T(G; 1 - k, 0)$ of the Tutte polynomial $T$.
- **Algebraic combinatorics.** The chromatic polynomial is the characteristic polynomial of the graphic matroid, up to a factor $k^c$, which is the setting of Huh's proof.
- **Map coloring.** Birkhoff introduced it to study the four color problem: the theorem is $P(G, 4) > 0$ for planar $G$.
- **Counting under constraints.** Problems such as frequency assignment and scheduling count the conflict-free assignments with $k$ labels, which is $P(G, k)$.

## References
