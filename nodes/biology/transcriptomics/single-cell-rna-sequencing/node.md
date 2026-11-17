---
tag: CV4BX3
kind: concept
slug: single-cell-rna-sequencing
name: Single-cell RNA sequencing
aliases:
- scRNA-seq
area: biology/transcriptomics
level: intro
summary: Measuring the transcripts of each cell separately with cell barcodes and unique molecular identifiers, giving a sparse cell by gene count matrix.
prereqs: [rna-sequencing, poisson-distribution]
see_also: [umi-deduplication, doublet-detection, pooling-size-factors, highly-variable-gene-selection, shared-nearest-neighbor-clustering, batch-effect-correction, trajectory-inference, negative-binomial-count-model]
sources:
  - paper: doi:10.1038/nmeth.1315
    title: Fuchou Tang et al., mRNA-Seq whole-transcriptome analysis of a single cell, Nature Methods 6(5), 377 to 382 (2009)
    locator: the sequencing of the transcriptome of one mouse blastomere
  - paper: doi:10.1016/j.cell.2015.05.002
    title: Evan Z. Macosko et al., Highly parallel genome-wide expression profiling of individual cells using nanoliter droplets, Cell 161(5), 1202 to 1214 (2015)
    locator: the Drop-seq method with barcoded beads in droplets, the dilute loading of cells, and the mixture of human and mouse cells used to count droplets with two cells
  - paper: doi:10.1038/nmeth.1778
    title: Teemu Kivioja et al., Counting absolute numbers of molecules using unique molecular identifiers, Nature Methods 9(1), 72 to 74 (2012)
    locator: the random molecular labels that let each original molecule be counted once after amplification
  - paper: doi:10.1038/nmeth.2772
    title: Saiful Islam et al., Quantitative single-cell RNA-seq with unique molecular identifiers, Nature Methods 11(2), 163 to 166 (2014)
    locator: the use of unique molecular identifiers in single-cell RNA-seq
  - paper: doi:10.15252/msb.20188746
    title: "Malte D. Luecken and Fabian J. Theis, Current best practices in single-cell RNA-seq analysis: a tutorial, Molecular Systems Biology 15(6), e8746 (2019)"
    locator: the standard workflow from quality control and normalization to clustering and trajectory analysis
---

Single-cell RNA sequencing (scRNA-seq) measures the messenger RNA of many cells one cell at a time. Each cell is put in its own small reaction, often a droplet with a bead. Every RNA molecule of that cell is copied with a short sequence that names the cell (the cell barcode) and a random sequence that names the molecule (the unique molecular identifier, or UMI). After sequencing, the reads are grouped by cell barcode, mapped to genes, and the distinct UMIs are counted. The result is a matrix with one row for each cell and one column for each gene. Most entries are zero, because each cell gives only a small sample of its molecules. Tang and co-authors (2009) sequenced the transcriptome of a single cell, and droplet methods such as Drop-seq (Macosko et al. 2015) made it possible to measure thousands of cells in one run.

## In plain words

Bulk sequencing grinds many cells together, like making a smoothie from a fruit basket: you learn the average taste, not what each fruit was. Single-cell sequencing keeps each cell apart. Each cell gets its own tiny tube with a name tag, and each message copied from it gets a second, random tag. After the reading, the name tag says which cell a message came from. The random tag lets you count each message once, even if the machine copied it many times. Each cell gives only a small part of its messages, so most counts are zero.

## The idea

**The count matrix.** For cell $i$ and gene $g$, the entry $x_{ig}$ is the number of distinct UMIs among the reads of cell $i$ that map to gene $g$. A typical cell gets counts for a few thousand of the tens of thousands of genes, so the matrix is sparse and is stored as a sparse matrix.

**Cell barcodes.** Each bead carries one barcode in many copies. A barcode with very few reads is usually an empty droplet that holds some free RNA from the solution, not a cell, so the first step separates cells from empty droplets by the number of UMIs per barcode.

**Unique molecular identifiers.** Amplification copies some molecules more than others. Two reads with the same cell barcode, gene and UMI come from one molecule, so counting UMIs instead of reads removes most of this bias (Kivioja et al. 2012, Islam et al. 2014). Sequencing errors in the UMI make false new UMIs; [UMI deduplication](/umi-deduplication/) merges them.

**Loading of cells.** Cells enter the droplets at random. If $\lambda$ is the mean number of cells per droplet, the number of cells in a droplet is close to a [Poisson variable](/poisson-distribution/) with mean $\lambda$. This is a theorem under the model: when each of $N$ cells lands in one of $D$ droplets at random, with $\lambda = N/D$ fixed and $D$ large, the count in one droplet tends to Poisson with mean $\lambda$. Among the droplets that hold at least one cell, the fraction that hold two or more is
$$\frac{1 - e^{-\lambda} - \lambda e^{-\lambda}}{1 - e^{-\lambda}} \approx \frac{\lambda}{2}$$
for small $\lambda$. So a low $\lambda$ gives few droplets with two cells, but most droplets are then empty, and few cells are measured per run. Droplets with two cells give false cell profiles that [doublet detection](/doublet-detection/) tries to find.

**Noise and depth.** The counts of one gene in cells of one type vary a lot, because each cell gives a small random sample of its molecules and the number of UMIs per cell also varies. The total count of a cell is not a biological quantity, so the counts are divided by a size factor per cell, for example from [pooling size factors](/pooling-size-factors/), and then usually taken as $\log(1 + x)$. A [negative binomial count model](/negative-binomial-count-model/) is a common description of the counts of one gene; how well it fits is a measurement on each data set.

**The usual workflow** (Luecken and Theis 2019). Quality control removes empty droplets, dying cells and doublets. Normalization divides by size factors. [Highly variable gene selection](/highly-variable-gene-selection/) keeps the informative genes. [Principal component analysis](/principal-component-analysis/) reduces to some tens of dimensions. A [nearest neighbor graph](/nearest-neighbor-graph/) of the cells is built in that space, and its communities are found with the [Louvain method](/louvain-method/) or the [Leiden algorithm](/leiden-algorithm/), as in [shared nearest neighbor clustering](/shared-nearest-neighbor-clustering/). [t-SNE](/t-sne/) and [UMAP](/umap/) draw the cells in two dimensions; these drawings are for display only, because they do not keep distances between groups. Data from several runs need [batch effect correction](/batch-effect-correction/), and continuous processes are studied by [trajectory inference](/trajectory-inference/).

## Examples

**Loading.** With $\lambda = 0.1$ cells per droplet, the Poisson model gives:

| cells in a droplet | 0 | 1 | 2 or more |
|---|---|---|---|
| fraction of droplets | 0.904837 | 0.090484 | 0.004679 |

So about 90 percent of the droplets are empty, and among the droplets with a cell, $0.004679/0.095163 = 4.917$ percent hold two or more cells. With $\lambda = 0.05$ the fraction falls to 2.479 percent, but only 4.9 percent of the droplets hold a cell. With $\lambda = 0.2$ it rises to 9.667 percent. Some of these droplets hold two cells of the same type, which look like one cell with more counts; mixing two species, as in the Drop-seq paper, makes the droplets with two cells of different species visible.

**A small count matrix.** Three cells and four genes, after UMI counting:

| cell | gene A | gene B | gene C | gene D |
|---|---|---|---|---|
| 1 | 5 | 0 | 0 | 1 |
| 2 | 0 | 3 | 0 | 0 |
| 3 | 9 | 0 | 2 | 1 |

Half of the entries are zero. Cell 3 has 12 UMIs and cell 1 has 6, so before cells 1 and 3 are compared, their counts must be scaled for this difference in depth.

## Where it is used

- Finding the cell types of a tissue, including rare types, by clustering the cells.
- Following development and differentiation with trajectory inference and RNA velocity.
- Comparing cells between conditions, such as disease and health, after batch correction.
- Building cell atlases of whole organs and organisms.

## References
