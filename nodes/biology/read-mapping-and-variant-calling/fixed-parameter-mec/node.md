---
tag: W2Z7FH
kind: algorithm
slug: fixed-parameter-mec
name: Fixed-parameter MEC dynamic programming
aliases:
- WhatsHap algorithm
area: biology/read-mapping-and-variant-calling
level: research
summary: Solve weighted MEC exactly with a dynamic program over the variant columns. The time is exponential only in the coverage and linear in the number of columns.
solves: [minimum-error-correction-problem]
model: word-ram
complexity:
  vars: {m: the number of variant columns, c: the largest number of fragments active at one column}
  time: {worst: O(2^c m), average: O(2^c m), best: O(2^c m)}
  space: {extra: O(2^c m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2015
  people: [Murray Patterson, Tobias Marschall, Nadia Pisanti, Leo van Iersel, Leen Stougie, Gunnar W. Klau, Alexander Schönhuth]
  note: Patterson et al. described WhatsHap, a dynamic program for weighted MEC whose cost depends on the coverage and not on the read length, for long reads that cover many variants.
prereqs: [minimum-error-correction-problem, fixed-parameter-tractable]
see_also: [haplotype-assembly, haplotype-phasing, kernelization, np-hard, viterbi-algorithm, local-search, bipartite-graph, variant-call-format]
sources:
  - paper: doi:10.1089/cmb.2014.0157
    title: Murray Patterson, Tobias Marschall, Nadia Pisanti, Leo van Iersel, Leen Stougie, Gunnar W. Klau and Alexander Schönhuth, WhatsHap, weighted haplotype assembly for future-generation sequencing reads, Journal of Computational Biology 22(6), 2015
    locator: pp. 498 to 509, the sections on the dynamic programming algorithm (the active fragments, the bipartitions of each column, the recurrence and the O(2^(c-1) m) bound) and on the all-heterozygous case
  - paper: doi:10.1007/s00453-007-0029-z
    title: Rudi Cilibrasi, Leo van Iersel, Steven Kelk and John Tromp, The complexity of the single individual SNP haplotyping problem, Algorithmica 49(1), 2007
    locator: pp. 13 to 36 (MEC is NP-hard also for gapless fragments, and polynomial cases)
  - paper: doi:10.1093/bib/3.1.23
    title: Ross Lippert, Russell Schwartz, Giuseppe Lancia and Sorin Istrail, Algorithmic strategies for the single nucleotide polymorphism haplotype assembly problem, Briefings in Bioinformatics 3(1), 2002
    locator: the sections on the fragment conflict models and their complexity
---

The fixed-parameter MEC dynamic program solves the [minimum error correction problem](/minimum-error-correction-problem/) exactly, column by column. At each variant column it keeps one table entry for each way to split the reads that cover the column into two groups, and it carries the best cost from one column to the next. The table of a column has $2^c$ entries when $c$ reads cover it, so the time is $O(2^c m)$ for $m$ columns: exponential in the coverage, but linear in the number of columns and not dependent on the read length. This makes MEC [fixed-parameter tractable](/fixed-parameter-tractable/) in the coverage. Patterson et al. (2015) used it in WhatsHap, which phases long reads that cover many variants.

## In plain words

You have many reads from the two copies of a chromosome, and at each place where the copies can differ, each read shows one of two letters. Some letters are wrong. You want to sort the reads into two piles, one for each copy, changing as few letters as possible so that each pile agrees with itself.

Work along the chromosome from left to right. At each place, only the reads that cover it matter, and there are not many of them. For each way to sort just those reads into two piles, write down the least cost of all the work done so far. When you move to the next place, the reads that cover both places must stay in their pile, so each new entry looks back only at the entries that agree with it. At the end, take the cheapest entry and follow the choices back.

## The problem

The input is a fragment matrix with $n$ rows (the fragments, usually reads) and $m$ columns (the heterozygous variant sites). Entry $F_i(j)$ is 0, 1 or a hole, and each non-hole entry has a weight $w_i(j) \ge 0$, often its Phred quality. Find a bipartition $(R, S)$ of the fragments and two haplotypes $h_1, h_2 \in \{0, 1\}^m$ that minimize the total weight of the entries that differ from the haplotype of their part:

$$\sum_{i \in R} \sum_{j : F_i(j) \ne h_1(j)} w_i(j) + \sum_{i \in S} \sum_{j : F_i(j) \ne h_2(j)} w_i(j).$$

With all weights 1 this is MEC; with weights it is weighted MEC (wMEC). In the all-heterozygous form, $h_2$ must be the complement of $h_1$.

A fragment is *active* at every column from its first to its last non-hole entry, holes inside included, and $A(j)$ is the set of fragments active at column $j$. The coverage $c$ is the largest $|A(j)|$. For a set $X$ of fragments, $W_j(X, a)$ is the weight of the entries of $X$ in column $j$ that are not $a$: the cost to set them all to $a$.

## The algorithm

For a bipartition $B$ of $A(j)$ and a set $Y$, $B \cap Y$ is the bipartition that $B$ induces on $A(j) \cap Y$.

```pseudo id=main
WHATSHAP-MEC(F, w, m)
L1  A(j) ← the fragments active at column j, for j = 1, ..., m
L2  for j ← 1 to m do
L3      X ← A(j)
L4      for each bipartition B = (R, S) of X do
L5          Δ(j, B) ← min_a W_j(R, a) + min_a W_j(S, a)
L6          if j = 1 then C(j, B) ← Δ(j, B)
L7          else C(j, B) ← Δ(j, B) + C̄(j - 1, B ∩ A(j - 1))
L8      C̄(j, B') ← min C(j, B) over the B with B ∩ A(j + 1) = B', and D(j, B') ← that B
L9  B*(m) ← a bipartition B of A(m) with the least C(m, B)
L10 for j ← m - 1 down to 1 do B*(j) ← D(j, B*(j + 1) ∩ A(j))
L11 h1(j), h2(j) ← the alleles that reach the two minima of Δ(j, B*(j)), for each j
L12 return C(m, B*(m)), h1, h2 and the parts of B*
```

Line L5 is the cost of column $j$ alone: each part takes the allele that is cheaper for it, and the entries against it are flipped. In the all-heterozygous form, line L5 becomes $\min_a (W_j(R, a) + W_j(S, 1 - a))$. Line L7 joins column $j$ to the best solution of the columns before it that agrees with $B$ on the fragments that are active at both $j - 1$ and $j$. Line L8 groups the entries of column $j$ by the part that will matter at column $j + 1$, which is how the table moves from one set of active fragments to the next: a fragment that ends at $j$ is dropped, and one that starts at $j + 1$ can go to either side.

The code encodes a bipartition of $A(j)$ as a bit mask, with bit $t$ set when the $t$-th active fragment is in $S$. It computes $W_j(X, 0)$ and $W_j(X, 1)$ for all masks $X$ at once, each from the mask with its lowest bit removed, and it maps a mask over $A(j)$ to a mask over $A(j) \cap A(j + 1)$ with a table built the same way.

## Example

The example of Patterson et al. (2015) has four fragments and two columns, with weights in brackets:

| fragment | column 1 | column 2 |
|---|---|---|
| $f_0$ | 0 (5) | |
| $f_1$ | 1 (3) | 0 (2) |
| $f_2$ | 1 (6) | 1 (1) |
| $f_3$ | | 0 (2) |

So $A(1) = \{f_0, f_1, f_2\}$ and $A(2) = \{f_1, f_2, f_3\}$. Column 1 has eight bipartitions; four of them, with the other four the same with $R$ and $S$ exchanged, are:

| $R$ | $S$ | $\Delta(1, B)$ | flips |
|---|---|---|---|
| $f_0, f_1, f_2$ | none | 5 | $f_0$ to 1 |
| $f_1, f_2$ | $f_0$ | 0 | none |
| $f_0, f_2$ | $f_1$ | 5 | $f_0$ to 1 |
| $f_0, f_1$ | $f_2$ | 3 | $f_1$ to 0 |

Line L8 groups these by the side of $f_1$ and $f_2$, the fragments that are also active at column 2. When $f_1$ and $f_2$ are on the same side, the best is 0 (with $f_0$ on the other side). When they are apart, the best is 3. At column 2, $f_1$ shows 0 and $f_2$ shows 1, so keeping them together costs 1, the weight of $f_2$ at column 2, whichever side $f_3$ takes. Splitting them costs at least $3 + 0$. The optimum is 1: the code returns $R = \{f_1, f_2, f_3\}$ with $h_1 = 10$ and $S = \{f_0\}$ with $h_2 = 00$, and the one flip is the entry of $f_2$ at column 2. In the all-heterozygous form the cost is also 1, with $h_2 = 01$.

## Correctness

Two facts make the table work. First, for a fixed bipartition of all fragments, the cost is a sum over columns, and the term of column $j$ depends only on the fragments in $A(j)$, so the best haplotypes are found column by column, by line L5. Second, a fragment is active on an interval of columns, so a sequence of bipartitions of the sets $A(j)$ that agree on every pair of adjacent columns comes from one bipartition of all fragments: a fragment cannot change sides without leaving its interval. Lines L6 to L8 compute, by induction on $j$, the least cost over such sequences that end in a given bipartition, and lines L9 to L11 follow the stored choices back. The proof is in proofs/correctness.md, and the tests compare the code with a search over all pairs of haplotypes.

## Complexity

- **Time.** Column $j$ costs $O(2^{|A(j)|})$ for the subset sums, $\Delta$, the projection and $C$. The total is $O(2^c m)$, plus $O(n + \sum_i \ell_i)$ to find the active sets, where $\ell_i$ is the number of columns a fragment spans. The read length does not enter, only how many reads overlap at one place.
- **Half the masks.** $(R, S)$ and $(S, R)$ have the same cost, so an implementation can keep one of the two and get $O(2^{c-1} m)$, the bound of Patterson et al. The code keeps both.
- **Space.** The back pointers take $O(2^c m)$ space. Only two columns of costs are kept at a time.
- **In practice.** With $c = 20$, a column has about $10^6$ entries, so tools first select a subset of the reads that keeps the coverage below a set value, and phase with the rest.

## Properties

- **Exact.** It returns an optimal solution of weighted MEC, a theorem, not a heuristic. The result is optimal for the reads that it is given; after read selection it is optimal for the selected reads only.
- **Fixed-parameter tractable in the coverage.** MEC is [NP-hard](/np-hard/), even for gapless fragments, so no polynomial algorithm is expected. This one is polynomial for each fixed coverage.
- **Linear in the number of columns.** It does not depend on how many columns a read spans, so long reads with many variants cost no more per column than short ones.
- **One pass.** It goes once from left to right and once back. The table does not depend on the order of the reads.

## Variants and improvements

- **All-heterozygous.** If the columns are known heterozygous sites, $h_2$ is the complement of $h_1$; only line L5 changes.
- **Genotypes and pedigrees.** Later work on WhatsHap extends the same dynamic program to re-genotype the sites and to phase a parent and child trio together, with a cost that grows with the number of people.
- **Read selection.** Before the dynamic program, keep a subset of the reads with high quality and many variants, with the coverage of each column at most a bound.
- **Polyploid genomes.** With $k$ haplotypes, the table has one entry for each assignment of the active reads to $k$ parts, $k^c$ entries per column.
- **Heuristics for higher coverage.** [Haplotype assembly](/haplotype-assembly/) tools such as HapCUT use max-cut style local search instead of an exact table, with no bound on the coverage.

## When to use it

Use it to phase one diploid sample from long reads, or from paired or linked reads, when the coverage after read selection is small, about 15 to 20. It is the standard exact method for this case. For short reads with few variants per read, a heuristic is fast enough and gives about the same phase. For the phase of many people from genotypes, the problem is [haplotype phasing](/haplotype-phasing/), which this method does not solve.

## Pitfalls

- **The coverage is the coverage of active fragments.** A paired read is active over the gap between its mates, so a library of pairs with a long insert can have a much higher $c$ than its depth suggests.
- **Exponential memory.** The back pointers are $O(2^c m)$. A region of very high coverage, such as a repeat, can make one column too large.
- **Weights must be comparable.** wMEC adds the weights of different reads, so Phred values that are not calibrated give the wrong optimum.
- **Ties.** Many optima can have the same cost, as in the example, where $f_3$ can go to either side. A phase between two blocks with no read in common is not defined; the table then joins the blocks in an arbitrary way.
- **Homozygous columns.** A column where both haplotypes have the same allele carries no phase information; if it is in the input, use the free form, not the all-heterozygous form.

## Implementations

## History

Lancia et al. (2001) and Lippert et al. (2002) defined MEC and other models of haplotype assembly from fragment conflicts. MEC is NP-hard, and Cilibrasi et al. (2007) proved that it stays NP-hard when no fragment has a hole. Patterson et al. described WhatsHap, the dynamic program on this page, and published it in the Journal of Computational Biology in 2015, for third-generation reads that span many variants. The WhatsHap tool later added pedigree phasing and genotyping.

## References
