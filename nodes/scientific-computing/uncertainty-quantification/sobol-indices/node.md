---
tag: M61B58
kind: definition
slug: sobol-indices
name: Sobol indices
aliases:
- Sobol sensitivity indices
- variance-based sensitivity indices
area: scientific-computing/uncertainty-quantification
level: core
summary: The shares of the output variance due to each input or group of inputs, from the Hoeffding-Sobol decomposition of the model.
prereqs: [hoeffding-sobol-decomposition, variance, conditional-expectation]
see_also: [saltelli-sampling-scheme, fourier-amplitude-sensitivity-test, morris-method, shapley-value, active-subspaces, polynomial-chaos-expansion, forward-uncertainty-propagation, monte-carlo-integration]
sources:
  - paper: "Ilya M. Sobol, Sensitivity estimates for nonlinear mathematical models, Mathematical Modeling and Computational Experiment 1(4), 1993, 407-414"
    title: Ilya M. Sobol, Sensitivity estimates for nonlinear mathematical models
    locator: the definition of the sensitivity indices of single inputs and groups of inputs as ratios of the variances of the decomposition terms (translation of the 1990 Russian paper)
  - paper: doi:10.1016/S0378-4754(00)00270-6
    title: I. M. Sobol, Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates, Mathematics and Computers in Simulation 55(1-3), 2001, 271-280
    locator: the indices of groups of variables, the total index and the fixing of unessential variables
  - paper: doi:10.1016/0951-8320(96)00002-6
    title: Toshimitsu Homma and Andrea Saltelli, Importance measures in global sensitivity analysis of nonlinear models, Reliability Engineering and System Safety 52(1), 1996, 1-17
    locator: the total sensitivity index
  - book: isbn:9780470059975
    title: Andrea Saltelli, Marco Ratto, Terry Andres, Francesca Campolongo, Jessica Cariboni, Debora Gatelli, Michaela Saisana and Stefano Tarantola, Global Sensitivity Analysis, The Primer, Wiley, 2008
    locator: Chapter 4 (variance-based methods, first order and total effects, factor prioritization and factor fixing)
  - paper: doi:10.1109/ISUMA.1990.151285
    title: Tsutomu Ishigami and Toshimitsu Homma, An importance quantification technique in uncertainty analysis for computer models, Proceedings of the First International Symposium on Uncertainty Modeling and Analysis (ISUMA 1990), IEEE, 1990, 398-403
    locator: the test function sin x1 + a sin^2 x2 + b x3^4 sin x1
---

Sobol indices measure how much of the uncertainty of a model output comes from each uncertain input, alone or together with other inputs. The output variance is split by the [Hoeffding-Sobol decomposition](/hoeffding-sobol-decomposition/) into parts that belong to single inputs and to groups of inputs, and each index is one part, or a sum of parts, divided by the total variance. The first order index of an input is the share it causes alone, and the total index is the share it takes part in. They are global measures, averaged over the whole input law, and they are defined only for independent inputs.

## Definition

Let the inputs $x = (x_1, \ldots, x_d)$ be independent random variables, and let $Y = f(x)$ be square integrable with $D = \mathrm{Var}(Y) > 0$. Let $f = \sum_{u} f_u(x_u)$ be the Hoeffding-Sobol decomposition of $f$, with $D_u = \mathrm{Var}(f_u)$, so that $D = \sum_{u \ne \emptyset} D_u$. Write $x_{\sim i}$ for all inputs except $x_i$.

- The **Sobol index** of a nonempty set $u$ of inputs is $S_u = D_u / D$. For $u = \{i, j\}$ it is the second order index $S_{ij}$.
- The **first order index**, or main effect, of input $i$ is
$$S_i = \frac{D_{\{i\}}}{D} = \frac{\mathrm{Var}(\mathbb{E}[Y \mid x_i])}{\mathrm{Var}(Y)}.$$
- The **closed index** of a set $u$ is $S^{\mathrm{clo}}_u = \mathrm{Var}(\mathbb{E}[Y \mid x_u])/D = \sum_{\emptyset \ne v \subseteq u} S_v$.
- The **total index** of input $i$ is
$$S_{Ti} = \sum_{u \ni i} S_u = \frac{\mathbb{E}[\mathrm{Var}(Y \mid x_{\sim i})]}{\mathrm{Var}(Y)} = 1 - \frac{\mathrm{Var}(\mathbb{E}[Y \mid x_{\sim i}])}{\mathrm{Var}(Y)}.$$

The second forms come from the identity $\mathbb{E}[f \mid x_u] = \sum_{v \subseteq u} f_v$ of the decomposition and from the law of total variance, $\mathrm{Var}(Y) = \mathrm{Var}(\mathbb{E}[Y \mid x_{\sim i}]) + \mathbb{E}[\mathrm{Var}(Y \mid x_{\sim i})]$. The first form of $S_i$ says: if $x_i$ could be fixed at its true value, the variance would drop by $S_i D$ on average. The form of $S_{Ti}$ says: if all inputs except $x_i$ were fixed, a share $S_{Ti}$ of the variance would remain on average.

From the definition, the following facts hold (they are theorems that follow from the decomposition):

- $0 \le S_i \le S_{Ti} \le 1$, and $S_{Ti} - S_i$ is the share of the interactions of input $i$.
- $\sum_i S_i \le 1 \le \sum_i S_{Ti}$, with equality on either side if and only if $f$ is additive.
- $S_{Ti} = 0$ if and only if $f$ does not depend on $x_i$ for almost every $x$, so input $i$ can be fixed at any value without changing the law of $Y$. This is the base of factor fixing.

## Examples and non-examples

**A small model.** Let $f = x_1 + 2x_2 + x_1x_2$ with $x_1, x_2$ independent and uniform on $[-1, 1]$. The decomposition terms are $x_1$, $2x_2$ and $x_1x_2$, with variances $1/3$, $4/3$ and $1/9$, so $D = 16/9$ and

| index | value |
|---|---|
| $S_1$ | $3/16 = 0.1875$ |
| $S_2$ | $3/4 = 0.75$ |
| $S_{12}$ | $1/16 = 0.0625$ |
| $S_{T1}$ | $1/4 = 0.25$ |
| $S_{T2}$ | $13/16 = 0.8125$ |

The first order indices add up to $15/16$; the missing $1/16$ is the interaction, which counts in both total indices.

**A linear model.** For $f = c_0 + \sum_i c_i x_i$ with independent inputs of variances $\sigma_i^2$, $S_i = S_{Ti} = c_i^2\sigma_i^2 / \sum_j c_j^2\sigma_j^2$. In this case, and in general only for linear models, the indices are the squared standardized regression coefficients.

**The Ishigami function.** For $f = \sin x_1 + 7\sin^2 x_2 + 0.1\, x_3^4 \sin x_1$ with $x_i$ independent and uniform on $[-\pi, \pi]$, the variance is $D = 13.8446$ and the only nonzero terms are $f_1$, $f_2$ and $f_{13}$:

| input | $S_i$ | $S_{Ti}$ |
|---|---|---|
| $x_1$ | 0.3139 | 0.5576 |
| $x_2$ | 0.4424 | 0.4424 |
| $x_3$ | 0 | 0.2437 |

Input $x_3$ has no effect alone, $\mathbb{E}[Y \mid x_3]$ is constant, but it changes the amplitude of the $\sin x_1$ term, so its total index is not zero. Fixing $x_3$ on the basis of $S_3 = 0$ would be wrong; the total index is the right measure for factor fixing.

**Non-example: a correlation.** Let $x$ be uniform on $[-1, 1]$ and $Y = x^2$. The correlation of $x$ and $Y$ is zero, but $S_1 = 1$: all of the variance comes from $x$. A correlation or a regression coefficient measures only the linear part of the dependence; the first order index is the squared correlation ratio, which sees every form of dependence.

**Non-example: a local derivative.** For $f = x_1x_2$ with inputs uniform on $[-1, 1]$, both partial derivatives are zero at the nominal point $(0, 0)$, so a local sensitivity study at that point finds no effect. The Sobol indices are $S_1 = S_2 = 0$ and $S_{12} = 1$: the inputs act only together, and their total indices are 1.

**Non-example: dependent inputs.** Let $x_1, x_2$ be standard normal with correlation $0.5$ and $Y = x_1 + x_2$. The ratios $\mathrm{Var}(\mathbb{E}[Y \mid x_i])/\mathrm{Var}(Y)$ are $0.75$ each and add up to $1.5$, so they are not shares of the variance. The Hoeffding-Sobol decomposition is not orthogonal for dependent inputs, and the definition above does not apply.

**Non-example: infinite variance.** If $Y$ is not square integrable, for example a Cauchy distributed input passed through $f(x) = x$, then $D$ is infinite and no index is defined.

## Related definitions

- **Elementary effects.** The measures $\mu^*_i$ and $\sigma_i$ of the [Morris method](/morris-method/) are cheap screening measures on a grid. They rank inputs, but they are not shares of the variance.
- **Fourier estimates.** The [Fourier amplitude sensitivity test](/fourier-amplitude-sensitivity-test/) estimates $S_i$ and $S_{Ti}$ from the spectrum of the output along a search curve, and the [Saltelli sampling scheme](/saltelli-sampling-scheme/) estimates them by Monte Carlo from two matrices and their column swaps.
- **Shapley effects.** The Shapley effect of input $i$ is the [Shapley value](/shapley-value/) of the game whose value of a set $u$ is $\mathrm{Var}(\mathbb{E}[Y \mid x_u])$. For independent inputs it is $\sum_{u \ni i} S_u / |u|$, between $S_i$ and $S_{Ti}$, and it splits each interaction equally among its inputs. Unlike the Sobol indices, the Shapley effects add up to 1 also for dependent inputs, which is why Owen and others proposed them.
- **Derivative-based measures.** The measure $\nu_i = \mathbb{E}[(\partial f/\partial x_i)^2]$ of Sobol and Kucherenko averages the squared derivative over the input law. For inputs uniform on $[0, 1]$, they proved the bound $S_{Ti} \le \nu_i / (\pi^2 D)$.
- **Active subspaces.** The [active subspaces](/active-subspaces/) method uses the matrix $\mathbb{E}[\nabla f \nabla f^{\top}]$ to find important directions, which may be combinations of inputs rather than single inputs.
- **Polynomial chaos indices.** If $f$ has a [polynomial chaos expansion](/polynomial-chaos-expansion/) in orthonormal polynomials of the independent inputs, each $D_u$ is the sum of the squared coefficients whose basis terms depend on exactly the inputs in $u$.
- **Variance and conditional expectation.** The indices are ratios of the [variance](/variance/) of a [conditional expectation](/conditional-expectation/) to the total variance. They are the variance-based part of [forward uncertainty propagation](/forward-uncertainty-propagation/), which asks for the law of $Y$; the indices then ask where its variance comes from.

## References
