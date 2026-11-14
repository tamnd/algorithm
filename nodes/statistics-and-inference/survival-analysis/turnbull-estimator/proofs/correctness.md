---
title: The innermost intervals carry a maximizer, the Kuhn-Tucker gap certifies the fit, and the self-consistency iteration increases the likelihood with a gap below n log m over k
proves: [correctness]
status: full
---

Let the observations be $I_i = (L_i, R_i]$ for $L_i < R_i$ and $I_i = \{L_i\}$ for $L_i = R_i$, $i = 1, \ldots, n$, with $R_i = \infty$ allowed.

## The innermost intervals

**Keys.** Give each endpoint a key: $(L_i, 0)$ for the left end of an exact time, $(R_i, 1)$ for a right end, $(L_i, 2)$ for any other left end; and give each real point $x$ the key $\kappa(x) = (x, \tfrac12)$. Keys are compared lexicographically, which is the order of line L1. Then

$$x \in I_i \iff \mathrm{key}(L_i) < \kappa(x) < \mathrm{key}(R_i).$$

For $L_i < R_i$: $(L_i, 2) < (x, \tfrac12)$ holds exactly when $L_i < x$, and $(x, \tfrac12) < (R_i, 1)$ exactly when $x \le R_i$. For $L_i = R_i = y$: $(y, 0) < (x, \tfrac12) < (y, 1)$ holds exactly when $x = y$. So every observation is the set of points whose keys lie strictly between its two endpoint keys, and the problem becomes one about intervals on a line of keys. No left key equals a right key, since their second components differ.

A pair of positions $k, k + 1$ in the sorted list with a left end at $k$ and a right end at $k + 1$ defines $Q = \{x : \mathrm{key}_k < \kappa(x) < \mathrm{key}_{k+1}\}$. If the left end is open with value $p$ and the right end has value $q$, this is $(p, q]$, nonempty because a right end with value $p$ sorts before $(p, 2)$, so $q > p$. If the left end is the exact time $p$, its own right end $(p, 1)$ is the first right key after $(p, 0)$, so $q = p$ and $Q = \{p\}$. These are the regions of line L2.

**Lemma 1 (each region is inside or outside each observation).** For every region $Q_j$ and every $i$, either $Q_j \subseteq I_i$ or $Q_j \cap I_i = \emptyset$, and $Q_j \subseteq I_i$ if and only if $\mathrm{key}(L_i) \le \mathrm{key}_k$ and $\mathrm{key}_{k+1} \le \mathrm{key}(R_i)$. The regions are pairwise disjoint, and $m \le n$.

*Proof.* No endpoint key lies strictly between $\mathrm{key}_k$ and $\mathrm{key}_{k+1}$, since they are adjacent. So each of $\mathrm{key}(L_i) < \mathrm{key}(R_i)$ is at most $\mathrm{key}_k$ or at least $\mathrm{key}_{k+1}$. If both are at most $\mathrm{key}_k$ or both at least $\mathrm{key}_{k+1}$, then $I_i$ and $Q_j$ are disjoint; otherwise $\mathrm{key}(L_i) \le \mathrm{key}_k$ and $\mathrm{key}_{k+1} \le \mathrm{key}(R_i)$, and $Q_j \subseteq I_i$. This is the test of the function `contains`. Two pairs cannot share a position, since position $k + 1$ of one pair holds a right end and cannot be the left end of another, so the key ranges and hence the regions are disjoint. Each pair uses a different left end, so $m \le n$. $\square$

**Lemma 2 (every point is dominated by a region).** For a point $x$ let $\Sigma(x) = \{i : x \in I_i\}$, and for a region let $\Sigma(Q_j) = \{i : Q_j \subseteq I_i\}$. For every $x$ there is a $j$ with $\Sigma(Q_j) \supseteq \Sigma(x)$. In particular every observation contains a region.

*Proof.* If $\Sigma(x)$ is empty, any $j$ works. Otherwise let $A$ be the largest left key and $B$ the smallest right key among the observations in $\Sigma(x)$. Then $A < \kappa(x) < B$, so $A$ comes before $B$ in the sorted list. The stretch of the list from $A$ to $B$ starts with a left end and ends with a right end, so somewhere in it a left end is directly followed by a right end. That pair gives a region $Q_j$ with $A \le \mathrm{key}_k < \mathrm{key}_{k+1} \le B$, and by Lemma 1, $Q_j \subseteq I_i$ for every $i \in \Sigma(x)$. For the last statement take any $x \in I_i$; then $i \in \Sigma(x)$, so the region found lies in $I_i$. $\square$

**Claim 1 (reduction to the regions).** For every distribution $F$ of $T$ there are masses $s \in \Delta_m$ with $D_i(s) \ge P_F(T \in I_i)$ for all $i$, where $D_i(s) = \sum_j \alpha_{ij} s_j$. Every distribution that gives mass $s_j$ to $Q_j$ has $P(T \in I_i) = D_i(s)$, however it spreads the mass inside each $Q_j$. Hence $\sup_F \mathcal L(F) = \max_{s \in \Delta_m} \prod_i D_i(s)$, and a maximizing $s$ gives the NPMLE.

*Proof.* The sets $\Sigma(x)$ change only at endpoints, so the line splits into finitely many intervals on which $\Sigma$ is constant. Choose for each $x$ the smallest $j(x)$ given by Lemma 2; it is constant on those intervals, so $x \mapsto j(x)$ is measurable. Let $s_j = P_F(j(T) = j)$. If $x \in I_i$ and $j(x) = j$ then $i \in \Sigma(x) \subseteq \Sigma(Q_j)$, so $\alpha_{ij} = 1$, and

$$P_F(T \in I_i) = \sum_j P_F(T \in I_i,\ j(T) = j) \le \sum_j \alpha_{ij} s_j = D_i(s).$$

The second statement follows from Lemma 1: each $Q_j$ lies entirely inside or outside $I_i$. $\square$

The maximum exists: $\ell(s) = \sum_i \log D_i(s)$ is continuous from the compact simplex to $[-\infty, \infty)$, and it is finite at the uniform point because every observation contains a region, so $D_i \ge 1/m$.

## Optimality and the certificate

For $s$ with every $D_i(s) > 0$, $\partial \ell/\partial s_j = \sum_i \alpha_{ij}/D_i(s) = n\, g_j(s)$, and

$$\sum_j s_j\, g_j(s) = \frac1n \sum_i \frac{\sum_j \alpha_{ij} s_j}{D_i(s)} = 1. \tag{1}$$

**Claim 2 (certificate).** For every such $s$ and every $s' \in \Delta_m$, $\ell(s') \le \ell(s) + n(\max_j g_j(s) - 1)$.

*Proof.* $\ell$ is concave, a sum of logarithms of linear functions, so it lies below its tangent plane: $\ell(s') \le \ell(s) + \sum_j n g_j(s)(s'_j - s_j) = \ell(s) + n(\sum_j s'_j g_j(s) - 1)$ by (1), and $\sum_j s'_j g_j(s) \le \max_j g_j(s)$ because $s'$ is a probability vector. $\square$

So when line L8 exits, the returned $\ell$ is within $n\varepsilon$ of the maximum.

**Claim 3 (Kuhn-Tucker conditions).** $\hat s$ maximizes $\ell$ over $\Delta_m$ if and only if $g_j(\hat s) \le 1$ for every $j$. Then $g_j(\hat s) = 1$ wherever $\hat s_j > 0$.

*Proof.* If all $g_j(\hat s) \le 1$, Claim 2 gives $\ell(s') \le \ell(\hat s)$ for all $s'$. Conversely, if $g_j(\hat s) > 1$ for some $j$, the direction $e_j - \hat s$ stays in the simplex for small steps, and the derivative of $\ell$ along it is $n(g_j(\hat s) - \sum_l \hat s_l g_l(\hat s)) = n(g_j(\hat s) - 1) > 0$, so $\hat s$ is not a maximizer. When all $g_j \le 1$, (1) is a weighted average of the $g_j$ with weights $\hat s_j$ that equals 1, so every $g_j$ with $\hat s_j > 0$ equals 1. $\square$

**Claim 4 (uniqueness of the fitted probabilities).** All maximizers have the same vector $(D_1(\hat s), \ldots, D_n(\hat s))$.

*Proof.* If two maximizers $\hat s$ and $\tilde s$ had different vectors, their midpoint would satisfy $\ell(\tfrac12(\hat s + \tilde s)) = \sum_i \log \tfrac12(D_i(\hat s) + D_i(\tilde s)) > \sum_i \tfrac12(\log D_i(\hat s) + \log D_i(\tilde s)) = \max \ell$, by strict concavity of $\log$ on the coordinates where they differ. $\square$

## The iteration

Line L9 maps $s$ to $s'$ with $s'_j = s_j g_j(s)$. By (1), $s' \in \Delta_m$. Every region lies in the observation whose left end defines it, so $g_j(s) > 0$ whenever all $D_i(s) > 0$; from the uniform start every iterate has all $s_j > 0$ and all $D_i > 0$.

**Claim 5 (EM step).** $s'$ is one step of the EM algorithm for the complete data "the region that contains $T_i$".

*Proof.* Given $T_i \in I_i$ and masses $s$, the probability that $T_i \in Q_j$ is $\alpha_{ij} s_j/D_i(s)$. The E step gives the expected count $\mu_j = \sum_i \alpha_{ij} s_j/D_i(s) = n s_j g_j(s)$ in $Q_j$, and the M step, the multinomial MLE from these counts, is $\mu_j/n = s'_j$. $\square$

**Claim 6 (ascent).** $\ell(s') - \ell(s) \ge n\, \mathrm{KL}(s' \,\|\, s) \ge 0$, where $\mathrm{KL}(a \,\|\, b) = \sum_j a_j \log(a_j/b_j)$, with equality only if $s' = s$.

*Proof.* For each $i$ the weights $w_{ij} = \alpha_{ij} s_j/D_i(s)$ are non-negative and sum to 1 over $j$, and $D_i(s')/D_i(s) = \sum_j w_{ij}\, g_j(s)$. By Jensen's inequality for the concave $\log$,

$$\ell(s') - \ell(s) = \sum_i \log \sum_j w_{ij}\, g_j \ge \sum_i \sum_j w_{ij} \log g_j = \sum_j n s'_j \log g_j = n \sum_j s'_j \log \frac{s'_j}{s_j},$$

using $\sum_i w_{ij} = n s_j g_j = n s'_j$. Gibbs' inequality gives $\mathrm{KL} \ge 0$, with equality only for equal vectors. $\square$

**Claim 7 (rate).** Let $\hat s$ be a maximizer and $s^{(0)}$ the uniform start. Then $\ell(\hat s) - \ell(s^{(k)}) \le n \log m/(k + 1)$ for every $k \ge 0$.

*Proof.* Fix $s$ with all $s_j > 0$ and $D_i(s) > 0$, and let $s'$ be its update. For $j$ with $\hat s_j > 0$, Claim 3 gives $g_j(\hat s) = 1$, so $u_{ij} = \alpha_{ij}/(n D_i(\hat s))$ are weights summing to 1 over $i$, and $g_j(s) = \sum_i u_{ij}\, D_i(\hat s)/D_i(s)$. By Jensen's inequality, $\log g_j(s) \ge \sum_i u_{ij} \log(D_i(\hat s)/D_i(s))$. Multiplying by $\hat s_j$ and summing over $j$,

$$\sum_j \hat s_j \log g_j(s) \ge \sum_i \frac{\sum_j \alpha_{ij} \hat s_j}{n D_i(\hat s)} \log \frac{D_i(\hat s)}{D_i(s)} = \frac{\ell(\hat s) - \ell(s)}{n}.$$

The left side is $\sum_j \hat s_j \log(s'_j/s_j) = \mathrm{KL}(\hat s \,\|\, s) - \mathrm{KL}(\hat s \,\|\, s')$. Summing over the steps $s^{(0)}, \ldots, s^{(k)}$ telescopes:

$$\sum_{r=0}^{k} \big(\ell(\hat s) - \ell(s^{(r)})\big) \le n\big(\mathrm{KL}(\hat s \,\|\, s^{(0)}) - \mathrm{KL}(\hat s \,\|\, s^{(k+1)})\big) \le n\, \mathrm{KL}(\hat s \,\|\, s^{(0)}) \le n \log m,$$

since $\mathrm{KL}(\hat s \,\|\, \text{uniform}) = \log m - H(\hat s) \le \log m$. By Claim 6 the terms decrease in $r$, so the last one is at most the average, $n \log m/(k + 1)$. $\square$

**Claim 8 (the loop ends).** For every $\varepsilon > 0$, line L8 exits after finitely many iterations.

*Proof.* By Claim 7, $\ell(s^{(k)}) \to \max \ell$. Suppose $\max_j g_j(s^{(k)}) > 1 + \varepsilon$ for infinitely many $k$. Those iterates have a convergent subsequence in the compact simplex, with limit $\bar s$. Since $\ell$ is upper semicontinuous, $\ell(\bar s) \ge \lim \ell(s^{(k)}) = \max \ell$, so $\bar s$ is a maximizer and $D_i(\bar s) > 0$ for all $i$. The $g_j$ are continuous where all $D_i > 0$, so $\max_j g_j(\bar s) \ge 1 + \varepsilon$, which contradicts Claim 3. $\square$

The proved rate is sublinear, and the example on the algorithm page with a zero mass where $g_j = 1$ shows that the iteration can be that slow. The faster linear convergence seen in other examples is only measured.

**Special cases.** For exact and right-censored data the regions are the distinct event times and, when the largest time is censored, the interval beyond it; the maximizer of Claim 1 is then the Kaplan-Meier estimate, by the NPMLE theorem in the [Kaplan-Meier correctness proof](/kaplan-meier-estimator/). For current status data the maximizer is the isotonic regression of the indicators (Ayer et al. 1955).

## Cost

The sort in line L1 costs $O(n \log n)$, line L2 one pass over $2n$ keys, and line L3 $nm$ calls of `contains`, each $O(1)$. Lines L6 and L7 cost $O(\sum_i |\{j : \alpha_{ij} = 1\}|) = O(nm)$, and lines L8 and L9 cost $O(m)$, per iteration. By Lemma 1 the regions inside $I_i$ are those between two positions of the sorted list, a contiguous run $a_i..b_i$; with prefix sums $P_j = s_1 + \cdots + s_j$, $D_i = P_{b_i} - P_{a_i - 1}$, and $g$ is obtained by adding $1/D_i$ to a difference array at $a_i$ and subtracting it at $b_i + 1$, so an iteration costs $O(n + m)$.
