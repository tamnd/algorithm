---
tag: 5SKH4T
kind: concept
slug: dot-matrix-plot
name: Dot matrix plot
aliases:
- dot plot
- diagram method
area: biology/sequence-alignment
level: intro
summary: A grid with one sequence on each axis and a dot where the letters, or the windows around them, match; similar regions show as diagonal lines.
prereqs: [pairwise-sequence-alignment]
see_also: [alignment-graph, local-alignment, seed-and-extend, fasta-algorithm, whole-genome-alignment, longest-common-substring, binomial-distribution]
sources:
  - paper: doi:10.1111/j.1432-1033.1970.tb01046.x
    title: Adrian J. Gibbs and George A. McIntyre, The diagram, a method for comparing sequences. Its use with amino acid and nucleotide sequences, European Journal of Biochemistry 16(1), 1970, 1-11
    locator: the diagram of the two sequences, with a mark at each pair of equal residues, and the reading of its diagonal runs
  - paper: doi:10.1073/pnas.78.12.7665
    title: Jacob V. Maizel Jr. and Robert P. Lenk, Enhanced graphic matrix analysis of nucleic acid and protein sequences, Proceedings of the National Academy of Sciences of the USA 78(12), 1981, 7665-7669
    locator: the computer-drawn dot matrix comparisons with a window and a stringency for each dot
---

A dot matrix plot, or dot plot, is a picture that compares two sequences. One sequence goes along the top of a grid and the other down the side, and the cell $(i, j)$ gets a dot when position $i$ of the first sequence matches position $j$ of the second. Regions that are similar show as diagonal runs of dots, so the eye finds them at once, together with repeats, insertions and rearrangements. Gibbs and McIntyre (1970) introduced the method. Maizel and Lenk (1981) made it practical for long sequences with a filter: a dot is drawn only if a window of $w$ letters around the cell has at least $t$ matches. The plot does not compute an alignment, but it shows the structure that the [alignment graph](/alignment-graph/) and the [local alignment](/local-alignment/) algorithms then use.

## In plain words

Write one sequence across the top of a sheet of squared paper and the other down the left side. Put a dot in each square where the letter above and the letter at the side are the same.

If the two sequences share a stretch, its letters match one after the other, and the dots form a slanted line from top left to bottom right. A gap in one sequence moves the line sideways or down. A sequence that repeats a part of itself gives several parallel lines. You see all of this at a glance, without choosing any single alignment.

With only four DNA letters, one square in four gets a dot by chance, and the picture fills with noise. So a better plot looks at a short stretch around each square and draws a dot only if most of the letters in that stretch match.

## The idea

### The raw plot

**Model.** Let $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ be sequences over an alphabet $\Sigma$ (DNA, RNA or amino acids). The *raw* dot plot is the $m \times n$ 0-1 matrix

$$P(i, j) = [x_i = y_j].$$

A run of dots on one diagonal, $P(i, j) = P(i + 1, j + 1) = \cdots = P(i + k - 1, j + k - 1) = 1$, is an exact common substring $x_i \cdots x_{i + k - 1} = y_j \cdots y_{j + k - 1}$. Each diagonal $j - i = c$ is one fixed offset of the two sequences.

The common shapes are:

- **A diagonal line:** a similar region. In a plot of a sequence against itself, the main diagonal is always full.
- **A line shifted to a parallel diagonal:** an insertion or a deletion between two similar regions. The size of the shift is the length of the gap.
- **Parallel lines off the main diagonal of a self-plot:** a repeat. A tandem repeat of period $p$ gives lines at the offsets $\pm p, \pm 2p, \ldots$
- **A square block of dots:** a low-complexity region, such as a run of one letter.
- **A line from bottom left to top right in a plot of $x$ against the reverse complement of $y$:** an inverted repeat, or a part of the DNA that is reversed between the two sequences.

### Noise and the window filter

If the letters are independent and uniform, $\Pr[x_i = y_j] = p = 1/|\Sigma|$: $1/4$ for DNA and $1/20$ for uniform amino acids. So about $mn/4$ cells of a raw DNA plot have a dot by chance, and the true diagonals are hard to see.

The filter of Maizel and Lenk uses a window length $w$ and a stringency $t \le w$. The cell $(i, j)$ gets a dot if

$$\sum_{k = -h}^{h} [x_{i + k} = y_{j + k}] \ge t, \qquad w = 2h + 1,$$

that is, if at least $t$ of the $w$ pairs on the diagonal segment centred at $(i, j)$ match. Some programs put the window at the start of the segment instead of its centre; this moves the dots along the diagonal but does not change the picture.

The number of matches in the window of a random cell follows the [binomial distribution](/binomial-distribution/) $\operatorname{Bin}(w, p)$, so the fraction of noise dots is $\Pr[\operatorname{Bin}(w, p) \ge t]$. A true similar region with few mismatches passes the test in each of its cells, so the filter removes much more noise than signal.

### Cost

A plot of $m \times n$ cells takes $\Theta(mn)$ time for the raw form. A direct filter adds up $w$ terms per cell, $O(mnw)$ time. A sliding sum along each diagonal adds the new pair and removes the old one at each step, so the filtered plot also takes $\Theta(mn)$ time. The plot itself needs $\Theta(mn)$ cells, or less if it is drawn at a lower resolution or kept as a list of the dots. For whole genomes, programs do not test every cell; they find the matching words first, as in [seed-and-extend](/seed-and-extend/), and draw only those.

### Relation to alignment

The plot and the [alignment graph](/alignment-graph/) use the same grid. A dot at $(i, j)$ marks a match edge of the graph, and an alignment is a path that moves down, right or down-right through the grid. The plot shows every such path at once, and the eye picks the diagonals. An alignment algorithm assigns a score to each path and picks the best one. So the dot plot is a first look, and the [local alignment](/local-alignment/) of the regions it shows is the next step.

## Examples

**A self-plot.** Take $x = y = $ TGCATGCATA ($m = n = 10$). The word TGCAT occurs at positions 1 and 5. The raw plot has 26 dots out of 100:

```
   T G C A T G C A T A
T  * . . . * . . . * .
G  . * . . . * . . . .
C  . . * . . . * . . .
A  . . . * . . . * . *
T  * . . . * . . . * .
G  . * . . . * . . . .
C  . . * . . . * . . .
A  . . . * . . . * . *
T  * . . . * . . . * .
A  . . . * . . . * . *
```

The main diagonal is full. The diagonals at offset $+4$ and $-4$ show the repeat, but the noise of single A and T matches makes other short lines.

With a window $w = 3$ and a stringency $t = 3$ (all three pairs must match, and the window must fit inside both sequences, so the first and last rows and columns are empty), 14 dots are left:

```
   T G C A T G C A T A
T  . . . . . . . . . .
G  . * . . . * . . . .
C  . . * . . . * . . .
A  . . . * . . . * . .
T  . . . . * . . . . .
G  . * . . . * . . . .
C  . . * . . . * . . .
A  . . . * . . . * . .
T  . . . . . . . . * .
A  . . . . . . . . . .
```

These are 8 dots on the main diagonal and 6 on the two diagonals at offset $\pm 4$: the repeat GCA at positions 2 to 4 and 6 to 8, without the noise. The window misses the ends of the repeat, which is the cost of the filter.

**The noise fraction.** The fraction of random cells that pass the filter, $\Pr[\operatorname{Bin}(w, p) \ge t]$:

| alphabet | $p$ | $w$ | $t$ | noise fraction |
|---|---|---|---|---|
| DNA | $1/4$ | 1 | 1 | $0.25$ (raw plot) |
| DNA | $1/4$ | 11 | 7 | $7.6 \times 10^{-3}$ |
| DNA | $1/4$ | 15 | 11 | $1.2 \times 10^{-4}$ |
| DNA | $1/4$ | 21 | 14 | $6.8 \times 10^{-5}$ |
| uniform amino acids | $1/20$ | 11 | 7 | $2.2 \times 10^{-7}$ |

For two DNA sequences of 10000 letters, the raw plot has about 25 million random dots, and the filter $w = 21$, $t = 14$ leaves about 6800.

## Where it is used

- A first look at two sequences before an alignment: to see whether they are related over their whole length (use [global alignment](/global-alignment/)), only in parts (use [local alignment](/local-alignment/)), or in a different order.
- Finding repeats in one sequence with a self-plot, and inverted repeats, which can fold into RNA hairpins, with a plot against the reverse complement.
- Whole-genome comparison: a plot of the matching words of two genomes shows the large rearrangements, such as inversions and translocations ([whole-genome alignment](/whole-genome-alignment/)).
- The diagonal idea is the first step of the [FASTA algorithm](/fasta-algorithm/), which counts the word hits on each diagonal before it aligns the best diagonals.

## References
