---
tag: GBD07V
kind: technique
slug: lowe-ratio-test
name: Lowe's ratio test
aliases:
- nearest neighbor distance ratio test
- NNDR test
area: computer-vision/local-features
level: core
summary: Keep a match only when the distance to the nearest descriptor is much smaller than the distance to the second nearest, which rejects ambiguous matches.
prereqs: [nearest-neighbor-search, feature-descriptor]
see_also: [feature-matching, mutual-nearest-neighbor-matching, sift, best-bin-first-search, randomized-kd-forest, rootsift, prosac, superglue]
sources:
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004"
    locator: "Section 7.1, keypoint matching: the ratio of the closest to the second-closest neighbor, the threshold 0.8 and its measured effect on correct and false matches"
  - paper: doi:10.1109/TPAMI.2005.188
    title: "Krystian Mikolajczyk and Cordelia Schmid, A performance evaluation of local descriptors, IEEE Transactions on Pattern Analysis and Machine Intelligence 27(10), 2005"
    locator: the comparison of matching strategies, a distance threshold, the nearest neighbor and the nearest neighbor distance ratio
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision: Algorithms and Applications, 2nd edition, Springer, 2022"
    locator: "Section 7.1.3, feature matching: matching strategies, the nearest neighbor distance ratio and efficient matching"
---

Lowe's ratio test is a filter for descriptor matches. For a descriptor of one image, find its nearest and its second nearest descriptor in the other image. If the nearest is much closer than the second, the match is distinctive and is kept; if the two are almost at the same distance, the match is ambiguous and is dropped. Lowe (2004) keeps a match when $d_1 < 0.8 \, d_2$. The value 0.8 is a tuned design choice, and his statement that it removes about 90 percent of the false matches and loses less than 5 percent of the correct ones is a measurement on his test data, not a theorem.

## In plain words

A descriptor is a list of numbers that describes a small patch of an image. To find the same patch in a second image, we look for the closest descriptor there. But the closest one is not always right. A brick wall or a row of windows has many patches that look alike, and a patch that is not in the second image at all still has some closest descriptor. The ratio test asks one more question: how close is the runner-up? If the best is clearly better than the runner-up, we trust it. If the two are nearly as good, we cannot tell them apart, so we throw the match away. A plain distance limit cannot do this, because some good matches are far and some bad matches are near.

## When it applies

- You match descriptors of two images, or of an image against a database, by [nearest neighbor search](/nearest-neighbor-search/) in a metric space.
- Many query descriptors have no true partner, because of occlusion, a small overlap or clutter, so a match must be judged by how distinct it is, not only by its distance.
- The distances of correct matches differ a lot from one feature to another, so one global distance threshold works poorly.
- A second neighbor is available at little extra cost: exact search, [best bin first search](/best-bin-first-search/) and the [randomized kd-forest](/randomized-kd-forest/) all return the $k$ nearest.

## The template

```pseudo id=main
RATIO-TEST-MATCH(A, B, r)                     ▷ |B| ≥ 2 and 0 < r ≤ 1
L1  for each descriptor a_i of A do
L2      (j, d_1, d_2) ← NEAREST-TWO(a_i, B)    ▷ hole: exact search, BBF or a kd-forest
L3      if d_1 < r · d_2 then
L4          output (i, j)
```

The holes are the search method in line L2, the distance and the ratio $r$. With exact search and Euclidean distance the code in `impl/python/lowe_ratio.py` follows these lines; `lowe_ratio_test.py` only re-exports it, because the tools read a file name that ends in `_test` as a test file. Line L3 compares squared distances with $r^2$, which gives the same answer without a square root. The proof in `proofs/correctness.md` shows that the scan of line L2 returns the true nearest two, that the kept set is the same after a common scaling, translation or rotation of all descriptors, that it grows with $r$, that a query with two nearest descriptors at the same distance is always rejected, and that two queries can keep the same partner.

Example. In the plane, let $B = \{(1, 0), (3, 0), (5, 4), (5, 6.2)\}$ and $r = 0.8$.

| query $a_i$ | nearest, $d_1$ | second, $d_2$ | $d_1 / d_2$ | kept with $r = 0.8$ |
|---|---|---|---|---|
| $(0, 0)$ | $(1, 0)$, 1 | $(3, 0)$, 3 | 0.333 | yes |
| $(5, 5)$ | $(5, 4)$, 1 | $(5, 6.2)$, 1.2 | 0.833 | no |
| $(2.1, 0)$ | $(3, 0)$, 0.9 | $(1, 0)$, 1.1 | 0.818 | no |

The second and third queries sit between two similar candidates, and the test drops them, even though their nearest distances, 1 and 0.9, are not larger than that of the first query. With $r = 0.85$ all three are kept.

Lowe's argument for the test is statistical. A correct match must be much closer than the nearest wrong descriptor, while for a wrong match many other wrong descriptors lie at a similar distance in the high-dimensional space. In Section 7.1 he plots the probability density of the ratio for correct and for false matches on his test images and picks 0.8 from these curves.

## Classic examples

- **SIFT matching.** [SIFT](/sift/) descriptors of 128 values are matched by the nearest neighbor with the ratio test, and the survivors go to a Hough transform and a pose check (Lowe 2004).
- **Approximate search.** [Best bin first search](/best-bin-first-search/) and the [randomized kd-forest](/randomized-kd-forest/) return the two nearest neighbors approximately. Lowe used BBF with a cutoff of 200 candidates for this step.
- **RootSIFT.** [RootSIFT](/rootsift/) changes the descriptor and keeps the ratio test as it is.
- **Panorama and reconstruction.** [Image stitching](/image-stitching/) and [structure from motion](/structure-from-motion-problem/) pipelines filter putative matches with the ratio test before [RANSAC](/ransac/), which then needs fewer samples because the outlier rate is lower.
- **Binary descriptors.** [ORB](/orb-features/) and [BRIEF](/brief-descriptor/) descriptors use the same test with [Hamming distance](/hamming-distance/), with a ratio tuned for that distance.

## Variations

- **Symmetric ratio test.** Run the test in both directions and keep the pairs that pass both ways, which also makes the result a matching; compare [mutual nearest neighbor matching](/mutual-nearest-neighbor-matching/).
- **Ratio as a score.** Instead of a hard cut, sort the matches by $d_1 / d_2$ and use the order, for example for the sampling order of [PROSAC](/prosac/).
- **A distance threshold.** Mikolajczyk and Schmid (2005) compare a plain threshold on $d_1$, the nearest neighbor and the ratio of nearest distances as matching strategies for many descriptors.
- **Learned matchers.** [SuperGlue](/superglue/) replaces the hand-made test with attention over both sets of points and a dustbin for points without a partner.

## Pitfalls

- **Repeated structure.** On facades, tiles or text, the true match has near copies, so $d_1 \approx d_2$ and the test drops correct matches. Use geometry or a learned matcher there.
- **Duplicate descriptors.** If $B$ holds the same descriptor twice, for example because the detector reports one point twice, every query that matches it is rejected. Remove duplicates, or take the second neighbor among descriptors at a different image position.
- **Matching an image against itself.** The nearest neighbor is the query itself at distance 0. Use the second and third neighbors instead of the first and second.
- **Squared distances.** A library that returns squared distances needs $r^2$, not $r$. With $r = 0.8$ on squared distances the test is the much looser $d_1 < 0.894 \, d_2$.
- **Approximate search.** An approximate second neighbor can be farther than the true one, which makes the ratio smaller and lets ambiguous matches pass.
- **Not a matching.** Several queries can keep the same partner. Add a mutual check if each feature may be used once.
- **The threshold.** 0.8 is tuned for SIFT on Lowe's data. Other descriptors and distances need their own value.

## References
