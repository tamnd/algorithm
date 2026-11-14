---
title: PlaceRow finds the exact least squared movement of a row with a fixed order, and Abacus returns a legal placement
proves: [correctness, termination, running time]
status: full
---

Fix one row $[a, b]$ and its cells $1, \ldots, k$ in the given order, with integer widths $W_i \ge 1$, weights $e_i > 0$, targets $x'_i$, and $\sum_i W_i \le b - a$. Write $\omega_i = \sum_{l < i} W_l$ for the width of the cells before $i$ (so $\omega_1 = 0$), and

$$ t_i = x'_i - \omega_i, \qquad B_j = b - \omega_{j+1} \quad (1 \le j \le k). $$

Then $B_1 > B_2 > \cdots > B_k = b - \sum_i W_i \ge a$, because each $W_i \ge 1$. For a set $\beta$ of consecutive cells, write $E_\beta = \sum_{i \in \beta} e_i$, $m_\beta = \sum_{i \in \beta} e_i t_i / E_\beta$ (the weighted mean of $t$ on $\beta$) and $f_\beta(v) = \sum_{i \in \beta} e_i (t_i - v) = E_\beta (m_\beta - v)$. If $\beta$ is split into a prefix $\pi$ and a suffix $\sigma$, then $f_\beta = f_\pi + f_\sigma$.

**Lemma 1 (the substitution).** Let $R_j$ be the problem: minimize $\sum_{i \le j} e_i (u_i - t_i)^2$ subject to $a \le u_1 \le u_2 \le \cdots \le u_j \le B_j$. The map $u_i = x_i - \omega_i$ is a bijection from the positions $x$ of cells $1, \ldots, j$ with $x_1 \ge a$, $x_i + W_i \le x_{i+1}$ and $x_j + W_j \le b$, onto the feasible set of $R_j$, and it keeps the objective $\sum e_i (x_i - x'_i)^2$.

*Proof.* $x_i + W_i \le x_{i+1}$ is $u_i + \omega_i + W_i \le u_{i+1} + \omega_{i+1}$, and $\omega_{i+1} = \omega_i + W_i$, so it is $u_i \le u_{i+1}$. $x_1 \ge a$ is $u_1 \ge a$. $x_j + W_j \le b$ is $u_j \le b - \omega_{j+1} = B_j$. Finally $x_i - x'_i = u_i - t_i$. $\square$

**Lemma 2 (clusters in the new coordinates).** Let $c$ be a cluster of the cells $l, \ldots, r$ in PlaceRow. Then $W_c = \omega_{r+1} - \omega_l$, $q_c = E_c (m_c + \omega_l)$, and with $u_c = x_c - \omega_l$ (the common value of $u$ on the cluster):

1. line L14 sets $u_c = m_c$;
2. line L15 clamps $u_c$ to $[a - \omega_l, B_r]$;
3. the test of line L16 for the cluster $c'$ just before $c$ is $u_{c'} > u_c$.

*Proof.* The offset of cell $i$ in the cluster is $\omega_i - \omega_l$. Line L12 adds cell $j = r$ with the offset $W_c = \omega_j - \omega_l$, and line L18 adds to each cell of $c$ the offset $W_{c'}$, the width before it. By induction on these two lines, $q_c = \sum_{i=l}^{r} e_i (x'_i - \omega_i + \omega_l) = \sum e_i (t_i + \omega_l) = E_c (m_c + \omega_l)$. So $q_c / e_c - \omega_l = m_c$. The clamp $x_c \ge a$ is $u_c \ge a - \omega_l$, and $x_c \le b - W_c$ is $u_c \le b - \omega_{r+1} = B_r$. If $c'$ has the cells $l', \ldots, l - 1$, then $x_{c'} + W_{c'} = u_{c'} + \omega_{l'} + (\omega_l - \omega_{l'}) = u_{c'} + \omega_l$, which is more than $x_c = u_c + \omega_l$ exactly when $u_{c'} > u_c$. $\square$

**The plain run.** In the plain run, cell $j$ always starts a new cluster $\{j\}$. The current (last) cluster $\gamma$ gets the value $u_\gamma = \min(\max(m_\gamma, a), B_j)$ if it is the first cluster of the row, and $u_\gamma = \min(m_\gamma, B_j)$ otherwise. While a cluster $\beta$ comes just before $\gamma$ with $u_\beta > u_\gamma$, the two merge into the current cluster $\beta\gamma$, which gets its value in the same way.

**Lemma 3.** PlaceRow (lines L10 to L18) makes the same clusters with the same values as the plain run.

*Proof.* By induction on the steps. All stored values are at least $a$: the first cluster is clamped to $a$ from below, and every other cluster stays only if its value is at least that of the cluster before it. Two things differ. (i) Line L11 adds $j$ to the last cluster $c$ when $u_c > t_j$ (Lemma 2 with $x'_j = t_j + \omega_j$). In the plain run, $\{j\}$ gets a value at most $t_j < u_c$, so it merges with $c$ at once, and line L18 for the one-cell cluster with $q = e_j x'_j$ makes the same change as line L12. Both then collapse the merged cluster. (ii) A cluster $\gamma$ that is not the first is clamped from below to $a - \omega_l$ by line L15, and not in the plain run. If $m_\gamma \ge a - \omega_l$, the clamp does nothing. If $m_\gamma < a - \omega_l$, PlaceRow gives $u_\gamma = a - \omega_l < a$ and the plain run gives $u_\gamma \le m_\gamma < a$. Both are less than the value of the cluster before it, which is at least $a$, so both runs merge, and the merged value is computed again from $q$ and $e$. $\square$

**Good blocks.** Call a block $\beta$ *balanced* if every proper prefix $\pi$ has $m_\pi \ge m_\beta$. Because $f_\pi(m_\beta) + f_\sigma(m_\beta) = f_\beta(m_\beta) = 0$ for the complementary suffix $\sigma$, this is the same as: every proper suffix has $m_\sigma \le m_\beta$. Call $\beta$ *high at* $v$ if every proper prefix has $m_\pi \ge v$, and *low at* $v$ if every proper suffix has $m_\sigma \le v$. A block of one cell is all of these. A balanced block is high at every $v \le m_\beta$ and low at every $v \ge m_\beta$.

**Invariant (J) after cell $j$.** The clusters $\beta_1, \ldots, \beta_s$ have values $v_1 \le v_2 \le \cdots \le v_s$, with $a \le v_1$ and $v_s \le B_j$, and each $\beta_k$ is in one of three states:

- *free*: $v_k = m_{\beta_k}$ and $\beta_k$ is balanced;
- *low*: $k = 1$, $v_1 = a > m_{\beta_1}$, and $\beta_1$ is low at $a$;
- *high*: $k = s$, $v_s = B_j < m_{\beta_s}$, and $\beta_s$ is high at $B_j$.

**Lemma 4 (optimality).** If (J) holds after cell $j$, the values of the clusters, copied to their cells, are the unique minimum of $R_j$.

*Proof.* Let $u_i = v_k$ for $i \in \beta_k$. It is feasible by (J). If $a = B_j$, the feasible set is the single point $u = a$, and we are done. Let $a < B_j$, so no cluster is both low and high. The objective is strictly convex because every $e_i > 0$, and the constraints are linear, so a feasible point that meets the KKT conditions is the unique minimum (see [KKT conditions](/kkt-conditions/)). With half the objective, multipliers $\lambda_0 \ge 0$ for $a - u_1 \le 0$, $\lambda_i \ge 0$ for $u_i - u_{i+1} \le 0$ ($1 \le i < j$), and $\lambda_j \ge 0$ for $u_j - B_j \le 0$, the stationarity condition for $u_i$ is $e_i (u_i - t_i) + \lambda_i - \lambda_{i-1} = 0$. So set

$$ \lambda_0 = \begin{cases} -f_{\beta_1}(a) & \text{if } \beta_1 \text{ is low,} \\ 0 & \text{otherwise,} \end{cases} \qquad \lambda_i = \lambda_0 + \sum_{l \le i} e_l (t_l - u_l) \quad (1 \le i \le j). $$

Stationarity holds by construction. It remains to show that every $\lambda_i \ge 0$, with complementary slackness. Note $\lambda_0 \ge 0$, since a low block has $m_{\beta_1} < a$.

*At the end of a cluster.* The sum over a cluster $\beta_k$ is $f_{\beta_k}(v_k)$. It is 0 for a free cluster, $f_{\beta_1}(a)$ for the low cluster, and $f_{\beta_s}(B_j) > 0$ for the high cluster. So $\lambda_i = 0$ at the last cell of each $\beta_k$ with $k < s$: the low part cancels $\lambda_0$, and the high cluster can only be the last. At $i = j$, $\lambda_j = f_{\beta_s}(B_j) > 0$ if $\beta_s$ is high, and then $u_j = B_j$; otherwise $\lambda_j = 0$. Also $\lambda_0 > 0$ only if $\beta_1$ is low, and then $u_1 = a$. So slackness holds for the bounds and for the constraints between clusters.

*Inside a cluster* $\beta_k$ with the cells $l, \ldots, r$, for $l \le i < r$, let $\pi = \{l, \ldots, i\}$ and $\sigma = \{i + 1, \ldots, r\}$. Then $u_i = u_{i+1}$, so slackness holds, and $\lambda_i = \lambda_{l-1} + f_\pi(v_k)$, where $\lambda_{l-1} = 0$ for $k \ge 2$ and $\lambda_{l - 1} = \lambda_0$ for $k = 1$. If $\beta_k$ is free, $f_\pi(m_{\beta_k}) \ge 0$ since it is balanced, so $\lambda_i \ge 0$. If $\beta_k$ is high, $\lambda_{l-1} \ge 0$ and $f_\pi(B_j) \ge 0$ since $m_\pi \ge B_j$. If $\beta_k = \beta_1$ is low, $\lambda_i = -f_{\beta_1}(a) + f_\pi(a) = -f_\sigma(a) \ge 0$ since $m_\sigma \le a$. $\square$

**Lemma 5 (one step keeps (J)).** If (J) holds after cell $j - 1$ (or $j = 1$), it holds after cell $j$ in the plain run.

*Proof.* Write $B = B_j$, and $B' = B_{j-1} > B$ if $j \ge 2$. Note $a \le B$. During the collapse of step $j$ we keep this claim (K): the clusters before the current cluster $\gamma$ are in the states of (J) for $j - 1$ with the bound $B'$, a high cluster among them can only be the one just before $\gamma$, and then $\gamma = \{j\}$; the current cluster is either balanced with $u_\gamma = m_\gamma$, or high at $B$ with $u_\gamma = B < m_\gamma$, or (only if it is the first cluster) low at $a$ with $u_\gamma = a > m_\gamma$.

At the start $\gamma = \{j\}$ is one cell, so it is in the state that its value gives, and (K) holds. Now let $\beta$ be the cluster before $\gamma$ with $u_\beta > u_\gamma$, and let $m = m_{\beta\gamma}$, a weighted mean of $m_\beta$ and $m_\gamma$. The prefixes of $\beta\gamma$ are the proper prefixes of $\beta$, $\beta$ itself, and $\beta$ with a proper prefix of $\gamma$; the suffixes are similar.

1. *$\beta$ free and $\gamma$ balanced.* Then $m_\beta > m_\gamma$, so $m_\gamma < m < m_\beta$. A proper prefix $\pi$ of $\beta$ has $m_\pi \ge m_\beta > m$, and $m_\beta > m$. For $\pi = \beta \cup \gamma'$ with a proper prefix $\gamma'$ of $\gamma$, the rest is a proper suffix $\sigma$ of $\gamma$ with $m_\sigma \le m_\gamma < m$, so $f_\pi(m) = -f_\sigma(m) > 0$. So $\beta\gamma$ is balanced, and its new value puts it in the free, high or low state.
2. *$\beta$ free and $\gamma$ high.* Then $m_\beta = u_\beta > B$ and $m_\gamma > B$, so $m > B \ge a$ and the new value is $B$. A proper prefix of $\beta$ has mean at least $m_\beta > B$; $\beta$ has $m_\beta > B$; and $\beta \cup \gamma'$ has $f = f_\beta(B) + f_{\gamma'}(B) > 0$. So $\beta\gamma$ is high at $B$.
3. *$\beta$ low (so it is the first cluster, $u_\beta = a$).* Then $\gamma$ is not first and $u_\gamma = \min(m_\gamma, B) < a \le B$, so $u_\gamma = m_\gamma$ and $\gamma$ is balanced. Then $m < a$, and the new value of the first cluster $\beta\gamma$ is $a$. A proper suffix of $\gamma$ has mean at most $m_\gamma < a$; $\gamma$ has $m_\gamma < a$; and $\beta'' \cup \gamma$ for a proper suffix $\beta''$ of $\beta$ has $f = f_{\beta''}(a) + f_\gamma(a) < 0$. So $\beta\gamma$ is low at $a$.
4. *$\beta$ high at $B'$.* By (K), $\gamma = \{j\}$, with $t = t_j$, and $u_\beta = B' > B \ge u_\gamma$. Every proper prefix of $\beta$ has mean at least $B'$, and $m_\beta > B'$. Let $v$ be the new value. If $v \le m$, then $v \le B < B'$, so every proper prefix of $\beta\gamma$ (those of $\beta$, and $\beta$) has mean more than $v$: $\beta\gamma$ is high at $v$, which is the high state for $v = B < m$ and the balanced (free) state for $v = m$. If $v > m$, then $\beta\gamma$ is first and $v = a > m$. Since $m < a < m_\beta$, also $t < m < a$, so the suffix $\{j\}$ is fine. For $\sigma = \beta'' \cup \{j\}$ with a proper suffix $\beta''$ of $\beta$ and the rest $\beta'$ of $\beta$, $f_\sigma(a) = f_{\beta\gamma}(a) - f_{\beta'}(a) < 0$, because $f_{\beta\gamma}(a) = E (m - a) < 0$ and $m_{\beta'} \ge B' > a$. So $\beta\gamma$ is low at $a$.

The case $\beta$ low and $\gamma$ high would need $a = u_\beta > u_\gamma = B$, which is false, and the case $\beta$ high with $\gamma \ne \{j\}$ is excluded by (K). So (K) holds after each merge. When the collapse stops, either $\gamma$ is first or $u_\beta \le u_\gamma$ for the cluster $\beta$ before it. A high cluster at $B'$ cannot be before $\gamma$, since $B' > B \ge u_\gamma$ would force a merge. So the earlier clusters are free or low, and their conditions do not depend on the bound. Their values are ordered, the last of them is at most $u_\gamma \le B$, and the first is at least $a$. If $\gamma$ is not first, $u_\gamma \ge u_\beta \ge a$, so $\gamma$ is free or high. This is (J) after cell $j$. $\square$

**Theorem 1 (PlaceRow is exact).** For the cells of a row in a fixed order with $\sum W_i \le b - a$, PlaceRow returns the unique positions with $a \le x_1$, $x_i + W_i \le x_{i+1}$ and $x_k + W_k \le b$ that minimize $\sum e_i (x_i - x'_i)^2$.

*Proof.* By Lemmas 3 and 5, (J) holds after cell $k$. By Lemma 4 the values solve $R_k$ uniquely, and by Lemmas 1 and 2 the cluster positions $x_c = u_c + \omega_l$ give the cells the positions $x_i = u_i + \omega_i$, the unique minimum of the row problem. $\blacksquare$

**Theorem 2 (legal output).** If Abacus does not stop with failure, line L9 returns a legal placement, and each cell is within $\frac12$ of its position in the exact row minimum.

*Proof.* Line L5 keeps the total width of each row at most $S$, so Theorem 1 applies with $[a, b] = [0, S]$. The clusters of the minimum satisfy $x_c + W_c \le x_{c+1}$, $x_1 \ge 0$ and $x_{\text{last}} + W_{\text{last}} \le S$. Let $R(x) = \lfloor x + \frac12 \rfloor$. It is nondecreasing, $R(n) = n$ and $R(x + n) = R(x) + n$ for every integer $n$. So $R(x_c) + W_c = R(x_c + W_c) \le R(x_{c+1})$, $R(x_1) \ge R(0) = 0$, and $R(x_{\text{last}}) + W_{\text{last}} = R(x_{\text{last}} + W_{\text{last}}) \le R(S) = S$. The cells of a cluster are put side by side from the integer $R(x_c)$, so they lie on sites, they do not overlap each other, and they do not overlap the next cluster. Each cell moves by $|R(x_c) - x_c| \le \frac12$. $\blacksquare$

**Theorem 3 (failure and the stop of line L4).** Abacus stops with failure only if cell $i$ is wider than the free width of every row. The stop of line L4 does not change the chosen row.

*Proof.* A row with room for cell $i$ passes line L5, gets a trial and a cost, so the failure of line L8 happens only when every row failed line L5. Rows are tried in order of $(y_r - y'_i)^2$, and the cost of row $r$ is at least $(y_r - y'_i)^2$. When this is at least the best cost so far, every later row also has a cost at least the best, and line L8 takes a strictly smaller cost or the earlier row on a tie, so no later row would be chosen. $\square$

**Theorem 4 (running time).** PlaceRow on $k$ cells makes at most $k$ clusters and at most $k - 1$ merges, so it runs in $O(k)$ time when a cluster stores its first and last cell. Abacus runs in $O(n \log n + K n k)$ time, where $k$ is the largest number of cells of a row.

*Proof.* Each step of the loop L10 starts at most one cluster, and each merge of line L17 removes one, so the number of merges is at most the number of clusters made, at most $k$. Each call of COLLAPSE does $O(1)$ work besides a merge, and there is one call per step plus one per merge. Lines L12 and L18 cost $O(1)$ when a cluster keeps its totals and the range of its cells (the cells of a cluster are consecutive in the order of the row). Line L9 then writes $k$ positions. The sort of line L1 costs $O(n \log n)$; each of the $n$ cells makes at most $K$ trials, each one PlaceRow on at most $k$ cells, and line L9 costs $O(n)$ over all rows. $\blacksquare$
