---
tag: 15AMY2
kind: definition
slug: open-reading-frame
name: Open reading frame
aliases:
- ORF
area: biology/gene-finding-and-motifs
level: intro
summary: A stretch of DNA in one of the six reading frames that has no stop codon inside and ends at a stop. It starts at a start codon, or in the second definition, right after the previous stop.
see_also: [orf-finding, gene-prediction, codon-adaptation-index, periodic-markov-chain-gene-model, interpolated-markov-model, genome-annotation, kmer]
sources:
  - url: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi
    title: NCBI, The Genetic Codes
    locator: table 1 (the standard code, stop codons TAA, TAG and TGA, start codons TTG, CTG and ATG) and table 11 (the bacterial, archaeal and plant plastid code, with the extra starts GTG and ATT, ATC, ATA)
  - url: https://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html
    title: EMBOSS getorf manual (Peter Rice, Ian Longden and Alan Bleasby, EMBOSS, Trends in Genetics 16(6), 2000)
    locator: the -find option, values 0 and 2 (regions between STOP codons) and 1 and 3 (regions between START and STOP codons), and -minsize (default 30 nucleotides)
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6, the sections on gene prediction (open reading frames and statistical approaches)
---

An open reading frame (ORF) is a stretch of DNA, read in one fixed frame of codons, that ends at a stop codon and has no other stop codon inside it. A cell reads a protein-coding gene in the same way: the ribosome starts at a start codon and reads three bases at a time until it meets a stop codon. A DNA sequence can be read in three frames on each strand, so it has six reading frames. Two definitions are in use. In the *start-stop* definition an ORF begins at a start codon, usually ATG. In the *stop-stop* definition it begins right after the previous stop codon in the same frame. Every gene of a bacterium is an ORF, but most ORFs are not genes, and a gene of a eukaryote with introns is not one ORF. The [ORF finding](/orf-finding/) page gives the scan that lists all ORFs, and [gene prediction](/gene-prediction/) is the harder task of deciding which ORFs are genes.

## Definition

Let $s = s_1 s_2 \cdots s_G$ be a DNA sequence over $\{A, C, G, T\}$, written 5' to 3', with positions numbered from 1. Its reverse complement $\mathrm{rc}(s)$ is the other strand, also read 5' to 3'. A *codon* is a word of three bases. The standard genetic code (NCBI table 1) maps the 64 codons to 20 amino acids and a stop signal: 61 codons are *sense codons*, and the 3 codons TAA, TAG and TGA are *stop codons*. Let $\mathrm{STOP} = \{\mathrm{TAA}, \mathrm{TAG}, \mathrm{TGA}\}$, and let $\mathrm{START}$ be a set of start codons, by default $\{\mathrm{ATG}\}$.

**Reading frame.** For a strand $t \in \{s, \mathrm{rc}(s)\}$ and an offset $f \in \{1, 2, 3\}$, the reading frame $(t, f)$ cuts $t$ into the codons $c_j = t_{f + 3j}\, t_{f + 3j + 1}\, t_{f + 3j + 2}$ for $j = 0, 1, \ldots$, as long as the codon fits in $t$. The six frames are written $+1, +2, +3$ for $t = s$ and $-1, -2, -3$ for $t = \mathrm{rc}(s)$. Two positions of $t$ are *in frame* when their distance is a multiple of 3.

**Start-stop ORF.** In a frame $(t, f)$, a start-stop ORF is a run of codons $c_a, c_{a+1}, \ldots, c_b$ with $c_a \in \mathrm{START}$, $c_b \in \mathrm{STOP}$, and $c_j \notin \mathrm{STOP}$ for $a \le j < b$. It has $b - a$ sense codons and $3(b - a + 1)$ bases with the stop codon. The start codon is the first sense codon; it encodes methionine for ATG. Some tools report every start-stop ORF; most keep, for each stop codon, only the longest one, which begins at the first start codon after the previous stop in the frame.

**Stop-stop ORF.** In a frame $(t, f)$, a stop-stop ORF is a run $c_a, \ldots, c_b$ with $c_b \in \mathrm{STOP}$, $c_j \notin \mathrm{STOP}$ for $a \le j < b$, and either $a = 0$ or $c_{a-1} \in \mathrm{STOP}$. So it is the maximal stop-free run of codons that ends at the stop codon $c_b$. It has $b - a$ sense codons, and it does not need a start codon.

**Length.** The length of an ORF is its number of sense codons, or its number of bases; say which. Tools add a minimum length, for example 30 bases in EMBOSS getorf or 100 codons in many genome papers. The minimum is a choice of the user, not part of the definition.

**End of the sequence.** A run of codons that reaches the 3' end of $t$ with no stop codon is not an ORF under these definitions, because it has no end. Tools that work on fragments or contigs report it as a *partial* ORF. On a circular genome, the frame continues across the origin.

**Facts that follow from the definitions.**

1. Each stop codon $c_b$ of a frame ends exactly one stop-stop ORF. So the stop-stop ORFs of $s$ are in one-to-one correspondence with the stop codons of the six frames, and there are at most $6 \lfloor G/3 \rfloor$ of them.
2. Each start-stop ORF lies inside exactly one stop-stop ORF, the one that ends at the same stop codon. A stop-stop ORF contains a start-stop ORF if and only if it contains a start codon, and the longest of these starts at its first start codon.
3. Two ORFs of the same frame and strand never overlap unless they end at the same stop codon. ORFs of different frames, or of different strands, can overlap.
4. In a random sequence with independent, uniform bases, the codons of one frame are independent, and each is a stop codon with probability $3/64$. So the number $K$ of sense codons before the first stop satisfies $P(K \ge k) = (61/64)^k$, with mean $61/3 \approx 20.3$. For $k = 100$ this is $0.0082$, and one megabase of random DNA has about 771 stop-stop ORFs of at least 100 sense codons in its six frames. At a GC content of 60 percent, the stop probability falls to $0.032$ and $P(K \ge 100)$ rises to $0.039$, so long ORFs by chance are more common in GC-rich genomes, whose stop codons are rarer.

Fact 4 is why a length cutoff works at all: a long ORF is unlikely by chance, so it is a candidate gene. The cutoff of 100 codons is a rule of thumb. It misses real short genes, and in a GC-rich genome it lets through many chance ORFs, often on the strand opposite a real gene.

## Examples and non-examples

Take the 28 bases $s = \mathrm{ATGAAATGGTAATTACTTCATGCATTAG}$ with the start set $\{\mathrm{ATG}\}$. Its reverse complement is $\mathrm{CTAATGCATGAAGTAATTACCATTTCAT}$. The translations of the six frames, with $*$ for a stop codon, are:

| frame | translation |
|---|---|
| $+1$ | M K W * L L H A L |
| $+2$ | * N G N Y F M H * |
| $+3$ | E M V I T S C I |
| $-1$ | L M H E V I T I S |
| $-2$ | * C M K * L P F H |
| $-3$ | N A * S N Y H F |

The start-stop ORFs (positions on $s$, from 1, with the stop codon included) are:

- frame $+1$, bases 1 to 12, ATG AAA TGG TAA, the peptide MKW with 3 sense codons;
- frame $+2$, bases 20 to 28, ATG CAT TAG, the peptide MH with 2 sense codons;
- frame $-2$, bases 13 to 21 of $s$, read on the other strand as ATG AAG TAA, the peptide MK with 2 sense codons.

The stop-stop ORFs give more. In frame $+2$, the stop-stop ORF that ends at the TAG at bases 26 to 28 begins right after the TGA at bases 2 to 4, so it covers bases 5 to 28 and has the 7 sense codons NGNYFMH. The start-stop ORF MH sits at its end, since its first ATG is at base 20. In frame $-2$, the stop-stop ORF that ends at TAA has the 3 sense codons CMK, one more than the start-stop ORF MK. In frame $+1$ the ORF begins at the first codon of the frame, so both definitions give MKW. The codon TGA at the start of frame $+2$ is a stop-stop ORF with 0 sense codons; tools drop it with any minimum length.

Non-examples:

- The frame $+1$ codons after TAA, L L H A L, reach the end of $s$ without a stop codon. They are not an ORF; a tool for contigs reports them as a partial ORF.
- Frame $+3$ has the start codon ATG at bases 6 to 8 and no stop codon after it. It is not an ORF.
- In ATG AAA TAA GGG TGA, the run from ATG to TGA is not an ORF, because TAA is an in-frame stop inside it. The ORF that starts at ATG ends at TAA.
- In ATG AAT AAG GGT GA, the bases TAA at positions 6 to 8 do not stop the frame of the ATG, because they are not in frame with it. The frame of ATG reads ATG, AAT, AAG, GGT and then only two bases, so it has no stop codon.
- A human gene with introns is not one ORF. Its coding exons together form an ORF only after splicing, in the mRNA. In the genome, the reading frame runs into introns, which often hold in-frame stop codons. [Gene prediction](/gene-prediction/) and the [GHMM gene finder](/generalized-hmm-gene-finder/) handle this case.

## Related definitions

- **Codon and genetic code.** The genetic code is the map from codons to amino acids. NCBI lists more than 25 codes. Table 1 is the standard code. Table 11, for bacteria, archaea and plant plastids, has the same stops but more start codons; GTG and TTG start many bacterial genes. A vertebrate mitochondrion uses table 2, where TGA codes for tryptophan and AGA and AGG are stops. An ORF depends on the code.
- **Coding sequence (CDS).** The part of a gene that is translated, from the start codon of the protein to the stop. In a bacterium it is one start-stop ORF, but it does not always begin at the first start codon of the ORF; finding the true start needs a ribosome binding site or other signals. In a eukaryote it is split over exons.
- **Frameshift.** An insertion or a deletion whose length is not a multiple of 3 moves all later codons to another frame. In sequence data it cuts an ORF into pieces in two frames.
- **Upstream ORF and small ORF.** An upstream ORF is a short ORF in the 5' untranslated region of an mRNA, before the main coding sequence. A small ORF is an ORF below the usual cutoff, for example under 100 codons, that is translated. Both are cases where the length rule of thumb fails.
- **Codon statistics.** Coding ORFs differ from chance ORFs in their codon usage and in the base composition at each codon position. The [codon adaptation index](/codon-adaptation-index/) scores codon usage, and the [three-periodic Markov chain](/periodic-markov-chain-gene-model/) and the [interpolated Markov model](/interpolated-markov-model/) score the bases of each frame. These models turn the list of ORFs into a list of genes.
- **ORF finding.** The [six-frame scan](/orf-finding/) lists all ORFs of a sequence of length $G$ in $O(G)$ time. The words of three bases it reads are the 3-[mers](/kmer/) of the sequence at the positions of one frame.

## References
