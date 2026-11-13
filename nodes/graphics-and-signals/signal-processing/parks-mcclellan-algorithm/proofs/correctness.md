---
title: The levelled error is a lower bound for the optimum, it does not decrease under the exchange, and equality with the grid error means optimality
proves: [correctness]
status: full
---

We use the notation of the page. $F$ is the finite grid, ordered by frequency, $W > 0$ on $F$, and $\mathcal P_L$ is the set of amplitudes $A(\omega) = \sum_{k=0}^{L} a_k \cos(k\omega)$. With $x = \cos\omega$, each $A \in \mathcal P_L$ is a polynomial of degree at most $L$ in $x$, and $\omega \mapsto \cos\omega$ is strictly decreasing on $[0, \pi]$. For $A \in \mathcal P_L$ let $E_A = W(D - A)$ and $\|E_A\| = \max_F |E_A|$. Let $\delta^* = \min_{A \in \mathcal P_L} \|E_A\|$, which exists because the minimum of a continuous norm-like function over a finite-dimensional space is attained.

A reference set is $R = \{\omega_0 < \cdots < \omega_{L+1}\} \subset F$, with $x_k = \cos\omega_k$, which are distinct.

**Lemma 1 (sign changes).** Fix $\sigma \in \{\pm 1\}$. No $P \in \mathcal P_L$ has values $P(\omega_k)$ that are nonzero with sign $(-1)^k \sigma$ for all $k = 0, \ldots, L+1$. If $P(\omega_k)(-1)^k \sigma \ge 0$ for all $k$, then $P = 0$.

*Proof.* As a polynomial in $x$, $P$ would change sign between each of the $L + 1$ pairs of neighbours $x_k, x_{k+1}$, so it would have $L + 1$ distinct roots and degree at most $L$, so $P = 0$, which contradicts $P(\omega_k) \ne 0$. For the weak form, the divided difference of order $L + 1$ of $P$ on $x_0, \ldots, x_{L+1}$ is zero: $\sum_k b_k P(\omega_k) = 0$ with $b_k = 1/\prod_{i \ne k}(x_k - x_i)$. The $x_i$ with $i < k$ are larger than $x_k$, so the sign of $b_k$ is $(-1)^k$. Then all terms $b_k P(\omega_k)$ have the sign of $\sigma$ or are zero, and they add up to zero, so $P(\omega_k) = 0$ for all $k$, and $P = 0$ because it has $L + 2$ roots. $\square$

**Theorem 2 (lines L3 and L4).** For a reference set $R$, the system $A(\omega_k) + (-1)^k \delta / W(\omega_k) = D(\omega_k)$, $k = 0, \ldots, L+1$, has exactly one solution $(A, \delta)$ with $A \in \mathcal P_L$. Its $\delta$ is the value of line L3, and its $A$ is the polynomial of line L4. On $R$, $E_A(\omega_k) = (-1)^k \delta$.

*Proof.* Apply the divided difference of order $L + 1$ to $A(\omega_k) = D(\omega_k) - (-1)^k \delta / W(\omega_k)$. It kills $A$, so $0 = \sum_k b_k D(\omega_k) - \delta \sum_k b_k (-1)^k / W(\omega_k)$. Each $b_k (-1)^k$ is positive, so the second sum is positive, and $\delta$ is determined and equals line L3. For this $\delta$, line L4 takes the polynomial of degree at most $L$ through the $L + 1$ values at $\omega_0, \ldots, \omega_L$. Let $P$ be the polynomial of degree at most $L + 1$ through all $L + 2$ values; its leading coefficient is the divided difference above, which is zero, so $P$ has degree at most $L$ and equals the polynomial of line L4. So line L4 also takes the right value at $\omega_{L+1}$. Uniqueness: two solutions $(A, \delta)$ and $(A', \delta')$ have $\delta = \delta'$ by the formula, and then $A - A'$ vanishes at $L + 2$ points. Finally $E_A(\omega_k) = W(\omega_k)(D(\omega_k) - A(\omega_k)) = (-1)^k \delta$. $\square$

**Theorem 3 (de la Vallée Poussin bound).** Let $A \in \mathcal P_L$ and $R$ a reference set with $E_A(\omega_k) = (-1)^k \sigma e_k$, $e_k > 0$, for a fixed sign $\sigma$. Then every $B \in \mathcal P_L$ has $\max_k |E_B(\omega_k)| \ge \min_k e_k$. In particular, $\delta^* \ge \min_k e_k$, and for the reference set of Theorem 2, $|\delta| \le \delta^* \le \|E_A\|$.

*Proof.* Suppose $|E_B(\omega_k)| < \min_j e_j \le e_k$ for all $k$. Then $W(A - B)(\omega_k) = E_B(\omega_k) - E_A(\omega_k)$ has the sign of $-E_A(\omega_k)$, which is $-(-1)^k \sigma$, and it is nonzero. Since $W > 0$, $A - B \in \mathcal P_L$ has nonzero values with alternating signs at $L + 2$ points, which Lemma 1 rules out. For the last claim, $e_k = |\delta|$ for all $k$ when $\delta \ne 0$ (if $\delta = 0$ the bound is trivial), so $\|E_B\| \ge |\delta|$ for every $B$, that is $\delta^* \ge |\delta|$. And $\delta^* \le \|E_A\|$ by the definition of $\delta^*$. $\square$

**Theorem 4 (the stopping test).** If line L9 stops with $\|E_A\| = |\delta|$, then $A$ is the unique optimum on $F$: $\|E_A\| = \delta^*$, and every $B \in \mathcal P_L$ with $\|E_B\| = \delta^*$ equals $A$. If it stops with $\|E_A\| - |\delta| \le \varepsilon \|E_A\|$, then $\|E_A\| \le \delta^*/(1 - \varepsilon)$.

*Proof.* By Theorem 3, $|\delta| \le \delta^* \le \|E_A\| = |\delta|$, so $A$ is optimal. Let $B$ be optimal too. At each $\omega_k$, $|E_B(\omega_k)| \le \delta^* = |\delta|$ and $E_A(\omega_k) = (-1)^k \delta$, so $W(A - B)(\omega_k) = E_B(\omega_k) - E_A(\omega_k)$ is zero or has the sign of $-(-1)^k \operatorname{sign}\delta$. By the weak form of Lemma 1, $A - B = 0$. For the second claim, $(1 - \varepsilon)\|E_A\| \le |\delta| \le \delta^*$. $\square$

This is the alternation theorem on the grid in the direction that the algorithm needs: an error that reaches its maximum with alternating signs at $L + 2$ points is optimal. (The converse, that every optimum has such points, is the [Chebyshev equioscillation theorem](/chebyshev-equioscillation-theorem/) and is not needed for the test.)

**Theorem 5 (the levelled error does not decrease).** Let $(A, \delta)$ belong to a reference set $R$, and let the new set $R'$ of line L10 satisfy $E_A(\omega'_k) = (-1)^k \sigma e'_k$ with $e'_k \ge |\delta|$, for a fixed sign $\sigma$. Then the levelled error $\delta'$ of $R'$ satisfies $|\delta'| \ge \min_k e'_k \ge |\delta|$.

*Proof.* Let $b'_k$ be the weights of $R'$. Since $\sum_k b'_k A(\omega'_k) = 0$,

$$\sum_k b'_k D(\omega'_k) = \sum_k b'_k \big(D(\omega'_k) - A(\omega'_k)\big) = \sum_k b'_k \frac{E_A(\omega'_k)}{W(\omega'_k)} = \sigma \sum_k \frac{b'_k (-1)^k}{W(\omega'_k)} e'_k.$$

Divide by $\sum_k b'_k (-1)^k / W(\omega'_k)$. With $\lambda_k = \big(b'_k(-1)^k / W(\omega'_k)\big) / \sum_j b'_j (-1)^j / W(\omega'_j)$, which are positive and add up to 1, line L3 gives $\delta' = \sigma \sum_k \lambda_k e'_k$. So $|\delta'| = \sum_k \lambda_k e'_k \ge \min_k e'_k$. $\square$

The hypothesis of Theorem 5 is what lines L6 to L8 aim for. Each old reference point has $|E_A| = |\delta|$ and alternating sign, so each sign run of local extrema around it has a member with $|E_A| \ge |\delta|$, and line L7 keeps the largest member of each run, so the kept points alternate in sign. Line L8 removes points only at the ends, which keeps the alternation. When the hypothesis holds, the levelled errors form a non-decreasing sequence bounded by $\delta^*$, as the trace on the page shows ($0.01072$, $0.04429$, $0.05083$, $0.05086$). The implementation does not assume convergence: it stops after a fixed number of iterations, and the tests check the alternation and the bound of Theorem 4 on a dense grid. $\blacksquare$
