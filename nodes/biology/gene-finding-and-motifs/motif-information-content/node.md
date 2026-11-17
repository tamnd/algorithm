---
tag: RHYT5C
kind: definition
slug: motif-information-content
name: Motif information content
aliases:
- information content of a weight matrix
area: biology/gene-finding-and-motifs
level: core
summary: The relative entropy of each motif column against the background, summed over columns, the height of the stacks in a sequence logo.
prereqs: [shannon-entropy, kullback-leibler-divergence, position-specific-scoring-matrix]
see_also: [sequence-logo, motif-finding-problem, pwm-score-p-value, meme-algorithm, greedy-motif-search, self-information, laplace-smoothing, consensus-sequence]
sources:
  - paper: doi:10.1016/0022-2836(86)90165-8
    title: Thomas D. Schneider, Gary D. Stormo, Larry Gold and Andrzej Ehrenfeucht, Information content of binding sites on nucleotide sequences, Journal of Molecular Biology 188(3), 1986
    locator: pp. 415 to 431, R_sequence as the sum of the information of the columns of a set of sites, R_frequency from the genome size and the number of sites, and the small-sample correction
  - paper: doi:10.1093/nar/18.20.6097
    title: Thomas D. Schneider and R. Michael Stephens, Sequence logos, a new way to display consensus sequences, Nucleic Acids Research 18(20), 1990
    locator: pp. 6097 to 6100, the stack height of a logo as the information content of the column
  - paper: doi:10.1093/bioinformatics/15.7.563
    title: Gerald Z. Hertz and Gary D. Stormo, Identifying DNA and protein patterns with statistically significant alignments of multiple sequences, Bioinformatics 15, 1999
    locator: pp. 563 to 577, the information content of an alignment against a background and its use as the score of CONSENSUS
---

## Definition

Let a motif of length $L$ be given by the letter frequencies $f_j(a)$ of its columns, $j = 1, \ldots, L$, over the alphabet $\{A, C, G, T\}$, for example the frequencies of a set of $n$ aligned binding sites. Let $q(a) > 0$ be the frequency of letter $a$ in the background. Columns are numbered from 1.

The **information content of column $j$** is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) of the column from the background, in bits:

$$I_j = \sum_{a} f_j(a) \log_2 \frac{f_j(a)}{q(a)},$$

with $0 \log 0 = 0$. The **information content of the motif** is $I = \sum_{j=1}^{L} I_j$.

For the uniform background $q(a) = 1/4$, $I_j = 2 - H_j$, where $H_j = -\sum_a f_j(a) \log_2 f_j(a)$ is the [Shannon entropy](/shannon-entropy/) of the column. This is the form of Schneider, Stormo, Gold and Ehrenfeucht (1986), who call the sum over the sites $R_{\mathrm{sequence}}$ and subtract a small-sample correction from each column, because the entropy of $n$ sampled letters is biased low for small $n$.

**Facts.**

1. $I_j \ge 0$, with equality exactly when $f_j = q$. This is Gibbs' inequality: $-I_j = \sum_a f_j(a) \log_2 (q(a)/f_j(a)) \le \log_2 \sum_{a : f_j(a) > 0} q(a) \le 0$ by Jensen's inequality for the concave $\log_2$, and both steps are equalities only when $q(a)/f_j(a)$ is constant on the support and the support carries all of $q$.
2. $I_j \le \log_2 (1/\min_a q(a))$, with equality for a column that holds only a letter of the smallest background frequency. Since $\log_2 (f_j(a)/q(a)) \le \log_2 (1/q(a)) \le \log_2 (1/\min q)$ for every $a$ with $f_j(a) > 0$, the average is at most the same bound. For the uniform background the bound is 2 bits per column, and $I \le 2L$.
3. **Likelihood ratio.** If $f$ is the frequency matrix of the sites $t_1, \ldots, t_n$, then $\sum_{i=1}^{n} \sum_{j=1}^{L} \log_2 \frac{f_j(t_{ij})}{q(t_{ij})} = n I$. *Proof.* Group the terms of the double sum by column and letter: letter $a$ appears $c_j(a) = n f_j(a)$ times in column $j$, so the sum is $\sum_j \sum_a n f_j(a) \log_2 (f_j(a)/q(a)) = n I$. $\square$ So $nI$ is the log-likelihood ratio, in bits, of the sites under their own column model against the background, and the motif of largest $I$ is the maximum likelihood motif for a fixed number of sites.
4. **Expected score.** With the weights $w_j(a) = \log_2 (f_j(a)/q(a))$ of a [position-specific scoring matrix](/position-specific-scoring-matrix/), a word drawn from the motif model has expected score $\sum_j \sum_a f_j(a) w_j(a) = I$. A word drawn from the background has expected score $-\sum_j \mathrm{KL}(q \Vert f_j) \le 0$ when all $f_j(a) > 0$. So $I$ measures how far the scores of true sites lie above the scores of random words on average.

## Examples and non-examples

**Five sites.** The sites TTC, ATC, TTC, GTC and TTC have the counts (A, C, G, T) = (1, 0, 1, 3), (0, 0, 0, 5) and (0, 5, 0, 0). With the uniform background:

| column | frequencies | $H_j$ | $I_j$ |
|---|---|---|---|
| 1 | 0.2, 0, 0.2, 0.6 | 1.3710 | 0.6290 |
| 2 | 0, 0, 0, 1 | 0 | 2 |
| 3 | 0, 1, 0, 0 | 0 | 2 |

So $I = 4.6290$ bits. The log-likelihood ratio of the five sites is $23.1452 = 5 \times 4.6290$ bits, as fact 3 says.

**Pseudocounts.** With one pseudocount per letter in each column, $f_j(a) = (c_j(a) + 1)/9$, the same sites give $I_1 = 0.1634$ and $I_2 = I_3 = 0.5534$, so $I = 1.2702$ bits. With only five sites the pseudocounts dominate. Report the pseudocounts with any information content, since the value depends on them.

**A non-uniform background.** Let $q(C) = q(G) = 0.2$ and $q(A) = q(T) = 0.3$. A column of only G has $I_j = \log_2 5 = 2.3219$ bits, more than 2, and a column of only A has $I_j = \log_2 (10/3) = 1.7370$ bits. The formula $2 - H_j$ gives 2 for both columns. So with a non-uniform background, $2 - H_j$ is not the information content; it is a non-example.

**Not the information of one site.** $I$ is an average over the sites. The [self-information](/self-information/) of one site, its score $\sum_j w_j(t_{ij})$, can be higher or lower than $I$: in the example, TTC scores $\log_2(0.6/0.25) + 2 + 2 = 5.2630$ bits and ATC scores $\log_2(0.2/0.25) + 4 = 3.6781$ bits.

**$R_{\mathrm{frequency}}$.** Schneider and his coauthors compare $R_{\mathrm{sequence}}$ with $R_{\mathrm{frequency}} = \log_2 (G/\gamma)$, the information needed to pick $\gamma$ sites out of $G$ possible positions. A genome of $G = 4{,}194{,}304$ positions with $\gamma = 64$ sites gives $R_{\mathrm{frequency}} = 16$ bits. They found the two values close for several sets of binding sites; the definition of $I$ does not depend on that finding.

## Related definitions

- **Sequence logo.** A [sequence logo](/sequence-logo/) draws column $j$ as a stack of height $I_j$ (with the small-sample correction), in which letter $a$ has height $f_j(a) I_j$.
- **Relative entropy and entropy.** $I_j$ is the [Kullback-Leibler divergence](/kullback-leibler-divergence/) $\mathrm{KL}(f_j \Vert q)$; for the uniform background it is the drop of the [Shannon entropy](/shannon-entropy/) from 2 bits.
- **Scoring matrices.** The log-odds matrix $w_j(a) = \log_2 (f_j(a)/q(a))$ is the [position-specific scoring matrix](/position-specific-scoring-matrix/) of the motif, and $I$ is the mean of its scores over the motif model. The [p-value of a matrix score](/pwm-score-p-value/) is computed under the background instead.
- **Motif scores.** The CONSENSUS program of Hertz and Stormo ranks alignments of sites by their information content, and [MEME](/meme-algorithm/) maximizes a likelihood whose motif part is $nI$ by fact 3. The Hamming score of [motif finding](/motif-finding-problem/) counts only the letters that differ from the consensus and treats all mismatches alike.
- **Pseudocounts.** Adding pseudocounts to the counts, as in [Laplace smoothing](/laplace-smoothing/), keeps every $f_j(a) > 0$, so the log-odds weights are finite, and lowers $I$.

## References
