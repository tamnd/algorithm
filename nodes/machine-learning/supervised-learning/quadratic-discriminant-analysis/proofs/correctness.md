---
title: QDA fits the Gaussian class model by maximum likelihood and returns the posterior argmax
proves: [correctness]
status: full
---

We use the pseudocode of the page. The model has priors $\pi_c$ and class densities $p(x \mid c) = \mathcal{N}(x; \mu_c, \Sigma_c)$ with $\Sigma_c$ symmetric positive definite.

**Claim 1 (the fit).** Let $\lambda = \gamma = 0$ and let every $W_c$ be positive definite. Then lines L2, L3 and L5 give the maximum likelihood estimates $\hat\pi_c = n_c / n$, $\hat\mu_c = \frac{1}{n_c}\sum_{y_i = c} x_i$ and $\hat\Sigma_c = W_c / n_c$.

*Proof.* The log likelihood of the training set is
$$ \ell = \sum_c n_c \log \pi_c + \sum_c \sum_{y_i = c} \Big( -\tfrac12 \log|\Sigma_c| - \tfrac12 (x_i - \mu_c)^{\top} \Sigma_c^{-1} (x_i - \mu_c) \Big) + \text{const}. $$
The prior term and the term of each class depend on disjoint parameters, so we maximize each one alone. The prior term $\sum_c n_c \log \pi_c$ over the probability simplex is maximized by $\pi_c = n_c/n$, by Gibbs' inequality: for any probability vector $\pi$, $\sum_c n_c \log(\hat\pi_c / \pi_c) = n \cdot \mathrm{KL}(\hat\pi \,\|\, \pi) \ge 0$.

Fix a class $c$ and write $P = \Sigma_c^{-1}$. For any $\mu$,
$$ \sum_{y_i = c} (x_i - \mu)^{\top} P (x_i - \mu) = \sum_{y_i = c} (x_i - \hat\mu_c)^{\top} P (x_i - \hat\mu_c) + n_c (\hat\mu_c - \mu)^{\top} P (\hat\mu_c - \mu), $$
because the cross terms sum to $2 (\hat\mu_c - \mu)^{\top} P \sum_{y_i = c} (x_i - \hat\mu_c) = 0$. The last term is at least 0, with equality only at $\mu = \hat\mu_c$, since $P$ is positive definite. So $\hat\mu_c$ maximizes the class term for every $\Sigma_c$. With $\mu = \hat\mu_c$, the quadratic sum equals $\operatorname{tr}(P W_c)$, and the class term is
$$ g(P) = \tfrac{n_c}{2} \log|P| - \tfrac12 \operatorname{tr}(P W_c). $$
Let $A = W_c^{1/2} P W_c^{1/2} / n_c$, which is positive definite with eigenvalues $a_1, \ldots, a_d > 0$. Then $\log|P| = \log|A| + d \log n_c - \log|W_c|$ and $\operatorname{tr}(P W_c) = n_c \operatorname{tr}(A)$, so
$$ g(P) = \tfrac{n_c}{2} \sum_{j=1}^d (\log a_j - a_j) + \text{const}. $$
The function $a \mapsto \log a - a$ has its only maximum at $a = 1$. So $g$ is maximized when $A = I$, that is $P = n_c W_c^{-1}$ and $\Sigma_c = W_c / n_c$. With $\lambda = \gamma = 0$, the formula of line L5 gives $S_c(0) = W_c / n_c$ and $\Sigma_c(0, 0) = S_c(0)$. $\square$

**Claim 2 (the factor is defined).** If $\lambda > 0$ and $W$ is positive definite, or if $W_c$ is positive definite, or if $\gamma > 0$ and $S_c(\lambda) \ne 0$, then $\Sigma_c(\lambda, \gamma)$ is positive definite and line L6 succeeds.

*Proof.* Each scatter matrix is a sum of outer products $v v^{\top}$, so it is positive semidefinite, and so is every $S_c(\lambda)$, a nonnegative combination of them divided by a positive number. A nonnegative combination of positive semidefinite matrices in which a positive definite matrix has a positive weight is positive definite. In the third case $\operatorname{tr} S_c(\lambda) > 0$, because a nonzero positive semidefinite matrix has a positive eigenvalue, so $\gamma \operatorname{tr}(S_c)/d \cdot I$ is positive definite. Every symmetric positive definite matrix has a unique lower triangular factor $L$ with positive diagonal and $L L^{\top} = \Sigma$, and the column by column recurrence of the implementation computes it: at column $j$ the value under the square root is the Schur complement pivot, which is positive (Golub and Van Loan, Section 4.2). $\square$

**Claim 3 (the prediction).** Lines L8 to L10 compute $\delta_c(x) = \log \pi_c + \log p(x \mid c) + \frac d2 \log 2\pi$, and line L11 returns a class with the largest posterior $P(c \mid x)$ under the fitted model.

*Proof.* From $\Sigma_c = L_c L_c^{\top}$ we get $|\Sigma_c| = |L_c|^2 = \prod_j L_c[j,j]^2$, because the determinant of a triangular matrix is the product of its diagonal. All diagonal entries are positive, so $\log|\Sigma_c| = 2 \sum_j \log L_c[j,j] = \ell_c$ (line L7). Also $\Sigma_c^{-1} = L_c^{-\top} L_c^{-1}$, so with $z = L_c^{-1}(x - \mu_c)$ (line L9),
$$ (x - \mu_c)^{\top} \Sigma_c^{-1} (x - \mu_c) = \big(L_c^{-1}(x - \mu_c)\big)^{\top} \big(L_c^{-1}(x - \mu_c)\big) = z^{\top} z . $$
So line L10 computes $-\frac12 \log|\Sigma_c| - \frac12 (x - \mu_c)^{\top}\Sigma_c^{-1}(x - \mu_c) + \log \pi_c$, which is $\log(\pi_c\, p(x \mid c))$ plus the constant $\frac d2 \log 2\pi$. By Bayes' theorem $P(c \mid x) = \pi_c\, p(x \mid c) / p(x)$, and $p(x)$ does not depend on $c$. The logarithm is increasing, so the classes with the largest $\delta_c$ are exactly the classes with the largest posterior, and line L11 returns one of them. $\square$

**Claim 4 (equal covariances give LDA).** If two classes $a$ and $b$ have $\Sigma_a = \Sigma_b = \Sigma$, then
$$ \delta_a(x) - \delta_b(x) = (\mu_a - \mu_b)^{\top} \Sigma^{-1} x - \tfrac12 (\mu_a + \mu_b)^{\top} \Sigma^{-1} (\mu_a - \mu_b) + \log\frac{\pi_a}{\pi_b}, $$
which is the linear discriminant of LDA. In particular, $\lambda = 1$ and $\gamma = 0$ give every class the pooled covariance $W/n$ and the LDA boundary.

*Proof.* The terms $-\frac12 \log|\Sigma|$ cancel. Expand $(x - \mu)^{\top} \Sigma^{-1} (x - \mu) = x^{\top} \Sigma^{-1} x - 2 \mu^{\top} \Sigma^{-1} x + \mu^{\top} \Sigma^{-1} \mu$, using the symmetry of $\Sigma^{-1}$. The terms $x^{\top} \Sigma^{-1} x$ cancel, and $\frac12(\mu_b^{\top} \Sigma^{-1} \mu_b - \mu_a^{\top} \Sigma^{-1} \mu_a) = -\frac12 (\mu_a + \mu_b)^{\top} \Sigma^{-1} (\mu_a - \mu_b)$. With $\lambda = 1$, $S_c(1) = W / n$ for every $c$. $\square$

**Cost.** Lines L3 and L4 cost $\Theta(n d)$ and $\Theta(n d^2)$. Line L5 costs $\Theta(k d^2)$, line L6 costs $\Theta(d^3)$ per class and line L7 costs $\Theta(d)$ per class. For one query, line L9 costs $\Theta(d^2)$ per class and line L10 costs $\Theta(d)$ per class. $\square$
