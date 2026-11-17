---
tag: V69TNX
kind: definition
slug: sam-alignment-format
name: SAM alignment format
aliases:
- Sequence Alignment/Map format
- BAM format
- CIGAR string
area: biology/read-mapping-and-variant-calling
level: intro
summary: A tab-separated text format with one line per alignment of a read to a reference, giving the position, strand flags, CIGAR string, mapping quality, mate and sequence.
prereqs: [read-mapping, phred-quality-score]
see_also: [mapping-quality, paired-end-read-mapping, read-pileup, duplicate-read-marking, variant-call-format, run-length-encoding, bwa, minimap2]
sources:
  - paper: doi:10.1093/bioinformatics/btp352
    title: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer, Gabor Marth, Goncalo Abecasis, Richard Durbin and 1000 Genome Project Data Processing Subgroup, The Sequence Alignment/Map format and SAMtools, Bioinformatics 25(16), 2009
    locator: pp. 2078 to 2079 (the SAM and BAM formats, the binning index and the SAMtools tools)
  - url: https://samtools.github.io/hts-specs/SAMv1.pdf
    title: The SAM/BAM Format Specification, version 1.6, hts-specs
    locator: Section 1.4 (the eleven mandatory fields, the FLAG bits and the CIGAR operations), Section 1.1 (the worked example), Section 1.5 (optional fields) and Section 4 (BAM)
---

The SAM (Sequence Alignment/Map) format stores the result of [read mapping](/read-mapping/): for each read, where it aligns on a reference genome, on which strand, with which gaps, and how sure the aligner is. A SAM file is plain text, with header lines that name the reference sequences and the programs that made the file, followed by one tab-separated line per alignment. BAM is the same records in a compressed binary form, and an index of a sorted BAM file lets a program read only the records that overlap a region. The format was defined for the 1000 Genomes Project by Li et al. (2009) and is kept in the hts-specs repository; this page follows version 1.6 of the specification.

## Definition

Positions are 1-based in SAM text, as in the specification, and a range $[a, b]$ includes both ends.

**Record.** An alignment line has eleven mandatory fields, separated by tabs, followed by any number of optional fields.

| # | field | meaning |
|---|---|---|
| 1 | QNAME | the name of the read or the read pair |
| 2 | FLAG | a bitwise set of yes or no properties, below |
| 3 | RNAME | the name of the reference sequence, `*` if unmapped |
| 4 | POS | the 1-based leftmost reference position of the first aligned base |
| 5 | MAPQ | the [mapping quality](/mapping-quality/), $-10 \log_{10}$ of the probability that the position is wrong, 255 if not available |
| 6 | CIGAR | the alignment as a list of operations, below |
| 7 | RNEXT | the reference of the mate, `=` if the same |
| 8 | PNEXT | the position of the mate |
| 9 | TLEN | the observed template length, signed |
| 10 | SEQ | the read bases, on the forward strand of the reference |
| 11 | QUAL | the base qualities, each as the ASCII code $Q + 33$ of its [Phred score](/phred-quality-score/) |

A read is stored in the orientation of the reference: if it maps to the reverse strand, SEQ and QUAL hold its reverse complement and its reversed qualities, and flag 0x10 is set.

**FLAG bits.**

| bit | meaning |
|---|---|
| 0x1 | the template has more than one segment (the read is paired) |
| 0x2 | each segment is properly aligned according to the aligner |
| 0x4 | this segment is unmapped |
| 0x8 | the next segment is unmapped |
| 0x10 | SEQ is reverse complemented |
| 0x20 | SEQ of the next segment is reverse complemented |
| 0x40 | the first segment of the template |
| 0x80 | the last segment of the template |
| 0x100 | a secondary alignment |
| 0x200 | the read fails quality checks |
| 0x400 | a PCR or optical duplicate |
| 0x800 | a supplementary alignment |

**CIGAR string.** A CIGAR string is a [run-length encoding](/run-length-encoding/) of the alignment: a list of pairs (length, operation). The operations are:

| op | meaning | consumes read | consumes reference |
|---|---|---|---|
| M | alignment match, which may be a sequence match or a mismatch | yes | yes |
| I | insertion to the reference | yes | no |
| D | deletion from the reference | no | yes |
| N | skipped region of the reference, such as an intron | no | yes |
| S | soft clip: bases present in SEQ but not aligned | yes | no |
| H | hard clip: bases not present in SEQ | no | no |
| P | padding, a silent deletion from a padded reference | no | no |
| = | sequence match | yes | yes |
| X | sequence mismatch | yes | yes |

The sum of the lengths of M, I, S, = and X must equal the length of SEQ. The *reference span* of a record is the sum of the lengths of M, D, N, = and X, so the record covers the reference positions $[\mathrm{POS}, \mathrm{POS} + \text{span} - 1]$.

**Optional fields.** Each has the form `TAG:TYPE:VALUE`, for example `NM:i:1` for an edit distance of 1 to the reference, `MD:Z:...` for the reference bases at mismatches and deletions, `RG:Z:...` for the read group, and `SA:Z:...` for the other parts of a chimeric alignment.

**BAM.** BAM stores the same records in binary, with integers in place of text, in blocks compressed by BGZF, a variant of gzip ([DEFLATE](/deflate/)) with blocks of at most 64 KiB. Positions in BAM are 0-based. A BAM file sorted by position can be indexed, and the index maps regions of the genome to file offsets, so a viewer or a caller reads only the blocks of a region.

## Examples and non-examples

The specification gives this example on the reference `AGCATGTTAGATAAGATAGCTGTGCTAGTAGGCAGTCAGCGCCAT` of 45 bases (the header and some fields are left out).

| QNAME | FLAG | POS | MAPQ | CIGAR | RNEXT | PNEXT | TLEN | SEQ |
|---|---|---|---|---|---|---|---|---|
| r001 | 99 | 7 | 30 | 8M2I4M1D3M | = | 37 | 39 | TTAGATAAAGGATACTG |
| r002 | 0 | 9 | 30 | 3S6M1P1I4M | * | 0 | 0 | AAAAGATAAGGATA |
| r003 | 0 | 9 | 30 | 5S6M | * | 0 | 0 | GCCTAAGCTAA |
| r004 | 0 | 16 | 30 | 6M14N5M | * | 0 | 0 | ATAGCTTCAGC |
| r003 | 2064 | 29 | 17 | 6H5M | * | 0 | 0 | TAGGC |
| r001 | 147 | 37 | 30 | 9M | = | 7 | -39 | CAGCGGCAT |

**Reading r001.** The CIGAR string 8M2I4M1D3M uses $8 + 2 + 4 + 3 = 17$ read bases, which is the length of SEQ, and $8 + 4 + 1 + 3 = 16$ reference bases, so the read covers positions 7 to 22. The first 8 read bases TTAGATAA align to reference positions 7 to 14, the next 2 bases AG are not in the reference, GATA aligns to 15 to 18, the reference base at 19 is deleted from the read, and CTG aligns to 20 to 22. The flag $99 = 0x1 + 0x2 + 0x20 + 0x40$ says: paired, properly paired, the mate is on the reverse strand, and this is the first read.

**Reading the mate.** The second r001 line has flag $147 = 0x1 + 0x2 + 0x10 + 0x80$: paired, properly paired, this read is on the reverse strand, and it is the last read. Its 9M covers 37 to 45. The template spans 7 to 45, which is 39 bases, so TLEN is $+39$ on the leftmost read and $-39$ on the other.

**A spliced read.** r004 has 6M14N5M: 6 bases at 16 to 21, then 14 skipped reference bases at 22 to 35, then 5 bases at 36 to 40. The span is 25, and the read has 11 bases. A [spliced read aligner](/spliced-read-alignment/) writes such records for RNA reads that cross an intron.

**A chimeric read.** r003 aligns in two parts. The first record has 5S6M at 9: the first 5 bases are soft clipped, so they stay in SEQ. The second record has flag $2064 = 0x800 + 0x10$, a supplementary alignment on the reverse strand at 29, with 6H5M: the 6 clipped bases are hard clipped and are not in its SEQ. The tag `SA:Z:ref,29,-,6H5M,17,0;` on the first record points to the second.

**Non-example: M is not a match.** The operation M only says that a read base is aligned to a reference base. In r001's mate, `CAGCGGCAT` against the reference `CAGCGCCAT` has one mismatch inside 9M, which the tag `NM:i:1` records. Only the operations = and X tell matches from mismatches; most aligners write M.

**Non-example: SEQ is not always the read as sequenced.** For a record with flag 0x10, SEQ is the reverse complement of the bases the sequencer read, and QUAL is reversed. Tools that need the sequencing order, such as the cycle covariate of [base quality score recalibration](/base-quality-score-recalibration/), must undo this.

**Non-example: POS is not the 5' end.** POS is the leftmost aligned base, after soft clips. For a reverse-strand read the 5' end is at the right, and soft clips also move it. [Duplicate marking](/duplicate-read-marking/) uses the unclipped 5' end, which it computes from POS and the CIGAR string.

## Related definitions

- **CIGAR string.** Field 6 of a record, defined above. The alias names one field of the format, not the format.
- **BAM.** The binary, compressed form of SAM, defined above. CRAM is a third form that stores only the differences from a reference sequence, which makes the files smaller.
- **Mapping quality.** Field 5; see [mapping quality](/mapping-quality/).
- **Template and mates.** The fields RNEXT, PNEXT, TLEN and the flags 0x1 to 0x80 describe [paired-end](/paired-end-reads/) reads; see [paired-end read mapping](/paired-end-read-mapping/).
- **Pileup.** Reading the records of a sorted file column by column gives the [read pileup](/read-pileup/) that variant callers use.
- **VCF.** The format for the variants that are called from the alignments; see [variant call format](/variant-call-format/).

## References
