---
tag: 6XQ8GR
kind: algorithm
slug: branch-and-bound-motif-search
name: Branch-and-bound motif search
aliases:
- branch-and-bound median string search
area: biology/gene-finding-and-motifs
level: intro
summary: Search the tree of l-mers or of motif start positions and prune a subtree when a bound shows it cannot beat the best score so far.
solves: [motif-finding-problem]
model: word-ram
complexity:
  vars: {n: the number of sequences, G: the length of each sequence, L: the motif length, W: "the number of windows per sequence, G - L + 1"}
  time: {worst: O(4^L n W), best: O(L n W), position_tree_worst: O(L W^n)}
  space: {extra: O(n W + L)}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 2004
  people: [Neil C. Jones, Pavel A. Pevzner]
  note: Jones and Pevzner gave both searches, on the tree of start positions and on the tree of candidate strings, in their 2004 textbook. Branch and bound as a general method goes back to Land and Doig (1960).
prereqs: [motif-finding-problem, median-string-problem, depth-first-branch-and-bound]
see_also: [brute-force-search, best-first-branch-and-bound, greedy-motif-search, planted-motif-problem, gibbs-motif-sampler, consensus-sequence, hamming-distance, position-specific-scoring-matrix]
sources:
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 4, Sections 4.7 (search trees), 4.8 (finding motifs, the branch and bound search on start positions) and 4.9 (finding a median string, the branch and bound search on prefixes)
  - book: isbn:9780990374619
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, 2nd edition, Active Learning Publishers, 2015
    locator: Chapter 2, Section 2.4, the median string search by enumeration of all k-mers
---

Branch-and-bound motif search finds an optimal solution of the [motif finding problem](/motif-finding-problem/) with the total Hamming distance score, without a test of every candidate. It walks a search tree depth first, keeps the best complete score found so far, and cuts a subtree when a lower bound shows that no leaf below it can do better. There are two trees: the tree of start positions, with $W^n$ leaves, and the tree of prefixes of the candidate [median string](/median-string-problem/), with $4^L$ leaves. The worst case is the same as exhaustive search, but on real and planted data most of the tree is cut.

## In plain words

Exhaustive search tries every candidate. Branch and bound tries the candidates in an order where they share their beginnings, like words in a dictionary. While it builds a candidate letter by letter, it keeps count of the mistakes that the part built so far already makes. Mistakes never go away when you add more letters. So if the part built so far already makes as many mistakes as the best full answer you have found, you skip every candidate that starts with that part.

The same trick works when you pick one window in each sequence: pick the windows one sequence at a time, and stop when the windows picked so far already disagree too much.

## The problem

**Input.** DNA sequences $s_1, \ldots, s_n$, each of length $G$, and a motif length $L \le G$. Each sequence has $W = G - L + 1$ windows. Positions are 1-based on this page and 0-based in the code.

**Output, position tree.** Starts $p = (p_1, \ldots, p_n)$ that minimize $\mathrm{Score}(p) = \sum_j (n - \max_a c_j(a))$, where $c_j(a)$ counts the letter $a$ in column $j$ of the chosen windows.

**Output, prefix tree.** A string $v$ of length $L$ that minimizes $D(v) = \sum_i \min_q d_H(v, s_i[q .. q + L - 1])$.

The two optimal values are equal, and each optimum gives the other (see the [median string problem](/median-string-problem/)).

## The algorithm

**The position tree.** A node at depth $i$ fixes the starts of the first $i$ sequences. Its *partial score* is the motif score of those $i$ rows, $\sum_j (i - \max_a c_j(a))$. Adding a row raises $i$ by one and each $\max_a c_j(a)$ by at most one, so the partial score never drops on the way down. A node whose partial score is not below the best complete score can be cut.

**The prefix tree.** A node at depth $k$ is a prefix $u$ of length $k$. For each sequence $i$ and window $q$, let $m[i][q] = d_H(u, s_i[q .. q + k - 1])$, the mismatches of $u$ with the first $k$ letters of the window. The mismatches of a prefix stay when the string grows, so $\sum_i \min_q m[i][q]$ is a lower bound on $D(v)$ for every extension $v$ of $u$, and it equals $D(u)$ at a leaf.

```pseudo id=main
BB-MOTIF(s[1 .. n], L)
L1  best ← nL + 1, bestp ← none
L2  c_j(a) ← 0 for every column j and letter a
L3  SEARCH(1)
L4  return bestp, best
SEARCH(i)
L5  if i > n then
L6      sc ← Σ_j (n - max_a c_j(a))
L7      if sc < best then best ← sc, bestp ← (p_1, ..., p_n)
L8      return
L9  for q ← 1 to W do
L10     p_i ← q, add the letters of s_i[q .. q + L - 1] to the counts c
L11     if Σ_j (i - max_a c_j(a)) < best then SEARCH(i + 1)
L12     remove the letters of s_i[q .. q + L - 1] from the counts c
BB-MEDIAN(s[1 .. n], L)
L13 best ← nL + 1, bestv ← none
L14 m[i][q] ← 0 for every sequence i and window q
L15 EXTEND(empty string, 0)
L16 return bestv, best
EXTEND(u, k)
L17 bound ← Σ_i min_q m[i][q]
L18 if bound ≥ best then return
L19 if k = L then best ← bound, bestv ← u, return
L20 for a in A, C, G, T do
L21     for every i and q: if s_i[q + k] ≠ a then m[i][q] ← m[i][q] + 1
L22     EXTEND(ua, k + 1)
L23     for every i and q: if s_i[q + k] ≠ a then m[i][q] ← m[i][q] - 1
```

Lines L1 to L12 are the search on start positions. The start value $nL + 1$ of line L1 is larger than any score, so the first leaf always sets the best. Line L11 is the cut: the partial score of the first $i$ rows is a lower bound on the score of every leaf below. Lines L13 to L23 are the search on prefixes. Line L21 adds the column $k + 1$ of each window to the counts when the prefix gets the letter $a$, and line L23 undoes it. Both searches test with a strict inequality, so a later leaf replaces the best only when it is strictly better, and the result is the first optimum in the order of the tree.

## Example

Take the five sequences of Rosalind problem BA2D, GGCGTTCAGGCA, AAGAATCAGTCA, CAAGGAGTTCGC, CACGTCAATCAC and CAATAATATTCG, with $L = 3$, so $W = 10$. The prefix tree has $1 + 4 + 16 + 64 = 85$ nodes. BB-MEDIAN visits 45 of them, in this order of events:

| prefix $u$ | bound | best before | action |
|---|---|---|---|
| (root), A, AA | 0, 0, 1 | 16 | go down |
| AAA | 6 | 16 | leaf: best ← 6 |
| AAC | 6 | 6 | cut (not below 6) |
| AAG | 3 | 6 | leaf: best ← 3 |
| AAT, AC | 3, 4 | 3 | cut |
| AG, AT | 2, 2 | 3 | go down; all eight leaves have bound 3 to 6, cut |
| C, CA | 0, 0 | 3 | go down |
| CAA | 2 | 3 | leaf: best ← 2 |
| CAC, CAG, CAT, CC, CG, CT | 4, 3, 5, 5, 2, 5 | 2 | cut |
| G | 1 | 2 | go down; GA, GC, GG cut; GT has bound 1, its leaves 3 to 6 are cut |
| T, TC | 0, 0 | 2 | go down; TCA has bound 2, which is not below 2, so it is cut |
| TA, TG, TT | 4, 5, 2 | 2 | cut |

The result is CAA with $D = 2$. TCA and TTC are also median strings, but the strict test keeps the first one. The position tree on the same input has $1 + 10 + \cdots + 10^5 = 111{,}111$ nodes, and BB-MOTIF visits 166 of them. It returns the 0-based starts (4, 4, 7, 3, 8), the windows TTC, ATC, TTC, GTC and TTC, with score 2.

**Measured pruning on planted motifs.** The test generator plants a motif of length 8 with exactly one change in each of 10 random sequences of length 100. On seeds 0, 1 and 2, BB-MEDIAN visits 12,757, 6,677 and 8,921 of the 87,381 nodes of the prefix tree, and returns the planted motif each time, with $D = 10$. These are measurements on three inputs, not a bound.

## Correctness

Both searches have the same shape. The bound at a node is at most the score of every leaf below it, and at a leaf it equals the score. A subtree is cut only when its bound is not below the best score found, so the cut removes no leaf that is strictly better than the current best. Every leaf that is not cut is reached, so the best of the reached leaves is optimal. For the position tree, the bound is the partial score, and the key fact is that adding a row never lowers it. For the prefix tree, the key fact is that the mismatches of a prefix are kept by each of its extensions, so the smallest mismatch count for a sequence can only grow. The full proof is in proofs/correctness.md.

## Complexity

- **Prefix tree, worst case.** The tree has $\sum_{k=0}^{L} 4^k < \frac{4}{3} 4^L$ nodes. Lines L17, L21 and L23 take $O(nW)$ time per node, so the time is $O(4^L n W)$. This is the cost of the plain enumeration on the tree; without the tree, each of the $4^L$ strings would cost $O(nWL)$.
- **Position tree, worst case.** The tree has $O(W^n)$ nodes, and lines L10 to L12 take $O(L)$ time per child. So the time is $O(L W^n)$.
- **Best case.** If the first leaf has score 0, every later bound is at least 0 and the search cuts every node after the first path. The prefix tree then visits $O(L)$ nodes and takes $O(L n W)$ time; the position tree tests $O(nW)$ children at $O(L)$ time each.
- **Space.** The table $m$ takes $nW$ words, the counts take $4L$ words, and the recursion depth is $L$ or $n$. So the extra space is $O(nW + L)$, and $O(nW)$ more for the windows of the position search.
- **In practice.** The number of nodes depends on the data and on how soon a good leaf is found. The measured counts above are examples, not bounds. A good first best score, for example from a [greedy motif search](/greedy-motif-search/), makes the cuts start earlier.

## Properties

- **Exact.** Both searches return an optimum of the total Hamming distance score for every input.
- **Deterministic.** The tree order is fixed (windows from left to right, letters in the order A, C, G, T) and the test is strict, so the result is the first optimum in that order.
- **The same optimum.** By the equivalence theorem, the score of BB-MOTIF equals the distance of BB-MEDIAN, and the consensus of the returned sites is a median string. On the example, the sites TTC, ATC, TTC, GTC and TTC have the consensus TTC, a median string that BB-MEDIAN does not return because CAA comes first.
- **Only for the Hamming score.** The bounds use the fact that each mismatch stays. They do not hold for an information content score, where a new row can raise or lower the score of a column.

## Variants and improvements

- **A better start.** Set $best$ in line L1 or L13 to the score of a heuristic solution plus one, so that the cuts work from the first node.
- **The maximization form.** Jones and Pevzner maximize $nL - \mathrm{Score}(p)$ and bound a node by the value of the rows placed so far plus $L$ for each row not yet placed. This is the same cut as the partial score above, written for the other form of the score.
- **Best first.** A [best-first branch and bound](/best-first-branch-and-bound/) expands the open node with the smallest bound. It visits fewer nodes, but it needs memory for the open nodes.
- **The $(L, d)$ version.** For the [planted motif problem](/planted-motif-problem/), cut a prefix when some sequence has no window within $d$ mismatches of it: $\min_q m[i][q] > d$ for some $i$. This lists all $(L, d)$ motifs.
- **Both strands.** Add the windows of the reverse complement of each sequence to the table $m$.

## When to use it

Use the prefix tree search when the worst case of $4^L n W$ cell updates is affordable and the exact optimum of the Hamming score is wanted. For $L = 8$ and 20 sequences of 600 letters this is $65{,}536 \times 20 \times 593 \approx 7.8 \times 10^8$ updates, which is practical; each extra letter multiplies it by 4. It is a good reference for the heuristic methods on small data. Do not use the position tree for more than a few short sequences, since $W^n$ grows with each sequence. For long motifs, use [Gibbs sampling](/gibbs-motif-sampler/), [MEME](/meme-algorithm/) or [PROJECTION](/random-projection-motif-finding/); for an information content score, use those or the [greedy search](/greedy-motif-search/).

## Pitfalls

- **Cut with a strict test.** Line L18 must cut when the bound equals the best. A cut only when the bound is strictly larger is still correct, but it visits every tied subtree and can lose most of the gain.
- **Undo exactly.** Line L23 must remove exactly what line L21 added, letter by letter. A copy of the whole table at each node is also correct, but it costs $O(nW)$ memory per level.
- **Window range.** The starts run from 1 to $W = G - L + 1$, not to $G$; a window that runs past the end of a sequence gives wrong counts.
- **Ties.** The motif finding problem often has many optimal answers. A test that compares the output with one fixed answer can fail for a correct search with another tree order.

## Implementations

## History

Branch and bound was introduced for integer programming by Land and Doig in 1960, and it became a standard tool for exact search. In the motif setting, Jones and Pevzner (2004) presented the motif finding problem and the median string problem in Chapter 4 of their textbook, showed that the two have the same optimum under the total Hamming distance, and used them as the main example of branch and bound in bioinformatics: first on the tree of start positions, then on the much smaller tree of candidate strings. Compeau and Pevzner (2015) teach the median string search by plain enumeration of all $k$-mers.

## References
