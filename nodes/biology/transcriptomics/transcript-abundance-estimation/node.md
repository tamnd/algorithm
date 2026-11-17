---
tag: F7SM8W
kind: problem
slug: transcript-abundance-estimation
name: Transcript abundance estimation
aliases:
- isoform quantification
- expression quantification
area: biology/transcriptomics
level: core
summary: 'Estimate how much of each transcript is in a sample when many reads are compatible with several isoforms or genes, usually as a maximum likelihood estimate found by EM.'
prereqs: [rna-sequencing, maximum-likelihood-estimation]
see_also: [em-isoform-quantification, pseudoalignment, selective-alignment, rpkm-and-fpkm, transcripts-per-million, expectation-maximization, differential-expression-analysis, bootstrap-method]
sources:
  - paper: doi:10.1093/bioinformatics/btp113
    title: Hui Jiang and Wing Hung Wong, Statistical inferences for isoform expression in RNA-Seq, Bioinformatics 25(8) (2009)
    locator: pp. 1026 to 1032 (a Poisson model of read counts over exon regions)
  - paper: doi:10.1093/bioinformatics/btp692
    title: Bo Li, Victor Ruotti, Ron M. Stewart, James A. Thomson and Colin N. Dewey, RNA-Seq gene expression estimation with read mapping uncertainty, Bioinformatics 26(4) (2010)
    locator: pp. 493 to 500, Section 2.2 (the EM algorithm and the concave likelihood)
  - paper: doi:10.1186/1471-2105-12-323
    title: Bo Li and Colin N. Dewey, RSEM, accurate transcript quantification from RNA-Seq data with or without a reference genome, BMC Bioinformatics 12 (2011)
    locator: Article 323, Methods (effective length, TPM and credibility intervals)
  - paper: doi:10.1038/nbt.1621
    title: Cole Trapnell, Brian A. Williams, Geo Pertea, Ali Mortazavi, Gordon Kwan, Marijke J. van Baren, Steven L. Salzberg, Barbara J. Wold and Lior Pachter, Transcript assembly and quantification by RNA-Seq reveals unannotated transcripts and isoform switching during cell differentiation, Nature Biotechnology 28(5) (2010)
    locator: pp. 511 to 515, Online Methods (the likelihood of the fragments, its unique maximum when the model is identifiable, and FPKM)
  - paper: doi:10.1038/nbt.3519
    title: Nicolas L. Bray, Harold Pimentel, Páll Melsted and Lior Pachter, Near-optimal probabilistic RNA-seq quantification, Nature Biotechnology 34(5) (2016)
    locator: pp. 525 to 527 (pseudoalignment and the EM on equivalence classes)
  - paper: doi:10.1038/nmeth.4197
    title: Rob Patro, Geet Duggal, Michael I. Love, Rafael A. Irizarry and Carl Kingsford, Salmon provides fast and bias-aware quantification of transcript expression, Nature Methods 14(4) (2017)
    locator: pp. 417 to 419 (the bias models and the inference on equivalence classes)
  - paper: doi:10.1038/nmeth.1226
    title: Ali Mortazavi, Brian A. Williams, Kenneth McCue, Lorian Schaeffer and Barbara Wold, Mapping and quantifying mammalian transcriptomes by RNA-Seq, Nature Methods 5(7) (2008)
    locator: pp. 621 to 628 (RPKM and the reassignment of multireads)
---

Transcript abundance estimation, or isoform quantification, finds how much of each known transcript a sample holds from its [RNA-seq](/rna-sequencing/) reads. The reads are short, and the isoforms of a gene share exons, so many reads fit two or more transcripts and cannot simply be counted. The standard answer is a probabilistic model in which each read comes from one transcript, chosen with a probability proportional to the abundance of the transcript times its length. The [maximum likelihood estimate](/maximum-likelihood-estimation/) of the abundances is found by the [EM algorithm](/em-isoform-quantification/). The log-likelihood is concave, so every local maximum is a global one, but the maximum is not unique when two transcripts cannot be told apart by the reads. RSEM, Cufflinks, kallisto and Salmon all solve versions of this problem.

## In plain words

You have a box of pieces from many messages, and you want to know how many copies of each message were in the sample. A piece that fits only one message is easy: it counts for that message. But many pieces fit two or three messages, because the messages share parts.

You cannot count such a piece for all of them, and dropping it throws away information. The fair way is to share it out. If message A is three times as common as message B, a piece that fits both is three times as likely to be from A. But you do not know how common A and B are; that is the question.

So you guess, share the pieces by the guess, count again, and repeat. The guess gets better each time and settles on the answer that best explains all the pieces.

## Definition

**Input.** A set of $m$ transcripts with effective lengths $\ell_1, \ldots, \ell_m$, where the effective length is the number of positions at which a fragment can start. A set of $N$ reads or read pairs, and for each read $r$ the probability $P(r \mid t)$ that a fragment from transcript $t$ gives this read, which is 0 when $r$ does not fit $t$. In the simplest model, $P(r \mid t) = 1 / \ell_t$ for every transcript that the read fits.

**Model.** A fragment comes from transcript $t$ with probability $\alpha_t$, and $\alpha$ is in the simplex: $\alpha_t \ge 0$ and $\sum_t \alpha_t = 1$. The reads are independent, so

$$\log L(\alpha) = \sum_{r} \log \sum_{t} \alpha_t \, P(r \mid t).$$

**Output.** The $\alpha$ that maximizes $\log L$, or a posterior distribution over $\alpha$. The fractions of molecules are $\tau_t = (\alpha_t / \ell_t) / \sum_u (\alpha_u / \ell_u)$, and the [transcripts per million](/transcripts-per-million/) are $10^6 \tau_t$. [FPKM](/rpkm-and-fpkm/) uses the expected counts $N \alpha_t$ instead: $\mathrm{FPKM}_t = N \alpha_t \cdot 10^9 / (\ell_t N)$.

**Equivalence classes.** With $P(r \mid t) = 1/\ell_t$, two reads that fit the same set of transcripts add the same term to $\log L$. Grouping the reads by their set $e$, with $c_e$ reads in it, gives $\log L(\alpha) = \sum_e c_e \log \sum_{t \in e} \alpha_t / \ell_t$, which has one term per class instead of one per read.

## Variants

- **How reads are matched to transcripts.** Full alignment to the transcripts or to the genome with a [read mapper](/read-mapping/), [pseudoalignment](/pseudoalignment/), which returns only the set of compatible transcripts, or [selective alignment](/selective-alignment/), which also scores the alignment.
- **Bias models.** $P(r \mid t)$ can depend on the fragment length, the position in the transcript, the GC content and the sequence near the fragment ends. Salmon fits such bias models and folds them into the effective lengths.
- **Point estimate or uncertainty.** RSEM gives credibility intervals by Gibbs sampling, kallisto gives bootstrap estimates by running the EM on resampled counts, and Salmon offers both bootstrap and Gibbs samples. See [bootstrap](/bootstrap-method/) and [Gibbs sampling](/gibbs-sampling/).
- **Gene-level estimates.** The abundance of a gene is the sum over its isoforms. It is far less uncertain than the isoform values, because reads shared between isoforms of one gene do not matter for the sum.
- **Count-based models.** Jiang and Wong (2009) model the read counts in exon regions as Poisson variables whose means are sums over the isoforms, which gives the same kind of likelihood.
- **Single-cell counts.** In [single-cell RNA-seq](/single-cell-rna-sequencing/), molecules are counted by barcodes after [UMI deduplication](/umi-deduplication/), and the same sharing problem appears for molecules that fit several genes.

## Examples

**Sharing reads by EM.** Two transcripts $t_1$ and $t_2$ have effective lengths 1000 and 500. Of 100 reads, 30 fit only $t_1$, 30 fit only $t_2$, and 40 fit both. The log-likelihood is

$$30 \log \frac{\alpha_1}{1000} + 40 \log\Big(\frac{\alpha_1}{1000} + \frac{\alpha_2}{500}\Big) + 30 \log \frac{\alpha_2}{500}.$$

The maximum is at $\alpha = (0.4, 0.6)$: setting $\alpha_2 = 1 - \alpha_1$, the derivative is $30/\alpha_1 - 40 \cdot 0.001 / (0.002 - 0.001 \alpha_1) - 30/(1 - \alpha_1)$, and at $\alpha_1 = 0.4$ it is $75 - 25 - 50 = 0$. The 40 shared reads are split 10 to $t_1$ and 30 to $t_2$, because a read that fits both is three times as likely to come from $t_2$ at these values. The molecule fractions are $0.4/1000 : 0.6/500 = 1 : 3$, so the TPM values are 250000 and 750000. Two simple rules give other answers. Dropping the shared reads, or splitting them equally, gives the counts 30 and 30 or 50 and 50, and in both cases TPM values of 333333 and 666667. The [EM page](/em-isoform-quantification/) runs the iteration on these numbers.

**A ridge.** Two transcripts $t_1$ and $t_2$ have the same effective length, and every read fits both. Then $\log L$ depends only on $\alpha_1 + \alpha_2$, and every split of the reads between the two is a maximum. No method can tell how the reads divide, and the EM returns a point on the ridge that depends on where it starts. The gene-level sum is still well defined.

**Lengths matter.** A transcript of effective length 2000 and one of 500 have the same number of molecules. The first gets four times as many reads, so $\alpha = (0.8, 0.2)$, while the molecule fractions are $\tau = (0.5, 0.5)$ and both have the TPM 500000.

## Known algorithms

- **EM on reads or on equivalence classes.** Li, Ruotti, Stewart, Thomson and Dewey (2010) gave the EM for this model with a noise transcript, and RSEM (2011) added effective lengths, TPM and credibility intervals. kallisto and Salmon run the EM on equivalence classes, which is much faster. See [EM isoform quantification](/em-isoform-quantification/).
- **Cufflinks.** Trapnell and colleagues (2010) maximize the likelihood of the fragments over the transcripts of each locus, with a fragment length model, and report FPKM. They note that the maximum is unique when the model is identifiable.
- **kallisto.** Bray, Pimentel, Melsted and Pachter (2016) find the equivalence class of each read by [pseudoalignment](/pseudoalignment/) and then run the EM on the class counts.
- **Salmon.** Patro, Duggal, Love, Irizarry and Kingsford (2017) map the reads, fit bias models, and estimate the abundances with an online phase followed by an EM or variational Bayes phase on equivalence classes. Its mapping step is now [selective alignment](/selective-alignment/).
- **Simple rules.** Counting only unique reads, or splitting each shared read equally, are fast but biased, as the first example shows. Mortazavi and colleagues (2008) gave an early rule that gave the reads of a multi-mapping group to their places in proportion to the unique reads near each place.

## Bounds

- **Concavity.** $\log L$ is a sum of logarithms of linear functions of $\alpha$, so it is concave on the simplex. Every local maximum is a global maximum, and the set of maxima is convex. This is a theorem, stated by Li and colleagues (2010).
- **Uniqueness.** The maximum is unique when the vectors $(P(r \mid t))_r$ for the transcripts $t$ are linearly independent, so that the class probabilities fix $\alpha$. If they are not, as in the ridge example, a whole segment of maxima exists. This is a property of the data and no estimator can avoid it.
- **EM.** Each EM round costs $O(\sum_e |e|)$ time on equivalence classes, and the log-likelihood never decreases. A fixed point of the EM at which every $\alpha_t > 0$ is a global maximum, by concavity. Both are theorems, proved on the [EM page](/em-isoform-quantification/). In practice the EM needs many rounds when transcripts are almost indistinguishable, which is a measurement, not a bound.
- **Statistical error.** Even with a perfect method, the estimate has the sampling error of $N$ reads, which is large for transcripts with few reads and for isoforms that share most of their sequence.

## Reductions

- **To mixture weights.** The problem is the maximum likelihood estimate of the weights of a finite mixture whose components $P(r \mid t)$ are fixed, the classic setting of [expectation maximization](/expectation-maximization/).
- **To Poisson regression.** With counts per exon region, the expected counts are linear in the abundances, and the model becomes a Poisson regression with nonnegative coefficients.
- **From transcript assembly.** When the transcripts are not known, [transcript assembly](/transcript-assembly/) or [de novo assembly](/de-novo-transcriptome-assembly/) gives them first. StringTie and Cufflinks do both steps.

## Applications

- Isoform-level and gene-level expression tables, the input of [differential expression analysis](/differential-expression-analysis/).
- Changes in isoform use between conditions, where gene-level counts stay the same.
- Allele-specific expression, with the two alleles of a gene as two transcripts.
- Expression in species without a genome, against a de novo assembled transcript set.

## References
