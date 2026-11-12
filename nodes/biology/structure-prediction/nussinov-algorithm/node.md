---
tag: 6XRW3C
kind: algorithm
slug: nussinov-algorithm
name: Nussinov algorithm
aliases:
- Nussinov folding
- Maximum base pairing
- Nussinov-Jacobson algorithm
area: biology/structure-prediction
level: intro
summary: Interval dynamic program that finds an RNA secondary structure with the largest number of nested base pairs in O(n^3) time and O(n^2) space.
solves: [rna-secondary-structure-prediction]
model: word-ram
complexity:
  vars: {n: the length of the RNA sequence}
  time: {worst: Θ(n^3), average: Θ(n^3), best: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1978
  people: [Ruth Nussinov, George Pieczenik, Jerrold R. Griggs, Daniel J. Kleitman, Ann B. Jacobson]
  note: Nussinov, Pieczenik, Griggs and Kleitman gave the loop matching dynamic program in 1978. Nussinov and Jacobson gave the fast form for RNA folding in 1980.
prereqs: [rna-secondary-structure, interval-dp]
see_also: [zuker-algorithm, mccaskill-algorithm, rna-secondary-structure-prediction, cyk-algorithm, matrix-chain-multiplication, traceback, rna-inverse-folding, pseudoknot]
sources:
  - paper: doi:10.1137/0135006
    title: Ruth Nussinov, George Pieczenik, Jerrold R. Griggs and Daniel J. Kleitman, Algorithms for loop matchings, SIAM Journal on Applied Mathematics 35(1), 1978, pages 68 to 82
    locator: the dynamic program for a maximum matching of nested pairs in a string
  - paper: doi:10.1073/pnas.77.11.6309
    title: Ruth Nussinov and Ann B. Jacobson, Fast algorithm for predicting the secondary structure of single-stranded RNA, PNAS 77(11), 1980, pages 6309 to 6313
    locator: the O(n^3) algorithm for RNA folding with energies per base pair
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 10, Section 10.2, RNA secondary structure prediction (base pair maximisation and the Nussinov folding algorithm), pages 267 to 276
---

The Nussinov algorithm finds an [RNA secondary structure](/rna-secondary-structure/) with the largest number of base pairs. It is an [interval dynamic program](/interval-dp/): the cell $N[i, j]$ holds the largest number of nested pairs in the part $s_i \cdots s_j$ of the sequence, and each cell is the best of "the last base is unpaired" and "the last base pairs with some base $k$". The table has $O(n^2)$ cells and each takes $O(n)$ time, so the algorithm runs in $\Theta(n^3)$ time and $\Theta(n^2)$ space. It is the simplest model of [RNA secondary structure prediction](/rna-secondary-structure-prediction/), and the [Zuker algorithm](/zuker-algorithm/) uses the same interval idea with loop energies.

## In plain words

An RNA molecule is a string of the letters A, C, G and U. The string folds back on itself, and some letters stick together in pairs: A with U, G with C, and G with U. Pairs must nest like brackets, and a pair needs at least three free letters inside it. The task is to choose as many pairs as possible.

Look at the last letter of a stretch. It is free, or it pairs with an earlier letter. If it is free, use the best answer for the stretch without it. If it pairs, the pair cuts the stretch into an inside part and a left part that no other pair can join. The answer is then one plus the best answers of the two parts. Solve the short stretches first and keep their answers in a table.

## The problem

**Input.** A sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$, a set of allowed pairs (here AU, UA, GC, CG, GU and UG), and a hairpin minimum $m \ge 0$ (here $m = 3$).

**Output.** A secondary structure $P$ of $s$ with the largest number $|P|$ of pairs. A secondary structure is a set of pairs $(i, j)$ with $i < j$ such that $(s_i, s_j)$ is allowed, $j - i - 1 \ge m$, no base is in two pairs, and no two pairs cross: there are no pairs $(i, j)$ and $(k, l)$ in $P$ with $i < k < j < l$. Pseudoknots are not allowed. The score is the number of pairs, with no energies and no stacking.

## The algorithm

For $1 \le i \le j \le n$, let $N(i, j)$ be the largest number of pairs of a secondary structure of $s_i \cdots s_j$, and let $N(i, j) = 0$ when $j \le i$. In a structure of $s_i \cdots s_j$, the base $j$ is unpaired, or it pairs with some $k$ with $i \le k \le j - m - 1$. In the second case, a pair with one end in $[i, k - 1]$ and the other in $[k + 1, j - 1]$ would cross $(k, j)$, so the rest of the structure is a structure of $s_i \cdots s_{k-1}$ together with a structure of $s_{k+1} \cdots s_{j-1}$. This gives the recurrence

$$N(i, j) = \max\Big(N(i, j - 1),\ \max_{\substack{i \le k \le j - m - 1 \\ (s_k, s_j) \text{ allowed}}} \big(N(i, k - 1) + 1 + N(k + 1, j - 1)\big)\Big).$$

The right side reads only shorter intervals, so the table is filled by increasing span $d = j - i$.

```pseudo id=main
NUSSINOV(s[1 .. n], m)                     ▷ N[i, j] = 0 when j ≤ i
L1  for d ← 1 to n − 1 do                     ▷ the span j − i
L2      for i ← 1 to n − d do
L3          j ← i + d
L4          N[i, j] ← N[i, j − 1]                 ▷ j is unpaired
L5          for k ← i to j − m − 1 do               ▷ j pairs with k
L6              if (s_k, s_j) is allowed then N[i, j] ← max(N[i, j], N[i, k − 1] + 1 + N[k + 1, j − 1])
L7  P ← empty set, T ← a stack that holds (1, n)
L8  while T is not empty do
L9      pop (i, j) from T; if j − i < 1 then go to L8
L10     if N[i, j] = N[i, j − 1] then push (i, j − 1) on T
L11     else
L12         find k in [i, j − m − 1] with (s_k, s_j) allowed and N[i, j] = N[i, k − 1] + 1 + N[k + 1, j − 1]
L13         add (k, j) to P; push (i, k − 1) and (k + 1, j − 1) on T
L14 return N[1, n], P
```

Lines L1 to L6 fill the table. When line L6 reads $N[i, k - 1]$ and $N[k + 1, j - 1]$, both intervals are shorter than $[i, j]$, so they are already filled. Lines L7 to L13 are the [traceback](/traceback/). They use an explicit stack of intervals instead of recursion, so a long sequence does not overflow the call stack. Line L12 always finds a $k$: if the test of line L10 fails, the maximum of line L6 came from some $k$.

## Example

Fold $s = $ GCAAAGCAAAGC ($n = 12$) with $m = 3$. Some cells of the table:

| cell | the candidates of lines L4 to L6 | value |
|---|---|---|
| $N(2, 6)$ | $N(2, 5) = 0$; $k = 2$ (C with G): $0 + 1 + N(3, 5) = 1$ | 1 |
| $N(7, 11)$ | $N(7, 10) = 0$; $k = 7$ (C with G): $0 + 1 + N(8, 10) = 1$ | 1 |
| $N(2, 11)$ | $N(2, 10) = 1$; $k = 2$: $0 + 1 + N(3, 10) = 1$; $k = 7$: $N(2, 6) + 1 + N(8, 10) = 2$ | 2 |
| $N(1, 12)$ | $N(1, 11) = 2$; $k = 1$ (G with C): $0 + 1 + N(2, 11) = 3$; $k = 6$: $N(1, 5) + 1 + N(7, 11) = 2$ | 3 |

The cell $N(2, 11)$ shows the split: the best choice pairs base 11 with base 7 and leaves the interval $[2, 6]$ to its left, which holds one more pair. The traceback starts at $(1, 12)$. Line L10 fails because $N(1, 11) = 2$, and line L12 finds $k = 1$. In $(2, 11)$ it finds $k = 7$, and in $(2, 6)$ it finds $k = 2$. The other intervals hold no pair. The result is 3 pairs, $(1, 12)$, $(2, 6)$ and $(7, 11)$:

```
GCAAAGCAAAGC
((...)(...))
```

The loop of line L5 runs $\binom{n - m + 1}{3}$ times in total, which is $\binom{10}{3} = 120$ here.

## Correctness

The proof is an induction on the span $j - i$. An interval of span 0 or less has no pair. For a longer interval, each structure falls into exactly one case of the recurrence: $j$ unpaired, or $j$ paired with a unique $k$. In the second case the non-crossing rule splits the rest of the structure into independent structures of $[i, k - 1]$ and $[k + 1, j - 1]$, so its size is at most $N(i, k - 1) + 1 + N(k + 1, j - 1)$ by induction. Conversely, each candidate value of line L6 is the size of a real structure, built from optimal structures of the two parts and the pair $(k, j)$. The traceback keeps the invariant that $|P|$ plus the sum of $N$ over the intervals on the stack equals $N(1, n)$. The full proof is below.

## Complexity

- **Time.** Line L6 runs once for each triple $i \le k \le j - m - 1$, that is $\binom{n - m + 1}{3} = n^3/6 + O(n^2)$ times for a fixed $m$, each in $O(1)$ time. So the time is $\Theta(n^3)$ for every input of length $n$: the loop does not depend on the letters. The traceback visits $O(n)$ intervals and spends $O(n)$ time on each, so it takes $O(n^2)$ time.
- **Space.** The table has $(n + 1)^2$ small integers, $\Theta(n^2)$ words. The stack of the traceback holds $O(n)$ intervals.

These bounds are in the [word RAM](/word-ram/) model. The cubic time is not optimal: Bringmann, Grandoni, Saha and Vassilevska Williams gave a truly subcubic algorithm for this pair counting problem with fast bounded-difference min-plus products. Their algorithm is of theoretical interest; the cubic program is what tools use.

## Properties

- **Exact.** It returns a structure with the largest number of pairs among all secondary structures, for every allowed pair set and every $m \ge 0$.
- **Unambiguous.** Each structure of $[i, j]$ is built in exactly one way by the recurrence: the case is fixed by the state of base $j$, and $k$ is its partner. Replace max by sum and $1$ by a weight, and the same recurrence counts structures or computes a partition function, as in the [McCaskill algorithm](/mccaskill-algorithm/).
- **Ties.** Many structures can have the largest number of pairs. The traceback returns one of them, chosen by the order of the tests of lines L10 and L12.
- **No pseudoknots.** The split at line L6 is valid only because pairs do not cross. With crossing pairs allowed, the largest number of pairs is a [maximum matching](/maximum-matching/) problem in a general graph; see [pseudoknot](/pseudoknot/).

## Variants and improvements

- **The four-case form.** The form in Durbin et al. takes the best of $N(i + 1, j)$, $N(i, j - 1)$, $N(i + 1, j - 1) + \delta(i, j)$ and a split $N(i, k) + N(k + 1, j)$. It gives the same maximum but builds most structures in many ways, so it cannot count structures or sum weights. The form on this page has one derivation per structure.
- **Weights per pair.** Give each pair type a score, for example a GC pair more than an AU pair, and maximize the total. Nussinov and Jacobson used energies per base pair in this way. The recurrence is the same with $1$ replaced by the weight of $(s_k, s_j)$.
- **Stochastic grammar form.** A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) with rules for unpaired bases, pairs and splits gives a probabilistic version. The [CYK algorithm](/cyk-algorithm/) then finds the most probable structure, and the inside algorithm sums over structures.
- **Energy loops.** The [Zuker algorithm](/zuker-algorithm/) replaces the score per pair by loop energies of the [nearest-neighbor model](/nearest-neighbor-model/). It needs more tables but keeps $O(n^3)$ time with a bound on the size of internal loops.
- **Faster in theory.** The four-Russians speed-up gives $O(n^3 / \log n)$ time, and bounded-difference min-plus products give $O(n^{3 - \varepsilon})$ for a fixed $\varepsilon > 0$.

## When to use it

Use the Nussinov algorithm to learn the interval dynamic program of RNA folding, to count or enumerate structures, and as a test case for new folding code. Do not use it to predict real structures: counting pairs ignores the stacking of neighbor pairs and the cost of loops, so it prefers many scattered pairs over a few stable helices. For predictions, use the [Zuker algorithm](/zuker-algorithm/) with the Turner parameters, or the [McCaskill algorithm](/mccaskill-algorithm/) for pair probabilities.

## Pitfalls

- **No hairpin minimum.** With $m = 0$ the algorithm pairs neighbor bases such as G and C in "GC", which is not possible in a real molecule. Use $m = 3$.
- **The wrong bound on $k$.** Line L5 must stop at $j - m - 1$. A bound of $j - 1$ allows hairpins with fewer than $m$ unpaired bases.
- **Empty intervals.** The terms $N(i, k - 1)$ for $k = i$ and $N(k + 1, j - 1)$ for a short hairpin read an empty interval, whose value is 0. In Python, an index of $-1$ reads the last row without an error, so test the bounds or pad the table.
- **Recursion in the traceback.** A recursive traceback has a depth up to $n$, which can pass the default recursion limit of Python for long sequences. Use an explicit stack, as in lines L7 to L13.
- **Counting with the four-case form.** If you change max to sum in the four-case form, each structure is counted many times. Use the unambiguous form.

## Implementations

## History

Ruth Nussinov, George Pieczenik, Jerrold Griggs and Daniel Kleitman published algorithms for loop matchings in 1978: a dynamic program that finds a largest set of nested pairs in a string. In 1980 Ruth Nussinov and Ann Jacobson gave the fast algorithm for the secondary structure of single-stranded RNA, with energies per base pair. The next year Zuker and Stiegler replaced the pair energies by loop energies, and that model is the base of today's folding programs. Durbin, Eddy, Krogh and Mitchison (1998) present the Nussinov algorithm as the first example of RNA folding and as a grammar.

## References
