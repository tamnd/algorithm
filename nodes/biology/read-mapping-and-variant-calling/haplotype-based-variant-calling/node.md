---
tag: REPJDG
kind: algorithm
slug: haplotype-based-variant-calling
name: Haplotype-based variant calling
aliases:
- local reassembly variant calling
- active region reassembly
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Assemble candidate haplotypes in an active region with a local de Bruijn graph, score reads against them with a pair HMM, then call genotypes.
solves: [variant-calling-problem]
model: real-ram
complexity:
  vars: {R: the number of reads, L: the read length, n: the region length, H: the number of candidate haplotypes, V: the number of candidate variants}
  time: {worst: O(R H L n + R H^2 + R H V), per_read_haplotype: O(L n)}
  space: {extra: O(R H + L n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2012
  people: [Erik Garrison, Gabor Marth, Ryan Poplin, Mark A. DePristo]
  note: FreeBayes (Garrison and Marth, 2012) called variants from the haplotypes seen in the reads of a short window. GATK HaplotypeCaller, described by Poplin et al. (2017), assembles the haplotypes of each active region with a local de Bruijn graph and scores the reads against them with a pair HMM.
prereqs: [variant-calling-problem, pair-hmm, de-bruijn-assembly, genotype-likelihood]
see_also: [bayesian-genotype-calling, kmer, forward-algorithm, affine-gap-alignment, variant-normalization, somatic-variant-calling, variation-graph, split-read-method]
sources:
  - paper: doi:10.1101/201178
    title: Ryan Poplin, Valentin Ruano-Rubio, Mark A. DePristo and others, Scaling accurate genetic variant discovery to tens of thousands of samples, bioRxiv 201178, 2017
    locator: the sections on the HaplotypeCaller (the active regions, the local assembly of haplotypes, the pair HMM likelihoods of the reads and the genotyping)
  - paper: arxiv:1207.3907
    title: Erik Garrison and Gabor Marth, Haplotype-based variant detection from short-read sequencing, arXiv 1207.3907, 2012
    locator: the sections on the haplotype windows, the observed haplotypes of the reads and the Bayesian model of the genotypes
---

A haplotype-based variant caller does not look at each column of the alignment on its own. In a short region where the reads suggest a variant, it builds the full sequences that the two copies of the genome may have there, the *candidate haplotypes*, by local assembly of the reads. It then measures how well each read fits each haplotype, chooses the pair of haplotypes that explains the reads best, and reads the variants and their genotypes off that pair. Local assembly removes most of the errors that a mapper makes near insertions and deletions, because each read is compared with whole haplotypes, not with the reference. GATK HaplotypeCaller is the best known caller of this kind; this page describes its steps, in a small form, for one diploid sample.

## In plain words

Near an insertion or a deletion, a mapper often places the reads badly, and the columns of the alignment then show false mismatches. So do not trust the columns.

Instead, take the reads of a short stretch and join the ones that overlap, like a small jigsaw. Each way through the puzzle is a possible version of the stretch. Then ask, for each read and each version, how likely the read is if it came from that version. A person has two versions of each stretch, one from each parent, so try every two versions and keep the best ones. The differences between those versions and the reference are the variants.

## The problem

The input is a region of the reference $\mathit{ref}$ of length $n$, and the $R$ reads that map to it, each with a Phred quality for each base. The sample is diploid. The output is a list of variants (substitutions, insertions and deletions) with a genotype of 1 or 2 copies, and their likelihoods. This is the [variant calling problem](/variant-calling-problem/) for one region, solved with haplotypes as the hidden variables, not with one allele per column as in [Bayesian genotype calling](/bayesian-genotype-calling/).

## The algorithm

```pseudo id=main
HAPLOTYPE-CALLER(ref, reads, k)
L1  G ← the de Bruijn graph of the k-mers of the reads and of ref, with a count on each edge
L2  remove each edge not on ref that fewer than min_count reads support
L3  H ← the paths of G from the first to the last k-mer of ref, ref first, at most H_max
L4  ℓ[r][h] ← ln P(r | h) by PAIR-HMM, for each read r and haplotype h
L5  (a, b) ← the pair with the largest Σ_r ln(½ e^ℓ[r][a] + ½ e^ℓ[r][b])
L6  for each h ≠ ref in H: align h to ref with affine gaps and list its variants
L7  for each variant v, with A the set of haplotypes that carry it do
L8      GL[g] ← Σ_r ln((g/2) max_{h ∈ A} e^ℓ[r][h] + (1 - g/2) max_{h ∉ A} e^ℓ[r][h]) for g = 0, 1, 2
L9      the posterior of g is proportional to e^GL[g] times the prior of g; call the g with the largest one
L10 return H, the pair (a, b), and the variants with a called genotype of 1 or 2
```

An edge of the graph is a $(k + 1)$-mer, and its count is the number of times it occurs in the reads. The edges of the reference stay, so the reference is always a path. A path that does not repeat a [k-mer](/kmer/) spells a haplotype of the region. Line L2 is the error filter: a sequencing error makes a few new $k$-mers that only one read supports, and the threshold removes them. This is the local form of [de Bruijn assembly](/de-bruijn-assembly/).

The likelihood of a read is the sum over all its alignments to the haplotype, computed by the forward algorithm of a [pair HMM](/pair-hmm/) with three states, match $M$, insertion $I$ and deletion $D$. A match emits $1 - e$ for the same base and $e/3$ for another, with $e = 10^{-q/10}$ from the base quality $q$. A gap opens with probability $\delta$ and goes on with probability $\gamma$. The read may start at any place of the haplotype.

```pseudo id=pair-hmm
PAIR-HMM(r, q, h)
P1  for i ← 1 to L do
P2      for j ← 1 to n do
P3          M[i][j] ← emit(i, j) ((1 - 2δ) M[i-1][j-1] + (1 - γ)(I[i-1][j-1] + D[i-1][j-1])), with M[1][j] = emit(1, j) / n
P4          I[i][j] ← ¼ (δ M[i-1][j] + γ I[i-1][j])
P5          D[i][j] ← δ M[i][j-1] + γ D[i][j-1]
P6  return ln Σ_j (M[L][j] + I[L][j])
```

Line L6 uses an alignment with [affine gaps](/affine-gap-alignment/) and shifts each insertion or deletion to the left, so that the same event on two haplotypes gets the same name, as in [variant normalization](/variant-normalization/). Line L8 is the genotype likelihood of $g$ copies of the variant: a read comes from a copy with the variant with probability $g/2$. The likelihood of a read given an allele is the largest of its likelihoods over the haplotypes with that allele. The prior of lines L9 is $(1 - 1.5\theta, \theta, \theta/2)$ for 0, 1 and 2 copies, with $\theta = 10^{-3}$.

### What this version leaves out

A real caller does more. This version omits:

- the choice of active regions from the pileup,
- the larger $k$ that HaplotypeCaller tries when the graph has a cycle,
- the recovery of dangling ends,
- gap penalties that depend on the context, such as a repeat,
- the reference confidence of the sites with no variant,
- multi-allelic sites,
- downsampling and the fast pair HMM in hardware.

A region whose reference has a repeated $k$-mer is rejected, not assembled with a larger $k$.

## Example

The reference has 12 bases, and a heterozygous sample has a C to T change at position 6:

$$\mathit{ref} = \texttt{ACGTTGCAAGTC}, \qquad \mathit{alt} = \texttt{ACGTTGTAAGTC}.$$

With $k = 4$ and five full-length reads, two of the reference and three of the alternative, every edge of the alternative has a count of 3, so the graph has two paths, $H = (\mathit{ref}, \mathit{alt})$. With only one read of the alternative, its edges have a count of 1 and line L2 removes them.

All bases have quality 30, so $e = 10^{-3}$. A read of the reference fits the reference with $\ln P = \ln(1/12) + 12 \ln(1 - e) + 11 \ln(1 - 2\delta) = -2.519$: the start, twelve matching bases and eleven steps without a gap. Against the other haplotype, one match becomes a mismatch, and $\ln P = -10.524$. The difference is $\ln((1 - e)/(e/3)) = 8.005$.

The best pair is $(\mathit{ref}, \mathit{alt})$. The variant is $(6, \texttt{C}, \texttt{T})$, and its genotype likelihoods, in $\log_{10}$, are $-15.90$ for no copy, $-6.97$ for one copy and $-12.42$ for two copies. With the prior, the posterior of one copy is 0.999997.

A larger simulation used a region of 120 bases with a homozygous substitution, a heterozygous substitution on one haplotype and a heterozygous deletion of 2 bases on the other. With 24 reads of 40 bases from each haplotype, a 1% error rate and $k = 15$, the caller found the three variants with the right genotypes and posteriors above 0.999, and the best pair was the true phase. The graph had 8 paths, since it allows every mix of the three variants. Over 20 random seeds it found 58 of the 60 variants, called no wrong genotype and no false variant, and found the true phase in 18 runs.

## Correctness

Lines P3 to P5 are the forward recurrence of the pair HMM, so by induction on $i$ and $j$, $M[i][j]$, $I[i][j]$ and $D[i][j]$ are the total probability of all state paths that emit the first $i$ bases of the read, end at position $j$ of the haplotype and end in that state. Line P6 sums the paths that end in a state that emits, so it returns $P(r \mid h)$ under the model. Line L5 tries every pair, so it returns a pair with the largest likelihood. Line L8 is the stated mixture for each genotype, and line L9 is Bayes' rule. These are theorems about the model, proved in proofs/correctness.md and checked in the tests against a sum over all alignments for short reads.

The whole method is a heuristic for the variant calling problem. The true haplotypes are found only when every edge of them has enough reads and the region has no repeated $k$-mer, the pair HMM is a model of the errors, and the max over haplotypes in line L8 is an approximation of the sum over them.

## Complexity

- **Assembly.** The graph has $O(R L)$ edges and takes $O(R L)$ time to build. The search for paths can take time exponential in the number of bubbles, so the number of haplotypes is capped at $H_{\max}$, 64 here.
- **Likelihoods.** One pair HMM is $O(L n)$, and line L4 does $R H$ of them, $O(R H L n)$ in total. This is the main cost, and real callers run it on vector units or special hardware.
- **Genotypes.** Line L5 tries $O(H^2)$ pairs over $R$ reads, and lines L7 and L8 take $O(H)$ for each read and variant.
- **Space.** $O(R H)$ for the likelihoods and $O(L n)$ for one pair HMM table, or $O(n)$ with two rows, as the code does.

## Properties

- **Good near indels.** The reads are compared with whole haplotypes, so a read with a deletion is not forced into false mismatches.
- **Phase for free.** The best pair says which variants of the region are on the same copy.
- **Exact within the model.** The forward sums and the search over pairs are exact; the assembly and the model are not.
- **Region by region.** Each region is solved alone. Variants farther apart than the region are not phased together.

## Variants and improvements

- **Other sources of haplotypes.** FreeBayes takes the haplotypes from the alignments in a short window, without assembly. Platypus combines local assembly and the alignments.
- **Joint calling.** GATK computes the likelihoods per sample and genotypes many samples together.
- **Somatic calling.** Mutect2 uses the same assembly and pair HMM, but tests the allele fraction in a tumor against a normal sample, as in [somatic variant calling](/somatic-variant-calling/).
- **Graphs of known variants.** Aligning reads to a [variation graph](/variation-graph/) gives some of the same benefit for known variants, without local assembly.
- **Learned models.** DeepVariant also realigns the reads of a region to locally assembled haplotypes, but replaces the genotype model with a neural network on images of the pileup.

## When to use it

Use it for germline calls of substitutions and short insertions and deletions from short reads, where it is the standard. It costs more than a pileup caller, so the active region step keeps it to the places where a variant is likely. For large structural variants, use [split reads](/split-read-method/) or read pairs; for low allele fractions, use a somatic caller.

## Pitfalls

- **Linear gaps in line L6.** With a linear gap cost, the alignment of a haplotype with a 2-base deletion to the reference can be two separate 1-base deletions with the same score, which gives two false variants. An affine cost with a high open penalty keeps the deletion in one piece.
- **Repeats in the region.** A repeated $k$-mer makes a cycle, and the paths through it are not the haplotypes. Use a larger $k$ or a smaller region.
- **The pruning threshold.** At low depth, the edges of a true haplotype can fall below min_count and the variant is lost; at high depth, errors that repeat can pass.
- **Too many paths.** Every mix of the variants is a path, so the number of haplotypes grows as a power of 2 in the number of variants of the region; the cap can drop the true one.
- **Base qualities.** The pair HMM trusts the qualities. Badly calibrated qualities make the likelihoods too sure; see [base quality score recalibration](/base-quality-score-recalibration/).

## Implementations

## History

Callers in the early years of short reads used the pileup column by column, and indels were often called badly because the mapper placed the reads in different ways around them. Garrison and Marth (2012) described FreeBayes, which calls variants from the haplotypes of the reads in short windows. GATK HaplotypeCaller, described with its joint calling by Poplin et al. (2017), assembles candidate haplotypes in each active region with a de Bruijn graph and scores each read against each haplotype with a pair HMM. The same plan is used in Mutect2 for somatic calls and for the candidates of later callers.

## References
