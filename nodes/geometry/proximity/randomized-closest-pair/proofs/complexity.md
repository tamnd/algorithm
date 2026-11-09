---
title: The randomized grid algorithm runs in expected linear time
proves: [time.expected, time.worst, space.extra]
status: full
---

**Assumption.** Each hash table operation (lookup of a cell, insertion of a point into a cell) takes $O(1)$ expected time, as with [universal hashing](/universal-hashing/), and the floor of $x/s$ takes $O(1)$ time. The random order of line L2 and the randomness of the hash function are independent.

**Lemma 1 (cell load).** At any time, a cell of $G$ holds at most $4$ items.

*Proof.* Items in $G$ are among $P[0], \ldots, P[k-1]$, so any two are at distance at least $\delta$ (by the invariant of the correctness proof, $\delta^2 = D_k$). A cell is a half-open square $[is, (i+1)s) \times [js, (j+1)s)$ with $s \le \delta$. Cut it into four half-open squares of side $s/2$. Two points in one of them are at distance less than $(s/2)\sqrt{2} < s \le \delta$, so each holds at most one item, and the cell holds at most $4$. $\square$

So line L8 examines at most $25$ cells and $100$ items, and a step without a rebuild costs $O(1)$ expected time.

**Lemma 2 (rebuild probability).** For $2 \le k \le n - 1$, the probability that line L11 runs at step $k$ is at most $2/(k + 1)$.

*Proof.* Condition on the set $S$ of items in positions $0, \ldots, k$, not on their order. Under a uniformly random order of $P$, given $S$, each item of $S$ is equally likely to be at position $k$, with probability $1/(k + 1)$. Fix one closest pair $\{a, b\}$ of $S$ (any rule that depends only on $S$). If $P[k] \notin \{a, b\}$, then $a$ and $b$ are among the first $k$ items, so $D_k \le \|a - b\|^2 = D_{k+1} \le D_k$, hence $D_{k+1} = D_k$ and line L9 fails. So line L11 runs only if $P[k] \in \{a, b\}$, which has conditional probability at most $2/(k + 1)$. Averaging over $S$ gives the claim. $\square$

**Expected time.** Line L2 takes $O(n)$ time (Fisher-Yates shuffle), and lines L3 to L5 take $O(1)$. Step $k$ costs $O(1)$ for lines L7 to L10 and L12, plus $O(k + 1)$ for line L11 if it runs. By linearity of expectation and Lemma 2,

$$\mathbb{E}[\text{time}] = O(n) + \sum_{k=2}^{n-1} \Big( O(1) + \frac{2}{k + 1} \cdot O(k + 1) \Big) = O(n).$$

**Worst case.** Every step costs at most $O(k + 1)$, so the time is $O(n^2)$ for every order. This is reached for the order $P[i] = (2^n - 2^{n-i}, 0)$, $i = 0, \ldots, n-1$: the gap between $P[i-1]$ and $P[i]$ is $2^{n-i}$, half the previous smallest gap, so every step rebuilds. A random order makes such orders unlikely.

**Space.** $G$ holds each inserted item once, and the order and the scaled coordinates take $O(n)$ words, so the extra space is $O(n)$. $\blacksquare$
