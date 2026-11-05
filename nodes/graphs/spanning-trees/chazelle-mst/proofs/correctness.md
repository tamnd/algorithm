---
title: The soft-heap filter returns the minimum spanning forest
proves: [correctness, termination]
status: full
---

This proof is for the simplified algorithm SOFT-HEAP-MSF on the page. Chazelle's full algorithm rests on the same two lemmas, the contractibility of the pieces (Lemma 2) and the filter (Lemma 3), and its time analysis is in the paper.

Let $G = (V, E)$ be a finite undirected graph without self-loops (they are dropped at the start), with parallel edges allowed. Each edge $e$ has the key $\mathrm{key}(e) = (w(e), i)$, where $i$ is its index. Keys are compared lexicographically, so distinct edges have distinct keys. All current keys of the soft heaps are keys of edges, so they live in the same totally ordered set. For a set of edges $X$, $\mathrm{MSF}(X)$ is the unique minimum spanning forest of the graph $(V, X)$ under the key order. "Minimum" means least in the order on the sorted list of keys, which for distinct keys is the same as least total key.

## Facts

**Fact 1 (cut property).** Let $A$ be a set of edges contained in some minimum spanning forest for a weight function $c$ (ties allowed). Let $S \subseteq V$ be a set such that no edge of $A$ has exactly one end in $S$, and let $e$ be an edge with exactly one end in $S$ such that $c(e) \le c(f)$ for each such edge $f$. Then $A \cup \{e\}$ is contained in some minimum spanning forest for $c$. This is the [cut property](/cut-property/) in its form with ties.

**Fact 2 (cycle property, distinct keys).** An edge $e$ is not in $\mathrm{MSF}(X)$ if and only if $X$ has a cycle through $e$ on which $e$ has the largest key. See the [cycle property](/cycle-property/).

**Fact 3 (exchange).** Let $T'$ be a minimum spanning forest for $c$, let $g \in T'$, and let $S$ be the vertex set of one of the two trees of $T' - g$ inside the component of $g$. If an edge $h$ has exactly one end in $S$, then $c(g) \le c(h)$.

*Proof.* The ends of $h$ lie in one component of $G$, because $h$ is an edge. That component is the component of $g$, since one end of $h$ is in $S$. So $T' - g + h$ is a spanning forest with the same components. If $c(h) < c(g)$, its weight is smaller, a contradiction. $\square$

**Fact 4.** If $\mathrm{MSF}(E) \subseteq K \subseteq E$, then $\mathrm{MSF}(K) = \mathrm{MSF}(E)$.

*Proof.* Every edge $e \in K \setminus \mathrm{MSF}(E)$ has, by Fact 2, a cycle in $E$ on which it is the heaviest edge. Its fundamental cycle with respect to $\mathrm{MSF}(E)$ is such a cycle, and it lies in $K$. So $e \notin \mathrm{MSF}(K)$, and $\mathrm{MSF}(K) \subseteq \mathrm{MSF}(E)$. Since $\mathrm{MSF}(E) \subseteq K \subseteq E$, both graphs have the same components, so the two forests have the same number of edges and are equal. $\square$

## Lemma 1: the soft heap

**Lemma 1.** In the soft heap of the implementation, every item has a current key at least its own key, the current key of an item never decreases, and DELETE-MIN returns an item whose current key is the smallest current key among all items in the heap.

*Proof.* The current key of an item is the ckey of the node whose list holds it. We show three invariants: (i) every item's key is at most the ckey of its node; (ii) the ckey of a child is at least the ckey of its parent; (iii) a node with an empty list is a leaf, except during a sift.

All three hold for a new node of rank 0. In SIFT$(x)$, the child $c$ with the smaller ckey is chosen. Its list moves to $x$, and $x.\mathrm{ckey}$ becomes $c.\mathrm{ckey}$. By (ii), this is at least the old ckey of $x$, so the current keys of the items already in $x$ do not decrease. The moved items keep their current key. (i) holds for all of them. The new ckey of $x$ is at most the ckey of the other child, by the choice of $c$, and at most the ckeys of the children of $c$, by (ii). Then $c$ is sifted recursively, which only raises its ckey, so (ii) is kept. If $c$ ends with an empty list, the loop in SIFT$(c)$ has stopped, so $c$ is a leaf, and it is removed. This keeps (iii).

A new node of a link is sifted at once, and its ckey becomes the ckey of a child. In DELETE-MIN, a root with an empty list is either sifted or, if it is a leaf, removed.

Items move only up the tree, and only by SIFT. So, by the argument above, current keys never decrease. DELETE-MIN takes an item from a root of smallest ckey. By (ii), every node has a ckey at least that of its root, so every item in the heap has a current key at least the returned one. $\square$

## Lemma 2: the pieces are contractible for the corrupted keys

Number the soft heaps $H_1, H_2, \dots$ in the order in which they are made at line L3. Each edge enters a given heap at most once. The root inserts each of its edges once, and line L7 skips edges whose other end is already in the piece. For an edge $e$ and a heap $H$ that held it, let $c_H(e)$ be the current key of $e$ when it was deleted from $H$ (line L5), or when $H$ was discarded (line L8). Define

$$w'(e) = \max_H c_H(e), \quad \text{and } w'(e) = \mathrm{key}(e) \text{ if } e \text{ was in no heap.}$$

By Lemma 1, $w'(e) \ge \mathrm{key}(e)$. Lines L5 and L8 put $e$ into $B$ whenever some $c_H(e) > \mathrm{key}(e)$. So

$$\{e : w'(e) \ne \mathrm{key}(e)\} \subseteq B, \qquad \text{that is, } w'(e) = \mathrm{key}(e) \text{ for } e \notin B. \tag{1}$$

Call an edge a *tree edge* if it is added at line L7 (the edge that brings $y$ into $C$) or used to join two pieces at line L6. Let $A$ be the set of tree edges.

**Lemma 2.** Some minimum spanning forest $T'$ for $w'$ (ties allowed) contains $A$. Every final piece, after all joins, is spanned by the tree edges inside it.

*Proof.* We add the tree edges to $A$ in the order of the run and apply Fact 1 with $c = w'$ at each step. Note that $w'$ is fixed by the whole run, so the comparisons below are between final values.

Consider the moment when a tree edge $e$ is found by DELETE-MIN from the heap $H$ of the piece $C$ being grown. Here $C$ is its vertex set at that moment, and $S = C$.

- *The cut respects $A$.* The tree edges added so far lie inside $C$ or inside earlier pieces, and earlier pieces are disjoint from $C$. A join only happens at the end of the growth of a piece.
- *Every edge $f$ with exactly one end in $C$ is in $H$ at this moment.* Let $f = (p, q)$ with $p \in C$ and $q \notin C$. When $p$ entered $C$ (or when $p = r$), $q$ was not in $C$, so $f$ was inserted into $H$. If $f$ had been deleted from $H$ before, then at that time its far end was in $C$ (it was skipped), or it brought its far end into $C$, or it ended the growth of $C$. The first two cases contradict $q \notin C$, and the third contradicts the fact that $C$ is still growing.
- *So $e$ is light for $w'$.* For each such $f$, Lemma 1 gives $w'(f) \ge c_H(f) \ge$ the current key of $f$ now $\ge$ the current key of $e$ now $= c_H(e)$. It remains to show $w'(e) = c_H(e)$.
  - If $e$ is added at line L7, both of its ends are now in $C$. An earlier heap holds an edge only if one of its ends is in an earlier piece, and a later heap only if one of its ends is free when it is inserted. So $H$ is the only heap that holds $e$, and $w'(e) = c_H(e)$.
  - If $e$ joins $C$ to an earlier piece at line L6, then $e \notin B$, so by (1) and Lemma 1, $w'(e) = \mathrm{key}(e) \le c_H(e) \le w'(e)$.

By Fact 1, $A$ stays inside a minimum spanning forest for $w'$ after each addition. Since $G$ is finite, the final $A$ is contained in one such forest $T'$.

A grown piece is spanned by its line-L7 edges, because each one brings a new vertex in and attaches it to the piece. A join adds an edge between two spanned pieces. So every final piece is spanned by the tree edges inside it. $\square$

## Lemma 3: the filter

Let $P_1, \dots, P_k$ be the final pieces. Let $H$ be the multigraph whose vertices are the pieces. For each edge $e \notin B$ whose ends lie in different pieces, $H$ has an edge between those pieces, with the same key. This is the graph of line L10.

**Lemma 3.** $\mathrm{MSF}(E) \subseteq \bigcup_i \mathrm{MSF}(G[P_i]) \cup \mathrm{MSF}(H) \cup B$, where the edges of $\mathrm{MSF}(H)$ are identified with the edges of $G$ they come from.

*Proof.* Let $e \in \mathrm{MSF}(E)$ with $e \notin B$.

*Case 1: both ends of $e$ are in one piece $P_i$.* If $e \notin \mathrm{MSF}(G[P_i])$, then by Fact 2 some cycle of $G[P_i]$ has $e$ as its heaviest edge. That is also a cycle of $G$, so $e \notin \mathrm{MSF}(E)$ by Fact 2, a contradiction.

*Case 2: the ends of $e$ are in different pieces.* Then $e$ is an edge of $H$. Suppose $e \notin \mathrm{MSF}(H)$. By Fact 2, $H$ has a cycle $Q$ through $e$ on which $e$ is the heaviest edge. As a cycle, $Q$ visits each piece at most once. At a piece $P_i$ that it visits, it arrives at a vertex $x_i \in P_i$ and leaves from a vertex $y_i \in P_i$, along two edges of $Q$. By Lemma 2, $T' \cap E(P_i)$ contains a spanning tree of $P_i$. Let $R_i$ be the path from $x_i$ to $y_i$ in that tree, which is empty if $x_i = y_i$. Then $R_i \subseteq T'$.

Let $W$ be the closed walk in $G$ that follows the edges of $Q$ and crosses each visited piece $P_i$ along $R_i$.

*Claim.* Every edge $g$ on a path $R_i$ has $\mathrm{key}(g) < \mathrm{key}(e)$.

Remove $g$ from $T'$, and let $S$ be the side that contains $x_i$. Since $g$ lies on the path $R_i$ in $T'$, $y_i \notin S$. A closed walk crosses the cut $(S, V \setminus S)$ an even number of times, counted with multiplicity. Consider the edges of $W$:

- $g$ itself is used once, since the paths $R_j$ lie in different pieces and a path uses each edge once;
- no other edge of $T'$ crosses the cut, because $S$ is a side of $T' - g$;
- the edges of $Q$ are the only other edges of $W$.

So some edge $h$ of $Q$ crosses the cut. Since $h \in Q$, it is an edge of $H$, so $h \notin B$, and $w'(h) = \mathrm{key}(h)$ by (1). By Fact 3, applied to $T'$ and $c = w'$, $w'(g) \le w'(h)$. Since $e$ is the heaviest edge of $Q$, $\mathrm{key}(h) \le \mathrm{key}(e)$. Together:

$$\mathrm{key}(g) \le w'(g) \le w'(h) = \mathrm{key}(h) \le \mathrm{key}(e).$$

Moreover $g \ne e$, since $g$ has both ends in $P_i$ and $e$ does not. Distinct edges have distinct keys, so $\mathrm{key}(g) < \mathrm{key}(e)$. This proves the claim.

Every edge of $W$ other than $e$ is lighter than $e$: the edges of $Q$ by the choice of $Q$, and the edges of the paths $R_i$ by the claim. The edge $e$ occurs exactly once in $W$, because it is not inside a piece. Removing it from $W$ leaves a walk between the two ends of $e$ that does not use $e$, and that walk contains a path. With $e$, the path forms a cycle of $G$ on which $e$ is the heaviest edge. By Fact 2, $e \notin \mathrm{MSF}(E)$, a contradiction. $\square$

## The theorem

**Theorem.** SOFT-HEAP-MSF$(G)$ terminates and returns $\mathrm{MSF}(E)$.

*Proof.* By induction on $m = |E|$.

*Base.* If $m \le$ base, line L1 returns Kruskal's result, which is $\mathrm{MSF}(E)$.

*Step.* Assume $m >$ base and $m \ge 1$. Lines L2 to L8 terminate, because each iteration deletes an item from a finite heap. Let $r$ be the first vertex, in the order of line L3, that has an edge. When $r$ is reached, it is still free, because a piece made earlier was grown from a vertex without edges and so stayed alone. So $r$ starts a piece, and its heap is not empty. Since $s \ge 2$, line L5 deletes some edge $e = (r, y)$ with $y \ne r$. Then one of three things happens:

- $e \in B$;
- $y$ joins the piece at line L7, so $e$ is inside a final piece;
- $y$ is in an earlier piece and the pieces are joined, so $e$ is again inside a final piece.

In each case $e$ is not an edge of $H$. So $H$ has at most $m - 1$ edges, and by the induction hypothesis, line L10 terminates and returns $\mathrm{MSF}(H)$.

Lines L9 and L12 are Kruskal's algorithm, which returns $\mathrm{MSF}$ of its input under the key order. By Lemma 3, $K = F \cup F' \cup B \supseteq \mathrm{MSF}(E)$, and $K \subseteq E$. By Fact 4, line L12 returns $\mathrm{MSF}(K) = \mathrm{MSF}(E)$. $\blacksquare$

The keys $(w, i)$ order the edges first by weight. So $\mathrm{MSF}(E)$ is a minimum spanning forest for the weights $w$, and when weights tie it is the one that Kruskal's algorithm picks with ties broken by index. If $G$ is disconnected, it is a minimum spanning forest, one tree per component.
