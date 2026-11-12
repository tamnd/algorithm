---
tag: 6SSFJ0
kind: concept
slug: sequence-logo
name: Sequence logo
aliases:
- motif logo
area: biology/sequence-alignment
level: intro
summary: "A picture of an alignment: one stack of letters per column, with stack height equal to the information content in bits and letter height proportional to frequency."
prereqs: [multiple-sequence-alignment, shannon-entropy]
see_also: [consensus-sequence, position-specific-scoring-matrix, profile-hmm, self-information, conditional-entropy]
sources:
  - paper: doi:10.1093/nar/18.20.6097
    title: Thomas D. Schneider and R. Michael Stephens, Sequence logos, a new way to display consensus sequences, Nucleic Acids Research 18(20), 1990, pages 6097 to 6100
    locator: the definition of the logo (stack height R_sequence(l) = log2 4 minus (H(l) + e(n)), letter height f(b,l) times R_sequence(l), letters sorted with the most common on top)
  - paper: doi:10.1016/0022-2836(86)90165-8
    title: Thomas D. Schneider, Gary D. Stormo, Larry Gold and Andrzej Ehrenfeucht, Information content of binding sites on nucleotide sequences, Journal of Molecular Biology 188(3), 1986, pages 415 to 431
    locator: R_sequence as the sum of the information of the columns of a set of sites, and the small-sample correction e(n)
  - paper: doi:10.1101/gr.849004
    title: Gavin E. Crooks, Gary Hon, John-Marc Chandonia and Steven E. Brenner, WebLogo, a sequence logo generator, Genome Research 14(6), 2004, pages 1188 to 1190
    locator: the logo program WebLogo, the size of the small-sample correction, and the error bars
---

A sequence logo is a picture of a [multiple sequence alignment](/multiple-sequence-alignment/) with one stack of letters for each column. The height of the stack is the information content of the column in bits: the maximum [entropy](/shannon-entropy/) of the alphabet minus the entropy of the column, minus a small-sample correction. Inside the stack, each letter has a height proportional to its frequency, and the most frequent letter is on top. Schneider and Stephens introduced logos in 1990 as a replacement for the [consensus sequence](/consensus-sequence/), which shows only the top letter of each column.

## In plain words

Take a set of related short sequences, written one above the other so that matching letters stand in the same column. For each column, draw a pile of letters.

A column where all sequences agree gets a tall pile with one big letter. A column where the letters are mixed in equal parts gets a short pile, because it tells you little. In between, the pile is of medium height, and each letter takes a share of the pile that matches how often it occurs. The most common letter goes on top.

So you can see at a glance which positions matter, which letter each position prefers, and how strongly. A plain consensus line shows only the top letter of each column and hides all of this.

## The idea

**Information of a column.** Let the alphabet have $s$ letters ($s = 4$ for DNA, $s = 20$ for proteins). For column $l$ of the alignment, let $n$ be the number of sequences with a letter (not a gap) in the column and $f(b, l)$ the fraction of them with letter $b$. The uncertainty of the column is the Shannon entropy

$$H(l) = -\sum_{b} f(b, l) \log_2 f(b, l),$$

with $0 \log_2 0 = 0$. Before you look at the column, a letter drawn uniformly at random has uncertainty $\log_2 s$. The information in the column is the drop in uncertainty:

$$R_{\text{sequence}}(l) = \log_2 s - \bigl(H(l) + e(n)\bigr).$$

For DNA the maximum is $\log_2 4 = 2$ bits, reached when the column has one base only. For proteins it is $\log_2 20 \approx 4.32$ bits.

**Letter heights.** The stack of column $l$ has height $R_{\text{sequence}}(l)$. Letter $b$ has height $f(b, l) \cdot R_{\text{sequence}}(l)$, so the letter heights add up to the stack height. The letters are sorted by frequency, with the most frequent on top. The top letter of each column, read from left to right, is the consensus.

**The small-sample correction $e(n)$.** The frequencies $f(b, l)$ come from only $n$ sequences. Even if the true column were uniform, a sample of $n$ letters looks less uniform than it is, and its entropy is low on average. Without a correction, a column with one sequence would always show 2 bits. Schneider et al. (1986) define the correction as the expected shortfall of the sample entropy for $n$ letters drawn from the uniform distribution:

$$e(n) = \log_2 s - \mathbb{E}\bigl[H_n\bigr],$$

where $H_n$ is the entropy of the frequencies of $n$ independent uniform letters. This makes the expected height of a random column zero. A second-order Taylor expansion of the entropy of the sample frequencies gives the large-$n$ form

$$e(n) \approx \frac{s - 1}{2 n \ln 2},$$

which is $3 / (2 n \ln 2)$ for DNA. The exact and approximate values for DNA are:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 10 | 20 |
|---|---|---|---|---|---|---|---|---|
| exact $e(n)$ | 2.0000 | 1.2500 | 0.8891 | 0.6760 | 0.5371 | 0.4408 | 0.2467 | 0.1140 |
| $3 / (2 n \ln 2)$ | 2.1640 | 1.0820 | 0.7213 | 0.5410 | 0.4328 | 0.3607 | 0.2164 | 0.1082 |

For one sequence the exact correction is the full 2 bits, so a column of one sequence has height 0, as it should. The approximation is poor for small $n$ and good for $n \ge 20$. Crooks et al. (2004) report that the correction matters for fewer than about 20 DNA or 40 protein sequences.

**Information and relative entropy.** For a uniform background, $\log_2 s - H(l) = \sum_b f(b, l) \log_2 \bigl(f(b, l) / (1/s)\bigr)$, the relative entropy of the column to the uniform distribution. When the background is not uniform, for example in a genome rich in A and T, many logo programs draw the relative entropy $\sum_b f(b, l) \log_2 (f(b, l) / q_b)$ to the background frequencies $q_b$ instead. This is the expected score of a [position-specific scoring matrix](/position-specific-scoring-matrix/) column, so a logo of this kind shows how much each column adds to a PSSM score.

**Total information.** Schneider et al. (1986) add the column heights over a binding site to get $R_{\text{sequence}} = \sum_l R_{\text{sequence}}(l)$, the information in bits that the site holds. They compare it with the information needed to find the sites in a genome.

**Reading a logo with care.**

- *Negative heights.* With the correction, a column with few letters can get $R < 0$. Programs then draw nothing or clip at zero. A negative value means only that the column holds no measurable information.
- *Gaps.* A column that is mostly gaps has a small $n$ and a large correction. It can also show a tall stack from two or three letters. Look at $n$ before you trust such a column.
- *Weights.* Near-identical sequences count many times. Sequence weights reduce this bias, but they also change the effective $n$ for the correction.
- *Height is not order.* A tall letter means a frequent letter in a conserved column. It does not mean that the letter is important for function on its own; the logo shows statistics of the sample only.
- *Error bars.* WebLogo can draw error bars of twice the small-sample correction, as a rough guide to the sampling error.

## Examples

Take the alignment of six DNA rows used on the [consensus sequence](/consensus-sequence/) page.

```
r1  T A T A - A T
r2  T A T G - A A
r3  T A T G - A T
r4  C A T A G A T
r5  T A - A - G T
r6  T G T G T A C
```

The table gives, for each column, the number $n$ of letters, the entropy $H$, the exact correction $e(n)$, the stack height $R$ and the letter heights, all in bits.

| column | counts | $n$ | $H$ | $e(n)$ | $R$ | letters, top first |
|---|---|---|---|---|---|---|
| 1 | T 5, C 1 | 6 | 0.6500 | 0.4408 | 0.9092 | T 0.7577, C 0.1515 |
| 2 | A 5, G 1 | 6 | 0.6500 | 0.4408 | 0.9092 | A 0.7577, G 0.1515 |
| 3 | T 5 | 5 | 0 | 0.5371 | 1.4629 | T 1.4629 |
| 4 | A 3, G 3 | 6 | 1.0000 | 0.4408 | 0.5592 | A 0.2796, G 0.2796 |
| 5 | G 1, T 1 | 2 | 1.0000 | 1.2500 | $-0.25$ | (none) |
| 6 | A 5, G 1 | 6 | 0.6500 | 0.4408 | 0.9092 | A 0.7577, G 0.1515 |
| 7 | T 4, A 1, C 1 | 6 | 1.2516 | 0.4408 | 0.3076 | T 0.2051, A 0.0513, C 0.0513 |

Column 3 is the tallest, because all of its five letters agree. Column 7 has the same consensus letter T as column 1 but only a third of its height, because its T is less certain. Column 4 is a tie, and its two letters stand at the same height in a short stack. Column 5, the insert column, has only two letters, and its correction of 1.25 bits is larger than what the two letters could give; its height is negative and the logo shows an empty column. The total over the six columns with positive height is 5.0573 bits.

Without the correction the heights would be 1.35, 1.35, 2.0, 1.0, 1.0, 1.35 and 0.7484 bits. The correction takes 0.44 to 0.54 bits from each column with five or six letters, which is between a quarter and more than half of the uncorrected height, because six sequences are few.

With a background of 30 percent A and T and 20 percent C and G, the relative entropy of column 1 is 1.1844 bits (T 0.9870, C 0.1974), and that of column 4 is 1.0294 bits, larger than its 1.0 bit against the uniform background, because G at 50 percent is far above its background of 20 percent.

## Where it is used

- **Transcription factor binding sites.** The original use: logos of DNA binding sites show the conserved positions and the information of a site, and databases of binding-site models show each model as a logo.
- **Protein families.** Logos of the columns of a family alignment, or of the match states of a [profile HMM](/profile-hmm/), show conserved residues at a glance.
- **Splice sites, start sites and other short signals.** These are short and are summarized well by one logo.
- **Results of motif finders.** Programs that find motifs, for example by [Gibbs sampling](/gibbs-sampling/), report each motif as a PSSM and draw it as a logo.
- **Tools.** WebLogo (Crooks et al. 2004) and its descendants compute the heights described above, with options for the background, the correction and the error bars.

## References
