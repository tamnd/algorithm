---
title: Maximum likelihood under the CFN model is hard to approximate
proves: [statement]
status: full
---

This is the proof of Roch (2006). It reduces maximum parsimony to maximum likelihood under the two-state CFN model, and it uses the hardness of approximating maximum parsimony as a black box.

**Setting.** A character is a map $\chi$ from the $n$ taxa to $\{0, 1\}$. An instance is a list $X = (\chi^1, \ldots, \chi^k)$ of characters. A tree $T$ has the taxa as leaves and no internal vertex of degree 2; $E = |E(T)| \le 2n - 3$. A parameter vector $p$ gives each edge a flip probability $p_e \in [0, \tfrac12]$. The CFN process draws the root state uniformly and flips the state along each edge $e$ with probability $p_e$, independently. Write $P[\chi \mid T, p]$ for the probability of the leaf states $\chi$, and

$$\tilde L(X \mid T, p) = -\sum_{i=1}^{k} \ln\bigl(2\, P[\chi^i \mid T, p]\bigr).$$

The 0 and 1 symmetry of the process gives $P[\chi] = P[\bar\chi]$, where $\bar\chi$ is the complement, and $\chi \ne \bar\chi$, so $2 P[\chi] = P[\chi] + P[\bar\chi] \le 1$ and every term of $\tilde L$ is nonnegative. The ML problem is to minimize $\tilde L(X \mid T, p)$ over $T$ and $p$; this is the same as maximizing the likelihood, since the factor 2 per character is a constant. An $\alpha$-approximation returns $(T, p)$ with $\tilde L(X \mid T, p) \le \alpha \cdot \min_{T', p'} \tilde L(X \mid T', p')$.

For a tree $T$, the parsimony score $l(\chi, T)$ is the least number of edges whose two ends get different labels, over all labelings of the internal vertices, and $l(X, T) = \sum_i l(\chi^i, T)$. The MP problem is to minimize $l(X, T)$ over $T$; write $l^*(X)$ for the minimum.

**Fact A (MP is hard to approximate).** There is a constant $c_0 > 0$ such that, unless P = NP, no polynomial-time algorithm returns for every instance $X$ a tree $T$ with $l(X, T) \le (1 + c_0)\, l^*(X)$.

This is Proposition 2 of Roch. Wareham (1993) gives a reduction from vertex cover on graphs of degree at most $B$ to MP such that a $(1 + c')$-approximation for MP gives a $(1 + 2Bc')$-approximation for that vertex cover problem. Clementi and Trevisan (1999) proved that for large enough $B$, vertex cover on graphs of degree at most $B$ has no $1.16$-approximation unless P = NP. Taking $c_0 < 0.16 / (2B)$ gives Fact A. We use these two results without proof.

We may assume that no character of $X$ is constant: a constant character has parsimony score 0 on every tree, so removing it changes neither the MP instance nor its approximations. Then $l(\chi^i, T) \ge 1$ for each $i$, so $l(X, T) \ge k$. Also $l(\chi, T) \le E$, so $l(X, T) \le kE$.

**The reduction.** Fix $\varepsilon \in (0, \tfrac14]$. Given $X$, let $M = \max\{2n, k\}$, $N_c = \lceil M^{1/\varepsilon} \rceil$, and let $X_0$ be $X$ followed by $N_c$ copies of the all-zero character. So $X_0$ has $K = k + N_c$ characters, and $K \le 2 N_c$. For fixed $\varepsilon$ this is polynomial in the size of $X$. Adding constant characters does not change parsimony scores, so $l(X_0, T) = l(X, T)$ for every $T$. Note $E < 2n \le M$, and $\ln K \ge \ln N_c \ge \tfrac1\varepsilon \ln M$.

Instances with $M$ below any fixed constant have a bounded number of taxa and characters, and MP on them is solved by brute force in constant time. So we may assume that $M$ is larger than any constant $M_0(\varepsilon)$ that we need below.

**Claim 1 (upper bound).** For every tree $T$ there is a $p$ with $\tilde L(X_0 \mid T, p) \le (1 + 2\varepsilon)\, l(X, T) \ln K$.

*Proof.* Let $l = l(X, T) \ge 1$ and set every $p_e = q = l / (E K)$. Since $l \le kE$, $q \le k / K < \tfrac12$. For a character $\chi$ of $X_0$, fix a labeling of $T$ that extends $\chi$ with exactly $l(\chi, T)$ changing edges. Its probability is at least the probability of the process producing this labeling, so

$$2 P[\chi \mid T, p] \ge q^{l(\chi, T)} (1 - q)^{E - l(\chi, T)} \ge q^{l(\chi, T)} (1 - q)^{E}.$$

Summing $-\ln$ of this over the $K$ characters, and using $\sum_\chi l(\chi, T) = l$,

$$\tilde L(X_0 \mid T, p) \le l \cdot (-\ln q) + K E \cdot (-\ln(1 - q)).$$

For $q \le \tfrac12$, $-\ln(1 - q) \le q / (1 - q) \le 2q$, so the second term is at most $2 K E q = 2l$. And $-\ln q = \ln K + \ln E - \ln l \le \ln K + \ln E$. So

$$\tilde L(X_0 \mid T, p) \le l \left(\ln K + \ln E + 2\right) = l \ln K \left(1 + \frac{\ln E + 2}{\ln K}\right) \le l \ln K \left(1 + \varepsilon \frac{\ln M + 2}{\ln M}\right),$$

which is at most $(1 + 2\varepsilon)\, l \ln K$ once $\ln M \ge 2$. $\square$

**Claim 2 (short edges).** If $\tilde L(X_0 \mid T, p) \le \beta$, then $p_e \le \beta / N_c$ for every edge $e$.

*Proof.* For the all-zero character $0$, $2P[0 \mid T, p] = P[0] + P[1]$ is the probability that all leaves have the same state. Every edge $e$ lies on the path between some two leaves $u$ and $v$, because $T$ has no vertex of degree 2 and its leaves are the taxa. The states of $u$ and $v$ differ exactly when an odd number of the edges on their path flip, which has probability $\tfrac12 \bigl(1 - \prod_{f} (1 - 2p_f)\bigr)$ over the edges $f$ of the path. All factors are in $[0, 1]$, so the product is at most $1 - 2p_e$, and the probability is at least $p_e$. So $2 P[0 \mid T, p] \le 1 - p_e$, and each all-zero character contributes $-\ln(1 - p_e) \ge p_e$ to $\tilde L$. The other terms are nonnegative, so $\beta \ge \tilde L \ge N_c\, p_e$. $\square$

**Claim 3 (lower bound).** Let $T$ be a tree and $p$ a vector with $p_e \le \bar p$ for every edge, where $E \bar p \le \tfrac12$. Then

$$\tilde L(X_0 \mid T, p) \ge l(X, T) \cdot \bigl(-\ln(E \bar p)\bigr) - k \ln 2.$$

*Proof.* Fix a non-constant character $\chi$ of $X$. A labeling of all the vertices of $T$ that agrees with $\chi$ at the leaves is fixed by the root state and the set $F$ of edges whose ends differ. For one set $F$, the two root states give complementary labelings, and they cannot both agree with $\chi$, because $\chi \ne \bar\chi$. Every such labeling has $|F| \ge l(\chi, T)$, and its probability is at most $\tfrac12 \bar p^{|F|}$. So

$$P[\chi \mid T, p] \le \frac12 \sum_{j \ge l(\chi, T)} \binom{E}{j} \bar p^{\,j} \le \frac12 \sum_{j \ge l(\chi, T)} (E \bar p)^j \le \frac12 \cdot \frac{(E \bar p)^{l(\chi, T)}}{1 - E\bar p} \le (E \bar p)^{l(\chi, T)}.$$

Hence $-\ln(2 P[\chi]) \ge l(\chi, T)(-\ln(E \bar p)) - \ln 2$. Summing over the $k$ characters of $X$, and using that the all-zero characters contribute nonnegative terms, gives the claim. $\square$

**Proposition (ML approximation gives MP approximation).** Let $c > 0$ and $\varepsilon \in (0, \tfrac14]$ satisfy $(1 + c)(1 + 2\varepsilon) \le 2$. If a polynomial-time algorithm is a $(1 + c)$-approximation for ML under the CFN model, then there is a polynomial-time algorithm that returns for every MP instance $X$ (with $M \ge M_0(\varepsilon)$) a tree $T$ with

$$l(X, T) \le \frac{(1 + c)(1 + 2\varepsilon)}{1 - 5\varepsilon}\, l^*(X).$$

*Proof.* Build $X_0$, run the ML algorithm on it, and return its tree $T$ with its vector $p$. Let $l^* = l^*(X)$. By Claim 1 applied to an MP-optimal tree, the ML optimum of $X_0$ is at most $(1 + 2\varepsilon) l^* \ln K$, so

$$\tilde L(X_0 \mid T, p) \le \beta := (1 + c)(1 + 2\varepsilon)\, l^* \ln K \le 2 l^* \ln K.$$

By Claim 2, every $p_e \le \bar p := \beta / N_c$. We check the condition of Claim 3. Since $l^* \le kE \le M^2$ and $E \le M$,

$$E \bar p \le \frac{2 M^3 \ln K}{N_c} \le \frac{2 M^3 \ln(2 N_c)}{N_c},$$

and with $N_c \ge M^4$ (as $\varepsilon \le \tfrac14$) this tends to 0 as $M$ grows, so $E \bar p \le \tfrac12$ for $M \ge M_0(\varepsilon)$. Next, using $\ln N_c \ge \ln K - \ln 2$,

$$-\ln(E \bar p) \ge \ln N_c - \ln(2 M^3 \ln K) \ge \ln K - 2\ln 2 - 3 \ln M - \ln \ln K.$$

Since $\ln K \ge \tfrac1\varepsilon \ln M$, the term $3 \ln M$ is at most $3\varepsilon \ln K$, and $2 \ln 2 + \ln \ln K \le \varepsilon \ln K$ for $M \ge M_0(\varepsilon)$. So $-\ln(E \bar p) \ge (1 - 4\varepsilon) \ln K$. Claim 3 and $k \le l(X, T)$ give

$$\tilde L(X_0 \mid T, p) \ge l(X, T) \bigl((1 - 4\varepsilon) \ln K - \ln 2\bigr) \ge (1 - 5\varepsilon)\, l(X, T) \ln K,$$

where the last step needs $\ln 2 \le \varepsilon \ln K$, again true for $M \ge M_0(\varepsilon)$. Comparing with $\tilde L \le \beta$ and dividing by $(1 - 5\varepsilon) \ln K$ gives the bound. $\square$

**Theorem.** There is a constant $c > 0$ such that, unless P = NP, no polynomial-time algorithm is a $(1 + c)$-approximation for maximum likelihood under the CFN model. In particular, no polynomial-time algorithm finds a maximum likelihood tree with its parameters unless P = NP.

*Proof.* Let $c_0$ be the constant of Fact A. Choose $\varepsilon \in (0, \tfrac14]$ and $c > 0$ so small that $(1 + c)(1 + 2\varepsilon) \le 2$ and $(1 + c)(1 + 2\varepsilon) / (1 - 5\varepsilon) \le 1 + c_0$. If a polynomial-time $(1 + c)$-approximation for ML existed, the Proposition, with brute force for the instances with $M < M_0(\varepsilon)$, would give a polynomial-time $(1 + c_0)$-approximation for MP, and Fact A would give P = NP. An exact algorithm is a $(1 + c)$-approximation for every $c$, which gives the last sentence. $\blacksquare$

**Remarks.** The flip probability $p_e$ is the CFN form of a branch length: $p_e = \tfrac12 (1 - e^{-2 t_e})$ for a branch of $t_e$ expected substitutions per site, so $p_e \in [0, \tfrac12)$ covers all finite lengths and $p_e = \tfrac12$ is the limit $t_e = \infty$. The all-zero characters force every branch to be short, of order $l^* \ln K / N_c$. On such a tree the probability of a character is dominated by its most parsimonious labelings, which is why the negative log-likelihood is close to $\ln K$ times the parsimony score.
