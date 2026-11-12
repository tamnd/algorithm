---
tag: G5A1W2
kind: concept
slug: affine-gap-penalty
name: Affine gap penalty
aliases:
- gap open and extend penalty
- affine gap cost
area: biology/sequence-alignment
level: core
summary: The gap model g(L) = d + (L-1)e with d >= e, a large charge to open a gap and a small charge for each further space; written o + Le in many tools.
prereqs: [gap-penalty, linear-gap-penalty]
see_also: [affine-gap-alignment, gotoh-algorithm, pair-hmm, scoring-matrix, blast, x-drop-extension]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (affine gap score d + (g-1)e) and Section 2.4 (alignment with affine gap scores); Chapter 4 (pair HMMs and the probabilistic meaning of gap scores)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, Section 11.8 (the affine gap weight W_g + q W_s)
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the gap weight w_k = uk + v and its O(mn) alignment algorithm
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, Nucleic Acids Research 25(17), 1997, 3389-3402
    locator: gap costs a + bk, with 10 + k used together with BLOSUM-62
---

An affine gap penalty charges a gap of length $L$ the cost $g(L) = d + (L-1)e$, where $d$ is the cost of the first space and $e \le d$ the cost of each further space. Many tools write the same function as $o + Le$, with an opening cost $o = d - e$ on top of $e$ per space. It is the standard [gap penalty](/gap-penalty/) for DNA and protein alignment, because one insertion or deletion of many residues is one event and should cost much less than many separate events. The [Gotoh algorithm](/gotoh-algorithm/) computes optimal alignments under it in $O(mn)$ time.

## In plain words

A gap is a run of dashes in one row of an alignment. The affine rule has two prices. Starting a new gap costs a lot. Making an existing gap one dash longer costs a little.

So one gap of ten dashes is cheap compared with ten gaps of one dash. This matches biology: a single mutation can insert or delete a whole stretch of letters at once, while ten separate mutations are much less likely.

The two prices are a design choice. If the opening price is high, the best alignment uses few gaps and accepts more mismatches. If the extension price is low, those few gaps can be long. Programs differ in how they name the two prices, so the same numbers can mean slightly different rules in different programs.

## The idea

**Definition.** Fix $d \ge e \ge 0$. A gap of length $L \ge 1$ costs

$$g(L) = d + (L - 1)e.$$

When $d = e$ this is the [linear gap penalty](/linear-gap-penalty/) $g(L) = dL$. Durbin et al. use this form, with $d$ called the gap-open penalty and $e$ the gap-extension penalty.

**The other common form.** With $o = d - e$, the same function is $g(L) = o + Le$. Here every space, including the first, pays $e$, and each gap pays $o$ once more. The forms map as follows.

| source | written as | in terms of $d$ and $e$ |
|---|---|---|
| Durbin et al. | $d + (L-1)e$ | as on this page |
| Gotoh (1982) | $w_k = uk + v$ | $u = e$, $v = d - e$ |
| Gusfield | $W_g + L\,W_s$ | $W_s = e$, $W_g = d - e$ |
| Altschul et al. (1997), BLAST | $a + bk$ | $b = e$, $a = d - e$ |

A setting "gap open 10, extend 1" therefore means $d = 10$ in a program that uses the first form and $d = 11$ in a program that uses the second. The 1997 gapped BLAST paper used the cost $10 + k$, so $d = 11$ and $e = 1$.

**The score with two counts.** Let an alignment have $G$ gaps and $R$ spaces in total. Its affine gap cost is

$$\sum_{\text{gaps}} \bigl(d + (L - 1)e\bigr) = (d - e)\,G + e\,R.$$

So an affine penalty is a linear penalty $e$ per space plus a fixed charge $d - e$ per gap. With the same $R$, an alignment with fewer gaps is cheaper. This is the whole effect of the model.

**Subadditivity and the condition $d \ge e$.** For lengths $a, b \ge 1$,

$$g(a) + g(b) - g(a + b) = d - e.$$

When $d \ge e$, one gap of length $a + b$ costs no more than two gaps of lengths $a$ and $b$, so $g$ is subadditive. The general and the three-table recurrences for gaps both depend on this; see [gap penalty](/gap-penalty/) and [Gotoh algorithm](/gotoh-algorithm/). When $d < e$, long gaps are penalized more than the same spaces split into short gaps, which no biological model suggests, and the standard recurrences overestimate the optimum.

**One column of memory.** Under a linear penalty each space costs $d$ wherever it is. Under an affine penalty a space costs $d$ if the column before it has no space in the same row, and $e$ if it has one. The cost of a column depends on the previous column, and on nothing earlier. That is why three tables suffice: one for alignments that end with a pair, one for those that end with a space in $y$, and one for those that end with a space in $x$. This is the [Gotoh algorithm](/gotoh-algorithm/).

**A probabilistic reading.** In a [pair HMM](/pair-hmm/), a gap state is entered with probability $\delta$ and, once entered, repeated with probability $\varepsilon$. A gap of length $L$ then has probability proportional to $\delta\, \varepsilon^{L-1}$, and its log is

$$\log \delta + (L - 1) \log \varepsilon = -\bigl(d + (L-1)e\bigr) \quad \text{with } d = -\log \delta,\ e = -\log \varepsilon.$$

So an affine penalty is a log-probability for a geometric distribution of gap lengths, with mean length $1/(1 - \varepsilon)$. Durbin et al. derive the exact correspondence, which adds terms for the transitions back to the match state.

## Examples

**Counting gaps and spaces.** With $d = 4$ and $e = 1$:

| alignment | gaps $G$ | spaces $R$ | cost $(d - e)G + eR$ |
|---|---|---|---|
| one gap of length 3 | 1 | 3 | $3 + 3 = 6$ |
| three gaps of length 1 | 3 | 3 | $9 + 3 = 12$ |
| one gap of length 10 | 1 | 10 | $3 + 10 = 13$ |

Under the linear penalty $d = 2$, the first two rows cost the same, 6. Under the affine penalty, a single gap of ten spaces costs about the same as three scattered spaces.

**Linear and affine choose differently.** Align $x = \texttt{CATGCAG}$ with $y = \texttt{CTCACG}$, match $+2$, mismatch $-1$. With the linear penalty $d = 2$, the optimum is $\texttt{CATGCA-G}$ over $\texttt{C-T-CACG}$, five matches and three gaps, score $4$. With $d = 4$, $e = 1$, the optimum is $\texttt{CATGCAG}$ over $\texttt{C-TCACG}$, one gap and three mismatches, score $-1$. The details are on the [linear gap penalty](/linear-gap-penalty/) page.

**From probabilities to penalties.** Measure scores in bits. With $\delta = 1/16$ and $\varepsilon = 1/2$, the gap scores are $d = 4$ bits and $e = 1$ bit, and the mean gap length is $2$. With $\varepsilon = 7/8$, the extension score is $e = \log_2(8/7) \approx 0.19$ bits, and the mean gap length is $8$. Long gaps are cheap to extend exactly when the model expects them to be long.

## Where it is used

- [Alignment with affine gap penalties](/affine-gap-alignment/) is the optimization problem, and the [Gotoh algorithm](/gotoh-algorithm/) solves it in $O(mn)$ time, for global and for local alignment.
- [BLAST](/blast/), [FASTA](/fasta-algorithm/), [minimap2](/minimap2/), [BWA](/bwa/) and other search and mapping tools score gaps with affine penalties, and their extension steps, such as [X-drop extension](/x-drop-extension/) and the [banded Smith-Waterman](/banded-smith-waterman/), use the three-table recurrence.
- Statistical parameters for gapped local alignment scores are estimated separately for each scoring matrix and each pair $(d, e)$, because no closed formula is known for gapped alignments; see [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- Some aligners combine two affine functions and take the smaller cost, which gives a concave piecewise linear penalty with cheap extension for very long gaps.

## References
