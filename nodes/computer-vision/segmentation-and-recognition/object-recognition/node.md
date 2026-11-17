---
tag: KGNJX9
kind: problem
slug: object-recognition
name: Object recognition
aliases:
- visual recognition
area: computer-vision/segmentation-and-recognition
level: intro
summary: "Say which known objects or object classes an image shows, from instance recognition of one particular object to recognition of a category."
prereqs: [digital-image]
see_also: [object-detection, alignment-recognition, bag-of-visual-words, eigenfaces, spatial-verification, semantic-segmentation, instance-segmentation, image-retrieval]
sources:
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 6, Recognition: Section 6.1 (instance recognition), Section 6.2 (image classification), Section 6.3 (object detection), Section 6.4 (semantic segmentation)"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004, 91-110"
    locator: "The recognition of known objects by matching keypoints, clustering the matches with a Hough transform on pose, and checking each cluster with an affine fit"
  - paper: doi:10.1007/s11263-009-0275-4
    title: "Mark Everingham, Luc Van Gool, Christopher K. I. Williams, John Winn and Andrew Zisserman, The PASCAL Visual Object Classes (VOC) challenge, International Journal of Computer Vision 88(2), 2010, 303-338"
    locator: "The classification, detection and segmentation tasks on 20 classes, and their evaluation"
  - paper: doi:10.1007/s11263-015-0816-y
    title: "Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg and Li Fei-Fei, ImageNet large scale visual recognition challenge, International Journal of Computer Vision 115(3), 2015, 211-252"
    locator: "The classification task with 1000 classes, the top-5 error, and the results of the challenge from 2010 to 2014"
---

Object recognition is the problem of saying which objects an image shows. It ranges from *instance recognition*, finding one particular object such as a given book cover or building, to *category recognition*, saying that the image contains a dog or a car of any kind. The answer can be a label for the whole image, a box for each object as in [object detection](/object-detection/), or a label for each pixel as in [semantic segmentation](/semantic-segmentation/). The hard part is that the same object gives very different pixels under changes of viewpoint, light, occlusion and, for a category, the shape and look of each member.

## In plain words

You show the computer a photo and ask "what is in it?" The question can mean different things. "Is this my car?" asks about one particular object. "Is there a car?" asks about a kind of object. "Where are all the cars?" also asks for their positions.

A photo is only a grid of numbers. The same car looks different from the front and from the side, in sun and in shade, and half hidden behind a tree. Two cars of different makes look more different still. A recognition method must give the same answer for all these pictures and a different answer for a picture of a truck. Older methods matched small distinctive patches or counted typical patterns. Modern methods learn the whole mapping from many labelled photos.

## Definition

Fix a finite set of labels $C$: either a set of known object instances, each given by one or more model images, or a set of categories, each given by labelled training images. The input is a [digital image](/digital-image/) $I$. The problem has three common output forms:

- **Classification.** A label $c \in C$, or a score for each label, for the image as a whole. Single-label classification assumes one main object; multi-label classification asks for every label present.
- **Detection.** A set of triples (label, box, score), one for each object; see [object detection](/object-detection/).
- **Segmentation.** A label for each pixel ([semantic segmentation](/semantic-segmentation/)), or a mask for each object ([instance segmentation](/instance-segmentation/)).

There is no closed-form correct answer: the ground truth is what human annotators say, and a method is judged by its error on a labelled test set, such as the top-5 error of ImageNet classification (the true label is not among the five best-scored labels) or the [detection mean average precision](/detection-mean-average-precision/) of PASCAL VOC and COCO.

## Variants

- **Instance recognition.** Find a known rigid object, often with its pose. Local features and geometry solve it well, because the object has the same texture in every image.
- **Category recognition.** Find any member of a class. The members differ in shape and appearance, so the method must learn what the class has in common.
- **Closed set and open set.** In a closed set every input belongs to one of the labels; in an open set the method must also say "none of these".
- **Fine-grained recognition.** Tell apart close categories, such as bird species or car models.
- **Face recognition and verification.** Name a person, or say whether two faces are of the same person.
- **Few-shot and zero-shot recognition.** Recognize a class from a few examples, or from a description only.

## Examples

- **A book cover.** Given one photo of a cover, find it in a photo of a shelf. Matching [SIFT](/sift/) keypoints and checking that the matches agree with one affine or projective map finds it even when it is small, rotated and partly hidden.
- **The 20 PASCAL VOC classes.** Person, car, cat, chair, bottle and 15 more, in everyday photos with clutter and several objects per image.
- **ImageNet classification.** 1000 classes and over a million training images; the score is the top-1 or top-5 error.
- **A non-example.** Finding the edges or the corners of an image is not recognition; it names no object. Matching two photos of the same scene for 3D reconstruction is not recognition either, although it uses the same features.

## Known algorithms

- **Alignment and hypothesis testing.** [Alignment recognition](/alignment-recognition/) and [geometric hashing](/geometric-hashing/) find a transform that maps model features onto image features and check the rest of the model under it.
- **Local features with geometric checks.** Lowe (2004) matches SIFT keypoints to a database, groups the matches with a Hough transform on pose, and checks each group with an affine fit. [Spatial verification](/spatial-verification/) with [RANSAC](/ransac/) is the general form.
- **Appearance subspaces.** [Eigenfaces](/eigenfaces/) project an image onto principal components of training faces and compare in that subspace.
- **Bags of features.** The [bag of visual words](/bag-of-visual-words/) represents an image by a histogram of quantized local features, with [spatial pyramid matching](/spatial-pyramid-matching/), [Fisher vectors](/fisher-vector/) or [VLAD](/vlad/) as stronger encodings, and a classifier such as a [support vector machine](/support-vector-machine/) on top.
- **Part-based models.** [Pictorial structures](/pictorial-structures/), the [deformable part model](/deformable-part-model/) and the [implicit shape model](/implicit-shape-model/) model an object as parts with a flexible layout.
- **Convolutional networks.** Since 2012, networks trained end to end on large labelled sets give the best results for classification, and their features drive detectors such as [R-CNN](/r-cnn/) and [Faster R-CNN](/faster-r-cnn/).

## Bounds

The problem has no useful worst-case lower bound; the measure of a method is its error rate on a benchmark, and every number below depends on the data set, the metric and the year. On ImageNet classification, Russakovsky et al. (2015) report that the top-5 error of the winning entries fell from about 28 percent in 2010 to under 7 percent in 2014, with the largest single drop in 2012, when a convolutional network won. For instance recognition, the cost is the matching: with $m$ features in the image and $M$ in a database, exact nearest-neighbour search costs $O(mM)$ distance computations, and approximate search with trees or quantization makes it sublinear in $M$ in practice. Alignment that tries every triple of model points against every triple of image points has $O(m^3 n^3)$ hypotheses for $m$ model and $n$ image features, which is why indexing and voting methods were developed.

## Reductions

- **Detection to classification.** [Sliding-window detection](/sliding-window-detection/) runs an image classifier on every window of an [image pyramid](/image-pyramid/), and proposal-based detectors classify a few thousand candidate regions.
- **Instance recognition to retrieval.** Recognizing a known object among many is [image retrieval](/image-retrieval/) with a geometric check of the top results.
- **Segmentation to classification.** A pixel label is a classification of the pixel with its context.

## Applications

Photo search and organization, visual search on phones, industrial inspection and bin picking, face unlock and photo tagging, driver assistance and autonomous driving (pedestrians, cars and signs), medical imaging, robotics, and content filtering.

## References
