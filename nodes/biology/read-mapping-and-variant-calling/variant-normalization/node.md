---
tag: YT7FC7
kind: algorithm
slug: variant-normalization
name: Variant normalization
aliases:
- left alignment of indels
- indel normalization
area: biology/read-mapping-and-variant-calling
level: core
summary: Write each variant in a unique form, parsimonious and left-aligned, so that the same indel in a repeat gets the same representation.
model: word-ram
complexity:
  vars: {k: the number of alleles, L: the length of the longest allele, s: the number of positions the variant moves left}
  time: {worst: O(k L (s + L)), average: O(k L (s + L)), best: Θ(k L)}
  space: {extra: O(k L)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2015
  people: [Adrian Tan, Goncalo R. Abecasis, Hyun Min Kang]
  note: Defined a normalized variant as one that is left-aligned and parsimonious, proved that the form is unique, and gave the algorithm in the vt tool.
prereqs: [variant-call-format, edit-distance]
see_also: [variant-calling-problem, haplotype-based-variant-calling, tandem-repeat-finding, global-alignment, affine-gap-penalty, precision-and-recall, genome-repeat, read-pileup]
sources:
  - paper: doi:10.1093/bioinformatics/btv112
    title: Adrian Tan, Goncalo R. Abecasis and Hyun Min Kang, Unified representation of genetic variants, Bioinformatics 31(13), 2015
    locator: pp. 2202 to 2204 (the definitions of left-aligned and parsimonious, the uniqueness theorem and the normalization algorithm)
  - url: https://samtools.github.io/hts-specs/VCFv4.3.pdf
    title: The Variant Call Format Specification, VCFv4.3, hts-specs
    locator: Section 1.6.1, the REF and ALT fields (the padding base of indels and the base after the event at position 1)
  - url: https://samtools.github.io/bcftools/bcftools.html
    title: bcftools manual
    locator: the section on bcftools norm (left alignment and normalization of indels, and the splitting of multiallelic records)
---

Variant normalization rewrites a variant record into one standard form, so that two records that describe the same change to the genome look the same. The problem comes from repeats: deleting one copy of CA from CACACA gives the same sequence whichever copy is deleted, so a caller can write the deletion at any of several positions, and it can also add extra reference bases on either side. Tan, Abecasis and Kang (2015) defined the normalized form as the one that is *parsimonious* (no base is shared by all alleles at either end, beyond one padding base) and *left-aligned* (it cannot move further left), and showed that it is unique. Tools such as vt normalize and bcftools norm compute it before call sets are merged or compared.

## In plain words

A change to a word can often be written in more than one way. If "banana" loses one "an", you cannot tell which "an" went, because all choices give "bana". You can also write the change with more letters around it than you need.

To make every writer agree, choose one rule. First cut off letters at the end that all versions share. If a version becomes empty, step one letter left and add the letter there to all versions. Repeat until nothing changes. Then cut off letters at the start that all versions share, but always keep at least one letter. The result is the shortest way to write the change, placed as far left as it can go.

## The problem

Positions are 1-based, as in [VCF](/variant-call-format/); the code indexes strings from 0. A variant is a position $p$ and alleles $x_0, x_1, \dots, x_k$, where $x_0$ is the reference allele, equal to the $|x_0|$ reference bases from position $p$, and $x_1, \dots, x_k$ are the alternate alleles. All alleles are non-empty and pairwise different. Allele $x_j$ gives the haplotype $H_j$, the reference with $x_0$ at $p$ replaced by $x_j$.

Two variants are **equivalent** if they give the same haplotypes in the same order. A variant is

- **left-aligned** if no equivalent variant has a smaller position and alleles of the same lengths;
- **parsimonious** if no equivalent variant has shorter alleles, that is, the alleles do not all end with the same base, and they do not all start with the same base unless one of them has length 1.

**Output.** The unique equivalent variant that is both left-aligned and parsimonious.

## The algorithm

```pseudo id=main
NORMALIZE(R, p, x_0, ..., x_k)
    changed ← true
L1  while changed do
L2      changed ← false
L3      if all alleles end with the same base then remove it from each; changed ← true
L4      if some allele is empty then
L5          p ← p - 1; put R[p] in front of each allele; changed ← true
L6  while all alleles start with the same base and every allele has length at least 2 do
L7      remove the first base of each allele; p ← p + 1
L8  return (p, x_0, ..., x_k)
```

Line L5 needs a base to the left. If the variant would have to move before position 1, the code stops with an error, where VCF would pad with the base after the event instead; the code leaves that case out. The first loop moves the event left one base at a time, rotating the alleles through the repeat; the second loop removes shared bases at the left end that the first loop could not see.

## Example

Take the reference `GTCACACAGT` and a haplotype `GTCACAGT` that lacks one copy of CA. Among the records that describe it are (6, `ACA`, `A`), (4, `ACA`, `A`), (3, `CAC`, `C`), (5, `CACAG`, `CAG`) and (2, `TCA`, `T`); there are 34 in all with non-empty alleles. Start from (6, `ACA`, `A`):

| round | after L3 | after L5 |
|---|---|---|
| 1 | (6, `AC`, empty) | (5, `CAC`, `C`) |
| 2 | (5, `CA`, empty) | (4, `ACA`, `A`) |
| 3 | (4, `AC`, empty) | (3, `CAC`, `C`) |
| 4 | (3, `CA`, empty) | (2, `TCA`, `T`) |
| 5 | no change, since `A` and `T` differ | no change |

The second loop does nothing, because `T` has length 1. The result is (2, `TCA`, `T`): the deletion of `CA` after the `T` at position 2. Every one of the 34 records normalizes to it.

An SNV written with extra bases, (3, `CAC`, `CGC`), loses the shared `C` at the end in line L3 and the shared `C` at the start in line L7, which gives (4, `A`, `G`).

## Correctness

Every equivalent variant is fixed by how many bases of the common prefix of the haplotypes it leaves on the left and how many of the common suffix it leaves on the right. Each step of the first loop keeps the haplotypes the same and either trims a base of the common suffix into the right flank or shifts the event one base left. That loop ends when the alleles no longer share a last base and none is empty, which happens exactly when the whole common suffix is in the right flank. The second loop then moves as much of the common prefix into the left flank as it can while every allele keeps at least one base. Both counts are then determined by the haplotypes alone, so the result is the same for every equivalent input, and it is both parsimonious and left-aligned. The full proof is in proofs/correctness.md. It assumes that no haplotype is a suffix of all the others; otherwise the event would slide to position 1.

## Complexity

- **Time.** Each round of the first loop does $O(k)$ work on the ends of the alleles, plus the cost of the string updates. The number of rounds is at most $s + L$, where $s$ is the shift to the left. The code builds new strings in each round, which costs $O(k L)$ per round and $O(k L (s + L))$ in total. With arrays and a moving window, each round costs $O(k)$ and the total is $O(k (s + L))$.
- **Space.** $O(k L)$ for the alleles.
- **In practice.** The shift is at most the length of the repeat around the event, so normalizing a whole VCF is fast compared with reading it.

## Properties

- **Unique output.** Equivalent inputs give the same output, which is the theorem of Tan et al. (2015).
- **Idempotent.** Normalizing a normalized variant changes nothing.
- **Keeps the haplotypes.** Every step keeps all the haplotypes the same.
- **Needs the reference.** Line L5 reads the reference base to the left, so the tool needs the reference sequence, not only the VCF.

## Variants and improvements

- **Right alignment.** Some formats, such as the HGVS nomenclature for clinical variants, place an event as far to the 3' end as possible. The same algorithm with the two ends swapped gives that form.
- **Multiallelic records.** A record with several ALT alleles can be normalized as a whole, as here, or split into one record per ALT allele first, which can give each allele a different position. bcftools norm can do both.
- **Complex variants.** Two records that describe the same haplotype as a different set of events, such as an MNV against two SNVs, or an insertion plus a deletion against a substitution, are not made equal by normalization. Comparing them needs the haplotypes; tools that compare call sets for [precision and recall](/precision-and-recall/) do this by rebuilding the haplotypes.
- **In callers.** Aligners and callers can produce left-aligned indels directly, by breaking ties in the alignment to the left.

## When to use it

Normalize every VCF before merging call sets, comparing them with a benchmark, or looking variants up in a database. Without it, a deletion in a repeat can be counted as a false positive in one set and a false negative in the other, although both sets have it.

## Pitfalls

- **A different reference.** The result depends on the reference sequence. Normalizing against another build, or a reference that differs from the one used for calling, gives wrong results or a REF mismatch.
- **Position 1.** An event that reaches the start of a sequence cannot be padded on the left; VCF uses the base after the event there.
- **Splitting first or not.** Normalizing a multiallelic record as a whole and normalizing its split records can give different positions. Pick one order and use it for all call sets.
- **Not a full comparison.** Normalized records that differ can still give the same haplotypes when they are not equivalent one record at a time, as for complex variants.
- **Repeats around the event.** In a long tandem repeat, the left-aligned position can be far from where the caller put the event; this is correct, but it can move the event out of a region of interest.

## Implementations

## History

VCF asks for a padding base on indels, but it does not fix which of the equivalent positions to use. Tan, Abecasis and Kang (2015) gave the formal definitions of left-aligned and parsimonious, proved that the normalized form is unique, and gave the algorithm in their tool vt. bcftools norm implements the same normalization.

## References
