---
tag: WE3F6C
kind: algorithm
slug: detr
name: DETR
aliases:
- detection transformer
area: computer-vision/segmentation-and-recognition
level: research
summary: Predict a fixed set of boxes with a transformer and train by a Hungarian matching of predictions to objects, with no anchors and no non-maximum suppression.
solves: [object-detection]
model: real-ram
complexity:
  vars: {N: the number of queries, M: the number of ground truth objects, C: the number of classes}
  time: {worst: "O(N C + N M^2)"}
  space: {extra: "O(N M)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2020
  people: [Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko]
  note: "Presented at ECCV 2020. It made detection a direct set prediction trained with a bipartite matching loss, and removed anchors and non-maximum suppression from the pipeline."
prereqs: [hungarian-algorithm, intersection-over-union, cross-entropy-loss, object-detection]
see_also: [assignment-problem, bipartite-matching, faster-r-cnn, yolo-detector, single-shot-multibox-detector, box-non-maximum-suppression, anchor-assignment, panoptic-segmentation]
sources:
  - paper: doi:10.1007/978-3-030-58452-8_13
    title: "Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov and Sergey Zagoruyko, End-to-end object detection with transformers, ECCV 2020, LNCS 12346, 213-229"
    locator: "Section 3.1, Object detection set prediction loss (the matching cost -p(c) + L_box with probabilities rather than log-probabilities, the Hungarian loss, the no-object term down-weighted by a factor 10, the box loss lambda_iou L_iou + lambda_L1 L1 with the generalized IoU); Section 3.2, DETR architecture (N object queries, auxiliary decoding losses); Section 4, Experiments (lambda_L1 = 5, lambda_iou = 2, N = 100; Table 1: AP 42.0 for DETR and 43.5 for DETR-R101 on COCO)"
  - url: https://arxiv.org/abs/2005.12872
    title: "Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov and Sergey Zagoruyko, End-to-end object detection with transformers, arXiv 2005.12872"
    locator: "the same sections"
  - paper: doi:10.1002/nav.3800020109
    title: "Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 1955, 83-97"
    locator: "the assignment algorithm that computes the matching"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.3, Object detection"
---

DETR, the detection transformer, treats object detection as the prediction of a set. A convolutional backbone computes a feature map, and a transformer encoder mixes the features of all positions. A transformer decoder then turns a fixed number $N$ of learned queries, 100 in the paper, into $N$ outputs. Each output is a class distribution over the $C$ classes and an extra "no object" class $\varnothing$, plus one box. In training, the $M$ true objects are matched one to one to $M$ of the $N$ outputs by the [Hungarian algorithm](/hungarian-algorithm/). The match is chosen to minimize a cost of class probability and box error. Every matched output learns its object, and every other output learns $\varnothing$. Because the loss punishes two outputs for one object, the network learns not to make duplicates. So DETR has no [anchors](/anchor-boxes/), no hand-made [assignment rule](/anchor-assignment/), and no [non-maximum suppression](/box-non-maximum-suppression/). With a ResNet-50 it reached 42.0 AP on COCO, close to a tuned [Faster R-CNN](/faster-r-cnn/). It was better on large objects and worse on small ones.

## In plain words

DETR asks the network for a fixed list of 100 guesses. Each guess is a box and a class, or "nothing here". In training, the true objects are paired with the guesses in the cheapest way, one guess per object. The cost of a pair is low when the guess names the right class and its box is close. The paired guesses learn their objects, and all other guesses learn to say "nothing". Since only one guess can be paired with an object, a second guess on the same object is pushed to say "nothing". So the network learns to give each object once, and no step to remove near copies is needed. At test time, the guesses that name a class with enough confidence are the output.

## The problem

The input is an image and a trained network that gives $N$ outputs $(\hat p_i, \hat b_i)$. Here $\hat p_i$ is a distribution over $C + 1$ classes, and $\hat b_i = (c_x, c_y, w, h)$ is a box relative to the image size. In training, the ground truth is a set of $M \le N$ objects $(c_j, b_j)$. The non-learned core is the set loss: find the one-to-one matching $\hat\sigma$ of the objects to the outputs of least total cost, then compute the loss under that matching. At test time the output is the set of non-$\varnothing$ predictions above a threshold, judged by [detection mean average precision](/detection-mean-average-precision/). The network is outside the page.

## The algorithm

```pseudo id=main
DETR-SET-LOSS(I, network, (c_j, b_j) for j = 1, ..., M)
L1  (p̂_i, b̂_i) for i = 1, ..., N ← network(I)      ▷ outside
L2  cost[j][i] ← -p̂_i(c_j) + λ_L1 ‖b_j - b̂_i‖_1 + λ_iou (1 - GIoU(b_j, b̂_i)) for all j, i
L3  σ̂ ← the one-to-one map of the M truths to the N queries of least total cost   ▷ Hungarian algorithm
L4  target_i ← c_j if σ̂(j) = i, else ∅
L5  L_cls ← the weighted mean of -log p̂_i(target_i), with weight 0.1 for ∅ and 1 otherwise
L6  L_box ← (1/M) Σ_j [λ_L1 ‖b_j - b̂_σ̂(j)‖_1 + λ_iou (1 - GIoU(b_j, b̂_σ̂(j)))]
L7  return L_cls + L_box
```

**Matching cost.** The paper uses $\lambda_{L1} = 5$ and $\lambda_{iou} = 2$. The class part of the cost is the probability $-\hat p_i(c_j)$, not its log. The paper reports that this keeps the class and box parts on the same scale and works better. The generalized IoU of two boxes $A$ and $B$, with $H$ the smallest box that holds both, is
$$\text{GIoU}(A, B) = \text{IoU}(A, B) - \frac{|H| - |A \cup B|}{|H|} \in (-1, 1].$$
Unlike the [IoU](/intersection-over-union/), it still falls as two boxes that do not overlap move apart. The L1 term alone would weight large boxes more than small ones, and the GIoU term does not depend on scale.

**Hungarian loss.** The class term of the outputs matched to $\varnothing$ is down-weighted by a factor of 10, since most of the $N$ outputs are $\varnothing$. The code takes the weighted mean over the queries and divides the box term by $M$. The paper adds the same loss after each decoder layer, as auxiliary losses, with a matching for each layer.

**Test time.** For each query, take the most likely class other than $\varnothing$ and its probability. The output is the queries whose probability is above a threshold. There is no NMS. The paper reports that NMS helps the outputs of the first decoder layer, and that the gain goes away as the layers get deeper.

## Example

Take two classes, cat (0) and dog (1), so each $\hat p_i$ is (cat, dog, $\varnothing$). The truths are a cat at $T_1 = (0.25, 0.5, 0.2, 0.2)$ and a dog at $T_2 = (0.75, 0.5, 0.2, 0.2)$. There are three queries:

| query | $\hat p_i$ | $\hat b_i$ |
|---|---|---|
| 1 | 0.5, 0.1, 0.4 | $T_1$ |
| 2 | 0.2, 0.3, 0.5 | $T_2$ |
| 3 | 0.7, 0.1, 0.2 | (0.3, 0.5, 0.2, 0.2) |

1. Query 3 is $T_1$ moved by 0.05. Its IoU with $T_1$ is $0.03/0.05 = 0.6$, and the enclosing box is the union, so its GIoU is also 0.6. Its cost for the cat is $-0.7 + 5 \cdot 0.05 + 2 \cdot 0.4 = 0.35$.
2. Query 1 has cost $-0.5$ for the cat, and query 2 has cost $-0.3$ for the dog, since their boxes are exact. The pairs across the image have costs above 4.9, because $T_1$ and $T_2$ are 0.5 apart with GIoU $-3/7$.
3. The best matching is cat to query 1 and dog to query 2, with total $-0.8$. Matching the cat to query 3, the most confident cat, would cost $0.35 - 0.3 = 0.05$.
4. So query 3 gets the target $\varnothing$, though it is the strongest cat guess. This is how the loss removes duplicates. The box loss is 0, and
$$L = \frac{-\ln 0.5 - \ln 0.3 - 0.1 \ln 0.2}{1 + 1 + 0.1} \approx 0.980.$$

At test time with a threshold of 0.45, these outputs give a cat from query 3 (0.7) and a cat from query 1 (0.5): two boxes for one object, which training on this loss pushes apart.

## Correctness

The network has no correctness theorem; its accuracy is measured. [The proof page](proofs/correctness.md) shows these facts for the steps that are not learned:

1. **Matching.** The Hungarian algorithm of the code returns a one-to-one map of the truths to the queries of least total cost. The tests compare it with all maps on small inputs.
2. **Order does not matter.** When the matching of least cost is unique, the loss does not change when the queries or the truths are listed in another order. So the network is not tied to an order of the objects.
3. **GIoU.** It lies in $(-1, 1]$, equals 1 only for equal boxes, and is symmetric.
4. **Duplicates cost.** Each truth is matched to exactly one query. If several queries give copies of one object, all but one get the target $\varnothing$, unless they are matched to other truths.

## Complexity

The network is outside. The cost matrix has $MN$ entries and costs $O(MN)$ to fill, after $O(NC)$ to read the outputs. The Hungarian algorithm with potentials assigns the $M$ rows one at a time. Each row takes at most $O(M)$ rounds of $O(N)$ work, so the total is $O(M^2 N)$. The loss is $O(N + M)$ after that. The test-time output costs $O(NC)$ and a sort. The extra space is $O(NM)$ for the matrix. The transformer encoder over $HW$ feature positions costs $O((HW)^2)$ per layer, which limits the feature resolution and is one reason why small objects are harder.

## Properties

- **End to end.** One loss from the image to the set of boxes, with no anchors, no assignment by IoU thresholds and no NMS.
- **Set loss.** The loss does not depend on the order of the queries or the objects.
- **Global reasoning.** The decoder attends to all queries and all positions, so the outputs can take each other into account.
- **Slow training.** The paper trains for hundreds of epochs, far more than Faster R-CNN needs, and the matching can change from step to step early in training.
- **Weaker on small objects.** The feature map has stride 32 in the base model, and there is no feature pyramid.
- **Deterministic at test time; not exact,** since it is a learned method.

## Variants and improvements

- **Deformable DETR.** Attention to a few sampled points on several feature levels, in the spirit of the [feature pyramid network](/feature-pyramid-network/). This gives faster training and better results on small objects.
- **Conditional, DAB, DN and DINO DETR.** Queries tied to anchor points or boxes, and denoising training with noisy truth boxes. They make the matching more stable and shorten training.
- **Panoptic DETR.** A mask head on the decoder outputs gives [panoptic segmentation](/panoptic-segmentation/) with the same matching, extended to stuff classes.
- **Set prediction elsewhere.** The same Hungarian loss trains keypoint, tracking and segmentation models. One-to-one assignment has also been added to convolutional detectors to drop NMS.

## When to use it

Use DETR or one of its descendants when an end-to-end detector without NMS and anchors is wanted, when objects overlap heavily so that NMS hurts, or when detection is one part of a larger set prediction. Use a detector with a feature pyramid when training time is short or small objects dominate. For a fast detector on a small device, a one-stage convolutional detector is still the usual choice.

## Pitfalls

- **Log-probabilities in the matching.** The paper uses probabilities in the cost and log-probabilities in the loss. Using the log in the cost changes its scale against the box terms.
- **Box format.** The L1 term is on $(c_x, c_y, w, h)$ relative to the image, and the GIoU needs corners. Mixing the formats or pixels gives wrong costs.
- **Degenerate boxes.** GIoU divides by the enclosing area. Boxes of zero width early in training need a guard.
- **The no-object weight.** Most of the $N$ targets are $\varnothing$. The paper down-weights them by 10 for this class imbalance, much as two-stage detectors sample their negatives.
- **$N$ too small.** If an image has more objects than queries, the matching cannot cover them. $N$ must be well above the usual number of objects.
- **Matching on a greedy basis.** Matching each truth to its best query in turn is not optimal and can give a query to the wrong object, as in the example. Use an exact assignment solver.

## Implementations

The network is outside this page. The Python code takes the class probabilities and boxes of the $N$ queries as inputs, and the tests build them by hand or with a fixed seed. The code implements the generalized IoU, the matching cost, the Hungarian algorithm with potentials for a rectangular cost matrix, the set loss of lines L1 to L7, and the test-time output without NMS. The tests check GIoU values and bounds, the Hungarian algorithm against all one-to-one maps on random matrices with ties, the example above, the loss with no truths, the invariance of the loss under reordering of the queries and the truths, and that the output keeps duplicates.

## History

Earlier detectors turned set prediction into many separate problems: score each [anchor](/anchor-boxes/) or [proposal](/object-proposals/), label it by an IoU rule, and remove duplicates by NMS. Set losses with a bipartite matching had been used before, for example by Stewart, Andriluka and Ng for people in crowds (2016), with recurrent networks. Carion, Massa, Synnaeve, Usunier, Kirillov and Zagoruyko put DETR on arXiv in May 2020 and presented it at ECCV 2020. They joined the matching loss with a transformer encoder and decoder and reached the accuracy of Faster R-CNN on COCO. Its slow training and weak small-object results led to Deformable DETR and a long line of descendants, such as DINO, which are among the strongest detectors on COCO.

## References
