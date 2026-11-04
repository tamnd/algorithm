---
title: The Chtholly tree keeps its runs correct, and assignments cost O(log n) amortized
proves: [correctness, complexity]
status: full
---

The structure is a set $\mathcal R$ of runs $(s, e, v)$ ordered by $s$. The invariant is:

> **(C)** The runs are non-empty and disjoint, their union is $[0, n)$, and $A[k] = v$ for each run $(s, e, v) \in \mathcal R$ and each $s \le k < e$.

At the start $\mathcal R$ holds one run per position, or one run per maximal block of equal values, and (C) holds.

**Lemma 1 (SPLIT).** Let (C) hold and $0 \le x \le n$. After SPLIT$(x)$, (C) holds for the same array $A$, and if $x < n$ some run starts at $x$; the result is that run. Every run that started at some point $y$ before still starts at $y$.

*Proof.* If $x = n$ nothing changes. Otherwise, by (C), exactly one run $(s, e, v)$ has $s \le x < e$, and it is the run with the largest start $\le x$, since the runs are disjoint and sorted by start. If $s = x$ it is returned. Else $s < x < e$, and the two runs $(s, x, v)$ and $(x, e, v)$ are non-empty, cover the same positions as $(s, e, v)$, and give them the same value. The other runs do not change. $\square$

**Lemma 2 (ASSIGN).** Let (C) hold and $0 \le l < r \le n$. After ASSIGN$(l, r, v)$, (C) holds for the array $A'$ with $A'[k] = v$ for $l \le k < r$ and $A'[k] = A[k]$ otherwise.

*Proof.* By Lemma 1, after line L6 a run starts at $r$ or $r = n$, and after line L7 a run starts at $l$; the split at $l$ does not remove the start at $r$. The runs with starts in $[l, r)$ are then those from lo up to hi, and since the run boundaries include $l$ and $r$, their union is exactly $[l, r)$. Line L8 deletes them and line L9 inserts $(l, r, v)$, which covers the same positions, is non-empty, and has the value $v$. The runs outside $[l, r)$ keep their positions and values. $\square$

**Lemma 3 (EACH).** After lines L10 and L11, the runs from lo up to hi tile $[l, r)$ in order. A change of $v$ in a visited run changes $A$ only on that run.

*Proof.* As in Lemma 2. $\square$

**Theorem (amortized cost).** Let the set be a balanced search tree, and let $R$ be the number of runs, so $R \le n$. Each split costs $O(\log n)$. Let an ASSIGN delete $k$ runs. Its actual cost is $O((k + 1) \log n)$, and it changes $R$ by at most $2 - k + 1 = 3 - k$. With the potential $\Phi = c R \log n$ for a large enough constant $c$, the amortized cost is $O((k + 1) \log n) + c (3 - k) \log n = O(\log n)$. An EACH that visits $k$ runs costs $O(k + \log n)$ and raises $\Phi$ by at most $2 c \log n$, so its amortized cost is $O(k + \log n)$. Starting from $R_0$ runs, $\Phi_0 = c R_0 \log n$ and $\Phi \ge 0$ always, so $m$ operations cost $O((R_0 + m) \log n + \sum k_{\mathrm{EACH}})$ in total. $\square$

**Remark (no bound for EACH).** The term $\sum k_{\mathrm{EACH}}$ cannot be bounded in general: with $A[k] = k$ there are $n$ runs, and $m$ calls of EACH$(0, n, f)$ without assignments visit $n m$ runs.
