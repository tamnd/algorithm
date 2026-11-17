---
tag: 47N3AD
kind: algorithm
slug: discordant-read-pair-method
name: Discordant read-pair method
aliases:
- paired-end mapping SV detection
area: biology/read-mapping-and-variant-calling
level: advanced
summary: Find read pairs whose mapped distance or orientation disagrees with the library, cluster the ones that agree with each other, and call a structural variant from each cluster with enough support.
solves: [structural-variant-detection]
model: word-ram
complexity:
  vars: {n: the number of discordant pairs, w: the largest number of pairs whose left mates fall in one window of length d}
  time: {worst: O(n log n + n w log n), best: O(n log n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2005
  people: [Eray Tuzun, Andrew J. Sharp, Jeffrey A. Bailey, Evan E. Eichler]
  note: Tuzun et al. mapped the two end sequences of fosmid clones to the human reference and called structural variants from the ends that were too far apart, too close or in the wrong orientation. Korbel et al. (2007) did the same with paired-end reads, and BreakDancer (2009) and DELLY (2012) brought the method to Illumina data.
prereqs: [structural-variant-detection, paired-end-read-mapping, paired-end-reads]
see_also: [split-read-method, read-depth-copy-number-analysis, union-find-connectivity, connected-components, mapping-quality, duplicate-read-marking, variant-call-format, interval-tree]
sources:
  - paper: doi:10.1038/ng1562
    title: Eray Tuzun, Andrew J. Sharp, Jeffrey A. Bailey and others, Fine-scale structural variation of the human genome, Nature Genetics 37(7), 2005
    locator: the sections on the mapping of fosmid end sequences and the discordant clones that mark deletions, insertions and inversions
  - paper: doi:10.1126/science.1149504
    title: Jan O. Korbel, Alexander Eckehart Urban, Jason P. Affourtit and others, Paired-end mapping reveals extensive structural variation in the human genome, Science 318(5849), 2007
    locator: the description of the method (the mapping of the two ends of each fragment and the clusters of pairs with an unexpected span or orientation)
  - paper: doi:10.1038/nmeth.1363
    title: Ken Chen, John W. Wallis, Michael D. McLellan and others, BreakDancer, an algorithm for high-resolution mapping of genomic structural variation, Nature Methods 6(9), 2009
    locator: the sections on the classification of anomalous read pairs, the clusters and the confidence score
  - paper: doi:10.1093/bioinformatics/bts378
    title: Tobias Rausch, Thomas Zichner, Andreas Schlattl and others, DELLY, structural variant discovery by integrated paired-end and split-read analysis, Bioinformatics 28(18), 2012
    locator: the sections on the paired-end clustering and the refinement of breakpoints by split reads
  - paper: doi:10.1038/nrg2958
    title: Can Alkan, Bradley P. Coe and Evan E. Eichler, Genome structural variation discovery and genotyping, Nature Reviews Genetics 12(5), 2011
    locator: the section on read-pair methods and the figure of the signatures of each class of variant
---

The discordant read-pair method finds structural variants from the layout of paired reads. In a paired library, the two mates of a fragment map to the reference at a known distance and in a known orientation. A deletion in the sample makes some pairs map too far apart, an insertion makes them too close, an inversion turns one mate around, and a tandem duplication swaps their order. The method takes the pairs that disagree with the library, joins the ones that tell the same story, and calls a variant from each group with enough pairs. It finds the type of the variant and its approximate place, but not the exact breakpoint, which [split reads](/split-read-method/) give.

## In plain words

Each read pair comes from one piece of DNA of about the same length, read from both ends. When you place the two reads on the reference, they usually land the right distance apart and face each other.

If a part of the sample is missing from the reference's point of view, pairs that cross the gap land too far apart. If something extra is in the sample, they land too close. If a part is turned around, one read faces the wrong way. One odd pair can be a mistake, so collect the odd pairs that land near each other at both ends. A group with several pairs is a call.

## The problem

The input is a set of pairs mapped to one chromosome. A pair is $(u, s, v, s')$: the leftmost positions $u \le v$ of its two mates on the reference and their strands. Both mates have length $L$, and the span of the pair is $v + L - u$. The library has the forward-reverse layout: a normal pair is $+$ then $-$, with a span near the mean $\mu$, with standard deviation $\sigma$. The output is a list of calls, each with a type, the number of supporting pairs and bounds on its breakpoints. See [structural variant detection](/structural-variant-detection/) for the problem and the other signals.

The robust estimates of $\mu$ and $\sigma$ are the median of the spans of all pairs and 1.4826 times their median absolute deviation, which ignore the few pairs from variants.

## The algorithm

With a threshold $z$, a pair is

- **DEL** if it is $+-$ with span $> \mu + z\sigma$,
- **INS** if it is $+-$ with span $< \mu - z\sigma$,
- **INV** if it is $++$ or $--$, and
- **DUP** if it is $-+$.

Two pairs of the same type and strand layout are *linked* when their left mates start at most $d$ apart and their right mates start at most $d$ apart. A cluster is a connected component of this relation.

```pseudo id=main
DISCORDANT-PAIRS(P, L, μ, σ, z, s_min, d)
L1  for each pair q in P do
L2      t ← the type of q (DEL, INS, INV, DUP or concordant)
L3      if t is not concordant then add q to the group (t, strands of q)
L4  for each group G: sort G by the left position u
L5      for each pair q in G, and each later pair q' with u(q') - u(q) ≤ d do
L6          if |v(q') - v(q)| ≤ d then
L7              UNION(q, q')
L8      for each component with at least s_min pairs do
L9          make a call with its type, support, breakpoint bounds and size
L10 return the calls
```

The default $d$ is $\mu + z\sigma$, the largest fragment that the library allows. Line L5 stops the inner loop at the first pair that is more than $d$ to the right, because the list is sorted. [Union-find](/union-find-connectivity/) joins the linked pairs into components.

The bounds of line L9 come from the mates next to the breakpoint. For a deletion, every left mate ends before the deleted part, so the left breakpoint is at or after the largest end of a left mate. Every right mate starts after it, so the right breakpoint is at or before the smallest start of a right mate. The size of a deletion is the median span minus $\mu$, and the size of an insertion is $\mu$ minus the median span. The two ends of an inversion give two clusters, the $++$ pairs at one breakpoint and the $--$ pairs at the other.

## Example

With $L = 50$, $\mu = 300$, $\sigma = 30$ and $z = 3$, a $+-$ pair is a DEL above a span of 390 and an INS below 210. Five pairs:

| $u$ | $v$ | span | type |
|---|---|---|---|
| 100 | 1240 | 1190 | DEL |
| 130 | 1255 | 1175 | DEL |
| 160 | 1290 | 1180 | DEL |
| 140 | 360 | 270 | concordant |
| 2000 | 3500 | 1550 | DEL |

The first three DEL pairs start within 60 bases of each other on the left and within 50 on the right, both below $d = 390$, so they form one cluster. The pair at 2000 is alone and has support 1, below $s_{\min} = 3$. The call is a DEL with support 3. The left breakpoint is at or after 210, the largest end of a left mate, and the right breakpoint is at or before 1240. The median span is 1180, so the size is $1180 - 300 = 880$ bases.

On a simulated chromosome of 30,000 bases with a deletion of 1000 bases, an inversion of 2000, a tandem duplication of 1500 and an insertion of 150 new bases, 3000 pairs and 15 random noise pairs gave the five expected calls. The deletion had 18 pairs, size 1014, and bounds 4997 and 6007 around the true 5000 and 6000. The insertion had only 6 pairs and size 148. The two ends of the inversion had 21 and 15 pairs. Over 30 seeds, 29 runs found all five calls.

## Correctness

The scan finds every link: the list is sorted by $u$, so once a later pair is more than $d$ to the right, all the pairs after it are too, and every linked pair is visited from its left member. Union-find then gives the connected components of the links. The pairs of one event also form one cluster: the two parts of a fragment that crosses a breakpoint add up to its length, at most $\mu + z\sigma$ for a pair that the library allows, and each part holds a whole mate, so the left mates of all such pairs lie in one window of length $\mu + z\sigma - 2L$, and so do the right mates. With $d \ge \mu + z\sigma - 2L$ they are all linked. These facts are proved in proofs/correctness.md.

The calls are a heuristic for the structural variant problem. The type of a pair is a test, and a pair can be discordant by chance, from a wrong mapping or from a chimeric fragment. Two variants closer than $d$ can join into one cluster.

## Complexity

- **Time.** The classification is $O(n)$ for $n$ pairs, the sort is $O(n \log n)$ and the scan makes $O(n w)$ comparisons, where $w$ is the largest number of pairs in one window of length $d$. Union-find with path halving makes each operation $O(\log n)$ amortized, so the total is $O(n \log n + n w \log n)$.
- **In practice.** Only the discordant pairs are clustered, a small part of all pairs, and $w$ is about the depth of discordant pairs at one event.
- **Space.** $O(n)$ for the groups and the union-find array.

## Properties

- **Heuristic.** The output depends on $z$, $d$ and $s_{\min}$. There is no objective that it optimizes.
- **Finds all four simple types.** Deletions, insertions shorter than the fragment, inversions and tandem duplications each have their own signature. With pairs on two chromosomes it also finds translocations.
- **Approximate breakpoints.** The bounds have a width of up to about a fragment length. The method does not see the exact base.
- **Size limits.** A deletion must be larger than about $z\sigma$ to make the span stand out, and an insertion must be shorter than the fragment for a pair to cross it.

## Variants and improvements

- **Scores.** BreakDancer gives each cluster a confidence score from the number of pairs and the expected rate of random discordant pairs.
- **Split-read refinement.** DELLY uses the [split reads](/split-read-method/) near a cluster to find the breakpoint to the base.
- **Pairs with one mate unmapped.** If one mate maps and the other does not, the unmapped mate can come from inserted sequence, and these pairs mark the place of a large insertion.
- **Multiple mappings.** VariationHunter and similar methods let a pair have several possible places and choose them so that the clusters are as few as possible, which helps in repeats.
- **Joint signals.** Many callers combine pairs with [read depth](/read-depth-copy-number-analysis/) and split reads, since each signal misses some classes.

## When to use it

Use it with a paired-end library to find structural variants larger than a few standard deviations of the insert size, and to tell their type. It is the main signal for inversions and for insertions of sequence that is not in the reference. It is weaker for small events, for exact breakpoints and in repeats, where split reads, local assembly or long reads do better.

## Pitfalls

- **A wrong library model.** A library with two insert sizes, or a wide one, makes many pairs look discordant. Estimate $\mu$ and $\sigma$ from the data, for each library.
- **Low mapping quality.** In repeats, a mate placed at the wrong copy makes a false discordant pair. Filter by [mapping quality](/mapping-quality/).
- **Duplicates.** PCR copies of one pair make a cluster look better supported than it is; [mark duplicates](/duplicate-read-marking/) first.
- **Biased sizes.** A long fragment has more start positions that let it cross a breakpoint, so the pairs that cross an event favor long fragments. A deletion then looks a little larger and an insertion a little smaller than it is. With the numbers of the simulation, the bias of the mean is about $\sigma^2/(\mu - 2L) = 4.5$ bases for the deletion and $\sigma^2/(\mu - 2L - 150) = 18$ for the insertion. Over 30 seeds, the size of the insertion of 150 bases was estimated between about 105 and 158.
- **Few pairs across insertions.** Only fragments longer than the insertion plus two mates can cross it, so insertions get less support than deletions of the same size.
- **Clusters that merge.** Two events within $d$ of each other give one call.

## Implementations

## History

Tuzun et al. (2005) mapped the end sequences of fosmid clones of a human genome to the reference and found deletions, insertions and inversions from the clones whose ends were too far apart, too close or in the wrong orientation. Korbel et al. (2007) used the same idea with paired ends from 454 sequencing, at a higher resolution. With Illumina paired-end data, BreakDancer (Chen et al., 2009) and DELLY (Rausch et al., 2012), which adds split reads, made it a standard step of structural variant calling. The review of Alkan, Coe and Eichler (2011) compares it with the other signals.

## References
