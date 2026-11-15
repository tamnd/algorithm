---
tag: 5Q24WE
kind: definition
slug: joint-spectral-radius
name: Joint spectral radius
aliases:
- JSR
area: control/discrete-event-and-hybrid-systems
level: advanced
summary: "The largest growth rate of long products of matrices from a set. It is below 1 if and only if the discrete-time switched linear system is GUES under arbitrary switching."
prereqs: [spectral-radius, matrix-norms]
see_also: [switched-system, common-lyapunov-function, exponential-stability, semidefinite-programming, undecidability, np-hard, power-iteration, perron-frobenius-theorem]
sources:
  - paper: "Gian-Carlo Rota and Gilbert Strang, A note on the joint spectral radius, Indagationes Mathematicae 22, 379-381, 1960"
    locator: the definition of the joint spectral radius and its characterization as an infimum over norms
  - book: isbn:9783540959793
    title: Raphaël Jungers, The Joint Spectral Radius, Theory and Applications, Lecture Notes in Control and Information Sciences 385, Springer, 2009
    locator: Chapter 1, Basics (definition and elementary properties); Chapter 2, Classical Results and Problems (extremal norms, complexity, computation, the finiteness property)
  - paper: doi:10.1016/S0167-6911(00)00049-9
    title: Vincent D. Blondel and John N. Tsitsiklis, The boundedness of all products of a pair of matrices is undecidable, Systems and Control Letters 41(2), 135-140, 2000
    locator: the main theorem and its consequence that the question whether the joint spectral radius is at most 1 is undecidable
  - paper: doi:10.1090/S0894-0347-01-00378-2
    title: Thierry Bousch and Jean Mairesse, Asymptotic height optimization for topical IFS, Tetris heaps, and the finiteness conjecture, Journal of the American Mathematical Society 15(1), 77-111, 2002
    locator: the counterexample to the finiteness conjecture
---

The joint spectral radius of a finite set of square matrices is the largest rate at which long products of matrices from the set can grow. For one matrix it is the ordinary [spectral radius](/spectral-radius/). For a set, it describes the discrete-time [switched linear system](/switched-system/) $x(t+1) = A_{\sigma(t)} x(t)$, where a switching signal $\sigma$ picks one matrix at each step: the joint spectral radius is below 1 if and only if every solution goes to zero at a uniform exponential rate, whatever the switching. This is a much stronger property than the stability of each matrix alone, since two matrices with spectral radius $1/2$ can give products that grow without bound. Gian-Carlo Rota and Gilbert Strang defined the quantity in 1960. It is easy to bound and hard to compute: deciding whether it is at most 1 is undecidable.

## Definition

Let $\mathcal{M} = \{A_1, \dots, A_m\}$ be a finite set of real $n \times n$ matrices, and let $\Sigma_k$ be the set of the $m^k$ products $A_{i_k} \cdots A_{i_1}$ of length $k$. For any [matrix norm](/matrix-norms/) induced by a vector norm, the **joint spectral radius** is

$$\rho(\mathcal{M}) = \lim_{k \to \infty} \max_{P \in \Sigma_k} \|P\|^{1/k}.$$

The limit exists and equals the infimum over $k$, because the sequence $\log \max_{P \in \Sigma_k} \|P\|$ is subadditive. It does not depend on the norm, because all norms on a finite-dimensional space are equivalent and the constants disappear under the root of order $k$.

Basic facts, for every $k \ge 1$:

$$\max_{P \in \Sigma_k} \rho(P)^{1/k} \;\le\; \rho(\mathcal{M}) \;\le\; \max_{P \in \Sigma_k} \|P\|^{1/k}.$$

- $\max_i \rho(A_i) \le \rho(\mathcal{M}) \le \max_i \|A_i\|$ (the case $k = 1$).
- $\rho(c\mathcal{M}) = |c|\,\rho(\mathcal{M})$, and $\rho(T^{-1} \mathcal{M} T) = \rho(\mathcal{M})$ for an invertible $T$.
- Rota and Strang: $\rho(\mathcal{M}) = \inf_{\|\cdot\|} \max_i \|A_i\|$, the infimum over all induced norms. A norm that reaches the infimum is called an extremal norm.
- **Stability.** $\rho(\mathcal{M}) < 1$ if and only if the system $x(t+1) = A_{\sigma(t)} x(t)$ is globally uniformly exponentially stable (GUES) under arbitrary switching. If $\rho(\mathcal{M}) = 1$, the products can stay bounded or can grow slower than any exponential, depending on the set.

The two inequalities above give a direct algorithm for an interval that contains $\rho(\mathcal{M})$. It lists the products of each length and keeps the best bounds:

```pseudo id=main
JSR-BOUNDS(M, K)                       ▷ M = {A_1, ..., A_m}, all n by n
L1  lo ← 0; hi ← ∞; prods ← [I]
L2  for k ← 1 to K do
L3      prods ← [A P : P in prods, A in M]            ▷ all m^k products of length k
L4      lo ← max(lo, max over P in prods of ρ(P)^(1/k))
L5      hi ← min(hi, max over P in prods of ‖P‖^(1/k))
L6  return (lo, hi)
```

The proof that $lo \le \rho(\mathcal{M}) \le hi$, and of the stability statement, is in proofs/correctness.md of this page. The cost is $O(m^K n^3)$, exponential in $K$, so the method only works for short products. The gap between the bounds can close slowly.

## Examples and non-examples

**A pair with a closed form.** Take

$$A_1 = \begin{bmatrix} 1 & 1 \\ 0 & 1 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} 1 & 0 \\ 1 & 1 \end{bmatrix}.$$

Each matrix has spectral radius 1, and each has 2-norm $\varphi = (1 + \sqrt 5)/2 \approx 1.618034$. The product $A_1 A_2 = \begin{bmatrix} 2 & 1 \\ 1 & 1 \end{bmatrix}$ has spectral radius $\varphi^2$. So the lower bound at $k = 2$ meets the upper bound at $k = 1$, and $\rho(\mathcal{M}) = \varphi$. The bounds of each length alone, with the 2-norm, are:

| $k$ | products | $\max \rho(P)^{1/k}$ | $\max \lVert P \rVert_2^{1/k}$ |
|---|---|---|---|
| 1 | 2 | 1 | 1.618034 |
| 2 | 4 | 1.618034 | 1.618034 |
| 3 | 8 | 1.551134 | 1.618034 |
| 4 | 16 | 1.618034 | 1.618034 |
| 5 | 32 | 1.581678 | 1.618034 |

The lower bound of a single length does not grow monotonically: the odd lengths cannot repeat $A_1 A_2$ an exact number of times. The algorithm keeps the best value found so far.

**Two Schur matrices that switch to instability.** Take

$$A_1 = \begin{bmatrix} 0.5 & 2 \\ 0 & 0.5 \end{bmatrix}, \qquad A_2 = \begin{bmatrix} 0.5 & 0 \\ 2 & 0.5 \end{bmatrix}.$$

Each has spectral radius $0.5$, so each system $x(t+1) = A_i x(t)$ alone goes to zero. But $A_2 A_1$ has spectral radius $2.25 + \sqrt 5 \approx 4.486$, so $\rho(\mathcal{M}) \ge \sqrt{4.486} \approx 2.118$. Each $A_i$ also has 2-norm $\sqrt{2.25 + \sqrt 5}$, so the bounds meet and $\rho(\mathcal{M}) = \sqrt{2.25 + \sqrt 5} = 0.5 + \varphi \approx 2.118$. Alternating the two matrices makes $\|x(t)\|$ grow like $2.118^t$.

**A set with a gap.** For $A_1 = \begin{bmatrix} 0.6 & 0.5 \\ 0 & 0.6 \end{bmatrix}$ and $A_2 = \begin{bmatrix} 0.6 & 0 \\ -0.5 & 0.6 \end{bmatrix}$, the products up to length 8 give $0.7896 \le \rho(\mathcal{M}) \le 0.8096$. The value is not known in closed form, but the upper bound is below 1, so the switched system is GUES.

**Special cases.**

- One matrix: $\rho(\{A\}) = \rho(A)$, by Gelfand's formula $\rho(A) = \lim_k \|A^k\|^{1/k}$.
- Matrices that are all upper triangular, or that all commute: $\rho(\mathcal{M}) = \max_i \rho(A_i)$. For a triangular set, the diagonal of a product is the product of the diagonals.
- Symmetric matrices, or more generally normal matrices: $\|A_i\|_2 = \rho(A_i)$, so the bound at $k = 1$ is exact and $\rho(\mathcal{M}) = \max_i \rho(A_i)$.

**Non-examples.**

- $\max_i \rho(A_i)$ is not the joint spectral radius in general: the Schur pair above has it equal to $0.5$, against a true value above 2.
- $\max_i \|A_i\|$ is only an upper bound, and its value depends on the norm. For the Schur pair it is $2.5$ in the infinity norm, against the true value $2.118$.
- For a continuous-time switched system $\dot x = A_{\sigma(t)} x$, the joint spectral radius of $\{A_i\}$ means nothing. The analog is the largest exponential growth rate of the solutions, and it is studied with Lyapunov functions instead.

**The finiteness property.** In the first example, the value is reached by one finite product: $\rho(\mathcal{M}) = \rho(P)^{1/k}$ with $P = A_1 A_2$ and $k = 2$. The conjecture that every finite set has such a product was disproved by Bousch and Mairesse (2002), so the lower bounds of the algorithm can stay strictly below $\rho(\mathcal{M})$ for every $K$.

## Related definitions

- [Spectral radius](/spectral-radius/): the case of one matrix. The joint version replaces the powers $A^k$ by all products of length $k$.
- [Switched system](/switched-system/): the joint spectral radius is the exact stability test for the discrete-time linear case under arbitrary switching.
- [Common Lyapunov function](/common-lyapunov-function/): a norm $\|x\|$ with $\|A_i x\| < \|x\|$ for all $i$ and $x \ne 0$ is a common Lyapunov function, and by the Rota-Strang formula one exists exactly when $\rho(\mathcal{M}) < 1$. A quadratic one, $x^\top P x$ with $A_i^\top P A_i - P$ negative definite for all $i$, is found by [semidefinite programming](/semidefinite-programming/) and gives the upper bound by the ellipsoidal norm $\|x\|_P = \sqrt{x^\top P x}$.
- [Exponential stability](/exponential-stability/): the property the condition $\rho(\mathcal{M}) < 1$ certifies, uniformly over all switching signals.
- Complexity: whether $\rho(\mathcal{M}) \le 1$ is [undecidable](/undecidability/) for pairs of matrices with rational entries (Blondel and Tsitsiklis 2000), and approximating $\rho(\mathcal{M})$ is [NP-hard](/np-hard/) (Jungers 2009, Chapter 2). Practical methods find extremal norms from polytopes or sums of squares, and they work well on most sets of moderate size.

## References
