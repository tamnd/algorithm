---
tag: 1AFCT8
kind: theorem
slug: popov-belevitch-hautus-test
name: Popov-Belevitch-Hautus test
aliases:
- PBH test
- Hautus lemma
area: control/state-space-control
level: core
summary: (A, B) is controllable if and only if [A - lambda I, B] has full rank n for every complex lambda; it is enough to check the eigenvalues of A. The dual test decides observability.
prereqs: [kalman-rank-condition, eigenvalue]
see_also: [controllability, observability, stabilizability, detectability, kalman-decomposition, pole-placement-theorem, transmission-zero, condition-number]
sources:
  - paper: "M. L. J. Hautus, Controllability and observability conditions of linear autonomous systems, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen, Series A, 72 (Indagationes Mathematicae 31), 443-448, 1969"
    locator: the rank test on [A - lambda I, B] and its dual for observability
  - paper: doi:10.1016/S1385-7258(70)80049-X
    title: M. L. J. Hautus, Stabilization, controllability and observability of linear autonomous systems, Indagationes Mathematicae (Proceedings) 73, 448-455, 1970
    locator: the same test restricted to eigenvalues in the closed right half plane, for stabilizability and detectability
  - paper: doi:10.1137/0301009
    title: Elmer G. Gilbert, Controllability and observability in multivariable control systems, SIAM Journal on Control 1(2), 128-151, 1963
    locator: the modal test for systems with distinct eigenvalues
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 6.2 (the equivalent conditions for controllability, among them the rank of [A - lambda I, B] at each eigenvalue) and Section 6.5 (conditions in Jordan form)
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Section 3.2, Controllability and Observability (the eigenvector tests, stabilizability and detectability)
---

The Popov-Belevitch-Hautus (PBH) test decides [controllability](/controllability/) one eigenvalue at a time: the pair $(A, B)$ is controllable if and only if the matrix $[A - \lambda I, B]$ has full row rank $n$ for every complex number $\lambda$, and only the [eigenvalues](/eigenvalue/) of $A$ need to be checked. Equivalently, no left eigenvector of $A$ is orthogonal to all columns of $B$. Unlike the [Kalman rank condition](/kalman-rank-condition/), it names the modes that fail, so the same test with $\lambda$ restricted to the closed right half plane decides [stabilizability](/stabilizability/), and its dual decides [observability](/observability/) and [detectability](/detectability/).

## Statement

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and $C \in \mathbb{R}^{p \times n}$. For $w \in \mathbb{C}^n$, $w^*$ is the conjugate transpose.

**Theorem.** The following are equivalent:

1. $(A, B)$ is controllable, that is, $\operatorname{rank} [B, AB, \dots, A^{n-1} B] = n$.
2. $\operatorname{rank} [A - \lambda I, \ B] = n$ for every $\lambda \in \mathbb{C}$.
3. $\operatorname{rank} [A - \lambda I, \ B] = n$ for every eigenvalue $\lambda$ of $A$.
4. There is no $w \in \mathbb{C}^n$, $w \ne 0$, with $w^* A = \lambda w^*$ for some $\lambda \in \mathbb{C}$ and $w^* B = 0$.

Moreover, if $w^* A = \lambda w^*$ and $w^* B = 0$ with $w \ne 0$, then $\lambda$ is an eigenvalue of $A - B K$ for every $K \in \mathbb{R}^{m \times n}$. Such a $\lambda$ is an *uncontrollable eigenvalue* (uncontrollable mode) of the pair.

**Dual form.** $(C, A)$ is observable if and only if $\operatorname{rank} \begin{bmatrix} A - \lambda I \\ C \end{bmatrix} = n$ for every eigenvalue $\lambda$ of $A$, if and only if no eigenvector $v \ne 0$ of $A$ has $C v = 0$.

The test holds as stated for discrete-time systems $x_{k+1} = A x_k + B u_k$, because the Kalman rank condition holds there too.

## In plain words

A linear system splits into modes, one for each eigenvalue, and each mode has a direction in the state space. The input can steer the system only if it can push on every mode. The test checks each eigenvalue: it asks whether some combination of the states, one that follows a single mode, is missed by every input. If such a combination exists, nothing the input does can change it, and no feedback can change its eigenvalue. Since there are at most as many eigenvalues as state variables, the check is short. The same test, run only on the modes that grow or do not decay, decides whether the system can be stabilized. Reading the output instead of the input gives the dual test for observability.

## Proof

**2 is equivalent to 3.** If $\lambda$ is not an eigenvalue of $A$, then $A - \lambda I$ is invertible, so $[A - \lambda I, B]$ has rank $n$ for any $B$. Only the eigenvalues can fail.

**3 is equivalent to 4.** The $n \times (n + m)$ matrix $[A - \lambda I, B]$ has rank less than $n$ if and only if some $w \ne 0$ has $w^* [A - \lambda I, B] = 0$, that is, $w^* A = \lambda w^*$ and $w^* B = 0$. Such a $w$ is a left eigenvector, so $\lambda$ is then an eigenvalue.

**1 implies 4.** Suppose $w \ne 0$, $w^* A = \lambda w^*$ and $w^* B = 0$. Then $w^* A^k B = \lambda^k w^* B = 0$ for every $k$, so $w^* [B, AB, \dots, A^{n-1} B] = 0$. The rank of a real matrix is the same over $\mathbb{R}$ and over $\mathbb{C}$, so the controllability matrix has rank less than $n$, and the pair is not controllable.

**4 implies 1.** Suppose the pair is not controllable, so $\mathcal{R} = \operatorname{range} [B, AB, \dots, A^{n-1} B]$ has dimension $q < n$. By the Kalman rank condition page, $\mathcal{R}$ contains the range of $B$ and is $A$-invariant. Choose an invertible $T = [T_1, T_2]$ whose first $q$ columns are a basis of $\mathcal{R}$. In the coordinates $\bar x = T^{-1} x$,

$$T^{-1} A T = \begin{bmatrix} A_{11} & A_{12} \\ 0 & A_{22} \end{bmatrix}, \qquad T^{-1} B = \begin{bmatrix} B_1 \\ 0 \end{bmatrix},$$

where the zero blocks hold because $A \mathcal{R} \subseteq \mathcal{R}$ and $\operatorname{range} B \subseteq \mathcal{R}$. The block $A_{22}$ has size $n - q \ge 1$, so it has an eigenvalue $\lambda \in \mathbb{C}$ with a left eigenvector $z \ne 0$, $z^* A_{22} = \lambda z^*$. Let $w^* = [0, z^*]\, T^{-1}$, which is nonzero. Then

$$w^* A = [0, z^*] (T^{-1} A T) T^{-1} = [0, z^* A_{22}] T^{-1} = \lambda w^*, \qquad w^* B = [0, z^*] \begin{bmatrix} B_1 \\ 0 \end{bmatrix} = 0 .$$

So 4 fails.

**The uncontrollable eigenvalue stays.** If $w^* A = \lambda w^*$ and $w^* B = 0$, then $w^* (A - BK) = \lambda w^* - (w^* B) K = \lambda w^*$, so $\lambda$ is an eigenvalue of $A - BK$ for every $K$.

**Dual form.** Apply the theorem to the pair $(A^T, C^T)$, which is controllable if and only if $(C, A)$ is observable. The transpose of $[A^T - \lambda I, C^T]$ is $\begin{bmatrix} A - \lambda I \\ C \end{bmatrix}$, which has the same rank. $\blacksquare$

## Consequences

**Examples.**

- $A = \begin{bmatrix} -1 & 0 \\ 0 & -1 \end{bmatrix}$, $B = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$. At $\lambda = -1$, $[A + I, B] = \begin{bmatrix} 0 & 0 & 1 \\ 0 & 0 & 1 \end{bmatrix}$ has rank 1. The left eigenvector $w = (1, -1)$ has $w^T B = 0$: the difference $x_1 - x_2$ is the mode the input misses.
- $A = \operatorname{diag}(1, -2)$, $B = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$. At $\lambda = 1$, $[A - I, B] = \begin{bmatrix} 0 & 0 & 1 \\ 0 & -3 & 0 \end{bmatrix}$ has rank 2. At $\lambda = -2$, $[A + 2I, B] = \begin{bmatrix} 3 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}$ has rank 1. The only uncontrollable eigenvalue is $-2$, so the pair is not controllable but it is stabilizable, and $-2$ is an eigenvalue of $A - BK$ for every $K$.
- The oscillator $A = \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ has the eigenvalues $\pm i$. At $\lambda = i$, the columns 1 and 3 of $[A - iI, B] = \begin{bmatrix} -i & 1 & 0 \\ -1 & -i & 1 \end{bmatrix}$ give the minor $-i \ne 0$, so the rank is 2; $\lambda = -i$ is the conjugate case. The pair is controllable.

**Stabilizability and detectability.** By the part about $A - BK$, an uncontrollable eigenvalue with $\operatorname{Re} \lambda \ge 0$ cannot be moved by feedback. The converse also holds (see [stabilizability](/stabilizability/)): $(A, B)$ is stabilizable if and only if $\operatorname{rank} [A - \lambda I, B] = n$ for every eigenvalue with $\operatorname{Re} \lambda \ge 0$ (Hautus 1970). Dually, $(C, A)$ is detectable if and only if the dual rank is $n$ at every eigenvalue with $\operatorname{Re} \lambda \ge 0$. In discrete time, replace $\operatorname{Re} \lambda \ge 0$ by $|\lambda| \ge 1$.

**Enough inputs.** Since $\operatorname{rank} [A - \lambda I, B] \le \operatorname{rank}(A - \lambda I) + \operatorname{rank} B$, a controllable pair needs $\operatorname{rank} B \ge n - \operatorname{rank}(A - \lambda I)$ for every eigenvalue $\lambda$. So the number of inputs must be at least the largest geometric multiplicity of an eigenvalue of $A$. A single input can never control $A = -I_2$, whatever $B$ is.

**Modal form.** If $A = \operatorname{diag}(\lambda_1, \dots, \lambda_n)$ with distinct $\lambda_i$, the left eigenvectors are the unit vectors, and the test says: the pair is controllable if and only if no row of $B$ is zero. This is Gilbert's form of the test (Gilbert 1963).

**Pole placement and zeros.** The [pole placement theorem](/pole-placement-theorem/) can only move the controllable eigenvalues; the PBH test lists the others. An uncontrollable eigenvalue is also called an input decoupling zero, and an unobservable one an output decoupling zero. They need not be poles or [transmission zeros](/transmission-zero/) of the transfer matrix, and a realization computed from the transfer matrix alone does not contain them.

**Numerical use.** Each check costs one rank decision of an $n \times (n + m)$ matrix, $O(n^2 (n + m))$ operations in the [real RAM](/real-ram/), so all eigenvalues together cost $O(n^3 (n + m))$ after the eigenvalues are known. In floating point the computed eigenvalues are perturbed, and the rank is read from singular values with a tolerance. The smallest singular value $\sigma_{\min} [A - \lambda I, B]$, minimized over all $\lambda \in \mathbb{C}$, is the distance from $(A, B)$ to the nearest uncontrollable pair in the spectral norm (Eising 1984, Systems and Control Letters 4(5)), and it is the quantity to report.

## Tightness

The test must use complex $\lambda$; checking real $\lambda$ only is wrong. Take two identical oscillators driven by one input:

$$A = \begin{bmatrix} 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \\ 0 & 0 & -1 & 0 \end{bmatrix}, \qquad B = \begin{bmatrix} 0 \\ 1 \\ 0 \\ 1 \end{bmatrix}.$$

The eigenvalues are $\pm i$, each twice, so for every real $\lambda$ the matrix $A - \lambda I$ is invertible and $[A - \lambda I, B]$ has rank 4. But at $\lambda = i$ the rank is 3, and the controllability matrix has rank 2: the difference of the two oscillator states is not affected by the input. The enough-inputs bound above shows the same thing, since $i$ has geometric multiplicity 2 and there is one input.

The restriction to the eigenvalues of $A$ is also sharp: at a non-eigenvalue the rank is always $n$, so those checks give no information, and at each eigenvalue the check can fail independently of the others, as in the second example above.

## History

A special case, for distinct eigenvalues in modal coordinates, is in Gilbert (1963). The general eigenvector test was found independently by several authors. Popov gave it in his 1966 book on hyperstability (in Romanian, translated as Hyperstability of Control Systems, Springer, 1973), Belevitch in his 1968 book Classical Network Theory (Holden-Day), and Hautus (1969) in the rank form used here. Hautus (1970) applied it to stabilizability and detectability and made it a standard tool for proofs about linear time-invariant systems.

## References
