---
tag: 2NWVDC
kind: technique
slug: repeat-masking
name: Repeat masking
aliases:
- interspersed repeat masking
area: biology/gene-finding-and-motifs
level: core
summary: Find copies of known repeat families by alignment to a library and mask them, so that later gene finding and alignment skip them.
prereqs: [smith-waterman, genome-repeat]
see_also: [tandem-repeat-finding, profile-hmm, hmmer, blast, local-alignment, e-value, genome-annotation, comparative-gene-finding]
sources:
  - url: https://www.repeatmasker.org/
    title: Arian F. A. Smit, Robert Hubley and Phil Green, RepeatMasker Open-4.0, 2013 to 2015
    locator: the program description, its search engines (nhmmer, cross_match, ABBlast/WUBlast, RMBlast, Decypher) and libraries (Dfam and Repbase), and the release notes of version 4.2.4
  - url: https://www.repeatmasker.org/faq.html
    title: RepeatMasker, frequently asked questions
    locator: the citation form of the program, the definition of simple repeats (units of typically 1 to 5 bp), and the default masking of repeats by N
  - paper: doi:10.1093/nar/27.2.573
    title: Gary Benson, Tandem repeats finder, a program to analyze DNA sequences, Nucleic Acids Research 27(2), 1999
    locator: pp. 573 to 580; the detection of approximate tandem repeats, which masking pipelines use for simple repeats
---

Repeat masking finds the copies of known repeat families in a genome, such as transposons and satellites, by local alignment of the genome with a library of family sequences or models, and then hides those copies by replacing their bases with N or by writing them in lowercase. The masked genome goes to the later steps, gene finding, similarity search and alignment, so that they do not waste time on repeats or report false genes and false matches inside them. The standard tool is RepeatMasker by Smit, Hubley and Green, which searches with [Smith-Waterman](/smith-waterman/) style aligners or with [profile HMMs](/profile-hmm/) against the Dfam and Repbase libraries. It is a heuristic step: its result depends on the library, the score thresholds and the rules that resolve overlapping hits.

## In plain words

Large genomes are full of copies of the same few hundred kinds of sequence. Most of them come from transposons, pieces of DNA that copied themselves into new places over millions of years and then decayed. Roughly half of the human genome can be traced to such copies. They cause trouble: a gene finder sees the open reading frames of old transposons and calls them genes, and a search for similar sequences finds thousands of meaningless hits. So, before anything else, take a catalogue of the known repeat kinds, look for each one along the genome, allowing for the changes that each copy has collected, and cover up every copy that you find. Later tools then read the covered parts as unknown and skip them.

## When it applies

- **Before gene finding and evidence alignment.** Every eukaryotic [genome annotation](/genome-annotation/) masks repeats first. Gene finders and aligners that see the repeats produce false gene models from transposon genes and false protein matches.
- **Before seed-based similarity search.** Tools such as [BLAST](/blast/) and genome aligners start from short exact matches. A repeat family with $10^5$ copies gives $10^{10}$ seed pairs between two genomes; masking, or at least down-weighting, the repeats keeps the search feasible.
- **When a library exists or can be built.** The technique needs representative sequences or models of the repeat families. For well-studied species, curated libraries exist. For a new species, a de novo tool builds the library from the genome itself, by finding sequences with many copies.
- **For copies that are recognizable.** Old copies that diverged by more than about 30 to 40 percent from their consensus are hard to tell from random sequence, and they stay unmasked. Masking finds what the library and the scoring can see, not all repeats.

## The template

The input is a genome $G$ of length $n$, a library $\mathcal{F}$ of repeat families (consensus sequences or profile HMMs), and a score threshold $t(f)$ for each family.

```pseudo id=main
MASK-REPEATS(G, F, t)
L1  H ← an empty list of hits
L2  for each family f in F do
L3      add to H every local alignment of f or its reverse complement with G whose score is at least t(f)
L4  sort H by score, best first
L5  for each hit h in H, in this order do
L6      cut from h the parts that a kept hit with a higher score covers, and keep the rest if it is long enough
L7  add the simple repeats and the low-complexity regions of G to the kept hits
L8  replace each base of G inside a kept hit by N, or write it in lowercase
L9  return the masked G and the table of kept hits (family, strand, coordinates, score, divergence)
```

**The search (lines L2 and L3).** Each family is aligned locally to the whole genome. RepeatMasker can use several search engines for this step: cross_match and RMBlast find word matches and extend them into Smith-Waterman style local alignments, with a scoring matrix chosen for the expected divergence of the copies and the base composition of the genome, and nhmmer searches with the profile HMMs of the Dfam library. A profile HMM gives each position of the family its own scores, so it uses the information of a family alignment that a single consensus loses.

**The threshold (line L3).** The score cut-off sets the balance between missed copies and false hits. It is a rule of thumb fit to the scores that unrelated sequences reach. With profile HMMs, the threshold can be set per family and turned into an [E-value](/e-value/) on the size of the genome.

**Resolving overlaps (lines L4 to L6).** Copies of related families overlap, and young transposons insert into old ones, so one region can carry several hits. A simple rule keeps the best-scoring hit and gives each base to it; programs also join the pieces of one copy that a later insertion split, and they report the nested structure.

**Simple repeats (line L7).** Short tandem repeats, with units of typically 1 to 5 bases (A, CA, CGG and so on), and regions of low complexity are found by a separate method, often [tandem repeat finding](/tandem-repeat-finding/), because they are not families with a common ancestor and a library search handles them badly.

**Hard and soft masking (line L8).** Hard masking replaces the bases by N, which removes them from every later step; the RepeatMasker default does this. Soft masking writes them in lowercase, so that tools can skip them in seed finding but still extend alignments through them. Many genome browsers, gene finders and aligners accept soft-masked genomes.

**Cost.** A full Smith-Waterman scan of a family of length $\ell$ against the genome costs $O(\ell n)$ time, so the whole library costs $O(n \sum_f \ell_f)$. For a large library and genome, this is too slow, and the engines use word seeds and banded extension to search only near promising matches, which gives up the guarantee of the full scan for speed.

## Classic examples

**A toy library search.** Take one family $f$ of 40 bases and a genome of 227 bases that holds two copies of it: at positions 61 to 100 a copy with two substitutions, and at positions 151 to 187 a reverse complement copy with a deletion of three bases. With match +2, mismatch -3 and a gap -5 per base, the best local alignments are:

| copy | strand | genome positions | alignment | score |
|---|---|---|---|---|
| 1 | + | 61 to 100 | 38 matches, 2 mismatches | $76 - 6 = 70$ |
| 2 | - | 151 to 187 | 37 matches, 3 gaps | $74 - 15 = 59$ |

A perfect copy would score 80. To set a threshold, align $f$ and its reverse complement with 200 random sequences of the same length (uniform bases, fixed seed). The best score per random sequence had a median of 14, a 95th percentile of 18, and a maximum of 20. A threshold of 30 then masks both copies and no random hit, in this measurement; in a real genome, with its uneven base composition and its many old copies, thresholds come from larger tests of the same kind.

**RepeatMasker.** The standard program, by Smit, Hubley and Green, distributed as RepeatMasker Open-4.0 and current at version 4.2.4. It screens a genome against the Dfam library of profile HMMs and the Repbase library of consensus sequences, reports each hit with its family, its class, its divergence from the consensus and its coordinates, and masks the hits by N by default.

**De novo libraries.** For a new species, a tool such as RepeatModeler (by Smit and Hubley) finds sequences with many copies in the genome, builds a consensus for each family, and classifies them by similarity to known transposons. The library then goes to RepeatMasker.

**Masking in alignment tools.** Search tools mask low-complexity regions of the query on their own, and genome aligners read soft-masked genomes so that they start no seeds in lowercase bases.

## Variations

- **Library-based and de novo.** Library-based masking finds known families with high sensitivity. De novo methods find families with no prior model, from k-mer counts or self-alignment of the genome; they also find multi-copy genes, which must then be removed from the library by hand or by filters.
- **Profile HMMs and consensus sequences.** A consensus is one sequence per family, and a profile HMM has scores per position learned from many copies. Profile HMMs are more sensitive for old copies, at a higher cost per base.
- **Divergence-aware scoring.** Copies of an old family have diverged more than copies of a young one. Scoring matrices built for a given divergence and base composition give better separation than one matrix for all families.
- **Masking by k-mer counts.** Some aligners do not mask by family at all. They count the k-mers of the genome and ignore or down-weight k-mers above a frequency cut-off, which removes the effect of repeats on seeding at almost no cost.
- **Annotation of repeats for their own sake.** The same search, with the table of hits as the product, is used to study transposon activity, the age of families (from their divergence) and the structure of centromeres.

## Pitfalls

- **Masking genes.** Some gene families have many copies, and some genes contain parts of old transposons. A library that holds such sequences masks real exons. Remove multi-copy host genes from a de novo library before masking.
- **Hard masking and then mapping reads.** Reads from a repeat cannot map to a genome masked by N, so their coverage disappears and they may map to a wrong place. Map reads to the unmasked or the soft-masked genome.
- **Library for the wrong species.** A library from a distant species misses the families specific to the new genome, and the genome stays largely unmasked. Use a species library, or build one de novo.
- **Old copies stay.** Copies that diverged far from the consensus score below the threshold and stay unmasked. Lowering the threshold masks them but also masks random sequence. There is no setting that finds all copies and no false ones.
- **Simple repeats in the search.** Without a separate step for simple repeats, families that contain a simple repeat match every microsatellite in the genome, and the table fills with false hits.
- **Comparing masked fractions.** The fraction of a genome that is masked depends on the library, the engine, the thresholds and the version. Two numbers from different runs are not comparable without the same settings.

## Exercises

1. In the toy example, compute the score of a copy of $f$ with $k$ substitutions and no gaps. For which $k$ does it fall below the threshold of 30?
2. Show that with linear gap costs a deletion of $d$ bases in a copy costs $5d$ in the toy scoring, and find the largest $d$ for which a copy with no other change still scores above 30.
3. Two hits overlap: family A covers positions 100 to 400 with score 900, family B covers 350 to 600 with score 700. Apply lines L4 to L6 with a minimum length of 50 bases, and give the kept hits.
4. A genome of $3 \cdot 10^9$ bases is searched with a library of 1000 families of average length 1000 by full Smith-Waterman. Estimate the number of cells, and the time at $10^9$ cells per second.
5. Explain why the threshold of the toy example would need to be higher for a genome of $10^9$ bases, using the growth of the maximum of many random local alignment scores with the length of the sequence.

## References
