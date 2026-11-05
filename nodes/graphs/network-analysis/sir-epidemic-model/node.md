---
tag: A9PY9C
kind: model
slug: sir-epidemic-model
name: SIR epidemic model
aliases:
- susceptible-infected-recovered
area: graphs/network-analysis
level: advanced
summary: Compartment model where nodes move from susceptible to infected to recovered.
prereqs: [epidemic-model, percolation, configuration-model]
see_also: [epidemic-model, epidemic-threshold, percolation, scale-free-network, configuration-model, giant-component, erdos-renyi-model, small-world-network]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: W. O. Kermack and A. G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London A 115(772), 700 to 721 (1927)
    locator: the compartment equations for a well-mixed population, the threshold, and the final size relation
  - paper: doi:10.1103/PhysRevE.66.016128
    title: M. E. J. Newman, Spread of epidemic disease on networks, Physical Review E 66(1), 016128 (2002)
    locator: the mapping of the SIR model on a network to bond percolation with transmissibility T, and the outbreak size and threshold for random graphs with a given degree distribution
  - paper: doi:10.1103/PhysRevLett.86.3200
    title: Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic spreading in scale-free networks, Physical Review Letters 86(14), 3200 to 3203 (2001)
    locator: the vanishing of the epidemic threshold on networks with power-law degrees when the second moment of the degree diverges
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 17, Epidemics on networks (the SIR model, its relation to percolation, and the threshold on random graphs)
  - book: isbn:9780521195331
    title: David Easley and Jon Kleinberg, Networks, Crowds, and Markets, Cambridge University Press, 2010
    locator: Chapter 21, Epidemics (the branching process, the SIR model on a network, and its relation to percolation)
---

The SIR model describes an infection in which each individual is *susceptible* (S), then possibly *infected* (I) and able to infect others, and finally *recovered* (R), immune or removed for good. In the original form of Kermack and McKendrick (1927) everyone can meet everyone, and the model is a system of three differential equations; on a network, infection passes only along edges, so the structure of the network decides whether an outbreak becomes an epidemic. The central result is that the final outcome of SIR on a network is a [percolation](/percolation/) problem, and that the [epidemic threshold](/epidemic-threshold/) depends on the ratio of the first two moments of the degrees, which vanishes in [scale-free networks](/scale-free-network/).

## The machine

**State.** A graph $G = (V, E)$, undirected unless stated otherwise, and a state $x_v \in \{S, I, R\}$ for each vertex. At the start, a few *seed* vertices are in state $I$ and all others are in $S$.

**Continuous-time dynamics.** Each infected vertex $u$ infects each susceptible neighbour $v$ at rate $\beta$, independently over edges, and recovers at rate $\gamma$, so its infectious period is exponential with mean $1/\gamma$. Infection moves $v$ from $S$ to $I$; recovery moves $u$ from $I$ to $R$, after which $u$ takes no further part. A weighted network gives each edge its own rate $\beta_{uv}$; on a directed network, infection passes only from the tail of an arc to its head.

**Discrete-time dynamics.** At each step, each infected vertex tries once to infect each susceptible neighbour, succeeding with probability $T$ independently, and then recovers. This is the Reed-Frost chain on a network. Several infected neighbours of $v$ make independent attempts at the same step.

**Mass action.** In a population of $n$ in which every pair is in contact, with fractions $s$, $i$ and $r$,

$$\frac{ds}{dt} = -\beta s i, \qquad \frac{di}{dt} = \beta s i - \gamma i, \qquad \frac{dr}{dt} = \gamma i,$$

with the time scaled so that $\beta$ is the rate of infectious contacts per person.

**Randomness and termination.** The network models are random processes: one run is one possible epidemic. Every run ends, because each vertex is infected at most once and recovers, and the number of infected vertices is 0 at the end. An epidemic never leaves the connected components (in a directed graph, the out-components) of the seeds, so on a disconnected graph the other components stay susceptible.

## What it counts

- **The final size** $r_\infty$: the fraction of vertices that were ever infected, the main output.
- **The probability of a large outbreak**: the chance that a single random seed starts an epidemic that reaches a positive fraction of the network, as opposed to dying out after a few cases.
- **The basic reproduction number** $R_0$: the expected number of vertices infected by a typical infected vertex early on, when almost all others are susceptible. An outbreak can be large only when $R_0 > 1$.
- **The threshold**: the value of the transmission parameter at which $R_0 = 1$.
- **The time course**: the peak number of infected vertices and the time to reach it, which depend on the dynamics, not only on the final-size structure.

## Relation to other models

- **[Percolation](/percolation/).** In the discrete-time model, each edge is used at most once, when one end is infected and the other susceptible, and it transmits with probability $T$ independently of the others. Flip all these coins in advance: the set of vertices ever infected is exactly the cluster of the seeds in bond percolation with occupation probability $T$. In continuous time with infectious periods $\tau_u$, an infected $u$ infects a neighbour with probability $1 - e^{-\beta \tau_u}$, and averaging gives the *transmissibility* $T = \beta/(\beta + \gamma)$ for exponential periods. The mapping is exact for a fixed infectious period; for variable periods the attempts of one vertex are correlated, and on random graphs the mapping still gives the threshold and the size of a large outbreak, but not the probability that one occurs.
- **SIS.** Recovered vertices return to $S$ instead of $R$, so an infection can persist forever; its threshold on scale-free networks also vanishes, but its analysis is not a percolation problem.
- **SI and SEIR.** SI has no recovery; SEIR adds an exposed state $E$ between $S$ and $I$, which delays the epidemic but does not change its final size.
- **Branching processes.** Early on, when few vertices are infected, the epidemic is close to a Galton-Watson branching process, whose extinction probability gives the chance of a small outbreak.
- **Other spreading models.** The [epidemic model](/epidemic-model/) family, rumour models, and the independent cascade model of influence maximization, which is the discrete-time SIR model with a probability for each edge.

## Known results in the model

**Mass action.** Kermack and McKendrick showed that the infection grows when $R_0 = \beta/\gamma > 1$ and that the final size satisfies

$$r_\infty = 1 - e^{-R_0\, r_\infty}$$

when almost everyone starts susceptible. For $R_0 = 2$ the positive root is $r_\infty \approx 0.797$: about 80 percent are infected, and 20 percent escape even without any intervention.

**Networks with given degrees.** On the [configuration model](/configuration-model/) with mean degree $\langle k \rangle$ and second moment $\langle k^2 \rangle$, a vertex infected along an edge has, on average, $\langle k^2 \rangle / \langle k \rangle - 1$ further neighbours, so

$$R_0 = T\, \frac{\langle k^2 \rangle - \langle k \rangle}{\langle k \rangle}, \qquad T_c = \frac{\langle k \rangle}{\langle k^2 \rangle - \langle k \rangle},$$

which is the bond [percolation](/percolation/) threshold. Above $T_c$, the final size of a large outbreak is the size of the giant cluster of bond percolation with probability $T$, and with a fixed infectious period the probability of a large outbreak from a random seed is the same number.

**The Erdős-Rényi graph.** With mean degree $c$, $R_0 = cT$, and the final size and the outbreak probability both solve $S = 1 - e^{-cTS}$, the same equation as mass action with $R_0 = cT$.

**Scale-free networks.** When $\langle k^2 \rangle$ diverges, as for degrees with a power law of exponent $\gamma \le 3$, $T_c \to 0$ as $n \to \infty$: every infection that can pass along an edge with positive probability can cause a large epidemic (Pastor-Satorras and Vespignani). Immunizing random vertices then barely helps, while immunizing the hubs, or the friends of random vertices, which are likely to be hubs, raises the threshold.

**An exact small case.** On a triangle with one seed and the discrete-time model with $T = 1/2$, the final size is 1 with probability $(1 - T)^2 = 1/4$, 2 with probability $2T(1 - T)^2 = 1/4$, and 3 with probability $T^2(3 - 2T) = 1/2$. Enumerating the coin flips of the dynamics and the clusters of bond percolation on the triangle gives the same distribution.

**A simulation.** On one Erdős-Rényi graph with $n = 50000$ and $c = 4$, the discrete-time model with $T = 0.5$ gives $R_0 = 2$ and predicts $S \approx 0.797$. Of 200 runs from a random seed, 79 percent became large, with a mean final size of $0.797$ of the network, and lasted about 27 steps on average; the rest died out after a few cases.

## References
