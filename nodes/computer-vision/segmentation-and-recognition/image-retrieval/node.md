---
tag: YH0SPR
kind: problem
slug: image-retrieval
name: Content-based image retrieval
aliases:
- CBIR
- visual instance search
area: computer-vision/segmentation-and-recognition
level: core
summary: Given a query image, rank a large collection by how likely each image is to show the same object or scene.
prereqs: [digital-image, feature-descriptor]
see_also: [bag-of-visual-words, vocabulary-tree, vlad, fisher-vector, spatial-verification, query-expansion, visual-place-recognition, mean-average-precision]
sources:
  - paper: doi:10.1109/ICCV.2003.1238663
    title: "Josef Sivic and Andrew Zisserman, Video Google: a text retrieval approach to object matching in videos, Ninth IEEE International Conference on Computer Vision (ICCV 2003), vol. 2, 1470-1477"
    locator: "Section 1 (object retrieval in video as text retrieval), Section 4 (tf-idf and the inverted file)"
  - paper: doi:10.1109/CVPR.2007.383172
    title: "James Philbin, Ondrej Chum, Michael Isard, Josef Sivic and Andrew Zisserman, Object retrieval with large vocabularies and fast spatial matching, CVPR 2007"
    locator: "Section 2 (the Oxford buildings data set: 5,062 images, 11 landmarks, 55 queries, the labels Good, OK, Junk and Absent, and mean average precision)"
  - paper: doi:10.1109/CVPR.2006.264
    title: "David Nister and Henrik Stewenius, Scalable recognition with a vocabulary tree, CVPR 2006, vol. 2, 2161-2168"
    locator: "The scoring with inverted files at the leaves of a tree of words"
  - paper: doi:10.1109/TPAMI.2011.235
    title: "Herve Jegou, Florent Perronnin, Matthijs Douze, Jorge Sanchez, Patrick Perez and Cordelia Schmid, Aggregating local image descriptors into compact codes, IEEE Transactions on Pattern Analysis and Machine Intelligence 34(9), 2012, 1704-1716"
    locator: "The aggregation of local descriptors into one vector per image and its compression into short codes for search in large collections"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.1, Instance recognition"
---

Content-based image retrieval is the problem of ranking a collection of images by how well each one matches a query image, using only the pixels and not text that comes with the images. This page is about instance retrieval: an image is relevant when it shows the same object, building or scene as the query, seen from another viewpoint, at another scale or under other light. The [bag of visual words](/bag-of-visual-words/) model, the [vocabulary tree](/vocabulary-tree/), [VLAD](/vlad/) and the [Fisher vector](/fisher-vector/) are ways to represent the images. [Spatial verification](/spatial-verification/) and [query expansion](/query-expansion/) are steps that improve a first ranking.

## In plain words

You have a photo of a building, and an archive of a million photos. You want the archive photos that show the same building first in the list, even if they were taken from the other side of the street, at night, or partly hidden by a bus.

Comparing every pixel of the query with every pixel of every photo does not work, because the same building looks different in each photo. Instead, each photo is reduced to many small local patches that look the same from many viewpoints. Two photos of the same building share many such patches. The hard parts are to compare the patches of a million photos fast, and to reject photos that share patches only by chance.

## Definition

**Input.** A database of $N$ images $d_1, \ldots, d_N$, and a query $q$. The query is an image or a rectangle in an image that marks the object of interest.

**Output.** A ranking: a permutation of the database, or its first $k$ entries, with the images most likely to be relevant first. Systems usually also return a score per image.

**Relevance.** An image is relevant when it shows the same object or scene instance as the query region. This is a judgment by people, so it is given as ground truth labels, not as a formula. The problem has no "correct" ranking that an algorithm can be proved to find. An algorithm is measured on labeled data.

**Measure.** The usual measure is [mean average precision](/mean-average-precision/). For one query, the average precision (AP) is the mean, over all relevant images, of the precision at the rank where each relevant image appears, and a relevant image that is never returned adds 0. The mAP is the mean of AP over the queries. On the Oxford buildings set, Philbin et al. label each pair as Good, OK, Junk or Absent. Good and OK images are relevant, and Junk images are removed from the ranking before AP is computed, so a system is neither rewarded nor punished for them.

## Variants

- **Instance against category.** Instance retrieval asks for the same object. Category retrieval asks for any object of the same class (any car, any beach), which is closer to [object recognition](/object-recognition/) and image classification.
- **Whole image against region query.** A region query asks for one object inside the query image and ignores the rest. Video Google and the Oxford protocol use region queries.
- **Near-duplicate detection.** The relevant images are edited copies of the query (crops, rescaling, compression). This is easier, and compact global descriptors often suffice.
- **Place recognition.** [Visual place recognition](/visual-place-recognition/) is retrieval where relevance means "taken near the same place", often with a position tolerance in meters, and with strong changes of season and light.
- **Large scale with distractors.** The Oxford set is extended with 100K or 1M unrelated images to test how the ranking degrades as $N$ grows.
- **Memory-bounded search.** Each image must fit in a fixed number of bytes, for example a short code of a [VLAD](/vlad/) vector compressed with [product quantization](/product-quantization/).

## Examples

**Average precision by hand.** A query has 4 relevant images in the database. The system returns the list relevant, not relevant, junk, relevant, not relevant, relevant, and the fourth relevant image is not returned. If the junk image counts as not relevant, the precisions at the three relevant ranks are $1/1$, $2/4$ and $3/6$, and AP $= (1 + 0.5 + 0.5)/4 = 0.5$. Under the Oxford protocol the junk image is first removed, so the list is relevant, not relevant, relevant, not relevant, relevant, the precisions are $1/1$, $2/3$ and $3/5$, and AP $= (1 + 0.6667 + 0.6)/4 = 0.5667$. The missing relevant image costs a quarter of the maximum in both cases. Implementations of AP differ in small details such as interpolation, so compare only numbers that come from the same evaluation code.

**A bag of words ranking.** The worked example of the [bag of visual words](/bag-of-visual-words/) page ranks three images for a query with tf-idf weights and the cosine score. It gives the scores 0.9487, 0.2448 and 0.0863, and the query reads only 4 entries of the inverted index.

**A data set.** The Oxford buildings set of Philbin et al. (CVPR 2007, Section 2) has 5,062 images of 1024 by 768 pixels collected from Flickr for 11 Oxford landmarks, with 5 query regions per landmark, so 55 queries. Distractor sets of about 100K and 1M further Flickr images are added for the large scale tests.

## Known algorithms

- **Bag of words with an inverted file** (Sivic and Zisserman 2003). Quantize local descriptors to visual words, weight them with [tf-idf](/tf-idf/), and score with an [inverted index](/inverted-index/). See [bag of visual words](/bag-of-visual-words/).
- **Large vocabularies.** The [vocabulary tree](/vocabulary-tree/) (Nister and Stewenius 2006) and approximate k-means with a [randomized k-d forest](/randomized-kd-forest/) (Philbin et al. 2007) give vocabularies of about $10^6$ words.
- **Aggregated vectors.** [VLAD](/vlad/) and the [Fisher vector](/fisher-vector/) turn each image into one dense vector. Search is then [nearest neighbor search](/nearest-neighbor-search/) in that space, usually [approximate](/approximate-nearest-neighbor/) with compressed codes (Jegou et al. 2012).
- **Re-ranking.** [Spatial verification](/spatial-verification/) fits a geometric transformation to the matches between the query and each of the top images, and moves images with many inliers up. [Query expansion](/query-expansion/) issues a new query built from the verified results.
- **Learned global descriptors.** A convolutional network maps an image to one vector, for example NetVLAD (Arandjelovic et al. 2016), which puts a trainable VLAD layer on top of the network. The network is outside this page; the search step is the same nearest neighbor search.

## Bounds

All costs below are in the [real RAM](/real-ram/) with one arithmetic operation per step. Let $N$ be the number of images, $n$ the number of local features in the query, $K$ the number of visual words and $D$ the dimension of a global vector.

- **Linear scan of global vectors.** One query costs $\Theta(N D)$ time and returns the exact ranking under the chosen score. Sorting the scores adds $O(N \log N)$, or $O(N + k \log k)$ for the first $k$.
- **Inverted file.** One query costs the quantization of $n$ features plus the total length of the posting lists of the query words. In the worst case every image contains every query word, and the cost is $O(n N)$; the gain over a scan is a property of the word statistics, not a worst-case bound.
- **High dimension.** For $D$ in the hundreds or thousands, no exact nearest neighbor method is known that is much faster than a scan in the worst case with near linear space. Practical systems use approximate search, which trades a measured loss of recall for speed. See [nearest neighbor search](/nearest-neighbor-search/) and [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).
- **Quality.** There is no theorem about the mAP of a method. All accuracy numbers are benchmark results and depend on the data set, the labels and the version of the evaluation.

## Reductions

- **To text retrieval.** With a [bag of visual words](/bag-of-visual-words/), an image becomes a document over a vocabulary of $K$ words, and the [vector space model](/vector-space-model/) with tf-idf and an inverted file applies without change.
- **To nearest neighbor search.** With one global vector per image (VLAD, Fisher vector, or a network descriptor), retrieval is $k$ nearest neighbor search under the Euclidean distance or the inner product.
- **To robust model fitting.** Spatial verification of one candidate image is an instance of [robust model fitting](/robust-model-fitting/): find the affine or similarity transformation that most tentative matches agree with, usually with [RANSAC](/ransac/).
- **From place recognition and loop closure.** [Visual place recognition](/visual-place-recognition/) and [loop closure detection](/loop-closure-detection/) in SLAM use instance retrieval as their first step, and add a check of the place or the pose.

## Applications

Search in photo collections and video archives (the original Video Google use case was finding an object across the frames of a film), landmark recognition, near-duplicate and copyright detection, product search by photo, place recognition and loop closure for robots, and the choice of image pairs to match in [structure from motion](/structure-from-motion-problem/).

## References
