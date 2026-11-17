---
tag: YXFK3J
kind: problem
slug: visual-place-recognition
name: Visual place recognition
aliases:
- image-based localization by retrieval
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Recognize from an image which known place it was taken at, by retrieval against a database of geotagged images under changes of light and season."
prereqs: [image-retrieval, precision-and-recall]
see_also: [loop-closure-detection, vlad, vocabulary-tree, spatial-verification, global-localization, kidnapped-robot-problem, perspective-n-point, query-expansion]
sources:
  - paper: doi:10.1109/TRO.2015.2496823
    title: "Stephanie Lowry, Niko Sunderhauf, Paul Newman, John J. Leonard, David Cox, Peter Corke and Michael J. Milford, Visual place recognition: a survey, IEEE Transactions on Robotics 32(1), 2016, 1-19"
    locator: "The definition of a place, the description of places by images, the use of appearance change and perceptual aliasing as the main difficulties, and the survey of methods"
  - paper: doi:10.1109/CVPR.2016.572
    title: "Relja Arandjelovic, Petr Gronat, Akihiko Torii, Tomas Pajdla and Josef Sivic, NetVLAD: CNN architecture for weakly supervised place recognition, CVPR 2016, 5297-5307"
    locator: "The task as retrieval against geotagged street-level images, the recall at N with a distance threshold of 25 meters, and the results on the Pittsburgh and Tokyo 24/7 data sets"
  - paper: doi:10.1177/0278364908090961
    title: "Mark Cummins and Paul Newman, FAB-MAP: probabilistic localization and mapping in the space of appearance, International Journal of Robotics Research 27(6), 2008, 647-665"
    locator: "The probability that an observation comes from each known place or from a new place"
  - paper: doi:10.1109/ICRA.2012.6224623
    title: "Michael J. Milford and Gordon F. Wyeth, SeqSLAM: visual route-based navigation for sunny summer days and stormy winter nights, ICRA 2012, 1643-1649"
    locator: "The matching of short sequences of small normalized images along straight lines of the difference matrix, across day and night and across seasons"
  - paper: doi:10.1109/CVPR.2015.7298790
    title: "Akihiko Torii, Relja Arandjelovic, Josef Sivic, Masatoshi Okutomi and Tomas Pajdla, 24/7 place recognition by view synthesis, CVPR 2015, 1808-1817"
    locator: "The Tokyo 24/7 query set taken by day, at sunset and at night, and the synthesis of new views of the database"
---

Visual place recognition asks where a photo was taken, by finding the known place it shows. The known places are given by a database of images with positions, for example street-level images with GPS tags or the key frames of a map. The query is answered by [image retrieval](/image-retrieval/): the database images most similar to the query give its place. The hard parts are perceptual aliasing (different places that look alike) and appearance change (the same place by day and by night, in summer and in winter). [Loop closure detection](/loop-closure-detection/) is a special case: a SLAM system recognizes places in its own past trajectory, online, and turns a match into a pose constraint. Place recognition in general also matches against databases built by other cameras at other times, and its answer is a place or a position, not a constraint.

## In plain words

You see a photo of a street corner and want to know which corner it is. You have a large set of photos of the city, each marked with where it was taken. Find the photos in the set that look most like the new one, and read off their places.

Two things make this hard. Many corners look alike, with the same shops, signs and trees. And one corner looks very different at night, in snow, or with a bus in front. A good method must ignore what changes, and still notice the small things that make each place different.

## Definition

**Input.** A database $\mathcal{D} = \{(I_j, p_j)\}_{j=1}^{N}$ of images $I_j$ with positions $p_j$ (in a plane, or on the map of a robot), and a query image $q$ taken at an unknown position $p_q$.

**Output.** A ranked list of database images, or the place of the best one, $\hat p = p_{j^*}$.

**Correctness.** For a distance threshold $\delta$, a retrieved image $I_j$ is correct when $\lVert p_j - p_q \rVert \le \delta$. A query is localized at $N$ when at least one of the top $N$ images is correct. The recall at $N$ is the fraction of queries localized at $N$. The NetVLAD paper uses $\delta = 25$ meters for street-level images. Since the true position comes from GPS or from a map, the ground truth itself has errors of a few meters.

**Open set.** In the robot setting the query can show a place that is not in the database. The answer must then be "new place", and methods are judged by [precision and recall](/precision-and-recall/) of the accepted matches, as in loop closure detection.

There is no exact answer to compute in general. Methods are compared by recall at $N$ or by precision and recall on data sets with ground truth, so all claims of quality below are benchmark results.

## Variants

- **Single image retrieval.** One query image against a database of single images. This is the setting of the NetVLAD paper, with the Pittsburgh and Tokyo 24/7 data sets.
- **Sequence matching.** The query and the database are image sequences along a route. SeqSLAM (Milford and Wyeth 2012) compares short sequences instead of single images. A run of matches along a line of constant speed in the difference matrix is much less likely to be wrong than one match.
- **Open set with a new-place decision.** FAB-MAP (Cummins and Newman 2008) computes the probability that the observation comes from each known place or from a new place.
- **Across conditions.** Day against night, or summer against winter. Tokyo 24/7 (Torii et al. 2015) has queries by day, at sunset and at night.
- **Place as a class.** Each place is a class, and a classifier gives the place directly. This works for a fixed set of places but does not add new places without training.

## Examples

Three queries and a database along a road, with $\delta = 25$ meters. The table lists the positions of the top 3 retrieved images.

| Query | True position | Top 3 positions (m) | Localized at |
|---|---|---|---|
| $q_1$ | 0 | 5, 40, 90 | 1 |
| $q_2$ | 12 | 50, 10, 60 | 2 |
| $q_3$ | 30 | 90, 80, 70 | not in top 3 |

The recall at 1 is $1/3$, the recall at 2 and at 3 is $2/3$. The first result of $q_2$ is a place 38 meters away that looks like the true one: a case of perceptual aliasing. Spatial verification or a sequence check might move the correct image to the top.

## Known algorithms

- **Bag of words with an inverted index.** Local features, a [vocabulary tree](/vocabulary-tree/) or a flat vocabulary, tf-idf scores, then [spatial verification](/spatial-verification/) on the top results. DBoW2 and FAB-MAP are of this kind.
- **Global descriptors.** One vector for each image, as [VLAD](/vlad/), a Fisher vector, or NetVLAD, which learns VLAD on top of a convolutional network from weakly labeled street-level images. Search is [nearest neighbor search](/nearest-neighbor-search/), often approximate.
- **Sequence methods.** SeqSLAM and its variants, for long routes driven many times.
- **Re-ranking.** [Query expansion](/query-expansion/) and geometric verification of the short list, often with local features after a global first search.

## Bounds

- **Perceptual aliasing makes the problem impossible in general.** If two different places give the same image, no method can tell which one the query shows. This is a fact about the input, not a property of any method. Only extra information, such as a sequence, odometry or a prior on the position, can separate them.
- **Search cost.** An exhaustive search with global descriptors of dimension $D$ costs $O(N D)$ per query. Approximate search, an inverted index, or a prior on the position makes it faster in practice, with no worst-case guarantee.

## Reductions

- **To image retrieval.** Place recognition is retrieval where the relevance of an image is defined by its distance to the query position. The methods of [image retrieval](/image-retrieval/) apply with this label.
- **Loop closure detection reduces to it.** A SLAM system queries its own key frames, excludes the most recent ones, and keeps a match only after a geometric check. The match is then used as an edge in the pose graph.
- **It is the first step of fine localization.** The retrieved images give a short list of nearby places. Matching local features against the 3D points seen from them and solving [perspective-n-point](/perspective-n-point/) with RANSAC gives the full 6 degree of freedom camera pose.

## Applications

- Loop closure and relocalization for robots and drones, including recovery when the robot is [kidnapped](/kidnapped-robot-problem/).
- Localization of cars in cities where GPS is poor, against a map of images.
- Augmented reality, which needs a coarse position before the precise pose.
- Finding the place of a photo taken from the web, for archives or for checking facts.

## References
