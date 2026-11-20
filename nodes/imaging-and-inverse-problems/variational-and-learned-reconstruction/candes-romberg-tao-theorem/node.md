---
tag: 9B045G
kind: theorem
slug: candes-romberg-tao-theorem
name: Candes-Romberg-Tao theorem
aliases:
- robust uncertainty principle
area: imaging-and-inverse-problems/variational-and-learned-reconstruction
level: advanced
summary: An s-sparse signal is recovered exactly by L1 minimization from about s log n random Fourier samples with high probability.
prereqs: [discrete-fourier-transform, basis-pursuit, compressed-sensing]
see_also: [null-space-property, restricted-isometry-property, mutual-coherence, donoho-tanner-phase-transition, compressed-sensing-mri, total-variation-denoising, single-pixel-camera, sparse-signal-recovery]
sources:
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candes, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: pages 489 to 509; Theorem 1.1 (N prime, uniqueness for |T| at most |Omega|/2, and its converse), Theorem 1.3 (Bernoulli sampling of frequencies, exact recovery by l1 minimization with probability 1 - O(N^-M)), Corollary 1.4 (total variation), the Dirac comb in Section 1.3, the dual polynomial of Section 2 and the numerical experiments of Section 5
  - paper: doi:10.4310/mrl.2005.v12.n1.a11
    title: Terence Tao, An uncertainty principle for cyclic groups of prime order, Mathematical Research Letters 12(1), 2005
    locator: pages 121 to 127 (for N prime, a nonzero f has |supp f| + |supp of its DFT| at least N + 1)
  - paper: doi:10.1137/0149053
    title: David L. Donoho and Philip B. Stark, Uncertainty principles and signal recovery, SIAM Journal on Applied Mathematics 49(3), 1989
    locator: pages 906 to 931 (the discrete uncertainty principle |supp f| times |supp of its DFT| at least N, and recovery of sparse signals from partial Fourier data)
  - paper: doi:10.1109/TIT.2006.871582
    title: David L. Donoho, Compressed sensing, IEEE Transactions on Information Theory 52(4), 2006
    locator: pages 1289 to 1306 (the companion result for random measurement matrices)
  - paper: doi:10.1016/j.crma.2008.03.014
    title: Emmanuel J. Candes, The restricted isometry property and its implications for compressed sensing, Comptes Rendus Mathematique 346(9-10), 2008
    locator: pages 589 to 592 (uniform and stable recovery from the restricted isometry property)
---

The Candes-Romberg-Tao theorem says that a signal of length $N$ with $|T|$ nonzero entries is recovered exactly by $\ell_1$ minimization, [basis pursuit](/basis-pursuit/), from its [discrete Fourier transform](/discrete-fourier-transform/) at a random set $\Omega$ of frequencies, with probability at least $1 - O(N^{-M})$, when $|T|$ is at most a constant times $|\Omega|/\log N$. It is one of the two papers that started [compressed sensing](/compressed-sensing/), and the source of [compressed sensing MRI](/compressed-sensing-mri/). It is a nonuniform result: the signal is fixed first, and the random frequencies then recover it. The [null space property](/null-space-property/) is the condition for recovery of all sparse signals at once, the [restricted isometry property](/restricted-isometry-property/) gives that uniform recovery with stability, and the [Donoho-Tanner phase transition](/donoho-tanner-phase-transition/) gives the exact constant for Gaussian matrices. This page states the theorem for Fourier samples and proves its deterministic core.

## Statement

Let $N \ge 2$ and identify signals $f \in \mathbb{C}^N$ with functions on $\{0, 1, \dots, N - 1\}$. The discrete Fourier transform is $\hat f(\omega) = \sum_{t=0}^{N-1} f(t)e^{-2\pi i\omega t/N}$. For a set $\Omega$ of frequencies, consider

$$(P_1)\qquad \min_{g \in \mathbb{C}^N}\|g\|_1 \quad\text{subject to}\quad \hat g(\omega) = \hat f(\omega) \text{ for all } \omega \in \Omega.$$

**Theorem (Candes, Romberg and Tao 2006, Theorem 1.3).** Fix $M > 0$ and $0 < \tau < 1$. Let $\Omega$ be a random set of frequencies that contains each $k \in \{0, \dots, N - 1\}$ independently with probability $\tau$, so that $\mathbb{E}|\Omega| = \tau N$. Let $f \in \mathbb{C}^N$ be supported on a set $T$, chosen independently of $\Omega$. If

$$|T| \le \alpha(M)\,\frac{\tau N}{\log N},$$

then with probability at least $1 - O(N^{-M})$ over the choice of $\Omega$, $f$ is the unique solution of $(P_1)$. The constant $\alpha(M)$ is explicit; the paper gives $\alpha(M) \asymp 1/[29.6(M + 1)]$ and does not try to optimize it.

The probability is over $\Omega$ only. The signal $f$, with its support and its phases, can be arbitrary, but it must not depend on $\Omega$. Since $|\Omega|$ is binomial, it is close to $\tau N$ with high probability, so the condition says that $|T|$ is at most a constant times $|\Omega|/\log N$. The paper also states the same result in two dimensions (Theorem 1.5).

**Theorem (Candes, Romberg and Tao 2006, Theorem 1.1).** Let $N$ be prime, let $\Omega$ be any set of frequencies, and let $f$ be supported on $T$ with $|T| \le \tfrac12|\Omega|$. Then $f$ is the only signal with at most $\tfrac12|\Omega|$ nonzero entries whose Fourier transform agrees with $\hat f$ on $\Omega$. Conversely, if $\Omega$ is not the set of all frequencies, there are two different signals with at most $\tfrac12|\Omega| + 1$ nonzero entries each and the same samples on $\Omega$.

Theorem 1.1 is deterministic, but it only says that the sparsest solution is unique. Finding it by search over supports takes exponential time. Theorem 1.3 gives a solution by a convex program, a linear program for real signals and a second-order cone program for complex ones, at the price of a random $\Omega$ and a $\log N$ factor.

## In plain words

Take a long signal that is zero almost everywhere, with a few spikes. Measure only a few of its frequencies, picked at random. Among all signals that agree with these measurements, choose the one with the smallest sum of absolute values. With very high probability, this choice is exactly the original signal. The number of frequencies needed is a little more than the number of spikes: a constant times the number of spikes times the logarithm of the length. The randomness of the frequencies is necessary. A bad choice of frequencies can miss a signal completely.

## Proof

The proof has a deterministic part, a dual certificate that makes $f$ the unique solution, and a probabilistic part, which shows that a random $\Omega$ admits such a certificate. The deterministic part is short and is proved here in full. For the probabilistic part this page gives the construction and cites the estimate.

Write $F_{\Omega T}$ for the matrix with entries $e^{-2\pi i\omega t/N}$, $\omega \in \Omega$, $t \in T$. It maps a signal supported on $T$ to its samples on $\Omega$. Let $\operatorname{sgn} f(t) = f(t)/|f(t)|$ for $t \in T$. Use $\langle u, v\rangle = \sum_t u(t)\overline{v(t)}$.

**Lemma (dual certificate, Section 2 of the paper).** Suppose that $F_{\Omega T}$ is injective, and that there is a $P \in \mathbb{C}^N$ such that $\hat P$ is zero outside $\Omega$, $P(t) = \operatorname{sgn} f(t)$ for $t \in T$, and $|P(t)| < 1$ for $t \notin T$. Then $f$ is the unique solution of $(P_1)$.

*Proof.* Let $g$ be feasible and let $h = g - f$. Then $\hat h(\omega) = 0$ for $\omega \in \Omega$, and $\hat P(\omega) = 0$ for $\omega \notin \Omega$, so by Parseval's identity

$$\langle h, P\rangle = \frac1N\sum_{\omega}\hat h(\omega)\overline{\hat P(\omega)} = 0.$$

For $t \in T$, $|f(t) + h(t)| \ge \operatorname{Re}\big(\overline{P(t)}(f(t) + h(t))\big) = |f(t)| + \operatorname{Re}\big(\overline{P(t)}h(t)\big)$, because $|P(t)| = 1$ and $\overline{P(t)}f(t) = |f(t)|$. For $t \notin T$, $|h(t)| \ge |P(t)||h(t)| \ge \operatorname{Re}\big(\overline{P(t)}h(t)\big)$, and the first inequality is strict when $h(t) \ne 0$. Add over all $t$:

$$\|g\|_1 = \sum_{t \in T}|f(t) + h(t)| + \sum_{t \notin T}|h(t)| \ge \|f\|_1 + \operatorname{Re}\langle h, P\rangle = \|f\|_1.$$

So $f$ is a solution. If $\|g\|_1 = \|f\|_1$, the strict inequality forces $h(t) = 0$ for all $t \notin T$. Then $h$ is supported on $T$ and $F_{\Omega T}h_T = 0$, so $h = 0$ by injectivity. $\square$

**The construction.** If $F_{\Omega T}$ is injective, the signal

$$P = F_\Omega^H\,F_{\Omega T}\big(F_{\Omega T}^HF_{\Omega T}\big)^{-1}\operatorname{sgn} f,$$

where $F_\Omega^H$ maps samples on $\Omega$ back to a signal on all of $\{0, \dots, N - 1\}$, has its Fourier transform supported on $\Omega$, and $P(t) = \operatorname{sgn} f(t)$ on $T$ by construction. It is the interpolant of least energy. The main work of the paper shows that for a random $\Omega$ with $|T| \le \alpha(M)|\Omega|/\log N$, the matrix $F_{\Omega T}^HF_{\Omega T}$ is close to $|\Omega|I$ and $|P(t)| < 1$ for every $t \notin T$, both with probability $1 - O(N^{-M})$. The authors expand the inverse in a Neumann series and bound high moments of the random terms by a combinatorial count. This page does not repeat that estimate.

**Proof of Theorem 1.1 from Tao's uncertainty principle.** Tao (2005) proved that for $N$ prime, every nonzero $h \in \mathbb{C}^N$ satisfies $|\operatorname{supp} h| + |\operatorname{supp}\hat h| \ge N + 1$. Let $f$ and $g$ both have at most $\tfrac12|\Omega|$ nonzero entries and the same samples on $\Omega$, and let $h = f - g$. Then $|\operatorname{supp} h| \le |\Omega|$, and $\hat h$ vanishes on $\Omega$, so $|\operatorname{supp}\hat h| \le N - |\Omega|$. The sum is at most $N$, so $h = 0$. $\square$

## Consequences

**Example: one spike.** Let $f = c\,e_0$ with $c \ne 0$, so $T = \{0\}$ and $\hat f(\omega) = c$ for all $\omega$. The signal $P(t) = \frac{\operatorname{sgn} c}{|\Omega|}\sum_{\omega \in \Omega}e^{2\pi i\omega t/N}$ has $\hat P$ supported on $\Omega$ and $P(0) = \operatorname{sgn} c$. For $t \ne 0$, $|P(t)| < 1$ unless all the numbers $e^{2\pi i\omega t/N}$, $\omega \in \Omega$, are equal. If $\Omega$ contains two frequencies whose difference is coprime to $N$, that cannot happen, and the lemma shows that $(P_1)$ returns $f$. If not, recovery can fail: for $N = 4$ and $\Omega = \{1, 3\}$, the signals $e_0$ and $-e_2$ both have the samples $(1, 1)$ and the same $\ell_1$ norm.

**Fourier imaging.** The theorem justifies sampling in the Fourier domain below the Nyquist rate and solving a convex program. The same paper derives a version for piecewise constant signals and total variation minimization (Corollary 1.4), and it opens with an experiment in which the Shepp-Logan phantom is recovered exactly by total variation minimization from Fourier samples on 22 approximately radial lines. That experiment is the start of [compressed sensing MRI](/compressed-sensing-mri/); see also [total variation denoising](/total-variation-denoising/).

**Incoherent sampling.** The proof uses two facts about the Fourier basis: all its entries have the same absolute value, and the spike basis is maximally incoherent with it in the sense of [mutual coherence](/mutual-coherence/). Later work by Candes and Romberg extended the result to sampling in one orthonormal basis a signal that is sparse in another, with the number of samples multiplied by the squared coherence between the two bases.

**Uniform and stable recovery.** Theorem 1.3 covers one signal per draw of $\Omega$, and it has no noise. Candes and Tao, and later Rudelson and Vershynin, proved the restricted isometry property for random rows of the DFT with a few more logarithmic factors. One random $\Omega$ then recovers all $s$-sparse signals at once, and the error stays bounded by the noise level. Candes (2008) gives the short form of that argument.

**Measurement (from the paper).** The numerical experiments of the paper found recovery in more than 50 percent of the trials when $|T| \le |\Omega|/4$, and in more than 90 percent when $|T| \le |\Omega|/8$. These are measurements, not part of the theorem. They show that the constant $\alpha(M)$ in the statement is far from what happens in practice.

## Tightness

**The logarithm is needed.** Let $N = k^2$ and let $f$ be the Dirac comb $f(t) = 1$ when $k$ divides $t$, so $|T| = k = \sqrt N$. Its transform is $\hat f(\omega) = k$ when $k$ divides $\omega$ and 0 otherwise, again a comb with $\sqrt N$ teeth. If $\Omega$ misses those $\sqrt N$ frequencies, every sample of $f$ is 0 and no method can tell $f$ from the zero signal. When each frequency is in $\Omega$ independently with probability $\tau = |\Omega|/N$, this happens with probability $(1 - \tau)^{\sqrt N} \approx e^{-\tau\sqrt N}$. For this to be at most $N^{-M}$ one needs $\tau\sqrt N \ge M\log N$, that is $|\Omega| \ge M|T|\log N$. So a bound of the form $|T| \le \alpha|\Omega|/\log N$ is the right shape for a failure probability of $N^{-M}$.

Check it by hand for $N = 4$: the comb $(1, 0, 1, 0)$ has transform $(2, 0, 2, 0)$, so the samples at $\Omega = \{1, 3\}$ are zero.

**The prime hypothesis of Theorem 1.1 is needed.** For $N = 9$ the comb $(1, 0, 0, 1, 0, 0, 1, 0, 0)$ has 3 nonzero entries and its transform is 3 at $\omega \in \{0, 3, 6\}$ and 0 elsewhere. Let $\Omega$ be the other 6 frequencies. Then $|T| = 3 = \tfrac12|\Omega|$, but the comb and the zero signal have the same samples on $\Omega$. For composite $N$ the subgroups of $\mathbb{Z}_N$ give such combs, and Tao's bound $N + 1$ fails.

**The converse in Theorem 1.1.** Its second part shows that $\tfrac12|\Omega|$ cannot be raised by more than 1 for uniqueness, even for prime $N$. Theorem 1.3 gives up uniqueness among all sparse signals with the same samples and asks only that a fixed signal be the $\ell_1$ minimizer, which a random $\Omega$ allows.

**Random against worst case sampling.** The theorem says nothing about a fixed, structured $\Omega$, for example the lowest frequencies. The comb shows that some $\Omega$ of size $N - \sqrt N$ miss a $\sqrt N$-sparse signal.

## History

Donoho and Stark (1989) proved the discrete uncertainty principle $|\operatorname{supp} f|\cdot|\operatorname{supp}\hat f| \ge N$ and used it to recover sparse signals from partial Fourier data, with the Dirac comb as the extreme case. Donoho and Huo (2001) proved exact recovery by $\ell_1$ minimization in a pair of bases under a coherence condition, which gives sparsity of order $\sqrt N$. Tao (2005) proved the sharp bound $N + 1$ for prime $N$. Candes, Romberg and Tao put the paper on arXiv in 2004 (math/0409186) and published it in 2006. They replaced the worst case over $\Omega$ by a random $\Omega$ and gained sparsity of order $|\Omega|/\log N$. Donoho's paper "Compressed sensing" (2006) proved a related result for random measurement matrices, and the two papers together started the field.

## References
