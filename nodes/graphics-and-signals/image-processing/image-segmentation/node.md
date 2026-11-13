---
tag: 6SZ1BS
kind: problem
slug: image-segmentation
name: Image segmentation
aliases:
- region partitioning
- region segmentation
area: graphics-and-signals/image-processing
level: intro
summary: Partition the pixels of an image into regions that are each uniform by some criterion and that differ from their neighbors, as a set of connected regions or a label per pixel.
prereqs: [digital-image, image-thresholding]
see_also: [image-thresholding, image-labeling, image-segmentation-graph-cuts, normalized-cut, spectral-clustering, active-contours, k-means, mean-shift]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation (Section 10.1, the definition by a uniformity predicate; Sections 10.3 to 10.7, thresholding, region growing and splitting, clustering and superpixels, graph cuts, morphological watersheds)
  - book: isbn:9781848829343
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, Springer, 2011
    locator: Chapter 5, Segmentation (Section 5.1, Active contours; 5.2, Split and merge; 5.3, Mean shift and mode finding; 5.4, Normalized cuts; 5.5, Graph cuts and energy-based methods)
  - paper: doi:10.1002/cpa.3160420503
    title: David Mumford and Jayant Shah, Optimal approximations by piecewise smooth functions and associated variational problems, Communications on Pure and Applied Mathematics 42(5), 577 to 685, 1989
    locator: the functional with a data term, a smoothness term and a term for the length of the boundaries
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 1222 to 1239, 2001
    locator: the NP-hardness of the Potts energy for three or more labels, and the expansion move algorithm
  - paper: doi:10.1109/34.868688
    title: Jianbo Shi and Jitendra Malik, Normalized cuts and image segmentation, IEEE Transactions on Pattern Analysis and Machine Intelligence 22(8), 888 to 905, 2000
    locator: the normalized cut criterion, its NP-completeness, and the spectral relaxation
---

Image segmentation is the problem of dividing the pixels of an image into regions, so that each region is uniform by some measure (gray value, color, texture, motion) and adjacent regions differ. The output is a partition of the pixel grid, usually stored as a label image that gives each pixel the number of its region. Unlike [thresholding](/image-thresholding/), which decides each pixel by its own value, segmentation uses where the pixels are: regions are normally required to be connected, and methods trade the fit of each region against the length or the contrast of the boundaries. There is no single correct answer, because what counts as one object depends on the task and the scale. So the problem is always posed with a criterion: a predicate, an energy, a clustering objective or a graph cut, and different criteria have very different costs, from linear time to NP-hard.

## In plain words

Segmentation cuts a picture into pieces, like a coloring book in reverse. Each piece should look the same inside, for example all sky, all road or all one shirt, and two pieces that touch should look different. The pieces must cover the whole picture without overlap, and usually each piece must be in one part, not scattered. The hard part is that the same picture has many good answers: a face can be one piece, or eyes, nose and mouth can be separate pieces. Methods differ in how they decide. Some grow pieces from seed points, some flood the picture like water rising in a landscape, some group pixels with similar color and position, and some cut a graph of the pixels where the cut is cheapest.

## Definition

The input is a [digital image](/digital-image/) $I$ on the pixel set $P = \{0, \ldots, W-1\} \times \{0, \ldots, H-1\}$, with a gray value, a color vector or a feature vector at each pixel, and an adjacency on $P$: 4-connectivity (side neighbors) or 8-connectivity (side and corner neighbors).

A segmentation is a partition of $P$ into regions $R_1, \ldots, R_K$: the regions are nonempty, pairwise disjoint, and their union is $P$. The output is a label image $\ell : P \to \{1, \ldots, K\}$ with $R_k = \ell^{-1}(k)$. The classic definition, as in Gonzalez and Woods, adds a uniformity predicate $Q$ on sets of pixels and asks that

1. each $R_k$ is connected,
2. $Q(R_k)$ is true for each $k$, and
3. $Q(R_j \cup R_k)$ is false for each pair of adjacent regions.

This definition rules out bad answers but does not choose among good ones, and for many predicates it has many solutions. Most methods therefore optimize a criterion instead:

- **Energy.** Minimize $E(\ell) = \sum_p D_p(\ell_p) + \sum_{(p, q) \text{ adjacent}} V_{pq}(\ell_p, \ell_q)$, a data cost for each label and a cost for each pair of neighbors with different labels. The Potts model sets $V_{pq} = \lambda [\ell_p \ne \ell_q]$. The Mumford-Shah functional is the continuous form, with a term for the length of the boundaries.
- **Graph partition.** Build a graph on the pixels with edge weights that measure similarity, and minimize a cut criterion, such as the [normalized cut](/normalized-cut/).
- **Clustering.** Map each pixel to a feature vector, such as color plus position, and cluster the vectors by [k-means](/k-means/), [mean shift](/mean-shift/) or a [mixture model](/gaussian-mixture-model/). The clusters need not be connected, so a [labeling](/image-labeling/) pass splits them afterwards.

The cost model is the word RAM or the real RAM on $N = WH$ pixels, with $m = O(N)$ edges on a 4- or 8-connected grid.

## Variants

- **Foreground and background (binary).** Two labels, often with user input: seeds, a box, or scribbles. [Graph cuts](/image-segmentation-graph-cuts/) and [GrabCut](/grabcut/) solve this form.
- **Oversegmentation into superpixels.** Many small, compact regions that respect edges, used as the units of later steps. [SLIC](/slic-superpixels/) and [Felzenszwalb's method](/felzenszwalb-segmentation/) are typical.
- **Seeded segmentation.** The user or a detector gives one seed per region, and the method assigns every other pixel. [Seeded region growing](/region-growing/) and marker-based [watershed](/watershed-segmentation/) work this way.
- **Unsupervised segmentation.** No seeds and no fixed number of regions. [Mean shift segmentation](/mean-shift-segmentation/), Felzenszwalb's method and watershed with merging are examples.
- **Boundary-based segmentation.** Find closed curves instead of regions, as in [active contours](/active-contours/), or link the output of [edge detection](/edge-detection/).
- **Semantic and instance segmentation.** A class name for each pixel (semantic), or a separate mask for each object instance. These are learned from labeled data and are outside the scope of this page's methods.
- **Volumes and video.** The same definitions on 3D grids (CT, MRI) with 6- or 26-connectivity, or on space-time volumes.

## Examples

**Connectivity changes the answer.** Take the $4 \times 4$ gray image with rows $(10, 10, 90, 90)$, $(10, 10, 90, 90)$, $(90, 90, 10, 10)$ and $(90, 90, 10, 10)$. Any threshold between 10 and 90 gives two classes, the dark and the bright pixels. With 4-connectivity the classes form four regions, one per $2 \times 2$ quadrant. With 8-connectivity the two dark quadrants touch at a corner, between the pixels in row 1, column 1 and row 2, column 2, so they form one region; the two bright quadrants touch at the other diagonal, so they also form one region. Each of the two regions then crosses the other, which is the paradox of digital topology. The usual fix is to use 8-connectivity for the foreground and 4-connectivity for the background, or the other way round; see [image labeling](/image-labeling/).

**The number of possible answers.** A partition of $N$ pixels is one of the Bell number $B_N$ set partitions, and requiring connected regions removes most of them. A short enumeration gives, for a $2 \times 2$ image, 15 partitions, of which 12 have 4-connected regions (the three that use a diagonal pair fail) and all 15 have 8-connected regions. For $3 \times 2$ the numbers are 203, 74 and 125, and for $3 \times 3$ they are 21147, 1434 and 4559. Exhaustive search is out of the question beyond toy sizes, so the criterion must have structure that an algorithm can use.

**Different criteria, different answers.** On the row of pixels $(10, 12, 11, 50, 52, 90)$, a two-class threshold groups $\{10, 12, 11\}$ against $\{50, 52, 90\}$. A rule that merges neighbors whose values differ by at most 5 gives three regions, $\{10, 12, 11\}$, $\{50, 52\}$ and $\{90\}$. A Potts energy with a squared data term and a large $\lambda$ prefers fewer regions and can merge 50 and 52 with 90. All three are valid segmentations under their own criterion.

## Known algorithms

- [Thresholding](/image-thresholding/), for example [Otsu's method](/otsu-thresholding/), then [connected component labeling](/connected-component-labeling/): $\Theta(N + L)$ plus near-linear labeling.
- [Region growing](/region-growing/): grow regions from seeds by adding the most similar boundary pixel, with a priority queue, $O(N \log N)$.
- [Watershed segmentation](/watershed-segmentation/): flood a gradient image from its minima or from markers. $O(N)$ after sorting the values, or $O(N \log N)$ with a priority queue.
- [Mean shift segmentation](/mean-shift-segmentation/): find the modes of the joint density of position and color, and group pixels by mode. The cost depends on the bandwidths and the number of iterations.
- [Felzenszwalb-Huttenlocher graph-based segmentation](/felzenszwalb-segmentation/): a Kruskal-like merge with an adaptive threshold, $O(m \log m)$, with a proof that the result is neither too coarse nor too fine.
- [SLIC superpixels](/slic-superpixels/): k-means in color and position with a local search window, $O(N)$ per iteration.
- [Graph cuts](/image-segmentation-graph-cuts/): exact minimum of a two-label energy with submodular pairwise terms by max flow. [GrabCut](/grabcut/) iterates color models and graph cuts from a box.
- [Normalized cuts](/normalized-cut/) and [spectral clustering](/spectral-clustering/): relax a graph partition to an eigenvector problem.
- [Active contours](/active-contours/): evolve a curve to a local minimum of an energy.

## Bounds

Every method reads every pixel, so $\Omega(N)$ time is necessary. The criterion sets the rest:

- Thresholding and connected components: $O(N \alpha(N))$ with union-find, or $O(N)$ with a flood fill.
- Two-label energies with $V_{pq}(0,1) + V_{pq}(1,0) \ge V_{pq}(0,0) + V_{pq}(1,1)$ (submodular) are minimized exactly by a minimum cut, in polynomial time; see [graph cuts](/image-segmentation-graph-cuts/) and the [min cut problem](/min-cut-problem/).
- The Potts energy with three or more labels is NP-hard to minimize, as Boykov, Veksler and Zabih show; their expansion moves find a local minimum within a factor of 2 of the optimum.
- Minimizing the normalized cut is NP-complete, as Shi and Malik show, which is why their method uses a spectral relaxation.
- Felzenszwalb and Huttenlocher's criterion has a solution that their $O(m \log m)$ algorithm finds, while a natural variant of the criterion, with a quantile in place of the minimum edge, is NP-hard; see [their method](/felzenszwalb-segmentation/).

## Reductions

- **Segmentation to labeling.** Any method that assigns classes to pixels without forcing connectivity (thresholding, clustering) becomes a segmentation into connected regions by [image labeling](/image-labeling/).
- **Binary segmentation to min cut.** A two-label energy with submodular pairwise terms reduces to an s-t [minimum cut](/min-cut-problem/) on a graph with one node per pixel and two terminals, and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) gives the solver.
- **Graph segmentation to spanning trees.** Merging regions in order of the weight of the edge between them follows [Kruskal's algorithm](/kruskal/) on the pixel graph. Cutting the $K - 1$ heaviest edges of a [minimum spanning tree](/minimum-spanning-tree/) gives the single-linkage clustering into $K$ regions, which Felzenszwalb's method refines with an adaptive threshold.
- **Clustering to segmentation.** Add the pixel position to each feature vector, cluster in the joint space, and split by connectivity. SLIC and mean shift segmentation are this reduction with k-means and mean shift.

## Applications

- Medical imaging: organ and tumor outlines in CT and MRI, cell segmentation in microscopy.
- Photo editing: cutting out a person or an object, background replacement, selective color correction.
- Robotics and driving: free space, road and obstacle regions.
- Remote sensing: fields, water and built-up areas in satellite images.
- Preprocessing: superpixels reduce the number of units for later labeling, tracking and recognition, and region masks feed [shape moments](/image-moments/) and measurements.

## References
