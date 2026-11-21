---
title: PRAM draws from the rows of P, and the inverse of P gives unbiased counts
proves: [correctness]
status: full
---

The categories are $1, \ldots, K$. The PRAM matrix $P = (p_{kl})$ has $p_{kl} \ge 0$ and $\sum_l p_{kl} = 1$ for each $k$. The input is a list of $n$ values $x_1, \ldots, x_n$, and $T_k$ is the number of $i$ with $x_i = k$. Lines L1 to L9 are those of the page. Line L3 draws $u$ uniformly from $[0, 1)$, independently for each record. We write $c_{k0} = 0$ and $c_{kl} = p_{k1} + \cdots + p_{kl}$, so $c_{kK} = 1$.

**Lemma 1 (one draw).** For a record with $x_i = k$, lines L3 to L5 set $y_i = l$ with probability exactly $p_{kl}$.

*Proof.* Line L4 picks the least $l$ with $c_{kl} > u$. Since $c_{kK} = 1 > u$, such an $l$ exists. The least such $l$ is $l$ exactly when $c_{k,l-1} \le u < c_{kl}$, because the sums do not decrease. The probability of this interval under the uniform law is $c_{kl} - c_{k,l-1} = p_{kl}$. If $p_{kl} = 0$ the interval is empty, and $l$ is never chosen. $\square$

**Theorem 1 (the expected released counts).** Let $T^*_l$ be the number of $i$ with $y_i = l$, as at line L7. Then $\mathbb{E}[T^*] = P^{\mathsf T} T$, that is, $\mathbb{E}[T^*_l] = \sum_k p_{kl} T_k$.

*Proof.* $T^*_l = \sum_i [y_i = l]$. By Lemma 1 and the linearity of expectation, $\mathbb{E}[T^*_l] = \sum_i p_{x_i l} = \sum_k T_k p_{kl}$. $\square$

**Theorem 2 (the estimate).** If $P$ is invertible, the vector $\hat T$ of lines L8 and L9, the solution of $P^{\mathsf T} \hat T = T^*$, satisfies $\mathbb{E}[\hat T] = T$. Its covariance is $\mathrm{Cov}(\hat T) = (P^{\mathsf T})^{-1} V P^{-1}$, where $V = \sum_k T_k (\mathrm{diag}(p_k) - p_k p_k^{\mathsf T})$ and $p_k$ is row $k$ of $P$ as a column vector.

*Proof.* $P^{\mathsf T}$ is invertible together with $P$, so line L8 has the unique solution $\hat T = (P^{\mathsf T})^{-1} T^*$. This map is linear, so by Theorem 1, $\mathbb{E}[\hat T] = (P^{\mathsf T})^{-1} P^{\mathsf T} T = T$. The released indicator vectors $e_{y_i}$ are independent. For a record with value $k$, $e_{y_i}$ is a draw of a multinomial with one trial and probabilities $p_k$, with covariance $\mathrm{diag}(p_k) - p_k p_k^{\mathsf T}$. Summing over the records gives $\mathrm{Cov}(T^*) = V$, and a linear map $A$ gives $\mathrm{Cov}(A T^*) = A V A^{\mathsf T}$ with $A = (P^{\mathsf T})^{-1}$. $\square$

**Theorem 3 (invariant PRAM).** Let $\lambda_l = \sum_j p_{jl} T_j$. Define $Q = (q_{lk})$ by $q_{lk} = p_{kl} T_k / \lambda_l$ when $\lambda_l > 0$, and $q_{lk} = [k = l]$ when $\lambda_l = 0$. Then $R = P Q$ is a PRAM matrix, and $T^{\mathsf T} R = T^{\mathsf T}$. So PRAM with $R$ has $\mathbb{E}[T^*] = T$, and the released counts need no correction.

*Proof.* Each row of $Q$ is a probability vector: for $\lambda_l > 0$, $\sum_k p_{kl} T_k / \lambda_l = 1$, and for $\lambda_l = 0$ it is a unit vector. A product of two matrices whose rows are probability vectors has the same property, so $R$ is a PRAM matrix. Next, $(T^{\mathsf T} P)_l = \lambda_l$, so

$$(T^{\mathsf T} R)_k = \sum_l \lambda_l q_{lk} = \sum_{l : \lambda_l > 0} p_{kl} T_k = T_k \sum_{l : \lambda_l > 0} p_{kl}.$$

If $T_k = 0$ both sides are 0. If $T_k > 0$, then $p_{kl} > 0$ implies $\lambda_l \ge p_{kl} T_k > 0$, so the last sum runs over all $l$ with $p_{kl} > 0$ and equals 1. Hence $(T^{\mathsf T} R)_k = T_k$. By Theorem 1 with $R$ in place of $P$, $\mathbb{E}[T^*] = R^{\mathsf T} T = T$. $\square$

**Theorem 4 (local differential privacy).** Assume that each column of $P$ is either all zero or all positive, and let $c = \max_l \max_{k, k'} p_{kl} / p_{k'l}$ over the positive columns. Then the release of one record by lines L3 to L5 is $\varepsilon$-locally differentially private with $\varepsilon = \ln c$, and no smaller $\varepsilon$ holds. If some column has both a zero and a positive entry, no finite $\varepsilon$ holds.

*Proof.* By Lemma 1, the output law for the input $k$ is row $p_k$. For outputs $l$ in a positive column, $\Pr[y = l \mid k] = p_{kl} \le c\, p_{k'l} = c \Pr[y = l \mid k']$, and outputs in a zero column have probability 0 for every input. So the bound holds for every set of outputs, which is the definition with $e^{\varepsilon} = c$. The pair $k, k'$ and the column $l$ where the maximum is reached give equality, so a smaller $\varepsilon$ fails. If $p_{kl} > 0 = p_{k'l}$, the output $l$ is possible under $k$ and impossible under $k'$, and no factor $e^{\varepsilon}$ bounds the ratio. $\blacksquare$

**Remark.** Theorem 4 is about one record and the matrix only. The privacy of a release by PRAM in the sense of statistical disclosure control is a policy question, and the matrix is chosen by the agency. Theorem 2 is the reason why the matrix is published.
