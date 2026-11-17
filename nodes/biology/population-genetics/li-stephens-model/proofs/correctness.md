---
title: The scaled forward pass computes the probability of the new haplotype in O(mK) time, and the backward, posterior and most likely path use the same structure
proves: [correctness]
status: full
---

**Setting.** Known haplotypes $h_1, \ldots, h_K$, a new haplotype $h$ over sites $1, \ldots, m$, switch probabilities $s_j = 1 - e^{-\rho_j / K} \in [0, 1)$ for $j = 1, \ldots, m - 1$, and emission probabilities $e_j(x) = P(h_j \mid X_j = x)$, which are $(K + \tilde\theta/2)/(K + \tilde\theta)$ or $(\tilde\theta/2)/(K + \tilde\theta)$. The transition is $T_j(x, y) = (1 - s_j)[x = y] + s_j / K$, and the start is uniform. With $\tilde\theta > 0$, every $e_j(x) > 0$.

**Lemma 1 (the model is a distribution).** Each row of $T_j$ sums to 1, and $e_j(x)$ summed over the two alleles of $h_j$ is 1.

*Proof.* $\sum_y T_j(x, y) = (1 - s_j) + K \cdot s_j / K = 1$, and all entries are at least $s_j / K \ge 0$. The two emission values add to $(K + \tilde\theta)/(K + \tilde\theta) = 1$. $\square$

**Lemma 2 (the forward recursion).** Let $A_j(x) = P(h_1, \ldots, h_j, X_j = x)$. Then $A_1(x) = e_1(x)/K$ and
$$A_{j+1}(y) = e_{j+1}(y)\Big[(1 - s_j) A_j(y) + \frac{s_j}{K} \sum_x A_j(x)\Big].$$

*Proof.* The first claim is the uniform start times the emission. For the second, condition on $X_j$: given $X_j = x$, the next state does not depend on $h_1, \ldots, h_j$, and $h_{j+1}$ depends only on $X_{j+1}$. So $A_{j+1}(y) = e_{j+1}(y) \sum_x A_j(x) T_j(x, y)$, and $\sum_x A_j(x) T_j(x, y) = (1 - s_j) A_j(y) + (s_j / K) \sum_x A_j(x)$. $\square$

**Theorem 1 (the scaled pass).** Let $\alpha_j$ and $c_j$ be the values after lines L2 and L7 at site $j$ in the code. Then $\alpha_j(x) = A_j(x) / P(h_1, \ldots, h_j)$, $c_j = P(h_j \mid h_1, \ldots, h_{j-1})$, and the returned value is $\log P(h)$.

*Proof.* By induction on $j$. At $j = 1$, line L1 computes $A_1$, and $c_1 = \sum_x A_1(x) = P(h_1)$, so $\alpha_1 = A_1 / P(h_1)$. Suppose the claim holds at $j$. Then $\sum_x \alpha_j(x) = 1$, so line L5 computes
$$e_{j+1}(y)\big[(1 - s_j)\alpha_j(y) + s_j/K\big] = \frac{e_{j+1}(y)\big[(1 - s_j) A_j(y) + (s_j/K) \sum_x A_j(x)\big]}{P(h_1, \ldots, h_j)} = \frac{A_{j+1}(y)}{P(h_1, \ldots, h_j)}$$
by Lemma 2. Its sum at line L6 is $P(h_1, \ldots, h_{j+1}) / P(h_1, \ldots, h_j) = P(h_{j+1} \mid h_1, \ldots, h_j) = c_{j+1}$, and line L7 divides by it, which gives $A_{j+1} / P(h_1, \ldots, h_{j+1})$. Finally $\prod_j c_j = P(h_1, \ldots, h_m) = P(h)$ by the chain rule, so the sum of $\log c_j$ is $\log P(h)$. Every $c_j > 0$ because every emission is positive, so the logarithms are defined. $\square$

**Theorem 2 (backward and posterior).** Let $B_j(x) = P(h_{j+1}, \ldots, h_m \mid X_j = x)$, with $B_m = 1$. The code computes $\beta_j = B_j / \prod_{t > j} c_t$, and $\alpha_j(x)\beta_j(x) = P(X_j = x \mid h)$.

*Proof.* Conditioning on $X_{j+1}$ gives $B_j(x) = \sum_y T_j(x, y) e_{j+1}(y) B_{j+1}(y) = (1 - s_j) e_{j+1}(x) B_{j+1}(x) + (s_j/K) \sum_y e_{j+1}(y) B_{j+1}(y)$. The code applies this to $\beta_{j+1}$ and divides by $c_{j+1}$, so by induction from $\beta_m = 1$ each $\beta_j$ equals $B_j / \prod_{t > j} c_t$. Then $\alpha_j(x) \beta_j(x) = A_j(x) B_j(x) / \prod_t c_t = P(h, X_j = x) / P(h)$. $\square$

**Theorem 3 (most likely path).** most_likely_path returns a path that maximizes $P(X_1, \ldots, X_m, h)$.

*Proof.* Let $V_j(x)$ be the largest log probability of a path ending in state $x$ at site $j$ together with $h_1, \ldots, h_j$. The Viterbi recursion is $V_{j+1}(x) = \log e_{j+1}(x) + \max_y [V_j(y) + \log T_j(y, x)]$. The transition takes only two values: $\log(1 - s_j + s_j/K)$ for $y = x$ and $\log(s_j/K)$ for $y \ne x$, and the first is at least the second. So the maximum is the larger of $V_j(x) + \log(1 - s_j + s_j/K)$ and $V_j(y^*) + \log(s_j/K)$, where $y^*$ maximizes $V_j$. If $y^* = x$, the first term wins, so it is correct to use $y^*$ even when it equals $x$. The code keeps the argument of the maximum as a pointer and traces the pointers back from the best final state, which gives a maximizing path by the usual argument for dynamic programming. $\square$

**Complexity.** Lines L4 to L7 cost $O(K)$ per site, because the sum over the previous state is replaced by the constant term $s/K$. So the forward pass takes $O(mK)$ time and $O(K)$ extra space beyond the stored vectors. The backward pass computes $\sum_y e_{j+1}(y)\beta_{j+1}(y)$ once per site, and the Viterbi pass finds $y^*$ once per site, so both are $O(mK)$. The reference function enumerate_likelihood sums over all $K^m$ paths and serves only to check these results on small inputs.
