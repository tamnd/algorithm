---
tag: NNH0F8
kind: data-structure
slug: ancestral-recombination-graph
name: Ancestral recombination graph
aliases:
- ARG
area: biology/phylogenetics
level: research
summary: Graph recording coalescence and recombination events among sampled sequences over time.
model: real-ram
complexity:
  vars: {n: the number of samples, e: the number of events in the graph, k: the largest number of live lineages, s: the largest number of material intervals on one lineage}
  time: {worst: O(e·k·s·log(k·s))}
  space: {extra: O(e·s)}
prereqs: [kingman-coalescent, directed-acyclic-graph]
see_also: [ancestral-recombination-graph-inference, coalescent-theory, phylogenetic-network, four-gamete-condition, perfect-phylogeny, interval-tree, importance-sampling, hidden-markov-model]
sources:
  - paper: doi:10.1016/0040-5809(83)90013-8
    title: R. R. Hudson, Properties of a neutral allele model with intragenic recombination, Theoretical Population Biology 23(2), 1983, 183-201
    locator: the coalescent with recombination along a sequence, simulated backward in time with ancestral material on each lineage
  - paper: doi:10.1089/cmb.1996.3.479
    title: R. C. Griffiths and P. Marjoram, Ancestral inference from samples of DNA sequences with recombination, Journal of Computational Biology 3(4), 1996, 479-502
    locator: the graph of the sample history with recombination, and likelihood inference over it by importance sampling
  - paper: doi:10.1007/978-1-4757-2609-1_16
    title: R. C. Griffiths and P. Marjoram, An ancestral recombination graph, in Progress in Population Genetics and Human Evolution, IMA Volumes in Mathematics and its Applications 87, Springer, 1997, 257-270
    locator: the name ancestral recombination graph, the birth and death process of the lineages and the ultimate ancestor
  - paper: doi:10.1006/tpbi.1998.1403
    title: C. Wiuf and J. Hein, Recombination as a point process along sequences, Theoretical Population Biology 55(3), 1999, 248-259
    locator: the construction of the graph along the sequence, one marginal tree after another
  - paper: doi:10.1098/rstb.2005.1673
    title: G. A. T. McVean and N. J. Cardin, Approximating the coalescent with recombination, Philosophical Transactions of the Royal Society B 360(1459), 2005, 1387-1393
    locator: the sequentially Markov coalescent, an approximation that keeps only the current marginal tree
  - paper: doi:10.1186/1471-2156-7-16
    title: P. Marjoram and J. D. Wall, Fast coalescent simulation, BMC Genetics 7, 2006, article 16
    locator: the SMC' approximation, which also allows coalescence back into the same branch
  - paper: doi:10.1371/journal.pcbi.1004842
    title: J. Kelleher, A. M. Etheridge and G. McVean, Efficient coalescent simulation and genealogical analysis for large sample sizes, PLOS Computational Biology 12(5), 2016, e1004842
    locator: Hudson's algorithm with interval lists of ancestral material, and the storage of the marginal trees as a tree sequence
---

An ancestral recombination graph (ARG) records the genealogy of a sample of DNA sequences from one population when recombination is present. It is a [directed acyclic graph](/directed-acyclic-graph/) whose nodes are ancestors at given times: the samples at time 0, coalescence nodes where two lineages meet in a common ancestor, and recombination nodes where one lineage takes its left part from one parent and its right part from another. At each position of the sequence, the edges that carry that position form a binary tree, the marginal tree. Neighbouring positions share most of their history, and the graph stores that history once. Hudson (1983) gave the process that generates the graph, the coalescent with recombination, and Griffiths and Marjoram (1996, 1997) named the graph and used it for inference.

## In plain words

Take a few copies of a gene from different people and follow them back in time. Without recombination, two copies sometimes meet in a parent, and the meetings form a family tree. With recombination, a copy can be built from two parents: its left part comes from one and its right part from the other. At that point the line splits in two as we go back. So the history is a network, not a tree. Each event happens at a time, and each line remembers which part of the gene it still carries for the sample. For any single letter of the gene, the lines that carry that letter form an ordinary family tree. Letters near each other usually have the same tree. The graph holds all these trees at once.

## The abstract type

The sequence is the interval $[0, 1)$ of positions. The structure holds a finite set of nodes, each with a time, and edges from each node to its parents. A *lineage* is an edge, or a free end above a node that has no parent yet. Each lineage $a$ carries its *material* $\mathrm{mat}(a)$, the set of positions at which it is ancestral to some sample whose common ancestor at that position is not yet reached. The operations are:

- **ADD-SAMPLE.** Make a node at time 0 with one lineage that carries all positions.
- **COALESCE$(a, b, t)$.** Close two live lineages at a node at time $t$, with one new lineage above it.
- **RECOMBINE$(a, x, t)$.** Close a live lineage at a node at time $t$ with breakpoint $x$, with two new lineages above it: the left one carries $\mathrm{mat}(a) \cap [0, x)$ and the right one $\mathrm{mat}(a) \cap [x, 1)$.
- **LOCAL-TREE$(x)$.** The marginal tree at position $x$, with its node times.
- **LOCAL-TREES.** The list of marginal trees along the sequence, each with the interval on which it holds.

SIMULATE$(n, \rho)$ builds a random graph for $n$ samples under the coalescent with recombination, with population recombination rate $\rho$ for the whole sequence.

## Representation

- **Nodes.** Arrays indexed by node: the time, the kind (sample, coalescence or recombination), the list of child lineages, the list of parents (one slot, or two slots for a recombination node), and the breakpoint of a recombination node.
- **Lineages.** A lineage is a pair $(v, j)$ of a node $v$ and a parent slot $j$. Slot 0 is the only edge above a sample or a coalescence node; slots 0 and 1 are the left and right edges above a recombination node.
- **Material.** A sorted list of disjoint half-open intervals for each lineage, with union, intersection and difference by merging the two lists.
- **Time.** Coalescent units, in which each pair of lineages coalesces at rate 1. With $\rho = 4Nr$ for a diploid population of size $N$ and a recombination probability $r$ per generation over the sequence, a lineage whose material spans a length $\ell$ recombines at rate $\rho\ell/2$.

## Operations

```pseudo id=main
SIMULATE(n, ρ)                                   ▷ Hudson's algorithm, backward in time
L1  live ← n sample lineages, each with material [0, 1); t ← 0
L2  while live is not empty do
L3      k ← |live|, C ← k(k − 1)/2, R ← (ρ/2) · Σ span(a) over a in live
L4      t ← t + an exponential time of rate C + R
L5      if a uniform number in [0, C + R) is below R then        ▷ recombination
L6          pick a in live with probability span(a)/Σ span, x uniform in the span of a
L7          RECOMBINE(a, x, t), and put its two lineages in place of a
L8      else pick a uniform pair a, b in live                    ▷ coalescence
L9          done ← (mat(a) ∩ mat(b)) − the material of the other live lineages
L10         w ← COALESCE(a, b, t), mat(w) ← (mat(a) ∪ mat(b)) − done
L11         remove a and b from live, and add w if mat(w) is not empty
```

The *span* of a lineage is the distance from the left end of its first material interval to the right end of its last one. Line L3 adds up the two kinds of rate: every pair coalesces at rate 1, and recombination falls uniformly on the span of each lineage. A breakpoint outside the span would leave one side with no material, so it is not simulated. Line L9 finds the positions whose last two carriers are $a$ and $b$. The node $w$ is the most recent common ancestor of the sample at those positions, and they leave the simulation.

**LOCAL-TREE$(x)$.** For each sample, follow its parents upward. At a recombination node with breakpoint $b$, take the left parent if $x < b$ and the right parent otherwise. The lowest node on all $n$ paths is the most recent common ancestor at $x$. The nodes of the tree are the samples and the coalescence nodes whose two child edges are both used by the paths. An equivalent test is that both child edges carry $x$ in their material.

**LOCAL-TREES.** The tree can change only at breakpoints. Sort the breakpoints, take one LOCAL-TREE inside each gap between them, and merge neighbouring gaps that have the same tree nodes.

## Example

Three samples $0, 1, 2$. Going back in time, sample 2 recombines at time $0.1$ with breakpoint $0.4$. Its left lineage carries $[0, 0.4)$ and its right lineage carries $[0.4, 1)$.

| node | kind | time | children | material above |
| --- | --- | --- | --- | --- |
| 0, 1, 2 | sample | 0 | none | $[0, 1)$ |
| 3 | recombination, breakpoint $0.4$ | $0.1$ | 2 | left $[0, 0.4)$, right $[0.4, 1)$ |
| 4 | coalescence | $0.2$ | 0, left of 3 | $[0, 1)$ |
| 5 | coalescence | $0.3$ | 1, right of 3 | $[0, 1)$ |
| 6 | coalescence | $0.9$ | 4, 5 | none |

At node 4, sample 0 carries all positions and the left lineage of 3 carries $[0, 0.4)$, so the new lineage carries $[0, 1)$. No position is done yet, because sample 1 still carries everything. The same holds at node 5. At node 6, both children carry all positions and no other lineage is left, so every position is done.

For a position $x < 0.4$, the path of sample 2 takes the left edge of node 3 and meets sample 0 at node 4. The marginal tree is $((0, 2), 1)$, with the cherry at time $0.2$ and the root at time $0.9$. For $x \ge 0.4$, the path of sample 2 takes the right edge and meets sample 1 at node 5, and the tree is $((1, 2), 0)$, with times $0.3$ and $0.9$. LOCAL-TREES returns the two intervals $[0, 0.4)$ and $[0.4, 1)$. In the first tree, node 5 has only one child edge that carries $x$ (the edge from sample 1), so it is a node of degree 2 on the path and is not a node of the tree.

## Correctness

The proof keeps one invariant for each position $x$: as long as the common ancestor at $x$ is not reached, the paths at $x$ end at the live lineages whose material holds $x$, and there are at least two of them. A recombination moves the paths at $x$ to the one new lineage that carries $x$. A coalescence of two carriers of $x$ joins their paths, and line L9 removes $x$ exactly when no third carrier is left, which is when the new node is the common ancestor at $x$. So the material on each edge is exactly the set of positions where the edge is a branch of the marginal tree, and both readings of LOCAL-TREE give the same binary tree. For the law, the number of carriers of $x$ does not change at a recombination, and each pair of carriers coalesces at rate 1. So the marginal tree at each position is a [Kingman coalescent](/kingman-coalescent/) tree, whatever $\rho$ is. The procedure stops with probability 1, by a comparison with the birth and death chain of Griffiths and Marjoram. The full proof is in the proof file of this page.

## Complexity

**Events.** The number $e$ of nodes is random. The recombinations that fall on the marginal tree at their breakpoint occur at rate $\rho/2$ per unit of tree length per unit of sequence. The expected length of a Kingman tree is $2\sum_{i=1}^{n-1} 1/i$, so their expected number is $\rho \sum_{i=1}^{n-1} 1/i$, about $\rho \ln n$. This also bounds the expected number of changes of the marginal tree along the sequence. Hudson's algorithm also simulates recombinations inside trapped material, the gaps between material intervals of one lineage. In the tests of this page, with 4 samples, their share grows with $\rho$: about 4% of all recombinations at $\rho = 4$ and more than half at $\rho = 64$. So $e$ grows faster than linearly in $\rho$.

**Per event.** Lines L3 and L6 take $O(k)$ time. Line L9 forms the union of the material of up to $k$ lineages, which takes $O(k s \log(k s))$ time with sorting. So the whole simulation takes $O(e\,k\,s \log(k s))$ time. A program that keeps the number of lineages that carry each position in a balanced search tree keyed by the breakpoints, as msprime does, avoids the union over all other lineages at line L9.

**Queries.** LOCAL-TREE follows $n$ paths. Each path has at most $e$ nodes, so a query takes $O(n e)$ time. LOCAL-TREES makes one query per gap between breakpoints. A sweep along the sequence that edits the tree at each breakpoint is faster, and this is how tree sequences are read.

**Space.** $O(e)$ nodes, plus the material lists, $O(e s)$ in all.

## Variants

- **The big ARG.** Griffiths and Marjoram keep every lineage, with or without material, and let each one recombine at rate $\rho/2$. The number of lineages is then a birth and death chain with birth rate $k\rho/2$ and death rate $k(k-1)/2$, and it stops at the ultimate ancestor, where one lineage is left. This graph is much larger than Hudson's, and its size grows very fast with $\rho$.
- **Along the sequence.** Wiuf and Hein (1999) build the same graph from left to right: start with a Kingman tree at position 0, then add one recombination at a time where the next breakpoint falls on the graph built so far.
- **Sequentially Markov coalescent.** McVean and Cardin (2005) keep only the current marginal tree as they move along the sequence, and forbid a lineage to coalesce back into a lineage that it is not ancestral to. The SMC' of Marjoram and Wall (2006) allows coalescence back into the same branch. The result is a Markov chain of trees, which is easy to fit with [hidden Markov models](/hidden-markov-model/).
- **Tree sequences.** msprime (Kelleher, Etheridge and McVean 2016) stores the output as a table of edges, each with the interval of positions on which it holds. It keeps the coalescence nodes and the edges of the marginal trees, but not the recombination nodes, and it is enough to recover every marginal tree.
- **Finite sites.** With $m$ loci and recombination only between them, the breakpoints are the $m - 1$ gaps, and the material is a set of loci.
- **Other models.** Population structure, changing population size, gene conversion and selection change the rates of lines L3 and L4 or add new kinds of events.

## When to use it

Use an ARG when a sample of sequences has recombined, so that no single tree explains all sites. It is the model behind coalescent simulation with recombination, likelihood methods for the recombination rate, and the [inference of ARGs](/ancestral-recombination-graph-inference/) from data. Use a single coalescent tree when the region is short enough that recombination can be ignored, which the [four-gamete test](/four-gamete-condition/) checks. Use a [phylogenetic network](/phylogenetic-network/) when the reticulations are between species, such as hybridization, and the times are not modelled. Use the sequentially Markov approximation for whole genomes, where the full ARG is too large.

## Pitfalls

- **Time units.** Some texts measure time in units of $2N$ generations and some in units of $4N$, and $\rho$ changes with them. The rates in line L3 hold for the unit in which a pair coalesces at rate 1.
- **Recombination on the span, not on the material.** A lineage can carry material on both sides of a gap. A breakpoint inside the gap still gives two lineages that both carry material, so Hudson's algorithm uses the span. Using only the length of the material gives too few recombinations.
- **Material at the common ancestor.** Removing the resolved positions at line L9 is what makes the procedure stop. Without it, the lineages keep recombining and the graph grows to the big ARG.
- **Equal trees.** A recombination can change the times of the marginal tree but not its shape, as always happens with two samples, or change nothing at all. Count trees by their nodes or by their shapes, and say which.
- **Not identifiable.** Many ARGs fit the same sequences. A recombination that leaves the tree unchanged leaves no trace in the data, so inferred graphs are estimates of one history.

## Implementations

## History

Hudson (1983) introduced the coalescent with recombination for a sequence with a continuum of positions, and simulated it backward in time with the ancestral material of each lineage, the method behind his later program ms. Griffiths and Marjoram (1996) used the graph of the sample history for likelihood inference by importance sampling, and in 1997 they gave it the name ancestral recombination graph and described the birth and death process of its lineages. Wiuf and Hein (1999) showed how to build it along the sequence. McVean and Cardin (2005) introduced the sequentially Markov approximation. Kelleher, Etheridge and McVean (2016) made Hudson's algorithm fast for large samples in msprime, with the output stored as a tree sequence.

## References
