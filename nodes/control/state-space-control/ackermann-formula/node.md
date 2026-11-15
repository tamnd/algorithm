---
tag: DZTY4S
kind: algorithm
slug: ackermann-formula
name: Ackermann's formula
aliases:
- Ackermann pole placement formula
area: control/state-space-control
level: core
summary: Gives the single-input pole placement gain as K = [0 ... 0 1] W^(-1) p(A), from the controllability matrix W and the desired polynomial p.
solves: [pole-placement-problem]
model: floating-point-model
complexity:
  vars: {n: the number of states}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, exact: true, recursive: false, online: false}
history:
  year: 1972
  people: [Jürgen Ackermann]
  note: "Ackermann published the formula in Regelungstechnik in 1972 as a direct way to compute the single-input gain without a change to canonical form."
prereqs: [controllability, kalman-rank-condition, cayley-hamilton-theorem, characteristic-polynomial]
see_also: [pole-placement-problem, pole-placement-theorem, robust-pole-placement, deadbeat-control, controllable-canonical-form, luenberger-observer, condition-number, state-feedback]
sources:
  - paper: doi:10.1524/auto.1972.20.112.297
    title: Jürgen Ackermann, Der Entwurf linearer Regelungssysteme im Zustandsraum, Regelungstechnik 20(7), 297-300, 1972
    locator: the formula for the feedback vector of a single-input system from the controllability matrix and the desired characteristic polynomial
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.2, State Feedback
  - book: isbn:9780486486130
    title: Karl J. Åström and Björn Wittenmark, Computer-Controlled Systems, Theory and Design, third edition, Prentice Hall, 1997 (Dover reprint, 2011)
    locator: Section 4.3, Regulation by State Feedback
  - paper: "Volker Mehrmann and Hongguo Xu, An analysis of the pole placement problem I. The single-input case, Electronic Transactions on Numerical Analysis 4, 89-105, 1996"
    locator: the conditioning of the single-input pole placement problem and of the closed-loop eigenvalues
  - paper: doi:10.1080/0020718508961188
    title: Jaroslav Kautsky, Nancy K. Nichols and Paul Van Dooren, Robust pole assignment in linear state feedback, International Journal of Control 41(5), 1129-1155, 1985
    locator: the introduction, on the numerical problems of methods that use canonical forms
---

Ackermann's formula computes the state feedback gain $K$ that gives a single-input system $\dot x = A x + b u$ the closed-loop characteristic polynomial $p(s)$, with $u = -Kx$:

$$K = \begin{bmatrix} 0 & \cdots & 0 & 1 \end{bmatrix} W^{-1} p(A), \qquad W = \begin{bmatrix} b & Ab & \cdots & A^{n-1} b \end{bmatrix}.$$

The formula needs no change of coordinates, and it is the same in discrete time. It is one method for the [pole placement problem](/pole-placement-problem/). The [pole placement theorem](/pole-placement-theorem/) says when a solution exists, and the formula is the constructive part of its single-input proof. With one input, $K$ is unique, so all exact methods give the same $K$; they differ only in rounding error. With more than one input, $K$ is not unique, and [robust pole placement](/robust-pole-placement/) uses the extra freedom to make the closed loop well conditioned. The formula is exact in exact arithmetic, but it is numerically unstable for larger $n$.

## In plain words

A machine has one control knob. Its state is a list of numbers, and the knob is set to a weighted sum of these numbers. The choice of weights decides how the machine settles: fast or slow, with or without oscillation. The designer writes down the wanted settling behaviour as a polynomial. Ackermann's formula turns that polynomial into the weights in one step. It uses only the model of the machine and a table of how the knob moves the state over successive steps. If some part of the state cannot be moved by the knob, the table is singular and no set of weights exists. The formula is short and easy to check by hand. On a computer it loses accuracy fast when the state has many numbers.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $b \in \mathbb{R}^n$ and a monic polynomial $p(s) = s^n + p_1 s^{n-1} + \cdots + p_n$ with real coefficients. Output: the row vector $K \in \mathbb{R}^{1 \times n}$ with $\det(sI - (A - bK)) = p(s)$. A solution exists for every $p$ if and only if $(A, b)$ is [controllable](/controllability/), that is, $W$ is invertible (the [Kalman rank condition](/kalman-rank-condition/)). The solution is then unique. If the wanted poles are $\lambda_1, \dots, \lambda_n$, then $p(s) = \prod_i (s - \lambda_i)$, and the complex poles must come in conjugate pairs for $p$ to be real.

The same formula serves the discrete system $x_{k+1} = A x_k + b u_k$ and the observer gain: for $\dot{\hat x} = A \hat x + B u + L(y - C\hat x)$ with one output, apply it to $(A^T, C^T)$ and set $L = K^T$; see [Luenberger observer](/luenberger-observer/).

## The algorithm

```pseudo id=main
ACKERMANN(A, b, p)                                 ▷ p = [1, p_1, ..., p_n]
L1  W ← [b, A b, ..., A^(n-1) b]                    ▷ n matrix-vector products
L2  solve W^T q = e_n; if W is singular, fail       ▷ q^T = last row of W^(-1)
L3  K ← 0 (a row vector); for each coefficient c of p, highest power first:
L4      K ← K A + c q^T                             ▷ Horner's rule on row vectors
L5  return K                                        ▷ K = q^T p(A)
```

Line L1 builds the controllability matrix one column at a time. Line L2 gets the last row of $W^{-1}$ by one linear solve; a singular $W$ means that $(A, b)$ is not controllable. Lines L3 and L4 compute $q^T p(A) = \sum_i p_i\, q^T A^{n-i}$ by Horner's rule, so the code multiplies row vectors by $A$ and never forms $p(A)$.

## Example

**Double integrator.** Take $A = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}$, $b = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and the poles $-1 \pm i$, so $p(s) = s^2 + 2s + 2$. Line L1 gives $W = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$, and line L2 gives $q^T = \begin{bmatrix} 1 & 0 \end{bmatrix}$. Then

$$p(A) = A^2 + 2A + 2I = \begin{bmatrix} 2 & 2 \\ 0 & 2 \end{bmatrix}, \qquad K = q^T p(A) = \begin{bmatrix} 2 & 2 \end{bmatrix}.$$

Check: $A - bK = \begin{bmatrix} 0 & 1 \\ -2 & -2 \end{bmatrix}$ has the characteristic polynomial $s^2 + 2s + 2$.

**A companion matrix.** For $A = \begin{bmatrix} 0 & 1 \\ -2 & -3 \end{bmatrix}$, $b = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$ and the poles $-4, -5$, the formula gives $K = \begin{bmatrix} 18 & 6 \end{bmatrix}$. Here $A$ is already in [controllable canonical form](/controllable-canonical-form/), and $K$ is the difference of the coefficient vectors: $p(s) = s^2 + 9s + 20$ and $\det(sI - A) = s^2 + 3s + 2$, so $K = \begin{bmatrix} 20 - 2 & 9 - 3 \end{bmatrix}$.

**Deadbeat in discrete time.** The [zero-order hold](/zero-order-hold-discretization/) model of the double integrator with period $h$ is $A = \begin{bmatrix} 1 & h \\ 0 & 1 \end{bmatrix}$, $b = \begin{bmatrix} h^2/2 \\ h \end{bmatrix}$. With $p(z) = z^2$, line L2 gives $q^T = \begin{bmatrix} 1/h^2 & -1/(2h) \end{bmatrix}$, and $K = q^T A^2 = \begin{bmatrix} 1/h^2 & 3/(2h) \end{bmatrix}$. Then $(A - bK)^2 = 0$, so every initial state reaches 0 in two samples. See [deadbeat control](/deadbeat-control/).

**Loss of accuracy.** Take $A = \operatorname{diag}(-1, -2, \dots, -n)$, $b$ the vector of ones, and the poles $-(n+1), \dots, -2n$, all well separated. The code was run in double precision, and the characteristic polynomial of the computed $A - bK$ was then evaluated exactly. The largest relative error of its coefficients, and the 2-norm condition number of $W$, were:

| $n$ | $\kappa_2(W)$ | relative coefficient error |
|---|---|---|
| 4 | $1.2 \times 10^{3}$ | $2 \times 10^{-15}$ |
| 6 | $7.3 \times 10^{5}$ | $3 \times 10^{-12}$ |
| 8 | $9.5 \times 10^{8}$ | $3 \times 10^{-9}$ |
| 10 | $2.1 \times 10^{12}$ | $9 \times 10^{-6}$ |
| 12 | $7.1 \times 10^{15}$ | $9 \times 10^{-2}$ |

The error grows roughly like $\kappa_2(W)$ times the unit roundoff. At $n = 12$ the placed polynomial is wrong in the second digit.

## Correctness

The full proof is in proofs/correctness.md. In short: write $A_c = A - bK$. Expanding $A_c^k$ gives $A_c^k = A^k - \sum_{j=0}^{k-1} A^j b\, (K A_c^{k-1-j})$. Summing with the coefficients of $p$ gives $p(A_c) = p(A) - W M$, where $M$ is an $n \times n$ matrix whose last row is $K$. If $p$ is the characteristic polynomial of $A_c$, the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives $p(A_c) = 0$, so $W M = p(A)$, and the last row of $M = W^{-1} p(A)$ is $K$. This proves uniqueness. Existence follows from the [controllable canonical form](/controllable-canonical-form/), where the gain that gives $p$ is obvious; by uniqueness it equals the formula.

## Complexity

Line L1 costs $n - 1$ matrix-vector products, $O(n^3)$ in total. Line L2 is one $LU$ solve, $O(n^3)$. Lines L3 and L4 cost $n + 1$ vector-matrix products, $O(n^3)$. The time is $O(n^3)$ and the extra space is $O(n^2)$ for $W$. Forming $p(A)$ by matrix products, as the textbook formula reads, costs $O(n^4)$ and is not needed.

In the [floating-point model](/floating-point-model/) the cost is the same, but the accuracy is poor. The controllability matrix of a well behaved system is often very ill conditioned, because its columns $A^k b$ turn towards the dominant eigenvector of $A$ as $k$ grows. The solve in line L2 then has a relative error of about $\kappa(W)$ times the unit roundoff, and the table above shows this growth. Mehrmann and Xu (1996) show that the single-input problem itself is often ill conditioned, so no method can be accurate for every input. Methods that use orthogonal transformations do not form $W$ and do better than the formula in practice.

## Properties

- **Exact in rational arithmetic.** With integer or rational data, every step is a rational operation, and the result is exact. This makes the formula a good reference for tests.
- **Linear in $p$.** The gain is affine in the coefficients of $p$: $K = q^T A^n + \sum_{i=1}^{n} p_i\, q^T A^{n-i}$. If $p$ is the open-loop polynomial, $K = 0$, by the Cayley-Hamilton theorem.
- **Same in continuous and discrete time.** The formula is pure algebra on $A$, $b$ and $p$. Only the choice of $p$ depends on the time domain: Hurwitz roots in continuous time, roots inside the unit circle in discrete time.
- **Invariance.** If $\tilde A = T A T^{-1}$ and $\tilde b = T b$, then $\tilde W = T W$, and the gain in the new coordinates is $\tilde K = K T^{-1}$, as it should be.

## Variants and improvements

- **Bass-Gura formula.** Transform to controllable canonical form by a matrix $T$ built from $W$ and the open-loop coefficients. In the new coordinates the gain is the difference of the wanted and the open-loop coefficient vectors, as in the companion example above; multiply by $T$ to return. It has the same unique result and the same numerical weakness.
- **Observer form.** For one output, $L = \left(e_n^T (W_o^T)^{-1} p(A^T)\right)^T = p(A) W_o^{-1} e_n$, with $W_o$ the [observability](/observability/) matrix.
- **Multi-input systems.** Choose a vector $v$ so that $(A - BK_0, Bv)$ is controllable for some $K_0$ (Heymann's lemma), and apply the formula to that pair. The result is one of many valid gains, often a poor one. [Robust pole placement](/robust-pole-placement/) chooses among them.
- **Orthogonal methods.** Reduce $(A, b)$ by an orthogonal similarity to Hessenberg form with $b$ a multiple of $e_1$, then compute $K$ by a recursion on the Hessenberg matrix. No controllability matrix is formed. MATLAB's `acker` is the formula of this page. MATLAB's `place` uses the [Kautsky-Nichols-Van Dooren method](/robust-pole-placement/), and SciPy's `place_poles` uses the Tits-Yang refinement of it by default.

## When to use it

Use the formula for hand computation, for teaching, for exact computation with rational data, and for systems of small order, say $n \le 6$ with well spread poles. It is also the standard proof of the single-input case of the [pole placement theorem](/pole-placement-theorem/). For larger $n$, for poles close together, or for any use in floating point where accuracy matters, use an orthogonal method. Even then, check the closed-loop eigenvalues of $A - bK$ after the design.

## Pitfalls

- **Instability for larger $n$.** As in the table above, the formula can give a gain that places the poles in the wrong place, with no warning. Compute the eigenvalues of $A - bK$ and compare.
- **Near loss of controllability.** If $(A, b)$ is close to an uncontrollable pair, $W$ is close to singular. The gain is then very large, and the closed loop is very sensitive, with any method. This is a property of the plant, not of the formula.
- **Sign convention.** The formula is for $u = -Kx$ and the closed loop $A - bK$. With $u = Kx$ the sign of $K$ changes.
- **Conjugate pairs.** If one pole of a complex pair is missing, $p$ has complex coefficients and $K$ is complex. The code rejects such pole lists.
- **Poles are not the whole design.** The formula places poles only. The zeros, the input size and the robustness margins follow from the choice of poles and are not under separate control; see [state feedback](/state-feedback/).

## Implementations

## History

Ackermann (1972) published the formula in the German journal Regelungstechnik as a direct design rule for single-input systems in state space. Before it, the usual route was a change of coordinates to a canonical form and a comparison of coefficients, as in the Bass-Gura formula. The formula became a standard textbook result and appears in Chen (1999) and in Åström and Wittenmark (1997). Its numerical weakness was well known by the 1980s; Kautsky, Nichols and Van Dooren (1985) cite the poor conditioning of canonical form methods as the reason for their algorithm, and Mehrmann and Xu (1996) analysed the conditioning of the single-input problem.

## References
