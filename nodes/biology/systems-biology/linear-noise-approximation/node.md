---
tag: 4M8YH0
kind: technique
slug: linear-noise-approximation
name: Linear noise approximation
aliases:
- van Kampen system size expansion
area: biology/systems-biology
level: advanced
summary: Expand the master equation in powers of the inverse square root of the system size to get the rate equations plus Gaussian fluctuations around them.
prereqs: [chemical-master-equation, jacobian-linearization, lyapunov-equation]
see_also: [chemical-langevin-equation, moment-closure, finite-state-projection, mass-action-kinetics, lyapunov-stability, central-limit-theorem, gene-regulatory-network, sylvester-equation]
sources:
  - book: isbn:9780444529657
    title: Nicolaas G. van Kampen, Stochastic Processes in Physics and Chemistry, 3rd edition, Elsevier, 2007
    locator: Chapter X, The expansion of the master equation, pp. 244-272, with Section 4 (the linear noise approximation, p. 258), Section 5 (several variables, p. 263) and Section 6 (higher orders, p. 267)
  - paper: doi:10.1101/gr.1196503
    title: Johan Elf and Måns Ehrenberg, Fast evaluation of fluctuations in biochemical networks with the linear noise approximation, Genome Research 13(11), 2003, 2475-2484
    locator: the stationary covariance from the Lyapunov equation with the Jacobian and the diffusion matrix, applied to biochemical networks
  - paper: doi:10.1088/1751-8121/aa54d9
    title: David Schnoerr, Guido Sanguinetti and Ramon Grima, Approximation and inference methods for stochastic biochemical kinetics, a tutorial review, Journal of Physics A 50(9), 2017, 093001
    locator: the section on the linear noise approximation, its accuracy, and its relation to the chemical Langevin equation
  - paper: doi:10.1063/1.1678692
    title: Thomas G. Kurtz, The relationship between stochastic and deterministic models for chemical reactions, Journal of Chemical Physics 57(7), 1972, 2976-2978
    locator: the rate equations as the large volume limit, the first term of the expansion
---

The linear noise approximation (LNA) describes the fluctuations of a reaction network with large counts as Gaussian noise around the solution of the deterministic rate equations. It comes from an expansion of the [chemical master equation](/chemical-master-equation/) in powers of $\Omega^{-1/2}$, where $\Omega$ is the system size (the volume times Avogadro's number, or any scale of the counts). The term of the highest order gives the rate equations, and the next term gives a linear stochastic equation for the fluctuations, whose covariance solves a [Lyapunov equation](/lyapunov-equation/) built from the Jacobian of the rate equations and a diffusion matrix. The LNA is the first order of that expansion, and van Kampen gave the full expansion; the higher terms give corrections of order $\Omega^{-1/2}$ and smaller. The LNA turns a question about a distribution over a huge state space into linear algebra of size $n$, which is why it is the standard first tool for noise in gene expression and signaling.

## In plain words

In a large system, the number of molecules follows the smooth curve that the usual rate equations predict, plus small random wiggles. The wiggles come from reactions that happen a little earlier or later than average.

The idea is to describe only the wiggles, and to treat them as small. Small wiggles near a steady state behave simply: each one is pushed back toward the curve at a rate set by how the network reacts to a small change, and new wiggles are added by every reaction that fires. Balancing the push back against the new wiggles gives the size of the noise and how the noise of one species goes with another.

The answer is a bell curve around the steady state. It is good for big counts and a single stable state. It cannot see rare jumps or small counts.

## When it applies

- **Large counts.** Every species that reacts has a count large enough that a change of one molecule changes the propensities little. In practice, counts in the tens or more.
- **One stable state.** The rate equations have one asymptotically stable steady state, or a solution that stays away from regions where the counts are small. The LNA is local: it linearizes around one solution.
- **Moments of order 1 and 2.** The question is about means, variances, covariances, correlation times or noise spectra, not about tails, extinction or switching.
- **Scaled propensities.** Each propensity can be written as $a_j(x) = \Omega f_j(x/\Omega) + O(1)$, where $f_j$ is the macroscopic rate in concentrations. Mass action propensities have this form.

## The template

1. **Scale.** Write $X = \Omega \phi(t) + \Omega^{1/2} \xi(t)$, where $\phi$ is the concentration on the deterministic path and $\xi$ is the fluctuation, of order 1.
2. **Order $\Omega^{1/2}$: the rate equations.** Collect the terms of the master equation of this order. They give $\dot\phi = S f(\phi)$ with the [stoichiometric matrix](/stoichiometric-matrix/) $S$. Solve for $\phi(t)$, or for the steady state $\phi^*$ with $S f(\phi^*) = 0$.
3. **The Jacobian.** $J = \partial (S f)/\partial \phi$ at $\phi(t)$, as in [Jacobian linearization](/jacobian-linearization/). At a stable steady state every eigenvalue of $J$ has a negative real part ([Lyapunov stability](/lyapunov-stability/)).
4. **The diffusion matrix.** $D = S \operatorname{diag}(f(\phi)) S^{\mathsf T}$: each reaction adds noise along its change vector, with the strength of its rate.
5. **Order $\Omega^0$: the fluctuations.** The terms of this order give a linear Fokker-Planck equation for $\xi$, so $\xi$ is Gaussian, with mean 0 if it starts at 0 and covariance $\Sigma$ that solves
$$\dot\Sigma = J \Sigma + \Sigma J^{\mathsf T} + D .$$
6. **The steady state.** At $\phi^*$, solve the Lyapunov equation $J \Sigma + \Sigma J^{\mathsf T} + D = 0$, a linear system for the $n(n+1)/2$ entries of $\Sigma$ (a [Sylvester equation](/sylvester-equation/) with a symmetric right side).
7. **Back to counts.** The mean count is $\Omega \phi$ and the covariance of the counts is $\Omega \Sigma$. Working in counts with $\Omega = 1$ gives the same numbers directly.

The time correlation at stationarity is $\operatorname{Cov}(\xi(t + s), \xi(t)) = e^{Js} \Sigma$, and the power spectrum is $(J + i\omega I)^{-1} D (J^{\mathsf T} - i\omega I)^{-1}$.

## Classic examples

**Immigration-death.** $\emptyset \to X$ at rate $k$ and $X \to \emptyset$ at rate $\gamma$ per molecule. In counts, $\dot\phi = k - \gamma\phi$, so $\phi^* = k/\gamma$. Then $J = -\gamma$ and $D = k + \gamma\phi^* = 2k$, and $-2\gamma \Sigma + 2k = 0$ gives $\Sigma = k/\gamma$. The variance equals the mean, the Fano factor is 1, as for the exact [Poisson](/poisson-distribution/)$(k/\gamma)$ law. For networks of reactions of order 0 and 1, the LNA mean and covariance are exact, because the moment equations of the master equation are then closed and linear.

**Two-stage gene expression.** mRNA $M$ is made at rate $k_m$ and decays at rate $\gamma_m$ per molecule; each mRNA makes protein $P$ at rate $k_p$, and protein decays at rate $\gamma_p$. The steady state is $m^* = k_m/\gamma_m$ and $p^* = k_p m^*/\gamma_p$. With $J = \begin{pmatrix} -\gamma_m & 0 \\ k_p & -\gamma_p \end{pmatrix}$ and $D = \operatorname{diag}(2 k_m, 2 k_p m^*)$, the Lyapunov equation gives the protein Fano factor

$$\frac{\Sigma_{PP}}{p^*} = 1 + \frac{k_p}{\gamma_m + \gamma_p}.$$

With $k_m = 2$, $\gamma_m = 1$, $k_p = 10$ and $\gamma_p = 0.1$, the mean protein count is 200, the variance is 2018.18, and the Fano factor is 10.09: proteins made in bursts from each mRNA are ten times noisier than a Poisson count. This is the result of Thattai and van Oudenaarden (2001), and it is exact because the network is linear.

**A nonlinear network.** $\emptyset \to A$ at rate $k = 10$ and $2A \to \emptyset$ with propensity $c\, x(x - 1)/2$, $c = 1$ (the convention $c = 2k_2/(N_A V)$ for a molar rate constant $k_2$). Each firing of the second reaction removes 2 molecules, so in counts $\dot\phi = k - c\phi^2$ and $\phi^* = \sqrt{k/c} = 3.162278$. Then $J = -2c\phi^*$ and $D = k + 4 \cdot c\phi^{*2}/2 = 3k$, so $\Sigma = 3k/(4c\phi^*) = 2.371708$. The exact stationary law of the master equation has mean 3.295346 and variance 2.436040. The LNA mean is 4 percent low and the variance 3 percent low: with counts near 3 the expansion is at its limit, and the error is of order $\Omega^{-1/2}$ relative to the fluctuations.

**The tails.** For the immigration-death law Poisson$(10)$, the exact $P(X \le 3) = 0.010336$, and the LNA normal law $N(10, 10)$ gives $P(X \le 3.5) = 0.019916$, almost twice as much. The LNA gets the bulk right and the tails wrong, even when its variance is exact.

## Variations

- **Time-dependent solutions.** Solve the rate equations and the ODE for $\Sigma$ together. This gives the LNA along a transient, and it is the basis of LNA likelihoods for time series data.
- **Higher orders.** The next terms of the expansion give corrections of order $\Omega^{-1/2}$ to the mean and of order $\Omega^{-1}$ to the variance. The first correction to the mean gives effective rate equations that move the mean of nonlinear networks closer to the exact value.
- **The LNA of the Langevin equation.** Linearizing the [chemical Langevin equation](/chemical-langevin-equation/) around the deterministic path gives the same $J$, $D$ and $\Sigma$. So the LNA is also the small noise limit of the CLE.
- **Conservation laws.** If $S$ has dependent rows (a total amount is conserved), $J$ is singular. Remove the dependent species with the conservation law, and apply the template to the reduced system.
- **Comparison with moment closure.** [Moment closure](/moment-closure/) with a normal closure keeps the nonlinear coupling of the mean and the variance, and often gives better means for nonlinear networks, at the risk of unphysical solutions. The LNA is always well defined near a stable steady state.

## Pitfalls

- **Bistable networks.** Around each stable state the LNA gives a Gaussian, but it says nothing about the switching between states, and a single LNA around one state can miss most of the probability mass. Use [finite state projection](/finite-state-projection/) or simulation.
- **Small counts.** With counts of a few molecules, the Gaussian puts mass on negative counts and the errors in the mean and the variance are large. The nonlinear example above is already at 4 percent with counts near 3.
- **The mean is the rate equation.** The LNA mean is the deterministic solution, with no correction. For nonlinear networks the exact mean differs, and the LNA cannot show it.
- **The factor for dimerization.** In counts, a reaction $2A \to \emptyset$ with propensity $c\, x(x-1)/2$ removes 2 molecules per firing, so it enters the drift as $-2 \cdot c\phi^2/2$ and the diffusion as $4 \cdot c\phi^2/2$. A wrong convention for $c$ changes the steady state.
- **Unstable or oscillating solutions.** Near a Hopf bifurcation or on a limit cycle, $\Sigma$ grows without bound along the cycle, and the LNA fails. Other expansions are needed for oscillators.
- **Tails.** Do not use the Gaussian to estimate small probabilities, such as the chance that a protein count drops below a threshold.

## Exercises

1. For immigration-death, solve $\dot\Sigma = -2\gamma\Sigma + k + \gamma\phi(t)$ from $\Sigma(0) = 0$ and $\phi(0) = 0$, and show that $\Sigma(t) = \phi(t)$ for all $t$, as for the exact Poisson law.
2. Derive the protein Fano factor $1 + k_p/(\gamma_m + \gamma_p)$ of the two-stage model by solving the three equations of the Lyapunov equation for $\Sigma_{MM}$, $\Sigma_{MP}$ and $\Sigma_{PP}$.
3. For $A \rightleftharpoons B$ with rates $k_1 x_A$ and $k_2 x_B$ and a total of $N$ molecules, show that the full $J$ is singular, reduce to one species, and show that the LNA variance is $N k_1 k_2/(k_1 + k_2)^2$, the variance of the exact binomial law.
4. In the nonlinear example, find the LNA variance for $k = 1000$ and $c = 1$, and explain why the relative error of the LNA should shrink as $k$ grows.
5. Show that the stationary covariance of a stable linear network does not depend on how the noise matrix $B$ with $BB^{\mathsf T} = D$ is chosen.

## References
