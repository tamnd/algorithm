---
tag: K1F6Z3
kind: theorem
slug: diversity-multiplexing-tradeoff
name: Diversity-multiplexing tradeoff
aliases:
- Zheng-Tse tradeoff
area: communications/mimo-communications
level: advanced
summary: For a slow fading MIMO channel at high SNR, the best diversity at multiplexing gain r is a piecewise linear function found by Zheng and Tse.
prereqs: [mimo-capacity, spatial-multiplexing, outage-probability, diversity-order]
see_also: [alamouti-code, golden-code, rank-and-determinant-criteria, d-blast, v-blast, outage-capacity, mimo-channel-model, rayleigh-fading-channel]
sources:
  - paper: doi:10.1109/TIT.2003.810646
    title: "Lizhong Zheng and David N. C. Tse, Diversity and multiplexing - a fundamental tradeoff in multiple-antenna channels, IEEE Transactions on Information Theory 49(5), 1073-1096, 2003"
    locator: "the definitions of multiplexing and diversity gain, the main theorem for block length at least m + n - 1, the outage lower bound and the error analysis of Gaussian codes, and the comparison of the Alamouti code and V-BLAST with the optimal curve"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "Section 9.1 (the diversity-multiplexing tradeoff, with the nt by nr i.i.d. Rayleigh channel in Section 9.1.6) and Section 9.2 (universal code design)"
  - book: isbn:9780521826150
    title: "Arogyaswami Paulraj, Rohit Nabar and Dhananjay Gore, Introduction to Space-Time Wireless Communications, Cambridge University Press, 2003"
    locator: "Chapter 12, Performance limits and tradeoffs in MIMO channels"
---

The diversity-multiplexing tradeoff (DMT) of Zheng and Tse says how fast the error probability of a slow fading MIMO link can fall when the rate also grows with the SNR. A scheme with multiplexing gain $r$ sends about $r \log_2 \rho$ bits per use, and its diversity gain $d$ is the slope of its error probability on a log-log plot. For an $N_t \times N_r$ i.i.d. Rayleigh channel, the best pairs $(r, d)$ form the piecewise linear curve through the points $(k, (N_t - k)(N_r - k))$. It joins the two extremes of the MIMO channel: full diversity $N_t N_r$ at a fixed rate, and the full [spatial multiplexing](/spatial-multiplexing/) slope $\min(N_t, N_r)$ of the [MIMO capacity](/mimo-capacity/). The $d(r)$ here is a function of the rate and is not the [diversity order](/diversity-order/) of one fixed scheme, though the two agree at $r = 0$.

## Statement

A **scheme** is a family of codes $\mathcal{C}(\rho)$, one for each SNR $\rho$, with block length $l$ and rate $R(\rho)$ bits per use, used over the [MIMO channel](/mimo-channel-model/) $y = Hx + w$ with $\mathbb{E}\,\mathrm{tr}(X X^H) \le l P$ for each codeword $X$. The scheme has **multiplexing gain** $r$ and **diversity gain** $d$ if

$$\lim_{\rho \to \infty} \frac{R(\rho)}{\log_2 \rho} = r, \qquad \lim_{\rho \to \infty} \frac{\log P_e(\rho)}{\log \rho} = -d,$$

where $P_e$ is the average error probability. Write $f \doteq \rho^{-d}$ for $\lim \log f / \log \rho = -d$.

**Theorem (Zheng and Tse, 2003).** Let $H$ have i.i.d. $\mathcal{CN}(0, 1)$ entries, stay fixed for the whole block (quasi-static fading), and be known at the receiver only. Let $l \ge N_t + N_r - 1$. Then the largest diversity gain at multiplexing gain $r$ is the function $d^*(r)$ that is linear between the points

$$\big(k,\ (N_t - k)(N_r - k)\big), \qquad k = 0, 1, \ldots, \min(N_t, N_r),$$

and $d^*(r) = 0$ for $r \ge \min(N_t, N_r)$. The curve equals the outage exponent: $P_{\text{out}}(r \log_2 \rho) \doteq \rho^{-d^*(r)}$, where $P_{\text{out}}(R) = \Pr[\log_2 \det(I + (\rho/N_t) H H^H) < R]$.

## In plain words

A link with several antennas can use them in two ways. It can send the same data over many paths, so that a message is lost only when all paths fade at once. Or it can send different data on each path to go faster.

The tradeoff says that you cannot have both in full. If you ask for more speed, and the speed keeps growing as the signal gets stronger, you must accept errors that fall more slowly. Zheng and Tse found the exact best balance for a channel that does not change during a message. The best balance is a broken line: at one end, no extra speed and the most protection; at the other end, the most speed and no protection. Each extra unit of speed costs fewer units of protection as the speed grows.

## Proof

**The scalar case in full.** Take $N_t = N_r = 1$, so $H = h \sim \mathcal{CN}(0, 1)$ and $|h|^2$ is exponential with mean 1. The claim is $d^*(r) = 1 - r$ for $0 \le r \le 1$.

*Outage.* $P_{\text{out}} = \Pr[\log_2(1 + \rho |h|^2) < r \log_2 \rho] = \Pr[|h|^2 < (\rho^r - 1)/\rho] = 1 - e^{-(\rho^r - 1)/\rho}$. For $r < 1$, this is $(\rho^r - 1)/\rho\,(1 + o(1)) \doteq \rho^{-(1 - r)}$.

*Converse.* Fix any scheme with multiplexing gain $r$ and a small $\epsilon > 0$, and condition on $h$. With messages chosen uniformly, Fano's inequality and the power limit give

$$P_e(h) \ge 1 - \frac{l \log_2(1 + \rho |h|^2) + 1}{l R(\rho)}.$$

On the event $E = \{\log_2(1 + \rho |h|^2) \le (r - \epsilon) \log_2 \rho\}$, and for $\rho$ large enough that $R(\rho) \ge (r - \epsilon/2) \log_2 \rho$, the right side is at least $1 - (r - \epsilon)/(r - \epsilon/2) - o(1)$, a positive constant. By the outage computation, $\Pr[E] \doteq \rho^{-(1 - r + \epsilon)}$. So $P_e \ge \Pr[E] \cdot \text{const}$, which gives $d \le 1 - r + \epsilon$ for every $\epsilon > 0$, so $d \le 1 - r$.

*Achievability with QAM.* Send one square QAM symbol per use with unit average energy, where $M$ is the largest power of 4 that is at most $\rho^r$. Then $R(\rho) = \log_2 M \ge r \log_2 \rho - 2$, and the minimum distance satisfies $d_{\min}^2 = 6/(M - 1) \ge 6 \rho^{-r}$. Given $h$, the minimum distance detector makes a symbol error only if the in-phase or the quadrature slicer errs, and each of these errs with probability at most $2Q$ of half the scaled distance over the noise deviation. With $Q(x) \le e^{-x^2/2}$,

$$P_e(h) \le 4\, Q\!\left(\sqrt{\rho |h|^2 d_{\min}^2 / 2}\right) \le 4 \exp\!\left(-\rho |h|^2 d_{\min}^2 / 4\right).$$

Averaging over the exponential $|h|^2$ gives $\mathbb{E}\, e^{-t |h|^2} = 1/(1 + t)$ with $t = \rho d_{\min}^2 / 4 \ge 1.5 \rho^{1 - r}$, so $P_e \le \rho^{-(1 - r) + o(1)}$ and $d \ge 1 - r$. $\square$

**The general case (outline of Zheng and Tse).** Let $m = \min(N_t, N_r)$, $n = \max(N_t, N_r)$, and let $\lambda_1 \le \cdots \le \lambda_m$ be the nonzero eigenvalues of $H H^H$. Write $\lambda_i = \rho^{-\alpha_i}$.

1. *Outage in terms of $\alpha$.* $\log_2 \det(I + (\rho/N_t) H H^H) = \sum_i \log_2(1 + \rho \lambda_i / N_t) \approx \log_2 \rho \sum_i (1 - \alpha_i)^+$. So outage at rate $r \log_2 \rho$ is, to first order in the exponent, the event $\sum_i (1 - \alpha_i)^+ < r$.
2. *The law of $\alpha$.* With the eigenvalues in increasing order, $\alpha_1 \ge \cdots \ge \alpha_m$. From the joint density of the eigenvalues of a complex Wishart matrix, the density of $\alpha$ is $\doteq \rho^{-\sum_i (2i - 1 + n - m) \alpha_i}$ on $\alpha_1 \ge \cdots \ge \alpha_m \ge 0$. Laplace's method gives

$$P_{\text{out}}(r \log_2 \rho) \doteq \rho^{-d_{\text{out}}(r)}, \qquad d_{\text{out}}(r) = \min_{\alpha \ge 0,\ \sum_i (1 - \alpha_i)^+ \le r}\ \sum_{i=1}^{m} (2i - 1 + n - m)\, \alpha_i.$$

   For an integer $r = k$, at least $m - k$ of the $\alpha_i$ must be at least 1, and the weights grow with $i$. So the minimizer puts $\alpha_i = 1$ on the $m - k$ smallest eigenvalues, $i = 1, \ldots, m - k$, which have the smallest weights, and $\alpha_i = 0$ on the rest. This gives $\sum_{i=1}^{m-k} (2i - 1 + n - m) = (m - k)^2 + (m - k)(n - m) = (m - k)(n - k)$. Between integers the minimum is linear.
3. *Converse.* As in the scalar case, Fano's inequality shows that any scheme has $P_e \ge P_{\text{out}}(R) \cdot \text{const}$ in the exponent, so $d \le d_{\text{out}}(r)$.
4. *Achievability.* For a Gaussian random code of length $l$, the error probability is at most $P_{\text{out}}$ plus the probability of an error outside outage. Zheng and Tse bound the second term with a union bound over codewords, given $\alpha$, and show that its exponent is at least $d_{\text{out}}(r)$ when $l \ge N_t + N_r - 1$.

The details of steps 2 and 4 are in Zheng and Tse (2003) and in Tse and Viswanath, Section 9.1.6. $\blacksquare$

## Consequences

- **The $2 \times 2$ channel.** The corner points are $(0, 4)$, $(1, 1)$ and $(2, 0)$, so $d^*(r) = 4 - 3r$ on $[0, 1]$ and $2 - r$ on $[1, 2]$.
- **Alamouti is optimal only at $r = 0$ on $2 \times 2$.** The [Alamouti code](/alamouti-code/) turns the channel into a scalar channel with gain $\|H\|_F^2$, a sum of 4 exponential variables, and sends one symbol per use. Its curve is $4(1 - r)$ for $0 \le r \le 1$. It meets $d^*$ at $r = 0$ and lies below it for $r > 0$; at $r = 1$ it gives 0 while $d^*(1) = 1$. On the $2 \times 1$ channel, $d^*(r) = 2(1 - r)$, and the Alamouti code is optimal.
- **V-BLAST with zero forcing.** Each of the $N_t$ streams sees diversity $N_r - N_t + 1$ and carries rate $r/N_t$, so the curve is $(N_r - N_t + 1)(1 - r/N_t)$. On $2 \times 2$, this is $1 - r/2$, far below $d^*$ at small $r$.
- **Repetition.** Sending each symbol from one antenna at a time over $N_t$ slots gives $N_t N_r (1 - N_t r)$: full diversity at $r = 0$ but a maximum rate of $1/N_t$.
- **Codes that reach the curve.** The [golden code](/golden-code/) reaches $d^*$ on $2 \times 2$. More generally, codes from cyclic division algebras with a nonvanishing determinant reach it with block length $N_t$, and D-BLAST with MMSE-SIC reaches it if the error at the start and end of the frame is ignored.
- **Design rule.** For $r = 0$ the theorem gives back the classical maximal diversity $N_t N_r$ of a fixed-rate code, which the [rank criterion](/rank-and-determinant-criteria/) gives for coded schemes.

## Tightness

- **Block length.** The proof needs $l \ge N_t + N_r - 1$. Zheng and Tse gave bounds for shorter blocks. Later work, by Elia and coauthors in 2006 with explicit codes from cyclic division algebras, showed that $l = N_t$ is enough to reach the outage curve.
- **Fading law.** The corner points use the i.i.d. Rayleigh law. Correlated, Rician or keyhole channels have other curves; for the keyhole channel the curve is that of a channel with a single degree of freedom.
- **Quasi-static fading.** In fast fading, a code can average over many channel states, and the error probability can fall faster than any power of $\rho$ at rates below the ergodic capacity, so the tradeoff in this form does not apply.
- **High SNR only.** The theorem is a statement about exponents. At a fixed SNR, a scheme with a worse curve can have the lower error rate, and the constants hidden in $\doteq$ can be large.
- **CSIT.** With channel knowledge at the transmitter and power control over many blocks, the outage can be removed in some settings, and the curve changes.

## History

Lizhong Zheng and David Tse posed and solved the problem in their 2003 paper in the IEEE Transactions on Information Theory, after the earlier view in which a space-time code was designed either for maximal diversity at a fixed rate, by the rank criterion of Tarokh, Seshadri and Calderbank, or for maximal rate, by V-BLAST. Their framework became the standard way to compare space-time codes, and it led to the search for codes that achieve the curve, among them the golden code and the perfect space-time codes.

## References
