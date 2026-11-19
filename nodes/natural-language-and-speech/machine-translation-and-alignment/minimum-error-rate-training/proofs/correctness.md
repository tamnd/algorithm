---
title: The line search of minimum error rate training finds the exact maximum of the metric along the line
proves: [correctness]
status: full
---

Fix a tuning set of $S$ sentences. Sentence $i$ has an n-best list of candidates $c = 1, \ldots, n_i$, each with a feature vector $h_{i,c} \in \mathbb{R}^D$ and a tuple of sufficient statistics $\phi_{i,c}$ (for BLEU: the clipped n-gram matches, the n-gram counts, the candidate length and the reference length). For weights $w$ the decoder picks, in each list, the candidate $\hat c_i(w)$ with the largest $w \cdot h_{i,c}$, the smallest index on ties. The corpus value is $M(w) = \mu\bigl(\sum_i \phi_{i, \hat c_i(w)}\bigr)$ for a function $\mu$ of the summed statistics. LINE-SEARCH gets $w$ and a direction $d$ and looks at $F(\gamma) = M(w + \gamma d)$ for $\gamma \in \mathbb{R}$.

For candidate $c$ of sentence $i$, $(w + \gamma d) \cdot h_{i,c} = a_{i,c} + \gamma \, b_{i,c}$ with $a_{i,c} = w \cdot h_{i,c}$ and $b_{i,c} = d \cdot h_{i,c}$: a line in $\gamma$.

**Lemma 1 (the upper envelope).** UPPER-ENVELOPE returns points $-\infty = g_0 < g_1 < \cdots < g_r$ and candidates $c_0, \ldots, c_r$ such that for every $\gamma$ in the open interval $(g_q, g_{q+1})$ (with $g_{r+1} = +\infty$), the line of $c_q$ is strictly above every line with another slope, and is a highest line.

*Proof.* Lines U1 sort the lines by slope and keep, for each slope, only the highest one. Among lines with one slope, the highest is above the others for every $\gamma$, so dropping the others changes no maximum. Now the slopes are strictly increasing. For two lines with slopes $b_0 < b$, the second is above the first exactly for $\gamma > x = (a_0 - a)/(b - b_0)$, the value of line U5.

Invariant: after each step of line U3, the stack holds the envelope of the lines read so far, as a list of lines with strictly increasing start points, each line highest from its start to the next start. This holds for one line, with start $-\infty$. Add a line $\ell$ with a larger slope than all lines on the stack. For large $\gamma$, $\ell$ is the highest, because its slope is the largest. Let the top line $\ell_0$ start at $s_0$. If $\ell$ passes $\ell_0$ at $x \le s_0$, then $\ell$ is above $\ell_0$ on all of $\ell_0$'s interval, and $\ell_0$ is no longer on the envelope: line U6 pops it. The interval of the line below now extends to the right, and the same test repeats. If $x > s_0$, then $\ell_0$ is highest on $(s_0, x)$, and $\ell$ is highest from $x$ on, because $\ell$ is above $\ell_0$ there and $\ell_0$ was above the lines below it from $s_0$ on. Line U7 pushes $\ell$ with start $x$. If the stack becomes empty, $\ell$ is above every earlier line everywhere and starts at $-\infty$. $\square$

So for each sentence, $\hat c_i(w + \gamma d)$ is constant on each open interval between its breakpoints $g_q$ (the tie rule matters only at the breakpoints and between parallel lines; parallel lines with equal intercepts are equal everywhere, and line U1 keeps the one that the tie rule picks).

**Lemma 2 (the sweep).** Let $G$ be the sorted set of all breakpoints of all sentences. On each open interval between two consecutive points of $G$, and on the two unbounded intervals, $F$ is constant. When the loop of line L9 has handled all events at a point $g \in G$, the running total equals $\sum_i \phi_{i, \hat c_i(\gamma)}$ for $\gamma$ in the interval that starts at $g$.

*Proof.* On an interval with no breakpoint, no sentence changes its choice, so the sum and $F$ are constant. At the start (line L5), the total is the sum of the statistics of the first envelope line of each sentence, which is the choice for $\gamma$ below every breakpoint. At a breakpoint $g_q$ of sentence $i$, the choice of $i$ changes from $c_{q-1}$ to $c_q$, and the event of line L6 holds $\phi_{i,c_q} - \phi_{i,c_{q-1}}$. Line L9 adds all events at one point together, so after them the total matches the choices just right of $g$. By induction over the sorted points, the claim holds. $\square$

**Theorem.** LINE-SEARCH returns $(\gamma^*, v)$ with $v = \max_{\gamma \notin G} F(\gamma)$ and $F(\gamma^*) = v$. That is, it finds the exact maximum of $F$ over all $\gamma$ that are not breakpoints.

*Proof.* By Lemma 2, $F$ takes finitely many values on the intervals between the points of $G$, and the loop evaluates $\mu$ on each of them once: line L8 on the leftmost interval and line L9 after each point. It keeps the largest value and a $\gamma$ inside its interval: one less than the first point for the leftmost interval, one more than the last point for the rightmost, and the midpoint otherwise. A midpoint is not a breakpoint, so $F(\gamma^*)$ is that interval's value. If $G$ is empty, $F$ is constant and $\gamma^* = 0$. $\square$

At a breakpoint itself $F$ can take another value, which depends on the tie rule; such a value is not robust to any small change of the weights, so the search ignores it.

**MERT as a whole.** Each accepted line search raises $M$ strictly, and $M$ takes finitely many values (one per choice of a candidate in each list), so coordinate ascent stops after finitely many accepted steps. It stops at a point where no line search along the given directions improves $M$. This is not a global maximum of $M$ over $\mathbb{R}^D$: $M$ is piecewise constant and not concave, and coordinate ascent can stop at a point that only the search along another direction could leave. This is a heuristic.

**Cost.** For sentence $i$ with $n_i$ candidates, line L3 costs $O(n_i D)$ and the envelope $O(n_i \log n_i)$ for the sort. There are at most $N = \sum_i n_i$ events, sorted in $O(N \log N)$, and each costs one addition of statistics and one evaluation of $\mu$. With statistics of constant size, a line search costs $O(N (D + \log N))$.
