---
tag: E0ME41
kind: model
slug: epidemic-renewal-equation
name: Epidemic renewal equation
aliases:
- renewal equation for incidence
area: biology/epidemic-and-ecological-models
level: advanced
summary: Incidence today is R_t times the past incidence weighted by the generation interval distribution, the basis of Rt estimation.
history:
  year: 1927
  people: [William Ogilvy Kermack, Anderson Gray McKendrick, Christophe Fraser]
  note: Kermack and McKendrick wrote their 1927 model with infectiousness that depends on the age of infection, which is a renewal equation. Fraser (2007) put the discrete form with a time-varying reproduction number at the centre of real-time estimation.
prereqs: [generation-interval, basic-reproduction-number, convolution]
see_also: [generation-interval, cori-rt-estimation, kermack-mckendrick-sir-model, galton-watson-process, final-size-relation, particle-filter, sequential-monte-carlo, laplace-transform]
sources:
  - paper: doi:10.1371/journal.pone.0000758
    title: "Christophe Fraser, Estimating individual and household reproduction numbers in an emerging epidemic, PLoS ONE 2(8), e758, 2007"
    locator: the renewal equation for incidence, and the instantaneous and case reproduction numbers
  - paper: doi:10.1098/rspa.1927.0118
    title: W. O. Kermack and A. G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London A 115(772), 1927
    locator: the general model with rates of infection and removal that depend on the age of infection
  - paper: "J. Wallinga and M. Lipsitch, How generation intervals shape the relationship between growth rates and reproductive numbers, Proceedings of the Royal Society B 274, 2007"
    title: Wallinga and Lipsitch 2007
    locator: the Euler-Lotka relation between the growth rate and the reproduction number
  - paper: "Anne Cori, Neil M. Ferguson, Christophe Fraser and Simon Cauchemez, A new framework and software to estimate time-varying reproduction numbers during epidemics, American Journal of Epidemiology 178(9), 2013"
    title: Cori et al. 2013
    locator: the Poisson renewal model of daily incidence used for estimation
---

The epidemic renewal equation models incidence, the number of new infections per day, as a weighted sum of past incidence. Each case infected $s$ days ago adds $R_t w_s$ expected new infections today, where $w$ is the [generation interval](/generation-interval/) distribution and $R_t$ is the reproduction number at time $t$. The equation needs no compartments and no assumptions about the course of the disease beyond the shape of $w$. It is the model behind most estimates of $R_t$ from case counts, among them the [Cori method](/cori-rt-estimation/).

## The machine

**The state.** The incidence series $I_1, I_2, \ldots, I_t$ up to the current day. Incidence before day 1, or a seed of initial cases, is given.

**The parameters.** The generation interval weights $w_1, w_2, \ldots, w_{s_{\max}}$, with $w_s \ge 0$, $\sum_s w_s = 1$ and $w_0 = 0$. The reproduction numbers $R_t \ge 0$, one per day. Here $R_t$ is the **instantaneous** reproduction number: the mean number of people that a case would infect if conditions stayed as they are on day $t$.

**The update rule.** Let

$$\Lambda_t = \sum_{s=1}^{s_{\max}} w_s I_{t-s}$$

be the total infectiousness on day $t$, the past incidence weighted by how infectious each cohort is today. The deterministic model is $I_t = R_t \Lambda_t$. The stochastic model used for estimation is

$$I_t \mid I_1, \ldots, I_{t-1} \sim \operatorname{Poisson}(R_t \Lambda_t).$$

**The assumptions.** A case's infectiousness profile, given its infection day, is $R_t w_s$ on day $t$, the same shape for every case. Cases infect independently (in the Poisson model). There is no explicit depletion of susceptibles; it shows up only as a fall in $R_t$. The model counts infections; reported cases add a delay and a reporting fraction, which must be modelled on top.

**A worked example.** Take $w_1 = 0.2$, $w_2 = 0.5$, $w_3 = 0.3$, a seed of $I_0 = 10$ cases, $R_t = 1.5$ for $t \le 8$ and $R_t = 0.8$ after. The deterministic model gives

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $I_t$ | 10 | 3.0 | 8.4 | 9.27 | 10.43 | 13.86 | 16.15 | 19.94 | 24.33 | 15.75 | 17.04 | 14.86 | 12.97 |

For example, $I_3 = 1.5 \times (0.2 \times 8.4 + 0.5 \times 3.0 + 0.3 \times 10) = 9.27$. The ratio $I_t / I_{t-1}$ settles near $e^{r} = 1.2186$, where $r = 0.19766$ is the growth rate for $R = 1.5$ (see below). After the change to $R_t = 0.8$, incidence drops at once, rises a little on day 10 as the large cohort of day 8 reaches its peak infectiousness, and then declines.

## What it counts

- **Expected incidence** given the past and the path of $R_t$.
- **The growth rate.** For a constant $R$, incidence grows like $e^{r t}$, with $r$ the real root of $1 = R \sum_s w_s e^{-r s}$.
- **The likelihood of an incidence series**, $\prod_t e^{-R_t \Lambda_t} (R_t \Lambda_t)^{I_t} / I_t!$, as a function of the path of $R_t$. The [Cori method](/cori-rt-estimation/) puts a gamma prior on $R_t$ over a window and gets a gamma posterior.
- **The case reproduction number** $R^c_t = \sum_s w_s R_{t+s}$, the mean number of people infected by a case infected on day $t$ over its whole course. It looks forward in time, while $R_t$ looks backward.

## Relation to other models

- **[Generation interval](/generation-interval/).** The weights $w$ are the discrete generation interval. With a constant $R$, the renewal equation turns the relation $R = 1/M(-r)$ into a statement about incidence data.
- **[Kermack-McKendrick SIR model](/kermack-mckendrick-sir-model/).** The SIR equations are a renewal equation with the exponential generation interval and $R_t = R_0 S_t / N$. The general Kermack-McKendrick model of 1927, with infectiousness that depends on the age of infection, is the continuous renewal equation $i(t) = \frac{S(t)}{N} \int_0^\infty \beta(\tau)\, i(t - \tau)\, d\tau$.
- **[Galton-Watson process](/galton-watson-process/).** In the Poisson renewal model with a constant $R$, each case has a Poisson($R$) number of offspring, spread over the following days by $w$. Counted by generations, the cases form a Galton-Watson process with Poisson offspring. So an outbreak from few cases dies out with the probability given by the [extinction theorem](/branching-process-extinction-theorem/), even when $R > 1$.
- **State-space models.** With $R_t$ as a hidden random walk, for example $\log R_t = \log R_{t-1} + \varepsilon_t$, the renewal equation becomes the observation model of a state-space model. A [particle filter](/particle-filter/) or another [sequential Monte Carlo](/sequential-monte-carlo/) method then gives the filtered law of $R_t$.
- **Demography.** The same equation with births in place of infections is the Lotka renewal equation, and the root $r$ is the Malthusian growth rate (compare the [Leslie matrix](/leslie-matrix/)).

## Known results in the model

**The growth rate.** For a constant $R$ and a generation interval with finite support, the equation $1 = R \sum_s w_s e^{-rs}$ has exactly one real root $r$, because the right side is strictly decreasing in $r$ and goes from $\infty$ to 0. So $r > 0$ if and only if $R > 1$. The general solution of the linear deterministic equation is a combination of $z^t$ terms over the roots of $z^{s_{\max}} = R \sum_s w_s z^{s_{\max} - s}$. When the $w_s$ with $w_s > 0$ have no common divisor greater than 1, the real root $e^r$ has the largest modulus, so $I_t / I_{t-1} \to e^r$ from any positive seed. In continuous time, this is the renewal theorem, and $r$ is found through the [Laplace transform](/laplace-transform/) of the generation interval.

**Depletion and the final size.** With $R_t = R_0 S_t / N$, the model is an SIR epidemic. If new infections are written as $S_t (1 - e^{-R_0 \Lambda_t / N})$, the escape form, then $\ln(S_\infty / S_0) = -R_0 \sum_t \Lambda_t / N$, and since $\sum_t \Lambda_t$ is the total number infected, the [final size relation](/final-size-relation/) $z = 1 - e^{-R_0 z}$ holds exactly for any $w$. With $w$ as above, $R_0 = 2$, $N = 10^6$ and one initial case, the escape form infects 0.79681 of the population. The linear form $I_t = R_0 (S_t/N) \Lambda_t$ is not the same: it infects 0.82655, because it lets a susceptible be infected more than once in one day.

**Instantaneous and case reproduction numbers.** If $R_t$ changes, $R_t$ and $R^c_t$ differ: $R^c_t$ reacts to a change in transmission before the change happens, and $R_t$ after. Estimates of $R_t$ from incidence up to day $t$ need only the past, which is why real-time methods use the instantaneous form ([Fraser](#references)).

**What the data cannot tell apart.** From incidence alone, $R_t$ and $w$ are not identified together: the same series fits a larger $R$ with a longer interval, as the relation $R = 1/M(-r)$ shows. So estimates of $R_t$ rest on an external estimate of $w$. Reporting delays smear the timing of infections, and a fixed reporting fraction scales $I_t$ and $\Lambda_t$ together and so leaves $R_t$ unchanged, but a fraction that changes over time does not.

**Overdispersion.** If a few cases infect many people, the Poisson model is too narrow. A common change is a negative binomial law for $I_t$ with mean $R_t \Lambda_t$. The mean equation does not change, but the probability of early extinction grows.

## References
