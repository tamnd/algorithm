---
tag: 1VF7N4
kind: technique
slug: polynomial-chaos-expansion
name: Polynomial chaos expansion
aliases:
- Wiener chaos expansion
- PCE
- Hermite chaos expansion
area: scientific-computing/uncertainty-quantification
level: core
summary: Expands a random model output in polynomials orthogonal for the input distribution, so the mean and variance come from the coefficients.
prereqs: [orthogonal-polynomials, random-variable, least-squares-approximation]
see_also: [generalized-polynomial-chaos, stochastic-galerkin-method, non-intrusive-spectral-projection, regression-polynomial-chaos, sparse-polynomial-chaos, stochastic-collocation-method, sobol-indices, karhunen-loeve-theorem]
sources:
  - paper: doi:10.2307/2371268
    title: Norbert Wiener, The homogeneous chaos, American Journal of Mathematics 60(4), 1938
    locator: the homogeneous chaos, the expansion of functionals of a Gaussian random measure in multiple Wiener integrals
  - paper: doi:10.2307/1969178
    title: Robert H. Cameron and William T. Martin, The orthogonal development of non-linear functionals in series of Fourier-Hermite functionals, Annals of Mathematics 48(2), 1947
    locator: the mean square convergence of the Fourier-Hermite series of every square integrable functional of Brownian motion
  - book: isbn:9780486428185
    title: Roger G. Ghanem and Pol D. Spanos, Stochastic Finite Elements, A Spectral Approach, revised edition, Dover, 2003
    locator: the Hermite polynomial chaos as a basis for the random solution of a finite element model, with the Karhunen-Loeve expansion of the random inputs
  - paper: doi:10.1051/m2an/2011045
    title: Oliver G. Ernst, Antje Mugler, Hans-Jorg Starkloff and Elisabeth Ullmann, On the convergence of generalized polynomial chaos expansions, ESAIM Mathematical Modelling and Numerical Analysis 46(2), 2012, 317-339
    locator: the density of polynomials in the space of square integrable functions of a random variable and its relation to the determinacy of the moment problem, with the lognormal counterexample
  - paper: doi:10.1016/j.ress.2007.04.002
    title: Bruno Sudret, Global sensitivity analysis using polynomial chaos expansions, Reliability Engineering and System Safety 93(7), 2008, 964-979
    locator: the Sobol sensitivity indices computed as sums of squared chaos coefficients
---

A polynomial chaos expansion (PCE) writes a random model output $Y = q(\xi)$, a function of a vector $\xi$ of independent random inputs with law $\rho$, as a series

$$q(\xi) = \sum_{\alpha} c_\alpha \Psi_\alpha(\xi), \qquad c_\alpha = \mathbb{E}[q(\xi) \Psi_\alpha(\xi)],$$

in polynomials $\Psi_\alpha$ that are orthonormal for $\rho$: $\mathbb{E}[\Psi_\alpha \Psi_\beta] = 1$ if $\alpha = \beta$ and 0 otherwise. Each $\Psi_\alpha$ is a product of one dimensional [orthogonal polynomials](/orthogonal-polynomials/), $\Psi_\alpha(\xi) = \prod_k \psi_{\alpha_k}(\xi_k)$, so $\alpha$ is a multi-index of degrees. Because $\Psi_0 = 1$, the mean is $c_0$ and the variance is $\sum_{\alpha \neq 0} c_\alpha^2$. A truncated expansion is a cheap surrogate of the model, and grouping the squared coefficients by the inputs they involve gives the [Sobol indices](/sobol-indices/). Wiener introduced the expansion for Gaussian inputs in 1938, with Hermite polynomials; Cameron and Martin proved its mean square convergence in 1947; Ghanem and Spanos made it a tool of engineering in 1991. The technique has two choices: the polynomial family, which [generalized polynomial chaos](/generalized-polynomial-chaos/) matches to the input law, and the way to compute the coefficients, which gives the methods listed below.

## In plain words

An uncertain input makes the output uncertain. Instead of running the model thousands of times and looking at the spread of results, write the output as a sum of simple polynomials of the input, chosen so that they do not overlap on average. Then each coefficient is the part of the output that its polynomial explains. The first coefficient is the average output. The squares of the others add up to the variance, and the ones that involve only one input tell you how much that input matters. For a smooth model a few dozen terms are often enough, and once you know them, the polynomial replaces the model.

## When it applies

- The inputs are finitely many independent random variables $\xi_1, \ldots, \xi_d$, or have been reduced to such variables, for example by the [Karhunen-Loeve theorem](/karhunen-loeve-theorem/) for a [random field](/random-field/). Dependent inputs are mapped to independent ones first.
- The output has finite variance, $\mathbb{E}[q(\xi)^2] < \infty$, so it lies in the Hilbert space $L^2_\rho$ where the expansion lives.
- The polynomials must be dense in $L^2_\rho$, or the series converges to the wrong function. For a Gaussian law this is the theorem of Cameron and Martin. For one input with all moments finite, Ernst, Mugler, Starkloff and Ullmann relate density to the determinacy of the moment problem: it holds for the uniform, Gaussian, gamma and beta laws, and it fails for polynomials in a lognormal variable.
- The output is a smooth function of the inputs. Then the coefficients decay fast and a low degree is enough. Kinks, jumps and bifurcations make the coefficients decay slowly.
- The number of inputs is moderate: the total degree basis of degree $p$ in $d$ inputs has $\binom{d+p}{p}$ terms.

## The template

**Notation.** $\psi^{(k)}_n$ is the orthonormal polynomial of degree $n$ for the law of $\xi_k$. $\mathcal{A}$ is a finite set of multi-indices that contains 0. The truncated expansion is $q_{\mathcal{A}} = \sum_{\alpha \in \mathcal{A}} c_\alpha \Psi_\alpha$.

```pseudo id=main
POLYNOMIAL-CHAOS(q, ρ, 𝒜)
L1  for each input k, choose the orthonormal family ψ^(k) for the law of ξ_k     ▷ hole: the family (Askey scheme)
L2  choose the index set 𝒜                                                         ▷ hole: total degree, hyperbolic, adaptive
L3  compute c_α ≈ E[q Ψ_α] for α in 𝒜                                             ▷ hole: Galerkin, projection, regression, l1
L4  mean ← c_0;  variance ← Σ_{α ≠ 0} c_α^2
L5  S_k ← Σ over α that involve only ξ_k of c_α^2 / variance                      ▷ first-order Sobol indices
L6  return the surrogate Σ c_α Ψ_α, the moments and the indices
```

Line L1 is the choice that [generalized polynomial chaos](/generalized-polynomial-chaos/) makes by the Askey scheme: Hermite polynomials for Gaussian inputs, Legendre for uniform, Laguerre for gamma, Jacobi for beta. Line L2 fixes the truncation; the total degree set $\{|\alpha| \le p\}$ is the default. Line L3 is the main hole, and the methods below fill it. Lines L4 and L5 need no more model runs.

**Best approximation (proved).** In $L^2_\rho$, the truncated expansion with the exact coefficients is the orthogonal projection of $q$ onto $\operatorname{span}\{\Psi_\alpha : \alpha \in \mathcal{A}\}$, so it is the best approximation there:

$$\|q - q_{\mathcal{A}}\|^2 = \sum_{\alpha \notin \mathcal{A}} c_\alpha^2 = \min_{v} \|q - v\|^2.$$

*Proof.* For $v = \sum_{\alpha \in \mathcal{A}} v_\alpha \Psi_\alpha$, $q - q_{\mathcal{A}}$ is orthogonal to every $\Psi_\alpha$ with $\alpha \in \mathcal{A}$, so by Pythagoras $\|q - v\|^2 = \|q - q_{\mathcal{A}}\|^2 + \sum_{\alpha \in \mathcal{A}} (c_\alpha - v_\alpha)^2$. If the $\Psi_\alpha$ are complete, Parseval's identity $\|q\|^2 = \sum_\alpha c_\alpha^2$ gives the tail sum. $\square$

The moments of line L4 follow because $\mathbb{E}[\Psi_\alpha] = \mathbb{E}[\Psi_\alpha \Psi_0] = 0$ for $\alpha \neq 0$, so $\mathbb{E}[q] = c_0$ and $\operatorname{Var}[q] = \|q\|^2 - c_0^2 = \sum_{\alpha \neq 0} c_\alpha^2$.

## Classic examples

**The exponential of a Gaussian.** Let $\xi \sim N(0, 1)$ and $q = e^\xi$, a lognormal output. With the orthonormal Hermite polynomials $\psi_n = \mathrm{He}_n / \sqrt{n!}$, the generating function $e^{t x - t^2/2} = \sum_n \mathrm{He}_n(x) t^n / n!$ at $t = 1$ gives $c_n = e^{1/2} / \sqrt{n!}$. The mean is $c_0 = e^{1/2} = 1.6487$ and the variance is $e^2 - e = 4.6708$. The relative error of the degree $p$ truncation, $\|q - q_p\| / \operatorname{sd}(q)$, is

| $p$ | $c_p$ | relative error |
|---|---|---|
| 1 | 1.6487 | 0.646 |
| 2 | 1.1658 | 0.356 |
| 3 | 0.6731 | 0.173 |
| 4 | 0.3365 | 0.0761 |
| 6 | 0.06144 | 0.0115 |
| 8 | 0.008211 | 0.00133 |

The coefficients decay faster than any geometric rate because $e^\xi$ is an entire function.

**A kink.** For $q = |\xi|$ with the same input, every odd coefficient is 0 and the relative error is 0.352, 0.226, 0.139, 0.084 and 0.050 at $p = 2, 4, 8, 16, 32$, so it falls only like $p^{-3/4}$. A function that is not smooth needs many terms, and a quantity such as the probability of $q > t$ computed from the surrogate is worse.

**Intrusive coefficients.** The [stochastic Galerkin method](/stochastic-galerkin-method/) puts the expansion into the model equations and asks the residual to be orthogonal to every $\Psi_\alpha$, which gives one coupled system for all coefficients.

**Projection by quadrature.** [Non-intrusive spectral projection](/non-intrusive-spectral-projection/) computes each $c_\alpha = \mathbb{E}[q \Psi_\alpha]$ by a [Gaussian quadrature](/gaussian-quadrature/) rule on the input law, with one model run per node.

**Regression.** [Regression polynomial chaos](/regression-polynomial-chaos/) fits the coefficients by least squares to random model runs, and [sparse polynomial chaos](/sparse-polynomial-chaos/) uses $\ell_1$ minimization when there are fewer runs than terms.

**Sensitivity.** The [Sobol indices](/sobol-indices/) of the output come from the coefficients: the total index of $\xi_k$ is the sum of $c_\alpha^2$ over all $\alpha$ with $\alpha_k > 0$, divided by the variance (Sudret 2008).

## Variations

- **Generalized polynomial chaos.** Use the family orthogonal for the actual input law, from the Askey scheme or computed numerically.
- **Arbitrary polynomial chaos.** Build orthonormal polynomials from the moments of data, by [Gram-Schmidt](/gram-schmidt-process/) or a three-term recurrence, when the law is known only through samples.
- **Index sets.** Hyperbolic sets $\{\alpha : (\sum_k \alpha_k^q)^{1/q} \le p\}$ with $q < 1$ keep high degrees in one input and drop high order interactions.
- **Multi-element and local expansions.** Split the input space into cells and use a separate expansion in each, for outputs with jumps.
- **Wiener chaos for random fields and processes.** The original setting: a functional of Brownian motion expanded in Hermite polynomials of countably many Gaussian variables.
- **Vector outputs.** Expand each output, or the leading modes of a principal component decomposition of the outputs, with the same basis.

## Pitfalls

- **Wrong family.** Hermite polynomials of a uniform input, or of a Gaussian input mapped from a uniform one, converge more slowly than the matched Legendre family; see [generalized polynomial chaos](/generalized-polynomial-chaos/).
- **Polynomials in a lognormal variable.** They are not dense in $L^2$, so a series in them need not converge to the output. Expand in the underlying Gaussian variable instead, as in the first example.
- **The curse of dimension.** $\binom{d+p}{p}$ grows fast: 10 inputs at degree 5 give 3003 terms. Use sparse index sets or sparse recovery.
- **Non-smooth outputs.** Kinks and jumps give slow convergence and oscillations, as in the second example.
- **Tails.** Mean square convergence does not control the tails. A probability of $10^{-4}$ read from a surrogate can be wrong even when the variance is right; check with a [reliability method](/first-order-reliability-method/) on the true model.
- **Dependent inputs.** The product basis is orthonormal only for independent inputs. Map dependent inputs to independent ones first.

## Exercises

1. Show that the orthonormal Hermite coefficients of $e^{a \xi}$ are $e^{a^2/2} a^n / \sqrt{n!}$, and find the variance from them.
2. Prove that $\mathbb{E}[q] = c_0$ and $\operatorname{Var}[q] = \sum_{\alpha \neq 0} c_\alpha^2$ for every $q$ in $L^2_\rho$ when the basis is complete.
3. For $d$ inputs and total degree $p$, count the multi-indices with $|\alpha| \le p$ and show that the count is $\binom{d+p}{p}$.
4. Compute the first-order Sobol indices of $q = \xi_1 + \xi_1 \xi_2$ with independent standard normal inputs from its expansion.
5. Explain why the odd coefficients of $|\xi|$ vanish, and estimate the decay of the even coefficients from the error table.

## References
