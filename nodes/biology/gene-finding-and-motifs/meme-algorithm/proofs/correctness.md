---
title: Each EM iteration of MEME does not lower the objective, and the E step gives the site rule
proves: [correctness]
status: full
---

Let $X_1, \ldots, X_N$ be windows of length $L$ over the letters A, C, G, T, let $\mu(a) > 0$ and $\beta > 0$. A parameter $\phi = (\theta, \theta_0, \lambda)$ has $\theta_j$ and $\theta_0$ in the open simplex of four letters and $0 < \lambda < 1$. Write $p_1(x) = \prod_j \theta_j(x_j)$ and $p_0(x) = \prod_j \theta_0(x_j)$, and

$$F(\phi) = \sum_k \log(\lambda p_1(X_k) + (1 - \lambda) p_0(X_k)) + \beta \sum_a \mu(a) \Big(\sum_j \log \theta_j(a) + \log \theta_0(a)\Big).$$

**Lemma 1 (the E step).** Line L7 sets $z_k = \lambda p_1(X_k) / (\lambda p_1(X_k) + (1 - \lambda) p_0(X_k))$, the posterior probability that $X_k$ comes from the motif component, by Bayes' theorem. The code computes $r_k = \sum_j \log(\theta_j(X_{k,j})/\theta_0(X_{k,j})) - \log((1 - \lambda)/\lambda)$ and returns $1/(1 + e^{-r_k})$, which is the same number: divide the numerator and the denominator by $\lambda p_1(X_k)$.

**Corollary (the site rule).** $z_k > 1/2$ exactly when $r_k > 0$, that is, when the log odds score of $X_k$ is above $\log((1 - \lambda)/\lambda)$, since $1/(1 + e^{-r})$ is increasing and equals $1/2$ at $r = 0$.

**Lemma 2 (the M step maximizes Q).** For weights $z_k \in [0, 1]$, let

$$Q(\phi') = \sum_k \Big[ z_k \big(\log \lambda' + \log p'_1(X_k)\big) + (1 - z_k)\big(\log (1 - \lambda') + \log p'_0(X_k)\big) \Big] + \beta \sum_a \mu(a) \Big(\sum_j \log \theta'_j(a) + \log \theta'_0(a)\Big).$$

Then lines L8 and L9 give the unique maximizer of $Q$, apart from the clamp of $\lambda$.

*Proof.* $Q$ is a sum of separate parts. The part in $\lambda'$ is $S \log \lambda' + (N - S) \log(1 - \lambda')$ with $S = \sum_k z_k$; it is strictly concave and its derivative is 0 at $\lambda' = S/N$. The part in $\theta'_j$ is $\sum_a (c_j(a) + \beta\mu(a)) \log \theta'_j(a)$ with $c_j(a) = \sum_k z_k [X_{k,j} = a]$. For positive weights $w_a$, the function $\sum_a w_a \log p_a$ on the simplex has its unique maximum at $p_a = w_a / \sum_b w_b$: by Gibbs' inequality, $\sum_a w_a \log (p_a / \hat p_a) = (\sum_b w_b) \sum_a \hat p_a \log(p_a/\hat p_a) \le 0$ with $\hat p_a = w_a/\sum_b w_b$, with equality only at $p = \hat p$. Here $\sum_a (c_j(a) + \beta\mu(a)) = \sum_a c_j(a) + \beta$, since $\sum_a \mu(a) = 1$, so the maximum is line L9. The part in $\theta'_0$ is the same with $c_0(a) = \sum_k (1 - z_k) \#\{j : X_{k,j} = a\}$. $\square$

**Theorem (ascent).** Let $\phi$ be the parameters before an iteration, $z$ the weights of the E step at $\phi$, and $\phi'$ the result of the M step. Then $F(\phi') \ge F(\phi)$.

*Proof.* Let $z'_k$ be the E step weight at $\phi'$. For each $k$,

$$\log P_{\phi'}(X_k) = z_k \log \frac{\lambda' p'_1(X_k)}{z'_k} + (1 - z_k) \log \frac{(1 - \lambda') p'_0(X_k)}{1 - z'_k},$$

since $\lambda' p'_1(X_k) / z'_k = (1 - \lambda') p'_0(X_k)/(1 - z'_k) = P_{\phi'}(X_k)$. So $F(\phi') = Q(\phi') - \sum_k h_k(z'_k)$ with $h_k(y) = z_k \log y + (1 - z_k) \log (1 - y)$, and in the same way $F(\phi) = Q(\phi) - \sum_k h_k(z_k)$. By Gibbs' inequality, $h_k(y) \le h_k(z_k)$ for all $y$. So $F(\phi') - F(\phi) \ge Q(\phi') - Q(\phi) \ge 0$, the last step by Lemma 2. $\square$

**Corollary (convergence of the objective).** $F$ is bounded above: each $\log P(X_k) \le 0$, and each prior term is at most 0. So the values of $F$ along the run increase to a limit. The parameters converge to a stationary point of $F$ under the usual regularity conditions of EM, which in general is a local maximum, not the global one. Different starts can reach different local maxima.

**The clamp.** The code keeps $\lambda$ in $[10^{-12}, 1 - 10^{-12}]$. If the clamp is active, the $\lambda$ part of $Q$ is concave and the clamped value is its maximum over the clamped interval, so the ascent proof still holds on that interval.

**Cost.** The E step and the M step each look at every letter of every window a constant number of times, so an iteration takes $O(NL)$ time and $O(N + L)$ extra space.

The tests check the ascent on the BA2F sample and on random inputs, Lemma 1 against a direct use of Bayes' theorem, the site rule, and Lemma 2 against 200 random parameters and small moves away from the maximizer.
