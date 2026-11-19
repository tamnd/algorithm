---
tag: JJFMC2
kind: algorithm
slug: dynamic-time-warping
name: Dynamic time warping
aliases:
- DTW
area: natural-language-and-speech/speech-recognition
level: core
summary: Align two sequences of feature vectors by dynamic programming over monotone warping paths, minimizing the summed local distances.
model: word-ram
complexity:
  vars: {n: the length of the first sequence, m: the length of the second sequence}
  time: {worst: "Θ(n m)"}
  space: {extra: "Θ(n m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1968
  people: [Taras K. Vintsyuk, Hiroaki Sakoe, Seibi Chiba]
  note: Vintsyuk matched spoken words to templates by dynamic programming in 1968. Sakoe and Chiba 1978 gave the symmetric and asymmetric step patterns, the normalization and the band constraint that most later work uses.
prereqs: [dag-dynamic-programming]
see_also: [sakoe-chiba-band, edit-distance, needleman-wunsch, forced-alignment, frechet-distance, longest-common-subsequence, cross-correlation, mel-frequency-cepstral-coefficients]
sources:
  - paper: doi:10.1109/TASSP.1978.1163055
    title: Hiroaki Sakoe and Seibi Chiba, Dynamic programming algorithm optimization for spoken word recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 26(1), 1978, pages 43 to 49
    locator: the symmetric and asymmetric forms of the recurrence, the normalization and the adjustment window
  - paper: doi:10.1007/BF01074755
    title: T. K. Vintsyuk, Speech discrimination by dynamic programming, Cybernetics 4(1), 1968, pages 52 to 57 (Kibernetika 4(1), pages 81 to 88, in Russian)
    locator: the dynamic programming alignment of an utterance with word templates
  - paper: doi:10.1109/TASSP.1975.1162641
    title: Fumitada Itakura, Minimum prediction residual principle applied to speech recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 23(1), 1975, pages 67 to 72
    locator: the slope constraint of the warping path
  - book: isbn:9780130151575
    title: Lawrence Rabiner and Biing-Hwang Juang, Fundamentals of Speech Recognition, Prentice Hall, 1993
    locator: Chapter 4 (pattern comparison techniques)
---

Dynamic time warping (DTW) compares two sequences that follow the same shape at different speeds, for example two recordings of one word, two gait signals or two price curves. It finds a monotone alignment of the positions of the two sequences, a warping path, that makes the sum of the local distances between the aligned elements as small as possible. A dynamic program over an $n \times m$ table finds this path in $\Theta(n m)$ time. The least cost is often used as a distance, but it is not a metric.

## In plain words

Two people say the same word, but one says it slowly and the other fast. A frame by frame comparison fails, because frame 10 of the slow one matches frame 6 of the fast one. DTW lets one sequence wait while the other moves on. Each element of one sequence pairs with one or more elements of the other, the pairs go forward in time in both sequences, and the first and the last elements pair with each other.

Among all such pairings, DTW finds the one with the smallest total difference. It fills a table: the entry for a pair of positions holds the best total for the two beginnings up to those positions. Each entry needs only three neighbors that are already known. The last entry is the answer, and following the choices back from it gives the pairing.

## The problem

The input is two sequences $x = x_1 \ldots x_n$ and $y = y_1 \ldots y_m$ with $n, m \ge 1$, and a local distance $d(a, b) \ge 0$, for example $|a - b|$ for numbers or the squared Euclidean distance for feature vectors such as [MFCC](/mel-frequency-cepstral-coefficients/) frames. Write $c(i, j) = d(x_i, y_j)$.

A warping path is a sequence of cells $p_1 = (1, 1), p_2, \ldots, p_L = (n, m)$ in which each step $p_\ell - p_{\ell - 1}$ is $(1, 1)$, $(1, 0)$ or $(0, 1)$. So the path is monotone and continuous, and it pairs the two first and the two last elements. Its length is between $\max(n, m)$ and $n + m - 1$.

A step pattern gives a weight $w_D$, $w_V$ or $w_H$ to the diagonal step $(1, 1)$, the vertical step $(1, 0)$ and the horizontal step $(0, 1)$. The cost of a path is $\sum_\ell w(p_\ell - p_{\ell-1})\, c(p_\ell)$, where the first cell $(1, 1)$ counts as entered by a diagonal step from a sentinel cell $(0, 0)$. The code has three patterns:

| pattern | $w_D$ | $w_V$ | $w_H$ | sum of the weights on every path |
|---|---|---|---|---|
| symmetric1 | 1 | 1 | 1 | depends on the path |
| symmetric2 | 2 | 1 | 1 | $n + m$ |
| asymmetric | 1 | 1 | 0 | $n$ |

symmetric2 weights a step by $\Delta i + \Delta j$ and asymmetric by $\Delta i$, as in Sakoe and Chiba 1978. For these two patterns the sum of the weights is the same on every path, so dividing the cost by it gives a normalized distance that does not favor short paths. The task is to find a path of least cost and its cost.

The problem is close to the [edit distance](/edit-distance/) and to [Needleman-Wunsch](/needleman-wunsch/) alignment. The difference is that DTW has no gaps: every element is paired, and an element that is "skipped" in an edit alignment is instead paired again with a neighbor.

## The algorithm

```pseudo id=main
DTW(x, y, d, w_D, w_V, w_H)
L1  D[0][0] ← 0,  D[i][0] ← ∞ and D[0][j] ← ∞ for i, j ≥ 1
L2  for i ← 1 to n do
L3      for j ← 1 to m do
L4          c ← d(x_i, y_j)
L5          best ← the least of D[i-1][j-1] + w_D c,  D[i-1][j] + w_V c,  D[i][j-1] + w_H c    ▷ a tie takes the first of these
L6          D[i][j] ← best,  back[i][j] ← the cell that gave best
L7  path ← [(n, m)]
L8  while the last cell of path is not (1, 1) do append back[last cell] to path
L9  return D[n][m] and the reversed path
```

The table $D$ has a sentinel row and column. $D[0][0] = 0$ lets the cell $(1, 1)$ use the diagonal rule, and the other sentinel cells are $\infty$, so no path leaves the table. The rows are filled in order, so the three cells that line L5 reads are already final. The cost can be normalized afterwards: divide by $n + m$ for symmetric2 and by $n$ for asymmetric.

## Example

Take $x = (1, 3, 4, 9, 8)$, $y = (1, 4, 9, 8)$, $d(a, b) = |a - b|$ and the pattern symmetric1. The table $D$, without the sentinels, is:

| | $y_1 = 1$ | $y_2 = 4$ | $y_3 = 9$ | $y_4 = 8$ |
|---|---|---|---|---|
| $x_1 = 1$ | 0 | 3 | 11 | 18 |
| $x_2 = 3$ | 2 | 1 | 7 | 12 |
| $x_3 = 4$ | 5 | 1 | 6 | 10 |
| $x_4 = 9$ | 13 | 6 | 1 | 2 |
| $x_5 = 8$ | 20 | 10 | 2 | 1 |

For example, $D[2][2] = \min(D[1][1], D[1][2], D[2][1]) + |3 - 4| = \min(0, 3, 2) + 1 = 1$. The cost is $D[5][4] = 1$, and the traceback gives the path $(1, 1), (2, 2), (3, 2), (4, 3), (5, 4)$. It pairs both 3 and 4 of $x$ with the 4 of $y$, so the extra element of $x$ costs only $|3 - 4| = 1$.

With symmetric2 the same path costs $2$, because the diagonal step into $(2, 2)$ has weight 2, and the normalized distance is $2 / 9$. With asymmetric the normalized distance is $1/5$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let $V(i, j)$ be the least cost of a path from the sentinel to $(i, j)$. The last step of such a path enters $(i, j)$ from $(i-1, j-1)$, $(i-1, j)$ or $(i, j-1)$, and the part before it is a path to that cell. The cost is additive along the path, so

$$V(i, j) = \min\big( V(i-1, j-1) + w_D c(i, j),\ V(i-1, j) + w_V c(i, j),\ V(i, j-1) + w_H c(i, j) \big).$$

An induction over the cells in row-major order shows that line L6 sets $D[i][j] = V(i, j)$. The back pointers give, for each cell, a predecessor that attains the minimum, so the traceback builds a path of cost $V(n, m)$. Each pointer decreases $i + j$, and the only cell whose pointer is the sentinel is $(1, 1)$, so the traceback stops there. The weights of symmetric2 and asymmetric sum to $n + m$ and $n$ on every path, because they are $\Delta i + \Delta j$ and $\Delta i$, and the steps from $(0, 0)$ to $(n, m)$ add up to $(n, m)$.

## Complexity

The table has $n m$ cells, and each takes one call of $d$ and three comparisons, so the time is $\Theta(n m)$ calls of $d$ and operations. For vectors of dimension $q$, a call of $d$ costs $\Theta(q)$. The table and the back pointers take $\Theta(n m)$ space. If only the cost is needed, two rows are enough, which takes $\Theta(\min(n, m))$ space when the shorter sequence indexes the columns. The path in linear space needs a divide and conquer method as in Hirschberg's algorithm for edit distance.

The number of warping paths from $(1, 1)$ to $(n, m)$ is the Delannoy number $\sum_k \binom{n-1}{k} \binom{m-1}{k} 2^k$, which is 1, 3, 13, 63, 321 and 1683 for $n = m = 1, \ldots, 6$. So the brute force search is exponential, and the dynamic program is the reason DTW is practical. The test test_path_counts_are_delannoy_numbers checks these counts.

## Properties

- **Not a metric.** The DTW cost is symmetric for symmetric patterns and is 0 for equal sequences, but it fails the [triangle inequality](/triangle-inequality/). With $a = (0)$, $b = (2)$ and $c = (2, 2)$, the costs are $\mathrm{DTW}(a, b) = 2$, $\mathrm{DTW}(b, c) = 0$ and $\mathrm{DTW}(a, c) = 4 > 2 + 0$. It also gives 0 to different sequences: $(1, 2, 2, 3)$ and $(1, 2, 3)$ have cost 0. So the indexes of a [metric space](/metric-space/) do not apply directly.
- **Asymmetric patterns.** With the asymmetric pattern the cost depends on the order of the arguments: $x = (0, 5)$ against $y = (0)$ costs 5, but $y$ against $x$ costs 0, because the horizontal step has weight 0.
- **Invariant to repeats.** Repeating an element, as in a slowed copy of a signal, does not change the cost against the original under symmetric1. The test test_identity_and_time_shift checks a slowed copy.
- **Exact.** The cost is the least over all warping paths. A band or a slope limit, as in the [Sakoe-Chiba band](/sakoe-chiba-band/), can miss the optimum.
- **A fixed tie rule.** The code prefers the diagonal step, then the vertical step, then the horizontal step.

## Variants and improvements

- **Global constraints.** The [Sakoe-Chiba band](/sakoe-chiba-band/) allows only the cells with $|i - j| \le r$, and the Itakura parallelogram (Itakura 1975) limits the slope of the path. Both cut the time to the number of allowed cells and stop the path from pairing one element with a long run of the other.
- **Slope constraints and other step patterns.** Sakoe and Chiba 1978 give patterns that force a diagonal step after a few horizontal or vertical ones. In their word recognition tests the symmetric form gave fewer errors than the asymmetric form. This is a measurement on their data, not a general rule.
- **Open ends.** Free the start or the end of one sequence to match a short pattern inside a long one, as in word spotting.
- **Connected words.** Vintsyuk's method and the later one-pass algorithms run DTW against a network of word templates to recognize word sequences. This is the template version of the Viterbi search in [forced alignment](/forced-alignment/) and HMM decoding.
- **Lower bounds for search.** For nearest neighbor search over many series, cheap lower bounds on the banded cost skip most of the full computations.
- **Related alignments.** The [Fréchet distance](/frechet-distance/) takes the maximum of the local distances in place of the sum, and the [longest common subsequence](/longest-common-subsequence/) and [Needleman-Wunsch](/needleman-wunsch/) allow gaps.

## When to use it

Use DTW for sequences that differ by local changes of speed, when no model of the data exists: template matching of isolated words with few templates, gesture and signature matching, and nearest neighbor classification of time series. If the timing differs only by a constant shift, [cross-correlation](/cross-correlation/) is simpler and faster. With a lot of training data, HMMs replaced DTW in speech recognition, because a statistical model of each word generalizes better than a set of templates.

## Pitfalls

- **Unnormalized costs.** Under symmetric1 a longer path has more terms, so costs of pairs of different lengths do not compare. Use symmetric2 or asymmetric and divide by the sum of the weights.
- **Pathological warping.** Without a band, one element can pair with a long run of the other, and a sequence can match a very different one at a low cost. Use a band or a slope limit.
- **Scale and offset.** The local distance compares raw values, so two series with different offsets or scales get a large cost. Normalize each series first if only the shape matters.
- **Treating the cost as a metric.** The triangle inequality fails, so pruning rules that assume it can drop true nearest neighbors.
- **Empty sequences.** A warping path needs at least one element in each sequence. The code raises an error for an empty input.

## Implementations

## History

Vintsyuk 1968 aligned speech to word templates by dynamic programming. The 1978 paper of Sakoe and Chiba compared the symmetric and asymmetric forms, used slope constraints and the adjustment window that is now called the Sakoe-Chiba band, and measured their effect on word recognition. Itakura 1975 used a slope constrained alignment with a distance from linear prediction. DTW template matching was the main method of isolated word recognition until HMMs took over in the 1980s (Rabiner and Juang 1993). The method later became a standard tool for time series outside speech.

## References
