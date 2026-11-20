---
title: The Saltelli estimators of the first order and total variances are unbiased
proves: [correctness]
status: full
---

We assume exact arithmetic and exact random numbers. The input $\xi = (\xi_1, \ldots, \xi_d)$ has independent components, and $Q = f(\xi)$ is square integrable with $D = \mathrm{Var}(Q) > 0$. For a set $u$ of indices, $\xi_u$ is the vector of the components in $u$, and $\sim i$ is the set of all indices except $i$. The [Sobol indices](/sobol-indices/) are $S_i = V_i / D$ and $S_{Ti} = V_{Ti} / D$ with

$$V_i = \mathrm{Var}\big(\mathbb{E}[Q \mid \xi_i]\big), \qquad V_{Ti} = \mathbb{E}\big[\mathrm{Var}(Q \mid \xi_{\sim i})\big].$$

One row $j$ of the sample matrices gives two independent draws $a$ and $b$ of $\xi$ and, for each $i$, the mixed point $c^{(i)} = (a_{\sim i}, b_i)$: the row of $A$ with its component $i$ taken from $B$. Different rows are independent.

**Lemma 1 (a mixed point has the input law).** $c^{(i)}$ has the law of $\xi$. The pair $(b, c^{(i)})$ shares the component $i$ and nothing else, and the pair $(a, c^{(i)})$ shares all components except $i$.

*Proof.* The components of $c^{(i)}$ are $a_k$ for $k \ne i$ and $b_i$. They are independent, because they come from different components or from different draws, and each has the law of $\xi_k$. As the components of $\xi$ are independent, the joint law is the law of $\xi$. The other two claims hold by construction. $\square$

**Lemma 2 (the first order numerator).** $\mathbb{E}\big[f(b) \big(f(c^{(i)}) - f(a)\big)\big] = V_i$.

*Proof.* Let $g_i(x) = \mathbb{E}[Q \mid \xi_i = x]$. Given $b_i$, the values $f(b)$ and $f(c^{(i)})$ depend on the independent vectors $b_{\sim i}$ and $a_{\sim i}$, so they are conditionally independent with the same conditional mean $g_i(b_i)$. So $\mathbb{E}[f(b) f(c^{(i)})] = \mathbb{E}[g_i(b_i)^2]$. The draws $a$ and $b$ are independent, so $\mathbb{E}[f(b) f(a)] = \mathbb{E}[Q]^2 = \mathbb{E}[g_i(\xi_i)]^2$. The difference is $\mathbb{E}[g_i^2] - \mathbb{E}[g_i]^2 = \mathrm{Var}(g_i(\xi_i)) = V_i$. $\square$

**Lemma 3 (the total numerator of Jansen).** $\frac{1}{2} \mathbb{E}\big[\big(f(a) - f(c^{(i)})\big)^2\big] = V_{Ti}$.

*Proof.* Given $a_{\sim i}$, the values $f(a)$ and $f(c^{(i)})$ depend on the independent components $a_i$ and $b_i$, which have the same law. So they are conditionally independent and identically distributed with the variance $\mathrm{Var}(Q \mid \xi_{\sim i} = a_{\sim i})$. For two such variables $X, X'$, $\frac{1}{2}\mathbb{E}[(X - X')^2] = \mathrm{Var}(X)$. Take the expectation over $a_{\sim i}$. $\square$

**Theorem (unbiased numerators, consistent indices).** Lines L7 and L8 give the terms $t_{1, j} = f(b_j)(f(c^{(i)}_j) - f(a_j))$ and $t_{2, j} = \frac{1}{2}(f(a_j) - f(c^{(i)}_j))^2$ of rows $j = 1, \ldots, N$. Their means $\widehat{V}_i$ and $\widehat{V}_{Ti}$ are unbiased for $V_i$ and $V_{Ti}$. Line L3 gives an unbiased estimate $\widehat{D}$ of $D$. As $N \to \infty$, $\widehat{V}_i / \widehat{D} \to S_i$ and $\widehat{V}_{Ti} / \widehat{D} \to S_{Ti}$ almost surely.

*Proof.* The rows are independent, so the means are unbiased by Lemmas 2 and 3. The $2N$ values $f(a_j)$ and $f(b_j)$ are independent draws of $Q$, so their [sample variance](/sample-variance/) with the divisor $2N - 1$ is unbiased for $D$. The terms of each row are independent and identically distributed with a finite mean (the products and squares of square integrable variables are integrable), so the strong [law of large numbers](/law-of-large-numbers/) gives almost sure convergence of each mean. A ratio of two convergent sequences converges to the ratio of the limits when the limit of the denominator is $D > 0$. $\blacksquare$

The ratios are not unbiased for finite $N$, because the expectation of a ratio is not the ratio of the expectations. The bias is of order $1/N$, smaller than the standard error of order $N^{-1/2}$.

**Corollary (an input that the model ignores).** If $f$ does not depend on $\xi_i$, then $f(c^{(i)}_j) = f(a_j)$ for every row, so both estimates of input $i$ are exactly zero, for every $N$.

**Corollary (the run count).** The model runs on the rows of $A$, $B$ and the $d$ mixed matrices, which is $N(d + 2)$ runs. All $d$ first order and $d$ total estimates use these same runs.

**Error bars.** If $f(\xi)^2$ is square integrable, the terms $t_{1, j}$ and $t_{2, j}$ have finite variance, and by the [central limit theorem](/central-limit-theorem/) $\widehat{V}_i$ is approximately normal with the standard error $s(t_1)/\sqrt{N}$, where $s$ is the sample standard deviation of the terms. The code returns this standard error divided by $\widehat{D}$, and a relative standard error of $\widehat{D}$. The tests compare the estimates with the exact values within four times the sum of the two parts. These error bars are asymptotic, not bounds.

**What is not proved.** Lemma 1 needs independent inputs. If the components of $\xi$ are dependent, a mixed point $c^{(i)}$ does not have the law of $\xi$, the model is evaluated at inputs that the real system cannot take, and the estimates are not estimates of conditional variances.
