---
title: The LOUDS formulas find the children and the parent of a node, and the LOUDS trie answers membership correctly
proves: [correctness, complexity]
status: full
---

We use the pseudocode, the notation and the invariant (L1) to (L4) of the page. Let $d_x$ be the number of children of node $x$, and $D_x = d_0 + \cdots + d_{x-1}$.

**Lemma 1 (breadth-first numbering).** The children of node $x$ are the nodes $1 + D_x, \ldots, D_x + d_x$, in order of their labels.

*Proof.* Breadth-first order with a queue visits the nodes in the order they are enqueued, and the children of each node are enqueued, in label order, when the node is visited. The root is node 0, and the nodes enqueued before the children of $x$ are the root and the children of nodes $0, \ldots, x - 1$, which are $1 + D_x$ nodes. $\square$

**Lemma 2 (layout).** $B = 10\, 1^{d_0} 0\, 1^{d_1} 0 \cdots 1^{d_{n-1}} 0$. Before the group of $x$ there are $x + 1$ zeros (the zero of $10$ and the closing zeros of nodes $0, \ldots, x - 1$) and $1 + D_x$ ones.

*Proof.* By construction, the group of $x$ follows the prefix $10$ and the groups of nodes $0, \ldots, x - 1$, each closed by one 0. Counting the bits of these parts gives the claim. $\square$

**CHILDREN.** By Lemma 2 the $(x + 1)$-th 0 is the bit just before the group of $x$, and the $(x + 2)$-th 0 closes it. So $a = select_0(x + 1) + 1$ and $e = select_0(x + 2)$ delimit the group, and $e - a = d_x$. The number of 1s before $a$ is $1 + D_x$, so $first = rank_1(a) = 1 + D_x$ and $last = first + d_x$. By Lemma 1 these are the children of $x$.

**PARENT.** Let $x \ge 1$ be a child of $q$. The 1s of $B$ are, in order, the leading 1 and the groups of nodes $0, 1, \ldots$; by Lemma 1 the $j$-th 1 of the groups, for $j \ge 1$, is node $j$. So the $(x + 1)$-th 1 of $B$ lies in the group of $q$, at position $p = select_1(x + 1)$. By Lemma 2 there are exactly $q + 1$ zeros before any position of the group of $q$, so $rank_0(p) - 1 = q$.

**CHILD and CONTAINS.** By (L3) the labels $L[first \ldots last - 1]$ are distinct and sorted, so the binary search finds the child with label $c$ if it exists, and reports NIL otherwise. CONTAINS starts at the root, whose string is empty, and line L5 keeps the claim that $x$ is the node whose string is the part of $s$ read so far: CHILD returns the child by the next symbol, whose string extends it by that symbol. If some child is missing, no node spells the read part, and since every key is the string of a node (the pointer trie built at line L7 has a node for each prefix of each key), $s$ is not a key. If the walk ends, $x$ spells $s$, and by construction $E[x]$ is set exactly when $s$ is a key.

**Complexity.** CHILDREN and PARENT use two select or rank operations, which take $O(1)$ time with a constant-time index. CHILD adds a binary search over at most $\sigma$ labels, $O(\log \sigma)$. CONTAINS makes $m$ calls of CHILD, $O(m \log \sigma)$. $B$ has $n$ ones and $n + 1$ zeros, so $2n + 1$ bits. $\blacksquare$
