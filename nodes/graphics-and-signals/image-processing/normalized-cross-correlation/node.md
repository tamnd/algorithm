---
tag: ZSW84C
kind: algorithm
slug: normalized-cross-correlation
name: Normalized cross-correlation
aliases:
- NCC
area: graphics-and-signals/image-processing
level: advanced
summary: Score each placement of a template by the correlation coefficient of the window and the template, so that a gain and offset change of brightness does not change the score.
solves: [template-matching]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, p: the template width, q: the template height}
  time: {worst: O(W H p q), average: O(W H p q), best: O(W H p q)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, invariant_to_gain_and_offset: true, range_minus_one_to_one: true, heuristic: false}
history:
  year: 1995
  people: [J. P. Lewis]
  note: The score is the sample correlation coefficient of statistics, used for image matching long before. Lewis (1995) showed how running sum tables of the image and of its square give the denominator in constant time per offset, so that the FFT can compute the numerator.
prereqs: [template-matching, integral-image, variance]
see_also: [phase-correlation, cross-correlation, matched-filter, convolution-theorem, fast-fourier-transform, image-registration, gaussian-pyramid, sift]
sources:
  - paper: "J. P. Lewis, Fast template matching, Vision Interface 95, Canadian Image Processing and Pattern Recognition Society, Quebec City, 120-123, 1995"
    title: J. P. Lewis, Fast template matching, Vision Interface 1995
    locator: the whole paper (the conference version of the report below)
  - url: http://scribblethink.org/Work/nvisionInterface/nip.pdf
    title: J. P. Lewis, Fast normalized cross-correlation, the expanded version of the Vision Interface 1995 paper
    locator: Section 2, equations (1) and (2) for the score; Section 4 for the FFT numerator and phase correlation; Section 5 for the running sum tables of f and f squared
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 13.3, Pattern classification by prototype matching, the part on using correlation for 2-D prototype matching
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (translational alignment and its normalized cross-correlation measure)
---

Normalized cross-correlation (NCC) is a score for [template matching](/template-matching/). It puts a $p \times q$ template $t$ at each offset $(u, v)$ of a $W \times H$ image $f$ and computes the correlation coefficient of the window under the template and the template itself. The score is in $[-1, 1]$. It is $1$ exactly when the window is a positive gain times the template plus a constant, so a change of brightness $f \mapsto a f + b$ with $a > 0$ does not change it. The match is the offset with the largest score. A direct scan costs $O(WHpq)$. The fast form of Lewis (1995) takes the window sums of $f$ and $f^2$ from two [integral images](/integral-image/) in $O(1)$ per offset, so only the cross term $\sum f t$ depends on the template, and the [FFT](/fast-fourier-transform/) computes that term for all offsets in $O(WH \log(WH))$. This page is about the image score over a sliding window. The signal pages [cross-correlation](/cross-correlation/) and [matched filter](/matched-filter/) cover the unnormalized correlation of signals and the detector that maximizes the signal to noise ratio.

## In plain words

You have a small picture, the template, and you want to find where it appears in a large picture. Slide the template over every place where it fits. At each place, compare the pixels under the template with the template. A plain comparison fails when the large picture is brighter or has more contrast than the template. NCC first removes the average brightness of both patches, then divides by their contrast, and only then compares them. The result is a number between minus one and one. One means the patch is the template with the brightness and contrast changed. Zero means no relation, and minus one means a negative copy. The best place is the one with the highest number. Two tables of running sums make the brightness and contrast of every patch cheap to get.

## The problem

The input is a gray [digital image](/digital-image/) $f$ with $W$ columns and $H$ rows and a template $t$ with $p \le W$ columns and $q \le H$ rows. Pixel $(x, y)$ is $f(x, y)$, with its center at the integer point $(x, y)$. There is one channel. The values are integers (for example 0 to 255) or reals, taken as they are stored: the score is invariant to an affine change of the stored values, so gamma encoded and linear values both work, but they give different scores because the gamma curve is not affine. The offsets are the $(u, v)$ with $0 \le u \le W - p$ and $0 \le v \le H - q$, where the template lies fully inside the image, so no border rule is needed. Let $n = pq$, and at an offset let the window be $f_{u,v}(i, j) = f(u + i, v + j)$ for $0 \le i < p$ and $0 \le j < q$. With $\bar f_{u,v}$ and $\bar t$ the means of window and template, the score is

$$\gamma(u, v) = \frac{\sum_{i,j} (f_{u,v}(i,j) - \bar f_{u,v})(t(i,j) - \bar t)}{\sqrt{\sum_{i,j} (f_{u,v}(i,j) - \bar f_{u,v})^2 \, \sum_{i,j} (t(i,j) - \bar t)^2}}.$$

It is undefined when the window or the template is flat (all its values are equal), because the denominator is then zero. The output is an offset with the largest defined score.

Multiply out the sums with the window sums $F = \sum f_{u,v}$, $F_2 = \sum f_{u,v}^2$, the template sums $T = \sum t$, $T_2 = \sum t^2$, and the cross term $C = \sum f_{u,v} t$. Then

$$\gamma = \frac{nC - FT}{\sqrt{(nF_2 - F^2)(nT_2 - T^2)}},$$

which is equation (2) of Lewis in this notation. The three parts $\mathit{num} = nC - FT$, $v_f = nF_2 - F^2$ and $v_t = nT_2 - T^2$ are $n$ times the centered sums, so they are integers when the pixels are integers.

## The algorithm

```pseudo id=main
NCC-MATCH(f, t)                                    ▷ f is W × H, t is p × q
L1  n ← p q;  T ← Σ t;  T2 ← Σ t²;  vt ← n T2 − T²
L2  if vt = 0 then return "undefined: the template is flat"
L3  S1 ← INTEGRAL-IMAGE(f);  S2 ← INTEGRAL-IMAGE(f²)
L4  for v ← 0 to H − q do
L5      for u ← 0 to W − p do
L6          F ← RECT-SUM(S1, u, v, u + p, v + q);  F2 ← RECT-SUM(S2, u, v, u + p, v + q)
L7          C ← Σ_{j < q} Σ_{i < p} f(u + i, v + j) t(i, j)      ▷ or C[v][u] from line L11
L8          num ← n C − F T;  vf ← n F2 − F²
L9          γ[v][u] ← num / sqrt(vf vt) if vf > 0, else undefined
L10 return the (u, v) with the largest defined γ[v][u], the first in row-major order on a tie

FFT-CROSS-TERMS(f, t)
L11 pad f and t with zeros to W' × H' with W' ≥ W and H' ≥ H;
    C ← the real part of IDFT(DFT(f) · conj(DFT(t))), read at the valid offsets
```

Line L1 computes the template sums once. Line L3 builds the two integral images in one pass each; [RECT-SUM](/integral-image/) at line L6 then reads four entries of a table for each sum. Line L7 is the only step whose cost depends on the template size. Lines L8 and L9 combine the sums into the score. Line L10 scans the table.

Line L11 replaces line L7 for a large template. By the [convolution theorem](/convolution-theorem/), the inverse DFT of $\hat f \cdot \overline{\hat t}$ is the circular cross-correlation $\sum_{i,j} f((u + i) \bmod W', (v + j) \bmod H') \, t(i, j)$. At a valid offset $u + i \le W - 1 < W'$ and $v + j < H'$, so no index wraps, and the value is the exact $C$ up to rounding. Padding to $W + p - 1$ is not needed for the valid offsets; a power of two at least $W$ is enough for a radix-2 FFT. Lewis also points out that the template can be centered first, $t' = t - \bar t$: then $\sum f t' = \mathit{num}/n$ directly, because $\sum t' = 0$ removes the $FT$ term.

The implementation compares scores exactly. The map $x \mapsto x|x|$ is strictly increasing, so $\gamma$ has the same order as the key $\mathit{num}\,|\mathit{num}| / (v_f v_t)$, which is a fraction of integers when the pixels are integers. No square root and no rounding can then change the chosen offset.

## Example

Take the $5 \times 4$ image below and the $2 \times 2$ template $t$ with rows $(9, 2)$ and $(2, 9)$, so $n = 4$, $T = 22$, $T_2 = 170$ and $v_t = 4 \cdot 170 - 22^2 = 196$. Row $y = 0$ is on top.

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 1 | 2 | 3 | 4 | 5 |
| 1 | 2 | 9 | 2 | 6 | 2 |
| 2 | 3 | 2 | 9 | 3 | 8 |
| 3 | 4 | 5 | 2 | 6 | 1 |

There are $4 \times 3 = 12$ offsets. At $(1, 1)$ the window is the template: $F = 22$, $F_2 = 170$ and $C = 170$, so $\mathit{num} = 4 \cdot 170 - 22 \cdot 22 = 196$, $v_f = 196$, and $\gamma = 196 / \sqrt{196 \cdot 196} = 1$. At $(2, 1)$ the window has rows $(2, 6)$ and $(9, 3)$: $F = 20$, $F_2 = 130$, $C = 75$, so $\mathit{num} = 300 - 440 = -140$, $v_f = 520 - 400 = 120$, and $\gamma = -140/\sqrt{120 \cdot 196} \approx -0.9129$. The full score table, rounded to four places, is:

| $v$ \ $u$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| 0 | 0.4685 | −0.6860 | 0.5071 | −0.8452 |
| 1 | −0.6860 | 1.0000 | −0.9129 | 0.9435 |
| 2 | 0.4472 | −0.8704 | 0.9129 | −0.9285 |

The match is $(1, 1)$. The sum of squared differences (SSD) also finds it: its table has rows $(64, 148, 49, 99)$, $(148, 0, 150, 11)$ and $(56, 156, 10, 152)$, with the minimum 0 at $(1, 1)$.

Now make the image brighter and give it more contrast: $f' = 2f + 10$. The NCC table does not change at all, so the match stays at $(1, 1)$ with score 1. The SSD table becomes rows $(658, 922, 618, 830)$, $(922, 1010, 1150, 798)$ and $(570, 1050, 870, 1034)$. Its minimum, 570, is at $(0, 2)$, and the true place has 1010, one of the worst values. This is the case NCC is made for.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). Three facts carry it. First, an algebra step shows that $\mathit{num}$, $v_f$ and $v_t$ are $n$ times the centered sums of the definition, so lines L6 to L9 compute $\gamma$ exactly when $F$, $F_2$ and $C$ are right; the integral image proof gives $F$ and $F_2$, and the convolution theorem with the no-wrap argument above gives $C$ in the FFT form. Second, the Cauchy-Schwarz inequality on the centered vectors gives $|\gamma| \le 1$, with $\gamma = 1$ exactly when the centered window is a positive multiple of the centered template. Third, replacing $f$ by $af + b$ with $a > 0$ multiplies the centered window by $a$, so the numerator and the square root both gain a factor $a$ and the score does not change; with $a < 0$ the score changes sign.

## Complexity

Let $N = (W - p + 1)(H - q + 1)$ be the number of offsets.

- Line L1 costs $\Theta(pq)$, and line L3 costs $\Theta(WH)$ time and $\Theta(WH)$ space for the two tables.
- Lines L6, L8 and L9 cost $O(1)$ per offset, so $\Theta(N)$ in total. This is the gain of Lewis: without the tables, $F$ and $F_2$ cost $\Theta(pq)$ per offset.
- Line L7 costs $\Theta(pq)$ per offset, so $\Theta(Npq)$, which is $O(WHpq)$. Over all template sizes this is largest near $p = W/2$ and $q = H/2$, where it is $\Theta(W^2H^2)$.
- With line L11 instead, three 2D FFTs of size $W' \times H'$ with $W' < 2W$ and $H' < 2H$ cost $O(WH\log(WH))$, so the whole method costs $O(WH \log(WH))$ for any template size.

These are worst case bounds in the real RAM; the direct form does the same work on every input. Which form is faster for a given $p$ and $q$ depends on the machine and the FFT code. Lewis compares operation counts; the crossover is a measured number, not a bound. The extra space is $\Theta(WH)$ in both forms.

With 8-bit pixels the parts grow fast: $v_f \le n F_2 \le n^2 \cdot 255^2$, and the product $v_f v_t$ can pass $2^{64}$ for a $100 \times 100$ template. Python integers do not overflow. In C, compute the parts in 64-bit integers and the final product and square root in double precision.

## Properties

- **Bounded.** $-1 \le \gamma \le 1$ by Cauchy-Schwarz. The bound is reached only by an exact affine copy.
- **Invariant to gain and offset.** $\gamma$ does not change when the window or the template is replaced by $a \cdot (\text{patch}) + b$ with $a > 0$. With $a < 0$ the sign changes, so $|\gamma|$ finds negative copies too.
- **Not invariant to other changes.** A gamma curve, a rotation, a change of scale, a blur or an occlusion changes the score. NCC compares patches in a fixed geometry.
- **Symmetric.** Swapping window and template gives the same score.
- **Exact.** With integer pixels, $\mathit{num}$, $v_f$ and $v_t$ are exact integers, and the order of scores can be decided without rounding. Only the FFT cross term is approximate.
- **Undefined on flat patches.** A window with $v_f = 0$ has no score. A nearly flat window has a score that noise decides.
- **The same as a correlation coefficient.** $\gamma$ is the sample correlation coefficient of the $n$ pairs $(f_{u,v}(i,j), t(i,j))$, which is the covariance divided by the two standard deviations (see [variance](/variance/) and [covariance matrix](/covariance-matrix/)).

## Variants and improvements

- **Centered template.** Store $t' = t - \bar t$ and compute $\sum f t'$. This removes the $FT$ term, and it is the form to use with the FFT.
- **Uncentered normalized correlation.** $C / \sqrt{F_2 T_2}$ divides by the norms without removing the means. It is invariant to a gain only, and a bright flat window scores high against any bright template.
- **Color.** Treat the window as one vector of $3n$ values, or average the scores of the channels. The first form is invariant to one gain and offset that all channels share. The second form is invariant to a separate gain and offset on each channel.
- **Coarse to fine.** Match on a reduced level of a [Gaussian pyramid](/gaussian-pyramid/), then search only near the best offset on the next finer level. This is a heuristic: a match that is lost at the coarse level is not found again.
- **Subpixel offset.** Fit a parabola through the scores at $u - 1$, $u$ and $u + 1$ of the best offset, and the same in $v$. The vertex gives a fractional offset. The fit assumes a smooth peak, which is a model, not a guarantee.
- **Frequency domain only.** [Phase correlation](/phase-correlation/) normalizes each frequency instead of each window. It finds a shift between two whole images, not a template position, and it is more robust to narrow band changes in brightness.

## When to use it

Use NCC to find a patch whose appearance is known up to a change of brightness and contrast, at the same scale and orientation: tracking a small patch from one video frame to the next, block matching for stereo, finding fiducial marks or a known part on a conveyor, and aligning two images by small tiles before a finer [registration](/image-registration/). Use SSD when the brightness is known to be the same, because it is cheaper and the template matching page covers early termination for it. When the target can rotate or change size, use features such as [SIFT](/sift/) instead, or search over rotated and scaled templates at a cost that grows with each new degree of freedom.

## Pitfalls

- **Flat windows.** Division by zero for $v_f = 0$, and huge noisy scores for $v_f$ close to zero. Mark flat windows as undefined, or require $v_f$ above a threshold.
- **Floating point variance.** $nF_2 - F^2$ in floating point can lose all digits and even come out negative. Use integer tables, as the [integral image](/integral-image/) page explains, and clamp the final score to $[-1, 1]$.
- **Mixing up correlation and convolution.** The FFT form needs $\hat f \cdot \overline{\hat t}$. With $\hat f \cdot \hat t$ it computes a convolution, which matches a template flipped in both directions.
- **Wrap around in the FFT form.** Offsets where the template passes the right or bottom edge of the unpadded image read wrapped or zero values. Read the result only at the valid offsets.
- **Gamma.** Two images that differ by a gamma curve, for example one decoded to linear values and one not, do not differ by an affine map. NCC then does not give 1 at the true place.
- **Assuming 1 means a unique match.** A template with a repeated pattern, or a window that is an affine copy by chance, also scores 1. Check the second best peak, or the shape of the peak, before trusting a match.
- **Ties and rounding.** Two offsets with scores that differ in the last place of a double can swap. Compare the exact key, or use a fixed tie rule as at line L10.

## Implementations

## History

The correlation coefficient comes from statistics, and normalized correlation was in use for image matching in photogrammetry and early pattern recognition long before fast methods appeared. The cost of the normalization made the FFT less useful, because the FFT gives only the numerator. J. P. Lewis presented the fix at Vision Interface 1995, in a paper titled Fast template matching: tables of running sums of the image and of its square, which are integral images, give the denominator for every offset at a constant cost, and the FFT gives the numerator. An expanded version, Fast normalized cross-correlation, is the form most often cited. Viola and Jones used the same two tables in 2001 to normalize the variance of each window in their [detector](/viola-jones-detector/).

## References
