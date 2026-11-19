---
tag: TXM3A8
kind: algorithm
slug: gale-church-alignment
name: Gale-Church alignment
aliases:
- length-based sentence alignment
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Align sentences by dynamic programming with a cost from a Gaussian model of the ratio of character lengths of matched sentences.
solves: [sentence-alignment]
model: word-ram
complexity:
  vars: {I: the number of sentences of the first text, J: the number of sentences of the second text}
  time: {worst: "Θ(I J)"}
  space: {extra: "Θ(I J)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1991
  people: [William A. Gale, Kenneth W. Church]
  note: Gale and Church presented the program at ACL 1991 and published the full version with the C code in Computational Linguistics in 1993. Brown, Lai and Mercer gave a similar length-based method at the same meeting, with lengths in words.
prereqs: [sentence-alignment, parallel-corpus, dag-dynamic-programming]
see_also: [edit-distance, needleman-wunsch, dynamic-time-warping, traceback, banded-alignment, gaussian-q-function, word-alignment, prefix-sums]
sources:
  - paper: "William A. Gale and Kenneth W. Church, A program for aligning sentences in bilingual corpora, Computational Linguistics 19(1), 1993, pages 75 to 102"
    title: Gale and Church 1993
    locator: "Section 4 (the distance measure and Table 5 of the match priors), Section 5 (the dynamic program), Section 6 (the evaluation), and the C program in the appendix"
  - paper: "William A. Gale and Kenneth W. Church, A program for aligning sentences in bilingual corpora, 29th Annual Meeting of the ACL, 1991, ACL Anthology P91-1023"
    title: Gale and Church 1991
    locator: the conference version
  - paper: doi:10.3115/981344.981366
    title: Peter F. Brown, Jennifer C. Lai and Robert L. Mercer, Aligning sentences in parallel corpora, 29th Annual Meeting of the ACL, 1991, pages 169 to 176
    locator: the length-based alignment with lengths in words
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 2 (Words, Sentences, Corpora)"
---

Gale-Church alignment solves [sentence alignment](/sentence-alignment/) for a [parallel corpus](/parallel-corpus/) with sentence lengths in characters only. It is a [dynamic program](/dag-dynamic-programming/) over the pairs (sentences used in text 1, sentences used in text 2). Each step adds a *bead* of type 1-1, 1-0, 0-1, 2-1, 1-2 or 2-2, and the cost of a bead is $-\ln$ of its prior times the probability of its length difference under a Gaussian model. The result is the cheapest monotone alignment in $\Theta(I J)$ time. Gale and Church (1993) found that it aligns about 96% of the sentences of their trilingual test set correctly. That figure is a measurement, not a guarantee.

## In plain words

A text and its translation have about the same number of sentences in the same order. Some sentences are split in two, some are merged, and a few are missing on one side. Long sentences tend to have long translations, and short ones short.

The method uses only the length of each sentence in characters. For a candidate pairing it asks two questions: how common is this kind of pairing (one with one, two with one, one with nothing), and how well do the lengths agree? Each answer gives a penalty. The method then walks through both texts together, as in edit distance, and keeps for each position the cheapest way to reach it. At the end it follows the stored choices back to get the pairs.

It needs no dictionary and no knowledge of the languages, and it is fast.

## The problem

The input is the lengths $x_1, \ldots, x_I$ of the sentences of text 1 and $y_1, \ldots, y_J$ of text 2, in characters. A *bead* of type $p$-$q$ joins $p$ consecutive sentences of text 1 with $q$ consecutive sentences of text 2. An alignment is a sequence of beads that covers both texts in order, each sentence in exactly one bead. The types are $T = \{1\text{-}1, 1\text{-}0, 0\text{-}1, 2\text{-}1, 1\text{-}2, 2\text{-}2\}$, as in Gale and Church (1993). The task is to find an alignment of the least total cost, where the cost of a bead with $l_1$ and $l_2$ characters is

$$\mathrm{cost}(l_1, l_2, p, q) = -\ln \mathrm{Prior}(p\text{-}q) - \ln P(\delta \mid \text{match}), \qquad P(\delta \mid \text{match}) = 2\bigl(1 - \Phi(|\delta|)\bigr).$$

Here $\Phi$ is the standard normal distribution function, so $2(1 - \Phi(|\delta|))$ is the two-sided tail of the [Q function](/gaussian-q-function/). The model behind it says that each character of text 1 gives a random number of characters of text 2, independently, with mean $c$ and variance $s^2$. Then $l_2 - c l_1$ is about normal with variance $s^2 l_1$. Section 4 of the paper writes

$$\delta = \frac{l_2 - c\, l_1}{\sqrt{l_1 s^2}}.$$

The C program in the appendix uses the mean of the two lengths in place of $l_1$: $\bar l = (l_1 + l_2 / c) / 2$ and $\delta = (c\, l_1 - l_2) / \sqrt{s^2 \bar l}$. The sign does not matter, because only $|\delta|$ is used. The program form is symmetric in the two texts and is defined for a 0-1 bead, where $l_1 = 0$ and the text form divides by zero. This page and its code use the program form.

The constants are those of the paper. The value $c = 1$ (they measured 1.1 for German to English and 1.06 for French to English, in characters) and $s^2 = 6.8$ (they measured 7.3 and 5.6). The priors come from 1312 hand-aligned beads (Table 5): 1-1 0.89, "1-0 or 0-1" 0.0099, "2-1 or 1-2" 0.089, 2-2 0.011. The program uses the value of each two-way category for both directions, so the six weights sum to 1.0988, not to 1. The constants and the priors are estimates from their data, so the cost is a heuristic model, not a property of translation.

## The algorithm

$D(i, j)$ is the least cost of an alignment of the first $i$ sentences of text 1 with the first $j$ sentences of text 2, and $B(i, j)$ is the type of its last bead. Every cell starts at $+\infty$.

```pseudo id=main
GALE-CHURCH(x_1 .. x_I, y_1 .. y_J)            ▷ costs in nats
L1  D(0, 0) ← 0
L2  for i ← 0 to I do
L3      for j ← 0 to J do
L4          if (i, j) = (0, 0) then continue
L5          for each type (p, q) in 1-1, 1-0, 0-1, 2-1, 1-2, 2-2 with p ≤ i and q ≤ j do
L6              d ← D(i - p, j - q) + COST(x_{i-p+1} + .. + x_i, y_{j-q+1} + .. + y_j, p, q)
L7              if d < D(i, j) then D(i, j) ← d; B(i, j) ← (p, q)
L8  (i, j) ← (I, J)
L9  while (i, j) ≠ (0, 0) do
L10     (p, q) ← B(i, j); output the bead (i - p + 1 .. i, j - q + 1 .. j); (i, j) ← (i - p, j - q)
L11 return the beads in reverse order and D(I, J)

COST(l_1, l_2, p, q)
L12 l̄ ← (l_1 + l_2 / c) / 2
L13 δ ← (l_2 - c l_1) / sqrt(s² l̄)
L14 return -ln Prior(p, q) - ln(2 (1 - Φ(|δ|)))
```

Lines L2 and L3 visit the cells in row-major order. Each type at line L5 points to a cell that comes earlier in this order, so its value is final when line L6 reads it. Line L6 adds the cost of the last bead to the best cost of the rest, as in [edit distance](/edit-distance/) with three more kinds of step. Line L7 keeps the minimum and its type. Lines L8 to L10 are the [traceback](/traceback/). The lengths of line L6 come from [prefix sums](/prefix-sums/), so each candidate costs $O(1)$.

**Tie rule.** Line L7 replaces only on a strict decrease, so among the types that reach the minimum at a cell it keeps the first in the order of line L5.

**Paragraphs first.** Gale and Church run the same program twice. It first aligns paragraphs (with the paragraph lengths), and then aligns the sentences inside each pair of aligned paragraphs. This keeps $I$ and $J$ small and keeps an error from spreading beyond one paragraph.

**Far tails.** For $|\delta|$ above about 38, $\Phi$ rounds to 1 in double precision and $\ln 0$ appears. The implementation switches to the asymptotic form $\ln(2(1 - \Phi(x))) \approx \tfrac12 \ln(2/\pi) - x^2/2 - \ln x$ for $x \ge 30$, so every bead has a finite cost. The C program returns a fixed large cost instead.

## Example

Text 1 has 5 sentences of 62, 31, 44, 18 and 70 characters, and text 2 has 4 sentences of 66, 80, 21 and 72 characters. With $c = 1$ and $s^2 = 6.8$, the table gives $D(i, j)$ and the type stored in $B(i, j)$, rounded to two decimals.

| $i$ \ $j$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 0 | 16.08 (0-1) | 34.30 (0-1) | 43.26 (0-1) | 60.26 (0-1) |
| 1 | 15.46 (1-0) | 0.28 (1-1) | 8.87 (1-2) | 17.83 (0-1) | 34.83 (0-1) |
| 2 | 26.05 (1-0) | 3.82 (2-1) | 4.85 (1-1) | 9.66 (1-2) | 17.26 (1-2) |
| 3 | 38.71 (1-0) | 16.48 (1-0) | 2.89 (2-1) | 6.04 (2-2) | 11.03 (1-2) |
| 4 | 47.17 (1-0) | 24.94 (1-0) | 7.13 (2-1) | 3.24 (1-1) | 11.09 (2-2) |
| 5 | 63.86 (1-0) | 41.63 (1-0) | 19.20 (2-1) | 12.48 (1-1) | 3.43 (1-1) |

The traceback from $(5, 4)$ reads 1-1, 1-1, 2-1, 1-1. So the alignment is (62 | 66), (31 + 44 | 80), (18 | 21), (70 | 72), with bead costs 0.2815, 2.6084, 0.3466 and 0.1918, and the total is 3.4283. For the 2-1 bead, $l_1 = 75$, $l_2 = 80$, $\bar l = 77.5$ and $\delta = 5 / \sqrt{6.8 \cdot 77.5} = 0.218$. Most of its cost is the prior: $-\ln 0.089 = 2.42$, against $-\ln 0.89 = 0.12$ for a 1-1 bead. A bead of one sentence with nothing (1-0 or 0-1) costs at least $-\ln 0.0099 = 4.62$, plus a large length term, which is why the first row and the first column are so expensive.

A second case shows a merge. With lengths 40, 25, 30, 62, 12 against 43, 58, 65, the last sentence of 12 characters does not become a 1-0 bead. It joins 62 in a 2-1 bead (74 against 65), which is cheaper.

## Correctness

The claim is that the output is a monotone alignment of the least total cost with the six types. A path from cell $(0, 0)$ to $(I, J)$ whose steps are bead types is the same thing as such an alignment. The invariant is that when cell $(i, j)$ has been visited, $D(i, j)$ is the least cost of a path to it: the last step of the best path is some type $(p, q)$, and the rest is a best path to $(i - p, j - q)$, which is the [principle of optimality](/principle-of-optimality/). The proof is an induction over the cells in row-major order, and the traceback then rebuilds a path of cost $D(I, J)$. The full proof is in the proofs file.

The claim is exact for the cost model. Whether the cheapest alignment is the right one is a question about the model, and the answer is only measured.

## Complexity

In the [word RAM](/word-ram/) model, with the lengths and the costs as machine numbers, there are $(I + 1)(J + 1)$ cells and each looks at most at 6 types. With prefix sums, each candidate of line L6 costs $O(1)$, including one call of erfc. So the time is $\Theta(I J)$ in every case. The table $D$ and the back pointers $B$ take $\Theta(I J)$ space. Without the back pointers, the last three rows of $D$ (the 2-1 and 2-2 types reach two rows back) give the cost in $\Theta(J)$ space, but not the alignment.

In practice the cost is small because the paragraphs are aligned first, so $I$ and $J$ are the numbers of sentences in one paragraph. A band around the diagonal, as in [banded alignment](/banded-alignment/), also cuts the work to $O((I + J) w)$ for a band of width $w$, but it is no longer exact if the best path leaves the band.

## Properties

- **Exact for its cost.** It finds a cheapest alignment under the stated cost. It is not exact for the true alignment.
- **Language independent.** It uses no words, only lengths, so it works for any pair of languages whose lengths correlate. The constants $c$ and $s^2$ depend weakly on the pair.
- **Monotone.** It cannot find crossing beads. A sentence moved to another place in the translation becomes a 1-0 and a 0-1 bead, or a wrong pair.
- **Local errors.** An error tends to stay in a few beads, because the path rejoins the right diagonal after a short run.
- **A confidence for free.** The cost of each bead is a score. Gale and Church kept the best 80% of the beads by this score, and the error rate on the rest fell from 4% to 0.7% (a measurement).

## Variants and improvements

- **Lengths in words.** Brown, Lai and Mercer (1991) used the same kind of dynamic program with sentence lengths in words, on the Canadian Hansards. Gale and Church argue that lengths in characters work better on their data.
- **Lexical cues.** Later methods add a score from a bilingual lexicon or from cognates (words with the same spelling), which helps where the lengths do not decide. These are no longer purely length-based.
- **Other bead sets.** Some implementations add 3-1 and 1-3 beads. The dynamic program changes only in line L5.
- **Linear space.** The divide and conquer method of [Hirschberg](/hirschberg-algorithm/) gives the alignment in $O(J)$ space with about twice the time, as for any dynamic program of this shape.

## When to use it

Use Gale-Church as the first step to build a [parallel corpus](/parallel-corpus/) from documents that are already paired, with paragraphs that mostly correspond and few omissions. It is fast and needs no resources, so it scales to corpora like the Canadian Hansards. When large parts are missing or reordered, or when the two languages have very different sentence lengths, use a method with lexical anchors. Before [word alignment](/word-alignment/), filter out the beads with the highest cost.

## Pitfalls

- **The text form of $\delta$.** With $\sqrt{l_1 s^2}$ at line L13, a 0-1 bead has $l_1 = 0$ and the cost is undefined. Use the mean length $\bar l$ of line L12, as the C program does.
- **$\ln 0$ at line L14.** For a large $|\delta|$, $1 - \Phi(|\delta|)$ rounds to 0 and the cost becomes $+\infty$. Then all candidates of a cell can tie at $+\infty$ and the traceback can break. Use an asymptotic form or a clamp.
- **The order of the loops.** Line L6 reads $D(i - p, j - q)$. If the loops run in an order in which that cell is not final, the result is wrong. Row-major order works for all six types.
- **No paragraph step.** On a long document with no paragraph alignment, the table has $I J$ cells and one omission early on can shift many beads. Align paragraphs first, or use anchors.
- **Normalized priors.** Dividing the six weights by 1.0988 adds $\ln 1.0988 = 0.094$ to the cost of every bead at line L14. An alignment with more beads then pays more, so the result can differ from the paper's program. State which form you use.

## Implementations

## History

William Gale and Kenneth Church presented the program at the ACL meeting of 1991, and the journal version with the C code appeared in Computational Linguistics in 1993. At the same meeting, Peter Brown, Jennifer Lai and Robert Mercer of IBM gave a length-based method that counted words, which they used on the Canadian Hansards. Gale and Church tested theirs on economic reports of the Union Bank of Switzerland in English, French and German. All but 4% of the sentences were aligned correctly, and they also aligned a sample of about 90 million words of the Hansards. The method became the standard first step to build sentence-aligned corpora for statistical machine translation.

## References
