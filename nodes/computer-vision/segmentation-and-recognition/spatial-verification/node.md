---
tag: 4CHNHR
kind: technique
slug: spatial-verification
name: Spatial verification
aliases:
- geometric verification
- geometric reranking
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Re-rank the top retrieved images by fitting a geometric transformation to their matches with the query and counting inliers."
prereqs: [image-retrieval, bag-of-visual-words, ransac]
see_also: [lo-ransac, query-expansion, homography-estimation, lowe-ratio-test, vocabulary-tree, hough-transform, visual-place-recognition, mean-average-precision]
sources:
  - paper: doi:10.1109/CVPR.2007.383172
    title: "James Philbin, Ondrej Chum, Michael Isard, Josef Sivic and Andrew Zisserman, Object retrieval with large vocabularies and fast spatial matching, CVPR 2007"
    locator: "The spatial re-ranking: hypotheses with 3, 4 or 5 degrees of freedom from single correspondences of affine regions, refinement to an affine transformation with LO-RANSAC, the re-ranking of the top 1000 images, and the results on Oxford 5K in Table 7"
  - paper: doi:10.1109/ICCV.2003.1238663
    title: "Josef Sivic and Andrew Zisserman, Video Google: a text retrieval approach to object matching in videos, ICCV 2003, volume 2, 1470-1477"
    locator: "The spatial consistency check that re-ranks retrieved frames by the matches whose neighbors also match"
  - paper: doi:10.1007/978-3-540-88682-2_24
    title: "Herve Jegou, Matthijs Douze and Cordelia Schmid, Hamming embedding and weak geometric consistency for large scale image search, ECCV 2008, Lecture Notes in Computer Science, 304-317"
    locator: "Weak geometric consistency: votes on the differences of orientation and log scale of the matched features, applied to all images during the search"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004, 91-110"
    locator: "Section 7, object recognition: Hough clustering of the matches by pose, then the least squares affine fit and the verification of each cluster"
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "The random sample consensus scheme that spatial verification uses to find the transformation with the most inliers"
---

Spatial verification is the second stage of [image retrieval](/image-retrieval/). The first stage, usually a [bag of visual words](/bag-of-visual-words/) search, ranks images by the visual words they share with the query and ignores where the words are. For each of the top $R$ images, spatial verification takes the tentative matches (features of the query and of the image with the same word), fits a geometric transformation to them with a robust method such as [RANSAC](/ransac/), and counts the matches that the transformation explains. Images with many such inliers are moved to the top. The method is a heuristic: a large inlier count is strong evidence that the two images show the same object, but it is not a proof.

## In plain words

The first search only checks which kinds of patches two pictures have in common, like checking that two texts use the same words. It does not check the word order. A picture of a different building with the same kind of windows can score high.

The check looks at where the shared patches are. If the two pictures show the same object, one simple movement of the image (a shift, a turn, a change of size, a slant) carries most of the patches of the query onto their partners. For each of the best results, the check finds the movement that carries the most patches, and counts them. Many agreeing patches mean a real match.

## When it applies

- The first stage returns a ranked list, and you can afford a more costly test on its top part, usually the top 100 to 1000 images.
- The features have positions, and also scale, orientation or an affine shape if you want one-match hypotheses. [SIFT](/sift/) features and affine covariant regions have these.
- The object is close to rigid and close to planar, or seen from similar views, so that one transformation of the image plane explains most of the true matches. For general 3D scenes, an epipolar model (the fundamental matrix) is used instead.
- The query has enough features on the object. Small objects with few features give few inliers.

## The template

```pseudo id=main
SPATIAL-VERIFY(q, ranked list, R, t_min)
L1  for each image d among the top R of the ranked list do
L2      M ← the tentative matches: pairs of features of q and d with the same visual word
L3      for each hypothesis T made from one match or from a minimal sample of M do
L4          inliers(T) ← the matches in M whose query feature T maps near its partner
L5      T* ← the hypothesis with the most inliers, refined on its inliers
L6      score(d) ← the number (or the idf sum) of the inliers of T*
L7      mark d as verified if it has at least t_min inliers
L8  re-rank the top R: verified images first, by score, then the others in the old order
L9  return the new list
```

Lines L3 and L4 are a consensus search. With features that have a position, a scale and an orientation, one match fixes a similarity transformation (4 degrees of freedom). With affine regions, one match fixes an affine transformation. Then the hypotheses can be listed one per match, with no random sampling, and the search is deterministic. With points only, use RANSAC on minimal samples of 3 matches for an affine map or 4 for a [homography](/homography-estimation/). Line L5 refines the best hypothesis, for example with [LO-RANSAC](/lo-ransac/) or least squares on the inliers.

**Example.** The query features have unit scale and the image features have scale 2. The tentative matches are $(1, 1) \to (12, 2)$, $(3, 1) \to (16, 2)$, $(2, 4) \to (14, 8)$, $(5, 3) \to (20, 6)$ and $(4, 4) \to (3, 15)$. A hypothesis with scale and translation (3 degrees of freedom) comes from one match: the scale is the ratio of the feature scales, $s = 2$, and $t = g - s f$. The first match gives $t = (10, 0)$, and the map $f \mapsto 2f + (10, 0)$ sends each of the first four query points exactly onto its partner, so it has 4 inliers. The last match gives $t = (3, 15) - (8, 8) = (-5, 7)$, which explains only that match. So $T^*$ has 4 inliers, and the fifth match is an outlier. With $t_{\min} = 4$, the image is verified. If the first stage ranked images $d_1, d_2, d_3$ and their best inlier counts are 2, 9 and 5, then $d_2$ and $d_3$ are verified and the new order is $d_2, d_3, d_1$.

## Classic examples

- **Video Google** (Sivic and Zisserman 2003). After the text-style search, a retrieved frame gets a higher score when the matched regions have neighbors that also match. This is a local test of spatial consistency, with no global transformation.
- **Lowe (2004).** For object recognition with SIFT, each match votes in a coarse Hough space of position, orientation and scale. Each bin with at least 3 votes is checked by a least squares affine fit, and matches that disagree are removed until the fit is stable.
- **Fast spatial matching** (Philbin et al. 2007). For each of the top 1000 images, each tentative match of two affine regions gives a hypothesis with 3, 4 or 5 degrees of freedom. The best one is refined to a 6 degree of freedom affine map with LO-RANSAC. An image needs at least 4 inliers to be re-ranked, and its score is the sum of the idf weights of the inliers. On Oxford 5K with a vocabulary of 1M words, the mean average precision rose from 0.618 to between 0.645 and 0.664 with the three hypothesis types (Table 7). That is a benchmark result.
- **Query expansion.** [Average query expansion](/query-expansion/) uses spatial verification to choose the results that it adds to the query. Chum et al. (2007) count an image as verified when it has more than 20 inliers.

## Variations

- **Weak geometric consistency** (Jegou et al. 2008). Each match votes for its difference of orientation and of log scale. Only the matches in the peak bins count. This needs no fit and runs on all the images during the search, not only on a short list.
- **Hough voting on the matches.** Each match votes for a transformation, and peaks of the vote space are the hypotheses. This is the idea of the [Hough transform](/hough-transform/) applied to matches.
- **Epipolar verification.** For 3D scenes with large changes of view, fit a fundamental matrix with RANSAC on 7 or 8 point samples. The test is weaker, since a point only has to lie near a line.
- **Verification for places.** In [visual place recognition](/visual-place-recognition/), the inlier count of the best match also decides whether the place is known or new.

## Pitfalls

- **Bursts and repeated structure.** Windows, tiles and fences give many matches to the same word, and a wrong transformation can collect many inliers. Count at most one match for each query feature and for each image feature.
- **Many tentative matches.** A word with many features in both images gives a product of matches. Drop the words with too many features, or keep only the best few matches for each.
- **A planar model for a non planar scene.** An affine map or a homography fits only one plane, or a distant scene. A 3D object seen from very different views gets few inliers, even for a correct match.
- **Fixed thresholds.** The inlier error threshold must follow the image size and the feature precision. The minimum inlier count trades false matches against missed ones and must be tuned on the data.
- **Cost.** Verification costs much more per image than the first stage. Its time grows linearly with $R$, so $R$ limits how deep in the list a true match can be found.

## Exercises

1. In the example, list all five hypotheses and their inlier counts with an error threshold of 1 pixel. Explain why the last match cannot be an inlier of any hypothesis from the other four.
2. With $n$ tentative matches and one hypothesis per match, show that lines L3 and L4 take $O(n^2)$ time. Compare this with RANSAC on samples of 3 matches when one third of the matches are inliers, using the [RANSAC iteration bound](/ransac-iteration-bound/) for a success probability of 0.99.
3. Construct a query and an image with a repeated pattern of 4 identical windows in a row, so that a wrong translation gets 3 inliers while the correct one gets 4. What changes if each feature may be used in at most one match?
4. Explain why weak geometric consistency cannot reject a match that has the right scale and orientation change but the wrong position.

## References
