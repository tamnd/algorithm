---
title: Prefix doubling sorts the suffixes, and the two searches find the range of a pattern
proves: [correctness, termination]
status: full
---

Let $S = S[0 \ldots n-1]$ with $n \ge 1$, $S_i = S[i \ldots n-1]$, and for $\ell \ge 0$ let $S_i^{\ell}$ be the prefix of length $\min(\ell, n - i)$ of $S_i$. Strings are compared in lexicographic order, in which a proper prefix is smaller.

**Lemma 1 (splitting).** For $k \ge 1$ and positions $i, j$: $S_i^{2k} < S_j^{2k}$ if and only if $S_i^{k} < S_j^{k}$, or $S_i^{k} = S_j^{k}$ and $S_{i+k}^{k} < S_{j+k}^{k}$, where a suffix that starts at $n$ or later is the empty string.

*Proof.* $S_i^{2k}$ is the concatenation $S_i^{k} \cdot S_{i+k}^{k}$: if $n - i \ge k$, the first part has length $k$ and the second is the rest, cut at length $k$; if $n - i < k$, the first part is all of $S_i$ and the second is empty. If $S_i^{k} \ne S_j^{k}$, then either they differ at a position less than $k$ and inside both, which decides both comparisons the same way, or one of them is a proper prefix of the other. In the second case the shorter one, say $S_i^k$, has length less than $k$, so it is all of $S_i$, and $S_i^{2k} = S_i^k$ is a proper prefix of $S_j^{2k}$ as well, so the order is again the same. If $S_i^{k} = S_j^{k}$, both have the same length; if that length is less than $k$ then both second parts are empty and the strings are equal, which matches "$S_{i+k}^k < S_{j+k}^k$ is false"; otherwise the comparison of the $2k$-prefixes is the comparison of the second parts. $\square$

**Invariant (R).** After line L2, and after line L6 in the round with value $k$ (writing $K = 2k$, or $K = 1$ after line L2): for all $i, j$, $rank[i] < rank[j]$ if and only if $S_i^K < S_j^K$, and $rank[i] = rank[j]$ if and only if $S_i^K = S_j^K$. Moreover the ranks are $0, 1, \ldots, d - 1$, where $d$ is the number of distinct $K$-prefixes, and after line L6 $SA$ lists the positions in non-decreasing order of rank.

*Initialization.* Line L2 ranks each position by its symbol among the sorted distinct symbols, which is the order of the 1-prefixes.

*Maintenance.* In the round with value $k$, (R) holds with $K = k$ before line L4. The key of line L4 is $(rank[i], rank[i+k])$ with $-1$ when $i + k \ge n$. The value $-1$ is below each rank, as the empty string is below each nonempty one. By (R) for $K = k$ and Lemma 1, $key(i) < key(j)$ in lexicographic order of pairs if and only if $S_i^{2k} < S_j^{2k}$, and $key(i) = key(j)$ if and only if $S_i^{2k} = S_j^{2k}$. Line L5 sorts by key, and line L6 gives rank 0 to the first position and adds 1 exactly when the key changes, so the new ranks are $0, \ldots, d-1$ and satisfy (R) with $K = 2k$.

*Termination and result.* If line L7 sees $rank[SA[n-1]] = n - 1$, the $n$ ranks are $0, \ldots, n-1$, so the $2k$-prefixes of the $n$ suffixes are pairwise distinct. Two suffixes whose $2k$-prefixes differ compare like these prefixes (a common prefix of length $2k$ would make them equal), so $SA$ is in increasing order of the suffixes and $rank$ is its inverse. The test holds at the latest when $2k \ge n$: then $S_i^{2k} = S_i$ for each $i$, and different suffixes are different strings. Since $k$ doubles in line L8, there are at most $\lceil \lg n \rceil + 1$ rounds, and the loop ends. $\square$

**Lemma 2 (monotone heads).** For a pattern $P$ of length $m$, let $h(r) = S_{SA[r]}^{m}$. Then $h(0) \le h(1) \le \cdots \le h(n-1)$, and the set of $r$ with $h(r) = P$ is $\{\, r : P \text{ is a prefix of } S_{SA[r]} \,\}$.

*Proof.* Let $x < y$ be two strings and cut both to length $m$. If $x$ and $y$ differ at a first position $p$ inside both, the cut strings are equal when $p \ge m$, and ordered like $x$ and $y$ otherwise. If $x$ is a proper prefix of $y$, the cut of $x$ is a prefix of the cut of $y$. In all cases the cuts satisfy $\le$. The second statement holds because $h(r)$ has length $m$ exactly when the suffix has length at least $m$, and then $h(r) = P$ means that $P$ is a prefix of the suffix; a shorter $h(r)$ is never equal to $P$. $\square$

**Theorem.** SA-BOUND$(P, \text{false})$ returns the least $r$ with $h(r) \ge P$, and SA-BOUND$(P, \text{true})$ the least $r$ with $h(r) > P$ ($n$ if there is none). The suffixes that start with $P$ are exactly those with ranks in $[lo, hi)$, where $lo$ and $hi$ are these two values.

*Proof.* The predicate $q(r)$, "$h(r) \ge P$" or "$h(r) > P$", is monotone in $r$ by Lemma 2: once true, it stays true. Lines L9 to L16 keep the invariant "$q(r)$ is false for $r < lo$, and true for $r \ge hi$ with $hi \le n$" (where $q(n)$ is read as true). It holds at line L9. In a step, $lo \le mid < hi$; line L14 sets $lo = mid + 1$ only when $q(mid)$ is false, so $q$ is false for all $r \le mid$ by monotonicity; line L15 sets $hi = mid$ only when $q(mid)$ is true. The length $hi - lo$ drops by at least $\lceil (hi - lo)/2 \rceil \ge 1$ in each step, so the loop ends with $lo = hi$, the least $r$ with $q(r)$ true. By Lemma 2, the ranks with $h(r) = P$ are those with $h(r) \ge P$ and not $h(r) > P$, which form the interval $[lo, hi)$, and they are the ranks of the suffixes that start with $P$. $\blacksquare$
