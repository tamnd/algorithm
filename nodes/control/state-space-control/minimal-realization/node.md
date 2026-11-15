---
tag: 8B0AE4
kind: theorem
slug: minimal-realization
name: Minimal realization theorem
aliases:
- minimal realization
- irreducible realization
area: control/state-space-control
level: core
summary: A realization has the least state dimension if and only if it is controllable and observable, and all minimal realizations are similar.
prereqs: [kalman-decomposition, markov-parameters, transfer-function-matrix]
see_also: [realization-problem, ho-kalman-algorithm, eigensystem-realization-algorithm, smith-mcmillan-form, controllable-canonical-form, observable-canonical-form, balanced-realization, poles-and-zeros]
sources:
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: a realization is irreducible if and only if it is controllable and observable, and irreducible realizations are unique up to a change of coordinates
  - paper: doi:10.1137/0301009
    title: Elmer G. Gilbert, Controllability and observability in multivariable control systems, SIAM Journal on Control 1(2), 128-151, 1963
    locator: the minimal order of a transfer matrix with simple poles as the sum of the ranks of its residues
  - paper: doi:10.1137/0113034
    title: R. E. Kalman, Irreducible realizations and the degree of a rational matrix, Journal of the Society for Industrial and Applied Mathematics 13(2), 520-544, 1965
    locator: the minimal order of a realization equals the McMillan degree of the transfer matrix
  - paper: doi:10.1524/auto.1966.14.112.545
    title: B. L. Ho and R. E. Kalman, Effective construction of linear state-variable models from input/output functions, Regelungstechnik 14, 545-548, 1966
    locator: the minimal order as the rank of the Hankel matrix of the Markov parameters, and the construction of a minimal realization from it
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 7.2 (minimal realizations of scalar transfer functions and coprimeness), Section 7.6 (degree of transfer matrices) and Section 7.7 (minimal realizations in the matrix case)
---

The minimal realization theorem says that a state-space realization of a transfer matrix has the fewest possible states exactly when it is controllable and observable, and that any two such realizations differ only by a change of state coordinates. The least number of states is the rank of the Hankel matrix of the Markov parameters, which equals the McMillan degree. The theorem describes what a minimal realization is. The [realization problem](/realization-problem/) asks whether a realization exists at all, and the [Ho-Kalman algorithm](/ho-kalman-algorithm/) (exact data) and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) (noisy data, with a truncated SVD) are methods that compute one.

## Statement

**Notation.** $G(s)$ is a proper rational $p \times m$ transfer matrix. A *realization* of order $n$ is a quadruple $(A, B, C, D)$ with $A \in \mathbb{R}^{n \times n}$ and $G(s) = C (sI - A)^{-1} B + D$. Then $D = G(\infty)$, and the [Markov parameters](/markov-parameters/) $h_k = C A^{k-1} B$ for $k \ge 1$ are the coefficients of $G(s) - D = \sum_{k \ge 1} h_k s^{-k}$, so they depend only on $G$. The block Hankel matrix with $N$ block rows and columns is

$$H_N = \begin{bmatrix} h_1 & h_2 & \cdots & h_N \\ h_2 & h_3 & \cdots & h_{N+1} \\ \vdots & & & \vdots \\ h_N & h_{N+1} & \cdots & h_{2N-1} \end{bmatrix}.$$

A realization is *minimal* if no realization of $G$ has a smaller order.

**Theorem (Kalman 1963).** Let $(A, B, C, D)$ be a realization of $G$ of order $n$.

1. It is minimal if and only if $(A, B)$ is controllable and $(C, A)$ is observable.
2. The minimal order is $n_{\min} = \operatorname{rank} H_N$ for every $N \ge n$, and this is also the McMillan degree of $G$, the sum of the degrees of the denominators in its [Smith-McMillan form](/smith-mcmillan-form/) (Kalman 1965).
3. If $(A_1, B_1, C_1, D)$ and $(A_2, B_2, C_2, D)$ are both minimal, there is exactly one invertible $T$ with $A_2 = T A_1 T^{-1}$, $B_2 = T B_1$ and $C_2 = C_1 T^{-1}$. It is $T = \mathcal{O}_2^{+} \mathcal{O}_1$, where $\mathcal{O}_i$ is the observability matrix of $(C_i, A_i)$ and $\mathcal{O}_2^{+} = (\mathcal{O}_2^T \mathcal{O}_2)^{-1} \mathcal{O}_2^T$.

For a scalar $G = b/a$ with $b$ and $a$ coprime, the minimal order is $\deg a$.

## In plain words

Many different state models can have the same input to output behavior. Some of them carry extra states that the input never moves or that the output never shows. Such states can be removed without changing the behavior, so those models are not as small as they could be. The theorem says that this is the only way a model can be too large: a model in which every state can be reached and every state can be seen already has the fewest states possible. It also says that all smallest models are the same model in different coordinates, so the smallest model is unique in every way that matters. The number of states it needs can be read from the impulse response alone, as the rank of a matrix built from it.

## Proof

*Step 1: the Hankel matrix factors.* Let $\mathcal{O}_N = [C; CA; \dots; CA^{N-1}]$ and $\mathcal{C}_N = [B, AB, \dots, A^{N-1} B]$. The block $(i, j)$ of $\mathcal{O}_N \mathcal{C}_N$ is $C A^{i-1} A^{j-1} B = h_{i+j-1}$, so $H_N = \mathcal{O}_N \mathcal{C}_N$. In the same way the shifted Hankel matrix $H_N^{\sigma}$ with blocks $h_{i+j}$ is $\mathcal{O}_N A\, \mathcal{C}_N$. Both depend only on $G$.

*Step 2: every realization bounds the rank.* For any realization of order $n'$, $\operatorname{rank} H_N \le n'$ for every $N$, because $\mathcal{O}_N$ has $n'$ columns.

*Step 3: controllable and observable implies minimal.* Let $(A, B)$ be controllable and $(C, A)$ observable, and $N \ge n$. Then $\mathcal{O}_N$ has rank $n$ (full column rank) and $\mathcal{C}_N$ has rank $n$ (full row rank), so $H_N = \mathcal{O}_N \mathcal{C}_N$ has rank $n$: if $\mathcal{O}_N \mathcal{C}_N z = 0$ then $\mathcal{C}_N z = 0$, so the kernel of $H_N$ is that of $\mathcal{C}_N$. By Step 2 every realization has order at least $n$, so this one is minimal, and $n_{\min} = \operatorname{rank} H_N$.

*Step 4: minimal implies controllable and observable.* If $(A, B)$ is not controllable or $(C, A)$ is not observable, the [Kalman decomposition](/kalman-decomposition/) gives the realization $(A_{11}, B_1, C_1, D)$ of the same $G$ with order $n_1 < n$. So the realization was not minimal.

Steps 3 and 4 prove part 1, and with Step 2 they give $n_{\min} = \operatorname{rank} H_N$ for $N \ge n$: a realization of order $n$ reduces by Step 4 to a minimal one of order $n_{\min} \le n$, which by Step 3 has $\operatorname{rank} H_N = n_{\min}$.

*Step 5: similarity.* Let both realizations be minimal of order $n$, and write $\mathcal{O}_i$, $\mathcal{C}_i$ for their matrices with $n$ block rows or columns. By Step 1, $\mathcal{O}_1 \mathcal{C}_1 = \mathcal{O}_2 \mathcal{C}_2$ and $\mathcal{O}_1 A_1 \mathcal{C}_1 = \mathcal{O}_2 A_2 \mathcal{C}_2$. Let $\mathcal{O}_2^{+}$ be the left inverse above and $\mathcal{C}_2^{+} = \mathcal{C}_2^T (\mathcal{C}_2 \mathcal{C}_2^T)^{-1}$ a right inverse. Put $T = \mathcal{O}_2^{+} \mathcal{O}_1$ and $S = \mathcal{C}_1 \mathcal{C}_2^{+}$. Then

- $T \mathcal{C}_1 = \mathcal{O}_2^{+} \mathcal{O}_2 \mathcal{C}_2 = \mathcal{C}_2$, and $\mathcal{O}_1 S = \mathcal{O}_2 \mathcal{C}_2 \mathcal{C}_2^{+} = \mathcal{O}_2$;
- $T S = \mathcal{O}_2^{+} \mathcal{O}_1 \mathcal{C}_1 \mathcal{C}_2^{+} = \mathcal{O}_2^{+} \mathcal{O}_2 \mathcal{C}_2 \mathcal{C}_2^{+} = I$, so $T$ is invertible and $S = T^{-1}$;
- the first block column of $T \mathcal{C}_1 = \mathcal{C}_2$ gives $T B_1 = B_2$, and the first block row of $\mathcal{O}_1 T^{-1} = \mathcal{O}_2$ gives $C_1 T^{-1} = C_2$;
- $A_2 = \mathcal{O}_2^{+} (\mathcal{O}_2 A_2 \mathcal{C}_2) \mathcal{C}_2^{+} = \mathcal{O}_2^{+} \mathcal{O}_1 A_1 \mathcal{C}_1 \mathcal{C}_2^{+} = T A_1 T^{-1}$.

If $T'$ is another such matrix, then $\mathcal{O}_1 = \mathcal{O}_2 T'$, and multiplying by $\mathcal{O}_2^{+}$ gives $T' = T$.

*Step 6: the scalar case.* For $G = b/a$ in lowest terms with $\deg a = r$, the [controllable canonical form](/controllable-canonical-form/) of order $r$ is controllable, and it is observable because $a$ and $b$ have no common root. By part 1 it is minimal, so $n_{\min} = r$.

The identity of $n_{\min}$ with the McMillan degree in part 2 is proved by Kalman (1965) from the Smith-McMillan form, and is not repeated here. $\blacksquare$

## Consequences

- **Poles are eigenvalues.** For a minimal realization, the poles of $G$, with their McMillan multiplicities, are exactly the eigenvalues of $A$. For a non-minimal realization, $A$ has extra eigenvalues: the hidden modes of the [Kalman decomposition](/kalman-decomposition/).
- **Stability.** For a minimal realization, $G$ has all its poles in the open left half plane if and only if $A$ is Hurwitz. So for minimal realizations, input-output stability and internal asymptotic stability agree. For non-minimal ones they can differ.
- **Reduction.** Any realization reduces to a minimal one by removing the uncontrollable part and then the unobservable part.
- **Gilbert's formula.** If $G(s) = D + \sum_{i=1}^{q} R_i / (s - p_i)$ with distinct poles $p_i$ and constant residue matrices $R_i$, the minimal order is $\sum_i \operatorname{rank} R_i$ (Gilbert 1963).
- **Discrete time.** The theorem is the same for $x_{k+1} = A x_k + B u_k$, where the Markov parameters are the impulse response samples.
- **Numerical rank.** Deciding the minimal order from data means deciding the rank of $H_N$, which is unstable under small errors. The [Hankel singular values](/hankel-singular-values/) of a realization measure how close it is to one of lower order, and the [eigensystem realization algorithm](/eigensystem-realization-algorithm/) truncates them.

**Worked example.** $G(s) = 1/((s + 1)(s + 2))$ has the Markov parameters $0, 1, -3, 7, -15, \dots$. Then $H_2 = \begin{bmatrix} 0 & 1 \\ 1 & -3 \end{bmatrix}$ has determinant $-1$, and $H_3 = \begin{bmatrix} 0 & 1 & -3 \\ 1 & -3 & 7 \\ -3 & 7 & -15 \end{bmatrix}$ has determinant $0$, so $n_{\min} = 2$. Two minimal realizations are the controllable form $A_1 = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B_1 = (0, 1)^T$, $C_1 = [1, 0]$ and the modal form $A_2 = \operatorname{diag}(-1, -2)$, $B_2 = (1, 1)^T$, $C_2 = [1, -1]$. Here $\mathcal{O}_1 = I$ and $\mathcal{O}_2 = \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix}$, so $T = \mathcal{O}_2^{-1} = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$. Check: $T B_1 = (1, 1)^T$, $C_1 T^{-1} = [1, 0] \begin{bmatrix} 1 & -1 \\ -1 & 2 \end{bmatrix} = [1, -1]$, and $T A_1 T^{-1} = \operatorname{diag}(-1, -2)$.

**Matrix examples.** $G(s) = \frac{1}{s + 1} \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}$ has one residue of rank 1, so $n_{\min} = 1$: $A = -1$, $B = [1, 1]$, $C = (1, 1)^T$. $G(s) = \frac{1}{s + 1} I_2$ has the same denominator but a residue of rank 2, so $n_{\min} = 2$. The degree of a common denominator does not give the minimal order of a matrix.

## Tightness

- **Controllability alone is not enough.** The controllable canonical form of $(s + 1)/(s^2 + 3 s + 2)$ has order 2 and is controllable, but it is not observable, and $G = 1/(s + 2)$ has a realization of order 1. Observability alone fails in the dual way.
- **Non-minimal realizations need not be similar.** $(\operatorname{diag}(-2, -1), (1, 0)^T, [1, 0], 0)$ and $(\operatorname{diag}(-2, -5), (1, 0)^T, [1, 0], 0)$ both realize $1/(s + 2)$ with order 2, but their $A$ matrices have different eigenvalues, so no $T$ relates them.
- **Finite dimension is needed.** A transfer function that is not rational, such as $e^{-s}$, has no realization of finite order at all; see [realization problem](/realization-problem/).

## History

McMillan defined the degree of a rational matrix in 1952, in his work on the synthesis of electrical networks, as the least number of reactive elements needed. Gilbert in 1963 found the minimal order of a transfer matrix with simple poles from the ranks of the residues. Kalman in the same issue of the SIAM Journal on Control proved that a realization is irreducible exactly when it is controllable and observable, and that irreducible realizations are unique up to a change of coordinates. In 1965 he showed that the minimal order equals the McMillan degree. Ho and Kalman in 1966 gave the rank of the Hankel matrix as the minimal order, with an algorithm that builds a minimal realization from the Markov parameters.

## References
