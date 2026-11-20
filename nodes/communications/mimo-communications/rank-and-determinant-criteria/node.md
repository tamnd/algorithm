---
tag: K08JDC
kind: theorem
slug: rank-and-determinant-criteria
name: Rank and determinant criteria
aliases:
- space-time code design criteria
area: communications/mimo-communications
level: advanced
summary: The diversity of a space-time code is the minimum rank of codeword differences, and the coding gain is set by their determinants.
prereqs: [mimo-channel-model, diversity-order, chernoff-bound, alamouti-code, orthogonal-space-time-block-codes]
see_also: [space-time-trellis-codes, golden-code, diversity-multiplexing-tradeoff, union-bound, rayleigh-fading-channel, eigenvalue, determinant, maximal-ratio-combining]
sources:
  - paper: doi:10.1109/18.661517
    title: "Vahid Tarokh, Nambi Seshadri and A. Robert Calderbank, Space-time codes for high data rate wireless communication - performance criterion and code construction, IEEE Transactions on Information Theory 44(2), 744-765, 1998"
    locator: "the pairwise error bound for quasi-static Rayleigh fading, the rank and determinant criteria, the criteria for fast fading, and the space-time trellis codes built from them"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 3.3.2, Transmit diversity - space-time codes (the pairwise error probability and the determinant criterion), and Section 9.2.4 (universal code design for MIMO channels)"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 6, Space-time coding without channel knowledge at the transmitter (the pairwise error probability and the design criteria)"
  - book: isbn:9780521842914
    title: "Hamid Jafarkhani, Space-Time Coding - Theory and Practice, Cambridge University Press, 2005"
    locator: the chapter on the design criteria for space-time codes
---

The rank and determinant criteria of Tarokh, Seshadri and Calderbank say how a space-time code should look if it is to have a low error rate in slow Rayleigh fading. Take two codewords and their difference matrix $\Delta$. The **rank criterion** says that the diversity of the code is $N_r$ times the smallest rank of any $\Delta$, so full diversity $N_t N_r$ needs every $\Delta$ to have full rank. The **determinant criterion** says that the coding gain, the shift of the error curve, grows with the smallest product of the nonzero eigenvalues of $\Delta \Delta^H$. The [Alamouti code](/alamouti-code/) and other [orthogonal space-time block codes](/orthogonal-space-time-block-codes/) meet the rank criterion by construction, [space-time trellis codes](/space-time-trellis-codes/) were searched for with it, and the [golden code](/golden-code/) keeps the determinant bounded away from zero as the constellation grows. Both criteria come from a Chernoff bound at high SNR, so they are design rules for one pair of codewords, not exact error rates.

## Statement

Codewords are $N_t \times T$ matrices, rows for antennas and columns for time, with the energy included in the entries. The channel is quasi-static: $Y = H X + W$ with $H \in \mathbb{C}^{N_r \times N_t}$ fixed over the $T$ slots, i.i.d. $\mathcal{CN}(0, 1)$ entries, known at the receiver, and $W$ with i.i.d. $\mathcal{CN}(0, N_0)$ entries. The receiver is the maximum likelihood decoder, $\hat X = \arg\min_X \|Y - H X\|_F^2$.

For two codewords $X \ne X'$, let $\Delta = X - X'$, let $r$ be the rank of $\Delta \Delta^H$, and let $\lambda_1, \ldots, \lambda_r$ be its nonzero eigenvalues.

**Theorem (pairwise error bound).** The probability that the decoder prefers $X'$ when $X$ was sent, ignoring all other codewords, satisfies

$$P(X \to X') \le \prod_{i=1}^{r} \left(1 + \frac{\lambda_i}{4 N_0}\right)^{-N_r} \le \left(\prod_{i=1}^{r} \lambda_i\right)^{-N_r} \left(\frac{1}{4 N_0}\right)^{-r N_r}.$$

**Rank criterion.** The bound falls as $N_0^{\,r N_r}$, so a code whose smallest rank over all pairs is $r_{\min}$ has diversity at least $r_{\min} N_r$. Full diversity $N_t N_r$ requires every difference matrix to have rank $N_t$.

**Determinant criterion.** Among codes with the same $r_{\min}$, the error bound is smaller when $\min_{\text{pairs}} \left(\prod_{i=1}^{r} \lambda_i\right)^{1/r}$ is larger. For full-rank codes, this is $\min |\det(\Delta \Delta^H)|^{1/N_t}$, the **coding gain**.

## In plain words

A space-time code is a list of patterns, one for each message, and each pattern says what every antenna sends at every moment. The receiver confuses two patterns when the fading makes them look alike.

Look at how two patterns differ. If the difference reaches the receiver through every transmit antenna in an independent way, all paths must fade at once before the two patterns can be confused, and that is rare. If the difference uses only some antennas, fewer paths protect it. So the first rule is: every pair of patterns must differ in a way that uses all antennas. The second rule is: among codes that obey the first rule, prefer the one whose closest pairs still differ by a large amount.

## Proof

**Step 1 (the conditional error).** Given $H$, the decoder prefers $X'$ when $\|Y - H X'\|_F^2 < \|Y - H X\|_F^2$. With $Y = H X + W$, this is $\|H \Delta + W\|_F^2 < \|W\|_F^2$, that is,

$$\|H \Delta\|_F^2 + 2\,\mathrm{Re}\, \mathrm{tr}(W^H H \Delta) < 0.$$

The second term is a real Gaussian with mean 0 and variance $2 N_0 \|H \Delta\|_F^2$, since each complex noise entry contributes $\mathrm{Re}(w^* c)$ with variance $N_0 |c|^2 / 2$. So

$$P(X \to X' \mid H) = Q\!\left(\sqrt{\frac{\|H \Delta\|_F^2}{2 N_0}}\right) \le \exp\!\left(-\frac{\|H \Delta\|_F^2}{4 N_0}\right),$$

by the Chernoff bound $Q(x) \le e^{-x^2/2}$ for $x \ge 0$.

**Step 2 (one receive antenna).** Write $h_i$ for row $i$ of $H$, so $\|H \Delta\|_F^2 = \sum_{i=1}^{N_r} h_i \Delta \Delta^H h_i^H$. Diagonalize $\Delta \Delta^H = U \Lambda U^H$ with $U$ unitary. The vector $g = h_i U$ has i.i.d. $\mathcal{CN}(0, 1)$ entries, because the law of $h_i$ is invariant under unitary maps. Then $h_i \Delta \Delta^H h_i^H = \sum_k \lambda_k |g_k|^2$, where the $|g_k|^2$ are independent exponential variables of mean 1. For such a variable and $t \ge 0$, $\mathbb{E}\, e^{-t |g|^2} = \int_0^\infty e^{-tu} e^{-u}\, du = 1/(1 + t)$. So

$$\mathbb{E} \exp\!\left(-\frac{h_i \Delta \Delta^H h_i^H}{4 N_0}\right) = \prod_{k=1}^{r} \left(1 + \frac{\lambda_k}{4 N_0}\right)^{-1},$$

where the zero eigenvalues contribute a factor 1.

**Step 3 (all receive antennas).** The rows $h_1, \ldots, h_{N_r}$ are independent, so the expectation of the product of their exponentials is the product of the expectations, which gives the first bound. The second bound uses $1 + \lambda_k/(4N_0) \ge \lambda_k/(4N_0)$.

**Step 4 (the criteria).** The second bound is $c\, N_0^{\,r N_r}$ with $c = (4^{r} \prod_k \lambda_k)^{-N_r}$, so as $N_0 \to 0$ with the codebook scaled by $\sqrt{P}$, the pairwise error falls as $\rho^{-r N_r}$. The error probability of the code is at most the sum of the pairwise bounds over the finitely many other codewords (the [union bound](/union-bound/)), and it is at least the largest single pairwise term times the prior of $X$. So the slope is set by the smallest rank, which is the rank criterion, and the constant by the eigenvalue products of the pairs that reach this rank, which is the determinant criterion. $\blacksquare$

## Consequences

- **Worked example.** Take the [Alamouti code](/alamouti-code/) with BPSK and half the energy on each antenna: $X = \frac{1}{\sqrt2} \begin{pmatrix} s_1 & -s_2 \\ s_2 & s_1 \end{pmatrix}$. For $s = (1, 1)$ and $s' = (-1, 1)$, $\Delta = \sqrt2\, I$, so $\lambda_1 = \lambda_2 = 2$, full rank. With $N_r = 1$ and $N_0 = 0.1$ (10 dB), the first bound is $(1 + 2/0.4)^{-2} = 6^{-2} = 0.027778$ and the high-SNR form is $(2 \cdot 2)^{-1} (0.4)^2 = 0.04$. The exact pairwise error, from Step 1 averaged over the fading, is $0.0055282$: the bound has the right slope but is 5 times too large here.
- **A rank-one code.** If both antennas send the same symbol at the same time, $X = (s, s)^T$ with $T = 1$, then $\Delta = (e, e)^T$ has rank one and $\lambda_1 = 2|e|^2$. The diversity is only $N_r$: this repetition is a beam with a fixed direction, and the array is lost.
- **Orthogonal designs.** For an OSTBC, $\Delta \Delta^H = (\sum_k |e_k|^2) I$ for every pair, so the rank criterion holds for every constellation, and the coding gain is the minimum squared distance of the constellation.
- **Trellis codes.** Tarokh, Seshadri and Calderbank checked the rank of every pair of paths that diverge and remerge in a trellis, and built 4-PSK and 8-PSK [space-time trellis codes](/space-time-trellis-codes/) with full diversity and good determinants.
- **Nonvanishing determinant.** For a family of codes with growing QAM size, the [golden code](/golden-code/) keeps $\min |\det \Delta|^2$ at a constant, before normalization, as the constellation grows. This property is what makes it reach the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).
- **Many receive antennas (a heuristic).** When $r N_r$ is large, the first form of the bound is dominated by $\sum_k \lambda_k = \|\Delta\|_F^2$, and designers often maximize the minimum Euclidean distance between codewords (the trace criterion) instead of the determinant.

## Tightness

- **The constant is loose.** The Chernoff bound can be off by a factor of several, as in the example above. The slope $r N_r$ is exact: the exact pairwise error is also of order $\rho^{-r N_r}$.
- **The union bound is loose at low SNR.** The criteria describe the high-SNR behavior; at moderate SNR, the number of nearest pairs matters as much as their determinants.
- **Quasi-static fading is assumed.** In fast fading, with $H$ independent from slot to slot, Tarokh, Seshadri and Calderbank gave other criteria: the diversity is $N_r$ times the number of nonzero columns of $\Delta$, and the gain is the product of the squared column norms.
- **Rayleigh fading is assumed.** With correlated fading, the eigenvalues that matter are those of a product of $\Delta \Delta^H$ with the transmit correlation; with a strong line-of-sight part, the bound changes form.
- **ML decoding is assumed.** A suboptimal receiver, such as zero forcing, can lose diversity that the code has.
- **Fixed rate.** The criteria are for a fixed codebook as the SNR grows. For rates that grow with the SNR, the right framework is the [diversity-multiplexing tradeoff](/diversity-multiplexing-tradeoff/).

## History

Guey, Fitz, Bell and Kuo gave the rank condition for transmit diversity in 1996. Tarokh, Seshadri and Calderbank stated the rank and determinant criteria for quasi-static fading, and the corresponding criteria for fast fading, in their 1998 paper in the IEEE Transactions on Information Theory, and used them to build the first space-time trellis codes. The criteria became the standard tools for space-time code design until the diversity-multiplexing tradeoff added the requirement that the minimum determinant should not vanish as the rate grows.

## References
