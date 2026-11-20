---
tag: 4VMCW9
kind: definition
slug: canonical-ensemble
name: Canonical ensemble
aliases:
- NVT ensemble
area: scientific-computing/molecular-simulation
level: core
summary: The distribution of states at fixed particle number, volume and temperature, with probability proportional to exp(-E/kT).
prereqs: [microcanonical-ensemble]
see_also: [partition-function, nose-hoover-thermostat, langevin-dynamics, andersen-thermostat, stochastic-velocity-rescaling, metropolis-hastings, free-energy-perturbation, ergodicity]
sources:
  - book: isbn:9780198803195
    title: Michael P. Allen and Dominic J. Tildesley, Computer Simulation of Liquids, second edition, Oxford University Press, 2017
    locator: Chapter 2, statistical mechanics (the common ensembles and their fluctuations)
  - book: isbn:9780198525264
    title: Mark E. Tuckerman, Statistical Mechanics, Theory and Molecular Simulation, Oxford University Press, 2010
    locator: Chapter 4, the canonical ensemble
  - book: isbn:9780122673511
    title: Daan Frenkel and Berend Smit, Understanding Molecular Simulation, From Algorithms to Applications, second edition, Academic Press, 2002
    locator: Chapter 2 (statistical mechanics and ensembles)
  - book: isbn:9783319163741
    title: Ben Leimkuhler and Charles Matthews, Molecular Dynamics, With Deterministic and Stochastic Numerical Methods, Springer, 2015
    locator: Chapter 6, the canonical distribution and stochastic differential equations
---

The canonical ensemble is the probability distribution of a system with a fixed number of particles $N$ and a fixed volume $V$ that exchanges energy with a large heat bath at temperature $T$. A state of energy $E$ has a probability proportional to the Boltzmann factor $e^{-E / k_B T}$, so low energies are favoured and the temperature sets how strongly. It is the ensemble of most experiments at a fixed temperature, of Metropolis Monte Carlo, and of molecular dynamics with a thermostat such as [Langevin dynamics](/langevin-dynamics/) or the [Nose-Hoover thermostat](/nose-hoover-thermostat/). Its normalization is the [partition function](/partition-function/) $Z$, and the Helmholtz free energy is $A = -k_B T \ln Z$.

## Definition

Let $\Gamma = (x_1, \ldots, x_N, p_1, \ldots, p_N)$ be a point of phase space with the positions in the volume $V$, and let $H(\Gamma) = K(p) + U(x)$ with $K = \sum_i |p_i|^2 / (2 m_i)$. Let $\beta = 1 / (k_B T)$. The canonical ensemble at $(N, V, T)$ is the probability density
$$\rho_{NVT}(\Gamma) = \frac{e^{-\beta H(\Gamma)}}{Z(N, V, T)}, \qquad Z(N, V, T) = \frac{1}{N!\, h_P^{dN}} \int e^{-\beta H(\Gamma)}\, d\Gamma,$$
in $d$ dimensions, where $h_P$ is Planck's constant, which fixes the units of $Z$, and $N!$ counts the exchanges of identical particles. The average of an observable $A$ is $\langle A \rangle_{NVT} = \int A\, \rho_{NVT}\, d\Gamma$.

Three facts follow at once and are used on every thermostat page:

- **It factors.** $e^{-\beta H} = e^{-\beta K(p)} e^{-\beta U(x)}$, so the momenta are independent of the positions. Each momentum component $p_{ia}$ is normal with mean 0 and variance $m_i k_B T$: the Maxwell-Boltzmann distribution. The positions have the density $e^{-\beta U(x)} / Z_x$, with the configurational integral $Z_x = \int e^{-\beta U}\,dx$. Monte Carlo methods sample this part alone.
- **The kinetic energy has a gamma law.** $K$ is a sum of $N_f$ squares of independent normals, so it has the density proportional to $K^{N_f/2 - 1} e^{-\beta K}$, with mean $\frac12 N_f k_B T$ and variance $\frac12 N_f (k_B T)^2$. Here $N_f$ is the number of velocity degrees of freedom: $dN$, minus $d$ if the total momentum is fixed, minus one for each holonomic constraint. A simulation reports the kinetic temperature $k_B T = 2 \langle K \rangle / N_f$, so it must give $N_f$.
- **It is the microcanonical ensemble averaged over the energy.** $\rho_{NVT} = \int \rho_{NVE}\, \Omega(E) e^{-\beta E}\, dE / Z$, where $\Omega(E)$ is the density of states of the [microcanonical ensemble](/microcanonical-ensemble/). So $Z$ is the Laplace transform of $\Omega$.

**The energy fluctuates.** From $\langle E \rangle = -\partial \ln Z / \partial \beta$ and one more derivative,
$$\langle \delta E^2 \rangle = \frac{\partial^2 \ln Z}{\partial \beta^2} = k_B T^2 C_V,$$
with the heat capacity $C_V = \partial \langle E \rangle / \partial T$ at fixed $N$ and $V$ (a theorem). For a system of $N$ particles, $\langle E \rangle$ and $C_V$ grow as $N$, so the relative size of the fluctuation is $O(N^{-1/2})$, and for large $N$ the canonical ensemble is concentrated near one energy. Averages of local quantities agree with the microcanonical ones up to $O(1/N)$. Fluctuations do not agree: the variance of $K$ above is the canonical value, and it is different at fixed energy.

**Sampling it.** A method samples the canonical ensemble if $\rho_{NVT}$ (or its marginal in $\Gamma$, for a method with extra variables) is a stationary density of the method and the method is ergodic, so that time averages converge to ensemble averages. Stationarity can be proved for a given method. [Ergodicity](/ergodicity/) holds for stochastic methods such as [Langevin dynamics](/langevin-dynamics/) and the [Andersen thermostat](/andersen-thermostat/) under mild conditions, and it is a hypothesis for deterministic methods such as the Nose-Hoover thermostat. A time-stepping method keeps $\rho_{NVT}$ only up to its time step error unless a Metropolis test corrects it.

## Examples and non-examples

**One harmonic oscillator.** Take $H = p^2/(2m) + k x^2 / 2$ with $m = k = k_B T = 1$ in reduced units. Then $x$ and $p$ are independent standard normals: $\langle x^2 \rangle = 1$, $\langle x^4 \rangle / \langle x^2 \rangle^2 = 3$, and $\langle H \rangle = 1$, half from each square. The probability of $|x| < \frac12$ is $\operatorname{erf}(0.5/\sqrt2) = 0.3829$. Compare the microcanonical ensemble at the same mean energy $E = 1$: there $x$ has the arcsine law on $[-\sqrt2, \sqrt2]$, with $\langle x^4 \rangle / \langle x^2 \rangle^2 = 1.5$ and $P(|x| < \frac12) = \frac{2}{\pi}\arcsin(0.5/\sqrt2) = 0.2301$. The ratio $\langle x^4 \rangle / \langle x^2 \rangle^2$ is a simple test of whether a thermostat samples the canonical ensemble.

**Energy fluctuation of the oscillator.** $H$ is the sum of two independent terms $\frac12 x^2$ and $\frac12 p^2$, each a half of a chi-squared variable with one degree of freedom, with variance $\frac12 (k_B T)^2$. So $\langle \delta E^2 \rangle = (k_B T)^2$. The formula $k_B T^2 C_V$ gives the same, since $\langle E \rangle = k_B T$ and $C_V = k_B$.

**A two-level system.** Two states with energies 0 and $\epsilon$, and $\beta\epsilon = 1$. Then $Z = 1 + e^{-1}$, the upper state has probability $e^{-1}/(1 + e^{-1}) = 0.268941$, and $\langle E \rangle = 0.268941\,\epsilon$. The variance is $p(1 - p)\epsilon^2 = 0.196612\,\epsilon^2$, so $C_V = \langle \delta E^2 \rangle / (k_B T^2) = (\beta\epsilon)^2 \cdot 0.196612\, k_B = 0.196612\, k_B$.

**The kinetic energy of 20 particles.** Take 20 particles on a line with $k_B T = 1$ and no constraint, so $N_f = 20$. The canonical law of $K$ has mean 10 and variance 10, so the standard deviation of the kinetic temperature $2K/N_f$ is $\sqrt{2/N_f} = 0.316$ times $T$. A run that reports the mean of $K$ only does not test the ensemble; the variance is the stronger test, and the thermostat pages of this area use these two numbers.

**Non-example: the Berendsen thermostat.** The [Berendsen thermostat](/berendsen-thermostat/) relaxes $K$ toward its target. For free particles the variance of $K$ goes to 0, not to $\frac12 N_f (k_B T)^2$, so it does not sample this ensemble.

**Non-example: one oscillator with one Nose-Hoover thermostat.** The canonical density is stationary for the Nose-Hoover equations, but on one harmonic oscillator the motion is not ergodic. A long run gives $\langle x^2 \rangle \approx 0.79$ and $\langle x^4 \rangle / \langle x^2 \rangle^2 \approx 1.54$ instead of 1 and 3 (a measurement on the Nose-Hoover page). [Nose-Hoover chains](/nose-hoover-chains/) repair this case.

**Non-example: plain molecular dynamics.** [Molecular dynamics](/molecular-dynamics/) without a thermostat conserves the energy, so it samples the microcanonical ensemble at best. Its kinetic energy fluctuates, but with the microcanonical variance.

## Related definitions

- **[Microcanonical ensemble](/microcanonical-ensemble/).** Fixed $N$, $V$ and $E$. The canonical ensemble is its average over $E$ with the weight $\Omega(E) e^{-\beta E}$.
- **[Partition function](/partition-function/).** The normalization $Z$. Derivatives of $\ln Z$ give the mean energy, the heat capacity and, through $A = -k_B T \ln Z$, the free energy, which [free energy perturbation](/free-energy-perturbation/) and [thermodynamic integration](/thermodynamic-integration/) compute as differences.
- **Isothermal-isobaric ensemble.** Fixed $N$, $P$ and $T$, with density proportional to $e^{-\beta(H + PV)}$ and the volume as an extra variable. The [Parrinello-Rahman barostat](/parrinello-rahman-barostat/) together with a thermostat samples a form of it.
- **Boltzmann distribution.** The same weight $e^{-\beta E}$ on a discrete set of states, as in the two-level example and in the [Ising model](/ising-model/).
- **[Stationary distribution](/stationary-distribution/).** A Monte Carlo chain such as [Metropolis-Hastings](/metropolis-hastings/) is built so that $e^{-\beta U}/Z_x$ is its stationary distribution, often through [detailed balance](/detailed-balance/).

## References
