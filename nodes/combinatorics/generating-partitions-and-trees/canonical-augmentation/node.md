---
tag: QTCC4Z
kind: technique
slug: canonical-augmentation
name: Canonical augmentation
aliases:
- McKay canonical augmentation
- Canonical construction path
- Generation by canonical deletion
area: combinatorics/generating-partitions-and-trees
level: research
summary: Generate non-isomorphic objects by adding one element at a time and accepting only canonical extensions.
prereqs: [canonical-labeling, automorphism-orbit, graph-automorphism-group]
see_also: [orderly-generation, graph-generation, nauty, canonical-labeling, automorphism-orbit, graph-isomorphism-problem, symmetry-breaking, generic-backtracking-algorithm]
sources:
  - paper: doi:10.1006/jagm.1997.0898
    title: Brendan D. McKay, Isomorph-free exhaustive generation, Journal of Algorithms 26(2) (1998), 306 to 324
    locator: the whole paper (canonical construction path, the acceptance rule, the proof that each class appears once, and the examples)
  - book: isbn:9783540289906
    title: Petteri Kaski and Patric R. J. Östergård, Classification Algorithms for Codes and Designs, Springer, 2006
    locator: Chapter 4, Isomorph-free exhaustive generation (generation by canonical augmentation)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60 (2014), 94 to 112
    locator: the canonical labeling and the automorphism groups that the acceptance test needs
---

Canonical augmentation, also called the canonical construction path method, lists combinatorial objects up to isomorphism by building each object from a smaller one and accepting it only if the element just added is, up to symmetry, the one that a fixed rule would remove first. The rule, a *canonical deletion*, is defined by a [canonical labeling](/canonical-labeling/), so it does not depend on how the object was built. Together with one augmentation per orbit of the parent's automorphism group, this gives each isomorphism class exactly once, without storing earlier outputs. McKay introduced the method in 1998; his graph generator geng in the [nauty](/nauty/) package uses it.

## In plain words

To list every graph with $n$ dots once, build graphs one dot at a time: take a graph with one dot less, add a new dot, and join it to some of the old dots. The same graph comes out many times, from different smaller graphs and from different choices.

To keep only one copy, ask the new graph which dot it would give up first. A fixed rule names this dot in a way that does not depend on how the dots are numbered. If the dot just added is that dot, or a dot that looks exactly like it, keep the graph; otherwise throw it away, because it will be built from another parent. Also skip choices that look the same in the parent graph.

## When it applies

- **Objects grow by one element.** Every object of size $k + 1$ arises from an object of size $k$ by adding one element: a vertex with its edges, an edge, a block of a design, a row of a matrix. The classes of the smallest objects are known.
- **Isomorphism is a group action.** Two objects are isomorphic when a relabeling maps one to the other, and the automorphism group of an object, the relabelings that fix it, can be computed.
- **A canonical deletion exists.** For each object $Y$ there is a function $m(Y)$ that picks an orbit of $\mathrm{Aut}(Y)$ on the elements that can be removed, and $m$ is invariant: if $\varphi$ is an isomorphism from $Y$ to $Y'$, then $\varphi(m(Y)) = m(Y')$. A canonical labeling gives one: take the removable element with the largest canonical label, perhaps after a cheap invariant such as the degree.
- **No hereditary condition is needed.** Unlike [orderly generation](/orderly-generation/), the parent of an accepted object need not be canonical in any sense, so the method also works when the objects cannot be built by adding elements in a fixed global order.

## The template

```pseudo id=main
SCAN(X)                                       ▷ X represents its class
L1  VISIT(X)
L2  for each orbit of Aut(X) on the augmentations of X do
L3      Y ← X augmented by one member of the orbit, with new element v
L4      if not PRUNE(Y) and v lies in the orbit m(Y) of Aut(Y) then
L5          SCAN(Y)
```

Call SCAN on one representative of each class of the smallest objects. The holes are:

- **AUGMENTATIONS.** The ways to add one element to $X$, and the action of $\mathrm{Aut}(X)$ on them. For graphs by vertices, an augmentation is a subset $S$ of the old vertices, and the new vertex is joined to $S$.
- **m(Y).** The canonical deletion: an orbit of $\mathrm{Aut}(Y)$ on the removable elements, chosen in an invariant way.
- **PRUNE(Y).** An optional test for a property of the objects, such as no triangle or a degree bound. It must be closed under the canonical deletion: if $Y$ has the property, so does $Y$ minus any element of $m(Y)$.

**Why each class appears once.** By induction on the size. *Every class appears.* Let $Y$ be any object, $v \in m(Y)$ and $X = Y - v$. By induction, a representative $X'$ of the class of $X$ is visited, with an isomorphism $\alpha$ from $X$ to $X'$. The augmentation of $X'$ that corresponds to $v$ under $\alpha$ lies in some orbit of $\mathrm{Aut}(X')$, and line L3 takes one member of it; the result $Y'$ is isomorphic to $Y$ by an isomorphism that maps $v$ to the new element $v'$. Since $m$ is invariant, $v' \in m(Y')$, so line L4 accepts $Y'$. *No class appears twice.* Let $Y_1$ and $Y_2$ be accepted and isomorphic, from parents $X_1$ and $X_2$ with new elements $v_1$ and $v_2$. An isomorphism $\varphi$ from $Y_1$ to $Y_2$ maps $m(Y_1)$ to $m(Y_2)$, so $\varphi(v_1)$ and $v_2$ lie in the same orbit, and after composing with an automorphism of $Y_2$ we get $\varphi(v_1) = v_2$. Then $\varphi$ maps $X_1$ onto $X_2$, so they are isomorphic, and by induction they are the same visited object $X$. Now $\varphi$ restricted to $X$ is an automorphism of $X$ that maps the first augmentation to the second, so both lie in one orbit of line L2, and line L3 took only one member of it. So $Y_1$ and $Y_2$ are the same output.

**The cost.** Each visited object costs one automorphism group computation, for line L2, and each tried augmentation costs one canonical labeling, for line L4. In practice the labeling is skipped for most candidates: if a cheap invariant, such as the degree of $v$, already shows that $v$ cannot lie in $m(Y)$, the candidate is rejected at once.

## Classic examples

- **Graphs by vertices.** Add a vertex joined to a subset $S$ of the old vertices, one $S$ per orbit of $\mathrm{Aut}(X)$, and let $m(Y)$ be the orbit of the vertex with the largest canonical label. From the two graphs with $2$ vertices, the empty graph and the edge, the six augmentations give $3K_1$, $K_2 \cup K_1$, $P_3$ from the empty graph and $K_2 \cup K_1$, $P_3$, $K_3$ from the edge. With the largest adjacency code as the canonical form, the last vertex of $K_2 \cup K_1$ is the isolated one and the last vertex of $P_3$ is a leaf, so the copies built from the empty graph are rejected, and the four graphs with $3$ vertices remain. To list all $208$ graphs with $1$ to $6$ vertices, line L4 runs $662$ times. This is the scheme of geng; see [graph generation](/graph-generation/).
- **Restricted graph classes.** Triangle-free graphs, graphs of bounded degree, bipartite graphs and graphs of girth at least $g$ are closed under deleting a vertex, so PRUNE handles them during the search, and geng offers such options.
- **Trees.** Free trees grow by adding a leaf, and a canonical deletion picks a leaf orbit. For trees, the specialized successor of the [Wright-Richmond-Odlyzko-McKay algorithm](/wright-richmond-odlyzko-mckay/) is faster, but the same template gives restricted trees, such as trees with a degree bound, directly.
- **Planar graphs and triangulations.** The plantri program of Brinkmann and McKay builds planar triangulations and related maps by local expansions and accepts them by a canonical construction path; canonical forms of plane graphs are much cheaper to compute than those of general graphs. See [planar graphs](/planar-graph/).
- **Codes and designs.** Kaski and Östergård classify error-correcting codes and combinatorial designs by adding codewords or blocks with canonical augmentation.

## Variations

- **Only siblings are compared.** The proof shows that duplicates can arise only from the same parent. So the orbit computation of line L2 can be replaced by a check among the accepted children of one parent, by comparing their canonical forms. This trades the group computation for a small table per node.
- **Several kinds of augmentation.** The objects can grow by different operations, such as adding a vertex or splitting an edge, as long as every object except the smallest has a canonical deletion of one of the kinds.
- **Weak canonical deletions.** The function $m$ may first compare cheap invariants and call the canonical labeling only to break ties, which keeps the cost per candidate low.
- **Parallel search.** The subtrees of different visited objects are independent, so a split by the parity of a counter, the res/mod option of geng, divides the work without communication.
- **Orderly generation.** With a fixed global order of the elements and the largest code as canonical form, the canonical deletion is "remove the last element", and the method becomes [orderly generation](/orderly-generation/).

## Pitfalls

- **A non-invariant deletion.** If $m(Y)$ depends on the labels of $Y$ as built, rather than on a canonical labeling, the acceptance test is not invariant, and classes are lost or repeated.
- **Testing the element instead of its orbit.** Line L4 must test whether $v$ is in the orbit $m(Y)$, not whether $v$ equals one chosen element; otherwise objects with symmetry are lost.
- **Forgetting the parent's symmetry.** Without the orbit reduction of line L2, or the sibling check that replaces it, symmetric parents give duplicate children.
- **PRUNE and deletion.** A filter that is not preserved by the canonical deletion can remove the canonical parent of a valid object, which then never appears.
- **Smallest objects.** The recursion must start from exactly one representative of each class of the smallest objects.

## Exercises

1. Using the rule of the first example, list the accepted augmentations from the four graphs with $3$ vertices, and check that they give the $11$ graphs with $4$ vertices.
2. Show that if the orbit reduction of line L2 is dropped, $P_3$ is built twice from the edge on the vertices $0, 1$, from $S = \{0\}$ and from $S = \{1\}$, and that both copies pass line L4.

## References
