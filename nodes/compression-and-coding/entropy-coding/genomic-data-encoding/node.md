---
tag: 9E652P
kind: technique
slug: genomic-data-encoding
name: Genomic data encoding
aliases:
- two-bit nucleotide packing
- reference-based read compression
area: compression-and-coding/entropy-coding
level: intro
summary: Store DNA in 2 bits per base with side lists for N runs and other IUPAC codes, and store mapped reads as their differences from a reference genome.
prereqs: [bit-packing, variable-byte-encoding]
see_also: [read-mapping, kmer, fm-index, bwa, context-modeling, arithmetic-coding, run-length-encoding, delta-encoding]
sources:
  - url: https://genome.ucsc.edu/FAQ/FAQformat.html#format7
    title: UCSC Genome Browser, Genome Browser data formats
    locator: the .2bit format (the header with signature 0x1A412743, the nBlock and maskBlock lists, and packedDna with T = 00, C = 01, A = 10, G = 11)
  - url: https://samtools.github.io/hts-specs/CRAMv3.pdf
    title: CRAM format specification, version 3.1, GA4GH and the hts-specs project
    locator: Section 10.6, the read features of mapped reads (FN, FP and FC, with codes such as X for a base substitution), and the substitution matrix of the compression header
  - paper: doi:10.1101/gr.114819.110
    title: Markus Hsi-Yang Fritz, Rasko Leinonen, Guy Cochrane and Ewan Birney, Efficient storage of high throughput DNA sequencing data using reference-based compression, Genome Research 21(5), 2011
    locator: the reference-based scheme for aligned reads and the controlled loss of quality values
  - paper: doi:10.1371/journal.pone.0059190
    title: James K. Bonfield and Matthew V. Mahoney, Compression of FASTQ and SAM format sequencing data, PLoS ONE 8(3), e59190, 2013
    locator: the context models for sequences, names and quality values in fqzcomp
  - paper: doi:10.1093/nar/gkp1137
    title: Peter J. A. Cock, Christopher J. Fields, Naohisa Goto, Michael L. Heuer and Peter M. Rice, The Sanger FASTQ file format for sequences with quality scores and the Solexa/Illumina FASTQ variants, Nucleic Acids Research 38(6), 2010
    locator: the FASTQ record layout and the Phred quality encoding with offset 33
---

Genomic data encoding is the set of simple codes that store DNA well before any general compressor runs. A DNA sequence uses four letters, A, C, G and T, so two bits per base are enough, a quarter of the space of one ASCII byte per base. Real sequences also hold N for an unknown base and other IUPAC codes for ambiguous bases; a 2-bit store keeps these in short side lists, such as the list of N runs in the UCSC 2bit format. Sequencing reads add a second idea: a read that a [read mapper](/read-mapping/) places on a known reference genome can be stored as its position and its few differences from the reference, which is the idea behind the CRAM format and the work of Fritz, Leinonen, Cochrane and Birney (2011).

## In plain words

There are only four DNA letters, so each letter can be one of four small codes, and four letters fit in one byte. A genome of three billion letters then takes about three quarters of a gigabyte instead of three gigabytes.

Some places in a genome are unknown and are written as N. These come in long stretches, so you keep a short list that says "from here, this many N". Rarer letters that mean "A or G" and so on go in a second list, with their places.

Reads from a sequencing machine are short copies of parts of a genome, with a few errors and real differences. If you already have the genome, you do not store the read again. You store where it starts and the few letters where it is different. That is often a few bytes for a read of a hundred letters.

## When it applies

- **Large DNA strings over a known alphabet.** Reference genomes, assembled contigs and k-mer tables are mostly A, C, G and T. Two-bit packing gives a fixed 4 to 1 saving over ASCII, keeps random access (base $i$ is in byte $\lfloor i/4 \rfloor$), and lets programs compare and hash short strings as integers.
- **Few symbols outside ACGT, in runs.** The side lists stay small when the N bases come in long runs, as in the gaps of a genome assembly, and when other IUPAC codes are rare. When they are common, a 4-bit code per base is simpler.
- **Reads that map to a known reference.** The reference-based delta needs the reads to be aligned first, and the decoder needs the exact same reference. It gains most when the reads are deep copies of one genome, as in resequencing of a species with a good reference.
- **Bases only.** Read names and quality values are a separate stream, and in FASTQ files of short reads they are often most of the compressed size. They need other models.

## The template

**Conventions.** A sequence is $x = x_0 x_1 \cdots x_{n-1}$ over the IUPAC nucleotide letters in upper case. The base codes are those of UCSC 2bit: T = 0, C = 1, A = 2, G = 3, and the first base of each byte is in its two most significant bits. A read is a pair $(p, y)$: its 0-based start position $p$ on the reference $R$ and its bases $y_0 \cdots y_{\ell - 1}$, with $\ell$ the read length. This simple form has substitutions only: base $y_j$ is aligned to $R[p + j]$. Integers in the read stream are written as [ULEB128 varints](/variable-byte-encoding/).

```pseudo id=main
PACK(x[0 .. n−1])                                ▷ 2 bits per base, N runs and exceptions on the side
L1  B ← ⌈n/4⌉ zero bytes; N ← empty list of (start, length); E ← empty list of (position, letter)
L2  for i ← 0 to n − 1
L3      v ← code(x[i]) if x[i] ∈ {A, C, G, T}, else 0
L4      B[⌊i/4⌋] ← B[⌊i/4⌋] OR (v << (6 − 2(i mod 4)))
L5      if x[i] = N then extend the last run of N if it ends at i, else append (i, 1) to N
L6      else if x[i] ∉ {A, C, G, T} then append (i, x[i]) to E
L7  return (n, B, N, E)

UNPACK(n, B, N, E)
L8  for i ← 0 to n − 1: x[i] ← letter((B[⌊i/4⌋] >> (6 − 2(i mod 4))) AND 3)
L9  for each (s, k) in N: x[s .. s + k − 1] ← N
L10 for each (i, c) in E: x[i] ← c
L11 return x

REF-ENCODE(R, reads (p, y) sorted by p)          ▷ a reference-based delta of mapped reads
L12 out ← empty byte string; prev ← 0
L13 for each read (p, y) in order
L14     write p − prev and |y| to out; prev ← p
L15     D ← the list of (j, y[j]) with y[j] ≠ R[p + j], in order of j
L16     write |D| to out; last ← 0
L17     for each (j, b) in D: write 4(j − last) + BS(R[p + j], b) to out; last ← j

REF-DECODE(R, in, m)
L18 prev ← 0; repeat m times: read δ and ℓ from in; p ← prev + δ; prev ← p
L19     y ← R[p .. p + ℓ − 1]; read k from in; last ← 0
L20     repeat k times: read z; j ← last + ⌊z/4⌋; y[j] ← BASE(R[p + j], z mod 4); last ← j
L21     emit (p, y)
```

Lines L1 to L7 fill the packed array and the two side lists in one pass. Line L3 puts 0 in the slot of any base that is not A, C, G or T; lines L9 and L10 overwrite those slots on decoding, so the value in the slot does not matter. Line L5 merges neighbors into runs, so a gap of a million N costs one pair of integers.

Lines L12 to L17 write, for each read, the gap from the previous start, the length, the number of differences, and one integer per difference. The substitution code $BS(r, b)$ is the index of the read base $b$ in the list A, C, G, T, N with the reference base $r$ left out. Since $b \ne r$, only 4 values are possible, and 2 bits are enough. The CRAM format has the same idea: its substitution matrix gives, for each reference base, a 2-bit code to each of the other four bases, and the writer can order them by frequency. Line L17 joins the offset gap and the code into one varint, so a difference closer than 32 bases to the last one takes one byte.

**Why it is right.** Each slot of $B$ is written once, and line L8 reads it back with the same shift, so all A, C, G and T are restored. Every N lies in exactly one run of $N$, and every other non-ACGT letter is in $E$, so lines L9 and L10 restore the rest. For the reads, line L18 rebuilds $p$ as the sum of the gaps, line L19 starts from the reference bases, which are right at every offset not in $D$, and line L20 rebuilds each offset $j$ as a sum of gaps and inverts $BS$ with the reference base at that offset.

**Cost.** PACK and UNPACK take $O(n)$ time. The packed array takes $\lceil n/4 \rceil$ bytes, and the side lists take $O(1)$ words per run of N and per exception. REF-ENCODE and REF-DECODE take time linear in the total length of the reads. With 32-bit words for the counts and list entries, the packed form in the implementation takes $12 + \lceil n/4 \rceil + 8 \cdot |N| + 5 \cdot |E|$ bytes.

**Example: packing.** For $x =$ ACGTNNNNCAYG, with $n = 12$:

| bases | codes | byte |
|---|---|---|
| A C G T | 10 01 11 00 | 9C |
| N N N N | 00 00 00 00 | 00 |
| C A Y G | 01 10 00 11 | 63 |

The N list is $[(4, 4)]$ and the exception list is $[(10, \mathrm{Y})]$. Here the side lists cost more than the bases, since the string is short. On a genome they are small next to the $\lceil n/4 \rceil$ bytes of $B$.

**Example: reads.** Take the reference $R =$ ACGTACGTTAGCCATG and three mapped reads:

| read | $p$ | $y$ | $R[p .. p + \ell - 1]$ | differences | bytes |
|---|---|---|---|---|---|
| 1 | 2 | GTACTT | GTACGT | $j = 4$: G to T, $BS = 2$ | 02 06 01 12 |
| 2 | 5 | CGTTAGC | CGTTAGC | none | 03 07 00 |
| 3 | 9 | AGCAATG | AGCCATG | $j = 3$: C to A, $BS = 0$ | 04 07 01 0C |

For read 1 the reference base is G, the list without G is A, C, T, N, and T has index 2, so line L17 writes $4 \cdot 4 + 2 = 18$ = 0x12. The 20 bases take 11 bytes. On a larger test, with a fixed seed, 2000 reads of length 100 drawn from a random reference of 100,000 bases with 1 substitution per 100 bases (1979 in all) take 200,000 bytes in ASCII, 50,000 bytes in 2-bit packing, and 9,093 bytes as a reference-based delta, about 0.36 bits per base.

## Classic examples

- **The UCSC 2bit format.** It stores whole genomes for the UCSC Genome Browser tools. After a header with the signature 0x1A412743 and an index of sequence names, each sequence has its length, a list of N blocks (starts and sizes), a list of mask blocks for the lower-case letters that mark repeats, and the packed bases, with T = 00, C = 01, A = 10 and G = 11. A reader can fetch any range of bases without reading the whole file, because base $i$ is at a known byte. The format has no place for the other IUPAC codes.
- **Packed k-mers.** A [k-mer](/kmer/) with $k \le 32$ fits in one 64-bit word in 2-bit form. Tools for [k-mer counting](/kmer-counting/) and [minimizer](/minimizer/) sampling update such a word in $O(1)$ when a window moves by one base: shift left by 2 and add the new code. With the UCSC codes, the complement of a base is its code XOR 2, which makes the reverse complement of a packed k-mer a few word operations.
- **Packed references in read mappers.** [BWA](/bwa/) keeps the reference in 2-bit form and builds its [FM-index](/fm-index/) over the 4-letter alphabet. Ambiguous bases are kept in a separate list, because the index has no symbol for them.
- **CRAM.** CRAM stores reads that are aligned to a reference as a start position, given as a delta from the previous read in sorted order, and a list of read features: substitutions (with the substitution matrix code), insertions, deletions, soft clips and others, each at an offset in the read. CRAM 3.1 is a standard of the Global Alliance for Genomics and Health (GA4GH). Fritz, Leinonen, Cochrane and Birney proposed this reference-based scheme in 2011, with an option to keep quality values only where they matter.
- **FASTQ quality compression.** A FASTQ record has a name, the bases and one quality character per base, a Phred score $Q$ stored as the ASCII code $Q + 33$. The quality values have dozens of possible values and depend on the position in the read and on the values before them, so they hold far more information than the bases. Compressors such as fqzcomp of Bonfield and Mahoney model each value from the previous values and the position with [context modeling](/context-modeling/) and code it with [arithmetic coding](/arithmetic-coding/); CRAM 3.1 adds a codec of this kind. Lossy schemes reduce the values to a few levels before coding, which saves much space at a small cost in accuracy.

## Variations

- **4-bit codes.** One nibble per base covers all 15 IUPAC codes and one more symbol, with no side lists. The BAM format stores read bases this way, with = as the extra symbol for a base equal to the reference. It halves the saving of 2-bit packing but keeps random access simple.
- **Masks for case.** Soft-masked genomes mark repeats with lower-case letters. The 2bit format keeps these as a second run list, the mask blocks, in the same form as the N blocks.
- **Entropy coding of the bases.** An order-$k$ context model with arithmetic coding takes DNA below 2 bits per base on many genomes, because repeats and the base composition make some letters more likely after a given context. This loses the random access of plain packing.
- **Indels and clips.** Real alignments have insertions, deletions and clipped ends. A full reference-based format such as CRAM writes these as more feature types, each with its offset and its data, in place of the substitutions-only list of lines L15 to L17.
- **Separate streams.** CRAM and most FASTQ compressors put each field (positions, lengths, feature codes, offsets, bases, qualities, names) in its own stream and give each stream its own model or code, since the fields have very different statistics.

## Pitfalls

- **An N mask that is not used.** Line L3 stores N as the code 0, which is T. A decoder that runs line L8 but skips line L9 turns every N into T without any error. Lines L8 to L10 must run together, and a format must store $N$ and $E$ with $B$.
- **Lower case and other letters.** Line L6 rejects anything that is not an upper-case IUPAC code, and line L3 would silently store a lower-case a as T if it did not. Soft-masked input must be split into its case mask and its upper-case letters before line L2.
- **A different reference.** Line L19 copies bases from $R$. If the decoder has another version of the reference, for example another assembly of the same genome, it rebuilds wrong reads with no error. CRAM stores an MD5 checksum of each reference sequence so that a decoder can check that it has the right one.
- **Unsorted reads.** Line L14 writes $p$ minus the previous start as an unsigned varint, so the reads must be sorted by position. With unsorted reads, write the gap with a signed code, such as a zigzag code, or sort first.
- **Offsets as absolute values.** Line L20 must add $\lfloor z/4 \rfloor$ to the last offset, as line L17 wrote a gap. Reading $j \leftarrow \lfloor z/4 \rfloor$ puts the second and later differences at the wrong places.

## Exercises

1. The human reference genome has about $3.1 \times 10^9$ bases. About how many bytes does its 2-bit packed array take, and how much does that save over ASCII? *Answer:* about $7.75 \times 10^8$ bytes, a saving of about $2.3 \times 10^9$ bytes.
2. Show that with the codes T = 0, C = 1, A = 2, G = 3, the complement of a base (A and T, C and G) is its code XOR 2. Then give the operations that compute the reverse complement of a packed k-mer for $k \le 32$ in a 64-bit word.
3. The substitution code of line L17 uses 2 bits, but a read base can be any of 5 letters. Explain why 2 bits are enough, and what changes if the reference itself can hold N.
4. In the example of reads above, the third read differs from the reference at offset 3. Change it so that it also differs at offset 6, with G read as N, and give the new bytes of the read. *Answer:* the reference base G leaves A, C, T, N, so N has code 3; the offset gap is 3, so the new integer is $4 \cdot 3 + 3 = 15$, and the read is 04 07 02 0C 0F.
5. Reads of length $\ell$ have independent substitutions at rate $e$ per base. Show that the expected number of differences per read is $\ell e$, and estimate the expected bytes per read of REF-ENCODE when $\ell e$ is small and the mean gap between starts is below 128.

## References
