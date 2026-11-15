---
title: The merge returns the common ids in order with at most m + n - 1 comparisons
proves: [correctness]
status: full
---

Let $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$ be strictly increasing. A comparison is one three-way comparison of an id of $A$ with an id of $B$, made in line L3 and finished in line L5 when the ids differ.

**Invariant.** Before each test of line L2:

> **(J)** $R$ is the list of the ids of $A[0 \ldots i-1] \cap B[0 \ldots j-1]$ in increasing order. No id of $A[0 \ldots i-1]$ is in $B[j \ldots n-1]$, and no id of $B[0 \ldots j-1]$ is in $A[i \ldots m-1]$. Each id in $R$ is less than $A[i]$ when $i < m$, and less than $B[j]$ when $j < n$.

*Initialization.* Line L1 sets $i = j = 0$ and $R$ empty. The prefixes are empty, so each statement of (J) holds.

*Maintenance.* Assume (J) and $i < m$, $j < n$. Write $x = A[i]$ and $y = B[j]$.

- Case $x = y$ (lines L3 and L4). The new prefixes add $x$ to $A$ and $y = x$ to $B$, so the new common set is the old one plus $x$. Each id of $R$ is less than $x$, so appending $x$ keeps $R$ in increasing order. For the second statement, $x$ is not in $B[j+1 \ldots]$, because $B$ is strictly increasing and $B[j] = x$. The old ids of $A[0 \ldots i-1]$ are not in $B[j \ldots]$, so they are not in $B[j+1 \ldots]$ either. The same holds with $A$ and $B$ swapped. For the third statement, $x < A[i+1]$ and $x < B[j+1]$ by the strict order.
- Case $x < y$ (line L5). The id $x$ is not in $B[j \ldots]$, because each id there is at least $y > x$. It is not in $B[0 \ldots j-1]$ either: if $x = B[q]$ with $q < j$, then $B[q]$ would be an id of $B[0 \ldots j-1]$ that is in $A[i \ldots]$, against (J). So $x$ is in no prefix of $B$, the common set does not change, and $R$ is still right. The id $x$ is not in $B[j \ldots]$, which gives the second statement for the new $i$. The other half of the second statement only loses an index of $A[i \ldots]$. The third statement holds because $A[i+1] > A[i]$.
- Case $x > y$ (line L6). This is the case above with $A$ and $B$ swapped.

*Termination.* Each step increases $i + j$ by 1 or 2, and $i + j \le m + n$, so the loop ends after at most $m + n$ steps.

**Theorem 1.** INTERSECT$(A, B)$ returns $A \cap B$ in increasing order.

*Proof.* When the loop ends, $i = m$ or $j = n$. Take the case $i = m$; the other case is symmetric. Let $z \in A \cap B$. Then $z$ is in $A[0 \ldots m-1]$, so by (J) it is not in $B[j \ldots n-1]$. So $z$ is in $B[0 \ldots j-1]$, and by (J) it is in $R$. Each id of $R$ is in both prefixes, so in $A \cap B$. And $R$ is in increasing order by (J). $\square$

**Theorem 2.** If $m, n \ge 1$, INTERSECT$(A, B)$ makes at most $m + n - 1$ comparisons. If $m = 0$ or $n = 0$, it makes none. The bound $m + n - 1$ is reached for each $m, n \ge 1$.

*Proof.* Each step of the loop makes one comparison and increases $i + j$ by at least 1. A step runs only when $i \le m - 1$ and $j \le n - 1$, so before the step $i + j \le m + n - 2$. Since $i + j \ge t - 1$ before step $t$, each step $t$ that runs has $t - 1 \le m + n - 2$, that is $t \le m + n - 1$. If one list is empty, line L2 fails at once.

For the tightness, let $B = (1, 2, \ldots, n-1, n+m)$ and $A = (n, n+1, \ldots, n+m-1)$. The lists have no common id, so each step increases $i + j$ by exactly 1. The first $n - 1$ steps compare $A[0] = n$ with $B[0], \ldots, B[n-2]$, which are all smaller, and move $j$ to $n - 1$. The next $m$ steps compare $A[0], \ldots, A[m-1]$ with $B[n-1] = n + m$, which is larger than each of them, and move $i$ to $m$. The loop then stops after $m + n - 1$ steps. $\square$

**Theorem 3.** For $k \ge 1$ lists with lengths $n_1 \le n_2 \le \cdots \le n_k$ after line L8, INTERSECT-ALL returns their intersection in increasing order, with at most $\sum_{t=2}^{k} (n_1 + n_t - 1)$ comparisons in the loop of lines L10 and L11.

*Proof.* After the $t$-th list is merged in, $R = L_1 \cap \cdots \cap L_t$, by Theorem 1 and induction on $t$. If $R$ is empty, the intersection of all lists is empty, so the early stop is right. The list $R$ before step $t$ is a subset of $L_1$, so its length is at most $n_1$, and Theorem 2 gives at most $n_1 + n_t - 1$ comparisons for step $t$. $\blacksquare$

**Remark.** The bound of Theorem 2 is within an additive $O(\log n)$ of the lower bound $\lceil \log_2 \binom{2n}{n} \rceil$ when $m = n$. The lower bound, with its proof by a counting argument, is in the proof file of [adaptive set intersection](/adaptive-set-intersection/).
