---
title: The median filter methods output the window medians, keep step edges, remove short impulses and are not linear
proves: [correctness]
status: full
---

We write $\hat x[i] = x[\min(\max(i, 0), n-1)]$ for the clamped signal, and $W_k$ for the multiset $\{\hat x[k-m], \ldots, \hat x[k+m]\}$ of $2m + 1$ values. Its median $\operatorname{med} W_k$ is the value at index $m$ when $W_k$ is sorted.

**Theorem 1 (1D method).** For each $k$, line L6 (or line L2 for $k = 0$) outputs $\operatorname{med} W_k$.

*Proof.* We show by induction on $k$ that after line L5 of step $k$ (after line L1 for $k = 0$), $S$ is the sorted list of $W_k$. For $k = 0$ this is line L1. Assume it for $k - 1$. The multisets satisfy $W_k = (W_{k-1} \setminus \{\hat x[k-m-1]\}) \cup \{\hat x[k+m]\}$, as multisets, because the window drops its first index and gains a new last index. The value $\hat x[k-m-1]$ is in $W_{k-1}$, so line L4 finds and removes one copy of it, and $S$ stays sorted. Line L5 inserts $\hat x[k+m]$ at its sorted place. So $S$ is the sorted list of $W_k$, and $S[m]$ is its median. $\square$

**Theorem 2 (2D method).** For each $c$, line L13 (or the assignment before the loop for $c = 0$) outputs the value of rank $t = (k^2 - 1)/2$ of the block $B_c$ around $(r, c)$.

*Proof.* For a multiset $B$ of values in $\{0, \ldots, L-1\}$, let $h_B(v)$ be the number of copies of $v$ and $\ell_B(v) = \sum_{u < v} h_B(u)$. The value of rank $t$ is the unique $v$ with $\ell_B(v) \le t < \ell_B(v) + h_B(v)$, because $\ell_B$ is non-decreasing and jumps from $\ell_B(v)$ to $\ell_B(v+1) = \ell_B(v) + h_B(v)$.

We show that at line L13 of step $c$, $hist = h_{B_c}$, $below = \ell_{B_c}(med)$, and $med$ is the value of rank $t$. Line L7 sets $hist = h_{B_0}$. Line L8 starts with $med = 0$ and $below = 0 = \ell(0)$, and raises $med$ while $\ell(med) + h(med) \le t$. Each raise keeps $below = \ell(med)$. It stops at the first $med$ with $t < \ell(med) + h(med)$. At that point $\ell(med) \le t$, because for $med = 0$ we have $\ell = 0 \le t$, and a raise happens only when $\ell(med + 1) \le t$. So $med$ has rank $t$. The loop stops before $L$ because $\ell(L-1) + h(L-1) = k^2 > t$.

For step $c \ge 1$, line L10 changes the block from $B_{c-1}$ to $B_c$: it removes the $k$ pixels of the column $c - m - 1$ and adds the $k$ pixels of the column $c + m$, all clamped. Each change of one count by $\pm 1$ at a value $v$ changes $\ell(med)$ by $\pm 1$ exactly when $v < med$, and line L10 changes $below$ in the same way. So after line L10, $hist = h_{B_c}$ and $below = \ell_{B_c}(med)$ for the old $med$.

Line L11 runs while $below > t$. Each pass sets $med \leftarrow med - 1$ and subtracts $h(med)$ for the new $med$, which gives $\ell$ of the new $med$. When it stops, $\ell(med) \le t$. It does stop, because $\ell(0) = 0 \le t$. Line L12 runs while $\ell(med) + h(med) \le t$ and raises $med$, keeping $below = \ell(med)$. When it stops, $t < \ell(med) + h(med)$. If line L11 did any pass, then before its last pass $\ell(med + 1) > t$, that is $\ell(med) + h(med) > t$ for the final $med$, so line L12 does no pass and both conditions hold. If line L11 did no pass, $\ell(med) \le t$ holds before line L12 and is kept by each of its passes, as in line L8. In both cases $med$ has rank $t$. $\blacksquare$

**Theorem 3 (step edges and monotone signals).** If $x$ is non-decreasing (or non-increasing), then $\operatorname{med} W_k = x[k]$ for each $k$.

*Proof.* Clamping keeps $\hat x$ non-decreasing on all integers, so the window $\hat x[k-m], \ldots, \hat x[k+m]$ is already sorted, and its value at index $m$ is $\hat x[k] = x[k]$. A step $(a, \ldots, a, b, \ldots, b)$ with $a \le b$ is a non-decreasing signal. $\square$

**Theorem 4 (short impulses).** Let $x[i] = a$ for all $i$ in an interval $[p, q]$, except for at most $m$ indices in $[p + m, q - m]$. Then $\operatorname{med} W_k = a$ for each $k$ in $[p + m, q - m]$.

*Proof.* For such $k$, the window $W_k$ lies inside $[p, q]$, so at least $(2m + 1) - m = m + 1$ of its values equal $a$. Sorted, these $m + 1$ equal values occupy $m + 1$ consecutive places among $0, \ldots, 2m$, and every block of $m + 1$ consecutive places contains the place $m$. So the median is $a$. $\square$

**Theorem 5 (not linear).** For $m = 1$, $n = 3$, $x = (0, 0, 1)$ and $y = (1, 0, 0)$, the filter $F$ has $F(x + y) \ne F(x) + F(y)$.

*Proof.* With clamping, the windows of $x$ are $(0, 0, 0)$, $(0, 0, 1)$ and $(0, 1, 1)$, so $F(x) = (0, 0, 1)$. By symmetry $F(y) = (1, 0, 0)$. The signal $x + y = (1, 0, 1)$ has the windows $(1, 1, 0)$, $(1, 0, 1)$ and $(0, 1, 1)$, so $F(x + y) = (1, 1, 1)$. At the middle index, $1 \ne 0 + 0$. $\blacksquare$
