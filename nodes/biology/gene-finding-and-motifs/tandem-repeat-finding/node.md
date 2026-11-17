---
tag: 3VVNE0
kind: algorithm
slug: tandem-repeat-finding
name: Tandem repeat finding
aliases:
- Tandem Repeats Finder
- Benson tandem repeat algorithm
area: biology/gene-finding-and-motifs
level: advanced
summary: Find approximate tandem repeats with k-tuple matches at a common distance as candidates, then confirm them by wraparound alignment.
model: word-ram
complexity:
  vars: {G: the length of the sequence, m: the largest period searched, k: the tuple length}
  time: {worst: O(G^2 m), average: O(G m), best: Θ(G)}
  space: {extra: O(G m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1999
  people: [Gary Benson]
  note: Benson published the k-tuple detection with statistical criteria and the confirmation by wraparound dynamic programming in Nucleic Acids Research in 1999.
prereqs: [smith-waterman, kmer, string-period]
see_also: [repeat-masking, genome-repeat, computing-runs, main-lorentz-algorithm, periodicity-detection, square, local-alignment, maximal-repeats]
sources:
  - paper: doi:10.1093/nar/27.2.573
    title: Gary Benson, Tandem repeats finder, a program to analyze DNA sequences, Nucleic Acids Research 27(2), 1999
    locator: pp. 573 to 580; the k-tuple history and distance lists, the sum of heads, random walk, apparent size and waiting time criteria, wraparound dynamic programming, the consensus pattern, and the default weights and parameters
  - paper: doi:10.1007/BF02458834
    title: Eugene W. Myers and Webb Miller, Approximate matching of regular expressions, Bulletin of Mathematical Biology 51(1), 1989
    locator: pp. 5 to 37; alignment of a sequence with a regular expression, which includes a pattern repeated any number of times
  - paper: "V. A. Fischetti, G. M. Landau, J. P. Schmidt and P. H. Sellers, Identifying periodic occurrences of a template with applications to protein structure, Combinatorial Pattern Matching (CPM 1992), Lecture Notes in Computer Science 644, pp. 111 to 120"
    locator: the wraparound dynamic program for the alignment of a text with tandem copies of a template
---

Tandem repeat finding locates the places in a DNA sequence where a short pattern occurs many times in a row, with some substitutions, insertions and deletions between the copies. Benson's method, published with the program TRF, works in two steps. A fast scan with $k$-tuple matches finds pairs of equal short words at the same distance $d$ many times in a small window, which is the sign of a repeat with period $d$. Each candidate is then confirmed by *wraparound dynamic programming* (WDP), an alignment of the sequence with any number of copies of the pattern, and is reported if at least two copies align with a high enough score.

## In plain words

A tandem repeat looks like CAGCAGCAGCAG: the same short word again and again, side by side. In real DNA the copies are not perfect, because mutations change, add or remove letters. To find such places, slide along the sequence and look at short words of a few letters. When a word appears again a fixed number of letters later, note that distance. Inside a repeat, the same distance shows up again and again, because every word of one copy appears again in the next copy. When one distance has been seen often enough in a short stretch, take the last copy as a guess of the repeated word, and line it up with the sequence around it, copy after copy. If many copies line up well, report the stretch, the word and the number of copies.

## The problem

**Input.** A DNA sequence $s$ of length $G$, a tuple length $k$, a largest period $m$, the alignment weights $\mu$ (match), $\sigma$ (mismatch) and $\delta$ (insertion or deletion), all positive, a minimum score, and a match probability $p_M$ for the detection test.

**Output.** A list of approximate tandem repeats. Each report is an interval $[a, b)$ of $s$, a period $d \le m$, a consensus pattern $P$ of length $d$, the alignment score of $s[a, b)$ with copies of $P$, and the number of copies, which is the number of pattern letters that the alignment uses divided by $d$.

A tandem repeat with period $d$ is a substring that aligns well with $P^c = P P \cdots P$ for some $c \ge 2$. With no errors this is the [string period](/string-period/) notion, and exact tandem repeats are [squares](/square/) and runs, which the string algorithms on [computing runs](/computing-runs/) and the [Main-Lorentz algorithm](/main-lorentz-algorithm/) find. DNA repeats have errors, so the definition uses an alignment score, and there is no single correct output: what counts as a repeat depends on the weights and the cutoffs. TRF is a heuristic for this task, not an exact algorithm for a fixed objective. Its confirmation step, WDP, is exact for what it computes.

Positions here are 0-based, and $[a, b)$ is half-open, as in the code.

## The algorithm

### Detection

Keep a *history list* $H[t]$ for each $k$-tuple $t$: the earlier positions where $t$ starts. At position $i$, the tuple $t = s[i, i + k)$ matches each earlier position $j$ in $H[t]$, at distance $d = i - j$. For each distance there is a *window list*: the matched tuples at distance $d$ that lie in the last $W(d)$ positions, with $W(d) = \max(d, 30)$ in the code. The *sum of heads* of the window is the number of positions covered by these matched tuples. If two copies of a repeat are aligned base by base, a position is a *head* when its base equals the base $d$ positions before it, and a $k$-tuple match at distance $d$ is a run of $k$ heads. So the sum of heads counts the heads that lie in runs of at least $k$.

Benson models the heads of two true copies as independent coin tosses that come up heads with probability $p_M$. A candidate needs a sum of heads at least as large as the value that 95 percent of true windows reach under this model. Benson gets the threshold from a normal approximation; the code computes the exact quantile with a small dynamic program over the length of the current run.

```pseudo id=main
FIND-TANDEM-REPEATS(s, k, m, p_M, min_score)
L1  H ← an empty history list for each k-tuple, R ← an empty list of repeats
L2  for i ← 0 to G - k do
L3      t ← s[i, i + k), c ← i + k
L4      for each j in H[t] with d = i - j ≤ m, nearest first do
L5          add i to the window list of d, and drop the tuples that start before c - W(d)
L6          if heads(d) ≥ threshold(W(d), k, p_M) and no report of R explains (c - 1, d) then
L7              P ← s[c - d, c), align P around c by WDP, then replace P by the consensus and realign
L8              u ← the number of pattern letters that the alignment uses
L9              if u ≥ 2d and score ≥ min_score then
L10                 add ([a, b), d, P, score, u / d) to R
L11     append i to H[t]
L12 return R without the reports that a report with a smaller period dividing theirs covers
```

A report *explains* $(c - 1, d)$ when its period is at most $d$ and position $c - 1$ lies inside it or less than one period after its end. Line L6 also tests each distance at most once per window, so a long repeat does not start a new alignment at every position. The window of line L7 starts at $3d + 30$ bases on each side of $c$, and it grows until the alignment ends at least $d + 20$ bases from both edges or reaches the end of $s$. The consensus takes, for each pattern position, the most common base aligned to it, and the loop of line L7 realigns with the new pattern until it does not change, at most three times.

### Wraparound dynamic programming

WDP aligns a text $T = t_1 \ldots t_n$ with a substring of $P^\infty = P P P \cdots$, locally. The table has one row per text position and one column per pattern position. Column 0 is a copy of column $d$: the end of one copy is the start of the next. With $s(t, p) = \mu$ for $t = p$ and $-\sigma$ otherwise:

```pseudo id=wdp
WDP(T, P, μ, σ, δ)    ▷ T of length n, P of length d
W1  V[0][0 .. d] ← 0
W2  for x ← 1 to n do
W3      for j ← 1 to d do V[x][j] ← max(0, V[x-1][j-1] + s(t_x, p_j), V[x-1][j] - δ, V[x][j-1] - δ)
W4      V[x][0] ← V[x][d]    ▷ the wrap
W5      for j ← 1 to d while V[x][j-1] - δ > V[x][j] do V[x][j] ← V[x][j-1] - δ
W6  (x*, j*) ← a cell with the largest value
W7  trace back from (x*, j*) to a cell of value 0, reading column 0 as column d
```

The move $V[x][j-1] - \delta$ deletes a pattern letter, and for $j = 1$ it reads column 0 of the same row, which is only known after the row is done. So each row is a cyclic system. Line W3 solves it without the wrap, line W4 copies the last column into column 0, and line W5 makes a second pass. Two passes are enough, because a run of $d$ or more deletions in one row returns to the same column with a lower score, so a best path crosses the wrap at most once. The second pass can stop at the first column where it changes nothing.

## Example

**WDP.** Align $T = \mathrm{ACGACGCGACG}$, which is ACG, ACG, CG (a copy with the A deleted) and ACG, with $P = \mathrm{ACG}$ and the TRF weights $\mu = 2$, $\sigma = 7$, $\delta = 7$:

| $x$ | $t_x$ | $j = 1$ (A) | $j = 2$ (C) | $j = 3$ (G) |
|---|---|---|---|---|
| 0 | | 0 | 0 | 0 |
| 1 | A | 2 | 0 | 0 |
| 2 | C | 0 | 4 | 0 |
| 3 | G | 0 | 0 | 6 |
| 4 | A | 8 | 1 | 0 |
| 5 | C | 1 | 10 | 3 |
| 6 | G | 5 | 3 | 12 |
| 7 | C | 5 | 7 | 5 |
| 8 | G | 2 | 0 | 9 |
| 9 | A | 11 | 4 | 2 |
| 10 | C | 4 | 13 | 6 |
| 11 | G | 8 | 6 | 15 |

Row 4 uses the wrap of line W3: $V[4][1] = V[3][3] + 2 = 8$, because column 0 of row 3 is column 3. Row 6 uses the second pass: after the first pass $V[6][1]$ is 0, line W4 sets column 0 to $V[6][3] = 12$, and line W5 sets $V[6][1] = 12 - 7 = 5$. This is the deleted A. Then $V[7][2] = 5 + 2 = 7$, $V[8][3] = 9$, and the path goes on to the best cell $V[11][3] = 15$. The traceback gives all 11 letters of $T$ against 12 letters of $P^\infty$, with one deletion: $11 \cdot 2 - 7 = 15$. The alignment uses 12 pattern letters, so it has 4 copies. A plain local alignment of $T$ with ACGACGACGACG gives the same score 15, as Theorem 1 of the proof says.

**The finder.** For $s = \mathrm{TTGCA}$ followed by ten copies of ACG and then GGTCA, with $k = 4$, $m = 50$, $p_M = 0.8$ and minimum score 50, the scan finds matches at distance 3 from position 8 on. The window for $d = 3$ has length 30, and its threshold is 9 heads. The first match at distance 3 covers 4 heads, and each later one adds 1, so the test passes at the tuple that starts at position 13 and ends at position 16. The WDP confirms the repeat, and the output is one report: $[5, 35)$, period 3, pattern ACG, score 60 (30 matches), 10 copies. The distances 6, 9, and so on also collect matches, but the period-3 report explains them.

**The threshold.** With $p_M = 0.75$, $k = 5$ and a window of 100, Benson's normal approximation gives a threshold of 26 heads. The exact law gives 27: the probability of fewer than 27 heads is at most 0.05, and the probability of fewer than 28 is more.

## Correctness

Two parts are exact, and the proof file proves them.

- **WDP is a local alignment with copies.** The value $V[x][j]$ is the best score of an alignment that ends at text position $x$ and at a pattern letter of phase $j$, or 0. Each row is the unique solution of its cyclic system, and two passes compute it (a theorem). The best cell gives the same score as a [Smith-Waterman](/smith-waterman/) alignment of $T$ with $P^M$ for $M$ large enough, so WDP is a [local alignment](/local-alignment/) against any number of copies, in $O(n d)$ time instead of $O(n \cdot n)$.
- **The threshold is the exact quantile under the model.** The dynamic program over (run length capped at $k$, count) gives the exact law of the sum of heads for independent heads with probability $p_M$. So a true window that follows the model passes line L6 with probability at least 0.95 (a theorem about the model).

Detection is a heuristic. A real repeat can fail the test because of indels, which move the matches to a nearby distance, or because its mutations cluster. A random sequence can pass it, and then the WDP score decides. So the finder has no guarantee to report every repeat with a score above the cutoff, and TRF does not claim one.

## Complexity

The model is the word RAM, and a $k$-tuple of DNA fits in one word.

- **Scan.** Each position appends to one history list and reads the entries within distance $m$, from the end, so it costs $O(1 + e_i)$, where $e_i \le m$ is the number of matches it finds. Each match costs $O(1)$ amortized for its window list. In random DNA with uniform bases, $e_i$ has mean about $m / 4^k$, so the scan costs $O(G (1 + m / 4^k))$, which is $O(G m)$; for a sequence with no repeated tuples it is $\Theta(G)$.
- **Thresholds.** The table for one window length $w$ takes $O(k w^2)$ time, and there are at most $m$ different lengths, all cached.
- **Confirmation.** A WDP of a window of length $n$ with a pattern of length $d$ costs $O(n d)$ time and space. Each distance is tested at most once per window length, so the number of tests is at most $G$ per distance, and a test window can grow to $G$. This gives the crude worst case $O(G^2 m)$; on sequences with few repeats the WDP work is small next to the scan.
- **Space.** The history lists take $O(G)$, the window lists $O(m^2)$, and a WDP table $O(G m)$ at most.

TRF has the same shape: a linear scan with lists, and WDP on candidates only. For patterns longer than 20, Benson restricts the WDP to a band around the diagonal, which lowers the cost of a test.

## Properties

- **Deterministic.** There is no randomness; the same input gives the same reports.
- **Not exact.** The output depends on the detection test, the window growth and the consensus rounds. Two repeats that differ only by their phase are reported with patterns that are rotations of each other.
- **Period choice.** A repeat with period $d$ also has matches at $2d$, $3d$ and so on. The code reports the smallest period that explains a region. TRF can report up to three periods for one region, for example when a repeat of period 6 is also a looser repeat of period 3.
- **Consensus.** With few copies, a tie in the majority vote keeps the old base, so a mutation in the first guess can stay in the consensus. Rounds of realignment reduce this but do not remove it.
- **Scores.** With $\mu = 2$ and $\sigma = \delta = 7$, one error costs as much as 3.5 matches. A minimum score of 50 needs at least 25 matching bases.

## Variants and improvements

- **What the code leaves out.** TRF also counts a match at distance $d$ for the distances $d \pm 1, \ldots, d \pm \Delta d$, so that indels do not split the evidence across neighbouring distances. It uses three more tests: a random walk bound that gives $\Delta d$, an *apparent size* test that rejects a distance when a smaller distance explains the same matches, and a *waiting time* test on the gaps between matches. It chooses the tuple size by the range of pattern sizes, uses banded WDP for patterns longer than 20, builds a consensus whose length can differ from $d$, and filters reports with related periods. The code keeps one $k$, a fixed minimum window, and the simple rule of line L12.
- **Parameters of the paper.** Benson gives two weight sets, $(\mu, \sigma, \delta) = (2, 7, 7)$ and $(2, 5, 7)$, two pairs of match and indel probabilities, $(p_M, p_I) = (0.80, 0.10)$ and $(0.75, 0.20)$, a minimum alignment score of 50, and pattern sizes from 1 to 500.
- **Exact repeats.** For repeats with no errors, the string algorithms are exact and fast: all squares by [Main-Lorentz](/main-lorentz-algorithm/) in $O(n \log n)$ time, and all runs in linear time ([computing runs](/computing-runs/), with the [runs theorem](/runs-theorem/) bound on their number).
- **Alignment with a regular expression.** WDP is a special case of the alignment of a sequence with the regular expression $P^*$, which Myers and Miller (1989) solve in general.
- **Masking.** [Repeat masking](/repeat-masking/) tools run a tandem repeat finder for the simple repeats, and a library search for the interspersed ones.

## When to use it

Use it to list microsatellites and minisatellites in a genome or a contig, to mask simple repeats before gene finding or alignment, to choose markers whose copy number varies between individuals, and to check an assembly for collapsed repeats. Use an exact runs algorithm when only perfect repeats matter. For repeat families spread over the genome, such as transposons, use a library search ([repeat masking](/repeat-masking/)); a tandem repeat finder sees only copies that are next to each other.

## Pitfalls

- **Period multiples.** A repeat with period 3 is also a repeat with period 6, 9 and so on, with a lower score per copy. Without a rule, the output lists each region many times.
- **Rotations.** ACG, CGA and GAC describe the same repeat. Compare patterns up to rotation, and pick a canonical rotation if the reports are merged.
- **Short windows.** For small periods a window of length $d$ holds too few tuples, and the threshold falls to 0, so every match becomes a candidate. The code uses a minimum window of 30; TRF uses smaller tuples for small patterns.
- **Weights in two conventions.** TRF writes the mismatch and indel weights as positive penalties. Many alignment libraries add negative scores. Mixing the two turns a penalty into a reward.
- **Low-complexity flanks.** A homopolymer next to a repeat aligns with many patterns. Check the reported ends, and mask homopolymers on their own if they matter.
- **Copy number.** The copy number is a ratio of aligned pattern letters to the period, so it can be fractional, and the last partial copy may be cut off by the local alignment.

## Implementations

## History

Benson (1999) described the program TRF in Nucleic Acids Research. It joins a fast filter based on $k$-tuple matches at a common distance, with criteria drawn from a probabilistic model of two aligned copies, with wraparound dynamic programming to confirm and align each candidate. Wraparound dynamic programming goes back to the alignment of sequences with regular expressions by Myers and Miller (1989) and to the search for periodic occurrences of a template by Fischetti, Landau, Schmidt and Sellers (1992). TRF became the standard tool for simple repeats, and repeat masking pipelines call it for that part of the work.

## References
