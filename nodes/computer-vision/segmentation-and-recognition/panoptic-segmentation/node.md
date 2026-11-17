---
tag: 0990Z7
kind: problem
slug: panoptic-segmentation
name: Panoptic segmentation
aliases:
- panoptic labeling
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Give every pixel a class and, for countable things, an instance id, joining semantic and instance segmentation in one output.
prereqs: [semantic-segmentation, instance-segmentation, intersection-over-union]
see_also: [mean-intersection-over-union, mask-r-cnn, detection-mean-average-precision, precision-and-recall, bipartite-matching, image-segmentation, detr, rand-index]
sources:
  - paper: doi:10.1109/CVPR.2019.00963
    title: "Alexander Kirillov, Kaiming He, Ross Girshick, Carsten Rother and Piotr Dollar, Panoptic segmentation, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019, 9404-9413 (arXiv 1801.00868)"
    locator: "Section 3 (the task format: a pair of a semantic label and an instance id per pixel, disjoint stuff and thing labels, the void label, no confidence scores), Section 4.1 (segment matching and Theorem 1, a match needs IoU above 0.5), Section 4.2 (Eq. 1 for PQ and Eq. 2 for PQ = SQ x RQ, computed per class and averaged), the paragraph on void labels and groups, the section on data sets (Cityscapes, ADE20k and Mapillary Vistas) and the machine baselines that merge semantic and instance outputs"
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar and C. Lawrence Zitnick, Microsoft COCO: common objects in context, ECCV 2014"
    locator: the instance masks of thing classes, and crowd regions
  - paper: doi:10.1109/ICCV.2017.322
    title: "Kaiming He, Georgia Gkioxari, Piotr Dollar and Ross Girshick, Mask R-CNN, IEEE International Conference on Computer Vision (ICCV), 2017 (arXiv 1703.06870)"
    locator: the instance segmentation method used for the thing part of panoptic baselines
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.4, Semantic segmentation (the part on panoptic segmentation)"
---

Panoptic segmentation is the problem of giving every pixel of an image a class and, if the class is a countable thing such as a person or a car, the id of the object that the pixel belongs to. Amorphous regions such as sky, road and grass are stuff and get only a class. The output is a partition of the image into segments, each with one class, and no two segments overlap. It joins [semantic segmentation](/semantic-segmentation/), which labels stuff and things but does not separate objects, and [instance segmentation](/instance-segmentation/), which separates objects but ignores stuff and allows overlaps. Kirillov, He, Girshick, Rother and Dollar (2019) defined the task and its score, the panoptic quality (PQ).

## In plain words

You give the computer a street photo. It must paint every pixel. Pixels of sky, road or trees get just a name, such as "sky". Pixels of people or cars get a name and a number, such as "car 1" or "car 2", so that each car is separate. No pixel can belong to two things at once. The score compares each piece of the answer with a piece drawn by hand. Two pieces are paired when they overlap by more than half of their joint area, and such a pair is always unique. The score rewards good overlap of paired pieces and punishes pieces that have no partner.

## Definition

Fix a set of classes $\mathcal{L} = \mathcal{L}^{\mathrm{St}} \cup \mathcal{L}^{\mathrm{Th}}$, the stuff classes and the thing classes, with $\mathcal{L}^{\mathrm{St}} \cap \mathcal{L}^{\mathrm{Th}} = \emptyset$. The input is an image of $W \times H$ pixels. The output gives each pixel $i$ a pair $(l_i, z_i)$, where $l_i \in \mathcal{L}$ is its class and $z_i$ is an instance id. Pixels with the same pair form one segment. For stuff classes the id is ignored, so all pixels of one stuff class form one segment. The ground truth has the same form, and a pixel may also be void: unknown, outside the classes, or not labeled. The output has no confidence scores.

**Matching.** A predicted segment $p$ and a ground-truth segment $g$ of the same class match if $\mathrm{IoU}(p, g) > 0.5$, with the [intersection over union](/intersection-over-union/) of pixel sets.

**Theorem 1 (Kirillov et al. 2019).** Since predicted segments do not overlap and ground-truth segments do not overlap, each ground-truth segment matches at most one predicted segment, and each predicted segment matches at most one ground-truth segment.

*Proof.* For any $p$ and $g$, $\mathrm{IoU}(p, g) = |p \cap g| / |p \cup g| \le |p \cap g| / |g|$, since $g \subseteq p \cup g$. If two different predicted segments $p_1$ and $p_2$ both had IoU above $0.5$ with $g$, then $|p_1 \cap g| > |g|/2$ and $|p_2 \cap g| > |g|/2$. But $p_1$ and $p_2$ are disjoint, so $|p_1 \cap g| + |p_2 \cap g| \le |g|$, which is a contradiction. The same argument with the roles of $p$ and $g$ swapped gives the second part. $\square$

So the matching is unique and needs no [bipartite matching](/bipartite-matching/) algorithm: every pair with IoU above 0.5 is a match. For a class, the matched pairs are the true positives TP, the unmatched predicted segments are the false positives FP, and the unmatched ground-truth segments are the false negatives FN. The panoptic quality of the class is
$$\mathrm{PQ} = \frac{\sum_{(p, g) \in \mathrm{TP}} \mathrm{IoU}(p, g)}{|\mathrm{TP}| + \tfrac12 |\mathrm{FP}| + \tfrac12 |\mathrm{FN}|} = \underbrace{\frac{\sum_{(p, g) \in \mathrm{TP}} \mathrm{IoU}(p, g)}{|\mathrm{TP}|}}_{\mathrm{SQ}} \times \underbrace{\frac{|\mathrm{TP}|}{|\mathrm{TP}| + \tfrac12 |\mathrm{FP}| + \tfrac12 |\mathrm{FN}|}}_{\mathrm{RQ}},$$
the product of the segmentation quality SQ and the recognition quality RQ, when TP is not empty. The PQ of a method is the mean of the PQ of the classes, computed over the whole test set. Void pixels are removed from predicted segments before the IoU is computed. An unmatched predicted segment with more than half of its pixels void is not a false positive. Groups of objects that are labeled as one crowd region are handled in the same way.

These facts follow from the definition and are theorems:

- **Range.** $0 \le \mathrm{PQ} \le 1$, and $\mathrm{SQ} \in (0.5, 1]$ when TP is not empty, since each matched IoU is above 0.5.
- **RQ is an F1 score.** $\mathrm{RQ} = 2|\mathrm{TP}| / (2|\mathrm{TP}| + |\mathrm{FP}| + |\mathrm{FN}|)$, the harmonic mean of the [precision and recall](/precision-and-recall/) of segments at the IoU threshold 0.5.
- **Perfect score.** PQ of a class is 1 if and only if every predicted and every ground-truth segment of the class is matched with IoU 1, that is, the segments are equal up to void pixels.

## Variants

- **Video panoptic segmentation.** Ids stay the same for the same object over the frames.
- **Panoptic segmentation of point clouds.** Stuff and thing labels for lidar points.
- **Part-aware panoptic segmentation.** Thing segments are split further into parts, such as the head and the arms of a person.
- **Other scores.** PQ treats a small and a large object alike. Variants weight stuff classes differently or use other matching rules.

## Examples

- **A worked PQ.** One thing class, person, and one stuff class, sky. The ground truth has two people, $g_1$ of 100 pixels and $g_2$ of 50 pixels, and a sky of 200 pixels. The prediction has $p_1$ of 90 pixels with 80 pixels in $g_1$, $p_2$ of 40 pixels with 20 pixels in $g_2$, and a sky segment of 190 pixels with 180 pixels in the true sky.
  - $\mathrm{IoU}(p_1, g_1) = 80 / (100 + 90 - 80) = 8/11 \approx 0.727 > 0.5$: a true positive.
  - $\mathrm{IoU}(p_2, g_2) = 20 / (50 + 40 - 20) = 2/7 \approx 0.286$: no match, so $p_2$ is a false positive and $g_2$ is a false negative.
  - Person: $\mathrm{SQ} = 8/11$, $\mathrm{RQ} = 1/(1 + 1/2 + 1/2) = 1/2$, $\mathrm{PQ} = 4/11 \approx 0.364$.
  - Sky: $\mathrm{IoU} = 180 / (200 + 190 - 180) = 6/7$, so $\mathrm{PQ} = \mathrm{SQ} = 6/7 \approx 0.857$ and $\mathrm{RQ} = 1$.
  - The PQ of the method is $(4/11 + 6/7)/2 = 47/77 \approx 0.610$.
- **Half a person is not enough.** If $p_2$ covered exactly half of $g_2$ and nothing else, its IoU would be $0.5$, which is not above $0.5$. The person counts as missed, and $p_2$ as a false positive.
- **A non-example.** The output of an instance segmentation method with two overlapping masks is not a panoptic output. The overlap must first be given to one of the two segments, for example by score.

## Known algorithms

- **Merge two outputs.** Run a semantic segmentation method and an instance segmentation method such as [Mask R-CNN](/mask-r-cnn/), then merge. Kirillov et al. (2019) give baselines of this kind: instance masks are placed in order of score, overlaps go to the earlier mask, and the pixels that are left take their stuff class from the semantic output. The rules for the merge are heuristics.
- **One network with two heads.** A shared backbone with a semantic head and an instance head, followed by the same merge, for example Panoptic FPN.
- **Bottom-up methods.** A semantic map and a map of offsets to object centers, with pixels grouped by the nearest center.
- **Mask classification.** Methods in the style of [DETR](/detr/) predict a set of masks, each with a class, and train with a one-to-one matching. Stuff and things are handled in the same way, and each pixel goes to the mask with the highest score.

The cost and the quality of the networks are outside this page. Their quality is a benchmark result on data sets such as COCO, Cityscapes, ADE20k and Mapillary Vistas.

## Bounds

There is no lower bound on the error of a method. The score is cheap to compute exactly. By Theorem 1, a class with $n_p$ predicted and $n_g$ ground-truth segments needs only the overlaps of the pairs that share a pixel. One pass over the $WH$ pixels counts all intersections of predicted and ground-truth segments in a hash table, and the IoU of every overlapping pair follows from the segment sizes. So PQ costs $O(WH)$ time per image with expected $O(1)$ hash operations, plus the number of overlapping pairs, which is at most $WH$.

## Reductions

- **To semantic segmentation.** Drop the instance ids. The result is a semantic label map.
- **To instance segmentation.** Keep only the thing segments, as masks without overlaps. Scores must be added for the instance metric.
- **From semantic and instance segmentation.** The merge described under known algorithms turns the two outputs into a panoptic output.
- **Of PQ to a detection score.** RQ is the F1 score of a detection problem in which a segment is found if its IoU is above 0.5.

## Applications

Scene understanding for autonomous driving, where every pixel needs a class and every road user an id; robot navigation; image editing that needs both background regions and separate objects; and as a target for one model that solves both semantic and instance segmentation.

## References
