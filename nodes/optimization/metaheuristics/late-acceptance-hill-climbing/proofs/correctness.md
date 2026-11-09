---
title: Late acceptance never lets the cost rise above the worst of the last L costs
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The objective $f$ is to be minimized, $L \ge 1$ is the length of the history list $C$, and $K \ge 0$ is the number of iterations. Write $c_0 = f(x_0)$, and $c_{I+1}$ for the cost $f(x)$ of the current solution at the end of iteration $I$, for $I = 0, \ldots, K - 1$. Write $y_I$ for the candidate of iteration $I$.

**Lemma 1 (termination).** The algorithm stops after exactly $K$ iterations, each with one candidate and one evaluation of $f$.

*Proof.* Line L3 is a loop of $K$ passes, and no line leaves it early. $\square$

**Lemma 2 (the history list).** At the start of iteration $I$, the slot $v = I \bmod L$ holds $C[v] = c_{I + 1 - L}$ if $I \ge L$, and $C[v] = c_0$ if $I < L$. In words: $C[v]$ is the current cost from $L$ iterations earlier, or the start cost while fewer than $L$ iterations have passed.

*Proof.* Line L2 sets every slot to $c_0$. Line L7 of iteration $J$ writes $c_{J+1}$ into slot $J \bmod L$, and no other line writes to $C$. If $I < L$, no earlier iteration $J < I$ has $J \bmod L = I \bmod L$, so the slot still holds $c_0$. If $I \ge L$, the last earlier iteration with the same slot is $J = I - L$, so the slot holds $c_{I - L + 1}$. $\square$

**Lemma 3 (one step).** For each $I$, $c_{I+1} \le \max(c_I, C[v])$, where $C[v]$ is the value of Lemma 2.

*Proof.* If line L6 rejects $y_I$, then $c_{I+1} = c_I$. If it accepts, then $f(y_I) \le C[v]$ or $f(y_I) \le c_I$, and $c_{I+1} = f(y_I)$. $\square$

**Theorem 1 (the window maximum never rises).** Let $M_I = \max(c_{I - L + 1}, \ldots, c_I)$, where indices below 0 are read as 0. Then $M_{I+1} \le M_I$ for every $I$. In particular $c_I \le c_0$ for all $I$: the current solution is never worse than the start.

*Proof.* By Lemmas 2 and 3, $c_{I+1} \le \max(c_I, c_{\max(0, I + 1 - L)})$. Both $c_I$ and $c_{\max(0, I+1-L)}$ lie in the window of $M_I$, so $c_{I+1} \le M_I$. The window of $M_{I+1}$ is the window of $M_I$ without its oldest entry, plus $c_{I+1}$. Every entry of it is at most $M_I$, so $M_{I+1} \le M_I$. Since $M_0 = c_0$, every $c_I \le M_I \le c_0$. $\square$

**Corollary (the case $L = 1$).** With $L = 1$, the slot $C[0]$ holds $c_I$ at the start of iteration $I$, so line L6 accepts exactly when $f(y_I) \le c_I$. The algorithm is then a randomized hill climber that accepts equal moves, and $c_{I+1} \le c_I$ for every $I$.

**Theorem 2 (correctness).** The algorithm returns $b$ with $f(b) = \min(c_0, c_1, \ldots, c_K)$, the best current cost seen, and $f(b) \le f(x_0)$.

*Proof.* Line L1 sets $b = x_0$. Line L8 replaces $b$ by $x$ exactly when $f(x) < f(b)$, so after iteration $I$, $f(b) = \min(c_0, \ldots, c_{I+1})$ by induction. Termination is Lemma 1. $\blacksquare$

**What is not claimed.** Nothing here says that $b$ is a global minimum, or a local minimum: the candidates are random, and the run ends after $K$ iterations whether or not the current solution can still improve. Theorem 1 shows only that the search drifts downhill in the sense of the window maximum. It can move from a solution to a worse one when the worse cost is at most the cost of $L$ iterations ago.
