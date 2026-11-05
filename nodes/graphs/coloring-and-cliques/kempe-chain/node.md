---
tag: G3FG4B
kind: concept
slug: kempe-chain
name: Kempe chain
aliases:
- Kempe chain interchange
- Kempe chains
area: graphs/coloring-and-cliques
level: advanced
summary: Maximal subgraph two-colored alternately; swapping its two colors keeps the coloring proper.
prereqs: [graph-coloring, connected-components]
see_also: [five-color-theorem, four-color-theorem, vizing-theorem, vizing-algorithm, brooks-theorem, edge-coloring, alternating-path, planar-graph-coloring]
sources:
  - paper: doi:10.2307/2369235
    title: A. B. Kempe, On the geographical problem of the four colours, American Journal of Mathematics 2(3), 193 to 200 (1879)
    locator: the whole paper (the chain interchange argument and the flawed proof of the four color theorem)
  - paper: "P. J. Heawood, Map-colour theorem, Quarterly Journal of Pure and Applied Mathematics 24, 332 to 338 (1890)"
    locator: the counterexample to Kempe's argument and the proof of the five color theorem
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 5.1, Colouring maps and planar graphs (proof of the five colour theorem); Section 5.3, Edge-colouring (proof of Vizing's theorem)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 6.3, Coloring of planar graphs (Kempe chains and the five color theorem)
---

A Kempe chain of a properly colored graph is a connected component of the subgraph induced by the vertices of two chosen colors $a$ and $b$. Its colors alternate along every path inside it, and swapping $a$ and $b$ on the whole chain gives another proper coloring. This swap, the Kempe interchange, is the main tool in the proof of the [five color theorem](/five-color-theorem/), in Kempe's flawed 1879 proof of the four color theorem, and, in its edge form, in the proof of [Vizing's theorem](/vizing-theorem/).

## In plain words

Pick two colors, say red and blue, in a colored map. Start at one red country and walk to every red or blue neighbor, then to their red or blue neighbors, and so on. The countries you reach form a chain.

Now turn every red country in the chain blue and every blue one red. Inside the chain, neighbors still differ, because they were different before and both changed. At the edge of the chain, every neighbor has a third color, or it would belong to the chain. So the map stays properly colored.

The trick is useful because it can free a color at one place without breaking anything elsewhere.

## The idea

Let $c : V \to \{1, \ldots, k\}$ be a proper coloring of a graph $G$, and let $a \ne b$ be two colors. Write $G_{a,b}$ for the subgraph induced by $c^{-1}(a) \cup c^{-1}(b)$. For a vertex $v$ with $c(v) \in \{a, b\}$, the **Kempe chain** $K_{a,b}(v)$ is the connected component of $G_{a,b}$ that contains $v$; see [connected components](/connected-components/).

**Lemma.** Let $K = K_{a,b}(v)$ and define $c'$ by $c'(u) = b$ if $u \in K$ and $c(u) = a$, $c'(u) = a$ if $u \in K$ and $c(u) = b$, and $c'(u) = c(u)$ otherwise. Then $c'$ is a proper coloring.

*Proof.* Take an edge $uw$. If neither end is in $K$, nothing changed. If both are in $K$, then $\{c(u), c(w)\} = \{a, b\}$ because $c$ is proper and both colors lie in $\{a, b\}$; the swap keeps them different. If $u \in K$ and $w \notin K$, then $c(w) \notin \{a, b\}$, since otherwise $w$ would be in the same component of $G_{a,b}$ as $u$. So $c'(w) = c(w) \notin \{a, b\}$ while $c'(u) \in \{a, b\}$. $\square$

The lemma needs the whole component. Swapping only part of a chain can put the same color on two adjacent vertices.

Two colorings are **Kempe equivalent** when a sequence of Kempe interchanges turns one into the other. The same idea works for edges: in a proper [edge coloring](/edge-coloring/), the edges of colors $a$ and $b$ form paths and even cycles, since each vertex meets at most one edge of each color, and swapping the colors on one such component keeps the edge coloring proper. These components are the Kempe chains of the [line graph](/line-graph/), and they are [alternating paths](/alternating-path/) in the sense of matchings.

## Examples

**A 5-cycle.** Take $C_5$ with edges $01, 12, 23, 34, 40$ and the coloring $c = (1, 2, 1, 2, 3)$ on the vertices $0, \ldots, 4$.

| colors | subgraph $G_{a,b}$ | chains | after swapping the chain of vertex 0 |
|---|---|---|---|
| 1, 2 | path $0\!-\!1\!-\!2\!-\!3$ | $\{0, 1, 2, 3\}$ | $(2, 1, 2, 1, 3)$ |
| 1, 3 | edge $40$, vertex $2$ | $\{0, 4\}$, $\{2\}$ | $(3, 2, 1, 2, 1)$ |
| 2, 3 | edge $34$, vertex $1$ | $\{3, 4\}$, $\{1\}$ | vertex 0 is in no chain |

Both swapped colorings are proper. Swapping colors 1 and 2 on vertex 0 alone would give $(2, 2, 1, 2, 3)$, with a conflict on the edge $01$.

**Freeing a color in the five color theorem.** In a planar graph, let $v$ have five neighbors $v_1, \ldots, v_5$ in clockwise order, colored $1, \ldots, 5$, with $v$ itself not yet colored. If $v_1$ and $v_3$ lie in different $\{1, 3\}$-chains, swap the chain of $v_1$: now no neighbor of $v$ has color 1, and $v$ takes it. Otherwise a path of colors 1 and 3 joins $v_1$ to $v_3$, and with $v$ it closes a cycle that separates $v_2$ from $v_4$ in the plane. So $v_2$ and $v_4$ lie in different $\{2, 4\}$-chains, and swapping the chain of $v_2$ frees color 2.

**Kempe's error.** Kempe ran the same argument with four colors for a vertex of degree 5, and made two swaps at once. Heawood found in 1890 that the two chains he swapped can cross, so the second swap can undo the first. The four color theorem needed another 86 years and a computer.

## Where it is used

- **Planar coloring.** The proof of the [five color theorem](/five-color-theorem/) and the linear-time [five color algorithm](/five-color-algorithm/) both rest on one Kempe interchange at a vertex of degree at most 5. The reducibility part of the proof of the [four color theorem](/four-color-theorem/) also uses Kempe interchanges on many configurations.
- **Edge coloring.** [Vizing's theorem](/vizing-theorem/) and the [Misra-Gries algorithm](/vizing-algorithm/) swap the colors on an alternating path of two colors to free a color at a vertex. König's edge coloring theorem for bipartite graphs is proved the same way.
- **Brooks' theorem.** One proof of [Brooks' theorem](/brooks-theorem/) recolors along Kempe chains to save a color at a vertex of degree $\Delta$.
- **Local search and sampling.** Kempe moves are a neighborhood for local search in timetabling, and the Wang-Swendsen-Kotecký Markov chain of statistical physics samples colorings with them.

## References
