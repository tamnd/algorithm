---
tag: SZDPCS
kind: concept
slug: epidemic-threshold
name: Epidemic threshold
aliases:
- percolation threshold for gossip
area: distributed/gossip
level: advanced
summary: The value of the spreading rate at which an epidemic changes from dying out to reaching a constant fraction of the nodes; R0 = 1 under mixing, β/δ = 1/λ1(A) on a graph.
prereqs: [epidemic-model, spectral-radius, adjacency-matrix, giant-component]
see_also: [epidemic-model, gossip-fanout, giant-component, percolation, scale-free-network, spectral-radius, perron-frobenius-theorem, configuration-model]
sources:
  - paper: doi:10.1098/rspa.1927.0118
    title: William O. Kermack and Anderson G. McKendrick, A contribution to the mathematical theory of epidemics, Proceedings of the Royal Society of London, Series A 115(772), 700-721, 1927
    locator: the threshold density of susceptibles
  - paper: doi:10.1137/S0036144500371907
    title: Herbert W. Hethcote, The mathematics of infectious diseases, SIAM Review 42(4), 599-653, 2000
    locator: Section 2 (R0 and the threshold of the SIR and SIS models)
  - paper: doi:10.1109/RELDIS.2003.1238052
    title: Yang Wang, Deepayan Chakrabarti, Chenxi Wang and Christos Faloutsos, Epidemic spreading in real networks, an eigenvalue viewpoint, Proceedings of the 22nd IEEE Symposium on Reliable Distributed Systems (SRDS), 2003
    locator: the discrete-time SIS model on a graph and the threshold β/δ < 1/λ1(A)
  - paper: doi:10.1109/INFCOM.2005.1498374
    title: Ayalvadi Ganesh, Laurent Massoulié and Don Towsley, The effect of network topology on the spread of epidemics, Proceedings of IEEE INFOCOM 2005
    locator: Section III (Theorem 3.1, fast die out below the spectral radius threshold, condition (1) as proposed by Wang et al.), Section IV (Theorem 4.1, slow die out above an isoperimetric threshold), Section V (star, hypercube, complete graph, Erdős-Rényi and power law graphs)
  - paper: doi:10.1103/PhysRevLett.86.3200
    title: Romualdo Pastor-Satorras and Alessandro Vespignani, Epidemic spreading in scale-free networks, Physical Review Letters 86(14), 3200-3203, 2001
    locator: the SIS model on scale-free networks; the threshold ⟨k⟩/⟨k²⟩, which tends to 0 for degree exponents at most 3
  - paper: doi:10.1109/TPDS.2003.1189583
    title: Anne-Marie Kermarrec, Laurent Massoulié and Ayalvadi J. Ganesh, Probabilistic reliable dissemination in large-scale systems, IEEE Transactions on Parallel and Distributed Systems 14(3), 248-258, 2003
    locator: Section 3.1 (Theorem 1, the threshold ln n for reaching every node)
---

The epidemic threshold is the value of the spreading rate at which an epidemic, or a gossip protocol, changes from dying out after a few steps to reaching a constant fraction of the nodes. Under homogeneous mixing it is $R_0 = \beta/\gamma = 1$, as Kermack and McKendrick (1927) found. On a graph with adjacency matrix $A$, the SIS threshold is $\beta/\delta = 1/\lambda_1(A)$, where $\lambda_1$ is the largest eigenvalue (Wang et al. 2003; Ganesh, Massoulié and Towsley 2005). On scale-free graphs the threshold goes to 0 as the graph grows (Pastor-Satorras and Vespignani 2001), and for gossip there is a second, higher threshold, $\ln n$ messages per node, for reaching every node.

## In plain words

Suppose each person who has a cold passes it on to some number of others before getting well. If each sick person infects fewer than one new person on average, the chain of infections gets shorter and shorter and soon stops. If each infects more than one, the number of sick people grows, and a large share of the population catches the cold. The change is sudden, and the point where it happens is the threshold. In a network, what counts is not the average number of contacts but how many contacts the most connected parts have: a few very well connected hubs can keep an infection alive even when it spreads slowly. For a gossip protocol, the same idea says how much each node must send so that a message reaches most nodes, and a little more is needed to reach all of them.

## The idea

### Notation and model

| Symbol | Meaning |
|---|---|
| $n$, $m$ | the numbers of nodes and edges of the contact graph |
| $\beta$ | the infection rate: per contact under mixing, per edge on a graph |
| $\gamma$, $\delta$ | the removal rate (SIR) and the cure rate (SIS) |
| $R_0$ | $\beta/\gamma$, the mean number of nodes one infective infects in a fully susceptible population |
| $A$, $\lambda_1(A)$ | the adjacency matrix and its largest eigenvalue, the spectral radius |
| $k$, $\langle k \rangle$, $\langle k^2 \rangle$ | a degree, and the first two moments of the degree distribution |
| $\Delta$, $D$ | the maximum degree and the diameter |
| $f$ | the number of crashed nodes, when nodes fail |

The models are the SI, SIS and SIR models of the [epidemic model](/epidemic-model/) page, in continuous time or in synchronous rounds. On a graph, an infective node infects each susceptible neighbor at rate $\beta$, independently.

### Homogeneous mixing: R0 = 1

In SIR, $\dot i = (\beta s - \gamma) i$. At the start $s \approx 1$, so $i$ grows if and only if $R_0 = \beta/\gamma > 1$. If $R_0 \le 1$, an infection that starts in a few nodes reaches only $o(n)$ of them; if $R_0 > 1$, it reaches the fraction $1 - s_\infty$, where $s_\infty$ is the root in $(0,1)$ of $s_\infty = e^{-R_0(1 - s_\infty)}$. The stochastic model adds one thing: with one initial infective and $R_0 > 1$, the infection still dies out early with probability about $1/R_0$, because the early chain of infections is a branching process.

The threshold is sharp. In the table, $1 - s_\infty$ is 0 up to $R_0 = 1$ and then rises fast:

| $R_0$ | 0.9 | 1.0 | 1.1 | 1.5 | 2 | 3 |
|---|---|---|---|---|---|---|
| fraction ever infected, $1 - s_\infty$ | 0 | 0 | 0.176 | 0.583 | 0.797 | 0.940 |

### On a graph: the largest eigenvalue

Let $p_i(t)$ be the probability that node $i$ is infected in round $t$ of a discrete SIS model in which an infected node is cured with probability $\delta$ per round and infects each neighbor with probability $\beta$ per round. While few nodes are infected, the linear approximation is
$$p(t + 1) \approx \left((1 - \delta) I + \beta A\right) p(t).$$
The matrix $(1 - \delta) I + \beta A$ has largest eigenvalue $1 - \delta + \beta \lambda_1(A)$, which is less than 1 if and only if
$$\frac{\beta}{\delta} < \frac{1}{\lambda_1(A)}.$$
Below this value the vector $p(t)$ shrinks geometrically, and the infection dies out. This is the threshold of Wang, Chakrabarti, Wang and Faloutsos (2003). Since $A$ is nonnegative, the [Perron-Frobenius theorem](/perron-frobenius-theorem/) gives a nonnegative eigenvector for $\lambda_1$, and $\langle k \rangle \le \lambda_1 \le \Delta$, with equality for regular graphs.

**The rigorous version (Ganesh, Massoulié and Towsley 2005).** For the continuous-time SIS process on a finite graph, the epidemic always dies out in the end, so the question is how long it lives. They prove that if $\beta / \delta < 1/\lambda_1(A)$, which is the condition of Wang et al., then the expected time until the epidemic dies out is $O(\log n)$ (Theorem 3.1). The proof bounds the process by a linear system with the matrix $\beta A - \delta I$. Conversely, if $\beta/\delta$ is larger than the inverse of a generalized isoperimetric constant of the graph, the expected lifetime is at least $e^{n^a}$ for a constant $a > 0$ (Theorem 4.1). They state that the two conditions are close for the hypercube, the complete graph and Erdős-Rényi graphs, and far apart for the star and power law graphs. These results are cited, not proved here.

**Examples of $1/\lambda_1$.**

| Graph | $\lambda_1(A)$ | threshold $1/\lambda_1$ for $n \approx 1000$ |
|---|---|---|
| complete graph $K_n$ | $n - 1$ | 0.0010 ($n = 1000$) |
| star with $n - 1$ leaves | $\sqrt{n - 1}$ | 0.0316 ($n = 1000$) |
| hypercube $Q_d$ | $d$ | 0.1 ($n = 1024$) |
| $k$-regular graph | $k$ | $1/k$ |
| cycle | 2 | 0.5 |

The star shows the effect of a hub: its average degree is below 2, but $\lambda_1 = \sqrt{n - 1}$, so a small rate already keeps the infection alive near the hub.

**A simulation.** A seeded run of the discrete SIS model on a 6-regular multigraph with $n = 500$, made of three random Hamiltonian cycles, with $\delta = 0.2$, 50 initial infectives and 5 seeds per row, gives the following. The linear threshold is $1/\lambda_1 = 1/6 \approx 0.167$.

| $\beta/\delta$ | 0.10 | 0.15 | 0.20 | 0.25 | 0.40 |
|---|---|---|---|---|---|
| runs still alive after 400 rounds | 0 of 5 | 0 of 5 | 2 of 5 | 5 of 5 | 5 of 5 |
| infected fraction in live runs | | | 0.02 to 0.04 | 0.22 to 0.32 | 0.49 to 0.52 |

Below $1/\lambda_1$ every run dies within 83 rounds. The change happens a little above $1/\lambda_1$, because the linear approximation ignores the fact that a node infected twice counts once, so $1/\lambda_1$ is the lower end of the transition.

### Scale-free graphs

Pastor-Satorras and Vespignani (2001) studied SIS on graphs with a power law degree distribution $P(k) \sim k^{-\gamma'}$ (they write $\gamma$ for the exponent; this page uses $\gamma'$ to avoid a clash with the removal rate). In their heterogeneous mean-field approximation, nodes of the same degree behave alike, and the threshold is
$$\frac{\beta}{\delta} = \frac{\langle k \rangle}{\langle k^2 \rangle}.$$
For $2 < \gamma' \le 3$, $\langle k^2 \rangle$ grows without bound as $n$ grows, so the threshold tends to 0: in a large [scale-free network](/scale-free-network/) any positive spreading rate keeps an infection alive. The spectral view gives the same picture, since $\lambda_1 \ge \sqrt{\Delta}$ (the star around the node of largest degree) and $\Delta$ grows with $n$.

### Percolation and the configuration model

In SIR with a fixed infectious period, each edge from an infective to a neighbor transmits with some probability $T$, the transmissibility, independently. The set of nodes ever infected is the set reached from the source in a bond [percolation](/percolation/) of the graph with edge probability $T$. In the [configuration model](/configuration-model/), a node reached along an edge has, on average, $(\langle k^2 \rangle - \langle k \rangle)/\langle k \rangle$ further edges, so the exploration is a branching process with mean $T(\langle k^2 \rangle - \langle k \rangle)/\langle k \rangle$, and a giant outbreak is possible if and only if this is larger than 1. For a constant degree $k$ this is $T(k - 1) > 1$; for the complete graph with $T = R_0/n$ it is $R_0 > 1$.

### Two thresholds for gossip

A gossip protocol must reach every node, not only a constant fraction. So it has two thresholds:

1. **Take-off.** With infect and die and fanout $k$, each node infects about $k$ others, so $R_0 = k$, and a message reaches a constant fraction $\pi$ of the nodes, with $\pi = 1 - e^{-k\pi}$, if and only if $k > 1$.
2. **Reaching everybody.** A fanout of $\ln n + c$ reaches all nodes with probability tending to $e^{-e^{-c}}$ (Kermarrec, Massoulié and Ganesh 2003, Theorem 1). This is the threshold of [gossip fanout](/gossip-fanout/), and it is the connectivity threshold of a random graph, not the giant component threshold.

The cost of the second threshold is a factor $\ln n$ in messages, and it is the reason for the $n \ln n$ messages of push gossip.

## Examples

- **Constant fanout.** With $n = 1000$ and infect and die, the fraction reached is about 0.80, 0.94 and 0.99 for fanout 2, 3 and 5, and only $o(n)$ for fanout 1 or less; see [gossip fanout](/gossip-fanout/).
- **Rumor mongering.** In the rumor mongering of Demers et al., a site loses interest with probability $1/k$ after each useless contact, and the residue equation is the SIR final size equation with $R_0 = k + 1 \ge 2$, so the rumor always takes off and leaves a residue of about $e^{-(k+1)}$ for large $k$; see [rumor mongering](/rumor-mongering/).
- **Worms and viruses.** Ganesh, Massoulié and Towsley apply the spectral threshold to the hypercube, as a model of a distributed hash table, and to the complete graph and power law graphs, as models of router and Internet topologies.
- **A degree sequence with a hub.** A graph made of a star with 999 leaves has mean degree about 2, but $\lambda_1 \approx 31.6$, so the spectral threshold is 0.032, much below the value $1/\langle k \rangle \approx 0.5$ that the mean degree would suggest.

## Where it is used

- **Choosing a fanout.** Gossip protocols set the fanout well above the take-off threshold, and above $\ln n$ when every node must be reached; see [probabilistic broadcast](/probabilistic-broadcast/) and [bimodal multicast](/bimodal-multicast/).
- **Network security.** The spectral threshold tells how fast a defense must clean infected hosts to make a worm die out on a given topology.
- **Overlay design.** An overlay with hubs keeps information, and also faults and stale data, alive; one with bounded degree has a higher threshold.
- **Failures.** If $f$ of the $n$ nodes crash and lose all messages sent to them, the effective fanout falls by the factor $(n - f)/n$, which moves a protocol toward the threshold.

## References
