---
title: The lexicographic successor visits each k-subset once, in increasing order
proves: [correctness]
status: full
---

Let $L(n, k)$ be the set of increasing lists $a = (a_1, \ldots, a_k)$ with $1 \le a_1 < \cdots < a_k \le n$. We compare lists lexicographically: $a < b$ when, at the first index $p$ with $a_p \ne b_p$, we have $a_p < b_p$. The map from a list to the set of its entries is a bijection from $L(n, k)$ to the $k$-subsets of $[n]$.

**Lemma 1 (bounds).** For $a \in L(n, k)$ and $1 \le i \le k$, we have $i \le a_i \le n - k + i$.

*Proof.* The entries $a_1 < \cdots < a_i$ are $i$ distinct integers of at least $1$, so $a_i \ge i$. The entries $a_i < a_{i+1} < \cdots < a_k$ are $k - i + 1$ distinct integers of at most $n$, so $a_i \le n - (k - i)$. $\square$

So $(1, 2, \ldots, k)$ is the smallest list of $L(n, k)$ and $(n - k + 1, \ldots, n)$ is the largest: each entry of the first is at its lower bound and each entry of the second is at its upper bound, and both are in $L(n, k)$ when $k \le n$.

**Lemma 2 (successor).** Let $a \in L(n, k)$ and let $i$ be the largest index with $a_i < n - k + i$. Then the next list after $a$ in lexicographic order is
$$a' = (a_1, \ldots, a_{i-1},\ a_i + 1,\ a_i + 2,\ \ldots,\ a_i + 1 + (k - i)).$$
If no such $i$ exists, $a$ is the largest list.

*Proof.* If no such $i$ exists, $a_j = n - k + j$ for each $j$, which is the largest list.

Otherwise, first $a' \in L(n, k)$. Its entries are increasing: $a_{i-1} < a_i < a_i + 1$, and the tail grows by $1$ at each step. Its last entry is $a_i + 1 + (k - i) \le (n - k + i) + (k - i) = n$, because $a_i + 1 \le n - k + i$. And $a' > a$, since they first differ at $i$, with $a_i + 1 > a_i$.

Now let $b \in L(n, k)$ with $b > a$, and let $p$ be the first index with $b_p \ne a_p$, so $b_p > a_p$. If $p > i$, then $a_p = n - k + p$ by the choice of $i$, and $b_p > n - k + p$ contradicts Lemma 1. So $p \le i$. If $p < i$, then $b$ and $a'$ first differ at $p$, where $b_p > a_p = a'_p$, so $b > a'$. If $p = i$, then $b_i \ge a_i + 1 = a'_i$. If $b_i > a'_i$, then $b > a'$. If $b_i = a'_i$, then for $j > i$, $b_j \ge b_i + (j - i) = a'_j$ because $b$ is increasing, so $b \ge a'$. In each case $b \ge a'$. So $a'$ is the least list greater than $a$. $\square$

**Lemma 3 (one step).** Before line L5 let $a$ be the current list, in $L(n, k)$. Then lines L5 to L9 either stop, when $a$ is the largest list, or change $a$ to its successor $a'$ of Lemma 2.

*Proof.* The loop of line L6 starts at $i = k$ and moves left while $a_i = n - k + i$. So it stops at the largest $i$ with $a_i \ne n - k + i$, which by Lemma 1 is the largest $i$ with $a_i < n - k + i$, or at $i = 0$ when there is no such index. In the second case line L7 stops, and by Lemma 2, $a$ is the largest list. In the first case, line L8 sets $a_i \leftarrow a_i + 1$, and line L9 sets $a_j \leftarrow a_{j-1} + 1$ for $j = i + 1, \ldots, k$ in this order, so $a_j = a_i + 1 + (j - i)$. This is $a'$. $\square$

**Theorem.** For $0 \le k \le n$, LEX-COMBINATIONS$(n, k)$ visits each list of $L(n, k)$ exactly once, in increasing lexicographic order, and then stops. For $k > n$ it visits nothing.

*Proof.* For $k > n$, line L1 returns, and $L(n, k)$ is empty. For $k \le n$, line L2 makes the smallest list. By Lemma 3 and induction on the number of visits, the $r$-th visit, counted from $0$, sees the $r$-th list of $L(n, k)$ in increasing order. After the largest list is visited, Lemma 3 says that the algorithm stops. The lists are visited in strictly increasing order, so none is visited twice, and since each step goes to the next list, none is skipped. For $k = 0$, $L(n, 0)$ holds only the empty list, the loop of line L6 does not run, and line L7 stops after one visit. $\blacksquare$

**The scan count.** At the visit of $a$, line L6 takes $d$ steps, where $d$ is the number of trailing entries of $a$ at their maximum. So the total number of steps is $\sum_{d \ge 1} m_d$, where $m_d$ is the number of lists whose last $d$ entries are at their maximum. These lists end with $n - d + 1, \ldots, n$, and their first $k - d$ entries form any list of $L(n - d, k - d)$. So $m_d = C(n - d, k - d)$ for $1 \le d \le k$. With $j = k - d$,
$$\sum_{d=1}^{k} C(n - d, k - d) = \sum_{j=0}^{k-1} C(n - k + j, j) = C(n, k - 1)$$
by the hockey stick identity $\sum_{j=0}^{m} C(r + j, j) = C(r + m + 1, m)$ with $r = n - k$ and $m = k - 1$. In each step except the last, line L9 writes $k - i$ entries, and this equals the number of steps of line L6 in that step. The last step takes $k$ steps of line L6 and writes nothing, so line L9 writes $C(n, k - 1) - k$ entries in total.
