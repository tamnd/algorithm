---
title: The Berkowitz recurrence returns the characteristic polynomial
proves: [correctness, termination]
status: full
---

Let $R$ be a commutative ring and $A$ an $n \times n$ matrix over $R$, indexed from $0$ as in the pseudocode. For $0 \le r \le n - 1$ let $A_r$ be the trailing principal block in rows and columns $r, \dots, n-1$, of size $n - r$. Polynomials are stored as coefficient lists, highest degree first.

**Claim.** BERKOWITZ$(A)$ stops and returns the coefficients of $\chi_A(x) = \det(xI - A)$.

**Termination.** Line L3 runs $r$ over $n - 1$ values, the loop of line L6 has $s \le n - 1$ steps, and every other line is a finite computation on lists of length at most $n + 1$.

**Lemma 1 (adjugate of $xI - S$).** Let $S$ be an $s \times s$ matrix over $R$ with $s \ge 1$ and $\chi_S(x) = \sum_{k=0}^{s} c_k x^k$. Then

$$
\operatorname{adj}(xI - S) = \sum_{k=1}^{s} c_k \sum_{j=0}^{k-1} x^{k-1-j} S^j.
$$

*Proof.* Call the right side $Y(x)$, a matrix over $R[x]$. For each $k$, $(xI - S)\sum_{j=0}^{k-1} x^{k-1-j} S^j = x^k I - S^k$, a telescoping sum. So $(xI - S)\,Y(x) = \sum_{k=1}^{s} c_k (x^k I - S^k)$. The term for $k = 0$ would be $c_0(I - I) = 0$, so this sum equals $\sum_{k=0}^{s} c_k (x^k I - S^k) = \chi_S(x) I - \chi_S(S)$, and $\chi_S(S) = 0$ by the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), which holds over every commutative ring. Let $M = xI - S$. Multiply $M Y = \chi_S(x) I$ on the left by $\operatorname{adj}(M)$; since $\operatorname{adj}(M) M = \det(M) I = \chi_S(x) I$, we get $\chi_S(x)\, Y = \chi_S(x) \operatorname{adj}(M)$. The polynomial $\chi_S$ is monic, and a monic polynomial is not a zero divisor in $R[x]$ (the leading coefficient of a product $\chi_S \cdot f$ with $f \ne 0$ is the leading coefficient of $f$). So $Y = \operatorname{adj}(M)$. $\square$

**Lemma 2 (bordered determinant).** Let $\alpha \in R$, $\beta$ a row vector and $\gamma$ a column vector of length $s$, and $D$ an $s \times s$ matrix over $R$. Then

$$
\det \begin{pmatrix} \alpha & \beta \\ \gamma & D \end{pmatrix} = \alpha \det D - \beta \operatorname{adj}(D)\, \gamma.
$$

*Proof.* Both sides are polynomials with integer coefficients in the $(s+1)^2$ entries, so it suffices to prove the identity when the entries are independent indeterminates over $\mathbb{Z}$; every other case follows by substituting ring elements. In that case the entries lie in the field of fractions $F$ of the polynomial ring, and $\det D \ne 0$ because it is a nonzero polynomial. Row reduction with $D$ gives
$\begin{pmatrix} 1 & -\beta D^{-1} \\ 0 & I \end{pmatrix} \begin{pmatrix} \alpha & \beta \\ \gamma & D \end{pmatrix} = \begin{pmatrix} \alpha - \beta D^{-1} \gamma & 0 \\ \gamma & D \end{pmatrix}$.
The first factor has determinant $1$, and the last matrix is block lower triangular, so the determinant is $(\alpha - \beta D^{-1}\gamma)\det D = \alpha \det D - \beta \operatorname{adj}(D) \gamma$, using $D^{-1} = \operatorname{adj}(D)/\det D$ from [Cramer's rule](/cramers-rule/). $\square$

**Lemma 3 (one step).** Write $A_r = \begin{pmatrix} a & \rho \\ \gamma & S \end{pmatrix}$ with $a = A[r, r]$, $\rho$ the rest of row $r$, $\gamma$ the rest of column $r$ and $S = A_{r+1}$ of size $s = n - r - 1 \ge 1$. Let $m_j = \rho S^j \gamma$ for $j \ge 0$, and let $q = (q_0, \dots, q_{s+1}) = (1, -a, -m_0, -m_1, \dots, -m_{s-1})$. If $p = (p_0, \dots, p_s)$ holds the coefficients of $\chi_S$, highest first, then the coefficients of $\chi_{A_r}$, highest first, are

$$
p'_i = \sum_{t} q_t\, p_{i - t} \qquad (0 \le i \le s + 1),
$$

where the sum runs over the $t$ with $0 \le t \le s + 1$ and $0 \le i - t \le s$.

*Proof.* Apply Lemma 2 to $xI - A_r$ over the ring $R[x]$, with $\alpha = x - a$, $\beta = -\rho$, $\gamma' = -\gamma$ and $D = xI - S$:

$$
\chi_{A_r}(x) = (x - a)\chi_S(x) - \rho \operatorname{adj}(xI - S)\, \gamma.
$$

By Lemma 1, with $\chi_S = \sum_k c_k x^k$,
$\rho \operatorname{adj}(xI - S) \gamma = \sum_{k=1}^{s} c_k \sum_{j=0}^{k-1} x^{k-1-j} m_j$.
The coefficient of $x^e$ in it is $\sum_{j \ge 0} c_{e+1+j}\, m_j$, with $c_k = 0$ for $k > s$. So the coefficient of $x^e$ in $\chi_{A_r}$ is

$$
c_{e-1} - a\, c_e - \sum_{j=0}^{s-1} c_{e+1+j}\, m_j,
$$

with $c_{-1} = 0$. Put $e = s + 1 - i$ and $p_k = c_{s-k}$. The three parts become $q_0 p_i$, $q_1 p_{i-1}$ and $\sum_j q_{j+2}\, p_{i-2-j}$, where a term is absent when its index of $p$ is outside $0, \dots, s$. Their sum is $\sum_t q_t p_{i-t}$. $\square$

**Invariant.** After line L2, and after each iteration of line L3 with index $r$, the list $p$ holds the coefficients of $\chi_{A_{r'}}$, where $r'$ is $n - 1$ after line L2 and $r$ after the iteration.

*Initialization.* $A_{n-1}$ is the $1 \times 1$ matrix $(A[n-1, n-1])$, whose characteristic polynomial is $x - A[n-1, n-1]$, the list $(1, -A[n-1, n-1])$ of line L2.

*Maintenance.* In the iteration with index $r$, line L5 starts $q = (1, -a)$ and $v = \rho$. Before the step $k$ of line L6, $v = \rho S^k$: true for $k = 0$, and line L8 multiplies $v$ on the right by $S$. So line L7 appends $-v\gamma = -\rho S^k \gamma = -m_k$, and after the loop $q$ is exactly the vector of Lemma 3. The loop skips the last product $vS$, which is never used. By the invariant before the iteration, $p$ holds $\chi_S = \chi_{A_{r+1}}$, and line L9 forms the sums $p'_i$ of Lemma 3. So $p$ now holds $\chi_{A_r}$.

*End.* If $n = 0$, line L1 returns $(1)$, the characteristic polynomial of the empty matrix. Otherwise, after the last iteration ($r = 0$, or no iteration when $n = 1$), $p$ holds $\chi_{A_0} = \chi_A$, which line L10 returns. Only additions, subtractions and multiplications in $R$ were used. $\blacksquare$

**Remark.** Since $\chi_A(0) = \det(-A) = (-1)^n \det A$, the last coefficient times $(-1)^n$ is the determinant, which is how the implementation's `berkowitz_determinant` gets it.
