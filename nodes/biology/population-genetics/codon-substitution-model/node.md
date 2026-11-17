---
tag: 0C36AP
kind: model
slug: codon-substitution-model
name: Codon substitution model
aliases:
- Goldman-Yang model
- Muse-Gaut model
area: biology/population-genetics
level: advanced
summary: A Markov model on the 61 sense codons with transition, codon frequency and omega parameters, used to estimate dN/dS by likelihood.
history:
  year: 1994
  people: [Nick Goldman, Ziheng Yang, Spencer V. Muse, Brandon S. Gaut]
  note: Goldman and Yang and, in the same issue, Muse and Gaut published in 1994 the first Markov models of substitution between codons, with separate rates for synonymous and nonsynonymous changes.
prereqs: [substitution-model, dn-ds-ratio, matrix-exponential]
see_also: [nei-gojobori-method, hky-model, gtr-model, phylogenetic-likelihood, felsenstein-pruning, likelihood-ratio-test, rate-heterogeneity, mcdonald-kreitman-test]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040153
    title: Nick Goldman and Ziheng Yang, A codon-based model of nucleotide substitution for protein-coding DNA sequences, Molecular Biology and Evolution 11(5), 1994
    locator: pp. 725-736 (the Markov model on the 61 sense codons with codon frequencies, the transition to transversion ratio and a nonsynonymous rate factor, fitted by likelihood)
  - paper: doi:10.1093/oxfordjournals.molbev.a040152
    title: Spencer V. Muse and Brandon S. Gaut, A likelihood approach for comparing synonymous and nonsynonymous nucleotide substitution rates, with application to the chloroplast genome, Molecular Biology and Evolution 11(5), 1994
    locator: pp. 715-724 (the codon model with nucleotide frequencies and separate synonymous and nonsynonymous rates)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 2 (codon substitution models, codon frequency models, and the definition of dN and dS under a codon model)
---

A codon substitution model is a continuous-time Markov chain on the 61 sense codons of the genetic code. It describes how a codon in a protein-coding gene changes along a branch of a tree, one base at a time, with a rate that depends on whether the change is a transition or a transversion, on how common the new codon is, and on whether the change keeps the amino acid. The last factor, $\omega$, is the [dN/dS ratio](/dn-ds-ratio/), so fitting the model by maximum likelihood estimates $\omega$ and gives tests of selection. Goldman and Yang, and Muse and Gaut, proposed the first such models in 1994. The model extends the nucleotide [substitution models](/substitution-model/) to the unit on which selection on proteins acts.

## The machine

**The state.** One of the 61 sense codons of the standard code; the three stop codons are left out, because a working gene does not have them inside its reading frame. A gene of $c$ codons is $c$ independent copies of the chain, one per codon, along the same tree.

**The parameters.** The transition to transversion rate ratio $\kappa$, the nonsynonymous to synonymous rate ratio $\omega$, and the equilibrium codon frequencies $\pi_1, \ldots, \pi_{61}$. Branch lengths $t$ are in expected nucleotide substitutions per codon.

**The rates.** For codons $i \ne j$, the rate in the widely used form of the model of Goldman and Yang is

$$q_{ij} = \begin{cases} 0 & \text{if } i \text{ and } j \text{ differ at two or three positions,} \\ \pi_j & \text{synonymous transversion,} \\ \kappa \pi_j & \text{synonymous transition,} \\ \omega \pi_j & \text{nonsynonymous transversion,} \\ \omega \kappa \pi_j & \text{nonsynonymous transition.} \end{cases}$$

The diagonal is $q_{ii} = -\sum_{j \ne i} q_{ij}$. The matrix is scaled by a constant so that $-\sum_i \pi_i q_{ii} = 1$, one expected substitution per codon per unit of $t$. The original 1994 model also had a factor for the physicochemical distance between the two amino acids; later work dropped it and kept a single $\omega$.

**The model of Muse and Gaut.** It uses the frequency of the target nucleotide at the changed position instead of the frequency of the target codon, and writes the synonymous and nonsynonymous rates as $\alpha$ and $\beta$, so that $\omega = \beta/\alpha$. For a change from codon $i$ to codon $j$ at position $k$ with new base $b$, $q_{ij} = \alpha \pi_b^{(k)}$ or $\beta \pi_b^{(k)}$. Later versions multiply these rates by those of a nucleotide model, such as $\kappa$ for transitions.

**Codon frequencies.** Common choices: all equal to $1/61$; the products of the four base frequencies over the three positions (F1x4) or of position-specific base frequencies (F3x4), normalized over the sense codons; or 61 free frequencies (F61).

**Transition probabilities and the likelihood.** Over a branch of length $t$, $P(t) = e^{Qt}$ by the [matrix exponential](/matrix-exponential/), usually through the eigendecomposition of the symmetrized matrix. The likelihood of an alignment on a tree is the product over codons of the [phylogenetic likelihood](/phylogenetic-likelihood/) of each column, computed by [Felsenstein's pruning](/felsenstein-pruning/) with $61 \times 61$ matrices.

**A small example.** With equal codon frequencies, $\kappa = 2$ and $\omega = 0.5$, the unscaled rates out of TTA (Leu) are: to CTA (Leu, transition, synonymous) $\kappa = 2$; to TTG (Leu, transition, synonymous) $2$; to ATA (Ile) and GTA (Val), transversions, $\omega = 0.5$ each; to TCA (Ser, transition) $\omega\kappa = 1$; to TTT and TTC (Phe), transversions, $0.5$ each; to TAA and TGA, stop codons, $0$. All rates carry the common factor $1/61$. The total rate is 7 times that factor, and $4/7$ of it is synonymous.

## What it counts

- **Substitutions per codon.** The branch length $t$ is the expected number of substitutions per codon. Under the model, the expected numbers of synonymous and nonsynonymous substitutions on a branch are $t \rho_S$ and $t \rho_N$, where $\rho_S = \sum_i \pi_i \sum_{j \text{ syn}} q_{ij}$ and $\rho_N = 1 - \rho_S$ for the scaled matrix.
- **Synonymous and nonsynonymous sites.** The sites are defined from the same model with $\omega = 1$: the synonymous sites per codon are $3 \rho_S^{(1)}$ and the nonsynonymous sites are $3(1 - \rho_S^{(1)})$, where $\rho_S^{(1)}$ is $\rho_S$ at $\omega = 1$. With these sites, $d_S$ and $d_N$ are the substitutions of each kind per site of that kind.
- **The likelihood of an alignment**, as a function of $\kappa$, $\omega$, the frequencies and the branch lengths.

## Relation to other models

- **Nucleotide models.** The [HKY model](/hky-model/) is the nucleotide model with transition bias and base frequencies; a codon model with $\omega = 1$ and F1x4 frequencies is close to HKY applied to the three positions jointly, but it still forbids changes to stop codons. [GTR](/gtr-model/) rates can replace the single $\kappa$.
- **Counting methods.** The [Nei-Gojobori method](/nei-gojobori-method/) is the counting analogue with $\kappa = 1$ and equal weights for all pathways. A codon model replaces the pathway average by the full matrix exponential, which accounts for multiple changes in the same codon.
- **Amino acid models.** Grouping the 61 codons by amino acid gives a chain on 20 amino acids only approximately, because the process on codons is not lumpable in general.
- **Variation of omega.** Site models let $\omega$ vary among codons as a mixture of classes or a distribution, branch models let it vary among branches, and branch-site models do both. A [likelihood ratio test](/likelihood-ratio-test/) of a model with a class with $\omega > 1$ against one without tests for positive selection at some sites. [Rate heterogeneity](/rate-heterogeneity/) among codons in the overall rate is a related extension.
- **Population genetics.** For a site with scaled selection coefficient $\gamma$, $\omega$ is the ratio of the fixation rates of nonsynonymous and synonymous mutations; mutation-selection codon models make the codon frequencies and the rates depend on fitnesses of the codons.

## Known results in the model

**Reversibility.** For the rates of the model of Goldman and Yang, $\pi_i q_{ij} = \pi_j q_{ji}$, because $q_{ij}/\pi_j$ depends only on the pair, through the type of change. So the chain is reversible with stationary distribution $\pi$, $Q$ is similar to a symmetric matrix, its eigenvalues are real, and the likelihood does not depend on the position of the root.

**dN/dS equals omega.** With sites defined at $\omega = 1$ as above, $d_N / d_S = \omega$ exactly for every $\kappa$ and $\pi$.

*Proof.* Write the unscaled rates as the sum of a synonymous part with total flow $R_S$ and a nonsynonymous part $\omega R_N$, where $R_S$ and $R_N$ do not depend on $\omega$. After scaling, the share of the synonymous flow is $\rho_S = R_S/(R_S + \omega R_N)$ and that of the nonsynonymous flow is $\rho_N = \omega R_N/(R_S + \omega R_N)$. The sites per codon are $3R_S/(R_S + R_N)$ and $3R_N/(R_S + R_N)$. So $d_S = t\rho_S (R_S + R_N)/(3R_S)$ and $d_N = t\rho_N (R_S + R_N)/(3R_N)$, and their ratio is $\omega$. $\square$

**Sites in the standard code.** The 61 sense codons have $549$ single-base changes; $23$ of them lead to a stop codon and $134$ are synonymous. With equal frequencies and $\kappa = 1$, the synonymous share at $\omega = 1$ is $134/526 = 0.2548$, so there are $0.764$ synonymous sites per codon. The Nei-Gojobori method gives $0.732$, because it counts changes to stop codons as nonsynonymous sites. With $\kappa = 2$ the synonymous sites rise to $0.835$ per codon, and with $\kappa = 5$ to $0.926$, because many third-position transitions are synonymous.

**Two sequences.** With two sequences the tree has one branch, and the model gives estimates of $t$, $\kappa$ and $\omega$ for the pair by likelihood, and from them $d_N$ and $d_S$. This is the likelihood counterpart of the counting methods.

**Saturation.** As $t \to \infty$, $P(t)$ tends to the matrix with every row equal to $\pi$, and the information about $\omega$ is lost; synonymous sites saturate first.

## References
