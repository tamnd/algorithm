---
title: The Luenberger observer error obeys e' = (A - LC) e, and the computed L gives A - LC the chosen characteristic polynomial
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$, and let $\alpha$ be a monic real polynomial of degree $n$.

## Lemma 1: the error equation

Let $x$ solve $\dot x = Ax + Bu$, $y = Cx$, and let $\hat x$ solve $\dot{\hat x} = A\hat x + Bu + L(y - C\hat x)$ with the same input $u$. Then $e = x - \hat x$ satisfies $\dot e = (A - LC)e$, so $e(t) = e^{(A - LC)t} e(0)$. In discrete time, $e_{k+1} = (A - LC) e_k$ and $e_k = (A - LC)^k e_0$.

*Proof.* Subtract the two equations: $\dot e = Ax - A\hat x - L(Cx - C\hat x) = (A - LC)e$, because the terms $Bu$ cancel. The solution of a linear system with constant matrix is given by the [matrix exponential](/matrix-exponential/). The discrete case is the same subtraction. $\square$

So $e(t) \to 0$ for every $e(0)$ if and only if $A - LC$ is Hurwitz (Schur in discrete time), and the input plays no role.

## Lemma 2: duality

$\det(sI - (A - LC)) = \det(sI - (A^T - C^T L^T))$, and $(C, A)$ is observable if and only if $(A^T, C^T)$ is controllable.

*Proof.* $(A - LC)^T = A^T - C^T L^T$, and a matrix and its transpose have the same determinant, so the same characteristic polynomial. The observability matrix of $(C, A)$ has the rows $C, CA, \dots, CA^{n-1}$; its transpose has the columns $C^T, A^T C^T, \dots, (A^T)^{n-1} C^T$, which is the controllability matrix of $(A^T, C^T)$. Both have the same rank. $\square$

So lines L1 and L2 are correct if PLACE is correct: if $K_d$ gives $\det(sI - (A^T - C^T K_d)) = \alpha(s)$, then $L = K_d^T$ gives $\det(sI - (A - LC)) = \alpha(s)$.

## Lemma 3: the construction of Hautus

Let $(\tilde A, \tilde B)$ be controllable with $\tilde B \in \mathbb{R}^{n \times q}$, and let $b$ be a nonzero column of $\tilde B$. Set $x_1 = b$. For $k = 1, \dots, n - 1$, if $\tilde A x_k \notin V_k = \operatorname{span}(x_1, \dots, x_k)$, set $u_k = 0$; otherwise choose a column $\tilde b_j \notin V_k$ and set $u_k = e_j$. Put $x_{k+1} = \tilde A x_k + \tilde B u_k$. Then the choice is always possible, $x_1, \dots, x_n$ are independent, and the matrix $F$ with $F x_k = u_k$ for $k < n$ and $F x_n = 0$ makes $(\tilde A + \tilde B F, b)$ controllable.

*Proof.* Suppose that for some $k < n$ neither choice works: $\tilde A x_k \in V_k$ and every column of $\tilde B$ is in $V_k$. For $i < k$, $\tilde A x_i = x_{i+1} - \tilde B u_i \in V_k$, and $\tilde A x_k \in V_k$, so $V_k$ is $\tilde A$-invariant. It contains $\operatorname{range} \tilde B$, so it contains $\tilde A^i \operatorname{range} \tilde B$ for all $i$, so it contains the controllable subspace, which is $\mathbb{R}^n$. This contradicts $\dim V_k = k < n$. When a choice works, $x_{k+1} \notin V_k$: either $\tilde A x_k \notin V_k$ and $u_k = 0$, or $\tilde A x_k \in V_k$ and $\tilde b_j \notin V_k$. So the vectors are independent, $X = [x_1, \dots, x_n]$ is invertible, and $F = U X^{-1}$ with $U = [u_1, \dots, u_{n-1}, 0]$ is the unique matrix with the stated values. Then $(\tilde A + \tilde B F) x_k = \tilde A x_k + \tilde B u_k = x_{k+1}$ for $k < n$, so $(\tilde A + \tilde B F)^{k} b = x_{k+1}$, and the controllability matrix of $(\tilde A + \tilde B F, b)$ is $X$, which is invertible. $\square$

The implementation tries $u_k = 0$ first and then the columns in order, which is one valid choice. It tests membership in $V_k$ by a rank computation, exactly for rational data. Note that $b \ne 0$ exists, because $\tilde B = 0$ would make the pair uncontrollable for $n \ge 1$.

## Lemma 4: PLACE is correct

Let $(\tilde A, \tilde B)$ be controllable, and let $F$, $b = \tilde B e_l$ be as in Lemma 3. Let $k_1$ be the Ackermann gain for the single-input pair $(\tilde A + \tilde B F, b)$ and $\alpha$. Then $K = -F + e_l k_1$ satisfies $\det(sI - (\tilde A - \tilde B K)) = \alpha(s)$.

*Proof.* $\tilde A - \tilde B K = \tilde A + \tilde B F - \tilde B e_l k_1 = (\tilde A + \tilde B F) - b k_1$. By Lemma 3, $(\tilde A + \tilde B F, b)$ is controllable, and the [Ackermann formula](/ackermann-formula/) page proves that $k_1$ gives this matrix the characteristic polynomial $\alpha$. $\square$

If PLACE cannot find a nonzero column or a new vector, Lemma 3 shows that the pair is not controllable, so by Lemma 2 $(C, A)$ is not observable, and the error raised is correct. If the pair is controllable, Lemma 3 shows that no failure occurs.

## Theorem

If $(C, A)$ is observable, the algorithm returns $L$ with $\det(sI - (A - LC)) = \alpha(s)$, and the observer of lines L3 and L4 has the error $e(t) = e^{(A - LC)t} e(0)$ for every input. If all roots of $\alpha$ have negative real parts (modulus less than 1 in discrete time), the error goes to 0 for every initial estimate. If $(C, A)$ is not observable, the algorithm raises an error.

*Proof.* Lemmas 1, 2 and 4. $\square$

## Remarks

- **Deadbeat observer.** With $\alpha(z) = z^n$, the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives $(A - LC)^n = 0$, so in discrete time $e_n = 0$ for every $e_0$ and every input sequence. The tests check this exactly in rational arithmetic.
- **Detectable but not observable.** By the [Kalman decomposition](/kalman-decomposition/), the unobservable eigenvalues are eigenvalues of $A - LC$ for every $L$. The algorithm raises an error in this case, although a stable $A - LC$ may exist if those eigenvalues are stable.
