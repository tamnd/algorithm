---
tag: 1GT795
kind: technique
slug: keyframe-selection
name: Keyframe selection
aliases:
- keyframes
area: computer-vision/structure-from-motion
level: core
summary: Keep only some frames, chosen when the view has changed enough, as the frames that carry the map and take part in optimization.
prereqs: [visual-odometry]
see_also: [sliding-window-bundle-adjustment, direct-sparse-odometry, semi-direct-visual-odometry, nister-visual-odometry, orb-slam, bundle-adjustment, scale-drift, loop-closure-detection]
sources:
  - paper: doi:10.1109/ISMAR.2007.4538852
    title: "Georg Klein and David Murray, Parallel tracking and mapping for small AR workspaces, IEEE and ACM International Symposium on Mixed and Augmented Reality (ISMAR), 2007"
    locator: "the map made of keyframes, the rules for adding a keyframe, and the bundle adjustment over keyframes in a separate thread"
  - paper: doi:10.1109/TPAMI.2017.2658577
    title: "Jakob Engel, Vladlen Koltun and Daniel Cremers, Direct sparse odometry, IEEE Transactions on Pattern Analysis and Machine Intelligence 40(3), 2018, 611-625"
    locator: "Section 3 (keyframe creation from the optical flow, the flow without rotation and the change of exposure; keyframe marginalization by visibility and distance)"
  - paper: doi:10.1109/ICRA.2014.6906584
    title: "Christian Forster, Matia Pizzoli and Davide Scaramuzza, SVO: Fast semi-direct monocular visual odometry, IEEE International Conference on Robotics and Automation (ICRA), 2014, 15-22"
    locator: "the keyframe rule (distance to all keyframes above 12 percent of the mean scene depth) and the removal of the farthest keyframe"
  - paper: doi:10.1109/TRO.2015.2463671
    title: "Raul Mur-Artal, J. M. M. Montiel and Juan D. Tardos, ORB-SLAM: a versatile and accurate monocular SLAM system, IEEE Transactions on Robotics 31(5), 2015, 1147-1163"
    locator: "the generous keyframe insertion in tracking and the culling of redundant keyframes in local mapping"
---

## In plain words

A camera takes 30 or more pictures a second, and most of them look almost the same as the one before. Saving all of them and optimizing all of them would be slow, and it would add little. So a system keeps only some pictures, the keyframes. A new picture becomes a keyframe when it shows enough that is new: the camera has moved far enough, the view has turned, the light has changed, or many tracked points have been lost. The map is built from the keyframes, and the costly optimization works only on them. Old keyframes that add little are removed.

## When it applies

- A sequence of frames comes from a camera at a high rate, and neighboring frames overlap a lot.
- The system keeps a map of points or depths that must be triangulated, which needs some distance (baseline) between the views.
- An optimization such as [bundle adjustment](/bundle-adjustment/) or [sliding window bundle adjustment](/sliding-window-bundle-adjustment/) must run on a bounded set of frames.
- The rules are heuristics. No rule is proved to be best, and their thresholds are tuned for a camera, a scene and a speed.

## The template

```pseudo id=main
KEYFRAME-STEP(new frame F with its pose, keyframes 𝒦, map)
L1  m ← change measures of F against 𝒦                 ▷ hole: distance, flow, overlap, exposure, time
L2  if F is tracked well and m passes the threshold then  ▷ hole: the combination and the thresholds
L3      add F to 𝒦 and start new points or depths in F
L4      while 𝒦 is too large or holds a redundant keyframe do
L5          remove one keyframe by the removal rule       ▷ hole: farthest, least visible, most redundant
L6  return 𝒦
```

The holes are the measures of line L1, the decision of line L2 and the removal rule of line L5. A good measure grows with what a new keyframe would add. Translation adds new depth information, because it gives a baseline for triangulation; rotation adds new parts of the scene but no baseline. Most rules compare the translation with the scene depth, because the parallax of a point at depth $z$ after a sideways move $b$ is about $f b / z$ pixels for a focal length $f$.

**Example.** A camera moves sideways at $0.1$ units per frame in a scene with mean depth $5$, with the rule of SVO: a new keyframe when the distance to every keyframe exceeds $0.12 \cdot 5 = 0.6$. Starting at keyframe 0, after 6 frames the distance is $0.6$, not more than $0.6$, so frame 7 is the first keyframe after frame 0, and then every 7th frame. With $f = 400$ pixels, the parallax between two keyframes is about $400 \cdot 0.7 / 5 = 56$ pixels for a point at the mean depth.

## Classic examples

- **PTAM (Klein and Murray, 2007).** The map is a set of keyframes, and a separate thread runs bundle adjustment on them. A frame is added when the tracking is good, some time has passed since the last keyframe, and the camera is far enough from the nearest keyframe compared with the scene depth.
- **Direct sparse odometry.** A new frame is a keyframe when $w_f f + w_{ft} f_t + w_a a > 1$, where $f$ is the root mean square optical flow of the points, $f_t$ the same flow without the rotation, and $a$ the change of the affine brightness. The window holds 7 keyframes. The two newest stay; a keyframe with less than 5 percent of its points visible in the newest frame leaves first; otherwise a distance score keeps the keyframes spread out in space. See [direct sparse odometry](/direct-sparse-odometry/).
- **Semi-direct visual odometry.** A new keyframe when the distance to all keyframes exceeds 12 percent of the mean scene depth, and the keyframe farthest from the new one is removed when there are too many. See [semi-direct visual odometry](/semi-direct-visual-odometry/).
- **ORB-SLAM.** It adds keyframes generously, as soon as the tracking shows that the view has changed enough (fewer tracked points than in the reference keyframe) and the local mapping can take one, and later removes keyframes whose points are seen by enough other keyframes. Many keyframes help tracking in hard motion, and the culling keeps the map small. See [ORB-SLAM](/orb-slam/).
- **Frame skipping in visual odometry.** [Nister visual odometry](/nister-visual-odometry/) and other feature-based systems compute the relative pose only between frames far enough apart, because the relative pose is poorly conditioned for a short baseline.

## Variations

- **Measures.** Distance compared with depth, optical flow in pixels, flow without rotation, the fraction of shared points (overlap), the number of tracked points, the change of exposure, the time since the last keyframe, or the uncertainty of the pose.
- **Removal.** Keep the newest, remove the farthest, remove the one with the fewest visible points, remove the one whose points are seen by enough other keyframes, or remove by marginalization into a prior, which keeps its information (see [sliding window bundle adjustment](/sliding-window-bundle-adjustment/)).
- **Information-based rules.** Some systems choose keyframes by the expected gain of information or the entropy of the pose. These rules are better founded but cost more to evaluate, and they are still approximations.
- **For loop closure.** The keyframes are also the places that [loop closure detection](/loop-closure-detection/) compares with the current view, so their spacing sets how densely the path is covered.

## Pitfalls

- **Pure rotation.** A rule based only on distance never fires when the camera only turns, and new parts of the scene get no points. A rule based only on flow fires, but the new keyframe has no baseline, so its points cannot be triangulated. Rules that combine both, like the one of DSO, handle both cases better.
- **Thresholds compared with depth.** A threshold in meters works only at one scene depth, and with one camera the scale is unknown anyway. Compare the distance with the mean or median depth.
- **Too few keyframes.** If the view changes a lot between keyframes, tracking against the newest keyframe fails, and the triangulation angle of new points grows too large for patch matching.
- **Too many keyframes.** Optimization cost grows, and a window of keyframes that are close together has short baselines, which gives poor depths and more [scale drift](/scale-drift/).
- **Bad frames.** A frame with motion blur or a tracking failure must not become a keyframe, because every later point that it hosts inherits its errors.

## Exercises

1. A camera moves forward along its optical axis at $0.05$ units per frame toward a wall at depth $4$. With the SVO rule ($0.12$ times the mean depth), how many frames pass before the first new keyframe? Remember that the mean depth falls as the camera approaches. (Answer: after $k$ frames the distance is $0.05 k$ and the depth is $4 - 0.05 k$; $0.05 k > 0.12 (4 - 0.05 k) = 0.48 - 0.006 k$ gives $k > 8.57$, so frame 9.)
2. In a rule of the DSO form with the weights $w_f = 1$, $w_{ft} = 2$, $w_a = 0$ and a threshold of $15$ (example values, not those of the paper), a frame moves sideways so that every point moves $4$ pixels. Is it a keyframe? What if the same $4$ pixels of flow come from a pure rotation? (Answer: $4 + 8 = 12$, no; with rotation $f_t = 0$, so $4$, no. A translation is closer to making a keyframe.)
3. Explain why removing the oldest keyframe, instead of the farthest one, can make the window collapse to a short segment of the path when the camera stops moving.

## References
