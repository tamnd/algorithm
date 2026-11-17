---
tag: C7FP1K
kind: model
slug: interpolated-markov-model
name: Interpolated Markov model
aliases:
- IMM
- Glimmer model
area: biology/gene-finding-and-motifs
level: advanced
summary: A Markov model that mixes contexts of different orders with weights set by how much data supports each, used in prokaryotic gene finding.
history:
  year: 1998
  people: [Steven L. Salzberg, Arthur L. Delcher, Simon Kasif, Owen White]
  note: Salzberg, Delcher, Kasif and White introduced the interpolated Markov model of coding DNA in the Glimmer gene finder in 1998.
prereqs: [markov-chain, periodic-markov-chain-gene-model]
see_also: [deleted-interpolation, katz-backoff, prediction-by-partial-matching, context-tree-weighting, chi-squared-goodness-of-fit-test, n-gram-language-model, orf-finding, gene-prediction]
sources:
  - paper: doi:10.1093/nar/26.2.544
    title: Steven L. Salzberg, Arthur L. Delcher, Simon Kasif and Owen White, Microbial gene identification using interpolated Markov models, Nucleic Acids Research 26(2), 1998
    locator: p. 546 (the recursion for IMM_k with k = 8, the threshold of 400 occurrences, the chi-squared test against the next shorter context) and p. 547 (the formula for lambda, the training on long ORFs, the overlap rule, and Table 1)
  - paper: doi:10.1093/nar/27.23.4636
    title: Arthur L. Delcher, Douglas Harmon, Simon Kasif, Owen White and Steven L. Salzberg, Improved microbial gene identification with GLIMMER, Nucleic Acids Research 27(23), 1999
    locator: pp. 4636 to 4641; the technical improvements of Glimmer 2 and a wider evaluation against published annotations
---

An interpolated Markov model (IMM) predicts each base of a DNA sequence from a mix of Markov chains of orders $0, 1, \ldots, k$. A high order uses a long context and can be more accurate, but many long contexts occur too rarely in the training data to give reliable estimates. An IMM gives each context a weight $\lambda$ that is large when the context occurs often, or when what follows it differs clearly from what the shorter context predicts, and small otherwise; the rest of the weight goes to the IMM of the next lower order. Salzberg, Delcher, Kasif and White (1998) introduced IMMs for finding genes in bacteria with the Glimmer system, with $k = 8$ and one model for each codon position, as in the [three-periodic Markov chain](/periodic-markov-chain-gene-model/). The idea is the same as interpolated smoothing of [n-gram models](/n-gram-language-model/) in speech recognition.

## The machine

**The state.** A position $x$ in a sequence $S$, and the contexts $S_{x,i} = s_{x-i} \cdots s_{x-1}$ of the $i$ bases before it, for $i = 0, 1, \ldots, k$. In a gene model, each of the three codon positions has its own IMM, and the codon position steps with each base, as in the three-periodic chain.

**The counts.** From the training genes, the IMM counts $f(S_{x,i} b)$, the number of occurrences of each string of length 1 to $k + 1$, separately for each codon position of the last base. The fixed-order estimate of order $i$ is

$$P_i(s_x \mid S_{x,i}) = \frac{f(S_{x,i} s_x)}{\sum_{b} f(S_{x,i} b)}.$$

**The rule.** The IMM of order 0 is the base frequency, $\mathrm{IMM}_0 = P_0$. For $i \ge 1$,

$$\mathrm{IMM}_i(s_x) = \lambda_i(S_{x,i}) \, P_i(s_x \mid S_{x,i}) + \big(1 - \lambda_i(S_{x,i})\big) \, \mathrm{IMM}_{i-1}(s_x),$$

and the probability of a sequence is $P(S) = \prod_x \mathrm{IMM}_k(s_x)$. Since each $\mathrm{IMM}_i$ is a convex combination of distributions over the four bases, it is a distribution too.

**The weights in Glimmer.** For a context $w$ of length $i$ with $n_w = \sum_b f(w b)$ occurrences:

- if $n_w \ge 400$, then $\lambda_i(w) = 1$, and the shorter contexts are not used. Salzberg et al. chose 400 because it gives about 95% confidence that the observed frequencies are within 0.05 of the true ones;
- otherwise, compare the four counts $f(w b)$ with the predictions $\mathrm{IMM}_{i-1}(b)$ of the next shorter context by a [chi-squared test](/chi-squared-goodness-of-fit-test/), and let $c$ be the confidence that they are not consistent. Then $\lambda_i(w) = 0$ if $c < 0.5$, and $\lambda_i(w) = \frac{c}{400} n_w$ if $c \ge 0.5$.

So a long context gets weight only if it is frequent, or if it is both fairly frequent and predicts something that its shorter context does not.

**Assumptions.** The same as for the three-periodic chain: the training genes are typical of the genome, there are no frame shifts, and the model sees only the coding content, not the start and stop signals.

## What it counts

The IMM gives a probability to every sequence, so it scores a stretch of DNA under each hypothesis, as a fixed-order chain does. Glimmer builds IMMs for the six reading frames and scores every open reading frame longer than a threshold in all six. An ORF whose score in its own frame is the highest and above a threshold is a candidate gene. When two candidates in different frames overlap by more than a minimum length, Glimmer scores the overlap region alone in the six frames, and removes the candidate whose frame loses there.

**Example.** Fix one codon position and the order $k = 2$. Suppose the context $A$ (order 1) occurs 500 times, followed by A, C, G and T with frequencies 0.5, 0.2, 0.1 and 0.2. Since $500 \ge 400$, $\lambda_1(A) = 1$ and $\mathrm{IMM}_1 = P_1 = (0.5, 0.2, 0.1, 0.2)$. The context $GA$ (order 2) occurs only 4 times, followed by A three times and G once. A fixed order 2 chain would give C and T after GA the probability 0. The IMM compares the counts $(3, 0, 1, 0)$ with the expected counts $4 \cdot \mathrm{IMM}_1 = (2, 0.8, 0.4, 0.8)$:

$$\chi^2 = \frac{1^2}{2} + \frac{0.8^2}{0.8} + \frac{0.6^2}{0.4} + \frac{0.8^2}{0.8} = 0.5 + 0.8 + 0.9 + 0.8 = 3.0.$$

With 3 degrees of freedom, $P(\chi^2_3 \le 3.0) \approx 0.608$, so $c = 0.608 \ge 0.5$ and $\lambda_2(GA) = 0.608 \cdot 4 / 400 \approx 0.0061$. Then

$$\mathrm{IMM}_2(\cdot \mid GA) = 0.0061 \cdot (0.75, 0, 0.25, 0) + 0.9939 \cdot (0.5, 0.2, 0.1, 0.2) \approx (0.5015, 0.1988, 0.1009, 0.1988).$$

Four occurrences move the prediction very little. If $GA$ had occurred 400 times with the same proportions, the IMM would use them as they are.

## Relation to other models

- **[Three-periodic Markov chain](/periodic-markov-chain-gene-model/).** A fixed-order chain is the IMM with $\lambda_i = 1$ at its order and no lower orders. Salzberg et al. note that, with zero weight on all contexts except those of length 5, the IMM is the fifth-order model.
- **[Deleted interpolation](/deleted-interpolation/).** The recursion is the linear interpolation of [Jelinek and Mercer](/jelinek-mercer-smoothing/), which sets the weights by fitting held-out data. Salzberg et al. cite it and tried such methods; Glimmer sets the weights from the counts and a test instead.
- **Back-off models.** [Katz back-off](/katz-backoff/) uses the longest context with enough data and falls back to a shorter one otherwise, in place of a mix. [Prediction by partial matching](/prediction-by-partial-matching/) and [context tree weighting](/context-tree-weighting/) mix contexts of many lengths for compression.
- **Interpolated context models.** Glimmer 2 (Delcher et al. 1999) replaced the IMM with an interpolated context model, a generalization in which the context positions that the model uses are chosen from the training data and need not be the bases just before the predicted one.
- **[Generalized HMM gene finders](/generalized-hmm-gene-finder/).** An IMM can serve as the content model of the coding states of a GHMM, in place of a fixed-order chain.

## Known results in the model

- **A proper distribution.** By induction on $i$, each $\mathrm{IMM}_i(\cdot \mid S_{x,i})$ is a probability distribution over the four bases, since it is a convex combination of two distributions. The product over a sequence is then a probability.
- **Size and data.** A $k$-th order model for DNA needs $4^{k+1}$ probabilities. In a genome of 1.8 million bases, most of the 4096 6-mers occur often enough for a fifth-order model, but a substantial number of 7-mers do not, and the problem is worse for orders 7 and 8. The IMM uses the long contexts only where the data supports them (Salzberg et al. 1998).
- **More genes found.** On the *Haemophilus influenzae* genome with 1717 annotated genes, trained on 1168 ORFs longer than 500 bases with no long overlapping ORF, the IMM found 1680 genes (97.8%) and a fixed fifth-order model found 1574 (91.7%), with the same training and the same overlap rule. The IMM also called 209 genes outside the annotation, against 104 for the fifth-order model (Salzberg et al. 1998, Table 1). On *Helicobacter pylori*, Glimmer found 1548 of the 1590 annotated genes.
- **Self-training.** Long ORFs almost never occur in non-coding DNA, so they make a training set that needs no annotation. Glimmer's results above used such training sets, and further work reports that Glimmer misses less than 1% of the genes that have significant homology to genes in other organisms (Delcher et al. 1999).
- **Cost.** Building the model is one pass of counting over the training genes, plus one test per context. Scoring is $O(k)$ per base, or $O(1)$ if the $\mathrm{IMM}_k$ values are stored for all contexts that occur.

## References
