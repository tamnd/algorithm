---
tag: 5WRFD0
kind: algorithm
slug: greedy-motif-search
name: Greedy motif search
aliases:
- CONSENSUS algorithm
area: biology/gene-finding-and-motifs
level: intro
summary: Seed with each window of the first sequence, add from each next sequence the window most probable under the profile of the windows so far, and keep the best result.
solves: [motif-finding-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1"}
  time: {worst: O(W^2 n L), average: O(W^2 n L)}
  space: {extra: O(n L)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Gerald Z. Hertz, George W. Hartzell, Gary D. Stormo]
  note: Hertz, Hartzell and Stormo built a weight matrix from unaligned sequences by adding one sequence at a time. Hertz and Stormo (1999) described the CONSENSUS program with p-values. The plain form on this page is the GreedyMotifSearch of Compeau and Pevzner.
prereqs: [motif-finding-problem, position-specific-scoring-matrix, greedy-algorithm]
see_also: [randomized-motif-search, gibbs-motif-sampler, branch-and-bound-motif-search, median-string-problem, motif-information-content, laplace-smoothing, consensus-sequence, meme-algorithm]
sources:
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Section 2.5 (greedy motif search) and the section on pseudocounts that follows it
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 5, Section 5.5, a greedy approach to motif finding (the seed from the best pair of windows)
  - paper: doi:10.1093/bioinformatics/6.2.81
    title: Gerald Z. Hertz, George W. Hartzell and Gary D. Stormo, Identification of consensus patterns in unaligned DNA sequences known to be functionally related, CABIOS 6(2), 1990
    locator: pp. 81 to 92, the greedy construction of a weight matrix, one sequence at a time
  - paper: doi:10.1093/bioinformatics/15.7.563
    title: Gerald Z. Hertz and Gary D. Stormo, Identifying DNA and protein patterns with statistically significant alignments of multiple sequences, Bioinformatics 15, 1999
    locator: pp. 563 to 577, the CONSENSUS program, its information content score and the p-values of the alignments
---

Greedy motif search is a fast heuristic for the [motif finding problem](/motif-finding-problem/). It tries each window of the first sequence as a seed. From the seed it builds a profile, the column frequencies of the windows chosen so far, and adds from each next sequence the window that is most probable under that profile. The best of the $W$ results is the output. It runs in $O(W^2 n L)$ time, but it can miss the optimum, and without pseudocounts it often does.

## In plain words

Start with one short piece of the first sequence and guess that it is the hidden word. Look in the second sequence for the piece that best fits your guess, and add it to your list. Now you have two pieces. For each column, count the letters of the pieces. Look in the third sequence for the piece that best fits these counts, and add it. Go on to the last sequence.

Do this once for every possible start piece in the first sequence, and keep the list whose pieces agree best. Each choice is made once and never changed, which is why the method is called greedy. A small fix helps a lot: add one to every count, so that a letter that you have not seen yet in a column is not ruled out.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$, each of length $G$, a motif length $L$, and a pseudocount $b \ge 0$ (0 or 1 in practice). Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**Output.** One window $t_i$ in each sequence, with a small motif score $\mathrm{Score}(t_1, \ldots, t_n) = \sum_j (n - \max_a c_j(a))$, where $c_j(a)$ counts the letter $a$ in column $j$ of the windows. The method does not promise the smallest score.

## The algorithm

Let the counts of the first $i - 1$ chosen windows, plus $b$, be $c_j(a)$. The profile is $P_j(a) = c_j(a) / (i - 1 + 4b)$, and the probability of a window $w$ is $\prod_j P_j(w_j)$. All windows share the denominator $(i - 1 + 4b)^L$, so the most probable window is the one with the largest product of counts $\prod_j c_j(w_j)$, an exact integer.

```pseudo id=main
GREEDY-MOTIF(s[1 .. n], L, b)
L1  best ← (s_1[1 .. L], ..., s_n[1 .. L]), bestscore ← Score(best)
L2  for q ← 1 to W do
L3      t_1 ← s_1[q .. q + L - 1], c_j(a) ← b for every column j and letter a
L4      for i ← 2 to n do
L5          add the letters of t_(i-1) to the counts c
L6          t_i ← the first window w of s_i with the largest Π_j c_j(w_j)
L7      if Score(t_1, ..., t_n) < bestscore then best ← (t_1, ..., t_n), bestscore ← Score(best)
L8  return best
```

Line L1 starts from the first window of every sequence, as Compeau and Pevzner do. Line L3 picks the seed. Lines L5 and L6 are the greedy step: the profile of the windows chosen so far picks the next window, and the choice is never undone. Line L6 breaks ties by the first window, and if every product is 0 (possible only with $b = 0$), it takes the first window of the sequence. Line L7 keeps a new result only if it is strictly better.

## Example

Take the five sequences of Rosalind problem BA2D, GGCGTTCAGGCA, AAGAATCAGTCA, CAAGGAGTTCGC, CACGTCAATCAC and CAATAATATTCG, with $L = 3$. The table shows the result of each seed for $b = 0$ and for $b = 1$, with the 1-based starts:

| seed $q$ | windows, $b = 0$ | score | windows, $b = 1$ | score |
|---|---|---|---|---|
| 1 | GGC AAG AAG CAC CAA | 7 | GGC GTC GGA GTC TTC | 4 |
| 2 | GCG AAG AAG ACG CAA | 5 | GCG AAG AAG ACG TCG | 4 |
| 3 | CGT AAG AAG AAT AAT | 4 | CGT AGT AGT CGT AAT | 3 |
| 4 | GTT AAG AAG AAT AAT | 4 | GTT GTC GTT GTC ATT | 3 |
| 5 | TTC AAG AAG ATC TTC | 6 | TTC ATC TTC ATC TTC | 2 |
| 6 | TCA TCA CAA TCA TAA | 3 | TCA TCA TCG TCA TCG | 2 |
| 7 | CAG CAG CAA CAA CAA | 2 | CAG CAG CAA CAA CAA | 2 |
| 8 | AGG AAG AAG CAC CAA | 5 | AGG AAG AAG ACG AAT | 3 |
| 9 | GGC AAG AAG CAC CAA | 7 | GGC GTC GGA GTC TTC | 4 |
| 10 | GCA AAG AAG ACG CAA | 6 | GCA GAA GGA TCA TAA | 5 |

With $b = 0$ the output is CAG, CAG, CAA, CAA, CAA from seed 7, at starts 7, 7, 1, 6, 1, which is the sample answer of BA2D. With $b = 1$ the first seed that reaches score 2 is seed 5, and the output is TTC, ATC, TTC, ATC, TTC, the sample answer of BA2E. Both have score 2, the optimum of this input.

The $b = 0$ column shows the trouble with zero counts. With seed 7, the profile of CAG and CAG gives probability 0 to every window of $s_3$, since $s_3$ has no CAG, and line L6 falls back to the first window CAA. Most seeds take AAG in $s_2$ for the same reason: no window of $s_2$ equals the seed, so every product is 0 and AAG, the first window, is taken. The profile of the seed and AAG then makes AAG the most probable window of $s_3$ too.

**A miss.** On CAGAACCT, GCTGTGAC and ATAAACTA with $L = 3$, the optimum is AAC, GAC, AAC (starts 4, 6, 4) with score 1. With $b = 0$, the seed AAC gives probability 0 to every window of the second sequence, since none is AAC, so the search takes the first window GCT, and the best of all seeds has score 2. With $b = 1$, GAC gets a positive probability and the optimum is found.

**Measured success on planted motifs.** The test generator plants a motif with exactly $d$ changes in each of 10 random sequences. A run counts as a success when the consensus of the output equals the planted motif. Over seeds 0 to 19:

| $G$ | $(L, d)$ | $b = 0$ | $b = 1$ |
|---|---|---|---|
| 100 | (8, 1) | 1 of 20 | 19 of 20 |
| 100 | (10, 2) | 0 of 20 | 10 of 20 |
| 200 | (12, 3) | 0 of 20 | 4 of 20 |

These are measurements on these seeds, not guarantees.

## Correctness

The method is a heuristic, so the claim is about what it returns, not about optimality. Each returned $t_i$ is a window of $s_i$, since line L6 picks from the windows of $s_i$ and line L1 starts with windows. The returned score is the smallest score over the $W$ seed runs and the start, since line L7 keeps a strict minimum. Line L6 returns a most probable window: the profile probabilities of all windows have the same denominator, so their order is the order of the integer products. The greedy result is not always optimal; the miss above is a counterexample, and the tests check it against brute force. The proof of the facts about line L6 and line L7 is in proofs/correctness.md.

## Complexity

- **Time.** There are $W$ seeds. For each seed and each of the $n - 1$ later sequences, line L5 takes $O(L)$ time and line L6 scans $W$ windows at $O(L)$ time each. Line L7 takes $O(nL)$. So the total is $O(W (n W L + n L)) = O(W^2 n L)$.
- **Space.** The counts take $4L$ words and the chosen windows $nL$ letters, so $O(nL)$.
- **In practice.** For $n = 20$, $G = 600$ and $L = 15$, $W^2 n L = 586^2 \times 20 \times 15 \approx 1.0 \times 10^8$ steps, which is fast. The exact searches cost $4^L$ or $W^n$ instead.

## Properties

- **Deterministic.** There is no randomness, and ties go to the first window and the first seed.
- **Not exact.** It can return a score above the optimum, as in the miss above.
- **Order dependent.** The result depends on the order of the sequences: the seed comes from $s_1$ and the profile grows in the given order. Another order can give another result.
- **Pseudocounts matter.** With $b = 0$ a single unseen letter gives a window probability 0, and the search can fall back to the first window of a sequence for no reason in the data. With $b = 1$ ([Laplace's rule](/laplace-smoothing/)) every window has a positive probability.

## Variants and improvements

- **The best pair as the seed.** Jones and Pevzner start from the pair of windows of $s_1$ and $s_2$ with the best score and then add one sequence at a time. The cost of the seed step is $O(W^2 L)$.
- **CONSENSUS.** The program of Hertz and Stormo builds alignments one sequence at a time in the same way, but it scores them by [information content](/motif-information-content/) against the background, and it reports the statistical significance of the result. It differs from the plain greedy search on this page in its score and its details.
- **Several orders.** Run the search with several orders of the sequences and keep the best result, to reduce the effect of the order.
- **As a start for a local search.** The output is a good start for a [randomized motif search](/randomized-motif-search/) or a [Gibbs sampler](/gibbs-motif-sampler/), or a first bound for a [branch and bound search](/branch-and-bound-motif-search/).

## When to use it

Use greedy motif search when you need a quick answer or a starting point, and the motif is strong: a long motif with few changes in each site. Always use a pseudocount. When the motif is subtle, as in the [planted (15, 4) motif](/planted-motif-problem/) of Pevzner and Sze, the greedy search fails most of the time, and a randomized search, [MEME](/meme-algorithm/) or [PROJECTION](/random-projection-motif-finding/) is the better choice. When $L$ is small, an exact [median string](/median-string-problem/) search is affordable and gives the optimum.

## Pitfalls

- **No pseudocounts.** With $b = 0$, most windows get probability 0 after one or two steps, and line L6 picks the first window of a sequence by default. The success rates above drop from 19 of 20 to 1 of 20.
- **Floating point products.** The product of $L$ probabilities underflows for long motifs, and ties between equal products can break in a different way after rounding. Compare integer products of counts, or sums of logarithms with a fixed tie rule.
- **Scoring the profile and not the windows.** Line L7 compares the motif scores of the windows, not the probabilities of the profile, which grow as the profile becomes narrow.
- **Reading the output as the answer.** The output has a small score but need not be optimal. Check it with an exact method on small data, or run the search with several orders.

## Implementations

## History

Hertz, Hartzell and Stormo (1990) described a greedy method that builds a weight matrix from unaligned sequences one sequence at a time and keeps the matrix least likely to arise by chance. Hertz and Stormo (1999) revised it as the CONSENSUS program, with an information content score and p-values for the alignments. Jones and Pevzner (2004) presented a greedy motif search that starts from the best pair of windows, and Compeau and Pevzner (2015) the form on this page, with every window of the first sequence as a seed and with Laplace's rule of succession as the fix for zero counts. The greedy search is now the standard first example of a motif finding heuristic.

## References
