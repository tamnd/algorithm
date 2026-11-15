---
tag: M8NY6K
kind: theorem
slug: pole-placement-theorem
name: Pole placement theorem
aliases:
- Wonham pole assignment theorem
area: control/state-space-control
level: core
summary: The eigenvalues of A - BK can be placed anywhere, in conjugate pairs, by a suitable real K if and only if (A, B) is controllable.
history:
  year: 1967
  people: [W. Murray Wonham]
  note: "The single-input case was known in the early 1960s. Wonham proved the multi-input case in 1967, Heymann reduced it to one input in 1968, and Hautus gave a short proof of Heymann's lemma in 1977."
prereqs: [controllability, kalman-rank-condition, controllable-canonical-form, kalman-decomposition]
see_also: [pole-placement-problem, ackermann-formula, robust-pole-placement, state-feedback, popov-belevitch-hautus-test, stabilizability, luenberger-observer, cayley-hamilton-theorem]
sources:
  - paper: doi:10.1109/TAC.1967.1098739
    title: W. M. Wonham, On pole assignment in multi-input controllable linear systems, IEEE Transactions on Automatic Control 12(6), 660-665, 1967
    locator: the theorem that every closed-loop spectrum can be assigned by state feedback if and only if the pair is controllable
  - paper: doi:10.1109/tac.1968.1099017
    title: M. Heymann, Comments on 'On pole assignment in multi-input controllable linear systems', IEEE Transactions on Automatic Control 13(6), 1968
    locator: the reduction of the multi-input case to the single-input case by a preliminary feedback
  - paper: doi:10.1109/tac.1977.1101617
    title: M. L. J. Hautus, A simple proof of Heymann's lemma, IEEE Transactions on Automatic Control 22(5), 885-886, 1977
    locator: the construction of the vectors x_1, ..., x_n and of the feedback F used in the proof on this page
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.2 (the single-input theorem and its proof by the controllable canonical form) and Section 8.6 (the multivariable case)
  - book: isbn:9780691193984
    title: Karl J. Åström and Richard M. Murray, Feedback Systems, An Introduction for Scientists and Engineers, second edition, Princeton University Press, 2021
    locator: Chapter 7, State Feedback (the section Stabilization by State Feedback)
---

The pole placement theorem says exactly when [state feedback](/state-feedback/) can give a linear system any closed-loop eigenvalues: if and only if the system is [controllable](/controllability/). It turns the [pole placement problem](/pole-placement-problem/) from a question into a design method. It is an existence result. [Ackermann's formula](/ackermann-formula/) computes the gain for one input, and [robust pole placement](/robust-pole-placement/) chooses a good gain among the many that exist for several inputs.

## Statement

**Theorem.** Let $A \in \mathbb{R}^{n \times n}$ and $B \in \mathbb{R}^{n \times m}$. The following are equivalent.

1. For every monic real polynomial $\alpha$ of degree $n$ there is $K \in \mathbb{R}^{m \times n}$ with $\det(sI - A + BK) = \alpha(s)$.
2. $(A, B)$ is controllable, that is, $\operatorname{rank}[B, AB, \dots, A^{n-1}B] = n$.

Equivalently, every list of $n$ complex numbers that is closed under complex conjugation is the spectrum of $A - BK$ for some real $K$, counted with multiplicity. If $m = 1$, the gain $K$ in item 1 is unique. The same statement holds in discrete time for $\Phi - \Gamma K$, since it is a statement about matrices.

**Theorem (uncontrollable pairs).** If the uncontrollable part of $(A, B)$ has the characteristic polynomial $\chi_u$, then $\det(sI - A + BK)$ is divisible by $\chi_u$ for every $K$, and every monic real $\alpha$ of degree $n$ that $\chi_u$ divides is reached.

## In plain words

Feeding the state back to the input changes the natural modes of a linear system. If the input can steer the system to every state, the modes can be put anywhere the designer wants, as long as complex modes come in mirror pairs. If some part of the state cannot be steered, the modes of that part stay where they are, whatever the feedback does. So controllability is exactly the condition for full freedom.

## Proof

**Necessity (2 follows from 1).** Suppose $(A, B)$ is not controllable. By the [Kalman decomposition](/kalman-decomposition/) there is an invertible $T$ with

$$TAT^{-1} = \begin{bmatrix} A_{11} & A_{12} \\ 0 & A_{22} \end{bmatrix}, \qquad TB = \begin{bmatrix} B_1 \\ 0 \end{bmatrix},$$

where $A_{22}$ has size $n - n_c \ge 1$. Write $KT^{-1} = [K_1, K_2]$. Then

$$T(A - BK)T^{-1} = \begin{bmatrix} A_{11} - B_1 K_1 & A_{12} - B_1 K_2 \\ 0 & A_{22} \end{bmatrix},$$

so $\det(sI - A + BK) = \det(sI - A_{11} + B_1 K_1)\,\chi_u(s)$ with $\chi_u(s) = \det(sI - A_{22})$. Every root of $\chi_u$ is an eigenvalue of $A - BK$ for every $K$. Take $\alpha(s) = (s - c)^n$ with a real $c$ that is not a root of $\chi_u$. No $K$ reaches it. This also proves the first half of the second theorem.

**Sufficiency for one input.** Let $m = 1$, $B = b$, and let $W = [b, Ab, \dots, A^{n-1}b]$ be invertible. Let $a(s) = \det(sI - A) = s^n + a_1 s^{n-1} + \dots + a_n$. By the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/), $A^n b = -a_1 A^{n-1}b - \dots - a_n b$, so $AW = WM$, where $M$ has ones on the subdiagonal, the last column $(-a_n, \dots, -a_1)^T$ and zeros elsewhere. Also $W^{-1}b = e_1$. Let $A_c$ be the companion matrix with ones on the superdiagonal and last row $(-a_n, \dots, -a_1)$, and $b_c = e_n$. The pair $(A_c, b_c)$ has the characteristic polynomial $a$ and an invertible controllability matrix $W_c$ (it has ones on the anti-diagonal and zeros above it), so by the same argument $A_c W_c = W_c M$ and $W_c^{-1} b_c = e_1$. Let $T = W_c W^{-1}$. Then

$$TAT^{-1} = W_c W^{-1} A W W_c^{-1} = W_c M W_c^{-1} = A_c, \qquad Tb = W_c e_1 = b_c.$$

This is the [controllable canonical form](/controllable-canonical-form/). For $k_c = (k_1, \dots, k_n)$, the matrix $A_c - b_c k_c$ is again a companion matrix, with last row $(-a_n - k_1, \dots, -a_1 - k_n)$. Its characteristic polynomial is

$$s^n + (a_1 + k_n)s^{n-1} + \dots + (a_n + k_1).$$

So $k_i = \alpha_{n+1-i} - a_{n+1-i}$ gives $\alpha$, and this is the only choice. With $K = k_c T$, $A - bK = T^{-1}(A_c - b_c k_c)T$ has the characteristic polynomial $\alpha$. Since $K \mapsto KT^{-1}$ is a bijection, $K$ is unique.

**Heymann's lemma.** If $(A, B)$ is controllable, there are $F \in \mathbb{R}^{m \times n}$ and a column $b = Bg$ of $B$ such that $(A + BF, b)$ is controllable.

*Proof (Hautus 1977).* Since $(A, B)$ is controllable and $n \ge 1$, $B \ne 0$. Let $x_1$ be a nonzero column $b_{j}$ of $B$ and $g = e_j$. Given independent $x_1, \dots, x_k$ with span $V_k$, choose $u_k$ and $x_{k+1}$ as follows. If $Ax_k \notin V_k$, set $u_k = 0$. Otherwise, if a column $b_i$ of $B$ is not in $V_k$, set $u_k = e_i$. Set $x_{k+1} = Ax_k + Bu_k$, which is not in $V_k$ in both cases. If neither case applies, then $Ax_k \in V_k$ and the image of $B$ lies in $V_k$. For $i < k$, $Ax_i = x_{i+1} - Bu_i \in V_k$. So $V_k$ is $A$-invariant and contains the image of $B$, hence it contains $[B, AB, \dots, A^{n-1}B]$, and $k = n$. So the construction gives a basis $x_1, \dots, x_n$. Define $F$ by $Fx_k = u_k$ for $k < n$ and $Fx_n = 0$. Then $(A + BF)x_k = x_{k+1}$ for $k < n$, so $b, (A + BF)b, \dots, (A + BF)^{n-1}b$ are $x_1, \dots, x_n$, which are independent. $\square$

**Sufficiency for several inputs.** Take $F$ and $b = Bg$ from Heymann's lemma. By the single-input case there is $k_1$ with $\det(sI - (A + BF) + bk_1) = \alpha(s)$. Let $K = -F + gk_1$. Then $A - BK = A + BF - Bgk_1 = A + BF - bk_1$, which has the characteristic polynomial $\alpha$. $\square$

**The uncontrollable case.** In the decomposition above, $(A_{11}, B_1)$ is controllable. By the first theorem there is $K_1$ with $\det(sI - A_{11} + B_1 K_1) = \alpha/\chi_u$ whenever $\chi_u$ divides $\alpha$. Take $K_2 = 0$ and $K = [K_1, 0]T$. $\square$

## Consequences

- **Stabilizability.** $(A, B)$ is [stabilizable](/stabilizability/), that is, some $K$ makes $A - BK$ Hurwitz, if and only if every root of $\chi_u$ has negative real part. In discrete time the roots must lie inside the unit circle.
- **Observers.** Since $\det(sI - A + LC) = \det(sI - A^T + C^T L^T)$, the eigenvalues of $A - LC$ can be placed freely if and only if $(C, A)$ is [observable](/observability/). This is the design step of the [Luenberger observer](/luenberger-observer/).
- **Deadbeat.** In discrete time a controllable pair has a gain with $\det(zI - \Phi + \Gamma K) = z^n$, so $(\Phi - \Gamma K)^n = 0$ and every state reaches 0 in at most $n$ steps. See [deadbeat control](/deadbeat-control/).
- **Uniqueness.** With one input the gain is unique. With $m > 1$ inputs and distinct eigenvalues, the gains form a set with $n(m - 1)$ free parameters in the generic case, which [robust pole placement](/robust-pole-placement/) uses.
- **Feedback does not change controllability.** $[B, (A - BK)B, \dots]$ spans the same space as $[B, AB, \dots]$, so $(A - BK, B)$ is controllable exactly when $(A, B)$ is.
- **Rule of thumb, not part of the theorem.** The theorem says nothing about the size of $K$. Moving eigenvalues far from those of $A$, or placing them for a pair that is close to uncontrollable, needs a large gain and gives an ill-conditioned problem.

## Tightness

- **Conjugate pairs are needed.** With $n = m = 1$, $A = 0$ and $B = 1$, the eigenvalue of $A - BK$ is $-K$. It equals $i$ only for $K = -i$, which is not real.
- **Controllability cannot be weakened.** In $A = \begin{bmatrix} -1 & 0 \\ 0 & 0 \end{bmatrix}$, $B = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$, the eigenvalue $-1$ stays for every $K$, so the spectrum $\{-2, -3\}$ is not reached, while $\{-1, -3\}$ is.
- **Only the characteristic polynomial is placed, not the Jordan form.** With one input, every eigenvalue of $A - bK$ has geometric multiplicity 1. Indeed, $(A - bK, b)$ is controllable, so by the [PBH test](/popov-belevitch-hautus-test/) $[\lambda I - A + bK, b]$ has rank $n$ and $\lambda I - A + bK$ has rank at least $n - 1$. So for $n = 2$ and one input, $A - bK = -I$ is impossible: $\alpha(s) = (s + 1)^2$ is reached only with a Jordan block. With $m = n$ inputs and $B = I$, $K = A + I$ gives $-I$.
- **Existence is not good numerics.** The gain exists for every controllable pair, but computing it in floating point can be ill conditioned. Mehrmann and Xu showed this in detail; see the [pole placement problem](/pole-placement-problem/).

## History

The single-input result was known in the early 1960s; it is often credited to Rissanen (1960) and to Popov (1964). Wonham (1967) proved that every spectrum can be assigned by state feedback in the multi-input case if and only if the pair is controllable. Heymann (1968) showed that a preliminary feedback reduces the multi-input case to one input, and Hautus (1977) gave the short constructive proof of Heymann's lemma that is used above. Kautsky, Nichols and Van Dooren (1985) turned the freedom of the multi-input case into a numerical method.

## References
