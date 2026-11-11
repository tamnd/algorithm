---
title: Correctness of the Gilbert-Moore code
proves: [correctness]
status: full
---

We prove that the Gilbert-Moore code is a prefix code whose codewords keep the order of the symbols, that its mean length satisfies $L < H + 2$, and that the dynamic program of Gilbert and Moore finds an optimal alphabetic code.

**Setup.** Symbols $1, \ldots, n$ come in a fixed order with probabilities $p_i > 0$ (counts divided by their total). Let $P_i = \sum_{j < i} p_j$. Symbol $i$ owns $I_i = [P_i, P_i + p_i)$. Let $l_i = \lceil \log_2 (1/p_i) \rceil + 1$ and let $c_i$ be the first $l_i$ bits after the binary point of the midpoint $m_i = P_i + p_i / 2$. Let $t_i$ be the value of $0.c_i$, and $J_i = [t_i, t_i + 2^{-l_i})$ the set of numbers whose binary expansion starts with $c_i$.

**Lemma 1.** $J_i \subseteq I_i$.

*Proof.* Since $l_i - 1 \ge \log_2 (1/p_i)$, we have $2^{-l_i} \le p_i / 2$. Truncation gives $m_i - 2^{-l_i} < t_i \le m_i$. So $t_i > P_i$ and $t_i + 2^{-l_i} \le m_i + p_i / 2 = P_i + p_i$. $\square$

**Theorem 1 (prefix and order).** The words $c_1, \ldots, c_n$ form a prefix code, and $c_i < c_j$ in lexicographic order when $i < j$.

*Proof.* If $c_i$ were a prefix of $c_j$ for $i \ne j$, then $J_j \subseteq J_i$, so $I_i$ and $I_j$ would share a point by Lemma 1; but they are disjoint. For $i < j$, the interval $I_i$ lies to the left of $I_j$, so every number starting with $c_i$ is less than every number starting with $c_j$. At the first position where the two words differ, $c_i$ therefore has 0 and $c_j$ has 1. $\square$

**Theorem 2 (length).** $H + 1 \le L < H + 2$ for $L = \sum_i p_i l_i$.

*Proof.* Multiply $\log_2 (1/p_i) + 1 \le l_i < \log_2 (1/p_i) + 2$ by $p_i$ and add over $i$. $\square$

**Corollary.** An optimal alphabetic code has mean length below $H + 2$, since the Gilbert-Moore code is one alphabetic code.

**The dynamic program.** An alphabetic prefix code is the same as a full binary tree whose leaves, read from left to right, are the symbols in their order; a codeword is the path to its leaf, 0 for left and 1 for right. (A prefix code that is alphabetic but not full can be shortened without losing the order, by removing an inner node with one child, so an optimal one is full.) For $i \le j$ let $W(i, j) = w_i + \cdots + w_j$ and let $c(i, j)$ be the least value of $\sum_{i \le s \le j} w_s d_s$ over full binary trees with leaves $i, \ldots, j$ in order, where $d_s$ is the depth of leaf $s$.

**Theorem 3.** $c(i, i) = 0$, and for $i < j$, $c(i, j) = W(i, j) + \min_{i \le k < j} \big( c(i, k) + c(k + 1, j) \big)$.

*Proof.* A tree with leaves $i, \ldots, j$, where $i < j$, has a root with two subtrees. Because the leaves are in order, the left subtree holds the leaves $i, \ldots, k$ and the right one $k + 1, \ldots, j$, for some $k$ with $i \le k < j$. Each leaf is one level deeper in the whole tree than in its subtree, so the cost is $W(i, j)$ plus the costs of the two subtrees. For a fixed $k$, the subtrees can be chosen independently, so the best choice uses an optimal tree on each side. Taking the best $k$ gives the formula. A single leaf has depth 0. $\square$

The table has $O(n^2)$ entries, each a minimum over $O(n)$ values of $k$, so the program takes $O(n^3)$ time and $O(n^2)$ space. Following the stored best $k$ from $(1, n)$ gives the depths of an optimal tree. $\square$
