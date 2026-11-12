---
title: The tile index finds every hit, and every long enough exact match contains a tile
proves: [correctness]
status: full
---

Let the database $T$ have length $G$, the query $Q$ have length $q$, and the tile size be $K$. A *tile* is $T[t \ldots t+K-1]$ with $t$ a multiple of $K$ and $t + K \le G$. A *hit* is a pair $(i, t)$ such that $Q[i \ldots i+K-1]$ equals the tile at $t$. No tile is dropped as overused in Lemmas 1 to 3.

**Lemma 1 (the index).** After lines L1 and L2, the list of a word $x$ holds exactly the positions $t$ of the tiles equal to $x$, in increasing order.

*Proof.* L1 visits every multiple of $K$ from 0 to $G - K$ once, in increasing order, and L2 appends $t$ to the list of $T[t \ldots t+K-1]$. $\square$

**Lemma 2 (perfect hits).** Lines L4 to L6 report exactly the hits.

*Proof.* L4 visits every query position $i$ with $i + K \le q$. By Lemma 1 the lookup at L5 returns exactly the tile positions $t$ with tile $= Q[i \ldots i+K-1]$. $\square$

The same argument holds for near-perfect hits, because the lookups for one query word are the word itself and its $K(A-1)$ neighbours at Hamming distance 1, which are all the words within Hamming distance 1.

**Lemma 3 (tiles in a match).** Let $T[s \ldots s+H-1] = Q[i \ldots i+H-1]$ be an exact match of length $H$. Then it contains at least $\lfloor (H+1)/K \rfloor - 1$ whole tiles, and each gives a hit on the diagonal $s - i$. The bound is tight.

*Proof.* A tile at $t$ lies inside the match when $s \le t \le s + H - K$. This interval of $H - K + 1$ integers holds at least $\lfloor (H-K+1)/K \rfloor = \lfloor (H+1)/K \rfloor - 1$ multiples of $K$, since any $K$ consecutive integers hold one. For a tile at $t$, the query word at $i + (t - s)$ equals it, which is the hit $(i + t - s, t)$ with diagonal $s - i$. The bound is reached when $s$ is one more than a multiple of $K$. $\square$

So with single perfect hits, BLAT finds every gapless match of length at least $2K - 1$, and with $N$ perfect hits and a window $W \ge (N-1)K$ it finds every gapless match of length at least $(N+1)K - 1$, since $N$ consecutive tiles of the match lie on one diagonal within $(N-1)K$ query letters.

**Lemma 4 (multiple hits).** Lines L7 to L11 keep a hit $(i, t)$ exactly when the diagonal $t - i$ holds $N$ hits whose query positions lie in a window of length at most $W$ that contains $i$.

*Proof.* The hits of one diagonal are sorted by query position at L8. For each index $hi$, the loop at L9 moves $lo$ to the smallest index with $qs[hi] - qs[lo] \le W$, so $[lo, hi]$ is the largest run that ends at $hi$ and spans at most $W$. If a set of $N$ hits within a window of $W$ contains $i$, let $hi$ be its largest member; the run $[lo, hi]$ contains the whole set, so it has at least $N$ hits and contains $i$, and L11 keeps $i$. Conversely, L11 keeps only members of such a run. $\square$

**Lemma 5 (clumps).** Lines L12 to L15 return the connected components of the graph whose vertices are the hits and whose edges join two hits that differ by at most $g$ in diagonal and in query position.

*Proof.* After the sort at L12 by diagonal, the inner loop at L13 and L14 visits, for each hit, every later hit whose diagonal is at most $g$ larger, and joins the two when their query positions also differ by at most $g$. Every edge of the graph joins a hit to a later hit in this order, with diagonals at most $g$ apart, so every edge is examined, and union-find merges exactly the components. $\square$

**Expected spurious hits.** In a random database and query with uniform independent letters, a query word equals a given tile with probability $4^{-K}$. There are $q - K + 1$ query words and about $G/K$ tiles, so by linearity of expectation the expected number of chance hits is $(q - K + 1)(G/K)\,4^{-K}$. With overlapping $K$-mers in the index the count would be $K$ times larger, and the index would be $K$ times larger too.

**Sensitivity.** Let a homologous region have length $H$ with no gaps, and let each position match with probability $M$, independently. The region contains at least $\tau = \lfloor (H+1)/K \rfloor - 1$ whole tiles that do not overlap. Each one matches in full with probability $M^K$, independently of the others. So the region gives at least one perfect hit with probability at least $1 - (1 - M^K)^{\tau}$.
