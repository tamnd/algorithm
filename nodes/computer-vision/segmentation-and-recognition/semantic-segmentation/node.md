---
tag: XBE0S3
kind: problem
slug: semantic-segmentation
name: Semantic segmentation
aliases:
- pixel labeling
- scene parsing
area: computer-vision/segmentation-and-recognition
level: core
summary: Assign a class label from a fixed set, such as road, car or sky, to every pixel of an image.
prereqs: [image-segmentation, object-recognition]
see_also: [mean-intersection-over-union, instance-segmentation, panoptic-segmentation, dense-crf, potts-model, image-segmentation-graph-cuts, conditional-random-field, slic-superpixels]
sources:
  - paper: doi:10.1109/CVPR.2015.7298965
    title: "Jonathan Long, Evan Shelhamer and Trevor Darrell, Fully convolutional networks for semantic segmentation, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015, 3431-3440 (arXiv 1411.4038)"
    locator: "Section 1 and Section 3 (dense prediction with a network that has only convolutional layers, upsampling and skip layers), Section 5 (the metrics pixel accuracy, mean accuracy, mean IU and frequency weighted IU)"
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "the segmentation task and Section 4.2.1 (20 object classes and background, the void label and its border band, the accuracy of Eq. (4))"
  - paper: arxiv:1210.5644
    title: "Philipp Krähenbühl and Vladlen Koltun, Efficient inference in fully connected CRFs with Gaussian edge potentials, NIPS 2011"
    locator: "the pixel labeling model with unary terms from a classifier and pairwise Potts terms over all pairs of pixels"
  - paper: doi:10.1109/34.969114
    title: "Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239"
    locator: "Section 6.1 with Theorem 6.1 (the factor 2 bound of expansion moves for the Potts model), Section 7 and the Appendix (NP-hardness of the Potts energy)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.4, Semantic segmentation"
---

Semantic segmentation is the problem of giving every pixel of an image one label from a fixed set of classes, such as road, car, person or sky. The output is a label map of the same size as the image. It joins [image segmentation](/image-segmentation/), which cuts the image into regions, with [object recognition](/object-recognition/), which names what is there. It does not separate objects of the same class: two cars that touch become one region of car pixels. Separating them is [instance segmentation](/instance-segmentation/), and doing both for every pixel is [panoptic segmentation](/panoptic-segmentation/). The standard score is the [mean intersection over union](/mean-intersection-over-union/).

## In plain words

You give the computer a photo and a list of kinds of things, for example road, building, tree, car, person and sky. The computer must paint every pixel of the photo with the color of the kind of thing that the pixel shows. The result looks like a coloring book page that someone filled in. It does not say how many cars there are. Two cars side by side get the same color and become one patch. To score the result, people compare it with a version painted by hand, class by class. Pixels on borders that are hard to judge are often left out of the score.

## Definition

Fix a set of classes $C = \{0, \ldots, K - 1\}$. The input is a [digital image](/digital-image/) $I$ of $W \times H$ pixels. The output is a label map $\ell$ with $\ell(u, v) \in C$ for every pixel $(u, v)$.

The ground truth is a label map $g$ drawn by people, where a pixel may also have the void label. Void marks pixels that are unclear, outside the classes, or on a thin band along object borders, and void pixels are not scored. PASCAL VOC uses 20 object classes and background, with the void label 255 and a void band of 5 pixels along the borders. A method is scored over a test set by the mean intersection over union of the classes. Pixel accuracy is also reported, but it favors large classes.

A method is usually a function learned from training images with labels. The problem has no unique correct output for an image: the labels of people differ near borders and for unclear regions, and the task is defined by the data set and its metric.

## Variants

- **Binary segmentation.** Two classes, foreground and background, as in figure and ground separation or in medical images of one organ.
- **Interactive segmentation.** A user marks some pixels or draws a box, and the method labels the rest; see [interactive segmentation](/interactive-segmentation/) and [GrabCut](/grabcut/).
- **Scene parsing.** Many classes that cover all pixels of a scene, both objects and amorphous regions such as grass, sky and road.
- **Video.** A label map for each frame, with labels that should be stable over time.
- **3D data.** Labels for points of a point cloud or for voxels, from lidar or depth sensors.
- **Weak supervision.** Training with image-level labels, boxes or scribbles instead of full label maps.
- **Open vocabulary.** Classes given at test time by words.

## Examples

- **A street scene.** In a photo of a street, the pixels of the road get the label road, those of the parked cars car, and those of the sky sky. The label map has one region of car pixels where three cars stand bumper to bumper.
- **A small object.** A traffic sign of 10 by 10 pixels has 100 pixels in an image of a million. If it is labeled pole, the pixel accuracy drops by 0.0001. If traffic sign pixels are rare in the test set, the IoU of that class drops by a large amount, and the mIoU with it.
- **A non-example.** A box around each car with the label car is [object detection](/object-detection/). A partition of the image into regions without class names is image segmentation.

## Known algorithms

- **Classifier and smoothness.** A classifier gives a score for each class at each pixel from local features, for example a [random forest](/random-forest/) or [logistic regression](/logistic-regression/). A [conditional random field](/conditional-random-field/) adds a [Potts model](/potts-model/) term that makes neighbors prefer the same label. Inference uses [graph cuts](/image-segmentation-graph-cuts/) for two labels, [alpha expansion](/alpha-expansion/) for more labels, or mean field. The [dense CRF](/dense-crf/) connects all pairs of pixels and uses mean field with fast filtering.
- **Regions first.** Superpixels from [SLIC](/slic-superpixels/), [Felzenszwalb and Huttenlocher](/felzenszwalb-segmentation/) or [mean shift](/mean-shift-segmentation/) are classified as units, which makes the labels follow image edges.
- **Fully convolutional networks.** Long, Shelhamer and Darrell (2015) turned a classification network into one that outputs a score map, upsampled it to the image size, and combined it with finer layers. Later networks use encoder and decoder paths, dilated convolutions, pyramid pooling or attention. Some use a dense CRF as a last step. The cost and the quality of these networks are outside this page; their quality is a benchmark result.
- **Mask classification.** Recent methods predict a set of masks, each with a class, and so solve semantic, instance and panoptic segmentation with one model.

## Bounds

There is no lower bound on the error of a method. Methods are compared by benchmark results, which depend on the data set, the metric and the year. The output space has $K^{WH}$ label maps. For the energy of a classifier plus a Potts term, three theorems of Boykov, Veksler and Zabih (2001) apply. For two labels and nonnegative pair weights, the minimum is a minimum cut, found exactly in polynomial time. For three or more labels, the minimum is NP-hard to find. Alpha expansion finds a labeling whose energy is at most twice the minimum. Scoring a label map costs $O(WH + K^2)$ with a confusion matrix.

## Reductions

- **To pixel classification.** Each pixel is classified with the help of a window around it. Without a smoothness term, the problem is $WH$ independent classification problems.
- **From panoptic segmentation.** Dropping the instance ids of a panoptic segmentation gives a semantic segmentation.
- **From instance segmentation, for objects.** The union of the masks of each class gives the object part of a label map. Amorphous classes such as sky still need a semantic method.
- **To energy minimization.** With a classifier for the unary terms and a Potts term, the problem becomes MAP inference in a [Markov random field](/markov-random-field/).

## Applications

Driving scenes for autonomous vehicles and driver assistance; medical images, such as organs and tumors in CT and MRI; land cover from satellite and aerial images; robot navigation; photo editing, such as sky replacement and background blur; and as an input for depth estimation, scene understanding and 3D reconstruction.

## References
