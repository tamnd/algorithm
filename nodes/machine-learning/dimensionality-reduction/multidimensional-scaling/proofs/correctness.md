---
title: Kruskal's alternating method never increases stress-1
proves: [correctness]
status: full
---

Let $P$ be the set of the $m = n(n-1)/2$ pairs $i < j$. For a configuration $X$ write $d_p = d_p(X)$, $S^*(X, \hat d) = \sum_{p \in P}(d_p - \hat d_p)^2$, $T^*(X) = \sum_{p \in P} d_p^2$, and $S = (S^*/T^*)^{1/2}$ for $T^* > 0$. Let $C$ be the set of the vectors $\hat d \in \mathbb{R}^P$ with $\hat d_p \le \hat d_q$ whenever $\delta_p < \delta_q$ (the primary approach). The set $C$ does not depend on $X$.

**Lemma 1 (isotonic regression in a fixed order).** For a list $y_1, \ldots, y_m$, pool adjacent violators returns the unique minimizer of $\sum_l (y_l - z_l)^2$ over $z_1 \le \cdots \le z_m$.

This is the correctness of the [pool adjacent violators](/pool-adjacent-violators/) algorithm, proved on its page. The test file checks it against the max-min formula $z_l = \max_{s \le l}\min_{t \ge l} \frac{1}{t - s + 1}\sum_{r=s}^{t} y_r$.

**Lemma 2 (ties sorted by distance).** Fix $X$. Let $\pi$ be the order of line L3: by $\delta_p$, and by $d_p$ inside a tie. Let $C_\pi \subseteq C$ be the set of the $\hat d$ that are non-decreasing along $\pi$. Then $\min_{C} S^*(X, \cdot) = \min_{C_\pi} S^*(X, \cdot)$, so the output $\hat d$ of line L4 minimizes $S^*(X, \cdot)$ and $S(X, \cdot)$ over $C$.

*Proof.* $C$ is closed, and $S^*(X, \cdot)$ is continuous and tends to infinity with $\|\hat d\|$, so a minimizer $z \in C$ exists. Suppose that $z \notin C_\pi$. Then there are two pairs $p, q$ in the same tie block with $d_p \le d_q$, $p$ before $q$ in $\pi$, and $z_p > z_q$. Swap $z_p$ and $z_q$ to get $z'$. It is still in $C$, because $C$ puts no constraint between members of a tie block, and the multiset of values that faces each other block is the same. The change of the objective is

$$(d_p - z_q)^2 + (d_q - z_p)^2 - (d_p - z_p)^2 - (d_q - z_q)^2 = 2(d_p - d_q)(z_p - z_q) \le 0 .$$

To see the identity, expand the squares: $d_p^2, d_q^2, z_p^2, z_q^2$ cancel, and the cross terms give $-2d_p z_q - 2d_q z_p + 2d_p z_p + 2d_q z_q = 2(d_p - d_q)(z_p - z_q)$. The sign follows from $d_p \le d_q$ and $z_p > z_q$. So $z'$ is also a minimizer. Swapping an inverted pair of a sequence lowers its number of inversions, so $z'$ has fewer inverted pairs inside the tie blocks than $z$. Repeating this a finite number of times gives a minimizer in $C_\pi$. Hence the minimum over $C_\pi$ is at most the minimum over $C$, and since $C_\pi \subseteq C$ the two minima are equal. By Lemma 1, line L4 finds the minimizer over $C_\pi$. Finally $T^*(X)$ does not depend on $\hat d$, so the same $\hat d$ minimizes $S(X, \cdot)$. $\square$

**Lemma 3 (the step).** If line L7 accepts the step $\alpha$, then $S(X', \hat d) < S(X, \hat d)$ for $X' = X - \alpha G$, and centering $X'$ does not change $S(X', \hat d)$.

*Proof.* The first claim is the acceptance test of line L7. Centering subtracts the same vector from each row, which leaves each $d_p$ unchanged, so $S^*$ and $T^*$ do not change. $\square$

**Theorem.** Let $S_t$ be the value of $S$ computed at line L5 in iteration $t$. Then $S_{t+1} < S_t$ for each iteration $t$ that reaches line L9. The sequence $(S_t)$ converges.

*Proof.* In iteration $t$, line L4 gives $\hat d^{(t)} \in C$ for the configuration $X_t$, and $S_t = S(X_t, \hat d^{(t)})$. By Lemma 3, the new configuration $X_{t+1}$ satisfies $S(X_{t+1}, \hat d^{(t)}) < S_t$. In iteration $t + 1$, $\hat d^{(t)}$ is still in $C$, and by Lemma 2 line L4 returns a minimizer over $C$ for $X_{t+1}$. So $S_{t+1} = S(X_{t+1}, \hat d^{(t+1)}) \le S(X_{t+1}, \hat d^{(t)}) < S_t$. A decreasing sequence bounded below by 0 converges. $\square$

**What the theorem does not say.** The limit of $S_t$ need not be the global minimum of $S$, and the configurations need not converge. The step of line L7 can also become too small to pass the test, in which case line L8 stops at a point that is only near a stationary point. The scale invariance $S(cX, c\hat d) = S(X, \hat d)$ for $c > 0$ follows from the homogeneity of $S^*$ and $T^*$ of degree 2, and it is the reason the denominator $T^*$ is present: without it, $X = 0$ with $\hat d = 0$ is a trivial minimizer.
