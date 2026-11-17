---
tag: D3ME5Y
kind: model
slug: sis-epidemic-model
name: SIS epidemic model
aliases:
- susceptible-infected-susceptible model
area: biology/epidemic-and-ecological-models
level: intro
summary: Infected individuals recover without immunity and return to the susceptible class, so the infection can persist at an endemic level.
prereqs: [compartmental-epidemic-model, basic-reproduction-number]
see_also: [kermack-mckendrick-sir-model, logistic-growth-model, heterogeneous-mean-field-epidemic, ross-macdonald-model, birth-death-process, epidemic-threshold, sir-epidemic-model, classical-runge-kutta-4]
sources:
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 2000
    locator: pages 599 to 653 (the SIS model, its threshold and its endemic equilibrium)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 2.3, Infection without immunity (the SIS model), and Section 3.1.1.1, high and low risk groups (an SIS model of a sexually transmitted infection in two groups)
  - paper: doi:10.1103/PhysRevLett.86.3200
    title: Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic spreading in scale-free networks, Physical Review Letters 86(14), 2001
    locator: pages 3200 to 3203 (the SIS model on networks with a degree distribution, and its threshold)
---

The SIS epidemic model is the [compartmental epidemic model](/compartmental-epidemic-model/) for an infection that gives no immunity: an infected individual recovers and is immediately susceptible again. Many bacterial infections, such as gonorrhea, and many sexually transmitted infections are modeled this way. Because the supply of susceptibles never runs out, the infection does not burn out as in the [Kermack-McKendrick SIR model](/kermack-mckendrick-sir-model/). When the [basic reproduction number](/basic-reproduction-number/) $R_0$ is larger than 1, it settles at an endemic level $1 - 1/R_0$ of the population. The infected fraction follows the [logistic equation](/logistic-growth-model/) exactly.

## The machine

**State.** A closed population of $N$ individuals, with $S$ susceptible and $I$ infected, and $S + I = N$. In fractions, $s = S/N$ and $i = I/N$, with $s + i = 1$.

**Parameters.** The transmission rate $\beta$ (transmitting contacts of one individual per unit of time) and the recovery rate $\gamma$ (so the mean infectious period is $1/\gamma$). Both are positive.

**Transitions.**

| Transition | Change | Rate |
|---|---|---|
| infection | $(S, I) \to (S - 1, I + 1)$ | $\beta S I / N$ |
| recovery | $(S, I) \to (S + 1, I - 1)$ | $\gamma I$ |

**Deterministic reading.**

$$
\frac{dS}{dt} = -\frac{\beta S I}{N} + \gamma I, \qquad \frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I .
$$

With $s = 1 - i$, the system reduces to one equation for the infected fraction:

$$
\frac{di}{dt} = \beta i (1 - i) - \gamma i = (\beta - \gamma)\, i \left( 1 - \frac{i}{i^*} \right), \qquad i^* = 1 - \frac{\gamma}{\beta} .
$$

**Stochastic reading.** The number $I$ of infected individuals is a [birth-death process](/birth-death-process/) on $\{0, 1, \ldots, N\}$ with birth rate $\beta I (N - I)/N$ and death rate $\gamma I$. The state $I = 0$ is absorbing.

**Assumptions.** Homogeneous mixing, frequency-dependent transmission, an exponential infectious period, no latent period, and no births or deaths. With births and deaths at the same rate $\mu$ (each newborn susceptible), the equation for $i$ keeps its form with $\gamma$ replaced by $\gamma + \mu$.

## What it counts

The model counts the fraction of the population that is infected now, the prevalence, as a function of time. It also gives the incidence $\beta s i$, the rate of new infections per individual, and at the endemic equilibrium the incidence equals the recovery rate $\gamma i^*$. It does not count the number of people who were ever infected, because the same person can be infected many times. The threshold quantity is

$$
R_0 = \frac{\beta}{\gamma},
$$

the number of new infections that one case causes during its mean infectious period $1/\gamma$ in a population that is all susceptible. With births and deaths, $R_0 = \beta / (\gamma + \mu)$. In terms of $R_0$, the endemic prevalence is $i^* = 1 - 1/R_0$, and the susceptible fraction at equilibrium is $s^* = 1/R_0$.

**A hand example.** Take $\beta = 0.3$ per day and $\gamma = 0.1$ per day. Then $R_0 = 3$ and $i^* = 2/3$: at equilibrium, two thirds of the population are infected, and the rate of new infections per individual is $0.3 \cdot (1/3) \cdot (2/3) = 1/15$ per day, which equals the recovery rate $0.1 \cdot 2/3$. Start from $i_0 = 0.01$. The solution (derived below) gives

| day | $i(t)$ |
|---|---|
| 0 | 0.0100 |
| 10 | 0.0674 |
| 20 | 0.3027 |
| 30 | 0.5733 |
| 50 | 0.6647 |

The prevalence reaches half of $i^*$ at $t = \ln(i^*/i_0 - 1) / (\beta - \gamma) = \ln(65.67) / 0.2 \approx 20.9$ days.

## Relation to other models

- **[SIR](/kermack-mckendrick-sir-model/).** Recovery gives lasting immunity. Without births, the SIR epidemic always ends, with $I \to 0$; the SIS infection persists when $R_0 > 1$. The SIRS model, where immunity wanes at a rate, lies between the two.
- **[Logistic growth](/logistic-growth-model/).** The SIS equation for $i$ is the logistic equation with growth rate $\beta - \gamma$ and carrying capacity $i^*$. So the solutions, the S-shaped curve and the stability results carry over directly.
- **SI.** With $\gamma = 0$, everyone is infected in the end: $i^* = 1$. Push gossip in [distributed systems](/epidemic-model/) has this form.
- **SIS with structure.** Split the population into groups with a contact matrix, and the threshold is the spectral radius of a [next-generation matrix](/next-generation-matrix/). On a contact network, the [degree-based mean-field model](/heterogeneous-mean-field-epidemic/) gives one SIS equation for each degree class, and its threshold falls with the variance of the degree distribution. The [SIR model on networks](/sir-epidemic-model/) is the network version of SIR; it uses one state per node instead of one fraction per class.
- **[Ross-Macdonald](/ross-macdonald-model/).** The classical malaria model is an SIS model in each of two host species, humans and mosquitoes, coupled by bites.

## Known results in the model

**Closed form.** The logistic equation has the solution

$$
i(t) = \frac{i^*}{1 + \left( i^*/i_0 - 1 \right) e^{-(\beta - \gamma) t}}
$$

for $\beta \ne \gamma$ and $i_0 > 0$. To check it, set $u = 1/i$. Then $du/dt = -(1/i^2)\, di/dt = -(\beta - \gamma) u + \beta$, a linear equation with the solution $u(t) = \beta/(\beta - \gamma) + (u_0 - \beta/(\beta - \gamma)) e^{-(\beta - \gamma) t}$, and $\beta / (\beta - \gamma) = 1/i^*$.

**Threshold.** Let $i_0 \in (0, 1]$.
- If $R_0 \le 1$, then $i(t) \to 0$. For $R_0 < 1$, $di/dt \le (\beta - \gamma) i$, so $i$ decays at least as fast as $e^{-(\beta - \gamma) t}$. For $R_0 = 1$, $di/dt = -\beta i^2$, and $i(t) = i_0 / (1 + \beta i_0 t)$ decays only like $1/t$.
- If $R_0 > 1$, then $i(t) \to i^* = 1 - 1/R_0$, monotonically, from above or below. The linearization at $i = 0$ has the eigenvalue $\beta - \gamma > 0$ (the disease-free state is unstable), and at $i = i^*$ it has the eigenvalue $-(\beta - \gamma) < 0$.

So $R_0 = 1$ is a transcritical bifurcation: the two equilibria $i = 0$ and $i = i^*$ cross and exchange stability.

**Early growth.** For small $i$, $i(t) \approx i_0 e^{(\beta - \gamma) t}$, with the growth rate $r = \gamma (R_0 - 1)$. In the example, $r = 0.2$ per day and the doubling time is $\ln 2 / 0.2 \approx 3.47$ days.

**Stochastic extinction.** In the Markov chain with finite $N$, the absorbing state $I = 0$ is reached with probability 1, so the infection always dies out in the end, also when $R_0 > 1$. The deterministic endemic level describes the quasi-stationary distribution, the distribution of $I$ conditioned on $I > 0$. For $R_0 > 1$ the mean time to extinction from that distribution grows exponentially with $N$, so in a large population the endemic state lasts for a very long time. For $R_0 < 1$, from a start with a fixed fraction of the population infected, the mean time to extinction grows only like $\ln N$. Near $R_0 = 1$ the threshold is not sharp in a small population.

**Equilibrium with groups.** For an SIS model with $n$ groups and an irreducible contact matrix, the same dichotomy holds: if the spectral radius of the next-generation matrix is at most 1, the infection dies out, and if it is larger than 1, there is one endemic equilibrium, and it attracts every start with some infection. The two-group model of high-risk and low-risk individuals for a sexually transmitted infection in Keeling and Rohani (2008, section 3.1.1.1) is an example. A small high-risk group can keep the infection endemic in the whole population, so control that reaches that group has a large effect.

## References
