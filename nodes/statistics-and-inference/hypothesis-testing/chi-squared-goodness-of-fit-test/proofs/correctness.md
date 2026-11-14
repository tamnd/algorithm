---
title: Under a simple null the Pearson statistic is the squared length of a projected normal vector in the limit, so it tends to chi-square with k - 1 degrees of freedom
proves: [correctness]
status: full
---

**Model.** $n$ independent observations fall into $k \ge 2$ categories. Category $i$ has probability $p_i > 0$, with $\sum_i p_i = 1$. The counts $O = (O_1, \ldots, O_k)$ are multinomial. The simple null hypothesis fixes $p = p^0$. Write $E_i = n p^0_i$ and

$$X^2 = \sum_{i = 1}^k \frac{(O_i - E_i)^2}{E_i}, \qquad G = 2 \sum_{i : O_i > 0} O_i \log \frac{O_i}{E_i}.$$

**Claim 1 (lines L1 to L3 compute the statistics).** Line L1 sets $n = \sum_i O_i$, line L2 sets $E_i = n p_i$, and line L3 sums the $k$ terms of $X^2$ or of $G$. In $G$ a cell with $O_i = 0$ contributes $0$, which is the limit of $o \log(o/e)$ as $o \to 0$. The sum uses `math.fsum`, so the only rounding is in the terms. Line L4 sets the degrees of freedom to $k - 1 - s$, where $s$ is the argument `fitted`, and line L5 returns $P(\chi^2_{k - 1 - s} > X^2)$ from the regularized upper incomplete gamma function of the helper module. $\square$

**Claim 2 (the mean and covariance of the counts).** Under $H_0$, $\mathbb{E}[O_i] = E_i$, $\operatorname{Var}(O_i) = n p^0_i (1 - p^0_i)$ and $\operatorname{Cov}(O_i, O_j) = -n p^0_i p^0_j$ for $i \ne j$.

*Proof.* Write $O = \sum_{m = 1}^n e_{J_m}$, where $J_m$ is the category of observation $m$ and $e_j$ is the $j$-th unit vector. The vectors $e_{J_m}$ are iid with mean $p^0$. Their second moment is $\mathbb{E}[e_J e_J^\top] = \operatorname{diag}(p^0)$, because $e_J e_J^\top$ has a single 1, on the diagonal at $(J, J)$. So each has covariance $\operatorname{diag}(p^0) - p^0 (p^0)^\top$, and the sum of $n$ independent copies has $n$ times this covariance. $\square$

**Claim 3 (the limit law under a simple null).** Under $H_0$, $X^2$ converges in distribution to $\chi^2_{k - 1}$ as $n \to \infty$, with $k$ and $p^0$ fixed.

*Proof.* Let $D = \operatorname{diag}(p^0)^{-1/2}$ and $Y_n = D (O - n p^0)/\sqrt n$, so the $i$-th entry is $(O_i - E_i)/\sqrt{E_i}$ and $X^2 = \lVert Y_n \rVert^2$. By Claim 2, $Y_n$ is $n^{-1/2}$ times a sum of $n$ iid centred vectors $D(e_{J_m} - p^0)$ with covariance

$$D \big(\operatorname{diag}(p^0) - p^0 (p^0)^\top\big) D = I - u u^\top, \qquad u = \big(\sqrt{p^0_1}, \ldots, \sqrt{p^0_k}\big)^\top.$$

The multivariate [central limit theorem](/central-limit-theorem/) gives $Y_n \to W$ in distribution, with $W \sim N(0, I - u u^\top)$. (The multivariate form follows from the one-dimensional form by the Cramér-Wold device: for each fixed vector $a$, $a^\top Y_n$ is a normalized sum of iid scalars with variance $a^\top (I - uu^\top) a$.) The map $y \mapsto \lVert y \rVert^2$ is continuous, so $X^2 \to \lVert W \rVert^2$ in distribution.

Now find the law of $\lVert W \rVert^2$. Since $\lVert u \rVert^2 = \sum_i p^0_i = 1$, the matrix $P = I - u u^\top$ is the orthogonal projection onto the hyperplane $u^\perp$, of rank $k - 1$. Choose an orthonormal basis $q_1, \ldots, q_{k - 1}$ of $u^\perp$ and let $Z \sim N(0, I_k)$. The vector $PZ$ is normal with covariance $P P^\top = P$, so it has the law of $W$. Also $PZ = \sum_{j < k} (q_j^\top Z) q_j$, so $\lVert PZ \rVert^2 = \sum_{j = 1}^{k - 1} (q_j^\top Z)^2$. The $q_j^\top Z$ are jointly normal with covariance $q_j^\top q_l = [j = l]$, so they are iid standard normal, and $\lVert W \rVert^2$ has the $\chi^2_{k - 1}$ law. $\square$

**Claim 4 (the size tends to the nominal level).** For a fixed $\alpha \in (0, 1)$, the test that rejects when $p \le \alpha$ has $P_{H_0}(\text{reject}) \to \alpha$.

*Proof.* Rejecting when $P(\chi^2_{k-1} > X^2) \le \alpha$ is rejecting when $X^2 \ge c$, where $c$ is the upper $\alpha$ point of $\chi^2_{k - 1}$, because the tail function is continuous and strictly decreasing. The limit law is continuous, so $P(X^2 \ge c) \to P(\chi^2_{k - 1} \ge c) = \alpha$. $\square$

The convergence is not uniform in $p^0$. If some $n p^0_i$ is small, the multinomial law is far from its normal limit, and the true size can be above or below $\alpha$. The tests compute the exact size by summing the multinomial probabilities of all outcomes for several small cases.

**Claim 5 (two categories).** For $k = 2$, $X^2 = z^2$ with $z = (O_1 - n p^0_1)/\sqrt{n p^0_1 (1 - p^0_1)}$, the score statistic of the binomial test.

*Proof.* Let $d = O_1 - n p^0_1$. Then $O_2 - n p^0_2 = -d$, so $X^2 = d^2 \big(1/(n p^0_1) + 1/(n p^0_2)\big) = d^2/(n p^0_1 p^0_2)$, which is $z^2$. $\square$

**Claim 6 (the G statistic has the same limit).** Under $H_0$, $G - X^2 \to 0$ in probability, so $G$ also tends to $\chi^2_{k - 1}$.

*Proof.* Let $f(t) = 2(1 + t)\log(1 + t) - 2t - t^2$ for $t > -1$. Then $f(0) = f'(0) = f''(0) = 0$ and $f'''(t) = -2/(1 + t)^2$, so $\lvert f'''(t) \rvert \le 8$ for $t \ge -1/2$, and Taylor's theorem gives $\lvert f(t) \rvert \le \tfrac43 \lvert t \rvert^3$ there. Put $d_i = O_i - E_i$ and $t_i = d_i/E_i$. Then $O_i = E_i(1 + t_i)$ and $2 O_i \log(O_i/E_i) = E_i(2t_i + t_i^2 + f(t_i))$ when $O_i > 0$. Summing over $i$ and using $\sum_i d_i = 0$,

$$G = \sum_i \frac{d_i^2}{E_i} + \sum_i E_i f(t_i) = X^2 + \sum_i E_i f(t_i).$$

By Claim 3, each $d_i/\sqrt n$ is bounded in probability, so $t_i = O_P(n^{-1/2})$. On the event that all $\lvert t_i \rvert \le 1/2$ (all $O_i > 0$ then), whose probability tends to 1, $\lvert G - X^2 \rvert \le \tfrac43 \sum_i \lvert d_i \rvert^3/E_i^2 = O_P(n^{3/2}/n^2) = O_P(n^{-1/2})$. Slutsky's theorem gives the limit of $G$. $\square$

**Fitted parameters (cited, not proved here).** Suppose the null is a family $p(\theta)$ with $\theta \in \mathbb{R}^s$, and $\hat\theta$ is the maximum likelihood estimate from the grouped counts $O$ (or the minimum chi-square estimate). Under smoothness and rank conditions, $X^2$ with $E_i = n p_i(\hat\theta)$ tends to $\chi^2_{k - 1 - s}$. Fisher (1922, 1924) gave the result, and Cramér's 1946 book has a complete proof. The idea is the same as in Claim 3: the estimate removes $s$ more dimensions, and $Y_n$ tends to a normal vector on a subspace of dimension $k - 1 - s$. If instead $\hat\theta$ is the maximum likelihood estimate from the ungrouped observations, Chernoff and Lehmann (1954) showed that the limit is $\sum_{j \le k - 1 - s} Z_j^2 + \sum_{j = 1}^{s} \lambda_j Z_{k - 1 - s + j}^2$ with iid standard normal $Z_j$ and $\lambda_j \in [0, 1]$, so it lies between $\chi^2_{k - 1 - s}$ and $\chi^2_{k - 1}$. The tests check this by simulation.

**Cost.** Lines L1 to L4 do $\Theta(k)$ arithmetic operations and store the $k$ expected counts. Line L5 is one evaluation of the incomplete gamma function, which we count as one operation of the real-RAM model.
