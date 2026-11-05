---
tag: 2PN4W8
kind: concept
slug: blossom
name: Blossom
aliases:
- odd cycle in an alternating tree
area: graphs/matching
level: advanced
summary: An odd alternating cycle contracted during Edmonds' search for augmenting paths.
prereqs: [augmenting-path, alternating-path]
see_also: [edmonds-blossom, micali-vazirani-algorithm, gallai-edmonds-decomposition, tutte-berge-formula, maximum-weight-matching, edmonds-polytope-theorem, lowest-common-ancestor, maximum-matching]
sources:
  - paper: doi:10.4153/CJM-1965-045-4
    title: Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17, 449 to 467 (1965)
    locator: the whole paper (blossoms, flowers, and the shrinking of blossoms in the search for augmenting paths)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.3, Matchings in general graphs (Edmonds' blossom algorithm)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 24.2, Cardinality matching algorithm (the shrinking of odd circuits)
---

A blossom, for a matching $M$ in a [graph](/graph/), is an odd cycle of $2k + 1$ edges of which $k$ are in $M$, so that exactly one vertex of the cycle, its base, is not matched along the cycle. Blossoms are what make matching in general graphs harder than in [bipartite graphs](/bipartite-graph/): they let one vertex be reached by [alternating paths](/alternating-path/) of both parities, which breaks the simple search for [augmenting paths](/augmenting-path/). Edmonds' answer, the core of [Edmonds' blossom algorithm](/edmonds-blossom/), is to contract a blossom to one vertex: the matching is maximum in the original graph if and only if it is maximum in the contracted one. Blossoms exist only in non-bipartite graphs; the definition is unweighted, and weighted matching algorithms attach a dual variable to each blossom.

## In plain words

To make a matching bigger, you look for a chain that starts at an unpaired vertex, switches between unused and used edges, and ends at another unpaired vertex. In a graph with two sides you can tell for each vertex whether the chain arrives there on an unused or a used edge, and you never need to visit it twice.

With an odd ring of vertices this breaks down. Going round the ring one way, the chain arrives at a vertex on an unused edge; going the other way, on a used edge. The trick is to squeeze the whole ring into one point, search the smaller graph, and when a chain passes through the point, unfold the ring and choose the way round that keeps the switching pattern.

## The idea

Let $G = (V, E)$ be a graph and $M$ a matching. Grow an *alternating tree* from a free vertex $r$: $r$ is *outer*; from an outer vertex $u$ follow an unmatched edge $uv$ to a vertex $v$ not yet in the tree, which becomes *inner*, and then the matched edge $vw$ to its partner $w$, which becomes outer. Every tree path from $r$ to an outer vertex is an alternating path of even length that ends with a matched edge, or has no edge.

**Definition.** Suppose an edge $uv \notin M$ joins two outer vertices of the same tree. Let $b$ be their lowest common ancestor. The tree paths from $b$ to $u$ and from $b$ to $v$, with the edge $uv$, form a cycle $B$. This cycle is a **blossom** with **base** $b$, and the tree path from $r$ to $b$ is its **stem**; Edmonds called a blossom with its stem a *flower*. The base $b$ is outer, because an inner vertex has one child, its partner, so two different branches cannot split at it.

**Facts about a blossom $B$ with base $b$.**

1. *$B$ is odd and alternates.* The tree path from $b$ to an outer vertex has even length, so $|B| = 2i + 2j + 1$ for the two path lengths $2i$ and $2j$. Each path starts at $b$ with an unmatched edge and alternates, and $uv$ is unmatched, so $B$ has $i + j = k$ matched edges, and every vertex of $B$ except $b$ is matched to a neighbour on $B$. The base is matched by its stem edge, or free if $b = r$.
2. *Every vertex of $B$ is outer in effect.* For each $x \in B$, one of the two ways round $B$ from $b$ to $x$ has even length. Following the stem and then that way gives an alternating path from $r$ to $x$ that ends with a matched edge, or ends at $b$. So from every vertex of $B$ the search may follow unmatched edges, as from an outer vertex.
3. *Removing any vertex leaves a perfect matching.* For $x \in B$, the cycle minus $x$ is a path with $2k$ vertices, which has a perfect matching. Graphs with this property are called factor-critical, and they are the building blocks of the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/).

**Contraction.** Let $G/B$ be the graph obtained by replacing the vertices of $B$ by one new vertex $\beta$, keeping each edge with one end in $B$ as an edge at $\beta$, and dropping the edges inside $B$. Let $M/B = M \setminus E(B)$, which is a matching of $G/B$ with $|M| - k$ edges: $\beta$ is matched by the stem edge of $b$, or free if $b$ is free.

**Theorem (Edmonds).** $M$ is a maximum matching of $G$ if and only if $M/B$ is a maximum matching of $G/B$.

*Proof.* Let $S$ be the stem, an alternating path from the free vertex $r$ to $b$ of even length. Flipping it, $M_1 = M \triangle E(S)$ is a matching of the same size, for which $b$ is free and $B$ is still alternating with base $b$; and $M_1/B = (M/B) \triangle E(S/B)$ has the same size as $M/B$, where $S/B$ is the stem ending at $\beta$. So $M$ is maximum if and only if $M_1$ is, and $M/B$ if and only if $M_1/B$ is, and it suffices to prove the theorem for $M_1$, for which $b$ is free and $\beta$ is free in $G/B$.

(If $M_1/B$ is not maximum, neither is $M_1$.) By [Berge's lemma](/berge-lemma/) there is an $M_1/B$-augmenting path $P'$ in $G/B$. If $P'$ avoids $\beta$, it is an $M_1$-augmenting path in $G$. Otherwise $\beta$ is free, so it is an end of $P'$, and the first edge of $P'$ comes from an edge $x y$ with $x \in B$, $y \notin B$, $xy \notin M_1$. Replace $\beta$ by the way round $B$ from $b$ to $x$ that has even length. It starts at $b$ with an unmatched edge, alternates, and so ends at $x$ with a matched edge; then $xy$ is unmatched. The result is an $M_1$-augmenting path in $G$ from the free vertex $b$.

(If $M_1$ is not maximum, neither is $M_1/B$.) Let $P$ be an $M_1$-augmenting path in $G$. If $P$ avoids $B$, it is augmenting in $G/B$. Otherwise, $P$ has two free ends and $b$ is the only free vertex of $B$, so one end $u$ of $P$ is not in $B$. Walk along $P$ from $u$ to the first vertex $x$ of $B$. In $G/B$ this part becomes a path from $u$ to $\beta$; it alternates, it starts at the free vertex $u$, and it ends at the free vertex $\beta$, so it is $M_1/B$-augmenting. $\square$

**Consequences.** The search may contract a blossom as soon as it finds one, continue in $G/B$ with $\beta$ as an outer vertex, and expand the blossoms afterwards, choosing the even way round each one; blossoms can nest, since $\beta$ can lie on a later blossom. If $M$ is maximum and $B$ is a blossom for $M$, then $\nu(G) = \nu(G/B) + k$. In a bipartite graph every cycle is even, so no edge ever joins two outer vertices of a tree and no blossom appears. In weighted matching, each contracted blossom gets a dual variable $z_B$ for the odd-set constraint $x(E(B)) \le k$, the constraints of [Edmonds' matching polytope theorem](/edmonds-polytope-theorem/).

## Examples

**A blossom with a stem.** Take the vertices $s, a, b, c, d, e, f, t$ and the edges $sa$, $ab$, $bc$, $cd$, $de$, $ef$, $fb$, $et$, with $M = \{ab, cd, ef\}$. The free vertices are $s$ and $t$.

| step | action | labels |
|---|---|---|
| 1 | root $s$ | $s$ outer |
| 2 | $s \to a$, then $a \Rightarrow b$ | $a$ inner, $b$ outer |
| 3 | $b \to c$, $c \Rightarrow d$; $b \to f$, $f \Rightarrow e$ | $c, f$ inner, $d, e$ outer |
| 4 | edge $de$ joins two outer vertices; their lowest common ancestor is $b$ | blossom $B = b\,c\,d\,e\,f$, base $b$, stem $s\,a\,b$ |
| 5 | contract $B$ to $\beta$; $G/B$ has edges $sa$, $a\beta$, $\beta t$ and $M/B = \{a\beta\}$ | $\beta$ outer |
| 6 | $\beta \to t$, and $t$ is free | augmenting path $s\,a\,\beta\,t$ in $G/B$ |
| 7 | $t$ is joined to $e \in B$; the even way from $b$ to $e$ is $b\,f\,e$ | augmenting path $s\,a\,b\,f\,e\,t$ in $G$ |

Flipping $s\,a\,b\,f\,e\,t$ gives the perfect matching $\{sa, bf, et, cd\}$. A search that ignores blossoms can fail here: if it reaches $e$ first along $s\,a\,b\,c\,d\,e$, it labels $e$ inner, follows only the matched edge $ef$ out of $e$, and never tries the edge $et$.

**A blossom with free base.** In the graph with the 5-cycle $r\,a\,b\,c\,d$, the extra edge $cx$, and $M = \{ab, cd\}$, the tree from $r$ finds the edge $bc$ between the outer vertices $b$ and $c$, and the blossom is the whole 5-cycle with base $r$ and an empty stem. Contracted, it leaves the edge $\beta x$ with both ends free, and expanding gives the augmenting path $r\,d\,c\,x$, as on the [alternating path](/alternating-path/) page.

**No augmenting path.** In the triangle $abc$ with $M = \{ab\}$, the only free vertex is $c$. The tree from $c$ follows the unmatched edge $ca$, so $a$ is inner and its partner $b$ is outer. The unmatched edge $bc$ joins the outer vertices $b$ and $c$, so the whole triangle is a blossom with base $c$, $k = 1$ and an empty stem. Contracting it leaves one vertex and no edge, where the empty matching is maximum. By the theorem, $M$ is maximum, and $\nu(K_3) = 0 + 1 = 1$.

**Not a blossom.** In a bipartite graph such as the even cycle $C_6$, a tree edge between two outer vertices would close an odd cycle, so it never occurs. An odd cycle in which two matched edges are adjacent cannot occur either, since $M$ is a matching; and an odd cycle of $2k + 1$ edges with fewer than $k$ matched edges has at least three vertices that are not matched along it, so it is not a blossom.

## Where it is used

- [Edmonds' blossom algorithm](/edmonds-blossom/) for [maximum matching](/maximum-matching/) in general graphs: grow alternating trees, contract blossoms, expand them along an augmenting path. The base of a new blossom is a [lowest common ancestor](/lowest-common-ancestor/) in the tree.
- The [Micali-Vazirani algorithm](/micali-vazirani-algorithm/), which handles blossoms implicitly during its search for shortest augmenting paths and reaches $O(m\sqrt n)$ time.
- Weighted algorithms for [maximum weight matching](/maximum-weight-matching/) and [minimum-weight perfect matching](/minimum-weight-perfect-matching/), where blossoms carry dual variables and can be expanded again when their dual reaches zero.
- The proofs of the [Tutte-Berge formula](/tutte-berge-formula/) and of the [Gallai-Edmonds decomposition](/gallai-edmonds-decomposition/), which read off a Tutte set from the final alternating forest and its blossoms.
- The polyhedral description of matchings: the odd sets of [Edmonds' matching polytope theorem](/edmonds-polytope-theorem/) come from the blossoms of the weighted algorithm.

## References
