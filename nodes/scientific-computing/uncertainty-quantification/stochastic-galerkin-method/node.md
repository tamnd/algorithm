---
tag: 850TYY
kind: algorithm
slug: stochastic-galerkin-method
name: Stochastic Galerkin method
aliases:
- spectral stochastic finite element method
- intrusive polynomial chaos
- stochastic Galerkin projection
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Projects the governing equations onto the polynomial chaos basis, giving one large coupled deterministic system for all coefficients.
solves: [forward-uncertainty-propagation]
model: real-ram
complexity:
  vars: {n: "the number of deterministic unknowns", d: "the number of random inputs", p: "the total degree", P: "the number of chaos terms (d+p choose p)"}
  time: {worst: O((P n)^3)}
  space: {extra: Θ((P n)^2)}
properties: {deterministic: true, intrusive: true, exact: false}
history:
  year: 1991
  people: [Roger G. Ghanem, Pol D. Spanos]
  note: Ghanem and Spanos combined the Karhunen-Loeve expansion of a random coefficient with a Wiener-Hermite chaos expansion of the solution and a Galerkin projection in 1991. Xiu and Karniadakis extended it to the Askey families in 2002.
prereqs: [galerkin-method, legendre-polynomials, polynomial-chaos-expansion]
see_also: [generalized-polynomial-chaos, non-intrusive-spectral-projection, stochastic-collocation-method, karhunen-loeve-theorem, random-field, kronecker-product, conjugate-gradient-method, cea-lemma]
sources:
  - book: isbn:9780486428185
    title: Roger G. Ghanem and Pol D. Spanos, Stochastic Finite Elements, A Spectral Approach, revised edition, Dover, 2003 (first edition Springer, 1991)
    locator: the spectral stochastic finite element method, with the Karhunen-Loeve expansion of the coefficient, the polynomial chaos expansion of the solution and the Galerkin projection onto the chaos basis
  - paper: doi:10.1137/S1064827501387826
    title: Dongbin Xiu and George Em Karniadakis, The Wiener-Askey polynomial chaos for stochastic differential equations, SIAM Journal on Scientific Computing 24(2), 2002, 619-644
    locator: the Galerkin projection with Askey chaos bases and its convergence in numerical examples
  - book: isbn:9780691142128
    title: Dongbin Xiu, Numerical Methods for Stochastic Computations, A Spectral Method Approach, Princeton University Press, 2010
    locator: Chapter 6 (the stochastic Galerkin method)
  - book: isbn:9789048135196
    title: Olivier P. Le Maitre and Omar M. Knio, Spectral Methods for Uncertainty Quantification, Springer, 2010
    locator: Chapter 4 (Galerkin methods) and the later chapter on solvers for stochastic Galerkin problems
  - paper: doi:10.1137/S0036142902418680
    title: Ivo Babuska, Raul Tempone and Georgios E. Zouraris, Galerkin finite element approximations of stochastic elliptic partial differential equations, SIAM Journal on Numerical Analysis 42(2), 2004, 800-825
    locator: the Galerkin approximation in the random and the physical variables together, with a priori error estimates
---

The stochastic Galerkin method computes a [polynomial chaos expansion](/polynomial-chaos-expansion/) of the solution of an equation with random inputs. It writes the unknown as $u(\xi) = \sum_\alpha c_\alpha \Psi_\alpha(\xi)$, a sum of chaos polynomials with unknown coefficient vectors, puts this sum into the equation, and asks that the residual be orthogonal to every polynomial of the basis. This is the [Galerkin method](/galerkin-method/) applied in the random variables. The result is one deterministic system for all coefficients at once, $P$ times as large as the original problem, where $P = \binom{d+p}{p}$ is the number of chaos terms. The method is intrusive: the solver of the model must be rewritten to assemble and solve the coupled system. In return, for smooth dependence on the input the error decays exponentially in the degree $p$, and the error is within a constant of the best possible polynomial approximation.

## In plain words

Suppose a structure has a stiffness that is not known exactly, only its range. You want to know how the deflection depends on the unknown stiffness. You guess that the deflection is a polynomial in the unknown value, with unknown coefficients. Put the guess into the equation. The equation will not hold exactly, but you can ask that the error is, on average, unrelated to each polynomial in the guess. That gives one equation for each coefficient. All of these equations are coupled, so you solve them together as one big linear system. After that, the mean of the deflection is the first coefficient, and the variance is the sum of the squares of the others. You run the solver once, but on a larger problem, instead of running it many times.

## The problem

The model is a linear system $A(\xi) u(\xi) = f$ with $n$ unknowns, for example a [finite element method](/finite-element-method/) discretization of a diffusion equation. The input $\xi = (\xi_1, \ldots, \xi_d)$ has independent components, each uniform on $[-1, 1]$, and the matrix depends on it in the affine way

$$A(\xi) = A_0 + \xi_1 A_1 + \cdots + \xi_d A_d,$$

which is the form a truncated [Karhunen-Loeve expansion](/karhunen-loeve-theorem/) of a [random field](/random-field/) coefficient gives. The matrices are symmetric, and $A(\xi)$ is positive definite for every $\xi$ in the box. The output is the mean $\mathbb{E}[u]$, the variance of each component, and a polynomial surrogate $u_p(\xi)$ of total degree at most $p$.

The basis is the set of products $\Psi_\alpha(\xi) = \prod_k \psi_{\alpha_k}(\xi_k)$, with $\psi_m = \sqrt{2m+1}\, P_m$ the orthonormal [Legendre polynomials](/legendre-polynomials/), for the multi-indices $\alpha \in \Lambda = \{\alpha \in \mathbb{N}^d : |\alpha| \le p\}$. Then $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$. For other input laws, the [generalized polynomial chaos](/generalized-polynomial-chaos/) picks the matching family, and the algorithm does not change.

## The algorithm

The Galerkin conditions $\mathbb{E}[(A(\xi) u_p(\xi) - f)\, \Psi_\beta(\xi)] = 0$ for all $\beta \in \Lambda$ are, after the substitution $u_p = \sum_\alpha c_\alpha \Psi_\alpha$,

$$\sum_{\alpha \in \Lambda} \sum_{k=0}^{d} \mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha]\, A_k c_\alpha = \mathbb{E}[\Psi_\beta]\, f, \qquad \xi_0 = 1.$$

With the $P \times P$ matrices $G_k[\beta, \alpha] = \mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha]$ this is $K c = F$ with $K = \sum_k G_k \otimes A_k$, a sum of [Kronecker products](/kronecker-product/).

```pseudo id=main
STOCHASTIC-GALERKIN(A_0, ..., A_d, f, p)
L1  Λ ← all α ∈ ℕ^d with |α| ≤ p, the zero index first;  P ← |Λ|
L2  G_0 ← I_P;  G_k[β, α] ← E[ξ_k Ψ_β Ψ_α] for k = 1..d        ▷ exact formulas, no quadrature
L3  K ← Σ_{k=0..d} G_k ⊗ A_k                                     ▷ P × P blocks of size n × n
L4  F ← e_0 ⊗ f                                                   ▷ E[Ψ_β] = 1 for β = 0, else 0
L5  solve K c = F for c = (c_α), α ∈ Λ
L6  mean ← c_0;  variance_i ← Σ_{α ≠ 0} (c_α)_i^2
L7  return c, mean, variance
```

Line L1 builds the total degree set, sorted by degree. Line L2 needs only one dimensional facts, because the inputs are independent: $\mathbb{E}[\xi_k \Psi_\beta \Psi_\alpha]$ is zero unless $\alpha$ and $\beta$ agree in every coordinate except $k$, and there they differ by one. The three term recurrence $\xi \psi_m = b_{m+1} \psi_{m+1} + b_m \psi_{m-1}$ with $b_m = m/\sqrt{(2m-1)(2m+1)}$ gives the nonzero entries. So each $G_k$ has at most two nonzero entries per row, and $K$ has at most $2d + 1$ nonzero blocks per block row. Line L5 is the single solve of the method; the reference code uses dense Gaussian elimination, and large problems use the [conjugate gradient method](/conjugate-gradient-method/) with the preconditioner $I_P \otimes A_0$. Line L6 uses orthonormality: the mean is the coefficient of $\Psi_0 = 1$ and the variance is the sum of the other squares.

## Example

Take the scalar model $(2 + \xi) u = 1$ with $\xi$ uniform on $[-1, 1]$. The exact moments are $\mathbb{E}[u] = \tfrac12 \ln 3 = 0.5493061443$ and $\mathbb{E}[u^2] = 1/3$, so $\mathrm{Var}(u) = 0.0315960931$. Here $A_0 = 2$, $A_1 = 1$, and $K = 2 I + G_1$ is a tridiagonal matrix of size $p + 1$. The values below come from the reference code; they are deterministic.

| $p$ | mean | error of mean | variance | error of variance | $L^2$ error | best $L^2$ error |
|---|---|---|---|---|---|---|
| 0 | 0.5000000000 | $4.93 \times 10^{-2}$ | 0 | $3.16 \times 10^{-2}$ | $1.84 \times 10^{-1}$ | $1.78 \times 10^{-1}$ |
| 1 | 0.5454545455 | $3.85 \times 10^{-3}$ | 0.0247933884 | $6.80 \times 10^{-3}$ | $5.11 \times 10^{-2}$ | $4.92 \times 10^{-2}$ |
| 2 | 0.5490196078 | $2.87 \times 10^{-4}$ | 0.0307574010 | $8.39 \times 10^{-4}$ | $1.39 \times 10^{-2}$ | $1.34 \times 10^{-2}$ |
| 3 | 0.5492851768 | $2.10 \times 10^{-5}$ | 0.0315104224 | $8.57 \times 10^{-5}$ | $3.75 \times 10^{-3}$ | $3.62 \times 10^{-3}$ |
| 4 | 0.5493046209 | $1.52 \times 10^{-6}$ | 0.0315881058 | $7.99 \times 10^{-6}$ | $1.01 \times 10^{-3}$ | $9.74 \times 10^{-4}$ |
| 6 | 0.5493061364 | $7.96 \times 10^{-9}$ | 0.0315960330 | $6.02 \times 10^{-8}$ | $7.29 \times 10^{-5}$ | $7.04 \times 10^{-5}$ |

The errors fall by a factor of about 13 per degree, which is exponential convergence. The last two columns compare $\|u - u_p\|_{L^2}$ with the error of the best degree $p$ approximation, the truncated exact expansion: the Galerkin error is at most 4 percent larger. The mean at $p = 1$ is $6/11$; it equals the two point Gauss-Legendre rule applied to $1/(2+\xi)$, an instance of the theorem in the Properties section.

The reference code also solves the diffusion problem $-(a u')' = 1$ on $(0, 1)$ with zero boundary values and linear elements on 8 cells, where $a = 1 + 0.5\, \xi_1$ on the left half and $a = 1 + 0.5\, \xi_2$ on the right half. At $p = 4$ the system has $P = 15$ blocks and 105 unknowns. The mean of $u(1/2)$ is $0.1308119236$ against $0.1308120359$ from a $40 \times 40$ Gauss rule on the exact solution, and the variance is $8.6820 \times 10^{-4}$ against $8.6834 \times 10^{-4}$.

## Correctness

The coefficients from line L5 satisfy the Galerkin conditions, because block row $\beta$ of $K c = F$ is the condition for $\Psi_\beta$ written out with the definition of $G_k$. The system has a unique solution: for a coefficient vector $v$ with surrogate $v_p(\xi) = \sum_\alpha v_\alpha \Psi_\alpha(\xi)$, orthonormality gives $v^{\mathsf T} K v = \mathbb{E}[v_p^{\mathsf T} A(\xi) v_p]$, which is positive unless $v = 0$. So $K$ is symmetric positive definite. The same identity says that the Galerkin solution is the best approximation of $u$ in the energy norm $\mathbb{E}[v^{\mathsf T} A(\xi) v]^{1/2}$ among all vector polynomials of total degree $p$, which is [Cea's lemma](/cea-lemma/) in the random variables. The proof file proves these facts and the theorem on Gauss rules below.

## Complexity

In the [real RAM](/real-ram/) model, line L2 costs $O(d P^2)$ with the simple test of the reference code, or $O(d P)$ with a hash of the indices. Line L3 forms $(P n)^2$ entries, of which only $O((2d + 1) P\, \mathrm{nnz}(A))$ are nonzero. A dense direct solve costs $O((P n)^3)$ time and $\Theta((P n)^2)$ space. With sparse storage, one product $K v$ costs $O((d + 1) P\, \mathrm{nnz}(A))$, and preconditioned CG needs a number of iterations that does not grow with $n$ or $p$ (the theorem below). $P = \binom{d+p}{p}$ grows like $d^p / p!$ for fixed $p$, so the method is practical only for moderate $d$.

## Properties

- **Theorem (spectral equivalence).** If $(1 - \tau) A_0 \preceq A(\xi) \preceq (1 + \tau) A_0$ for all $\xi$ in the box, with $0 \le \tau < 1$, then $(1 - \tau)(I_P \otimes A_0) \preceq K \preceq (1 + \tau)(I_P \otimes A_0)$. So the condition number of $K$ preconditioned by $I_P \otimes A_0$ is at most $(1 + \tau)/(1 - \tau)$, for every $p$ and $n$. In the example $\tau = 1/2$ and the bound is 3.
- **Theorem (one input).** If $d = 1$, the Galerkin coefficients are $c_\alpha = \sum_j w_j\, \psi_\alpha(x_j)\, A(x_j)^{-1} f$, where $x_j, w_j$ are the $p + 1$ point Gauss-Legendre nodes and weights for the uniform law. So for one input and affine dependence, stochastic Galerkin gives the same coefficients as [non-intrusive spectral projection](/non-intrusive-spectral-projection/) and the same surrogate as [stochastic collocation](/stochastic-collocation-method/) at the Gauss nodes. This does not hold for $d \ge 2$ or for a nonlinear dependence on $\xi$.
- **Quasi-optimal.** The error is the best possible in the energy norm (a theorem); in the norm $\mathbb{E}[v^{\mathsf T} A_0 v]^{1/2}$, which is the $L^2$ norm up to a factor when $n = 1$, it is at most $\sqrt{(1+\tau)/(1-\tau)}$ times the best error.
- **Intrusive.** The deterministic solver must be changed to form $K$. One run of a large solve replaces many runs of the original solver.
- **Deterministic.** There is no sampling error; the only errors are the truncation at degree $p$ and the solver tolerance.

## Variants and improvements

- **Other input laws.** Hermite, Laguerre or Jacobi chaos for Gaussian, gamma or beta inputs, by the Wiener-Askey scheme of [generalized polynomial chaos](/generalized-polynomial-chaos/). Only the recurrence constants in line L2 change.
- **Non-affine and nonlinear models.** For a lognormal coefficient or a nonlinear equation, the Galerkin projection needs triple products $\mathbb{E}[\Psi_\alpha \Psi_\beta \Psi_\gamma]$ or a pseudospectral evaluation of the nonlinear terms, and $K$ loses its sparsity.
- **Solvers.** Mean-based block diagonal preconditioning, Kronecker product preconditioners, and low-rank tensor solvers that never store all $P n$ unknowns.
- **Adaptive and anisotropic bases.** Different degrees for different inputs, or index sets grown by error indicators, reduce $P$ when the inputs are of unequal importance.
- **Space-random discretization.** Babuska, Tempone and Zouraris analyzed the joint finite element discretization in the physical and the random variables, with $h$ and $p$ versions in both.

## When to use it

Use stochastic Galerkin when you own the solver, the model is linear or mildly nonlinear in the unknown, the coefficients are affine or polynomial in a moderate number of inputs, and you need the whole law of the output, not only a mean. Use [non-intrusive spectral projection](/non-intrusive-spectral-projection/), [regression-based polynomial chaos](/regression-polynomial-chaos/) or [stochastic collocation](/stochastic-collocation-method/) when the model is a black box or when the dependence on $\xi$ is strongly nonlinear; these run the existing solver at many inputs. Use [Monte Carlo integration](/monte-carlo-integration/) or [multilevel Monte Carlo](/multilevel-monte-carlo/) when $d$ is large or the output is not smooth in $\xi$.

## Pitfalls

- **A coefficient that is not positive.** If $A(\xi)$ is indefinite for some $\xi$ in the support, for example $a = 1 + 2\xi$, the exact solution has a pole and $K$ can be singular. A truncated expansion of a positive field can also lose positivity; check the bound on $\tau$.
- **Gaussian inputs in an affine coefficient.** $a = 1 + 0.3\, \xi$ with Gaussian $\xi$ is negative with positive probability, and the problem has no finite variance solution. Use a lognormal or a bounded law.
- **Large $P$.** With $d = 10$ and $p = 4$, $P = 1001$ and the system is 1001 times the size of one solve. The block structure must be kept sparse.
- **Wrong normalization.** With unnormalized polynomials, $\mathbb{E}[\Psi_\alpha^2] \ne 1$; the mean is still $c_0$ but the variance is $\sum_{\alpha \ne 0} c_\alpha^2\, \mathbb{E}[\Psi_\alpha^2]$.
- **Long time integration.** For time dependent problems with a random frequency, a fixed degree $p$ loses accuracy as time grows, because the solution oscillates faster and faster in $\xi$.

## Implementations

## History

Ghanem and Spanos introduced the spectral stochastic finite element method in their 1991 book. They expanded the random coefficient by the [Karhunen-Loeve theorem](/karhunen-loeve-theorem/), the solution in the Wiener-Hermite chaos of Wiener and of Cameron and Martin, and applied a Galerkin projection to both. Xiu and Karniadakis replaced the Hermite basis by the Askey families in 2002, which made the method practical for uniform and other non-Gaussian inputs. Babuska, Tempone and Zouraris gave the first error analysis of the joint discretization for elliptic problems in 2004. Later work went into solvers and preconditioners for the large coupled system and into adaptive index sets.

## References
