---
title: The tournament method returns the largest and the second largest
proves: [correctness, termination]
status: full
---

Let $b_1 \le \cdots \le b_n$ be the items of $A$ in sorted order, with $n \ge 2$. The claim is: TOURNAMENT-SECOND$(A)$ stops and returns $(b_n, b_{n-1})$, after at most $n + \lceil \lg n \rceil - 2$ comparisons.

**Termination and the shape of the rounds.** A round on $p \ge 2$ players makes $\lfloor p/2 \rfloor \ge 1$ matches and leaves $\lceil p/2 \rceil < p$ players (lines L4 to L9). So the number of players drops in each round and the loop of line L2 stops with one player. A round never adds a player, and each match removes exactly one, the loser, so the tournament makes exactly $n - 1$ matches, and each index other than the champion $m$ is the loser $l$ of exactly one match. Lines L11 and L12 scan a finite list, so the algorithm stops.

**Lemma 1 (the beaten lists).** If $l$ is appended to beaten$[w]$ in line L7, then $A[w] \ge A[l]$, and $w$ is still a player after the round in which $l$ leaves.

*Proof.* Line L6 sets $(w, l) = (u, v)$ only if $A[u] \ge A[v]$, and $(w, l) = (v, u)$ only if $A[u] < A[v]$. In both cases $A[w] \ge A[l]$. Line L7 appends $w$ to $Q$, the players of the next round. $\square$

**Lemma 2 (the champion).** $A[m] = b_n$, and for each index $i \ne m$ there is an index $j$ in beaten$[m]$ with $A[j] \ge A[i]$.

*Proof.* Let $i \ne m$. Then $i$ lost exactly one match, to some $w_1$; write $i = w_0$. If $w_1 \ne m$, then $w_1$ also lost exactly one match, to some $w_2$, in a later round than the one in which $w_0$ lost, by Lemma 1. The rounds are finite, so the chain $w_0, w_1, w_2, \ldots$ reaches the only index that never lost, $m$. Let $w_t = m$. Then $w_{t-1}$ is in beaten$[m]$, and by Lemma 1, $A[w_{t-1}] \ge A[w_{t-2}] \ge \cdots \ge A[w_0] = A[i]$. Take $j = w_{t-1}$. Also $A[m] \ge A[j] \ge A[i]$ for each $i \ne m$, so $A[m]$ is a largest item, $b_n$. $\square$

**Lemma 3 (the scan).** Let $B$ be beaten$[m]$. After line L12, $s$ is in $B$ and $A[s] \ge A[i]$ for each $i$ in $B$.

*Proof.* The list $B$ is not empty, since $n \ge 2$ and so $m$ won at least one match: the last round has two players. Line L11 sets $s$ to the first entry. Line L12 keeps the invariant "$A[s]$ is the largest value among the entries of $B$ seen so far, and $s$ is one of them": an entry $i$ with $A[i] > A[s]$ replaces $s$, and other entries are at most $A[s]$. $\square$

**Conclusion.** By Lemma 2, $A[m] = b_n$. Remove the index $m$ from $A$; the other items, sorted, are $b_1, \ldots, b_{n-1}$, so their largest is $b_{n-1}$. By Lemmas 2 and 3, $A[s] \ge A[j] \ge A[i]$ for each $i \ne m$, where $j$ is the index of Lemma 2, and $s \ne m$ is one of these indices. So $A[s]$ is the largest item other than $A[m]$, which is $b_{n-1}$.

**The count.** The tournament makes $n - 1$ comparisons. After $r$ rounds at most $\lceil n / 2^r \rceil$ players are left, so there are at most $\lceil \lg n \rceil$ rounds, and $m$ plays at most one match in each, so $|B| \le \lceil \lg n \rceil$. Line L12 makes $|B| - 1$ comparisons. The total is at most $n - 1 + \lceil \lg n \rceil - 1 = n + \lceil \lg n \rceil - 2$. $\blacksquare$
