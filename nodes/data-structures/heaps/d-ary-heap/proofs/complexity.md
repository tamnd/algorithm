---
title: The costs of the d-ary heap operations
proves: [time.worst, space]
status: full
---

Let $d \ge 2$, $n \ge 1$, and let $h$ be the height of the tree, the largest depth of a node.

**Lemma 1 (levels).** The nodes at depth $t$ are the indices $j \le n$ with $(d^t - 1)/(d - 1) < j \le (d^{t+1} - 1)/(d - 1)$. So $h$ is the least integer with $(d^{h+1} - 1)/(d - 1) \ge n$, and $h < \log_d n + 1$.

*Proof.* By induction on $t$. Depth 0 is the index 1. Let depth $t$ be the range $a < j \le b$, with $a = (d^t - 1)/(d - 1)$ and $b = (d^{t+1} - 1)/(d - 1)$. The children of these nodes are the indices from $d(a + 1 - 1) + 2 = da + 2$ to $db + 1$, and $da + 1 = b$ and $db + 1 = (d^{t+2} - 1)/(d - 1)$, so depth $t + 1$ is the range $b < j \le (d^{t+2} - 1)/(d - 1)$. A node at depth $h$ exists, so $(d^h - 1)/(d - 1) \le n - 1$, which gives $d^h \le (d - 1)(n - 1) + 1 < (d - 1) n + 1 \le d n$. So $h < \log_d n + 1$. $\square$

**Insert and decrease-key.** SIFT-UP does one comparison and at most one swap per level and goes up from depth at most $h$, so it costs $O(h + 1) = O(\log_d n + 1)$ by Lemma 1.

**Extract-min.** SIFT-DOWN goes down at most $h$ levels, and each iteration of line L6 does at most $d$ comparisons in lines L8 to L10. So it does at most $d(h + 1)$ comparisons, $O(d \log_d n)$ for $n \ge 2$.

**Lemma 2 (sum of heights).** Let $N_t$ be the number of nodes of height at least $t$. Then $N_t \le (n - 1)/d^t + 1$ for $1 \le t \le h$, and $\sum_{j} \mathrm{height}(j) \le (n - 1)/(d - 1) + h$.

*Proof.* A node $j$ has height at least $t$ exactly when its first descendant $t$ levels down exists. The first child of $j$ is $d(j - 1) + 2$, so with $g(j) = j - 1 + 1/(d - 1)$ we get $g(\text{first child}) = d\,g(j)$, and the first descendant $t$ levels down, $L_t(j)$, has $g(L_t(j)) = d^t g(j)$. So $L_t(j) \le n$ means $d^t (j - 1) + d^t/(d - 1) \le n - 1 + 1/(d - 1)$, which implies $j - 1 \le (n - 1)/d^t$. The nodes with this property are $1, \ldots, N_t$, so $N_t \le (n - 1)/d^t + 1$. Then

$$\sum_j \mathrm{height}(j) = \sum_{t=1}^{h} N_t \le \sum_{t=1}^{h} \left( \frac{n - 1}{d^t} + 1 \right) < \frac{n - 1}{d - 1} + h. \quad \square$$

**Build.** Line L22 runs SIFT-DOWN once at each internal node. At a node of height $t$, each iteration of line L6 that does a comparison is at a node with a child, and there are at most $t$ such iterations, one per level. So the sift does at most $d\,t$ comparisons. With Lemma 2 and Lemma 1, build does at most

$$d \sum_j \mathrm{height}(j) \le \frac{d(n - 1)}{d - 1} + d\,h < 2n + d(\log_d n + 1)$$

comparisons, and its time is $O$ of the same bound, so build is $O(n)$ for each $d \le n$.

**Space.** The array has $n$ cells, and each operation uses $O(1)$ extra cells.

**Theorem.** In a $d$-ary heap of $n$ keys, insert and decrease-key take $O(\log_d n + 1)$ time, extract-min takes $O(d \log_d n + d)$ time, find-min takes $O(1)$ time, and build takes $O(n + d \log_d n + d)$ time, which is $O(n)$ for $d \le n$.

*Proof.* The cases above. $\blacksquare$
