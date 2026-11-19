---
title: The fast align normalizer is a sum of two geometric series, and its EM never lowers the likelihood
proves: [correctness]
status: full
---

Notation as on the page. A pair has the source $f_1 \ldots f_m$ and the target $e_1 \ldots e_l$, with $m, l \ge 1$ and the null word $e_0$. For $1 \le j \le m$ and $1 \le i \le l$ let $h(i) = h(i, j, m, l) = -|i/l - j/m|$, and for $\lambda \ge 0$ let $Z = \sum_{i=1}^{l} e^{\lambda h(i)}$. The distortion is $\delta(0) = p_0$ and $\delta(i) = (1 - p_0) e^{\lambda h(i)} / Z$ for $i \ge 1$, with $0 < p_0 < 1$.

## The normalizer

**Lemma 1.** Let $u = \lfloor j l / m \rfloor$ and $r = e^{-\lambda / l}$. Then

$$Z = \sum_{k=0}^{u-1} e^{\lambda h(u)} r^k + \sum_{k=0}^{l-u-1} e^{\lambda h(u+1)} r^k,$$

where an empty sum is 0. So $Z = s_u(e^{\lambda h(u)}, r) + s_{l-u}(e^{\lambda h(u+1)}, r)$ with $s_n(g, r) = g(1 - r^n)/(1 - r)$ for $r < 1$ and $s_n(g, 1) = g n$.

*Proof.* Since $1 \le j \le m$, we have $0 < j l / m \le l$, so $0 \le u \le l$. By the definition of the floor, $i / l \le j / m$ exactly when $i \le u$. For $1 \le i \le u$, $h(i) = i/l - j/m$, so $h(u - k) = h(u) - k/l$ and $e^{\lambda h(u-k)} = e^{\lambda h(u)} r^k$ for $k = 0, \ldots, u - 1$. These are the $u$ terms with $i \le u$. For $u + 1 \le i \le l$, $h(i) = j/m - i/l$, so $h(u + 1 + k) = h(u + 1) - k/l$ and $e^{\lambda h(u+1+k)} = e^{\lambda h(u+1)} r^k$ for $k = 0, \ldots, l - u - 1$. These are the other $l - u$ terms. Every $i$ in $1 \ldots l$ is in exactly one group. The closed form of $s_n$ is the finite geometric sum. $\square$

The count of the second series is $l - u$, the number of target positions after $u$. The implementation writes $s_n$ as $g \cdot \mathrm{expm1}(n \ln r) / \mathrm{expm1}(\ln r)$, which is the same number and has no cancellation near $r = 1$.

**Lemma 2.** $\sum_{i=0}^{l} \delta(i) = 1$, and every $\delta(i) > 0$.

*Proof.* $Z > 0$ as a sum of positive terms, and $\sum_{i \ge 1} (1 - p_0) e^{\lambda h(i)} / Z = 1 - p_0$. $\square$

**Lemma 3.** $\ln Z$ is a convex function of $\lambda$, and $\frac{d}{d\lambda} \ln Z = E_\lambda[h]$, the mean of $h(i)$ under the weights $e^{\lambda h(i)} / Z$.

*Proof.* $Z' = \sum_i h(i) e^{\lambda h(i)}$, so $(\ln Z)' = Z'/Z = E_\lambda[h]$. Then $(\ln Z)'' = E_\lambda[h^2] - E_\lambda[h]^2$, a variance, so it is $\ge 0$. $\square$

$E_\lambda[h]$ is also $O(1)$: the numerator $\sum_i h(i) e^{\lambda h(i)}$ splits into the same two groups as in Lemma 1, and in each group it is $\sum_k (a - k/l)\, g\, r^k$, an arithmetic-geometric sum with a closed form.

## The E step

The model is $p(f, a \mid e) = \prod_{j=1}^m \delta(a_j \mid j, m, l)\, \theta(f_j \mid e_{a_j})$ over all $a \in \{0, \ldots, l\}^m$ (the length of $f$ is given).

**Lemma 4.** $p(f \mid e) = \prod_{j=1}^m \sum_{i=0}^l \delta(i \mid j)\, \theta(f_j \mid e_i)$, and the posterior is $p(a \mid f, e) = \prod_j q_j(a_j)$ with $q_j(i) = \delta(i \mid j) \theta(f_j \mid e_i) / \sum_{i'} \delta(i' \mid j) \theta(f_j \mid e_{i'})$.

*Proof.* The sum over $a$ of a product of factors that each depend on one $a_j$ is the product of the sums, by the distributive law. Divide $p(f, a \mid e)$ by $p(f \mid e)$. $\square$

So the expected count of the link $(f_j, e_i)$ under the posterior is $q_j(i)$, which is what lines L5 and L6 compute. This costs $O(l)$ per source position, $O(l m)$ per pair, instead of a sum over $(l + 1)^m$ alignments.

## Monotonicity

Let $\phi = (\theta, \lambda)$ be the current parameters, and let

$$Q(\phi') = \sum_{\text{pairs}} \sum_{j} \sum_{i} q_j(i) \bigl( \ln \theta'(f_j \mid e_i) + \ln \delta'(i \mid j) \bigr),$$

with $q$ computed from $\phi$. The standard EM argument gives $L(\phi') - L(\phi) \ge Q(\phi') - Q(\phi)$, where $L$ is the log likelihood. It follows from [Jensen's inequality](/jensens-inequality/) applied to $\ln \sum_a p(a \mid f, e; \phi) \cdot p(f, a \mid e; \phi') / p(f, a \mid e; \phi)$. So it is enough that $Q(\phi') \ge Q(\phi)$.

$Q$ splits into a part in $\theta'$ and a part in $\lambda'$ ($p_0$ is fixed).

**Lemma 5.** Line L7 maximizes the $\theta'$ part.

*Proof.* For each target word $e$, the $\theta'$ part is $\sum_f c(f, e) \ln \theta'(f \mid e)$ with $\sum_f \theta'(f \mid e) = 1$. By Gibbs' inequality (the [Kullback-Leibler divergence](/kullback-leibler-divergence/) is non-negative) the maximum is at $\theta'(f \mid e) = c(f, e) / \sum_{f'} c(f', e)$. $\square$

**Lemma 6.** The $\lambda'$ part is $G(\lambda') = \lambda' S - \sum_{(j, m, l)} N_{j m l} \ln Z(j, m, l, \lambda') + \text{const}$, with $S = \sum q_j(i) h(i)$ over the links with $i \ge 1$ and $N_{jml}$ the posterior mass on $i \ge 1$ at the positions with these values. $G$ is concave, and its derivative $S - \sum N_{jml} E_{\lambda'}[h]$ is non-increasing.

*Proof.* $\ln \delta'(i) = \ln(1 - p_0) + \lambda' h(i) - \ln Z$ for $i \ge 1$, and $\ln \delta'(0) = \ln p_0$. Sum with the weights $q_j(i)$. Concavity and the derivative follow from Lemma 3 and $N_{jml} \ge 0$. $\square$

So line L8 can find the maximum of $G$ on $[0, \Lambda]$ by bisection on the sign of the derivative: if the derivative is $\le 0$ at 0 the maximum is at 0, if it is $\ge 0$ at $\Lambda$ the maximum is at $\Lambda$, and otherwise bisection converges to the root. The implementation keeps the new $\lambda'$ only if $G(\lambda') \ge G(\lambda)$, which holds for the exact maximizer and protects against the rounding of the bisection.

**Theorem.** One iteration of lines L3 to L8 gives parameters with a log likelihood at least that of the old ones.

*Proof.* By Lemma 5 the $\theta'$ part of $Q$ does not decrease, and by the test after line L8 the $\lambda'$ part does not decrease. So $Q(\phi') \ge Q(\phi)$, and $L(\phi') \ge L(\phi)$ by the EM inequality. $\square$

This is a theorem about the likelihood only. EM can stop at a local maximum, because the log likelihood of Model 2 is not concave in $(\theta, \lambda)$. On data that is exactly diagonal, $G$ grows without bound and the best $\lambda$ is $\Lambda$, the cap of the implementation.
