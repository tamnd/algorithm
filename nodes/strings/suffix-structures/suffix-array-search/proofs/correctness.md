---
title: SA-BOUND returns the lower bound or the upper bound of the pattern
proves: [correctness, termination, complexity]
status: full
---

Let $S = S[0 \ldots n-1]$, $SA$ its suffix array, $P = P[0 \ldots m-1]$ with $m \ge 0$. Write $T_q = S_{SA[q]}$ for the suffix of rank $q$ and $T_q^m$ for its prefix of length $\min(m, |T_q|)$. Add $T_{-1}$, smaller than every string, and $T_n$, larger than every string, with $lcp(T_{-1}, x) = lcp(T_n, x) = 0$ for each $x$. Write $lcp(a, b)$ for the length of the longest common prefix of $T_a$ and $T_b$.

Call rank $q$ *low* if $T_q^m < P$ (non-strict search) or $T_q^m \le P$ (strict search). By Lemma 2 of the suffix array proof, the $T_q^m$ are sorted, so the low ranks are $0, \ldots, b - 1$ for some $b$, and $b$ is the lower bound (or the upper bound). Count $-1$ as low and $n$ as not low.

**Fact A (order of sorted strings).** For $a < c$ among $-1, \ldots, n$ and $d = lcp(a, c)$: either $T_a$ has length $d$, or both have a symbol at position $d$ and $T_a[d] < T_c[d]$ (with the virtual ranks this holds by convention). This is the definition of $T_a < T_c$.

**Fact B.** For $a < c < e$, $lcp(a, e) = \min(lcp(a, c), lcp(c, e))$ when all three are real, and $lcp(a, e) \le lcp(a, c)$, $lcp(a, e) \le lcp(c, e)$ in all cases. This is the usual property of sorted strings: $lcp(a, e) = \min(LCP[a+1], \ldots, LCP[e])$.

**Invariant.** At each test of line L3: $lo$ is low, $hi$ is not low, $lo < hi$, $l = lcp(P, T_{lo})$ and $r = lcp(P, T_{hi})$, where $lcp(P, x)$ is the length of the longest common prefix of $P$ and $x$. Also $Llcp[mid] = lcp(lo, mid)$ and $Rlcp[mid] = lcp(mid, hi)$ for the midpoint computed in line L4. The last statement holds because $(lo, hi)$ is always one of the intervals of the fixed recursion $(-1, n) \to (lo, mid), (mid, hi)$ used to build the tables.

**Initialization.** $lo = -1$ is low, $hi = n$ is not, and $l = r = 0$.

**Maintenance.** Let $lo < mid < hi$.

*Line L6: $l \ge r$ and $Llcp[mid] > l$.* Then $T_{mid}$ agrees with $T_{lo}$ on the first $l + 1$ symbols, so $lo \ne -1$ and $T_{lo}$ has a symbol at position $l$. If $l = m$, then $P$ is a prefix of $T_{lo}$; since $lo$ is low, the search is strict, and $P$ is also a prefix of $T_{mid}$, so $mid$ is low. If $l < m$, then $T_{lo}$ and $P$ differ at $l$, and $T_{lo}[l] < P[l]$ because $lo$ is low; $T_{mid}[l] = T_{lo}[l] < P[l]$ and they agree before $l$, so $T_{mid}^m < P$ and $mid$ is low, with $lcp(P, T_{mid}) = l$. In both cases $lo \leftarrow mid$ keeps the invariant with the same $l$.

*Line L7: $l \ge r$ and $Llcp[mid] = d < l$.* Then $lo \ne -1$ (else $l = 0$), and by Fact A at position $d$ either $T_{lo}$ ends at $d$, which is impossible since $T_{lo}$ agrees with $P$ on $l > d$ symbols, or $T_{lo}[d] < T_{mid}[d]$ (or $mid$ is virtual, which it is not). Since $T_{lo}[d] = P[d]$ and $d < l \le m$, we get $P[d] < T_{mid}[d]$ with agreement before $d$. So $T_{mid}^m > P$, $mid$ is not low in either search, and $lcp(P, T_{mid}) = d$. Setting $hi \leftarrow mid$, $r \leftarrow d$ keeps the invariant.

*Lines L9 and L10* are the mirror images, with $T_{hi}$, Fact A for $mid < hi$, and "not low" in place of "low". For L9, $Rlcp[mid] > r$ means $T_{mid}$ agrees with $T_{hi}$ beyond position $r$; if $r = m$ then $P$ is a prefix of $T_{hi}$, the search is not strict, and $P$ is a prefix of $T_{mid}$, so $mid$ is not low; if $r < m$, $T_{hi}$ has a symbol at $r$ (else $T_{hi}$ would be a proper prefix of $P$, hence low), $T_{hi}[r] > P[r]$, and the same holds for $T_{mid}$. For L10, $Rlcp[mid] = d < r$ gives $T_{mid}[d] < T_{hi}[d] = P[d]$ or $T_{mid}$ ending at $d$, so $mid$ is low with $lcp(P, T_{mid}) = d$.

*Lines L8, L11, L12 to L15.* If $l \ge r$ and $Llcp[mid] = l$, then $T_{mid}$ agrees with $T_{lo}$, and so with $P$, on the first $l$ symbols (if $lo = -1$ then $l = 0$ and there is nothing to show). The case $l < r$, $Rlcp[mid] = r$ is the same with $hi$. So line L12 starts with a $k$ such that $T_{mid}$ and $P$ agree on $k$ symbols, and ends with $k = lcp(P, T_{mid})$. Line L13 then decides lowness: if $k = m$, $T_{mid}^m = P$, low exactly in the strict search; if $T_{mid}$ ends at $k < m$, $T_{mid}^m = T_{mid}$ is a proper prefix of $P$, so low; otherwise the order of $T_{mid}[k]$ and $P[k]$ decides. Lines L14 and L15 move $lo$ or $hi$ and store $k$ into $l$ or $r$, which keeps the invariant.

**Termination and result.** Each pass replaces $(lo, hi)$ by $(lo, mid)$ or $(mid, hi)$ with $lo < mid < hi$, so $hi - lo$ decreases, and the loop ends with $hi = lo + 1$. Then $lo$ is low and $hi$ is not; since the low ranks are $-1, 0, \ldots, b - 1$, $hi = b$. So line L16 returns the lower bound for the non-strict search and the upper bound for the strict one, and the suffixes that start with $P$ are exactly the ranks in $[lb, ub)$.

**Comparison count.** With $\lfloor (lo + hi)/2 \rfloor$, the new gap is at most $\lceil (hi - lo)/2 \rceil$, so from $hi - lo = n + 1$ there are at most $\lceil \lg(n+1) \rceil$ passes. The value $\max(l, r)$ never decreases: lines L6 and L9 change neither; line L7 runs with $l \ge r$ and sets $r$ below $l$; line L10 runs with $l < r$ and sets $l$ below $r$; lines L14 and L15 store the end of line L12, which started at $\max(l, r)$. Each successful equality test in line L12 makes $k$, and then $\max(l, r)$, one larger than any earlier value, and $\max(l, r) \le m$, so the successful tests number at most $m$ over the whole search. Each pass has at most one failed equality test and at most one order test in line L13. So the search uses at most $m + 2 \lceil \lg(n+1) \rceil$ symbol comparisons. $\blacksquare$
