---
tag: XWGWFG
kind: model
slug: gene-regulatory-network
name: Gene regulatory network
aliases:
- GRN
- transcriptional regulatory network
area: biology/systems-biology
level: intro
summary: A directed graph of genes and the transcription factors that activate or repress them, with a dynamic model on top.
prereqs: [directed-graph, ode-initial-value-problem]
see_also: [hill-equation, genetic-toggle-switch, repressilator, feed-forward-loop, random-boolean-network, gene-regulatory-network-inference, chemical-reaction-network, gillespie-algorithm]
sources:
  - book: isbn:9781439837177
    title: Uri Alon, An Introduction to Systems Biology, Design Principles of Biological Circuits, 2nd edition, CRC Press, 2019
    locator: the chapters on transcription networks, the response time of a gene, and autoregulation
  - paper: doi:10.1089/10665270252833208
    title: Hidde de Jong, Modeling and simulation of genetic regulatory systems, a literature review, Journal of Computational Biology 9(1), 67-103, 2002
    locator: the survey of graph, Boolean, differential equation and stochastic models of gene regulation
  - paper: doi:10.1016/0022-5193(73)90247-6
    title: René Thomas, Boolean formalization of genetic control circuits, Journal of Theoretical Biology 42(3), 563-585, 1973
    locator: the logical description of genetic circuits and the role of feedback circuits
  - paper: doi:10.1016/j.aam.2007.11.003
    title: Élisabeth Remy, Paul Ruet and Denis Thieffry, Graphic requirements for multistability and attractive cycles in a Boolean dynamical framework, Advances in Applied Mathematics 41(3), 335-350, 2008
    locator: proofs of Thomas's rules on positive and negative circuits for asynchronous Boolean networks
  - paper: doi:10.1038/ng881
    title: Shai S. Shen-Orr, Ron Milo, Shmoolik Mangan and Uri Alon, Network motifs in the transcriptional regulation network of Escherichia coli, Nature Genetics 31(1), 64-68, 2002
    locator: the E. coli transcription network and the subgraphs that occur in it more often than in random networks
  - paper: doi:10.1016/0022-5193(69)90015-0
    title: Stuart A. Kauffman, Metabolic stability and epigenesis in randomly constructed genetic nets, Journal of Theoretical Biology 22(3), 437-467, 1969
    locator: Boolean networks as models of gene control, with attractors read as cell types
---

A gene regulatory network is a model of how genes control each other's activity. The genes are the nodes of a [directed graph](/directed-graph/), and an edge from gene $i$ to gene $j$ means that the protein made by $i$, a *transcription factor*, binds near gene $j$ and activates or represses its transcription. Each edge has a sign: $+$ for activation and $-$ for repression. The graph alone gives the wiring. A dynamic model on top of it, Boolean, by differential equations, or stochastic, says how the levels of the gene products change in time, and its steady states, oscillations and response times are what the model predicts. Small networks of this kind are the [genetic toggle switch](/genetic-toggle-switch/), two genes that repress each other, and the [repressilator](/repressilator/), a ring of three repressors. The [feed-forward loop](/feed-forward-loop/) is a three-gene pattern that occurs often inside large networks. A [random Boolean network](/random-boolean-network/) is the version with random wiring and random rules, used to ask what typical networks do. Finding the edges of a real network from data is a separate problem, [gene regulatory network inference](/gene-regulatory-network-inference/).

## The machine

**The graph.** A set $V$ of genes and a set of signed edges $(i, j, \sigma)$ with $\sigma \in \{+, -\}$. The regulators of $j$ are $\mathrm{pa}(j) = \{i : (i, j, \sigma) \text{ is an edge}\}$. An edge from $j$ to itself is *autoregulation*. A directed cycle is a *feedback circuit*, and its sign is the product of the signs of its edges: a circuit with an even number of repressions is *positive*, one with an odd number is *negative*.

**Boolean dynamics.** Each gene is on or off, $x_j \in \{0, 1\}$, and has a Boolean function $f_j$ of its regulators. An activator enters the function as a positive literal and a repressor as a negative one; the function says how several inputs combine, for example AND when both activators must bind. Updates are synchronous, $x \to F(x)$, or asynchronous, one gene at a time. The long run states are the attractors, found by [Boolean network attractor detection](/boolean-network-attractor-detection/).

**Differential equation dynamics.** The level $x_j \ge 0$ of the product of gene $j$ follows

$$\frac{dx_j}{dt} = \beta_j \, g_j\big(x_{\mathrm{pa}(j)}\big) - \alpha_j x_j,$$

where $\beta_j$ is the largest production rate, $\alpha_j$ is the rate of removal by degradation and dilution, and $g_j$ takes values in $[0, 1]$. For one regulator, $g_j$ is a [Hill function](/hill-equation/): $x^n / (K^n + x^n)$ for an activator and $K^n / (K^n + x^n)$ for a repressor, with threshold $K$ and Hill coefficient $n$. As $n \to \infty$ these become step functions, and the model approaches the Boolean one. The system is an [initial value problem](/ode-initial-value-problem/) for given starting levels.

**Stochastic dynamics.** In a single cell, a gene product may have only a few copies. Production and degradation are then random events of a [chemical reaction network](/chemical-reaction-network/), with rates $\beta_j g_j$ and $\alpha_j x_j$ for integer counts $x_j$, simulated exactly by the [Gillespie algorithm](/gillespie-algorithm/). The differential equations describe the mean behavior when the counts are large.

**An example: one gene switched on.** A gene with no regulators, or with its activator present from time 0, has $dx/dt = \beta - \alpha x$ and $x(0) = 0$. The solution is

$$x(t) = \frac{\beta}{\alpha}\left(1 - e^{-\alpha t}\right),$$

which rises to the steady state $x_{\mathrm{st}} = \beta / \alpha$. It reaches half of it when $e^{-\alpha t} = 1/2$, at $t_{1/2} = \ln 2 / \alpha$. When production stops at a level $x_{\mathrm{st}}$, $x(t) = x_{\mathrm{st}} e^{-\alpha t}$, with the same half time. For a stable protein in a growing bacterium, $\alpha$ is about the dilution rate $\ln 2 / \tau$ for the cell cycle time $\tau$, so $t_{1/2}$ is about one cell cycle.

## What it counts

- The steady states of the dynamics and their stability. More than one stable steady state means memory: the cell can stay in either state, as in the toggle switch and in cell fate choices.
- Oscillations, their period and amplitude, as in the repressilator and in circadian clocks.
- The response time: how long the target takes to reach half of its new level after a signal changes.
- The input function of each gene: which combinations of regulators turn it on.
- The noise: the spread of levels across cells in the stochastic model.
- Structural counts of the graph: the in-degree and out-degree of genes, the feedback circuits, and the number of times each small pattern, such as the feed-forward loop, occurs.

## Relation to other models

- **[Random Boolean network](/random-boolean-network/).** The Boolean model with random wiring and random functions. It describes the typical behavior of a family of networks, while a gene regulatory network model describes one given network.
- **[Chemical reaction network](/chemical-reaction-network/).** A detailed model of a gene regulatory network lists the binding of factors to DNA, transcription, translation and degradation as reactions. The Hill functions arise from it when binding is fast, by the [quasi-steady-state approximation](/quasi-steady-state-approximation/).
- **[Feed-forward loop](/feed-forward-loop/), [genetic toggle switch](/genetic-toggle-switch/) and [repressilator](/repressilator/).** Small subnetworks with their own pages. The toggle switch has a positive circuit and the repressilator a negative one, while a feed-forward loop has no circuit at all.
- **Bayesian networks.** The statistical models used for [inference](/gene-regulatory-network-inference/) treat the network as a [Bayesian network](/bayesian-network/) or a [dynamic Bayesian network](/dynamic-bayesian-network/), in which an edge is a dependence of distributions, not a binding event.
- **Signaling and metabolic networks.** Signaling networks act on proteins in seconds to minutes, and metabolic networks carry fluxes of small molecules; transcription acts more slowly, on the time scale of $\ln 2 / \alpha$.

## Known results in the model

**Response time (theorem).** For a gene with constant production that starts or stops at time 0, the time to reach half of the change is $\ln 2 / \alpha$, whatever $\beta$ is. The proof is the solution of the example above. So a cell cannot speed up a response of a stable protein by making more of it, only by faster degradation or by a different circuit.

**Negative autoregulation has one steady state (theorem).** If $g$ is decreasing, the equation $dx/dt = \beta g(x) - \alpha x$ has exactly one steady state for $x \ge 0$, and it is stable. *Proof.* The right side $h(x) = \beta g(x) - \alpha x$ is strictly decreasing, with $h(0) = \beta g(0) \ge 0$ and $h(x) \to -\infty$. So it has one zero $x^*$, with $h > 0$ below it and $h < 0$ above it, and solutions move toward it. $\square$

**Positive autoregulation can be bistable (example).** Take $dx/dt = x^2 / (1 + x^2) - 0.4 x$, an activator with $n = 2$ and $K = 1$ that activates its own gene. The steady states solve $x = 0$ or $0.4 x^2 - x + 0.4 = 0$, so they are $0$, $1/2$ and $2$. The derivative of the right side is $2x / (1 + x^2)^2 - 0.4$, which is $-0.4$ at 0, $0.24$ at $1/2$ and $-0.24$ at 2. So 0 and 2 are stable and $1/2$ is unstable: the gene stays off or stays on, depending on where it starts.

**Thomas's rules (theorems in several frameworks).** Thomas proposed that a positive feedback circuit is needed for more than one stable steady state, and a negative feedback circuit is needed for stable oscillations. The two examples above are cases of the first rule. The rules were proved for the differential equation model under conditions on the Jacobian and, by Remy, Ruet and Thieffry (2008), for asynchronous Boolean networks, where the circuits are those of the local interaction graphs. A network without feedback circuits, such as a feed-forward loop on its own, has a unique steady state in these frameworks.

**Every Boolean run ends in an attractor (theorem).** The Boolean model has finitely many states, so every synchronous run enters a cycle, and every asynchronous run enters a terminal strongly connected component of the state graph. Kauffman (1969) read the attractors as cell types.

**Structure of real networks (measurement).** In the transcription network of E. coli, Shen-Orr et al. (2002) found that some three-gene and four-gene patterns, among them the feed-forward loop, occur much more often than in random networks with the same degrees. Such over-represented patterns are called network motifs.

## References
