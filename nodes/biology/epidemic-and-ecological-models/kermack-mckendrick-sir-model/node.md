---
tag: 83TGQK
kind: model
slug: kermack-mckendrick-sir-model
name: Kermack-McKendrick SIR model
aliases:
- SIR model
- Kermack-McKendrick model
area: biology/epidemic-and-ecological-models
level: intro
summary: "The deterministic SIR model of a well-mixed population: susceptible, infected and removed classes with mass-action infection and a constant removal rate."
history:
  year: 1927
  people: [W. O. Kermack, A. G. McKendrick]
  note: Kermack and McKendrick gave a general model with infectivity and removal rates that depend on the time since infection; the ODE with constant rates is its best known special case.
prereqs: [compartmental-epidemic-model, ode-initial-value-problem]
see_also: [final-size-relation, basic-reproduction-number, sis-epidemic-model, seir-epidemic-model, sir-epidemic-model, epidemic-model, stochastic-sir-model, classical-runge-kutta-4]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: W. O. Kermack and A. G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London A 115(772), 1927
    locator: pages 700 to 721 (the general model with infectivity depending on the time since infection, the threshold density of susceptibles and the final size equation)
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 2.1.1, The SIR model without demography (the threshold phenomenon and epidemic burnout), and Section 2.1.2, The SIR model with demography
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 2000
    locator: pages 599 to 653 (the classic SIR epidemic model, its phase plane, the threshold and the final size)
  - book: isbn:9780198545996
    title: Roy M. Anderson and Robert M. May, Infectious Diseases of Humans, Dynamics and Control, Oxford University Press, 1991
    locator: Part I, microparasites (the basic model of a directly transmitted infection, its threshold and its early growth)
  - paper: "Thomas G. Kurtz, Solutions of ordinary differential equations as limits of pure jump Markov processes, Journal of Applied Probability 7(1), 1970, pages 49 to 58"
    locator: the convergence of density-dependent Markov jump processes to the solution of their ODE on finite time intervals
---

The Kermack-McKendrick SIR model is the deterministic model of an epidemic in a closed, well-mixed population. Each individual is susceptible (S), infected and infectious (I), or removed (R), and three ordinary differential equations move the population from S to I by contact and from I to R at a constant per capita rate. It is the simplest [compartmental epidemic model](/compartmental-epidemic-model/) with immunity, and the gossip page [epidemic model](/epidemic-model/) uses the same equations for the spread of a message among servers. The [SIR model on networks](/sir-epidemic-model/) is its network version: there each individual is a node and infection passes only along edges, while here every individual meets every other at the same rate.

## The machine

**The state.** The counts $S(t)$, $I(t)$ and $R(t)$ at time $t$, with $S + I + R = N$ for a fixed population size $N$. "Removed" covers recovery with lasting immunity, isolation and death; the removed individuals take no further part. The fractions are $s = S/N$, $i = I/N$ and $r = R/N$.

**The parameters.**
- $\beta$, the transmission rate, per unit of time: one infected individual makes contacts that would infect a susceptible at rate $\beta$, and a fraction $S/N$ of these contacts are with susceptibles.
- $\gamma$, the removal rate, per unit of time: each infected individual is removed at rate $\gamma$, so the infectious period is exponential with mean $1/\gamma$.

**The equations.** With frequency-dependent transmission,

$$
\frac{dS}{dt} = -\frac{\beta S I}{N}, \qquad \frac{dI}{dt} = \frac{\beta S I}{N} - \gamma I, \qquad \frac{dR}{dt} = \gamma I,
$$

with $S(0) = S_0 > 0$, $I(0) = I_0 > 0$ and $R(0) = N - S_0 - I_0$. The [basic reproduction number](/basic-reproduction-number/) is $R_0 = \beta / \gamma$: one infected individual in a fully susceptible population infects others at rate $\beta$ for a mean time $1/\gamma$. With density-dependent transmission, $\beta S I / N$ is replaced by $\beta S I$, and then $R_0 = \beta N / \gamma$.

**The standing assumptions.**
- The population is closed: no births, no deaths from other causes, no travel. This fits one epidemic wave that is short compared with a human lifetime.
- Mixing is homogeneous: each pair of individuals has the same contact rate.
- An infected individual is infectious at once (no latent period) and with constant infectivity until removal.
- Removal is permanent: there is no reinfection.
- The counts are large, so random fluctuations are ignored. The equations are the large population limit of a Markov chain (see "Relation to other models").

**The general model of 1927.** Kermack and McKendrick (1927) did not assume constant rates. In their model, an individual infected for a time $\tau$ infects at rate $A(\tau)$, and the force of infection is an integral of $A$ over the past incidence. The ODE above is the case $A(\tau) = \beta e^{-\gamma \tau}$, which holds when infectivity is constant and removal comes at a constant rate. Their threshold result and their final size equation hold for the general $A$, with $R_0 = \int_0^\infty A(\tau) \, d\tau$.

**A worked trajectory.** Take $N = 10000$, $I_0 = 10$, $S_0 = 9990$, $\beta = 0.4$ per day and $\gamma = 0.2$ per day, so $R_0 = 2$ and the mean infectious period is 5 days. The [classical Runge-Kutta method](/classical-runge-kutta-4/) with a step of 0.01 days gives:

| day | $S$ | $I$ | $R$ |
|---|---|---|---|
| 0 | 9990.0 | 10.0 | 0.0 |
| 10 | 9864.4 | 72.3 | 63.2 |
| 20 | 9061.8 | 450.6 | 487.6 |
| 30 | 6268.7 | 1401.2 | 2330.1 |
| 40 | 3498.7 | 1255.3 | 5246.0 |
| 60 | 2159.0 | 181.3 | 7659.7 |
| 100 | 2029.6 | 1.6 | 7968.8 |

The peak comes at about day 33.8, with $I \approx 1539.3$ and $S = N / R_0 = 5000$. The epidemic ends with $R(\infty) \approx 7971.5$ and $S(\infty) \approx 2028.5$: about one person in five never gets infected.

## What it counts

- **The epidemic curve.** The prevalence $I(t)$ and the incidence $\beta S(t) I(t) / N$, the rate of new infections.
- **The early growth rate.** While $S \approx N$, the infected count grows as $I(t) \approx I_0 e^{r t}$ with $r = \beta - \gamma = \gamma (R_0 - 1)$. In the example, $r = 0.2$ per day, and the doubling time is $\ln 2 / r \approx 3.47$ days.
- **The peak.** The largest prevalence $I_{\max}$ and the time at which it occurs.
- **The final size.** The number $R(\infty) - R(0)$ of individuals ever infected, and the number $S(\infty)$ who escape infection.

## Relation to other models

- **[Compartmental epidemic model](/compartmental-epidemic-model/).** The general concept. This page is its SIR case with constant rates.
- **[SIR model on networks](/sir-epidemic-model/).** The same three classes, but infection passes only along the edges of a contact graph. Its final size is a [percolation](/percolation/) problem on the graph, and its threshold depends on the degree distribution. The present model is the limit of complete mixing.
- **[Epidemic model of gossip](/epidemic-model/).** The same equations, read as the spread of an update among servers. The gossip page uses the final size equation to bound the fraction of servers that a protocol misses.
- **[Stochastic SIR model](/stochastic-sir-model/).** The continuous-time Markov chain with infection rate $\beta S I / N$ and removal rate $\gamma I$. For a fixed time horizon its fractions converge to the solution of the ODE as $N \to \infty$ (Kurtz 1970). The chain can die out early by chance, which the ODE cannot show. The [Reed-Frost model](/reed-frost-model/) is the discrete-time chain binomial version.
- **[SIS](/sis-epidemic-model/) and [SEIR](/seir-epidemic-model/) models.** SIS drops immunity, so an endemic state is possible. SEIR adds a latent class; its final size is the same as here for the same $R_0$.
- **SIR with demography.** Births into S and deaths from each class at rate $\mu$ give an endemic equilibrium with $s^* = 1/R_0$ and $R_0 = \beta / (\gamma + \mu)$, reached through damped oscillations (Keeling and Rohani 2008, section 2.1.2). The [SEIR page](/seir-epidemic-model/) works out this case with a latent class.
- **[Epidemic renewal equation](/epidemic-renewal-equation/).** The general model of 1927, with infectivity $A(\tau)$, is a renewal equation for the incidence.

## Known results in the model

All results below are for the equations of "The machine", with $S_0 > 0$ and $I_0 > 0$.

**Conservation.** $S + I + R = N$ for all $t \ge 0$, because the three derivatives sum to zero. The solution exists for all $t \ge 0$, and $S$, $I$ and $R$ stay positive (for $R$, positive for $t > 0$): $S(t) = S_0 \exp\left(-\frac{\beta}{N} \int_0^t I\right) > 0$ and $I(t) = I_0 \exp\left(\int_0^t (\beta S / N - \gamma)\right) > 0$.

**The threshold.** $dI/dt > 0$ exactly when $S > N / R_0$. So the number of infected individuals grows at the start if and only if $R_0 S_0 / N > 1$. Since $S$ decreases, $I$ rises while $S > N / R_0$, peaks once when $S = N / R_0$, and then falls. If $R_0 S_0 \le N$, then $I$ falls from the start. This is the threshold theorem of Kermack and McKendrick.

**A first integral.** The quantity

$$
V(S, I) = S + I - \frac{N}{R_0} \ln S
$$

is constant along each solution.

*Proof.* $\frac{dV}{dt} = \frac{dS}{dt} + \frac{dI}{dt} - \frac{N}{R_0} \frac{1}{S} \frac{dS}{dt} = -\gamma I + \frac{N \gamma}{\beta} \cdot \frac{\beta I}{N} = 0$. $\square$

So each orbit in the $(S, I)$ plane is the curve $I = V_0 - S + \frac{N}{R_0} \ln S$ with $V_0 = V(S_0, I_0)$. In the worked example, $V$ and $S + I + R$ stay constant within $2 \times 10^{-10}$ along the numerical solution.

**The peak.** Put $S = N / R_0$ in the first integral:

$$
I_{\max} = S_0 + I_0 - \frac{N}{R_0} - \frac{N}{R_0} \ln \frac{R_0 S_0}{N}.
$$

For the worked example this is $1539.27$, which matches the numerical peak. When $S_0 \to N$ and $I_0 \to 0$, the peak fraction is $i_{\max} = 1 - (1 + \ln R_0) / R_0$: 0.153426 for $R_0 = 2$ and 0.300463 for $R_0 = 3$. At the peak of the example, $N - S = 5000$ individuals have been infected, about 63 percent of the final total of 7971.5: the epidemic overshoots the threshold by a large amount after the peak.

**Burnout, not exhaustion.** $I(t) \to 0$ and $S(t) \to S_\infty > 0$ as $t \to \infty$. The epidemic stops because the susceptibles fall below the threshold $N / R_0$, not because none are left.

*Proof.* $R$ is increasing and bounded by $N$, so it has a limit, and $\int_0^\infty \gamma I \, dt = R(\infty) - R(0)$ is finite. $I$ has a bounded derivative, so it is uniformly continuous, and an integrable, uniformly continuous, positive function tends to 0. $S$ is decreasing and positive, so it has a limit $S_\infty \ge 0$. If $S_\infty = 0$, then $\ln S \to -\infty$ and $V \to +\infty$, which contradicts that $V$ is constant. So $S_\infty > 0$. $\square$

**The final size.** Letting $t \to \infty$ in the first integral gives the equation for $S_\infty$:

$$
S_\infty - \frac{N}{R_0} \ln S_\infty = S_0 + I_0 - \frac{N}{R_0} \ln S_0 .
$$

In the example, its root is $S_\infty = 2028.46$, so $7971.54$ individuals are removed in the end. In the limit $S_0 \to N$, $I_0 \to 0$, the fraction $z$ ever infected solves $z = 1 - e^{-R_0 z}$, which gives $z = 0.796812$ for $R_0 = 2$. The [final size relation](/final-size-relation/) states and proves this result, with its hypotheses, and gives the values for other $R_0$.

**No closed form in $t$.** The orbit has the closed form above, but $S(t)$ is not an elementary function of $t$; numerical solution of the initial value problem is the normal method. The system is not stiff for usual parameter values, so an explicit [Runge-Kutta method](/runge-kutta-methods/) with a fixed step is enough.

## References
