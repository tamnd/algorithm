---
title: A linear acyclic model with independent non-Gaussian errors is identified by the distribution of x, and DirectLiNGAM with an exact independence test returns a causal order and the weights; the Darmois-Skitovich theorem is cited
proves: [correctness, termination]
status: partial
---

**What is proved and what is cited.** This file proves that the weight matrix $B$ is identified (two such models with the same distribution of $x$ have the same $B$), and that DirectLiNGAM finds a causal order and $B$ when it can decide exactly whether two variables are independent. It cites the Darmois-Skitovich theorem. It does not prove that the implementation's choice step, which compares approximate entropies instead of testing independence, picks an exogenous variable; Hyvärinen and Smith (2013) show this for the exact likelihood ratio of two variables, and the tests measure it for the approximation.

**Setting.** The model is $x = Bx + e$ on $n$ variables. $B$ is the weight matrix of a DAG: $B_{ji} \ne 0$ means the edge $i \to j$, and the graph has no directed cycle, so some ordering of the variables (a causal order) makes $B$ strictly lower triangular. The errors $e_1, \dots, e_n$ are independent, with mean 0 and finite positive variances. Then $I - B$ is invertible (it is unit triangular in a causal order), and $x = Ae$ with $A = (I - B)^{-1}$. The entry $A_{jk}$ is the total effect of $e_k$ on $x_j$; $A_{jj} = 1$, and $A_{jk} = 0$ unless $k$ is an ancestor of $j$ or $k = j$.

**Theorem (Darmois 1953, Skitovich 1953; cited).** Let $e_1, \dots, e_n$ be independent random variables and $y_1 = \sum_k a_k e_k$, $y_2 = \sum_k c_k e_k$. If $y_1$ and $y_2$ are independent, then every $e_k$ with $a_k c_k \ne 0$ is Gaussian.

**Theorem 1 (identifiability).** Let $x = Bx + e = B'x + e'$, where both $B$ and $B'$ are weight matrices of DAGs, $e$ and $e'$ both have independent components with finite positive variances, and at most one component of $e$ is Gaussian. Then $B' = B$ and $e' = e$.

*Proof.* From $x = (I - B)^{-1}e$ and $e' = (I - B')x$ we get $e' = Me$ with $M = (I - B')(I - B)^{-1}$, an invertible matrix. Take two rows $r \ne s$. The components $e'_r = \sum_k M_{rk}e_k$ and $e'_s = \sum_k M_{sk}e_k$ are independent, so by Darmois-Skitovich $M_{rk}M_{sk} = 0$ for every $k$ with $e_k$ non-Gaussian. So each column $k$ of a non-Gaussian $e_k$ has at most one non-zero entry, and since $M$ is invertible, exactly one, in a row $\rho(k)$. Two such columns cannot share a row: they would both be multiples of the same unit vector, and $M$ would be singular.

If all $e_k$ are non-Gaussian, $\rho$ is a bijection and $M = PD$ for a permutation matrix $P$ and an invertible diagonal $D$. If exactly one $e_{k_0}$ is Gaussian, the $n - 1$ other columns fill $n - 1$ distinct rows, and the remaining row $r_0$ has its only non-zero entry in column $k_0$. Suppose $M_{r k_0} \ne 0$ for some $r \ne r_0$. Independent components with finite variances are uncorrelated, but $\operatorname{Cov}(e'_r, e'_{r_0}) = M_{rk_0}M_{r_0k_0}\operatorname{Var}(e_{k_0}) \ne 0$, since the other terms vanish. This contradiction shows that column $k_0$ also has one non-zero entry, and again $M = PD$.

So every row $i$ of $I - B' = PD(I - B)$ is a non-zero multiple $d_i$ of a row $\sigma(i)$ of $I - B$, for a permutation $\sigma$. The diagonal entry gives $1 = (I - B')_{ii} = d_i(I - B)_{\sigma(i)i}$, so $(I - B)_{\sigma(i)i} \ne 0$ for every $i$. If $\sigma(i) \ne i$, this entry is $-B_{\sigma(i)i}$, an edge $i \to \sigma(i)$. If $\sigma$ were not the identity, it would have a cycle $i, \sigma(i), \sigma^2(i), \dots, i$ of length at least 2, and these edges would form a directed cycle in the graph of $B$. So $\sigma$ is the identity, $d_i = 1$ for all $i$, $I - B' = I - B$, and $e' = e$. $\square$

With two or more Gaussian errors the theorem fails: the tests show that every order of three Gaussian variables gives a linear model with independent errors and the same covariance.

For the rest of the file, every $e_k$ is non-Gaussian. For variables $i \ne j$, the residual of $x_i$ on $x_j$ is $r_i^{(j)} = x_i - \frac{\operatorname{Cov}(x_i, x_j)}{\operatorname{Var}(x_j)}x_j$. A variable is exogenous when it has no parent.

**Lemma 2 (an exogenous variable is independent of its residuals).** If $x_m$ is exogenous, then $x_m$ is independent of $r_i^{(m)}$ for every $i \ne m$.

*Proof.* $x_m = e_m$. Write $x_i = \sum_k A_{ik}e_k$. Then $\operatorname{Cov}(x_i, x_m) = A_{im}\operatorname{Var}(e_m)$, so $r_i^{(m)} = x_i - A_{im}e_m = \sum_{k \ne m}A_{ik}e_k$, a function of errors other than $e_m$, and so independent of $e_m$. $\square$

**Lemma 3 (a variable with a parent has a dependent residual).** If $x_j$ has a parent, then $x_j$ and $r_i^{(j)}$ are dependent for some $i \ne j$.

*Proof.* Fix a causal order and let $p$ be the parent of $j$ that comes last in it. The other parents of $j$ come before $p$, so they are not descendants of $p$, and $e_p$ does not appear in them. In $x_j = \sum_q B_{jq}x_q + e_j$ the error $e_p$ appears only through $B_{jp}x_p$, so $A_{jp} = B_{jp} \ne 0$. Take $i = p$ and $c = \operatorname{Cov}(x_p, x_j)/\operatorname{Var}(x_j)$, so $r_p^{(j)} = x_p - cx_j$. The variable $x_p$ does not contain $e_j$, because $p$ is not a descendant of $j$. If $c \ne 0$, then $e_j$ has the coefficient $1$ in $x_j$ and $-c$ in $r_p^{(j)}$. If $c = 0$, then $r_p^{(j)} = x_p$, and $e_p$ has the coefficient $1$ in $x_p$ and $B_{jp}$ in $x_j$. In both cases one non-Gaussian error has non-zero coefficients in both variables, so by Darmois-Skitovich they are dependent. $\square$

**Lemma 4 (removing an exogenous variable).** Let $x_m$ be exogenous and $r_j = r_j^{(m)}$ for $j \ne m$. Then $r_j = \sum_{q \ne m}B_{jq}r_q + e_j$. So the residuals follow the same kind of model on the other variables, with the same weights and errors.

*Proof.* By Lemma 2, $r_j = x_j - A_{jm}x_m$. The total effects satisfy $A_{jm} = B_{jm} + \sum_{q \ne m}B_{jq}A_{qm}$, because every directed path from $m$ to $j$ ends with one edge into $j$ (and $A_{mm} = 1$). So

$$x_j = \sum_{q \ne m}B_{jq}(r_q + A_{qm}x_m) + B_{jm}x_m + e_j = \sum_{q \ne m}B_{jq}r_q + A_{jm}x_m + e_j,$$

and subtracting $A_{jm}x_m$ gives the claim. $\square$

**Theorem 5 (DirectLiNGAM with an exact test).** Replace the choice of line L7 by: choose a variable $m$ in $U$ that is independent of all its residuals $r_j^{(m)}$, $j \in U \setminus \{m\}$. Then such an $m$ always exists, the loop ends after $n - 1$ rounds, $K$ is a causal order, and the regressions of line L11 without the threshold return $B$.

*Proof.* By induction on the rounds, the current variables follow a model of the theorem's kind on $U$, with the weights of $B$ restricted to $U$: this holds at the start, and Lemma 4 keeps it after line L8. A DAG has a node with no parent, so by Lemma 2 a valid choice exists, and by Lemma 3 every valid choice has no parent among the current variables. In the restricted model, $m$ has no parent in $U$, so every edge of $B$ into $m$ starts at a variable that left $U$ earlier, and no edge goes from a later variable into $m$. Each round removes one variable, so there are $n - 1$ rounds, and $K$ is a causal order. In line L11, the regression of $x_j$ on the variables before it is $x_j = \sum_q B_{jq}x_q + e_j$ with $e_j$ independent of those variables, which are not descendants of $j$. As the covariance matrix of the variables before $j$ is positive definite, the least-squares coefficients are unique and equal the $B_{jq}$. $\square$

**What the implementation does instead.** Line L7 of the implementation chooses the $m$ that minimizes $\sum_j \min(0, R(m, j))^2$, where $R(m, j)$ is the log-likelihood ratio of the models $x_m \to x_j$ and $x_j \to x_m$, computed with an approximation of the differential entropy. Hyvärinen and Smith (2013) show that with exact entropies $R(m, j) > 0$ in the population when $x_m \to x_j$ is the true model of two variables (cited). The approximation has no such guarantee, and the threshold of line L11 drops small weights. The tests measure the result: with uniform errors the order was right in all 50 random models on five variables with 1000 samples.
