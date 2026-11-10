---
title: PRIVATE-HISTOGRAM returns the count of each key, with no race between its parallel tasks
proves: [correctness, termination]
status: full
---

We use the lines of PRIVATE-HISTOGRAM on the page. The input is $x[0 \ldots n-1]$ with each $x[i] \in \{0, \ldots, k-1\}$, cut into $p \ge 1$ blocks: block $b$ is $x[b s \ldots (b+1)s - 1]$ cut off at $n$, with $s = \max\{1, \lceil n/p \rceil\}$. Some blocks at the end can be empty. For a set $Q$ of blocks, let $\mathrm{cnt}_Q(j)$ be the number of positions $i$ in the blocks of $Q$ with $x[i] = j$.

**Lemma 1 (the blocks cover the input).** The $p$ blocks are disjoint, and together they hold each position $0, \ldots, n-1$ once.

*Proof.* Block $b$ holds the positions $i$ with $\lfloor i/s \rfloor = b$ and $i < n$. Each $i < n$ has one value of $\lfloor i/s \rfloor$, and it is less than $p$, because $i \le n - 1 < ps$: if $n \ge 1$ then $s \ge n/p$, so $ps \ge n$. $\blacksquare$

**Lemma 2 (one call).** The call on the blocks $lo, \ldots, hi - 1$ with $hi - lo \ge 1$ ends and returns a new array $H$ with $H[j] = \mathrm{cnt}_{[lo, hi)}(j)$ for each $j$.

*Proof.* By induction on $q = hi - lo$. For $q = 1$, line L2 makes a new array of zeros, and line L3 adds 1 to $H[v]$ once for each item $v$ of block $lo$, so $H[j]$ is the number of items of the block equal to $j$. For $q \ge 2$, line L5 gives $lo < mid < hi$, so both calls of lines L6 and L7 have fewer blocks and, by the hypothesis, end and return $\mathrm{cnt}_{[lo, mid)}$ and $\mathrm{cnt}_{[mid, hi)}$. The two ranges of blocks are disjoint, so line L9 gives $H[j] = \mathrm{cnt}_{[lo, mid)}(j) + \mathrm{cnt}_{[mid, hi)}(j) = \mathrm{cnt}_{[lo, hi)}(j)$. $\blacksquare$

**Lemma 3 (no races).** The two calls of lines L6 and L7 and the $k$ iterations of line L9 run in parallel with no [determinacy race](/determinacy-race/).

*Proof.* Both calls read only $x$, which no call writes, and each writes only arrays that it makes itself at line L2 or gets back from its own calls, so the two calls share no written cell. The iteration $j$ of line L9 reads $G[j]$ and writes $H[j]$, and no other iteration touches these cells. $\blacksquare$

**Theorem.** The call on all $p$ blocks returns $H$ with $H[j] = |\{ i : x[i] = j \}|$ for each $j$, which is the histogram of $x$.

*Proof.* By Lemma 2, $H[j] = \mathrm{cnt}_{[0, p)}(j)$, and by Lemma 1 this counts each position of $x$ once. By Lemma 3 the parallel run gives the same result as the sequential one. $\blacksquare$

The same proof holds for any associative and commutative way to combine two counts, so the method also computes, for each key, the sum or the maximum of values attached to the items.
