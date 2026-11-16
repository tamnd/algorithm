---
tag: RN7F3T
kind: technique
slug: tracking-by-detection
name: Tracking by detection
aliases:
- detect then track
area: computer-vision/visual-tracking
level: core
summary: Run an object detector on every frame and link the detections into tracks by data association, instead of tracking each target by its appearance alone.
prereqs: [object-detection, data-association, kalman-filter]
see_also: [multi-object-tracking, sort-tracker, deep-sort, bytetrack, network-flow-tracking, track-gating, hungarian-algorithm, visual-object-tracking]
sources:
  - paper: doi:10.1109/CVPR.2008.4587583
    title: Mykhaylo Andriluka, Stefan Roth and Bernt Schiele, People-tracking-by-detection and people-detection-by-tracking, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008, 1 to 8
    locator: the whole paper (people found by a detector in each frame and linked over time, with tracking that also improves the detections)
  - paper: doi:10.1109/TPAMI.2010.232
    title: Michael D. Breitenstein, Fabian Reichlin, Bastian Leibe, Esther Koller-Meier and Luc Van Gool, Online multiperson tracking-by-detection from a single, uncalibrated camera, IEEE Transactions on Pattern Analysis and Machine Intelligence 33(9), 2011, 1820 to 1833
    locator: the whole paper (online tracking of people from the output of a detector, including its confidence)
  - paper: doi:10.1109/CVPR.2008.4587584
    title: Li Zhang, Yuan Li and Ramakant Nevatia, Global data association for multi-object tracking using network flows, IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008, 1 to 8
    locator: the whole paper (the batch linking of all detections of a video by min-cost flow)
  - paper: doi:10.1109/ICIP.2016.7533003
    title: Alex Bewley, Zongyuan Ge, Lionel Ott, Fabio Ramos and Ben Upcroft, Simple online and realtime tracking, IEEE International Conference on Image Processing (ICIP), 2016, 3464 to 3468
    locator: the whole paper (a strong detector, a Kalman filter per box and the Hungarian algorithm on overlap)
  - paper: doi:10.1016/j.artint.2020.103448
    title: Wenhan Luo, Junliang Xing, Anton Milan, Xiaoqin Zhang, Wei Liu and Tae-Kyun Kim, Multiple object tracking, a literature review, Artificial Intelligence 293, 2021, article 103448
    locator: the whole paper (detection-based tracking as the main design of multiple object trackers)
---

Tracking by detection is the design of a tracker in two separate stages. First, an [object detector](/object-detection/) runs on each frame on its own and returns boxes with scores. Second, a [data association](/data-association/) step links the boxes of different frames into tracks, using a motion model, the appearance of the boxes, or both. The tracker never searches the image for a target itself. It trusts the detector to say where the objects are, and its own work is to decide which detection is which object. The design became the standard approach to [multi-object tracking](/multi-object-tracking/) in video once detectors of people and cars became reliable. It is a technique, not a problem: multi-object tracking is the problem it solves, data association is the subproblem it solves in every frame or over a window, and [SORT](/sort-tracker/), [DeepSORT](/deep-sort/) and [ByteTrack](/bytetrack/) are particular trackers built on it, which differ in the cost of a pair and in the order of the matching. The other main design follows each target by its own appearance model, as in [visual object tracking](/visual-object-tracking/), which needs no detector of the class but must be started by hand for each object.

## In plain words

Imagine one helper whose only job is to point at every person in each photo of a video, without caring who is who. A second helper takes these points and works out which point in this photo is the same person as which point in the last photo, using where each person was heading and what they wore. The first helper can be very good at finding people, because that is all it does. The second helper only has to solve a matching puzzle. If the first helper misses someone, the second must guess where that person went until they are pointed at again.

## When it applies

It applies when:

- **a good detector exists for the class of the objects.** People, faces, cars and cells have such detectors. The quality of the tracks is bounded by the quality of the detections;
- **the objects are many, or enter and leave.** The detector finds new objects in every frame, so starting a track needs no manual box;
- **the detector can run on every frame, or often enough.** Its cost usually dominates the cost of the association;
- **consecutive detections of one object are close in position, overlap or appearance,** so that a cost between them separates the right pairs from the wrong ones.

It works badly when the detector cannot see the objects, for example tiny or heavily hidden objects, or when the class has no detector.

## The template

```pseudo id=main
TRACK-BY-DETECTION(the frames F_1..F_T)
L1   tracks ← ∅
L2   for t = 1 .. T do
L3       D ← DETECT(F_t)                                 ▷ boxes with scores
L4       for each track: PREDICT its box in frame t      ▷ a Kalman filter, or the last box
L5       C ← COST(tracks, D)                             ▷ IoU, Mahalanobis distance, appearance, with a gate
L6       M ← ASSOCIATE(C)                                ▷ Hungarian, greedy, cascade, or two rounds by score
L7       update each matched track with its detection
L8       MANAGE: start tracks from unmatched detections, end tracks missed too long
L9   return the tracks
```

The holes are DETECT, PREDICT, COST, ASSOCIATE and MANAGE. A batch tracker replaces lines L4 to L8 by one global association over all frames, as in [network flow tracking](/network-flow-tracking/). The rules of MANAGE, such as confirming a track after three hits in a row and deleting it after thirty misses, are a heuristic. They are tuned, not derived from a model.

## Classic examples

- **[SORT](/sort-tracker/).** PREDICT is a constant velocity [Kalman filter](/kalman-filter/) on the box, COST is one minus the IoU, and ASSOCIATE is the [Hungarian algorithm](/hungarian-algorithm/) with an overlap threshold.
- **[DeepSORT](/deep-sort/).** COST adds a learned appearance distance, gated by the motion model at 9.4877, and ASSOCIATE matches tracks in order of the time since their last match.
- **[ByteTrack](/bytetrack/).** ASSOCIATE first matches the high-score detections, then matches the tracks still unmatched to the low-score detections that other trackers throw away.
- **[Network flow tracking](/network-flow-tracking/).** A batch version: all detections of a video are linked at once by a min-cost flow.
- **[Multiple hypothesis tracking](/multiple-hypothesis-tracking/).** ASSOCIATE keeps several hypotheses and decides a few frames later.
- **[Global nearest neighbor](/global-nearest-neighbor-association/).** The radar form of the same loop, with point measurements in place of boxes.

## Variations

- **Online and batch.** Online trackers decide in each frame. Batch and sliding window trackers use later frames and fix earlier mistakes.
- **Motion only and motion with appearance.** Appearance features keep identities through long gaps and crowds, at the cost of a second network.
- **Detection by tracking.** The tracks feed back into the detector, raising the score of a weak detection where a track predicts an object, as in the work of Andriluka, Roth and Schiele (2008).
- **Using low scores.** Detections below the usual threshold are kept for a second round of matching, as in ByteTrack.
- **Joint detection and tracking.** One network outputs the boxes and the motion or identity of each box, which merges DETECT and COST.
- **Detector confidence as a cue.** Breitenstein and others (2011) used the continuous confidence of the detector, not only its final boxes, to guide the tracks.

## Pitfalls

- **Missed detections break tracks.** A person hidden for some frames gets no detection. If MANAGE ends tracks too soon, the person comes back with a new identity.
- **False detections start false tracks.** Requiring a few hits before a track is confirmed reduces them, at the cost of a delay.
- **Non-maximum suppression in crowds.** [Box non-maximum suppression](/box-non-maximum-suppression/) can remove the box of a person who stands behind another, so the tracker never sees that person.
- **Camera motion.** A constant velocity model in image coordinates fails when the camera pans. Compensate the motion of the camera first.
- **Low frame rate.** Boxes of one object no longer overlap between frames, so IoU costs fail and motion or appearance must carry the matching.
- **Tuning to one benchmark.** Thresholds for scores, gates and track ages tuned on one dataset often do not transfer.

## Exercises

1. In the template, let PREDICT keep the last box and COST be one minus the IoU. Give a sequence of frames in which two people cross and the tracker exchanges their identities, and show how a constant velocity Kalman filter prevents it.
2. A detector misses each person independently with probability 0.1 per frame. If MANAGE deletes a track after 3 misses in a row, what is the probability that a track survives 100 frames of a person who is always visible?
3. Explain why ByteTrack's second round can recover a person hidden behind another, and why it does not start new tracks from the low-score detections.
4. Write the batch version of the template as a min-cost flow and say which of the holes become edge costs.
5. Compare the cost of DETECT and of ASSOCIATE for 20 people per frame with a detector that takes 30 milliseconds per frame.

## References
