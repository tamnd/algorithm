---
tag: XKW8W3
kind: theorem
slug: crossing-lemma
name: Crossing lemma
aliases:
- Ajtai-Chvátal-Newborn-Szemerédi crossing lemma
area: graphs/planar-graphs
level: advanced
summary: A simple graph with n vertices and m >= 4n edges has crossing number at least m^3/(64 n^2).
prereqs: [crossing-number, euler-formula, planar-edge-bound]
see_also: [crossing-number, graph-drawing, planar-separator-theorem, fary-theorem, kuratowski-theorem, planarization-heuristic]
sources:
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: the chapter on crossing numbers of graphs (the probabilistic proof of the crossing lemma)
  - paper: "Miklós Ajtai, Václav Chvátal, Monroe M. Newborn and Endre Szemerédi, Crossing-free subgraphs, Annals of Discrete Mathematics 12, 9 to 12 (1982)"
    locator: the first proof of the lower bound c m^3/n^2
  - book: "F. Thomson Leighton, Complexity Issues in VLSI, MIT Press, 1983"
    locator: the independent proof of the crossing lemma and its use for VLSI layout area
  - paper: "László A. Székely, Crossing numbers and hard Erdős problems in discrete geometry, Combinatorics, Probability and Computing 6(3), 353 to 358 (1997)"
    locator: the proofs of the Szemerédi-Trotter theorem and the unit distance bound from the crossing lemma
  - paper: "János Pach and Géza Tóth, Graphs drawn with few crossings per edge, Combinatorica 17(3), 427 to 439 (1997)"
    locator: the improved constant from bounds on graphs with few crossings per edge
  - paper: "Eyal Ackerman, On topological graphs with at most four crossings per edge, Computational Geometry 85, 101574 (2019)"
    locator: the constant 1/29 for m at least 7n
---

The crossing lemma says that a graph with many more edges than vertices has many crossings in every drawing: if a simple graph has $n$ vertices and $m \ge 4n$ edges, then its [crossing number](/crossing-number/) is at least $m^3 / (64 n^2)$. The bound from [Euler's formula](/euler-formula/) alone is only linear in $m$; the crossing lemma boosts it to cubic by applying Euler's bound to a random induced subgraph. The order $m^3/n^2$ is best possible. Through Székely's method, the lemma gives short proofs of central bounds in combinatorial geometry, such as the Szemerédi-Trotter theorem on point-line incidences.

## Statement

All graphs are finite and simple. For a graph $G$, $\mathrm{cr}(G)$ is the least number of crossings in a drawing of $G$ in the plane (see [crossing number](/crossing-number/) for the precise notion of drawing).

**Theorem (Ajtai, Chvátal, Newborn and Szemerédi; Leighton).** If $G$ has $n$ vertices and $m \ge 4n$ edges, then

$$\mathrm{cr}(G) \ge \frac{m^3}{64 n^2}.$$

The statement is about the abstract graph and all of its drawings, so no embedding is given. The proof uses one optimal drawing, given by coordinates and curves (or as a planarization with a rotation system), only to count crossings.

## In plain words

Draw a network with many more links than points. Then the drawing must have a lot of crossings, and the count grows quickly: double the number of links while keeping the points, and the forced crossings go up eightfold.

The reason is a trick with chance. Pick a random part of the points and keep only the links among them. Each crossing survives only if all four of its points are kept, which is rare, but links survive more often. A network that is too dense must still have crossings, so the original drawing must have had many. Choosing how many points to keep in the best way gives the bound.

## Proof

**Step 1: a linear bound.** For every simple graph, $\mathrm{cr}(G) \ge m - 3n$. Take a drawing with $\mathrm{cr}(G)$ crossings and delete one edge at each crossing; the remaining graph is planar and simple, so it has at most $3n - 6$ edges when $n \ge 3$ (the [planar edge bound](/planar-edge-bound/)) and at most $1 \le 3n$ edge when $n \le 2$. So $m - \mathrm{cr}(G) \le 3n$.

**Step 2: a good optimal drawing.** Fix a drawing $D$ of $G$ with $X = \mathrm{cr}(G)$ crossings. In an optimal drawing, adjacent edges do not cross (otherwise exchanging the pieces of the two edges between their common end and the crossing, and smoothing, removes that crossing without creating new ones). So each crossing involves two edges with four distinct ends.

**Step 3: random sampling.** Let $0 < p \le 1$, and keep each vertex independently with probability $p$. Let $G_p$ be the induced subgraph on the kept vertices, drawn as in $D$, and let $n_p$, $m_p$, $X_p$ be its numbers of vertices, edges and crossings of $D$ that remain. An edge remains with probability $p^2$, and a crossing remains with probability $p^4$, by Step 2. By linearity of expectation,

$$\mathbb{E}[n_p] = pn, \qquad \mathbb{E}[m_p] = p^2 m, \qquad \mathbb{E}[X_p] = p^4 X.$$

The drawing of $G_p$ has $X_p$ crossings, so $X_p \ge \mathrm{cr}(G_p) \ge m_p - 3n_p$ by Step 1, for every outcome. Taking expectations, $p^4 X \ge p^2 m - 3pn$, that is,

$$X \ge \frac{m}{p^2} - \frac{3n}{p^3}.$$

**Step 4: the choice of $p$.** Put $p = 4n/m$, which is at most 1 because $m \ge 4n$. Then

$$X \ge \frac{m^3}{16 n^2} - \frac{3 n m^3}{64 n^3} = \frac{4 m^3 - 3 m^3}{64 n^2} = \frac{m^3}{64 n^2}. \qquad \blacksquare$$

## Consequences

**Szemerédi-Trotter theorem (Székely's proof).** Let $P$ be a set of points and $L$ a set of lines in the plane, and let $I$ be the number of pairs $(q, \ell)$ with $q \in P$ on $\ell \in L$. Then $I \le 4 |P|^{2/3} |L|^{2/3} + 4|P| + |L|$.

*Proof.* Build a graph on $P$: on each line, join consecutive points of $P$. A line with $k \ge 1$ points gives $k - 1$ edges, so $m \ge I - |L|$. The graph is simple, since two points lie on one common line. Its drawing along the lines has at most $\binom{|L|}{2} < |L|^2$ crossings, since two lines meet at most once. If $m < 4|P|$, then $I < 4|P| + |L|$. Otherwise the crossing lemma gives $|L|^2 > m^3 / (64 |P|^2)$, so $m < 4 |P|^{2/3} |L|^{2/3}$, and $I \le m + |L|$. $\square$

**Unit distances.** Among $n$ points in the plane, at most $O(n^{4/3})$ pairs are at distance 1 (Székely): draw unit circles around the points and apply a version of the lemma for multigraphs with bounded edge multiplicity.

**VLSI layout.** Leighton used the lemma to bound the area of chip layouts from below; see [crossing number](/crossing-number/).

**Bisection and separators.** Together with [planar separator](/planar-separator-theorem/) arguments, crossing bounds give lower bounds on the bisection width of dense drawings, and conversely.

## Tightness

**The order $m^3/n^2$ is best possible.** Let $k \ge 9$ and let $G$ be the disjoint union of $n/k$ copies of $K_k$. Then $m = (n/k)\binom{k}{2} \approx nk/2$, and drawing each copy with at most $k^4/64$ crossings (the cylindrical drawing achieving Guy's number $Z(k) \le k^4/64$) gives $\mathrm{cr}(G) \le (n/k) k^4/64 = nk^3/64 \approx m^3/(8n^2)$. So the bound is off by at most a constant factor.

**The constant.** The constant $1/64$ comes from this simple proof. Using better bounds for graphs whose drawings have few crossings per edge, Pach and Tóth improved it, and Ackerman proved $\mathrm{cr}(G) \ge m^3/(29 n^2)$ for $m \ge 7n$. The best possible constant is unknown.

**The condition on $m$.** Some condition like $m \ge 4n$ is needed: [maximal planar graphs](/maximal-planar-graph/) have $m = 3n - 6$ and $\mathrm{cr} = 0$, while $m^3/(64n^2) > 0$. With the condition $m \ge 4n$ replaced by $m > 3n$, a weaker form $\mathrm{cr}(G) \ge c\, m^3/n^2$ still holds with a smaller constant depending on how far $m$ exceeds $3n$.

**Small cases.**

| graph | $n$ | $m$ | lemma applies? | bound | $\mathrm{cr}$ |
|---|---|---|---|---|---|
| single vertex, any tree | $n$ | $n - 1$ | no ($m < 4n$) | | 0 |
| $K_4$ | 4 | 6 | no | | 0 |
| $K_5$ | 5 | 10 | no | Step 1 gives $10 - 15 < 0$; Euler gives 1 | 1 |
| $K_{3,3}$ | 6 | 9 | no | Euler for triangle-free gives 1 | 1 |
| $K_9$ | 9 | 36 | yes ($36 = 4 \cdot 9$) | $36^3/(64 \cdot 81) = 9$ | $36 = Z(9)$ |
| $K_{16}$ | 16 | 120 | yes | $120^3/(64 \cdot 256) \approx 105.5$, so at least 106 | at most $Z(16) = 588$; the exact value is open |

For small graphs, the Euler bound $m - 3n + 6$ is often stronger: for $K_9$ it gives $36 - 21 = 15$, and for $K_{16}$ it gives $120 - 42 = 78$, against 106 from the lemma. The lemma wins once $m$ is large compared with $n$; for $K_n$ it grows like $n^4/512$, while the Euler bound grows like $n^2/2$.

## History

Ajtai, Chvátal, Newborn and Szemerédi proved the lemma in 1982 in a paper on crossing-free subgraphs, with a smaller constant, and Leighton found it independently in 1983 while studying VLSI layouts. The short probabilistic proof above is folklore; it is usually credited to Chazelle, Sharir and Welzl and appears in Proofs from THE BOOK. In 1997 Székely showed that the lemma gives simple proofs of the Szemerédi-Trotter theorem and of bounds on unit distances and on $k$-sets, which made it a standard tool in discrete geometry. Pach and Tóth (1997) and later Ackerman improved the constant.

## References
