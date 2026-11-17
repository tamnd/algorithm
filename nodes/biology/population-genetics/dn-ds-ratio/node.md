---
tag: XT0SNP
kind: definition
slug: dn-ds-ratio
name: dN/dS ratio
aliases:
- Ka/Ks ratio
- omega ratio
area: biology/population-genetics
level: core
summary: The rate of nonsynonymous substitutions per nonsynonymous site over the synonymous rate. A value above 1 suggests positive selection.
history:
  year: 1986
  people: [Masatoshi Nei, Takashi Gojobori]
  note: Counting methods for synonymous and nonsynonymous rates came in the early 1980s; Nei and Gojobori gave the simple form in 1986, and Goldman and Yang and Muse and Gaut made omega a model parameter in 1994.
prereqs: [kimura-fixation-probability, jukes-cantor-model]
see_also: [nei-gojobori-method, codon-substitution-model, mcdonald-kreitman-test, substitution-model, effective-population-size, likelihood-ratio-test, codon-adaptation-index]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040410
    title: Masatoshi Nei and Takashi Gojobori, Simple methods for estimating the numbers of synonymous and nonsynonymous nucleotide substitutions, Molecular Biology and Evolution 3(5), 1986
    locator: pp. 418-426 (synonymous and nonsynonymous sites, and the numbers of substitutions per site of each kind)
  - paper: doi:10.1093/oxfordjournals.molbev.a040153
    title: Nick Goldman and Ziheng Yang, A codon-based model of nucleotide substitution for protein-coding DNA sequences, Molecular Biology and Evolution 11(5), 1994
    locator: pp. 725-736 (the codon model with the nonsynonymous to synonymous rate ratio as a parameter)
  - paper: doi:10.1093/genetics/47.6.713
    title: Motoo Kimura, On the probability of fixation of mutant genes in a population, Genetics 47(6), 1962
    locator: pp. 713-719 (the fixation probability of a new mutant with selection)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 2 (synonymous and nonsynonymous rates and their ratio)
---

The dN/dS ratio $\omega$ of a protein-coding gene is the number of nonsynonymous substitutions per nonsynonymous site, $d_N$, divided by the number of synonymous substitutions per synonymous site, $d_S$, between two sequences or along a branch of a tree. A synonymous change keeps the amino acid and is close to neutral; a nonsynonymous change replaces it, and selection on the protein acts on it. So $\omega$ measures the rate at which amino acid changes are fixed, relative to the neutral rate. A value below 1 is the sign of purifying selection, a value near 1 of neutral evolution, and a value above 1 of positive selection, which favours changes. Counting methods such as the [Nei-Gojobori method](/nei-gojobori-method/) and likelihood with a [codon substitution model](/codon-substitution-model/) estimate it.

## Definition

**Sites.** For a sense codon $x$, let $s(x)$ be the number of its synonymous sites: the sum over its three positions of the fraction of the three possible base changes at that position that keep the amino acid. The other $n(x) = 3 - s(x)$ sites are nonsynonymous. The synonymous and nonsynonymous site counts $S$ and $N$ of a gene are the sums over its codons, so $S + N = 3c$ for a gene of $c$ codons. In a codon model, the sites are defined in the same spirit by the rates of the model, weighted by the codon frequencies and the transition bias.

**Rates.** $d_S$ is the expected number of synonymous substitutions between the two sequences, divided by $S$, and $d_N$ is the expected number of nonsynonymous substitutions divided by $N$. Both count substitutions, not observed differences, so they include changes hidden by later changes at the same site.

**The ratio.**

$$\omega = \frac{d_N}{d_S}.$$

It is defined when $d_S > 0$. In a codon model, $\omega$ is the ratio of the rate of a nonsynonymous change to that of a synonymous change between codons that differ at one position, with the other factors of the rate the same. Then $d_N / d_S = \omega$ holds exactly for the expected values under the model.

**Population genetic meaning.** If synonymous changes are neutral and all nonsynonymous mutations have the same scaled selection coefficient $\gamma = 4Ns$ in a diploid population of [effective size](/effective-population-size/) $N$, the rate of substitution is the mutation rate times $2N$ times the [fixation probability](/kimura-fixation-probability/). For a new mutant with small $s$, relative to a neutral one, this gives

$$\omega \approx \frac{\gamma}{1 - e^{-\gamma}},$$

which is $1$ at $\gamma = 0$, below 1 for $\gamma < 0$ and above 1 for $\gamma > 0$. Over a gene, $\omega$ is the mean of this factor over all nonsynonymous mutations.

## Examples and non-examples

- **Neutral changes.** With $\gamma = 0$, $\omega = 1$: the protein changes as fast as the synonymous sites.
- **Weak purifying selection.** With $\gamma = -2$, $\omega \approx 2/(e^2 - 1) = 0.313$. With $\gamma = -10$, $\omega \approx 10/(e^{10} - 1) = 0.00045$: such changes almost never fix.
- **Weak positive selection.** With $\gamma = 2$, $\omega \approx 2/(1 - e^{-2}) = 2.313$.
- **A mixed gene.** If 90% of nonsynonymous mutations have $\gamma = -10$ and 10% are neutral, $\omega \approx 0.9 \cdot 0.00045 + 0.1 \cdot 1 = 0.10$. Most genes have $\omega$ well below 1, because most sites are constrained, even when a few sites are under positive selection.
- **A worked estimate.** In the example of the [Nei-Gojobori method](/nei-gojobori-method/), ten codons give $d_N = 0.1105$ and $d_S = 1.3010$, so $\omega = 0.085$.
- **Not the ratio of raw counts.** The ratio $N_d / S_d$ of nonsynonymous to synonymous differences is not $\omega$. With the standard code, the mean of $s(x)$ over the 61 sense codons is $134/183 = 0.732$, so only about a quarter of the sites are synonymous, and a neutral gene has about three times as many nonsynonymous as synonymous changes, with $\omega$ still near 1.
- **Not the same as the ratio within a species.** The ratio $p_N / p_S$ of polymorphisms inside one population has a different relation to selection, because weakly deleterious variants are still present as polymorphisms but rarely fix. The [McDonald-Kreitman test](/mcdonald-kreitman-test/) uses that difference.
- **Not the codon adaptation index.** The [codon adaptation index](/codon-adaptation-index/) measures which synonymous codons a gene uses, not how fast its amino acids change.

## Related definitions

- **Synonymous and nonsynonymous sites.** The site counts $S$ and $N$ of the definition. Under a model with transition bias, more third-position changes are transitions and many are synonymous, so methods that ignore the bias give too few synonymous sites.
- **Branch and site versions.** In a codon model on a tree, $\omega$ can differ between branches (branch models), between sites (site models), or both (branch-site models). A [likelihood ratio test](/likelihood-ratio-test/) between nested versions tests for sites with $\omega > 1$.
- **The neutrality index and the fraction of adaptive substitutions.** The McDonald-Kreitman test combines $d_N / d_S$ with $p_N / p_S$; the fraction $\alpha = 1 - (D_s P_n)/(D_n P_s)$ estimates the share of amino acid substitutions that were adaptive.
- **Ka and Ks.** Another notation for $d_N$ and $d_S$, used in some programs and papers.

## References
