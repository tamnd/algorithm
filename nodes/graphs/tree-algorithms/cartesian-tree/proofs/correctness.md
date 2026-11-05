---
title: The stack build gives the Cartesian tree, and range minima are lowest common ancestors
proves: [correctness, termination]
status: full
---

Let $A[0..n-1]$ be an array over a totally ordered set. Compare positions by the pairs $(A[i], i)$, which are distinct; "the minimum of a range" means the position with the least pair, which is the leftmost minimum of the values. For $0 \le a \le b \le n - 1$ let $C(a, b)$ be the binary tree on the positions $a, \ldots, b$ defined by: the root is the minimum $m$ of $[a, b]$, the left subtree is $C(a, m - 1)$ and the right subtree is $C(m + 1, b)$, where $C(a, a - 1)$ is empty. The Cartesian tree of $A$ is $C(0, n - 1)$.

**Lemma 1 (characterization).** A binary tree on the positions $a, \ldots, b$ is $C(a, b)$ if and only if (1) its inorder is $a, a + 1, \ldots, b$ and (2) every node has a smaller pair than each of its descendants.

*Proof.* $C(a, b)$ has both properties, by induction on $b - a$: the inorder is $In(C(a, m-1)) \cdot (m) \cdot In(C(m+1, b))$, and $m$ has the least pair in $[a, b]$. Conversely, let $T$ have both properties and root $x$. By (2), $x$ has the least pair, so $x = m$. By (1), the left subtree holds exactly the positions before $m$ in inorder, $a, \ldots, m - 1$, and has both properties, so by induction it is $C(a, m - 1)$; the same holds on the right. $\square$

**Lemma 2 (subtrees are ranges).** In $C(0, n-1)$ the subtree of each node $x$ is a range $[lo(x), hi(x)]$ of positions, and $x$ is its minimum.

*Proof.* By the recursive definition, each subtree is some $C(a, b)$, whose node set is $[a, b]$ and whose root is the minimum of $[a, b]$. $\square$

**Lemma 3 (the spine).** In $C(0, i)$ the right spine, the path from the root that always takes the right child, consists of the positions $s$ such that $(A[s], s) < (A[t], t)$ for all $t$ with $s < t \le i$, in increasing order of position and of pair.

*Proof.* The spine of $C(a, b)$ is the root $m$ followed by the spine of $C(m + 1, b)$. By induction on $b - a$, its nodes are $m$ and the positions of $[m + 1, b]$ that beat every later position in $[m+1, b]$. A position $s < m$ is not on the spine and is beaten by $m$, which is later. The position $m$ beats everything after it. A position $s > m$ beats every later position of $[m+1, b]$, which is all of its later positions. So the spine is as stated. $\square$

**Lemma 4 (one round).** Suppose that before round $i$ (lines L3 to L8) the arrays $parent$, $left$, $right$ restricted to the positions $0, \ldots, i - 1$ describe $C(0, i - 1)$, and the stack $S$ holds its right spine with the root at the bottom. Then after the round they describe $C(0, i)$, and $S$ holds its right spine.

*Proof.* Let the spine be $s_1, \ldots, s_k$, bottom to top. By Lemma 3 the pairs increase along it. Line L4 compares $A[s_k] > A[i]$, which, since $s_k < i$, is the same as $(A[s_k], s_k) > (A[i], i)$. The loop pops the spine nodes with a larger pair than $i$; they form a top segment $s_{q+1}, \ldots, s_k$, because the pairs increase. Afterwards $last = s_{q+1}$ (or NIL if nothing was popped), and the top is $s_q$ (or the stack is empty if $q = 0$).

Consider the tree $T$ produced by lines L6 and L7: $i$ becomes the right child of $s_q$, replacing $s_{q+1}$, and $s_{q+1}$ with its whole subtree becomes the left child of $i$; $i$ has no right child. If $q = 0$, $i$ is the root and the whole old tree is its left subtree.

Check property (1) of Lemma 1. The old right subtree of $s_q$ was the range $[s_q + 1, i - 1]$, the end of the inorder. Now the right subtree of $s_q$ is $i$ with that range as its left subtree, so the inorder is the old one followed by $i$. Check property (2). The ancestors of $i$ are $s_1, \ldots, s_q$, all with smaller pairs. The descendants of $i$ are the subtree of $s_{q+1}$, the range $[s_{q+1}, i - 1]$; its minimum is $s_{q+1}$ by Lemma 2, and $s_{q+1}$ has a larger pair than $i$. All other ancestor relations are as before, except that $i$ was inserted between $s_q$ and $s_{q+1}$, and $s_q < i < s_{q+1}$ in pairs. So by Lemma 1, $T = C(0, i)$.

Line L8 pushes $i$, so the stack is $s_1, \ldots, s_q, i$. In $T$ the spine goes from the root along $s_1, \ldots, s_q$, then to the right child $i$ of $s_q$, which has no right child. So the stack holds the spine of $C(0, i)$. $\square$

**Termination and the result.** Before round 0 the tree and the stack are empty, which describes $C(0, -1)$. By Lemma 4 and induction on $i$, after round $n - 1$ the arrays describe $C(0, n - 1)$, and the bottom of the stack is its root, which line L9 returns. Every round ends, because the loop of line L4 pops a node each time and the stack is finite; each position is pushed exactly once, so there are at most $n$ pops in all.

**Lemma 5 (range minimum).** For $0 \le i \le j \le n - 1$, the minimum of $[i, j]$ is $\mathrm{lca}(i, j)$ in $C(0, n - 1)$.

*Proof.* Let $x = \mathrm{lca}(i, j)$. By Lemma 2 the subtree of $x$ is a range that contains $i$ and $j$, so it contains $[i, j]$, and $x$ is the minimum of that range. If $x$ were outside $[i, j]$, say $x < i$, then $i$ and $j$ would both be in the right subtree of $x$ by property (1), and the right child of $x$ would be a deeper common ancestor. The case $x > j$ is the same with the left subtree. So $x \in [i, j]$, and as the minimum of a range that contains $[i, j]$, it is the minimum of $[i, j]$. $\blacksquare$
