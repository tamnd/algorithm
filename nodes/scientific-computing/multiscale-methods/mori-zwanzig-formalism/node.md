---
tag: 6VYJDV
kind: theorem
slug: mori-zwanzig-formalism
name: Mori-Zwanzig formalism
aliases:
- generalized Langevin equation
area: scientific-computing/multiscale-methods
level: advanced
summary: Projects a large dynamical system onto resolved variables exactly, giving a Markov term, a memory integral and a noise term.
prereqs: [conditional-expectation, langevin-dynamics]
see_also: [green-kubo-relations, force-matching-coarse-graining, iterative-boltzmann-inversion, dissipative-particle-dynamics, brownian-dynamics, collective-variable, autocorrelation, laplace-transform]
sources:
  - paper: doi:10.1103/PhysRev.124.983
    title: Robert Zwanzig, Memory effects in irreversible thermodynamics, Physical Review 124(4), 1961, 983-992
    locator: the projection operator and the exact equation with a memory term for the projected part of the distribution
  - paper: doi:10.1143/PTP.33.423
    title: Hazime Mori, Transport, collective motion, and Brownian motion, Progress of Theoretical Physics 33(3), 1965, 423-455
    locator: the linear projection onto the resolved variables, the generalized Langevin equation and the relation between the memory kernel and the correlation of the random force
  - paper: doi:10.1073/pnas.97.7.2968
    title: Alexandre J. Chorin, Ole H. Hald and Raz Kupferman, Optimal prediction and the Mori-Zwanzig representation of irreversible processes, Proceedings of the National Academy of Sciences 97(7), 2000, 2968-2973
    locator: the nonlinear form with the conditional expectation as the projection, and optimal prediction as the Markov term
  - paper: doi:10.1016/S0167-2789(02)00446-3
    title: Alexandre J. Chorin, Ole H. Hald and Raz Kupferman, Optimal prediction with memory, Physica D 166(3-4), 2002, 239-257
    locator: approximations of the memory term in numerical reduced models
  - paper: doi:10.1007/BF02786691
    title: Dror Givon, Raz Kupferman and Ole H. Hald, Existence proof for orthogonal dynamics and the Mori-Zwanzig formalism, Israel Journal of Mathematics 145, 2005, 221-241
    locator: the existence of the orthogonal dynamics semigroup, which the exact equation needs
  - paper: doi:10.1088/0951-7715/17/6/R01
    title: "Dror Givon, Raz Kupferman and Andrew Stuart, Extracting macroscopic dynamics: model problems and algorithms, Nonlinearity 17(6), 2004, R55-R127"
    locator: a review of model reduction with and without scale separation, including the Mori-Zwanzig formalism
  - book: isbn:9780195140187
    title: Robert Zwanzig, Nonequilibrium Statistical Mechanics, Oxford University Press, 2001
    locator: Chapter 8, projection operators and the derivation of the generalized Langevin equation
---

The Mori-Zwanzig formalism takes a large deterministic dynamical system, for example all atoms of a liquid, and a few resolved variables, for example the positions of coarse-grained sites or one slow coordinate, and writes an exact equation for the resolved variables alone. The equation has three terms: a Markov term that depends on the resolved variables at the present time, a memory integral over their past, and a noise term that depends on the initial values of the unresolved variables and is orthogonal to the resolved ones. This equation is the generalized Langevin equation. It is an identity, not an approximation: no information is lost, but the noise and the memory are as hard to compute as the full system. All practical reduced models, such as the [Langevin equation](/langevin-dynamics/), [Brownian dynamics](/brownian-dynamics/), [dissipative particle dynamics](/dissipative-particle-dynamics/) and coarse-grained force fields from [force matching](/force-matching-coarse-graining/), come from approximations of the memory and the noise.

## Statement

**Setting.** Let $\dot z = R(z)$ be a dynamical system on a phase space $\Gamma$ with the flow $\varphi_t$, and let $\mu$ be a probability measure on $\Gamma$, the distribution of the initial states. Observables are functions $g$ on $\Gamma$ in the Hilbert space $H = L^2(\mu)$ with the inner product $\langle f, g \rangle = \int f g\, d\mu$. The Liouville operator is $L g = R \cdot \nabla g$, and $e^{tL} g = g \circ \varphi_t$ is the observable $g$ evaluated along the solution, so $\frac{d}{dt} e^{tL} g = e^{tL} L g$. The resolved variables are observables $u_1, \dots, u_m$, and $u_j(t) = e^{tL} u_j$.

**Projection.** Let $P$ be an orthogonal projection in $H$ whose range contains $u_1, \dots, u_m$, and $Q = I - P$. The two standard choices are:
- Mori's linear projection onto the span of $u_1, \dots, u_m$: $P g = \sum_{k, l} \langle g, u_k \rangle (C^{-1})_{k l}\, u_l$ with the matrix $C_{k l} = \langle u_k, u_l \rangle$, assumed invertible.
- The conditional expectation $P g = \mathbb{E}_\mu[g \mid u]$, the projection onto all functions of $u$ in $H$ (Zwanzig; Chorin, Hald and Kupferman).

**Hypothesis (orthogonal dynamics).** The operators $e^{tL}$ and $e^{tQL}$ are defined on $H$, and $s \mapsto e^{(t-s)L} e^{sQL} g$ is differentiable with the product rule for the observables $g$ used below. This holds when $L$ is bounded on $H$, in particular when the observables stay in a finite dimensional subspace that $L$ maps into itself, as in the example below. For unbounded $L$, the existence of the orthogonal dynamics $e^{tQL}$ is a theorem of Givon, Kupferman and Hald (2005) for a broad class of systems and projections.

**Theorem (Dyson identity).** For $t \ge 0$,
$$e^{tL} = e^{tQL} + \int_0^t e^{(t - s) L}\, P L\, e^{s Q L}\, ds .$$

**Theorem (the generalized Langevin equation).** Let $F_j(t) = e^{tQL} Q L u_j$, the noise. Then for every $j$ and $t \ge 0$, as an identity of functions on $\Gamma$ (so for every initial state),
$$\frac{d u_j(t)}{dt} = \underbrace{e^{tL} P L u_j}_{\text{Markov}} + \underbrace{\int_0^t e^{(t-s) L}\, P L F_j(s)\, ds}_{\text{memory}} + \underbrace{F_j(t)}_{\text{noise}},$$
and $P F_j(t) = 0$ for all $t$. With the conditional expectation, $P L u_j$ and $P L F_j(s)$ are functions of $u$, so the Markov term is a function of $u(t)$ and the memory term is $\int_0^t K_j(u(t - s), s)\, ds$ for some functions $K_j$.

**Theorem (Mori's form and the second fluctuation-dissipation relation).** With Mori's projection, write $u$ for the column of the $u_j$. Then
$$\frac{d u(t)}{dt} = \Omega\, u(t) - \int_0^t K(s)\, u(t - s)\, ds + F(t), \qquad \langle F_j(t), u_k \rangle = 0,$$
with $\Omega_{j l} = \sum_k \langle L u_j, u_k \rangle (C^{-1})_{k l}$ and $K_{j l}(s) = -\sum_k \langle L F_j(s), u_k \rangle (C^{-1})_{k l}$. If moreover $\mu$ is invariant and $L$ is skew-adjoint on $H$ (the flow preserves $\mu$, as a Hamiltonian flow preserves the canonical distribution), then
$$K_{j l}(s) = \sum_k \langle F_j(s), F_k(0) \rangle (C^{-1})_{k l} .$$
The memory kernel is the autocorrelation of the noise.

## In plain words

Suppose you watch only a few numbers of a huge system, such as the position of one large molecule in a liquid, and you want a rule for how they change. The rule cannot be a simple law of the present values alone, because the molecules you do not watch carry information from the past.

The formalism shows that the rule has three parts, and that together they are exact. The first part is the average push that the present state gives. The second part is a memory: the past values of the watched numbers still act through the unwatched molecules. The third part looks random, because it depends on where the unwatched molecules started. The exact rule is not cheaper than the full system. Its value is that it shows what you throw away when you simplify it, and how the memory and the random part are linked.

## Proof

**Dyson identity.** Fix $t$ and let $G(s) = e^{(t - s) L} e^{s Q L}$ for $0 \le s \le t$. By the product rule,
$$G'(s) = -e^{(t-s) L} L\, e^{s Q L} + e^{(t-s) L} Q L\, e^{s Q L} = -e^{(t-s) L} P L\, e^{s Q L},$$
since $L - QL = PL$. Integrating from $0$ to $t$ gives $G(t) - G(0) = e^{tQL} - e^{tL} = -\int_0^t e^{(t-s) L} P L e^{s Q L}\, ds$, which is the identity. $\square$

**The generalized Langevin equation.** Write $\frac{d}{dt} e^{tL} u_j = e^{tL} L u_j = e^{tL} P L u_j + e^{tL} Q L u_j$. Apply the Dyson identity to $Q L u_j$:
$$e^{tL} Q L u_j = e^{tQL} Q L u_j + \int_0^t e^{(t-s) L} P L\, e^{sQL} Q L u_j\, ds = F_j(t) + \int_0^t e^{(t-s) L} P L F_j(s)\, ds .$$
This gives the equation. For the noise, $F_j(0) = Q L u_j$ is in the range of $Q$, and $\frac{d}{dt} P F_j(t) = P Q L F_j(t) = 0$ because $P Q = 0$. So $P F_j(t) = P F_j(0) = 0$. With the conditional expectation, $P g$ is a function of $u$ for every $g$, and $e^{tL} f(u) = f(u(t))$, which gives the forms of the Markov and memory terms. $\square$

**Mori's form.** With Mori's projection, $P g = \sum_{k, l} \langle g, u_k \rangle (C^{-1})_{k l} u_l$ and $e^{\tau L} u_l = u_l(\tau)$. So $e^{tL} P L u_j = \sum_l \Omega_{j l} u_l(t)$ and $e^{(t-s) L} P L F_j(s) = \sum_l \big( \sum_k \langle L F_j(s), u_k \rangle (C^{-1})_{k l} \big) u_l(t - s) = -\sum_l K_{j l}(s) u_l(t - s)$. The relation $\langle F_j(t), u_k \rangle = 0$ is $P F_j(t) = 0$, because $u_k$ is in the range of $P$ and $P$ is orthogonal. If $L$ is skew-adjoint, $\langle L F_j(s), u_k \rangle = -\langle F_j(s), L u_k \rangle = -\langle F_j(s), Q L u_k \rangle - \langle F_j(s), P L u_k \rangle$. The last term is zero, since $F_j(s)$ is orthogonal to the range of $P$, and $Q L u_k = F_k(0)$. So $K_{j l}(s) = \sum_k \langle F_j(s), F_k(0) \rangle (C^{-1})_{k l}$. $\square$

**Example by hand.** Take the linear system $\dot x = a x + b y$, $\dot y = c x + d y$, with $x$ resolved, and a distribution $\mu$ of $(x_0, y_0)$ with finite second moments and $\langle x, y \rangle = 0$. The linear functions form a two-dimensional space that $L$ maps into itself: $L x = a x + b y$ and $L y = c x + d y$. Mori's projection is $P g = \langle g, x \rangle x / \langle x, x \rangle$, so $P x = x$ and $P y = 0$. Then $P L x = a x$ and $Q L x = b y$. On $y$, $Q L y = Q (c x + d y) = d y$, so the orthogonal dynamics is $e^{s Q L} y = e^{d s} y$, and the noise is $F(s) = b e^{d s} y$, which is $b e^{d s} y_0$ as a function of the initial state. The memory integrand is $P L F(s) = b e^{d s} P(c x + d y) = b c\, e^{d s} x$. The generalized Langevin equation is
$$\dot x(t) = a\, x(t) + b c \int_0^t e^{d s}\, x(t - s)\, ds + b\, e^{d t} y_0 .$$
This is what eliminating $y$ by variation of constants gives: $y(t) = e^{d t} y_0 + c \int_0^t e^{d (t - s')} x(s')\, ds'$, put into $\dot x = a x + b y$, with $s = t - s'$.

For the harmonic oscillator, $a = d = 0$, $b = 1$, $c = -1$, the equation is $\dot x(t) = -\int_0^t x(t - s)\, ds + y_0$. With $x_0 = 1$ and $y_0 = 0$, $x(t) = \cos t$, and indeed $-\int_0^t \cos(t - s)\, ds = -\sin t = \dot x(t)$. With the standard Gaussian $\mu$, which the rotation preserves, $L$ is skew-adjoint on the linear functions, and Mori's relation gives $K(s) = \langle F(s), F(0) \rangle / \langle x, x \rangle = \langle y, y \rangle / \langle x, x \rangle = 1$, the same kernel. $\blacksquare$

## Consequences

**The correlation function.** Take the inner product of Mori's equation with $u_k$ at time $0$. Since $\langle F_j(t), u_k \rangle = 0$, the correlation matrix $\Phi(t) = \langle u(t), u^T \rangle$ obeys the closed equation $\dot \Phi(t) = \Omega \Phi(t) - \int_0^t K(s) \Phi(t - s)\, ds$ exactly, and in [Laplace transform](/laplace-transform/) $\hat \Phi(z) = (z I - \Omega + \hat K(z))^{-1} C$. So the memory kernel can be computed from a measured [autocorrelation](/autocorrelation/) function. For the oscillator, $\hat K = 1/z$ and $\hat \Phi = 1 / (z + 1/z) = z / (z^2 + 1)$, the transform of $\cos t$.

The rest are approximations, not consequences of the identity.

**The Markov approximation and the Langevin equation.** If the noise decorrelates much faster than $u$ changes, replace $K(s)$ by $2 \gamma\, \delta(s)$ with the friction $\gamma = \int_0^\infty K(s)\, ds$, a formula of the [Green-Kubo](/green-kubo-relations/) type, and the noise by white noise with the same covariance. This gives the Langevin equation with the fluctuation-dissipation relation. It is a heuristic in general; it is a theorem in limits with a separation of time scales (see Givon, Kupferman and Stuart 2004).

**Optimal prediction and the mean force.** Dropping the memory and the noise leaves $\dot u = \mathbb{E}[L u \mid u]$ with the conditional expectation: the best prediction of the rate of change given the present resolved state (Chorin, Hald and Kupferman 2000). For resolved coordinates and momenta of coarse-grained sites in a canonical system, the Markov term contains the mean force, the gradient of the potential of mean force, which is what [force matching](/force-matching-coarse-graining/) estimates and what [iterative Boltzmann inversion](/iterative-boltzmann-inversion/) targets through the structure.

**Short memory approximations.** Expanding the memory term for short times, or modeling the kernel with a few parameters, gives reduced models that keep part of the memory (Chorin, Hald and Kupferman 2002). Dissipative particle dynamics can be read as a Markov approximation with pairwise friction, which keeps the momentum conservation of the full system.

## Tightness

- **No reduction for free.** The noise $F_j(t)$ depends on the full initial state, and the orthogonal dynamics $e^{tQL}$ is as costly to compute as the full dynamics. The identity is exact because nothing is discarded.
- **The noise is not white, not Gaussian and not independent.** In general, $F_j$ is only orthogonal to the range of $P$. With Mori's projection, it is uncorrelated with $u(0)$ but can depend on it nonlinearly.
- **The Markov approximation can fail completely.** For the oscillator, $K(s) = 1$ for all $s$: the memory never decays, $\int_0^\infty K\, ds$ does not exist, and no Langevin equation describes $x$. A Markov model needs a separation of time scales.
- **The projection and the measure matter.** Different projections give different Markov terms, memories and noises for the same dynamics. The identity holds for every initial state, but the statistical properties of the noise (zero mean, the relation of $K$ to its correlation) hold only on average over the $\mu$ used to define $P$, and the second fluctuation-dissipation relation needs $\mu$ to be invariant and $L$ skew-adjoint.

## History

Zwanzig introduced projection operators in statistical mechanics around 1960, and in 1961 he wrote an exact equation with a memory term for the relevant part of the phase space distribution. Mori introduced in 1965 the linear projection onto the resolved variables and wrote the generalized Langevin equation, with the memory kernel given by the correlation of the random force. Chorin, Hald and Kupferman took the formalism into numerical analysis in 2000 and 2002, with the conditional expectation as the projection and approximations of the memory for reduced models, and Givon, Kupferman and Hald proved the existence of the orthogonal dynamics in 2005.

## References
