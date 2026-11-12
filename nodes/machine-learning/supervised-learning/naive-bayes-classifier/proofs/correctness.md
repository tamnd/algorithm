---
title: Multinomial naive Bayes fits the stated estimates and returns the posterior argmax of the fitted model
proves: [correctness]
status: full
---

We use the pseudocode of the page. The model has a prior $\pi$ on the $k$ classes and, for each class $c$, a distribution $\theta_c$ on the vocabulary $V$. A document with token counts $(n_t)_{t \in V}$ and length $L = \sum_t n_t$ has
$$ p(x \mid c) = \frac{L!}{\prod_t n_t!} \prod_{t \in V} \theta_{c,t}^{\,n_t}. $$

**Claim 1 (the fit).** With $\alpha = 0$, line L3 and line L5 give the maximum likelihood estimates of $\pi$ and of each $\theta_c$ on the training set, when every class has at least one token. With $\alpha > 0$, line L5 gives the posterior mean of $\theta_c$ under a symmetric Dirichlet prior with parameter $\alpha$.

*Proof.* The log likelihood of the training set is
$$ \ell = \sum_c n_c \log \pi_c + \sum_c \sum_{t \in V} N_{c,t} \log \theta_{c,t} + \text{const}, $$
where the constant collects the multinomial coefficients, which do not depend on the parameters. The terms separate: one for $\pi$ and one for each $\theta_c$, each of the form $\sum_t a_t \log q_t$ over a probability vector $q$ with counts $a_t \ge 0$ and $A = \sum_t a_t > 0$. Let $\hat q_t = a_t / A$. For any probability vector $q$,
$$ \sum_t a_t \log \hat q_t - \sum_t a_t \log q_t = A \sum_t \hat q_t \log\frac{\hat q_t}{q_t} \ge 0, $$
because the sum on the right is a Kullback-Leibler divergence, which is not negative by Gibbs' inequality (it follows from $\log u \le u - 1$). So $\hat q$ maximizes the term. For $\pi$ this gives $n_c / n$ (line L3), and for $\theta_c$ it gives $N_{c,t} / \sum_{t'} N_{c,t'}$ (line L5 with $\alpha = 0$). For $\alpha > 0$: the Dirichlet distribution with parameters $(\alpha, \ldots, \alpha)$ is conjugate to the categorical counts, so the posterior of $\theta_c$ is Dirichlet with parameters $(N_{c,t} + \alpha)_t$, and its mean is $(N_{c,t} + \alpha)/(\sum_{t'} N_{c,t'} + \alpha |V|)$, which is line L5. $\square$

**Claim 2 (the prediction).** For a document whose tokens are all in $V$, line L7 returns $P(c \mid x)$ under the fitted model, and line L8 returns a class that maximizes it.

*Proof.* By Bayes' theorem, $P(c \mid x) = \pi_c p(x \mid c) / \sum_{c'} \pi_{c'} p(x \mid c')$. The multinomial coefficient is the same for each class and cancels, so
$$ P(c \mid x) = \frac{\pi_c \prod_t \theta_{c,t}^{n_t}}{\sum_{c'} \pi_{c'} \prod_t \theta_{c',t}^{n_t}} = \frac{e^{s_c}}{\sum_{c'} e^{s_{c'}}}, $$
because line L6 computes $s_c = \log \pi_c + \sum_t n_t \log \theta_{c,t}$ (a token that occurs $n_t$ times is added $n_t$ times). Let $m = \max_c s_c$. Then $\log \sum_{c'} e^{s_{c'}} = m + \log \sum_{c'} e^{s_{c'} - m}$, which is the value $Z$ of line L7, so $\exp(s_c - Z) = P(c \mid x)$. The map $u \mapsto e^{u - Z}$ is increasing, so a class with the largest $s_c$ has the largest posterior, and line L8 returns it. Tokens outside $V$ have no parameter; skipping them is the same as computing the posterior of the document restricted to $V$. $\square$

**Numerical safety.** In line L7 every exponent $s_{c'} - m$ is at most 0 and one of them is 0, so the sum is between 1 and $k$ and its logarithm is finite. The direct product $\prod_t \theta_{c,t}^{n_t}$ can underflow to 0 for long documents, but each $s_c$ is a finite sum of finite logarithms when $\alpha > 0$.

**Cost.** Lines L1 to L4 read each token once, line L5 costs one logarithm for each pair $(c, t)$, so training costs $\Theta(T + k|V|)$ for $T$ training tokens. Line L6 costs $\Theta(L)$ per class, and lines L7 and L8 cost $\Theta(k)$. $\square$
