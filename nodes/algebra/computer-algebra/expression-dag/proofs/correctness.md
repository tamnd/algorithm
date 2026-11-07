---
title: Hash consing keeps the DAG invariant, identifiers decide equality, and the walks are correct
proves: [correctness, termination]
status: full
---

For a node $i$ of a store $D$, write $T(i)$ for its unfolded tree: $T(i)$ is the leaf $\text{val}[i]$ if $i$ is a leaf, and the tree with root $\text{op}[i]$ and subtrees $T(c_1), T(c_2)$ if $\text{kids}[i] = (c_1, c_2)$. This is well defined by induction on $i$ once every child identifier is less than its parent, the second clause of (H).

**Lemma 1 (MAKE keeps the invariant).** If (H) holds and every identifier in kids is a node of $D$, then after MAKE$(D, \text{op}, \text{val}, \text{kids})$ (H) holds, and the returned node $i$ has key $(\text{op}, \text{val}, \text{kids})$.

*Proof.* If the key is in the table (line L2), nothing changes, and the table maps the key to a node whose key it is, by (H). Otherwise line L3 appends node $i = N$, where $N$ was the number of nodes, with that key, and line L4 adds the single entry from the key to $i$. The key was not in the table, and by (H) the table contained exactly the keys of nodes $0, \ldots, N - 1$, so no earlier node has this key; the table now contains exactly the keys of nodes $0, \ldots, N$, each mapped to its node. Every child identifier is an existing node, so it is less than $N = i$. The arity conditions are those of the constructors that call MAKE. $\square$

**Theorem 1 (identifiers decide tree equality).** If (H) holds, then for nodes $i$ and $j$, $T(i) = T(j)$ if and only if $i = j$.

*Proof.* If $i = j$ the trees are equal. For the converse we use induction on $\max(i, j)$. Suppose $T(i) = T(j)$. Then the roots agree, so $\text{op}[i] = \text{op}[j]$, and for leaves $\text{val}[i] = \text{val}[j]$. If they are leaves, their keys are equal. If they are operator nodes with children $(a_1, a_2)$ and $(b_1, b_2)$, then $T(a_k) = T(b_k)$ for $k = 1, 2$, and $\max(a_k, b_k) < \max(i, j)$ by (H), so by induction $a_k = b_k$, and again the keys of $i$ and $j$ are equal. By (H) the table maps that key to $i$ and also to $j$, so $i = j$. $\square$

So `equal`, which compares identifiers, decides syntactic identity of the unfolded trees. Since constants are stored as reduced fractions, equal constants have equal keys.

**Lemma 2 (order).** The list of nodes reachable from $e$, sorted by identifier, lists each such node once and each node after all of its children.

*Proof.* The search adds a node to the set when it first meets it, and pushes it once, so each reachable node is found and listed once. A child of a reachable node is reachable, and its identifier is smaller, so it comes earlier in the sorted list. $\square$

**Theorem 2 (EVAL).** EVAL$(D, e, \rho)$ returns $[\![T(e)]\!]_\rho$, the value of the unfolded tree, if $\rho$ defines every symbol of $T(e)$.

*Proof.* We show $v[u] = [\![T(u)]\!]_\rho$ for each reachable $u$, by induction along the order of Lemma 2. Lines E2 and E3 are the values of the leaves. At line E4 both children were handled earlier, so $v[u.left]$ and $v[u.right]$ are the values of the subtrees, and the operator combines them as in the definition of $[\![\cdot]\!]_\rho$. Line E5 returns $v[e]$. $\square$

**Theorem 3 (SUBS and DIFF).** $T(\text{SUBS}(e, x, r)) = T(e)[x := T(r)]$, and $[\![T(\text{DIFF}(e, x))]\!]_\rho$ is the partial derivative of $[\![T(e)]\!]$ with respect to $x$ at $\rho$.

*Proof.* Both walks go along the order of Lemma 2 and build results with MAKE, which by Lemma 1 keeps (H) and returns a node with the requested key, so the tree of the result is the tree with the requested root and subtrees. For SUBS, induction along the order shows $T(R[u]) = T(u)[x := T(r)]$: the symbol $x$ becomes $r$, other leaves stay, and an operator node is rebuilt from the results of its children. For DIFF, the same induction with the sum, product and power rules shows that $T(D[u])$ has the value of the derivative of $T(u)$; the smart constructors only fold constants and apply $0 + w = w$, $w - 0 = w$, $0 \cdot w = 0$ and $1 \cdot w = w$, which keep the value. For powers, $k a^{k-1} \partial a$ is written with $a^{k-1}$ replaced by $1$ when $k = 1$ and by $a$ when $k = 2$, and the derivative is 0 when $k = 0$. Nodes that MAKE creates during the walk are not in the list of Lemma 2, which was computed first, so the walk does not visit them. $\square$

**Termination and cost.** The search and each walk touch each of the $m$ reachable nodes once and do $O(1)$ work per node, apart from MAKE calls, of which there are $O(1)$ per node, and the sort, which takes $O(m \log m)$. Each MAKE does one table lookup and at most one insertion. So every operation terminates, and SUBS and DIFF add $O(m)$ nodes. $\blacksquare$
