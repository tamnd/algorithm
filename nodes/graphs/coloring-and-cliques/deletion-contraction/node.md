---
tag: KJ3788
kind: technique
slug: deletion-contraction
name: Deletion-contraction
aliases:
- deletion-contraction recurrence
area: graphs/coloring-and-cliques
level: advanced
summary: Recurrence relating a graph to its edge-deleted and edge-contracted minors; used for chromatic and Tutte polynomials.
prereqs: [chromatic-polynomial, graph-coloring]
see_also: [chromatic-polynomial, counting-graph-colorings, graph-coloring, line-graph, kempe-chain, bjorklund-chromatic-number, inclusion-exclusion-principle, hadwiger-conjecture]
sources:
  - paper: doi:10.4153/CJM-1954-010-9
    title: W. T. Tutte, A contribution to the theory of chromatic polynomials, Canadian Journal of Mathematics 6, 80 to 91 (1954)
    locator: the whole paper (the two-variable polynomial defined by deletion and contraction)
  - paper: doi:10.1016/S0021-9800(68)80087-0
    title: Ronald C. Read, An introduction to chromatic polynomials, Journal of Combinatorial Theory 4(1), 52 to 71 (1968)
    locator: the reduction theorem P(G) = P(G - e) - P(G / e) and its use for computation
  - paper: doi:10.1016/0012-365X(73)90108-8
    title: Richard P. Stanley, Acyclic orientations of graphs, Discrete Mathematics 5(2), 171 to 178 (1973)
    locator: the recurrence for acyclic orientations and Corollary 1.3
  - paper: doi:10.1017/S0305004100068936
    title: F. Jaeger, D. L. Vertigan and D. J. A. Welsh, On the computational complexity of the Jones and Tutte polynomials, Mathematical Proceedings of the Cambridge Philosophical Society 108(1), 35 to 53 (1990)
    locator: "the main theorem (evaluating the Tutte polynomial is #P-hard at all but a few points of the plane)"
  - book: isbn:9780387984889
    title: Béla Bollobás, Modern Graph Theory, Springer, 1998
    locator: Chapter X, The Tutte polynomial (the deletion-contraction recurrence and the universality of the Tutte polynomial)
---

Deletion-contraction computes a graph invariant by picking an edge $e$ and expressing the value on $G$ through the values on $G - e$, the graph with $e$ deleted, and on $G / e$, the graph with $e$ contracted. Both are smaller, so the recurrence ends at graphs with no edges. The chromatic polynomial satisfies $P(G) = P(G - e) - P(G / e)$, the number of spanning trees satisfies $\tau(G) = \tau(G - e) + \tau(G / e)$, and the Tutte polynomial is the most general invariant with such a rule. The plain recursion takes time exponential in $n + m$, which is expected, since most of these invariants are #P-hard.

## In plain words

Take one line of the network. Ask a question about it that has two answers, and split the count into two cases.

For colorings, the question is whether the two ends of the line have the same color. If you erase the line, you count both cases. If you glue the two ends into one point, you count only the case where they have the same color. So the colorings you want are those of the erased network minus those of the glued network.

Both new networks have one line fewer. Do it again and again, until no lines are left, where the count is easy.

## When it applies

The technique applies to an invariant $f$ of graphs, usually multigraphs with loops allowed, when:

1. **The two cases split cleanly.** For a fixed edge $e = uv$, the objects counted on $G - e$ split into those where $e$ "matters" and those where it does not, and one class is in bijection with the objects counted on $G / e$.
2. **The base case is easy.** Graphs without edges, or with only loops and bridges, have a closed form.
3. **Isomorphic graphs give equal values,** so the recursion can be cut by recognizing small graphs such as trees, cycles and complete graphs.

Here $G - e$ removes $e$ and keeps all vertices. $G / e$ removes $e$ and merges $u$ and $v$ into one vertex; edges parallel to $e$ become loops, and edges from $u$ and $v$ to a common neighbor become parallel edges. For a loop, contraction is the same as deletion.

## The template

Let $f$ satisfy, for each edge $e$ that is not a loop,

$$f(G) = \alpha\, f(G - e) + \beta\, f(G / e),$$

with a base value $f(\overline{K_r})$ for each edgeless graph on $r$ vertices.

```
DC(G)
  if G has no edges then return base(|V(G)|)
  if G is in the table of known values then return the table entry
  e ← an edge of G that is not a loop (handle loops by the rule for loops)
  return α · DC(G - e) + β · DC(G / e)
```

**Running time.** Let $L(n, m)$ be the number of leaves of the recursion tree for a graph with $n$ vertices and $m$ edges. The two children have $(n, m - 1)$ and $(n - 1, m - 1)$, so $L(n, m) \le L(n, m - 1) + L(n - 1, m - 1)$ with $L(n, 0) = 1$. By induction, $L(n, m) \le \varphi^{n + m}$, where $\varphi = (1 + \sqrt 5)/2 \approx 1.618$, because $\varphi^{a - 1} + \varphi^{a - 2} = \varphi^a$. Each node does polynomial work, so the time is $O^*(\varphi^{n + m})$. Tables of small graphs, isomorphism caching and good edge choices cut this down a lot in practice, but not below exponential in the worst case.

**Correctness.** The value is right by induction on the number of edges, given the identity for each edge and the base case. The identity is proved once for the invariant, usually by the bijection of condition 1.

## Classic examples

**Chromatic polynomial.** For a non-loop edge $e = uv$, the proper $k$-colorings of $G - e$ with $c(u) \ne c(v)$ are the proper colorings of $G$, and those with $c(u) = c(v)$ are in bijection with the proper colorings of $G / e$. So

$$P(G, k) = P(G - e, k) - P(G / e, k), \qquad P(\overline{K_r}, k) = k^r,$$

and $P(G, k) = 0$ if $G$ has a loop. For the 4-cycle, deleting one edge gives the path $P_4$ and contracting it gives the triangle:

$$P(C_4, k) = k(k-1)^3 - k(k-1)(k-2) = k^4 - 4k^3 + 6k^2 - 3k.$$

At $k = 3$ this is $24 - 6 = 18$, the number of proper 3-colorings of $C_4$. See the [chromatic polynomial](/chromatic-polynomial/).

**Spanning trees.** A spanning tree of $G$ either avoids $e$, and is a spanning tree of $G - e$, or contains $e$, and then contracting $e$ gives a spanning tree of $G / e$, bijectively. So $\tau(G) = \tau(G - e) + \tau(G / e)$, with loops deleted first. For $K_4$, $\tau(K_4 - e) = 8$, and $K_4 / e$ is a triangle with two of its edges doubled, which has $2 \cdot 2 + 2 \cdot 1 + 2 \cdot 1 = 8$ spanning trees. So $\tau(K_4) = 16$, which agrees with Cayley's formula $4^{4-2}$.

**Acyclic orientations.** The number $a(G)$ of acyclic orientations satisfies $a(G) = a(G - e) + a(G / e)$ for a non-loop edge $e$, with $a(\overline{K_r}) = 1$ and $a(G) = 0$ if $G$ has a loop. So $a(C_4) = a(P_4) + a(C_3) = 8 + 6 = 14$. Comparing with the chromatic recurrence shows $a(G) = (-1)^n P(G, -1)$ (Stanley 1973).

**Tutte polynomial.** Tutte (1954) defined $T(G; x, y)$ by $T(G) = T(G - e) + T(G / e)$ for an edge $e$ that is neither a loop nor a bridge, $T(G) = x\, T(G / e)$ for a bridge, $T(G) = y\, T(G - e)$ for a loop, and $T = 1$ for a graph without edges. Every invariant that satisfies a deletion-contraction rule of this kind and is multiplicative on disjoint unions is an evaluation of $T$, up to simple factors. For example,

- $\tau(G) = T(G; 1, 1)$ for connected $G$;
- $P(G, k) = (-1)^{n - c} k^c\, T(G; 1 - k, 0)$, where $c$ is the number of components;
- $a(G) = T(G; 2, 0)$.

## Variations

- **Deletion-contraction on vertices.** Recurrences on a vertex $v$, such as the independent set polynomial $I(G) = I(G - v) + x\, I(G - N[v])$, follow the same pattern with a different pair of minors.
- **Addition-identification.** The chromatic rule can be read backwards: for a non-edge $uv$, $P(G) = P(G + uv) + P(G / \{u, v\})$. Repeating it until the graph is complete writes $P(G)$ as a sum of falling factorials $k(k-1)\cdots(k-r+1)$. This is the better direction for dense graphs.
- **Splitting off blocks.** If $G$ is a union of $G_1$ and $G_2$ that meet in one vertex, then $P(G) = P(G_1) P(G_2) / k$. Applying such product rules before recursing shrinks the tree.
- **Induction over minors.** The graphs reached by deletions and contractions are the minors of $G$. Proofs about colorings and minors, such as the known cases of [Hadwiger's conjecture](/hadwiger-conjecture/), take a minimal counterexample and use that deleting or contracting any edge gives a smaller graph for which the claim holds.

## Pitfalls

- **Simplifying too early.** Contraction can create parallel edges and loops. For the chromatic polynomial, parallel edges can be merged and a loop gives 0. For the Tutte polynomial and for spanning trees, parallel edges must be kept, since they change the value.
- **Wrong sign.** The chromatic rule has a minus sign, the spanning tree and Tutte rules a plus sign. Mixing them gives wrong coefficients.
- **Bridges in the Tutte rule.** The rule $T(G) = T(G - e) + T(G / e)$ holds only when $e$ is neither a loop nor a bridge. For a bridge, $G - e$ has one more component, and the rule is $T(G) = x\, T(G / e)$.
- **Expecting polynomial time.** The recursion tree can have about $\varphi^{n + m}$ leaves. Evaluating the Tutte polynomial is #P-hard at all but a few points (Jaeger, Vertigan and Welsh 1990), so no speed-up of the recursion makes it polynomial in general. For the chromatic polynomial at one value of $k$, inclusion-exclusion over independent sets runs in $O^*(2^n)$ time, which beats $\varphi^{n + m}$ on dense graphs.

## Exercises

1. Use deletion-contraction to show that $P(T, k) = k(k-1)^{n-1}$ for every tree $T$ on $n$ vertices. Hint: contract a leaf edge and delete it.
2. Prove $P(C_n, k) = (k-1)^n + (-1)^n (k - 1)$ by induction on $n$, deleting one edge of $C_n$.
3. Show that the coefficient of $k^{n-1}$ in $P(G, k)$ is $-m$ for a simple graph, using the recurrence and induction on $m$.
4. Show that $\tau(G) \le \varphi^{n + m}$ follows from the recursion tree bound, and find a family of graphs where $\tau(G)$ itself grows exponentially in $n$.
5. Compute $T(C_3; x, y)$ and check that $T(C_3; 1, 1) = 3$ and $T(C_3; 2, 0) = 6$.

## References
