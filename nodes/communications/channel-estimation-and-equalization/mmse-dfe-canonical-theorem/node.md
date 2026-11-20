---
tag: 0B3DXD
kind: theorem
slug: mmse-dfe-canonical-theorem
name: Canonical MMSE-DFE theorem
aliases:
- MMSE-DFE capacity theorem
area: communications/channel-estimation-and-equalization
level: advanced
summary: "With infinite-length filters, ideal feedback, Gaussian codes and the water-filling input spectrum, the unbiased MMSE-DFE reaches the capacity of a Gaussian ISI channel: log2(1 + SNR_U) = C."
prereqs: [decision-feedback-equalizer, channel-capacity, mmse-linear-equalizer, water-filling-power-allocation]
see_also: [tomlinson-harashima-precoding, mimo-capacity, v-blast, successive-interference-cancellation, discrete-multitone, snr-gap-approximation, shannon-hartley-theorem, viterbi-equalizer]
sources:
  - paper: "John M. Cioffi, Glen P. Dudevoir, M. Vedat Eyuboglu and G. David Forney, Jr., MMSE decision-feedback equalizers and coding, Part I: Equalization results, IEEE Transactions on Communications 43(10), 1995, pages 2582 to 2594"
    locator: "the bias of the MMSE-DFE, the unbiased SNR and its relation to the mutual information of the ISI channel"
  - paper: "John M. Cioffi, Glen P. Dudevoir, M. Vedat Eyuboglu and G. David Forney, Jr., MMSE decision-feedback equalizers and coding, Part II: Coding results, IEEE Transactions on Communications 43(10), 1995, pages 2595 to 2604"
    locator: "coding with the MMSE-DFE and precoding"
  - paper: "J. Salz, Optimum mean-square decision feedback equalization, Bell System Technical Journal 52(8), 1973, pages 1341 to 1373"
    locator: "the minimum mean squared error of the infinite-length MMSE-DFE"
  - book: isbn:9780471241959
    title: "Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006"
    locator: "Chapter 2 (the chain rule for mutual information) and Chapter 9 (Gaussian channels and water-filling)"
---

The canonical MMSE-DFE theorem says that the [decision feedback equalizer](/decision-feedback-equalizer/) with the MMSE design loses no information on a Gaussian channel with [intersymbol interference](/intersymbol-interference/), if four conditions hold: the filters are infinitely long, the fed-back decisions are correct, the transmitter uses Gaussian codes, and the input spectrum is the water-filling spectrum. Then the unbiased SNR at the slicer satisfies $\log_2(1 + \mathrm{SNR}_U) = C$, the [channel capacity](/channel-capacity/) of the ISI channel. So an ISI channel plus an MMSE-DFE acts like one AWGN channel with that SNR, and a code for the AWGN channel works at capacity. The [linear MMSE equalizer](/mmse-linear-equalizer/) does not have this property, and the ZF-DFE has it only in the limit of high SNR. The same chain-rule argument on a matrix channel gives the capacity of [V-BLAST](/v-blast/) with MMSE nulling, and of [successive interference cancellation](/successive-interference-cancellation/) on the multiple-access channel. In practice, the feedback is moved to the transmitter by [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/), because a decoder cannot give correct decisions at once.

## Statement

**Model.** The discrete-time channel is $y[n] = \sum_l h_l\, x[n-l] + w[n]$, with $\sum_l |h_l| < \infty$, frequency response $H(\omega) = \sum_l h_l e^{-j\omega l}$, and $w[n]$ i.i.d. $\mathcal{CN}(0, N_0)$. The input $x[n]$ is a stationary Gaussian process with power spectral density $S_x(\omega)$ and power $\frac{1}{2\pi}\int S_x\, d\omega = E_s$, and $x[n] = \sum_k p_k a[n-k]$ is a monic minimum-phase filter $p$ of an i.i.d. innovations sequence $a[n] \sim \mathcal{CN}(0, \sigma_a^2)$. The receiver knows $h$, $p$ and $N_0$. The MMSE-DFE estimates $a[n]$ with an infinite-length feedforward filter on $y$ and an infinite-length causal feedback filter on $a[n-1], a[n-2], \ldots$, which are assumed correct (ideal feedback).

Write $Q(\omega) = S_x(\omega) |H(\omega)|^2 / N_0$ for the SNR spectrum, and assume $\log(1 + Q)$ is integrable and $S_x > 0$ almost everywhere.

**Theorem (Cioffi, Dudevoir, Eyuboglu and Forney, 1995).** The minimum mean squared error of the MMSE-DFE is
$$J = \sigma_a^2 \exp\!\Big(-\frac{1}{2\pi}\int_{-\pi}^{\pi} \ln\big(1 + Q(\omega)\big)\, d\omega\Big),$$
the slicer input is $q[n] = (1 - J/\sigma_a^2)\, a[n] + e[n]$ with $e[n]$ uncorrelated with $a[n]$, and the unbiased SNR $\mathrm{SNR}_U = \sigma_a^2/J - 1$ satisfies
$$\log_2(1 + \mathrm{SNR}_U) = \frac{1}{2\pi}\int_{-\pi}^{\pi} \log_2\big(1 + Q(\omega)\big)\, d\omega = \bar I(x; y),$$
the mutual information rate between the input and the output, in bits per symbol.

**Corollary (capacity).** Among input spectra with power $E_s$, the rate $\bar I$ is largest for the water-filling spectrum $S_x(\omega) = (K - N_0/|H(\omega)|^2)^+$, with the level $K$ set by the power. If $\ln S_x$ is integrable on $[-\pi, \pi)$ (for example, if $S_x$ is bounded away from zero), the MMSE-DFE for it reaches the capacity $C$ of the ISI channel: $\log_2(1 + \mathrm{SNR}_U) = C$. If the water-filling spectrum is zero on a set of positive measure, the result holds with one MMSE-DFE per interval of the band where it is positive, each at a symbol rate equal to the width of its interval.

**Finite form.** For a block channel $y = Hx + w$ with $H$ of size $n \times m$, $x \sim \mathcal{CN}(0, E_s I)$ and $w \sim \mathcal{CN}(0, N_0 I)$, let $\varepsilon_k$ be the error of the MMSE estimate of $x_k$ from $y$ and the correct $x_1, \ldots, x_{k-1}$. Then
$$\sum_{k=1}^m \log_2 \frac{E_s}{\varepsilon_k} = \log_2 \det\!\Big(I + \frac{E_s}{N_0} H^H H\Big) = I(x; y),$$
and $1/\varepsilon_k = \det A_k / \det A_{k+1}$, where $A_k$ is the trailing block from row $k$ on of $A = H^H H/N_0 + I/E_s$ and $\det A_{m+1} = 1$. These are the pivots of the triangular factorization of $A$ that eliminates from the last row up.

## In plain words

A decision feedback equalizer splits the received signal into one symbol at a time. For each symbol, it uses everything received and all the earlier symbols, which it assumes it knows. Information theory has a chain rule: what the received signal tells about a block equals the sum, over the symbols, of what it tells about each one when the earlier ones are known. The MMSE-DFE computes exactly these terms when the signals are Gaussian. So no information is lost in the split. The equalizer turns a channel with echoes into a clean channel whose quality is the full capacity, provided the transmitter shapes its power well and the earlier decisions are right.

## Proof

**Step 1: the finite form.** Take the block model. For jointly Gaussian vectors, the conditional distribution of $x_k$ given $y$ and $x_1, \ldots, x_{k-1}$ is Gaussian, its mean is the linear MMSE estimate, and its variance is the MMSE $\varepsilon_k$. The DFE with ideal feedback computes this estimate: the feedback uses $x_1, \ldots, x_{k-1}$ and the feedforward filter uses $y$, and by Theorem 1 of the [decision feedback equalizer](/decision-feedback-equalizer/) page its taps are the Wiener solution. The chain rule for mutual information gives
$$I(x; y) = \sum_{k=1}^m I(x_k; y \mid x_1, \ldots, x_{k-1}).$$
The symbols are independent, so $x_k$ given $x_1, \ldots, x_{k-1}$ still has the variance $E_s$. A complex Gaussian of variance $\sigma^2$ has the differential entropy $\log_2(\pi e \sigma^2)$, so each term is
$$h(x_k \mid x_{<k}) - h(x_k \mid y, x_{<k}) = \log_2(\pi e E_s) - \log_2(\pi e \varepsilon_k) = \log_2 \frac{E_s}{\varepsilon_k}.$$
Also $I(x; y) = h(y) - h(w) = \log_2 \det(E_s HH^H + N_0 I) - \log_2 \det(N_0 I) = \log_2 \det(I + (E_s/N_0) H^H H)$, by $\det(I + AB) = \det(I + BA)$. For the Cholesky statement: the error covariance of $x_k, \ldots, x_m$ given $y$ and $x_{<k}$ is $A_k^{-1}$, where $A_k$ is the trailing block of $A = H^H H/N_0 + I/E_s$ from row $k$ on. So $\varepsilon_k = [A_k^{-1}]_{11} = \det A_{k+1} / \det A_k$ by Cramer's rule, and the product of the $E_s/\varepsilon_k$ telescopes to $E_s^m \det A = \det(I + (E_s/N_0) H^H H)$, which is the same identity again. $\square$

**Step 2: the bias and the unbiased SNR.** By Corollary 1 of the [DFE](/decision-feedback-equalizer/) page, the slicer input is $q = (1 - \varepsilon/\sigma^2) a + e$ with $e$ uncorrelated with $a$, where $\sigma^2$ is the symbol variance and $\varepsilon$ the error. The error $q - a$ has variance $\varepsilon$, and it splits as $-(\varepsilon/\sigma^2) a + e$, so $\mathrm{Var}(e) = \varepsilon - \varepsilon^2/\sigma^2 = \varepsilon(1 - \varepsilon/\sigma^2)$. Scaling $q$ by $1/(1 - \varepsilon/\sigma^2)$ gives $a + e'$ with $\mathrm{Var}(e') = \varepsilon / (1 - \varepsilon/\sigma^2)$, so
$$\mathrm{SNR}_U = \frac{\sigma^2 (1 - \varepsilon/\sigma^2)}{\varepsilon} = \frac{\sigma^2}{\varepsilon} - 1, \qquad 1 + \mathrm{SNR}_U = \frac{\sigma^2}{\varepsilon}.$$
So each term of Step 1 is $\log_2(1 + \mathrm{SNR}_{U,k})$. $\square$

**Step 3: the infinite length.** Write the stationary model in terms of the innovations: $y = (h * p) * a + w$, a channel $h' = h * p$ with white input of variance $\sigma_a^2$. Apply Step 1 to a block of $N$ innovations with the full convolution matrix $H'_N$. Then $\frac{1}{N} \log_2 \det(I + (\sigma_a^2/N_0) H_N'^H H'_N)$ is the normalized log-determinant of a Toeplitz matrix with symbol $1 + \sigma_a^2 |H'(\omega)|^2 / N_0 = 1 + Q(\omega)$, because $\sigma_a^2 |P(\omega)|^2 = S_x(\omega)$. By Szegő's limit theorem for Toeplitz matrices, it tends to $\frac{1}{2\pi}\int \log_2(1 + Q)\, d\omega$, which is also the mutual information rate $\bar I(x; y)$ of the stationary channel. For a symbol far from both ends of the block, $\varepsilon_k$ is the error of a DFE with long but finite filters, and as the filters grow it decreases to the error $J$ of the infinite-length MMSE-DFE. The average of the $\log_2(\sigma_a^2/\varepsilon_k)$ is dominated by these middle terms, so $\log_2(\sigma_a^2/J) = \frac{1}{2\pi}\int \log_2(1 + Q)\, d\omega$. This is the formula for $J$, and with Step 2 the theorem. Salz derived the same $J$ directly by spectral factorization of $N_0 + \sigma_a^2|H'(\omega)|^2$. $\square$

**Step 4: the corollary.** The rate $\frac{1}{2\pi}\int \log_2(1 + S_x |H|^2/N_0)\, d\omega$ under the power constraint is a concave problem in $S_x$. Its maximizer is the water-filling spectrum, by the same KKT argument as for parallel Gaussian channels; see [water-filling power allocation](/water-filling-power-allocation/). The maximum is the capacity of the Gaussian ISI channel. If $\ln S_x$ is integrable, the water-filling spectrum has a monic minimum-phase factorization $S_x = \sigma_a^2 |P|^2$ with $\sigma_a^2 = \exp \frac{1}{2\pi}\int \ln S_x\, d\omega$ (the Paley-Wiener condition), and Steps 1 to 3 apply. If it vanishes on a set of positive measure, $\log S_x$ is not integrable, the innovations form does not exist, and the argument is applied to each interval of the band separately. $\square$

## Consequences

- **An ISI channel becomes an AWGN channel.** With ideal feedback and the unbiased scaling, the slicer input is the symbol plus an uncorrelated error, at the SNR $\mathrm{SNR}_U$. A good code for the AWGN channel at this SNR therefore works on the ISI channel at capacity, in the Gaussian limit.
- **Use the unbiased SNR.** The biased ratio $\sigma_a^2/J = 1 + \mathrm{SNR}_U$ overstates the SNR by 1. At low SNR this changes the predicted rate by a large factor.
- **The ZF-DFE.** Its SNR is $\exp\frac{1}{2\pi}\int \ln Q\, d\omega$ (for a white input), and $\log_2(1 + \mathrm{SNR}_{ZF})$ is less than $\bar I$. The gap tends to zero at high SNR.
- **The linear MMSE equalizer loses.** Its unbiased SNR is set by the arithmetic mean of $1/(1 + Q)$, and the arithmetic-geometric mean inequality gives $\log_2(1 + \mathrm{SNR}_{U,\mathrm{lin}}) \le \bar I$, with equality only for a flat $Q$.
- **The same chain rule elsewhere.** On the MIMO channel, MMSE nulling with successive cancellation in any order reaches the rate $\log_2\det(I + (E_s/N_0) H^H H)$ of the [MIMO channel](/mimo-capacity/) with equal power on the antennas, and the same argument gives the corner points of the multiple-access capacity region.
- **Precoding.** Since a decoder cannot give the correct decisions at once, [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) or more general precoders move the feedback to the transmitter. THP gives up a small power loss and a shaping loss for this.

**Example.** Take $h = (1, 0.5)$, $E_s = 1$, $N_0 = 0.1$ and a white input. Then $1 + Q(\omega) = 1 + 10(1.25 + \cos\omega)$, and its geometric mean is $10 \times (1.35 + \sqrt{1.35^2 - 1})/2 = 11.2846$. So $J = 1/11.2846 = 0.088616$, $\mathrm{SNR}_U = 10.28$, and the rate is $\log_2 11.2846 = 3.4963$ bits per symbol. The water-filling spectrum has the level $K = 1 + N_0 \cdot \frac{1}{2\pi}\int d\omega/(1.25 + \cos\omega) = 1 + 0.1/0.75 = 1.1333$, positive at every frequency, and the capacity is $\log_2(K/N_0) = 3.5025$ bits, because the geometric mean of $1.25 + \cos\omega$ is 1. In the finite form with blocks of $m$ symbols, the average of $\log_2(E_s/\varepsilon_k)$ is 3.4594 for $m = 1$, 3.4848 for $m = 4$ and 3.4948 for $m = 32$, and tends to 3.4963. On the channel B of Proakis, $h = (0.407, 0.815, 0.407)$ at 20 dB, the white input gives 5.076 bits, and water-filling gives 5.246 bits on 85 percent of the band, which is one interval around $\omega = 0$; that case needs the band version of the corollary.

The finite form is easy to check with a few lines of Python and the shared `cbb` helper:

```python
import math, cbb
h, es, n0, m = [1, 0.5], 1.0, 0.1, 8
H = [[complex(h[j - i]) if 0 <= j - i < len(h) else 0j for j in range(m)] for i in range(m + len(h) - 1)]
A = [[sum(H[t][i].conjugate() * H[t][k] for t in range(len(H))) / n0 + (1 / es if i == k else 0) for k in range(m)] for i in range(m)]
eps = [cbb.inv([row[k:] for row in A[k:]])[0][0].real for k in range(m)]
lhs = sum(math.log2(es / e) for e in eps)
rhs = math.log2((cbb.det(A) * es ** m).real)
print(lhs, rhs)  # both 27.9243
```

## Tightness

- **Finite filters.** On $h = (1, 0.5)$ at 10 dB, the DFE with one feedforward tap and one feedback tap has $J = 1/11$ and the rate $\log_2 11 = 3.4594$ bits, against 3.4963 for infinite length. The finite form shows the loss comes from the symbols at the ends of a block.
- **Ideal feedback.** With real decisions and coding, the decisions before decoding are unreliable, so error propagation breaks the chain rule. This is a real loss, and it is the reason for precoding.
- **Gaussian inputs.** With a finite alphabet, the mutual information of each scalar channel is less than $\log_2(1 + \mathrm{SNR}_U)$ (for example, at most 1 bit for BPSK), and the sum of the per-symbol terms can be less than the mutual information of the block, because the error $e[n]$ is not Gaussian and not independent of the past.
- **The input spectrum.** With a white input, the theorem gives the mutual information rate, not the capacity: 3.4963 against 3.5025 bits in the example, and 5.076 against 5.246 bits on the channel B of Proakis.
- **The bias.** Coding at the biased SNR $\sigma_a^2/J$ overstates the rate. The theorem is exact only for the unbiased SNR.
- **One DFE for a split band.** If the water-filling band has several intervals and a single DFE runs at the full symbol rate, the innovations form does not exist, and the DFE cannot reach capacity.

## History

Salz derived the error of the infinite-length MMSE-DFE in 1973. In 1995, Cioffi, Dudevoir, Eyuboglu and Forney showed that the MMSE-DFE is biased, that the unbiased version is the right one for coding, and that its SNR gives the mutual information of the ISI channel, so the MMSE-DFE with ideal feedback is canonical. The result explains why coding with a DFE and precoding works close to capacity on telephone lines and DSL, and it led to the generalized DFE for block and MIMO channels.

## References
