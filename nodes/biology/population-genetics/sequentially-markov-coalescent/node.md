---
tag: 03ACX0
kind: model
slug: sequentially-markov-coalescent
name: Sequentially Markov coalescent
aliases:
- SMC model
- SMC prime
area: biology/population-genetics
level: advanced
summary: An approximation of the coalescent with recombination in which the genealogy along the genome is a Markov chain of local trees.
history:
  year: 2005
  people: [Gilean A. T. McVean, Niall J. Cardin]
  note: McVean and Cardin proposed in 2005 to approximate the coalescent with recombination by a Markov chain of local trees along the sequence; Marjoram and Wall gave the SMC' variant in 2006.
prereqs: [kingman-coalescent, ancestral-recombination-graph, coalescent-simulation]
see_also: [psmc, ancestral-recombination-graph-inference, hidden-markov-model, coalescent-theory, infinite-sites-model, forward-backward-algorithm]
sources:
  - paper: doi:10.1098/rstb.2005.1673
    title: Gilean A. T. McVean and Niall J. Cardin, Approximating the coalescent with recombination, Philosophical Transactions of the Royal Society B 360(1459), 2005
    locator: pp. 1387-1393 (the SMC, its construction along the sequence, and comparisons with the full coalescent with recombination)
  - paper: doi:10.1186/1471-2156-7-16
    title: Paul Marjoram and Jeffrey D. Wall, Fast "coalescent" simulation, BMC Genetics 7, 2006
    locator: article 16 (the SMC' variant, which also allows coalescence with the branch that was cut, and its accuracy)
  - paper: doi:10.1006/tpbi.1998.1403
    title: Carsten Wiuf and Jotun Hein, Recombination as a point process along sequences, Theoretical Population Biology 55(3), 1999
    locator: pp. 248-259 (the construction of the coalescent with recombination along the sequence, which is not Markov)
  - paper: doi:10.1038/nature10231
    title: Heng Li and Richard Durbin, Inference of human population history from individual whole-genome sequences, Nature 475(7357), 2011
    locator: pp. 493-496 (a hidden Markov model of the pairwise coalescence time along the genome, based on the SMC)
---

The sequentially Markov coalescent (SMC) is a model of the genealogy of a sample of recombining sequences. It is an approximation of the coalescent with recombination, whose full history is the [ancestral recombination graph](/ancestral-recombination-graph/). Walking along the sequence, the SMC keeps only the current local tree. At a recombination point it cuts one branch of the tree and lets the cut lineage join the rest of the tree again, so that the next tree depends only on the current one. The sequence of local trees is then a Markov chain, which the full model does not give. McVean and Cardin proposed it in 2005, and the SMC' of Marjoram and Wall (2006) is a closer variant. Fast simulators and the hidden Markov models of [PSMC](/psmc/) and of [ARG inference](/ancestral-recombination-graph-inference/) use them.

## The machine

**The state.** A position $x$ in the sequence, which is the interval $[0, \ell]$, and the local tree $T_x$ of the $n$ sampled copies at $x$: a rooted binary tree with node ages. Time runs backward in units of $2N$ generations, as in the [Kingman coalescent](/kingman-coalescent/).

**The parameters.** The population recombination rate $\rho = 4Nr$ per unit of sequence, where $r$ is the probability of a crossover per unit of sequence per generation, and the mutation rate $\theta = 4N\mu$ per unit of sequence for the data.

**The rules.**
1. At $x = 0$, $T_0$ is a Kingman coalescent tree.
2. Recombination points along the sequence come at rate $\frac{\rho}{2} L(T_x)$, where $L(T_x)$ is the total branch length of the current tree. Between two points the tree stays the same.
3. At a recombination point, choose a point $(b, u)$ uniformly on the branches of the tree: branch $b$, at age $u$. Cut branch $b$ at age $u$; the part of $b$ above $u$ is removed, and the part below $u$ becomes a floating lineage that starts at age $u$.
4. The floating lineage joins the rest of the tree going back in time from $u$. At each age $t > u$ it joins each lineage of the rest of the tree at rate 1, and above the root of the rest it joins the root lineage at rate 1. Where it joins, it makes a new node.
5. **SMC.** The rest of the tree does not include the removed part of branch $b$. **SMC'.** The removed part of $b$ is still available, so the floating lineage may join its own old branch; then the tree does not change.

**The standing assumptions.** Neutrality, a constant population size, random mating, no structure, crossovers at a constant rate along the sequence and no gene conversion. Mutations fall on each local tree under the [infinite sites model](/infinite-sites-model/) with rate $\theta/2$ per unit of branch length per unit of sequence.

**A small example.** Take $n = 3$ with copies a, b, c. The tree at $x$ joins a and b at age $0.3$ and that pair with c at age $1.0$. Its total length is $0.3 + 0.3 + 1.0 + 0.7 = 2.3$, so the next recombination point comes at rate $1.15 \rho$. Suppose rule 3 cuts the branch above a at age $u = 0.2$. Under the SMC, the rest of the tree is the branch of b and the branch of c, which join at age $1.0$. From age $0.2$ to $1.0$ the floating lineage of a joins either of the two at total rate 2, and above $1.0$ it joins the root lineage at rate 1. If it joins c at age $0.6$, the new tree joins a and c at $0.6$ and that pair with b at $1.0$: the topology has changed. If it joins b at age $0.6$, the topology stays and the node of a and b moves from $0.3$ to $0.6$. Under the SMC', between $0.2$ and $0.3$ the old branch of a is a third lineage that the floating lineage may join, and if it does, the tree at the next position is the same as before.

## What it counts

- The local trees $T_x$ and the breakpoints where they change. Under the SMC, each recombination point changes the tree, because the floating lineage always joins a branch other than its own.
- For $n = 2$, the coalescence time $T_x$ of the two copies along the sequence, a Markov process on $(0, \infty)$. This is the hidden state of [PSMC](/psmc/).
- The pattern of mutations along the sequence: mutations on $T_x$ give the alleles at site $x$, so the data at nearby sites are correlated through shared trees.
- Statistics of linkage between pairs of sites, which depend on the joint law of the trees at two positions.

## Relation to other models

- **The ancestral recombination graph.** The full coalescent with recombination of Hudson (1983) gives the same marginal law of each local tree, but the trees along the sequence are not a Markov chain: a lineage may join a part of the graph that is not in the current tree and that only an earlier tree, farther back along the sequence, contains (Wiuf and Hein 1999). The SMC removes exactly those events. In the backward-in-time description of McVean and Cardin, it allows coalescence only between lineages whose ancestral material overlaps. The SMC' also allows it between lineages whose material is adjacent.
- **SMC against SMC'.** The SMC' keeps one more kind of event: the floating lineage may join the branch it was cut from. Such an event leaves the tree the same, and events of this kind are common in the full model. Marjoram and Wall (2006) found that the SMC' gives linkage statistics much closer to the full model than the SMC.
- **Simulation.** A simulator along the sequence that follows rules 1 to 5 runs in time about linear in the length of the sequence, while a backward simulation of the full graph slows down quickly as $\rho$ grows. MaCS and others keep a little more than the current tree to get closer to the full model.
- **Hidden Markov models.** Because the local trees form a Markov chain and the data at a site depend only on the local tree, the SMC with mutations is a continuous-state [hidden Markov model](/hidden-markov-model/) along the sequence. Discretizing the times gives a finite HMM that the [forward-backward algorithm](/forward-backward-algorithm/) handles. PSMC does this for $n = 2$, MSMC for more copies, and ARGweaver samples whole ARGs under a discretized SMC'.

## Known results in the model

**Marginal trees.** Under both the SMC and the SMC', the local tree $T_x$ at every fixed position $x$ is a Kingman coalescent tree, as in the full model. The process of trees is stationary along the sequence.

**Two copies, same tree at two sites.** For $n = 2$ under the SMC, the probability that two sites at distance $\delta$ have the same local tree is

$$P(T_x = T_{x+\delta}) = \frac{1}{1 + \rho\delta}.$$

*Proof.* The tree of two copies has total length $2T$, where $T = T_x$ is exponential with rate 1. Given $T = t$, recombination points come at rate $\frac{\rho}{2} \cdot 2t = \rho t$ along the sequence. Under the SMC each point changes $T$ to a new value with a continuous law, so the tree at $x + \delta$ is the same exactly when no point falls in $(x, x + \delta]$, which has probability $e^{-\rho t \delta}$. Averaging over $T$, $\int_0^\infty e^{-t} e^{-\rho \delta t}\, dt = 1/(1 + \rho\delta)$. $\square$

For $\rho\delta = 0.5$, the probability is $2/3$. Under the SMC' the same tree can come back after an event, so the probability is larger.

**Two copies, the transition.** For $n = 2$ under the SMC, given a recombination point on a tree with coalescence time $t$, the cut age $u$ is uniform on $(0, t)$, and the new time is $u + E$ with $E$ exponential with rate 1, independent of $u$. The floating lineage has only the other lineage to join, which exists at all ages above $u$. A recombination point is more likely on a tall tree, with weight proportional to $t$, so the tree just before a point has the size-biased density $t e^{-t}$. Then $u$ has the density $\int_u^\infty t e^{-t} \cdot (1/t)\, dt = e^{-u}$, and the new time $u + E$ again has the density $t e^{-t}$. So the chain keeps the Kingman marginal.

**Number of recombination points.** Along a sequence of total recombination rate $R = \rho \ell$, the expected number of recombination points is $E[\frac{R}{2} L(T_0)] = R a_n$, with $a_n = \sum_{i=1}^{n-1} 1/i$, because $E[L] = 2 a_n$ and the process of trees is stationary. Under the SMC every one of them is a change of tree.

**Accuracy.** The SMC underestimates the correlation of trees at nearby sites, because it removes the events in which a lineage joins back its own ancestry. The SMC' corrects the most common of these, and its single-site and two-site statistics are close to those of the full model in the simulations of Marjoram and Wall (2006).

## References
