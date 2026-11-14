---
tag: A5A7MR
kind: algorithm
slug: magniez-santha-szegedy-triangle
name: Magniez-Santha-Szegedy triangle finding
aliases:
- MSS triangle algorithm
area: quantum/quantum-search
level: research
summary: A nested quantum walk that finds a triangle in an n-vertex graph with Õ(n^(13/10)) adjacency-matrix queries and one-sided bounded error, below the O(n^(3/2)) of Grover search.
solves: [triangle-finding]
model: quantum-query-model
complexity:
  vars: {n: the number of vertices, r: the size of the vertex set held by the walk}
  queries: {worst: "Õ(n^(13/10))"}
properties: {deterministic: false, exact: false, one_sided_error: true, oracle: bit}
history:
  year: 2003
  people: [Frédéric Magniez, Miklos Santha, Mario Szegedy]
  note: Posted as arXiv:quant-ph/0310134 in October 2003, presented at SODA 2005 and published in the SIAM Journal on Computing in 2007. It used Ambainis's element distinctness walk, from a preliminary version, for a new problem.
prereqs: [triangle-finding, ambainis-element-distinctness, amplitude-amplification, quantum-query-complexity]
see_also: [quantum-walk-search, belovs-k-distinctness, quantum-query-model, grover-search, boolean-matrix-multiplication, triangle-detection-hypothesis, quantum-random-access-memory, k-distinctness]
sources:
  - paper: doi:10.1137/050643684
    title: "Frédéric Magniez, Miklos Santha and Mario Szegedy, Quantum algorithms for the triangle problem, SIAM Journal on Computing 37(2), 2007, pages 413-424"
    locator: with the numbering of arXiv:quant-ph/0310134 version 3, Theorem 1 (the combinatorial algorithm with Õ(n^(10/7)) queries), Generic Algorithm, Theorem 2 and Corollaries 1 and 2 (the cost s(r) + (n/r)^(k/2)(c(r) + sqrt(r) u(r))), the cost table of Section 4.1, Theorem 3 (graph collision in Õ(n^(2/3))), Theorem 4 (Õ(n^(13/10)) at r = n^(3/5)) and Theorem 5 (a copy of a fixed graph on k vertices in Õ(n^(2 - 2/k)))
  - paper: arxiv:quant-ph/0310134
    title: "Frédéric Magniez, Miklos Santha and Mario Szegedy, Quantum algorithms for the triangle problem, Proceedings of the 16th ACM-SIAM SODA, 2005, pages 1109-1117"
    locator: the conference version, as given in the first footnote of the arXiv version
  - paper: doi:10.1137/S0097539705447311
    title: "Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1), 2007, pages 210-239"
    locator: with the numbering of arXiv:quant-ph/0311001, the walk on r-subsets and its analysis for one marked set
  - paper: doi:10.1137/S0097539702402780
    title: "Harry Buhrman, Christoph Dürr, Mark Heiligman, Peter Høyer, Frédéric Magniez, Miklos Santha and Ronald de Wolf, Quantum algorithms for element distinctness, SIAM Journal on Computing 34(6), 2005, pages 1324-1330"
    locator: the triangle result (O(n + sqrt(n m)) queries for a graph with m edges); a general locator
  - paper: doi:10.1137/090745854
    title: "Frédéric Magniez, Ashwin Nayak, Jérémie Roland and Miklos Santha, Search via quantum walk, SIAM Journal on Computing 40(1), 2011, pages 142-164"
    locator: with the numbering of arXiv:quant-ph/0608026, Theorem 3 (the cost of a walk search for any number of marked sets)
  - paper: doi:10.1145/2213977.2213985
    title: "Aleksandrs Belovs, Span programs for functions with constant-sized 1-certificates, Proceedings of the 44th ACM STOC, 2012, pages 77-84"
    locator: the abstract (triangle finding with O(n^(35/27)) queries by a learning graph), arXiv:1105.4024
  - paper: doi:10.1137/1.9781611973105.107
    title: "Troy Lee, Frédéric Magniez and Miklos Santha, Improved quantum query algorithms for triangle finding and associativity testing, Proceedings of the 24th ACM-SIAM SODA, 2013, pages 1486-1502"
    locator: the main result (O(n^(9/7)) queries); a general locator
  - paper: doi:10.1137/1.9781611973105.106
    title: "Stacey Jeffery, Robin Kothari and Frédéric Magniez, Nested quantum walks with quantum data structures, Proceedings of the 24th ACM-SIAM SODA, 2013, pages 1474-1485"
    locator: the abstract (nested walks reproduce the bounds O(n^(35/27)) and O(n^(9/7)) up to logarithmic factors), arXiv:1210.1199
  - paper: doi:10.1109/FOCS.2014.31
    title: "François Le Gall, Improved quantum algorithm for triangle finding via combinatorial arguments, Proceedings of the 55th IEEE FOCS, 2014, pages 216-225"
    locator: the abstract (Õ(n^(5/4)) queries, and the lower bound Omega(n^(9/7)/sqrt(log n)) of Belovs and Rosmanis for non-adaptive learning graphs), arXiv:1407.0085
---

The Magniez-Santha-Szegedy (MSS) algorithm finds a triangle in a graph on $n$ vertices with $\tilde O(n^{13/10})$ queries to the adjacency matrix, with one-sided bounded error. It runs a quantum walk on sets of $r = n^{3/5}$ vertices, as in [Ambainis's element distinctness algorithm](/ambainis-element-distinctness/), and its check is a second walk, for the *graph collision* problem, inside [amplitude amplification](/amplitude-amplification/) over the third vertex. [Grover search](/grover-search/) over all triples gives only $O(n^{3/2})$, and a classical algorithm needs $\Theta(n^2)$ queries. The bound is for the [quantum query model](/quantum-query-model/); see [quantum query complexity](/quantum-query-complexity/). This page is the algorithm; the problem and the later bounds, down to $\tilde O(n^{5/4})$, are on [triangle finding](/triangle-finding/).

## In plain words

You must find three people who all know each other, and you can only ask "do these two know each other?". A classical search asks about almost every pair. The quantum method keeps a small group of people in mind, in many versions at once, and it knows all the pairs inside the group. It tests whether the group holds two people of a triangle, and if not, it swaps one person for a new one. Quantum walks make this test and swap loop much cheaper than a classical loop. The test itself is clever: for each possible third person, it asks which group members that person knows, and looks for two of them who know each other. This inner search is a small quantum walk of its own. The result is a strong gain over plain quantum search.

## The problem

The input is a graph $G$ on the vertex set $[n] = \{1, \ldots, n\}$, given by the bit oracle $O_G|u, v\rangle|b\rangle = |u, v\rangle|b \oplus [uv \in E]\rangle$ on the adjacency matrix. The phase form is equivalent, with one query, by [phase kickback](/phase-kickback/). The output is a triangle $\{u, u', v\}$ of $G$, or "none" if $G$ has no triangle. The cost is the number of queries, with bounded error. The definition and the known bounds are on [triangle finding](/triangle-finding/).

## The algorithm

For a set $A$ of vertices, the data $D(A)$ are the edges of $G$ inside $A$. The set $A$ is *marked* when it contains an edge of some triangle. For a fixed vertex $v$, the *graph collision* problem on $G|A$ asks for an edge $uu'$ inside $A$ with $uv$ and $u'v$ both edges; it has a solution exactly when $uu'v$ is a triangle with $u, u' \in A$.

```pseudo id=main
MSS-TRIANGLE(n, O_G)
L1  r ← ⌈n^(3/5)⌉
L2  prepare the uniform superposition of |A⟩|D(A)⟩|x⟩ over r-sets A ⊆ [n] and x ∉ A    ▷ s(r) = r(r - 1)/2 queries
L3  repeat T1 = Θ(n/r) times
L4      flip the phase of |A⟩ if CHECK(A) finds a triangle                             ▷ c(r) queries, in superposition
L5      do T2 = Θ(√r) steps of the walk: swap one vertex of A with x, and update D(A)   ▷ 2r queries per step
L6  measure A, and return CHECK(A), a triangle or "none"
CHECK(A), with D(A) known
L7  amplitude amplification over v ∈ [n] with Θ(√n) rounds, for a v for which L8 succeeds
L8      graph collision on G|A with f(u) = [uv ∈ E], by the walk of Ambainis on r^(2/3)-subsets of A   ▷ Õ(r^(2/3)) queries
L9  return (u, u', v) for the edge uu' found by L8, or "none"
```

Line L5 is one step of the walk of Ambainis on the states $|A\rangle|x\rangle$: diffuse $x$ over the vertices outside $A$, add $x$ to $A$, diffuse $x$ over $A$, and remove $x$ from $A$; each change of $A$ reads or erases $r$ edge bits of $D(A)$. Lines L3 to L5 are the search of [quantum walk search](/quantum-walk-search/) on the Johnson graph of $r$-sets, with the phase flip in place of a check of the state. In line L8 the edges of $G|A$ are free, since they are in $D(A)$; only the values $f(u)$ cost queries, so the inner walk has setup $q$, update $1$ and check $0$ on $q$-subsets.

## Example

Take $n = 8$ and the graph with only the triangle $\{0, 1, 2\}$, and use $r = 3$ (here $n^{3/5} \approx 3.5$).

1. For $A = \{0, 1, 5\}$, the edge $01$ is inside $A$. For $v = 2$, $f(0) = f(1) = 1$, so graph collision finds $01$, and CHECK returns the triangle $(0, 1, 2)$. For $A = \{0, 3, 5\}$ no $v$ works, and CHECK returns "none".
2. A set is marked when it holds two of $0, 1, 2$: $3 \cdot 5 + 1 = 16$ of the $56$ sets, so a random set is marked with probability $2/7 \approx 0.286$.
3. With $T_2 = 2$ walk steps per round, the probability that the measured $A$ is marked after $T_1 = 0, 1, \ldots, 5$ rounds is $0.286, 0.697, 0.325, 0.055, 0.823, 0.546$. It does not follow a clean sine curve, since two steps of the walk only approximate the reflection of an exact amplitude amplification.
4. The run with $T_1 = 4$ costs $3$ queries for the setup, $4 \cdot 2 \cdot 6 = 48$ for the walk steps and $5$ checks of $c(3) = \sqrt{8} \cdot 3^{2/3} \approx 5.9$ each, about 80 in all, more than the 28 entries of the matrix. The gain shows only for large $n$: at $n = 10^6$ the formula gives about $2.0 \cdot n^{1.3} \approx 1.3 \cdot 10^8$, against $n^{3/2} = 10^9$ for Grover search and about $5 \cdot 10^{11}$ entries.

The Python file simulates lines L2 to L6 exactly on the states $|A\rangle|x\rangle$ for graphs with up to 10 vertices; there, CHECK is run classically and its quantum cost $c(r)$ is counted by the formula, so the simulation covers the outer walk but not the inner walks of L7 and L8. The tests check the exact optimum $r = n^{3/5}$ with exponent $13/10$ of the cost formula, with Fractions, and that the plain check $c(r) = \sqrt{n}\,r$ gives only $3/2$; the cost formula against its minimum over $r$ for $n = 10^4$ to $10^8$; graph collision at $q = r^{2/3}$; CHECK against brute force on all 1024 graphs on 5 vertices for every set of 2 or 3 vertices; the query counts of the data structure; the eigenvector of the Johnson walk with eigenvalue $1 - n/(r(n - r))$; the gain on one triangle for $n = 8, 9, 10$; and, with seed 2026, 40 random graphs against a brute-force list of triangles: a returned triangle is always real, a triangle-free graph always gives "none", and at least 80% of the graphs with a triangle give one within five runs.

## Correctness

1. **One-sided error.** Line L9 returns $(u, u', v)$ only for edges $uu'$, $uv$ and $u'v$, so every output is a triangle of $G$, and a triangle-free graph gives "none".
2. **The check.** CHECK$(A)$ finds a triangle exactly when a triangle of $G$ has an edge inside $A$: for such a triangle $uu'v$, the graph collision instance of $v$ has the solution $uu'$, and L7 finds a good $v$.
3. **The marked fraction.** If $G$ has a triangle $\{a, b, c\}$, every $r$-set that holds $a$ and $b$ is marked, a fraction $\varepsilon = r(r-1)/(n(n-1)) \approx (r/n)^2$.
4. **The walk.** The walk that swaps one vertex of $A$ is the walk on the Johnson graph, with spectral gap $\delta = n/(r(n - r)) \ge 1/r$. By the theorem of [quantum walk search](/quantum-walk-search/), $O(1/\sqrt{\varepsilon}) = O(n/r)$ rounds of $O(1/\sqrt{\delta}) = O(\sqrt{r})$ steps give a marked set with constant probability. The original analysis of Ambainis assumed one marked set; MSS reduce the general case to it with random restrictions, at a logarithmic cost, and the later MNRS theorem needs no such step.

The full proof is in the proof file.

## Complexity

- **Queries:** $\tilde O(s + (n/r)(c + \sqrt{r}\,u))$ with $s = r^2$, $u = r$ and $c = \sqrt{n}\,r^{2/3}$, that is $\tilde O(r^2 + n^{3/2}r^{-1/3} + n r^{1/2})$. The last two terms are equal at $r = n^{3/5}$, where the total is $\tilde O(n^{13/10})$, about $n^{1.3}$; the setup term is $n^{6/5}$.
- **Error:** one-sided and bounded; a constant number of runs gives success probability $2/3$. The logarithmic factors come from the error reduction of the many checks and from the reduction to one marked set.
- **Space:** the data register holds the $r(r-1)/2$ edge bits of $G|A$, about $n^{6/5}/2$ qubits.
- **Time:** the query bound is not a time bound. Each walk step changes $r$ bits of the data register, and a fast step needs [quantum random access memory](/quantum-random-access-memory/) or a quantum data structure.

## Properties

- Bounded-error and one-sided: it never returns a false triangle.
- It uses the bit oracle of the adjacency matrix; the phase oracle is equivalent.
- It uses quantum walks at two levels: the check of the outer walk is a second walk inside amplitude amplification.
- It finds a triangle, so it also decides whether one exists.

## Variants and improvements

- **The combinatorial algorithm** of the same paper needs $\tilde O(n^{10/7})$ queries and only $O(\log n)$ qubits in its quantum parts. It uses only Grover search and the neighborhoods of random vertices.
- **Fixed subgraphs.** The same method finds a copy of a fixed graph $H$ on $k > 3$ vertices in $\tilde O(n^{2 - 2/k})$ queries (Theorem 5 of the paper), and the same bound holds for monotone graph properties with 1-certificates of at most $k$ vertices.
- **Sparse graphs.** Buhrman et al. gave $O(n + \sqrt{nm})$ queries for a graph with $m$ edges, the first quantum triangle bound.
- **Later query bounds.** Belovs's learning graphs gave $O(n^{35/27})$ (posted 2011, STOC 2012), Lee, Magniez and Santha gave $O(n^{9/7})$ (SODA 2013), and Le Gall gave $\tilde O(n^{5/4})$ (FOCS 2014). Jeffery, Kothari and Magniez reproduced the first two with nested quantum walks and quantum data structures.

## When to use it

Use it as the model of a nested quantum walk: an outer walk on sets of vertices whose check is a second quantum search. For the best query bound for triangles, the later algorithms on [triangle finding](/triangle-finding/) are better. For time on a real machine, the data structures of the walk matter more than the query count, and on dense graphs classical fast [Boolean matrix multiplication](/boolean-matrix-multiplication/) finds triangles in time $O(n^\omega)$.

## Pitfalls

- **The value of $r$.** The proof of Theorem 4 in the arXiv version first sets $r = n^{2/3}$ and then evaluates the cost at $r = n^{3/5}$. The right value is $n^{3/5}$; at $n^{2/3}$ the walk term is $n^{4/3}$.
- **The exponent.** The bound is $\tilde O(n^{13/10})$ with logarithmic factors, not $O(n^{1.3})$ exactly.
- **A plain check is not enough.** With CHECK done by Grover search over $v$ and the pairs of $A$, $c = \sqrt{n}\,r$, and the term $(n/r)c$ is $n^{3/2}$ for every $r$; the graph collision walk is what brings the gain.
- **Queries are not time.** See the complexity section.
- **Several marked sets.** The walk of Ambainis was first analysed for one marked set. Use the MNRS theorem, or random restrictions with a logarithmic factor.

## Implementations

## History

Buhrman, Dürr, Heiligman, Høyer, Magniez, Santha and de Wolf asked for the quantum query complexity of triangle finding and gave $O(n + \sqrt{nm})$, which is $O(n^{3/2})$ on dense graphs. Magniez, Santha and Szegedy posted their paper in October 2003, shortly before Ambainis posted his element distinctness walk; they worked from a preliminary version of it. It gave $\tilde O(n^{10/7})$ by combinatorics and $\tilde O(n^{13/10})$ by the nested walk, appeared at SODA 2005, and was published in the SIAM Journal on Computing in 2007. The bound stood until Belovs's learning graphs, posted in 2011 and published at STOC 2012.

## References
