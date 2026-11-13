---
tag: KNX3QB
kind: problem
slug: image-labeling
name: Image labeling
aliases:
- connected component labeling problem
- blob extraction
area: graphics-and-signals/image-processing
level: advanced
summary: Give each connected region of foreground pixels in a binary image its own label, for a chosen 4- or 8-connectivity; the connected components problem on the grid graph of the pixels.
prereqs: [digital-image, connected-components]
see_also: [connected-component-labeling, flood-fill, connected-components, union-find-connectivity, image-thresholding, image-segmentation, image-moments, breadth-first-search]
sources:
  - paper: doi:10.1145/321356.321357
    title: Azriel Rosenfeld and John L. Pfaltz, Sequential operations in digital picture processing, Journal of the ACM 13(4), 471 to 494, 1966
    locator: the definition of connected components of a picture subset and their sequential labeling
  - paper: doi:10.1145/321556.321570
    title: Azriel Rosenfeld, Connectivity in digital pictures, Journal of the ACM 17(1), 1970
    locator: 4- and 8-connectivity, the use of opposite connectivities for a set and its complement, surrounding and holes
  - paper: doi:10.1016/j.patcog.2017.04.018
    title: Lifeng He, Xiwei Ren, Qihang Gao, Xiao Zhao, Bin Yao and Yuyan Chao, The connected-component labeling problem, a review of state-of-the-art algorithms, Pattern Recognition 70, 25 to 43, 2017
    locator: the problem statement and the families of algorithms (multi-pass, two-pass, one-pass contour tracing, run-based, parallel and hardware)
  - paper: doi:10.1016/0196-6774(82)90008-6
    title: Yossi Shiloach and Uzi Vishkin, An O(log n) parallel connectivity algorithm, Journal of Algorithms 3(1), 57 to 67, 1982
    locator: connected components of a graph in O(log n) parallel time on a CRCW PRAM
---

Image labeling is the problem of finding the connected regions of a binary image and giving each its own label. The input is a binary image and a connectivity, 4 or 8; the output is a label image in which every foreground pixel carries the number of its region and every background pixel carries 0. Equivalently, it is the [connected components](/connected-components/) problem on the graph whose nodes are the foreground pixels and whose edges join adjacent pixels. That graph is implicit in the grid and has at most $4N$ edges for $N$ pixels, so the problem is linear in principle, and the interest lies in doing it with sequential memory access, little extra memory, or in parallel. Labeling turns the output of [thresholding](/image-thresholding/) into objects that can be counted and measured. The standard algorithm is [two-pass connected component labeling](/connected-component-labeling/) with union-find.

## In plain words

A black and white picture shows white blobs on a black ground: coins on a table, letters on a page. The task is to name each blob, so that every pixel of the first coin says "1", every pixel of the second coin says "2", and so on. Two white pixels belong to the same blob when you can walk from one to the other over white pixels. You must decide what a step is: only up, down, left and right, or also the four diagonal moves. That choice changes the answer. Two coins that touch only at one corner are two blobs in the first rule and one blob in the second.

## Definition

The input is a binary [digital image](/digital-image/) $B$ of $W \times H$ pixels, $N = WH$, with $B(p) \in \{0, 1\}$, and a connectivity $c \in \{4, 8\}$. Pixels outside the image count as background. The pixels $p$ and $q$ are $c$-adjacent if they differ by one in one coordinate ($c = 4$) or by at most one in each coordinate ($c = 8$), and $p \ne q$. A $c$-path is a sequence of pixels in which consecutive pixels are $c$-adjacent. A $c$-component of the foreground is a maximal set of foreground pixels in which any two are joined by a $c$-path of foreground pixels.

The output is a label image $\ell$ with $\ell(p) = 0$ for background pixels, and $\ell(p) = \ell(q) > 0$ for foreground pixels $p$ and $q$ if and only if they are in the same $c$-component. The labels are a permutation of $1, \ldots, K$, where $K$ is the number of components; a common convention numbers the components in the raster order of their first pixel, which makes the output unique. Many applications also want, for each component, its area, bounding box, [moments](/image-moments/) or perimeter.

The cost model is the word RAM. The image is read in raster order, row by row.

## Variants

- **Background and holes.** Label the background with the other connectivity. With the dual connectivity, the holes of the foreground are exactly the background components that do not touch the image border.
- **Gray-level images.** Label the maximal connected sets of pixels with equal values (flat zones), or with neighboring values that differ by at most $\delta$. The second form is a simple segmentation, and it is not transitive in the values: a slow ramp becomes one region.
- **Higher dimensions.** In 3D, use 6-, 18- or 26-adjacency. The consistent pairs are 6 with 26 and 26 with 6 (and 6 with 18 in some treatments).
- **Statistics only.** Output the number of components and per-component features without writing a label image. One raster pass suffices if the features are kept per provisional label and added together at each merge, which suits streams of rows and hardware.
- **Labeling on other graphs.** On a general graph the problem is [connected components](/connected-components/), and on an online sequence of edges it is [union-find connectivity](/union-find-connectivity/).

## Examples

**Connectivity changes the count.** Take the $5 \times 5$ image with rows $(1, 1, 1, 0, 0)$, $(1, 0, 1, 0, 1)$, $(1, 1, 1, 0, 0)$, $(0, 0, 0, 1, 0)$ and $(1, 0, 0, 0, 1)$. With 4-adjacency it has five components: the ring of 8 pixels in the top left, and the single pixels at $(4, 1)$, $(3, 3)$, $(0, 4)$ and $(4, 4)$. With 8-adjacency the pixel $(3, 3)$ touches the ring at its corner $(2, 2)$ and the pixel $(4, 4)$ at a corner, so there are three components: 10 pixels, then $(4, 1)$, then $(0, 4)$. In both cases the ring encloses one hole, its center $(1, 1)$, and the Euler number (objects minus holes) is $5 - 1 = 4$ for the pair (4, 8) and $3 - 1 = 2$ for the pair (8, 4).

**The digital Jordan paradox.** In a $3 \times 3$ image, set the four side pixels $(1, 0)$, $(0, 1)$, $(2, 1)$ and $(1, 2)$ to 1 and the rest to 0. With 4-adjacency for both foreground and background, the four pixels are four separate components, yet the center is not 4-connected to the border, so four separate pixels enclose a hole. With 8-adjacency for both, the four pixels form one closed ring, yet the center is 8-connected to the corners, so the ring encloses nothing. Only the dual pairs give a consistent answer: under (8, 4) one ring with one hole, under (4, 8) four pixels and no hole. This is why practical systems pair 8-connectivity for the objects with 4-connectivity for the background, or the reverse, as Rosenfeld showed in 1970.

**A U shape.** In a raster scan, the two arms of a U are met first in the top row as two separate runs. A method that decides labels only from the pixels seen so far must later merge them at the bottom of the U. Every scan-based algorithm needs some way to record such merges, which is why the two-pass method keeps an equivalence structure.

## Known algorithms

- [Two-pass connected component labeling](/connected-component-labeling/): raster scan with provisional labels and a union-find forest, then a relabeling pass. $O(N \alpha(N))$ time, sequential access.
- [Flood fill](/flood-fill/) by [breadth-first search](/breadth-first-search/) or an explicit stack: start at each unlabeled foreground pixel and visit its component. $\Theta(N)$ time, random access.
- Multi-pass label propagation: repeat forward and backward raster passes that replace each label by the least label among its neighbors, until nothing changes. Simple, but the number of passes grows with the shape of the components (a spiral needs many).
- Run-based and block-based two-pass methods: label runs of a row or $2 \times 2$ blocks instead of pixels.
- Contour tracing: trace the outer and hole boundaries of each component when first met, and fill the interior in the same scan.
- Parallel methods: label propagation on tiles followed by a merge of the tile borders, or a parallel union-find. On a PRAM, the Shiloach-Vishkin method finds the connected components of a graph in $O(\log N)$ time.

## Bounds

The output has $N$ entries and the answer depends on every pixel (flipping one pixel can join two components or split one), so every algorithm needs $\Omega(N)$ time. A flood fill reaches $\Theta(N)$ time and $\Theta(N)$ extra space, because each pixel enters the queue once and each has at most 8 neighbors. The two-pass method takes $O(N \alpha(N))$ with union by rank and path compression, which is linear for every practical $N$. Since the grid graph has bounded degree, any linear-time connected components algorithm on graphs with $O(N)$ edges also gives $\Theta(N)$. Under 8-connectivity the number of components is at most $\lceil W/2 \rceil \lceil H/2 \rceil$, about $N/4$, because the foreground pixels of each aligned $2 \times 2$ block are pairwise adjacent; isolated pixels in every other row and column reach the bound. Under 4-connectivity a checkerboard has $\lceil N/2 \rceil$ components when it starts with a foreground corner.

## Reductions

- **To graph connected components.** Image labeling is the connected components problem on the implicit grid graph, so any algorithm for [connected components](/connected-components/) applies, from [breadth-first search](/breadth-first-search/) to [union-find](/union-find-connectivity/).
- **From segmentation.** A pixel classifier (thresholding, clustering) followed by labeling of each class gives a segmentation into connected regions; see [image segmentation](/image-segmentation/).
- **To shape measurement.** Labels select the pixel sets for [image moments](/image-moments/), areas, centroids and orientations.
- **To topology.** The number of components and holes gives the Euler number, which with the dual connectivities can also be computed from local $2 \times 2$ patterns without labeling.

## Applications

- Counting objects: cells, colonies, particles, coins, defects on a wafer.
- Character recognition: each connected component of ink is a character or a part of one.
- Blob analysis in industrial vision: area, position and orientation of each part.
- Cleaning masks: remove components smaller than a given area, or fill holes.
- Region adjacency graphs for later merging in segmentation.

## References
