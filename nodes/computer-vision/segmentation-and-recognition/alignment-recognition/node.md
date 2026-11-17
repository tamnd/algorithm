---
tag: VCMMH6
kind: technique
slug: alignment-recognition
name: Recognition by alignment
aliases:
- hypothesize and verify
- Huttenlocher-Ullman alignment
area: computer-vision/segmentation-and-recognition
level: advanced
summary: "Hypothesize a model pose from a minimal set of model to image matches and verify it by projecting the whole model and counting supporting features."
prereqs: [object-recognition, affine-camera-model, minimal-solver]
see_also: [geometric-hashing, generalized-hough-transform, ransac, perspective-n-point, p3p, spatial-verification, template-matching, chamfer-distance]
sources:
  - paper: doi:10.1007/BF00054921
    title: "Daniel P. Huttenlocher and Shimon Ullman, Recognizing solid objects by alignment with an image, International Journal of Computer Vision 5(2), 1990, 195-212"
    locator: "The alignment method: three model points and three image points fix a weak perspective transformation up to a reflection, each such triple gives a pose, and each pose is verified by transforming the whole model and comparing it with the image"
  - paper: doi:10.1016/0004-3702(87)90070-1
    title: "David G. Lowe, Three-dimensional object recognition from single two-dimensional images, Artificial Intelligence 31(3), 1987, 355-395"
    locator: "The SCERPO system: perceptual grouping to choose a few matches, the pose from them, and the verification by projecting the model and matching more features"
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: "Random minimal samples to hypothesize a model and the count of the consensus set to verify it, applied to the location determination problem"
  - paper: doi:10.1023/B:VISI.0000029664.99615.94
    title: "David G. Lowe, Distinctive image features from scale-invariant keypoints, International Journal of Computer Vision 60(2), 2004, 91-110"
    locator: "Section 7, object recognition: clusters of SIFT matches that agree on a pose, the affine fit and the verification of each cluster"
---

Recognition by alignment finds a known object in an image and its pose. Choose a minimal set of matches between features of the model and features of the image, just enough to fix the pose. Compute the pose that brings these model features onto the image features. Then project the whole model with this pose and count how many of its other features land on image features of the same kind. A correct pose explains many features, a wrong one explains few. Huttenlocher and Ullman (1990) used three points and a weak perspective camera, and showed that three points fix the pose up to a reflection. The method turns recognition, a search over all matchings, into a search over minimal sets. [RANSAC](/ransac/) uses the same two steps with random samples.

## In plain words

You know what a chair looks like, and you want to find it in a photo. Pick two or three points of the chair and guess which points of the photo they are. The guess tells you where the chair would be, how it is turned and how big it is. Now draw the whole chair there, in thin lines, on the photo. If the lines fall on edges of the photo almost everywhere, the guess was right. If they fall on nothing, try another guess.

Most guesses are wrong, but each one is fast to test, and one good guess is enough.

## When it applies

- The object is rigid, or made of rigid parts, and you have a model: 3D points, 2D points, line segments or local features with positions.
- A camera model with few parameters relates the model to the image: a similarity or an affine map in the plane, a [weak perspective](/affine-camera-model/) camera, or a full perspective camera.
- A [minimal solver](/minimal-solver/) gives the pose from $k$ matches: $k = 2$ points for a similarity in the plane, $k = 3$ for an affine map or for weak perspective, and $k = 3$ for a calibrated perspective camera with [P3P](/p3p/), which has up to four solutions.
- The image has few enough features, or the features carry enough labels, that the number of minimal sets to try is affordable.

## The template

```pseudo id=main
ALIGN(model features M, image features F, k, t_min)
L1  for each set S of k model features do
L2      for each ordered set S' of k image features of compatible kinds do
L3          for each pose T that the minimal solver finds from S to S' do
L4              project every feature of M by T
L5              s ← the number of projected features with a compatible image feature near them
L6              if s ≥ t_min then report T with support s
L7  refine each reported pose on its supporting matches and keep the best ones
L8  return the poses
```

Lines L1 to L3 make the pose hypotheses, and lines L4 to L6 test them. With $m$ model features and $n$ image features, the loops make at most $\binom{m}{k} \cdot n (n-1) \cdots (n-k+1)$ hypotheses, times the number of solutions of the solver. That is a counting fact. For $k = 3$, it is $O(m^3 n^3)$. If each test costs $O(m)$ with a grid or a [k-d tree](/kd-tree/) on the image features, the whole search costs $O(m^4 n^3)$. RANSAC replaces the full loops by random samples and stops when the [iteration bound](/ransac-iteration-bound/) is met.

**Example.** A planar model has the four corners of the unit square, $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$, and a fifth point $(0.5, 2)$ that breaks the symmetry. The image contains the model turned by 90 degrees, scaled by 2 and moved by $(10, 10)$, so $p \mapsto 2 (-p_v, p_u) + (10, 10)$, which gives $(10, 10)$, $(10, 12)$, $(8, 12)$, $(8, 10)$ and $(6, 11)$. The image also has one clutter point $(3, 3)$. A similarity has 4 degrees of freedom, so $k = 2$. The hypothesis $(0, 0) \to (10, 10)$, $(1, 0) \to (10, 12)$ maps the model difference $(1, 0)$ to $(0, 2)$: scale 2, angle 90 degrees, translation $(10, 10)$. It sends all five model points exactly onto image points, so its support is 5. The hypothesis $(0, 0) \to (10, 10)$, $(1, 0) \to (8, 12)$ has scale $2\sqrt 2$ and angle 135 degrees. It sends $(1, 1)$ to $(6, 10)$ and $(0, 1)$ to $(8, 8)$, which are not image points, and its support is 2, the two points it was built from. With 10 model pairs and 30 ordered image pairs, the search tries 300 hypotheses.

## Classic examples

- **Huttenlocher and Ullman (1990).** Three model points and three image points fix a weak perspective pose (rotation, scale and translation) up to a reflection. Each pose is tested by transforming the whole model, and edge contours confirm or reject it. They used a small number of distinctive points of the edge contours as features, which keeps $n$ small.
- **SCERPO** (Lowe 1987). Perceptual grouping of line segments (parallel lines, lines that meet at their ends) chooses a few likely matches. The pose under full perspective comes from Newton iterations, and new matches found with the projected model refine it.
- **RANSAC** (Fischler and Bolles 1981). The same two steps with random minimal samples, applied to the location determination problem, which is camera pose from known 3D points ([perspective-n-point](/perspective-n-point/)).
- **SIFT object recognition** (Lowe 2004). One SIFT match already gives a similarity. Matches are clustered by pose, and each cluster is tested by an affine fit. This is alignment with $k = 1$ and a [Hough](/generalized-hough-transform/) step to group the hypotheses.
- **Spatial verification in retrieval.** [Spatial verification](/spatial-verification/) applies alignment to each of the top images of a search, with one hypothesis per match of two affine regions.

## Variations

- **Indexing instead of search.** [Geometric hashing](/geometric-hashing/) stores, offline, the invariant coordinates of all model features in every basis of $k$ model features. At run time one image basis looks up all the matching model bases at once, which removes the loop over model sets.
- **Pose clustering.** Each minimal match votes for its pose, and peaks of the vote space are the hypotheses, as in the [generalized Hough transform](/generalized-hough-transform/).
- **Interpretation tree search.** Extend a partial matching one feature at a time and prune it with pairwise constraints (distances, angles) before any pose is computed.
- **Edge-based testing.** Test a pose by the distance from the projected model edges to the image edges, with a [distance transform](/distance-transform/) as in [chamfer matching](/chamfer-distance/), instead of counting points.

## Pitfalls

- **Combinatorial cost.** The number of hypotheses grows as $m^k n^k$. Without labels on the features (type, scale, orientation, descriptor) to limit compatible matches, the method is slow for large $n$.
- **Unstable minimal sets.** Model points that are close together, or almost collinear, give poses with large errors far from them. A correct match can then fail the test. Prefer spread out minimal sets, and refine the pose before the final count.
- **Several solutions.** Weak perspective from three points has two solutions, related by a reflection, and P3P has up to four. Test all of them.
- **Support from clutter.** In a dense image, a wrong pose finds many image features near its projected features by chance. The threshold $t_{\min}$ must grow with the density of image features, or the test must use orientation and type as well as position.
- **Symmetric models.** A symmetric model has several correct poses with the same support. That is not an error, but the pose is not unique.

## Exercises

1. In the example, list the hypotheses that map the model pair $(0, 0), (1, 0)$ to an image pair and have support at least 3. Which property of the fifth model point makes the answer unique?
2. Show that $\binom{m}{k} \cdot n!/(n-k)!$ is the number of hypotheses of lines L1 and L2, and compute it for $m = 20$, $n = 200$ and $k = 3$.
3. With a fraction $w$ of the image features on the object, and $k = 3$, how many random samples does RANSAC need to find an all-correct sample with probability 0.99? Compare with the full search of exercise 2 for $w = 0.1$.
4. Explain why two points give a similarity in the plane but not an affine map, and why an affine map needs three points that are not on one line.

## References
