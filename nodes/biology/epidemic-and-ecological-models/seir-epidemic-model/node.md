---
tag: MCAZGR
kind: model
slug: seir-epidemic-model
name: SEIR epidemic model
aliases:
- susceptible-exposed-infectious-recovered model
area: biology/epidemic-and-ecological-models
level: core
summary: An SIR model with an exposed class of individuals who are infected but not yet infectious, for diseases with a latent period.
prereqs: [kermack-mckendrick-sir-model, basic-reproduction-number]
see_also: [next-generation-matrix, final-size-relation, generation-interval, compartmental-epidemic-model, sir-epidemic-model, jacobian-linearization, classical-runge-kutta-4, stochastic-sir-model]
sources:
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 2000
    locator: pages 599 to 653 (the SEIR and MSEIR models with births and deaths, their threshold quantities and endemic equilibria)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 2.5, Infection with a latent period (the SEIR model), Section 2.1.2.3, oscillatory dynamics, Section 2.1.2.4, the mean age at infection, and Section 3.3.1, SEIR and multi-compartment models
  - paper: doi:10.1007/s11538-005-9047-7
    title: Junling Ma and David J. D. Earn, Generality of the final size formula for an epidemic of a newly invading infectious disease, Bulletin of Mathematical Biology 68(3), 2006
    locator: pages 679 to 702 (the final size formula of the SIR model holds also with a latent period and several infectious stages)
  - book: isbn:9780198545996
    title: Roy M. Anderson and Robert M. May, Infectious Diseases of Humans, Dynamics and Control, Oxford University Press, 1991
    locator: Part I, microparasites (models with latent periods, the interepidemic period and the age at infection for measles and other childhood infections)
---

The SEIR epidemic model adds to the [Kermack-McKendrick SIR model](/kermack-mckendrick-sir-model/) an exposed class E of individuals who are infected but cannot yet transmit. It is the standard model for diseases with a clear latent period, such as measles, chickenpox and influenza. The latent period does not change the [basic reproduction number](/basic-reproduction-number/) when there are no deaths during it, and it does not change the final size of an epidemic in a closed population. It does slow the growth of the epidemic, because each generation of cases takes longer. With births and deaths, the model has an endemic equilibrium, and the approach to it shows damped oscillations with a period of a few years, the classical explanation of recurrent childhood epidemics. Like the Kermack-McKendrick model, it assumes a well-mixed population; the [SIR model on networks](/sir-epidemic-model/) puts the same states on the nodes of a contact graph instead.

## The machine

**State.** The numbers $S$, $E$, $I$ and $R$ of susceptible, exposed, infectious and recovered individuals, with $S + E + I + R = N$.

**Parameters.** The transmission rate $\beta$, the rate $\sigma$ at which exposed individuals become infectious (the mean latent period is $1/\sigma$), the recovery rate $\gamma$ (the mean infectious period is $1/\gamma$), and an optional birth and death rate $\mu$. With $\mu > 0$, births enter S at the rate $\mu N$ and each class loses individuals at the per capita rate $\mu$, so $N$ stays constant.

**Equations.**

$$
\begin{aligned}
\frac{dS}{dt} &= \mu N - \frac{\beta S I}{N} - \mu S, \\
\frac{dE}{dt} &= \frac{\beta S I}{N} - (\sigma + \mu) E, \\
\frac{dI}{dt} &= \sigma E - (\gamma + \mu) I, \\
\frac{dR}{dt} &= \gamma I - \mu R .
\end{aligned}
$$

Only infectious individuals transmit, and a new infection enters E, not I. With $\mu = 0$ this is the closed epidemic model. The stochastic reading is the continuous-time Markov chain with the same rates, one event per individual transfer.

**Assumptions.** Homogeneous mixing, frequency-dependent transmission, exponential latent and infectious periods, and lasting immunity.

## What it counts

**The basic reproduction number.** Use the [next-generation matrix](/next-generation-matrix/) with the infected classes $x = (E, I)$ at the disease-free state $S = N$. New infections appear only in E, at the rate $\beta I$, and all other flows go into $V$:

$$
F = \begin{pmatrix} 0 & \beta \\ 0 & 0 \end{pmatrix}, \qquad V = \begin{pmatrix} \sigma + \mu & 0 \\ -\sigma & \gamma + \mu \end{pmatrix}, \qquad F V^{-1} = \begin{pmatrix} \dfrac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu)} & \dfrac{\beta}{\gamma + \mu} \\ 0 & 0 \end{pmatrix}.
$$

The matrix is triangular, so its spectral radius is its top left entry:

$$
R_0 = \frac{\beta \sigma}{(\sigma + \mu)(\gamma + \mu)} .
$$

The factor $\sigma / (\sigma + \mu)$ is the probability that an exposed individual lives to become infectious, and $\beta / (\gamma + \mu)$ is the expected number of infections it then causes. With $\mu = 0$, $R_0 = \beta / \gamma$, the same as for SIR.

**The growth rate.** Without births, the linearization of $(E, I)$ at the disease-free state has the growth rate $r$ that solves $(r + \sigma)(r + \gamma) = \beta \sigma$, so

$$
R_0 = \left( 1 + \frac{r}{\sigma} \right) \left( 1 + \frac{r}{\gamma} \right).
$$

For SIR the relation is $R_0 = 1 + r / \gamma$, so if you fit SIR equations to an SEIR disease, you get an $R_0$ that is too small. The mean [generation interval](/generation-interval/) is $1/\sigma + 1/\gamma$.

**A hand example.** Take $\beta = 0.4$ and $\gamma = 0.2$ per day, so $R_0 = 2$ for every $\sigma$. Solve the quadratic $r^2 + (\sigma + \gamma) r + \sigma \gamma - \beta \sigma = 0$:

| mean latent period $1/\sigma$ | $r$ per day | doubling time | check $(1 + r/\sigma)(1 + r/\gamma)$ |
|---|---|---|---|
| 5 days | 0.0828 | 8.4 days | 2.000 |
| 2 days | 0.1217 | 5.7 days | 2.000 |
| 1 day | 0.1483 | 4.7 days | 2.000 |
| none (SIR) | 0.2000 | 3.5 days | $1 + r/\gamma = 2$ |

For $1/\sigma = 5$ days, $(r + 0.2)^2 = 0.08$, so $r = \sqrt{0.08} - 0.2 \approx 0.0828$.

## Relation to other models

- **[SIR](/kermack-mckendrick-sir-model/).** The limit $\sigma \to \infty$, an instant latent period. The final size and $R_0$ without births are the same as for SIR, but the time course is slower.
- **Stage splitting.** Split E into $k$ stages, each left at rate $k \sigma$, to make the latent period Erlang distributed with the same mean and a smaller variance (see the [compartmental epidemic model](/compartmental-epidemic-model/)). The same trick applies to I.
- **SEIRS, MSEIR.** Waning immunity returns R to S; a class M of infants protected by maternal antibodies comes before S (Hethcote 2000).
- **The general Kermack-McKendrick model.** The 1927 model with an infectivity $A(\tau)$ that depends on the time since infection contains SEIR as the case where $A(\tau)$ is $\beta$ times the probability of being in I at time $\tau$.
- **Stochastic SEIR.** The Markov chain with the same rates, simulated with the [Gillespie algorithm](/gillespie-algorithm/). Its early phase is a branching process with two types, E and I, and the extinction probability depends on whether the first case is exposed or infectious.
- **[SIR model on networks](/sir-epidemic-model/).** States on the nodes of a contact graph instead of class counts in a well-mixed population. The final size there depends on the graph, not only on $R_0$.

## Known results in the model

**Final size without births.** With $\mu = 0$, the fraction $z$ of the population ever infected, for an epidemic that starts from a very small number of cases, solves the same [final size relation](/final-size-relation/) as SIR:

$$
z = 1 - e^{-R_0 z}.
$$

The proof is the same as for SIR: $d \ln S / dt = -\beta I / N$ and $dR/dt = \gamma I$, so $\ln S$ and $R$ change in a fixed ratio, and at the end all of E and I have moved to R. Ma and Earn (2006) show that the formula holds for any number of latent and infectious stages. For $R_0 = 2$, $z \approx 0.797$.

**The endemic equilibrium.** With $\mu > 0$ and $R_0 > 1$, there is one endemic equilibrium, with fractions

$$
s^* = \frac{1}{R_0}, \qquad i^* = \frac{\mu (R_0 - 1)}{\beta}, \qquad e^* = \frac{(\gamma + \mu)\, i^*}{\sigma}, \qquad r^* = 1 - s^* - e^* - i^* .
$$

To derive $s^*$, set $dE/dt = dI/dt = 0$: then $\beta s^* = (\sigma + \mu)(\gamma + \mu)/\sigma$, so $s^* = 1/R_0$. Then $dS/dt = 0$ gives $\mu (1 - s^*) = \beta s^* i^*$. For $R_0 \le 1$, the only equilibrium is the disease-free one, and it is stable.

**Damped oscillations.** At the endemic equilibrium, the [linearization](/jacobian-linearization/) has one fast real eigenvalue and a complex pair with a small negative real part, so the system returns to the equilibrium in slow, damped oscillations. Take numbers like measles: a life span of 70 years ($\mu = 1/25550$ per day), a latent period of 8 days, an infectious period of 5 days and $R_0 = 15$, which gives $\beta \approx 3.0015$ per day. Then $s^* = 1/15$, $e^* \approx 2.92 \times 10^{-4}$, $i^* \approx 1.83 \times 10^{-4}$, and the eigenvalues of the reduced system in $(s, e, i)$ are about $-0.3252$ and $-0.000229 \pm 0.006488 i$ per day. The period of the oscillation is $2\pi / 0.006488 \approx 968$ days, about 2.65 years. The approximation

$$
T \approx 2 \pi \sqrt{A G},
$$

with the mean age at infection $A \approx 1 / (\mu (R_0 - 1)) = 70/14 = 5$ years and $G = 1/\sigma + 1/\gamma = 13$ days, gives $2\pi \sqrt{5 \cdot 365 \cdot 13} \approx 968$ days. The damping time is $1/0.000229 \approx 4400$ days, about 12 years. In the deterministic model the oscillations die out; in real populations, seasonal changes in contact rates and chance events keep them going.

**The mean age at infection.** At the endemic equilibrium, a susceptible individual is infected at the rate $\beta i^* = \mu (R_0 - 1)$, so the mean age at infection is about $1 / (\mu (R_0 - 1))$, which is about $L / (R_0 - 1)$ for a life expectancy $L$. With $L = 70$ years and $R_0 = 15$ it is 5 years. Vaccination lowers the effective $R_0$ and so raises the mean age at infection.

**Numerical note.** With births, the time scales differ by a factor of more than 1000 (a fast eigenvalue of about $-0.33$ per day against a slow one of about $-0.0002$ per day). An explicit method such as the [classical Runge-Kutta method](/classical-runge-kutta-4/) with a step of a fraction of a day is still stable and accurate, but runs over decades need many steps. An implicit method for a [stiff problem](/stiff-ode-problem/) allows larger steps.

## References
