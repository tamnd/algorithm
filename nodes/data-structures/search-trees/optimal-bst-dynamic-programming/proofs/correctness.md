---
title: OPTIMAL-BST computes the minimum expected cost and an optimal root for every interval
proves: [correctness, termination]
status: full
---

Fix $n \ge 0$, weights $p_1, \ldots, p_n \ge 0$ and $q_0, \ldots, q_n \ge 0$. For $1 \le i \le n + 1$ and $i - 1 \le j \le n$, let $\mathcal{T}(i, j)$ be the set of BSTs on the keys $k_i, \ldots, k_j$, each with the gaps $d_{i-1}, \ldots, d_j$ as leaves. For $j = i - 1$ the only tree is the single leaf $d_{i-1}$. For $T \in \mathcal{T}(i, j)$ let
$$c(T) = \sum_{l=i}^{j} p_l\,(\mathrm{depth}_T(k_l) + 1) + \sum_{l=i-1}^{j} q_l\,(\mathrm{depth}_T(d_l) + 1),$$
so the single leaf costs $q_{i-1}$. Let $W(i, j) = \sum_{l=i}^{j} p_l + \sum_{l=i-1}^{j} q_l$ and $E(i, j) = \min_{T \in \mathcal{T}(i, j)} c(T)$; the set is finite and not empty, so the minimum exists.

**Lemma 1 (decomposition).** For $i \le j$, each $T \in \mathcal{T}(i, j)$ has a root $k_r$ with $i \le r \le j$, a left subtree $L \in \mathcal{T}(i, r - 1)$ and a right subtree $R \in \mathcal{T}(r + 1, j)$, and
$$c(T) = c(L) + c(R) + W(i, j).$$
Each choice of $r$, $L$ and $R$ gives a tree of $\mathcal{T}(i, j)$.

*Proof.* By the BST property, the keys below and to the left of $k_r$ are exactly $k_i, \ldots, k_{r-1}$, and the gaps among them, and each leaf $d_l$ lies on the side of $k_r$ that the search for a value in $d_l$ takes: $d_{i-1}, \ldots, d_{r-1}$ on the left and $d_r, \ldots, d_j$ on the right. So $L \in \mathcal{T}(i, r-1)$ and $R \in \mathcal{T}(r+1, j)$. Each node $v$ of $L$ or $R$ has $\mathrm{depth}_T(v) = \mathrm{depth}_L(v) + 1$ (or with $R$), so its term in $c(T)$ is its term in $c(L)$ or $c(R)$ plus its weight. The root has depth 0 and term $p_r$. Adding up, $c(T) = c(L) + c(R) + \sum_{v} \mathrm{weight}(v) = c(L) + c(R) + W(i, j)$, since every key and every gap of the interval appears once. Conversely, a root $k_r$ with any $L$ and $R$ of the right intervals is a BST on $k_i, \ldots, k_j$, because all keys of $L$ are less than $k_r$ and all keys of $R$ are greater. $\square$

**Lemma 2 (recurrence).** $E(i, i - 1) = q_{i-1}$, and for $i \le j$,
$$E(i, j) = \min_{i \le r \le j} \bigl( E(i, r - 1) + E(r + 1, j) \bigr) + W(i, j).$$

*Proof.* The first claim holds because $\mathcal{T}(i, i-1)$ has one tree. For $i \le j$, by Lemma 1, $c(T) \ge E(i, r-1) + E(r+1, j) + W(i, j)$ for each tree with root $k_r$, so $E(i, j)$ is at least the right side. Choosing for each $r$ an optimal $L$ and an optimal $R$ gives a tree whose cost equals the term for $r$, so $E(i, j)$ is at most the right side. $\square$

**Invariant of the loops.** After the iteration of line L2 with value $\ell$ (and, for $\ell = 0$, after line L1), for each interval with $j - i + 1 \le \ell$: $w[i, j] = W(i, j)$, $e[i, j] = E(i, j)$, and, if $i \le j$, $root[i, j]$ is a value of $r$ that reaches the minimum in Lemma 2.

*Base.* Line L1 sets $e[i, i-1] = w[i, i-1] = q_{i-1} = E(i, i-1) = W(i, i-1)$.

*Step.* Take $\ell \ge 1$ and an interval $[i, j]$ with $j = i + \ell - 1$, visited by line L3. Line L4 sets $w[i, j] = w[i, j-1] + p_j + q_j$; the interval $[i, j-1]$ has length $\ell - 1$, so by the invariant $w[i, j-1] = W(i, j-1)$, and $W(i, j) = W(i, j-1) + p_j + q_j$. For each $r$ in line L5, the intervals $[i, r-1]$ and $[r+1, j]$ have length less than $\ell$, so line L6 computes $t_r = E(i, r-1) + E(r+1, j) + W(i, j)$. Lines L5 to L7 keep the running minimum of $t_i, \ldots, t_r$ in $e[i, j]$ and an index that reaches it in $root[i, j]$; the start value $\infty$ is beaten by $t_i$. After the loop, $e[i, j] = \min_r t_r = E(i, j)$ by Lemma 2. Intervals of the same length do not use each other, so the order of line L3 does not matter.

**Termination.** All loops have fixed bounds.

**The tree.** By induction on the length, the tree built from the table (root $k_{root[i,j]}$, subtrees built from $[i, root[i,j]-1]$ and $[root[i,j]+1, j]$, and the leaf $d_{i-1}$ for an empty interval) has cost $E(i, j)$: by Lemma 1 its cost is $E(i, r-1) + E(r+1, j) + W(i, j)$ with $r = root[i, j]$, which is the minimum. For $i = 1, j = n$ this is an optimal tree with cost $e[1, n]$. $\blacksquare$
