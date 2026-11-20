---
tag: 6BFBPS
kind: model
slug: kennedy-ohagan-calibration
name: "Kennedy-O'Hagan calibration model"
aliases:
- Bayesian calibration of computer models
area: scientific-computing/uncertainty-quantification
level: advanced
summary: Models data as a simulator at unknown parameters plus a Gaussian process discrepancy plus noise, and infers parameters and discrepancy together.
model: real-ram
history:
  year: 2001
  people: [Marc C. Kennedy, "Anthony O'Hagan"]
  note: "Kennedy and O'Hagan put a Gaussian process prior on the simulator and on its discrepancy from reality, so that calibration accounts for the code uncertainty and for the model error. Brynjarsdóttir and O'Hagan showed in 2014 that the calibrated parameters are only meaningful with real prior knowledge of the discrepancy."
prereqs: [gaussian-process, bayes-theorem]
see_also: [kriging, bayesian-inverse-problem, metropolis-hastings, marginal-likelihood, forward-uncertainty-propagation, latin-hypercube-sampling, cholesky-decomposition, approximate-bayesian-computation]
sources:
  - paper: doi:10.1111/1467-9868.00294
    title: "Marc C. Kennedy and Anthony O'Hagan, Bayesian calibration of computer models, Journal of the Royal Statistical Society Series B 63(3), 2001, 425-464"
    locator: the model for the field data with the simulator, the scale parameter and the discrepancy, the Gaussian process priors, and the estimation of the hyperparameters before the posterior of the calibration parameters
  - paper: doi:10.1088/0266-5611/30/11/114007
    title: "Jenný Brynjarsdóttir and Anthony O'Hagan, Learning about physical parameters: the importance of model discrepancy, Inverse Problems 30(11), 2014, 114007"
    locator: the simple machine example, and the bias and overconfidence of calibration without a discrepancy or with an uninformative one
---

The Kennedy-O'Hagan model is a statistical model for the calibration of a computer simulator against field measurements. The simulator $\eta(x, t)$ has control inputs $x$, which the experimenter sets and knows, and calibration inputs $t$, which are physical constants or tuning parameters with an unknown best value $\theta$. The model says that reality is the simulator at $\theta$ plus a discrepancy, $\zeta(x) = \rho\, \eta(x, \theta) + \delta(x)$, and that each measurement is reality plus noise. Both the simulator, which is too expensive to run everywhere, and the discrepancy are given [Gaussian process](/gaussian-process/) priors. With [Bayes' theorem](/bayes-theorem/) the model gives a posterior for $\theta$ and a prediction of reality at new inputs, with three sources of uncertainty: the noise, the unknown simulator between its runs, and the model error.

A [Bayesian inverse problem](/bayesian-inverse-problem/) also puts a prior on $\theta$ and takes a posterior, but it assumes that data equals the forward map at $\theta$ plus noise, so all misfit is noise. The Kennedy-O'Hagan model adds the term $\delta$ for the misfit that the simulator cannot remove at any $\theta$. [Gaussian process regression](/gaussian-process/) or [kriging](/kriging/) of the field data alone has no simulator and no $\theta$; the Kennedy-O'Hagan model uses it twice, once as an emulator of $\eta$ and once for $\delta$.

## The machine

**The data.**

- Simulator runs: outputs $y_j = \eta(x^*_j, t_j)$ for $j = 1, \ldots, N$ at a design of points $(x^*_j, t_j)$, often from [Latin hypercube sampling](/latin-hypercube-sampling/).
- Field data: $z_i = \zeta(x_i) + e_i$ for $i = 1, \ldots, n$, with independent noise $e_i \sim N(0, \lambda)$.

**The model.**

$$z_i = \rho\, \eta(x_i, \theta) + \delta(x_i) + e_i .$$

- $\theta$ is the unknown best value of the calibration inputs, with a prior $p(\theta)$.
- $\rho$ is an unknown scale, often fixed to 1.
- $\eta(\cdot, \cdot)$ has a Gaussian process prior with mean $h_1(x, t)^T \beta_1$ and covariance $\sigma_1^2 c_1((x, t), (x', t'))$, for example a squared exponential with one length scale per input.
- $\delta(\cdot)$ has an independent Gaussian process prior with mean $h_2(x)^T \beta_2$ and covariance $\sigma_2^2 c_2(x, x')$.
- The hyperparameters are $\phi = (\beta_1, \sigma_1^2, \beta_2, \sigma_2^2, \lambda, \rho)$ and the length scales.

**The joint distribution.** Given $\theta$ and $\phi$, the vector $d = (y, z)$ is Gaussian, because it is linear in the two processes and the noise. Its covariance has the block form

$$V_d(\theta) = \begin{pmatrix} \sigma_1^2 C_1(D_1, D_1) & \rho \sigma_1^2 C_1(D_1, D_2(\theta)) \\ \rho \sigma_1^2 C_1(D_2(\theta), D_1) & \rho^2 \sigma_1^2 C_1(D_2(\theta), D_2(\theta)) + \sigma_2^2 C_2(X, X) + \lambda I \end{pmatrix},$$

where $D_1$ is the design of the runs, $D_2(\theta)$ is the set of points $(x_i, \theta)$, and $X$ is the set of the $x_i$. So the likelihood of $\theta$ is a Gaussian density with a covariance that depends on $\theta$.

**The inference.**

- Kennedy and O'Hagan estimate the hyperparameters first, those of $\eta$ from the runs alone and the rest from all data, and then plug them in.
- The posterior of $\theta$ is $p(\theta \mid d, \hat\phi) \propto p(\theta)\, N(d; m_d(\theta), V_d(\theta))$, computed by numerical integration over a low-dimensional $\theta$.
- A full Bayesian version also samples $\phi$, for example by [Metropolis-Hastings](/metropolis-hastings/).

**The prediction.** For a new $x$, the posterior of $\zeta(x)$ given $d$ and $\theta$ is Gaussian by the conditioning formulas of Gaussian process regression, and the prediction averages it over the posterior of $\theta$.

## What it counts

The model gives three outputs:

- the posterior of the calibration parameters $\theta$;
- the posterior of the discrepancy $\delta(x)$;
- the predictive distribution of reality $\zeta(x)$ and of new measurements.

The main cost is the Gaussian likelihood. Each value of $\theta$ needs a [Cholesky factorization](/cholesky-decomposition/) of the $(N + n) \times (N + n)$ matrix $V_d(\theta)$, which costs $O((N + n)^3)$ in the [real RAM](/real-ram/) model, and $O((N + n)^2)$ memory. A grid over $\theta$ or an MCMC run multiplies this by the number of evaluations. The simulator itself is only run at the $N$ design points, before the inference.

## Relation to other models

- **Bayesian inverse problems.** With $\delta = 0$, an exact simulator ($N = \infty$, or a cheap $\eta$) and $\rho = 1$, the model is the Bayesian inverse problem $z = \eta(X, \theta) + e$. The [well-posedness theorem](/bayesian-inverse-problem-well-posedness/) of that setting applies to the posterior of $\theta$ for fixed hyperparameters.
- **Least squares calibration.** Fitting $\theta$ by least squares between $z$ and $\eta(X, \theta)$ gives a point estimate with no discrepancy and no code uncertainty.
- **Gaussian process regression.** With no simulator ($\rho = 0$), the model is Gaussian process regression of the field data with the covariance of $\delta$ and noise $\lambda$. The emulator part alone is the regression of the runs, as in [kriging](/kriging/) of computer experiments.
- **Approximate Bayesian computation.** [ABC](/approximate-bayesian-computation/) also calibrates simulators by Bayes, but with simulated data instead of a likelihood, and usually with no explicit discrepancy.
- **Forward propagation.** After calibration, the posterior of $\theta$ is the input distribution for [forward uncertainty propagation](/forward-uncertainty-propagation/) of the simulator.

## Known results in the model

**Non-identifiability (theorem, by hand).** Take a scalar $\theta$ with the prior $N(0, 1)$, the simulator $\eta(x, t) = t$, $\rho = 1$, and a discrepancy that is a constant bias, $\delta(x) = b$ with $b \sim N(0, s^2)$ (a Gaussian process with $c_2 \equiv 1$). Then every measurement is $z_i = \theta + b + e_i$ with $e_i \sim N(0, \lambda)$. The mean $\bar z$ is sufficient, and $\bar z = \theta + b + \bar e$ with $\bar e \sim N(0, \lambda / n)$. By the formulas for a Gaussian pair,

$$\operatorname{Var}(\theta \mid z) = 1 - \frac{1}{1 + s^2 + \lambda / n} = \frac{s^2 + \lambda / n}{1 + s^2 + \lambda / n} \ \ge\ \frac{s^2}{1 + s^2}, \qquad \operatorname{E}(\theta \mid z) = \frac{\bar z}{1 + s^2 + \lambda / n}.$$

The data only fix $\theta + b$. As $n \to \infty$, the posterior variance goes to $s^2/(1 + s^2)$, not to 0, so $\theta$ cannot be learned beyond its prior information and the prior of $b$. The same holds in the general form: for $\Sigma = s^2 C_2(X, X) + \lambda I$, $\operatorname{Var}(\theta \mid z) = 1 / (1 + \mathbf{1}^T \Sigma^{-1} \mathbf{1})$, and with $C_2 = \mathbf{1} \mathbf{1}^T$ the Sherman-Morrison formula gives $\mathbf{1}^T \Sigma^{-1} \mathbf{1} = n / (\lambda + n s^2)$, which is the formula above.

**Overconfidence without a discrepancy (by hand).** Let $s^2 = 1$, $\lambda = 0.25$, $n = 10$, the true $\theta = 0.6$ and the true bias $b = 0.4$, and let the noise average to 0, so $\bar z = 1$.

- With the discrepancy, the posterior is $N(1 / 2.025, 1.025 / 2.025) = N(0.494, 0.506)$, with the standard deviation 0.711, and the true value 0.6 is well inside it.
- Without the discrepancy ($s^2 = 0$), the posterior is $N(1 / 1.025, 0.025 / 1.025) = N(0.976, 0.0244)$, with the standard deviation 0.156. The true value is $0.376 / 0.156 = 2.4$ standard deviations away, and more data makes this worse, since the variance goes to 0 while the mean goes to $\theta + b = 1$.

**The meaning of $\theta$.** Brynjarsdóttir and O'Hagan showed with a simple machine example that a discrepancy with a vague Gaussian process prior does not fix the problem: the posterior of $\theta$ is then wide or still away from the true value, because the data are explained equally well by many pairs of $\theta$ and $\delta$. Physical parameters are only learned well when the prior of $\delta$ has real information, for example that it is 0 at $x = 0$. If the goal is only to predict $\zeta$, the confounding matters less, because the predictions of different pairs agree where there is data.

**Code uncertainty.** When the simulator is replaced by its emulator, the posterior variance of $\zeta(x)$ includes the emulator variance. At the design points of the runs this part is 0, and it grows between them, so a poor design widens the posterior of $\theta$.

## References
