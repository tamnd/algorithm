---
tag: BSR162
kind: algorithm
slug: exon-chaining
name: Exon chaining
aliases:
- weighted interval chaining of exons
area: biology/gene-finding-and-motifs
level: intro
summary: Choose a set of non-overlapping candidate exons of maximum total weight by dynamic programming over their sorted end points.
solves: [weighted-interval-scheduling]
model: word-ram
complexity:
  vars: {n: the number of candidate exons}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [weighted-interval-scheduling, gene-prediction]
see_also: [spliced-alignment-problem, colinear-chaining, dag-longest-path, seed-chaining, generalized-hmm-gene-finder, spliced-read-alignment, smith-waterman, interval-tree]
sources:
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 6.13, Similarity-Based Approaches to Gene Prediction (the Exon Chaining problem on p. 201, the algorithm ExonChaining, and figures 6.26 and 6.27); Problem 6.56
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design, Addison-Wesley, 2005
    locator: Section 6.1, Weighted Interval Scheduling, A Recursive Procedure
  - paper: doi:10.1073/pnas.93.17.9061
    title: Mikhail S. Gelfand, Andrey A. Mironov and Pavel A. Pevzner, Gene recognition via spliced sequence alignment, Proceedings of the National Academy of Sciences USA 93(17), 1996
    locator: pp. 9061 to 9066; the spliced alignment that replaces a plain chain of exon scores by one alignment with the target protein
---

Exon chaining chooses, from a list of candidate exons in a genomic sequence, a set of exons that do not overlap and whose total weight is as large as possible. Each candidate is an interval of the genome with a weight, for example the score of a local alignment of that interval with a related protein. The problem is [weighted interval scheduling](/weighted-interval-scheduling/), and one sweep over the $2n$ sorted end points solves it exactly in $O(n \log n)$ time. The chosen chain is a quick first model of the exon structure of a gene; the [spliced alignment problem](/spliced-alignment-problem/) is the stricter version that also checks that the exons fit the protein in order.

## In plain words

Somebody has marked some stretches of a genome that may be pieces of a gene, and has given each stretch a score: how much it looks like a piece of a known protein. Stretches can overlap, but the pieces of a real gene do not. We want the set of stretches with no overlaps and the largest total score. Walk along the genome from left to right and keep one number: the best total so far. When a stretch starts, write down that number next to it. When the stretch ends, see if the number written at its start plus its own score beats the best total so far, and if it does, take it. At the end, the best total is the answer, and the notes tell which stretches give it.

## The problem

**Input.** A list of $n$ candidate exons $I_1, \ldots, I_n$. Exon $I_j = (l_j, r_j, w_j)$ covers the genome positions $l_j$ to $r_j$, both included, with $1 \le l_j \le r_j$, and has a weight $w_j$, a real number.

**Output.** A *chain*: a set of exons that pairwise do not overlap, listed from left to right, with the largest total weight. Two exons overlap when they share at least one position, so an exon that starts at the position where another ends overlaps it. The empty chain is allowed and has weight 0.

This is weighted interval scheduling with the genome as the time axis. Jones and Pevzner state it with positive weights and assume that all $2n$ end points are distinct, so that no exon starts exactly where another ends. The version here drops both assumptions: it allows any weights and equal end points, and the rule for equal points is part of the algorithm.

The input does not say where the candidates come from. In the setting of Jones and Pevzner, they are the parts of the genome that are similar to a target protein or mRNA, extended or shortened so that they sit between AG and GT dinucleotides, and the weight is the local alignment score or a mix of that score and the strength of the splice sites. This is a different task from [spliced read alignment](/spliced-read-alignment/) and [maximal mappable prefix alignment](/maximal-mappable-prefix-alignment/), which map millions of short RNA-seq reads to the genome; exon chaining and spliced alignment assemble one gene model from candidate exons and one related protein or transcript.

## The algorithm

Sort the $2n$ end points by position. At equal positions, put every left point before every right point, so that an exon that starts at position $x$ never counts as compatible with an exon that ends at $x$. Then scan. The variable `best` is the weight of the best chain among the exons whose right end has been passed. At the left end of $I_j$, store `best` as $s[j]$: by the order of the points, it is the best weight of a chain that ends before $l_j$. At the right end of $I_j$, the best chain that uses $I_j$ has weight $s[j] + w_j$, so compare it with `best`.

```pseudo id=main
EXON-CHAINING(I_1, ..., I_n)    ▷ I_j = (l_j, r_j, w_j) with l_j ≤ r_j
L1  P ← the 2n points (l_j, left, j) and (r_j, right, j)
L2  sort P by position, with left points before right points at equal positions
L3  best ← 0, last ← nil
L4  for each point (x, side, j) of P in sorted order do
L5      if side = left then
L6          s[j] ← best, pred[j] ← last
L7      else if s[j] + w_j > best then
L8          best ← s[j] + w_j, last ← j
L9  C ← the empty list, j ← last
L10 while j ≠ nil do put j at the front of C, j ← pred[j]
L11 return best, C
```

The variable `last` is the last exon of a best chain so far, and $\mathit{pred}[j]$ is the last exon of the best chain that ends before $I_j$. Lines L9 and L10 follow these links back to rebuild the chain.

Jones and Pevzner write the same scan as a longest path in a graph with $2n$ vertices, one per end point in sorted order, $2n - 1$ edges of weight 0 between neighbours and one edge of weight $w_j$ from $l_j$ to $r_j$ for each exon, so $3n - 1$ edges. With $s_i$ the longest path to the $i$-th vertex, $s_i = \max(s_{i-1}, s_{i'} + w)$ if vertex $i$ is the right end of an exon of weight $w$ whose left end is vertex $i'$, and $s_i = s_{i-1}$ otherwise. The pseudocode above keeps only the last value $s_{i-1}$ (as `best`) and the values at left ends (as $s[j]$), and it adds the tie rule and the traceback. The graph is a DAG, so this is a special case of the [longest path in a DAG](/dag-longest-path/).

## Example

Take seven candidate exons:

| exon | $l$ | $r$ | $w$ |
|---|---|---|---|
| A | 1 | 5 | 5 |
| B | 3 | 9 | 8 |
| C | 7 | 12 | 6 |
| D | 10 | 14 | 4 |
| E | 13 | 20 | 9 |
| F | 15 | 18 | 3 |
| G | 21 | 24 | 5 |

The sorted points and the actions of the scan are:

| position | point | line | action | best |
|---|---|---|---|---|
| 1 | left of A | L6 | $s[A] = 0$ | 0 |
| 3 | left of B | L6 | $s[B] = 0$ | 0 |
| 5 | right of A | L7, L8 | $0 + 5 = 5 > 0$ | 5, last A |
| 7 | left of C | L6 | $s[C] = 5$, $\mathit{pred}[C] = A$ | 5 |
| 9 | right of B | L7, L8 | $0 + 8 = 8 > 5$ | 8, last B |
| 10 | left of D | L6 | $s[D] = 8$, $\mathit{pred}[D] = B$ | 8 |
| 12 | right of C | L7, L8 | $5 + 6 = 11 > 8$ | 11, last C |
| 13 | left of E | L6 | $s[E] = 11$, $\mathit{pred}[E] = C$ | 11 |
| 14 | right of D | L7, L8 | $8 + 4 = 12 > 11$ | 12, last D |
| 15 | left of F | L6 | $s[F] = 12$, $\mathit{pred}[F] = D$ | 12 |
| 18 | right of F | L7, L8 | $12 + 3 = 15 > 12$ | 15, last F |
| 20 | right of E | L7, L8 | $11 + 9 = 20 > 15$ | 20, last E |
| 21 | left of G | L6 | $s[G] = 20$, $\mathit{pred}[G] = E$ | 20 |
| 24 | right of G | L7, L8 | $20 + 5 = 25 > 20$ | 25, last G |

The traceback goes G, E, C, A, so the best chain is A, C, E, G with weight $5 + 6 + 9 + 5 = 25$. The next best chain is B, E, G with weight 22. The exon B has the largest single weight but is not in the best chain. At position 13, E starts before D ends at 14, so $s[E]$ is 11 and not 12: D and E overlap. The test file checks this example and compares the result with a search over all subsets.

## Correctness

The proof is an induction over the sorted points. Let $R$ be the set of exons whose right point has been handled.

1. When the scan reaches the left point of $I_j$, the set $R$ is exactly the set of exons with $r_i < l_j$. An exon with $r_i = l_j$ is not in it, because left points sort first at equal positions.
2. At the right point of $I_j$, every exon of a chain inside $R \cup \{I_j\}$ has its right end at most $r_j$. In a chain that uses $I_j$, the other exons do not overlap $I_j$, so they all end before $l_j$. Their best weight is $s[j]$.
3. So the best weight inside $R \cup \{I_j\}$ is $\max(\mathit{best}, s[j] + w_j)$, which is what lines L7 and L8 compute.

At the end $R$ holds every exon, so `best` is the optimum (a theorem). The links $\mathit{pred}$ are written once, and each one points to an exon that ends before the current exon starts, so the traceback stops and gives a chain of weight `best`. The full proof is in the proofs folder.

## Complexity

- **Time.** On a word RAM with positions that fit in a word, line L2 sorts $2n$ points in $O(n \log n)$ time with a comparison sort. The loop of line L4 does $O(1)$ work per point, and the traceback takes at most $n$ steps. So the total is $\Theta(n \log n)$, and the sort is the only part above linear. If the points come sorted, for example from a scan along the genome, or if the positions are integers in a range of size $O(n)$, a counting sort or a merge of two sorted lists makes the whole method run in $O(n)$ time.
- **Lower bound.** For general interval scheduling, the sort cannot be avoided in the algebraic decision tree model; the [weighted interval scheduling](/weighted-interval-scheduling/) page gives the bound.
- **Space.** $\Theta(n)$ for the points and the arrays $s$ and $\mathit{pred}$.

The cost to find the candidate exons is not part of this. If they come from local alignments of a genome of length $G$ with a protein of length $m$, that step costs $O(G m)$ with [Smith-Waterman](/smith-waterman/), and it is much more than the chaining.

## Properties

- **Exact.** It returns a chain of the largest total weight; there is no approximation.
- **Weights of any sign.** An exon with $w_j \le 0$ is never chosen, because it cannot raise `best`. Fractions and integers give exact results.
- **Tie rule.** The strict test of line L7 keeps the first best chain found. Of all best chains, the returned one has the leftmost right end of its last exon.
- **Only overlap counts.** The weight of a chain is a plain sum. The chain does not know the order of the exons along the target protein, the reading frame, or the lengths of the introns between them.
- **Not online.** It needs all candidates before the scan, because it sorts them. If the candidates arrive in order of their left ends and the right ends are handled with a priority queue, the same scan runs as a stream.

## Variants and improvements

- **Equal weights.** If all exons have the same weight, the best chain is a largest set of disjoint intervals. The greedy rule "take the exon with the leftmost right end, drop the ones that overlap it, repeat" finds it. This is Problem 6.56 of Jones and Pevzner and the unweighted interval scheduling problem.
- **The textbook form.** Sort the exons by right end, find with [binary search](/binary-search/) the last exon $p(j)$ that ends before $l_j$, and set $\mathrm{OPT}(j) = \max(\mathrm{OPT}(j - 1), \mathrm{OPT}(p(j)) + w_j)$. This is the form of Kleinberg and Tardos. It gives the same value; the test file uses it as a second method.
- **Order along the target.** The best chain may join an exon that matches the end of the protein with a later exon that matches its start (figure 6.27 of Jones and Pevzner). If each candidate also has an interval on the target, ask for a chain that increases in both the genome and the target. This is [colinear chaining](/colinear-chaining/), which still runs in $O(n \log n)$ time with a range maximum tree.
- **Rules between neighbours.** A minimum intron length, a compatible reading frame, or a penalty for each intron depends on the pair of consecutive exons. Then the chain is a path in a DAG with an edge for each allowed pair, which costs $O(n^2)$ time in general, and less if the rule is a simple distance rule that a range query can handle.
- **Spliced alignment.** Score a chain by the alignment of the joined exons with the target, not by a sum of separate scores. This is the [spliced alignment problem](/spliced-alignment-problem/) of Gelfand, Mironov and Pevzner, solved by dynamic programming over the candidate blocks.
- **Gene finders.** A [generalized HMM gene finder](/generalized-hmm-gene-finder/) also builds the best chain of exons, but with scores for the exons, the introns and the signals between them, and with frame and strand rules. Exon chaining is the simplest case of that dynamic program.

## When to use it

Use it to turn a set of local hits of a protein or a transcript on a genome into a first gene model, when speed matters more than a full alignment. It is also the right tool for any selection of disjoint weighted intervals on a line: hits of a profile, ORFs, or seeds on one sequence. When the order along the target matters, use [colinear chaining](/colinear-chaining/) or [seed chaining](/seed-chaining/); when the exon boundaries and the alignment both matter, use [spliced alignment](/spliced-alignment-problem/). To map RNA-seq reads, use a read aligner such as [spliced read alignment](/spliced-read-alignment/); exon chaining does not map reads.

## Pitfalls

- **Ties at shared positions.** Sort left points first at equal positions, or treat exons as half-open intervals and say so. If right points sort first, two exons that share one base both enter the chain.
- **Distinct points in the book.** The graph of Jones and Pevzner assumes that no two end points are equal. Code that copies it without a tie rule gives wrong chains on real candidate sets, where many exons share a splice site.
- **The best chain is not always a gene.** A large weight can come from exons that match the target in the wrong order or in different frames. Check the order along the target, or use colinear chaining or spliced alignment. This is a limit of the model, not of the algorithm.
- **Fixed ends.** The candidate ends are fixed before the chain is chosen, so an exon with a slightly wrong end cannot be moved to fit its neighbour. Spliced alignment has the same issue in a smaller form.
- **Both strands.** Candidates on the plus and the minus strand can overlap in the genome but belong to different genes. Chain each strand on its own.
- **Recursion.** The memoized recursive form of Kleinberg and Tardos needs a depth of $n$. Use the loop.

## Implementations

## History

Weighted interval scheduling is a standard first example of dynamic programming in algorithm textbooks, for example Section 6.1 of Kleinberg and Tardos (2005). Jones and Pevzner (2004) present it as the Exon Chaining problem in Section 6.13 of their textbook, with candidate exons from similarity to a target protein, and they show its main weakness: a chain of separate high scores need not form one valid alignment. Gelfand, Mironov and Pevzner (1996) had already given the stronger formulation, spliced alignment, which scores the whole chain by one alignment with the target.

## References
