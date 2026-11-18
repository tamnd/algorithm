---
title: Wilber's guess and check gives the least weight subsequence in linear time
proves: [correctness, termination, time.worst]
status: full
---

**Claim.** Let $n \ge 1$ and let $w(i, j)$, for $0 \le i < j \le n$, be finite reals with

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \qquad \text{for all } i \le i' < j \le j',$$

the condition that Hirschberg and Larmore call concave (the quadrangle inequality of a Monge array). Then WILBER (lines W1 to W12) stops and returns $F[j] = F(j)$ for $j = 0, \ldots, n$, where $F(0) = 0$ and $F(j) = \min_{0 \le i < j} (F(i) + w(i, j))$, with $F[P[j]] + w(P[j], j) = F(j)$. It uses $O(n)$ evaluations of $w$.

**Setup.** Write $g_i(j) = F(i) + w(i, j)$ for $i < j$. The program keeps an array $G$ of values: final values $F(i)$ for $i \le c$ and guesses after $c$. For a set of targets $J$ and a set of candidates $I$, the call of SMAWK in lines W4 and W6 works on the array $M$ with a row for each $j \in J$ and a column for each $i \in I$, both in increasing order, with $M[j][i] = G[i] + w(i, j)$ if $i < j$ and $+\infty$ if $i \ge j$, and returns for each row the leftmost column of its minimum.

**Lemma 1 (a later candidate that wins keeps winning).** Let $i < i' < j \le j'$. If $g_{i'}(j) < g_i(j)$, then $g_{i'}(j') \le g_i(j')$. The same holds with any values $G$ in place of $F$.

*Proof.* The inequality with $F(i) + F(i')$ added to both sides gives $g_{i'}(j') - g_i(j') \le g_{i'}(j) - g_i(j) < 0$. Only the sum of a value of $i$ and a value of $i'$ is added, so any values work. $\square$

**Lemma 2 (the arrays are totally monotone).** For rows $j < j'$ and columns $i < i'$ of $M$, if $M[j][i] > M[j][i']$ then $M[j'][i] > M[j'][i']$. So SMAWK returns the leftmost minimum of each row with $O(|I| + |J|)$ evaluations (see [SMAWK](/smawk-algorithm/)).

*Proof.* From $M[j][i] > M[j][i']$, the entry $M[j][i']$ is finite, so $i < i' < j < j'$ and all four entries are finite. Then Lemma 1 with $G$ gives $M[j'][i] - M[j'][i'] \ge M[j][i] - M[j][i'] > 0$. (The infinite entries lie where the column is at least the row, so a row's finite entries form a prefix that grows with the row; this pattern keeps the strict condition.) The cost bound is the one of SMAWK: REDUCE keeps at most $|J|$ columns with $O(|I|)$ evaluations, the recursion is on half of the rows, and the interpolation reads each kept column $O(1)$ times per row, so $T(|J|, |I|) = O(|I|) + T(|J|/2, |J|) + O(|J|) = O(|I| + |J|)$. $\square$

**Invariant.** At the start of each pass of the loop of line W2:

- (W1) $0 \le r \le c \le n$, and $F[i] = G[i] = F(i)$ for $0 \le i \le c$;
- (W2) for every target $j$ with $c < j \le n$, $\min_{0 \le i \le c} g_i(j) = \min_{r \le i \le c} g_i(j)$: the candidates before $r$ can be ignored.

*Initialization.* Line W1 sets $c = r = 0$ and $F[0] = G[0] = 0 = F(0)$. (W2) holds because both sides are $g_0(j)$.

*Maintenance.* Let $p = \min(2c - r + 1, n)$ (line W3). Since $r \le c$, $p \ge c + 1$, and $p - c \le c - r + 1$.

*The guesses.* Line W4 runs SMAWK on the targets $c + 1, \ldots, p$ and the candidates $r, \ldots, c$. All candidates are below all targets, so all entries are finite and use final values. By Lemma 2 and (W2), line W5 sets $G[j] = N(j) := \min_{i \le c} g_i(j)$ for $c < j \le p$. For each such $j$,

$$F(j) = \min\bigl(N(j),\ \min_{c < i < j} g_i(j)\bigr). \tag{1}$$

*The check.* If $p \ge c + 2$, line W6 runs SMAWK on the targets $c + 2, \ldots, p$ and the candidates $c + 1, \ldots, p - 1$ with the guesses $G$. For a target $j$ the finite entries are the candidates $c + 1, \ldots, j - 1$, so it returns $H(j) = \min_{c < i < j} (G[i] + w(i, j))$ and a column where it is attained. Let $j_0$ be the least target with $H(j_0) < G[j_0]$ (line W7), or $j_0 = p + 1$ if there is none (and also if $p = c + 1$).

*Claim A: $F(j) = G[j]$ for $c < j < j_0$.* By induction on $j$. For $j = c + 1$, the inner minimum of (1) is empty, so $F(c+1) = N(c+1)$. For $c + 2 \le j < j_0$, the hypothesis gives $F(i) = G[i]$ for $c < i < j$, so the inner minimum of (1) is $H(j)$, and $H(j) \ge G[j] = N(j)$ because $j < j_0$. So $F(j) = N(j) = G[j]$.

*Claim B: if $j_0 \le p$, then $F(j_0) = H(j_0)$.* By Claim A all the values that $H(j_0)$ uses are final, so $H(j_0) = \min_{c < i < j_0} g_i(j_0)$, and by (1) $F(j_0) = \min(N(j_0), H(j_0)) = H(j_0)$, since $H(j_0) < N(j_0)$.

*No failure (lines W8 and W9).* Then $j_0 = p + 1$. By Claim A, setting $F[j] = G[j]$ for $c < j \le p$ and $c \leftarrow p$ keeps (W1). (W2) for the new $c = p$ and the same $r$: for $j > p$, the candidates $i \le c$ (old $c$) reduce to $r, \ldots, c$ by the old (W2), and the candidates $c < i \le p$ are all at least $r$. So (W2) holds.

*Failure (lines W10 and W11).* By Claims A and B, the values set for $c < j \le j_0$ are final, and $G[j_0]$ is set to $F(j_0)$, so (W1) holds for the new $c = j_0$; also the new $r = c + 1 \le j_0$. For (W2), let $i^*$ be the column that line W6 returned for $j_0$, so $c < i^* < j_0$ and $g_{i^*}(j_0) = H(j_0) < N(j_0) \le g_i(j_0)$ for every $i \le c$. By Lemma 1, $g_{i^*}(j) \le g_i(j)$ for every $j > j_0$ and every $i \le c$. So for $j > j_0$ the candidates $0, \ldots, c$ are never better than $i^*$, which lies in $c + 1, \ldots, j_0$, and (W2) holds with $r = c + 1$.

*Termination.* Each pass increases $c$: to $p \ge c + 1$, or to $j_0 \ge c + 2$. So the loop stops with $c = n$, and by (W1) $F[j] = F(j)$ for all $j$. The predecessor $P[j]$ is the column where the minimum was attained, so $F[P[j]] + w(P[j], j) = F(j)$.

**Cost.** By Lemma 2, a pass costs $O((c - r + 1) + (p - c)) = O(c - r + 1)$ evaluations, since $p - c \le c - r + 1$. In a pass without failure and with $p = 2c - r + 1$, $c$ grows by $c - r + 1$. In a pass with failure, $r$ grows from $r$ to $c + 1$, that is by $c - r + 1$. At most one pass has $p = n < 2c - r + 1$ and no failure, the last one, and it costs $O(n)$. Both $c$ and $r$ never decrease and stay at most $n$, and there are at most $n$ passes, so the total is $O(n + n + n) = O(n)$ evaluations. $\blacksquare$

**Why the weights must be finite.** If $w(i, j) = +\infty$ marks a line that is too long, then an infinite entry $M[j][i]$ with a finite $M[j][i']$ forces nothing on a later row where both entries are infinite, so the strict condition of Lemma 2 fails, and SMAWK can drop the column that holds the minimum. The test `test_infinite_weights_can_fail` finds such inputs. A large finite penalty that is a convex function of the width keeps the inequality and avoids the problem.
