---
tag: W66F43
kind: problem
slug: assembly-graph-simplification
name: Assembly graph simplification
aliases:
- graph cleaning
- assembly graph cleaning
area: biology/genome-assembly
level: core
summary: Remove the tips, bubbles and low-coverage edges that read errors add to an assembly graph, so that the unitigs get longer. All rules in use are heuristics that can also delete true sequence.
prereqs: [de-bruijn-assembly, unitig, kmer-spectrum]
see_also: [tip-removal, bubble-popping, read-error-correction, contig, genome-repeat, string-graph, poisson-distribution, sequencing-coverage]
sources:
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829 (tip removal, the Tour Bus algorithm, the coverage cutoff for erroneous connections, and their order)
  - paper: doi:10.1089/cmb.2012.0021
    title: Anton Bankevich and others, SPAdes, a new genome assembly algorithm and its applications to single-cell sequencing, Journal of Computational Biology 19(5) (2012)
    locator: pp. 455 to 477, Section 8 (tip clipping, chimeric edge removal, bulge removal in increasing order of coverage)
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753, Error Correction and Data Corruption (the vertex counts of the N. meningitidis graph before and after error correction)
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602, Introduction (simplification steps are heuristics whose properties are hard to prove)
---

Assembly graph simplification is the clean-up step between building an assembly graph and reading contigs from it. Read errors add many false $k$-mers to a [de Bruijn graph](/de-bruijn-graph/). Each one makes a branch, and each branch ends a [unitig](/unitig/), so without clean-up the contigs are short. The usual rules delete short dead ends ([tips](/tip-removal/)), one side of short parallel paths ([bubbles](/bubble-popping/)), and edges whose coverage is much lower than that of their neighbors (chimeric or erroneous connections). None of these rules is safe: for each one there is an input on which it deletes true sequence, and for some inputs no rule can tell an error from a true variant.

## In plain words

You build the assembly graph from the reads, and each read error adds a small false piece to it. A false piece near the end of a read sticks out as a short dead end. A false piece in the middle of a read makes a short detour next to the true path. A read that joins two far parts of the genome makes a thin false bridge.

Simplification removes these pieces, so that the true paths have no forks and become long contigs. The clues are length and coverage: the false pieces are short and few reads support them. But true pieces can also be short and weakly supported, for example at the end of a chromosome, at a place where the two copies of a chromosome differ, or in a region that the machine reads badly. So each rule is a guess.

## Definition

The genome $S$ has length $G$. There are $N$ reads of length $L$, so the coverage is $c = NL/G$, and each letter of a read is wrong with a small probability. The **assembly graph** $H$ is the edge-centric de Bruijn graph of order $k$ of the reads, with a count on each edge. The **true graph** $H^*$ is the de Bruijn graph of the $k$-mers of $S$. If the reads cover $S$, each edge of $H^*$ is in $H$, and the other edges of $H$ come from errors.

The goal is a subgraph $H' \subseteq H$ that is as close as possible to $H^*$: it keeps each edge of $H^*$ and deletes each false edge. The assembler does not know $H^*$, so it uses rules that look at the shape of the graph and the counts. A rule is **sound** if it never deletes an edge of $H^*$. The standard rules are:

1. **Count threshold.** Delete each $k$-mer with count below $t$.
2. **Tip removal.** Delete a short unitig that ends in a dead end and has a lower count at its junction than another branch there.
3. **Bubble popping.** If two short paths of similar length join the same two vertices, delete the one with lower coverage.
4. **Erroneous connection removal.** Delete an edge or unitig whose coverage is much lower than the coverage of the paths next to it, or below a global cutoff.

The problem is not a single optimization problem, because the error model and the genome are not known. It is usually studied as a set of rules, their order, and their failure cases.

## Variants

- **By graph.** The same rules work on the de Bruijn graph and on the [string graph](/string-graph/) of long reads. The string graph also needs transitive reduction, which removes the overlaps implied by two shorter ones.
- **By goal.** A haploid consensus pops all bubbles. A diploid or metagenome assembly keeps bubbles and reports them as variants.
- **By order.** Velvet runs tip removal, then the Tour Bus bubble merge, then a coverage cutoff for erroneous connections. SPAdes interleaves tip clipping, bulge removal and chimeric edge removal and processes edges in increasing order of coverage.
- **Before the graph.** [Read error correction](/read-error-correction/) fixes the reads before the graph is built, as in EULER. The graph then has fewer false branches, and the graph rules have less to do.

## Examples

**How many false vertices.** Pevzner, Tang and Waterman report for the *N. meningitidis* project, with 20-tuples, that the graph of the error-free data has 4,039,248 vertices, and the graph of the real reads has 9,474,411. After their error correction the count is 4,081,857. So more than half of the vertices of the raw graph came from errors.

**A count threshold loses true k-mers.** A true $k$-mer is covered by a read that starts in a window of $L - k + 1$ positions, so its count is close to a Poisson variable with mean $c_k = c(L-k+1)/L$. Take $G = 5{,}000{,}000$, $L = 100$, $k = 31$ and $t = 2$, so each $k$-mer with count 0 or 1 is deleted.

| coverage $c$ | $c_k$ | $P(\text{count} \le 1) = e^{-c_k}(1 + c_k)$ | expected true $k$-mers lost |
|---|---|---|---|
| 10 | 7 | 0.00730 | about 36,000 |
| 30 | 21 | $1.7 \times 10^{-8}$ | about 0.08 |

At coverage 10 the threshold makes thousands of gaps in the true graph. At coverage 30 it is safe in this model. Real coverage is not uniform, so low-coverage regions behave like the first row.

**Each rule can delete a true sequence.**

| rule | false target | true sequence it can delete |
|---|---|---|
| tip removal | error in the last $k - 1$ letters of a read | the end of a linear chromosome after a repeat, or a region next to a coverage gap |
| bubble popping | error at least $k - 1$ letters from both read ends | the lower-coverage allele at a heterozygous site, or one of two repeat copies that differ in one letter |
| coverage cutoff | chimeric read that joins two far parts of the genome | a true region with low coverage, such as a region with extreme GC content |

The [tip removal](/tip-removal/) and [bubble popping](/bubble-popping/) pages give exact small inputs for the first two rows.

**The same reads from two genomes.** Let $h_1 = \mathtt{GATTACAGGCTCAAGTCCGA}$ and let $h_2$ be $h_1$ with the letter at index 10 changed from $\mathtt{T}$ to $\mathtt{G}$. Take six reads of length 10 from $h_1$ at positions 0, 2, 4, 6, 8, 10, and four reads from $h_2$ at positions 1, 4, 7, 10. Each of the four $h_2$ reads covers index 10, so it is also the $h_1$ read at the same position with one error at index 10. So the same ten reads can come from a diploid genome $(h_1, h_2)$ with no errors, or from the haploid genome $h_1$ with four errors at one site. The assembly graph and its counts are the same in both cases.

## Known algorithms

- **[Tip removal](/tip-removal/).** Velvet removes tips shorter than $2k$ with a minority count at the junction, in increasing order of count. An error near a read end makes a tip of at most $k - 1$ edges.
- **[Bubble popping](/bubble-popping/).** Velvet's Tour Bus merges paths of fewer than 200 nodes, shorter than 100 bp and at least 80% similar. SPAdes removes short bulges and projects their coverage onto the kept path. An error inside a read makes a bubble of two $k$-edge paths whose strings differ in one letter.
- **Coverage cutoff.** After tips and bubbles, Velvet removes the nodes below a coverage cutoff chosen by the user, to cut erroneous connections. Choosing it from the valley of the [k-mer spectrum](/kmer-spectrum/) is the common practice.
- **Chimeric edge removal.** SPAdes removes an edge whose coverage is low compared with the edges next to it. This targets the false bridges of chimeric reads, which can join any two parts of the genome.
- **Isolated short paths.** Assemblers drop short components that touch nothing else, which come from contamination or from reads full of errors.

The cost of each step depends on how far its search may go from a junction; the pages on [tip removal](/tip-removal/) and [bubble popping](/bubble-popping/) give the bounds for simple implementations.

## Bounds

**No rule that sees only the graph and the counts is sound and also removes all errors.** The proof is the example of the same reads from two genomes. A deterministic rule maps the graph with its counts to a subgraph. On the input of that example, either it keeps both sides of the bubble, and then the haploid assembly keeps the four error $k$-mers, or it deletes one side, and then for the diploid genome it deletes a true $k$-mer. So no rule can be right for both genomes. The same argument works for any rule that sees the reads themselves, because the reads are also the same.

**Rules can only be right with some probability.** Under the Poisson model, a true $k$-mer has a count near $c_k$, and an error $k$-mer has a count near 1 unless the same error occurs in many reads. So when $c_k$ is large, a rule that compares counts makes errors with small probability. The table above shows how fast this improves with $c$. Uneven coverage, heterozygosity and repeats break the model, and then no fixed threshold works for the whole genome.

**Outside the safe model.** Tomescu and Medvedev describe the strings that every genome with the given graph must contain, under a model without errors. Simplification is the step that changes the graph to make that model fit, so its results are not covered by their guarantees.

## Reductions

- **To [read error correction](/read-error-correction/).** If each read is corrected, the graph of the corrected reads is close to $H^*$, and simplification has little to do. Read error correction faces the same ambiguity: a $k$-mer with a low count can be an error or a rare true variant.
- **To [consensus sequence calling](/consensus-sequence-calling/).** Popping a bubble and keeping the side with more reads is a majority vote at that site, which is a consensus call.
- **To shortest paths.** The search for the other side of a bubble is a [shortest path](/single-source-shortest-paths/) search bounded by a length, usually by [Dijkstra's algorithm](/dijkstra/) or a [breadth-first search](/breadth-first-search/).

## Applications

Every de Bruijn assembler for short reads simplifies its graph before it outputs contigs: Velvet, SPAdes, ABySS and SOAPdenovo all do. Long-read assemblers apply the same tip and bubble rules to the string graph. Variant-aware assemblers turn the rules around: they find bubbles in order to report the variants inside them, instead of deleting them.

## References
