---
tag: AD4KKT
kind: problem
slug: genome-annotation
name: Genome annotation
aliases:
- structural genome annotation
area: biology/gene-finding-and-motifs
level: core
summary: Mark the genes, repeats, non-coding RNAs and regulatory elements of an assembled genome and give the genes their likely functions.
prereqs: [gene-prediction, repeat-masking, homology-based-function-transfer]
see_also: [spliced-alignment-problem, comparative-gene-finding, generalized-hmm-gene-finder, profile-hmm, covariance-model, hmmer, rna-sequencing, transcript-assembly]
sources:
  - paper: doi:10.1038/nrg3174
    title: Mark Yandell and Daniel Ence, A beginner's guide to eukaryotic genome annotation, Nature Reviews Genetics 13(5), 2012
    locator: pp. 329 to 342; the stages of eukaryotic annotation (repeats, evidence alignment, gene prediction, synthesis of gene models, quality control and functional annotation)
  - paper: doi:10.1101/gr.6743907
    title: Brandi L. Cantarel, Ian Korf, Sofia M. C. Robb, Genis Parra, Eric Ross, Barry Moore, Carson Holt, Alejandro Sánchez Alvarado and Mark Yandell, MAKER, an easy-to-use annotation pipeline designed for emerging model organism genomes, Genome Research 18(1), 2008
    locator: pp. 188 to 196; a pipeline that runs RepeatMasker, BLAST, SNAP and Exonerate and joins their results into gene models, tested on C. elegans and S. mediterranea
  - paper: doi:10.1186/1471-2105-10-67
    title: Karen Eilbeck, Barry Moore, Carson Holt and Mark Yandell, Quantitative measures for the management and comparison of annotated genomes, BMC Bioinformatics 10, 2009, article 67
    locator: measures of the change between annotation releases and of the agreement between a gene model and its evidence, applied to five eukaryotic genomes
---

Genome annotation is the task of marking the functional parts of an assembled genome: the protein-coding genes with their exons, introns and untranslated ends, the non-coding RNA genes, the repeats and transposons, and sometimes the regulatory elements, and then giving each gene a likely function. The first part is often called structural annotation and the second functional annotation. Unlike [gene prediction](/gene-prediction/) under a fixed model, annotation has no single objective function and no optimal answer: it is a pipeline of many tools whose results are joined by rules and checked against evidence. Its quality is measured, gene by gene, against transcripts, proteins and curated reference sets.

## In plain words

A new genome sequence is a few hundred million letters with no labels. Annotation is the work of writing the labels. First, find the parts that are copies of known repeats, and hide them, so that they do not confuse the later steps. Then line up every piece of outside evidence with the genome: RNA from the same species, which shows which parts are copied into messages, and proteins from other species, which show where similar genes lie. Run gene finders that look only at the letters. Join all this into one best guess for each gene, and score each guess by how well the evidence supports it. Last, compare each gene with genes that are already understood, and copy over a name and a function where the match is good.

## Definition

**Input.**
- An assembled genome: a set of contigs or chromosomes $G$, of total length $n$.
- Evidence: RNA-seq reads or assembled transcripts of the same species, ESTs or full-length cDNAs, proteins of related species, and, where available, a related annotated genome.
- Libraries and models: a library of repeat families, models of non-coding RNA families, protein family models, and trained gene finders for the species or a close one.

**Output.**
- A set of features, each with a location on $G$ (contig, start, end, strand) and a type: gene, mRNA, exon, CDS, UTR, tRNA, rRNA, other non-coding RNA, repeat, pseudogene. The usual file format is GFF3, which links the features into a tree (gene, its transcripts, their exons).
- For each protein-coding gene, one or more transcripts with a coding sequence that translates without internal stops.
- Functional labels: a name, protein domains, Gene Ontology terms and enzyme numbers, each with the evidence it came from.
- A quality score for each gene model.

**The question.** There is no formal question with one correct answer. A good annotation agrees with the biology, which is not known in full. In practice, each gene model should be supported by evidence where evidence exists, consistent with the gene model of the species, and conservative where there is no evidence. Different pipelines, run on the same genome, give different gene sets, and the differences are not errors of one tool but different choices.

## Variants

- **Prokaryotic annotation.** Genes have no introns, and most of the genome codes for protein. The core step is [ORF finding](/orf-finding/) with a coding model, plus tRNA and rRNA detection. It is fast and quite accurate; the hard parts are start codons and short genes.
- **Eukaryotic annotation.** Genes have introns, alternative splicing, long untranslated ends, and lie in a sea of repeats. The pipeline is longer, and evidence from RNA matters much more.
- **Re-annotation.** An existing annotation is updated with new evidence or a new assembly. The measure here is the change between releases, gene by gene.
- **Annotation transfer.** The genes of a related, well-annotated assembly are moved to the new one by whole-genome alignment, then checked and completed.
- **Functional annotation only.** The gene models are given, and only the functions are assigned, mostly by [homology-based function transfer](/homology-based-function-transfer/) and by protein family models.
- **Regulatory annotation.** Promoters, enhancers and other elements are marked from chromatin assays, conservation ([phylogenetic footprinting](/phylogenetic-footprinting/)) or sequence models such as a [convolutional regulatory sequence model](/convolutional-regulatory-sequence-model/). This is usually a separate step from gene annotation.

## Examples

**Scoring a gene model against its evidence.** Let a predicted transcript have three exons, at [101, 250], [401, 520] and [701, 900] (470 bases), and let the aligned transcript evidence have exons at [101, 250], [401, 540] and [701, 850] (440 bases). They share $150 + 120 + 150 = 420$ bases. Define the sensitivity as the shared length over the evidence length and the specificity as the shared length over the prediction length:

$$\mathrm{SN} = \frac{420}{440} = 0.9545, \qquad \mathrm{SP} = \frac{420}{470} = 0.8936.$$

Their mean is the congruence $C = 0.9241$, and the annotation edit distance used by MAKER is $\mathrm{AED} = 1 - C = 0.076$. An AED of 0 means perfect agreement and 1 means no overlap. At the exon level, only the first of the three exons matches exactly, so the exon-level sensitivity is $1/3$. The same pair of models thus looks good at the base level and poor at the exon level, which is why reports give both.

**A typical eukaryotic pipeline.** For a new animal genome, a pipeline in the style of MAKER does the following:
1. Build a library of the repeat families of the genome, and mask them ([repeat masking](/repeat-masking/)); simple repeats are found by [tandem repeat finding](/tandem-repeat-finding/).
2. Align RNA-seq reads with a [spliced read aligner](/spliced-read-alignment/), and assemble them into transcripts ([transcript assembly](/transcript-assembly/)).
3. Align proteins of related species to the masked genome, first with [BLAST](/blast/) to find the regions, then with a spliced protein aligner ([spliced alignment](/spliced-alignment-problem/)) to get the exons.
4. Run one or more *ab initio* gene finders ([generalized HMMs](/generalized-hmm-gene-finder/)), trained on the species, and feed them the evidence as hints.
5. Choose, for each locus, the gene model that agrees best with the evidence, and record its AED.
6. Search the proteins against protein family databases built from [profile HMMs](/profile-hmm/) with [HMMER](/hmmer/), and against curated proteins; transfer names and functions.
7. Search the genome for non-coding RNA families with [covariance models](/covariance-model/), and for tRNAs with dedicated tools.

## Known algorithms

Genome annotation is solved by pipelines, not by one algorithm. The steps and their methods:

| step | method | page |
|---|---|---|
| repeats | library search by local alignment, de novo family discovery | [repeat masking](/repeat-masking/) |
| simple repeats | k-tuple detection and wraparound alignment | [tandem repeat finding](/tandem-repeat-finding/) |
| RNA evidence | spliced read mapping and transcript assembly | [spliced read alignment](/spliced-read-alignment/), [transcript assembly](/transcript-assembly/) |
| protein evidence | seed search, then spliced alignment | [BLAST](/blast/), [spliced alignment](/spliced-alignment-problem/) |
| gene models | GHMM parse with hints, comparative models | [generalized HMM gene finder](/generalized-hmm-gene-finder/), [comparative gene finding](/comparative-gene-finding/) |
| synthesis | rules or weighted votes over the evidence | (pipeline specific) |
| functions | best hits and protein family models | [homology-based function transfer](/homology-based-function-transfer/), [profile HMM](/profile-hmm/) |
| non-coding RNA | covariance models of RNA families | [covariance model](/covariance-model/), [RNA homology search](/rna-homology-search/) |

**MAKER (Cantarel et al. 2008).** MAKER runs RepeatMasker, BLAST, the gene finder SNAP and the aligner Exonerate, and joins their outputs into gene models with evidence attached. The paper tests it on the well-annotated *C. elegans* genome and on the new genome of the planarian *S. mediterranea*. Its design goal is that a small group can annotate a new genome without building its own pipeline.

**The synthesis step.** Tools that join evidence into gene models use rules (prefer models that agree with transcripts), weighted votes (each source gives a weight to each candidate exon, and a dynamic program picks the best chain, as in [exon chaining](/exon-chaining/)), or a gene finder that takes the evidence as extra scores. All of them are heuristics: their weights are set by hand or fit on a training set.

## Bounds

The problem has no objective, so it has no complexity bound of its own. The cost of a pipeline is the sum of the costs of its steps, and a few steps dominate:
- **Alignment of evidence.** Mapping $N$ reads costs about $O(N \ell)$ after an index of the genome is built in $O(n)$ time, for reads of length $\ell$. Spliced alignment of proteins costs $O((L + b) m)$ per protein and region, where $L$ is the length of the candidate blocks, $b$ their number and $m$ the protein length; a seed search first limits the regions.
- **Gene finding.** A GHMM parse costs $O(n)$ times a factor that depends on the number of states and the length limits of exons.
- **Non-coding RNA search.** A covariance model scan with CYK costs $O(M W^2 + B W^3)$ per window of length $W$ for a model with $M$ states and $B$ bifurcations; this makes a whole-genome scan with many RNA families slow, so filters are run first.
- **Repeats.** A library search costs one local alignment search per family; the de novo discovery of repeat families is often the slowest step for a large plant genome.

On a large genome, the run time is measured in CPU days, and it is a measurement, not a bound.

## Reductions

- **To gene prediction.** With no evidence, structural annotation of protein-coding genes reduces to [gene prediction](/gene-prediction/) on the masked genome.
- **To spliced alignment.** With a full-length transcript or a close protein for every gene, the gene models are the solutions of the [spliced alignment problem](/spliced-alignment-problem/) for each one.
- **To exon chaining.** The synthesis of candidate exons from many sources, each with a weight, is an instance of [exon chaining](/exon-chaining/) in its simplest form.
- **Functional annotation to search.** Assigning functions reduces to similarity search against annotated proteins and families, followed by the rules of [homology-based function transfer](/homology-based-function-transfer/). Its errors depend on the database: Schnoes and colleagues (2009) measured misannotation rates of 5 to 63 percent on average across six enzyme superfamilies in three large databases, against near 0 percent for most families in Swiss-Prot.

## Applications

- **Every genome project.** The genome is used through its annotation: gene lists, protein sets, comparative studies and the design of experiments all start from it.
- **Gene expression studies.** RNA-seq reads are counted per gene and per transcript of the annotation; errors in the models become errors in the counts.
- **Variant interpretation.** A variant is called coding, splice-site or intronic from the annotation, so the effect of a variant depends on which annotation is used.
- **Evolution studies.** Gene family sizes, gene gain and loss, and selection tests are computed on annotated genes, and differences in annotation quality between species can mimic biology.

**Pitfalls in use.**
- **Unmasked repeats** produce many false genes from transposon open reading frames.
- **Fragmented assemblies** split genes across contigs; a gene that crosses a gap is annotated as two partial genes.
- **Over-transfer of functions.** A function copied from a protein that was itself annotated by similarity can be wrong, and the error then spreads to new genomes.
- **Comparing annotations.** Two annotations differ in their definitions (which transcripts are kept, how UTRs are drawn), so a count of genes is not comparable between pipelines without the same rules.

## References
