---
title: Fagin's algorithm returns a top k set for each monotone aggregation, and its depth on independent lists
proves: [correctness, complexity]
status: full
---

Setting. There are $N$ objects and $m$ lists $L_1, \ldots, L_m$. List $L_i$ holds each object $R$ once, with grade $x_i(R)$, in non-increasing order of grade. The aggregation $t$ is *monotone*: $x_i \le x'_i$ for all $i$ implies $t(x_1, \ldots, x_m) \le t(x'_1, \ldots, x'_m)$. Write $t(R) = t(x_1(R), \ldots, x_m(R))$. A set $Y$ of $\min(k, N)$ objects is a *top $k$ set* if $t(y) \ge t(z)$ for all $y \in Y$ and $z \notin Y$.

**Lemma 1.** Let $d$ be the depth at which the loop of lines L2 to L4 stops, and suppose $d < N$ or every object has been seen. Let $z$ be an object that was not seen by sorted access. Then $t(z) \le t(h)$ for each object $h$ that was seen in all $m$ lists.

*Proof.* For each $i$, $h$ is among the first $d$ entries of $L_i$ and $z$ is not, so $x_i(z) \le x_i(h)$ because the list is sorted. By monotonicity, $t(z) \le t(h)$. $\square$

**Theorem 1 (correctness).** For a monotone $t$, FA returns a top $k$ set, with the exact score of each returned object.

*Proof.* Lines L5 and L6 fetch every missing grade of every seen object by random access, so each seen object gets its exact score, and line L7 returns the $\min(k, N)$ seen objects with the highest scores. (There are at least that many seen objects: either the loop stopped with at least $k$ matches, or $d = N$ and all objects are seen.) Let $y$ be returned and $z$ not returned. If $z$ was seen, then $t(y) \ge t(z)$ by the choice at line L7. If $z$ was not seen, then $d < N$, so the loop stopped because at least $k$ objects $h_1, \ldots, h_k$ were seen in all lists. By Lemma 1, $t(h_j) \ge t(z)$ for each $j$. These are $k$ seen objects with score at least $t(z)$, so the $k$-th highest score among seen objects is at least $t(z)$, and $t(y)$ is at least that $k$-th highest score. $\blacksquare$

**Theorem 2 (cost for a given depth).** If FA stops at depth $d$, it makes $m d$ sorted accesses and at most $(m - 1) m d$ random accesses, and keeps at most $m d$ objects in its buffer.

*Proof.* Each round of line L3 makes $m$ sorted accesses. At most $m d$ distinct objects are seen, and each needs at most $m - 1$ random accesses, since at least one of its grades came from sorted access. $\blacksquare$

**Theorem 3 (depth on independent lists, in expectation).** Suppose the $m$ lists are independent uniformly random orders of the $N$ objects. The expected number of objects that lie in the first $d$ entries of all $m$ lists is $N (d / N)^m$. So the expected number of matches reaches $k$ at depth $d^* = N^{(m-1)/m} k^{1/m}$, which is where FA is expected to stop.

*Proof.* A fixed object lies in the first $d$ entries of one list with probability $d / N$, independently over the lists, so it lies in all of them with probability $(d / N)^m$. Linearity of expectation gives $N (d / N)^m$, which equals $k$ at $d = d^*$. $\blacksquare$

Fagin (1999) showed more: the number of matches is concentrated, so FA stops at depth $O(d^*)$ with arbitrarily high probability, and for a strict $t$ every correct algorithm has middleware cost $\Omega(d^*)$ with high probability on such databases. These two results make FA optimal in the worst case with high probability; they are cited, not proved, here.
