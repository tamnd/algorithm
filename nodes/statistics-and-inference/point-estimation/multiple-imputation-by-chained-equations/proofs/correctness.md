---
title: MICE keeps the observed data, fills every cell, stops after m T q regressions, and with one incomplete column gives exact posterior predictive draws
proves: [correctness]
status: full
---

Line numbers refer to the `main` pseudocode. The table $Y$ has $n$ rows and $p$ columns. For a column $j$, $O_j$ is the set of rows where $Y_{ij}$ is observed and $M_j$ the set of rows where it is missing; the incomplete columns are the $q$ columns with $M_j \ne \emptyset$. The regression of column $j$ has the design matrix $X^{(j)}$ with a constant column and the $p - 1$ other columns, so it has $p$ coefficients. The preconditions are: for every incomplete column, $|O_j| > p$, and the rows of $X^{(j)}$ in $O_j$ have full column rank at every visit of line L5. The random numbers are taken to be exact draws from their laws.

**Lemma 1 (observed values never change).** At every point of the run, the working table has $Y_{ij}$ equal to the observed value for every $j$ and every $i \in O_j$.

*Proof.* The working table starts as a copy of the data. Only two lines write to it. Line L2 writes the entries $(i, j)$ with $i \in M_j$, and line L6 writes the entries $(i, j)$ with $i \in M_j$ for the current column $j$. No line writes an entry with $i \in O_j$. $\square$

**Lemma 2 (every cell is filled).** After line L2, every entry of the working table is a real number, and this stays true until line L7. So each stored table is complete.

*Proof.* Line L2 gives each entry with $i \in M_j$ a value from the observed values of column $j$, which exist because $|O_j| > p \ge 1$. The other entries are observed. Line L6 replaces a number with the real number $x_i^{\mathsf T}\beta^* + \sigma^* z$. No line writes a missing marker. $\square$

**Lemma 3 (the draw of line L5 is the exact posterior of a normal linear model).** Let $y \in \mathbb R^{k}$ and $X \in \mathbb R^{k \times p}$ have full column rank with $k > p$. Put $\hat\beta = (X^{\mathsf T}X)^{-1}X^{\mathsf T}y$ and $\mathrm{RSS} = \lVert y - X\hat\beta\rVert^2$. Under the model $y \mid \beta, \sigma \sim N(X\beta, \sigma^2 I_k)$ with the prior density $\pi(\beta, \sigma^2) \propto 1/\sigma^2$, the posterior is given by $\sigma^2 = \mathrm{RSS}/c$ with $c \sim \chi^2_{k-p}$, and then $\beta \mid \sigma^2 \sim N(\hat\beta, \sigma^2(X^{\mathsf T}X)^{-1})$. The step of line L5 draws $c$ as twice a Gamma variate with shape $(k - p)/2$ and $\beta^* = \hat\beta + \sigma^* L z$ with $LL^{\mathsf T} = (X^{\mathsf T}X)^{-1}$ and $z$ standard normal, so it draws from this posterior.

*Proof.* The identity $\lVert y - X\beta\rVert^2 = \mathrm{RSS} + (\beta - \hat\beta)^{\mathsf T}X^{\mathsf T}X(\beta - \hat\beta)$ holds because $X^{\mathsf T}(y - X\hat\beta) = 0$. The posterior density is therefore proportional to
$$(\sigma^2)^{-k/2 - 1}\exp\Bigl(-\frac{\mathrm{RSS}}{2\sigma^2}\Bigr)\exp\Bigl(-\frac{(\beta - \hat\beta)^{\mathsf T}X^{\mathsf T}X(\beta - \hat\beta)}{2\sigma^2}\Bigr).$$
For fixed $\sigma^2$, the last factor is the kernel of $N(\hat\beta, \sigma^2(X^{\mathsf T}X)^{-1})$, and its integral over $\beta$ is a constant times $(\sigma^2)^{p/2}$. So the marginal density of $\sigma^2$ is proportional to $(\sigma^2)^{-(k-p)/2 - 1}\exp(-\mathrm{RSS}/(2\sigma^2))$. The change of variable $c = \mathrm{RSS}/\sigma^2$ gives a density proportional to $c^{(k-p)/2 - 1}e^{-c/2}$, which is $\chi^2_{k-p}$. Twice a Gamma variate with shape $a$ and scale 1 is $\chi^2_{2a}$. The matrix $(X^{\mathsf T}X)^{-1}$ is positive definite, so its Cholesky factor $L$ exists, and $\hat\beta + \sigma^* Lz$ has mean $\hat\beta$ and covariance $\sigma^{*2}LL^{\mathsf T}$. $\square$

**Lemma 4 (one incomplete column gives exact draws for any T).** Suppose only column $j$ is incomplete. Then every visit of lines L5 and L6 draws the missing values of column $j$ from the posterior predictive law of the model of Lemma 3, fitted to the rows $O_j$ with the other columns as predictors. This law does not depend on the initial fill of line L2 or on the sweep number. So each stored table is one exact posterior predictive draw for every $T \ge 1$, and the $m$ tables are independent given the data.

*Proof.* With $q = 1$, the predictors of column $j$ are the other columns, which are complete and never change (Lemma 1). The response values in line L5 are the observed values $Y_{ij}$, $i \in O_j$. So the input of line L5 is the same at every visit, and by Lemma 3 the pair $(\beta^*, \sigma^*)$ is a draw from the posterior. Line L6 then draws $Y_{ij} = x_i^{\mathsf T}\beta^* + \sigma^* z_i$ with fresh independent $z_i$, which is a draw from the posterior predictive law of the missing responses: first the parameters from the posterior, then the data from the model. The values written in line L2 are overwritten in the first sweep and are never read as predictors, because column $j$ is not a predictor of itself. Each sweep and each imputation uses fresh random numbers, so the stored tables are independent draws. $\square$

Lemma 4 says that for one incomplete column MICE is the same procedure as normal linear regression imputation on the [multiple imputation](/multiple-imputation/) page, and the extra sweeps only cost time.

**Lemma 5 (predictive mean matching imputes observed values).** In the `pmm` variant, every value written for column $j$ is one of the observed values $Y_{kj}$, $k \in O_j$.

*Proof.* The variant replaces line L6 by a choice among the donors, which are rows of $O_j$, and writes the observed value of the chosen donor. Line L2 also writes observed values. $\square$

**Theorem (termination, cost and output).** The run stops after exactly $mTq$ executions of line L5. It returns $m$ complete tables, each equal to the data on all observed entries. If the table has one incomplete column, each returned table is an exact and independent draw of the missing values from the posterior predictive law of the normal linear regression model with the prior of Lemma 3.

*Proof.* The loops of lines L1, L3 and L4 have fixed ranges of $m$, $T$ and $q$ elements, and their bodies have no other loops except the loops over the finite sets $M_j$. So line L5 runs $mTq$ times and the run stops. Lemmas 1 and 2 give the form of the output, and Lemma 4 gives the law of the output when $q = 1$. $\blacksquare$

**What is not proved.** For two or more incomplete columns, the sweep of lines L3 to L6 defines a Markov chain on the missing values, and each conditional draw is exact given the current values of the other columns. But the $q$ regression models are specified one at a time, and in general there is no joint distribution whose full conditionals they are. Then the chain is not a [Gibbs sampler](/gibbs-sampling/) for any joint model, its stationary law can depend on the visiting order, and nothing above shows that it converges or what it converges to. When the conditional models are compatible with one joint model, Liu, Gelman, Hill, Su and Kropko (2014) give conditions under which the stationary law of such an iterative imputation is close to the posterior predictive law of that joint model in large samples. This page does not prove that result. The measured coverage on the main page is evidence for one data model only.
