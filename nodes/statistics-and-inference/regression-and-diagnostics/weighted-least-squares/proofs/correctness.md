---
title: Weighted least squares by QR of the scaled rows computes the weighted estimate, which is the best linear unbiased estimator for known weights
proves: [correctness, termination]
status: full
---

The arithmetic is exact. The model is $y = Xb + \varepsilon$ with $X$ a fixed real $n \times p$ matrix, $\mathrm E[\varepsilon] = 0$ and $\operatorname{Cov}(\varepsilon) = \sigma^2 W^{-1}$, where $W = \operatorname{diag}(w_1, \dots, w_n)$ and every $w_i > 0$ is known. Rows with $w_i = 0$ are treated at the end. Write $W^{1/2} = \operatorname{diag}(\sqrt{w_i})$, $\tilde X = W^{1/2}X$ and $\tilde y = W^{1/2}y$, which is what lines L1 and L2 build. Assume $\operatorname{rank} X = p$; since $W^{1/2}$ is nonsingular, $\operatorname{rank}\tilde X = p$ too.

**Lemma 1 (the loop computes the weighted minimizer).** Lines L3 and L4 return the unique minimizer $\hat b$ of $S(\beta) = \sum_i w_i (y_i - x_i^\top\beta)^2$, and line L5 returns $S(\hat b)$.

*Proof.* $S(\beta) = \|\tilde y - \tilde X\beta\|^2$, because $w_i (y_i - x_i^\top\beta)^2 = (\sqrt{w_i}\,y_i - \sqrt{w_i}\,x_i^\top\beta)^2$. Line L3 computes $Q^\top\tilde X = \binom{R}{0}$ and $c = Q^\top\tilde y$ with $Q$ orthogonal and $R$ upper triangular and nonsingular (the Householder argument is Lemma 1 of the proof on the [F-test page](/regression-f-test/); it needs only rank $p$). Since $Q^\top$ keeps lengths, $S(\beta) = \|c_{1..p} - R\beta\|^2 + \sum_{i > p} c_i^2$. The first term is 0 exactly for $\beta = R^{-1}c_{1..p}$, which line L4 computes by back substitution, and is positive for every other $\beta$. So the minimizer is unique and the minimum is $\sum_{i > p} c_i^2$, the value of line L5. $\square$

**Lemma 2 (the closed form).** $\hat b = (X^\top W X)^{-1}X^\top W y$.

*Proof.* $S$ is a convex quadratic, and its gradient $-2X^\top W(y - X\beta)$ vanishes at the minimizer, so $X^\top W X\hat b = X^\top W y$. The matrix $X^\top W X = \tilde X^\top\tilde X = R^\top R$ is nonsingular. $\square$

**Lemma 3 (unbiased, and best).** $\mathrm E[\hat b] = b$ and $\operatorname{Cov}(\hat b) = \sigma^2 (X^\top W X)^{-1}$. For every linear unbiased estimator $\tilde b = Cy$ of $b$, $\operatorname{Cov}(\tilde b) - \operatorname{Cov}(\hat b)$ is positive semidefinite.

*Proof.* The scaled vector satisfies $\tilde y = \tilde X b + \tilde\varepsilon$ with $\tilde\varepsilon = W^{1/2}\varepsilon$, $\mathrm E[\tilde\varepsilon] = 0$ and $\operatorname{Cov}(\tilde\varepsilon) = W^{1/2}\sigma^2W^{-1}W^{1/2} = \sigma^2 I$. So the scaled model meets the hypotheses of the [Gauss-Markov theorem](/gauss-markov-theorem/), and by Lemma 1 $\hat b$ is its least squares estimate. Gauss-Markov gives unbiasedness, the covariance $\sigma^2(\tilde X^\top\tilde X)^{-1} = \sigma^2(X^\top WX)^{-1}$, and minimality among estimators linear in $\tilde y$ that are unbiased. A map $y \mapsto Cy$ is linear in $y$ exactly when $\tilde y \mapsto CW^{-1/2}\tilde y$ is linear in $\tilde y$, and the two give the same random vector, so the classes of linear unbiased estimators in the two models are the same. $\square$

**Lemma 4 (the variance estimate and exact intervals).** With all $n$ weights positive, $s^2 = S(\hat b)/(n - p)$ satisfies $\mathrm E[s^2] = \sigma^2$, and the matrix of line L7 is $s^2 (X^\top WX)^{-1}$. If in addition $\varepsilon$ is normal, then $(\hat b_j - b_j)/\sqrt{s^2[(X^\top WX)^{-1}]_{jj}}$ has the $t_{n-p}$ law for each $j$, so the intervals of `confidence_intervals` have coverage exactly $1 - \alpha$.

*Proof.* In the scaled model, $c_{p+1}, \dots, c_n$ are uncorrelated with mean 0 and variance $\sigma^2$, since $\operatorname{Cov}(Q^\top\tilde\varepsilon) = \sigma^2 I$ and $\mathrm E[Q^\top\tilde y] = \binom{Rb}{0}$. So $\mathrm E[\sum_{i > p}c_i^2] = (n - p)\sigma^2$. Line L7 forms $s^2R^{-1}R^{-\top} = s^2(R^\top R)^{-1} = s^2(X^\top WX)^{-1}$. Under normality the scaled model is the normal linear model with identity covariance, where $\hat b - b = R^{-1}(c_{1..p} - Rb)$ is a function of $c_1, \dots, c_p$ and $s^2$ of $c_{p+1}, \dots, c_n$; these are independent normal coordinates, $(n - p)s^2/\sigma^2 \sim \chi^2_{n-p}$, and the ratio has the $t_{n-p}$ law by definition. $\square$

**Zero weights.** A row with $w_i = 0$ adds 0 to $S(\beta)$ for every $\beta$, so the minimizer and the minimum are those of the fit without the row. Its variance $\sigma^2/w_i$ is infinite, so it carries no information and does not count in the residual degrees of freedom; line L1 skips it, and line L6 divides by $m - p$, where $m$ is the number of positive weights. The rank condition then applies to the rows with positive weight.

**Termination.** Line L1 runs over at most $n$ rows. The QR of line L3 has $p$ steps, each a finite sum over at most $n$ rows and $p$ columns, and lines L4 to L7 are finite sums. So the algorithm stops after $\Theta(np^2)$ operations for $n \ge p$.
