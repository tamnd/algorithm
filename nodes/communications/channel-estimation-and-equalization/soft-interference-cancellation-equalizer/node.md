---
tag: G8QTJ4
kind: algorithm
slug: soft-interference-cancellation-equalizer
name: MMSE turbo equalizer with soft interference cancellation
aliases:
- Tuchler-Koetter-Singer equalizer
- SISO MMSE equalizer
area: communications/channel-estimation-and-equalization
level: advanced
summary: "A linear MMSE equalizer that uses decoder priors: it subtracts the soft symbol means and outputs extrinsic LLRs. Exact form O(W^3) per symbol for a window W; a fixed-filter form is far cheaper."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {K: the number of symbols, W: the window length N1 + N2 + 1, L: the number of channel taps}
  time: {worst: O(K W^3)}
  space: {extra: O(W^2)}
properties: {deterministic: true, soft_input: true, soft_output: true, extrinsic_output: true, exact_map: false, needs_channel: true, needs_noise_level: true}
history:
  year: 2002
  people: [Michael Tüchler, Ralf Koetter, Andrew C. Singer]
  note: "Wang and Poor (1999) used soft interference cancellation followed by an MMSE filter for coded CDMA. Tüchler, Koetter and Singer (2002) and Tüchler, Singer and Koetter (2002) gave the MMSE equalizer with priors as a low-cost replacement for the BCJR equalizer in turbo equalization."
prereqs: [mmse-linear-equalizer, turbo-equalization]
see_also: [bcjr-algorithm, viterbi-equalizer, frequency-domain-equalization, parallel-interference-cancellation, expectation-propagation-detection, mmse-mimo-detector, decision-feedback-equalizer, soft-demapping]
sources:
  - paper: doi:10.1109/TCOMM.2002.1006557
    title: "Michael Tüchler, Ralf Koetter and Andrew C. Singer, Turbo equalization: principles and new results, IEEE Transactions on Communications 50(5), 2002, pages 754 to 767"
    locator: "the linear MMSE equalizer with a priori information inside the turbo loop, its exact and approximate forms, and the comparison with the MAP equalizer"
  - paper: doi:10.1109/78.984761
    title: "Michael Tüchler, Andrew C. Singer and Ralf Koetter, Minimum mean squared error equalization using a priori information, IEEE Transactions on Signal Processing 50(3), 2002, pages 673 to 683"
    locator: "the MMSE filter whose coefficients are recomputed for each symbol from the prior means and variances"
  - paper: doi:10.1109/MSP.2004.1267050
    title: "Ralf Koetter, Andrew C. Singer and Michael Tüchler, Turbo equalization, IEEE Signal Processing Magazine 21(1), 2004, pages 67 to 80"
    locator: "a tutorial on turbo equalization with the MAP and the MMSE equalizers"
  - paper: "Xiaodong Wang and H. Vincent Poor, Iterative (turbo) soft interference cancellation and decoding for coded CDMA, IEEE Transactions on Communications 47(7), 1999, pages 1046 to 1061"
    locator: "soft interference cancellation with the decoder outputs, followed by an MMSE filter"
---

The MMSE turbo equalizer with soft interference cancellation is the low-cost soft-in soft-out equalizer of [turbo equalization](/turbo-equalization/). It is a linear [MMSE equalizer](/mmse-linear-equalizer/) that also uses prior LLRs from the decoder. For each symbol $x_n$, it turns the priors of the other symbols into soft means and variances, subtracts the mean interference from the received window, and filters the rest with the MMSE filter for those variances. It then turns the filter output into an extrinsic LLR with a Gaussian model. The difference from the [turbo equalization](/turbo-equalization/) page is the scope. That page is the loop: equalizer, deinterleaver, decoder, interleaver, and back. This page is one equalizer for that loop, which replaces the [BCJR](/bcjr-algorithm/) equalizer. The BCJR equalizer costs $O(2^L)$ per symbol for BPSK and $L$ taps. This one costs $O(W^3)$ per symbol in its exact form, for a window of $W$ samples, and much less in its fixed-filter form.

## In plain words

A coded signal passes through a channel with echoes. A decoder already has a guess about each transmitted bit, with a level of confidence. To estimate one symbol, the equalizer uses the guesses for its neighbours. It removes their expected echoes from the received samples, and it trusts this more where the decoder is more confident. What is left is mostly the wanted symbol plus noise and the echoes of the uncertain neighbours. A linear filter, tuned to that remaining uncertainty, then gives the best linear estimate of the symbol. The equalizer ignores the decoder's guess about the symbol itself, so that it returns only new information. This new information goes back to the decoder, and the two repeat.

## The problem

The input is a block of $K$ BPSK symbols $x_k = 1 - 2 b_k$ sent through a real channel $h = (h_0, \ldots, h_{L-1})$ that the receiver knows:
$$y_m = \sum_{l=0}^{L-1} h_l\, x_{m-l} + w_m, \qquad w_m \sim N(0, \sigma^2), \qquad m = 0, \ldots, K + L - 2.$$
The receiver also has a prior LLR $L_a(x_k) = \ln P(b_k = 0) / P(b_k = 1)$ for each symbol, from the decoder. The prior gives the soft mean and variance
$$\bar x_k = \tanh(L_a(x_k) / 2), \qquad v_k = 1 - \bar x_k^2.$$
The output is an extrinsic LLR $L_e(x_n)$ for each $n$, which must not depend on $L_a(x_n)$. A linear MMSE estimate of $x_n$ from a window of samples is wanted, not the exact posterior, which the BCJR algorithm gives at exponential cost.

For symbol $n$, the window is $Y = (y_{n-N_2}, \ldots, y_{n+N_1})$, with $W = N_1 + N_2 + 1$ samples and $N_1 \ge L - 1$. It equals $H X + w$ for the $W + L - 1$ symbols $X = (x_{n-N_2-L+1}, \ldots, x_{n+N_1})$ and the $W \times (W + L - 1)$ matrix $H$ with $H_{ij} = h_{i-j+L-1}$. Column $N_2 + L - 1$ of $H$ belongs to $x_n$; call it $s$. Symbols outside the block are known zeros, and samples outside it are zero.

## The algorithm

```pseudo id=main
SISO-MMSE(y, h, L_a, σ², N1, N2)
L1  x̄_k ← tanh(L_a(x_k)/2),  v_k ← 1 - x̄_k²  for all k
L2  for n ← 0 to K - 1 do
L3      Y ← (y[n-N2], ..., y[n+N1]);  X̄, V ← means and diagonal of variances of the window symbols
L4      C ← H V Hᵀ + σ² I + (1 - v_n) s sᵀ        ▷ the covariance with x_n unknown
L5      f ← C⁻¹ s
L6      x̂ ← fᵀ (Y - H X̄ + x̄_n s)                ▷ cancel the soft interference
L7      μ ← sᵀ f
L8      L_e(x_n) ← 2 x̂ / (1 - μ)
L9  return L_e
```

Line L1 converts the priors to soft symbols. A prior of 0 gives mean 0 and variance 1, and a very large prior gives mean $\pm 1$ and variance 0. Line L3 reads the window. Line L4 is the covariance of $Y$ when $x_n$ has mean 0 and variance 1 and every other symbol has its prior mean and variance: the term $(1 - v_n) s s^T$ replaces $v_n$ by 1 in $H V H^T$. Line L5 is the MMSE filter for that covariance. Line L6 subtracts the mean of $Y$ under the same model, $H \bar X - \bar x_n s$, and filters the rest. Line L7 is the gain of the filter on $x_n$. Line L8 is the LLR of $\hat x$ under the model $\hat x \mid x_n \sim N(\mu x_n, \mu (1 - \mu))$.

The **fixed-filter form** replaces $V$ in line L4 by $\bar v I$, with $\bar v$ the mean of all $v_k$, and runs lines L4 and L5 once per block. Then only lines L6 to L8 run per symbol. The code has both forms; the flag `approx` selects the second.

## Example

**One symbol by hand.** Take $h = (1, 0.5)$, $\sigma^2 = 0.5$, $N_1 = N_2 = 1$, five symbols with priors $(0, 2, 0, -2, 0)$ and the samples $y = (1.2, 0.4, -0.9, -0.8, 0.6, 0.3)$. For $n = 2$, line L1 gives $\bar x = (0, 0.7616, 0, -0.7616)$ and $v = (1, 0.42, 1, 0.42)$ for $x_0$ to $x_3$. The window is $Y = (y_1, y_2, y_3) = (0.4, -0.9, -0.8)$, and
$$H = \begin{pmatrix} 0.5 & 1 & 0 & 0 \\ 0 & 0.5 & 1 & 0 \\ 0 & 0 & 0.5 & 1 \end{pmatrix}, \quad s = (0, 1, 0.5), \quad C = \begin{pmatrix} 1.170 & 0.210 & 0 \\ 0.210 & 1.605 & 0.5 \\ 0 & 0.5 & 1.170 \end{pmatrix}.$$
Line L5 gives $f = (-0.1043, 0.5809, 0.1791)$. The cancelled window is $Y - H \bar X = (-0.3616, -1.2808, -0.0384)$, because $\bar x_2 = 0$. Then $\hat x = -0.7132$, $\mu = 0.6705$ and $L_e(x_2) = 2(-0.7132)/0.3295 = -4.33$. The five outputs are $(4.41, -0.60, -4.33, -0.95, 4.08)$.

**Better priors, fewer errors.** On the Proakis B channel $(0.407, 0.815, 0.407)$ with $\sigma = 0.5$, $N_1 = N_2 = 4$, $K = 6000$ symbols (seed 7), the priors are drawn as consistent Gaussian LLRs, $L_a = x \sigma_a^2 / 2 + N(0, \sigma_a^2)$ (seed 8). The table gives the error rate of the sign of $L_e$ alone. This is a measurement.

| prior variance $\sigma_a^2$ | 0 | 1 | 4 | 16 | perfect |
|---|---|---|---|---|---|
| exact form | 0.1325 | 0.1150 | 0.0778 | 0.0278 | 0.0220 |
| fixed-filter form | 0.1325 | 0.1155 | 0.0875 | 0.0333 | 0.0220 |

The matched filter bound is $Q(\|h\|/\sigma) = 0.0230$. With perfect priors, all the interference is removed, and both forms reach the bound. With no priors, both forms are the plain MMSE equalizer. In between, the exact form is better, because it uses the variance of each neighbour.

## Correctness

**Claim 1 (the linear MMSE estimate).** Model $x_n$ as mean 0 and variance 1, and every other symbol in the window as independent with mean $\bar x_k$ and variance $v_k$. Then $\hat x$ of line L6 is the linear MMSE estimate of $x_n$ from $Y$, and $\mu$ of line L7 is its covariance with $x_n$. This is a theorem. Under the model, $E[Y] = H \bar X - \bar x_n s$, $\mathrm{Cov}(Y) = C$ and $\mathrm{Cov}(Y, x_n) = s$, and the linear MMSE estimate is $E x_n + \mathrm{Cov}(x_n, Y)\, \mathrm{Cov}(Y)^{-1} (Y - E Y) = s^T C^{-1} (Y - E Y)$. The test enumerates all 32 symbol patterns of a small case, builds the mean and the covariance from them, and matches the code to $10^{-9}$.

**Claim 2 (extrinsic).** $L_e(x_n)$ does not depend on $L_a(x_n)$. This is a theorem: $x_n$ enters line L4 through $H V H^T + (1 - v_n) s s^T$, in which the $v_n$ terms cancel, and line L6 through $-H \bar X + \bar x_n s$, in which the $\bar x_n$ terms cancel.

**Claim 3 (the Gaussian LLR).** For each value of $x_n$, $E[\hat x \mid x_n] = \mu x_n$ and $\mathrm{Var}[\hat x \mid x_n] = \mu - \mu^2$, with $0 \le \mu < 1$. These moments are a theorem. Line L8 is the exact LLR of a Gaussian with these moments, $\ln N(\hat x; \mu, \mu - \mu^2) / N(\hat x; -\mu, \mu - \mu^2) = 2 \hat x / (1 - \mu)$. The Gaussian shape is a heuristic: $\hat x$ is a sum of noise and residual symbols, and it is only close to Gaussian. So $L_e$ is not the true extrinsic LLR, and the equalizer is not the MAP equalizer.

**Special cases, as closed forms.** With all priors 0, $v = 1$, $\bar x = 0$ and $f = (H H^T + \sigma^2 I)^{-1} s$, the MMSE linear equalizer. With perfect priors, $v = 0$, $C = \sigma^2 I + s s^T$ and $L_e(x_n) = 2 s^T (Y - H \bar X + \bar x_n s) / \sigma^2$, the matched filter after exact cancellation, which is the true LLR for that case. The proofs folder has the details.

## Complexity

In the exact form, line L4 builds a $W \times W$ matrix in $O(W^2 (W + L))$ operations, and line L5 solves it in $O(W^3)$. Since $L \le N_1 + 1 \le W$, $K$ symbols cost $O(K W^3)$ time in the [real RAM](/real-ram/) and $O(W^2)$ extra space. The window moves by one sample per symbol, so $C$ shares a $(W-1) \times (W-1)$ block with the previous one, and a bordering update of the inverse brings the cost to $O(W^2)$ per symbol; the code does not do this. The fixed-filter form solves once, in $O(W^3)$, and then costs $O(W + L)$ per symbol if $H^T f$ is computed once; the code computes line L6 directly, in $O(W (W + L))$. The BCJR equalizer, for comparison, costs $O(2^L)$ per symbol for BPSK, one step per trellis edge, so the MMSE equalizer pays off for long channels and large alphabets.

## Properties

- **Soft in, soft out, extrinsic.** The output can go back to a decoder without the prior of the same symbol.
- **It reduces to known equalizers.** With no priors, it is the linear MMSE equalizer. With perfect priors, it is the matched filter after cancellation, which reaches the matched filter bound.
- **Not MAP.** It is linear in $Y$ and its LLR uses a Gaussian model, so in the first iteration it is worse than the BCJR equalizer on a hard channel such as Proakis B.
- **Needs the channel and the noise level.** Both enter $C$; an estimate is used in practice.
- **The fixed-filter form is exact for equal variances.** When all $|L_a|$ are equal, $V = \bar v I$ in the interior of the block, and the two forms agree there to rounding. The test checks this.

## Variants and improvements

- **Fixed-filter form.** One filter per block from the mean variance, as above. It trades some performance for a large drop in cost.
- **Frequency-domain form.** With a cyclic prefix, the fixed filter becomes one division per frequency, as in [frequency domain equalization](/frequency-domain-equalization/).
- **Decision feedback.** Feed back the soft means of past symbols in a [decision feedback](/decision-feedback-equalizer/) structure.
- **Expectation propagation.** [EP detection](/expectation-propagation-detection/) also uses Gaussian models of the symbols, but it refines the means and variances from the equalizer's own posterior, not only from the decoder priors.
- **MIMO and CDMA.** The same steps with a MIMO channel matrix give the soft MMSE MIMO detector; Wang and Poor (1999) used them for coded CDMA.

## When to use it

Use it as the equalizer of a turbo receiver when the BCJR equalizer is too costly: long channels, large alphabets, or MIMO. Use the fixed-filter or frequency-domain form when the cost must be close to that of a plain MMSE equalizer. For short channels with BPSK, the BCJR equalizer is cheap and better, especially in the first iteration.

## Pitfalls

- **Feeding back posterior LLRs into line L1.** The prior must be the extrinsic output of the decoder. Posteriors count the equalizer's own information twice, and the loop becomes overconfident.
- **Leaving $x_n$ with its prior in line L4 or line L6.** Then the output is not extrinsic, and Claim 2 fails.
- **Overflow in line L1.** Use $\tanh$, not $(e^L - 1)/(e^L + 1)$, for large $|L_a|$.
- **A noise variance that is too small in line L4.** With perfect priors, $C$ tends to $s s^T$ as $\sigma^2 \to 0$, and the LLRs become huge. Do not set $\sigma^2$ to 0.
- **Edge effects.** At the ends of the block, the window reaches outside. Treat missing symbols as known zeros and missing samples as zero, as in the code, or use a terminated block.

## Implementations

## History

Wang and Poor (1999) combined soft interference cancellation with an MMSE filter in an iterative receiver for coded CDMA. Tüchler, Koetter and Singer (2002) and Tüchler, Singer and Koetter (2002) worked out the MMSE equalizer with a priori information for turbo equalization, with exact and approximate forms, and showed that it comes close to the MAP equalizer at much lower cost. Koetter, Singer and Tüchler (2004) gave a tutorial on the method.

## References
