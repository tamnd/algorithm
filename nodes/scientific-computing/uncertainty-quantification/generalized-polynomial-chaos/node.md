---
tag: A8KFH6
kind: technique
slug: generalized-polynomial-chaos
name: Generalized polynomial chaos
aliases:
- Wiener-Askey polynomial chaos
- gPC
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Matches the polynomial family to the input law by the Askey scheme, such as Hermite for Gaussian and Legendre for uniform inputs.
prereqs: [polynomial-chaos-expansion, orthogonal-polynomials, legendre-polynomials]
see_also: [stochastic-galerkin-method, non-intrusive-spectral-projection, regression-polynomial-chaos, stochastic-collocation-method, golub-welsch-algorithm, gaussian-quadrature, gauss-hermite-quadrature, chebyshev-polynomials]
sources:
  - paper: doi:10.1137/S1064827501387826
    title: Dongbin Xiu and George Em Karniadakis, The Wiener-Askey polynomial chaos for stochastic differential equations, SIAM Journal on Scientific Computing 24(2), 2002, 619-644
    locator: the correspondence between the laws of the inputs and the orthogonal polynomials of the Askey scheme, and the exponential convergence of the matched expansions in examples
  - book: isbn:9780691142128
    title: Dongbin Xiu, Numerical Methods for Stochastic Computations, A Spectral Method Approach, Princeton University Press, 2010
    locator: the chapters on orthogonal polynomials, generalized polynomial chaos in one and several variables, and the Galerkin and collocation methods built on it
  - paper: doi:10.1051/m2an/2011045
    title: Oliver G. Ernst, Antje Mugler, Hans-Jorg Starkloff and Elisabeth Ullmann, On the convergence of generalized polynomial chaos expansions, ESAIM Mathematical Modelling and Numerical Analysis 46(2), 2012, 317-339
    locator: the density of polynomials in the space of square integrable functions of a random variable, the determinacy of the moment problem, and the failure of density for the lognormal law
---

Generalized polynomial chaos (gPC) is the [polynomial chaos expansion](/polynomial-chaos-expansion/) with the polynomial family chosen to match the law of each input. If $\xi_k$ has density $\rho_k$, the expansion uses the polynomials orthogonal for the weight $\rho_k$, so that $\mathbb{E}[\psi_m(\xi_k) \psi_n(\xi_k)] = \delta_{mn}$. Wiener's original chaos used Hermite polynomials, which are orthogonal for the Gaussian law. Xiu and Karniadakis observed in 2002 that the classical families of the Askey scheme are orthogonal for other standard laws: Legendre for the uniform law, Laguerre for the gamma law, Jacobi for the beta law, and Charlier, Krawtchouk, Meixner and Hahn polynomials for discrete laws. Expanding in the matched family avoids a nonlinear change of variables, and for a smooth output it keeps the fast decay of the coefficients. For a uniform input and $q = e^\xi$, the matched Legendre expansion of degree 8 has a relative error of $10^{-8}$, while a Hermite expansion of the same output after a map to a Gaussian variable has $1.6 \times 10^{-2}$.

## In plain words

A polynomial chaos expansion works best when its polynomials fit the shape of the input's distribution. Hermite polynomials fit the bell curve. If the input is spread evenly over an interval, Legendre polynomials fit it, and if it is a waiting time, Laguerre polynomials fit it. A table, the Askey scheme, gives the right family for the common distributions. With the right family, the output is a simple polynomial of the input, and the expansion converges fast. With the wrong family, you must first bend the input into the shape the polynomials expect, and the bend makes the output harder to approximate.

## When it applies

- The inputs are independent, and each has a law whose moments are all finite.
- The polynomials must be dense in $L^2$ of that law. For laws on a bounded interval this always holds. On unbounded supports it holds for the Gaussian and gamma laws, but Ernst, Mugler, Starkloff and Ullmann show that it fails for the lognormal law, whose moments do not determine it.
- The law is one of the standard families of the Askey scheme, or its moments can be computed, so that the orthogonal polynomials can be built numerically.
- The output is smooth in each input. Then the matched expansion converges at the rate set by the smoothness of the output as a function of $\xi$, without a loss from a change of variables.

## The template

**Notation.** $\rho_k$ is the law of input $k$. Monic orthogonal polynomials satisfy the three-term recurrence $\pi_{n+1}(x) = (x - a_n) \pi_n(x) - b_n \pi_{n-1}(x)$, with $b_n > 0$. The orthonormal polynomials are $\psi_n = \pi_n / \sqrt{b_1 \cdots b_n}$ when $\rho_k$ is a probability law.

```pseudo id=main
GPC-BASIS(ρ_1..ρ_d, 𝒜)
L1  for k ← 1 to d do
L2      if ρ_k is in the Askey table then take its family and the known recurrence a_n, b_n   ▷ hole: the table entry
L3      else compute a_n, b_n from the moments or a discretization of ρ_k                     ▷ hole: Stieltjes, Chebyshev, Lanczos
L4      ψ^(k)_n ← the orthonormal polynomials from the recurrence
L5  Ψ_α(ξ) ← Π_k ψ^(k)_{α_k}(ξ_k) for α in 𝒜
L6  return the basis {Ψ_α} and the Gauss rules of each ρ_k                                      ▷ for the coefficient methods
```

The Askey table for the standard laws is:

| input law | support | weight | family |
|---|---|---|---|
| Gaussian | $(-\infty, \infty)$ | $e^{-x^2/2}$ | Hermite |
| gamma | $[0, \infty)$ | $x^a e^{-x}$ | Laguerre $L^{(a)}_n$ |
| beta | $[-1, 1]$ | $(1-x)^a (1+x)^b$ | Jacobi $P^{(a,b)}_n$ |
| uniform | $[-1, 1]$ | 1 | Legendre |
| Poisson | $\{0, 1, \ldots\}$ | $e^{-\lambda} \lambda^x / x!$ | Charlier |
| binomial | $\{0, \ldots, N\}$ | $\binom{N}{x} p^x (1-p)^{N-x}$ | Krawtchouk |
| negative binomial | $\{0, 1, \ldots\}$ | negative binomial mass | Meixner |
| hypergeometric | $\{0, \ldots, N\}$ | hypergeometric mass | Hahn |

Other intervals follow by an affine map. The recurrence of line L3 also gives the Gauss quadrature rule of $\rho_k$ by the [Golub-Welsch algorithm](/golub-welsch-algorithm/), which [non-intrusive spectral projection](/non-intrusive-spectral-projection/) and the [stochastic Galerkin method](/stochastic-galerkin-method/) use.

**Orthonormality of the product basis (proved).** If the inputs are independent and each family is orthonormal for its law, then $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \delta_{\alpha\beta}$.

*Proof.* By independence, $\mathbb{E}[\Psi_\alpha \Psi_\beta] = \prod_k \mathbb{E}[\psi^{(k)}_{\alpha_k}(\xi_k) \psi^{(k)}_{\beta_k}(\xi_k)] = \prod_k \delta_{\alpha_k \beta_k}$, which is 1 if $\alpha = \beta$ and 0 otherwise. $\square$

For dependent inputs the product is not orthogonal, which is why dependent inputs are first mapped to independent ones.

## Classic examples

**Legendre against Hermite for a uniform input.** Let $\xi$ be uniform on $[-1, 1]$ and $q = e^\xi$. The [Legendre](/legendre-polynomials/) expansion uses $\psi_n = \sqrt{2n+1}\, P_n(\xi)$. A Hermite expansion needs a Gaussian variable: write $\xi = 2\Phi(\eta) - 1$ with $\eta \sim N(0, 1)$ and expand $e^{2\Phi(\eta) - 1}$ in Hermite polynomials of $\eta$. Both expansions have the exact mean $\sinh 1 = 1.1752$ at degree 0. The relative errors $\|q - q_p\| / \operatorname{sd}(q)$, from coefficients computed by a fine quadrature, are

| $p$ | Legendre in $\xi$ | Hermite in $\eta$ |
|---|---|---|
| 1 | 0.247 | 0.298 |
| 2 | $4.08 \times 10^{-2}$ | 0.208 |
| 3 | $5.08 \times 10^{-3}$ | 0.124 |
| 4 | $5.06 \times 10^{-4}$ | $7.29 \times 10^{-2}$ |
| 6 | $3.0 \times 10^{-6}$ | $3.13 \times 10^{-2}$ |
| 8 | $1.0 \times 10^{-8}$ | $1.57 \times 10^{-2}$ |
| 10 | $6.3 \times 10^{-11}$ | $8.8 \times 10^{-3}$ |
| 20 | | $8.9 \times 10^{-4}$ |

The Legendre error falls faster than geometrically, because $e^\xi$ is entire. The Hermite error falls much more slowly: it drops by a factor of 10 from $p = 10$ to $p = 20$, while the Legendre error drops by a factor of more than 100 for every two degrees. The nonlinear map $\eta \mapsto 2\Phi(\eta) - 1$ makes the output a harder function to approximate by polynomials, even though it is the same random variable.

**Gaussian inputs.** For $\xi \sim N(0, 1)$ the matched family is Hermite, which is the original Wiener chaos; the [polynomial chaos expansion](/polynomial-chaos-expansion/) page expands $e^\xi$ in it. The Gauss rules are the [Gauss-Hermite](/gauss-hermite-quadrature/) rules.

**Stochastic Galerkin and collocation.** The [stochastic Galerkin method](/stochastic-galerkin-method/) with Legendre chaos for uniform coefficients of a diffusion equation, and the [stochastic collocation method](/stochastic-collocation-method/) on the nodes of the matched law, are the standard gPC solvers of Xiu and Karniadakis and later authors.

**Chebyshev weights.** For the arcsine law on $[-1, 1]$, with density $1/(\pi\sqrt{1 - x^2})$, the matched family is the [Chebyshev polynomials](/chebyshev-polynomials/), a Jacobi case with $a = b = -1/2$.

## Variations

- **Arbitrary polynomial chaos.** Build the recurrence from moments of data or a histogram when the law has no closed form. The moment map is badly conditioned, so the discretized Stieltjes or Lanczos procedures are preferred for high degrees.
- **Mixed families.** Each input gets its own family, for example Hermite for a Gaussian load and Legendre for a uniform stiffness.
- **Multi-element gPC.** Split the support into cells and build the orthogonal polynomials of the restricted law in each cell, for outputs with jumps or for laws with long tails.
- **Isoprobabilistic maps.** If the family of the law is unknown or not dense, map the input to a Gaussian or uniform variable and expand in that variable, as with the lognormal law.
- **Dependent inputs.** Use a Rosenblatt map to independent variables, or a basis orthonormalized by Gram-Schmidt for the joint law.

## Pitfalls

- **Polynomials in a lognormal variable.** The lognormal law is not determined by its moments, and its orthogonal polynomials are not dense in $L^2$, so an expansion in them need not converge to the output. Write the lognormal input as $e^{\mu + \sigma \eta}$ and expand in Hermite polynomials of $\eta$.
- **A mismatched family.** A Hermite expansion of a bounded input converges slowly, as the table shows, and its truncations have unbounded tails that the true output does not have.
- **Parameter conventions.** The beta law and the Jacobi weight use different parameter names; the Jacobi weight $(1-x)^a(1+x)^b$ corresponds to a beta law with shape parameters $b + 1$ and $a + 1$ on $[-1, 1]$. Check the normalization numerically.
- **Unnormalized polynomials.** Formulas for the mean and variance from coefficients assume orthonormal polynomials. Standard Legendre $P_n$ have $\mathbb{E}[P_n^2] = 1/(2n+1)$ for the uniform law on $[-1, 1]$.
- **Ill-conditioned moments.** Building polynomials from raw moments loses digits fast as the degree grows, because the map from moments to recurrence coefficients is badly conditioned. Use a stable recurrence method.

## Exercises

1. Show that $\sqrt{2n+1}\, P_n$ are orthonormal for the uniform law on $[-1, 1]$, and give the orthonormal family for the uniform law on $[a, b]$.
2. Find the first three orthonormal polynomials for the exponential law with mean 1, and check that they are Laguerre polynomials up to sign.
3. Compute the Legendre coefficients of $e^\xi$ for $p \le 3$ and compare the variance from them with $\operatorname{Var}[e^\xi] = \frac{1}{4}(e^2 - e^{-2}) - \sinh^2 1$.
4. Compute the Hermite coefficients of $e^{2\Phi(\eta) - 1}$ by quadrature up to degree 20, and fit a rate to the error table.
5. A model has a Gaussian input and a Poisson input. Write the six basis functions of the total degree 2 product basis.

## References
