---
tag: PCC8GC
kind: algorithm
slug: robust-pole-placement
name: Kautsky-Nichols-Van Dooren pole placement
aliases:
- KNV algorithm
- robust eigenstructure assignment
area: control/state-space-control
level: advanced
summary: Places the eigenvalues of A - BK and uses the freedom of a multi-input gain to make the eigenvector matrix well conditioned, so the poles are less sensitive.
solves: [pole-placement-problem]
model: floating-point-model
complexity:
  vars: {n: the number of states, m: the number of inputs, s: the number of sweeps}
  time: {worst: "O(n^4 (s + 1))"}
  space: {extra: "O(n^2 m)"}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1985
  people: [Jaroslav Kautsky, Nancy K. Nichols, Paul Van Dooren]
  note: "Kautsky, Nichols and Van Dooren proposed in 1985 to choose the closed-loop eigenvectors so that the eigenvector matrix is well conditioned; Tits and Yang gave related globally convergent methods in 1996."
prereqs: [pole-placement-theorem, ackermann-formula, eigenvalue-condition-number, qr-decomposition]
see_also: [pole-placement-problem, condition-number, nonsymmetric-eigenproblem, singular-value-decomposition, infinite-horizon-lqr, state-feedback, luenberger-observer, floating-point-model]
sources:
  - paper: doi:10.1080/0020718508961188
    title: Jaroslav Kautsky, Nancy K. Nichols and Paul Van Dooren, Robust pole assignment in linear state feedback, International Journal of Control 41(5), 1129-1155, 1985
    locator: the parametrization of the eigenvectors by the subspaces S_j, the formula for K, and method 0 with its column updates
  - paper: doi:10.1109/9.539425
    title: André L. Tits and Yaguang Yang, Globally convergent algorithms for robust pole assignment by state feedback, IEEE Transactions on Automatic Control 41(10), 1432-1452, 1996
    locator: the maximization of the absolute value of det X, its relation to method 0, and the treatment of complex conjugate pairs
  - paper: "Volker Mehrmann and Hongguo Xu, An analysis of the pole placement problem II. The multi-input case, Electronic Transactions on Numerical Analysis 5, 77-97, 1997"
    locator: the conditioning of the multi-input pole placement problem
  - book: isbn:9780195117776
    title: Chi-Tsong Chen, Linear System Theory and Design, third edition, Oxford University Press, 1999
    locator: Section 8.6, State Feedback, Multivariable Case
---

Kautsky-Nichols-Van Dooren (KNV) pole placement computes a state feedback gain $K$ for $\dot x = Ax + Bu$, $u = -Kx$, such that $A - BK$ has given eigenvalues $\lambda_1, \dots, \lambda_n$ and a matrix $X$ of unit eigenvectors that is as well conditioned as the method can find. With $m > 1$ inputs the [pole placement problem](/pole-placement-problem/) has many solutions, because each eigenvector can be chosen in an $m$-dimensional subspace. KNV uses this freedom to make the placed eigenvalues insensitive to errors in $A$, $B$ and $K$. It differs from [Ackermann's formula](/ackermann-formula/), which has no freedom to use because it handles one input, and from the [pole placement theorem](/pole-placement-theorem/), which only says that a solution exists. This page describes method 0 of the 1985 paper, the simplest of its methods.

## In plain words

A machine with several control knobs can be made to settle in the same way by many different settings of the knob weights. Some settings are fragile: a tiny error in the model or in the weights moves the settling behaviour a lot. Others are robust. The method looks at the modes of the closed loop, the directions in which the state settles. Fragile settings have modes that point in almost the same direction. The method changes one mode direction at a time and turns it as far as it can from the others, within the directions the knobs allow. When no mode can be turned further, it computes the knob weights for these directions. The settling rates stay exactly as the designer asked.

## The problem

Input: $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ of rank $m$ with $(A, B)$ [controllable](/controllability/), and $n$ numbers $\lambda_1, \dots, \lambda_n$, closed under complex conjugation. Output: a real $K \in \mathbb{R}^{m \times n}$ and an invertible $X$ with unit columns such that $(A - BK) X = X \Lambda$, $\Lambda = \operatorname{diag}(\lambda_j)$, and with a small 2-norm condition number $\kappa_2(X) = \|X\|_2 \|X^{-1}\|_2$.

The measure comes from the Bauer-Fike theorem: if $A - BK$ changes by $\Delta$, every eigenvalue of the changed matrix lies within $\kappa_2(X) \|\Delta\|_2$ of some $\lambda_j$. The [eigenvalue condition numbers](/eigenvalue-condition-number/) of the single $\lambda_j$ are also bounded by $\kappa_2(X)$. A small $\kappa_2(X)$ also tends to give a smaller $\|K\|$, because $K = Z^{-1} U_0^T (A - X \Lambda X^{-1})$ and $\|X \Lambda X^{-1}\|_2 \le \kappa_2(X) \max_j |\lambda_j|$.

## The algorithm

```pseudo id=main
KNV0(A, B, λ_1..λ_n)
L1  B = [U_0, U_1] [Z; 0]                       ▷ QR of B; Z is m by m, invertible
L2  for each j: S_j ← orthonormal basis of null(U_1^T (A - λ_j I))   ▷ n by m
L3  for each j: x_j ← unit vector in range S_j (from a fixed random start)
L4  repeat sweeps until κ_2(X) stops falling:
L5      for each j: y_j ← unit vector orthogonal to all x_i with i ≠ j
L6                  x_j ← S_j S_j^H y_j, normalized
L7  M ← X Λ X^(-1)
L8  return K = Z^(-1) U_0^T (A - M)
```

Line L1 splits the state space into the range of $B$, spanned by $U_0$, and its orthogonal complement, spanned by $U_1$. Line L2 finds, for each wanted eigenvalue, all vectors that can be eigenvectors for it: $x$ is one exactly when $(A - \lambda_j I) x$ lies in the range of $B$, that is, when $U_1^T (A - \lambda_j I) x = 0$. Lines L5 and L6 replace one eigenvector by the unit vector of $S_j$ that is closest to the normal $y_j$ of the other columns. For a complex pair, the code updates the member with positive imaginary part and sets its partner to the complex conjugate, so that $K$ is real. Lines L7 and L8 solve $BK = A - X \Lambda X^{-1}$ for $K$.

## Example

Take

$$A = \begin{bmatrix} 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \\ -1 & 2 & 0 & -1 \end{bmatrix}, \qquad B = \begin{bmatrix} 0 & 0 \\ 1 & 0 \\ 0 & 0 \\ 0 & 1 \end{bmatrix},$$

and the poles $-1, -2, -3, -4$. The code returns

$$K = \begin{bmatrix} 7.9452 & 5.9781 & 0.4796 & -0.2082 \\ -1.5204 & 1.7918 & 3.0548 & 3.0219 \end{bmatrix},$$

with $\kappa_2(X) = 9.11$ and $\|K\|_2 = 9.96$. The eigenvalues of $A - BK$ agree with the wanted ones to about $10^{-14}$.

A rank-one design uses one direction of the inputs: set $u = -v\, k\, x$, with $k$ from Ackermann's formula for the single-input pair $(A, Bv)$. For the same poles:

| design | $\kappa_2(X)$ | $\|K\|_2$ |
|---|---|---|
| KNV method 0 | 9.11 | 9.96 |
| rank one, $v = (1, 1)$ | 224 | 43.1 |
| rank one, $v = (0, 1)$ | 595 | 67.4 |
| rank one, $v = (1, 0)$ | 860 | 81.6 |

All four gains place the same eigenvalues. The KNV gain is the smallest, and its eigenvalues are about 25 to 95 times less sensitive by the Bauer-Fike bound.

## Correctness

The full proof is in proofs/correctness.md. It has three parts.

- **The gain.** For an invertible $X$ with unit columns, there is a $K$ with $(A - BK)X = X\Lambda$ if and only if every column $x_j$ lies in range $S_j$, and then $K$ is the matrix of line L8. Multiply $BK = A - X\Lambda X^{-1}$ on the left by $[U_0, U_1]^T$: the top block gives $ZK = U_0^T(A - X\Lambda X^{-1})$, and the bottom block is the condition $U_1^T(A - \lambda_j I)x_j = 0$.
- **The subspaces.** If $(A, B)$ is controllable, each $S_j$ has dimension exactly $m$. This follows from the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/): $\operatorname{rank}[A - \lambda I, B] = m + \operatorname{rank} U_1^T (A - \lambda I)$.
- **The sweep.** If every other column is fixed, $|\det X| = |y_j^H x_j| \cdot |\det [\dots, y_j, \dots]|$, and line L6 maximizes $|y_j^H x_j|$ over unit vectors of range $S_j$ by the Cauchy-Schwarz inequality. So for real eigenvalues no step decreases $|\det X|$. By Hadamard's inequality $|\det X| \le 1$, with equality only for orthonormal columns, so the sweep pushes $X$ towards orthogonality.

If the poles are closed under conjugation and the conjugate columns are conjugate, $X \Lambda X^{-1}$ is real, so $K$ is real.

## Complexity

In the [floating-point model](/floating-point-model/): line L1 costs $O(n^2 m)$. Line L2 costs $O(n^3)$ for each $j$, $O(n^4)$ in total, and stores $n$ bases of size $n \times m$, which is the $O(n^2 m)$ extra space. In this implementation each step of line L5 orthogonalizes $n - 1$ columns, $O(n^3)$, so a sweep costs $O(n^4)$; with updates of a QR factorization of $X$ a sweep costs $O(n^3)$. Lines L7 and L8 cost $O(n^3)$. The code stops when a sweep does not lower $\kappa_2(X)$, or after a fixed number of sweeps; no general bound on the number of sweeps is known.

Rounding errors in lines L7 and L8 act like a small change $\Delta$ of the closed-loop matrix. By the Bauer-Fike theorem the placed eigenvalues then move by at most $\kappa_2(X) \|\Delta\|_2$. So a small $\kappa_2(X)$ is both the robustness of the design and the accuracy of the computation.

## Properties

- **Exact placement, approximate optimum.** The eigenvalues are placed exactly in exact arithmetic for any choice of the $x_j$ in range $S_j$. Only the conditioning is optimized, and only locally.
- **Monotone sweeps for real poles.** Each step does not decrease $|\det X|$, so the values converge. Nothing guarantees that $X$ converges to a global maximum, or that $\kappa_2(X)$ is minimal.
- **Single input.** With $m = 1$, each $S_j$ is one line, $X$ is fixed by the poles, and the method returns the unique single-input gain, the same as Ackermann's formula in exact arithmetic.
- **Full input.** With $m = n$, $S_j = \mathbb{R}^n$, and for real poles one sweep gives an orthonormal $X$ with $\kappa_2(X) = 1$: each new column is orthogonal to all columns at the time of its update, and the later updates keep this.
- **Repeated poles.** A pole can be repeated at most $m$ times with a diagonalizable closed loop, since its eigenvectors must be independent vectors of one $m$-dimensional $S_j$. The full method allows this; the code on this page needs distinct poles.

## Variants and improvements

- **Other KNV methods.** The 1985 paper gives further methods with other update rules and other measures of conditioning.
- **Tits and Yang (1996).** Maximize $|\det X|$ directly, update two columns at a time, also for complex pairs, and prove that the iteration converges from any start. SciPy's `place_poles` uses this method by default and KNV method 0 as an option. MATLAB's `place` uses a KNV method.
- **Eigenstructure assignment.** Choose the eigenvectors for other goals, such as decoupling of modes or the shape of the response, instead of conditioning.
- **Observer design.** Apply the method to $(A^T, C^T)$ and set $L = K^T$ to get a well conditioned [Luenberger observer](/luenberger-observer/).
- **Optimal control instead.** The [infinite-horizon LQR](/infinite-horizon-lqr/) chooses $K$ by a cost and gives guaranteed margins for state feedback. Pole placement with KNV gives the exact poles, LQR gives the margins.

## When to use it

Use KNV, or the Tits-Yang method, whenever a multi-input system needs a pole placement gain computed in floating point. It is the default in the main control libraries. It is also the right choice when the rank-one approach gives a large gain or poles that move under small model errors. Do not expect it to make an ill posed design good: if the wanted poles are far from the open-loop ones, or if $(A, B)$ is close to an uncontrollable pair, every gain is large, and KNV only finds a less bad one.

## Pitfalls

- **Robust poles are not a robust loop.** A small $\kappa_2(X)$ means that the eigenvalues move little under small changes of $A - BK$. It gives no gain margin or phase margin at the plant input, and it says nothing about unmodelled dynamics; see [model uncertainty](/model-uncertainty/).
- **Repeated poles.** Do not ask for a pole more than $m$ times; the closed loop then has a Jordan block, and its eigenvalue is very sensitive. Spread close poles a little instead.
- **Local optimum.** The result depends on the starting $X$. Try a few starts, or use the Tits-Yang method, when the conditioning matters.
- **Rank of $B$.** Remove dependent columns of $B$ first; the method needs $Z$ invertible. A redundant input adds nothing to the freedom of $X$.
- **Complex pairs.** Give both members of a pair. The code checks this and rejects an unpaired complex pole.

## Implementations

## History

Kautsky, Nichols and Van Dooren (1985) showed that the choice of the eigenvectors decides the sensitivity of the placed poles, gave the parametrization of the possible eigenvectors by the subspaces $S_j$, and proposed iterative methods, method 0 among them, that make $X$ well conditioned. Their paper also showed the numerical problems of methods that go through canonical forms. Tits and Yang (1996) reformulated the problem as the maximization of $|\det X|$, extended the updates to complex pairs, and gave globally convergent algorithms. Mehrmann and Xu (1996, 1997) analysed the conditioning of the single-input and multi-input problems.

## References
