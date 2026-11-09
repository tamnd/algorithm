---
title: A hash-consed term DAG stores each distinct subterm exactly once
proves: [correctness]
status: full
---

We use the notation of the page. Nodes are numbered $0, 1, 2, \ldots$ in order of creation. Node $i$ has a symbol, a flag that says whether it is a variable, and a tuple of children. Its **key** is $(\mathrm{var}, x)$ for a variable $x$, and $(\mathrm{app}, f, (c_1, \ldots, c_k))$ for a function node. $H$ is the hash table from keys to nodes. The term of a node is defined by $\mathrm{term}(i) = x$ for a variable node with name $x$, and $\mathrm{term}(i) = f(\mathrm{term}(c_1), \ldots, \mathrm{term}(c_k))$ for a function node.

## The invariant

**(H1)** For each node $i$, $H[\mathrm{key}(i)] = i$, and $H$ has no other entries.
**(H2)** Each child of node $i$ is a node $c < i$.

(H1) implies that two different nodes have different keys, since $H$ maps each key to one node.

Both hold for the empty DAG.

**MAKE-NODE keeps the invariant.** Suppose MAKE-NODE$(f, (c_1, \ldots, c_k))$ is called with existing nodes $c_l$, so $c_l < D$, where $D$ is the number of nodes. If the key is in $H$ (L2), nothing changes. Otherwise L3 creates node $D$ with this key, and L4 adds $H[\mathrm{key}] = D$. The key was not in $H$, so (H1) still holds, and the children are smaller than $D$, so (H2) holds. A variable node has no children.

**MAKE-NODE returns the right term.** In both cases the node returned has the given key, so its term is $f(\mathrm{term}(c_1), \ldots, \mathrm{term}(c_k))$, or the variable $x$.

## Maximal sharing

**Theorem.** For nodes $i$ and $j$: $\mathrm{term}(i) = \mathrm{term}(j)$ if and only if $i = j$.

*Proof.* If $i = j$ the terms are equal. For the converse, use induction on $\max(i, j)$. Suppose $\mathrm{term}(i) = \mathrm{term}(j)$.

- If the term is a variable $x$, both nodes are variable nodes with the key $(\mathrm{var}, x)$. By (H1), $i = H[(\mathrm{var}, x)] = j$.
- If the term is $f(t_1, \ldots, t_k)$, both nodes are function nodes with symbol $f$ and $k$ children, and $\mathrm{term}(c_l(i)) = t_l = \mathrm{term}(c_l(j))$ for each $l$. By (H2), $c_l(i) < i$ and $c_l(j) < j$, so the induction hypothesis gives $c_l(i) = c_l(j)$. So $i$ and $j$ have the same key, and by (H1), $i = j$. $\square$

## INTERN is correct

**Claim.** INTERN$(t)$ returns a node $i$ with $\mathrm{term}(i) = t$.

*Proof.* By induction on $t$. For a variable $x$ (L6), MAKE-NODE with the key $(\mathrm{var}, x)$ returns a node whose term is $x$. For $t = f(t_1, \ldots, t_k)$ (L7), the arguments are interned first, which by induction gives nodes $c_l$ with $\mathrm{term}(c_l) = t_l$. MAKE-NODE then returns a node with term $f(t_1, \ldots, t_k)$. The implementation does the same in postorder with an explicit stack. $\square$

**Corollary.** After a set of terms has been interned, the nodes are in one-to-one correspondence with the distinct subterms of these terms. Each node was made for some subterm, by the claim, and two subterms that are equal get the same node, by the theorem. So the number of nodes is the number of distinct subterms, and equality of two interned terms is the equality of their node ids.

## The derived operations

**Tree size.** Let $z(i) = |\mathrm{term}(i)|$. Then $z(i) = 1$ for a variable or constant node, and $z(i) = 1 + \sum_l z(c_l(i))$ otherwise. By (H2), computing $z(0), z(1), \ldots$ in increasing order uses only values already computed, so one pass gives each $z(i)$.

**Unfold.** UNFOLD$(i)$ builds $\mathrm{term}(i)$ from the definition of $\mathrm{term}$, with each node built once and then reused. By (H2), the recursion along children ends. $\blacksquare$
