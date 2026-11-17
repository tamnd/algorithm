---
tag: KE9NQC
kind: definition
slug: generation-interval
name: Generation interval
aliases:
- serial interval
- generation time distribution
area: biology/epidemic-and-ecological-models
level: core
summary: The time from the infection of an infector to the infection of a person it infects. Its distribution links the epidemic growth rate to the reproduction number.
history:
  year: 2007
  people: [Jacco Wallinga, Marc Lipsitch]
  note: Wallinga and Lipsitch showed in 2007 that the reproduction number follows from the growth rate through the moment generating function of the generation interval, and they stressed that the generation interval and the serial interval are different quantities.
prereqs: [basic-reproduction-number, moment-generating-function]
see_also: [epidemic-renewal-equation, cori-rt-estimation, basic-reproduction-number, seir-epidemic-model, stochastic-sir-model, galton-watson-process, laplace-transform, convolution]
sources:
  - paper: "J. Wallinga and M. Lipsitch, How generation intervals shape the relationship between growth rates and reproductive numbers, Proceedings of the Royal Society B 274, 2007"
    title: Wallinga and Lipsitch 2007
    locator: the relation R = 1 / M(-r) and its special cases for common interval distributions
  - paper: "Ake Svensson, A note on generation times in epidemic models, Mathematical Biosciences 208, 2007"
    title: Svensson 2007
    locator: the definition of the generation time and its mean in a stochastic epidemic model
  - paper: doi:10.1371/journal.pone.0000758
    title: "Christophe Fraser, Estimating individual and household reproduction numbers in an emerging epidemic, PLoS ONE 2(8), e758, 2007"
    locator: the renewal form of incidence with the infectiousness profile, and the instantaneous reproduction number
  - paper: "David Champredon and Jonathan Dushoff, Intrinsic and realized generation intervals in infectious-disease transmission, Proceedings of the Royal Society B 282, 2015"
    title: Champredon and Dushoff 2015
    locator: the difference between the intrinsic interval and the intervals measured forward or backward in a growing epidemic
---

## Definition

Consider a transmission pair: an infector, infected at time $t_1$, who infects a second person at time $t_2$. The **generation interval** of the pair is $\tau = t_2 - t_1$, the time from the infection of the infector to the infection of the person it infects. It is never negative.

The **generation interval distribution** $g$ is the law of $\tau$ in a population. In the usual model it is the **intrinsic** distribution: the normalized infectiousness profile of a typical case. If a case infected at time 0 makes new infections at rate $\beta(\tau)$ at age of infection $\tau$, with no depletion of susceptibles, then

$$R = \int_0^\infty \beta(\tau)\, d\tau, \qquad g(\tau) = \frac{\beta(\tau)}{R}.$$

In discrete time, with days $s = 1, 2, \ldots$, the distribution is a list of weights $w_s \ge 0$ with $\sum_s w_s = 1$ and $w_0 = 0$: a case does not infect anyone on the day of its own infection.

**The link to the growth rate.** If incidence grows like $e^{r t}$ while the population is almost fully susceptible, the renewal equation $i(t) = \int_0^\infty \beta(\tau)\, i(t - \tau)\, d\tau$ gives $1 = R \int_0^\infty g(\tau) e^{-r\tau}\, d\tau$, so

$$R = \frac{1}{M(-r)}, \qquad M(u) = \int_0^\infty e^{u\tau} g(\tau)\, d\tau,$$

where $M$ is the [moment generating function](/moment-generating-function/) of $g$, and $M(-r)$ is its [Laplace transform](/laplace-transform/) at $r$. In discrete time, $R = 1 / \sum_s w_s e^{-r s}$. This is the Euler-Lotka equation of demography applied to infections.

The **serial interval** is a different quantity: the time from the onset of symptoms in the infector to the onset of symptoms in the person it infects. The serial interval is the one that contact tracing usually observes, and it can be negative.

## Examples and non-examples

**Exponential interval (SIR).** In the [stochastic SIR model](/stochastic-sir-model/) and its deterministic limit, a case infects at a constant rate during an exponential infectious period with rate $\gamma$. The infectiousness profile is $\beta e^{-\gamma\tau}$, so $g$ is exponential with mean $T = 1/\gamma$, $M(-r) = 1/(1 + r T)$ and $R = 1 + r T$. With $r = 0.1$ per day and $T = 5$ days, $R = 1.5$.

**Gamma interval.** For a gamma distribution with shape $k$ and scale $\theta$ (mean $k\theta$), $M(-r) = (1 + r\theta)^{-k}$ and $R = (1 + r\theta)^k$. With $k = 4$, $\theta = 1.25$ (mean 5 days) and $r = 0.1$, $R = 1.125^4 = 1.6018$.

**Fixed interval.** If every generation takes exactly $T$ days, $R = e^{r T}$. With $T = 5$ and $r = 0.1$, $R = e^{0.5} = 1.6487$. This is the largest value for a given mean: since $e^{-r\tau}$ is convex in $\tau$, Jensen's inequality gives $M(-r) \ge e^{-rT}$, so $R \le e^{rT}$ for every interval law with mean $T$ when $r > 0$. The three examples show that the same growth rate can mean quite different reproduction numbers.

**SEIR.** With an exponential latent period of rate $\sigma$ followed by an exponential infectious period of rate $\gamma$, the generation interval is the sum of an exponential latent time and an exponential time into the infectious period. So $M(-r) = \frac{\sigma}{\sigma + r} \cdot \frac{\gamma}{\gamma + r}$ and $R = (1 + r/\sigma)(1 + r/\gamma)$. With a mean latent period of 3 days, a mean infectious period of 5 days and $r = 0.1$, $R = 1.3 \times 1.5 = 1.95$. See the [SEIR model](/seir-epidemic-model/).

**A discrete example.** With $w_1 = 0.2$, $w_2 = 0.5$, $w_3 = 0.3$ (mean 2.1 days) and $R = 1.5$, the growth rate is the root of $\sum_s w_s e^{-rs} = 1/1.5$, which is $r = 0.19766$ per day.

**Non-example: the serial interval.** The serial interval equals the generation interval plus the incubation period of the infected person minus the incubation period of the infector. So its mean is the same as that of the generation interval when the two incubation periods have the same law, but its variance is larger, and it is negative when the infected person shows symptoms first. This happens for diseases with transmission before symptoms. So the alias "serial interval" names a related but different quantity.

**Non-example: the interval measured in a growing epidemic.** If one looks backward from the people infected at a given time, recent infectors are over-represented in a growing epidemic, because there are more of them. The backward intervals are shorter on average than the intrinsic ones. The intervals measured forward from a cohort of infectors are cut short when susceptibles run out. These realized intervals differ from $g$ ([Champredon and Dushoff](#references)).

**Non-example: the duration of infection.** The infectious period is how long a case can infect. The generation interval is when, within that period, a given infection happens. For an exponential infectious period the two have the same mean, but this is special to that case: for a fixed infectious period of length $D$ and constant infectiousness, the generation interval is uniform on $[0, D]$ with mean $D/2$.

## Related definitions

- **[Basic reproduction number](/basic-reproduction-number/).** $R_0$ is the integral of the infectiousness profile; $g$ is its shape. Together they fix the whole profile $\beta(\tau) = R_0 g(\tau)$, and so the early growth rate $r$.
- **[Epidemic renewal equation](/epidemic-renewal-equation/).** The incidence model $E[I_t] = R_t \sum_s w_s I_{t-s}$ uses the discrete generation interval as its kernel. The [Cori method](/cori-rt-estimation/) estimates $R_t$ from it, and the estimate depends on the assumed $w$.
- **Generation time in a branching process.** In a [Galton-Watson process](/galton-watson-process/), every generation lasts one step: the generation interval is fixed at 1. A branching process in continuous time with a random interval law is a Crump-Mode-Jagers process, and its Malthusian parameter is the $r$ above.
- **Mean generation time.** $T_g = \int \tau g(\tau)\, d\tau$. For small $r$, $R \approx 1 + r T_g$ for any law, since $M(-r) = 1 - r T_g + O(r^2)$.
- **Convolution.** The renewal equation is a [convolution](/convolution/) of past incidence with the infectiousness profile.

## References
