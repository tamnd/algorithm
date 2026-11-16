---
tag: 5K7F44
kind: technique
slug: mutual-nearest-neighbor-matching
name: Mutual nearest neighbor matching
aliases:
- cross-check matching
- symmetric matching
area: computer-vision/local-features
level: core
summary: Keep a pair only when each feature is the nearest neighbor of the other in descriptor space.
prereqs: [nearest-neighbor-search, feature-descriptor]
see_also: [feature-matching, lowe-ratio-test, left-right-consistency-check, forward-backward-error, loftr, superglue, stable-matching, hungarian-algorithm]
sources:
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 2nd edition, Springer, 2022"
    locator: "Section 7.1.3, feature matching: matching strategies and error rates"
  - paper: doi:10.1109/CVPR46437.2021.00881
    title: "Jiaming Sun, Zehong Shen, Yuang Wang, Hujun Bao and Xiaowei Zhou, LoFTR, detector-free local feature matching with transformers, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2021"
    locator: "Section 3.3, the match selection by a confidence threshold and the mutual nearest neighbor criterion"
  - paper: doi:10.1109/CVPR42600.2020.00499
    title: "Paul-Edouard Sarlin, Daniel DeTone, Tomasz Malisiewicz and Andrew Rabinovich, SuperGlue, learning feature matching with graph neural networks, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2020"
    locator: the mutual nearest neighbor baselines of the experiments
---

Mutual nearest neighbor matching keeps a pair of features $(a_i, b_j)$ only when $b_j$ is the nearest neighbor of $a_i$ among the features of the second image and $a_i$ is the nearest neighbor of $b_j$ among the features of the first. One nearest neighbor search in each direction and a comparison give the result. Unlike plain nearest neighbor matching, the result is a partial matching: each feature is used at most once. The check has no parameter, so it needs no tuning, and it is often combined with the [ratio test](/lowe-ratio-test/) or a distance threshold.

## In plain words

Two people at a party each have to pick the one person they like most. If Ann picks Bob and Bob picks Ann, they are a pair. If Ann picks Bob but Bob picks Carol, nobody is paired with Ann. Feature matching works the same way. A point in the first image picks the most similar point in the second image, and that point picks back. Only the pairs that pick each other are kept. A point that is not in the other image at all still picks someone, but the one it picks usually prefers another point, so the false pick is dropped.

## When it applies

- You have two sets of features, descriptors or embeddings, with a distance or a similarity between any two, and you want a one-to-one correspondence.
- Many features have no true partner, and you want to drop most of them without a tuned threshold.
- You can afford a nearest neighbor search in both directions. With exact search the cost is $O(m n D)$ for $m$ and $n$ descriptors of length $D$; the two directions can share the distance matrix.
- The score can be a distance to minimize or a similarity to maximize, such as the confidence matrix of a learned matcher.

## The template

```pseudo id=main
MUTUAL-NN-MATCH(A, B)
L1  for each a_i of A: f(i) ← NEAREST(a_i, B)        ▷ hole: the distance and the search method
L2  for each b_j of B: g(j) ← NEAREST(b_j, A)
L3  for each i do
L4      if g(f(i)) = i then output (i, f(i))
```

The holes are the distance and the nearest neighbor search of lines L1 and L2. Ties must go to a fixed choice, such as the smaller index, so that $f$ and $g$ are functions. The code in `impl/python/mutual_nearest_neighbor_matching.py` uses exact search and Euclidean distance. The proof in `proofs/correctness.md` shows that the output is exactly the set of pairs whose distance is the first smallest of its row and of its column, that it is a partial matching, that swapping the two sets gives the same pairs, that the closest pair overall is always kept, so the output is never empty for non-empty sets, and that with distinct distances every mutual pair is also chosen by the greedy matching, which takes the pairs in increasing order of distance.

Example. On a line, let $A = \{0, 4, 5\}$ and $B = \{1, 4.5, 9\}$.

| feature | nearest in the other set | picked back? |
|---|---|---|
| $a_0 = 0$ | $b_0 = 1$ | $b_0$ picks $a_0$: yes |
| $a_1 = 4$ | $b_1 = 4.5$ | $b_1$ is at 0.5 from both $a_1$ and $a_2$; the tie goes to $a_1$: yes |
| $a_2 = 5$ | $b_1 = 4.5$ | $b_1$ picks $a_1$: no |
| $b_2 = 9$ | $a_2 = 5$ | $a_2$ picks $b_1$: no |

The result is $\{(a_0, b_0), (a_1, b_1)\}$. Plain nearest neighbor matching from $A$ would use $b_1$ twice. The point $b_2$ is far from everything and stays unmatched.

## Classic examples

- **Brute-force descriptor matching.** Many matching libraries offer a "cross-check" flag on brute-force matching that keeps only the mutual pairs; it is the parameter-free alternative to the [ratio test](/lowe-ratio-test/).
- **Stereo.** The [left-right consistency check](/left-right-consistency-check/) keeps a disparity only when matching from the right image back to the left returns the same pixel, the same idea on a dense grid.
- **Tracking.** The [forward-backward error](/forward-backward-error/) tracks a point forward and then back and keeps it when it returns near its start.
- **Learned matchers.** [LoFTR](/loftr/) keeps the mutual best pairs of its confidence matrix above a threshold, and [SuperGlue](/superglue/) keeps mutual best pairs of its assignment matrix.

## Variations

- **With the ratio test.** Apply the [ratio test](/lowe-ratio-test/) in one or both directions and then the mutual check, which removes both ambiguous and one-sided matches.
- **Mutual k nearest neighbors.** Keep a pair when each is among the $k$ nearest of the other. The result is no longer a matching.
- **Global assignment.** The [Hungarian algorithm](/hungarian-algorithm/) finds the one-to-one matching of minimum total distance. It always matches $\min(m, n)$ pairs, so it needs a cost for leaving a feature unmatched to reject outliers.
- **Greedy and stable matching.** Taking the closest free pair again and again gives a full matching that contains every mutual pair when the distances are distinct, and that is [stable](/stable-matching/) for the preferences "closer is better".

## Pitfalls

- **Ties.** Descriptors with equal distances, for example quantized or binary ones with [Hamming distance](/hamming-distance/), give ties. Without a fixed tie rule the result depends on the scan order, and a pair can be kept in one direction and not in the other.
- **Repeated structure.** If two features of $B$ are near copies, the one that is not chosen loses its true partner. The check keeps one of them, which may be the wrong one; it does not test for ambiguity as the ratio test does.
- **Approximate search.** With approximate nearest neighbors in either direction, a true mutual pair can be missed, and the result can differ when the sets are swapped.
- **Not a quality test.** A mutual pair can still be far apart, for example two outliers that are each the other's best. Add a distance threshold or a geometric check such as [RANSAC](/ransac/).

## References
