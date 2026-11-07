---
title: Every answer of the Risch-Norman heuristic is an antiderivative
proves: [correctness]
status: full
---

**Setting.** $K$ is a field of characteristic $0$ (in the code, $K = \mathbb{Q}$). The differential field is $E = K(x, \theta_1, \ldots, \theta_m)$ with derivation $'$, where $x' = 1$, the constants of $E$ are $K$, and $\theta_i' = N_i / d$ with $N_i \in K[x, \theta]$ and $0 \ne d \in K[x]$. The scaled derivation is $D = d \cdot {}'$, so on polynomials $D p = d\, \partial p / \partial x + \sum_i N_i\, \partial p / \partial \theta_i$, and $D$ maps $K[x, \theta]$ into itself. The input is $f = P / Q$ with $P, Q \in K[x, \theta]$, $Q = \prod_k q_k^{e_k}$ given by its factors, and a finite list of extra candidates. The output is FAIL or $(U, B, (c_j, v_j)_j)$ with $U, B, v_j \in K[x, \theta]$ and $c_j \in K$.

**Theorem.** (a) If the algorithm returns $(U, B, (c_j, v_j))$, then $B \ne 0$, every $v_j \ne 0$, and in any differential extension of $E$ that contains $\log v_j$ for each $j$ (elements $\ell_j$ with $\ell_j' = v_j' / v_j$),
$$\Bigl(\frac{U}{B} + \sum_j c_j \log v_j\Bigr)' = f.$$
(b) The algorithm returns FAIL exactly when no $U$ in the span of the monomials of total degree at most $\delta$ and no constants $c_j \in K$ satisfy (a) with the $B$ and the $v_j$ chosen in L1 and L2.

FAIL does not say that $f$ has no elementary integral. Part (b) only says that the search in the chosen finite family was complete.

## Lemma 1 (the derivative of the guess)

Let $W = \prod_j v_j$ over the candidates of L2, and for unknowns $u_\mu$ and $c_j$ in $K$, let $U = \sum_{|\mu| \le \delta} u_\mu\, x^{\mu_0} \theta^{\mu'}$. Then
$$d \cdot B^2 W Q \cdot \Bigl[\Bigl(\frac{U}{B} + \sum_j c_j \log v_j\Bigr)' - \frac{P}{Q}\Bigr] = Q W (DU \cdot B - U \cdot DB) + \sum_j c_j\, Dv_j\, B^2 Q \prod_{k \ne j} v_k - d P B^2 W.$$

*Proof.* The quotient rule holds for any derivation: $(U/B)' = (U' B - U B') / B^2$. Multiplying by $d$ turns $'$ into $D$ on polynomials, so $d (U/B)' = (DU \cdot B - U \cdot DB) / B^2$. For the logarithms, $d (\log v_j)' = d\, v_j' / v_j = D v_j / v_j$. Multiply the bracket by $d B^2 W Q$ and use $W / v_j = \prod_{k \ne j} v_k$. $\square$

## Lemma 2 (the linear system)

The right side of Lemma 1 is linear in the unknowns $(u_\mu, c_j)$: $D$ is $K$-linear because the constants of $E$ are $K$, and the products are with fixed polynomials. Write it as $\sum_\mu u_\mu\, \mathrm{col}_\mu + \sum_j c_j\, \mathrm{col}_j - \mathrm{rhs}$, where $\mathrm{col}_\mu = Q W (D(x^{\mu_0}\theta^{\mu'}) B - x^{\mu_0}\theta^{\mu'} DB)$, $\mathrm{col}_j = Dv_j\, B^2 Q \prod_{k \ne j} v_k$ and $\mathrm{rhs} = d P B^2 W$. These are the columns built in L5 and the right side built in L6. A polynomial is zero exactly when every coefficient is zero, so the right side of Lemma 1 vanishes exactly when the vector of unknowns solves the linear system with one equation for each monomial that occurs in some column or in $\mathrm{rhs}$. $\square$

## Lemma 3 (step L7)

Gauss-Jordan elimination over $K$ returns a solution of a linear system when one exists, and reports that none exists otherwise.

*Proof.* Each step swaps two rows, scales a row by a nonzero element of $K$, or adds a multiple of one row to another. These are invertible, so the solution set stays the same. At the end the matrix is in reduced row echelon form with pivot columns $p_1 < \cdots < p_r$. A row below the first $r$ has zero coefficients. If such a row has a nonzero right side, it reads $0 = c \ne 0$ and the system has no solution. Otherwise set every free unknown to $0$ and the pivot unknown of row $i$ to the right side of row $i$. Each of the first $r$ rows has a $1$ in its pivot column, zeros in the other pivot columns, and only free unknowns elsewhere, so every equation holds. All arithmetic is exact in $K$. $\square$

## Proof of the theorem

$B$ is a product of powers of the factors $q_k$ of $Q$. These are nonzero, since $Q$ is the denominator of $f$, so $B \ne 0$. The candidates $v_j$ are nonzero factors of $Q$ or nonzero extra polynomials, so $W \ne 0$. Also $d \ne 0$. So $d B^2 W Q \ne 0$, and the bracket in Lemma 1 is zero exactly when the right side of Lemma 1 is the zero polynomial.

(a) If L7 returns a vector, Lemma 3 says it solves the system, and Lemma 2 says that the right side of Lemma 1 is zero for it. Divide by $d B^2 W Q \ne 0$ in the field of fractions: the bracket is zero, which is the claim. Candidates with $c_j = 0$ are dropped from the output, and this does not change the sum.

(b) If some $U$ of total degree at most $\delta$ and some constants $c_j$ satisfy (a), then the bracket is zero, so by Lemma 1 and Lemma 2 their coefficients solve the system, and Lemma 3 returns a solution. Conversely, by (a), a returned vector gives such $U$ and $c_j$. So FAIL is returned exactly when no such choice exists.

The zero integrand gives $U = 0$, $B = 1$ and no logarithms, whose derivative is $0 = f$. $\blacksquare$

**Remark (what is not proved).** The theorem is about soundness. The choice of $B$ in L1 follows the structure of the integral in the purely transcendental case: a normal factor $q$ of multiplicity $e$ in $Q$ occurs with multiplicity at most $e - 1$ in the denominator of the rational part, as in Hermite reduction. The guess may still be too small in three ways. The degree bound $\delta$ can be too low. A special factor can need another exponent. The logarithmic part can need arguments that are not among the candidates, or constants $c_j$ outside $K$. In each case the algorithm returns FAIL although an elementary integral exists.
