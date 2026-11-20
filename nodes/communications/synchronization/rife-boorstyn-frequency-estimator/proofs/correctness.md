---
title: The ML frequency of a tone is the periodogram peak, and the coarse FFT search with golden-section refinement finds it exactly without noise
proves: [correctness]
status: full
---

The input is $r_t = b_0 e^{j\omega_0 t} + w_t$, $t = 0, \ldots, N - 1$, $N \ge 2$, with an unknown complex amplitude $b_0 = A e^{j\phi} \neq 0$, an unknown frequency $\omega_0 \in [-\pi, \pi)$, and $w_t \sim \mathcal{CN}(0, N_0)$ white. Let $X(\omega) = \sum_t r_t e^{-j\omega t}$ and $P(\omega) = |X(\omega)|^2/N$, the [periodogram](/periodogram/). Line L1 computes $X$ at the $K$ points $2\pi i/K$ with a zero-padded FFT, $K \ge 4N$ a power of two. Line L2 takes the index $i^\ast$ of the largest $|X|$. Line L3 sets the interval $[a, b] = [2\pi(i^\ast - 1)/K, 2\pi(i^\ast + 1)/K]$. Line L4 runs a golden-section search for the maximum of $P$ on $[a, b]$, and line L5 reduces the result to $[-\pi, \pi)$. Write $\Delta = 2\pi/K \le \pi/(2N)$.

**Theorem 1 (the ML estimate is the periodogram peak).** The maximum likelihood estimate of $\omega_0$, with $b_0$ unknown, is any maximizer of $P$ over $[-\pi, \pi)$.

*Proof.* The log-likelihood is $-\frac{1}{N_0}\sum_t |r_t - b e^{j\omega t}|^2$ plus a constant. For a fixed $\omega$, this is a least squares problem in $b$, with the solution $\hat b(\omega) = X(\omega)/N$, since the vector $(e^{j\omega t})_t$ has squared norm $N$. The minimum is $\sum_t |r_t|^2 - |X(\omega)|^2/N$. So maximizing the likelihood over $(b, \omega)$ is the same as maximizing $|X(\omega)|^2/N = P(\omega)$ over $\omega$, and $\hat b = X(\hat\omega)/N$. $\square$

**Lemma 2 (the Dirichlet kernel).** Let $D(x) = \frac{\sin(Nx/2)}{\sin(x/2)}$, with $D(0) = N$. Then $|D|$ is strictly decreasing on $[0, 2\pi/N]$, and $|D(x)| \le N/2$ for $2\pi/N \le |x| \le \pi$.

*Proof.* With $c = (N-1)/2$, $D(x) = \sum_{t=0}^{N-1} \cos((t - c)x)$, and $D'(x) = -\sum_t (t - c)\sin((t-c)x)$. For $0 < x \le 2\pi/N < 2\pi/(N-1)$, every $|t - c|\,x$ is at most $c \cdot 2\pi/(N-1) = \pi$, so each term $(t-c)\sin((t-c)x) \ge 0$, and the terms with $|t - c| = c$ are positive. Hence $D$ is strictly decreasing on $[0, 2\pi/N]$, from $N$ to $0$, and $D \ge 0$ there. For $2\pi/N \le |x| \le \pi$, $|\sin(x/2)| \ge \sin(\pi/N) \ge \frac{2}{\pi}\cdot\frac{\pi}{N} = \frac2N$, so $|D(x)| \le N/2$. $\square$

**Theorem 2 (exact without noise).** If $w_t = 0$, the algorithm returns $\omega_0$ to within the tolerance of the golden-section search.

*Proof.* Without noise, $|X(\omega)| = |b_0|\,|D(\omega - \omega_0)|$ with the difference taken modulo $2\pi$, so $P$ has its unique maximum at $\omega_0$. Let $g$ be the grid point nearest to $\omega_0$; $|g - \omega_0| \le \Delta/2 \le \pi/(4N)$. By Lemma 2, $|D(g - \omega_0)| \ge D(\pi/(4N)) = \frac{\sin(\pi/8)}{\sin(\pi/(8N))} \ge \frac{8N\sin(\pi/8)}{\pi} > 0.97N$, which is larger than every value outside the main lobe $|x| < 2\pi/N$. Inside the main lobe, $|D|$ decreases with $|x|$, so no other grid point has a larger value. So line L2 picks $g$, up to ties that only occur at equal distance and change nothing below. The interval of line L3 is $[g - \Delta, g + \Delta]$, which contains $\omega_0$, and every point of it is within $\frac32\Delta \le \frac{3\pi}{4N} < \frac{2\pi}{N}$ of $\omega_0$. On it, $P(\omega) = \frac{|b_0|^2}{N} D(\omega - \omega_0)^2$ is strictly increasing up to $\omega_0$ and strictly decreasing after it, so it is unimodal. Golden-section search on a unimodal function keeps the maximizer in its bracket and shrinks the bracket by the factor $0.618$ per step, so it returns $\omega_0$ to within the tolerance. $\square$

**Theorem 3 (with noise).** The algorithm returns the global maximizer of $P$, that is the ML estimate, whenever (a) the global maximizer lies within $\Delta$ of the grid point with the largest value and (b) $P$ is unimodal on that interval. Without these conditions it returns a local maximum of $P$ on the interval.

*Proof.* Under (b), the golden-section search converges to the maximizer of $P$ on $[a, b]$; under (a), that is the global maximizer. Without them, golden-section search still returns a point of its last bracket, where $P$ has a local maximum or a bracket end. $\square$

Conditions (a) and (b) hold at high SNR, because $P$ is then close to the noise-free case of Theorem 2, plus a small perturbation; they are a rule, not a theorem, at moderate SNR, and the tests check against a dense brute-force grid that the estimate is the global peak. The variance of the ML estimate tends to the [Cramer-Rao bound](/cramer-rao-bound/) $\frac{6}{\mathrm{SNR}\,N(N^2-1)}$ as the SNR grows. That is a closed form under assumptions (asymptotic efficiency of ML above threshold), shown by Rife and Boorstyn and measured in the tests. Below a threshold in $N \cdot \mathrm{SNR}$, a noise peak elsewhere is higher than the signal peak with a noticeable probability, and the estimate is an outlier anywhere in $[-\pi, \pi)$.

**Complexity.** Line L1 is an FFT of $K = O(N)$ points, $O(N \log N)$. Line L2 is $O(N)$. Line L4 needs $O(\log(\Delta/\mathrm{tol}))$ evaluations of $P$, each $O(N)$. The total is $O(N\log N + N\log(1/(N\,\mathrm{tol})))$ time and $O(N)$ space.
