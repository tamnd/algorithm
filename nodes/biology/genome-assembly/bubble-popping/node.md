---
tag: ZPJBHM
kind: algorithm
slug: bubble-popping
name: Bubble popping
aliases:
- bubble removal
- bulge removal
area: biology/genome-assembly
level: core
summary: Find two short parallel paths between the same pair of vertices of an assembly graph and delete the one with lower coverage. It removes errors inside reads, and also true alleles.
solves: [assembly-graph-simplification]
model: word-ram
complexity:
  vars: {m: the number of edges (distinct k-mers), k: the k-mer length, r: the number of bubbles popped}
  time: {worst: O((r+1)·m·(k+m)·log m)}
  space: {extra: O(k·m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Daniel R. Zerbino, Ewan Birney]
  note: Velvet merged bubbles with the Tour Bus search. SPAdes (2012) removed bulges in increasing order of coverage and projected the removed path onto the kept one.
prereqs: [de-bruijn-assembly, unitig, assembly-graph-simplification, dijkstra]
see_also: [tip-removal, read-error-correction, consensus-sequence-calling, genome-repeat, kmer-spectrum, contig, edit-distance, k-shortest-paths]
sources:
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829, sections on bubbles and the Tour Bus algorithm (the 200 node, 100 bp and 80% similarity thresholds)
  - paper: doi:10.1089/cmb.2012.0021
    title: Anton Bankevich and others, SPAdes, a new genome assembly algorithm and its applications to single-cell sequencing, Journal of Computational Biology 19(5) (2012)
    locator: pp. 455 to 477, Sections 6.3 and 8.4 (bulge corremoval and the projection of the removed path)
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753, Error Correction and Data Corruption (errors make a tangle of erroneous edges)
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602, Introduction (bubble popping as a heuristic outside the safe model)
---

Bubble popping removes the small loops that sequencing errors and small variants make in a de Bruijn graph. A substitution error in the middle of a read makes $k$ false $k$-mers that leave the true path at one vertex and join it again $k$ edges later. The two paths form a *bubble* (SPAdes says *bulge*). Bubble popping finds such pairs of short, similar paths and deletes the one with lower coverage, so that the true path becomes one [unitig](/unitig/) again. Velvet does this with its Tour Bus search and SPAdes with bulge removal. It is a heuristic: a heterozygous site or two copies of a repeat that differ in one letter also make a bubble, and popping it deletes a true sequence.

## In plain words

The genome is one road in the assembly graph. A read error in the middle of a read builds a short detour: it leaves the road and comes back to it a little later. Few cars use the detour, because only the reads with the error go that way.

Bubble popping looks for two short routes that start at the same place and end at the same place and have almost the same length. It keeps the busier route and removes the other one. Then the road has no fork there.

The danger: in a diploid genome, the two copies of a chromosome can differ in one letter. That also makes two routes, and both are real. If one copy got fewer reads by chance, the method removes a real copy.

## The problem

The input is an edge-centric [de Bruijn graph](/de-bruijn-graph/) of order $k$ built from reads, as in [de Bruijn assembly](/de-bruijn-assembly/), with the count of each $k$-mer. The genome $S$ has length $G$, the $N$ reads have length $L$, the coverage is $c = NL/G$, and the reads have substitution errors at a low rate. For a path $P$ with $m_P$ edges, $\mathrm{cov}(P)$ is the mean count of its edges.

A unitig $P$ from $u$ to $w$ is **poppable** for a length bound $\ell$ and a length slack $\delta$ if $u \ne w$, $m_P \le \ell$, and there is another path $Q$ from $u$ to $w$ through other unitigs with $m_Q \le \ell$, $|m_P - m_Q| \le \delta$ and $\mathrm{cov}(Q) \ge \mathrm{cov}(P)$. The path $Q$ is fixed as the one with the fewest edges, and among those the largest total count. The task is to delete poppable unitigs until none is left. This is a step of [assembly graph simplification](/assembly-graph-simplification/).

## The algorithm

The defaults are $\ell = 2k$ edges and $\delta = 2$.

```pseudo id=main
BUBBLE-POPPING(G, ℓ, δ)                   ▷ G has a count on each edge
L1  repeat
L2      U ← the unitigs of G, in increasing order of cov
L3      for each P in U, from u to w, with m_P edges do
L4          if u = w or m_P > ℓ then skip P
L5          Q ← a path u → w through other unitigs: fewest edges, then largest total count
L6          if Q exists and m_Q ≤ ℓ and |m_P − m_Q| ≤ δ and cov(Q) ≥ cov(P) then
L7              choose P and leave the for loop
L8      if a unitig P was chosen then delete the edges of P
L9      else return G
```

Line L5 is [Dijkstra's algorithm](/dijkstra/) on the graph of unitigs. A unitig with $m$ edges and total count $t$ has the weight $(m, -t)$, and weights are compared in lexicographic order, so the search finds the fewest edges first and then the most coverage. Line L2 takes the weakest unitigs first, as SPAdes does: a unitig with mean count near 1 is most likely an error. After each deletion the vertices $u$ and $w$ can become simple, the unitigs around them merge, and line L2 computes them again.

The implementation deletes $P$ and leaves the counts of $Q$ as they are. SPAdes also adds the coverage of $P$ to $Q$, which it calls projection, so that the kept path has the coverage of both.

## Example

**An error bubble.** Let $k = 5$ and $S = \mathtt{ATGGCGTACCTTAGCAGTCCA}$ ($G = 21$). Eight reads of length 10 start at positions 0, 2, 3, 4, 6, 8, 9 and 11. A ninth read is a copy of $S[4 \ldots 13] = \mathtt{CGTACCTTAG}$ with an error at its index 5, $\mathtt{C} \to \mathtt{A}$: $\mathtt{CGTACATTAG}$. Index 5 is at least $k - 1 = 4$ letters from both ends of the read, so all five 5-mers that contain it are inside the read.

| unitig | edges | counts | cov |
|---|---|---|---|
| ATGGCGTAC | 5 | 1, 1, 2, 3, 5 | 2.4 |
| GTACATTAG | 5 | 1, 1, 1, 1, 1 | 1 |
| GTACCTTAG | 5 | 4, 4, 4, 4, 4 | 4 |
| TTAGCAGTCCA | 7 | 3, 4, 3, 3, 2, 1, 1 | 2.43 |

Line L2 takes $P = \mathtt{GTACATTAG}$ first, with cov 1. It goes from $\mathtt{GTAC}$ to $\mathtt{TTAG}$. Line L5 finds $Q = \mathtt{GTACCTTAG}$, also 5 edges, with cov 4. Line L6 holds: $5 \le 10$, $|5 - 5| = 0 \le 2$, $4 \ge 1$. Line L8 deletes the five false $k$-mers. Now $\mathtt{GTAC}$ and $\mathtt{TTAG}$ are simple, and the next round finds one unitig, $S$ itself, and no bubble. The two sides of the bubble spell $\mathtt{GTACATTAG}$ and $\mathtt{GTACCTTAG}$: $2k - 1 = 9$ letters that differ only in the middle one.

**A true allele is lost.** A diploid genome has the two copies $h_1 = \mathtt{GATTACAGGCTCAAGTCCGA}$ and $h_2 = \mathtt{GATTACAGGCGCAAGTCCGA}$, which differ at index 10. Six reads of length 10 come from $h_1$ (at positions 0, 2, 4, 6, 8, 10) and four from $h_2$ (at 1, 4, 7, 10). With $k = 5$ the unitigs are $\mathtt{GATTACAGGC}$, $\mathtt{AGGCTCAAG}$ (each count 3), $\mathtt{AGGCGCAAG}$ (each count 2) and $\mathtt{CAAGTCCGA}$. The $h_2$ side has cov 2 and the $h_1$ side cov 3, both with 5 edges, so line L8 deletes the $h_2$ side. The output is the single contig $h_1$: the assembly has lost the variant. With $\ell = 4$ no unitig of the bubble is short enough, and both alleles stay.

## Correctness

[The proof](proofs/correctness.md) shows four things. Line L5 returns the path with the fewest edges and then the largest total count, because Dijkstra's algorithm works with these lexicographic weights. The loop stops after at most $m + 1$ rounds and leaves no poppable unitig. Each pop keeps reachability: if a walk from $x$ to $y$ used the deleted unitig $P$, the same walk with $Q$ in place of $P$ still exists. And a substitution at index $i$ of a read with $k - 1 \le i \le L - k$ makes $k$ false $k$-mers that form a poppable unitig from the true vertex before the error to the true vertex after it, if the false $(k-1)$-mers are new and no much shorter path joins the two vertices. Deleting it removes no $k$-mer of the genome.

The proof does not show that only errors are popped, because that is false, as the second example shows.

## Complexity

Let $m$ be the number of edges and $r$ the number of pops. One round builds the unitigs in $O(km \log m)$ time with sorting. For each candidate, line L5 runs Dijkstra on at most $m$ unitigs in $O(m \log m)$ time. There are at most $m$ candidates in a round and $r + 1$ rounds, so the total is $O((r+1) \cdot m \cdot (k + m) \log m)$ time and $O(km)$ space.

Real assemblers bound the search. Velvet's Tour Bus stops a search at 200 nodes, and both SPAdes and Velvet only look at short paths, so line L5 explores only the part of the graph within the length bound around $u$. With a bound $\ell$ and a graph of bounded degree, each search visits a number of unitigs that depends on $\ell$ and the degree but not on $m$.

## Properties

- **A heuristic.** It is outside the safe model of [contigs](/contig/): it can delete true sequence, and so it can make a contig that is in only one of the two copies of a chromosome.
- **Keeps reachability.** A pop never cuts the graph apart, because the kept path joins the same two vertices.
- **Deterministic.** The order is fixed by the mean count and then by the string.
- **Order-dependent.** Popping one bubble merges unitigs, which changes the next candidates. The order by coverage is part of the method.
- **Collapses haplotypes.** On a diploid genome the output is a mosaic: at each popped site it keeps the allele with more reads.

## Variants and improvements

- **Tour Bus (Velvet).** A Dijkstra-like search from each node, in which a path with high coverage counts as short. When the search reaches a node it has seen before, it goes back along both paths to their last common node and compares the two sequences. If both paths have fewer than 200 nodes, both sequences are shorter than 100 bp and they are at least 80% similar, the path found first, which has the higher coverage, is kept and the other is merged into it.
- **Bulge corremoval (SPAdes).** A simple bulge is a short path $P$ with an alternative $Q$ of similar length. SPAdes removes $P$ and projects its edges and coverage onto $Q$, so the later steps still see the reads of $P$. It processes edges in increasing order of coverage and interleaves this with tip clipping and the removal of chimeric edges.
- **Similarity test.** Compare the two sequences by [edit distance](/edit-distance/), not only by length, so that a bubble between two unrelated paths is not popped.
- **Keeping variants.** Diploid and metagenome assemblers keep the bubble and report both paths, or mark it as a variant site, instead of deleting one side.
- **Superbubbles.** A bubble can hold more than two paths and nested branches. Later work defines superbubbles, regions of the graph with one entrance and one exit, and gives fast algorithms to find them all.

## When to use it

Use it after [tip removal](/tip-removal/) on a de Bruijn graph of short reads with substitution errors, when you want a haploid consensus. Turn it off, or keep both sides, when you want the variants: diploid assembly, a population sample, a metagenome with near-identical strains, or a genome with recent segmental duplications.

## Pitfalls

- **Losing alleles.** The second example: a heterozygous site with uneven read sampling loses its lower allele.
- **Merging repeat copies.** Two copies of a repeat that differ in one letter make a bubble inside the repeat. Popping it makes both copies look the same, and the difference is lost.
- **A loose length bound.** With a large $\ell$, two long paths that are unrelated but join the same two vertices, such as the two arms around a repeat, look like a bubble. Keep $\ell$ near $2k$ or test the sequence similarity.
- **Ties.** If both sides have the same coverage, the choice is arbitrary. Do not pop ties if you need to keep variants.
- **Not recomputing unitigs.** After a pop, two unitigs at $u$ or $w$ can merge into one longer path. A stale list can then pop a long true path that was split only by the bubble.

## Implementations

## History

Pevzner, Tang and Waterman (2001) observed that read errors turn the simple de Bruijn graph of a genome into a tangle of erroneous edges, and EULER corrected the reads before it built the graph. Zerbino and Birney (2008) introduced the Tour Bus algorithm in Velvet to merge bubbles in the graph itself. Bankevich and others (2012) used bulge corremoval in SPAdes, with removal in increasing order of coverage and projection of the removed path. Tomescu and Medvedev (2017) list bubble popping among the heuristics that their safe model of contig assembly does not cover.

## References
