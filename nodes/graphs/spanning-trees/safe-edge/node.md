---
tag: 7X7FKS
kind: definition
slug: safe-edge
name: Safe edge
area: graphs/spanning-trees
level: core
summary: Edge that can be added to a subset of some minimum spanning tree while keeping it a subset of some minimum spanning tree.
prereqs: [minimum-spanning-tree, cut]
see_also: [generic-mst-method, cut-property, cycle-property, kruskal, prim, boruvka, mst-optimality-conditions, spanning-forest]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.1, Growing a minimum spanning tree (the definitions of a safe edge, a cut that respects a set, a light edge, Theorem 21.1 and Corollary 21.2)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (Section 7.2, The only minimum spanning tree algorithm, with safe and useless edges)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The minimum spanning tree problem (the cut property, (4.17))
---

A safe edge for a set $A$ of edges, where $A$ is part of some [minimum spanning tree](/minimum-spanning-tree/), is an edge $e \notin A$ such that $A \cup \{e\}$ is still part of some minimum spanning tree. The [generic MST method](/generic-mst-method/) starts with $A = \emptyset$ and adds one safe edge at a time, and Kruskal's, Prim's and Borůvka's algorithms are three ways to find a safe edge fast. The [cut property](/cut-property/) gives the usual test: a lightest edge across a [cut](/cut/) that no edge of $A$ crosses is safe. The converse also holds, so this test finds every safe edge.

## Definition

Let $G = (V, E)$ be a finite, connected, undirected graph with a weight $w(e) \in \mathbb{R}$ on each edge. Weights may tie and may be negative. Let $A \subseteq E$ be a set that is contained in some minimum spanning tree of $G$.

**Safe edge.** An edge $e \in E \setminus A$ is **safe for $A$** if there is a minimum spanning tree $T$ of $G$ with $A \cup \{e\} \subseteq T$.

The notion depends on $A$. An edge can be safe for one set and not for a larger one. For a graph that is not connected, replace "minimum spanning tree" by "minimum spanning forest" everywhere; all statements below stay true with the same proofs.

The test for safety uses three more terms (CLRS, Section 21.1).

- A **cut** is a partition $(S, V \setminus S)$ of $V$ with $\emptyset \ne S \ne V$. An edge **crosses** the cut if it has one end in $S$ and one end in $V \setminus S$.
- A cut **respects** $A$ if no edge of $A$ crosses it.
- An edge is a **light edge** across a cut if it crosses the cut and its weight is the least among all edges that cross the cut. With ties, a cut can have several light edges.

**Characterization.** Let $A$ be contained in some MST and $e = uv \in E \setminus A$. Then $e$ is safe for $A$ if and only if there is a cut that respects $A$ in which $e$ is a light edge.

*Proof, "if".* This is the [cut property](/cut-property/) (CLRS Theorem 21.1). Let $T$ be an MST with $A \subseteq T$, and let $(S, V \setminus S)$ respect $A$, with $e$ light across it. If $e \in T$, we are done. Otherwise, the path from $u$ to $v$ in $T$ goes from one side of the cut to the other, so it has an edge $f$ that crosses the cut. Then $f \notin A$, because the cut respects $A$, and $w(e) \le w(f)$, because $e$ is light. The set $T' = T \setminus \{f\} \cup \{e\}$ is a spanning tree, since $f$ lies on the cycle that $e$ closes in $T$, and $w(T') = w(T) - w(f) + w(e) \le w(T)$. So $T'$ is an MST, and it contains $A \cup \{e\}$.

*Proof, "only if".* Let $T$ be an MST with $A \cup \{e\} \subseteq T$. Removing $e$ from $T$ leaves two trees. Let $S$ be the vertex set of the tree that holds $u$. Then $e$ is the only edge of $T$ that crosses $(S, V \setminus S)$, so no edge of $A \subseteq T \setminus \{e\}$ crosses it, and the cut respects $A$. Suppose that an edge $f$ crosses the cut with $w(f) < w(e)$. Then $T \setminus \{e\} \cup \{f\}$ is a spanning tree, because $f$ joins the two trees, and it is lighter than $T$. This is a contradiction. So $e$ is a light edge across the cut. $\square$

**Component form.** If $A$ is in some MST and $C$ is the vertex set of a tree of the forest $(V, A)$, then a lightest edge with exactly one end in $C$ is safe for $A$ (CLRS Corollary 21.2). The cut $(C, V \setminus C)$ respects $A$, because $C$ is a whole component of $(V, A)$.

## Examples and non-examples

**A graph with a unique MST.** Take the graph on the vertices $a$ to $f$ with the weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. Its only MST is $T = \{bc, bd, ef, ac, ce\}$, of weight 13. For each $A \subseteq T$, the edges safe for $A$ are exactly the edges of $T \setminus A$, because $T$ is the only MST that can hold $A \cup \{e\}$.

- For $A = \{bc\}$, the component of $a$ is $\{a\}$, with edges $ab = 4$ and $ac = 3$. So $ac$ is safe, by the component form.
- For $A = \{bc, bd\}$, the cut $(\{a, b, c, d\}, \{e, f\})$ respects $A$. Its crossing edges are $ce = 5$, $de = 7$ and $df = 6$, so $ce$ is light and safe.
- **Non-example.** The edge $cd$ of weight 4 is not safe for $A = \emptyset$. It is light across no cut: each cut that it crosses is also crossed by $bc$ or $bd$, both lighter. The edge $cd$ is the heaviest edge of the cycle $c, b, d$, and the [cycle property](/cycle-property/) rules it out.

**Ties.** Take the triangle on $x, y, z$ with all three weights equal to 1. Each spanning tree is an MST.

- For $A = \emptyset$, each of the three edges is safe.
- For $A = \{xy\}$, both $yz$ and $xz$ are safe.
- **Non-example.** For $A = \{xy\}$, the edges $yz$ and $xz$ are each safe, but they are not safe together: $\{xy, yz, xz\}$ is a cycle. So the safe edges for a set cannot all be added at once. The generic method adds one, and then tests again for the new set.

**A light edge for a cut that does not respect $A$.** In the triangle with weights $xy = 1$, $yz = 2$, $xz = 3$, let $A = \{xy, yz\}$, the MST. The cut $(\{x\}, \{y, z\})$ has the light edge $xy$, but $xy \in A$. The cut $(\{z\}, \{x, y\})$ has the light edge $yz$, also in $A$. No edge outside $A$ is safe, because $A$ is already a spanning tree. This is why the definition needs the cut to respect $A$: the edge $xz$ is light for no respecting cut, since no cut respects $A$ at all when $A$ is a spanning tree.

## Related definitions

- [Generic MST method](/generic-mst-method/): the loop "while $A$ is not a spanning tree, add a safe edge for $A$". Each step keeps the invariant that $A$ is in some MST.
- [Cut property](/cut-property/): the "if" half of the characterization, the rule used by [Kruskal's](/kruskal/), [Prim's](/prim/) and [Borůvka's](/boruvka/) algorithms.
- [Cycle property](/cycle-property/): the dual rule. An edge that is the strict maximum on some cycle is never safe, for any $A$. Erickson calls an edge outside $A$ whose two ends are already joined by $A$ *useless*: it closes a cycle with $A$, so it can never be added.
- [MST optimality conditions](/mst-optimality-conditions/): a spanning tree is an MST exactly when each of its edges is light across the cut that it defines.
- [Cut](/cut/): the general notion of a cut and of its crossing edges.

## References
