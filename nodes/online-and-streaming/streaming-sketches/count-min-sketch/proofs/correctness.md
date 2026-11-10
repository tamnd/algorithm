---
title: The count-min sketch never underestimates and overestimates by more than epsilon times the L1 norm with probability at most delta
proves: [correctness]
status: full
---

Let the items be $0, \ldots, P - 1$ for a prime $P$, and let $f$ be the frequency vector after a sequence of updates $(x, c)$. The hash functions $h_1, \ldots, h_d$ are drawn independently, each from the family $h(x) = ((a x + b) \bmod P) \bmod w$ with $a \in \{1, \ldots, P - 1\}$ and $b \in \{0, \ldots, P - 1\}$. This family is universal: for $x \ne y$, $\Pr[h(x) = h(y)] \le 1/w$, as shown on [universal hashing](/universal-hashing/). All probabilities below are over the choice of the hash functions; the stream and the queries are fixed in advance.

**Lemma 1 (the table is linear).** After CM-UPDATE is used for every update, $C[j][b] = \sum_{y : h_j(y) = b} f_y$ for every row $j$ and column $b$.

*Proof.* By induction on the number of updates. At the start both sides are 0. An update $(x, c)$ adds $c$ to $f_x$, so it adds $c$ to the right side exactly for the pairs $(j, h_j(x))$. Lines L1 and L2 add $c$ to exactly these counters. $\square$

**Corollary (merge).** If $C$ and $C'$ are the tables for $f$ and $g$ with the same $w$, $d$ and hash functions, then by Lemma 1 the table $C + C'$ of line L7 is $\sum_{y : h_j(y) = b} (f_y + g_y)$, the table for $f + g$. In the same way $C - C'$ is the table for $f - g$.

**Theorem 1.** Assume $f_y \ge 0$ for all $y$ (the strict turnstile model). For each item $x$:

1. $\hat f_x \ge f_x$ always.
2. If $w \ge e/\varepsilon$ and $d \ge \ln(1/\delta)$, then $\Pr[\hat f_x > f_x + \varepsilon \|f\|_1] \le \delta$.

*Proof.* By Lemma 1, row $j$ gives $C[j][h_j(x)] = f_x + X_j$ with
$$ X_j = \sum_{y \ne x} f_y \cdot 1[h_j(y) = h_j(x)] . $$
Every term is non-negative, so $X_j \ge 0$ and $C[j][h_j(x)] \ge f_x$ for every $j$. Line L3 returns the minimum, so $\hat f_x = f_x + \min_j X_j \ge f_x$. This is part 1.

For part 2, if $\|f\|_1 = 0$ then $f = 0$, all $X_j = 0$ and there is nothing to prove. Otherwise, by linearity of expectation and universality,
$$ \mathbb{E}[X_j] = \sum_{y \ne x} f_y \Pr[h_j(y) = h_j(x)] \le \frac{1}{w} \sum_{y \ne x} f_y \le \frac{\|f\|_1}{w} \le \frac{\varepsilon}{e} \|f\|_1 . $$
Since $X_j \ge 0$, Markov's inequality gives
$$ \Pr[X_j > \varepsilon \|f\|_1] \le \frac{\mathbb{E}[X_j]}{\varepsilon \|f\|_1} \le \frac{1}{e} . $$
The variable $X_j$ depends only on $h_j$, and the hash functions are independent, so the events $X_j > \varepsilon \|f\|_1$ for $j = 1, \ldots, d$ are independent. The minimum is above $\varepsilon \|f\|_1$ only if all $d$ of them occur, so
$$ \Pr[\hat f_x > f_x + \varepsilon \|f\|_1] = \Pr[\min_j X_j > \varepsilon \|f\|_1] \le e^{-d} \le \delta . \qquad \square $$

**Theorem 2 (conservative update).** Let a stream of updates $(x, c)$ with $c > 0$ be processed in two tables with the same hash functions: $U$ with CM-CONSERVATIVE-UPDATE and $C$ with CM-UPDATE. Then at all times, for all $j$ and $b$,

- (a) $U[j][b] \le C[j][b]$, and
- (b) $U[j][h_j(y)] \ge f_y$ for every item $y$.

Hence the conservative estimate $\min_j U[j][h_j(x)]$ is at least $f_x$ and at most the plain estimate $\hat f_x$, and the bound of Theorem 1 holds for it with the same probability.

*Proof.* By induction on the updates. At the start all counters and all $f_y$ are 0. Consider an update $(x, c)$ with $c > 0$, and write $U$, $C$, $f$ for the values before it and $U'$, $C'$, $f'$ for the values after it.

Line L4 sets $v = \min_j U[j][h_j(x)] + c$. By (b) for $x$, $v \ge f_x + c = f'_x$.

For (b): lines L5 and L6 set every counter of $x$ to at least $v \ge f'_x$. No counter falls, and $f'_y = f_y$ for $y \ne x$, so (b) holds for all other items too.

For (a): only the counters $(j, h_j(x))$ change in either table. For such a counter, $U'[j][h_j(x)] = \max(U[j][h_j(x)], v)$. The first term is at most $C[j][h_j(x)] \le C[j][h_j(x)] + c = C'[j][h_j(x)]$ by (a) and $c > 0$. For the second, $v \le U[j][h_j(x)] + c \le C[j][h_j(x)] + c = C'[j][h_j(x)]$, because the minimum in line L4 is at most the term for row $j$. So $U' \le C'$ at this counter, and (a) holds.

The two bounds on the estimate follow by taking the minimum over $j$ in (a) and (b). The event $\hat f_x \le f_x + \varepsilon \|f\|_1$ of Theorem 1 then implies the same bound for the conservative estimate. $\square$

**Theorem 3 (merging conservative sketches).** Let $U_1$ and $U_2$ be conservative tables for streams $S_1$ and $S_2$ with positive updates and the same hash functions, with frequency vectors $f^{(1)}$ and $f^{(2)}$. Then the table $U_1 + U_2$ gives, for each item $x$, an estimate between $f^{(1)}_x + f^{(2)}_x$ and the plain estimate of the concatenated stream. So the bound of Theorem 1 for the concatenated stream holds for it.

*Proof.* By Theorem 2 (b), $U_1[j][h_j(x)] + U_2[j][h_j(x)] \ge f^{(1)}_x + f^{(2)}_x$ for every $j$. By Theorem 2 (a), $U_i \le C_i$, where $C_i$ is the plain table of $S_i$. By the merge corollary, $C_1 + C_2$ is the plain table of the concatenated stream. Take the minimum over $j$. $\square$

The merged table is not in general the conservative table of the concatenated stream, but it has the same guarantee.

**Theorem 4 (range queries).** Let the items be $0, \ldots, 2^L - 1$ with $L \ge 1$, let all counts be non-negative, and keep for each level $\ell = 0, \ldots, L$ an independent sketch of the vector $g^{(\ell)}_i = \sum_{x : \lfloor x / 2^\ell \rfloor = i} f_x$. Answer a range $[lo, hi]$ with the sum of the estimates of the intervals in the greedy dyadic cover. Then the answer is at least $\sum_{x = lo}^{hi} f_x$, and it exceeds this sum by more than $2L \varepsilon \|f\|_1$ with probability at most $2L\delta$.

*Proof.* The greedy cover starts at $lo$, takes the largest level $\ell$ such that $2^\ell$ divides $lo$ and $lo + 2^\ell - 1 \le hi$, takes the interval $[lo, lo + 2^\ell - 1]$, and moves $lo$ past it. The intervals are disjoint and their union is $[lo, hi]$.

*The cover has at most $2L$ intervals.* The search for $\ell$ stops for one of two reasons at level $\ell$: either $2^{\ell + 1}$ does not divide $lo$ while $lo + 2^{\ell+1} - 1 \le hi$ (a *rising* step), or $lo + 2^{\ell+1} - 1 > hi$ (a *falling* step).

- After a rising step at level $\ell$, $2^\ell$ divides $lo$ and $2^{\ell+1}$ does not, so the new start $lo + 2^\ell$ is divisible by $2^{\ell+1}$. At this new start, divisibility cannot stop the search at any level $\ell' \le \ell$. So the next step is either a rising step at a level $\ell' \ge \ell + 1$ or a falling step.
- At a falling step at level $\ell$, the remaining length is less than $2^{\ell+1}$, so after the step it is less than $2^\ell$, and the new start is divisible by $2^\ell$. Every later step then has a level $\ell' < \ell$ and is a falling step, since divisibility by $2^{\ell'+1}$ holds.

So the steps are rising steps with strictly increasing levels followed by falling steps with strictly decreasing levels. A level-$L$ interval is the whole domain, and then the cover is that one interval. Otherwise all levels are in $\{0, \ldots, L - 1\}$, and each level appears at most once among the rising steps and at most once among the falling steps. This gives at most $2L$ intervals.

*The error.* For each level, $\|g^{(\ell)}\|_1 = \|f\|_1$ and all entries are non-negative. By Theorem 1 each interval estimate is at least its true sum, so the answer is at least the true range sum. Each interval estimate exceeds its true sum by more than $\varepsilon \|f\|_1$ with probability at most $\delta$. By the union bound over the at most $2L$ intervals, the probability that some interval does so is at most $2L\delta$. If none does, the total excess is at most $2L \varepsilon \|f\|_1$. $\blacksquare$
