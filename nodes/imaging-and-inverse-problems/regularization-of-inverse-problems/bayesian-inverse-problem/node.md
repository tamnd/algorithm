---
tag: EPTVPM
kind: concept
slug: bayesian-inverse-problem
name: Bayesian inverse problem
aliases:
- statistical inversion
- Bayesian inversion
area: imaging-and-inverse-problems/regularization-of-inverse-problems
level: advanced
summary: "Treat the unknown as a random variable, so that the solution of the inverse problem is the posterior distribution given the data, prior and noise model."
prereqs: [bayes-theorem, inverse-problem, tikhonov-regularization]
see_also: [linear-gaussian-inverse-problem, maximum-a-posteriori-estimation, preconditioned-crank-nicolson-mcmc, randomize-then-optimize, laplace-approximation, ensemble-kalman-inversion, bayesian-inverse-problem-well-posedness, regularization-parameter-choice]
sources:
  - paper: doi:10.1017/S0962492910000061
    title: Andrew M. Stuart, Inverse problems, a Bayesian perspective, Acta Numerica 19, 2010
    locator: pages 451 to 559
  - book: isbn:9780387220734
    title: Jari Kaipio and Erkki Somersalo, Statistical and Computational Inverse Problems, Springer, 2005
  - paper: doi:10.1007/978-3-319-12385-1_7
    title: Masoumeh Dashti and Andrew M. Stuart, The Bayesian approach to inverse problems, in Handbook of Uncertainty Quantification, Springer, 2017
    locator: pages 311 to 428
---

A Bayesian inverse problem treats the unknown $u$ and the noise as random variables. Before the data are seen, $u$ has a prior distribution $\mu_0$. The noise model gives the likelihood of the data $y$ for each $u$. Bayes' theorem combines the two into the posterior distribution of $u$ given $y$, and that distribution is the solution. A point estimate, such as the posterior mean or the maximum a posteriori (MAP) point, is one summary of it; credible intervals and the probability of events are others. For a linear forward map with Gaussian prior and noise, the MAP point is exactly a Tikhonov solution, so the Bayesian view contains classical regularization and adds a measure of uncertainty. For nonlinear maps or non-Gaussian priors, the posterior has no closed form and is explored by sampling methods such as [preconditioned Crank-Nicolson MCMC](/preconditioned-crank-nicolson-mcmc/) and [randomize-then-optimize](/randomize-then-optimize/), or approximated.

## In plain words

You do not ask for one answer. You ask how plausible every possible answer is. You start with a belief about the unknown before you look at the data, for example that it is smooth. You also say how noisy the measurements are. The data then make some answers more plausible and others less. The result is a probability distribution over answers. Its peak is the classical regularized answer. Its width tells you how sure you can be, and it shows which parts of the unknown the data do not fix at all.

## The idea

**Setting.** The data are $y = G(u) + \eta$, with the forward map $G: X \to \mathbb{R}^m$ (see [forward operator](/forward-operator/)), the unknown $u$ in a space $X$, and noise $\eta \sim N(0, \Gamma)$ independent of $u$. The prior is a probability measure $\mu_0$ on $X$.

**Bayes' formula.** Define the misfit, or negative log-likelihood up to a constant,

$$\Phi(u; y) = \tfrac12\lVert\Gamma^{-1/2}(y - G(u))\rVert^2.$$

In finite dimensions, with a prior density $\pi_0$, the posterior density is

$$\pi^y(u) = \frac{1}{Z(y)}\exp(-\Phi(u; y))\,\pi_0(u), \qquad Z(y) = \int\exp(-\Phi(u; y))\,\pi_0(u)\,du.$$

When $X$ is a function space there is no Lebesgue density, and the same statement is written as a density of the posterior $\mu^y$ with respect to the prior,

$$\frac{d\mu^y}{d\mu_0}(u) = \frac{1}{Z(y)}\exp(-\Phi(u; y)).$$

Stuart (2010) gives conditions on $\Phi$ and $\mu_0$ under which this defines a probability measure that depends continuously on $y$ in the Hellinger metric. So the Bayesian problem is well posed even when the inverse problem $G(u) = y$ is not; see [well-posedness of the Bayesian inverse problem](/bayesian-inverse-problem-well-posedness/).

**The link to Tikhonov regularization.** Take a Gaussian prior $N(m_0, C_0)$ in finite dimensions. Then $-\log\pi^y(u)$ is, up to a constant,

$$\tfrac12\lVert\Gamma^{-1/2}(y - G(u))\rVert^2 + \tfrac12\lVert C_0^{-1/2}(u - m_0)\rVert^2,$$

and the MAP point is the minimizer of this Tikhonov functional; see [maximum a posteriori estimation](/maximum-a-posteriori-estimation/). With $\Gamma = \sigma^2I$, $C_0 = \gamma^2I$ and $m_0 = 0$, it is Tikhonov regularization with parameter $\alpha = \sigma^2/\gamma^2$. The regularization parameter is a ratio of noise variance to prior variance, and choosing it becomes a modeling question or a hyperparameter estimation problem; see [regularization parameter choice](/regularization-parameter-choice/).

**The linear Gaussian case.** If $G(u) = Au$ is linear, the posterior is Gaussian with

$$C_{\mathrm{post}} = (A^T\Gamma^{-1}A + C_0^{-1})^{-1}, \qquad m_{\mathrm{post}} = C_{\mathrm{post}}(A^T\Gamma^{-1}y + C_0^{-1}m_0).$$

The mean equals the MAP point. See [linear Gaussian inverse problem](/linear-gaussian-inverse-problem/).

**Computing with the posterior.** Outside the linear Gaussian case the posterior must be computed numerically:

- the MAP point by optimization, and a Gaussian approximation around it by the [Laplace approximation](/laplace-approximation/);
- samples by Markov chain Monte Carlo, for example [random-walk Metropolis](/random-walk-metropolis/), [MALA](/metropolis-adjusted-langevin-algorithm/), [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/), and on function spaces [pCN](/preconditioned-crank-nicolson-mcmc/), whose acceptance rate does not degrade as the discretization is refined;
- samples by optimization, as in [randomize-then-optimize](/randomize-then-optimize/), which solves a perturbed least squares problem for each sample;
- approximations by [ensemble Kalman inversion](/ensemble-kalman-inversion/) and [variational inference](/variational-inference/).

**Discretize last.** The function-space form suggests defining the posterior on $X$ first and discretizing it after. Then priors, algorithms and error bounds do not depend on the mesh, and a method that works on the infinite-dimensional problem keeps its behavior as the mesh is refined. This is the reason for pCN.

## Examples

**A scalar problem.** Let $y = au + \eta$ with $a = 0.1$, $\eta \sim N(0, \sigma^2)$, $\sigma = 0.05$, prior $u \sim N(0, 1)$, and observed $y = 0.12$. Least squares gives $u = y/a = 1.2$ with standard deviation $\sigma/a = 0.5$. The posterior is Gaussian with variance

$$\Big(\frac{a^2}{\sigma^2} + 1\Big)^{-1} = \frac{1}{4 + 1} = 0.2$$

and mean $0.2 \cdot ay/\sigma^2 = 0.2 \cdot 4.8 = 0.96$. Tikhonov with $\alpha = \sigma^2/1 = 0.0025$ gives $ay/(a^2 + \alpha) = 0.012/0.0125 = 0.96$, the same number. The posterior standard deviation is $0.447$, a little smaller than the prior one, because the data carry about four times the information of the prior here.

**Which components the data fix.** Take the diagonal problem $A = \mathrm{diag}(s_i)$ with $s_i = 1/i^2$, noise $\sigma = 10^{-3}$ and prior $N(0, I)$. Each coefficient has posterior variance $(s_i^2/\sigma^2 + 1)^{-1} = (10^6/i^4 + 1)^{-1}$. For $i = 1$ this is about $10^{-6}$: the data fix the coefficient. For $i = 32$ it is $0.51$, and for larger $i$ it tends to $1$, the prior variance: the data say almost nothing, and the posterior returns the prior. The crossover at $i^4 \approx 10^6$ is where the filter factor $s_i^2/(s_i^2 + \alpha)$ of Tikhonov regularization with $\alpha = \sigma^2$ passes $1/2$. This is exact arithmetic on the formula, not a measurement.

**A nonlinear problem.** In electrical impedance tomography, $G$ maps a conductivity field to boundary voltages, and the posterior is non-Gaussian and on a function space. Typical practice is a Gaussian or Besov prior on the log-conductivity, a MAP estimate by Gauss-Newton, and pCN or a Laplace approximation for uncertainty.

## Where it is used

- Medical and geophysical imaging, where uncertainty of the image matters for decisions; Kaipio and Somersalo use electrical impedance tomography as a main example.
- Data assimilation in weather and ocean models, where the [Kalman filter](/kalman-filter/) and its ensemble forms are Bayesian updates.
- Calibration of partial differential equation models from measurements, and design of experiments that minimize posterior uncertainty.
- Hierarchical models, where the noise level and the prior scale get their own priors, which gives a Bayesian answer to the parameter choice problem.

The view goes back to work on statistical inversion in the 1970s, such as Franklin's 1970 paper on stochastic extensions of ill-posed linear problems, and to Tarantola's books in geophysics. The function-space formulation with $d\mu^y/d\mu_0$ and well-posedness in the Hellinger metric is from Stuart (2010). These historical notes are general; no exact locators are given for the older works.

## References
