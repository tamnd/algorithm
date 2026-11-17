---
tag: JC1H8Q
kind: problem
slug: instance-segmentation
name: Instance segmentation
aliases:
- object instance segmentation
area: computer-vision/segmentation-and-recognition
level: core
summary: Detect each object of the known classes in an image and give the exact set of its pixels, keeping objects of the same class apart.
prereqs: [object-detection, semantic-segmentation]
see_also: [mask-r-cnn, panoptic-segmentation, detection-mean-average-precision, intersection-over-union, roi-pooling, watershed-segmentation, grabcut, detr]
sources:
  - paper: doi:10.1109/ICCV.2017.322
    title: "Kaiming He, Georgia Gkioxari, Piotr Dollar and Ross Girshick, Mask R-CNN, IEEE International Conference on Computer Vision (ICCV), 2017 (arXiv 1703.06870)"
    locator: "Section 1 and Section 2 (the task, and the earlier approaches built on segment proposals or on semantic segmentation), Section 4 (instance segmentation on COCO with mask AP)"
  - paper: doi:10.1007/978-3-319-10602-1_48
    title: "Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollar and C. Lawrence Zitnick, Microsoft COCO: common objects in context, ECCV 2014"
    locator: "the data set of 80 object categories with a segmentation mask for each instance, and crowd regions"
  - paper: doi:10.1109/CVPR.2019.00963
    title: "Alexander Kirillov, Kaiming He, Ross Girshick, Carsten Rother and Piotr Dollar, Panoptic segmentation, IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2019, 9404-9413 (arXiv 1801.00868)"
    locator: "Section 2 and Section 3 (instance segmentation as the task for things, with overlapping segments and confidence scores, against the panoptic task)"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 6.4, Semantic segmentation (the part on instance segmentation)"
---

Instance segmentation is the problem of finding each object of a fixed set of classes in an image and giving, for each one, its class, the set of its pixels and a confidence score. It is [object detection](/object-detection/) with a pixel mask in place of a box. Unlike [semantic segmentation](/semantic-segmentation/), it keeps objects of the same class apart: three cars that touch give three masks. It covers only countable objects, such as people, cars and cups, and leaves out amorphous regions such as sky and grass. [Panoptic segmentation](/panoptic-segmentation/) adds those regions and asks for one label per pixel. The usual score is the [detection mean average precision](/detection-mean-average-precision/) with the IoU of masks in place of the IoU of boxes.

## In plain words

You give the computer a photo and a list of kinds of objects, for example person, car and dog. For each object it finds, it must give the exact outline, as a set of pixels, say what kind of object it is, and say how sure it is. If two people stand close together, the computer must give two outlines, one for each person, and not one blob. Things like sky or road are not objects here, so they are left out. A found object counts as correct when its pixels overlap enough with the pixels that a person marked for that object, and each true object can be found only once.

## Definition

Fix a set of classes $C = \{1, \ldots, K\}$. The input is a [digital image](/digital-image/) $I$ of $W \times H$ pixels. The output is a finite set of detections
$$\{(c_i, M_i, s_i) : i = 1, \ldots, m\}, \qquad c_i \in C, \quad M_i \subseteq \{0, \ldots, W - 1\} \times \{0, \ldots, H - 1\}, \quad s_i \in \mathbb{R},$$
where $M_i$ is the mask, the set of pixels of the object, $s_i$ is the score, and $m$ is chosen by the method. The masks may overlap.

The ground truth is a set of annotated masks $(c, G)$, drawn by people. The [intersection over union](/intersection-over-union/) of two masks counts pixels: $|M \cap G| / |M \cup G|$. The detections are matched to the ground truth in order of decreasing score, and a detection is a true positive if it matches an unmatched ground-truth mask of its class with IoU above a threshold $\tau$. From the matches, the precision and recall at each score cut give the average precision of each class, and their mean over the classes is the score. COCO averages this mask AP over $\tau \in \{0.5, 0.55, \ldots, 0.95\}$ and marks groups of objects that are hard to separate as crowd regions, which do not count as misses.

There is no exact correct output for an image. The masks that people draw differ near borders and at occlusions, and the problem is defined by its data set and its metric.

## Variants

- **Class-agnostic instances.** Objects without class labels, as in cell counting or in object proposals with masks.
- **Interactive instance segmentation.** A user gives a box or some clicks on one object, and the method returns its mask; [GrabCut](/grabcut/) does this from a box.
- **Amodal masks.** The mask covers the hidden parts of an occluded object too.
- **Video instance segmentation.** Masks in each frame, with the same id for the same object over time; it is related to [multi-object tracking](/multi-object-tracking/).
- **3D instances.** Separate objects in a point cloud or a set of voxels.
- **Non-overlapping output.** If each pixel must belong to at most one instance, the output is a partition of the object pixels, as in the thing part of panoptic segmentation.

## Examples

- **Three cars.** In a street photo with three cars bumper to bumper, a good output has three masks of class car. A semantic segmentation of the same photo has one region of car pixels.
- **A good box, a poor mask.** A detection whose box fits a person well but whose mask also covers the bicycle under the person can have a box IoU of 0.9 and a mask IoU below 0.5. It counts for box AP and fails for mask AP at $\tau = 0.5$.
- **A duplicate.** Two masks of class dog on the same dog, with scores 0.9 and 0.6. The first is a true positive and the second a false positive, even if its mask is just as good.
- **A non-example.** A label map that says which pixels are dog, without separating the dogs, is a semantic segmentation.

## Known algorithms

- **Detect, then segment.** A detector gives boxes, and a second step finds the object pixels in each box. [Mask R-CNN](/mask-r-cnn/) adds a mask head to Faster R-CNN, with RoIAlign in place of [RoI pooling](/roi-pooling/). The cost and the quality of its network are outside this page; its quality is a benchmark result.
- **Segment, then classify.** Region proposals with masks, from bottom-up grouping such as [selective search](/selective-search/) or [hierarchical segmentation](/ultrametric-contour-map/), are scored by a classifier. Many methods before 2017 worked in this way.
- **Group pixels.** A network gives each pixel a vector or an offset to its object center, and a clustering step, for example [mean shift](/mean-shift/) or [agglomerative clustering](/agglomerative-clustering/), groups the pixels into instances.
- **Classical methods for one class.** Cells and nuclei in microscope images are often split by [watershed segmentation](/watershed-segmentation/) with markers on a [distance transform](/distance-transform/) of a foreground mask.
- **Set prediction.** Methods in the style of [DETR](/detr/) predict a fixed-size set of masks with classes and train with a one-to-one matching to the ground truth, without non-maximum suppression.

## Bounds

There is no lower bound on the error. Methods are compared by benchmark results that depend on the data set, the metric and the year. The output has a simple size: $m$ masks of up to $WH$ pixels each, so $O(mWH)$ bits if the masks are stored as full bitmaps. Run-length codes or polygons make this smaller for compact objects. The score costs one mask IoU for each pair of a detection and a ground-truth mask of the same class, $O(WH)$ each in the worst case, or less with run-length codes. The greedy matching of the metric makes each ground-truth mask match at most one detection.

## Reductions

- **To detection and binary segmentation.** Detect boxes, then solve a foreground and background problem in each box. This is the reduction that Mask R-CNN and GrabCut use.
- **To detection.** The bounding box of each mask is a detection, so a solution gives one of [object detection](/object-detection/).
- **To semantic segmentation, for objects.** The union of the masks of each class gives the object part of a semantic label map.
- **From panoptic segmentation.** The thing segments of a panoptic output are an instance segmentation without overlaps; the scores must be added.

## Applications

Counting and measuring cells, fruit, animals or people; robot grasping and picking from a bin; photo editing that selects one person or object; autonomous driving, where each pedestrian and car is tracked; sports analysis; and as the thing part of a panoptic segmentation.

## References
