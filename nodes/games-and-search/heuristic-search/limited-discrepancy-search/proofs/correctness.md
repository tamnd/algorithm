---
title: Iteration k of LDS visits each node with at most k discrepancies once, ILDS visits each leaf once in all, and LDS returns a goal with the fewest discrepancies
proves: [correctness]
status: full
---

We use the pseudocode of the page and the ILDS procedure of the implementation. The tree is finite. For a node $u$ below a node $n$, the *discrepancies of $u$ from $n$*, written $\delta_n(u)$, are the number of steps on the path from $n$ to $u$ that go to a child other than the first. We write $\delta(u) = \delta_{\mathrm{root}}(u)$.

**Lemma 1 (one probe).** Suppose that no node below $n$, $n$ included, is a goal. Then PROBE$(n, k)$ visits exactly the nodes $u$ below $n$ with $\delta_n(u) \le k$, each once, and returns failure.

*Proof.* By induction on the height of $n$. If $n$ is a leaf, PROBE visits $n$ only, and $\delta_n(n) = 0 \le k$. Otherwise PROBE visits $n$ and then makes calls on the children. A node $u$ strictly below $n$ lies below exactly one child $c$, and $\delta_n(u) = \delta_c(u)$ if $c$ is the first child and $\delta_n(u) = 1 + \delta_c(u)$ otherwise.

If $k = 0$, line L7 calls PROBE$(c_1, 0)$ on the first child only. By induction it visits the nodes $u$ below $c_1$ with $\delta_{c_1}(u) = 0$, which are the nodes below $n$ other than $n$ with $\delta_n(u) = 0$. Nodes below other children have $\delta_n \ge 1$.

If $k > 0$, line L8 calls PROBE$(c, k - 1)$ once for each other child $c$, which by induction visits the nodes below $c$ with $\delta_c(u) \le k - 1$, that is, $\delta_n(u) \le k$. Line L9 calls PROBE$(c_1, k)$, which visits the nodes below $c_1$ with $\delta_n(u) = \delta_{c_1}(u) \le k$. The subtrees of the children are disjoint and each child gets one call, so each node is visited once. $\square$

**Theorem 2 (the answer of LDS).** Let $k^* = \min \delta(t)$ over the goal nodes $t$, or $\infty$ if there is none. If $k^* \le k_{\max}$, LDS returns in iteration $k^*$ a path from the root to a goal $t$ with $\delta(t) \le k^*$, so $\delta(t) = k^*$. If $k^* > k_{\max}$, it returns failure.

*Proof.* A returned path is built at line L5 by a call on a goal, and the calls form the path from the root, so it is a path from the root to a goal. In iteration $k < k^*$, every node with $\delta \le k$ is not a goal, and PROBE visits only nodes with $\delta \le k$: this is Lemma 1 when no goal lies in the part that the probe can reach, and the same induction shows that a probe that returns early visits a subset of those nodes. So iteration $k$ returns failure. In iteration $k^*$, PROBE visits nodes with $\delta \le k^*$ in the order of Lemma 1 until it meets a goal, and it meets one, since the goal $t$ with $\delta(t) = k^*$ would be visited otherwise. The goal it meets has $\delta \le k^*$, so its $\delta$ is $k^*$. If $k^* > k_{\max}$, each iteration up to $k_{\max}$ returns failure, and so does LDS. $\square$

Every node has $\delta$ at most the depth of the tree, so with $k_{\max}$ at least the depth, LDS finds a goal whenever one exists. Each probe ends on a finite tree by Lemma 1, so LDS ends.

**Corollary 3 (the leaves).** If no goal exists, iteration $k$ of LDS visits each leaf with $\delta \le k$ exactly once, and over the iterations $0, \ldots, d$, a node $u$ is visited $d - \delta(u) + 1$ times.

*Proof.* The first claim is Lemma 1 at the root. Node $u$ is visited in iteration $k$ exactly when $\delta(u) \le k$, that is, for $k = \delta(u), \ldots, d$. $\square$

For ILDS, all leaves are at depth $d$, and PROBE$(n, k, r)$ carries the number $r$ of levels below $n$. Its body is: if $n$ is a goal, return; if $n$ is a leaf, return failure; if $r > k$, call PROBE$(c_1, k, r - 1)$; if $k > 0$, call PROBE$(c, k - 1, r - 1)$ for each other child $c$.

**Lemma 4 (one probe of ILDS).** Suppose that no node below $n$ is a goal, that $n$ is at depth $d - r$, and that $0 \le k \le r$. Then PROBE$(n, k, r)$ visits exactly the nodes $u$ below $n$, at depth $d - r + j$ say, with $\delta_n(u) \le k \le \delta_n(u) + (r - j)$, each once. In particular it visits exactly the leaves below $n$ with $\delta_n = k$.

*Proof.* By induction on $r$. If $r = 0$, $n$ is a leaf, $k = 0$, and PROBE visits only $n$, which satisfies $0 \le 0 \le 0$. Let $r \ge 1$. The node $n$ itself has $j = 0$, $\delta_n(n) = 0$ and $0 \le k \le r$, so it should be visited, and it is. Take a node $u$ below the first child $c_1$, at depth $j \ge 1$ below $n$. Then $\delta_n(u) = \delta_{c_1}(u)$, and $u$ is $j - 1$ levels below $c_1$, which has $r - 1$ levels below it, so the number of levels left below $u$ is $r - j$ in both views. So $u$ satisfies the condition for $(n, k, r)$ if and only if it satisfies it for $(c_1, k, r - 1)$. The call on $c_1$ is made exactly when $r > k$, that is, $k \le r - 1$, which is the range of the induction, so it visits exactly these nodes. When $r \le k$, that is, $r = k$, no call is made, and no node below $c_1$ satisfies the condition: the path from $c_1$ to $u$ has $j - 1$ steps, so $\delta_n(u) + (r - j) \le (j - 1) + (r - j) = r - 1 < k$.

A node below another child $c$ has $\delta_n(u) = 1 + \delta_c(u)$ and the same number $r - j$ of levels left, so the condition $1 + \delta_c(u) \le k \le 1 + \delta_c(u) + (r - j)$ for $(n, k, r)$ is the condition $\delta_c(u) \le k - 1 \le \delta_c(u) + (r - j)$ for $(c, k - 1, r - 1)$. The call on $c$ is made exactly when $k > 0$, that is, $k - 1 \ge 0$, and $k - 1 \le r - 1$ holds. When $k = 0$, every node below $c$ has $\delta_n \ge 1 > k$, and none is visited. The subtrees are disjoint, so each node is visited once. For a leaf, $j = r$, and the condition becomes $\delta_n(u) = k$. $\square$

**Theorem 5 (ILDS).** In a tree with all leaves at depth $d$ and no goal, iteration $k$ of ILDS visits exactly the leaves with $\delta = k$, each once. Over the iterations $0, \ldots, d$, each leaf is visited once, and a complete binary tree of depth $d$ costs
$$\sum_{j=0}^{d} 2^j (d - j + 1) = 2^{d+2} - d - 3$$
node visits. With goals, ILDS returns a goal with the least $\delta$, as in Theorem 2.

*Proof.* Lemma 4 at the root with $r = d$ gives the first claim. A node at depth $j$ with $\delta(u) = i$ is visited in iteration $k$ exactly when $i \le k \le i + d - j$, so in $d - j + 1$ iterations. A complete binary tree has $2^j$ nodes at depth $j$, which gives the sum. Write $m = d - j$. Then the sum is $2^d \sum_{m=0}^{d} (m + 1) 2^{-m}$, and $\sum_{m=0}^{d} (m + 1) 2^{-m} = 4 - (d + 3) 2^{-d}$, which gives $2^{d+2} - d - 3$. The claim with goals follows from Lemma 4 as Theorem 2 follows from Lemma 1. $\square$

**Remark (the count for LDS).** By Corollary 3, LDS visits a node $u$ at depth $j$ in $d - \delta(u) + 1$ iterations. Since $d - \delta(u) + 1 \le d + 1$, the total over a complete binary tree is at most $(d + 1)(2^{d+1} - 1) = O(d\,2^d)$. Counting the leaves alone gives $\sum_i \binom{d}{i}(d - i + 1) = (d/2 + 1) 2^d$ leaf visits, so the bound is tight up to a constant factor.
