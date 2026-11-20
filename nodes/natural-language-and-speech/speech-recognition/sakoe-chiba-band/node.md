---
tag: HMGHCC
kind: technique
slug: sakoe-chiba-band
name: Sakoe-Chiba band
aliases:
- Sakoe-Chiba constraint
area: natural-language-and-speech/speech-recognition
level: core
summary: Restrict the warping path of DTW to the cells within a fixed distance r of the diagonal. This saves time and stops degenerate alignments, but it can miss the optimum.
prereqs: [dynamic-time-warping]
see_also: [banded-alignment, edit-distance, global-alignment, hirschberg-algorithm, forced-alignment, time-synchronous-beam-search, nearest-neighbor-search, template-matching]
sources:
  - paper: doi:10.1109/TASSP.1978.1163055
    title: Hiroaki Sakoe and Seibi Chiba, Dynamic programming algorithm optimization for spoken word recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 26(1), 1978, pages 43 to 49
    locator: the adjustment window condition on the warping path and the slope constraint
  - paper: doi:10.1109/TASSP.1975.1162641
    title: Fumitada Itakura, Minimum prediction residual principle applied to speech recognition, IEEE Transactions on Acoustics, Speech, and Signal Processing 23(1), 1975, pages 67 to 72
    locator: the local slope constraint of the warping path, which gives the parallelogram
  - book: isbn:9780130151575
    title: Lawrence Rabiner and Biing-Hwang Juang, Fundamentals of Speech Recognition, Prentice Hall, 1993
    locator: Chapter 4 (pattern comparison techniques, time alignment and normalization)
---

The Sakoe-Chiba band is a global constraint on [dynamic time warping](/dynamic-time-warping/): a warping path may use only the cells $(i, j)$ with $|i - j| \le r$, for a fixed band width $r$. The dynamic program then fills about $n (2r + 1)$ cells in place of $n m$, and no element of one sequence can pair with a long run of the other. The price is that the best path inside the band can cost more than the best path overall. The Itakura parallelogram is a related constraint (Itakura 1975) that limits the slope of the path and so restricts it to a parallelogram around the diagonal.

## In plain words

DTW lets one sequence wait while the other moves on, and it fills a table with one entry for each pair of positions. Most of that table is far from the diagonal, where one sequence is far ahead of the other. Such pairings are rarely right: two recordings of one word do not drift apart by half a second.

The band keeps only a strip of the table along the diagonal, and treats everything outside the strip as forbidden. The program fills only the strip, so it runs much faster on long sequences. It also cannot pick a strange pairing far from the diagonal. But if the true best pairing leaves the strip, the band gives a worse answer, so the width of the strip is a trade-off.

## When it applies

The technique applies to a dynamic program over a two-dimensional table in which a path moves from the top left corner to the bottom right corner with monotone steps, and in which good paths stay near the diagonal. DTW is the first case. The same idea works for [edit distance](/edit-distance/) and for [global alignment](/global-alignment/), where it is called [banded alignment](/banded-alignment/).

It fits when the two sequences have about the same speed, so the offset $i - j$ of a good path stays small, and when $|n - m| \le r$. If the lengths differ a lot, use a band around the line from $(1, 1)$ to $(n, m)$ in place of the main diagonal, or rescale one sequence first.

## The template

```pseudo id=main
BANDED-DTW(x, y, d, BAND)            ▷ BAND(i) is the hole: the range of columns j allowed in row i
L1  if the cell (n, m) is not in BAND(n), or (1, 1) is not in BAND(1), then report "no path in the band"
L2  D[0][0] ← 0,  and every cell outside the band counts as ∞
L3  for i ← 1 to n do
L4      for j in BAND(i), clipped to 1 .. m do
L5          D[i][j] ← d(x_i, y_j) + min(D[i-1][j-1], D[i-1][j], D[i][j-1])
L6  return D[n][m], and the path from the back pointers
```

The hole is BAND. The Sakoe-Chiba band of width $r$ is $\mathrm{BAND}(i) = \{ i - r, \ldots, i + r \}$. With this band, a warping path exists if and only if $|n - m| \le r$: the last cell must satisfy $|n - m| \le r$, and if it does, the path that goes along the diagonal and then straight to $(n, m)$ stays in the band. Line L1 checks this. Line L5 is the recurrence of the symmetric1 pattern on the dynamic time warping page, and the other step patterns work the same way.

Walk through the template with $x = (0, 0, 0, 5)$, $y = (0, 5, 5, 5)$ and $d(a, b) = |a - b|$.

- Without a band, the best path is $(1, 1), (2, 1), (3, 1), (4, 2), (4, 3), (4, 4)$. It pairs the three zeros of $x$ with the zero of $y$ and the five of $x$ with the three fives of $y$, and it costs 0. It uses the cells $(3, 1)$ and $(4, 2)$, which have $|i - j| = 2$.
- With $r = 2$ that path is in the band, and the cost is 0.
- With $r = 1$ it is not. The best path in the band is $(1, 1), (2, 1), (3, 2), (4, 3), (4, 4)$, which pairs the third zero of $x$ with a five and costs 5.
- With $r = 0$ only the diagonal is left, and the cost is $0 + 5 + 5 + 0 = 10$.

So the band missed the optimum for $r \le 1$. The test test_band_misses_the_optimum checks these values.

**Cost.** Row $i$ has at most $2r + 1$ cells, so the template fills at most $n (2r + 1)$ cells, and exactly $n (2r + 1) - r (r + 1)$ when $n = m > r$. The time and the memory are $O(n r)$ for $r \ge 1$, against $\Theta(n m)$ without the band. The code stores only the cells of the band.

**What the band guarantees.** The banded cost is the least cost over the warping paths inside the band (a theorem, from the same induction as for DTW, applied to the cells of the band). It is at least the unconstrained cost, it does not increase as $r$ grows, and it equals the unconstrained cost when $r \ge \max(n, m) - 1$. The tests check all three. The banded cost is exact only if some optimal path stays in the band, and the band has no way to check this.

## Classic examples

- **Isolated word recognition.** Sakoe and Chiba 1978 compared spoken words with stored templates by [dynamic time warping](/dynamic-time-warping/) under an adjustment window $|i - j| \le r$, together with a slope constraint. The window cut the cost of each comparison and removed alignments that were not plausible for speech.
- **Banded alignment of strings.** For [edit distance](/edit-distance/) and [global alignment](/global-alignment/) of similar strings, [banded alignment](/banded-alignment/) fills only the diagonals near the main one. For unit costs, the band can be doubled until its width exceeds the cost found, which makes the result exact.
- **Nearest neighbor search over time series.** A [nearest neighbor search](/nearest-neighbor-search/) that compares a query with many stored series uses a band of a few percent of the length. The band cuts the cost of each comparison, and its width becomes a parameter of the classifier, chosen on held-out data like any other.
- **Alignment with a known transcript.** The limits $lo_t$ and $hi_t$ of [forced alignment](/forced-alignment/) are a band in the frame and state table, but there they are exact: they only drop cells that no complete path can use.

## Variations

- **Itakura parallelogram.** Itakura 1975 limited the local slope of the path, so that each sequence advances at most twice as fast as the other. Together with the fixed ends, this keeps the path in a parallelogram with corners $(1, 1)$ and $(n, m)$ and sides of slope $1/2$ and $2$, so a path exists only if $m/2 \le n \le 2m$, roughly. The parallelogram is narrow near the ends and wide in the middle, while the band has the same width everywhere.
- **Slope constraints.** Sakoe and Chiba 1978 also gave step patterns that allow at most a few horizontal or vertical steps in a row. A slope constraint acts on each step, while a band acts on the position.
- **A band around the scaled diagonal.** For sequences of different lengths, allow the cells with $|j - i m / n| \le r$, so the band follows the line from $(1, 1)$ to $(n, m)$.
- **Data-dependent bands.** Compute the path at a coarse resolution, project it to the fine resolution, and fill only a band around it. This is fast, but it is a heuristic and not exact.
- **Beam pruning.** A [time-synchronous beam search](/time-synchronous-beam-search/) keeps the cells whose score is close to the best one in each column. The beam adapts to the data, but like the band it can lose the best path.

## Pitfalls

- **A band that is too narrow.** The banded cost is only an upper bound on the true DTW cost. If the sequences have a large time offset, every path in the band is poor. The band width is a heuristic, to be set on development data, often as a percentage of the length.
- **Different lengths.** With $|n - m| > r$ there is no path. The code raises an error, and a silent $\infty$ could look like a very bad match.
- **Mixing constraints.** The band and a slope limit together can leave no path, even when each one alone leaves one.
- **Comparing costs across widths.** The banded cost depends on $r$. Use the same width for all the comparisons of one task.
- **Assuming exactness.** Lower bounds and pruning rules that are proved for the banded cost do not bound the unconstrained cost from the same side.

## Exercises

1. Prove that a warping path with $|i - j| \le r$ in every cell exists if and only if $|n - m| \le r$.
2. Show that the band of width $r$ has exactly $n (2r + 1) - r (r + 1)$ cells when $n = m > r$, and check it against the test test_cells_filled.
3. Prove that the banded cost does not increase when $r$ grows, and that it equals the unconstrained DTW cost for $r \ge \max(n, m) - 1$.
4. Find two sequences of length 3 whose banded cost with $r = 0$ is larger than with $r = 1$, and two sequences for which the two costs are equal although the best paths differ.
5. In one form of the Itakura constraint, each step advances $i$ by 1 and $j$ by 0, 1 or 2, and no two consecutive steps advance $j$ by 0. Show that a path from $(1, 1)$ to $(n, m)$ exists only if $m - 1 \le 2 (n - 1)$ and $m - 1 \ge \lfloor (n - 1) / 2 \rfloor$.

## References
