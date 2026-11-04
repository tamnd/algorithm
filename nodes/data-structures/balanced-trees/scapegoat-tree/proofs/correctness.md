---
title: The scapegoat tree keeps its keys and its depth bound
proves: [correctness]
status: full
---

Fix $\alpha$ with $\frac12 < \alpha < 1$, and write $\log$ for $\log_{1/\alpha}$. The depth of the root is 0, and $\text{size}(x)$ is the number of nodes in the subtree of $x$. The tree keeps two counters, $n$ and $q$. We show that after each operation the following hold.

1. (S1) The tree is a binary search tree whose keys are the keys inserted and not deleted, and $n$ is their number.
2. (S2) $\alpha q \le n \le q$.
3. (S3) Each node has depth at most $\log q$.

All three hold for the empty tree with $n = q = 0$ (there are no nodes, so (S3) holds).

**Rebuilding.** REBUILD$(w)$ lists the nodes of the subtree of $w$ in key order (line L9) and links them again by BUILD (line L10). BUILD puts $a[mid]$ at the root, the nodes left of $mid$ in its left subtree and those right of $mid$ in its right subtree, so by induction on $hi - lo$ the result is a search tree on the same nodes in the same order. Its two subtrees have sizes that differ by at most one, so a tree on $m \ge 1$ nodes has height $\lfloor \lg m \rfloor$, the least possible height of a binary tree on $m$ nodes. Rebuilding does not change the key set or the order, and only the depths of nodes inside the rebuilt subtree change.

**Lemma 1.** Let $u$ be a node of depth $d > \log q$ in a tree with $n \le q$ nodes. Then some proper ancestor $w$ of $u$ has a child $c$ on the path to $u$ with $\text{size}(c) > \alpha \cdot \text{size}(w)$.

*Proof.* Let $x_0 = u, x_1, \ldots, x_d$ be the path from $u$ up to the root. If $\text{size}(x_{j-1}) \le \alpha \cdot \text{size}(x_j)$ for all $j$, then $\text{size}(x_d) \ge (1/\alpha)^d \, \text{size}(x_0) = (1/\alpha)^d > q \ge n$, which is not possible, since the root has $n$ nodes. $\square$

So the loop of line L4 always stops at a node $w$, and $w$ is the first such ancestor met when walking up from $u$.

**Insertion.** If $k$ is present, line L1 returns and nothing changes. Otherwise a leaf $u$ with key $k$ is attached where the search ended, which keeps (S1), and line L2 adds one to $n$ and $q$, which keeps (S1) and (S2), because $\alpha(q + 1) \le n + 1 \le q + 1$ follows from $\alpha q \le n \le q$ and $\alpha < 1$. Let $q$ now denote the new value. The old nodes keep their depths, which are at most the old $\log(q - 1) < \log q$. Let $d$ be the depth of $u$. If $d \le \log q$, (S3) holds and line L3 does nothing.

Otherwise $d > \log q$. The parent of $u$ is an old node, so $d - 1 \le \log q$, and $u$ is the only node of depth more than $\log q$. By Lemma 1, line L4 finds $w$; let $d_w$ be its depth, $i = d - d_w \ge 1$ the depth of $u$ below $w$, $m = \text{size}(w)$, and $c$ the child of $w$ on the path to $u$, with $\text{size}(c) > \alpha m$.

*Claim: $m < 2^i$.* Before $u$ was attached, the subtree of $w$ had $m - 1$ nodes, all at depth at most $d - 1$ in the tree, that is at most $i - 1$ below $w$. A binary tree of height at most $i - 1$ has at most $2^i - 1$ nodes, so $m - 1 \le 2^i - 1$. If $m - 1 = 2^i - 1$, that old subtree was the perfect tree of height $i - 1$, in which both children of $w$ have $2^{i-1} - 1$ nodes. Then after the insertion $\text{size}(c) = 2^{i-1} = m / 2 < \alpha m$, a contradiction. So $m \le 2^i - 1$.

By the claim, the rebuilt subtree has height $\lfloor \lg m \rfloor \le i - 1$. Its nodes, $u$ among them, now have depth at most $d_w + i - 1 = d - 1 \le \log q$. The nodes outside the subtree of $w$ keep their depths, which are at most $\log q$. So (S3) holds, and by the paragraph on rebuilding, (S1) holds.

**Deletion.** If $k$ is absent, line L6 returns and nothing changes. Otherwise line L6 is the deletion of a binary search tree: a node with at most one child is replaced by that child, and a node with two children takes the key of its successor, whose node, which has no left child, is replaced by its right child. This keeps (S1). Each node keeps its depth or moves up one level, so no depth grows, and since $q$ is unchanged, (S3) holds. Line L7 makes $n$ the new count. Now $n \le q$ still holds. If $n \ge \alpha q$, (S2) holds and line L8 does nothing. Otherwise line L8 rebuilds the whole tree and sets $q = n$, so (S2) holds with equality. The new tree has height $\lfloor \lg n \rfloor \le \log n = \log q$, since $1/\alpha < 2$, and so (S3) holds. If $n = 0$, the tree is empty.

**Theorem.** After any sequence of operations from the empty tree, the tree holds exactly the keys inserted and not deleted, CONTAINS answers correctly, and the height is at most $\log_{1/\alpha} q \le \log_{1/\alpha} n + 1$.

*Proof.* The cases above show that (S1) to (S3) hold after each operation. CONTAINS is the search of a binary search tree, which is correct by (S1). By (S2), $q \le n/\alpha$, so $\log q \le \log n + 1$. $\blacksquare$
