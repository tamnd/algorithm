---
tag: QCTP6D
kind: algorithm
slug: codon-adaptation-index
name: Codon adaptation index
aliases:
- CAI
area: biology/gene-finding-and-motifs
level: core
summary: Give each codon a weight from its usage in highly expressed genes, then score a gene by the geometric mean of the weights of its codons. The score is in (0, 1].
model: real-ram
complexity:
  vars: {M: the number of codons in the reference set, N: the number of codons in the gene}
  time: {worst: Θ(M + N), average: Θ(M + N), best: Θ(M + N)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [open-reading-frame]
see_also: [orf-finding, gene-prediction, codon-substitution-model, dn-ds-ratio, periodic-markov-chain-gene-model, log-sum-exp-trick, shannon-entropy]
sources:
  - paper: doi:10.1093/nar/15.3.1281
    title: Paul M. Sharp and Wen-Hsiung Li, The codon adaptation index, a measure of directional synonymous codon usage bias, and its potential applications, Nucleic Acids Research 15(3), 1987
    locator: pp. 1281 to 1295; equations [1] to [8], the count 0.5 for codons absent from the reference set, Table 1 (p. 1284) with RSCU and w for E. coli and yeast, and Table 2 with CAI values of genes
  - paper: doi:10.1016/0378-1119(90)90491-9
    title: Frank Wright, The 'effective number of codons' used in a gene, Gene 87(1), 1990
    locator: pp. 23 to 29, the definition of the effective number of codons, from 20 to 61
  - paper: doi:10.1093/nar/gkh834
    title: Mario dos Reis, Renos Savva and Lorenz Wernisch, Solving the riddle of codon usage preferences, a test for translational selection, Nucleic Acids Research 32(17), 2004
    locator: pp. 5036 to 5044, the tRNA adaptation index, a geometric mean of relative adaptiveness values computed from tRNA gene copy numbers
---

The codon adaptation index (CAI) measures how strongly a gene uses the codons that a set of highly expressed genes prefers. Most amino acids are coded by two to six synonymous codons, and in many organisms the genes that are expressed at high levels use some of these codons much more than others. Sharp and Li (1987) give each codon a weight $w$ between 0 and 1: its count in a reference set of highly expressed genes, divided by the count of the most used codon of the same amino acid. The CAI of a gene is the geometric mean of the weights of its codons. A value near 1 means the gene uses the preferred codons almost everywhere, and a low value means it does not. The index predicts expression level from sequence alone, helps to choose codons for a gene that is to be expressed in another host, and is one of the codon statistics that separate real genes from [chance ORFs](/open-reading-frame/).

## In plain words

Take a set of genes that the cell makes in large amounts. For each amino acid, count how often each of its codons occurs there. The codon used most gets the weight 1, and every other codon gets its count divided by that count, so a codon used half as often gets 1/2. To score a new gene, look up the weight of each of its codons and take the geometric mean: multiply the weights and take the L-th root, where L is the number of codons. In practice, add the logarithms and divide by L. A gene made only of preferred codons scores 1. Skip codons that carry no choice, such as ATG for methionine, and the stop codons.

## The problem

**Input.** A reference set of protein-coding sequences, read in frame from the start codon, with $M$ codons in total; a gene with $N$ codons in the same frame; and a genetic code, by default NCBI table 1.

**Output.** A table of weights $w_c$, one for each sense codon $c$, and the index $\mathrm{CAI} \in (0, 1]$ of the gene.

Let $X_c$ be the number of times codon $c$ occurs in the reference set. For a codon of amino acid $a$, the relative synonymous codon usage is $\mathrm{RSCU}_c = X_c / (\frac{1}{n_a} \sum_{d} X_d)$, where the sum is over the $n_a$ codons $d$ of $a$. It is 1 when all codons of $a$ are used equally. The relative adaptiveness is $w_c = \mathrm{RSCU}_c / \mathrm{RSCU}_{\max} = X_c / X_{\max}$, where $X_{\max}$ is the largest count among the codons of $a$. Let $c_1, \ldots, c_L$ be the codons of the gene that belong to amino acids with at least two codons; stop codons are left out, and so are ATG and TGG in the standard code. Then

$$\mathrm{CAI} = \Big(\prod_{k=1}^{L} w_{c_k}\Big)^{1/L} = \exp\Big(\frac{1}{L} \sum_{k=1}^{L} \ln w_{c_k}\Big).$$

A codon that the reference set never uses would get $w = 0$ and make the index of any gene that uses it 0. Sharp and Li give such a codon the count $0.5$ instead.

## The algorithm

```pseudo id=main
CAI-WEIGHTS(reference)
L1  X[c] ← the number of times sense codon c occurs in the reference genes, in frame
L2  replace every X[c] = 0 by 1/2
L3  for each amino acid a: Xmax[a] ← the largest X[c] over the codons c of a
L4  for each sense codon c of amino acid a: w[c] ← X[c] / Xmax[a]

CAI(g, w)
L5  S ← 0; L ← 0
L6  for each codon c of g, in frame, do
L7      if c is a sense codon of an amino acid with two or more codons then
L8          S ← S + ln w[c]; L ← L + 1
L9  return exp(S / L)
```

The weights are computed once for an organism and then used for any number of genes. Line L2 comes before line L3, so that an amino acid that never occurs in the reference set gets weight 1 for all its codons instead of a division by zero. Line L8 works in log space: the product of a few hundred weights below 1 underflows a double, but the sum of their logarithms does not.

## Example

Take a reference set of two short genes, written as codons:

- GCT GCT GCT GCT AAA AAA GCC
- GCT GCT GCC GCC GCA AAA AAA AAG

Line L1 counts, for alanine, GCT 6, GCC 3, GCA 1 and GCG 0, and for lysine, AAA 4 and AAG 1. Line L2 sets the count of GCG to 1/2. The weights are:

| codon | amino acid | count $X$ | $X_{\max}$ | $w$ |
|---|---|---|---|---|
| GCT | Ala | 6 | 6 | 1 |
| GCC | Ala | 3 | 6 | 1/2 |
| GCA | Ala | 1 | 6 | 1/6 |
| GCG | Ala | 1/2 | 6 | 1/12 |
| AAA | Lys | 4 | 4 | 1 |
| AAG | Lys | 1 | 4 | 1/4 |

All other amino acids are absent, so all their codons have the count 1/2 and the weight 1. Now score the gene ATG GCC AAG GCT AAA GCG TGG TAA. Line L7 skips ATG and TGG, which have no synonyms, and the stop TAA. The other $L = 5$ codons have the weights $1/2, 1/4, 1, 1, 1/12$, whose product is $1/96$. So

$$\mathrm{CAI} = 96^{-1/5} = \exp(-\ln 96 / 5) \approx \exp(-0.91287) \approx 0.40137.$$

The RSCU form gives the same number. For alanine the mean count is $(6 + 3 + 1 + 0.5)/4 = 2.625$, so $\mathrm{RSCU}_{\mathrm{GCC}} = 3/2.625 \approx 1.143$ and the largest RSCU is $6/2.625 \approx 2.286$, and their ratio is again $1/2$.

Sharp and Li give a real case. In their Table 1 for *E. coli*, the first five codons of the ribosomal protein gene rpsU after the start, CCG GTA ATT AAA GTA, have the weights 1.00, 0.495, 0.185, 1.000 and 0.495. The geometric mean of these five is about 0.5386. Over all 70 codons of the gene, without the start codon, the CAI is 0.726. In their Table 2 the ribosomal protein genes of *E. coli* have CAI values from 0.467 to 0.813, the highest value is 0.849 for lpp, and the lowest is 0.218 for hsdS.

## Correctness

After lines L1 and L2, every count $X_c$ is positive. The mean count $\frac{1}{n_a} \sum_d X_d$ is the same for all codons of one amino acid, so it cancels in $\mathrm{RSCU}_c / \mathrm{RSCU}_{\max}$, and line L4 computes $w_c$ as defined, with $0 < w_c \le 1$. The loop of lines L6 to L8 keeps $S$ equal to the sum of $\ln w_c$ over the counted codons seen so far, and $L$ equal to their number. So line L9 returns $\exp(\frac{1}{L} \sum \ln w_{c_k}) = (\prod w_{c_k})^{1/L}$, which is also $\mathrm{CAI}_{\mathrm{obs}} / \mathrm{CAI}_{\max}$, the ratio of the geometric means of the observed RSCU values and of their largest possible values. Every factor is in $(0, 1]$, so the CAI is in $(0, 1]$, and it is 1 exactly when every counted codon has weight 1. The full proof is in the proofs folder.

## Complexity

- **Time.** Line L1 reads each of the $M$ reference codons once, with one table look-up each, so it takes $\Theta(M)$ time. Lines L2 to L4 touch the 61 sense codons, a constant. Lines L6 to L8 read the $N$ codons of the gene once, with a look-up, a logarithm and an addition each, so the score takes $\Theta(N)$ time. The weights are computed once, and then each further gene costs $\Theta(N)$.
- **Space.** Two tables of 64 entries, so $\Theta(1)$ extra space beyond the input.
- **Faster scoring.** The logarithms $\ln w_c$ can be stored once in the table. The score of every ORF of a genome then comes from a prefix sum of $\ln w$ per frame, one subtraction per ORF.

## Properties

- **Range.** $0 < \mathrm{CAI} \le 1$. It is 1 only for a gene that uses an optimal codon at every counted position.
- **Depends only on the codon counts.** The index is $\exp(\frac{1}{L} \sum_c f_c \ln w_c)$, where $f_c$ is the count of codon $c$ in the gene. This is equation [8] of Sharp and Li, a sum over the codons of 18 amino acids. The order of the codons does not matter.
- **Normalized for amino acid composition.** Each weight compares a codon only with its synonyms, so a gene rich in an amino acid with a strongly preferred codon is not scored higher for that reason alone. Sharp and Li write that gene length has no intrinsic effect on CAI, but that the values of short genes may vary more.
- **Relative to the reference set.** The weights come from one reference set of one organism. A CAI computed with the weights of *E. coli* says how well a gene fits *E. coli*, not how well it fits its own genome.
- **Deterministic.** There is no randomness and no fitting step: the weights are ratios of counts.

## Variants and improvements

- **RSCU.** The relative synonymous codon usage of each codon, without the geometric mean, is the table that Sharp and Li compute first. It is a descriptive summary of codon usage in a set of genes.
- **Effective number of codons.** Wright (1990) measures how far the codon usage of a gene is from equal use of synonyms, from 20 (one codon per amino acid) to 61 (all synonyms used equally). It needs no reference set, so it measures bias of any cause, not adaptation to a set of highly expressed genes.
- **tRNA adaptation index.** dos Reis, Savva and Wernisch (2004) compute the weights from the copy numbers of the tRNA genes of the genome and the wobble rules, and then take the same geometric mean. It needs no list of highly expressed genes.
- **Reference sets chosen from the genome.** When no list of highly expressed genes is known, a method can start from all genes, compute weights, take the genes with the highest CAI as a new reference set, and repeat until the set does not change.
- **Codon models for gene finding.** A gene finder replaces the weights by the full probability of each codon in coding DNA, as in the [three-periodic Markov chain](/periodic-markov-chain-gene-model/), and compares it with a model of non-coding DNA. CAI is the simpler score for one gene; the Markov models decide whether a region codes at all.
- **Codon optimization.** To express a gene in another host, choose for each amino acid the codon with weight 1 in the host. This gives CAI 1. Many design tools also keep some variety of codons and check other features of the sequence, so a CAI of 1 is not the only goal.

## When to use it

Use the CAI to compare the expected expression level of the genes of one organism, to find highly expressed genes in a new genome, to check a gene designed for expression in a host, and to find genes that came recently from another genome, whose codon usage does not fit. Compute the weights with a reference set of the same organism, such as the ribosomal protein genes and the elongation factors. Do not compare CAI values computed with different reference sets, and do not use CAI as the only evidence that an ORF is a gene; for that, use [gene prediction](/gene-prediction/) models.

## Pitfalls

- **The arithmetic mean.** The index is a geometric mean. An arithmetic mean of the weights gives a different and larger number.
- **Zero weights.** Without the count 1/2 for unused codons, a single rare codon makes the index 0. Some tools use another small count, so their values can differ slightly.
- **Underflow.** The direct product of the weights of a long gene underflows to 0 in floating point. Add logarithms, as in line L8.
- **Codons with no choice.** ATG and TGG, and the stop codon, must not count, or a gene with many methionines scores higher. In other genetic codes the set of single-codon amino acids changes; vertebrate mitochondria code TGA as tryptophan.
- **Initiation codon.** A bacterial gene that starts with GTG or TTG would count that codon as valine or leucine. Remove the start codon before scoring, as Sharp and Li do.
- **Frame and length.** The gene must be in frame from its first codon, and its length should be a multiple of 3. A frameshift turns the rest of the gene into nonsense codons with low weights.
- **Mutation bias.** In a genome with a strong GC or AT bias, all genes share the same codon bias for reasons that have nothing to do with expression. The CAI then mixes the two effects.

## Implementations

## History

Sharp and Li (1987) defined the index and gave the reference sets and the weights for *E. coli* (27 very highly expressed genes, among them 17 ribosomal protein genes, the elongation factors, recA and dnaK) and for yeast (24 genes). They showed that CAI values are correlated with the expression levels of genes in both organisms. Wright (1990) added the effective number of codons, a measure that needs no reference set, and dos Reis, Savva and Wernisch (2004) took the same geometric mean over weights derived from tRNA gene copy numbers.

## References
