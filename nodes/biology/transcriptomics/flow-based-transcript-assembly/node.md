---
tag: 9XQGWM
kind: algorithm
slug: flow-based-transcript-assembly
name: Flow-based transcript assembly
aliases:
- StringTie assembly
area: biology/transcriptomics
level: advanced
summary: 'Assemble transcripts from a splice graph: take the heaviest path of compatible reads, give it the max flow of its reads as abundance, remove that flow, and repeat.'
solves: [transcript-assembly]
model: word-ram
complexity:
  vars: {n: the number of nodes of the splice graph, E: the number of edges, F: the number of fragments, λ: the largest number of nodes in a fragment, R: "the number of rounds, at most W_0/c_min"}
  time: {worst: O(R·((n+E)·F·λ + n·(n+F)^2))}
  space: {extra: O(n + E + F·λ)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2015
  people: [Mihaela Pertea, Geo M. Pertea, Corina M. Antonescu, Tsung-Cheng Chang, Joshua T. Mendell, Steven L. Salzberg]
  note: StringTie built the heaviest path through the splice graph, computed its abundance as a maximum flow, removed the flow and repeated, so that assembly and quantification were done together.
prereqs: [transcript-assembly, splice-graph, max-flow-problem, flow-decomposition]
see_also: [minimum-path-cover-transcript-assembly, edmonds-karp, ford-fulkerson, min-cost-flow-problem, dag-longest-path, em-isoform-quantification, paired-end-reads, np-hard]
sources:
  - paper: doi:10.1038/nbt.3122
    title: Mihaela Pertea, Geo M. Pertea, Corina M. Antonescu, Tsung-Cheng Chang, Joshua T. Mendell and Steven L. Salzberg, StringTie enables improved reconstruction of a transcriptome from RNA-seq reads, Nature Biotechnology 33(3) (2015)
    locator: pp. 290 to 295, Online Methods (the splice graph, the heaviest path, the flow network and the removal of the flow)
  - paper: doi:10.1016/j.ejor.2006.05.043
    title: Benedicte Vatinlen, Fabrice Chauvet, Philippe Chrétienne and Philippe Mahey, Simple bounds and greedy algorithms for decomposing a flow into a minimal set of paths, European Journal of Operational Research 185(3) (2008)
    locator: pp. 1390 to 1401
  - paper: "Tzvika Hartman, Avinatan Hassidim, Haim Kaplan, Danny Raz and Michal Segalov, How to split a flow?, IEEE INFOCOM 2012"
    title: Tzvika Hartman, Avinatan Hassidim, Haim Kaplan, Danny Raz and Michal Segalov, How to split a flow?, Proceedings of IEEE INFOCOM 2012
    locator: pp. 828 to 836 (minimum flow decomposition is NP-hard even with the flow values 1, 2 and 4)
  - paper: doi:10.1038/nbt.4020
    title: Mingfu Shao and Carl Kingsford, Accurate assembly of transcripts through phase-preserving graph decomposition, Nature Biotechnology 35(12) (2017)
    locator: pp. 1167 to 1169
  - paper: doi:10.1145/321694.321699
    title: Jack Edmonds and Richard M. Karp, Theoretical improvements in algorithmic efficiency for network flow problems, Journal of the ACM 19(2) (1972)
    locator: pp. 248 to 264
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Part V, the chapter on transcriptomics (transcript assembly with network flows)
---

Flow-based transcript assembly builds transcripts and their abundances in one loop over the [splice graph](/splice-graph/) of a locus. It starts at the most covered node, grows the heaviest path of reads that agree with each other toward both ends, and computes how many reads the path can carry as a [maximum flow](/max-flow-problem/) through a small network of its reads. That flow is the abundance of the transcript. The flow is then removed from the reads, and the loop repeats until the coverage left is too low. This is the method of StringTie. It is a greedy heuristic: the underlying task, to split the coverage into the fewest weighted paths, is NP-hard, and the loop neither finds the fewest paths nor always finds the true ones.

## In plain words

Picture the splice graph as a set of roads, and each read as a car that drove along a short stretch. The busiest place is a good place to look for a real route.

Start there and walk backward and forward, each time choosing the next stretch that the most cars agree with. That gives one route. Now ask how many cars could have driven that whole route, piece by piece, without using any stretch more often than the cars on it allow. That number is how much of this transcript there is.

Take those cars away and look again for the busiest place. Stop when the roads are almost empty.

## The problem

The input is a splice graph $G$ on the nodes $1, \ldots, n$, with every edge $(u, v)$ having $u < v$, and a set of fragments. A fragment $f$ is the node path of a read or of a read pair, with at least two nodes, and a weight $w(f)$, its number of reads; reads on one node only are left out here. The coverage $W(v)$ of a node is the total weight of the fragments that hold it. The output is a list of paths with abundances, such that the abundances explain the weights well. This is a heuristic form of [transcript assembly](/transcript-assembly/), in which the exact goal would be a [flow decomposition](/flow-decomposition/) of the coverage into few paths.

Two definitions are used. A fragment $f$ is *compatible* with a path $Q$ if they share a node and agree on all the nodes between their common first and last ids. A fragment is *explained* by a path $P = (v_1, \ldots, v_m)$ if it is a contiguous part of $P$. The network $N(P)$ has a source $s$, a sink $t$, an edge $\mathrm{in}_i \to \mathrm{out}_i$ for each node $v_i$ with capacity $c_i$, the weight of the explained fragments that hold $v_i$, and an edge $\mathrm{out}_a \to \mathrm{in}_b$ with capacity $w(f)$ for each explained fragment $f = (v_a, \ldots, v_b)$. The edges $s \to \mathrm{in}_1$ and $\mathrm{out}_m \to t$ have no limit.

## The algorithm

```pseudo id=main
FLOW-ASSEMBLY(G, fragments with weights w, threshold c_min)
L1  T ← empty list
L2  while some node v has W(v) ≥ c_min do
L3      v* ← the node with the largest W, the smallest id on ties
L4      P ← (v*)
L5      repeat: prepend to P the predecessor u of first(P) with the largest positive weight of fragments that hold u and are compatible with u·P
L6      repeat: append to P the successor u of last(P) with the largest positive weight of fragments that hold u and are compatible with P·u
L7      (φ, g) ← a maximum flow of N(P), with g_f the flow through each explained fragment f
L8      if φ ≥ c_min then
L9          append (P, φ) to T, and set w(f) ← w(f) - g_f for each explained fragment f
L10     else set w(f) ← 0 for each fragment f that holds v*
L11 return T
```

Lines L3 to L6 build the heaviest path. Starting at the most covered node makes it likely that the path is the main isoform of the locus. The extension follows the reads: a neighbour gets the weight of only those fragments that fit the path built so far, so a read that took another splice choice upstream does not pull the path its way. Line L7 is the [Edmonds-Karp](/edmonds-karp/) algorithm on a network with $2m + 2$ nodes. A unit of flow goes from $v_1$ to $v_m$ through a chain of explained fragments, each one starting where the previous one ends, so $\varphi$ is the number of reads that the whole path can carry. Line L9 removes exactly the reads that the flow used. Line L10 is the escape when the heaviest path carries too little: the reads at $v^*$ are dropped, so the next round starts elsewhere.

The pseudocode numbers nodes from 1; the code numbers them from 0. The code is a small version of StringTie. It uses read counts where StringTie uses coverage per base, and it leaves out StringTie's bias factor on the node capacities, its use of read pairs, its filters for short or weak transcripts, and its strand and locus logic.

## Example

**One round at a time.** The nodes are A, B and C, with the edges $AB$, $BC$ and $AC$. The fragments are $AB$ with 30 reads, $BC$ with 30 and $AC$ with 10, and $c_{\min} = 1$.

| round | coverage $W$ (A, B, C) | path | network | $\varphi$ | weights after |
|---|---|---|---|---|---|
| 1 | 40, 60, 40 | start at B; prepend A (30 from $AB$; $AC$ skips B); append C (30 from $BC$) | $c_A = 30$, $c_B = 60$, $c_C = 30$; fragment edges $AB$ 30 and $BC$ 30 | 30 | $AB = 0$, $BC = 0$, $AC = 10$ |
| 2 | 10, 0, 10 | start at A, the smaller id; append C (10 from $AC$; B has no weight left) | $c_A = 10$, $c_C = 10$; fragment edge $AC$ 10 | 10 | all 0 |

The output is $ABC$ with 30 reads and $AC$ with 10. In round 1 the fragment $AC$ is not compatible with the path $AB$, because it jumps over B, so it does not add to the score of A.

**A case the loop gets wrong.** The true transcripts are $v_1 v_2 v_3 v_4 v_5$ with 10 reads on each junction and $v_1 v_3 v_5$ with 20, and every read covers one junction. The weights are 10 on $v_1 v_2$, $v_2 v_3$, $v_3 v_4$ and $v_4 v_5$, and 20 on $v_1 v_3$ and $v_3 v_5$. The loop starts at $v_3$ with $W = 60$. Both predecessors score 20, and the tie goes to $v_1$; the successors also tie, and $v_4$ wins. The first path is $v_1 v_3 v_4 v_5$ with $\varphi = 10$, which is not a true transcript. Then come $v_1 v_2 v_3 v_5$ with 10 and $v_1 v_3 v_5$ with 10. The three paths explain every read, as the two true ones do. One read that covers $v_2 v_3 v_4$ links the two choices, and then the loop returns $v_1 v_3 v_5$ with 20 and $v_1 v_2 v_3 v_4 v_5$ with 10. The test file checks both outputs.

## Correctness

[The proof](proofs/correctness.md) shows what holds for the loop and what does not. Every path is a path of $G$ with at least two nodes. The maximum flow splits into chains of explained fragments from the first node to the last, so $\varphi$ never exceeds the reads that the path can carry, the weights never go below 0, and the sum of all abundances is at most the number of reads. Each round removes at least $c_{\min}$ of weight, so the loop stops after at most $W_0 / c_{\min}$ rounds, where $W_0$ is the total weight, with every node below $c_{\min}$. These are theorems. That the paths are the true transcripts is not one: the second example is a counterexample, and with junction reads only no method can decide it.

## Complexity

The word RAM, with $n$ nodes, $E$ edges, $F$ fragments of at most $\lambda$ nodes, and $R \le W_0 / c_{\min}$ rounds.

- Lines L2 and L3: the coverage of all nodes, $O(n F \lambda)$ as the code computes it, or $O(F \lambda)$ with a running count.
- Lines L5 and L6: each step scores the neighbours of one end, and each score checks every fragment in $O(\lambda)$. Over all steps of a round that is $O((n + E) F \lambda)$.
- Line L7: $N(P)$ has $2m + 2 \le 2n + 2$ nodes and $m + F + 2$ edges. Edmonds-Karp costs $O(|V| |E|^2) = O(n (n + F)^2)$.

The total is $O(R \cdot ((n + E) F \lambda + n (n + F)^2))$ time and $O(n + E + F \lambda)$ space. The bound is loose. A locus has tens of nodes and few rounds, and the max flow on a path network is fast in practice.

## Properties

- **A heuristic.** It returns a decomposition, not the fewest paths and not always the true paths (Section 4 of the proof).
- **Assembly and quantification together.** Each transcript comes with its abundance from line L7, and later transcripts see only the reads that earlier ones did not use.
- **Terminates.** At most $W_0 / c_{\min}$ rounds, a theorem.
- **Never overspends reads.** The abundances add up to at most the number of reads, a theorem.
- **Order-dependent.** The first path takes its reads first. A different start or tie rule gives a different output.

## Variants and improvements

- **StringTie.** Coverage per base on the nodes and the reads, a bias factor on the node capacities, read pairs joined into longer fragments, and filters that drop transcripts with too little coverage or too short a length.
- **Scallop.** Shao and Kingsford (2017) decompose the splice graph flow while they keep *phasing paths*, the paths that single reads or pairs cover, so that the choices at two splice sites stay linked.
- **Minimum flow decomposition.** The exact problem: split a flow into the fewest weighted source-to-sink paths. It is NP-hard in the strong sense, even on DAGs (Vatinlen, Chauvet, Chrétienne and Mahey 2008), and stays NP-hard with the flow values 1, 2 and 4 (Hartman, Hassidim, Kaplan, Raz and Segalov 2012). Greedy rules such as the widest path first are the usual approximations.
- **Min-cost flow formulations.** Methods in the book of Mäkinen, Belazzougui, Cunial and Tomescu (2015) fit a flow to noisy coverage with a [min-cost flow](/min-cost-flow-problem/) and then decompose it.
- **Path covers.** Without weights, the fewest transcripts that explain all reads come from [minimum path cover assembly](/minimum-path-cover-transcript-assembly/), as in Cufflinks.

## When to use it

Use it for genome-guided assembly of short reads, when the isoforms of a gene have very different abundances: the coverage separates them, which a path cover cannot do. StringTie reported more complete and accurate assemblies than Cufflinks and other assemblers on simulated and real data, which is a measurement on benchmarks, not a guarantee. If reads or pairs are long enough to span several splice sites, a method that keeps phasing paths, such as Scallop, uses that information better. Without a genome, use [de novo transcriptome assembly](/de-novo-transcriptome-assembly/). If only the abundances of known transcripts are needed, skip assembly and use [EM quantification](/em-isoform-quantification/).

## Pitfalls

- **Scoring all fragments in line L5.** If the extension counts every fragment at $u$, not only those compatible with $u \cdot P$, a read that jumps over the path pulls it the wrong way, as $AC$ would in the first example. Count only compatible fragments.
- **Taking the coverage as the abundance.** The weight at the start node $v^*$ includes the reads of other isoforms. The abundance is the flow $\varphi$ of line L7, which is limited by the weakest part of the path.
- **Missing line L10.** If the heaviest path carries less than $c_{\min}$, nothing is removed and the loop repeats forever. Drop the reads at $v^*$, or mark $v^*$ as done.
- **Trusting unphased paths.** With junction reads only, a path can mix the choices of two transcripts, as in the second example. Paths through two or more splice choices need reads or pairs that span both.
- **Overlapping fragments in $N(P)$.** In the network a unit of flow moves from a fragment to one that starts exactly where it ends. Two explained fragments that overlap in more than one node cannot both carry the same read flow, so some weight stays behind and can come back as a short extra path. The toy keeps this limit.

## Implementations

## History

Edmonds and Karp (1972) gave the shortest augmenting path rule for maximum flow. Vatinlen, Chauvet, Chrétienne and Mahey (2008) studied the decomposition of a flow into the fewest paths and greedy algorithms for it, and Hartman, Hassidim, Kaplan, Raz and Segalov (2012) showed that it stays hard for small flow values. Pertea, Pertea, Antonescu, Chang, Mendell and Salzberg (2015) combined the heaviest path and maximum flow in StringTie, so that assembly and quantification were done in one loop. Shao and Kingsford (2017) added phasing paths to the flow decomposition in Scallop.

## References
