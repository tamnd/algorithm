---
tag: JT779F
kind: model
slug: random-boolean-network
name: Random Boolean network
aliases:
- Kauffman network
- NK Boolean network
area: biology/systems-biology
level: core
summary: "Kauffman's model of gene regulation: N genes, each on or off, updated at once by a random Boolean function of K random inputs."
history:
  year: 1969
  people: [Stuart A. Kauffman]
  note: Kauffman proposed random Boolean networks as a model of genetic control in 1969 and read their attractors as cell types.
prereqs: [gene-regulatory-network, boolean-function, functional-graph]
see_also: [cellular-automaton, boolean-network-attractor-detection, cycle-detection, percolation, ising-model, markov-chain, gene-regulatory-network-inference, genetic-toggle-switch]
sources:
  - paper: doi:10.1016/0022-5193(69)90015-0
    title: Stuart A. Kauffman, Metabolic stability and epigenesis in randomly constructed genetic nets, Journal of Theoretical Biology 22(3), 437-467, 1969
    locator: the definition of the random nets with N genes and K inputs, and the simulations of their cycles
  - paper: doi:10.1209/0295-5075/1/2/001
    title: Bernard Derrida and Yves Pomeau, Random networks of automata, a simple annealed approximation, Europhysics Letters 1(2), 45-49, 1986
    locator: the annealed approximation for the distance between two runs and the transition between order and chaos
  - paper: doi:10.1103/PhysRevLett.90.098701
    title: Björn Samuelsson and Carl Troein, Superpolynomial growth in the number of attractors in Kauffman networks, Physical Review Letters 90, 098701, 2003
    locator: the number of attractors of critical networks with K = 2
  - paper: doi:10.1007/3-540-46885-4_34
    title: Philippe Flajolet and Andrew M. Odlyzko, Random mapping statistics, Advances in Cryptology, EUROCRYPT 89, LNCS 434, 329-354, 1990
    locator: the number of cyclic points and of components of a random mapping
  - book: isbn:9780195079517
    title: Stuart A. Kauffman, The Origins of Order, Self-Organization and Selection in Evolution, Oxford University Press, 1993
    locator: the chapters on random Boolean networks as models of genomic regulation
---

A random Boolean network, or Kauffman network, is a random [gene regulatory network](/gene-regulatory-network/) in which each of $N$ genes is on or off. Each gene reads $K$ other genes, chosen at random, and computes its next value with a random Boolean function of them, and all genes update at the same time. Kauffman proposed the model in 1969 to ask what a typical network of gene control does, without the details of any one cell. A run of a network always ends in a cycle of states, an *attractor*, and Kauffman read the attractors as the cell types of an organism. The model shows a transition: for unbiased functions, networks with $K = 1$ are ordered, with $K \ge 3$ they are chaotic, and $K = 2$ is critical.

## The machine

**The network.** There are $N$ genes, numbered 1 to $N$. Gene $i$ has an input list of $K$ distinct genes $j_{i1}, \ldots, j_{iK}$, which may include $i$, and a Boolean function $f_i : \{0, 1\}^K \to \{0, 1\}$ stored as a truth table of $2^K$ bits.

**The random ensemble.** For each gene independently, the input list is a uniform random list of $K$ distinct genes, and each of the $2^K$ entries of the truth table is 1 with probability $p$, independently. The parameter $p$ is the *bias*; $p = 1/2$ makes every Boolean function of $K$ inputs equally likely. Some authors draw the inputs with repetition, which changes the small $N$ numbers but not the large $N$ limits. A network drawn once and then kept fixed is a *quenched* network; redrawing it at every step gives the *annealed* model, which is easier to analyze.

**The dynamics.** The state is a vector $x(t) \in \{0, 1\}^N$, and all genes update at once:

$$x_i(t + 1) = f_i\big(x_{j_{i1}}(t), \ldots, x_{j_{iK}}(t)\big), \qquad i = 1, \ldots, N.$$

So the network defines one map $F : \{0, 1\}^N \to \{0, 1\}^N$, and its state graph, with an edge from $x$ to $F(x)$, is a [functional graph](/functional-graph/) on $2^N$ states. Every state has one successor, so every run enters a cycle after a transient. The cycles are the *attractors*, a cycle of length 1 is a *fixed point*, and the set of states that reach an attractor is its *basin*. The basins partition the state space.

**Finding all attractors.** For a small network, one scan over the state space finds every attractor and every basin:

```pseudo id=main
ATTRACTORS(F, N)
L1  label[s] ← none for each of the 2^N states s
L2  for each state s do
L3      path ← empty list; t ← s
L4      while label[t] = none and t is not on path do append t to path; t ← F(t)
L5      if label[t] = none then the states of path from t onward form a new attractor a else a ← label[t]
L6      label[u] ← a for each u on path
L7  return the attractors and, for each one, the number of states with its label
```

Each state joins one path and gets its label once, so the scan makes $2^N$ steps after the table of $F$ is built. Building the table costs $O(2^N N K)$ time. This is the full state space search of [Boolean network attractor detection](/boolean-network-attractor-detection/); for large $N$ it is out of reach, and that page describes the methods that avoid it.

**An example.** Take three genes A, B and C with $A' = B$, $B' = A$ and $C' = A \wedge B$, written as states $ABC$. Then $000$ is a fixed point, reached also from $001$. The state $111$ is a fixed point, reached also from $110$. The states $010$ and $100$ form a cycle of length 2, since $010 \to 100 \to 010$, and $011$ and $101$ lead into it. So there are three attractors, with basins of 2, 2 and 4 states. This network is not random, but it is a member of the ensemble with $N = 3$ and $K \le 2$.

## What it counts

- The number of attractors of a network, and how it grows with $N$.
- The length of each attractor and of the transients that lead to it.
- The size of each basin, as a fraction of the $2^N$ states.
- The *spread*: the number of genes that differ at the next step when one gene of a state is flipped. Its mean decides whether small changes die out (ordered) or grow (chaotic).
- The frozen genes: those that end with the same value on every attractor, whatever the start.

## Relation to other models

- **[Gene regulatory network](/gene-regulatory-network/).** A Boolean model of a real network has the inputs and functions of known regulators. A random Boolean network replaces them by random draws, so its results are about typical networks, not about one cell.
- **[Cellular automaton](/cellular-automaton/).** A cellular automaton also has cells with finite states and a synchronous update, but its cells sit on a regular lattice, read their geometric neighbors, and all use the same rule. A random Boolean network has random wiring and a different random rule at each gene.
- **Random mappings.** With $K = N$, every entry of the map $F$ is an independent uniform state, so $F$ is a uniform random map of a set of size $M = 2^N$ to itself, and its attractors are the cycles of that map.
- **Asynchronous networks.** If one gene updates at a time, in a random or arbitrary order, a state can have several successors, and the attractors become the terminal strongly connected components of the state graph. The attractors of the two schemes differ in general. In the example above, the cycle of $010$ and $100$ is not an attractor under one at a time updates: from $010$, an update of A alone gives $110$, and an update of C then gives the fixed point $111$.
- **Mean field and spin models.** The annealed approximation of Derrida and Pomeau treats the network like a mean field model of statistical physics, as for the [Ising model](/ising-model/), and the order to chaos transition is a [percolation](/percolation/) like transition of the spread of a change.

## Known results in the model

**The expected number of fixed points is 1 (theorem).** For every $N$, $K$ and $p$, the expected number of fixed points of a random network is 1.

*Proof.* Fix a state $x$. The value $f_i(x)$ is one entry of the truth table of gene $i$, which is 1 with probability $p$ whatever the inputs of $i$ are. So $P(f_i(x) = x_i)$ is $p$ if $x_i = 1$ and $1 - p$ if $x_i = 0$. The tables of different genes are independent, so $P(F(x) = x) = \prod_i p^{x_i} (1 - p)^{1 - x_i}$, which is the probability of $x$ under independent bits with bias $p$. The sum over all $x$ is 1. $\square$

**The one step spread is $2 p (1 - p) K$ (theorem).** Draw a random network, a state $x$ and a gene $g$, all uniform and independent, and let $D$ be the number of genes whose next value changes when $x_g$ is flipped. Then $E[D] = 2 p (1 - p) K$.

*Proof.* Gene $i$ has $g$ among its inputs with probability $K/N$. Then the flip changes the entry of the truth table that $f_i$ reads, from one entry to another one, and two different entries are independent bits with bias $p$, which differ with probability $2 p (1 - p)$. If $g$ is not an input of $i$, $f_i$ does not change. So $E[D] = N \cdot (K / N) \cdot 2 p (1 - p)$. $\square$

**The critical line (annealed approximation).** Derrida and Pomeau (1986) followed the distance between two runs in the annealed model and found that a small distance shrinks when $2 p (1 - p) K < 1$ and grows when $2 p (1 - p) K > 1$. For $p = 1/2$ the critical value is $K_c = 2$. This matches the spread above: on average, one flipped gene changes less than one gene at the next step in the ordered phase and more than one in the chaotic phase. The approximation ignores the fixed wiring of a quenched network, so it is a guide for quenched networks, not a proof about them.

**Fully random networks (theorem).** For $K = N$ the network is a uniform random map on $M = 2^N$ states. The number $k$ of states on cycles has $P(k) = \frac{k}{M} \prod_{i=1}^{k-1} \left(1 - \frac{i}{M}\right)$, and given $k$, the cycles are those of a uniform permutation of $k$ points, so their number has mean $H_k = \sum_{i \le k} 1/i$ and variance $H_k - \sum_{i \le k} 1/i^2$. The expected number of cyclic states grows like $\sqrt{\pi M / 2}$ and the expected number of attractors like $\frac12 \ln M = \frac{N \ln 2}{2}$ (Flajolet and Odlyzko). So attractors in the chaotic limit are few but very long, with lengths of the order of $2^{N/2}$. For $N = 4$ the exact mean number of attractors is $2.1224$ with variance $0.9520$; the test of the implementation draws 2000 networks with $N = K = 4$ and measures a mean of $2.1065$, within one standard error.

**Critical networks have many attractors.** Kauffman's simulations of networks with $K = 2$ suggested that the number of attractors grows like $\sqrt{N}$, and he compared this with the number of cell types of organisms. That estimate came from sampling a few starting states, which misses small basins. Samuelsson and Troein (2003) showed that the mean number of attractors of critical $K = 2$ networks grows faster than any power of $N$.

**Networks with one input (theorem).** For $K = 1$, each gene is a constant, a copy or a negation of its one input, so the wiring is a set of loops with trees hanging off them. A loop of $L$ genes with no constant returns to its state after at most $2L$ steps, since after $L$ steps every gene is flipped by the parity of the negations on the loop. A gene off the loops repeats, with a delay, the gene it reads. So every attractor length divides the least common multiple of the numbers $2L$ over the loops, and genes that read a constant freeze.

## References
