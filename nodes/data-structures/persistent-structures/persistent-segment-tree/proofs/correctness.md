---
title: The persistent segment tree keeps every version and answers sums and ranks correctly
proves: [correctness]
status: full
---

Fix $n \ge 1$. For a node $t$ and a range $[lo, hi)$ with $hi - lo \ge 1$, say that $t$ is *well formed for* $[lo, hi)$ if either $hi - lo = 1$ and $t$ is a leaf, or $hi - lo \ge 2$, $t$ is an inner node, $t.left$ is well formed for $[lo, mid)$, $t.right$ is well formed for $[mid, hi)$, and $t.sum = t.left.sum + t.right.sum$, where $mid = \lfloor (lo + hi)/2 \rfloor$. For such a $t$, define the array $\text{val}(t, lo, hi)$ by $\text{val}(t, lo, lo + 1) = \langle t.sum \rangle$ for a leaf, and $\text{val}(t, lo, hi) = \text{val}(t.left, lo, mid) \cdot \text{val}(t.right, mid, hi)$ otherwise. Since $lo < mid < hi$ when $hi - lo \ge 2$, both ranges are shorter, so the definitions are by induction on $hi - lo$.

**Lemma 1.** If $t$ is well formed for $[lo, hi)$, then $t.sum$ is the sum of $\text{val}(t, lo, hi)$.

*Proof.* By induction on $hi - lo$. For a leaf both sides are $t.sum$. For an inner node, $t.sum = t.left.sum + t.right.sum$, and by induction these are the sums of the two halves of $\text{val}(t, lo, hi)$. $\square$

**Lemma 2 (no change).** No procedure writes a field of an existing node. Hence, if $t$ is well formed for $[lo, hi)$ at some moment, it stays well formed for $[lo, hi)$ and $\text{val}(t, lo, hi)$ never changes.

*Proof.* BUILD and UPDATE only call NEW-NODE, which writes the fields of a node that did not exist before, and QUERY, GET and KTH only read. Well formedness and $\text{val}$ depend only on the fields of the nodes reachable from $t$, and none of them changes. $\square$

**Lemma 3 (build).** BUILD$(a, lo, hi)$ returns a node that is well formed for $[lo, hi)$ with $\text{val} = a[lo..hi)$.

*Proof.* By induction on $hi - lo$. Line L1 handles the leaf. Otherwise lines L3 build well formed trees for the two halves with the right arrays, and line L4 makes a node whose sum is the sum of the two child sums. $\square$

**Lemma 4 (update).** If $t$ is well formed for $[lo, hi)$ and $lo \le i < hi$, then UPDATE$(t, lo, hi, i, x)$ returns a node $t'$ that is well formed for $[lo, hi)$, with $\text{val}(t', lo, hi)$ equal to $\text{val}(t, lo, hi)$ except that position $i$ holds $x$. It makes exactly one new node per level, that is, $d + 1$ nodes where $d$ is the depth of the leaf of $i$.

*Proof.* By induction on $hi - lo$. If $hi - lo = 1$ then $i = lo$, and line L5 returns a leaf with sum $x$. Otherwise let $i < mid$ (the case $i \ge mid$ is the same with the sides swapped). By induction, $l$ is well formed for $[lo, mid)$ with the array of $t.left$ changed at $i$. The node $r = t.right$ is well formed for $[mid, hi)$ because $t$ is, and its array is the old one, which has no position $i$. Line L9 makes a node with these children and with the sum of their sums, so it is well formed, and its array is the concatenation, which is the old array with position $i$ changed. One node is made at this level plus, by induction, one per lower level on the path. $\square$

**Lemma 5 (query).** If $t$ is well formed for $[lo, hi)$, then QUERY$(t, lo, hi, l, r)$ returns the sum of $\text{val}(t, lo, hi)$ over the positions in $[lo, hi) \cap [l, r)$.

*Proof.* By induction on $hi - lo$. If the ranges do not meet (line L10) the sum is empty, 0. If $[lo, hi) \subseteq [l, r)$ (line L11) the answer is the full sum, which is $t.sum$ by Lemma 1. Otherwise $hi - lo \ge 2$, because a range of length 1 either is inside $[l, r)$ or does not meet it. Then $[lo, hi) \cap [l, r)$ is the disjoint union of its parts in $[lo, mid)$ and in $[mid, hi)$, and line L13 adds the two answers, which are right by induction. $\square$

**Theorem 1.** After any sequence of operations, for each version $v$ the root $roots[v]$ is well formed for $[0, n)$, and $\text{val}(roots[v], 0, n)$ is the array that the abstract type gives to version $v$. Each query returns the abstract answer on its version.

*Proof.* By induction on the number of operations. Version 0 is right by Lemma 3. An operation `update(v, i, x)` adds a root that is right by Lemma 4 applied to $roots[v]$, which is well formed by induction. By Lemma 2 no earlier root changes its array. `add` is `get` followed by `update`. `get` follows the one path to the leaf of $i$, and by the definition of $\text{val}$ that leaf holds position $i$. `query` is right by Lemma 5 with $[lo, hi) = [0, n)$. $\square$

**Theorem 2 (kth).** Let $u$ and $v$ be roots, both well formed for $[0, n)$, with $D = \text{val}(v) - \text{val}(u) \ge 0$ at each position, and let $1 \le k \le \sum D$. Then KTH$(u, v, k)$ returns the least $p$ with $\sum_{j \le p} D[j] \ge k$.

*Proof.* Line K1 rejects other $k$, using Lemma 1 for $\sum D = v.sum - u.sum$. Let $p^*$ be the answer. We claim that at the test of line K2 the nodes $u$ and $v$ are well formed for the current $[lo, hi)$, $p^* \in [lo, hi)$, and $k$ equals $k_0 - \sum_{j < lo} D[j]$ for the original $k_0$, with $1 \le k \le \sum_{lo \le j < hi} D[j]$. This holds at the start. In a step, let $c$ be the value of line K3; by Lemma 1, $c = \sum_{lo \le j < mid} D[j]$. If $k \le c$, then the $k$-th unit after position $lo - 1$ lies in $[lo, mid)$, so $p^* < mid$, and line K4 keeps the claim with $k$ unchanged. If $k > c$, then $p^* \ge mid$, and line K5 subtracts the $c$ units of $[lo, mid)$, which keeps $k = k_0 - \sum_{j < mid} D[j]$ and $1 \le k$. Each step halves the range, so the loop ends with $hi - lo = 1$, and then $p^* = lo$, which line K6 returns. $\blacksquare$
