---
tag: 4N8FJY
kind: model
slug: heterogeneous-mean-field-epidemic
name: Degree-based mean-field epidemic model
aliases:
- heterogeneous mean-field theory
area: biology/epidemic-and-ecological-models
level: advanced
summary: "Track the infected fraction in each degree class of a network. On scale-free networks with degree exponent at most 3, the epidemic threshold vanishes as size grows."
prereqs: [sis-epidemic-model, degree-distribution, basic-reproduction-number]
see_also: [scale-free-network, configuration-model, epidemic-threshold, sir-epidemic-model, mean-field-approximation, percolation, next-generation-matrix, herd-immunity-threshold]
sources:
  - paper: doi:10.1103/PhysRevLett.86.3200
    title: Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic spreading in scale-free networks, Physical Review Letters 86(14), 2001
    locator: pages 3200 to 3203 (the SIS equations for each degree class, the threshold <k>/<k^2>, and its absence on scale-free networks)
  - paper: doi:10.1140/epjb/e20020122
    title: Y. Moreno, R. Pastor-Satorras and A. Vespignani, Epidemic outbreaks in complex heterogeneous networks, European Physical Journal B 26(4), 2002
    locator: pages 521 to 529 (the SIR model for each degree class and its threshold <k>/(<k^2> - <k>))
  - paper: doi:10.1103/RevModPhys.87.925
    title: Romualdo Pastor-Satorras, Claudio Castellano, Piet Van Mieghem and Alessandro Vespignani, Epidemic processes in complex networks, Reviews of Modern Physics 87(3), 2015
    locator: pages 925 to 979 (the degree-based mean-field theory, its limits, the quenched mean-field theory with the largest eigenvalue of the adjacency matrix, and immunization strategies)
  - paper: doi:10.1103/PhysRevE.66.016128
    title: M. E. J. Newman, Spread of epidemic disease on networks, Physical Review E 66(1), 2002
    locator: the exact threshold of SIR epidemics on random graphs with a given degree distribution, through bond percolation
  - book: isbn:9780691116174
    title: Matt J. Keeling and Pejman Rohani, Modeling Infectious Diseases in Humans and Animals, Princeton University Press, 2008
    locator: Section 7.6, networks (7.6.1.5 scale-free networks), and Section 7.8.1, pair-wise models
---

The degree-based mean-field epidemic model describes an epidemic on a large contact network by one equation for each degree: the fraction $\rho_k$ of nodes with $k$ contacts that are infected. All nodes of the same degree are treated as equal, and the network enters only through its [degree distribution](/degree-distribution/) $P(k)$. The model shows why hubs matter. A node with $k$ contacts is infected about $k$ times as often as a node with one contact, and it passes the infection on to about $k$ others, so the threshold depends on the second moment $\langle k^2 \rangle$ and not only on the mean degree $\langle k \rangle$. On a [scale-free network](/scale-free-network/) with degree exponent at most 3, $\langle k^2 \rangle$ grows without bound with the size of the network, and the [epidemic threshold](/epidemic-threshold/) tends to zero (Pastor-Satorras and Vespignani 2001). The model is a [mean-field approximation](/mean-field-approximation/) of the [SIR model on networks](/sir-epidemic-model/) and of its SIS version. It is not the well-mixed [Kermack-McKendrick model](/kermack-mckendrick-sir-model/): mixing is homogeneous only within a degree class.

## The machine

**Network.** An uncorrelated random network with degree distribution $P(k)$, mean degree $\langle k \rangle = \sum_k k P(k)$ and second moment $\langle k^2 \rangle = \sum_k k^2 P(k)$, such as the [configuration model](/configuration-model/). Uncorrelated means that an edge leads to a node of degree $k'$ with probability $k' P(k') / \langle k \rangle$, whatever the degree of the node at its other end.

**State.** For each degree $k$, the fraction $\rho_k(t)$ of degree $k$ nodes that are infected (SIS), or the fractions $s_k$, $\rho_k$ and $r_k$ (SIR).

**Parameters.** Each edge from an infected to a susceptible node transmits at rate $\beta$, and each infected node recovers at rate $\mu$. Measure time in units of $1/\mu$, so the recovery rate is 1 and the spreading rate is $\lambda = \beta / \mu$.

**SIS equations.**

$$
\frac{d\rho_k}{dt} = -\rho_k + \lambda k (1 - \rho_k)\, \Theta, \qquad \Theta = \frac{1}{\langle k \rangle} \sum_{k'} k' P(k')\, \rho_{k'} .
$$

$\Theta$ is the probability that a random edge leads to an infected node. A susceptible node of degree $k$ has $k$ edges, each leads to an infected node with probability $\Theta$, and each such edge transmits at rate $\lambda$.

**SIR equations.** The same, with a recovered class and one change: a node that was infected through one edge cannot infect back along it, so in the edge probability each infected node of degree $k'$ counts with weight $k' - 1$ instead of $k'$:

$$
\frac{d\rho_k}{dt} = -\rho_k + \lambda k\, s_k\, \Theta, \qquad \Theta = \frac{1}{\langle k \rangle} \sum_{k'} (k' - 1) P(k')\, \rho_{k'}, \qquad \frac{ds_k}{dt} = -\lambda k\, s_k\, \Theta .
$$

**Assumptions.** All nodes of one degree are equal, degrees are uncorrelated, and the dynamics on each node depends on its neighbors only through the mean $\Theta$. This is exact for the annealed network, where the edges are redrawn much faster than the epidemic changes, and it is an approximation for a fixed (quenched) network.

## What it counts

**Prevalence.** The fraction of infected nodes is $\rho = \sum_k P(k) \rho_k$. In the SIS model the stationary state, from $d\rho_k/dt = 0$, is

$$
\rho_k = \frac{\lambda k \Theta}{1 + \lambda k \Theta}, \qquad \Theta = \frac{1}{\langle k \rangle} \sum_k k P(k) \frac{\lambda k \Theta}{1 + \lambda k \Theta} .
$$

The right side of the second equation, as a function of $\Theta$, is increasing and concave, with slope $\lambda \langle k^2 \rangle / \langle k \rangle$ at $\Theta = 0$. So a solution $\Theta > 0$ exists exactly when that slope is larger than 1.

**Threshold.** The epidemic threshold of the SIS model is

$$
\lambda_c^{\mathrm{SIS}} = \frac{\langle k \rangle}{\langle k^2 \rangle},
$$

and the threshold of the SIR version is

$$
\lambda_c^{\mathrm{SIR}} = \frac{\langle k \rangle}{\langle k^2 \rangle - \langle k \rangle}
$$

(Moreno, Pastor-Satorras and Vespignani 2002). On a regular network where every node has degree $k$, these are $1/k$ and $1/(k - 1)$.

**As a reproduction number.** The linearization of the SIS equations at $\rho = 0$ has the [next-generation matrix](/next-generation-matrix/) $K_{k k'} = \lambda k\, k' P(k') / \langle k \rangle$: a node of degree $k'$, infected for a mean time 1, infects the degree class $k$ through its $k'$ edges. $K$ has rank 1, with the eigenvector $(k)$ and the eigenvalue $\lambda \langle k^2 \rangle / \langle k \rangle$, so

$$
R_0 = \lambda \frac{\langle k^2 \rangle}{\langle k \rangle} \quad \text{(SIS)}, \qquad R_0 = \lambda \frac{\langle k^2 \rangle - \langle k \rangle}{\langle k \rangle} \quad \text{(SIR)},
$$

and each threshold is $R_0 = 1$.

**A hand example.** Half of the nodes have degree 1 and half have degree 5. Then $\langle k \rangle = 3$ and $\langle k^2 \rangle = (1 + 25)/2 = 13$. The SIS threshold is $3/13 \approx 0.231$ and the SIR threshold is $3/10 = 0.3$. A regular network with the same mean degree 3 has the thresholds $1/3$ and $1/2$. At $\lambda = 0.5$, the stationary SIS state has $\Theta \approx 0.4930$, $\rho_1 \approx 0.198$, $\rho_5 \approx 0.552$ and the prevalence $\rho \approx 0.375$; you can check that $\rho_5 = 1.2326 / 2.2326$ with $\lambda \cdot 5 \cdot \Theta = 1.2326$, and that $(0.5 \cdot 1 \cdot \rho_1 + 0.5 \cdot 5 \cdot \rho_5) / 3$ gives back $\Theta$. The regular network with $k = 3$ has the prevalence $1 - 1/(\lambda k) = 1/3$. At $\lambda = 0.3$, the infection persists on the mixed network, with prevalence about 0.148, but dies out on the regular one, where $\lambda k = 0.9 < 1$.

## Relation to other models

- **[SIS model](/sis-epidemic-model/).** With one degree class $k$, the equation is the well-mixed SIS model with $\beta = \lambda k$ and $\gamma = 1$.
- **[SIR model on networks](/sir-epidemic-model/).** The exact model on a fixed graph. For SIR on the configuration model, the exact threshold, stated for the transmissibility $T$ (the probability that an infected node infects a given neighbor), is $T_c = \langle k \rangle / (\langle k^2 \rangle - \langle k \rangle)$, the bond [percolation](/percolation/) threshold of the network (Newman 2002). It has the same form as the mean-field threshold, with $T$ in place of $\lambda$.
- **Quenched mean field.** One equation per node, with the adjacency matrix $A$: the SIS threshold is $1 / \Lambda_{\max}(A)$, the inverse of the largest [eigenvalue](/eigenvalue/) of $A$. For SIS on a fixed network, this and other results show that the threshold vanishes for large networks with any power-law degree distribution, also with exponent larger than 3, where the degree-based model predicts a finite threshold (Pastor-Satorras and others 2015).
- **Pair approximations.** Equations for pairs of nodes, such as susceptible-infected edges, correct for the correlations that the mean-field model ignores (Keeling and Rohani 2008, section 7.8.1 treat such pairwise models).
- **[Erdos-Renyi graphs](/erdos-renyi-model/).** With a Poisson degree distribution of mean $c$, $\langle k^2 \rangle = c^2 + c$, so the SIS threshold is $1/(c + 1)$, close to the regular value. Narrow degree distributions give almost the well-mixed result.

## Known results in the model

**The threshold vanishes on scale-free networks.** Let $P(k) \propto k^{-\alpha}$ for $k_{\min} \le k \le k_{\max}$. For $2 < \alpha \le 3$, the mean is finite but $\langle k^2 \rangle$ grows without bound as $k_{\max} \to \infty$, so $\lambda_c \to 0$. For $\alpha = 3$ the growth is slow, like $\ln k_{\max}$. With $\alpha = 3$, $k_{\min} = 3$ and the sums computed exactly:

| $k_{\max}$ | 100 | 1000 | 10000 | 100000 |
|---|---|---|---|---|
| $\lambda_c^{\mathrm{SIS}} = \langle k \rangle / \langle k^2 \rangle$ | 0.1044 | 0.0658 | 0.0476 | 0.0373 |

In a network of $N$ nodes the largest degree grows with $N$, so the threshold falls as the network grows. For $\alpha > 3$, $\langle k^2 \rangle$ stays finite and so does $\lambda_c$ in the degree-based model.

**The hubs are infected first.** In the SIS stationary state, $\rho_k = \lambda k \Theta / (1 + \lambda k \Theta)$ increases with $k$. Near the threshold, $\rho_k$ is about proportional to $k$, so the infection lives mainly on the nodes with the most contacts. In the SIR version, at the start of the outbreak, the infected fraction in class $k$ is proportional to $k$: the infection reaches the hubs first and then spreads to nodes of lower degree.

**Random immunization does not work well.** Immunize a random fraction $g$ of the nodes. In the degree-based model this multiplies $\lambda$ by $1 - g$, so the [herd immunity threshold](/herd-immunity-threshold/) is $g_c = 1 - \lambda_c / \lambda$, which tends to 1 when $\lambda_c \to 0$. In the hand example at $\lambda = 0.5$, $g_c = 1 - 0.2308 / 0.5 \approx 0.54$. Immunizing the nodes of highest degree instead removes the terms that make $\langle k^2 \rangle$ large, and needs a much smaller fraction (Pastor-Satorras and others 2015).

**Early growth.** Near $\rho = 0$, the SIS prevalence grows like $e^{(\lambda \langle k^2 \rangle / \langle k \rangle - 1) t}$, so on a heterogeneous network the epidemic also grows faster than on a regular network with the same mean degree.

**Limits of the model.** The degree-based model ignores the fixed structure of a real network: clustering, degree correlations, and the fact that an infected node can reinfect the neighbor that infected it. For SIR on the configuration model its threshold has the same form as the exact percolation threshold. For SIS on fixed networks it gives a finite threshold for $\alpha > 3$ where the exact threshold vanishes, because a single hub with its neighbors can keep the infection alive for a long time (Pastor-Satorras and others 2015).

## References
