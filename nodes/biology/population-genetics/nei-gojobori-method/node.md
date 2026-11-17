---
tag: 10S5MW
kind: algorithm
slug: nei-gojobori-method
name: Nei-Gojobori method
aliases:
- Nei-Gojobori counting method
area: biology/population-genetics
level: core
summary: Estimate dN and dS by counting synonymous and nonsynonymous sites and differences between two coding sequences, with a Jukes-Cantor correction.
model: real-ram
complexity:
  vars: {c: the number of codons}
  time: {worst: Θ(c), average: Θ(c), best: Θ(c)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1986
  people: [Masatoshi Nei, Takashi Gojobori]
  note: Nei and Gojobori gave in 1986 a simple counting method for the numbers of synonymous and nonsynonymous substitutions between two coding sequences.
prereqs: [dn-ds-ratio, jukes-cantor-model]
see_also: [codon-substitution-model, mcdonald-kreitman-test, kimura-two-parameter-model, substitution-model, codon-adaptation-index, nucleotide-diversity]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a040410
    title: Masatoshi Nei and Takashi Gojobori, Simple methods for estimating the numbers of synonymous and nonsynonymous nucleotide substitutions, Molecular Biology and Evolution 3(5), 1986
    locator: pp. 418-426 (the counting of synonymous and nonsynonymous sites, the pathways for codons with two or three differences, and the Jukes-Cantor correction)
  - book: isbn:9780199602612
    title: Ziheng Yang, Molecular Evolution, A Statistical Approach, Oxford University Press, 2014
    locator: Chapter 2 (counting methods and likelihood methods for the estimation of dS and dN)
---

The Nei-Gojobori method estimates, for two aligned protein-coding sequences, the number of synonymous substitutions per synonymous site $d_S$ and the number of nonsynonymous substitutions per nonsynonymous site $d_N$. A synonymous change keeps the amino acid and a nonsynonymous change replaces it, so their [ratio](/dn-ds-ratio/) $\omega = d_N / d_S$ measures how strongly selection acts on the protein. The method counts sites and differences codon by codon with the genetic code, divides them, and corrects the two proportions for multiple hits with the [Jukes-Cantor](/jukes-cantor-model/) formula. Nei and Gojobori published it in 1986, and it is still the default counting method in many programs.

## In plain words

Not every base of a gene can change the protein. At the third base of a codon for alanine, any change still gives alanine; at the middle base of almost any codon, every change gives another amino acid. So the number of synonymous differences must be divided by the number of "synonymous places", not by the length.

The method gives each base of each codon a share of synonymous and nonsynonymous: if one of the three possible changes at a base keeps the amino acid, that base counts as $1/3$ synonymous and $2/3$ nonsynonymous. Adding up gives the two kinds of sites. Then it counts the differences between the two sequences of each kind. When two codons differ at more than one base, it averages over all orders of the changes. Last, it divides differences by sites and corrects for changes that hit a base twice.

## The problem

**Input.** Two aligned coding sequences $X$ and $Y$ in the same reading frame, of $c$ codons each, with no stop codon. A genetic code, here the standard code of NCBI table 1.

**Output.** The numbers of synonymous and nonsynonymous sites $S$ and $N$, of differences $S_d$ and $N_d$, the proportions $p_S = S_d / S$ and $p_N = N_d / N$, and the distances

$$d_S = -\tfrac{3}{4} \ln\left(1 - \tfrac{4}{3} p_S\right), \qquad d_N = -\tfrac{3}{4} \ln\left(1 - \tfrac{4}{3} p_N\right).$$

**Sites of a codon.** For a sense codon $x$ and a position $i$, let $f_i(x)$ be the fraction of the three other bases at $i$ that give a codon for the same amino acid. Then $s(x) = f_1(x) + f_2(x) + f_3(x)$ and $n(x) = 3 - s(x)$. A change to a stop codon counts as nonsynonymous. For the pair, $S = \sum (s(x) + s(y))/2$ over the codon pairs and $N = 3c - S$.

**Differences of a codon pair.** If $x$ and $y$ differ at one position, the difference is synonymous when they code the same amino acid and nonsynonymous otherwise. If they differ at $k = 2$ or $3$ positions, there are $k!$ orders of the single changes, called pathways. Each step of a pathway is synonymous or not, and $s_d$ and $n_d$ are the averages of the counts over the pathways, all with the same weight.

## The algorithm

```pseudo id=main
NEI-GOJOBORI(X, Y)
L1  S ← 0; S_d ← 0; N_d ← 0; c ← 0
L2  for each pair of codons (x, y) at the same place in X and Y do
L3      S ← S + (s(x) + s(y)) / 2
L4      (s_d, n_d) ← the mean synonymous and nonsynonymous steps over the pathways from x to y
L5      S_d ← S_d + s_d; N_d ← N_d + n_d; c ← c + 1
L6  N ← 3c − S; p_S ← S_d / S; p_N ← N_d / N
L7  d_S ← −(3/4) ln(1 − 4 p_S / 3); d_N ← −(3/4) ln(1 − 4 p_N / 3)
L8  return d_S, d_N and d_N / d_S
```

The values $s(x)$ for the 61 sense codons and $(s_d, n_d)$ for the $61^2$ pairs depend only on the code, so a program can compute them once. The implementation uses exact fractions for sites and differences.

**Pathways through stop codons.** A pathway may pass through a stop codon, which would end the protein. The 1986 paper does not discuss this case. Programs commonly leave such pathways out, and the implementation does the same by default. For the standard code, every pair of sense codons has at least one pathway without a stop. Codons with a gap or an unknown base in either sequence are left out.

## Example

Take ten codons:

| codon | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $X$ | ATG | GCT | TTA | CCT | GAA | AAA | GGG | TGG | TTT | CAT |
| $Y$ | ATG | GCC | CTA | CCT | GAT | AAA | GGA | TGG | GTA | CAT |
| $s(x)$ | 0 | 1 | 2/3 | 1 | 1/3 | 1/3 | 1 | 0 | 1/3 | 1/3 |
| $s(y)$ | 0 | 1 | 4/3 | 1 | 1/3 | 1/3 | 1 | 0 | 1 | 1/3 |

Two values show the rule. For TTA (Leu), TTG is Leu, so $f_3 = 1/3$; CTA is Leu, so $f_1 = 1/3$; no change at the middle base keeps Leu. So $s = 2/3$. For CTA (Leu), all three changes at the third base keep Leu and TTA does at the first base, so $s = 4/3$.

So $S = (5 + 19/3)/2 = 17/3 = 5.667$ and $N = 30 - 17/3 = 73/3 = 24.333$.

The differences: codons 2 (Ala to Ala), 3 (Leu to Leu) and 7 (Gly to Gly) are synonymous, and codon 5 (Glu to Asp) is nonsynonymous. Codon 9, TTT (Phe) to GTA (Val), differs at positions 1 and 3. The pathway TTT, GTT, GTA has one nonsynonymous step (Phe to Val) and one synonymous step (Val to Val). The pathway TTT, TTA, GTA has two nonsynonymous steps (Phe to Leu, Leu to Val). So $s_d = 1/2$ and $n_d = 3/2$. In total, $S_d = 3.5$ and $N_d = 2.5$.

Then $p_S = 3.5 / 5.667 = 0.6176$ and $p_N = 2.5 / 24.333 = 0.1027$, so $d_S = -0.75 \ln(1 - 0.8235) = 1.3010$ and $d_N = 0.1105$, and $\omega = 0.085$. The protein changes much more slowly than the synonymous sites, which is the usual sign of purifying selection. With only ten codons, $p_S$ is near the limit $3/4$ where the correction fails, and the estimate has a large error.

## Correctness

Line L3 adds the mean of the site counts of the two codons, as Nei and Gojobori do, so the result does not depend on which sequence comes first. Lines L4 and L5 add the mean counts over the pathways; every pathway between codons that differ at $k$ positions has exactly $k$ steps, so $s_d + n_d = k$ and $S_d + N_d$ is the number of differing bases. Line L6 gives $S + N = 3c$, the number of bases.

The site count is the right divisor in this sense: if every base mutates at the same rate to each of the three other bases, the expected number of synonymous changes at codon $x$ per unit of time is proportional to $s(x)$, and that of changes to another amino acid or to a stop codon is proportional to $n(x)$, with the same factor. So, if all these changes stayed in the sequence, $p_S$ and $p_N$ would have the same expected value for small divergence. Changes to stop codons do not stay in a working gene, so even without other selection $p_N$ is a little lower than $p_S$. Line L7 applies the Jukes-Cantor correction to each class as if its sites were a separate sequence with equal rates among the four bases. The full proof is below.

## Complexity

- **Time.** Each codon pair costs $O(1)$: at most nine neighbours for each site count and at most six pathways of three steps. So the time is $\Theta(c)$ in every case.
- **Space.** Five counters: $\Theta(1)$. With precomputed tables, 61 site values and $61^2$ difference pairs, a constant for a fixed code.
- **Many sequences.** All pairs of $m$ sequences cost $\Theta(m^2 c)$.

## Properties

- **Exact counts.** The site and difference counts are rational numbers; the implementation keeps them exact.
- **Symmetric.** Swapping $X$ and $Y$ gives the same result.
- **Equal weights.** All bases and all pathways have the same weight, so the method ignores the higher rate of transitions than transversions, the unequal use of codons, and the fact that some pathways are much more likely than others.
- **Undefined at saturation.** If $p \ge 3/4$, the logarithm is not defined. Near that limit the variance is very large. The usual large-sample variance is $\operatorname{Var}(d) \approx p(1 - p) / (L (1 - 4p/3)^2)$, with $L$ the number of sites of the class.
- **No uncertainty about the order.** Averaging over pathways is a choice, not an estimate of the true order of the changes.

## Variants and improvements

- **Weighted pathways.** Miyata and Yasunaga (1980) weighted pathways by how likely each amino acid change is, instead of giving them equal weights.
- **Modified counting with transitions.** Methods such as that of Li, Wu and Luo (1985) classify sites as nondegenerate, twofold or fourfold degenerate and use the [Kimura two-parameter](/kimura-two-parameter-model/) distance, so that the transition bias is taken into account.
- **Codon frequencies and the transition ratio.** Yang and Nielsen (2000) count sites with the transition to transversion ratio and the codon frequencies estimated from the data.
- **Maximum likelihood.** A [codon substitution model](/codon-substitution-model/) estimates $\omega$ by likelihood, handles the transition bias and the codon frequencies inside one model, and extends to many sequences on a tree.

## When to use it

Use it for a fast and simple estimate of $d_N$, $d_S$ and $\omega$ between two closely related coding sequences, for example in screens of many gene pairs, or as a check on likelihood estimates. For distant sequences, strong transition bias, strong codon bias or more than two sequences, use a codon substitution model by likelihood. For a test of adaptive evolution that uses polymorphism inside a species as well, use the [McDonald-Kreitman test](/mcdonald-kreitman-test/).

## Pitfalls

- **Saturation.** For distant sequences $p_S$ approaches $3/4$, $d_S$ becomes very large and noisy, and $\omega$ is then strongly biased. Treat estimates with $d_S$ above about 1 with care.
- **Transition bias.** Transitions at third positions are often synonymous, so a high transition rate inflates synonymous differences relative to sites and lowers $\omega$ when the method ignores it.
- **Alignment.** The sequences must be in frame. A frame shift or a misaligned codon creates many false nonsynonymous differences.
- **Stop codons.** An internal stop codon means a pseudogene, a frame error or a sequencing error. Remove it before counting.
- **Reading $\omega$.** A value above 1 over the whole gene is rare, because most sites are constrained. A value below 1 does not mean there was no positive selection at a few sites.

## Implementations

## History

Nei and Gojobori published the method in 1986, after the weighted pathway method of Miyata and Yasunaga (1980) and the degeneracy classes of Li, Wu and Luo (1985). Their version gives all pathways the same weight, which makes it simple to compute by hand or by a small table. Likelihood methods based on codon models, from Goldman and Yang (1994) and Muse and Gaut (1994), came later and are now the standard for careful analyses, but the counting method stays common for its speed and simplicity.

## References
