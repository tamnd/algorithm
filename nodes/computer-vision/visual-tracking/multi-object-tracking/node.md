---
tag: VG0R54
kind: problem
slug: multi-object-tracking
name: Multi-object tracking
aliases:
- MOT
- multi-target tracking
area: computer-vision/visual-tracking
level: core
summary: Find all objects in each frame of a video and keep a consistent identity for each one over time, through occlusions, entries and exits.
model: real-ram
complexity:
  vars: {n: the number of detections in all frames, L: the number of allowed links between detections}
  time: {worst: O(n² (n + L))}
prereqs: [object-detection, kalman-filter, assignment-problem]
see_also: [data-association, tracking-by-detection, visual-object-tracking, clear-mot-metrics, idf1-score, hota-metric, sort-tracker, network-flow-tracking]
sources:
  - paper: doi:10.1016/j.artint.2020.103448
    title: Wenhan Luo, Junliang Xing, Anton Milan, Xiaoqin Zhang, Wei Liu and Tae-Kyun Kim, Multiple object tracking, a literature review, Artificial Intelligence 293, 2021, article 103448
    locator: the whole paper (the formulation of the problem, online and batch methods, and the evaluation)
  - paper: doi:10.1155/2008/246309
    title: Keni Bernardin and Rainer Stiefelhagen, Evaluating multiple object tracking performance, the CLEAR MOT metrics, EURASIP Journal on Image and Video Processing 2008, article 246309
    locator: the whole paper (the matching of hypotheses to objects, MOTA and MOTP)
  - book: isbn:9780120797608
    title: Yaakov Bar-Shalom and Thomas E. Fortmann, Tracking and Data Association, Academic Press, 1988
    locator: the whole book (the tracking of several targets in clutter from radar and sonar measurements)
  - paper: doi:10.1109/MAES.2004.1263228
    title: Samuel S. Blackman, Multiple hypothesis tracking for multiple target tracking, IEEE Aerospace and Electronic Systems Magazine 19(1), 2004, 5 to 18
    locator: the whole paper (the parts of a multiple target tracker and the methods of association)
  - paper: doi:10.1109/CVPR.2008.4587584
    title: Li Zhang, Yuan Li and Ramakant Nevatia, Global data association for multi-object tracking using network flows, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008, 1 to 8
    locator: the whole paper (the association of all detections of a video as a min-cost flow)
---

Multi-object tracking, or MOT, is the problem of finding every object of some given classes, such as people or cars, in each frame of a video, and of giving each object one identity that stays the same for as long as it is in view. The output is a set of tracks, each a sequence of boxes or points with one identity. Objects enter and leave, hide behind each other, and look alike, and the detector that finds them misses some and reports some that are not there. The same problem was studied for radar and sonar as multi-target tracking, with points in place of boxes. It differs from [visual object tracking](/visual-object-tracking/), which follows one target given by a box in the first frame and knows nothing of its class. Inside MOT, [data association](/data-association/) is the subproblem of deciding which measurement belongs to which track. [Tracking by detection](/tracking-by-detection/) is the most common way to solve MOT, by running a detector and then solving data association. [SORT](/sort-tracker/), [DeepSORT](/deep-sort/) and [ByteTrack](/bytetrack/) are particular online trackers of that kind, so they are solutions of this problem, not the problem itself.

## In plain words

You watch a video of a busy street and must put a numbered tag on every person in every picture. The same person must keep the same number from the moment they walk in until they leave. People walk behind each other, wear similar coats and sometimes are not seen at all for a moment. A good answer finds everybody, adds nobody who is not there, and never lets two people swap their numbers. Doing all three at once is hard, because the rules pull against each other: being careful about swaps can make you drop people, and finding everyone can make you invent people.

## Definition

The input is a sequence of frames $F_1, \ldots, F_T$ and a set of object classes. The true scene has a set of objects, and object $o$ is visible in a set of frames, where it has a box $g_{o,t}$. The output is a set of tracks. A track $h$ has an identity and a box $b_{h,t}$ for each frame $t$ in a set of frames. An *online* tracker must output the boxes of frame $t$ using only $F_1, \ldots, F_t$. A *batch* (offline) tracker may use the whole video.

**Quality.** In each frame, the output boxes are matched one to one to the true boxes, and a pair counts only if its [intersection over union](/intersection-over-union/) is at least a threshold, often 0.5. Three kinds of error follow: a *miss* or false negative (FN), a true box with no match; a *false positive* (FP), an output box with no match; and an *identity switch* (IDSW), a true object whose matched track changes from one frame to a later one. The [CLEAR MOT metrics](/clear-mot-metrics/) sum them over all frames:

$$\mathrm{MOTA} = 1 - \frac{\sum_t (\mathrm{FN}_t + \mathrm{FP}_t + \mathrm{IDSW}_t)}{\sum_t \mathrm{GT}_t},$$

with $\mathrm{GT}_t$ the number of true boxes in frame $t$. MOTA can be negative. [IDF1](/idf1-score/) instead matches whole tracks to whole objects once for the video and counts the frames where the identity is right, and [HOTA](/hota-metric/) weighs detection and association equally. No single score ranks trackers the same way as the others.

**The linking model.** Many methods reduce MOT to a combinatorial problem on detections. A detector gives $n$ detections, each in one frame. A set of allowed links $(i, j)$ joins detection $i$ to a detection $j$ of a later frame. A track is a chain of detections joined by allowed links. Each detection, link, track start and track end has a cost, and the task is a set of chains with no detection in common, of least total cost. Detections in no chain are taken as false.

## Variants

- **Online and batch.** Online trackers serve live cameras and robots. Batch trackers can use future frames to fix past decisions and usually score better.
- **Known or unknown number of objects.** Radar trackers such as [JPDA](/joint-probabilistic-data-association/) often assume the targets are known, and video trackers must start and end tracks.
- **Points, boxes, masks and 3D.** Radar gives points, video gives boxes, segmentation trackers give masks, and driving data gives 3D boxes from lidar.
- **Several cameras.** The same object must keep its identity across views, which needs appearance matching between cameras.
- **Random finite sets.** The state is a set of unknown size, and the [PHD filter](/phd-filter/) estimates its density without tracks.
- **Cells, animals and particles.** Objects can divide or merge, so the tracks form trees, not chains.

## Examples

**Counting errors.** Two people are in view in three frames, so $\sum_t \mathrm{GT}_t = 6$. The tracker finds both in frame 1, with identities $a$ and $b$. In frame 2 it misses the second person and reports one box on empty road. In frame 3 it finds both people but with the identities exchanged. Then $\mathrm{FN} = 1$, $\mathrm{FP} = 1$ and $\mathrm{IDSW} = 2$, because each person's track changes in frame 3. So $\mathrm{MOTA} = 1 - 4/6 = 1/3$, although every box but one was on a person.

**Two frames as an assignment.** Tracks $A$ and $B$ predict positions 0 and 10, and the detector reports 1 and 9. With costs equal to the distance, the assignment $A \to 1$, $B \to 9$ costs 2, and the other costs 18. With only two frames, the linking model is the [assignment problem](/assignment-problem/), solved by the [Hungarian algorithm](/hungarian-algorithm/).

**Crossing.** Two people of the same look walk toward each other, meet behind a pole and walk on. The frames are the same whether they crossed or turned back, so any tracker gives one person the wrong identity in one of the two cases. A motion model that expects constant velocity bets on the crossing, which is usually right.

## Known algorithms

| Algorithm | Mode | Association | Cost |
|---|---|---|---|
| [Global nearest neighbor](/global-nearest-neighbor-association/) | online | one best assignment per frame | $O((n_f + m_f)^3)$ per frame |
| [JPDA](/joint-probabilistic-data-association/) | online | soft weights over all joint events | exponential in the size of a cluster |
| [Multiple hypothesis tracking](/multiple-hypothesis-tracking/) | online with delay | the best hypotheses over several frames | grows with the number of hypotheses kept |
| [Network flow tracking](/network-flow-tracking/) | batch | min-cost flow over all frames | $O(K n (n + L))$ for $K$ tracks |
| [PHD filter](/phd-filter/) | online | none, a density of targets | polynomial in the measurements |
| [SORT](/sort-tracker/) | online | Hungarian algorithm on IoU | one assignment per frame |
| [DeepSORT](/deep-sort/) | online | motion gate and appearance, in a cascade | one assignment per age of track |
| [ByteTrack](/bytetrack/) | online | high-score detections first, then low-score | two assignments per frame |

Here $n_f$ and $m_f$ are the tracks and measurements of one frame. The last three rely on a strong detector and use simple rules, a heuristic, to start and end tracks.

## Bounds

- **Pairwise costs are easy.** In the linking model, when the cost of a track is a sum over single detections and consecutive pairs, the problem is a [min-cost flow problem](/min-cost-flow-problem/) on a graph with $2n + 2$ nodes and $3n + L$ edges. Successive shortest paths with Bellman-Ford solve it in $O(n^2 (n + L))$ time, since there are at most $n$ tracks. This is the bound in the front matter.
- **Two frames.** The linking model on two frames is the assignment problem, solvable in $O(k^3)$ time for $k$ detections per frame.
- **Costs on three frames are hard.** If the cost of a track depends on triples of detections, or if the association of three or more frames is posed as a multidimensional assignment, the problem is NP-hard by a reduction from three-dimensional matching. The proof is on the [MHT](/multiple-hypothesis-tracking/) page.
- **Soft association is hard to compute.** The marginal probabilities that JPDA needs include the permanent of a matrix as a special case, which is #P-hard.
- **No tracker is always right.** Two scenes with the same frames and different identities, as in the crossing example, get the same output, so one of them is scored with an identity switch.

## Reductions

- **To data association.** Each frame of an online tracker is an instance of [data association](/data-association/), with the tracks predicted by a [Kalman filter](/kalman-filter/).
- **To min-cost flow.** The batch linking model with pairwise costs is a min-cost flow, as above.
- **To assignment.** One frame with one hypothesis is an assignment problem.
- **To filtering.** With a model of births, deaths, detection and clutter, MOT is Bayesian filtering of a random finite set, approximated by the PHD filter.
- **From visual object tracking.** Running one single-object tracker per object solves MOT when the objects never meet, but fails at occlusions, which is why MOT methods share information between tracks.

## Applications

- Counting and following people in surveillance, retail and sports video.
- Tracking vehicles, cyclists and pedestrians around a self-driving car.
- Air traffic control and military surveillance with radar and sonar.
- Measuring the motion and division of cells in microscopy.
- Studying the behavior of animals in groups.
- Analysis of sports, where each player and the ball keep their identities.

## References
