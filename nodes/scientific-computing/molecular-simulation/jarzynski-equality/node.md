---
tag: 5BZCTG
kind: theorem
slug: jarzynski-equality
name: Jarzynski equality
aliases:
- Jarzynski relation
area: scientific-computing/molecular-simulation
level: advanced
summary: "The average of exp(-W/kT) over nonequilibrium processes that drive a system from state A to B equals exp(-dF/kT), linking work and free energy."
prereqs: [canonical-ensemble, free-energy-perturbation, jensens-inequality, markov-chain]
see_also: [thermodynamic-integration, bennett-acceptance-ratio, annealed-importance-sampling, importance-sampling, hamiltonian-systems, detailed-balance, effective-sample-size, umbrella-sampling]
sources:
  - paper: doi:10.1103/PhysRevLett.78.2690
    title: Christopher Jarzynski, Nonequilibrium equality for free energy differences, Physical Review Letters 78, 1997, 2690-2693
    locator: the equality for a system that starts in equilibrium and is driven by a time-dependent parameter, with the Hamiltonian derivation
  - paper: doi:10.1023/A:1023208217925
    title: Gavin E. Crooks, Nonequilibrium measurements of free energy differences for microscopically reversible Markovian systems, Journal of Statistical Physics 90, 1998, 1481-1487
    locator: the proof of the equality for Markov dynamics in which each step keeps the canonical distribution of the current parameter
  - paper: doi:10.1103/PhysRevE.60.2721
    title: Gavin E. Crooks, Entropy production fluctuation theorem and the nonequilibrium work relation for free energy differences, Physical Review E 60, 1999, 2721-2726
    locator: the fluctuation theorem relating the forward and reverse work distributions, from which the equality follows
  - paper: doi:10.1103/PhysRevE.73.046105
    title: Christopher Jarzynski, Rare events and the convergence of exponentially averaged work values, Physical Review E 73, 046105, 2006
    locator: the estimate that the number of trajectories needed grows exponentially with the dissipated work
  - paper: doi:10.1126/science.1071152
    title: Jan Liphardt, Sophie Dumont, Steven B. Smith, Ignacio Tinoco Jr. and Carlos Bustamante, Equilibrium information from nonequilibrium measurements in an experimental test of Jarzynski's equality, Science 296(5574), 2002, 1832-1835
    locator: the test of the equality by mechanically unfolding single RNA molecules with optical tweezers
  - book: isbn:9781848162471
    title: Tony Lelièvre, Mathias Rousset and Gabriel Stoltz, Free Energy Computations, A Mathematical Perspective, Imperial College Press, 2010
    locator: the chapter on nonequilibrium methods and the Jarzynski-Crooks identities
---

## Statement

**Setting.** A system has states $z$ in a space $\Gamma$ with a reference measure $dz$ (phase space volume, or counting measure for a discrete system), and an energy $H_\lambda(z)$ that depends on a control parameter $\lambda$. For each $\lambda$ the partition function $Z_\lambda = \int e^{-\beta H_\lambda(z)}\,dz$ is finite and positive, the [canonical](/canonical-ensemble/) density is $\pi_\lambda = e^{-\beta H_\lambda} / Z_\lambda$, and the free energy is $F_\lambda = -\beta^{-1} \ln Z_\lambda$, with $\beta = 1/(k_B T)$.

A *protocol* is a sequence $\lambda_0, \lambda_1, \dots, \lambda_n$. The process starts with $z_0 \sim \pi_{\lambda_0}$. For $i = 1, \dots, n$ it first switches the parameter from $\lambda_{i-1}$ to $\lambda_i$ at the fixed state $z_{i-1}$, which costs the work $H_{\lambda_i}(z_{i-1}) - H_{\lambda_{i-1}}(z_{i-1})$, and then moves the state by a Markov kernel, $z_i \sim K_i(z_{i-1}, \cdot)$, that keeps $\pi_{\lambda_i}$ invariant: $\int \pi_{\lambda_i}(z) K_i(z, dz') = \pi_{\lambda_i}(z')\,dz'$. The total work is
$$W = \sum_{i=1}^{n} \bigl(H_{\lambda_i}(z_{i-1}) - H_{\lambda_{i-1}}(z_{i-1})\bigr).$$
The kernels need not satisfy detailed balance, and the system need not be anywhere near equilibrium during the process.

**Theorem (Jarzynski 1997; Crooks 1998).** For every protocol and every such choice of kernels,
$$\bigl\langle e^{-\beta W} \bigr\rangle = e^{-\beta (F_{\lambda_n} - F_{\lambda_0})},$$
where the average is over the process.

**Theorem (the Hamiltonian case).** Let $\Gamma = \mathbb R^{2d}$ with Lebesgue measure, let $\lambda(t)$, $0 \le t \le \tau$, be continuously differentiable, and let $z(t)$ follow Hamilton's equations for $H_{\lambda(t)}$ from $z(0) \sim \pi_{\lambda(0)}$, with a flow map $\Phi$ from $z(0)$ to $z(\tau)$ that is defined everywhere. The work is $W = \int_0^\tau \dot\lambda\, \partial_\lambda H_{\lambda(t)}(z(t))\,dt = H_{\lambda(\tau)}(z(\tau)) - H_{\lambda(0)}(z(0))$. Then $\langle e^{-\beta W} \rangle = e^{-\beta (F_{\lambda(\tau)} - F_{\lambda(0)})}$.

The free energy difference $\Delta F$ is an equilibrium quantity, yet the left side is an average over processes of any speed. A process of zero steps after one instantaneous switch is [free energy perturbation](/free-energy-perturbation/); an infinitely slow process gives [thermodynamic integration](/thermodynamic-integration/) (Consequence 3).

## In plain words

Pull on a molecule, for example by stretching it with a spring, and measure the work you do. If you pull slowly, the work equals the change in free energy. If you pull fast, you waste energy as heat, and the work is larger on average.

The Jarzynski equality says that a special kind of average of the work still gives the exact free energy change, however fast you pull. You must start from equilibrium, repeat the pull many times, and average a quantity that weights each pull by how small its work was. The rare pulls that took little work matter most.

The catch is that, for fast pulls, these lucky pulls are so rare that you need very many repeats.

## Proof

**The Markov case.** Write $\pi_i$, $H_i$, $Z_i$ for $\pi_{\lambda_i}$, $H_{\lambda_i}$, $Z_{\lambda_i}$. For $k = 0, \dots, n$ let $W_k = \sum_{i=1}^{k} (H_i - H_{i-1})(z_{i-1})$ be the work of the first $k$ switches, and define the measure $\mu_k$ on $\Gamma$ by
$$\mu_k(A) = E\bigl[e^{-\beta W_k}\, \mathbf 1\{z_k \in A\}\bigr].$$
We show by induction that $\mu_k(dz) = (Z_k / Z_0)\, \pi_k(z)\,dz$, that is $\mu_k(dz) = e^{-\beta H_k(z)}\,dz / Z_0$.

For $k = 0$, $W_0 = 0$ and $z_0 \sim \pi_0$, so $\mu_0(dz) = \pi_0(z)\,dz = e^{-\beta H_0(z)}\,dz / Z_0$.

Assume the claim for $k - 1$. The pair $(W_{k-1}, z_{k-1})$ is a function of $z_0, \dots, z_{k-1}$, and given these, $z_k \sim K_k(z_{k-1}, \cdot)$ by the Markov property. With $W_k = W_{k-1} + (H_k - H_{k-1})(z_{k-1})$,
$$\mu_k(A) = E\Bigl[e^{-\beta W_{k-1}}\, e^{-\beta (H_k - H_{k-1})(z_{k-1})}\, K_k(z_{k-1}, A)\Bigr] = \int e^{-\beta (H_k - H_{k-1})(z)}\, K_k(z, A)\, \mu_{k-1}(dz).$$
By the induction hypothesis, $\mu_{k-1}(dz) = e^{-\beta H_{k-1}(z)}\,dz / Z_0$, so
$$\mu_k(A) = \frac{1}{Z_0} \int e^{-\beta H_k(z)}\, K_k(z, A)\,dz = \frac{Z_k}{Z_0} \int \pi_k(z)\, K_k(z, A)\,dz = \frac{Z_k}{Z_0} \int_A \pi_k(z')\,dz',$$
where the last step is the invariance of $\pi_k$ under $K_k$. This is the claim for $k$. All integrands are nonnegative, so the exchanges of expectation and integral are justified by Tonelli's theorem.

At $k = n$, $\langle e^{-\beta W} \rangle = \mu_n(\Gamma) = Z_n / Z_0 = e^{-\beta (F_{\lambda_n} - F_{\lambda_0})}$. $\square$

**The Hamiltonian case.** Along a solution of Hamilton's equations for $H_{\lambda(t)}$, $\frac{d}{dt} H_{\lambda(t)}(z(t)) = \dot\lambda\, \partial_\lambda H + \nabla_z H \cdot \dot z = \dot\lambda\, \partial_\lambda H$, because $\nabla_z H \cdot J \nabla_z H = 0$ for the antisymmetric matrix $J$ of Hamilton's equations. Integrating gives the two forms of $W$. Then
$$\langle e^{-\beta W} \rangle = \int \frac{e^{-\beta H_{\lambda(0)}(z_0)}}{Z_{\lambda(0)}}\, e^{-\beta (H_{\lambda(\tau)}(\Phi(z_0)) - H_{\lambda(0)}(z_0))}\,dz_0 = \frac{1}{Z_{\lambda(0)}} \int e^{-\beta H_{\lambda(\tau)}(\Phi(z_0))}\,dz_0.$$
The flow of a time-dependent Hamiltonian vector field has divergence 0, so by Liouville's theorem on phase space volume $\Phi$ is a bijection that preserves Lebesgue measure. The change of variables $z = \Phi(z_0)$ turns the last integral into $\int e^{-\beta H_{\lambda(\tau)}(z)}\,dz = Z_{\lambda(\tau)}$. $\square$

**Example 1 (an instantaneous switch of a spring).** Take $H_\lambda(x) = k_\lambda x^2 / 2$ on $\mathbb R$ with $k_0 = 1$, $k_1 = 2$, $\beta = 1$, and one switch with no kernel step. Then $x \sim N(0, 1)$ and $W = x^2 / 2$, so $\langle e^{-W} \rangle = E[e^{-x^2 / 2}] = 1/\sqrt 2$, and $\Delta F = \frac12 \ln 2 = 0.3466$, which is $-\ln(Z_1 / Z_0)$ with $Z_k = \sqrt{2\pi / k}$. The mean work is $\langle W \rangle = 0.5 > \Delta F$.

**Example 2 (a two-level system).** Two states with energies $0$ and $\epsilon_\lambda$, where $\epsilon$ is switched at once from 0 to $\epsilon$. At the start both states have probability $\frac12$, the work is $\epsilon$ in the upper state and 0 in the lower one, and $\langle e^{-\beta W} \rangle = \frac12 (1 + e^{-\beta \epsilon}) = Z_1 / Z_0$ with $Z_0 = 2$ and $Z_1 = 1 + e^{-\beta \epsilon}$.

**Example 3 (finite speed).** For the spring of Example 1, switch $k$ from 1 to 2 in $n$ equal steps, each followed by one Metropolis step for the new $k$ with proposals uniform on $[-1, 1]$ (seed 7):

| $n$ | trajectories | $\langle W \rangle$ | standard deviation of $W$ | $-\ln \langle e^{-W} \rangle$ | fraction with $W < \Delta F$ |
|---|---|---|---|---|---|
| 1 | 20000 | 0.5048 | 0.708 | 0.3499 | 0.591 |
| 10 | 20000 | 0.4235 | 0.475 | 0.3475 | 0.611 |
| 100 | 5000 | 0.3582 | 0.152 | 0.3476 | 0.567 |

The mean work falls towards $\Delta F = 0.3466$ as the process slows down, and the exponential average gives $\Delta F$ within about 0.003 at every speed.

## Consequences

**1. The second law for the mean work.** By [Jensen's inequality](/jensens-inequality/) for the convex function $e^{-\beta w}$, $e^{-\beta \langle W \rangle} \le \langle e^{-\beta W} \rangle = e^{-\beta \Delta F}$, so $\langle W \rangle \ge \Delta F$, with equality only if $W$ is constant with probability 1. The difference $\langle W \rangle - \Delta F$ is the mean dissipated work.

**2. Rare violations.** For every $\xi > 0$, $P(W \le \Delta F - \xi) \le e^{-\beta \xi}$. *Proof.* By Markov's inequality, $P(e^{-\beta W} \ge e^{-\beta (\Delta F - \xi)}) \le \langle e^{-\beta W} \rangle\, e^{\beta (\Delta F - \xi)} = e^{-\beta \xi}$. Single trajectories with $W < \Delta F$ are common; in Example 3 more than half of them have it. Only large violations are rare.

**3. The two limits.** With $n = 1$ and no kernel step, $W = H_1(z_0) - H_0(z_0)$ and the theorem is Zwanzig's identity of free energy perturbation. At the other extreme, let $\lambda_i = i / n$ on a path with $\sup |\partial_\lambda H|$ and $\sup |\partial^2_\lambda H|$ bounded, and let each kernel draw a fresh sample, $K_i(z, \cdot) = \pi_{\lambda_i}$. Then the terms of $W$ are independent, each with mean $\langle H_i - H_{i-1} \rangle_{i-1} = \frac1n \langle \partial_\lambda H \rangle_{\lambda_{i-1}} + O(n^{-2})$ and variance $O(n^{-2})$. So $E[W] \to \int_0^1 \langle \partial_\lambda H \rangle_\lambda\, d\lambda$, the Riemann sum converging because the integrand is continuous by dominated convergence, and $\mathrm{var}(W) = O(1/n)$. The limit is Kirkwood's formula of thermodynamic integration, and $W \to \Delta F$ in mean square.

**4. Gaussian work.** If $W$ is normal with mean $m$ and variance $s^2$, the moment generating function gives $\langle e^{-\beta W} \rangle = e^{-\beta m + \beta^2 s^2 / 2}$, so $\Delta F = m - \beta s^2 / 2$. For near-equilibrium processes this is a useful estimate; in Example 3 it gives 0.254, 0.311 and 0.347 for $n = 1, 10, 100$, good only for the slowest process, where the work is close to normal.

**5. Crooks' theorem and BAR.** For dynamics that are reversible in a suitable sense, Crooks (1999) proved that the forward and reverse work densities satisfy $P_F(W) / P_R(-W) = e^{\beta (W - \Delta F)}$; integrating over $W$ gives the equality. With work from both directions, the [Bennett acceptance ratio](/bennett-acceptance-ratio/) equation gives the estimate of least variance.

**6. Annealed importance sampling.** In statistics the Markov case is the identity behind [annealed importance sampling](/annealed-importance-sampling/) (Neal 2001), with $e^{-\beta W}$ as the importance weight of a path.

## Tightness

**The start must be canonical.** In Example 2, start in the lower state with probability 1. Then $W = 0$ always and $\langle e^{-\beta W} \rangle = 1 \ne \frac12 (1 + e^{-\beta \epsilon})$. The proof uses $z_0 \sim \pi_{\lambda_0}$ in its first step, and it does not hold for other starts. The end state need not be in equilibrium.

**Each kernel must keep the current canonical density.** In Example 2, switch $\epsilon$ from 0 up to $\epsilon$, then apply a kernel, then switch back down to 0, so $\Delta F = 0$. The second switch costs $-\epsilon$ in the upper state. With the identity kernel, which keeps every density, $W = 0$ always and the average is 1, as it should be. With a kernel that always moves the system to the lower state, which does not keep $\pi_{\lambda_1}$, $W = \epsilon$ in the upper start and 0 in the lower one, and the average is $\frac12 (1 + e^{-\beta\epsilon}) \ne 1$.

**The equality is exact, the estimator is not.** The sample mean of $e^{-\beta W}$ over $N$ trajectories is unbiased, but its logarithm is biased upward for $\Delta F$ by Jensen's inequality, and its variance can be huge. The average is dominated by rare trajectories with small work, and Jarzynski (2006) estimates that the number of trajectories needed grows like $e^{\beta W_{\text{dis}}}$ with the typical dissipated work $W_{\text{dis}} = \langle W \rangle - \Delta F$. For the spring of Example 1 switched from $k = 2$ down to $k = 1$, $W = -x^2/2$ with $x \sim N(0, \frac12)$, and $\langle e^{-2\beta W} \rangle = E[e^{x^2}] = \infty$: the equality holds, but the estimator has infinite variance.

**The work must be the work done by the protocol.** For a system coupled to a heat bath, $W$ is the energy change caused by changing $\lambda$, not the total change of energy, which also contains heat. In the Markov case this is the split into switches (work) and kernel steps (heat).

## History

Jarzynski (1997) found the equality and proved it for Hamiltonian dynamics and for a system coupled to a heat bath. Crooks (1998) proved it for Markov dynamics that keep the current canonical density, as in the proof above, and in 1999 derived his fluctuation theorem for the work distributions. Liphardt, Dumont, Smith, Tinoco and Bustamante (2002) tested it by unfolding single RNA molecules with optical tweezers and recovered the equilibrium free energy from irreversible pulls. Jarzynski (2006) analysed why the exponential average converges slowly. The same identity appeared in statistics as annealed importance sampling.

## References
