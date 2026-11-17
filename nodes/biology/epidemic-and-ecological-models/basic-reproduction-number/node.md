---
tag: Q55PAT
kind: definition
slug: basic-reproduction-number
name: Basic reproduction number
aliases:
- R0
- basic reproductive ratio
area: biology/epidemic-and-ecological-models
level: intro
summary: The expected number of secondary infections caused by one infected individual in a fully susceptible population.
prereqs: [compartmental-epidemic-model]
see_also: [next-generation-matrix, herd-immunity-threshold, final-size-relation, epidemic-threshold, kermack-mckendrick-sir-model, generation-interval, galton-watson-process, spectral-radius]
sources:
  - paper: doi:10.1007/BF00178324
    title: O. Diekmann, J. A. P. Heesterbeek and J. A. J. Metz, On the definition and the computation of the basic reproduction ratio R0 in models for infectious diseases in heterogeneous populations, Journal of Mathematical Biology 28(4), 1990
    locator: pages 365 to 382 (R0 as the spectral radius of the next-generation operator, for individuals of several types)
  - paper: doi:10.1016/S0025-5564(02)00108-6
    title: P. van den Driessche and James Watmough, Reproduction numbers and sub-threshold endemic equilibria for compartmental models of disease transmission, Mathematical Biosciences 180(1-2), 2002
    locator: pages 29 to 48 (the matrices F and V, R0 as the spectral radius of F V^(-1), and Theorem 2, the local stability of the disease-free equilibrium when R0 < 1 and its instability when R0 > 1)
  - paper: doi:10.1098/rsif.2009.0386
    title: O. Diekmann, J. A. P. Heesterbeek and M. G. Roberts, The construction of next-generation matrices for compartmental epidemic models, Journal of the Royal Society Interface 7(47), 2010
    locator: pages 873 to 885 (the next-generation matrix with large and small domain, and the appendix that proves R0 > 1 exactly when the early growth rate is positive)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 2.1.1.1, The threshold phenomenon, and Sections 2.8.1 and 2.8.2, estimating R0 from reported cases and from seroprevalence data
---

The basic reproduction number $R_0$ is the expected number of new infections that one typical infected individual causes during its whole infectious period, in a population where everyone else is susceptible. It is a property of a pathogen in a given host population, not of the pathogen alone. In a [compartmental epidemic model](/compartmental-epidemic-model/), $R_0$ is the threshold quantity: an outbreak can grow when $R_0 > 1$ and dies out when $R_0 < 1$. For models with several types of infected individuals, the exact definition is the [spectral radius](/spectral-radius/) of the [next-generation matrix](/next-generation-matrix/).

## Definition

**One type of infected individual.** Suppose that an individual infected for a time $\tau$ causes new infections at the expected rate $A(\tau)$, when all its contacts are with susceptibles. Then

$$
R_0 = \int_0^\infty A(\tau) \, d\tau .
$$

In the [Kermack-McKendrick model](/kermack-mckendrick-sir-model/), an infected individual is still infectious at time $\tau$ with probability $e^{-\gamma \tau}$ and infects at rate $\beta$ while it is, so $A(\tau) = \beta e^{-\gamma \tau}$ and $R_0 = \beta / \gamma$.

**Several types.** Suppose that infected individuals have types $1, \ldots, n$ (by age, place, host species or stage of infection). Let $K_{ij}$ be the expected number of new infections of type $i$ caused by one newly infected individual of type $j$ during its whole infection, at the disease-free state. The matrix $K = (K_{ij})$ is the next-generation matrix, and

$$
R_0 = \rho(K),
$$

the largest absolute value of an eigenvalue of $K$ (Diekmann, Heesterbeek and Metz 1990). $K$ has non-negative entries, so by the [Perron-Frobenius theorem](/perron-frobenius-theorem/) $\rho(K)$ is itself an eigenvalue, with an eigenvector $w \ge 0$. The "typical" infected individual of the informal definition is a random individual whose type has the distribution $w / \sum_i w_i$: if the types of one generation of cases have this distribution, then the next generation is $R_0$ times larger and has the same distribution.

**The compartmental form.** For an ODE model, split the rate of change of the infected classes $x$ at the disease-free equilibrium $x_0$ into the rate $\mathcal{F}(x)$ of new infections and the rate $\mathcal{V}(x)$ of all other transfers, so that $dx/dt = \mathcal{F}(x) - \mathcal{V}(x)$. With the Jacobians $F = D\mathcal{F}(x_0)$ and $V = D\mathcal{V}(x_0)$, the next-generation matrix is $F V^{-1}$, and $R_0 = \rho(F V^{-1})$ (van den Driessche and Watmough 2002). Entry $(V^{-1})_{jk}$ is the expected time that an individual who enters infected class $k$ spends in class $j$; entry $F_{ij}$ is the rate at which an individual in class $j$ produces new infections in class $i$.

**The threshold property.** Under the conditions of van den Driessche and Watmough (2002) on $\mathcal{F}$ and $\mathcal{V}$, the disease-free equilibrium is locally asymptotically stable if $R_0 < 1$ and unstable if $R_0 > 1$ (their Theorem 2). Equivalently, $R_0 > 1$ exactly when the early exponential growth rate $r$ of the linearized system is positive, and $R_0 = 1$ exactly when $r = 0$ (Diekmann, Heesterbeek and Roberts 2010, appendix). In a stochastic model of a large population, the probability that one case starts a major outbreak is positive only when $R_0 > 1$; this is the [epidemic threshold](/epidemic-threshold/) of the [stochastic SIR model](/stochastic-sir-model/).

## Examples and non-examples

**SIR.** With $\beta = 0.4$ per day and $\gamma = 0.2$ per day, $R_0 = 0.4 / 0.2 = 2$: each case infects 0.4 others per day for a mean of 5 days.

**SEIR with births and deaths.** With incubation rate $\sigma$, recovery rate $\gamma$ and a death rate $\mu$ from every class, an infected individual reaches the infectious class with probability $\sigma / (\sigma + \mu)$ and then stays infectious for a mean time $1 / (\gamma + \mu)$, so

$$
R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu)} .
$$

With $\mu = 0$ this is $\beta / \gamma$ again. The [SEIR page](/seir-epidemic-model/) derives it with the next-generation matrix.

**Two groups.** Two groups of equal size mix unevenly, with

$$
K = \begin{pmatrix} 3 & 1 \\ 1 & 0.5 \end{pmatrix}.
$$

A case in group 1 infects 3 people in group 1 and 1 in group 2; a case in group 2 infects 1 in group 1 and 0.5 in group 2. The characteristic polynomial is $\lambda^2 - 3.5 \lambda + 0.5$, so $R_0 = (3.5 + \sqrt{10.25}) / 2 \approx 3.3508$.

**Non-example: the mean over individuals.** In the same two-group example, the column sums of $K$ are 4 and 1.5, the total numbers of cases caused by a case in each group. Their mean, 2.75, is not $R_0$. Cases in group 1 are over-represented in each generation (the Perron eigenvector is about $(1, 0.351)$), so the growth factor per generation is 3.3508, not 2.75.

**Non-example: the growth rate.** $R_0$ counts infections per generation, not per day. In an SEIR model with $\beta = 0.4$ and $\gamma = 0.2$ per day, $R_0 = 2$ for every incubation rate $\sigma$, but the early growth rate is $r = 0.0828$, $0.1217$ and $0.1483$ per day for $\sigma = 0.2$, $0.5$ and $1$ per day, with doubling times of 8.4, 5.7 and 4.7 days. To get $R_0$ from an observed growth rate, you need the distribution of the [generation interval](/generation-interval/): for SIR, $R_0 = 1 + r / \gamma$, and for SEIR, $R_0 = (1 + r / \sigma)(1 + r / \gamma)$.

**Non-example: the effective reproduction number.** Late in an epidemic, a case infects fewer people, because many contacts are already immune. That number, $R_t$ or $R(t)$, is $R_0 s(t)$ in the Kermack-McKendrick model. It is not $R_0$, which is defined at the disease-free state only.

**Non-example: the product of the two legs.** In the [Ross-Macdonald model](/ross-macdonald-model/) of malaria, Macdonald's $R_0$ is the number of human cases caused by one human case through one round of mosquitoes. It is the product of two legs, human to mosquito and mosquito to human. The spectral radius of the next-generation matrix counts one leg per generation, so it is the square root of that product. Both are threshold quantities with threshold 1, but they are not the same number; each page must say which one it uses.

**Recovering $R_0$ from data, in the Kermack-McKendrick model.** From the fraction $z$ ever infected in a closed epidemic that started from very few cases, the [final size relation](/final-size-relation/) gives $R_0 = -\ln(1 - z) / z$: for $z = 0.5$, $R_0 = 2 \ln 2 \approx 1.386$. From an endemic equilibrium with births, $R_0 = 1 / s^*$, the inverse of the susceptible fraction (Keeling and Rohani 2008, section 2.8.2).

## Related definitions

- **[Next-generation matrix](/next-generation-matrix/).** The technique that computes $R_0$ for models with several infected classes.
- **Effective reproduction number $R_t$.** The mean number of infections caused by a case infected at time $t$, under the immunity and the control measures at that time. The [Cori method](/cori-rt-estimation/) estimates it from case counts with the [renewal equation](/epidemic-renewal-equation/).
- **Control reproduction number.** $R_0$ of the model with a control measure in place, for example vaccination of a fraction $v$, which gives $R_0 (1 - v)$ under homogeneous mixing and a perfect vaccine. The [herd immunity threshold](/herd-immunity-threshold/) is the value of $v$ that makes it 1.
- **Offspring mean of a branching process.** At the start of an outbreak, the cases form a [Galton-Watson process](/galton-watson-process/) whose mean number of offspring is $R_0$. The branching process extinction theorem gives the probability that the outbreak dies out.
- **[Epidemic threshold](/epidemic-threshold/).** The value of a spreading parameter at which $R_0 = 1$. On a contact network it depends on the degree distribution (see the [degree-based mean-field model](/heterogeneous-mean-field-epidemic/)).
- **Generation interval.** The time from the infection of an infector to the infection of a person that it infects. With $R_0$, it decides the growth rate.

## References
