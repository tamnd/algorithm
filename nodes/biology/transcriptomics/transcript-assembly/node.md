---
tag: JT0ZD8
kind: problem
slug: transcript-assembly
name: Transcript assembly
aliases:
- isoform reconstruction
area: biology/transcriptomics
level: core
summary: 'Reconstruct the full-length transcripts and isoforms of each gene, and often their abundances, from RNA-seq reads aligned to a genome, as paths through a splice graph.'
prereqs: [spliced-read-alignment, splice-graph]
see_also: [minimum-path-cover-transcript-assembly, flow-based-transcript-assembly, de-novo-transcriptome-assembly, transcript-abundance-estimation, minimum-path-cover-problem, flow-decomposition, genome-assembly-problem, np-hard]
sources:
  - paper: doi:10.1038/nbt.1621
    title: Cole Trapnell, Brian A. Williams, Geo Pertea, Ali Mortazavi, Gordon Kwan, Marijke J. van Baren, Steven L. Salzberg, Barbara J. Wold and Lior Pachter, Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation, Nature Biotechnology 28(5) (2010)
    locator: pp. 511 to 515, Online Methods (the fewest transcripts that explain the fragments)
  - paper: doi:10.1038/nbt.3122
    title: Mihaela Pertea, Geo M. Pertea, Corina M. Antonescu, Tsung-Cheng Chang, Joshua T. Mendell and Steven L. Salzberg, StringTie enables improved reconstruction of a transcriptome from RNA-seq reads, Nature Biotechnology 33(3) (2015)
    locator: pp. 290 to 295, Online Methods (heaviest paths and maximum flow)
  - paper: doi:10.1038/nbt.4020
    title: Mingfu Shao and Carl Kingsford, Accurate assembly of transcripts through phase-preserving graph decomposition, Nature Biotechnology 35(12) (2017)
    locator: pp. 1167 to 1169
  - paper: doi:10.1093/bioinformatics/18.suppl_1.S181
    title: Steffen Heber, Max Alekseyev, Sing-Hoi Sze, Haixu Tang and Pavel A. Pevzner, Splicing graphs and EST assembly problem, Bioinformatics 18(Suppl 1) (2002)
    locator: pp. S181 to S188
  - paper: doi:10.1186/1471-2105-15-S9-S5
    title: Romeo Rizzi, Alexandru I. Tomescu and Veli Mäkinen, On the complexity of minimum path cover with subpath constraints for multi-assembly, BMC Bioinformatics 15(Suppl 9) (2014)
    locator: Article S5 (subpath constraints in polynomial time; pairs of subpaths are NP-hard)
  - paper: doi:10.1093/comjnl/bxu116
    title: Niko Beerenwinkel, Stefano Beretta, Paola Bonizzoni, Riccardo Dondi and Yuri Pirola, Covering pairs in directed acyclic graphs, The Computer Journal 58(7) (2015)
    locator: pp. 1673 to 1686
  - paper: doi:10.1016/j.ejor.2006.05.043
    title: Benedicte Vatinlen, Fabrice Chauvet, Philippe Chrétienne and Philippe Mahey, Simple bounds and greedy algorithms for decomposing a flow into a minimal set of paths, European Journal of Operational Research 185(3) (2008)
    locator: pp. 1390 to 1401
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Part V, the chapter on transcriptomics (transcript assembly as path cover and flow problems)
---

Transcript assembly rebuilds the full-length transcripts of the genes in a sample from short [RNA-seq](/rna-sequencing/) reads. In the genome-guided form, the reads are first placed on the genome by [spliced read alignment](/spliced-read-alignment/). The aligned reads of one gene give a [splice graph](/splice-graph/), in which every transcript is a path from a start to an end, and every read is a short piece of such a path. The task is to choose a small set of paths, often with an abundance for each, that explains the reads. The reads are short and many isoforms share exons, so the reads usually fit many sets of paths. Every exact formulation therefore adds a rule, such as the fewest paths, and the natural weighted rule is NP-hard. Cufflinks and StringTie are the two classic methods.

## In plain words

A gene is a row of building blocks. Each version of its message takes some of the blocks, in order, and skips the others. You never see a whole message. You see only short pieces, each of which shows one, two or three blocks next to each other.

The task is to guess the full messages from the pieces. A piece that shows blocks 1 and 3 next to each other tells you that some message skips block 2. But two pieces that each show two blocks do not tell you whether they came from the same message.

So many guesses fit the same pieces. Methods choose the guess with the fewest messages, or the guess whose message counts fit the number of pieces best.

## Definition

**Input.** A splice graph $G = (V, E)$, a directed acyclic graph whose nodes are exon segments in genome order, with a source $s$ and a sink $t$ added at the starts and ends of transcripts. A set of fragments, each a path of $G$ (one read, or a read pair whose gap has one possible filling), or a pair of paths (a read pair whose gap is unknown). Optionally, a weight on each node, edge or fragment: the number of reads.

**Output.** A set of $s$-$t$ paths $P_1, \ldots, P_k$, the transcripts, and optionally an abundance $a_i \ge 0$ for each. Every fragment must be *explained*: contained as a subpath in some $P_i$, or both of its parts in one $P_i$ for a pair.

**Objectives.** The reads alone do not fix the answer, so each formulation adds one.

- **Minimum path cover.** The fewest paths that explain all fragments. Unweighted. This is the formulation of Cufflinks; see [minimum path cover assembly](/minimum-path-cover-transcript-assembly/).
- **Minimum flow decomposition.** The edge weights form a flow from $s$ to $t$ (or nearly so, with noise), and the task is the fewest weighted paths whose weights add up to the flow on every edge. See [flow decomposition](/flow-decomposition/).
- **Best fit with few paths.** Choose paths and abundances that fit the observed coverage under a noise model, with a penalty on the number of paths. StringTie's greedy loop is a heuristic for a fit of this kind; see [flow-based assembly](/flow-based-transcript-assembly/).

The problem is the multi-path form of [genome assembly](/genome-assembly-problem/): there, one string must explain all reads, and here several paths in one small graph must.

## Variants

- **Genome-guided or de novo.** With a genome, the splice graph comes from the alignments. Without one, the graph is built from the reads themselves, usually as a de Bruijn graph; see [de novo transcriptome assembly](/de-novo-transcriptome-assembly/).
- **Reference-annotation guided.** Known transcripts are given and kept as candidates, and the assembler adds new ones only where the reads demand them.
- **Short reads, pairs and long reads.** Longer fragments span more splice choices and so leave less ambiguity. Full-length long reads make assembly almost a matter of grouping reads, but they have more errors and fewer reads per transcript.
- **With or without abundances.** Some formulations return only the transcripts and leave the abundances to [abundance estimation](/transcript-abundance-estimation/) afterwards; others, such as StringTie, compute both together.
- **Phasing paths.** Scallop of Shao and Kingsford (2017) keeps the paths covered by single reads or pairs as constraints while it decomposes the flow, so that linked splice choices stay linked.

## Examples

**Two path covers of the same reads.** Let the splice graph have nodes $v_1, \ldots, v_5$ in genome order and the edges $v_1 v_2$, $v_2 v_3$, $v_3 v_4$, $v_4 v_5$, $v_1 v_3$ and $v_3 v_5$, so that exons 2 and 4 can each be skipped. The true transcripts are $T_1 = v_1 v_2 v_3 v_4 v_5$ with 10 reads per junction and $T_2 = v_1 v_3 v_5$ with 20, and each read covers one junction.

| answer | paths | explains every junction | edge weights fit |
|---|---|---|---|
| truth | $v_1 v_2 v_3 v_4 v_5$ (10), $v_1 v_3 v_5$ (20) | yes | yes |
| swapped | $v_1 v_2 v_3 v_5$, $v_1 v_3 v_4 v_5$ | yes | no two weights fit |
| three paths | $v_1 v_2 v_3 v_5$ (10), $v_1 v_3 v_4 v_5$ (10), $v_1 v_3 v_5$ (10) | yes | yes |

The minimum path cover has size 2, and both the truth and the swapped pair reach it, so the unweighted objective cannot choose. The weights decide here. A 2-path flow decomposition must use $v_1 v_2$ in one path of weight 10 and $v_1 v_3$ in the other of weight 20. The path of weight 20 cannot use $v_3 v_4$, which carries only 10, so it ends with $v_3 v_5$, and the other path must then take $v_3 v_4$. So the truth is the only flow decomposition into 2 paths. The three-path answer also fits the weights but uses one path more. A single read that spans $v_2 v_3 v_4$ would rule out the swapped pair even without weights.

**Too many candidates to list.** A gene with $k$ cassette exons, each of which can be included or skipped on its own, has a splice graph that is a chain with a skip edge over each such exon. It has $2^k$ source-to-sink paths, so 1024 candidate isoforms for $k = 10$. Methods that list all paths and then choose among them, as some early tools did, do not scale to such genes. Path covers and flows work on the graph and never list the paths.

## Known algorithms

- **Minimum path cover by bipartite matching (Cufflinks).** Trapnell and colleagues (2010) order the fragments of a locus by compatibility and find the fewest chains with a constructive proof of [Dilworth's theorem](/dilworth-theorem/), a maximum [bipartite matching](/bipartite-matching/). It is exact for the minimum path cover with single subpaths. See [minimum path cover assembly](/minimum-path-cover-transcript-assembly/).
- **Heaviest path and max flow (StringTie).** Pertea and colleagues (2015) take the heaviest path of compatible reads, give it the maximum flow of its reads as its abundance, remove that flow, and repeat. It is a greedy heuristic. See [flow-based assembly](/flow-based-transcript-assembly/).
- **Phase-preserving decomposition (Scallop).** Shao and Kingsford (2017) decompose the splice graph flow while they keep the phasing paths of reads and pairs.
- **Sparse fitting.** Other tools list candidate paths and choose a few by a regression with a sparsity penalty. These are heuristics, and the candidate list is the limit, as in the second example.
- **De novo graphs.** Trinity and other de novo assemblers build the graph from [k-mers](/kmer/) and then find paths in it with read support; see [de novo transcriptome assembly](/de-novo-transcriptome-assembly/).

## Bounds

- **Single subpaths: polynomial.** The fewest paths that explain a set of fragments, each a single path of a DAG, can be found in polynomial time: by a reduction to the classical minimum path cover (Rizzi, Tomescu and Mäkinen 2014), and in the Cufflinks form by bipartite matching on the compatibility order, which is a theorem by Dilworth's theorem. See the [minimum path cover problem](/minimum-path-cover-problem/).
- **Pairs of subpaths: NP-hard.** When a constraint is a pair of subpaths that must lie on the same path, as for read pairs with an unknown gap, the minimum path cover is NP-hard (Rizzi, Tomescu and Mäkinen 2014), and deciding whether three paths are enough is already NP-hard (Beerenwinkel, Beretta, Bonizzoni, Dondi and Pirola 2015).
- **Minimum flow decomposition: NP-hard.** Splitting a flow on a DAG into the fewest weighted paths is NP-hard in the strong sense (Vatinlen, Chauvet, Chrétienne and Mahey 2008). Greedy rules give decompositions but not always the fewest paths.
- **Identifiability.** The first example shows that the reads, even with exact weights, may fit several answers, and that more answers fit when the weights are dropped. No algorithm can return the truth in such cases; this is a property of the data, not of the methods.

## Reductions

- **To minimum path cover.** With single-path fragments, transcript assembly reduces to the minimum path cover of a DAG, and then to a maximum matching in a bipartite graph built from the reachability of the fragments.
- **To flow decomposition.** With edge weights, it reduces to the decomposition of a flow into weighted paths.
- **From the set of reads to a graph.** The construction of the [splice graph](/splice-graph/) from alignments is the step that turns reads into a graph problem; for de novo assembly the [de Bruijn graph](/de-bruijn-graph/) plays the same role.
- **To quantification.** Once the transcripts are known, finding their abundances is [transcript abundance estimation](/transcript-abundance-estimation/), solved by maximum likelihood with [EM](/em-isoform-quantification/).

## Applications

- Finding new isoforms, exons and genes that a gene annotation does not have.
- Building annotations for newly sequenced genomes from RNA-seq.
- Comparing isoform use between tissues, cell types or conditions, as Cufflinks did for the differentiation of mouse muscle cells.
- Finding abnormal transcripts in disease samples, such as those from mutations at splice sites in cancer.

## References
