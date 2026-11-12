---
tag: H5YXHD
kind: algorithm
slug: colinear-chaining
name: Colinear chaining algorithm
aliases:
- sparse dynamic programming chaining
- fragment chaining
area: biology/sequence-alignment
level: advanced
summary: Finds a maximum-weight chain of matching fragments that increase in both sequences, by a sweep over one axis and a range-maximum tree over the other, in O(n log n) time.
solves: [seed-chaining]
model: comparison-model
complexity:
  vars: {n: the number of fragments}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1992
  people: [David Eppstein, Zvi Galil, Raffaele Giancarlo, Giuseppe F. Italiano]
  note: Sparse dynamic programming for fragment alignment; Abouelhoda and Ohlebusch (2005) gave the general chaining algorithm with range-maximum queries.
prereqs: [longest-increasing-subsequence, fenwick-tree]
see_also: [seed-chaining, maximal-exact-match, mummer, minimap2, weighted-interval-scheduling, dag-longest-path, segment-tree, whole-genome-alignment]
sources:
  - paper: doi:10.1145/146637.146650
    title: David Eppstein, Zvi Galil, Raffaele Giancarlo and Giuseppe F. Italiano, Sparse dynamic programming I, linear cost functions, Journal of the ACM 39(3), 1992
    locator: pages 519 to 545, the fragment alignment problem and its sparse dynamic program
  - paper: doi:10.1145/146637.146656
    title: David Eppstein, Zvi Galil, Raffaele Giancarlo and Giuseppe F. Italiano, Sparse dynamic programming II, convex and concave cost functions, Journal of the ACM 39(3), 1992
    locator: pages 546 to 567, fragment alignment with convex and concave gap costs
  - paper: doi:10.1016/j.jda.2004.08.011
    title: Mohamed Ibrahim Abouelhoda and Enno Ohlebusch, Chaining algorithms for multiple genome comparison, Journal of Discrete Algorithms 3(2-4), 2005
    locator: pages 321 to 341, the line-sweep chaining algorithm with range maximum queries over activated fragments, and its gap cost variants
  - paper: doi:10.1093/nar/27.11.2369
    title: Arthur L. Delcher, Simon Kasif, Robert D. Fleischmann, Jeremy Peterson, Owen White and Steven L. Salzberg, Alignment of whole genomes, Nucleic Acids Research 27(11), 1999
    locator: pages 2369 to 2376, Sorting the MUMs (a variant of the longest increasing subsequence algorithm that chains MUMs)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design
    locator: Chapter 6, Alignments (sparse dynamic programming and the chaining of anchors)
  - paper: doi:10.1016/0012-365X(75)90103-X
    title: Michael L. Fredman, On computing the length of longest increasing subsequences, Discrete Mathematics 11(1), 1975
    locator: pages 29 to 35, the lower bound on comparisons for the longest increasing subsequence
---

The colinear chaining algorithm takes $n$ matching fragments between two sequences, each a rectangle with a weight, and finds a heaviest *chain*: a list of fragments that move forward in both sequences at once. It runs in $\Theta(n \log n)$ time and $\Theta(n)$ space by a sweep along the first sequence that keeps a range-maximum tree, such as a [Fenwick tree](/fenwick-tree/), over the second. The method is sparse dynamic programming in the sense of Eppstein, Galil, Giancarlo and Italiano (1992); Abouelhoda and Ohlebusch (2005) gave it in this general form for genome comparison. It is exact for the chaining model without gap costs, and it is the step that turns the many [maximal exact matches](/maximal-exact-match/) or k-mer hits of two genomes into one backbone alignment, as in [MUMmer](/mummer/). With gap costs the problem is [seed chaining](/seed-chaining/), which needs other methods.

## In plain words

You compare two long DNA sequences and find many short places where they agree. Each place says "this part of the first sequence matches that part of the second". If the two sequences are related, the true matches come in the same order in both: when a match is earlier in the first sequence, it is also earlier in the second. Chance matches break this order.

Chaining picks the set of matches with the largest total size that keeps the order and does not overlap. It looks at the matches from left to right along the first sequence. For each match it asks: what is the best chain that ends before this match in both sequences? A small tree answers this question fast, so the whole job takes little more time than sorting the matches.

## The problem

A *fragment* $f$ is a pair of intervals and a weight: it covers $[x_1(f), x_2(f)]$ in the first sequence and $[y_1(f), y_2(f)]$ in the second, with $x_1 \le x_2$, $y_1 \le y_2$ and an integer weight $w(f) > 0$. For an exact match of length $\ell$ at positions $i$ and $j$, this is $[i, i+\ell-1] \times [j, j+\ell-1]$ with $w = \ell$.

Fragment $f$ *precedes* $g$, written $f \prec g$, when

$$x_2(f) < x_1(g) \quad\text{and}\quad y_2(f) < y_1(g).$$

So $f$ ends before $g$ starts in both sequences. The relation is transitive. A *chain* is a list $f_1 \prec f_2 \prec \cdots \prec f_r$, and its weight is $\sum w(f_i)$.

**Task.** Given $n$ fragments, find a chain of maximum weight.

The input is only the fragments; the sequences themselves are not needed. The model is the [comparison model](/comparison-model/) on the coordinates, plus integer addition of weights.

## The algorithm

Let $\mathit{score}(f)$ be the maximum weight of a chain that ends with $f$. Then

$$\mathit{score}(f) = w(f) + \max\bigl(\{0\} \cup \{\mathit{score}(g) : g \prec f\}\bigr).$$

This is a longest path in the DAG of $\prec$ ([DAG longest path](/dag-longest-path/)), but that DAG can have $\Theta(n^2)$ edges. The sweep avoids them. Each fragment gives two events: a *start* at $x_1(f)$, where its score is computed, and an *end* at $x_2(f)$, where it becomes *active*, that is, available as a predecessor. When the sweep reaches the start of $f$, the active fragments are exactly those with $x_2(g) < x_1(f)$, so the first condition of $\prec$ holds by itself, and the second condition $y_2(g) < y_1(f)$ is a prefix of the $y$ axis. A tree $T$ keyed by $y_2$ answers "the largest score among active fragments with $y_2 < y$" in $O(\log n)$ time.

```pseudo id=main
COLINEAR-CHAIN(F)                         ▷ F: n fragments (x1, x2, y1, y2, w)
L1  E ← the events (x1(f), start, f) and (x2(f), end, f) for each f in F
L2  sort E by coordinate, and put start before end at equal coordinates
L3  T ← a prefix-maximum tree over the sorted values y2(f), all entries (0, NIL)
L4  for each event (c, type, f) in E, in order do
L5      if type = start then
L6          (s, g) ← T.MAX-BELOW(y1(f))   ▷ best active fragment with y2 < y1(f)
L7          score[f] ← w(f) + s; pred[f] ← g
L8      else T.RAISE(y2(f), (score[f], f))
L9  f* ← a fragment with the largest score
L10 return score[f*] and the chain f*, pred[f*], pred[pred[f*]], … in reverse
```

Line L2 puts starts first at equal coordinates, so a fragment that ends at $c$ is not a predecessor of one that starts at $c$; this gives the strict inequality $x_2(g) < x_1(f)$. It also puts the start of each fragment before its own end, since $x_1 \le x_2$. Line L6 counts the $y_2$ values below $y_1(f)$ by binary search and takes the prefix maximum. Line L8 raises one slot to the new value. A [segment tree](/segment-tree/) or a balanced search tree with maxima works as well as a Fenwick tree.

## Example

Six fragments, with the coordinates in the first and second sequence:

| fragment | $[x_1, x_2]$ | $[y_1, y_2]$ | $w$ |
|---|---|---|---|
| A | $[0, 4]$ | $[2, 6]$ | 5 |
| B | $[3, 8]$ | $[10, 15]$ | 6 |
| C | $[6, 9]$ | $[8, 11]$ | 4 |
| D | $[11, 15]$ | $[12, 16]$ | 5 |
| E | $[12, 14]$ | $[20, 22]$ | 3 |
| F | $[17, 22]$ | $[18, 23]$ | 6 |

The sorted events are: start A (0), start B (3), end A (4), start C (6), end B (8), end C (9), start D (11), start E (12), end E (14), end D (15), start F (17), end F (22).

- Start A: nothing is active, so $\mathit{score}(A) = 5$.
- Start B: nothing is active (A ends at 4, after 3), so $\mathit{score}(B) = 6$. A and B overlap in the first sequence.
- End A makes A active with $y_2 = 6$. Start C asks for $y_2 < 8$ and finds A, so $\mathit{score}(C) = 4 + 5 = 9$.
- End B and end C make B ($y_2 = 15$) and C ($y_2 = 11$) active. Start D asks for $y_2 < 12$: A (5) and C (9) qualify, B does not, so $\mathit{score}(D) = 5 + 9 = 14$. Start E asks for $y_2 < 20$: A, B and C qualify, so $\mathit{score}(E) = 3 + 9 = 12$.
- End E and end D make E ($y_2 = 22$) and D ($y_2 = 16$) active. Start F asks for $y_2 < 18$: the best is D with 14, so $\mathit{score}(F) = 6 + 14 = 20$. E is not usable, because it ends at 22 in the second sequence.

The best chain is $A \prec C \prec D \prec F$ with weight 20. B is heavier than C but crosses D in the second sequence ($15 \ge 12$), and E is out of order with F. These two are the kind of fragments, such as matches from repeats, that chaining removes.

## Correctness

The proof is by induction over the events. *Invariant:* when the sweep reaches an event, every fragment whose start event is already processed has its correct $\mathit{score}$, and $T$ holds $(\mathit{score}(g), g)$ at slot $y_2(g)$ for exactly the fragments $g$ whose end event is already processed. At the start event of $f$, by the order of line L2, the processed end events are those with $x_2(g) < x_1(f)$. Each such $g$ has its start before its end, so its score is final. Line L6 then returns the largest score among the fragments $g$ with $x_2(g) < x_1(f)$ and $y_2(g) < y_1(f)$, which are exactly the $g \prec f$, or 0 when there is none. This is the recurrence, so $\mathit{score}(f)$ is correct. A best chain ends at some fragment, so line L9 finds its weight, and the pointers $\mathit{pred}$ list a chain of that weight. The full proof is in the proofs file.

## Complexity

| step | time | space |
|---|---|---|
| sort $2n$ events and $n$ values of $y_2$ | $\Theta(n \log n)$ | $\Theta(n)$ |
| $n$ queries and $n$ updates on $T$ | $O(n \log n)$ | $\Theta(n)$ |
| trace back | $O(n)$ | $\Theta(n)$ |

The time is $\Theta(n \log n)$ in the worst case and the extra space is $\Theta(n)$. If the coordinates are small integers, the sort is a counting sort and the tree can be a van Emde Boas tree, which gives $O(n \log \log n)$ time; Eppstein et al. reach such bounds.

**Lower bound.** In the comparison model no algorithm does better than $\Theta(n \log n)$ in the worst case. Given a sequence $a_1, \ldots, a_n$ of distinct numbers, the fragments $[i, i] \times [a_i, a_i]$ with weight 1 have as their chains exactly the increasing subsequences, so a best chain is a [longest increasing subsequence](/longest-increasing-subsequence/). Fredman (1975) showed that computing the length of a longest increasing subsequence needs $n \log_2 n - n \log_2 \log_2 n + O(n)$ comparisons in the worst case.

## Properties

- **Exact.** It returns an optimal chain for the model, not an approximation.
- **Output independent of the sequences.** It sees only coordinates and weights, so the sequence length does not enter the cost.
- **Ties.** Several chains can have the best weight; the tie rule of the tree decides which one is returned.
- **One chain.** It returns one best chain. The scores of all fragments are a by-product, so the best chain that ends at each fragment is also available.

## Variants and improvements

- **Gap costs.** Real chains pay for the distance between fragments. With a cost that is linear in the $L_1$ or $L_\infty$ gap, the scores can be shifted so that the same sweep still works in $O(n \log n)$ time (Abouelhoda and Ohlebusch). With concave or convex gap costs the sparse dynamic programs of Eppstein et al. apply. The scoring of [minimap2](/minimap2/) is not of this kind, so minimap2 uses a quadratic recurrence with a bounded number of predecessors; see [seed chaining](/seed-chaining/).
- **Overlaps.** Fragments that overlap in one sequence can be allowed if the overlapping part is cut from the weight. MUMmer's chaining of MUMs takes the lengths of the matches and their overlaps into account.
- **More than two sequences.** For $d$ sequences, fragments are boxes in $d$ dimensions, and the sweep needs a range-maximum structure in $d - 1$ dimensions, such as a $k$-d tree or a range tree, which costs more per query.
- **Weighted interval scheduling.** With one sequence only, chaining is [weighted interval scheduling](/weighted-interval-scheduling/), solved by the same recurrence after sorting.
- **Longest increasing subsequence.** With unit weights and single points, it is the LIS problem, and the sweep becomes patience sorting with binary search.

## When to use it

Use it when you have a set of exact or near-exact anchors between two sequences and you want the heaviest ordered subset, as the backbone of a [whole-genome alignment](/whole-genome-alignment/) or of a long-read alignment. It is a good choice when the anchors are long and the gaps between them do not need a precise cost. When the gap cost matters, for example to separate two copies of a gene, use a gap-aware [seed chaining](/seed-chaining/) method. When the two sequences are rearranged, one chain covers only one collinear block: run the chaining repeatedly, or use a method that finds many chains.

## Pitfalls

- **Strict and loose order.** With $\le$ instead of $<$, touching fragments chain, and a match of length $\ell$ split into two pieces can count its middle letter twice. Fix the order of events at equal coordinates on purpose.
- **Order of events.** If the end event of $g$ comes before the start event of $f$ at the same coordinate, the algorithm allows $x_2(g) = x_1(f)$, which is the loose order.
- **The other strand.** Matches on the reverse complement strand have decreasing $y$ as $x$ grows. Chain them separately, after flipping their $y$ coordinates.
- **Negative weights.** If a weight can be zero or negative, a chain should not be forced to include it; the term $\max(0, \cdot)$ in the recurrence handles predecessors but not the fragment itself. Drop such fragments first.
- **Too many fragments.** With short matches, $n$ can be close to the product of the sequence lengths. Use a minimum match length, or unique matches, before chaining.

## Implementations

## History

Wilbur and Lipman (1983) already joined diagonal word matches into an alignment for fast sequence comparison. Eppstein, Galil, Giancarlo and Italiano (1992) treated such problems as *sparse dynamic programming*, where only $n$ cells of a large table matter, and gave fast algorithms for the fragment alignment problem with linear, convex and concave gap costs. MUMmer (Delcher et al., 1999) chained the maximal unique matches of two genomes with a variant of the longest increasing subsequence algorithm. Abouelhoda and Ohlebusch (2005) gave the chaining algorithm in its general form, with a line sweep and range-maximum queries over activated fragments, for two or more genomes and for several gap costs.

## References
