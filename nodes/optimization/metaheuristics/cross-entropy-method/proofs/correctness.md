---
title: The cross-entropy update is a maximum likelihood fit, keeps valid parameters, absorbs at 0 and 1, and depends only on the order of the scores
proves: [correctness]
status: full
---

We use the pseudocode of the page. In one iteration, the elite $E$ is a list of $k = \lceil \rho m \rceil$ samples, with repetitions allowed.

**Claim 1 (the update).** Line L5 maximizes $L(u) = \sum_{X \in E} \ln f(X; u)$. This is the same as minimizing the cross-entropy $H(q, f_u) = -\sum_x q(x) \ln f(x; u)$, and the Kullback-Leibler divergence $D(q \,\|\, f_u)$, where $q$ is the empirical distribution of $E$. For independent bits, $f(x; u) = \prod_j u_j^{x_j} (1 - u_j)^{1 - x_j}$, and the maximizer is $w_j = \frac{1}{k} \sum_{X \in E} X_j$. For a Gaussian with mean $\mu$ and a diagonal covariance with standard deviations $s_j$, the maximizer is the elite mean $\hat\mu_j = \frac1k \sum_{X \in E} X_j$ and $\hat s_j = \bigl(\frac1k \sum_{X \in E} (X_j - \hat\mu_j)^2\bigr)^{1/2}$, when every $\hat s_j > 0$.

*Proof.* Since $q(x)$ is the number of copies of $x$ in $E$ divided by $k$, $L(u) = -k\, H(q, f_u)$, and $D(q \,\|\, f_u) = H(q, f_u) - H(q)$, where the entropy $H(q)$ does not depend on $u$. So the three problems have the same solutions.

For bits, $L(u) = \sum_j \bigl(a_j \ln u_j + (k - a_j) \ln(1 - u_j)\bigr)$, where $a_j$ is the number of elite samples with $X_j = 1$. The terms are separate in $j$. For $0 < a_j < k$, the function $a \ln t + (k - a) \ln(1 - t)$ is strictly concave on $(0, 1)$ and goes to $-\infty$ at both ends, and its derivative $a/t - (k - a)/(1 - t)$ is 0 exactly at $t = a/k$. For $a_j = 0$ the term is $k \ln(1 - t)$, which is largest at $t = 0$, and for $a_j = k$ it is $k \ln t$, largest at $t = 1$. In all cases the maximizer is $w_j = a_j/k$.

For the Gaussian, $L(\mu, s) = \sum_j \bigl(-k \ln s_j - \frac{1}{2 s_j^2} \sum_{X \in E} (X_j - \mu_j)^2\bigr)$ plus a constant, again separate in $j$. For each fixed $s_j$, the sum of squares is smallest at $\mu_j = \hat\mu_j$, where it equals $k \hat s_j^2$. Then $-k \ln s - k \hat s^2/(2 s^2)$ has the derivative $-k/s + k \hat s^2/s^3$, which is positive for $s < \hat s$ and negative for $s > \hat s$, so the maximum is at $s = \hat s$. $\square$

When all elite values of a coordinate are equal, $\hat s_j = 0$ and the likelihood has no maximum. The rule of line L5 then takes the limit $\hat s_j = 0$, which the implementation computes.

**Claim 2 (valid parameters).** For bits, if $p \in [0, 1]^n$ then after line L6 $p \in [0, 1]^n$. For the Gaussian, the standard deviations stay $\ge 0$.

*Proof.* By Claim 1, $w_j = a_j/k \in [0, 1]$, and line L6 forms $\alpha w_j + (1 - \alpha) p_j$ with $\alpha \in (0, 1]$, a convex combination of two numbers in $[0, 1]$. For the Gaussian, $\hat s_j \ge 0$ and the convex combination of two numbers $\ge 0$ is $\ge 0$. $\square$

**Claim 3 (absorption).** For bits, if $p_j = 0$ before an iteration, then $p_j = 0$ after it, and the same holds for 1. For the Gaussian, if $s_j = 0$ before an iteration, then $s_j = 0$ and $\mu_j$ is unchanged after it.

*Proof.* If $p_j = 0$, every sample has $X_j = 0$, so every elite sample does, $a_j = 0$, $w_j = 0$, and line L6 gives $\alpha \cdot 0 + (1 - \alpha) \cdot 0 = 0$. The case $p_j = 1$ is the same with $a_j = k$. If $s_j = 0$, every sample has $X_j = \mu_j$, so $\hat\mu_j = \mu_j$ and $\hat s_j = 0$, and line L6 keeps both. $\square$

So once a bit is fixed, no later iteration can change it, whatever its effect on the score. If it is fixed at a value that no optimal solution has, the method can never sample an optimum again.

**Claim 4 (invariance).** Let $g$ be strictly increasing. With the same random numbers and the same rule for ties, the runs on $S$ and on $g \circ S$ give the same parameters and the same best solution.

*Proof.* By induction on $t$. If the parameters are the same before iteration $t$, line L3 gives the same samples. The order of the scores is the same, since $g(S(x)) > g(S(y))$ if and only if $S(x) > S(y)$, and equal scores stay equal, so line L4 picks the same elite and the same best sample. Lines L5 and L6 use only the elite samples and the old parameters, not the scores, so the new parameters are the same. $\square$
