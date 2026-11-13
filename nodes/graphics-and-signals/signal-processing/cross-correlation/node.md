---
tag: ST8WA2
kind: definition
slug: cross-correlation
name: Cross-correlation
aliases:
- sliding dot product
area: graphics-and-signals/signal-processing
level: core
summary: "The inner product of one signal with a shifted copy of another as a function of the lag k: r_xy[k] = sum of x[n+k] conj(y[n]), or its expectation for two stationary processes."
prereqs: [discrete-convolution]
see_also: [autocorrelation, matched-filter, normalized-cross-correlation, power-spectral-density, convolution-theorem, fast-fourier-transform, signal-detection, beamforming]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 10.6.1 (correlation estimates computed with the DFT and the zero padding that avoids circular wrap-around)
  - book: isbn:9780471594314
    title: Monson H. Hayes, Statistical Digital Signal Processing and Modeling, Wiley, 1996
    locator: Chapter 3, Discrete-Time Random Processes (the cross-correlation of two jointly stationary processes and the cross power spectrum)
  - paper: doi:10.1109/TASSP.1976.1162830
    title: Charles H. Knapp and G. Clifford Carter, The generalized correlation method for estimation of time delay, IEEE Transactions on Acoustics, Speech, and Signal Processing 24(4), 1976
    locator: pp. 320 to 327 (the delay between two sensors as the peak of a cross-correlation, and the frequency weightings of the generalized method)
---

The cross-correlation of two signals $x[n]$ and $y[n]$ is the inner product of $x$ with a copy of $y$ shifted by $k$ samples, as a function of the lag $k$: $r_{xy}[k] = \sum_n x[n+k]\,\overline{y[n]}$. It is large where the shifted copy lines up with $x$, so its peak gives the delay between two recordings of the same source, and the [matched filter](/matched-filter/) is a cross-correlation of the received signal with the known pulse. The [autocorrelation](/autocorrelation/) is the case $y = x$. This page is the one-dimensional signal tool; the windowed, brightness-invariant score used to find a template in an image is [normalized cross-correlation](/normalized-cross-correlation/).

## Definition

**Notation.** Signals are complex sequences sampled at the rate $f_s$ in Hz, a bar is the complex conjugate, and the lag $k$ is an integer number of samples, a delay of $k/f_s$ seconds. Frequencies $\omega$ are in radians per sample.

**For finite signals.** Let $x$ have $N_x$ samples and $y$ have $N_y$ samples, both zero outside their index ranges $0 \le n < N_x$ and $0 \le n < N_y$. The *cross-correlation* is

$$r_{xy}[k] = \sum_{n} x[n+k]\,\overline{y[n]}, \qquad -(N_y - 1) \le k \le N_x - 1,$$

and $r_{xy}[k] = 0$ for every other lag, because the sum is empty. So there are $N_x + N_y - 1$ lags that can be nonzero. With this convention a peak at a positive lag $k$ means that $x$ contains $y$ delayed by $k$ samples. Estimates divide by $N$ (biased) or by the number of terms (unbiased), as on the [autocorrelation](/autocorrelation/) page.

**For random processes.** Two processes are *jointly wide-sense stationary* when each is WSS and $\mathbb{E}\,x[n+k]\overline{y[n]}$ depends only on $k$. Their cross-correlation is

$$r_{xy}[k] = \mathbb{E}\, x[n+k]\, \overline{y[n]},$$

and its Fourier transform $S_{xy}(\omega) = \sum_k r_{xy}[k] e^{-i\omega k}$ is the *cross power spectral density*. Unlike a power spectrum, $S_{xy}$ is complex in general; its phase carries the delay.

**The identities.** These hold for the finite sums and, with expectations, for processes.

1. *Swap.* $r_{xy}[-k] = \overline{r_{yx}[k]}$. Swapping the two signals mirrors the lag axis and conjugates.
2. *Convolution form.* $r_{xy}[k] = (x * \tilde y)[k]$ with $\tilde y[n] = \overline{y[-n]}$, the time-reversed conjugate of $y$. So a correlator is an [FIR filter](/fir-filter/) whose impulse response is $\tilde y$ delayed to be causal, and every fast [convolution](/discrete-convolution/) method applies.
3. *Spectrum.* In the DTFT, $r_{xy}$ has the transform $X(e^{i\omega})\,\overline{Y(e^{i\omega})}$, by the [convolution theorem](/convolution-theorem/).
4. *Cauchy-Schwarz bound.* $|r_{xy}[k]|^2 \le r_{xx}[0]\, r_{yy}[0]$ for every $k$, where $r_{xx}[0] = \sum |x[n]|^2$ is the energy of $x$. Equality at a lag $k$ holds exactly when the overlapping parts are proportional, which is why the peak of a correlation detects a scaled copy.

**The correlation coefficient.** Dividing by the bound gives $\rho_{xy}[k] = r_{xy}[k] / \sqrt{r_{xx}[0]\,r_{yy}[0]}$, with $|\rho_{xy}[k]| \le 1$. This uses one normalization for the whole signals. Template matching needs a different normalization for every window of the image and the removal of the local mean, which is the subject of the [normalized cross-correlation](/normalized-cross-correlation/) page.

**Computation.** The direct sum costs $N_x N_y$ multiplies for all lags together, since each pair $(n+k, n)$ is used once. With the [FFT](/fast-fourier-transform/), pad both signals to a length $L \ge N_x + N_y - 1$, compute $X[m]\,\overline{Y[m]}$ and take the inverse DFT. Entry $k$ holds $r_{xy}[k]$ for $0 \le k \le N_x - 1$, and entry $L + k$ holds the negative lag $k$. The cost is $O(L \log L)$ operations. For a long $x$ and a short $y$, the [overlap-add](/overlap-add-method/) and [overlap-save](/overlap-save-method/) methods do the same work block by block.

## Examples and non-examples

**A worked pair.** Let $x = (0, 0, 1, 2, -1)$ and $y = (1, 2, -1)$, so $x$ is $y$ delayed by two samples. The lags run from $-2$ to $4$. The implementation on this page computes these sums exactly, and its FFT version agrees to within $10^{-12}$ times $\sqrt{r_{xx}[0]\,r_{yy}[0]}$.

| lag $k$ | nonzero products $x[n+k]\,y[n]$ | $r_{xy}[k]$ |
|---|---|---|
| $-2$ | none | 0 |
| $-1$ | none | 0 |
| 0 | $x[2]\,y[2] = -1$ | $-1$ |
| 1 | $x[2]\,y[1] + x[3]\,y[2] = 2 - 2$ | 0 |
| 2 | $x[2]\,y[0] + x[3]\,y[1] + x[4]\,y[2] = 1 + 4 + 1$ | 6 |
| 3 | $x[3]\,y[0] + x[4]\,y[1] = 2 - 2$ | 0 |
| 4 | $x[4]\,y[0] = -1$ | $-1$ |

The peak is $6$ at $k = 2$, the delay. It equals $r_{yy}[0] = 1 + 4 + 1$, the bound of identity 4, because the overlap at that lag is an exact copy. The rest of the row, $(-1, 0, 6, 0, -1)$, is the autocorrelation of $y$ shifted by 2.

**Delay estimation in noise.** In the test of this page, $y$ is a random $\pm 1$ pulse of 32 samples and $x$ has 80 samples: $y$ delayed by a random $d \in [0, 40]$ plus Gaussian noise of standard deviation $0.5$. The lag of the largest $|r_{xy}[k]|$ was equal to $d$ in all 500 trials (seed 4204). The peak is about $32$. At other lags the noise term has standard deviation $\sqrt{32}\cdot 0.5 \approx 2.8$ and the sidelobes of a random pulse have a spread of about $\sqrt{32} \approx 5.7$, so the peak is about five spreads above the rest and a miss is rare. Knapp and Carter weight $X\overline{Y}$ by a frequency function before the inverse transform to sharpen this peak when the noise is colored.

**Non-example: a cyclic correlation without padding.** Take $x = (1, 2, 3, 4)$ and $y = (1, 0, 0, 5)$ and use DFTs of length $L = 4$. The inverse DFT of $X\overline{Y}$ at index 1 is $7$, but $r_{xy}[1] = x[1]\,y[0] = 2$. The other $5 = x[0]\,y[3]$ is the lag $-3$, which wraps onto index $1 - 4 = -3$. A cyclic correlation is a correct answer only for signals that are periodic with period $L$.

**Non-example: a correlation peak is not a match.** For $x = (10, 10, 10, 10)$ and $y = (1, 1)$ the lags 0, 1 and 2 all give the value 20, so the peak does not locate anything. In general a part of the signal with more energy can win over a dim part that has a better shape. A raw correlation measures energy as well as shape; divide by the local energy, as in the correlation coefficient or in [normalized cross-correlation](/normalized-cross-correlation/), when the shape is what matters.

### Pitfalls

- *The lag sign.* Some texts and libraries define $r_{xy}[k] = \sum_n x[n]\overline{y[n+k]}$, which is $r_{xy}[-k]$ in the convention here, and others conjugate the first factor. Check the convention before you read a delay off a peak.
- *Using an FFT length below $N_x + N_y - 1$.* The negative lags wrap onto the positive ones, as in the non-example above.
- *Correlating with the mean in.* Two signals with large offsets have a large correlation at every lag. Subtract the means when similarity of the fluctuations is wanted.

## Related definitions

- [Autocorrelation](/autocorrelation/): the cross-correlation of a signal with itself.
- [Discrete convolution](/discrete-convolution/): $r_{xy}$ is $x$ convolved with the time-reversed conjugate of $y$.
- [Matched filter](/matched-filter/): the filter that maximizes the output signal-to-noise ratio is a correlator against the known signal.
- [Power spectral density](/power-spectral-density/): the cross power spectral density is the Fourier transform of $r_{xy}$.
- [Normalized cross-correlation](/normalized-cross-correlation/): the windowed and mean-removed score for template matching in images, and [phase correlation](/phase-correlation/), which keeps only the phase of $X\overline{Y}$.
- [Delay-and-sum beamforming](/delay-and-sum-beamforming/): it aligns sensor signals by the delays that cross-correlation estimates.

## References
