---
title: ABC keeps its points in the box, its sources only improve between restarts, and it returns the best point it evaluated
proves: [correctness]
status: full
---

We use the pseudocode of the page for minimizing $f$ on the box $B = \prod_{j=1}^D [\ell_j, u_j]$ with $\ell_j < u_j$, and with $SN \ge 2$. A **try** on source $i$ is one use of the neighbor rule followed by greedy selection, in line L3 or line L5.

**Lemma (the fitness transform).** The function $\text{fit}(y) = 1/(1 + y)$ for $y \ge 0$ and $1 + |y|$ for $y < 0$ is positive and strictly decreasing on $\mathbb{R}$.

*Proof.* For $y \ge 0$, $1/(1 + y) \in (0, 1]$ and it decreases strictly. For $y < 0$, $1 + |y| = 1 - y > 1$ and it decreases strictly. Every value for $y < 0$ is above 1, and every value for $y \ge 0$ is at most 1, so the two parts join into one strictly decreasing function. $\square$

So $\text{fit}(a) > \text{fit}(b)$ holds exactly when $a < b$. In exact arithmetic, greedy selection accepts $v$ exactly when $f(v) < f(x_i)$.

**Claim 1 (feasibility).** Every source and every evaluated point lies in $B$.

*Proof.* Line L1 and line L7 draw points uniformly in $B$. A neighbor $v$ of $x_i \in B$ equals $x_i$ in all coordinates but $j$, and its coordinate $j$ is clipped to $[\ell_j, u_j]$, so $v \in B$. Greedy selection stores only $x_i$ or $v$. By induction over the tries and scouts, all sources lie in $B$, and so do all neighbors. $\square$

**Claim 2 (monotone sources).** Between two consecutive resets of source $i$ by line L7, each try on $i$ either leaves $x_i$ unchanged or replaces it by a point with a strictly smaller value of $f$.

*Proof.* Only a try on $i$ or a scout on $i$ changes $x_i$. A try replaces $x_i$ by $v$ only if $\text{fit}(v) > \text{fit}(x_i)$, which by the lemma means $f(v) < f(x_i)$. $\square$

**Claim 3 (the best point).** At the end of each cycle, the stored best point $g$ satisfies $f(g) = \min\{f(y) : y \text{ evaluated so far}\}$, so $f(g)$ never increases.

*Proof.* By induction on the cycles; before cycle 1 we take $g$ as the best start point, which is the minimum over the points of line L1. Consider one cycle. Each point $y$ evaluated in lines L3 and L5 is a neighbor of some source $i$. If $y$ is accepted, $x_i = y$ at that moment, and by Claim 2 the value of $x_i$ at line L6 is at most $f(y)$. If $y$ is rejected, $f(y) \ge f(x_i)$ at that moment, and again the value of $x_i$ at line L6 is at most $f(y)$. Line L6 sets $g$ to the best of the old $g$ and all sources, so after it, $f(g)$ is at most the value of every point evaluated so far, and $g$ is one of these points. Line L7 evaluates one more point and updates $g$ if that point is better. The source that line L7 drops is not lost: its value was already counted in line L6. $\square$

**Claim 4 (selection).** In line L5, given the sources after line L3, source $i$ is chosen with probability $p_i = \text{fit}(x_i) / \sum_s \text{fit}(x_s)$, and $p_i > p_s$ exactly when $f(x_i) < f(x_s)$.

*Proof.* The roulette wheel gives index $i$ the interval $[c_{i-1}, c_i)$ of $[0, \Phi)$, where $c_i$ is the prefix sum of the fitness values and $\Phi$ their total. For $U$ uniform in $[0, 1)$, the point $U \Phi$ falls in that interval with probability $(c_i - c_{i-1})/\Phi = p_i$. All fitness values are positive by the lemma, so $\Phi > 0$. The order of the $p_i$ is the order of the fitness values, and by the lemma it is the reverse order of the values of $f$. $\square$

**Claim 5 (trial counters).** At every time, $\text{trial}_i$ equals the number of tries on $i$ since the last accepted try on $i$, the last scout on $i$, or the start, whichever is latest. Hence, if no source has $\text{trial}_i > \text{limit}$ at line L7, no scout happens in that cycle, and line L7 resets at most one source per cycle.

*Proof.* The counter starts at 0, and line L7 sets it to 0 when it resets the source. An accepted try sets it to 0, and a rejected try adds 1. These are the only changes, which gives the first statement by induction over the events. Line L7 acts on one index, the one with the largest counter, and only when that counter exceeds $\text{limit}$. $\square$

**Remark.** The claims hold in exact arithmetic. In floating point, the lemma can fail at the level of rounding: $1/(1 + y)$ rounds to 1.0 for $0 \le y \le 2^{-53}$, so two different small values of $f$ can get equal fitness, and greedy selection then rejects an improvement. The claims still hold with the computed fitness. Rounding is monotone, so the computed fitness is still non-increasing in $f$, and a computed increase of fitness still implies a strict decrease of $f$. Only the converse fails: some improvements are rejected. In Claim 4, "exactly when" becomes "only when". $\blacksquare$
