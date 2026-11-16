---
tag: MRQ8VT
kind: definition
slug: feature-track
name: Feature track
aliases:
- point track
- multiview correspondence
area: computer-vision/structure-from-motion
level: core
summary: The set of image features in several views that show one scene point, built by joining pairwise matches, often with union-find.
prereqs: [feature-matching, union-find-connectivity]
see_also: [view-graph, structure-from-motion-problem, incremental-structure-from-motion, global-structure-from-motion, point-triangulation, kanade-lucas-tomasi-tracker, connected-components, disjoint-set-forest]
sources:
  - paper: doi:10.1145/1141911.1141964
    title: "Noah Snavely, Steven M. Seitz and Richard Szeliski, Photo tourism: exploring photo collections in 3D, ACM Transactions on Graphics 25(3), 2006, 835-846"
    locator: "the section on finding correspondences (pairwise matches joined into tracks, and the rule that drops a track with two features in one image)"
  - paper: doi:10.1109/CVPR.2016.445
    title: "Johannes L. Schönberger and Jan-Michael Frahm, Structure-from-motion revisited, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2016), 4104-4113"
    locator: "the correspondence search and the scene graph (tracks as the multiview correspondences of the incremental pipeline)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Chapter 11, Structure from motion and SLAM (feature tracks and their use in multi-frame structure from motion)"
---

A feature track is the set of image features, at most one in each image, that show the same scene point. It is the unit of data of [structure from motion](/structure-from-motion-problem/): one track becomes one 3D point, and each feature in it becomes one observation of that point. Matching gives only pairs of features, one pair for each image pair, so the tracks are built by joining the pairs: two pairs that share a feature belong to the same track. In graph terms, a track is a [connected component](/connected-components/) of the match graph, and [union-find](/union-find-connectivity/) computes all components in near-linear time. A component that holds two features of the same image cannot be one scene point, so it is marked inconsistent and is split or dropped. In a video, a tracker such as the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/) follows each feature from frame to frame, and the tracks come directly from the tracker.

## Definition

### Features, matches and tracks

A **feature** is a pair $(i, k)$: the keypoint with index $k$ in image $i$, with its pixel position $x_{ik}$. A **match** is a pair of features $\{(i, k), (i', k')\}$ with $i \ne i'$ that the [feature matching](/feature-matching/) step, usually followed by a geometric check, accepts as images of one scene point.

The **match graph** has the matched features as vertices and the matches as edges. A **track** is the vertex set $T$ of one connected component of the match graph. The **length** of the track is $|T| \ge 2$. A track is **consistent** if no image occurs twice in it, that is, if the map $(i, k) \mapsto i$ is one to one on $T$. Only consistent tracks are passed to reconstruction, where a consistent track $T$ gives the unknown point $X_T$ and one observation $x_{ik}$ for each $(i, k) \in T$.

```pseudo id=main
BUILD-TRACKS(matches)
L1  for each match (a, b) in matches
L2      MAKE-SET(a) and MAKE-SET(b), if they are new
L3      UNION(a, b)
L4  for each feature f in the forest
L5      add f to the group of FIND(f)
L6  for each group T
L7      consistent(T) <- (no two features of T have the same image)
L8  return all groups T, each with its flag consistent(T)
```

Lines L1 to L3 run union-find with union by size and path halving over the matches, and lines L4 and L5 collect the components. Line L7 is the consistency test. The caller keeps the consistent tracks and drops or splits the others.

## Examples and non-examples

- **A chain.** The matches $(A, 0)$ to $(B, 3)$ and $(B, 3)$ to $(C, 1)$ give the track $\{(A, 0), (B, 3), (C, 1)\}$ of length 3, which is consistent. The pair $(A, 0)$ and $(C, 1)$ was never matched directly, but it is still in the track; this is how tracks become longer than the pairs that make them.
- **A non-example: an inconsistent component.** Add the matches $(A, 5)$ to $(C, 2)$, $(C, 2)$ to $(D, 0)$ and $(D, 0)$ to $(A, 7)$. Their component is $\{(A, 5), (A, 7), (C, 2), (D, 0)\}$. Two features of image $A$ are in it, so it is not a track of one point: one of the matches is wrong, or two features of image $A$ sit on the same scene point. The reference code returns exactly these two groups, the first marked consistent and the second not.
- **A video track.** In a video, a keypoint followed by a tracker through frames $0$ to $9$ gives one track of length 10 with one feature in each frame. It is consistent by construction.
- **A non-example: an unmatched feature.** A keypoint that is in no match is not in the match graph, so it is in no track. A track needs at least two views, because one view does not fix the depth of a point.
- **A non-example: a match that is not a track.** A pair that the geometric check rejected is not an edge, so it joins nothing, even if the descriptors are close.

## Related definitions

- **Match graph and view graph.** The match graph has features as vertices. The [view graph](/view-graph/) has images as vertices and an edge for each image pair with enough verified matches; it is the match graph seen at the level of images.
- **Connected components and union-find.** A track is a [connected component](/connected-components/); the [disjoint-set forest](/disjoint-set-forest/) builds all of them with $m$ unions in $O(m\,\alpha(m))$ time for $m$ matches.
- **Observation.** One feature of a consistent track is one observation of its 3D point, which enters the [reprojection error](/reprojection-error/) and [bundle adjustment](/bundle-adjustment/).
- **Measurement matrix.** When every track has a feature in every image, the tracks fill the measurement matrix of the [Tomasi-Kanade](/tomasi-kanade-factorization/) and [Sturm-Triggs](/sturm-triggs-factorization/) factorization methods.
- **Triangulation.** The 3D point of a track is found by [point triangulation](/point-triangulation/) from its features and the camera poses.

## References
