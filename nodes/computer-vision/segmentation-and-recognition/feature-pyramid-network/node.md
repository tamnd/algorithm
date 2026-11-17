---
tag: SWG7ZE
kind: technique
slug: feature-pyramid-network
name: Feature pyramid network
aliases:
- FPN
area: computer-vision/segmentation-and-recognition
level: advanced
summary: Build a pyramid of feature maps with strong semantics at every scale by a top-down path with lateral connections, and detect objects on each level.
prereqs: [faster-r-cnn, image-pyramid, convolution]
see_also: [anchor-boxes, anchor-assignment, roi-pooling, mask-r-cnn, single-shot-multibox-detector, focal-loss, gaussian-pyramid, nearest-neighbor-interpolation]
sources:
  - paper: doi:10.1109/CVPR.2017.106
    title: "Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan and Serge Belongie, Feature pyramid networks for object detection, CVPR 2017"
    locator: "Section 3, Feature pyramid networks (bottom-up pathway, top-down pathway with nearest neighbor upsampling by 2, 1 x 1 lateral connections, a 3 x 3 convolution on each merged map, d = 256); Section 4.1, FPN for RPN (one anchor area from 32^2 to 512^2 on P2 to P6, 3 ratios, 15 anchors, P6 by subsampling P5); Section 4.2, FPN for Fast R-CNN (Eq. 1, the level k = floor(k0 + log2(sqrt(wh)/224)) with k0 = 4); Section 5, Experiments (COCO test-dev AP 36.2 with ResNet-101)"
  - url: https://arxiv.org/abs/1612.03144
    title: "Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan and Serge Belongie, Feature pyramid networks for object detection, arXiv 1612.03144"
    locator: "the same sections"
  - url: https://arxiv.org/abs/1708.02002
    title: "Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He and Piotr Dollar, Focal loss for dense object detection, ICCV 2017 (arXiv 1708.02002)"
    locator: "Section 4, RetinaNet detector (an FPN with levels P3 to P7 as the backbone of a one-stage detector)"
  - paper: doi:10.1109/TPAMI.2016.2577031
    title: "Shaoqing Ren, Kaiming He, Ross Girshick and Jian Sun, Faster R-CNN: towards real-time object detection with region proposal networks, IEEE Transactions on Pattern Analysis and Machine Intelligence 39(6), 2017, 1137-1149"
    locator: "Section 3.1.1, Anchors (the single-scale feature map with multi-scale anchors that FPN replaces)"
---

A feature pyramid network (FPN) turns one convolutional network into a pyramid of feature maps, one for each scale, that all carry strong, high-level features. A classification network computes maps of falling resolution: the early maps are fine but carry low-level features such as edges, and the late maps carry the meaning of the image at a coarse stride. FPN adds a top-down path. It starts at the coarsest map, upsamples it by 2 again and again, and at each step adds the map of the same size from the bottom-up path through a $1 \times 1$ convolution, the lateral connection. The result is a map at each stride, 4 to 32 pixels for $P_2$ to $P_5$, that is both fine and semantic. A detector then works on each level with one shared head: small objects on the fine levels, large ones on the coarse levels. With [Faster R-CNN](/faster-r-cnn/) it raised the COCO results of single models at little extra cost, and it is the backbone of [Mask R-CNN](/mask-r-cnn/), RetinaNet and most later detectors.

## In plain words

A detector must find both small and large objects. The old answer was to shrink the photo several times and run the detector on each copy, an [image pyramid](/image-pyramid/), which is slow. A network already makes maps at several sizes inside, but the big early maps know only about edges and colours, while the small late maps know about objects but are too coarse to place small things. FPN fixes this by passing the meaning back down. It takes the small late map, makes it twice as large, and adds the matching earlier map to it. It repeats this down to the largest map. Every map in the result now knows about objects and is sharp at its own size. Small objects are found on the large maps and large objects on the small maps.

## When it applies

The technique needs a backbone network with stages of stride $2^l$, such as a ResNet with outputs $C_2, C_3, C_4, C_5$ at strides 4, 8, 16 and 32. It applies to any task that has to find things over a wide range of sizes in one image: [object detection](/object-detection/), [instance segmentation](/instance-segmentation/), [semantic](/semantic-segmentation/) and [panoptic](/panoptic-segmentation/) segmentation, and keypoint detection. The upsampling by 2 needs the map sizes of the levels to differ by a factor of exactly 2, so the input is padded to a multiple of the largest stride. FPN is a part of the network and is trained with it; it is not a separate algorithm that runs on a fixed network.

## The template

```pseudo id=template
FPN(C_2, ..., C_5)                    ▷ C_l has stride 2^l, any number of channels
L1  P_5 ← conv1×1(C_5) to d channels
L2  for l = 4 down to 2
L3      P_l ← UPSAMPLE2(P_{l+1}) + conv1×1(C_l)   ▷ nearest neighbor upsampling by 2
L4  for l = 2, ..., 5: P_l ← conv3×3(P_l)          ▷ reduces the aliasing of the upsampling
L5  P_6 ← subsample P_5 by 2                       ▷ only for the proposal stage
L6  apply one head with shared weights to every level P_l
L7  for a region of interest of size w × h, pool it from P_k with
        k = clamp(⌊4 + log2(√(wh) / 224)⌋, 2, 5)
```

All levels have the same number of channels, $d = 256$ in the paper, so that one head with shared weights fits on every level. The lateral and output convolutions are plain linear layers; the paper reports that adding nonlinearities to them made little difference.

**Anchors on the levels.** For the region proposal network, the paper puts anchors of one area on each level, $32^2, 64^2, 128^2, 256^2, 512^2$ on $P_2$ to $P_6$, each with the ratios 1:2, 1:1 and 2:1, so 15 [anchor](/anchor-boxes/) shapes in all and 3 per position. The labels follow the IoU rule of Faster R-CNN, now over the anchors of all levels together.

**Region to level (line L7).** For the second stage, an RoI of size $w \times h$ in image pixels is pooled from level $k = \lfloor k_0 + \log_2(\sqrt{wh}/224) \rfloor$ with $k_0 = 4$. The constant 224 is the input size of ImageNet pretraining, so an RoI of that size goes to $P_4$, the level of stride 16 that single-scale Faster R-CNN used. The level drops by one each time the side halves. The paper's formula has no clamp; implementations clamp $k$ to the levels that exist.

## Classic examples

- **Faster R-CNN with FPN.** The RPN works on $P_2$ to $P_6$ and the second stage pools from $P_2$ to $P_5$ by the rule of line L7. The paper reports COCO test-dev AP 36.2 with ResNet-101 for a single model.
- **Mask R-CNN.** [Mask R-CNN](/mask-r-cnn/) uses the same FPN and the same level rule for its box and mask heads, with RoIAlign in place of [RoI pooling](/roi-pooling/).
- **RetinaNet.** The one-stage detector of the [focal loss](/focal-loss/) paper uses levels $P_3$ to $P_7$ and 9 anchors per position, with one classification and one box head shared across the levels.
- **Segmentation heads.** Panoptic FPN merges all levels into one map at stride 4 for [semantic segmentation](/semantic-segmentation/). Encoder-decoder networks such as U-Net have the same shape of top-down path with skip connections, but predict only on the finest level.

## Variations

- **No top-down path.** The [single shot multibox detector](/single-shot-multibox-detector/) predicts on the maps of the bottom-up path directly and adds new coarser layers on top. The FPN paper notes that it does not use the earlier maps of higher resolution, which matter for small objects.
- **Bottom-up path again.** PANet adds a second bottom-up path after the top-down one, so that fine localization reaches the coarse levels by a short path.
- **Weighted and repeated merging.** BiFPN of EfficientDet repeats top-down and bottom-up merging several times and learns a weight for each input of a sum. NAS-FPN finds the connections by architecture search.
- **Merge by concatenation.** Some detectors, such as YOLOv3, concatenate the upsampled map with the lateral map instead of adding them.
- **Image pyramid of features.** Featurized image pyramids run the whole network on each scale of an [image pyramid](/image-pyramid/); they are more accurate in some settings but several times slower, and FPN aims to get most of the gain at the cost of one pass.

## Pitfalls

- **Map sizes that do not match.** With an input side that is not a multiple of 32, a stride-2 stage rounds and the upsampled map is one cell larger or smaller than the lateral map. Pad the input or crop the upsampled map.
- **No $3 \times 3$ convolution after the merge.** Nearest neighbor upsampling repeats each value in a $2 \times 2$ block; the paper adds the $3 \times 3$ convolution to reduce this aliasing.
- **Different channel counts.** A shared head needs the same $d$ on every level; the lateral $1 \times 1$ convolutions exist for this as much as for mixing.
- **Level rule without a clamp.** For an RoI of side 32 the formula gives $\lfloor 4 + \log_2(1/7) \rfloor = 1$, a level that does not exist. Clamp to the levels of the network.
- **Anchors on the wrong level.** The anchor size of a level should match the stride of the level; one anchor size per level with 3 shapes is what the paper uses, and more scales per level, as in RetinaNet, are a separate choice.
- **Cost of the finest level.** $P_2$ has 16 times the cells of $P_4$; heads that are heavy per cell, such as dense one-stage heads, often start at $P_3$.

## Exercises

1. An RoI is $112 \times 112$ pixels. Which level does the rule of line L7 choose? *Answer:* $\log_2(112/224) = -1$, so $k = 3$, the level of stride 8.
2. An RoI is $64 \times 256$. Which level? *Answer:* $\sqrt{wh} = 128$, $\log_2(128/224) \approx -0.81$, so $k = \lfloor 3.19 \rfloor = 3$.
3. An RoI is $400 \times 500$. *Answer:* $\sqrt{wh} \approx 447.2$, $\log_2(447.2/224) \approx 0.998$, so $k = \lfloor 4.998 \rfloor = 4$; a slightly larger RoI of $448 \times 448$ gives exactly $k = 5$.
4. Show that nearest neighbor upsampling by 2 followed by a $2 \times 2$ average pooling of stride 2 gives back the original map, and that the reverse order does not. *Answer:* each $2 \times 2$ block after upsampling holds four copies of one value, whose mean is that value; average pooling first loses the differences inside each block, which upsampling cannot restore.
5. A ResNet input of $800 \times 1216$ pixels gives which sizes of $P_2$ to $P_6$? *Answer:* $200 \times 304$, $100 \times 152$, $50 \times 76$, $25 \times 38$ and $13 \times 19$, where $P_6$ subsamples $P_5$ with stride 2 and rounds up.
6. How many anchors does the RPN of the paper place on an $800 \times 1216$ input? *Answer:* 3 per position on each level, so $3(60800 + 15200 + 3800 + 950 + 247) = 3 \cdot 80997 = 242991$.

## References
