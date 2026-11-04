---
title: Floyd's method uses fewer than n swaps and 2n comparisons
proves: [time.worst, time.best, time.average, space.extra]
status: full
---

Let $n \ge 1$. For a node $i$, its *height* $h(i)$ is the largest $h \ge 0$ such that $2^h i \le n$. We write $T(i)$ for the set of nodes of the subtree of $i$.

**Lemma 1.** $h(i)$ is the largest depth of a node of $T(i)$ below $i$.

*Proof.* The nodes of $T(i)$ at depth $d$ below $i$ are the indices $2^d i, 2^d i + 1, \ldots, 2^d i + 2^d - 1$ that are at most $n$, by induction on $d$: the children of the indices $2^{d} i$ to $2^d i + 2^d - 1$ are the indices $2^{d+1} i$ to $2^{d+1} i + 2^{d+1} - 1$. So there is a node at depth $d$ exactly when the smallest of them, $2^d i$, is at most $n$. $\square$

**Lemma 2.** MAX-HEAPIFY$(A, n, i)$ does at most $h(i)$ swaps and at most $2h(i)$ key comparisons.

*Proof.* Let $i_0$ be the first value of $i$, so the claim is about $h(i_0)$. Each swap moves $i$ one level down inside $T(i_0)$, so by Lemma 1 there are at most $h(i_0)$ swaps. Each iteration does at most 2 comparisons (lines L5 and L6), and an iteration at a leaf does none, because both tests $l \le n$ and $r \le n$ fail. Let $s$ be the number of swaps. There are $s + 1$ iterations. If the last one is at a leaf, the comparisons are at most $2s \le 2h(i_0)$. Else the last node has a child, so it is at depth $s \le h(i_0) - 1$, and the comparisons are at most $2(s + 1) \le 2h(i_0)$. $\square$

**Lemma 3.** $\sum_{i=1}^{n} h(i) = n - s_2(n)$, where $s_2(n)$ is the number of 1 bits of $n$.

*Proof.* By the definition, $h(i) \ge h$ exactly when $2^h i \le n$, that is, when $i \le \lfloor n/2^h \rfloor$. So, counting each $i$ once for each $h$ with $1 \le h \le h(i)$,

$$\sum_{i=1}^{n} h(i) = \sum_{h \ge 1} \#\{i : h(i) \ge h\} = \sum_{h \ge 1} \left\lfloor \frac{n}{2^h} \right\rfloor.$$

Write $n = \sum_{j=0}^{L} b_j 2^j$ with $b_j \in \{0, 1\}$. Then $\lfloor n/2^h \rfloor = \sum_{j \ge h} b_j 2^{j-h}$, because the part $\sum_{j < h} b_j 2^j$ is less than $2^h$. Summing over $h \ge 1$ and exchanging the sums,

$$\sum_{h \ge 1} \sum_{j \ge h} b_j 2^{j-h} = \sum_{j \ge 1} b_j \sum_{h=1}^{j} 2^{j-h} = \sum_{j \ge 0} b_j (2^j - 1) = n - \sum_j b_j = n - s_2(n).$$

(The term $j = 0$ adds $b_0 (2^0 - 1) = 0$.) $\square$

**Theorem.** BUILD-MAX-HEAP does at most $n - s_2(n)$ swaps and at most $2(n - s_2(n))$ key comparisons. Its time is $\Theta(n)$ on each input of size $n$, and its extra space is $\Theta(1)$.

*Proof.* Line L1 calls MAX-HEAPIFY once for each $i \le \lfloor n/2 \rfloor$. The leaves $i > \lfloor n/2 \rfloor$ have $h(i) = 0$, so by Lemmas 2 and 3 the swaps are at most $\sum_i h(i) = n - s_2(n)$ and the comparisons at most $2(n - s_2(n))$. Each call costs $O(1)$ plus $O(1)$ for each iteration, and each iteration other than the last does one swap. So the time is $O(\lfloor n/2 \rfloor + n - s_2(n)) = O(n)$. Line L1 does $\lfloor n/2 \rfloor$ iterations on every input, so the time is $\Omega(n)$ in the best case too. The method keeps only the indices $i$, $l$, $r$ and $m$ and one key for a swap. $\blacksquare$
