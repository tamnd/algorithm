---
tag: S2HG9A
kind: theorem
slug: kalman-decomposition
name: Kalman canonical decomposition
aliases:
- Kalman decomposition
area: control/state-space-control
level: core
summary: A change of state coordinates splits any LTI system into its controllable and observable, controllable only, observable only and other parts.
prereqs: [controllability, observability, kalman-rank-condition]
see_also: [minimal-realization, stabilizability, detectability, popov-belevitch-hautus-test, transfer-function-matrix, poles-and-zeros, realization-problem, controlled-invariant-subspace]
sources:
  - paper: doi:10.1073/pnas.48.4.596
    title: R. E. Kalman, Canonical structure of linear dynamical systems, Proceedings of the National Academy of Sciences 48(4), 596-600, 1962
    locator: the split of the state space into four parts by controllability and observability
  - paper: doi:10.1137/0301010
    title: R. E. Kalman, Mathematical description of linear dynamical systems, SIAM Journal on Control 1(2), 152-192, 1963
    locator: the canonical structure theorem, and the fact that the transfer function describes only the controllable and observable part
  - paper: doi:10.1137/0301009
    title: Elmer G. Gilbert, Controllability and observability in multivariable control systems, SIAM Journal on Control 1(2), 128-151, 1963
    locator: the same split for systems with distinct eigenvalues, read from the modal form
  - paper: doi:10.1109/TAC.1981.1102559
    title: Paul Van Dooren, The generalized eigenstructure problem in linear system theory, IEEE Transactions on Automatic Control 26(1), 111-129, 1981
    locator: the staircase reduction with orthogonal transformations, which computes the controllable and unobservable subspaces
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.4, Canonical Decomposition
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.3, Kalman Canonical Decomposition
---

The Kalman decomposition is a change of state coordinates that splits a linear time-invariant system into four parts: the part that is controllable and observable, the part that is controllable but not observable, the part that is observable but not controllable, and the part that is neither. The coefficient matrices take a fixed block triangular pattern. The transfer function depends only on the first part, so the other three parts are hidden from input-output data, and dropping them gives a [minimal realization](/minimal-realization/).

## Statement

**Notation.** $\dot x = A x + B u$, $y = C x + D u$ with $x \in \mathbb{R}^n$, $u \in \mathbb{R}^m$, $y \in \mathbb{R}^p$. $\mathcal{R} = \operatorname{range} [B, AB, \dots, A^{n-1} B]$ is the reachable subspace and $\mathcal{N} = \ker [C; CA; \dots; CA^{n-1}]$ is the unobservable subspace.

**Theorem (Kalman 1962).** There is an invertible $T \in \mathbb{R}^{n \times n}$ such that the coordinates $\bar x = T x = (x_{co}, x_{c\bar o}, x_{\bar c o}, x_{\bar c \bar o})$ give

$$\bar A = T A T^{-1} = \begin{bmatrix} A_{11} & 0 & A_{13} & 0 \\ A_{21} & A_{22} & A_{23} & A_{24} \\ 0 & 0 & A_{33} & 0 \\ 0 & 0 & A_{43} & A_{44} \end{bmatrix}, \quad \bar B = T B = \begin{bmatrix} B_1 \\ B_2 \\ 0 \\ 0 \end{bmatrix}, \quad \bar C = C T^{-1} = \begin{bmatrix} C_1 & 0 & C_3 & 0 \end{bmatrix},$$

where some blocks can be empty, and:

1. the pair $\left( \begin{bmatrix} A_{11} & 0 \\ A_{21} & A_{22} \end{bmatrix}, \begin{bmatrix} B_1 \\ B_2 \end{bmatrix} \right)$ is controllable;
2. the pair $\left( \begin{bmatrix} C_1 & C_3 \end{bmatrix}, \begin{bmatrix} A_{11} & A_{13} \\ 0 & A_{33} \end{bmatrix} \right)$ is observable;
3. $(A_{11}, B_1)$ is controllable and $(C_1, A_{11})$ is observable;
4. the transfer matrix is $G(s) = C (sI - A)^{-1} B + D = C_1 (sI - A_{11})^{-1} B_1 + D$, and the Markov parameters are $C A^k B = C_1 A_{11}^k B_1$ for all $k \ge 0$.

The block sizes are $n_1 = \dim \mathcal{R} - \dim (\mathcal{R} \cap \mathcal{N})$, $n_2 = \dim(\mathcal{R} \cap \mathcal{N})$, $n_3 = n - \dim(\mathcal{R} + \mathcal{N})$ and $n_4 = \dim \mathcal{N} - \dim(\mathcal{R} \cap \mathcal{N})$. They do not depend on the choice of $T$, and neither do the eigenvalues of each diagonal block.

## In plain words

Any linear system with constant coefficients can be looked at in coordinates that sort its state into four groups. The input reaches the first two groups and not the last two. The output sees the first and third groups and not the second and fourth. In these coordinates the input enters only where it can reach, the output reads only what it can see, and each group can drive only the groups that it is allowed to drive without breaking those rules. The input to output behavior then passes only through the first group, the part that is both reachable and visible. The other three groups still move and can still grow without bound, but no experiment that only applies inputs from rest and records outputs can detect them. A model of the first group alone has the same transfer function and the fewest possible states.

## Proof

*Step 1: the four subspaces.* $\mathcal{R}$ is $A$-invariant and contains $\operatorname{range} B$. $\mathcal{N}$ is $A$-invariant and lies in $\ker C$. So $\mathcal{R} \cap \mathcal{N}$ and $\mathcal{R} + \mathcal{N}$ are $A$-invariant too. Choose bases as follows: $V_2$ a basis of $\mathcal{R} \cap \mathcal{N}$; $V_1$ so that $[V_1, V_2]$ is a basis of $\mathcal{R}$; $V_4$ so that $[V_2, V_4]$ is a basis of $\mathcal{N}$; $V_3$ so that $[V_1, V_2, V_3, V_4]$ is a basis of $\mathbb{R}^n$. The columns $[V_1, V_2, V_4]$ span $\mathcal{R} + \mathcal{N}$, since $\dim(\mathcal{R} + \mathcal{N}) = \dim \mathcal{R} + \dim \mathcal{N} - \dim(\mathcal{R} \cap \mathcal{N})$. Put $T^{-1} = [V_1, V_2, V_3, V_4]$.

*Step 2: the zero pattern.* Column block $j$ of $\bar A$ holds the coordinates of $A V_j$. $A \mathcal{R} \subseteq \mathcal{R}$ gives zeros in rows 3 and 4 of columns 1 and 2. $A \mathcal{N} \subseteq \mathcal{N}$ gives zeros in rows 1 and 3 of columns 2 and 4. $A (\mathcal{R} + \mathcal{N}) \subseteq \mathcal{R} + \mathcal{N}$ gives a zero in row 3 of column 1, 2 and 4, which adds nothing new. $\operatorname{range} B \subseteq \mathcal{R}$ gives the zero rows 3 and 4 of $\bar B$. $C \mathcal{N} = 0$ gives the zero columns 2 and 4 of $\bar C$. This is the stated pattern.

*Step 3: controllability of the top part.* Write $A_c = \begin{bmatrix} A_{11} & 0 \\ A_{21} & A_{22} \end{bmatrix}$ and $B_c = \begin{bmatrix} B_1 \\ B_2 \end{bmatrix}$. Since $\bar A$ is block upper triangular with $A_c$ in the top left corner and $\bar B$ has zeros below, $\bar A^k \bar B = \begin{bmatrix} A_c^k B_c \\ 0 \end{bmatrix}$. The range of $[\bar B, \bar A \bar B, \dots]$ is $T \mathcal{R}$, the span of the first two coordinate blocks, which has dimension $n_1 + n_2$. So $[B_c, A_c B_c, \dots]$ has full row rank $n_1 + n_2$, and $(A_c, B_c)$ is controllable by the [Kalman rank condition](/kalman-rank-condition/).

*Step 4: observability of the other part.* Write $A_o = \begin{bmatrix} A_{11} & A_{13} \\ 0 & A_{33} \end{bmatrix}$ and $C_o = [C_1, C_3]$. Rows 1 and 3 of $\bar A$ have zeros in columns 2 and 4, so blocks 1 and 3 of $\bar A \bar x$ depend only on blocks 1 and 3 of $\bar x$, through $A_o$. By induction, $\bar C \bar A^k \bar x = C_o A_o^k (x_1, x_3)$ for every $\bar x = (x_1, x_2, x_3, x_4)$. Suppose $C_o A_o^k (z_1, z_3) = 0$ for all $k$. Then $\bar x = (z_1, 0, z_3, 0)$ lies in the unobservable subspace $T \mathcal{N}$, which is the span of blocks 2 and 4. So $z_1 = 0$ and $z_3 = 0$, and $(C_o, A_o)$ is observable.

*Step 5: the core block.* Let $w^* A_{11} = \lambda w^*$ and $w^* B_1 = 0$. Then $(w^*, 0)$ is a left eigenvector of $A_c$ with $(w^*, 0) B_c = 0$, which the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/) forbids, since $(A_c, B_c)$ is controllable. So $w = 0$ and $(A_{11}, B_1)$ is controllable. In the same way, $A_{11} v = \lambda v$ and $C_1 v = 0$ give the eigenvector $(v, 0)$ of $A_o$ with $C_o (v, 0) = 0$, so $v = 0$ and $(C_1, A_{11})$ is observable.

*Step 6: the transfer matrix.* $G$ does not change under $T$. By Step 3, $\bar A^k \bar B$ is zero in blocks 3 and 4, and its first block is $A_{11}^k B_1$, because the first block row of $A_c$ is $[A_{11}, 0]$. $\bar C$ reads only blocks 1 and 3, so $C A^k B = \bar C \bar A^k \bar B = C_1 A_{11}^k B_1$. Summing the series $(sI - A)^{-1} = \sum_k A^k s^{-k-1}$ for large $|s|$ gives $G(s) - D = C_1 (sI - A_{11})^{-1} B_1$ there, and both sides are rational, so they agree for all $s$.

*Step 7: invariance.* The subspaces $\mathcal{R}$, $\mathcal{N}$, $\mathcal{R} \cap \mathcal{N}$ and $\mathcal{R} + \mathcal{N}$ do not depend on $T$, so neither do the block sizes. $A_{22}$ is the matrix of $A$ restricted to $\mathcal{R} \cap \mathcal{N}$. $A_{11}$ is the matrix of the map that $A$ induces on the quotient $\mathcal{R} / (\mathcal{R} \cap \mathcal{N})$, $A_{44}$ that of the map induced on $\mathcal{N} / (\mathcal{R} \cap \mathcal{N})$, and $A_{33}$ that of the map induced on $\mathbb{R}^n / (\mathcal{R} + \mathcal{N})$. These maps are defined without a basis, so each diagonal block is fixed up to similarity, and so are its eigenvalues. $\blacksquare$

## Consequences

- **Hidden modes.** The eigenvalues of $A$ are those of $A_{11}$, $A_{22}$, $A_{33}$ and $A_{44}$. Only those of $A_{11}$ can be poles of $G$. The eigenvalues of $A_{22}$, $A_{33}$ and $A_{44}$ are the input decoupling and output decoupling zeros: modes that the input cannot excite, the output cannot show, or both. A system can have a transfer function with all poles in the open left half plane and still have $A$ not Hurwitz, when one of these hidden modes is unstable. Then the system is not internally asymptotically stable.
- **Minimal realizations.** $(A_{11}, B_1, C_1, D)$ is controllable and observable and has the same transfer matrix. By the [minimal realization theorem](/minimal-realization/) it is minimal, and its order $n_1$ is the McMillan degree of $G$. A realization is minimal exactly when $n_2 = n_3 = n_4 = 0$.
- **Stabilizability and detectability.** $(A, B)$ is [stabilizable](/stabilizability/) exactly when $A_{33}$ and $A_{44}$ are Hurwitz. $(C, A)$ is [detectable](/detectability/) exactly when $A_{22}$ and $A_{44}$ are Hurwitz. Feedback $u = -K x$ cannot move the eigenvalues of $A_{33}$ and $A_{44}$, and output injection cannot move those of $A_{22}$ and $A_{44}$.
- **Partial decompositions.** Using only $\mathcal{R}$ gives the two-block controllability decomposition $\begin{bmatrix} A_c & * \\ 0 & A_{\bar c} \end{bmatrix}$, and using only $\mathcal{N}$ gives the observability decomposition $\begin{bmatrix} A_o & 0 \\ * & A_{\bar o} \end{bmatrix}$. Most uses need only one of the two.
- **Computation.** Basis vectors taken from the controllability and observability matrices give a correct $T$ in exact arithmetic, but in floating point the rank decisions are unreliable, as on the [Kalman rank condition](/kalman-rank-condition/) page. The staircase algorithm (Van Dooren 1981) finds $\mathcal{R}$ and $\mathcal{N}$ with orthogonal transformations, with a sequence of rank decisions made by the [singular value decomposition](/singular-value-decomposition/) or a rank revealing [QR decomposition](/qr-decomposition/). Its cost is of the order of $n^3$ operations when $m$ and $p$ are at most $n$. The rank decisions still need a tolerance, so the computed $n_1$ is the order of a nearby system.

**Worked example.** $A = \operatorname{diag}(-1, -2, -3, -4)$, $B = (1, 1, 0, 0)^T$, $C = [1, 0, 1, 0]$. The eigenvalues are distinct, so by Gilbert's test the mode $i$ is controllable exactly when $b_i \ne 0$ and observable exactly when $c_i \ne 0$. The coordinates are already in the order $co$, $c \bar o$, $\bar c o$, $\bar c \bar o$, with $T = I$. Then $G(s) = 1/(s + 1)$, and the modes $-2$, $-3$, $-4$ are hidden.

**A two-state example.** $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $B = (0, 1)^T$, $C = [1, 1]$. The pair $(A, B)$ is controllable, and $\mathcal{N}$ is spanned by $(1, -1)$. With $T^{-1} = \begin{bmatrix} 1 & 1 \\ 0 & -1 \end{bmatrix}$ (which is its own inverse), $\bar A = \begin{bmatrix} -2 & 0 \\ 2 & -1 \end{bmatrix}$, $\bar B = (1, -1)^T$ and $\bar C = [1, 0]$. The pattern is $\begin{bmatrix} A_{11} & 0 \\ A_{21} & A_{22} \end{bmatrix}$ with $A_{11} = -2$, $B_1 = 1$, $C_1 = 1$, so $G(s) = 1/(s + 2)$, and the mode $-1$ is controllable and unobservable.

**An unstable hidden mode.** $A = \operatorname{diag}(1, -2)$, $B = (1, 1)^T$, $C = [0, 1]$. Then $G(s) = 1/(s + 2)$ and the impulse response $e^{-2t}$ decays, but any input that excites $x_1$ makes it grow like $e^{t}$. The mode $1$ is controllable and unobservable, so the pair $(C, A)$ is not detectable.

## Tightness

- **The off-diagonal blocks cannot be removed in general.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $B = (1, 0)^T$, $C = [0, 1]$. Here $\mathcal{R} = \mathcal{N} = \operatorname{span}(e_1)$, so $e_1$ is the $c \bar o$ part and $e_2$ is the $\bar c o$ part, and $\bar A = A$ with $A_{22} = A_{33} = 0$ and $A_{23} = 1$. Every admissible choice of coordinates keeps $A_{22} = A_{33} = 0$, so $A_{23} = 0$ would make $\bar A$ the zero matrix, which is not similar to $A$. When the diagonal blocks have no eigenvalue in common, the [Sylvester equations](/sylvester-equation/) $A_{ii} X - X A_{jj} = -A_{ij}$ are solvable and a further change of coordinates makes $\bar A$ block diagonal; with common eigenvalues this can fail, as here. In this example $G(s) = 0$ and $n_1 = 0$.
- **The blocks are not unique.** The complements $V_1$, $V_3$, $V_4$ can be chosen in many ways. Only the block sizes, the similarity class of each diagonal block and the transfer matrix are fixed.
- **Time-varying systems.** For $\dot x = A(t) x + B(t) u$ the reachable and unobservable subspaces can change dimension with $t$, and a decomposition with constant block sizes holds only on intervals where those dimensions are constant.

## History

Kalman stated the split into four parts in 1962 in the Proceedings of the National Academy of Sciences, under the name canonical structure. Gilbert had the same split for systems with distinct eigenvalues, read from the diagonal modal form, in the 1963 paper in which he also gave his tests for controllability and observability. Kalman's long 1963 paper in the SIAM Journal on Control gave the full treatment and drew the main conclusion: a transfer function describes only the controllable and observable part of a system, so a state model built from input-output data can only recover that part. That conclusion led to the [realization problem](/realization-problem/) and the Ho-Kalman algorithm of 1966. The staircase algorithms of the late 1970s and of Van Dooren in 1981 made the decomposition computable with orthogonal transformations.

## References
