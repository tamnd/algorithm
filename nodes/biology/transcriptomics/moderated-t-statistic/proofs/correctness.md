---
title: Under the hierarchical model, the moderated t has a t distribution with d0 + d degrees of freedom
proves: [correctness]
status: full
---

We prove the main result of Smyth (2004) for one coefficient: under the hierarchical model, with the prior parameters known, the moderated t has a $t$ distribution with $d_0 + d$ degrees of freedom under the null hypothesis (Theorem 2). The posterior variance is the inverse of the posterior mean of the precision (Lemma 1), which explains the formula at line L6. We also derive the moment equations that lines L2 to L4 solve (Lemma 3). With estimated $d_0$ and $s_0^2$, the $t_{d_0+d}$ law holds only approximately. Smyth (2004) gives the asymptotic argument; it is cited, not proved here, and the page labels it as an approximation.

**The model.** For each gene $g$, given its variance $\sigma_g^2$:

- the estimated coefficient (here a difference of two group means) is $\hat\beta_g \sim N(\beta_g, v\sigma_g^2)$, with a known $v$ (here $1/n_A + 1/n_B$);
- the residual variance is $s_g^2 \sim \sigma_g^2\chi^2_d/d$, with $d$ residual degrees of freedom;
- $\hat\beta_g$ and $s_g^2$ are independent.

The prior is $1/\sigma_g^2 \sim \chi^2_{d_0}/(d_0s_0^2)$, a scaled inverse chi-squared prior on $\sigma_g^2$. The posterior variance is $\tilde s_g^2 = (d_0s_0^2 + ds_g^2)/(d_0 + d)$, and the moderated t is $\tilde t_g = \hat\beta_g/(\tilde s_g\sqrt v)$.

These assumptions hold exactly for normal data with equal variances in the two groups. For read counts they hold only after a transformation, as in voom, and then only approximately.

**Lemma 1 (posterior of the precision).** Write $\tau = 1/\sigma_g^2$. Given $s_g^2$, $\tau$ has a gamma distribution with shape $(d_0 + d)/2$ and rate $(d_0s_0^2 + ds_g^2)/2$. Its posterior mean is $1/\tilde s_g^2$.

*Proof.* The prior says $d_0s_0^2\tau \sim \chi^2_{d_0}$, so the prior density of $\tau$ is proportional to $\tau^{d_0/2 - 1}e^{-d_0s_0^2\tau/2}$. Given $\tau$, $W = d s_g^2\tau \sim \chi^2_d$, so the density of $s_g^2$ is proportional to $\tau^{d/2}(s_g^2)^{d/2-1}e^{-ds_g^2\tau/2}$, as a function of $\tau$ and $s_g^2$. By [Bayes' theorem](/bayes-theorem/), the posterior density of $\tau$ is proportional to $\tau^{(d_0+d)/2 - 1}e^{-(d_0s_0^2 + ds_g^2)\tau/2}$, which is the stated gamma law. A gamma law with shape $a$ and rate $b$ has mean $a/b = (d_0 + d)/(d_0s_0^2 + ds_g^2) = 1/\tilde s_g^2$. $\square$

**Theorem 2 (null distribution).** If $\beta_g = 0$, then $\tilde t_g$ has a $t$ distribution with $d_0 + d$ degrees of freedom, for every $d_0 > 0$, $s_0^2 > 0$ and $d \ge 1$.

*Proof.* Let $Z = \hat\beta_g/(\sigma_g\sqrt v)$, $W_1 = ds_g^2/\sigma_g^2$ and $W_0 = d_0s_0^2/\sigma_g^2$. Given $\sigma_g$, $Z \sim N(0, 1)$ and $W_1 \sim \chi^2_d$, and they are independent. These conditional laws do not depend on $\sigma_g$. So $Z$, $W_1$ and $\sigma_g$ are mutually independent: for any sets $B_1, B_2, B_3$, $P(Z \in B_1, W_1 \in B_2, \sigma_g \in B_3) = E[\mathbf 1\{\sigma_g \in B_3\}P(Z \in B_1)P(W_1 \in B_2)]$. The variable $W_0$ is a function of $\sigma_g$, and by the prior $W_0 \sim \chi^2_{d_0}$. So $Z$, $W_0$ and $W_1$ are independent, and $W_0 + W_1 \sim \chi^2_{d_0 + d}$, independent of $Z$. Now
$$\tilde t_g = \frac{\hat\beta_g}{\tilde s_g\sqrt v} = \frac{Z\sigma_g}{\tilde s_g} = \frac{Z}{\sqrt{(W_0 + W_1)/(d_0 + d)}},$$
because $(d_0 + d)\tilde s_g^2/\sigma_g^2 = W_0 + W_1$. This is the definition of a $t$ variable with $d_0 + d$ degrees of freedom. $\square$

**Limits.** With $d_0 = 0$, $\tilde s_g^2 = s_g^2$ and the moderated t is the ordinary pooled [t-test](/student-t-test/) on $d$ degrees of freedom. As $d_0 \to \infty$ with $s_0^2$ fixed, $\tilde s_g^2 \to s_0^2$ and $\tilde t_g$ tends to a $z$ statistic with known variance $s_0^2$; the code uses the normal law when $d_0 = \infty$. For finite $d_0$, $\tilde s_g^2$ is a weighted mean of $s_g^2$ and $s_0^2$, so it lies between them.

**Lemma 3 (the moment equations).** Under the model, let $e_g = \ln s_g^2 - \psi(d/2) + \ln(d/2)$, with $\psi$ the digamma function and $\psi'$ the trigamma function. Then
$$E[e_g] = \ln s_0^2 - \psi(d_0/2) + \ln(d_0/2), \qquad \operatorname{Var}(e_g) = \psi'(d/2) + \psi'(d_0/2).$$

*Proof.* Write $s_g^2 = s_0^2 \cdot (W_1/d)/(W_0/d_0)$ with $W_0$ and $W_1$ as in Theorem 2, which are independent. So $\ln s_g^2 = \ln s_0^2 + \ln(W_1/d) - \ln(W_0/d_0)$. A $\chi^2_k$ variable is a gamma variable with shape $k/2$ and scale 2. For a gamma variable $X$ with shape $a$ and scale $\theta$, $E\ln X = \psi(a) + \ln\theta$ and $\operatorname{Var}\ln X = \psi'(a)$; both follow by differentiating $\ln\Gamma(a + s)$ at $s = 0$, since $E[X^s] = \theta^s\Gamma(a + s)/\Gamma(a)$. So $E\ln(W_k/k) = \psi(k/2) - \ln(k/2)$ and $\operatorname{Var}\ln(W_k/k) = \psi'(k/2)$. Adding the means and, by independence, the variances gives the claim. $\square$

Lines L2 to L4 replace $E[e_g]$ and $\operatorname{Var}(e_g)$ by the sample mean $\bar e$ and the sample variance of the $e_g$, and solve the two equations: $\psi'(d_0/2) = \widehat{\operatorname{Var}}(e) - \psi'(d/2)$ and $s_0^2 = \exp(\bar e + \psi(d_0/2) - \ln(d_0/2))$. The function $\psi'(x) = \sum_{k \ge 0}(x + k)^{-2}$ decreases strictly from $\infty$ to 0 on $(0, \infty)$, so the first equation has exactly one solution when its right side is positive. When it is not, the sample variance of the $e_g$ is no larger than the variance that sampling error alone gives, and line L5 sets $d_0 = \infty$. Then, as in limma, $s_0^2$ is the mean of the $s_g^2$. The method of moments is consistent as the number of genes grows when the genes are independent; that is a standard fact and is cited, not proved here. Genes are not independent in practice, so the estimates are a heuristic.

**Degrees of freedom cap.** limma caps $d_0 + d$ at the total residual degrees of freedom of all genes, $Gd$, and the code does the same. This changes nothing unless $d_0$ is very large.

**Special functions.** The code computes $\psi$, $\psi'$ and $\psi''$ by the recurrences $\psi(x) = \psi(x+1) - 1/x$, $\psi'(x) = \psi'(x+1) + 1/x^2$ and $\psi''(x) = \psi''(x+1) - 2/x^3$ up to $x \ge 10$, and then by their asymptotic series. It inverts $\psi'$ by Newton's method on $1/\psi'(x) = 1/y$, from $x = 0.5 + 1/y$, as limma does. The $t$ tail is $P(T > t) = \frac12 I_{d/(d+t^2)}(d/2, 1/2)$ for $t \ge 0$, with the regularized incomplete beta function $I$ computed by its continued fraction. The tests check these against known values: $\psi(1) = -\gamma$, $\psi'(1) = \pi^2/6$, $\psi'(1/2) = \pi^2/2$, the closed forms of the $t$ tail for 1 and 2 degrees of freedom, and the binomial sum for $I_x(a, b)$ with integer $a$ and $b$.

**What the tests check.** Theorem 2 is checked by simulation from the model with the true prior: over 4000 null genes, the fraction of p-values below 0.01, 0.05 and 0.5 must be within $4\sqrt{u(1-u)/4000}$ of $u$. The estimation of $d_0$ and $s_0^2$ is only measured.

**Complexity.** For $G$ genes and $n$ samples, the gene-wise statistics take $\Theta(Gn)$ time. The fit of the prior takes $\Theta(G)$ plus a sort for the median floor, $O(G\log G)$. Each p-value needs one continued fraction, which takes a bounded number of steps for the degrees of freedom met in practice. The extra space is $\Theta(G)$.
