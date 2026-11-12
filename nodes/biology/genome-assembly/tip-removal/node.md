---
tag: W7590Z
kind: algorithm
slug: tip-removal
name: Tip removal
aliases:
- dead-end removal
- tip clipping
area: biology/genome-assembly
level: core
summary: Delete short dead-end branches of a de Bruijn graph whose coverage is lower than the branch they leave. Most of them come from read errors near the ends of reads.
solves: [assembly-graph-simplification]
model: word-ram
complexity:
  vars: {m: the number of edges (distinct k-mers), k: the k-mer length, r: the number of tips removed}
  time: {worst: O(k·m·(r+1)·log m)}
  space: {extra: O(k·m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2008
  people: [Daniel R. Zerbino, Ewan Birney]
  note: Velvet removed tips shorter than 2k whose junction arc had a minority count, in increasing order of coverage.
prereqs: [de-bruijn-assembly, unitig, assembly-graph-simplification]
see_also: [bubble-popping, read-error-correction, kmer-spectrum, contig, de-bruijn-graph, genome-repeat]
sources:
  - paper: doi:10.1101/gr.074492.107
    title: Daniel R. Zerbino and Ewan Birney, Velvet, algorithms for de novo short read assembly using de Bruijn graphs, Genome Research 18(5) (2008)
    locator: pp. 821 to 829, section Tip removal (the 2k length bound and the minority count condition)
  - paper: doi:10.1089/cmb.2012.0021
    title: Anton Bankevich and others, SPAdes, a new genome assembly algorithm and its applications to single-cell sequencing, Journal of Computational Biology 19(5) (2012)
    locator: pp. 455 to 477, Section 8.2 (tip clipping)
  - paper: doi:10.1089/cmb.2016.0141
    title: Alexandru I. Tomescu and Paul Medvedev, Safe and complete contig assembly through omnitigs, Journal of Computational Biology 24(6) (2017)
    locator: pp. 590 to 602, Introduction (tip removal as a heuristic outside the safe model)
---

Tip removal deletes the short dead ends of a de Bruijn graph. A sequencing error in the last $k - 1$ letters of a read makes a chain of false $k$-mers that leaves the true path and stops, because no read goes on from it. Such a chain is a *tip*. It blocks the true [unitig](/unitig/) at the branch point, so the contigs get shorter. Velvet removes a tip if it is shorter than $2k$ and its coverage at the junction is lower than that of another branch there. The rule is a heuristic: it also removes true sequence at genome ends and next to coverage gaps.

## In plain words

Picture the assembly graph as roads. The genome is one long road. A read error near the end of a read builds a short side road that leaves the main road and stops in a field. Few cars used it, because only one read had the error.

Tip removal finds each side road that stops in a field, is short, and has less traffic than the road it leaves, and digs it up. After that, the main road has no fork there, and a longer stretch of it becomes one contig. The danger: the true road can also end, at the end of a chromosome or where no reads were made. If that end is short and has less traffic, the method digs up a true piece too.

## The problem

The input is an edge-centric [de Bruijn graph](/de-bruijn-graph/) of order $k$ built from reads, as in [de Bruijn assembly](/de-bruijn-assembly/). Each edge is a $k$-mer $x$ with its count $\mathrm{count}(x)$ in the reads. The genome $S$ has length $G$, the $N$ reads have length $L$, and the coverage is $c = NL/G$. The reads have substitution errors at a low rate. A true $k$-mer has an expected count of about $c(L-k+1)/L$, and a $k$-mer with an error has a count near 1.

A unitig $P = e_1 \cdots e_m$ is a **removable tip** for a bound $\ell$ if $m < \ell$ and

- it starts at a vertex with in-degree 0 and ends at a vertex $w$ with in-degree at least 2, and $\mathrm{count}(e_m)$ is smaller than the count of some other edge into $w$ (a source tip), or
- it ends at a vertex with out-degree 0 and starts at a vertex $u$ with out-degree at least 2, and $\mathrm{count}(e_1)$ is smaller than the count of some other edge out of $u$ (a sink tip).

The task is to delete removable tips until none is left. This is one step of [assembly graph simplification](/assembly-graph-simplification/).

## The algorithm

The default bound is $\ell = 2k$ edges.

```pseudo id=main
TIP-REMOVAL(G, ℓ)                        ▷ G has a count on each edge
L1  repeat
L2      T ← ∅
L3      for each unitig P = e1 … em of G do
L4          if in(tail(e1)) = 0 and in(head(em)) ≥ 2 then a ← em; A ← the other edges into head(em)
L5          else if out(head(em)) = 0 and out(tail(e1)) ≥ 2 then a ← e1; A ← the other edges out of tail(e1)
L6          else skip P
L7          if m < ℓ and count(a) < max{count(f) : f in A} then add (count(a), P) to T
L8      if T = ∅ then return G
L9      delete the edges of the member of T with the smallest count(a)
```

Line L4 finds source tips and line L5 sink tips. Line L7 is the minority rule of Velvet: a tip is removed only if its edge at the junction has a lower count than some other edge on the same side. Two branches with the same count are left alone, because they can be two true ends. Line L9 removes one tip and then line L3 computes the unitigs again. This matters: when a tip goes, its junction can become a simple vertex, two unitigs merge into one, and the merged unitig is no longer a tip candidate. A path of simple vertices that is a whole component, such as an isolated cycle, has no dead end and is never a tip.

## Example

**An error tip.** Let $k = 5$ and $S = \mathtt{ATGGCGTACCTTAGCAGTCCA}$ ($G = 21$). Seven reads of length 10 start at positions 0, 2, 4, 6, 8, 9 and 11. The read at position 8 should be $\mathtt{CCTTAGCAGT}$, and an eighth copy of it, $\mathtt{CCTTAGCATT}$, has an error at its index 8, one letter from its end. The error is in two 5-mers, $\mathtt{AGCAT}$ and $\mathtt{GCATT}$, each with count 1.

| step | what happens |
|---|---|
| graph | vertex $\mathtt{AGCA}$ has out-edges $\mathtt{AGCAG}$ (count 3) and $\mathtt{AGCAT}$ (count 1) |
| unitigs | $\mathtt{ATGGCGTACCTTAGCA}$, $\mathtt{AGCAGTCCA}$, $\mathtt{AGCATT}$ |
| L5 | the unitig $\mathtt{AGCAT}, \mathtt{GCATT}$ ends at $\mathtt{CATT}$ with out-degree 0 and starts at $\mathtt{AGCA}$ with out-degree 2 |
| L7 | $2 < \ell = 10$ and $1 < 3$, so it is a removable tip |
| L9 | delete $\mathtt{AGCAT}$ and $\mathtt{GCATT}$ |
| L3 | $\mathtt{AGCA}$ is now simple; one unitig, $\mathtt{ATGGCGTACCTTAGCAGTCCA} = S$ |
| L8 | no tip is left; return |

**A true end is lost.** Let $k = 5$ and $S = u R v R w$ with $u = \mathtt{CGGGAGTC}$, $R = \mathtt{CCTG}$, $v = \mathtt{AGAGGCTT}$ and $w = \mathtt{GTT}$, so $S = \mathtt{CGGGAGTCCCTGAGAGGCTTCCTGGTT}$ ($G = 27$). The 4-mer $R$ occurs twice and no other 4-mer repeats. The reads are all 18 substrings of length 10, with no errors. Near the end of $S$ fewer reads cover each $k$-mer, so the edge $\mathtt{CCTGG}$ into $w$ has count 3 and the edge $\mathtt{CCTGA}$ into $v$ has count 6. The unitigs are $\mathtt{CGGGAGTCCCTG}$, $\mathtt{CCTGAGAGGCTTCCTG}$ and $\mathtt{CCTGGTT}$. The last one has 3 edges, ends at a dead end, and starts at $\mathtt{CCTG}$ with out-degree 2, and $3 < 6$. So line L9 deletes it, and the true end $\mathtt{GTT}$ of the genome is gone from the output. With $\ell = 3$ it stays. The source chain $\mathtt{CGGGAGTCCCTG}$ (8 edges) is also short, but its junction edge has count 6 against 4 for the other edge into $\mathtt{CCTG}$, so the minority rule keeps it.

## Correctness

[The proof](proofs/correctness.md) shows two things. First, the loop stops after at most $m + 1$ rounds, the output is a subgraph of the input, it has no removable tip, and each deleted edge was on a removable tip at the time. Second, an error at index $i$ of a read of length $L$, with $d = L - 1 - i \le k - 2$ letters after it, makes a removable sink tip of $d + 1 \le k - 1$ edges, if its false $(k-1)$-mers are new and the true $k$-mer at the branch has count at least 2. The deletion of that tip touches no $k$-mer of the genome. An error at least $k - 1$ letters from both ends of the read makes a bubble instead, which is the job of [bubble popping](/bubble-popping/).

The proof does not show that no true $k$-mer is lost, because this is false, as the second example shows.

## Complexity

Let $m$ be the number of edges and $r$ the number of tips removed. One round of lines L2 to L7 builds the degree tables and walks each unitig once, in $O(km)$ expected time with hashing. The implementation sorts the $k$-mers to get a fixed order, which costs $O(km \log m)$ for each round. There are $r + 1$ rounds, so the total is $O(k m (r+1) \log m)$ time and $O(km)$ space.

A faster version keeps the tips in a priority queue by junction count. A deletion changes only the degrees at its junction, so it only recomputes the one or two unitigs that meet there. The work for one deletion is then the length of the tip plus the length of the unitigs at its junction, with $O(\log m)$ for each queue operation.

## Properties

- **A heuristic.** It is not part of the safe model of [contigs](/contig/). It trades a small risk of losing true ends for much longer contigs.
- **Local.** Each decision looks at one unitig and the edges at one junction.
- **Deterministic.** The order of deletions is fixed by the count and then by the string.
- **Iterative.** Deleting one tip can merge unitigs, and the merged unitig can make or break a later tip. So the result can depend on the order, and the order is part of the method.

## Variants and improvements

- **Length in letters or in edges.** A unitig of $m$ edges spells $m + k - 1$ letters. A bound of $2k$ letters allows tips of at most $k$ edges, a bound of $2k$ edges allows $2k - 1$ edges. Both cover the error tips from the read ends, which have at most $k - 1$ edges.
- **SPAdes tip clipping.** SPAdes clips tips whose length is below a bound tied to the read length, and compares the coverage of the tip with the coverage of the other edges at the junction. It interleaves this with bubble removal and the removal of chimeric edges, in increasing order of coverage.
- **Read error correction first.** If the reads are corrected before the graph is built, as in EULER, most error tips never appear. See [read error correction](/read-error-correction/).
- **A count threshold.** Dropping all $k$-mers with count below a threshold $t$ removes most error $k$-mers at once, but it also cuts true low-coverage regions. Tip removal is more selective, because it only looks at dead ends.
- **Rounds with other steps.** A bubble that is merged or a chimeric edge that is cut can leave a new dead end. So assemblers run tip removal again after the other simplification steps.

## When to use it

Use it on every de Bruijn graph built from short reads with errors, after a mild count threshold and before bubble popping. Use a smaller bound or skip it near the ends of linear chromosomes, or when you assemble a sample with uneven coverage, such as single cells or a metagenome, where a true low-coverage branch is common.

## Pitfalls

- **Losing true ends.** The second example: a repeat near the end of a genome makes the true end a short dead end with lower coverage, and the rule removes it.
- **Eroding at coverage gaps.** A region without reads cuts the true path. The two parts next to the gap are dead ends. If one of them hangs from a repeat and is short, it is removed. Velvet warns about this case.
- **Forgetting the minority rule.** Without it, two true alleles that end near each other, or two true ends, can both be removed.
- **Not recomputing unitigs.** If you find all tips once and delete them all, you can delete a chain that stopped being a tip after an earlier deletion merged it with a long unitig.
- **Recursion.** A walk along a unitig can be long. Use a loop.

## Implementations

## History

Zerbino and Birney introduced tip removal in Velvet (2008), with the bound $2k$, the minority count rule and the removal in increasing order of multiplicity, before the Tour Bus step for bubbles. SPAdes (Bankevich and others, 2012) used tip clipping with a length bound from the read length, mixed with bulge and chimeric edge removal. Tomescu and Medvedev (2017) list tip removal among the heuristics outside their safe model of contig assembly.

## References
