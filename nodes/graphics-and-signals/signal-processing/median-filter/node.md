---
tag: HHPV82
kind: algorithm
slug: median-filter
name: Median filter
aliases:
- median smoothing
- running median
area: graphics-and-signals/signal-processing
level: intro
summary: Replace each sample or pixel by the median of its window. It removes impulse noise and keeps step edges, and it is not a linear filter.
solves: [signal-denoising]
model: comparison-model
complexity:
  vars: {N: the number of samples or pixels, m: the window radius (width 2m + 1), L: the number of gray levels}
  time: {worst: O(N (m + L)), average: O(N m), best: O(N m)}
  space: {extra: O(m + L)}
properties: {linear: false, causal: false, stable: true, linear_phase: "not defined, the filter is not linear", deterministic: true, online: true, in_place: false}
history:
  year: 1974
  people: [John W. Tukey]
  note: Tukey proposed running medians to smooth data in a talk at EASCON 1974 and in his book Exploratory Data Analysis of 1977. Huang, Yang and Tang gave the fast histogram method for images in 1979.
prereqs: [median, discrete-convolution]
see_also: [sliding-window-median, quickselect, image-smoothing, morphological-filtering, savitzky-golay-filter, weighted-median, signal-denoising, image-histogram]
sources:
  - paper: "John W. Tukey, Nonlinear (Nonsuperposable) Methods for Smoothing Data, Conference Record EASCON 1974, page 673 (abstract); reprinted in The Collected Works of John W. Tukey, Volume II, Wadsworth, 1985, pages 837 to 856"
    locator: running medians of three and of five, and their repeated use (the reprint has the full text)
  - book: isbn:9780201076165
    title: John W. Tukey, Exploratory Data Analysis, Addison-Wesley, 1977
    locator: the chapters on smoothing sequences (running medians, repeated medians and the treatment of the end values); general locator
  - paper: doi:10.1109/TASSP.1979.1163188
    title: Thomas S. Huang, George J. Yang and Gregory Y. Tang, A Fast Two-Dimensional Median Filtering Algorithm, IEEE Transactions on Acoustics, Speech, and Signal Processing 27(1), 1979
    locator: pp. 13 to 18 (the running histogram along a row, and the update of the median with a count of the values below it)
  - paper: doi:10.1109/TASSP.1981.1163708
    title: Neal C. Gallagher Jr. and Gary L. Wise, A Theoretical Analysis of the Properties of Median Filters, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(6), 1981
    locator: pp. 1136 to 1141 (root signals are locally monotone, and repeated filtering of a finite signal reaches a root)
---

A median filter replaces each sample $x[n]$ by the [median](/median/) of the $2m + 1$ samples $x[n-m], \ldots, x[n+m]$ around it. In two dimensions it replaces each pixel by the median of the $k \times k$ block around it, $k = 2m + 1$. It removes impulse noise, such as single wrong samples or salt and pepper pixels, and unlike a linear smoothing filter it keeps a step edge sharp. It is not a linear filter, so it has no frequency response. A direct method sorts each window. The 1D method below keeps the window sorted and costs $O(m)$ per sample. The 2D method of Huang, Yang and Tang keeps a histogram of the block and costs $O(m)$ per pixel plus a short walk of the median. This is the one page of the encyclopedia for the median filter in one and two dimensions; [image smoothing](/image-smoothing/) links here for the image case.

## In plain words

Look at a few samples on each side of the current one. Sort them and take the middle value. That is the new sample. Then move one step and do it again.

If one sample is far too large, it goes to the end of the sorted list, so it is never the middle value. So a single spike disappears. A clean jump from low to high also survives: near the jump most of the values in the window are on one side, and the middle value is one of them. An average would blur the jump and smear the spike over its neighbors. The price is that the median filter can remove thin lines and small details, and the median of a sum is not the sum of the medians.

## The problem

**1D.** The input is a signal $x[0 \ldots n-1]$ of real numbers, or of any totally ordered values, and a radius $m \ge 0$. The border rule is clamping: $\hat x[i] = x[\min(\max(i, 0), n-1)]$. The output is $y[k] = \operatorname{med}\{\hat x[k-m], \ldots, \hat x[k+m]\}$, the value at index $m$ of the sorted window, for $k = 0, \ldots, n-1$.

**2D.** The input is a one-channel image $I$ of $H$ rows and $W$ columns, with pixel centers at the integer coordinates $(r, c)$, and integer values in $\{0, \ldots, L-1\}$, for example $L = 256$ for 8-bit gray levels. The border rule is clamping in each coordinate. The output pixel $O[r][c]$ is the median of the $k^2$ values $\hat I[r + a][c + b]$ for $-m \le a, b \le m$, which is the value with rank $t = (k^2 - 1)/2$ (from 0) in sorted order. A color image is filtered one channel at a time. The filter treats values as numbers; whether they are linear or gamma encoded does not change which value is the median, because both encodings are increasing.

This is one method of [signal denoising](/signal-denoising/) for impulse noise.

## The algorithm

```pseudo id=main
MEDIAN-FILTER-1D(x[0 .. n − 1], m)               ▷ x̂[i] = x[min(max(i, 0), n − 1)]
L1  S ← the sorted list of x̂[−m], …, x̂[m]
L2  y[0] ← S[m]
L3  for k ← 1 to n − 1 do
L4      remove one copy of x̂[k − m − 1] from S      ▷ find it by binary search
L5      insert x̂[k + m] into S, keeping S sorted
L6      y[k] ← S[m]

MEDIAN-FILTER-2D-ROW(I, r, m, L)                 ▷ Huang, Yang and Tang; t = (k² − 1)/2
L7  hist[0 .. L − 1] ← the counts of the k × k block around (r, 0)
L8  med ← 0, below ← 0; while below + hist[med] ≤ t do below ← below + hist[med], med ← med + 1
L9  for c ← 1 to W − 1 do                        ▷ O[r][0] ← med before the loop
L10     for each of the k rows of the block: hist[left pixel] −= 1, hist[new right pixel] += 1, and change below by 1 if that pixel is < med
L11     while below > t do med ← med − 1, below ← below − hist[med]
L12     while below + hist[med] ≤ t do below ← below + hist[med], med ← med + 1
L13     O[r][c] ← med
```

The 1D window changes by one value per step: the oldest value leaves and a new one comes in. A sorted list handles this with two binary searches. In an array the insert and the removal move up to $2m$ values, which is a fast memory move.

The 2D method keeps the histogram of the block and the count $below$ of the values in the block that are smaller than $med$. The median is the value $v$ with $below(v) \le t < below(v) + hist[v]$. When the block moves one column to the right, line L10 changes $2k$ counts and keeps $below$ correct for the old $med$. Lines L11 and L12 then walk $med$ down or up until the condition holds again. On a natural image the median moves by a few levels between neighbors, so the walk is short.

## Example

**1D, $m = 1$.** Take $x = [2, 80, 6, 3, 1, 4, 0, 5]$. With clamping, the first window is $(2, 2, 80)$ and the last is $(0, 5, 5)$.

| $k$ | window | sorted | $y[k]$ |
|---|---|---|---|
| 0 | 2, 2, 80 | 2, 2, 80 | 2 |
| 1 | 2, 80, 6 | 2, 6, 80 | 6 |
| 2 | 80, 6, 3 | 3, 6, 80 | 6 |
| 3 | 6, 3, 1 | 1, 3, 6 | 3 |
| 4 | 3, 1, 4 | 1, 3, 4 | 3 |
| 5 | 1, 4, 0 | 0, 1, 4 | 1 |
| 6 | 4, 0, 5 | 0, 4, 5 | 4 |
| 7 | 0, 5, 5 | 0, 5, 5 | 5 |

The spike 80 is gone. A moving average of three would give $\tfrac{88}{3} \approx 29.3$ at $k = 1$ and spread the spike over three outputs.

**2D, $m = 1$.** Take the $4 \times 4$ image with an isolated bright pixel at $(1, 1)$ and an edge between levels 10 and 200:

$$I = \begin{pmatrix} 10 & 10 & 10 & 200 \\ 10 & 255 & 10 & 200 \\ 10 & 10 & 200 & 200 \\ 0 & 10 & 200 & 200 \end{pmatrix}, \qquad O = \begin{pmatrix} 10 & 10 & 10 & 200 \\ 10 & 10 & 200 & 200 \\ 10 & 10 & 200 & 200 \\ 10 & 10 & 200 & 200 \end{pmatrix}.$$

The value 255 and the dark pixel 0 in the corner are removed. The edge stays sharp, with only the values 10 and 200 in the output, but the pixel $(1, 2)$ changes from 10 to 200: the median filter rounds the corners of a region at the scale of the window.

## Correctness

The 1D method keeps one invariant: before line L4 of step $k$, $S$ is the sorted list of the window of $k - 1$. Line L4 removes the value that is in the window of $k - 1$ but not of $k$, and line L5 adds the value that is new. So after line L5, $S$ is the sorted window of $k$, and $S[m]$ is its median. The 2D method keeps the invariant that $hist$ counts the block and $below$ counts the values of the block below $med$. After lines L11 and L12, $below \le t < below + hist[med]$, which says that $med$ is the value of rank $t$. The full proof, with the edge, impulse and nonlinearity properties, is in the proof file.

## Complexity

The cost model is the number of comparisons and count updates per output sample.

- **Direct method.** Sort each window: $O(m \log m)$ per sample in 1D, $O(k^2 \log k)$ per pixel in 2D. Use [quickselect](/quickselect/) instead of sorting for $O(m)$ and $O(k^2)$ expected time.
- **Sorted window, 1D.** $O(\log m)$ comparisons and $O(m)$ moves per sample, so $O(Nm)$ in total and $O(m)$ space. With a balanced structure, such as two heaps or an [order statistic tree](/order-statistic-tree/), the cost is $O(\log m)$ per sample; see the [sliding window median](/sliding-window-median/) for that method and its lower bound.
- **Huang histogram, 2D.** $2k$ count updates per pixel, plus the walk of the median. The walk is at most $L$ steps, and on smooth images a few steps. The total is $O(N(m + L))$ in the worst case. Space is $O(L)$.
- **Constant time per pixel.** Perreault and Hébert (2007) keep one histogram per column and add and remove whole columns, so each pixel costs $O(L)$ updates independent of $m$. It pays off for large windows.

## Properties

- **Not linear.** Take a window of 3 with clamping, $x = (0, 0, 1)$ and $y = (1, 0, 0)$. Then the filter gives $(0, 0, 1)$ and $(1, 0, 0)$, so the sum of the outputs is $(1, 0, 1)$. But $x + y = (1, 0, 1)$ gives $(1, 1, 1)$. At the middle, $\operatorname{med}(1, 0, 1) = 1$ but $0 + 0 = 0$. So the filter has no impulse response and no frequency response, and it is not a convolution.
- **Commutes with increasing maps.** For an increasing function $f$, the median of $f(x)$ is $f$ of the median of $x$. So the result does not depend on gamma encoding, and $\operatorname{med}(a x + b) = a \operatorname{med}(x) + b$ for $a > 0$.
- **Keeps step edges.** A step $x = (0, \ldots, 0, 9, \ldots, 9)$ passes unchanged. More generally, every monotone signal passes unchanged.
- **Removes short impulses.** In a constant run that is longer than the window, a burst of at most $m$ outliers is removed completely. A burst of $m + 1$ or more is kept, because it is the majority of some window.
- **Root signals.** A signal that the filter does not change is a root. Gallagher and Wise showed that the roots are the locally monotone signals, and that repeated filtering of a finite signal reaches a root after a finite number of passes.
- **Stable and bounded.** Each output lies between the smallest and the largest value of its window. So the output range is the input range, with no overshoot.
- **Not causal as written.** The window is centered. A causal version uses $x[n-2m], \ldots, x[n]$, which delays the output by $m$ samples.

## Variants and improvements

- **Weighted median filter.** Repeat each sample of the window a given number of times before taking the median, see the [weighted median](/weighted-median/). The center weight controls how much detail survives.
- **Rank order filters.** Take the value of rank $j$ instead of the median. Rank 0 and rank $k^2 - 1$ give the erosion and the dilation of [morphological filtering](/morphological-filtering/) with a flat square element.
- **Separable approximation.** Filter the rows with a 1D median, then the columns. This is cheaper but it is not the 2D median.
- **Adaptive median filter.** Grow the window until the median is not an extreme value, and change only pixels that look like impulses. This keeps more detail at high noise levels.
- **Repeated median.** Apply the filter until the signal is a root. Tukey combined medians of 3 and 5 with other steps into smoothers such as 4253H.

## When to use it

Use a median filter for impulse noise: dropouts and spikes in sensor data, salt and pepper noise in images, and outliers in a time series. Use it when edges must stay sharp, for example before edge detection. For Gaussian noise, a linear filter such as the Gaussian blur of [image smoothing](/image-smoothing/) or the [Savitzky-Golay filter](/savitzky-golay-filter/) reduces noise more for the same window. For streaming data with a large window, use the heap method of the [sliding window median](/sliding-window-median/).

## Pitfalls

- **Even windows.** A window of even size has two middle values. Use an odd window, or state which of the two you take.
- **The border.** Clamping, mirroring and zero padding give different values near the edge. Zero padding pulls dark values in at the border.
- **Thin lines and corners.** A line thinner than $m + 1$ pixels and corners smaller than the window are removed. The filter does not know what is noise.
- **Color by vector.** The median of each channel separately can make a color that is in no input pixel. If that matters, use a vector median.
- **Linear expectations.** You cannot design a median filter in the frequency domain, and two median filters in a row are not one median filter with a larger window.
- **Floating point keys.** A NaN in the window breaks the order. Remove NaNs first.

## Implementations

## History

John Tukey proposed running medians as a smoother for data in a talk at EASCON in 1974, and treated them at length in Exploratory Data Analysis in 1977. Running medians of 3, applied repeatedly, and combinations with other steps became standard in exploratory data analysis. Image processing took up the method in the 1970s. In 1979 Huang, Yang and Tang gave the running histogram that makes the 2D filter fast. Gallagher and Wise described the root signals in 1981, and Perreault and Hébert gave a method with a cost per pixel that does not depend on the window size in 2007.

## References
