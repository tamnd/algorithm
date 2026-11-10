---
title: PRIVATE-HISTOGRAM has work n + 3pk - 2k and span ceil(lg p)(ceil(lg k) + 2) + k + ceil(n/p)
proves: [time.worst, depth.worst, space.extra]
status: full
---

**The cost model.** A step costs 1. Line L2 costs $k$ (one step per bin), and line L3 costs one step per item. A group of $r$ parallel tasks adds $r - 1$ to the work and $\lceil \lg r \rceil$ to the span, so the spawn of lines L6 and L7 adds 1 to both, and the parallel loop of line L9 over $k$ bins has work $k + (k - 1) = 2k - 1$ and span $\lceil \lg k \rceil + 1$. We write $n_b$ for the size of block $b$, with $s = \max\{1, \lceil n/p \rceil\}$ as in the correctness proof. The sizes do not increase with $b$: they are $s$ up to the block that holds position $n - 1$, then the rest of $n$, then 0. The implementation counts in this model, and the tests check both formulas below with equality.

**Theorem 1 (work).** $W = n + 3pk - 2k$.

*Proof.* The recursion is a binary tree with the $p$ blocks as its leaves, so it has $p - 1$ inner calls. The leaf of block $b$ costs $k + n_b$, and the leaves add up to $pk + n$. An inner call costs 1 for the spawn and $2k - 1$ for line L9, which is $2k$, so the inner calls add up to $2k(p - 1)$. The total is $n + pk + 2kp - 2k$. $\blacksquare$

**Theorem 2 (span).** $S = \lceil \lg p \rceil (\lceil \lg k \rceil + 2) + k + \lceil n/p \rceil$.

*Proof.* Write $c = \lceil \lg k \rceil + 2$, the span that an inner call adds on top of its larger child: 1 for the spawn and $\lceil \lg k \rceil + 1$ for line L9. We show that a call on $q \ge 1$ blocks starting at block $lo$ has span $\lceil \lg q \rceil c + k + n_{lo}$, by induction on $q$. For $q = 1$ the span is the leaf cost $k + n_{lo}$. For $q \ge 2$, line L5 gives the left call the $\lceil q/2 \rceil$ blocks from $lo$ and the right call the $\lfloor q/2 \rfloor$ blocks from $mid > lo$. By the hypothesis, the right span $\lceil \lg \lfloor q/2 \rfloor \rceil c + k + n_{mid}$ is at most the left span $\lceil \lg \lceil q/2 \rceil \rceil c + k + n_{lo}$, since $n_{mid} \le n_{lo}$. So the span is $(\lceil \lg \lceil q/2 \rceil \rceil + 1)c + k + n_{lo} = \lceil \lg q \rceil c + k + n_{lo}$, because $\lceil \lg \lceil q/2 \rceil \rceil = \lceil \lg q \rceil - 1$ for $q \ge 2$. For the top call, $lo = 0$ and $n_0 = \min\{n, s\} = \lceil n/p \rceil$. $\blacksquare$

**Corollary 3 (the choice of p).** With $p = \lceil n/k \rceil$ blocks for $n \ge 1$,

$$W \le 4n + 3k, \qquad S \le 2k + \lceil \lg n \rceil (\lceil \lg k \rceil + 2) = O(k + \log n \log k).$$

*Proof.* $pk < (n/k + 1)k = n + k$, so $W < n + 3(n + k) = 4n + 3k$. Also $\lceil n/p \rceil \le k$ and $p \le n$, so $\lceil \lg p \rceil \le \lceil \lg n \rceil$. $\blacksquare$

**Theorem 4 (the trade-off with k).** For this method, $W \cdot S \ge nk$ when $p \le n$; so a work of $O(n)$ forces a span of $\Omega(k)$, and a span of $O(\log n)$ forces a work of $\Omega(nk / \log n)$ when $k = \Omega(\log n)$.

*Proof.* By Theorems 1 and 2, $W \ge pk$ and $S \ge \lceil n/p \rceil \ge n/p$, so $W S \ge nk$. If $W \le Cn$, then $S \ge k/C$. If $S \le C \log n$, then $W \ge nk/(C \log n)$. $\blacksquare$

**Theorem 5 (space).** The run on one processor holds at most $(\lceil \lg p \rceil + 1)k$ counters at a time, beyond the input. A parallel run holds at most $pk$ counters at a time.

*Proof.* On one processor, a call holds its own array while its right call runs, so the live arrays are one for each level of the chain of active calls, and the tree has $\lceil \lg p \rceil + 1$ levels. In a parallel run, an inner call reuses the array of its left child, so at most one array per block is live. $\blacksquare$
