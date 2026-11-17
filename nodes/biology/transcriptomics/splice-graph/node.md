---
tag: 7RCBRT
kind: data-structure
slug: splice-graph
name: Splice graph
aliases:
- splicing graph
area: biology/transcriptomics
level: core
summary: A DAG of the exon segments of a gene locus, with an edge for each junction seen in the reads. Each transcript is a path, but not every path is a transcript.
prereqs: [rna-sequencing, spliced-read-alignment, directed-acyclic-graph]
see_also: [transcript-assembly, flow-based-transcript-assembly, minimum-path-cover-transcript-assembly, de-bruijn-graph, string-graph, topological-sort, dag-longest-path, sam-alignment-format]
sources:
  - paper: doi:10.1093/bioinformatics/18.suppl_1.S181
    title: Steffen Heber, Max Alekseyev, Sing-Hoi Sze, Haixu Tang and Pavel A. Pevzner, Splicing graphs and EST assembly problem, Bioinformatics 18(Suppl 1) (2002)
    locator: pp. S181 to S188 (the splicing graph; each transcript is a path in it)
  - paper: doi:10.1038/nbt.3122
    title: Mihaela Pertea, Geo M. Pertea, Corina M. Antonescu, Tsung-Cheng Chang, Joshua T. Mendell and Steven L. Salzberg, StringTie enables improved reconstruction of a transcriptome from RNA-seq reads, Nature Biotechnology 33(3) (2015)
    locator: pp. 290 to 295, Online Methods (the alternative splice graph with a source and a sink, built from spliced alignments)
  - paper: doi:10.1038/nbt.4020
    title: Mingfu Shao and Carl Kingsford, Accurate assembly of transcripts through phase-preserving graph decomposition, Nature Biotechnology 35(12) (2017)
    locator: pp. 1167 to 1169 (a weighted splice graph with phasing paths)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Part V, the chapter on transcriptomics (splicing graphs, path covers and flows)
---

A splice graph is a directed acyclic graph that holds all the ways a gene was seen to splice in a sample. Its nodes are the segments of the genome that the reads cover, cut at every splice site, and its edges join a segment to the next one along a read, either directly or across an intron. Every transcript that the reads came from is a path of the graph, and the [transcript assembly](/transcript-assembly/) problem is to pick the right paths and their abundances. Heber, Alekseyev, Sze, Tang and Pevzner (2002) introduced the splicing graph for EST data, and genome-guided assemblers such as StringTie build one from [spliced read alignments](/spliced-read-alignment/).

## In plain words

Think of a gene as a road with optional parts. Some parts are always used, some are skipped by some copies of the message, and some start a little later than others.

Cut the road at every place where a read jumps away or lands. Each piece between two cuts is a node. Draw an arrow from one piece to the next whenever some read goes from the first to the second, either by running straight on or by jumping over an intron.

Each message that the cell made is now a route through the arrows. The graph also allows routes that mix the choices of different messages, so a route is a candidate, not a proof.

## The abstract type

A splice graph of one locus on one strand is a [directed acyclic graph](/directed-acyclic-graph/) $G = (V, E)$ with an interval of the genome on each node. It supports these operations:

- BUILD(alignments): make the graph from a set of spliced alignments.
- PATH-OF(alignment): the list of nodes that an alignment passes through.
- COUNT-PATHS(): the number of paths from a source (a node with no predecessor) to a sink (a node with no successor).
- PATHS(): the list of these paths.
- SPELL(path): the exons of a path, with touching nodes merged.

Weighted versions also store the number of reads on each node and on each edge, which is the input of [flow-based assembly](/flow-based-transcript-assembly/) and [path cover assembly](/minimum-path-cover-transcript-assembly/).

## Representation

The page uses 1-based closed intervals, as in SAM and GFF; the code uses 0-based half-open intervals, so the page's $201..250$ is $[200, 250)$ in the code. An alignment is a list of blocks, the parts between the N operations of its CIGAR. The gap between two blocks is an intron: its *donor* is the last base of the block before it and its *acceptor* is the first base of the block after it.

The fields are a sorted array of node intervals, a successor and a predecessor list for each node, and the sorted list of introns. The invariants: the node intervals are disjoint and in coordinate order; no donor and no acceptor is strictly inside a node, so a junction always leaves from the end of a node and lands at the start of a node; and every edge goes from a node to a node further right. The last invariant makes the coordinate order a [topological order](/topological-sort/).

## Operations

```pseudo id=main
BUILD(alignments)
L1  B ← all blocks of all alignments; I ← all introns (donor, acceptor) of all alignments
L2  C ← the donors and the acceptors in I
L3  U ← the union of B as maximal covered intervals, in coordinate order
L4  V ← the intervals of U cut at each point of C strictly inside them, in order
L5  for each block in B: add an edge between each pair of consecutive nodes that the block overlaps
L6  for each intron (d, a) in I: add an edge from the node that ends at d to the node that starts at a
L7  return (V, E)
```

Line L4 makes the cuts that line L6 needs: every donor ends a node and every acceptor starts one. Line L5 joins the nodes that one block runs through. A covered region that holds no splice site stays one node, however many reads cover it. With the cuts sorted, BUILD costs $O((|B| + |I|) \log(|B| + |I|))$ time plus the total length of the paths of the blocks.

```pseudo id=pathof
PATH-OF(alignment)
P1  P ← empty list
P2  for each block [s..e] of the alignment, in order:
P3      append the nodes that overlap [s..e], in order, by binary search for s in the node starts
P4  return P
```

PATH-OF costs $O(r \log |V| + |P|)$ for an alignment with $r$ blocks. It is how a read becomes a subpath constraint for the assemblers.

```pseudo id=count
COUNT-PATHS()
C1  for v ← 1 to |V| do
C2      w(v) ← 1 if v has no predecessor, else the sum of w(u) over the edges (u, v)
C3  return the sum of w(v) over the nodes v with no successor
```

COUNT-PATHS costs $O(|V| + |E|)$. PATHS lists the paths by depth-first search from each source, in time proportional to the total length of its output. The count can be exponential: a gene with $k$ exons that can each be skipped independently has $2^k$ paths.

## Example

A gene has the exons E1 = $1..100$, E2 = $201..300$ and E3 = $401..500$, and E2 has a second acceptor at 251. Three transcripts are expressed: $t_1$ = E1, E2, E3; $t_2$ = E1, $251..300$, E3; and $t_3$ = E1, E3, which skips E2. Their full-length alignments are the input of BUILD.

| step | state |
|---|---|
| L1 | introns, as (donor, acceptor): (100, 201), (300, 401), (100, 251), (100, 401) |
| L2 | splice sites: donors 100 and 300, acceptors 201, 251 and 401 |
| L3 | covered intervals: $1..100$, $201..300$, $401..500$ |
| L4 | nodes: $v_1 = 1..100$, $v_2 = 201..250$, $v_3 = 251..300$, $v_4 = 401..500$ |
| L5 | the block $201..300$ of $t_1$ runs through $v_2$ and $v_3$: edge $(v_2, v_3)$ |
| L6 | junction edges $(v_1, v_2)$, $(v_3, v_4)$, $(v_1, v_3)$, $(v_1, v_4)$ |

COUNT-PATHS gives $w(v_1) = 1$, $w(v_2) = 1$, $w(v_3) = w(v_1) + w(v_2) = 2$, $w(v_4) = w(v_1) + w(v_3) = 3$, and the answer 3. The paths are $v_1 v_2 v_3 v_4$, $v_1 v_3 v_4$ and $v_1 v_4$, and SPELL turns them back into $t_1$, $t_2$ and $t_3$.

Now a short read with the CIGAR `20M150N20M` at position 81 has the blocks $81..100$ and $251..270$. PATH-OF gives $(v_1, v_3)$: the read shows the junction of $t_2$ and nothing about where the transcript starts or ends. Add a fourth transcript E1, $201..300$ without E3; it adds no node and no edge, but it makes $v_3$ a possible end, and the graph cannot record that.

## Correctness

[The proof](proofs/correctness.md) shows four facts. The nodes partition the covered bases, and the cuts are exactly the splice sites inside covered regions. Every input alignment is a path, PATH-OF returns it, and its exons have the same introns as the alignment. The edge set is exactly the set of consecutive pairs of these paths, so the graph has no edge without a read behind it, and every edge goes to the right, so the graph is acyclic. COUNT-PATHS is right by induction in coordinate order. The proof also gives the two limits: some paths are not transcripts, and a transcript that starts or ends inside a node is not a source-to-sink path.

## Complexity

$|B|$ is the number of blocks, $|I|$ the number of distinct introns, $r$ the number of blocks of one alignment and $|P|$ the length of its path.

| operation | time | space |
|---|---|---|
| BUILD | $O((\lvert B \rvert + \lvert I \rvert) \log(\lvert B \rvert + \lvert I \rvert))$ plus the total path length | $O(\lvert V \rvert + \lvert E \rvert)$ |
| PATH-OF | $O(r \log \lvert V \rvert + \lvert P \rvert)$ | $O(\lvert P \rvert)$ |
| COUNT-PATHS | $O(\lvert V \rvert + \lvert E \rvert)$ | $O(\lvert V \rvert)$ |
| PATHS | $O(\lvert V \rvert + \lvert E \rvert)$ plus the size of the output | $O(\lvert V \rvert)$ for the stack, plus the output |

The graph is small: $|V| \le 2|I| + $ the number of covered intervals, and $|E| \le |V| + |I|$, because line L5 only adds edges between touching nodes and line L6 adds one edge for each intron. The code is a toy and cuts each covered interval by a scan over all splice sites, which costs $O(|U| \cdot |C|)$ instead of the sorted merge.

## Variants

- **A source and a sink.** StringTie adds a source node and a sink node to the graph, joined to the nodes where transcripts can start and end, so that every candidate transcript is a path from the source to the sink.
- **Weights.** The number of reads on each node and each junction, or the mean coverage per base. These weights are what assemblers use to choose paths.
- **Phasing paths.** Scallop keeps, besides the edges, the paths that single reads or read pairs cover, so that the choices at two splice sites stay linked. The general form is a path problem with subpath constraints.
- **Splicing graphs from ESTs.** Heber and others built the graph from expressed sequence tags and gene annotations, before short reads.
- **Annotation graphs.** Built from known transcripts only, the graph holds the annotated splicing, and the reads only add weights.
- **One graph per strand.** With a stranded library, reads give the strand. Without one, the strand of a junction comes from its splice site motif, such as GT-AG.

## When to use it

Use a splice graph for genome-guided assembly and for splicing analysis when a reference genome is known: it holds every junction of a locus in a few hundred nodes, and it can be built in one pass over sorted alignments. Without a genome, use a [de Bruijn graph](/de-bruijn-graph/) of the reads instead, as in [de novo transcriptome assembly](/de-novo-transcriptome-assembly/). For a [read mapper](/read-mapping/) that maps only to known transcripts, a transcript index is simpler, and the graph is not needed.

## Pitfalls

- **Reading every path as a transcript.** The paths combine all choices, and their number can be exponential. Line C3 counts candidates, not isoforms; assemblers pick a few paths with the read evidence.
- **Lost starts and ends.** Line L4 cuts only at splice sites. Two transcripts that start at different points of the same first exon share one node. Cut also at read start clusters, or keep the ends in a separate list, if the starts matter.
- **Off by one at junctions.** In 1-based closed coordinates the donor of an intron $101..200$ is base 100 and the acceptor is base 201. Mixing this with half-open coordinates in line L6 joins the wrong nodes.
- **Spurious junctions.** A read that is misaligned by a few bases makes a false intron in line L1, and a false node boundary in line L4. Filter junctions by read count, by anchor length and by splice motif before BUILD.
- **Mixed strands.** Antisense genes overlap. Build one graph per strand, or the paths mix the two genes.

## Implementations

## History

Heber, Alekseyev, Sze, Tang and Pevzner (2002) defined the splicing graph and used it to assemble ESTs, with each transcript as a path. With RNA-seq, genome-guided assemblers built graphs of the same kind from spliced alignments: Pertea and others (2015) used an alternative splice graph with a source and a sink in StringTie, and Shao and Kingsford (2017) added phasing paths in Scallop. Mäkinen, Belazzougui, Cunial and Tomescu (2015) give the graph models of transcript assembly, path covers and flows, in a textbook.

## References
