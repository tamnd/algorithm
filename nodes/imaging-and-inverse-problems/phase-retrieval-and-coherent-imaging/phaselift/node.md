---
tag: K3F300
kind: algorithm
slug: phaselift
name: PhaseLift
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: research
summary: "Phase retrieval as a convex problem. Lift x to the matrix X = x x^*, in which the data are linear, and find a positive semidefinite X that fits them with the least trace."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {n: the length of the signal, m: the number of measurements, K: the number of iterations}
  time: {worst: O(K (m n^2 + n^3))}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2013
  people: [Emmanuel Candès, Thomas Strohmer, Vladislav Voroninski]
  note: Candès, Strohmer and Voroninski gave the trace minimization relaxation and proved exact recovery from about n log n Gaussian measurements, and Candès and Li (2014) brought the number down to the order of n.
prereqs: [phase-retrieval, semidefinite-programming, projected-gradient-descent]
see_also: [wirtinger-flow, spectral-initialization, compressed-sensing, matrix-completion, complement-property, interior-point-method, admm, eigenvalue]
sources:
  - paper: doi:10.1002/cpa.21432
    title: Emmanuel J. Candès, Thomas Strohmer and Vladislav Voroninski, PhaseLift, exact and stable signal recovery from magnitude measurements via convex programming, Communications on Pure and Applied Mathematics 66(8), 2013, 1241 to 1274
    locator: the trace minimization relaxation and its exact recovery theorem for m of order n log n, as restated in Theorem 1.1 of Candès and Li (2014)
  - paper: doi:10.1007/s10208-013-9162-z
    title: Emmanuel J. Candès and Xiaodong Li, Solving quadratic equations via PhaseLift when there are about as many equations as unknowns, Foundations of Computational Mathematics 14(5), 2014, 1017 to 1026
    locator: problem (1.2) (PhaseLift), Theorem 1.2 (m >= c_0 n, all signals at once), Lemma 2.2 (the lifted signal as the unique feasible point), problem (1.6) and Theorem 1.3 (noisy data) (preprint arXiv 1208.6247)
---

PhaseLift is a convex method for [phase retrieval](/phase-retrieval/) with known sampling vectors. The data $y_r = |a_r^* x|^2$ are quadratic in $x$, but they are linear in the matrix $X = x x^*$, because $|a_r^* x|^2 = a_r^* X a_r$. The method looks for $X$ in place of $x$. The condition that $X$ has rank one is not convex, so PhaseLift keeps only the condition that $X$ is positive semidefinite, and uses the trace to prefer matrices of low rank:

$$\text{minimize } \operatorname{tr} X \quad \text{subject to } a_r^* X a_r = y_r \ (r = 1, \dots, m), \quad X \succeq 0 .$$

This is a [semidefinite program](/semidefinite-programming/). Candès, Strohmer and Voroninski (2013) proved that for about $n \log n$ Gaussian vectors its only solution is $x x^*$. Candès and Li (2014) brought the number down to the order of $n$, and showed that then $x x^*$ is the only feasible point. The signal is the top eigenvector of $X$, up to a global phase.

## In plain words

The unknown is a list of complex numbers, and each measurement gives a squared size, which mixes the numbers in pairs. That makes the equations hard: there are many false answers, and a search can get stuck in one.

The trick is to treat each product of two unknowns as a new unknown of its own. Put all these products in a square table. Then every measurement is a simple sum over the table, and simple sums are easy. The price is that the table has many more entries than the list, and a true table has a special form. The method keeps a weaker property of that form, which turns the search into one with a single best answer. With enough random measurements, that answer is the true table, and the list can be read off from it.

## The problem

The input is $m$ vectors $a_r \in \mathbb{C}^n$ and the values $y_r = |a_r^* x|^2$. The output is a $z$ with a small $\operatorname{dist}(z, x) = \min_\varphi \|z - e^{i\varphi} x\|$; no method can find the global phase. Write $\mathcal{A}(X) = (a_r^* X a_r)_{r=1}^m$ for the linear map on the Hermitian matrices.

## The algorithm

The semidefinite program can be solved by any SDP method, such as an [interior point method](/interior-point-method/) for small $n$. The implementation here uses [projected gradient descent](/projected-gradient-descent/) on the penalized form

$$F(X) = \tfrac12 \|\mathcal{A}(X) - y\|^2 + \lambda \operatorname{tr} X \quad \text{over } X \succeq 0,$$

with $\lambda = 0$ by default. When $x x^*$ is the only feasible point, as in the theorem of Candès and Li, the minimizer of $F$ with $\lambda = 0$ is $x x^*$, and the trace does not matter.

```pseudo id=main
PHASELIFT(a₁, …, a_m, y, K, λ)
L1  L ← ‖𝒜‖²                                ▷ or any bound L ≥ ‖𝒜‖², such as Σ_r ‖a_r‖⁴
L2  X ← 0  (n × n)
L3  for k ← 1 to K do
L4      ρ ← 𝒜(X) − y                         ▷ ρ_r = a_r* X a_r − y_r
L5      G ← Σ_r ρ_r a_r a_r* + λ I
L6      X ← P₊(X − G / L)                   ▷ set the negative eigenvalues to 0
L7  return X
```

Then $z = \sqrt{w_1}\, u_1$ from the top eigenpair $(w_1, u_1)$ of $X$. Line L5 is the gradient $\mathcal{A}^*(\rho) + \lambda I$. Line L6 is the projection onto the positive semidefinite matrices: write $X = \sum_k w_k u_k u_k^*$ and replace each $w_k$ by $\max(w_k, 0)$. The implementation does this on the real symmetric form $\begin{pmatrix} B & -C \\ C & B \end{pmatrix}$ of $X = B + iC$, with the [Jacobi eigenvalue method](/jacobi-eigenvalue-algorithm/) of the shared helper. It gets $\|\mathcal{A}\|$ from the [singular values](/singular-value-decomposition/) of the $m \times n^2$ real matrix of $\mathcal{A}$.

## Example

A case by hand. Take $x = (1, 1 + i)$ and the four vectors $e_1$, $e_2$, $e_1 + e_2$ and $e_1 + i e_2$. Write $X = \begin{pmatrix} p & s \\ \bar s & q \end{pmatrix}$ with real $p$ and $q$. The four values $a_r^* X a_r$ are

$$p, \qquad q, \qquad p + q + 2 \operatorname{Re} s, \qquad p + q - 2 \operatorname{Im} s,$$

and the data are $y = (1, 2, 5, 5)$. These four linear equations give $p = 1$, $q = 2$ and $s = 1 - i$, so

$$X = \begin{pmatrix} 1 & 1 - i \\ 1 + i & 2 \end{pmatrix} = x x^* .$$

Its eigenvalues are $3$ and $0$, and $\sqrt3$ times the top unit eigenvector is $x$ up to a phase. Here the four real numbers of a $2 \times 2$ Hermitian matrix are fixed by four equations, so the lifted problem has one solution. The implementation starts from $X = 0$ with $F = 27.5$, and reaches $\|X - x x^*\| = 0.0065$ after 100 steps and $8 \cdot 10^{-11}$ after 500 steps.

Random measurements. Take $n = 4$, $m = 32$, a unit $x \in \mathbb{C}^4$ and complex Gaussian vectors, all from seed 1, with $\lambda = 0$ (measurements of the implementation):

| step $k$ | 0 | 10 | 50 | 100 | 200 | 300 |
|---|---|---|---|---|---|---|
| $\operatorname{dist}(z_k, x)$ | 1 | 0.22 | 0.034 | 0.0053 | 1.4e-4 | 3.8e-6 |
| $\|X_k - x x^*\|$ | 1 | 0.35 | 0.065 | 0.010 | 2.5e-4 | 6.5e-6 |
| $F(X_k)$ | 28 | 0.47 | 0.011 | 2.7e-4 | 1.7e-7 | 1.1e-10 |

Here $\|\mathcal{A}\|^2 = 146$, and the cheap bound $\sum_r \|a_r\|^4 = 518$ is 3.55 times larger. With that bound the step is shorter, and after 300 steps $\operatorname{dist}$ is only $0.0098$. With $\lambda = 0.05$ the result has rank one and trace $0.9985$, and $\operatorname{dist} = 0.0013$: the penalty adds a small bias toward a smaller trace.

## Correctness

The proof page shows these facts.

- **Lifting.** $a_r^* X a_r = \langle a_r a_r^*, X \rangle$ is linear in $X$, and $\mathcal{A}(x x^*) = y$. The top eigenpair of $x x^*$ gives $x$ up to a phase.
- **The projection.** Clipping the eigenvalues at $0$ gives the unique nearest positive semidefinite matrix, and the real form gives the same result.
- **The rate.** With the step $1/L$ and $L \ge \|\mathcal{A}\|^2$, $F(X_k)$ does not increase, $\|X_k - X^*\|$ does not increase, and $F(X_k) - F^* \le L \|X_0 - X^*\|^2 / (2k)$.
- **Recovery.** If $x x^*$ is the only positive semidefinite matrix that fits the data, then $X_k \to x x^*$ and $z_k \to x$ up to a phase.

Candès and Li (2014, Theorem 1.2) show that for $m \ge c_0\, n$ Gaussian vectors, with probability at least $1 - O(e^{-\gamma m})$, PhaseLift recovers every $x$ at once, and their Lemma 2.2 gives the unique feasible point. This is cited, not proved here.

## Complexity

One step computes $\mathcal{A}(X)$ and $\mathcal{A}^*(\rho)$ in $O(m n^2)$ time and an eigenvalue decomposition in $O(n^3)$ time, so $K$ steps cost $O(K(m n^2 + n^3))$. The extra space is $O(n^2)$ for the matrices. The exact $\|\mathcal{A}\|$ costs more than one step, because it works with an $m \times n^2$ matrix; the bound $\sum_r \|a_r\|^4$ costs $O(m n)$. For coded diffraction patterns the products with the $a_r$ are [fast Fourier transforms](/fast-fourier-transform/), but the matrix still has $n^2$ entries. This size is the main limit of PhaseLift: a signal of $10^4$ samples gives a matrix of $10^8$ entries.

## Properties

- **Convex.** There are no false local minima, and the result does not depend on a start.
- **Up to a global phase.** The lifted matrix $x x^*$ does not change when $x$ is replaced by $e^{i\varphi} x$.
- **Order $n$ measurements** are enough for Gaussian vectors, by Candès and Li (2014).
- **Universal.** For one draw of the vectors, the result of Candès and Li holds for all signals at once.
- **Expensive.** The unknown has $n^2$ entries in place of $n$.

## Variants and improvements

- **Noisy data.** Candès and Li (2014, problem (1.6)) fit the data in the $\ell_1$ norm over the positive semidefinite matrices, and bound the error by a constant times $\|w\|_1 / m$ for the noise $w$ (Theorem 1.3).
- **Feasibility only.** When the feasible point is unique, the trace can be dropped, as in the implementation here. Candès and Li note a similar argument by Demanet and Hand.
- **Other solvers.** [ADMM](/admm/), [accelerated gradient methods](/fista/), or a factored form $X = Z Z^*$ with few columns, which gives up convexity to save memory.
- **Nonconvex methods.** [Wirtinger flow](/wirtinger-flow/) works with $x$ itself, from a [spectral start](/spectral-initialization/). It needs about $n \log n$ Gaussian measurements in its theorem, but each step costs only $O(m n)$.

## When to use it

Use PhaseLift for small or medium $n$, when a guarantee that does not depend on a start matters, and when the vectors are random, as in Gaussian or coded diffraction measurements. It is also a good reference to test nonconvex methods against. For large images use [Wirtinger flow](/wirtinger-flow/) or other nonconvex methods. For the classical Fourier problem with a support, the theory does not apply.

## Pitfalls

- **Memory.** The matrix has $n^2$ entries. Do not form $\mathcal{A}$ as an $m \times n^2$ matrix for large $n$.
- **A step that is too long.** The step $1/L$ needs $L \ge \|\mathcal{A}\|^2$. An estimate of $\|\mathcal{A}\|$ from a few power steps is a lower bound and can be too small.
- **Rank above one.** With noise or with too few measurements, the result can have rank above one. Take the top eigenpair, and check how large the second eigenvalue is.
- **Too few measurements.** If the data do not fix $x$ up to a phase, no relaxation can help. Balan, Casazza and Edidin showed that $4n - 2$ generic measurements fix $x$ (see the [complement property](/complement-property/)), and the theorem of PhaseLift needs a larger multiple of $n$.
- **The trace weight.** A large $\lambda$ shrinks the result; the trace is a convex stand-in for the rank, not the rank itself.

## Implementations

## History

Candès, Eldar, Strohmer and Voroninski, in a paper on phase retrieval through matrix completion, and Candès, Strohmer and Voroninski (2013) proposed to lift the problem to $X = x x^*$ and to replace the rank by the trace. The second paper proved exact recovery from about $n \log n$ Gaussian measurements for a fixed signal. Candès and Li (2014) removed the logarithm, made the result hold for all signals at once, and gave the error bound for noisy data. The use of the trace as a convex stand-in for the rank links PhaseLift to low rank matrix recovery and [matrix completion](/matrix-completion/).

## References
