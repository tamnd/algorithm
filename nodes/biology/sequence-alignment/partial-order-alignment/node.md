---
tag: K4CMRB
kind: algorithm
slug: partial-order-alignment
name: Partial order alignment
aliases:
- POA
- graph-based multiple alignment
- partial order graph alignment
area: biology/sequence-alignment
level: research
summary: Builds a multiple alignment as a directed acyclic graph of letters, aligning each new sequence to the whole graph by dynamic programming and fusing it in.
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence, V: the number of nodes of the graph, E: the number of edges of the graph}
  time: {worst: "O(k^2 n^2)"}
  space: {extra: "O(V n)"}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 2002
  people: [Christopher Lee, Catherine Grasso, Mark F. Sharlow]
  note: Lee, Grasso and Sharlow kept the multiple alignment as a partial order graph instead of a profile, and used it on multidomain proteins and on EST assemblies with alternative splicing.
prereqs: [progressive-alignment, needleman-wunsch, sequence-to-graph-alignment, topological-sort]
see_also: [multiple-sequence-alignment, sum-of-pairs-score, directed-acyclic-graph, consensus-sequence, consensus-sequence-calling, overlap-layout-consensus, banded-alignment, mafft]
sources:
  - paper: doi:10.1093/bioinformatics/18.3.452
    title: Christopher Lee, Catherine Grasso and Mark F. Sharlow, Multiple sequence alignment using partial order graphs, Bioinformatics 18(3), 2002, pages 452 to 464
    locator: the partial order representation of a multiple alignment, alignment of a new sequence to the graph by pairwise dynamic programming, and the applications to SH2 domain proteins and EST assemblies
  - paper: doi:10.1093/bioinformatics/btg109
    title: Christopher Lee, Generating consensus sequences from partial order multiple sequence alignment graphs, Bioinformatics 19(8), 2003, pages 999 to 1008
    locator: the heaviest bundle algorithm for one or more consensus sequences from a partial order graph
  - paper: doi:10.1093/bioinformatics/bth126
    title: Catherine Grasso and Christopher Lee, Combining partial order alignment and progressive multiple sequence alignment increases alignment speed and scalability to very large alignment problems, Bioinformatics 20(10), 2004, pages 1546 to 1556
    locator: the alignment of two partial order graphs, and progressive POA along a guide tree
  - paper: doi:10.1101/gr.214270.116
    title: Robert Vaser, Ivan Sović, Niranjan Nagarajan and Mile Šikić, Fast and accurate de novo genome assembly from long uncorrected reads, Genome Research 27(5), 2017, pages 737 to 746
    locator: Racon, a consensus module for long reads based on SIMD partial order alignment
  - paper: doi:10.1093/bioinformatics/btaa963
    title: Yan Gao, Yongzhuang Liu, Yanmei Ma, Bo Liu, Yadong Wang and Yi Xing, abPOA, an SIMD-based C library for fast partial order alignment using adaptive band, Bioinformatics 37(15), 2021, pages 2209 to 2211
    locator: adaptive banded dynamic programming for partial order alignment
---

Partial order alignment (POA) is a method for [multiple sequence alignment](/multiple-sequence-alignment/) by Christopher Lee, Catherine Grasso and Mark Sharlow, published in 2002. It keeps the alignment as a [directed acyclic graph](/directed-acyclic-graph/): each node holds one letter, each sequence is a path through the graph, and nodes in the same alignment column are linked. To add a sequence, POA aligns it to the whole graph with a [Needleman-Wunsch](/needleman-wunsch/) recurrence in which a node looks back at all of its predecessors, as in [sequence-to-graph alignment](/sequence-to-graph-alignment/). Then it fuses the sequence into the graph: a matching letter reuses a node, and other letters make new nodes. A [progressive aligner](/progressive-alignment/) reduces the current alignment to a profile of columns; POA keeps every path, so the new sequence can follow one sequence in one region and another sequence in the next.

## In plain words

Draw the first sequence as a chain of letters. To add a second sequence, line it up against the chain. Where the letters agree, the second sequence walks along the same letters. Where they differ, it gets its own letters, next to the old ones, and the chain splits into two branches that join again later.

Every next sequence is lined up against this branching picture. It may follow any route through it, so it can copy one earlier sequence at the start and another at the end. Then it is drawn in the same way.

At the end, the letters that stand next to each other form the columns of the alignment, and each sequence gives one row.

## The problem

The input is $k$ sequences $S_1, \ldots, S_k$ over an alphabet $\Sigma$, a score $s(a, b)$ for two letters and a score $g < 0$ for a letter against a gap. The output is a multiple alignment: rows of equal length, row $r$ spelling $S_r$ with gaps added, and no column of gaps only. POA does not promise the best [sum-of-pairs score](/sum-of-pairs-score/); it adds the sequences one at a time, and each step aligns the new sequence to the best path through the graph built so far.

The *partial order graph* $G$ has one node per letter, an edge $u \to v$ when some sequence has the letter of $u$ right before the letter of $v$, and a label on each edge that lists the sequences that use it. The nodes are grouped into columns. A column holds at most one node of each letter and at most one node of each sequence, and the columns have a linear order that every edge follows. The nodes of one column are often called an *aligned ring*.

## The algorithm

```pseudo id=main
POA(S[1..k], s, g)
L1  G ← an empty graph; for r ← 1 to k do
L2      A ← ALIGN(G, S_r)
L3          in ALIGN: for each node v in topological order and j ← 0 to |S_r|, H[v][j] ← the largest of H[u][j−1] + s(v, y_j) and H[u][j] + g over the predecessors u of v, and H[v][j−1] + g; a node without predecessors uses the start row j·g in place of H[u]
L4          in ALIGN: take the largest H[v][|S_r|] over the nodes v without successors, and trace back to get the path and the pairs
L5      for each letter y_j aligned to a node v: use the node with letter y_j in the column of v, and create it there if it does not exist
L6      for each letter y_j aligned to a gap: create a new node in a new column, placed right after the last column on the path of S_r
L7      add an edge between each two consecutive nodes of S_r, and label it with r
L8  return one row per sequence: in each column, the letter of its node in that column, or a gap
```

**Alignment to the graph (lines L3 and L4).** This is the global alignment recurrence with one change: where [Needleman-Wunsch](/needleman-wunsch/) looks at row $i - 1$, a node looks at the rows of all of its predecessors. Line L3 has the three moves of pairwise alignment: a letter against a node, a node against a gap, and a letter against a gap. The value $H[v][j]$ is the best score of an alignment of $y_1 \ldots y_j$ with a path that starts at a node without predecessors and ends at $v$. The nodes are taken in [topological order](/topological-sort/), so the rows of all predecessors are ready. Nodes that are not on the chosen path cost nothing.

**Fusion (lines L5 to L7).** A letter that matches its node reuses it, so a part shared by many sequences stays a single chain. A mismatched letter goes into the column of its node as a new node, or reuses a node of that column that has the same letter. An inserted letter starts a new column. The new edges and labels record the path of $S_r$, so each sequence can be read back from the graph.

**Columns and output (line L8).** Each column becomes one alignment column. The implementation keeps the columns in a list, and inserts each new column right after the previous column on the path; then every edge goes from an earlier column to a later one, and the list, read node by node, is a topological order. Other implementations sort the graph topologically again after each addition, which serves the same purpose.

## Example

Use $+1$ for a match, $-1$ for a mismatch and $-2$ for a letter against a gap, and take

$$S_1 = \texttt{ACGT},\quad S_2 = \texttt{AGGTT},\quad S_3 = \texttt{ACGTT}.$$

The graph of $S_1$ is the chain $\texttt{A} \to \texttt{C} \to \texttt{G} \to \texttt{T}$. The best alignment of $S_2$ to it is `ACG-T` over `AGGTT`, with score $1 - 1 + 1 - 2 + 1 = 0$. Fusion reuses the nodes `A`, `G` and `T` of $S_1$. It adds a node `G` in the column of `C`, because the letters differ, and a node `T` in a new column before the last `T`, for the inserted letter. The graph now has 6 nodes:

| column | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| nodes | `A` | `C`, `G` | `G` | `T` (new) | `T` |
| used by | $S_1, S_2$ | $S_1$ on `C`, $S_2$ on `G` | $S_1, S_2$ | $S_2$ | $S_1, S_2$ |

Now $S_3 = \texttt{ACGTT}$ arrives. Neither earlier sequence matches it fully, but the path `A`, `C`, `G`, new `T`, `T` spells it exactly. This path uses `C` from $S_1$ and the inserted `T` from $S_2$. The recurrence finds it, with score 5, and fusion reuses all five nodes. The output is

```
S1  ACG-T
S2  AGGTT
S3  ACGTT
```

with sum-of-pairs score $0 + 3 + 2 = 5$, the optimum found by exact dynamic programming over all alignments of the three sequences.

## Correctness

The output is a valid multiple alignment, each call of ALIGN returns the best global alignment of the new sequence to a path from a node without predecessors to a node without successors, and for two sequences the output is an optimal pairwise alignment.

The recurrence of line L3 follows the last step of an alignment of $y_1 \ldots y_j$ with a path that ends at $v$: either $v$ is matched with $y_j$, or $v$ is against a gap, or $y_j$ is against a gap; in the first two cases the path before $v$ ends at a predecessor $u$ of $v$, or is empty if $v$ has none. Induction in topological order shows that $H[v][j]$ is the best such score, so line L4 finds the best path to a node without successors. Fusion keeps three invariants: each sequence is a path of nodes with its letters, the columns are ordered so that every edge goes forward, and each sequence has at most one node in each column. These give one letter per column per row, in order, and every column holds a node of some sequence, so the rows form a valid alignment. The proof file has the details.

## Complexity

The model is the word RAM, with one unit per arithmetic operation. Let $N = \sum_r |S_r| \le kn$.

- **One alignment (lines L3 and L4).** Each cell $(v, j)$ looks at the predecessors of $v$, so a sequence of length $n$ costs $O((V + E)\, n)$ time and $O(V n)$ space for the table and the traceback.
- **One fusion (lines L5 to L7).** Each letter adds at most one node, one column and one edge. With the column list as an array, placing a new column costs $O(V)$, so a fusion costs $O(V n)$.
- **Size of the graph.** Each letter adds at most one node and one edge, so $V \le N$ and $E < N$.

The total is $O(k \cdot N \cdot n) = O(k^2 n^2)$ time in the worst case, and $O(N n)$ space. When the sequences are similar, most letters reuse nodes, $V$ and $E$ stay close to $n$, and the time is about $O(k n^2)$, linear in the number of sequences. Lee, Grasso and Sharlow report alignment of 5000 sequences in about 4 hours on a Pentium II.

## Properties

- **Online.** Sequences are added one at a time, and a new sequence can be added to a finished graph.
- **Depends on input order.** A different order can give a different graph and a different alignment.
- **No profile.** The new sequence is compared with real paths through earlier sequences, not with column frequencies, so it can switch between earlier sequences from one region to the next.
- **Compact for similar sequences.** Shared letters share nodes.
- **Exact for two sequences.** The graph of one sequence is a chain, and ALIGN is then Needleman-Wunsch.

## Variants and improvements

- **Local and semi-global modes.** Replacing the global recurrence by a [Smith-Waterman](/smith-waterman/) or semi-global one lets a sequence align to part of the graph, which is useful for reads that cover only part of a region.
- **Consensus by heaviest bundle.** Lee (2003) finds one or more consensus sequences as the paths of largest total edge weight in the graph, where the weight of an edge grows with the number of sequences that use it. See [consensus sequence calling](/consensus-sequence-calling/).
- **Progressive POA.** Grasso and Lee (2004) align two partial order graphs to each other, and use this to merge groups along a guide tree, as in [progressive alignment](/progressive-alignment/). On large problems it ran 10 to 30 times faster than ClustalW.
- **Fast libraries for long reads.** Racon (Vaser and coauthors, 2017) computes consensus sequences of long, noisy reads with POA vectorized by SIMD instructions. abPOA (Gao and coauthors, 2021) adds an adaptive band, in the spirit of [banded alignment](/banded-alignment/).
- **Affine gaps.** The three-state recurrence of Gotoh carries over to graphs, with each state looking at all predecessors.

## When to use it

Use POA when many similar sequences must be merged, when sequences arrive one at a time, or when a consensus sequence is the goal. Typical uses are the consensus of long sequencing reads in [assembly](/overlap-layout-consensus/) and polishing, and the grouping of transcripts with alternative splicing. For divergent protein families, where the best alignment is not near a path through earlier sequences, use a consistency-based or iterative method such as [MAFFT](/mafft/).

## Pitfalls

- **Order matters.** Errors in early sequences shape the graph for all later ones. Add the most reliable sequences first, or use the progressive variant with a guide tree.
- **End conditions.** In the global version the path must start at a node without predecessors and end at a node without successors. A sequence that should end inside the graph then pays for the rest of a path; a semi-global or local mode avoids this.
- **The graph only grows.** Each mismatch or insertion adds a node, so very noisy sequences give a large graph and slow alignment.
- **Topological order.** The recurrence is wrong if a node is filled before one of its predecessors.
- **Rows from columns.** Two nodes of the same sequence must never share a column; the fusion rules keep this, and changes to them must too.

## Implementations

## History

Christopher Lee, Catherine Grasso and Mark Sharlow published partial order alignment in Bioinformatics in 2002. They noted that a progressive aligner reduces the alignment to a profile at each step, and that this loses information. They kept the alignment as a graph instead, and showed it on multidomain SH2 proteins and on EST data with alternative splicing and polymorphism. Lee added the heaviest bundle consensus in 2003, and Grasso and Lee joined POA with progressive alignment in 2004. Later, POA returned as a consensus engine for long sequencing reads, in tools such as Racon and abPOA.

## References
