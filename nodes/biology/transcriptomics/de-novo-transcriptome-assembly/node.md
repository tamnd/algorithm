---
tag: S9ZV7H
kind: problem
slug: de-novo-transcriptome-assembly
name: De novo transcriptome assembly
aliases:
- Trinity assembly
area: biology/transcriptomics
level: advanced
summary: 'Assemble transcripts from RNA-seq reads without a genome, with de Bruijn graphs that must handle very uneven coverage and isoforms that share exons.'
prereqs: [rna-sequencing, de-bruijn-assembly]
see_also: [transcript-assembly, de-bruijn-graph, genome-assembly-problem, kmer-counting, read-error-correction, unitig, splice-graph, em-isoform-quantification]
sources:
  - paper: doi:10.1038/nbt.1883
    title: Manfred G. Grabherr, Brian J. Haas, Moran Yassour, Joshua Z. Levin, Dawn A. Thompson, Ido Amit, Xian Adiconis, Lin Fan, Raktima Raychowdhury, Qiandong Zeng, Zehua Chen, Evan Mauceli, Nir Hacohen, Andreas Gnirke, Nicholas Rhind, Federica di Palma, Bruce W. Birren, Chad Nusbaum, Kerstin Lindblad-Toh, Nir Friedman and Aviv Regev, Full-length transcriptome assembly from RNA-Seq data without a reference genome, Nature Biotechnology 29(7) (2011)
    locator: pp. 644 to 652 (Inchworm, Chrysalis and Butterfly)
  - paper: doi:10.1093/bioinformatics/bts094
    title: Marcel H. Schulz, Daniel R. Zerbino, Martin Vingron and Ewan Birney, Oases, robust de novo RNA-seq assembly across the dynamic range of expression levels, Bioinformatics 28(8) (2012)
    locator: pp. 1086 to 1092 (assemblies for several k merged into one)
  - paper: doi:10.1186/1471-2105-12-323
    title: Bo Li and Colin N. Dewey, RSEM, accurate transcript quantification from RNA-Seq data with or without a reference genome, BMC Bioinformatics 12 (2011)
    locator: Article 323 (quantification against a de novo assembly)
  - paper: doi:10.1038/nrg2484
    title: Zhong Wang, Mark Gerstein and Michael Snyder, RNA-Seq, a revolutionary tool for transcriptomics, Nature Reviews Genetics 10(1) (2009)
    locator: pp. 57 to 63 (de novo assembly for organisms without a genome)
---

De novo transcriptome assembly builds the transcripts of a sample from [RNA-seq](/rna-sequencing/) reads alone, without a reference genome. It is used for species whose genome is not sequenced or is poor, and for transcripts that the genome does not show well, such as fusions. The methods come from [de Bruijn assembly](/de-bruijn-assembly/) of genomes, but the input differs in two ways that break the usual rules. Coverage is very uneven, because the expression of genes spans several orders of magnitude, so a single coverage cutoff cannot separate errors from rare transcripts. And one gene gives several isoforms that share exons, so branches in the graph are often real and must be kept. Trinity (2011) and Oases (2012) are the classic tools.

## In plain words

You have many short pieces of text from many different messages, but no book to compare them with. You must put the pieces together into the full messages.

Two things make this harder than rebuilding one book. Some messages are copied a million times and some only a few times. A typo in a common message then appears as often as the real text of a rare one, so you cannot throw away rare pieces as typos.

Also, several messages share whole parts and differ in others. Where two pieces of text agree up to a point and then go different ways, both ways can be real. You must keep both and find out which ways go together.

## Definition

**Input.** A multiset of reads, often in pairs and often with strand information, from the transcripts of one sample, with sequencing errors. No genome.

**Output.** A set of transcript sequences such that the reads align to them, each sequence is a full-length transcript of the sample, and the isoforms of one gene are grouped.

As for [genome assembly](/genome-assembly-problem/), the last conditions cannot be checked from the input. The working formulation is graph-based. Build the [de Bruijn graph](/de-bruijn-graph/) of the [k-mers](/kmer/) of the reads, with their counts. Each transcript spells a path in this graph. Split the graph into components that hold the isoforms of one gene, or of a family of similar genes. In each component, find a small set of paths that explains the reads and their pairs. Inside one component this is the same path cover or flow problem as genome-guided [transcript assembly](/transcript-assembly/), on a graph built from the reads instead of from alignments.

## Variants

- **Strand-specific or not.** With stranded libraries, a k-mer and its reverse complement are different nodes, which separates genes that overlap on opposite strands. Without strand information, the graph must merge them.
- **Single k or many k.** A small $k$ connects transcripts of low coverage; a large $k$ separates repeats and similar genes. Oases runs several values of $k$ and merges the results.
- **Short or long reads.** Long reads that cover whole transcripts make assembly mostly a matter of grouping and correcting reads, and short reads are then used to correct the errors.
- **Single cells and metatranscriptomes.** Samples from one cell have very low and uneven coverage; samples from many species mix their transcripts.
- **Hybrid.** A draft genome or the genome of a related species can guide part of the assembly.

## Examples

**One cutoff cannot fit both genes.** Gene A is covered by 1000 reads at each base, and gene B by 3 reads. The error rate is 1 percent per base, and an error is one of the three other bases at random. At one position of A, about $1000 \cdot 0.01 / 3 \approx 3.3$ reads carry the same wrong base, so the k-mers that cover that error have about the same count as the true k-mers of B. A cutoff that removes the error k-mers of A removes all of B, and a cutoff that keeps B keeps the errors of A. This is a calculation with a simple error model, and it shows why de novo transcriptome assemblers compare a branch with its neighbours in the graph instead of using one global cutoff.

**A real bubble.** Two isoforms of one gene are $X E Y$ and $X Y$, where the exon $E$ is skipped in the second. If $X$, $E$ and $Y$ are longer than $k$, the de Bruijn graph has a branch at the end of $X$, one way through $E$ and one way directly into $Y$, and the two ways join again at the start of $Y$. A genome assembler treats such a bubble as an error or as two alleles and pops it. In a transcriptome both ways are real, and the depth of each way gives the share of each isoform.

**Repeats between isoforms.** Two isoforms $X_1 M X_2$ and $Y_1 M Y_2$ share a middle exon $M$ that is longer than the reads and fragments. No read spans $M$, so nothing in the reads tells whether $X_1$ goes with $X_2$ or with $Y_2$. The swapped pair $X_1 M Y_2$ and $Y_1 M X_2$ holds exactly the same reads as the true pair, and only different abundances of the two isoforms can make one pairing fit the counts better. This is the same ambiguity as with a repeat in genome assembly, and the same as the swapped pair on the [transcript assembly](/transcript-assembly/) page.

## Known algorithms

- **Trinity.** Grabherr and colleagues (2011) work in three steps. Inchworm counts the k-mers ($k = 25$) and extends contigs greedily from the most frequent unused k-mer. Chrysalis groups the contigs that share $k - 1$ overlaps and are linked by reads into components, often one per gene, and builds a de Bruijn graph for each component. Butterfly traces paths through each graph that the reads and the read pairs support, and reports them as isoforms.
- **Oases.** Schulz, Zerbino, Vingron and Birney (2012) build on the Velvet genome assembler. They assemble the reads with several values of $k$, find the transcripts in each graph with the help of read pairs, and merge the results, so that both rare and common transcripts are assembled.
- **General de Bruijn tools.** [k-mer counting](/kmer-counting/), [read error correction](/read-error-correction/) and the compaction of non-branching paths into [unitigs](/unitig/) are common to genome and transcriptome assemblers.

After assembly, the reads are mapped back to the transcripts to estimate their abundances, for example with RSEM, which was designed to work with or without a reference genome, by [EM quantification](/em-isoform-quantification/).

## Bounds

- **Hardness.** The exact formulations inherit the hardness of their parts. The path cover with paired constraints and the minimum flow decomposition are NP-hard even when the graph is given, as on the [transcript assembly](/transcript-assembly/) page, and the shortest-superstring style of genome assembly is NP-hard too. Practical tools are heuristics.
- **Ambiguity.** If two isoforms differ at two places that are farther apart than the longest fragment, the reads do not tell which choices go together, as in the third example. This holds for every method and is a property of the data.
- **Resources.** The k-mer table holds every distinct k-mer of the reads, including the error k-mers, which can be most of them for deep runs. Memory is often the limit, which is a measurement on real data, not a bound.

## Reductions

- **To de Bruijn graph assembly.** Within one component, the problem is genome assembly in a de Bruijn graph, but with many output paths instead of one.
- **To genome-guided transcript assembly.** Once a component graph is built, finding the isoforms is a path cover or flow decomposition problem, as for a [splice graph](/splice-graph/).
- **To abundance estimation.** With the transcripts fixed, the abundances come from [transcript abundance estimation](/transcript-abundance-estimation/).

## Applications

- Transcript sets and gene models for species without a reference genome, in ecology, evolution and agriculture.
- Expression studies in such species, by mapping the reads back to the assembled transcripts.
- Finding transcripts that the genome does not show well, such as fusion transcripts in cancer.
- Viral and microbial transcripts in mixed samples.

## References
