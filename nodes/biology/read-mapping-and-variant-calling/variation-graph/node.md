---
tag: XJVQNQ
kind: data-structure
slug: variation-graph
name: Variation graph
aliases:
- genome graph
- pangenome graph
area: biology/read-mapping-and-variant-calling
level: advanced
summary: A sequence graph whose paths spell a reference and known variant haplotypes, so that reads align to the variation instead of one linear genome.
prereqs: [directed-acyclic-graph, read-mapping, variant-call-format]
see_also: [sequence-to-graph-alignment, de-bruijn-graph, string-graph, positional-burrows-wheeler-transform, haplotype-phasing, topological-sort, haplotype-based-variant-calling, splice-graph]
sources:
  - paper: doi:10.1038/nbt.4227
    title: Erik Garrison, Jouni Sirén, Adam M. Novak and others, Variation graph toolkit improves read mapping by representing genetic variation in the reference, Nature Biotechnology 36(9), 2018
    locator: pp. 875 to 879 (the variation graph with nodes, edges and embedded paths, its construction from a reference and a VCF file, and the mapping of reads to it)
  - paper: doi:10.1101/gr.214155.116
    title: Benedict Paten, Adam M. Novak, Jordan M. Eizenga and Erik Garrison, Genome graphs and the evolution of genome inference, Genome Research 27(5), 2017
    locator: pp. 665 to 676 (a review of graph models of genomes, the bidirected sequence graph, and the ways to build and index such graphs)
---

A variation graph stores a reference genome together with known variants as one graph. Each node holds a piece of DNA sequence, and each edge says that one piece can follow another. The reference is one path through the graph, and each variant adds a second route around the reference bases it changes. Every path from the start to the end spells one possible genome, a *haplotype*. Reads can then be aligned to the graph instead of to one linear sequence, so a read that carries a known variant matches it exactly, without the bias toward the reference allele that a linear reference gives. The vg toolkit of Garrison et al. (2018) made this practical at the scale of a human genome.

## In plain words

A reference genome is one long line of letters. But people differ from it at millions of places, and a read from a person with a different letter looks like an error when you compare it to that line.

A variation graph splits the line at each known difference and adds a short side road with the other version. A side road can also be empty, for a missing piece, or extra letters, for an added piece. Each way through the graph, taking the main road or the side road at each place, spells one version of the genome. A read can now match the version it comes from.

## The abstract type

A *sequence graph* is a directed graph whose nodes are labeled with non-empty strings. A walk $w_1 \to w_2 \to \cdots \to w_t$ spells the concatenation of its node strings. A variation graph is a sequence graph with a set of named *paths*, the walks that spell known sequences, such as the reference or the haplotypes of a sample.

This page builds the graph from a reference and a list of variants. A variant $(p, a, b)$ replaces the reference bases $\mathit{ref}[p{:}p + |a|]$, which must equal $a$, by the string $b$. One of $a$ and $b$ may be empty, for an insertion or a deletion, and $a \ne b$. The variants must not touch each other or the ends of the reference. The structure supports:

- BUILD$(\mathit{ref}, \text{variants})$: make the graph and the path of the reference;
- SPELL$(\text{path})$: the string of a walk;
- HAPLOTYPE$(C)$: the walk that takes the alternative allele of the variants in the set $C$ and the reference allele of the others;
- FIND$(s)$: every place (node, offset) where the string $s$ starts an exact match along some walk.

## Representation

The nodes are numbered $0, 1, 2, \ldots$ in the order of their start on the reference, and each node keeps its string and a sorted list of its successors. The graph keeps the named paths as lists of node ids, and for each variant its *bubble*: the node before it, the node after it, and the two routes between them. Real toolkits use a *bidirected* graph, in which each node can be read on either strand and an edge joins two node sides, so that inversions and reads from both strands fit in one graph.

## Operations

BUILD cuts the reference at both ends of every variant, which makes the reference nodes, and adds one node for each non-empty alternative allele. An inserted node is numbered before the reference node that starts at the same place, so that every edge goes from a smaller id to a larger one.

```pseudo id=main
BUILD(ref, V)
L1  cuts ← {0, |ref|} ∪ {p, p + |a| : (p, a, b) in V}, sorted
L2  make a reference node for ref[x..y) for each two adjacent cuts x < y
L3  make an alt node for b for each (p, a, b) in V with b non-empty, numbered by start position
L4  join the reference nodes in order with edges; this is the path "ref"
L5  for each variant (p, a, b) in V, with u the node that ends at p and w the node that starts at p + |a| do
L6      if b is non-empty then add the edges u → (the node of b) → w
L7      else add the edge u → w
```

FIND keeps a set of states, each a start place and a current place. It begins at every base equal to $s[0]$ and, for each next character of $s$, moves every state one base on: inside the node if it is not at the end, and to base 0 of each successor if it is.

```pseudo id=find
FIND(G, s)
L8  S ← {(i, k, i, k) : base k of node i equals s[0]}
L9  for each next character c of s do
L10     a state at (i, k) with k + 1 < |seq(i)| moves to (i, k + 1)
L11     a state at the end of node i moves to (j, 0) for each successor j of i; keep only the states whose new base is c
L12 return the sorted set of the start places (i, k) of the states left
```

SPELL joins the strings of the nodes of a walk, after checking each edge. HAPLOTYPE follows the reference path and, at each bubble in $C$, takes the alternative route. Mapping reads with errors is [sequence-to-graph alignment](/sequence-to-graph-alignment/), the dynamic program of alignment run along the graph in [topological order](/topological-sort/).

## Example

The reference is $\texttt{CTAGGATCCAGT}$, of 12 bases, and there are three variants: a substitution $(2, \texttt{A}, \texttt{G})$, a deletion $(5, \texttt{AT}, \text{empty})$ and an insertion $(9, \text{empty}, \texttt{TT})$. The cuts are 0, 2, 3, 5, 7, 9 and 12. BUILD makes eight nodes:

| id | string | kind |
|---|---|---|
| 0 | CT | reference |
| 1 | A | reference allele of the substitution |
| 2 | G | alternative allele of the substitution |
| 3 | GG | reference |
| 4 | AT | reference allele of the deletion |
| 5 | CC | reference |
| 6 | TT | inserted |
| 7 | AGT | reference |

The edges are $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $3 \to 5$, $4 \to 5$, $5 \to 6$, $5 \to 7$ and $6 \to 7$. The edge $3 \to 5$ skips the deleted bases, and node 6 is a route from 5 to 7 next to the direct edge. The reference path is $0, 1, 3, 4, 5, 7$, which spells the reference. The walk $0, 2, 3, 5, 6, 7$ takes all three variants and spells $\texttt{CTGGGCCTTAGT}$. There are $2^3 = 8$ walks from node 0 to node 7, one for each set of variants.

FIND($\texttt{AGGCCTTA}$) returns $(1, 0)$: the match runs through nodes 1, 3, 5, 6 and 7, on the haplotype with the deletion and the insertion, and the string does not occur in the reference. FIND($\texttt{GGATCC}$) returns $(3, 0)$, a match on the reference path. FIND($\texttt{GG}$) returns $(2, 0)$ and $(3, 0)$: the first match crosses the edge $2 \to 3$. FIND($\texttt{GGGG}$) returns nothing, because no walk has four G bases in a row.

## Correctness

The cuts never fall inside the reference allele of a variant, so each variant gives one bubble between a node $u$ and a node $w$ with exactly two routes, which spell $a$ and $b$. Between two bubbles there is at least one reference base, so a walk from the source to the sink visits the reference nodes outside the bubbles in order and makes one choice at each bubble. This gives the theorem that the walks from the source to the sink are exactly the $2^v$ haplotypes of the $v$ variants, each spelling the reference with its chosen variants applied. The ids are a topological order, so the graph is acyclic. FIND keeps the invariant that after $t$ steps its states are exactly the walks that spell $s[0..t]$, which follows from the rule for the next base along a walk. The full proofs are in proofs/correctness.md, and the tests check the walks against the haplotypes, and FIND against a search in the strings of all walks.

## Complexity

- **BUILD.** Sorting the variants and the cuts takes $O(v \log v)$ time, and copying the reference takes $O(n)$ for a reference of length $n$. The graph has at most $3v + 1$ nodes and $4v$ edges.
- **SPELL and HAPLOTYPE.** Linear in the length of the result.
- **FIND.** With $N$ bases in the graph and out-degree at most $d$, the current places are at most $N$, so a test for whether $s$ occurs costs $O(|s| N d)$. Keeping the start of each state can raise the number of states to $N^2$ in the worst case.
- **Space.** $O(n + \sum |b|)$ for the strings and $O(v)$ for the edges and bubbles.

A search of each read against the whole graph state by state is too slow for a genome. Toolkits index the graph instead: vg uses GCSA2, a generalization of the [FM-index](/fm-index/) to the paths of a graph, to find seeds, and then aligns around them.

## Variants

- **Bidirected graphs.** Each node has two sides, for the two strands. This allows inversions and the reads of both strands.
- **Graphs from assemblies.** Instead of a reference and a VCF file, the graph can come from the alignment of many whole genome assemblies, which also holds large and nested variants.
- **Graphs with cycles.** Duplications and repeats make cycles, which the build of this page never makes.
- **Haplotype indexes.** The GBWT stores the haplotypes of many samples as paths in compact form, in the style of the [positional Burrows-Wheeler transform](/positional-burrows-wheeler-transform/), so that a mapper can prefer the walks that real haplotypes take.
- **De Bruijn graphs.** A [de Bruijn graph](/de-bruijn-graph/) of the k-mers of many genomes is another kind of sequence graph, with nodes of a fixed length.

## When to use it

Use a variation graph when reads come from a population with many known variants, and a linear reference would bias the alignment toward its own alleles, as near insertions and deletions or in regions of high diversity such as the HLA genes. It also lets a caller genotype known structural variants from short reads, since the reads that cross them align to their routes. When the variants are rare, or the reads are long and few, a linear reference is simpler and the gain is small.

## Pitfalls

- **Too many variants.** Every bubble doubles the number of walks, and close variants make many combinations that no real haplotype has. Reads can then align to a walk that does not exist in the population. Filter rare variants, or use a haplotype index.
- **Overlapping variants.** Two variants that share bases need a joint bubble; the simple build of this page rejects them.
- **Coordinates.** A position on the graph is a node and an offset. To report results in reference coordinates, project them onto the reference path, and decide what to do with places on alternative routes.
- **Normalization of the input.** The same insertion or deletion written at two places in a repeat gives two bubbles; [normalize the variants](/variant-normalization/) first.

## Implementations

## History

Graph models of genomes come from assembly, with the de Bruijn graph and the [string graph](/string-graph/). Paten, Novak, Eizenga and Garrison (2017) reviewed the use of such graphs as a reference for a population, in place of one linear genome. Garrison et al. (2018) described the vg toolkit, which builds a variation graph from a reference and a VCF file, indexes it with GCSA2 and maps reads to it, and showed that it reduces the bias toward the reference allele. Later work built graphs from many complete assemblies.

## References
