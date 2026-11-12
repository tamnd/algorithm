---
title: The Fenwick scan returns the number of inversions
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with the input $A[1 \ldots n]$. For $q \in [1, n]$ let $g(q) = |\{p < q : A[p] > A[q]\}|$, the number of inversions with right end $q$. Each inversion $(p, q)$ has exactly one right end, so

$$\operatorname{inv}(A) = \sum_{q=1}^{n} g(q). \tag{1}$$

**Step 1: the ranks preserve order.** Line L1 makes $V = (v_1 < v_2 < \cdots < v_m)$, the distinct values of $A$, and line L2 sets $r[j] = t$ where $v_t = A[j]$. Such a $t$ exists and is unique, because $A[j]$ is one of the values and the $v_t$ are distinct. For any $p, q$, since $v$ is strictly increasing in $t$, $A[p] > A[q]$ if and only if $r[p] > r[q]$, and $A[p] = A[q]$ if and only if $r[p] = r[q]$. Also $1 \le r[j] \le m$.

**Step 2: the Fenwick tree lemma.** Let $f[1 \ldots m]$ be a frequency array, and say that $T$ *represents* $f$ when $T[i] = \sum_{v = i - \operatorname{lowbit}(i) + 1}^{i} f[v]$ for each $i \in [1, m]$. The [Fenwick tree](/fenwick-tree/) page proves, in its file `proofs/correctness.md`, that if $T$ represents $f$, then PREFIX$(T, i)$ returns $f[1] + \cdots + f[i]$ for $0 \le i \le m$, and that after ADD$(T, m, i, d)$ with $1 \le i \le m$ the array $T$ represents $f$ with $f[i]$ increased by $d$. Both loops terminate: PREFIX clears one set bit of $i$ at each step, so it stops after at most $\lfloor \lg m \rfloor + 1$ steps, and ADD at least doubles $\operatorname{lowbit}(i) \ge 1$ at each step, so $i$ exceeds $m$ after at most $\lfloor \lg m \rfloor + 1$ steps.

**Step 3: the invariant of the scan.** For $1 \le j \le n + 1$ let $f_j[v] = |\{p < j : r[p] = v\}|$. We show that the loop of line L4 keeps:

> **(S)** Before the iteration for $j$: $T$ represents $f_j$, and $c = \sum_{q < j} g(q)$.

*Initialization.* Line L3 sets $T$ to zeros and $c = 0$. The array $f_1$ is all zeros, and an all-zero $T$ represents it, since each $T[i]$ is a sum of zeros. The sum $\sum_{q < 1} g(q)$ is empty. So (S) holds for $j = 1$.

*Maintenance.* Assume (S) for some $j \le n$. By Step 2, PREFIX$(T, r[j])$ returns

$$\sum_{v \le r[j]} f_j[v] = |\{p < j : r[p] \le r[j]\}| = |\{p < j : A[p] \le A[j]\}|,$$

where the last equality is Step 1. There are $j - 1$ indices $p < j$, and each has either $A[p] \le A[j]$ or $A[p] > A[j]$, but not both. So $(j - 1) - \mathrm{PREFIX}(T, r[j]) = |\{p < j : A[p] > A[j]\}| = g(j)$, and after line L5, $c = \sum_{q \le j} g(q)$. Line L6 calls ADD$(T, m, r[j], 1)$ with $1 \le r[j] \le m$, so by Step 2 the array $T$ then represents $f_j$ with $f_j[r[j]]$ increased by 1, which is $f_{j+1}$. So (S) holds for $j + 1$.

*Termination.* The loop of line L4 runs for $j = 1, \ldots, n$ and each iteration terminates by Step 2. After the last one, (S) holds for $j = n + 1$, so $c = \sum_{q \le n} g(q)$, which by (1) is $\operatorname{inv}(A)$. Line L7 returns it. $\blacksquare$

**The online property.** The same invariant shows that after the iteration for $j$, $c$ is $\sum_{q \le j} g(q)$, which is the inversion count of the prefix $A[1 \ldots j]$, because an inversion of the prefix is an inversion $(p, q)$ of $A$ with $q \le j$.
