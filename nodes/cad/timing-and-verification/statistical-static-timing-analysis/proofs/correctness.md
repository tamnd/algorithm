---
title: The canonical sum is exact, and Clark's statistical max keeps the mean, the variance and the covariance with each global source of the true max of two Gaussian inputs
proves: [Clark's moment formulas, exactness of the sum, the private term is real, exactness on chains, reduction to STA, running time]
status: full
---

**Setting.** Let $Z_1, \ldots, Z_m$ be independent standard normal variables (the global sources). A *canonical form* is a random variable
$$ X = \mu + \sum_{i=1}^m a_i Z_i + r R, $$
where $r \ge 0$ and $R$ is a standard normal variable that is independent of $Z_1, \ldots, Z_m$ and of the private variables of all other canonical forms in use. Its variance is $\sigma^2 = \sum_i a_i^2 + r^2$, and $\mathrm{Cov}(X, Z_i) = a_i$. For two canonical forms $A$ and $B$ with coefficients $a_i$ and $b_i$, the pair $(A, B)$ is jointly Gaussian with $\mathrm{Cov}(A, B) = \sum_i a_i b_i$. Write $\Phi$ and $\varphi$ for the standard normal distribution function and density.

What is proved here is a statement about each operation on Gaussian inputs. The statement that the arrival times of a whole DAG are close to the true distributions is not proved; the algorithm page reports it as a measurement.

**Lemma 1 (truncated moments).** Let $D = \mu_D + \theta U$ with $U$ standard normal, $\theta > 0$, and let $\alpha = \mu_D / \theta$. Then
$$ P(D > 0) = \Phi(\alpha), \qquad E[(D - \mu_D) \mathbf{1}\{D > 0\}] = \theta \varphi(\alpha), \qquad E[D^2 \mathbf{1}\{D > 0\}] = (\mu_D^2 + \theta^2) \Phi(\alpha) + \mu_D \theta \varphi(\alpha). $$

*Proof.* $D > 0$ if and only if $U > -\alpha$, which has probability $1 - \Phi(-\alpha) = \Phi(\alpha)$. Since $\varphi'(u) = -u \varphi(u)$, we get $E[U \mathbf{1}\{U > c\}] = \int_c^\infty u \varphi(u) \, du = \varphi(c)$, and by parts $E[U^2 \mathbf{1}\{U > c\}] = c \varphi(c) + 1 - \Phi(c)$. With $c = -\alpha$ and the symmetry of $\varphi$, the first moment gives $\theta \varphi(\alpha)$. For the second, $E[D^2 \mathbf{1}\{D > 0\}] = \mu_D^2 \Phi(\alpha) + 2 \mu_D \theta \varphi(\alpha) + \theta^2 (\Phi(\alpha) - \alpha \varphi(\alpha))$, and $\theta^2 \alpha = \mu_D \theta$, which gives the formula. $\square$

**Lemma 2 (regression on $D$).** Let $(Y, D)$ be jointly Gaussian with $\mathrm{Var}(D) = \theta^2 > 0$. Then $Y = \mu_Y + \beta (D - \mu_D) + W$ with $\beta = \mathrm{Cov}(Y, D) / \theta^2$, where $W$ has mean 0 and is independent of $D$. Consequently, for every function $f$ with $E|f(D)| < \infty$ and $E|D f(D)| < \infty$, $\mathrm{Cov}(f(D), Y) = \beta \, \mathrm{Cov}(f(D), D)$.

*Proof.* $W = Y - \mu_Y - \beta (D - \mu_D)$ is Gaussian with mean 0 and $\mathrm{Cov}(W, D) = \mathrm{Cov}(Y, D) - \beta \theta^2 = 0$. Jointly Gaussian variables with covariance 0 are independent. Then $\mathrm{Cov}(f(D), W) = 0$, which gives the second claim. $\square$

**Lemma 3.** With $D$ as in Lemma 1 and $D^+ = \max(D, 0)$, $\mathrm{Cov}(D^+, D) = \theta^2 \Phi(\alpha)$.

*Proof.* $\mathrm{Cov}(D^+, D) = E[D^2 \mathbf{1}\{D > 0\}] - \mu_D E[D \mathbf{1}\{D > 0\}]$. By Lemma 1, $E[D \mathbf{1}\{D > 0\}] = \mu_D \Phi(\alpha) + \theta \varphi(\alpha)$. Subtracting $\mu_D$ times this from the third formula of Lemma 1 leaves $\theta^2 \Phi(\alpha)$. $\square$

**Theorem 1 (Clark 1961).** Let $(A, B)$ be jointly Gaussian with means $\mu_A, \mu_B$, variances $\sigma_A^2, \sigma_B^2$ and covariance $c_{AB}$, with $\theta^2 = \sigma_A^2 + \sigma_B^2 - 2 c_{AB} > 0$. Let $\alpha = (\mu_A - \mu_B)/\theta$, $T = \Phi(\alpha)$ and $M = \max(A, B)$. Then $T = P(A > B)$ and
$$ E[M] = \mu_A T + \mu_B (1 - T) + \theta \varphi(\alpha), $$
$$ E[M^2] = (\mu_A^2 + \sigma_A^2) T + (\mu_B^2 + \sigma_B^2)(1 - T) + (\mu_A + \mu_B) \theta \varphi(\alpha), $$
and for every $Y$ such that $(A, B, Y)$ is jointly Gaussian,
$$ \mathrm{Cov}(M, Y) = T \, \mathrm{Cov}(A, Y) + (1 - T) \, \mathrm{Cov}(B, Y). $$

*Proof.* Let $D = A - B$, so $\mu_D = \mu_A - \mu_B$, $\mathrm{Var}(D) = \theta^2$ and $M = B + D^+$. Then $T = P(D > 0)$ by Lemma 1.

Mean: $E[M] = \mu_B + E[D^+] = \mu_B + \mu_D T + \theta \varphi(\alpha)$ by Lemma 1, which is the formula.

Covariance: $\mathrm{Cov}(M, Y) = \mathrm{Cov}(B, Y) + \mathrm{Cov}(D^+, Y)$. By Lemmas 2 and 3, $\mathrm{Cov}(D^+, Y) = \frac{\mathrm{Cov}(D, Y)}{\theta^2} \theta^2 T = T (\mathrm{Cov}(A, Y) - \mathrm{Cov}(B, Y))$. Adding $\mathrm{Cov}(B, Y)$ gives the formula.

Second moment: $E[M^2] = E[B^2] + 2 E[B D^+] + E[(D^+)^2]$. Here $E[B^2] = \mu_B^2 + \sigma_B^2$. By the covariance formula with $Y = B$ applied to $D^+ = M - B$, $\mathrm{Cov}(B, D^+) = T (c_{AB} - \sigma_B^2)$, so $E[B D^+] = T (c_{AB} - \sigma_B^2) + \mu_B (\mu_D T + \theta \varphi(\alpha))$. By Lemma 1, $E[(D^+)^2] = (\mu_D^2 + \theta^2) T + \mu_D \theta \varphi(\alpha)$. Collect terms. The terms with $\varphi$ are $(2 \mu_B + \mu_D) \theta \varphi(\alpha) = (\mu_A + \mu_B) \theta \varphi(\alpha)$. The terms with $T$ are $T$ times
$$ 2 c_{AB} - 2 \sigma_B^2 + 2 \mu_B \mu_D + \mu_D^2 + \sigma_A^2 + \sigma_B^2 - 2 c_{AB} = (\mu_A^2 - \mu_B^2) + (\sigma_A^2 - \sigma_B^2). $$
With $\mu_B^2 + \sigma_B^2$ from $E[B^2]$, this is the formula. $\square$

**Theorem 2 (the canonical max).** Let $A$ and $B$ be canonical forms with $\theta^2 > 0$, and let $C = \mathrm{MAX}(A, B)$ be the form built in lines L11 to L17: mean $E[M]$ and second moment $E[M^2]$ from Theorem 1, coefficients $c_i = T a_i + (1 - T) b_i$ and $r = \sqrt{E[M^2] - E[M]^2 - \sum_i c_i^2}$. Then the expression under the root is non-negative, and $C$ has the same mean, the same variance and the same covariance with each $Z_i$ as $M = \max(A, B)$. If $\theta = 0$, lines L9 and L10 return $M$ itself.

*Proof.* Each $(A, B, Z_i)$ is jointly Gaussian, so by Theorem 1 with $Y = Z_i$, $\mathrm{Cov}(M, Z_i) = T a_i + (1 - T) b_i = c_i$. The $Z_i$ are orthonormal in the space of square-integrable variables with the covariance as inner product, so Bessel's inequality gives $\sum_i \mathrm{Cov}(M, Z_i)^2 \le \mathrm{Var}(M) = E[M^2] - E[M]^2$. So $r$ is real. Then $E[C] = E[M]$, $\mathrm{Cov}(C, Z_i) = c_i = \mathrm{Cov}(M, Z_i)$ and $\mathrm{Var}(C) = \sum_i c_i^2 + r^2 = \mathrm{Var}(M)$. If $\theta = 0$, then $A - B$ has variance 0, so it is the constant $\mu_A - \mu_B$, and $M$ is $A$ when $\mu_A \ge \mu_B$ and $B$ otherwise. $\square$

The form $C$ is Gaussian and $M$ is not, unless $\theta = 0$ or one input almost surely exceeds the other. This is the only approximation of a single max step. A second one comes from the model: the private term of $C$ is treated as independent of all other private terms, although $M$ depends on the private terms of $A$ and $B$. On a DAG with reconvergent paths, both effects add up, and no bound on the total error is proved here.

**Theorem 3 (the sum).** For canonical forms $A$ and $B$, the form $\mathrm{ADD}(A, B)$ of lines L7 and L8, with mean $\mu_A + \mu_B$, coefficients $a_i + b_i$ and private coefficient $\sqrt{r_A^2 + r_B^2}$, has the same distribution as $A + B$, and the same joint distribution with $(Z_1, \ldots, Z_m)$.

*Proof.* $A + B = (\mu_A + \mu_B) + \sum_i (a_i + b_i) Z_i + (r_A R_A + r_B R_B)$. The last term is Gaussian with mean 0 and variance $r_A^2 + r_B^2$, and independent of the $Z_i$, so it has the same distribution as $\sqrt{r_A^2 + r_B^2} \, R$ for a new standard normal $R$ that is independent of the $Z_i$. $\square$

**Theorem 4 (chains are exact).** Suppose every vertex of the DAG has at most one in-edge, the start arrival times and the edge delays are canonical forms, and the private variables of all of them are independent. Then the arrival time that the algorithm computes at each vertex has the same joint distribution with $(Z_1, \ldots, Z_m)$ as the true arrival time, the sum of the delays on the unique path from a start point.

*Proof.* With one in-edge per vertex, line L5 never calls MAX. By induction along the topological order, the true arrival time at $v$ is $AT(u) + d(u, v)$, where $AT(u)$ depends only on the private variables of the edges on the path to $u$ and of its start point, which are independent of the private variable of $d(u, v)$. Theorem 3 applies at each step. $\square$

The same argument shows that the algorithm is exact in mean, variance and covariance with each $Z_i$ at a vertex where only one max is taken, of two path sums whose private variables are disjoint, as in the diamond example of the algorithm page.

**Theorem 5 (no variation gives STA).** If all coefficients and all private terms are 0, the algorithm computes the arrival times of [static timing analysis](/static-timing-analysis/).

*Proof.* All forms are constants. ADD adds the means. In MAX, $\theta = 0$, so lines L9 and L10 return the input with the larger mean, which is the max of two numbers. So lines L2 to L5 are lines L2 to L4 of STA. $\square$

**Theorem 6 (running time).** On a timing graph with $V$ vertices, $E$ edges and $m$ global sources, the algorithm takes $\Theta((V + E) \cdot m)$ arithmetic operations and evaluations of $\Phi$, $\varphi$ and the square root, and $\Theta(V m)$ extra space for the forms.

*Proof.* The topological order takes $\Theta(V + E)$. Each edge is used once in line L4 and at most once in line L5, and ADD and MAX each take $\Theta(m)$ operations and a constant number of function evaluations. Each vertex stores one form of size $m + 2$. $\square$

$\blacksquare$
