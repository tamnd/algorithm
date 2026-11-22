---
title: The template attack computes the log likelihood of each guess, and the maximum likelihood rule is optimal
proves: [correctness]
status: full
---

Write $\varphi(x; \mu, \Sigma) = (2\pi)^{-T/2} (\det\Sigma)^{-1/2} \exp\big(-\tfrac12 (x - \mu)^\top \Sigma^{-1} (x - \mu)\big)$ for the density of $\mathcal{N}(\mu, \Sigma)$ in dimension $T$, with $\Sigma$ symmetric positive definite.

**Lemma 1 (line L8).** Let $C$ be lower triangular with positive diagonal and $CC^\top = \Sigma$. Let $y$ solve $Cy = d$ by forward substitution. Then $d^\top \Sigma^{-1} d = \lVert y \rVert^2$ and $\ln\det\Sigma = 2\sum_i \ln C_{ii}$.

*Proof.* $\Sigma^{-1} = (C^\top)^{-1} C^{-1}$, so $d^\top \Sigma^{-1} d = (C^{-1}d)^\top (C^{-1}d) = y^\top y$. Forward substitution finds $y_i = (d_i - \sum_{q < i} C_{iq} y_q)/C_{ii}$ in order $i = 1, \ldots, T$, which is the unique solution because $C$ is triangular with a nonzero diagonal. The determinant of a triangular matrix is the product of its diagonal, so $\det\Sigma = (\det C)^2 = \prod_i C_{ii}^2$. $\square$

So after the loop of line L7, $\mathrm{score}(g) = \sum_i \ln \varphi(\ell_i; \mu_{S(p_i \oplus g)}, \Sigma) + \tfrac{mT}{2}\ln 2\pi$. The added constant is the same for every guess.

**Lemma 2 (the loop of line L5).** Line L11 returns the first guess with the largest score.

*Proof.* Each score is finite, so the first guess passes line L9, and later guesses replace best only with a strictly larger score. By induction, top is the largest score so far and best is the first guess that reaches it. $\square$

**The model.** The key $K$ is uniform on $\{0, \ldots, 15\}$. Given $K = k$ and the inputs $p_1, \ldots, p_m$, the traces are independent and $\ell_i$ has density $f_k(\ell_i \mid p_i) = \varphi(\ell_i; \mu_{S(p_i \oplus k)}, \Sigma)$. The inputs are known and independent of $K$. Write $L_k(x) = \prod_i f_k(\ell_i \mid p_i)$ for the likelihood of the observation $x = (p_i, \ell_i)_{i \le m}$ under the key $k$.

**Theorem (optimality).** Let $d$ be any decision rule that maps an observation $x$ to a guess $d(x)$. Then $\Pr[d(x) = K] \le \Pr[d^\ast(x) = K]$, where $d^\ast(x)$ is a guess with the largest likelihood $L_k(x)$. With exact templates ($\mu_v$ and $\Sigma$ of the model), the template attack is such a rule $d^\ast$.

*Proof.* Fix the inputs; the argument is the same for each choice of them, and so it holds after averaging over the inputs. The traces have the density $q(x) = \tfrac{1}{16}\sum_k L_k(x)$, and by [Bayes' theorem](/bayes-theorem/) the posterior of the key is $\Pr[K = k \mid x] = L_k(x) / \sum_{k'} L_{k'}(x)$. So

$$\Pr[d(x) = K] = \int \tfrac{1}{16} L_{d(x)}(x)\, dx \le \int \tfrac{1}{16} \max_k L_k(x)\, dx = \Pr[d^\ast(x) = K].$$

The inequality holds point by point, because $L_{d(x)}(x) \le \max_k L_k(x)$. With the uniform prior, the largest posterior and the largest likelihood are reached at the same key. By Lemma 1, with exact templates the score of guess $g$ is $\ln L_g(x)$ plus a constant that does not depend on $g$, and the logarithm is increasing, so the guess of line L11 has the largest likelihood. $\blacksquare$

The theorem is about the stated model: it assumes that the templates are the true distribution of the target's traces. It gives no bound when the profiling device and the target differ.

**Proposition (estimated templates converge).** Fix the model and let the number $n$ of profiling traces grow, with each value drawn uniformly. Then with probability 1, the means of line L1 converge to $\mu_v$, the pooled covariance of line L2 converges to $\Sigma$, and for fixed attack traces each score converges to its value under the exact templates.

*Proof.* Each class receives a number of traces that grows without bound, with probability 1. By the strong [law of large numbers](/law-of-large-numbers/) the class means converge to $\mu_v$. The pooled covariance is $\frac{1}{n - V}\sum_i (\ell_i - \hat\mu_{v_i})(\ell_i - \hat\mu_{v_i})^\top$. Write $\ell_i - \hat\mu_{v_i} = (\ell_i - \mu_{v_i}) - (\hat\mu_{v_i} - \mu_{v_i})$. The average of $(\ell_i - \mu_{v_i})(\ell_i - \mu_{v_i})^\top$ converges to $\Sigma$ by the law of large numbers, and the terms with $\hat\mu_v - \mu_v$ tend to 0 because that difference tends to 0 while the averages that multiply it stay bounded. The factor $n/(n - V)$ tends to 1. The Cholesky factor is a continuous function of a positive definite matrix, and the score of Lemma 1 is a continuous function of the means and the factor. So the scores converge. $\square$

If, in addition, the exact scores have a unique maximum, the estimated rule picks the same guess as the exact rule for all large $n$, and so its success probability tends to that of the optimal rule.
