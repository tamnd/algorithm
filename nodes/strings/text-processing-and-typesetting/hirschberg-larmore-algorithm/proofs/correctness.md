---
title: The queue of candidates gives the least weight subsequence for a concave weight
proves: [correctness, termination]
status: full
---

**Claim.** Let $n \ge 1$ and let $w(i, j)$, for $0 \le i < j \le n$, take values in the reals or $+\infty$. Assume the inequality

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \qquad \text{for all } i \le i' < j \le j',$$

whenever all four values are finite (this is the condition that Hirschberg and Larmore call concave; it is the quadrangle inequality of a Monge array), and assume that the infinite values are closed under lengthening: if $w(i, j) = +\infty$ then $w(i'', j'') = +\infty$ for all $i'' \le i$ and $j'' \ge j$. Then HIRSCHBERG-LARMORE (lines L1 to L10) stops and returns $F[j] = F(j)$ for $j = 0, \ldots, n$, where $F(0) = 0$ and $F(j) = \min_{0 \le i < j} (F(i) + w(i, j))$, and $F[P[j]] + w(P[j], j) = F(j)$. It uses $O(n \log n)$ evaluations of $w$.

**Setup.** For $i < j$ write $g_i(j) = F(i) + w(i, j)$, the cost of reaching $j$ with $i$ as the last break. For a step $j$ and a target $j' \ge j$, let $\mathrm{best}_j(j') = \min_{i < j} g_i(j')$, the best value at $j'$ over the candidates $0, \ldots, j - 1$. So $F(j) = \mathrm{best}_j(j)$.

**Lemma 1 (a later candidate that wins keeps winning).** Let $i < i' < j \le j'$. If $g_{i'}(j) \le g_i(j)$, then $g_{i'}(j') \le g_i(j')$.

*Proof.* If $g_i(j') = +\infty$ there is nothing to show. Otherwise $F(i)$ and $w(i, j')$ are finite. By the closure, $w(i, j)$, $w(i', j)$ and $w(i', j')$ are finite too: each pair $(i, j)$, $(i', j)$, $(i', j')$ has $i \le$ its first index and $j' \ge$ its second index, so if its value were infinite, $w(i, j')$ would be infinite. Then $g_i(j)$ is finite, so $g_{i'}(j) \le g_i(j)$ makes $F(i')$ finite. All four values of the inequality are finite, and adding $F(i) + F(i')$ to both sides gives $g_i(j) + g_{i'}(j') \le g_i(j') + g_{i'}(j)$, that is $g_{i'}(j') - g_i(j') \le g_{i'}(j) - g_i(j) \le 0$. $\square$

**Lemma 2 (the new candidate wins on a final interval).** Fix $j < n$ and let $D = \{\, j' : j < j' \le n,\ g_j(j') \le \mathrm{best}_j(j') \,\}$, the targets where the new candidate $j$ is at least as good as all earlier ones. If $j' \in D$ and $j' \le j'' \le n$, then $j'' \in D$. So $D$ is empty or $D = \{d, \ldots, n\}$ for some $d$.

*Proof.* Take any $c < j$. Then $g_j(j') \le \mathrm{best}_j(j') \le g_c(j')$, and Lemma 1 with $i = c$ and $i' = j$ gives $g_j(j'') \le g_c(j'')$. This holds for every $c < j$, so $g_j(j'') \le \mathrm{best}_j(j'')$. $\square$

**Invariant.** At the start of step $j$ (line L3), the queue holds pairs $(c_1, s_1), \ldots, (c_r, s_r)$ with $r \ge 1$, $c_1 < \cdots < c_r < j$, $s_1 \le j$ and $s_1 < s_2 < \cdots < s_r \le n$, and

> **(Q)** for every $j'$ with $j \le j' \le n$, the candidate $c_t$ with $t = \max\{\, t : s_t \le j' \,\}$ has $g_{c_t}(j') = \mathrm{best}_j(j')$.

We say that $c_t$ *owns* the targets $j'$ with $s_t \le j' < s_{t+1}$ (with $s_{r+1} = n + 1$).

*Initialization.* For $j = 1$ the queue is $(0, 1)$ (line L2), and the only candidate is 0.

*Maintenance, the value.* Line L4 drops the front while $s_2 \le j$. A dropped $c_1$ owns no target $j' \ge j$, because $s_2 \le j \le j'$, so (Q) still holds, and now $s_1 \le j < s_2$. Hence $c_1$ owns $j$ and line L5 sets $F[j] = g_{c_1}(j) = \mathrm{best}_j(j) = F(j)$, with $P[j] = c_1$ a minimizer.

*Maintenance, the new candidate.* If $j = n$ the loop ends. Otherwise the step must make (Q) hold for $j + 1$, where the candidates are $0, \ldots, j$ and $\mathrm{best}_{j+1}(j') = \min(\mathrm{best}_j(j'), g_j(j'))$. By Lemma 2, $j$ attains this minimum exactly on $D$, a final interval $\{d, \ldots, n\}$ or the empty set, and the old owner attains it on the rest. So the right queue is the old one with the owners cut off at $d$, followed by $(j, d)$.

Lines L6 to L9 build this queue. Look at the back pair $(c_r, s_r)$ and let $s = \max(s_r, j + 1)$; the back candidate owns all of $s, \ldots, n$. Line L7 compares $g_j(s)$ with $g_{c_r}(s) = \mathrm{best}_j(s)$.

- If $g_j(s) \le g_{c_r}(s)$, then $s \in D$, so by Lemma 2 all targets from $s$ to $n$ are in $D$, and $c_r$ is no longer needed for any target $\ge j + 1$: every target it owns is at least $s$, or below $j + 1$. Line L7 drops it. The new back pair now owns up to $n$, and on the targets it did not own before, $j$ wins anyway, so the argument repeats with the new back pair.
- Otherwise $s \notin D$, so $D \subseteq \{s + 1, \ldots, n\}$. On $s, \ldots, n$ the back candidate owns every target, so for $s < c \le n$ the test $g_j(c) \le g_{c_r}(c)$ is the test $c \in D$, which is false and then true by Lemma 2. The binary search of line L8 keeps the invariant that every $c < lo$ in its range is not in $D$ and every $c \ge hi$ in the range $s + 1, \ldots, n$ is in $D$, or $hi = n + 1$; it stops with $lo = d$, the least element of $D$, or $lo = n + 1$ when $D$ is empty. Line L9 appends $(j, d)$ when $d \le n$.
- If every pair is dropped, then $D \supseteq \{j + 1, \ldots, n\}$: the last dropped pair was the front, with $s = \max(s_1, j+1) = j + 1$. Line L10 appends $(j, j + 1)$.

In all cases the new queue is the right one. The order conditions hold: $c_r < j$, and the new start $d$ is larger than the $s$ of the last kept pair, since $d \ge s + 1 > s_r$. The front start is at most $j + 1$: either the front is unchanged with $s_1 \le j$, or it is $(j, j + 1)$. So the invariant holds at the start of step $j + 1$.

*Termination.* The outer loop runs $n$ times. Each pass of line L4 or of the loop at line L6 drops a pair, each candidate enters the queue at most once, so there are fewer than $2n$ drops in all, and each binary search makes at most $\lceil \log_2 n \rceil + 1$ steps.

**Conclusion.** By the maintenance step, $F[j] = F(j)$ and $P[j]$ is a minimizer for every $j = 1, \ldots, n$, and $F[0] = 0$ by line L1. Each step evaluates $w$ once in line L5, twice for each dropped pair, and twice per step of the binary search, so the total is $O(n \log n)$. $\blacksquare$

**Why the closure is needed.** If an infinite value sits inside a finite region, Lemma 1 can fail. Take $w(i', j') = +\infty$ for one pair and finite values around it: the later candidate $i'$ can win at $j < j'$ and lose at $j'$ only because of the hole. The binary search then reads a test that is not monotone and can return the wrong start.
