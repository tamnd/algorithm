---
tag: PVRX8R
kind: problem
slug: forward-uncertainty-propagation
name: Forward uncertainty propagation
aliases:
- uncertainty propagation
area: scientific-computing/uncertainty-quantification
level: intro
summary: Given a model and the probability distributions of its inputs, compute the distribution, moments or failure probabilities of its outputs.
model: real-ram
prereqs: [random-variable, expected-value, variance]
see_also: [monte-carlo-integration, multilevel-monte-carlo, polynomial-chaos-expansion, stochastic-collocation-method, sobol-indices, random-field, bayesian-inverse-problem, first-order-reliability-method]
sources:
  - book: isbn:9781611973211
    title: Ralph C. Smith, Uncertainty Quantification. Theory, Implementation, and Applications, SIAM, 2014
    locator: the chapters on the propagation of uncertainty in models (sampling, perturbation and stochastic spectral methods) and on the representation of random inputs
  - book: isbn:9783319233949
    title: T. J. Sullivan, Introduction to Uncertainty Quantification, Springer, Texts in Applied Mathematics 63, 2015
    locator: the chapters on the forward problem, Monte Carlo and quadrature, spectral expansions, the stochastic Galerkin method and non-intrusive methods
  - book: isbn:9780691142128
    title: Dongbin Xiu, Numerical Methods for Stochastic Computations. A Spectral Method Approach, Princeton University Press, 2010
    locator: Chapter 1 (the problem of propagating input uncertainty through a model) and the chapters on generalized polynomial chaos, the stochastic Galerkin method and stochastic collocation
  - paper: doi:10.1017/S096249291500001X
    title: Michael B. Giles, Multilevel Monte Carlo methods, Acta Numerica 24, 2015, 259-328
    locator: Section 1 (Monte Carlo cost and the multilevel complexity) and the applications to random coefficient PDEs
---

Forward uncertainty propagation asks how the uncertainty of the inputs of a model carries over to its outputs. The inputs, such as material properties, loads, rate constants or initial data, are modelled as random variables or [random fields](/random-field/) with known laws. The model, often a differential equation solved numerically, maps each input to an output, and the task is to find the law of a quantity of interest computed from that output: its mean and variance, a quantile, or the probability that it passes a safety limit. Every method makes a trade between the number of model runs, which are expensive, and the smoothness and dimension of the map from the inputs to the output.

## In plain words

A computer model takes some numbers in and gives a number out. Some of the input numbers are not known exactly; you only know which values are likely and which are rare.

The question is: given that, which output values are likely? How large is the output on average, how much does it spread, and how often does it go over a danger line?

The simplest answer is to draw many random inputs, run the model on each, and look at the outputs. That works for any model, but it needs many runs. Better methods use fewer runs by spreading the inputs more evenly, by running cheaper rough versions of the model, or by fitting a simple formula to the model and using the formula instead.

## Definition

Let $(\Omega, \mathcal{F}, \mathbb{P})$ be a probability space and $\xi : \Omega \to \Gamma \subseteq \mathbb{R}^d$ a random input with law $\mu$; if the input is a random field, $\xi$ is the vector of its first $d$ Karhunen-Loève coefficients. Let $u(\xi)$ be the model output, for example the solution of a partial differential equation with data $\xi$, and $Q = q(u(\xi))$ a scalar quantity of interest. The law of $Q$ is the pushforward $\mu \circ (q \circ u)^{-1}$.

**Input:** the law $\mu$; access to the model, either as a black box that returns $Q$ (or an approximation $Q_h$ at discretization level $h$) for a given $\xi$ at cost $C$ per run, or as the equations themselves; and a tolerance $\varepsilon$.

**Output:** an estimate of one or more of

- the moments $\mathbb{E}[Q]$, $\mathrm{Var}(Q)$ and $\mathbb{E}[g(Q)]$ for a given $g$;
- the distribution function $F_Q(t) = \mathbb{P}(Q \le t)$, a quantile, or a density;
- a failure probability $p_f = \mathbb{P}(Q > q^*)$ for a threshold $q^*$;

with a root mean square error, or an error with a stated confidence, at most $\varepsilon$. The cost is the number of model runs times their cost, or for an intrusive method the cost of solving the coupled system.

## Variants

- **Moments, laws and rare events.** Estimating $\mathbb{E}[Q]$ to a tolerance is an integration problem; estimating $p_f$ for small $p_f$ is a rare event problem, where relative error matters; estimating the whole law $F_Q$ asks for all quantiles at once.
- **Sensitivity analysis.** Besides the law of $Q$, find which inputs cause its variance, with [Sobol indices](/sobol-indices/) or with screening by the [Morris method](/morris-method/).
- **Intrusive and non-intrusive.** Non-intrusive methods only run the existing solver at chosen inputs. Intrusive methods, such as the [stochastic Galerkin method](/stochastic-galerkin-method/), rewrite the model equations into one larger deterministic system for the coefficients of the output.
- **Finite and infinite dimension.** With a few scalar inputs, $d$ is small. With a random field input, $d$ is in principle infinite, and a truncation adds an error that must be balanced with the others.
- **Dependent inputs.** With dependent inputs, $\mu$ is given by marginals and a copula, or by a joint density, and a transformation such as the Rosenblatt transformation maps $\xi$ to independent variables first.
- **Epistemic uncertainty.** When the input law itself is not known, the problem becomes one of bounds over a set of laws, such as intervals or imprecise probabilities, or of a law over laws.
- **Time-dependent outputs.** $Q$ may be a trajectory, and the task is its law at each time or the law of a time maximum.

## Examples

**One lognormal output.** Let $\xi$ be standard normal and $Q = e^{\xi}$. The exact law is lognormal, with $\mathbb{E}[Q] = e^{1/2} = 1.64872$, $\mathrm{Var}(Q) = e^2 - e = 4.67077$ and $\mathbb{P}(Q > 5) = \mathbb{P}(\xi > \ln 5) = 0.05376$. Three ways to estimate the mean:

| method | estimate of $\mathbb{E}[Q]$ | estimate of $\mathrm{Var}(Q)$ | comment |
|---|---|---|---|
| linearization at the mean | $e^0 = 1$ | $1$ | the first order perturbation method; 39 percent low |
| second order perturbation | $1 + \frac{1}{2} = 1.5$ | | still 9 percent low |
| Monte Carlo, $N = 10^4$ | unbiased, with standard error $0.0216$ | unbiased | the error is $\sqrt{4.67077/N}$, a theorem |

The perturbation methods are cheap but biased for a nonlinear map with a large input spread. Monte Carlo is unbiased at any spread, and its error does not depend on the map, only on its variance.

**A random coefficient.** Let $-(a u')' = 1$ on $(0, 1)$ with $u(0) = u(1) = 0$, and let the coefficient be a random constant $a = e^{\xi}$ with $\xi$ standard normal. The solution is $u(x) = x(1 - x)/(2a)$, so $Q = u(1/2) = e^{-\xi}/8$, with mean $e^{1/2}/8 = 0.20609$. With a random field $a(x)$ instead of a constant there is no closed form, each run needs a numerical solve, and $Q_h$ depends on the mesh, which is the setting of [multilevel Monte Carlo](/multilevel-monte-carlo/).

**A failure probability.** For $p_f = 0.05376$ in the first example, the relative standard error of plain Monte Carlo is $\sqrt{(1 - p_f)/(N p_f)}$, so a 10 percent relative error needs about $N = 1760$ runs; for $p_f = 10^{-6}$ it needs about $10^8$. This is why rare events need special methods.

## Known algorithms

- **Sampling.** [Monte Carlo integration](/monte-carlo-integration/) with independent samples; [Latin hypercube sampling](/latin-hypercube-sampling/), which stratifies each input; [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/) with low discrepancy points such as the [Sobol sequence](/sobol-sequence/).
- **Many levels or fidelities.** [Multilevel Monte Carlo](/multilevel-monte-carlo/) on a hierarchy of discretizations; [multifidelity Monte Carlo](/multifidelity-monte-carlo/) with cheaper models as control variates.
- **Spectral and surrogate methods.** The [polynomial chaos expansion](/polynomial-chaos-expansion/) and [generalized polynomial chaos](/generalized-polynomial-chaos/); the [stochastic collocation method](/stochastic-collocation-method/) on sparse grids; the [stochastic Galerkin method](/stochastic-galerkin-method/); Gaussian process surrogates ([kriging](/kriging/)); the [reduced basis method](/reduced-basis-method/) for parametric PDEs.
- **Rare events.** The [first order reliability method](/first-order-reliability-method/), which linearizes the limit state at the most probable failure point; [importance sampling](/importance-sampling/); [subset simulation](/subset-simulation/).
- **Sensitivity.** The [Saltelli sampling scheme](/saltelli-sampling-scheme/), the [Fourier amplitude sensitivity test](/fourier-amplitude-sensitivity-test/) and the Morris method.

## Bounds

- **Monte Carlo.** With $N$ independent runs, the root mean square error of the sample mean is $\sigma_Q / \sqrt{N}$, so a tolerance $\varepsilon$ costs $N = \sigma_Q^2 / \varepsilon^2$ runs, for any dimension $d$ (a theorem). Confidence intervals come from the [central limit theorem](/central-limit-theorem/).
- **Discretization.** If $|\mathbb{E}[Q_h - Q]| = O(h^{\alpha})$ and a run costs $O(h^{-\gamma})$, plain Monte Carlo with $Q_h$ costs $O(\varepsilon^{-2 - \gamma/\alpha})$. Under the conditions of the [MLMC complexity theorem](/mlmc-complexity-theorem/) with a variance rate $\beta > \gamma$, multilevel Monte Carlo costs $O(\varepsilon^{-2})$, the cost of plain Monte Carlo with exact samples of unit cost.
- **Quasi-Monte Carlo.** By the Koksma-Hlawka inequality, the error is at most the Hardy-Krause variation of the integrand times the star discrepancy of the points, which is $O((\log N)^d / N)$ for low discrepancy sequences (a theorem). The bound is useful only for small $d$ or integrands of low effective dimension.
- **Deterministic quadrature.** For integrands with $r$ bounded derivatives on $[0, 1]^d$, the best worst-case error of a deterministic rule with $N$ points is of order $N^{-r/d}$ (a theorem of Bakhvalov), which is the [curse of dimensionality](/curse-of-dimensionality/) for large $d$.
- **Spectral methods.** If $Q$ depends analytically on $\xi$, polynomial chaos and collocation errors fall faster than any power of the polynomial degree $p$. A total degree basis has $\binom{d + p}{p}$ terms, which grows like $d^p / p!$ in $d$; this is the limit of spectral methods for large $d$.
- **Rare events.** For plain Monte Carlo, the relative error for $p_f$ is $\sqrt{(1 - p_f)/(N p_f)}$, so a fixed relative error costs $O(1/p_f)$ runs (a theorem).

## Reductions

- **Moments are integrals.** $\mathbb{E}[g(Q)] = \int_{\Gamma} g(q(u(\xi)))\, d\mu(\xi)$, so estimating a moment is [numerical integration](/numerical-integration/) over the input law, and every integration method applies.
- **Probabilities are moments.** $p_f = \mathbb{E}[\mathbf{1}\{Q > q^*\}]$ and $F_Q(t) = \mathbb{E}[\mathbf{1}\{Q \le t\}]$, so they are integrals of indicator functions, which are not smooth; this is why spectral methods and quasi-Monte Carlo lose their fast rates on them.
- **Input transformation.** By [inverse transform sampling](/inverse-transform-sampling/) or the Rosenblatt transformation, any input law reduces to independent uniform or normal variables, so a method needs only one reference law.
- **Fields to vectors.** A [random field](/random-field/) input reduces to finitely many random variables by its truncated [Karhunen-Loève expansion](/karhunen-loeve-theorem/).
- **Surrogates.** Fitting a cheap approximation $\tilde{Q}(\xi)$ to $Q$ reduces the problem to propagation through $\tilde{Q}$, where sampling is nearly free, plus the error of the approximation.
- **The inverse problem.** A [Bayesian inverse problem](/bayesian-inverse-problem/) and [calibration](/kennedy-ohagan-calibration/) need the forward map at many inputs inside a sampler, so forward propagation is their inner step.

## Applications

Forward propagation is used to set safety margins in structural reliability, where $p_f$ is the probability of failure of a structure under random loads and strengths; in subsurface flow, where the permeability is a random field and $Q$ is a flow rate or a travel time; in nuclear reactor safety and in the certification of aircraft components; in weather and climate prediction, where ensembles of runs propagate the uncertainty of initial states and parameters; and in finance, where the mean of a discounted payoff under a random asset path is the price of an option.

## References
