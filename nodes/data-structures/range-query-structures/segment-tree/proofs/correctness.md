---
title: The operations of a segment tree keep the node invariant and return the range product
proves: [correctness, termination]
status: full
---

Let $(S, \oplus, e)$ be a monoid and let $n \ge 1$. For integers $a, b$ we write $\Pi(a, b) = A[a] \oplus A[a+1] \oplus \cdots \oplus A[b]$ when $a \le b$, and $\Pi(a, b) = e$ when $a > b$. By associativity, $\Pi(a, b)$ does not depend on the brackets, and for $a \le m + 1 \le b + 1$,

$$\Pi(a, b) = \Pi(a, m) \oplus \Pi(m + 1, b). \tag{1}$$

For $a \le b$ this is associativity; when one side is empty it is the identity law. The *range* of a node is the pair $(lo, hi)$ that the calls pass with it. The invariant is

> **(S)** for each node $v$ of range $(lo, hi)$: $T[v] = \Pi(lo, hi)$.

**Lemma 0 (the calls are well formed).** Each call BUILD$(v, lo, hi)$, QUERY$(v, lo, hi, l, r)$ or UPDATE$(v, lo, hi, i, x)$ that starts from $(1, 0, n - 1)$ has $0 \le lo \le hi \le n - 1$. If $lo < hi$, the two child ranges $(lo, mid)$ and $(mid + 1, hi)$ are nonempty, they are adjacent, their union is $(lo, hi)$, and each is shorter than $(lo, hi)$.

*Proof.* The first call has $lo = 0 \le n - 1 = hi$. If $lo < hi$, then $lo \le mid = \lfloor (lo + hi)/2 \rfloor < hi$, so $lo \le mid$ and $mid + 1 \le hi$. Both child lengths, $mid - lo + 1$ and $hi - mid$, are at least 1 and at most $hi - lo$. By induction on the depth of the call, every call has a nonempty range inside $[0, n - 1]$. $\square$

**Termination.** Each recursive call is on a child range, whose length $hi - lo$ is smaller by at least 1 than that of the caller, by Lemma 0. A call with $hi - lo = 0$ makes no recursive call in BUILD (line L1) or UPDATE (line L10). In QUERY, a call with $lo = hi$ returns in line L6 or line L7, since the single index $lo$ is either outside $[l, r]$ or inside it. So every call ends.

**Lemma 1 (build).** After BUILD$(v, lo, hi)$, (S) holds for $v$ and for every node below $v$.

*Proof.* By strong induction on $k = hi - lo$. If $k = 0$, line L1 sets $T[v] = A[lo] = \Pi(lo, lo)$, and $v$ has no node below it. If $k \ge 1$, lines L3 and L4 build the two children; their lengths are smaller, so by the induction hypothesis $T[2v] = \Pi(lo, mid)$ and $T[2v + 1] = \Pi(mid + 1, hi)$, and (S) holds below them. The two subtrees use disjoint node indices, because the indices below $2v$ start with the bits of $2v$ and those below $2v + 1$ start with the bits of $2v + 1$, so the second call does not change a cell that the first one set. Line L5 then sets $T[v] = \Pi(lo, mid) \oplus \Pi(mid + 1, hi) = \Pi(lo, hi)$ by (1). $\square$

**Lemma 2 (query).** Assume (S). Then QUERY$(v, lo, hi, l, r)$ returns $\Pi(\max(l, lo), \min(r, hi))$, that is, the product of $A$ over $[lo, hi] \cap [l, r]$ in left to right order, and $e$ when the intersection is empty. It does not change $T$.

*Proof.* By strong induction on $k = hi - lo$. Write $a = \max(l, lo)$ and $b = \min(r, hi)$.

- If $r < lo$ or $hi < l$, the intersection is empty, so $a > b$ and the answer is $e$, which line L6 returns.
- Otherwise, if $l \le lo$ and $hi \le r$, then $a = lo$ and $b = hi$, and line L7 returns $T[v] = \Pi(lo, hi)$ by (S).
- Otherwise $lo < hi$, since a range of one index is either disjoint from $[l, r]$ or inside it. By Lemma 0 the children have shorter ranges, so by the induction hypothesis the two calls of line L9 return $\Pi(\max(l, lo), \min(r, mid))$ and $\Pi(\max(l, mid + 1), \min(r, hi))$. We show that their product is $\Pi(a, b)$. Let $m = \min(\max(mid, a - 1), b)$, the last index of the intersection that is at most $mid$, or $a - 1$ if there is none. The first value equals $\Pi(a, m)$ and the second equals $\Pi(m + 1, b)$: if $a \le mid$ and $b \ge mid + 1$, then $m = mid$ and both are clear; if $b \le mid$, then $m = b$, the first value is $\Pi(a, b)$ and the second range is empty, so it gives $e = \Pi(b + 1, b)$; if $a \ge mid + 1$, then $m = a - 1$, the first range is empty and the second is $\Pi(a, b)$. In each case $a \le m + 1 \le b + 1$, so by (1) the product of line L9 is $\Pi(a, b)$, with the left value first.

QUERY only reads $T$. $\square$

The top call QUERY$(1, 0, n - 1, l, r)$ with $0 \le l \le r \le n - 1$ therefore returns $\Pi(l, r) = A[l] \oplus \cdots \oplus A[r]$.

**Lemma 3 (update).** Assume (S) before UPDATE$(1, 0, n - 1, i, x)$ with $0 \le i \le n - 1$, and let $A'$ be $A$ with $A'[i] = x$. Afterwards (S) holds for $A'$.

*Proof.* We show, by strong induction on $k = hi - lo$, that if $lo \le i \le hi$ and (S) holds for $A$ at every node below $v$ and at $v$, then after UPDATE$(v, lo, hi, i, x)$ the statement (S) holds for $A'$ at $v$ and at every node below $v$. If $k = 0$, then $lo = hi = i$ and line L10 sets $T[v] = x = A'[i]$. If $k \ge 1$, then $i$ lies in exactly one child range, by Lemma 0: the left one when $i \le mid$ and the right one otherwise, which is the test of lines L12 and L13. By the induction hypothesis, after the call that child and all nodes below it satisfy (S) for $A'$. The other child does not hold $i$ in its range, so its subtree satisfies (S) for $A$, and $A$ and $A'$ agree on its range, so it satisfies (S) for $A'$ as well; the call did not touch its cells, because they lie in the other subtree. Line L14 sets $T[v] = \Pi'(lo, mid) \oplus \Pi'(mid + 1, hi) = \Pi'(lo, hi)$ by (1) for $A'$.

At the top call, every node of the tree is the root or below it. The nodes that the call does not reach have a range without $i$, and they keep (S) by the same argument. $\square$

**Theorem.** After BUILD$(1, 0, n - 1)$ and any sequence of updates, each query $(l, r)$ with $0 \le l \le r \le n - 1$ returns $A[l] \oplus \cdots \oplus A[r]$ for the current array, and every call ends.

*Proof.* Lemma 1 gives (S) after BUILD. Lemma 3 keeps (S) across each update, and Lemma 2 shows that a query does not change $T$ and returns the right value under (S). Termination was shown above. $\blacksquare$
