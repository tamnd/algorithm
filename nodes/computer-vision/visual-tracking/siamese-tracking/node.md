---
tag: RDHCZ9
kind: algorithm
slug: siamese-tracking
name: Siamese fully convolutional tracking
aliases:
- SiamFC
area: computer-vision/visual-tracking
level: research
summary: Track by cross-correlating features of the target exemplar with features of a larger search region, both from one network trained offline.
solves: [visual-object-tracking]
model: real-ram
complexity:
  vars: {N: the number of frames, S: the number of scales searched, F: the cost of the features of one search crop, C: the number of feature channels, Z: the number of cells of the exemplar feature map, X: the number of cells of the search feature map, M: the number of cells of the score map, U: the upsampling factor}
  time: {worst: Θ(N (S (F + C Z M) + U² M)), average: Θ(N (S (F + C Z M) + U² M)), best: Θ(N (S (F + C Z M) + U² M))}
  space: {extra: Θ(C (X + Z) + S M + U² M)}
properties: {deterministic: true, exact: false, local: true, iterative: false, online: true}
history:
  year: 2016
  people: [Luca Bertinetto, Jack Valmadre, João F. Henriques, Andrea Vedaldi, Philip H. S. Torr]
  note: Bertinetto, Valmadre, Henriques, Vedaldi and Torr trained a fully convolutional Siamese network offline on ImageNet Video and tracked by one cross-correlation per scale, with no update of the model during tracking.
prereqs: [visual-object-tracking, cross-correlation, convolution]
see_also: [correlation-filter-tracking, kernelized-correlation-filter, template-matching, normalized-cross-correlation, tracking-by-detection, object-detection, data-augmentation, intersection-over-union]
sources:
  - paper: doi:10.1007/978-3-319-48881-3_56
    title: Luca Bertinetto, Jack Valmadre, João F. Henriques, Andrea Vedaldi and Philip H. S. Torr, Fully-convolutional Siamese networks for object tracking, ECCV 2016 Workshops, Lecture Notes in Computer Science 9914, 2016, 850 to 865 (also arXiv 1606.09549)
    locator: Sections 2.1, 2.2, 2.4 and 4.1 of the arXiv version (equations 1 to 7, Table 1, the tracking settings and the frame rates)
  - paper: doi:10.1109/TPAMI.2014.2388226
    title: Yi Wu, Jongwoo Lim and Ming-Hsuan Yang, Object tracking benchmark, IEEE Transactions on Pattern Analysis and Machine Intelligence 37(9), 2015, 1834 to 1848
    locator: the whole paper (the benchmark sequences and the success plot built from the overlap of boxes)
  - paper: doi:10.1109/TPAMI.2016.2516982
    title: Matej Kristan, Jiri Matas, Aleš Leonardis, Tomáš Vojíř, Roman Pflugfelder, Gustavo Fernández, Georg Nebehay, Fatih Porikli and Luka Čehovin, A novel performance evaluation methodology for single-target trackers, IEEE Transactions on Pattern Analysis and Machine Intelligence 38(11), 2016, 2137 to 2155
    locator: the whole paper (the VOT evaluation with accuracy and robustness)
---

Siamese fully convolutional tracking follows one object through a video by comparing a picture of the object, the exemplar, with every position of a larger search region in each new frame. Both pictures go through the same function $\varphi$, a network trained in advance on many videos, and the comparison is a [cross-correlation](/cross-correlation/) of the two feature maps. The result is a score map, and the tracker moves to its maximum. Because the network has no padding and only shifts and local operations, one correlation gives exactly the similarity of every shifted sub-window, so the search costs about as much as one pass of the network over the search region. Bertinetto, Valmadre, Henriques, Vedaldi and Torr published the method in 2016. They never updated the exemplar during tracking, and they reported 86 frames per second with 3 scales on one GPU. The network is outside this page: the page implements the correlation, the loss and the steps from the score map to the new box, with a small fixed embedding in place of the trained one.

## In plain words

Take a photo of the object in the first frame. In each new frame, cut a larger piece around where the object was. Now slide the photo over that piece and, at each position, measure how much the two agree. The position with the best agreement is where the object went. Doing this on raw pixels fails when the light or the pose changes, so both pictures are first turned into feature maps by a network that has learned, from thousands of videos, what makes two views of one object look alike. The trick is that the sliding can be done after the network, on the feature maps, so the network looks at the search piece only once. A gentle preference for small moves and a few zoom levels finish the tracker.

## The problem

Given the first frame and a box $(x_1, y_1, x_2, y_2)$ around the target, output a box in each later frame (the [visual object tracking](/visual-object-tracking/) problem). Pixel $(u, v)$ has its center at the point $(u, v)$.

The method learns a function $f(z, x)$ that is high when the exemplar image $z$ and a candidate image $x$ of the same size show the same object. It takes the form

$$
f(z, x) = \varphi(z) \star \varphi(x) + b,
$$

where $\varphi$ maps an image to $C$ feature maps, $\star$ is the cross-correlation summed over the channels, and $b$ is a real bias. When $x$ is larger than $z$, the output is not one number but a score map: entry $\tau$ is the similarity of $z$ to the sub-window of $x$ at offset $k_\varphi \tau$, where $k_\varphi$ is the total stride of $\varphi$. This holds when $\varphi$ is fully convolutional, which means that it commutes with translation:

$$
\varphi(L_{k_\varphi \tau} x) = L_\tau\, \varphi(x), \qquad (L_\tau x)[u] = x[u - \tau].
$$

Training uses pairs of crops from labelled videos: an exemplar centered on the target and a search image centered on the target in another frame at most $T$ frames away. A cell $u$ of the score map gets the label $y[u] = +1$ if $k_\varphi |u - c| \le R$, where $c$ is the center of the map, and $-1$ otherwise. The loss of one cell with score $v$ is the logistic loss

$$
\ell(y, v) = \log\big(1 + e^{-y v}\big),
$$

and the loss of a map is the mean over its cells, with the positive and the negative cells weighted so that each class has the same total weight. The weights of $\varphi$ and $b$ are found by stochastic gradient descent on this loss.

Crops include context. If the target has size $w \times h$, let $p = (w + h) / 4$; the exemplar is the square with the area of $(w + 2p) \times (h + 2p)$, rescaled to a fixed size, and the search crop is a larger square with the same center and the same scale factor.

## The algorithm

```pseudo id=main
TRAIN(pairs (z, x) from labelled videos)
L1   y ← the label map: +1 within radius R of the center, -1 elsewhere
L2   L ← the weighted mean of ℓ(y[u], v[u]) with v = φ(z) ⋆ φ(x) + b
L3   take one step of stochastic gradient descent on L for the weights of φ and b

TRACK(frames, box)
L4   φz ← φ(the exemplar crop of the first frame)                ▷ computed once
L5   for each scale factor s_i do  x_i ← the search crop at the old center, side scaled by s · s_i
L6       v_i ← φz ⋆ φ(x_i)
L7       multiply the peak of v_i by the scale penalty if s_i ≠ 1
L8   i* ← the scale with the largest penalized peak;  V ← v_{i*} upsampled by U
L9   (j, k) ← the maximum of (1 - λ) V' + λ H, with V' = V scaled to [0, 1] and H a cosine window
L10  move the center by the offset of (j, k) from the center of V, times the stride and the pixel size
L11  s ← s · ((1 - γ) + γ s_{i*})                              ▷ damped scale update
L12  return the box with the new center and size
```

The settings of Bertinetto and colleagues are these. The exemplar crop is $127 \times 127$ and the search crop $255 \times 255$ pixels, and the context is chosen so that $s(w + 2p) \times s(h + 2p) = 127^2$. The parts of a crop outside the image are filled with the mean color. $\varphi$ has five convolutional layers similar to the first part of the network of Krizhevsky and colleagues, with max pooling after the first two, ReLU after all but the last, no padding, and a total stride of 8. It gives a $6 \times 6 \times 128$ map for the exemplar and $22 \times 22 \times 128$ for the search crop, so the score map is $17 \times 17$. They train on the ImageNet Video data, 4417 videos with more than 2 million boxes, for 50 epochs of 50,000 pairs. During tracking they upsample the score map from $17 \times 17$ to $272 \times 272$ with bicubic interpolation, search 5 scales $1.025^{\{-2, -1, 0, 1, 2\}}$ (or 3 in a faster version), and update the scale by linear interpolation with the factor $\gamma = 0.35$. The search region is about four times the previous size of the target. The paper adds the cosine window and penalizes changes of scale; the weight $\lambda$ and the penalty value are not given in the text.

## Example

**One correlation by hand.** Take one channel in one dimension, $\varphi(z) = (1, 2)$, $\varphi(x) = (0, 1, 2, 1, 0)$ and $b = 0$. The score map has $5 - 2 + 1 = 4$ entries:

$$
v = (1 \cdot 0 + 2 \cdot 1,\; 1 \cdot 1 + 2 \cdot 2,\; 1 \cdot 2 + 2 \cdot 1,\; 1 \cdot 1 + 2 \cdot 0) = (2, 5, 4, 1).
$$

The maximum is at offset 1, where the window of $x$ is $(1, 2)$, the same as the exemplar. Each entry is the inner product of $\varphi(z)$ with one window of $\varphi(x)$, which is what Claim 1 of the proof says in general. Now extend the search map to $(0, 1, 2, 1, 0, 5, 5)$. The window $(5, 5)$ scores $1 \cdot 5 + 2 \cdot 5 = 15$ and wins, although it does not look like $(1, 2)$. A plain inner product prefers strong features. A trained $\varphi$ has to make background features small, and a fixed $\varphi$ does not.

**The loss.** On the $17 \times 17$ map with stride 8 and $R = 16$, the positive cells are those within 2 cells of the center: 13 cells. With all scores 0 the balanced loss is $\log 2 \approx 0.693$. A score $v = 2$ costs $\log(1 + e^{-2}) \approx 0.127$ on a positive cell and $\log(1 + e^{2}) \approx 2.127$ on a negative cell.

**Tracking with fixed features.** The implementation uses four $3 \times 3$ gradient filters with a ReLU as $\varphi$ (stride 1, no padding), an exemplar crop of $20 \times 20$, a search crop of $44 \times 44$, a $25 \times 25$ score map, 3 scales $1.025^{\{-1, 0, 1\}}$ with the penalty 0.97, $\gamma = 0.35$, $\lambda = 0.25$ and bicubic upsampling by $U = 4$. These are this page's choices. The frames are $48 \times 48$, with a smooth background and a $10 \times 10$ target of random gray levels that moves by $(2.3, 1.6)$ pixels per frame, rendered at subpixel positions. The first box is $(10, 12, 20, 22)$, so the context side is 20 and one crop pixel is one image pixel. Over 7 frames the center errors are 0.34, 0.25, 0.25, 0.25, 0.21, 0.08 and 0.37 pixel. The size is not stable: in frames 5 and 6 the smaller scale wins after the penalty (in frame 5 the peaks are $13.01$, $12.58$ and $11.51$ million for the scales $1/1.025$, 1 and $1.025$, and $13.01 \times 0.97 = 12.62$ beats $12.58$), and the width goes from 10 to 9.92 and 9.83, then back to 9.92. With a target that shrinks by 4% per frame, the width goes 10, 10, 9.83, 9.67, 9.51, 9.35, 9.19 while the true width goes down to 7.51. The scale search moves the right way but lags, because gradient features change little with a small zoom. A trained embedding is what makes the scores sensitive to scale.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows these facts.

- **Theorem: one correlation scores every sub-window.** If every layer of $\varphi$ is a local operation with no padding and a stride, then entry $\tau$ of $\varphi(z) \star \varphi(x) + b$ equals $\langle \varphi(z), \varphi(x_\tau) \rangle + b$, where $x_\tau$ is the sub-window at offset $k_\varphi \tau$. Padding breaks this.
- **Theorem: the logistic loss.** $\ell(y, v)$ is strictly convex in $v$, decreasing in the margin $y v$, equal to $\log 2$ at $v = 0$, with derivative $-y / (1 + e^{y v})$. It is convex in the scores, not in the weights of the network.
- **Theorem: upsampling.** The maximum of a bilinear upsampling is always at a node of the original map, so it gives no finer position; bicubic interpolation with the Keys kernel keeps the nodes, reproduces quadratics, and can put the peak between nodes.
- **Theorem: the step from the map to the box.** The offset of the peak from the center of the map, times the stride and the pixel size, is the displacement of the exemplar window, and the damped scale update multiplies the size by a factor between 1 and the chosen scale.

Nothing proves that the maximum of the score map is on the target. That depends on the learned embedding, and the accuracy figures of the paper are benchmark results, not theorems.

## Complexity

Let $F$ be the cost of $\varphi$ on one search crop, $C$ the number of channels, $Z$ the number of cells of $\varphi(z)$, $X$ of $\varphi(x)$, and $M$ of the score map. One scale costs $F$ for the features and $\Theta(C Z M)$ for the correlation. The upsampling and the window cost $\Theta(U^2 M)$. A frame costs $\Theta(S (F + C Z M) + U^2 M)$, and $N$ frames cost $N$ times that. The exemplar features are computed once. The extra space is $\Theta(C (X + Z))$ for the feature maps, $\Theta(S M)$ for the score maps and $\Theta(U^2 M)$ for the upsampled map. For a trained network, $F$ dominates. The cost of the network is outside this page and depends on its layers. Scoring the $M$ sub-windows one by one would cost $M$ passes of the network over an exemplar-sized window, and the fully convolutional form removes that factor.

## Properties

- **No update online.** The exemplar features of the first frame are kept for the whole video. The tracker cannot drift by learning the background, and it cannot adapt to a new appearance either.
- **Fully convolutional.** The score map is exact for every shifted window, and the search region can have any size.
- **Translation equivariant.** A shift of the search image by a multiple of the stride shifts the score map. There is no learned bias toward the center of the crop. The cosine window adds one by design.
- **Deterministic.** Tracking has no random steps.
- **Coarse grid.** The score map has one cell per stride of the network, 8 pixels in the paper. The upsampling makes the position finer.
- **Fixed aspect ratio.** The size changes only by a common factor, so the box keeps its first aspect ratio.

## Variants and improvements

- **Correlation filter layer.** Valmadre and colleagues put a differentiable [correlation filter](/correlation-filter-tracking/) on the exemplar features and trained through it (2017). The exemplar can then be updated online cheaply.
- **Region proposals.** Later Siamese trackers add a second branch that predicts box offsets and sizes at each cell, as in [object detection](/object-detection/). This replaces the scale search and gives any aspect ratio.
- **Deeper backbones.** Deeper networks need padding, which breaks the exact equivariance. One fix is to vary the position of the target during training so that the network does not learn a bias toward the center.
- **Distractor-aware training.** Add hard negative pairs from other objects of the same class, so that similar objects score lower.
- **Masks.** A third branch can output a segmentation mask of the target for each cell.
- **Templates updated online.** Keep a small set of exemplars, or a running mean of the exemplar features, to follow changes of appearance.

## When to use it

Use a Siamese tracker when you track one object of any class in real time, and a GPU and a trained network are available. It suits short-term tracking where the object changes slowly and does not leave the frame for long. For a tracker with no trained network, use the [kernelized correlation filter](/kernelized-correlation-filter/). It learns online and runs on a CPU. For long sequences where the object leaves and comes back, add a detector, as [tracking-learning-detection](/tracking-learning-detection/) does. For many objects of known classes, use [tracking by detection](/tracking-by-detection/).

## Pitfalls

- **Padding in the network.** With zero padding the score map is not the similarity of the sub-windows, and the network can learn to prefer the center of the crop. Without padding, every layer shrinks the map.
- **Wrong map-to-image scale.** The displacement is the map offset times the stride times the size of a crop pixel in the image. Forgetting either factor moves the box by the wrong amount.
- **Bilinear upsampling.** It never moves the maximum off a node, so it adds cost and no accuracy. Use bicubic interpolation or fit a parabola around the peak.
- **Unnormalized scores.** The plain inner product grows with the strength of the features, so a bright or highly textured region can win, as the example shows. A trained network learns to avoid this only for scenes like its training data.
- **Training data from the benchmark.** If the network is trained on videos from the test benchmark, the results are not fair. The VOT rules forbid this, and Bertinetto and colleagues trained on ImageNet Video for this reason.
- **Scale drift.** Small wrong scale choices add up. The penalty and the damping slow this down but do not stop it, and the example shows the size moving on a target of constant size.

## Implementations

The trained network is outside this page, and no page trains a network. The Python code implements the cross-correlation of feature maps of line L6 with a fixed embedding: four $3 \times 3$ gradient filters with a ReLU, stride 1 and no padding. Any function with the same signature can replace `features`. The code also gives the label map and the balanced logistic loss of lines L1 and L2, the crop with context, the scale search with the penalty, bicubic upsampling, the cosine window and the damped scale update. Of line L3, only the step for the bias $b$ is implemented, since every score has the derivative 1 in $b$. The step for the weights of the network is not. The tests check the equality of the score map with the similarity of every sub-window, the shift of the score map, the loss and its gradient, the 13 positive cells, the upsampling, and tracking a moving and a shrinking target.

## History

Siamese networks, two copies of one network with shared weights whose outputs are compared, go back to the signature verification work of Bromley and colleagues in the early 1990s. They were later used for face verification, for patch descriptors and for one-shot recognition. In tracking, the usual approach before 2016 was to learn a model online from the video itself, as in [tracking-learning-detection](/tracking-learning-detection/) and the [kernelized correlation filter](/kernelized-correlation-filter/), or to fine-tune a pretrained network during tracking, which was slow. In 2016 Bertinetto, Valmadre, Henriques, Vedaldi and Torr trained a fully convolutional Siamese network offline on ImageNet Video and tracked with no online learning. They reported results competitive with the best trackers of the time on the OTB and VOT benchmarks at more than real-time speed. The same year Held, Thrun and Savarese regressed the box directly with a network, and Tao, Gavves and Smeulders matched sampled candidate boxes with a Siamese network. Later Siamese trackers added correlation filter layers, region proposal branches, deeper backbones and masks.

## References
