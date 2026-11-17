---
tag: WZKYKW
kind: algorithm
slug: doublet-detection
name: Doublet detection
aliases:
- Scrublet
- doublet scoring
area: biology/transcriptomics
level: advanced
summary: Flag barcodes that hold two cells by simulating artificial doublets from pairs of cells and scoring each barcode by its doublet neighbors.
model: real-ram
complexity:
  vars: {n: the number of cells, d: the number of genes, p: the number of principal components}
  time: {worst: O(n^2 (p + log n) + n d^2 + d^3)}
  space: {extra: O(n^2 + n d + d^2)}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2019
  people: [Samuel L. Wolock, Romain Lopez, Allon M. Klein]
  note: Scrublet (Wolock, Lopez and Klein 2019) and DoubletFinder (McGinnis, Murrow and Gartner 2019) both score cells against simulated doublets in a reduced space.
prereqs: [principal-component-analysis, k-nearest-neighbor-graph]
see_also: [single-cell-rna-sequencing, k-nearest-neighbor-graph, nearest-neighbor-graph, principal-component-analysis, bayes-theorem, shared-nearest-neighbor-clustering, umap, umi-deduplication]
sources:
  - paper: doi:10.1016/j.cels.2018.11.005
    title: Samuel L. Wolock, Romain Lopez and Allon M. Klein, Scrublet, computational identification of cell doublets in single-cell transcriptomic data, Cell Systems 8(4) (2019), 281-291
    locator: the simulation of doublets, the k-nearest-neighbor classifier with the adjusted k, and the doublet score with the expected doublet rate
  - paper: doi:10.1016/j.cels.2019.03.003
    title: Christopher S. McGinnis, Lyndsay M. Murrow and Zev J. Gartner, DoubletFinder, doublet detection in single-cell RNA sequencing data using artificial nearest neighbors, Cell Systems 8(4) (2019), 329-337
    locator: the proportion of artificial nearest neighbors as a doublet score
  - paper: doi:10.1016/j.cell.2015.05.002
    title: Evan Z. Macosko et al., Highly parallel genome-wide expression profiling of individual cells using nanoliter droplets, Cell 161(5) (2015), 1202-1214
    locator: the mixed species experiment that measures the rate of barcodes with two cells
---

Doublet detection finds the barcodes of a single-cell experiment that hold two cells. In droplet methods, cells enter droplets at random, so some droplets get two cells, and their reads share one cell barcode. Such a doublet looks like a cell with a mixed profile, and it can appear as a false intermediate state or a false new type. Scrublet (Wolock, Lopez and Klein 2019) makes artificial doublets by adding the counts of random pairs of observed cells, puts the real and the artificial profiles in one [principal component](/principal-component-analysis/) space, and scores each cell by the fraction of artificial doublets among its nearest neighbors. Bayes' rule with the expected doublet rate turns this fraction into a probability. The method is a heuristic. It finds doublets of two different cell types well and doublets of one type poorly, and the tests measure both. It uses a [k-nearest-neighbor graph](/k-nearest-neighbor-graph/) as a classifier: the labels of the neighbors give the score. This is a different use from [graph clustering](/shared-nearest-neighbor-clustering/), where the graph is cut into groups.

## In plain words

Some barcodes hold two cells, and you cannot see that from one barcode alone. But you can make fake doublets yourself: pick two real cells at random and add their counts. Now put the real cells and the fake doublets together and look at the neighborhood of each real cell. A normal cell lives among other normal cells of its type. A real doublet of two types looks like the fake doublets made from those two types, so many of its neighbors are fake doublets. Count the fake neighbors and turn the count into a probability, using how many doublets you expect. Then pick a cutoff in the valley between the low and the high scores of the fake doublets. A doublet of two cells of the same type looks like a normal cell, and no method of this kind can find it.

## The problem

**Input.** A matrix of raw counts, $n$ cells by $d$ genes, usually after the choice of [highly variable genes](/highly-variable-gene-selection/). The ratio $r$ of simulated doublets to observed cells, the expected doublet rate $\rho$, the number of neighbors $k$ and the number of components $p$.

**Output.** A doublet score in $(0, 1)$ for each cell, and a call for each cell: doublet or singlet.

**Model.** A doublet has the sum of the counts of two cells. A cell is a doublet with prior probability $\rho$. The scores rest on the assumption that the simulated doublets have the same distribution as the real ones. The real doublet rate depends on the number of cells loaded; the [single-cell RNA-seq](/single-cell-rna-sequencing/) page gives the Poisson calculation.

## The algorithm

```pseudo id=main
SCRUBLET(X, r, ρ, k, p)                ▷ X: n cells by d genes, raw counts
L1  for i ← 1 to r n do pick cells a, b at random; y_i ← x_a + x_b
L2  scale each observed and simulated profile to the mean total of the observed cells
L3  standardize each gene with the mean and standard deviation of the observed cells
L4  fit p principal components on the observed cells; project all profiles on them
L5  k_adj ← round(k (1 + r))
L6  for each profile, find its k_adj nearest neighbors among all (1 + r) n profiles
L7      q ← (the number of simulated neighbors + 1) / (k_adj + 2)
L8      score ← q ρ / r / (1 - ρ - q (1 - ρ - ρ/r))
L9  t ← the valley of the histogram of the scores of the simulated doublets
L10 return the scores, and call each observed cell with score > t a doublet
```

Line L1 picks the two cells uniformly and independently, so a pair can repeat a cell, as in Scrublet. The simulated doublets use the raw counts, and line L2 removes the larger total of a doublet, so only its mixed composition stays. Lines L3 and L4 use statistics of the observed cells only and apply them to the simulated ones, which puts both sets in the same space. Line L5 grows $k$ so that each profile still has about $k$ observed neighbors. Line L7 is the fraction of simulated neighbors with one pseudo count on each side. Line L8 is Bayes' rule with the prior $\rho$, as the correctness section shows. Line L9 uses the simulated doublets because they have two modes: doublets of two types score high, and doublets of one type score near the prior.

Scrublet defaults to $r = 2$, $\rho = 0.1$, $k = \operatorname{round}(0.5\sqrt n)$ and 30 components, and it selects variable genes and fits the components with a fast solver. The code here takes the genes as given, uses a brute-force neighbor search and a full eigendecomposition, and defaults to 10 components for small test data.

## Example

Take $\rho = 0.1$, $r = 2$ and $k_{adj} = 15$. A cell has $q = (n_d + 1)/17$.

| simulated neighbors $n_d$ | $q$ | score |
|---|---|---|
| 0 | 0.0588 | 0.00346 |
| 4 | 0.2941 | 0.0226 |
| 10 | 0.6471 | 0.0924 |
| 15 | 0.9412 | 0.4706 |

The score is $\frac{q\rho/r}{(q\rho/r) + (1 - \rho)(1 - q)}$. For $n_d = 10$ the numerator is $0.6471 \cdot 0.05 = 0.03235$ and the second term is $0.9 \cdot 0.3529 = 0.3176$, so the score is $0.03235/0.3500 = 0.0924$, close to the prior 0.1. This is expected: two thirds of all profiles are simulated, and $q = 0.6471$ is near $2/3$, so the neighborhood has the global mix and the score stays near $\rho$. Only a neighborhood with nearly all simulated neighbors gives a high score, and even with all 15 neighbors simulated the score is $0.4706$, because the pseudo counts keep $q$ below 1. The scores are on a low scale, which is why the threshold comes from the data at line L9 and not from a fixed value such as 0.5.

In a simulation with three cell types, 150 singlets, 15 doublets of two types and 10 doublets of one type, the scores of the heterotypic doublets were above those of the singlets in every pair, and the threshold of line L9 called all 15 of them and no singlet. The 10 homotypic doublets had scores like the singlets and none was called. These numbers are measured, not proved.

## Correctness

No method can be shown to find the doublets, so the [proof](proofs/correctness.md) shows what the score means. If the observed neighbors of a point estimate the density of singlets there and the simulated neighbors estimate the density of doublets, then line L8 is exactly the posterior probability of a doublet by [Bayes' theorem](/bayes-theorem/), with prior $\rho$. The score is strictly increasing in $q$, lies in $(0, 1)$, and equals $\rho$ when the neighborhood has the global share $r/(1 + r)$ of simulated profiles. The choice $k_{adj} = k(1 + r)$ keeps the expected number of observed neighbors at $k$. Last, after normalization a doublet of two cells of one type has the expected profile of a singlet of that type, so homotypic doublets cannot be found from the profile. The approximation in the model is that a fraction $\rho$ of the observed cells are doublets, which lowers the score of true doublets a little.

## Complexity

On a [real RAM](/real-ram/) with $r$ fixed, lines L1 to L3 take $O(nd)$ time. Line L4 takes $O(nd^2)$ for the covariance, $O(d^3)$ per sweep of the eigendecomposition, and $O(ndp)$ for the projection. The brute-force search at line L6 takes $O(n^2(p + \log n))$, which is the largest term for many cells. Scrublet uses an approximate [nearest neighbor](/nearest-neighbor-graph/) search there, which makes the method fast for $10^5$ cells. The extra space is $O(n^2)$ for the brute-force distances and $O(nd + d^2)$ for the data and the covariance.

## Properties

- **Randomized.** The pairs of line L1 are random, so the scores change a little with the seed.
- **Bayesian score.** The score is a posterior probability under a stated density model, with the doublet rate as the prior.
- **Unsupervised.** It needs no labels, only the counts and an expected rate.
- **Blind to homotypic doublets.** Two cells of one type make a profile like one cell of that type.
- **Depends on the embedding.** The genes, the scaling and the number of components change the neighbors and so the scores.

## Variants and improvements

- **DoubletFinder** (McGinnis, Murrow and Gartner 2019) uses the proportion of artificial neighbors directly, chooses its neighborhood size by a sweep, and thresholds by the expected number of doublets.
- **Classifier methods** train a classifier, for example gradient boosted trees, to separate real cells from simulated doublets.
- **Experimental methods** use cell hashing with tagged antibodies, or genetic variants when cells of several donors are pooled. They also find homotypic doublets when the two cells come from different samples.
- **Cluster-aware simulation** draws the pairs from different clusters only, to model heterotypic doublets.

## When to use it

Use it on each sample of a droplet experiment before clustering, and remove the called doublets or mark them. It matters most when many cells were loaded, because the doublet rate grows with the load. Set $\rho$ from the load and the platform. When samples were pooled with hashtags or from several donors, use the experimental labels first and the score for the rest. Do not run it on data that already merges several samples, because the simulation would add counts of cells that could never share a droplet.

## Pitfalls

- **The threshold.** The valley of line L9 does not always exist. When the histogram of the simulated scores has no clear second mode, the threshold has to be set by hand, and the calls depend on it.
- **Homotypic doublets** are not found. The fraction of doublets that Scrublet can see is smaller than $\rho$ when one cell type dominates.
- **Real intermediate states,** such as cells in transition between two types, look like doublets of the two types and can get high scores.
- **Too few cells of a type** give the simulated doublets little support, and the scores near that type are noisy.
- **Merged samples.** Run it per sample, before integration or [batch correction](/batch-effect-correction/).

## Implementations

## History

Macosko et al. (2015) measured the rate of barcodes with two cells by mixing human and mouse cells, which gives reads of both species in a doublet. Experimental methods with tagged antibodies and with genetic variants followed. Wolock, Lopez and Klein (2019) published Scrublet, and McGinnis, Murrow and Gartner (2019) published DoubletFinder in the same issue of Cell Systems. Both score cells against simulated doublets in a reduced space.

## References
