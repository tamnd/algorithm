---
tag: 7XWT5K
kind: definition
slug: mean-intersection-over-union
name: Mean intersection over union
aliases:
- mIoU
- Jaccard score for segmentation
area: computer-vision/segmentation-and-recognition
level: core
summary: The intersection over union of predicted and true pixels for each class, averaged over classes, the standard score for semantic segmentation.
prereqs: [intersection-over-union, confusion-matrix]
see_also: [semantic-segmentation, jaccard-similarity, precision-and-recall, panoptic-segmentation, boundary-f-measure, detection-mean-average-precision, rand-index]
sources:
  - paper: doi:10.1109/CVPR.2015.7298965
    title: "Jonathan Long, Evan Shelhamer and Trevor Darrell, Fully convolutional networks for semantic segmentation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, 3431-3440 (arXiv 1411.4038)"
    locator: "Section 5, Metrics (pixel accuracy, mean accuracy, mean IU and frequency weighted IU, written with n_ij and t_i)"
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "Section 4.2.1, Segmentation accuracy, Eq. (4) (true positives over true positives, false positives and false negatives, void pixels excluded, the void border of 5 pixels)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.4, Semantic segmentation (the evaluation of per-pixel labels)"
---

Mean intersection over union (mIoU) is the standard score of [semantic segmentation](/semantic-segmentation/). For each class it takes the pixels that are truly of that class and the pixels that are predicted as that class, over the whole data set, and divides the size of their intersection by the size of their union. This is the [intersection over union](/intersection-over-union/), or [Jaccard index](/jaccard-similarity/), of two pixel sets. The score is the mean of these values over the classes. It is 1 only for a perfect labeling, and every class has the same weight, whatever its size. Pixels marked void in the ground truth do not count.

## Definition

Let there be $K$ classes and a data set of pairs of label images $(g, p)$ of the same size, where $g$ is the ground truth and $p$ the prediction. A true label is a class $0, \ldots, K - 1$ or the void label, which is 255 in PASCAL VOC. Let $V$ be the set of all non-void pixels of all images. The [confusion matrix](/confusion-matrix/) is
$$n_{ij} = \bigl|\{x \in V : g(x) = i,\ p(x) = j\}\bigr|,$$
the number of pixels of true class $i$ predicted as class $j$. With $t_i = \sum_j n_{ij}$, the number of pixels of true class $i$, the IoU of class $i$ is
$$\mathrm{IoU}_i = \frac{n_{ii}}{t_i + \sum_j n_{ji} - n_{ii}} = \frac{\mathrm{TP}_i}{\mathrm{TP}_i + \mathrm{FP}_i + \mathrm{FN}_i},$$
and the mIoU is the mean of $\mathrm{IoU}_i$ over the classes. Long, Shelhamer and Darrell (2015) write the score in this form, and PASCAL VOC writes it as true positives over the sum of true positives, false positives and false negatives.

```pseudo id=main
MEAN-IOU(pairs, K, void)
L1  n ← K × K matrix of zeros
L2  for each pair (g, p) and each pixel x of the image do
L3      if g(x) = void then skip x
L4      n[g(x)][p(x)] ← n[g(x)][p(x)] + 1
L5  S ← 0 ; c ← 0
L6  for i ← 0 to K - 1 do
L7      t ← Σ_j n[i][j] + Σ_j n[j][i] - n[i][i]       ▷ TP + FN + FP
L8      if t > 0 then S ← S + n[i][i] / t ; c ← c + 1
L9  return S / c
```

The proof file shows that $t$ in line L7 is the size of the union of the true and the predicted region of class $i$, so that each term is an exact Jaccard index (a theorem). It also shows that the score is in $[0, 1]$ and that it is 1 exactly when the prediction equals the truth on all non-void pixels. The cost is $O(N + K^2)$ for $N$ pixels, and the matrix needs $O(K^2)$ space for any number of images.

Three conventions change the number and must be stated with a result:

- **Data set or image.** The matrix is summed over all images before the division. The mean over images of the mIoU of each image is a different score.
- **Absent classes.** A class that is neither true nor predicted anywhere has the ratio $0/0$. Line L8 leaves it out. A class that is predicted but not true counts with the value 0. Some codes average over all $K$ classes instead.
- **Void.** Void pixels are skipped whatever the prediction there. In PASCAL VOC the void label covers a band of 5 pixels along object borders and unclear regions, so errors at the borders do not count.

Long, Shelhamer and Darrell (2015) report three more scores from the same matrix: the pixel accuracy $\sum_i n_{ii} / \sum_i t_i$, the mean accuracy $\frac{1}{K} \sum_i n_{ii} / t_i$, and the frequency weighted IU $\sum_i t_i \mathrm{IoU}_i / \sum_i t_i$.

## Examples and non-examples

- **A small example.** One image with three classes, read row by row:
  $g$ = `0 0 1 1 / 0 0 1 1 / 0 0 2 2 / void 0 2 2` and $p$ = `0 0 0 1 / 0 1 1 1 / 0 0 2 2 / 2 0 0 2`. The void pixel is skipped, so 15 pixels count. The confusion matrix has rows $(6, 1, 0)$, $(1, 3, 0)$ and $(1, 0, 3)$. The class IoUs are $6/(7 + 8 - 6) = 2/3$, $3/(4 + 4 - 3) = 3/5$ and $3/(4 + 3 - 3) = 3/4$, and the mIoU is $121/180 \approx 0.672$. The pixel accuracy is $12/15 = 0.8$, the mean accuracy is $11/14 \approx 0.786$ and the frequency weighted IU is $151/225 \approx 0.671$.
- **Small classes count fully.** In an image of 64 pixels with one pixel of class 1 and all predictions 0, the pixel accuracy is $63/64 \approx 0.98$, but the mIoU is $(63/64 + 0)/2 \approx 0.49$. This is the reason to report mIoU and not only accuracy (Proposition 5 of the proof).
- **The order of the means.** Image A has truth `0 0 0 1` and prediction `0 0 0 0`, with mIoU $(3/4 + 0)/2 = 3/8$. Image B has truth and prediction `1 1 1 1`, with mIoU 1, since class 0 is absent. The mean of the two is $11/16$. The summed matrix has rows $(3, 0)$ and $(1, 4)$, which gives $(3/4 + 4/5)/2 = 31/40$. The two numbers differ, and papers must say which one they report.
- **Not detection mAP.** mIoU looks only at the class of each pixel. It does not know about objects, so two touching objects of one class that are merged into one region get a perfect score. Instance tasks use [detection mean average precision](/detection-mean-average-precision/) on masks or the panoptic quality of [panoptic segmentation](/panoptic-segmentation/).
- **Not the Dice score.** The Dice score of a class, $2 n_{ii} / (t_i + \sum_j n_{ji})$, equals $2J/(1 + J)$ for its IoU $J$. It ranks one class in the same order, but the mean of the Dice scores is a different number. In the small example the Dice scores are $4/5$, $3/4$ and $6/7$.

## Related definitions

The [intersection over union](/intersection-over-union/) of two boxes or two masks is the ratio for a single pair; the mIoU applies it to the pixel sets of each class and averages. The per-class score is the Jaccard similarity of two sets, and the Dice score is the F1 score of [precision and recall](/precision-and-recall/) on the pixels of the class. Mean accuracy averages the recall of each class, and it ignores false positives. The [boundary F-measure](/boundary-f-measure/) scores only the pixels near region borders, which mIoU weights by their small number. For segmentations without class labels, scores that compare partitions, such as the [Rand index](/rand-index/), are used instead. The panoptic quality of [panoptic segmentation](/panoptic-segmentation/) averages the IoU of matched segments and adds a count of unmatched ones.

The Python code of this page builds the confusion matrix, computes the class IoUs, the mIoU and the other three scores of Long et al. with exact fractions, and its tests compare each class IoU with a Jaccard index computed on sets of pixels.

## References
