---
title: The divide-and-conquer algorithm returns a maximum-sum subarray
proves: [correctness]
status: full
---

We use the pseudocode of the page on $A[1..n]$ with $n \ge 1$. Write $S(i, j) = A[i] + \dots + A[j]$ for $i \le j$. For $lo \le hi$ let $M(lo, hi) = \max\{S(i, j) : lo \le i \le j \le hi\}$.

**Lemma 1 (crossing scan).** In a call with $lo < hi$ and $mid = \lfloor (lo + hi)/2 \rfloor$, after lines L4 to L6 we have $lo \le ci \le mid < cj \le hi$, $S(ci, cj) = sC$, and
$$sC = \max\{S(i, j) : lo \le i \le mid < j \le hi\}.$$

*Proof.* Since $lo < hi$, we have $lo \le mid < hi$, so both loops run at least once. In line L4 the running sum $t$ equals $S(i, mid)$ after the item $A[i]$ is added. The loop tries every $i$ from $mid$ down to $lo$ and keeps the largest value $ls$ with an index $ci$ that reaches it, so $ls = \max_{lo \le i \le mid} S(i, mid) = S(ci, mid)$. In the same way, line L5 gives $rs = \max_{mid < j \le hi} S(mid + 1, j) = S(mid + 1, cj)$. For $i \le mid < j$, $S(i, j) = S(i, mid) + S(mid + 1, j)$, and the two terms depend on different indices, so the largest such sum is $ls + rs = S(ci, cj)$. $\blacksquare$

**Theorem.** For $1 \le lo \le hi \le n$, $\text{MAXSUB}(A, lo, hi)$ stops and returns $(s, i, j)$ with $lo \le i \le j \le hi$, $S(i, j) = s$ and $s = M(lo, hi)$.

*Proof.* By strong induction on $m = hi - lo + 1$.

*Base, $m = 1$.* Line L1 returns $(A[lo], lo, lo)$, and $A[lo..lo]$ is the only subarray of $A[lo..hi]$.

*Step, $m \ge 2$.* Then $lo \le mid < hi$, so the two calls in line L3 are on $A[lo..mid]$ and $A[mid+1..hi]$, which are non-empty and shorter than $m$. By the induction hypothesis they stop and return $sL = M(lo, mid)$ with $S(iL, jL) = sL$, and $sR = M(mid + 1, hi)$ with $S(iR, jR) = sR$. By Lemma 1, $sC$ is the largest sum of a subarray that contains both $A[mid]$ and $A[mid + 1]$, with $S(ci, cj) = sC$.

Every subarray $A[i..j]$ of $A[lo..hi]$ has exactly one of these forms: $j \le mid$, or $i > mid$, or $i \le mid < j$. So
$$M(lo, hi) = \max(sL, sR, sC).$$
Lines L7 to L9 return a candidate whose value is at least the other two, together with its indices, and all three index pairs lie in $[lo, hi]$. $\blacksquare$

**Corollary.** $\text{MAXSUB}(A, 1, n)$ returns a maximum-sum non-empty subarray of $A$.

**Running time.** Let $T(m)$ be the number of additions in lines L4 and L5 over a call on $m$ items and all the calls under it. Then $T(1) = 0$ and $T(m) = T(\lceil m/2 \rceil) + T(\lfloor m/2 \rfloor) + m$. For $m = 2^k$ this gives $T(m) = m \lg m$ by induction: $T(2^k) = 2 \cdot 2^{k-1}(k - 1) + 2^k = k 2^k$. Since $T$ does not decrease in $m$ (again by induction), $T(m) = \Theta(m \log m)$ for every $m$, and every other line of a call costs $O(1)$, with $m - 1$ calls of more than one item. $\blacksquare$
