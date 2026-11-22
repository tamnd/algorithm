---
title: The logit of a logistic model, the balanced shadow design, the per-record cut of the Gaussian likelihood ratio, and the zero advantage against a model that ignores its data
proves: [correctness]
status: full
---

**Setting.** A shadow or target model $g$ gives a record $(x, y)$, $y \in \{0, 1\}$, the confidence $c = \Pr_g[y \mid x]$ and the score $\phi = \ln(c / (1 - c))$. The Gaussian log density is $\ell(u; \mu, v) = -\tfrac{1}{2}\ln(2\pi v) - (u - \mu)^2/(2v)$ for $v > 0$, and the online score is $\Lambda = \ell(\phi^*; \mu_{\text{in}}, v_{\text{in}}) - \ell(\phi^*; \mu_{\text{out}}, v_{\text{out}})$, with the means of the IN and OUT values and the given or fitted variances, raised to the floor.

**Claim 1 (the logit of a logistic model).** For $g = (w, b)$, $z = \langle w, x \rangle + b$ and $s = 2y - 1$, $\phi = s z$.

*Proof.* The model gives the label $1$ with probability $\sigma(z) = 1/(1 + e^{-z})$, and $1 - \sigma(z) = \sigma(-z)$, so $c = \sigma(s z)$ for both labels. For any $u$, $\sigma(u)/(1 - \sigma(u)) = \sigma(u)/\sigma(-u) = e^{u}$, because $\sigma(u) = e^u \sigma(-u)$. So $\phi = \ln e^{s z} = s z$. $\square$

**Claim 2 (balanced shadows).** train_shadows with $p$ pairs on a pool of even size $m$ returns $2p$ models, each trained on exactly $m/2$ records, and every record is IN for exactly $p$ models.

*Proof.* In each pair the code draws a set $H$ of $m/2$ distinct indices and builds the masks $[i \in H]$ and $[i \notin H]$. Each mask has $m/2$ true entries, and for each $i$ exactly one of the two masks is true. Each model is train_logistic on the records of its mask. Summing over the $p$ pairs, record $i$ is IN for $p$ models. $\square$

So in the game of the tests, where a target uses the $2p - 2$ models of the other pairs as shadows, every record has exactly $p - 1$ IN and $p - 1$ OUT values; with $p = 16$ both lists are nonempty, which is the precondition of lira_scores.

**Claim 3 (the score is the log likelihood ratio).** online_score returns $\ln\big(N(\phi^*; \mu_{\text{in}}, v_{\text{in}}) / N(\phi^*; \mu_{\text{out}}, v_{\text{out}})\big)$, where $N(\cdot; \mu, v)$ is the normal density.

*Proof.* gaussian_fit returns the mean and the population variance; the variance used is the given one if any, else the fitted one, and then at least the floor, so it is positive. log_normal returns $\ell(u; \mu, v) = \ln N(u; \mu, v)$, and the score is the difference of two such logarithms, which is the logarithm of the ratio. $\square$

**Claim 4 (a per-record cut).** If $v_{\text{in}} = v_{\text{out}} = v$, then

$$\Lambda = \frac{\mu_{\text{in}} - \mu_{\text{out}}}{v}\Big(\phi^* - \frac{\mu_{\text{in}} + \mu_{\text{out}}}{2}\Big).$$

So when $\mu_{\text{in}} > \mu_{\text{out}}$, the rule $\Lambda \ge t$ is the rule $\phi^* \ge \frac{\mu_{\text{in}} + \mu_{\text{out}}}{2} + \frac{t v}{\mu_{\text{in}} - \mu_{\text{out}}}$, a threshold on $\phi^*$ whose cut depends on the record through its means.

*Proof.* The terms $-\tfrac{1}{2}\ln(2\pi v)$ cancel, so $\Lambda = \big((\phi^* - \mu_{\text{out}})^2 - (\phi^* - \mu_{\text{in}})^2\big)/(2v)$. The difference of squares is $(\mu_{\text{in}} - \mu_{\text{out}})(2\phi^* - \mu_{\text{in}} - \mu_{\text{out}})$. Divide by $2v$. For the rule, divide $\Lambda \ge t$ by the positive number $(\mu_{\text{in}} - \mu_{\text{out}})/v$. $\square$

In the example, record A has means $3$ and $1$ and $v = 2/3$, so $\Lambda = 3(2.5 - 2) = 1.5$; record B has means $6$ and $4$, so $\Lambda = 3(4.5 - 5) = -1.5$.

**Claim 5 (a model that ignores its data).** Consider the game of the tests: $p$ pairs with independent uniform halves $H_1, \ldots, H_p$, and each model $j$, in pair $q(j)$, is the target once, with the models of the other $p - 1$ pairs as shadows. Suppose every model is trained on data drawn independently of the halves (the control of the tests, which trains each model on fresh draws), and treat the seeded generator as a source of independent draws. Then for each fixed cut $t$, the expected TPR of the rule $\Lambda \ge t$ over all targets equals its expected FPR.

*Proof.* Let $\beta_{ij} \in \{0, 1\}$ be the mask of target $j$ on record $i$; it is a function of $H_{q(j)}$ alone, and $\Pr[\beta_{ij} = 1] = 1/2$ because $H_{q(j)}$ is a uniform half. The score $\Lambda_{ij}$ is computed by lira_scores from the values $\phi$ of the target and of the shadows, which are functions of the models, and from the masks of the shadows, which are functions of the halves $H_{q'}$ with $q' \ne q(j)$. The models and these halves are independent of $H_{q(j)}$, so $\Lambda_{ij}$ is independent of $\beta_{ij}$, and $\mathbb{E}\big[\mathbf{1}[\Lambda_{ij} \ge t]\, \beta_{ij}\big] = \tfrac{1}{2}\Pr[\Lambda_{ij} \ge t] = \mathbb{E}\big[\mathbf{1}[\Lambda_{ij} \ge t]\,(1 - \beta_{ij})\big]$. By Claim 2 each target has exactly $m/2$ members and $m/2$ nonmembers, so with $2p$ targets both totals are $p m$, and

$$\mathbb{E}[\text{TPR}] = \frac{1}{p m}\sum_{i, j} \mathbb{E}\big[\mathbf{1}[\Lambda_{ij} \ge t]\, \beta_{ij}\big] = \frac{1}{p m}\sum_{i, j} \mathbb{E}\big[\mathbf{1}[\Lambda_{ij} \ge t]\,(1 - \beta_{ij})\big] = \mathbb{E}[\text{FPR}]. \qquad \square$$

The partner of the target is left out of the shadows on purpose: its mask is the complement of the target's, so with it the split of the shadow values would depend on $\beta_{ij}$, and the IN and OUT lists would have different lengths for members and nonmembers.

**The algorithm.** Line L1 is train_shadows (Claim 2); lines L2 to L5 are lira_scores, which computes $\phi$ by Claim 1 and the score by Claim 3, with one variance for all records when asked; line L6 compares the score with the cut. The Neyman-Pearson lemma makes the exact likelihood ratio the most powerful test; the Gaussian fit is an approximation, so the power of the attack on the target is not claimed and is measured in the tests. In the control of Claim 5 with $t = 0$, the measured TPR minus FPR, $0.0625$ over 512 members and 512 nonmembers that share records and models, is sampling noise around $0$. $\blacksquare$
