---
title: Split conformal intervals have coverage between 1 - alpha and 1 - alpha + 1/(n_2 + 1)
proves: [correctness]
status: full
---

We use the pseudocode of the page. $Z_1, \ldots, Z_n, Z_{n+1}$ with $Z_i = (X_i, Y_i)$ are the data and the new point. The split of line L1 is independent of the data. $I_1$ has $n_1$ indices and $I_2$ has $n_2 = n - n_1$. Write $k = \lceil (n_2 + 1)(1 - \alpha) \rceil$, $R_i = \lvert Y_i - \hat\mu(X_i) \rvert$ for $i \in I_2 \cup \{n + 1\}$, and $R^{\mathrm{cal}}_{(1)} \le \cdots \le R^{\mathrm{cal}}_{(n_2)}$ for the sorted calibration scores.

This file proves the coverage bounds for every law and every fitting procedure, under exchangeability. Nothing about the width of the interval or about coverage at a fixed $x$ is proved; the page only measures those.

**Claim 1 (the event of coverage).** If $k \le n_2$, then $Y_{n+1} \in [\hat\mu(X_{n+1}) - q, \hat\mu(X_{n+1}) + q]$ if and only if $S \le k - 1$, where $S = \#\{i \in I_2 : R_i < R_{n+1}\}$. If $k > n_2$, the new point is always covered.

*Proof.* If $k > n_2$, line L5 sets $q = \infty$. Otherwise line L6 sets $q = R^{\mathrm{cal}}_{(k)}$, and the new point is covered exactly when $R_{n+1} \le R^{\mathrm{cal}}_{(k)}$. If $R_{n+1} \le R^{\mathrm{cal}}_{(k)}$, every calibration score below $R_{n+1}$ is below $R^{\mathrm{cal}}_{(k)}$, so it is one of $R^{\mathrm{cal}}_{(1)}, \ldots, R^{\mathrm{cal}}_{(k-1)}$, and $S \le k - 1$. If $R_{n+1} > R^{\mathrm{cal}}_{(k)}$, then $R^{\mathrm{cal}}_{(1)}, \ldots, R^{\mathrm{cal}}_{(k)}$ are all below $R_{n+1}$ and $S \ge k$. $\square$

**Claim 2 (the scores are exchangeable given the training part).** Conditional on the split and on $(Z_i)_{i \in I_1}$, the $n_2 + 1$ scores $(R_i)_{i \in I_2 \cup \{n+1\}}$ are exchangeable.

*Proof.* The split does not depend on the data, so conditional on it, $(Z_i)_{i \in I_1}$ followed by $(Z_i)_{i \in I_2 \cup \{n+1\}}$ is still an exchangeable sequence. Permuting the last $n_2 + 1$ points therefore does not change the joint law, and hence does not change their conditional law given the first block. Given the training block, $\hat\mu$ is a fixed function, and each score is the same fixed function $z \mapsto \lvert y - \hat\mu(x) \rvert$ of its own point. A fixed function applied to each member of an exchangeable vector gives an exchangeable vector. $\square$

**Claim 3 (lower bound).** $P\bigl(Y_{n+1} \in C(X_{n+1})\bigr) \ge k/(n_2 + 1) \ge 1 - \alpha$ when $k \le n_2$, and the coverage is 1 when $k > n_2$.

*Proof.* Work conditionally on the split and the training block, and index the $n_2 + 1$ scores by $j$. Let $S_j$ be the number of the other $n_2$ scores that are strictly smaller than $R_j$; then $S = S_{n+1}$. Let $T_{(1)} \le \cdots \le T_{(n_2 + 1)}$ be all $n_2 + 1$ scores sorted. If $S_j \ge k$, then at least $k$ scores are strictly below $R_j$, so $R_j > T_{(k)}$. At most $n_2 + 1 - k$ indices have a score strictly above $T_{(k)}$. So at most $n_2 + 1 - k$ indices have $S_j \ge k$, and at least $k$ have $S_j \le k - 1$. Permuting the scores permutes the $S_j$ in the same way, and the scores are exchangeable (Claim 2), so the vector $(S_j)$ is exchangeable and $P(S_j \le k - 1)$ is the same for every $j$. Hence

$$P(S_{n+1} \le k - 1) = \frac{1}{n_2 + 1} E\,\#\{j : S_j \le k - 1\} \ge \frac{k}{n_2 + 1}.$$

By Claim 1 this is the conditional coverage, and averaging over the training block keeps the bound. Finally $k \ge (n_2 + 1)(1 - \alpha)$ by the definition of the ceiling. The case $k > n_2$ is Claim 1. $\square$

**Claim 4 (upper bound for distinct scores).** If the $n_2 + 1$ scores are almost surely distinct, for example when $Y$ given $X$ has a continuous law, then for $k \le n_2$

$$P\bigl(Y_{n+1} \in C(X_{n+1})\bigr) = \frac{k}{n_2 + 1} < 1 - \alpha + \frac{1}{n_2 + 1}.$$

*Proof.* With distinct scores, $S_j$ is the rank of $R_j$ minus one, the $S_j$ are $0, 1, \ldots, n_2$ in some order, and exactly $k$ indices have $S_j \le k - 1$. The display in Claim 3 is then an equality. The ceiling gives $k < (n_2 + 1)(1 - \alpha) + 1$; divide by $n_2 + 1$. $\square$

With an even split, $n_2 = n/2$, the slack is $1/(n/2 + 1) = 2/(n + 2)$, the bound of Lei et al. (2018, Theorem 2.2). If ties have positive probability, the upper bound can fail; with constant scores the coverage is 1.

**Claim 5 (coverage given the calibration set).** Suppose the points are iid and, given the training block, the score $R$ of a new point has a continuous distribution function $F$. Then the coverage conditional on the training and calibration blocks is $F(q)$, and for $k \le n_2$ it has the Beta law with parameters $k$ and $n_2 + 1 - k$.

*Proof.* Given both blocks, $q$ is fixed and the new point is independent of them, so the conditional coverage is $P(R_{n+1} \le q) = F(q)$. The calibration scores are iid with the continuous distribution function $F$, so $U_i = F(R_i)$ are iid uniform on $[0, 1]$, and $F$ is nondecreasing, so $F(R^{\mathrm{cal}}_{(k)}) = U_{(k)}$, the $k$-th order statistic of $n_2$ uniforms, whose law is Beta$(k, n_2 + 1 - k)$. Its mean is $k/(n_2 + 1)$, which agrees with Claim 4. $\square$

**Claim 6 (cost).** Lines L1 and L3 to L5 take $O(n)$ time besides the $n_2$ predictions, line L2 is one fit, and line L6 takes $O(n_2 \log n_2)$ time by sorting or $O(n_2)$ by linear-time selection. The space is $O(n)$ besides the model.

*Proof.* Line L1 is a shuffle of $n$ indices. Line L3 makes one prediction and one subtraction for each calibration point. Line L4 is arithmetic. Selection of the $k$-th smallest of $n_2$ numbers takes linear time by the median of medians method, or the sort can be used. $\square$

**What the tests check.** The test file fixes a training block and enumerates all $6! = 720$ orderings of five calibration points and one new point. With distinct scores the coverage is exactly $k/6$ for each $\alpha$ tested (Claims 3 and 4), and with tied scores it is at least $1 - \alpha$ (Claim 3). It also checks the identity $1/(n/2 + 1) = 2/(n + 2)$ and the inequalities $1 - \alpha \le k/(n_2 + 1) < 1 - \alpha + 1/(n_2 + 1)$ for all $n_2 < 60$.
