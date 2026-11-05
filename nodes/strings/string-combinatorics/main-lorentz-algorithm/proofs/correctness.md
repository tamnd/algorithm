---
title: MAIN-LORENTZ reports every square occurrence exactly once
proves: [correctness, termination]
status: full
---

**Notation.** $s = s[0..n-1]$ is a string over an alphabet with equality of letters only, with 0-based indices. A square occurrence is a pair $(i, m)$ with $m \ge 1$, $0 \le i$, $i + 2m \le n$ and $s[x] = s[x+m]$ for $i \le x < i + m$; it occupies the interval $[i, i+2m)$. For words $x, y$, $\mathrm{lcp}(x, y)$ and $\mathrm{lcs}(x, y)$ are the lengths of their longest common prefix and longest common suffix. For a segment $[lo, hi)$ with $hi - lo \ge 2$, $mid = \lfloor (lo+hi)/2 \rfloor$, $u = s[lo..mid-1]$ and $v = s[mid..hi-1]$; then $|u| \ge 1$ and $|v| \ge 1$. A square occurrence is inside the segment if $lo \le i$ and $i + 2m \le hi$, and it crosses the split if moreover $i \le mid - 1$ and $i + 2m - 1 \ge mid$.

**Lemma 1 (the Z-values).** By the correctness of the Z-algorithm, $Z(t)[r] = \mathrm{lcp}(t, t[r..])$. In the iteration for the segment $[lo, hi)$:

1. For $1 \le m < |u|$, $A[m] = \mathrm{lcs}(s[lo..mid-m-1], s[lo..mid-1])$, and $A[m] \le |u| - m$. For $m = |u|$, line L7 uses $k_1 = 0$, which is the same lcs, since $s[lo..lo-1]$ is empty.
2. For $1 \le m \le |u|$, $B[|v| + 1 + |u| - m] = \mathrm{lcp}(s[mid-m..mid-1], s[mid..hi-1])$, and it is at most $\min(m, |v|)$.
3. For $1 \le m \le |v|$, $C[|u| + 1 + |v| - m] = \mathrm{lcs}(s[lo..mid-1], s[mid..mid+m-1])$, and it is at most $\min(m, |u|)$.
4. For $1 \le m < |v|$, $D[m] = \mathrm{lcp}(s[mid..hi-1], s[mid+m..hi-1])$, and $D[m] \le |v| - m$. For $m = |v|$, line L10 uses $k_2 = 0$, the same lcp.

*Proof.* (1) $\overline{u}[m..]$ is the reversal of $u[0..|u|-m-1] = s[lo..mid-m-1]$, and a common prefix of two reversals is a common suffix of the words. (2) In $t = v \# u$, the suffix at $r = |v| + 1 + |u| - m$ is $u[|u|-m..] = s[mid-m..mid-1]$, of length $m$, without $\#$. A common prefix of $t$ and $t[r..]$ cannot reach the index $|v|$ of $t$, where $t$ has $\#$, so it is a common prefix of $v$ and $s[mid-m..mid-1]$, and conversely. (3) In $\overline{u} \# \overline{v}$, the suffix at $|u| + 1 + |v| - m$ is the reversal of $v[0..m-1]$, without $\#$; as in (2), the common prefix is a common prefix of $\overline{u}$ and that reversal, that is, a common suffix of $u$ and $v[0..m-1]$. (4) Directly from the definition. $\square$

**Lemma 2 (left squares).** Fix a segment and $1 \le m \le |u|$, let $k_1, k_2, a_1, a_2$ be the values of lines L7 and L8, and let $p = mid - m$. For an integer $i$, with $a = p - i$, the following are equivalent:

- (a) $(i, m)$ is a square occurrence inside the segment that crosses the split and has $i + m \le mid$;
- (b) $a_1 \le a \le a_2$.

*Proof.* The conditions $i + m \le mid$ and $i + 2m - 1 \ge mid$ say $0 \le a \le m - 1$; and then $i \le mid - 1$ holds. Split the equalities $s[x] = s[x+m]$, $i \le x < i + m$, at $x = p$:

- for $i \le x < p$: $s[p-a..p-1] = s[mid-a..mid-1]$, the suffixes of length $a$ of $s[lo..p-1]$ and $s[lo..mid-1]$;
- for $p \le x < i + m$: $s[p..p+m-a-1] = s[mid..mid+m-a-1]$, the prefixes of length $m - a$ of $s[p..mid-1]$ and $s[mid..hi-1]$.

(a) ⇒ (b). Since $i \ge lo$, the first part is a common suffix of length $a$ of $s[lo..p-1]$ and $s[lo..mid-1]$, so $a \le k_1$ by Lemma 1. Since $i + 2m = mid + m - a \le hi$, the second part is a common prefix of length $m - a$ of $s[p..mid-1]$ and $s[mid..hi-1]$, so $m - a \le k_2$. With $0 \le a \le m - 1$, this is $\max(0, m - k_2) \le a \le \min(m - 1, k_1)$.

(b) ⇒ (a). From $a \le k_1 \le p - lo$ (Lemma 1), $i = p - a \ge lo$, and the first part holds. From $m - a \le k_2 \le |v|$, $i + 2m = mid + (m - a) \le hi$, and the second part holds. With $0 \le a \le m - 1$, $(i, m)$ is a square occurrence inside the segment that crosses the split, with $i + m \le mid$. $\square$

**Lemma 3 (right squares).** Fix a segment and $1 \le m \le |v|$, let $k_1, k_2, a_1, a_2$ be the values of lines L10 and L11, and let $q = mid + m$. For an integer $i$, with $a = mid - i$, the following are equivalent:

- (a) $(i, m)$ is a square occurrence inside the segment that crosses the split and has $i + m > mid$;
- (b) $a_1 \le a \le a_2$.

*Proof.* The conditions $i \le mid - 1$ and $i + m \ge mid + 1$ say $1 \le a \le m - 1$; and then $i + 2m - 1 \ge mid$ holds. Split the equalities at $x = mid$:

- for $i \le x < mid$: $s[mid-a..mid-1] = s[q-a..q-1]$, the suffixes of length $a$ of $s[lo..mid-1]$ and $s[mid..q-1]$;
- for $mid \le x < i + m$: $s[mid..mid+m-a-1] = s[q..q+m-a-1]$, the prefixes of length $m - a$ of $s[mid..hi-1]$ and $s[q..hi-1]$.

(a) ⇒ (b). Since $i \ge lo$ and $q \le i + 2m \le hi$, the first part gives $a \le k_1$, and since $i + 2m = q + m - a \le hi$, the second part gives $m - a \le k_2$, by Lemma 1. So $\max(1, m - k_2) \le a \le \min(m - 1, k_1)$.

(b) ⇒ (a). From $a \le k_1 \le |u|$, $i = mid - a \ge lo$. If $m = |v|$ then $k_2 = 0$ and $a_1 \ge m > a_2$, so (b) is impossible; so $m < |v|$, $q < hi$, and from $m - a \le k_2 \le hi - q$, $i + 2m = q + m - a \le hi$. Both parts hold, and with $1 \le a \le m - 1$, $(i, m)$ is a square occurrence inside the segment that crosses the split, with $i + m > mid$. $\square$

**Lemma 4 (the segment tree).** Call $[0, n)$ the root, and give each segment $[lo, hi)$ with $hi - lo \ge 2$ the children $[lo, mid)$ and $[mid, hi)$, each nonempty and shorter. Each segment of this tree is pushed exactly once and popped exactly once, and the loop of line L2 terminates.

*Proof.* The root is pushed at line L1. A segment is pushed at line L4 only as a child of the segment just popped, and only once per pop. By induction on depth, each tree segment is pushed exactly once: the root once, and a child exactly when its parent is popped, which happens once. Each push adds a segment shorter than the popped one, so the lengths along any chain of pushes decrease, and the tree is finite: it has at most $2n - 1$ segments for $n \ge 1$, and one for $n = 0$. The loop pops one segment per iteration and stops when the stack is empty, so it runs once per tree segment. $\square$

**Theorem.** MAIN-LORENTZ terminates, and every square occurrence of $s$ lies in exactly one returned triple, and every $i$ in every returned triple $(l, h, m)$ gives a square occurrence $(i, m)$.

*Proof.* Termination is Lemma 4. Every triple appended at line L8 or L11 has the form $\{\, i : a_1 \le a \le a_2 \,\}$ for one segment, side and $m$, so by Lemmas 2 and 3 all its members are square occurrences.

Let $(i, m)$ be a square occurrence. Its interval $[i, i + 2m)$ has length at least 2 and lies in the root. Starting at the root, while the current segment has a child that contains the interval, move to that child. Since lengths decrease, this stops at a segment $[lo, hi)$ that contains the interval, and neither child does. The segment has length at least 2, since it contains the interval, so it has a split $mid$, and the interval meets both $[lo, mid)$ and $[mid, hi)$, so $i \le mid - 1$ and $i + 2m - 1 \ge mid$: the occurrence crosses the split. This segment is unique, because the segments that contain the interval form a path from the root (two segments of the tree are nested or disjoint), and the occurrence crosses the split of exactly the last segment on that path: at each earlier segment it lies in one child, so it does not contain both $s[mid-1]$ and $s[mid]$.

At that segment, $1 \le m \le |u|$ if $i + m \le mid$ (since $lo \le i$), and $1 \le m < |v|$ if $i + m > mid$ (since $i + 2m \le hi$). By Lemma 2 or Lemma 3, the occurrence is in the triple of that side and that $m$, and in only one, because the side is fixed by $i + m \le mid$ and $a$ is fixed by $i$. At every other segment, the occurrence is either not inside the segment or does not cross its split, so by Lemmas 2 and 3 no triple of that segment contains it. $\blacksquare$
