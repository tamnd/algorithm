---
title: LEAST-ROTATION returns the smallest start of the least rotation
proves: [correctness]
status: full
---

We use the pseudocode of the page. The word is $s = s[0..n-1]$ with $n \ge 1$ over a totally ordered alphabet, all indices of $s$ are taken modulo $n$, and $\mathrm{rot}_j = s[j..n-1]\,s[0..j-1]$ for $0 \le j \le n - 1$; for any integer $j$ we write $\mathrm{rot}_j$ for $\mathrm{rot}_{j \bmod n}$, so $\mathrm{rot}_j[t] = s[j + t]$. Let $R = \min_j \mathrm{rot}_j$ in lexicographic order. A start $j \in \{0, \ldots, n-1\}$ is *least* if $\mathrm{rot}_j = R$ and a *loser* otherwise. Let $m^*$ be the smallest least start.

**Lemma 1 (elimination).** Let $x$ and $y$ be integers and $0 \le k < n$ with $s[x + t] = s[y + t]$ for $0 \le t < k$ and $s[x + k] < s[y + k]$. Then for each $0 \le t \le k$, $\mathrm{rot}_{x+t} < \mathrm{rot}_{y+t}$, so $(y + t) \bmod n$ is a loser.

*Proof.* The words $\mathrm{rot}_{x+t}$ and $\mathrm{rot}_{y+t}$ have the same length $n$. Their letters at positions $0, \ldots, k - t - 1$ are $s[x + t + r]$ and $s[y + t + r]$ with $t + r < k$, which are equal; at position $k - t \le n - 1$ they are $s[x + k] < s[y + k]$. So the first is smaller. $\square$

**Lemma 2 (period).** If $\mathrm{rot}_g = \mathrm{rot}_h$ with $0 \le g < h \le n - 1$, then $\mathrm{rot}_{j} = \mathrm{rot}_{j + (h - g)}$ for every integer $j$.

*Proof.* $s[g + t] = s[h + t]$ for all $0 \le t < n$, hence for all integers $t$ since indices are taken modulo $n$. Put $t = j - g$. $\square$

**Invariant.** Before each test of line L2:

> **(I)** $0 \le g < h$, $g \le n - 1$, and every $j$ with $0 \le j < \min(h, n)$ and $j \ne g$ is a loser.

In particular, by (I), $m^* = g$ or $m^* \ge h$.

*Initialization.* Line L1 sets $g = 0$ and $h = 1$; the only $j < 1$ is $g$.

*Maintenance.* Assume (I) and $h < n$. Lines L3 to L5 end with the largest $k \le n$ such that $s[g + t] = s[h + t]$ for $0 \le t < k$. If $k = n$, line L6 returns; that case is treated below. Otherwise $k < n$ and $s[g + k] \ne s[h + k]$.

- *Line L8.* Here $s[g + k] < s[h + k]$. By Lemma 1 with $x = g$, $y = h$, the starts $h, h + 1, \ldots, h + k$ that are below $n$ are losers. With the old losers, every $j < \min(h + k + 1, n)$ other than $g$ is a loser, and $g < h < h + k + 1$. So (I) holds with the new $h = h + k + 1$.
- *Lines L10 and L11.* Here $s[h + k] < s[g + k]$. By Lemma 1 with $x = h$, $y = g$, the starts $g, \ldots, g + k$ below $n$ are losers. Let $M = \max(h, g + k + 1)$. Every $j < M$ is a loser: if $j < h$ and $j \ne g$ this is (I); $j = g$ was just shown; if $h \le j < g + k + 1$ then $j = g + t$ with $1 \le t \le k$. Since $m^*$ is not a loser, $m^* \ge M$, so $M \le n - 1$. Line L10 sets $g = M$ and line L11 sets $h = M + 1$; then $g \le n - 1$, $g < h$, and the only $j < h$ that may not be a loser is $g$. So (I) holds.

*Termination of the loop.* If the loop ends because $h \ge n$, then by (I) every start other than $g$ is a loser, and $m^*$ exists, so $m^* = g$ and line L12 returns it.

*The return at line L6.* Here $\mathrm{rot}_g = \mathrm{rot}_h$ with $g < h \le n - 1$; let $d = h - g$. By (I), $m^* = g$ or $m^* \ge h$. Suppose $m^* \ge h$. The numbers $m^* - d, m^* - 2d, \ldots$ decrease by $d$, so exactly one of them, say $j = m^* - qd$ with $q \ge 1$, lies in the interval $[g, h)$, which has length $d$. By Lemma 2 applied $q$ times, $\mathrm{rot}_j = \mathrm{rot}_{m^*} = R$, so $j$ is a least start with $j < m^*$, contradicting the choice of $m^*$. Hence $m^* = g$ and line L6 returns it.

*The loop stops.* Each pass of the loop of line L2 that does not return increases $g + h$ by at least $k + 1 \ge 1$: line L8 adds $k + 1$, and lines L10 and L11 replace $g + h$ by $2M + 1 \ge (g + k + 1) + h + 1$. While the loop runs, $g + h \le 2n - 2$, so the number of passes is finite, and the inner loop of line L4 makes at most $n$ steps per pass.

**Claim.** LEAST-ROTATION returns $m^*$, the smallest index at which the least rotation of $s$ starts. This follows from the two exits above. $\blacksquare$

**Comparison count.** A pass that stops at a difference after $k$ equal letters performs $k + 1$ three-way letter comparisons and increases $g + h$ by at least $k + 1$. Initially $g + h = 1$. After the last such pass, $g \le n - 1$ and $h \le (n - 1) + (n - 1) + 1 = 2n - 1$, so these passes perform at most $3n - 3$ comparisons in total. A pass that returns at line L6 performs $n$ comparisons and starts with $g + h \le 2n - 3$, so the passes before it performed at most $2n - 4$ comparisons. In both cases the total is at most $3n - 3 < 3n$. Each comparison costs $O(1)$ together with the index updates, so the running time is $\Theta(n)$ and the extra space is $\Theta(1)$. ∎
