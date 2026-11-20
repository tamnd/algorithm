---
tag: MWEVWM
kind: theorem
slug: hoeffding-sobol-decomposition
name: Hoeffding-Sobol decomposition
aliases:
- functional ANOVA decomposition
area: scientific-computing/uncertainty-quantification
level: core
summary: A square integrable function of independent inputs splits uniquely into orthogonal terms of growing interaction order, whose variances add up.
prereqs: [conditional-expectation, variance]
see_also: [sobol-indices, saltelli-sampling-scheme, u-statistic, polynomial-chaos-expansion, fourier-amplitude-sensitivity-test, morris-method, shapley-value, curse-of-dimensionality]
sources:
  - paper: doi:10.1214/aoms/1177730196
    title: Wassily Hoeffding, A class of statistics with asymptotically normal distribution, Annals of Mathematical Statistics 19(3), 1948, 293-325
    locator: the decomposition of a symmetric function of independent variables into uncorrelated parts of growing order, used for the variance of U-statistics
  - paper: "I. M. Sobol, Sensitivity estimates for nonlinear mathematical models, Mathematical Modeling and Computational Experiment 1(4), 1993, 407-414"
    title: I. M. Sobol, Sensitivity estimates for nonlinear mathematical models
    locator: the decomposition into summands of different dimensions on the unit cube, its uniqueness under the zero integral conditions, and the variance split
  - paper: doi:10.1214/aos/1176345462
    title: Bradley Efron and Charles Stein, The jackknife estimate of variance, Annals of Statistics 9(3), 1981, 586-596
    locator: the orthogonal decomposition of a function of independent variables and the inequality of Efron and Stein that follows from it
  - paper: doi:10.1016/S0378-4754(00)00270-6
    title: I. M. Sobol, Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates, Mathematics and Computers in Simulation 55(1-3), 2001, 271-280
    locator: the ANOVA representation, the indices of groups of variables and the total indices
---

## Statement

Let $x = (x_1, \ldots, x_d)$ have independent components, with the product law $\mu = \mu_1 \otimes \cdots \otimes \mu_d$, and let $f \in L^2(\mu)$. For a set $u \subseteq \{1, \ldots, d\}$, write $x_u$ for the components with index in $u$ and $x_{\sim u}$ for the rest.

**Theorem.** There is a unique family of functions $f_u \in L^2(\mu)$, one for each $u \subseteq \{1, \ldots, d\}$, such that

1. $f(x) = \sum_{u} f_u(x_u)$ for $\mu$-almost every $x$, where $f_u$ depends only on $x_u$ and $f_\emptyset$ is a constant;
2. for every nonempty $u$ and every $j \in u$, $\int f_u(x_u)\, d\mu_j(x_j) = 0$ for almost every value of the other components of $x_u$.

The terms are

$$f_u(x_u) = \sum_{v \subseteq u} (-1)^{|u| - |v|}\, g_v(x_v), \qquad g_v(x_v) = \mathbb{E}[f(x) \mid x_v],$$

so $f_\emptyset = \mathbb{E}[f]$. They are orthogonal: $\mathbb{E}[f_u f_v] = 0$ for $u \ne v$, and $\mathbb{E}[f_u] = 0$ for $u \ne \emptyset$. Hence the variances add up:

$$\mathrm{Var}(f) = \sum_{u \ne \emptyset} \mathrm{Var}(f_u), \qquad \mathbb{E}[f \mid x_u] = \sum_{v \subseteq u} f_v.$$

The terms with $|u| = 1$ are the main effects, the terms with $|u| = 2$ are the two-way interactions, and so on up to the single term of order $d$. The ratios $\mathrm{Var}(f_u)/\mathrm{Var}(f)$ are the [Sobol indices](/sobol-indices/).

## In plain words

Take any model output that depends on several independent random inputs. You can write it, in exactly one way, as a constant plus a part that each input causes alone, plus a part that each pair of inputs causes together beyond their separate parts, plus a part for each triple, and so on. Each part averages to zero when you average over any one of its own inputs.

These parts do not overlap. Because of this, the spread of the output is simply the sum of the spreads of the parts. You can then say what share of the spread comes from each input, each pair or each larger group. This is the base of variance-based sensitivity analysis.

## Proof

Write $D = \{1, \ldots, d\}$. By independence, the conditional expectation integrates out the other components: $g_v(x_v) = \int f(x_v, x_{\sim v})\, d\mu_{\sim v}(x_{\sim v})$, where $\mu_{\sim v}$ is the product of the $\mu_j$ for $j \notin v$. By [Jensen's inequality for conditional expectation](/conditional-expectation/), $\mathbb{E}[g_v^2] \le \mathbb{E}[f^2]$, so each $g_v$ and each $f_u$ is in $L^2(\mu)$.

**Step 1 (the sum is f).** The formula for $f_u$ is the Möbius inversion of $g_u = \sum_{v \subseteq u} f_v$ on the lattice of subsets. To see the inversion, substitute: $\sum_{v \subseteq u} f_v = \sum_{v \subseteq u} \sum_{w \subseteq v} (-1)^{|v| - |w|} g_w = \sum_{w \subseteq u} g_w \sum_{w \subseteq v \subseteq u} (-1)^{|v| - |w|}$. The inner sum is $(1 - 1)^{|u| - |w|}$, which is 1 for $w = u$ and 0 otherwise. So $\sum_{v \subseteq u} f_v = g_u$ for every $u$. With $u = D$, $g_D = \mathbb{E}[f \mid x] = f$, which is condition 1. It also proves $\mathbb{E}[f \mid x_u] = \sum_{v \subseteq u} f_v$.

**Step 2 (zero integrals).** Fix $u \ne \emptyset$ and $j \in u$. Split the subsets of $u$ into pairs $(v, v \cup \{j\})$ with $j \notin v$. The function $g_v$ does not depend on $x_j$, so its integral over $x_j$ is $g_v$. By Fubini's theorem, the integral of $g_{v \cup \{j\}}$ over $x_j$ is also $g_v$, since integrating out first $x_j$ and then $x_{\sim(v \cup \{j\})}$ integrates out $x_{\sim v}$. The two members of the pair have opposite signs $(-1)^{|u| - |v|}$ and $(-1)^{|u| - |v| - 1}$, so

$$\int f_u\, d\mu_j = \sum_{v \subseteq u,\ j \notin v} (-1)^{|u| - |v|}\big(g_v - g_v\big) = 0.$$

This is condition 2.

**Step 3 (orthogonality).** Let $u \ne v$, and pick $j$ in one set but not the other, say $j \in u \setminus v$. The product $f_u f_v$ is integrable by the Cauchy-Schwarz inequality. Integrate over $x_j$ first: $f_v$ does not depend on $x_j$, so by Fubini's theorem and Step 2

$$\mathbb{E}[f_u f_v] = \int f_v \Big(\int f_u\, d\mu_j\Big)\, d\mu_{\sim j} = 0.$$

With $v = \emptyset$ and the constant $f_\emptyset$, this gives $\mathbb{E}[f_u] = 0$ for $u \ne \emptyset$.

**Step 4 (uniqueness).** Let $(f'_u)$ be a second family with conditions 1 and 2, and put $h_u = f_u - f'_u$. Each $h_u$ depends only on $x_u$ and has the zero integrals of condition 2, so Step 3 applies to the $h_u$ without change: they are orthogonal. By condition 1, $\sum_u h_u = 0$ almost everywhere. Then

$$0 = \mathbb{E}\Big[\Big(\sum_u h_u\Big)^2\Big] = \sum_u \mathbb{E}[h_u^2],$$

so every $h_u = 0$ almost everywhere.

**Step 5 (the variances add up).** $f - \mathbb{E}[f] = \sum_{u \ne \emptyset} f_u$ by Steps 1 and 3, and the terms are orthogonal with mean zero, so $\mathrm{Var}(f) = \mathbb{E}[(\sum_{u \ne \emptyset} f_u)^2] = \sum_{u \ne \emptyset} \mathbb{E}[f_u^2] = \sum_{u \ne \emptyset} \mathrm{Var}(f_u)$. $\blacksquare$

**A worked case.** Let $f = x_1 + 2x_2 + x_1x_2$ with $x_1, x_2$ independent and uniform on $[-1, 1]$. Then $g_\emptyset = 0$, $g_{\{1\}} = x_1$, $g_{\{2\}} = 2x_2$ and $g_{\{1,2\}} = f$, so $f_\emptyset = 0$, $f_1 = x_1$, $f_2 = 2x_2$ and $f_{12} = x_1x_2$. Their variances are $1/3$, $4/3$ and $1/9$, which add up to $\mathrm{Var}(f) = 16/9$. The shares are $3/16$, $3/4$ and $1/16$.

## Consequences

- **Sobol indices.** The shares $S_u = \mathrm{Var}(f_u)/\mathrm{Var}(f)$ are nonnegative and add up to 1 over the $2^d - 1$ nonempty sets. The closed index of a group, $\mathrm{Var}(\mathbb{E}[f \mid x_u])/\mathrm{Var}(f) = \sum_{\emptyset \ne v \subseteq u} S_v$, and the total index of input $i$, $\sum_{u \ni i} S_u$, follow from the identity $\mathbb{E}[f \mid x_u] = \sum_{v \subseteq u} f_v$. This is what the [Saltelli sampling scheme](/saltelli-sampling-scheme/), the [Fourier amplitude sensitivity test](/fourier-amplitude-sensitivity-test/) and [polynomial chaos](/polynomial-chaos-expansion/) estimate.
- **Additive models.** The first order indices add up to 1 if and only if all terms with $|u| \ge 2$ are zero, that is, if $f$ is additive.
- **Best low order approximation.** Every function of at most $k$ of the inputs splits, by the theorem, into terms $f_u$ with $|u| \le k$. So the truncation $\sum_{|u| \le k} f_u$ is the orthogonal projection of $f$ onto the functions of at most $k$ inputs, and its error is $\sum_{|u| > k} \mathrm{Var}(f_u)$. If this error is small for a small $k$, $f$ has a low effective dimension in the superposition sense, which is one reason why [quasi-Monte Carlo](/quasi-monte-carlo-integration/) works in high dimension for some integrands.
- **The Efron-Stein inequality.** $\mathbb{E}[\mathrm{Var}(f \mid x_{\sim i})] = \sum_{u \ni i} \mathrm{Var}(f_u)$, so $\sum_i \mathbb{E}[\mathrm{Var}(f \mid x_{\sim i})] = \sum_u |u|\, \mathrm{Var}(f_u) \ge \mathrm{Var}(f)$. In index form, the total indices add up to at least 1.
- **U-statistics.** Applied to a symmetric kernel of independent and identically distributed variables, the decomposition gives the variance of a [U-statistic](/u-statistic/) and its leading term, which is how Hoeffding proved its asymptotic normality.
- **Polynomial chaos.** If $f$ is expanded in products of orthonormal polynomials of the single inputs, the terms $f_u$ are the sums of the products whose nonconstant factors are exactly the inputs in $u$. So the Sobol indices are sums of squared coefficients.

## Tightness

- **Independence is needed.** Let $x_1, x_2$ be standard normal with correlation $\rho$, and $f = x_1 + x_2$. The terms $x_1$ and $x_2$ have the zero integrals of condition 2 for the marginals, but $\mathbb{E}[x_1x_2] = \rho$, so $\mathrm{Var}(f) = 2 + 2\rho$ is not the sum $2$ of their variances. The ratios $\mathrm{Var}(\mathbb{E}[f \mid x_i])/\mathrm{Var}(f) = (1 + \rho)/2$ add up to $1 + \rho$, which is $1.5$ for $\rho = 0.5$, more than all of the variance, for an additive $f$. Generalized decompositions for dependent inputs, such as that of Hooker (2007), give up either orthogonality or the simple variance split.
- **The zero integral conditions are needed for uniqueness.** Without condition 2, $x_1 + x_2 = (x_1 + c) + (x_2 - c)$ for every constant $c$, and the split is not unique.
- **The terms depend on the input law.** On $[0, 1]^2$ with uniform inputs, $x_1x_2 = \frac{1}{4} + \frac{1}{2}(x_1 - \frac{1}{2}) + \frac{1}{2}(x_2 - \frac{1}{2}) + (x_1 - \frac{1}{2})(x_2 - \frac{1}{2})$, with variances $1/48$, $1/48$ and $1/144$. On $[-1, 1]^2$ the same function $x_1x_2$ is a pure interaction. So the indices are a property of the model together with the input law, not of the model alone.
- **Square integrability is needed.** For $f \notin L^2(\mu)$, the variance is infinite and the split is not defined; the terms $g_v$ may still exist if $f$ is integrable, but the orthogonality argument of Step 3 fails.

## History

Hoeffding introduced the decomposition in 1948 for symmetric functions of independent variables, to find the variance and the limit law of U-statistics. Sobol used the expansion of a function on the unit cube into summands of different dimensions in his 1969 book on multidimensional quadrature, proved its uniqueness under the zero integral conditions, and in 1990 (English translation 1993) based his global sensitivity indices on it. Efron and Stein (1981) used it to prove their variance inequality for the jackknife. The name functional ANOVA comes from the analysis of variance of Fisher, of which the decomposition is the continuous form, and the double name Hoeffding-Sobol is common in the sensitivity analysis literature.

## References
