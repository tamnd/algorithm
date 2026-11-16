---
tag: 2FRG4D
kind: algorithm
slug: vibe-background-subtraction
name: ViBe
aliases:
- visual background extractor
area: computer-vision/visual-tracking
level: advanced
summary: Keep a set of past sample values per pixel, call a pixel background when enough samples are close, and update the samples randomly in time and space.
solves: [background-subtraction]
model: real-ram
complexity:
  vars: {P: the number of pixels in a frame, N: the number of samples per pixel, F: the number of frames}
  time: {worst: O(F P N)}
  space: {extra: O(P N)}
properties: {deterministic: false, online: true, randomized: true, iterative: false, exact: false}
history:
  year: 2009
  people: [Olivier Barnich, Marc Van Droogenbroeck]
  note: "Barnich and Van Droogenbroeck presented ViBe at ICASSP 2009 and described it in full in IEEE Transactions on Image Processing in 2011."
prereqs: [background-subtraction, reservoir-sampling]
see_also: [stauffer-grimson-background-model, background-subtraction, kernel-density-estimation, reservoir-sampling, median-filter, morphological-opening, connected-component-labeling, digital-image]
sources:
  - paper: doi:10.1109/TIP.2010.2101613
    title: "Olivier Barnich and Marc Van Droogenbroeck, ViBe: a universal background subtraction algorithm for video sequences, IEEE Transactions on Image Processing 20(6), 2011, 1709-1724"
    locator: "Section 3.1 (the classification), Section 3.2 (the start from one frame), Section 3.3 (the conservative, random and spatial update), Section 4.1 (the parameter values)"
  - paper: doi:10.1109/ICASSP.2009.4959741
    title: "Olivier Barnich and Marc Van Droogenbroeck, ViBe: a powerful random technique to estimate the background in video sequences, IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2009, 945-948"
    locator: "the whole paper (the first version of the method)"
  - paper: doi:10.1109/CVPR.1999.784637
    title: "Chris Stauffer and W. Eric L. Grimson, Adaptive background mixture models for real-time tracking, CVPR 1999, vol. 2, 246-252"
    locator: "the parametric model that ViBe is compared with"
  - paper: doi:10.1016/j.cosrev.2014.04.001
    title: "Thierry Bouwmans, Traditional and recent approaches in background modeling for foreground detection: an overview, Computer Science Review 11, 2014, 31-66"
    locator: "the survey of sample based models"
---

ViBe, the visual background extractor, is a method for [background subtraction](/background-subtraction/) that keeps raw values instead of a fitted model. Each pixel stores a set of $N$ sample values from its past and from its neighbors. A new value is background if at least a few samples are close to it. A background pixel then replaces one of its samples, chosen at random, with the new value, and sometimes also puts the value into a random neighbor's set. The random choice of which sample to drop gives each sample a lifetime that decays exponentially, without a time stamp. The spread to neighbors lets a wrong start, such as an object present in the first frame, fade from its border. The [Stauffer-Grimson model](/stauffer-grimson-background-model/) fits a mixture of Gaussians to each pixel and updates it with a learning rate; ViBe needs no density, no learning rate and no floating point, and it can start from a single frame.

## In plain words

Each pixel keeps a small bag of 20 old values that it has seen, or that its neighbors have seen. When a new picture comes, the pixel checks how many values in its bag are close to its new value. If at least two are close, the pixel is background; otherwise it is foreground, something that moved in. A background pixel now and then throws a random value out of its bag and puts the new value in. Now and then it also puts its value into a neighbor's bag. Because the value thrown out is random, old values leave slowly and new ones come in without any clock. Foreground pixels never change their own bag, so a walking person does not become background.

## The problem

The input is a sequence of gray images of the same size from a fixed camera; for color, the distance below is the Euclidean distance between color vectors. The output for each frame is a binary mask, 1 for foreground. The method is online and randomized.

**The model.** Pixel $x$ holds the samples $M(x) = \{s_1, \ldots, s_N\}$. The parameters are $N$, the radius $R$, the count $\#_{\min}$ and the subsampling factor $\varphi$. The paper uses $N = 20$, $R = 20$, $\#_{\min} = 2$ and $\varphi = 16$, chosen by experiment.

## The algorithm

```pseudo id=main
VIBE-FRAME(the frame v, the samples M, N, R, #min, φ)
L1   (first frame only) for each pixel x: M(x) ← N values of random pixels of the 3 × 3 neighborhood of x
L2   for each pixel x: count the samples s ∈ M(x) with |v(x) - s| < R, stopping at #min
L3       x is background if the count reaches #min, else foreground
L4   for each foreground pixel: no update
L5   for each background pixel x: with probability 1/φ, replace a sample of M(x) chosen at random by v(x)
L6       with probability 1/φ, choose a random 8-neighbor y of x and replace a random sample of M(y) by v(x)
```

The classification of line L2 stops as soon as $\#_{\min}$ samples are close, so on most background pixels it reads only a few samples. Lines L5 and L6 are the three parts of the update of the paper. The update is *conservative*: only background values enter the model. The replaced sample is chosen at random, not the oldest one. Only one frame in $\varphi$ on average updates a pixel, which the paper calls time subsampling. And the value also spreads to a neighbor, which keeps the models of nearby pixels consistent. The implementation classifies the whole frame before it updates, so the result does not depend on the order of the pixels, and it starts the model with a value from the pixel itself or one of its 8 neighbors, chosen at random.

## Example

**Classification.** A pixel with $N = 6$ has the samples $100, 104, 131, 96, 160, 119$, and $R = 20$, $\#_{\min} = 2$.

- The value 110 is closer than 20 to 100, 104, 96 and 119. The count reaches 2 at the second sample, so it is background.
- The value 140 is closer than 20 only to 131. The sample 160 is at distance exactly 20, which is not closer than $R$. The count is 1, so it is foreground.
- The value 150 is closer than 20 to 131 (distance 19) and to 160 (distance 10), so it is background.

**The lifetime of a sample.** Each update of a pixel's own set keeps a given sample with probability $(N - 1)/N$, whatever happened before. So the chance that a sample survives $k$ updates is $((N-1)/N)^k$. With $N = 5$ and an update in every frame ($\varphi = 1$), a sample survives 3 frames with probability $0.8^3 = 0.512$. With $\varphi = 16$ and $N = 20$, a pixel that only updates its own set keeps a sample for $\varphi N = 320$ frames on average. An inner pixel whose 8 neighbors are also background loses samples to its neighbors too, and the mean lifetime falls to about 160 frames.

**A ghost.** In the first frame of a $12 \times 12$ image, a $6 \times 6$ object of value 200 stands on a flat background of value 50, and then it goes away. The models of the object's pixels hold the value 200, so the free background there is foreground: a ghost. The 20 border pixels of the object took some samples from the background at the start. In the seeded run of the tests they all have at least 2 such samples, so the ghost starts with the 16 inner pixels. With $\varphi = 1$, the background values of the neighbors spread inward, and the ghost counts per frame are 16, 16, 12, 10, 7, 3, 1, 1, 0. With $\varphi = 16$, 10 pixels are still ghost after 70 frames.

**A short video.** On a $16 \times 16$ gradient background with noise of standard deviation 2, a bright $6 \times 6$ square moves in after 25 frames. In the 15 frames with the square, every square pixel is foreground, and at most 2 percent of the foreground pixels are false.

## Correctness

ViBe is a heuristic: the proved facts are about its random update, not about the quality of the mask. The proofs are in [proofs/correctness.md](proofs/correctness.md).

- **Theorem: memoryless survival.** A sample in a set that is updated $k$ times survives with probability $((N - 1)/N)^k$, independently of its age. This equals $e^{-k \ln(N / (N - 1))}$, an exponential decay.
- **Theorem: expected lifetime.** For a pixel that is always background and only updates its own set, the lifetime of a sample in frames is geometric with mean $\varphi N$. For an inner pixel whose 8 neighbors are background and have 8 neighbors each, the survival per frame is $(1 - \tfrac{1}{\varphi N})(1 - \tfrac{1}{8 \varphi N})^8$, and the mean is about $\varphi N / 2$.
- **Theorem: conservative update.** Line L5 never writes into the set of a foreground pixel; only line L6 of a background neighbor can. In a frame where all pixels are foreground, the model does not change.
- **Theorem: a ghost on a flat background only shrinks.** If all later frames are the same flat image, a pixel that is background stays background, so the number of ghost pixels never grows.
- **Not proved.** How fast a ghost disappears on real video, and how the parameters trade false alarms for misses, are benchmark results.

## Complexity

Let $P$ be the number of pixels and $N$ the number of samples per pixel, in the [real RAM](/real-ram/) model with a random integer at unit cost. Line L2 reads at most $N$ samples per pixel, and lines L5 and L6 make constant work. One frame costs $O(P N)$ time, and $F$ frames cost $O(F P N)$. The start of line L1 costs $O(P N)$ once, and the model takes $O(P N)$ space. On background pixels the early stop makes the classification much cheaper than $N$ reads in practice.

## Properties

- **Randomized.** The update uses random numbers; the result of a run depends on the seed.
- **Start from one frame.** No training sequence is needed.
- **No float arithmetic.** On 8-bit images all steps use small integers.
- **No ordering of samples.** No sample has a time stamp, and the decay is exponential by the random choice alone.
- **Spatial consistency (a heuristic).** Neighbor updates make nearby pixels share values, which can also help when the camera shakes a little.

## Variants and improvements

- **Color.** Use the Euclidean distance between color vectors, or the sum of absolute differences.
- **Adaptive radius and rate (a heuristic).** Change $R$ and $\varphi$ per pixel from the recent decisions, so that noisy pixels get a larger radius.
- **No spread across the mask border (a heuristic).** Skip a neighbor update when the chosen neighbor is foreground. Stopped objects then stay foreground longer, but ghosts also stay longer.
- **Post processing.** [Morphological opening](/morphological-opening/), a [median filter](/median-filter/) of the mask, and [connected component labeling](/connected-component-labeling/) clean the mask.
- **Kernel density estimation.** A sample based model can score a value with a [kernel density](/kernel-density-estimation/) sum instead of a count. This needs a kernel evaluation for each sample, and the early stop is lost.

## When to use it

Use ViBe for a fixed camera when the mask must be computed fast and on simple hardware, when the model must start without a training period, or when the first frames contain moving objects that must be forgotten. It is a strong and simple baseline. Do not use it when a stopped object must stay foreground for long, since the spread from its border makes it background; and do not use it with a moving camera.

## Pitfalls

- **Ghosts with a slow update.** With $\varphi = 16$ an object in the first frame leaves a ghost for many frames; in the example above, 10 of 16 ghost pixels remain after 70 frames. A smaller $\varphi$ removes it faster but also absorbs slow objects faster.
- **Objects eaten from their border.** The neighbor spread works on any foreground region, also on a real object that stands still. Its border pixels become background first.
- **The strict test.** Decide once whether a sample at distance exactly $R$ counts, and keep it the same in tests and code.
- **Visiting order.** If the update runs inside the same loop as the classification, a neighbor update can change the decision of a pixel that is visited later in the same frame. Classify first, then update.
- **Seeds in tests.** The method is random; fix the seed of the generator, and test probabilities with a tolerance.

## Implementations

The Python file follows the paper for gray images, with the parameters of the paper as defaults, and classifies each frame before the update. The tests compare the early stop with a full count, check the classification example above, measure the survival of a marked sample against $((N-1)/N)^k$ and its mean lifetime against $\varphi N$ by sampling, check the lifetime formula for an inner pixel, check that foreground pixels never update, check that a ghost shrinks frame by frame to nothing with $\varphi = 1$, and run the moving square video.

## History

The parametric model of [Stauffer and Grimson](/stauffer-grimson-background-model/) from 1999 was a common baseline for pixel models; the survey of Bouwmans covers it and the sample based models. In 2009, Barnich and Van Droogenbroeck presented ViBe at ICASSP. Its main ideas were to replace a random sample instead of the oldest one, to spread values to neighbors, and to start from one frame. The journal version of 2011 gave the full method, the analysis of the exponential decay of the sample lifetimes, and the parameter values found by experiment.

## References
