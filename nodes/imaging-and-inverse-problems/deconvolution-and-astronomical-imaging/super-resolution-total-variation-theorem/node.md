---
tag: ZVQWAE
kind: theorem
slug: super-resolution-total-variation-theorem
name: Exact super-resolution by total variation minimization
aliases:
- Candes-Fernandez-Granda theorem
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: research
summary: "For f_c of at least 128, spikes on the circle at least 2 over f_c apart are the unique measure of least total variation norm with their Fourier coefficients up to f_c."
model: real-ram
prereqs: [beurling-lasso, discrete-fourier-transform, lagrangian-duality, hermite-interpolation]
see_also: [beurling-lasso, super-resolution, compressed-sensing, basis-pursuit, semidefinite-programming, prony-method, rayleigh-criterion, single-molecule-localization]
sources:
  - paper: doi:10.1002/cpa.21455
    title: "Emmanuel J. Candes and Carlos Fernandez-Granda, Towards a mathematical theory of super-resolution, Communications on Pure and Applied Mathematics 67(6), 2014, 906 to 956"
    locator: "Theorem 1.2 (one dimension, separation 2 over f_c), Section 2.5 (real amplitudes, 1.87 over f_c), Theorem 1.3 (two dimensions, 2.38 over f_c) and Section 4 (the semidefinite program)"
  - paper: doi:10.1093/imaiai/iaw005
    title: "Carlos Fernandez-Granda, Super-resolution of point sources via convex programming, Information and Inference 5(3), 2016, 251 to 303"
    locator: "Theorem 2.2, exact recovery at the separation 1.26 over f_c for f_c of at least 1000"
  - paper: doi:10.1016/j.jmaa.2012.05.011
    title: "Yohann de Castro and Fabrice Gamboa, Exact reconstruction using Beurling minimal extrapolation, Journal of Mathematical Analysis and Applications, 2012"
    locator: exact recovery of nonnegative sparse measures with no separation condition
  - paper: doi:10.1007/s10208-014-9228-6
    title: "Vincent Duval and Gabriel Peyre, Exact support recovery for sparse spikes deconvolution, Foundations of Computational Mathematics, 2015"
    locator: the nondegenerate dual certificate and the stability of the support under small noise
---

## Statement

Let $x = \sum_{j} a_j\delta_{t_j}$ be a finite sum of spikes on the torus $\mathbb T = [0, 1)$ with complex amplitudes $a_j \ne 0$ and the support $T = \{t_j\}$. Its Fourier coefficients up to the cutoff frequency $f_c$ are

$$y_k = \int_{\mathbb T} e^{-2\pi ikt}\,dx(t) = \sum_j a_j e^{-2\pi ikt_j}, \qquad |k| \le f_c.$$

Write $\Delta(T) = \min_{j \ne l}|t_j - t_l|$ for the minimum separation, with the distance measured around the circle.

**Theorem (Candes and Fernandez-Granda 2014, Theorem 1.2).** If $f_c \ge 128$ and $\Delta(T) \ge 2/f_c$, then $x$ is the unique solution of

$$\min_{\tilde x \in \mathcal M(\mathbb T)} \lVert\tilde x\rVert_{TV} \quad\text{subject to}\quad \int e^{-2\pi ikt}\,d\tilde x(t) = y_k \ \text{ for } |k| \le f_c,$$

the minimum over all complex Radon measures on the circle.

**Refinements.**

- For real amplitudes the separation $1.87/f_c$ is enough (Candes and Fernandez-Granda 2014, Section 2.5).
- Fernandez-Granda (2016, Theorem 2.2) lowers the separation to $1.26/f_c$ for $f_c \ge 10^3$.
- In two dimensions, for spikes on the torus $\mathbb T^2$ with the coefficients $\lVert k\rVert_\infty \le f_c$, the separation $2.38/f_c$ in the max norm is enough (Candes and Fernandez-Granda 2014, Theorem 1.3).

The minimization is the noiseless [Beurling LASSO](/beurling-lasso/). Its dual is a finite semidefinite program (Section 4 of the 2014 paper), so the theorem gives a polynomial time algorithm that recovers $x$ exactly.

## In plain words

You see a set of point sources only through a low-pass filter: the $2f_c + 1$ lowest Fourier coefficients. The sources can be anywhere on a continuum of positions, so there are infinitely many sets of sources that fit the data. Among all of them, take the one with the smallest total absolute amplitude. The theorem says that this choice is exactly the truth whenever the sources are at least about two filter widths $1/f_c$ apart. No grid is needed, and the positions come out exact, not just to within a pixel. If the sources are closer, the smallest-amplitude fit can be a different set of sources.

## Proof

The proof has two parts. The first, a short duality argument, shows that a certain interpolating trigonometric polynomial, a dual certificate, forces uniqueness. The second shows that such a polynomial exists when the spikes are separated. This page proves the first part in full and outlines the second, whose estimates are long.

**Lemma 1 (dual certificate).** Suppose there is a trigonometric polynomial $q(t) = \sum_{|k| \le f_c} c_k e^{2\pi ikt}$ with

$$q(t_j) = \frac{a_j}{|a_j|} \ \text{ for every } t_j \in T, \qquad |q(t)| < 1 \ \text{ for } t \notin T,$$

and $|T| \le 2f_c + 1$. Then $x$ is the unique solution.

*Proof.* Let $\hat x$ be feasible and $h = \hat x - x$. Then $\int e^{-2\pi ikt}\,dh = 0$ for $|k| \le f_c$, so

$$\int \overline{q}\,dh = \sum_{|k| \le f_c}\overline{c_k}\int e^{-2\pi ikt}\,dh = 0.$$

Split $h = h_T + h_{T^c}$ into its restrictions to $T$ and to the complement of $T$. The measures $x + h_T$ and $h_{T^c}$ live on disjoint sets, so $\lVert\hat x\rVert_{TV} = \lVert x + h_T\rVert_{TV} + \lVert h_{T^c}\rVert_{TV}$. For any measure $\nu$ and any function with $|q| \le 1$ on its support, $\lVert\nu\rVert_{TV} \ge \operatorname{Re}\int\overline q\,d\nu$. Also $\int\overline q\,dx = \sum_j \overline{a_j}a_j/|a_j| = \lVert x\rVert_{TV}$. So

$$\lVert x + h_T\rVert_{TV} \ge \lVert x\rVert_{TV} + \operatorname{Re}\int\overline q\,dh_T = \lVert x\rVert_{TV} - \operatorname{Re}\int\overline q\,dh_{T^c},$$

and

$$\lVert\hat x\rVert_{TV} \ge \lVert x\rVert_{TV} + \int(1 - |q|)\,d|h_{T^c}|.$$

The function $1 - |q|$ is positive on the complement of $T$, so the last integral is positive unless $h_{T^c} = 0$. Hence a minimizer has $h_{T^c} = 0$, so $h = \sum_j b_j\delta_{t_j}$ with $\sum_j b_j e^{-2\pi ikt_j} = 0$ for $|k| \le f_c$. The vectors $(e^{-2\pi ikt_j})_{|k| \le f_c}$ are columns of a Vandermonde matrix with distinct nodes on the unit circle and $|T| \le 2f_c + 1$ columns, so they are linearly independent, and $b = 0$. So $\hat x = x$. $\square$

The condition $|T| \le 2f_c + 1$ holds under the separation of the theorem, since at most $f_c/2$ points fit on the circle $2/f_c$ apart.

**Lemma 2 (existence of the certificate, outline).** Let $K$ be the normalized fourth power of the Fejer kernel,

$$K(t) = \Bigl(\frac{\sin((f_c/2 + 1)\pi t)}{(f_c/2 + 1)\sin(\pi t)}\Bigr)^4,$$

a trigonometric polynomial of degree $f_c$ (for even $f_c$) with $K(0) = 1$, a sharp peak of width about $1/f_c$, and tails that decay like $(f_c t)^{-4}$. Look for

$$q(t) = \sum_j \alpha_j K(t - t_j) + \beta_j K'(t - t_j),$$

and fix the $2|T|$ coefficients by the [Hermite interpolation](/hermite-interpolation/) conditions $q(t_j) = a_j/|a_j|$ and $q'(t_j) = 0$. When $\Delta(T) \ge 2/f_c$, the tails of $K$, $K'$ and $K''$ at the other spikes are small, so the linear system is a small perturbation of a diagonal one. It is invertible, with $\alpha_j$ close to $a_j/|a_j|$ and $\beta_j$ close to $0$. Explicit bounds on $K$ and its first three derivatives then show two things. Near each $t_j$, $|q|$ has a strict local maximum of value $1$, because $q'(t_j) = 0$ and the second derivative of $|q|^2$ there is negative. Away from all $t_j$, $|q| < 1$, because each kernel term is small there. The numerical constants in these bounds need $f_c \ge 128$. With $q$ from Lemma 2, Lemma 1 proves the theorem. $\blacksquare$

The derivative conditions are essential: without $q'(t_j) = 0$, the interpolant of the values $\pm 1$ alone would exceed $1$ in modulus next to the spikes.

## Consequences

- **An exact algorithm.** For Fourier data the noiseless problem is solved by a semidefinite program for the dual. The certificate $q$ of the solver is then $\pm 1$ exactly on $T$, so the positions are the roots on the circle of the polynomial $1 - |q|^2$, and the amplitudes follow by least squares.
- **A certificate for small cases.** The theorem needs $f_c \ge 128$, but Lemma 1 applies to any $f_c$. For the spikes $+1$ at $0$ and $-1$ at $1/2$, the polynomial $\cos(2\pi t)$ of degree $1$ is a certificate. For one spike at $0$ with a positive amplitude, $(1 + \cos 2\pi t)/2$ is one.
- **Nonnegative spikes need no separation.** If all $a_j > 0$ and $|T| \le f_c$, then $P(t) = \prod_j\sin^2(\pi(t - t_j))$ is a nonnegative trigonometric polynomial of degree $|T|$ that vanishes only on $T$, and $q = 1 - P/\max P$ is a certificate. This is the setting of de Castro and Gamboa (2012).
- **Noise.** The same certificate, with the nondegeneracy that the proof gives (a negative second derivative of $|q|^2$ at the spikes), makes the penalized Beurling LASSO stable: for small noise it finds the same number of spikes, close to the true ones (Duval and Peyre 2015).
- **Super-resolution factor.** The data have the resolution $1/f_c$, and a grid of step $1/N$ would need the super-resolution factor $N/f_c$. The theorem holds for any such factor; only the separation matters, not the grid.

## Tightness

**Some separation is needed.** Take $f_c = M \ge 1$ and $0 < d < 1/2$. Let

$$x = \sum_{r=0}^{M-1}\bigl(\delta_{(r + d/2)/M} - \delta_{(r - d/2)/M}\bigr), \qquad \nu = \sin(\pi d)\sum_{r=0}^{M-1}\bigl(\delta_{(r + 1/4)/M} - \delta_{(r - 1/4)/M}\bigr).$$

For any $u$, $\sum_{r=0}^{M-1}e^{-2\pi ik(r + u)/M}$ is $Me^{-2\pi iku/M}$ if $M$ divides $k$ and $0$ otherwise. For $|k| \le M$ only $k = 0$ and $k = \pm M$ remain. Both measures have the coefficient $0$ at $k = 0$. At $k = \pm M$ they have $M(e^{\mp\pi id} - e^{\pm\pi id}) = \mp 2iM\sin(\pi d)$ and $M\sin(\pi d)(e^{\mp\pi i/2} - e^{\pm\pi i/2}) = \mp 2iM\sin(\pi d)$, which agree. So both are feasible, but

$$\lVert\nu\rVert_{TV} = 2M\sin(\pi d) < 2M = \lVert x\rVert_{TV}.$$

The separation of $x$ is $d/M = d/f_c$, so for every $f_c$ there are spikes $d/f_c$ apart, for any $d < 1/2$, that total variation minimization does not recover. In fact $\nu$ is the unique solution, with the certificate $\sin(2\pi Mt)$. For $f_c = 1$ the norm $2\sin(\pi d)$ of $\nu$ is $0.618$, $1.414$ and $1.902$ for $d = 0.1$, $0.25$ and $0.4$, against $2$ for $x$. So the constant of the theorem cannot be lowered below $1/2$. Between $1/2$ and the best proved constant $1.26$ there is a gap; this page does not claim where in it the true threshold lies.

**Opposite signs closer than $1/(\pi f_c)$ always fail.** If $x$ is a minimizer, strong duality holds (the dual is finite dimensional and $p = 0$ is strictly feasible), so there is a polynomial $q$ of degree $f_c$ with $|q| \le 1$ and $q(t_j) = a_j/|a_j|$ on $T$. If two spikes have real amplitudes of opposite sign, $q$ goes from $1$ to $-1$ between them. By Bernstein's inequality, $|q'| \le 2\pi f_c$, so the two spikes are at least $2/(2\pi f_c) = 1/(\pi f_c)$ apart. So no measure with opposite-sign spikes closer than that is ever recovered. For nonnegative amplitudes no separation is needed, as shown above.

## History

Beurling studied minimal extrapolation of measures from part of their Fourier transform, and de Castro and Gamboa (2012) used total variation minimization over measures to recover nonnegative spikes exactly. Candes and Fernandez-Granda posted their paper in 2012 and published it in 2014. It proved exact recovery of signed and complex spikes under the separation $2/f_c$, with the certificate built from the fourth power of the Fejer kernel, and solved the problem by a semidefinite program. Fernandez-Granda (2016) refined the construction and reached $1.26/f_c$. Duval and Peyre (2015) studied the penalized problem and showed when the support is stable under noise. The results started a body of work on off-the-grid sparse recovery, including the atomic norm view of line spectral estimation.

## References
