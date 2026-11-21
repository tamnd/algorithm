---
tag: Q00HZV
kind: algorithm
slug: d-bar-method
name: D-bar method
aliases:
- D-bar reconstruction for EIT
area: imaging-and-inverse-problems/tomographic-reconstruction
level: research
summary: Reconstruct a 2D conductivity from boundary data through scattering transforms and a d-bar equation, a direct nonlinear method for EIT.
model: real-ram
complexity:
  vars: {n: "the side of the n x n grid of points z where the conductivity is wanted", m: "the number of grid points k in the disk |k| <= R", c: "the number of electrodes or boundary Fourier modes", K: "the number of fixed-point iterations for one point z"}
  time: {per_iteration: "O(m^2)", total: "O(m c^2 + n^2 K m^2)"}
  space: {extra: "O(m^2 + n^2)"}
properties: {deterministic: true, iterative: true, direct_in_gamma: true, parallel_over_points: true, regularized_by_cutoff: true, in_place: false, recursive: false}
history:
  year: 2000
  people: [Samuli Siltanen, Jennifer L. Mueller, David Isaacson]
  note: Siltanen, Mueller and Isaacson turned Nachman's 1996 uniqueness proof for the planar conductivity problem into a numerical method, with the approximate scattering transform t^exp and a cutoff.
prereqs: [calderon-problem, fixed-point-iteration, banach-fixed-point-theorem]
see_also: [gauss-newton-algorithm, tikhonov-regularization, regularization-parameter-choice, degree-of-ill-posedness, novikov-inversion-formula, fast-fourier-transform, gmres, classical-runge-kutta-4]
sources:
  - paper: doi:10.2307/2118653
    title: A. I. Nachman, Global uniqueness for a two-dimensional inverse boundary value problem, Annals of Mathematics 143(1), 1996
    locator: pp. 71 to 96 (the scattering transform, the d-bar equation in k, and gamma = mu(z, 0)^2)
  - paper: doi:10.1088/0266-5611/16/3/310
    title: S. Siltanen, J. Mueller and D. Isaacson, An implementation of the reconstruction algorithm of A Nachman for the 2D inverse conductivity problem, Inverse Problems 16(3), 2000
    locator: pp. 681 to 699, with the corrigendum in Inverse Problems 17, 2001, p. 1561 (the first implementation, and the approximation t^exp)
  - paper: doi:10.1137/S1064827501394568
    title: J. L. Mueller and S. Siltanen, Direct reconstructions of conductivities from boundary measurements, SIAM Journal on Scientific Computing 24(4), 2003
    locator: pp. 1232 to 1266 (the method on simulated noisy data, with the cutoff as a regularization)
  - paper: doi:10.3934/ipi.2009.3.599
    title: K. Knudsen, M. Lassas, J. L. Mueller and S. Siltanen, Regularized D-bar method for the inverse conductivity problem, Inverse Problems and Imaging 3(4), 2009
    locator: pp. 599 to 624 (a cutoff chosen from the noise level gives a regularization strategy)
  - book: isbn:9781611972337
    title: J. L. Mueller and S. Siltanen, Linear and Nonlinear Inverse Problems with Practical Applications, SIAM, 2012
    locator: Chapter 15, A regularized D-bar method for direct EIT, and Chapter 16 (general locator)
---

The D-bar method computes a conductivity in a plane domain directly from boundary measurements, without fitting a forward model by iterations. It solves the [Calderon problem](/calderon-problem/) in two dimensions, the mathematical core of electrical impedance tomography (EIT). The method follows Nachman's 1996 uniqueness proof. From the Dirichlet-to-Neumann map $\Lambda_\gamma$ it computes a scattering transform $\mathbf{t}(k)$ of a complex parameter $k$. Then for each point $z$ it solves a linear integral equation in $k$, the d-bar equation, and reads off $\gamma(z) = \mu(z, 0)^2$. The practical form, from Siltanen, Mueller and Isaacson (2000), uses the approximation $\mathbf{t}^{\exp}$ and cuts it off at $|k| \le R$. The cutoff is the regularization: a small $R$ gives a smooth, stable image, and a large $R$ gives detail and amplifies the noise.

## In plain words

You drive currents through electrodes on the edge of a body and measure the voltages. You want the conductivity inside. The relation is nonlinear, and most methods guess an image, simulate the measurements, and correct the guess many times.

The D-bar method does not guess. It first turns all the boundary data into one function of a complex frequency, the scattering transform. Then, for each point inside the body, it solves one linear equation in the frequency variable. The value of the solution at frequency zero gives the conductivity at that point. The points do not depend on each other, so they can be done in parallel.

The data are noisy, and the noise grows at high frequencies. So the method uses only the frequencies in a disk. A small disk gives a blurred but stable image. A larger disk gives more detail and more noise.

## The problem

The input is the Dirichlet-to-Neumann map $\Lambda_\gamma$ of a real conductivity $\gamma > 0$ on the unit disk $\Omega$, with $\gamma = 1$ near the boundary. $\Lambda_\gamma$ maps the boundary voltage $f$ to the current $\gamma\, \partial u / \partial \nu$, where $\nabla \cdot (\gamma \nabla u) = 0$ in $\Omega$ and $u = f$ on $\partial\Omega$. In practice $\Lambda_\gamma$ is a $c \times c$ matrix in the basis of trigonometric functions or of electrode patterns, with noise. The output is $\gamma(z)$ at the points $z = x_1 + i x_2$ of an $n \times n$ grid.

Write $e_z(k) = \exp(i(kz + \overline{kz}))$ for $k \in \mathbb{C}$. Nachman's scattering transform is $\mathbf{t}(k) = \int_{\partial\Omega} e^{i \bar k \bar z} (\Lambda_\gamma - \Lambda_1)\psi(\cdot, k)\, ds$, where $\psi(z, k) \approx e^{ikz}$ are special solutions that need a boundary integral equation of their own. The approximation
$$\mathbf{t}^{\exp}(k) = \int_{\partial\Omega} e^{i \bar k \bar z} (\Lambda_\gamma - \Lambda_1)\, e^{ikz}\, ds(z)$$
replaces $\psi$ by $e^{ikz}$ and needs only the data. For a radial conductivity, $\Lambda_\gamma e^{i n \varphi} = \lambda_{|n|} e^{i n \varphi}$, and
$$\mathbf{t}^{\exp}(k) = 2\pi \sum_{n \ge 1} (-1)^n \frac{|k|^{2n}}{(n!)^2} (\lambda_n - n).$$
The weights $|k|^{2n}/(n!)^2$ grow very fast with $|k|$, which is how the noise in $\lambda_n$ reaches $\mathbf{t}^{\exp}$.

The truncated d-bar equation for one point $z$ is
$$\mu(z, k) = 1 + \frac{1}{4\pi^2} \int_{|k'| \le R} \frac{\mathbf{t}^{\exp}(k')\, e_{-z}(k')\, \overline{\mu(z, k')}}{(k - k')\, \overline{k'}} \, dA(k').$$
It is the integral form of $\bar\partial_k \mu = \frac{1}{4\pi \bar k}\, \mathbf{t}(k) e_{-z}(k)\, \overline{\mu}$ with $\mu - 1 \to 0$ at infinity, because $1/(\pi k)$ is a fundamental solution of $\bar\partial_k$. The equation is real-linear in $\mu$, not complex-linear, because of the conjugate. The reconstruction is $\gamma_R(z) = \operatorname{Re} \mu(z, 0)^2$.

## The algorithm

```pseudo id=main
D-BAR(λ_1..λ_c, Z, R, h, ε, K)             ▷ radial data: λ_n are the DN eigenvalues
L1  G ← the points k = h(i + i' j) with |k| ≤ R, with k = 0 first
L2  t_k ← 2π Σ_n (-1)^n |k|^(2n) (λ_n - n) / (n!)^2 for each k in G     ▷ t^exp
L3  for each point z in Z do
L4      w_k ← h² t_k e_{-z}(k) / (4π² conj(k)) for k ≠ 0, and w_0 ← 0
L5      μ ← 1 at every point of G
L6      repeat at most K times
L7          μ_k ← 1 + Σ_{k' ≠ k} w_k' conj(μ_k') / (k - k') for each k in G
L8      until the largest change of μ is below ε
L9      γ(z) ← Re μ_0²
L10 return γ
```

Line L2 is the only line that sees the data. For data that are not radial, L2 expands $e^{ikz}$ and $e^{i\bar k \bar z}$ in the boundary basis and applies the measured matrix of $\Lambda_\gamma - \Lambda_1$, at a cost of $O(c^2)$ per point $k$. Line L4 sets the weight of $k = 0$ to 0: near 0, $\mathbf{t}^{\exp}(k) = O(|k|^2)$, so $\mathbf{t}^{\exp}(k)/\bar k \to 0$. Line L7 is the midpoint rule on cells of side $h$, with the cell $k' = k$ left out; that cell holds the singularity, and for a smooth integrand it contributes $O(h)$. Each point $z$ is independent of the others.

## Example

Take the radial conductivity $\gamma(r) = 1 + 0.2 \exp(1 - 1/(1 - (r/0.6)^2))$ for $r < 0.6$ and $\gamma = 1$ for $r \ge 0.6$. It is smooth, equal to 1 near the boundary, and has the peak $\gamma(0) = 1.2$. The DN eigenvalues, from a Runge-Kutta solve of the radial equation, are $\lambda_1 = 1.0275936$, $\lambda_2 = 2.0104328$ and $\lambda_3 = 3.0033316$; the excess $\lambda_n - n$ falls by a factor of about 3 for each $n$. Line L2 gives $\mathbf{t}^{\exp} = -0.0423$ at $|k| = 0.5$, $-0.1576$ at $|k| = 1$, $-0.4658$ at $|k| = 2$ and $-0.5917$ at $|k| = 3$. It is real and radial, as it must be for radial data.

With $R = 3$ and $h = 0.3$ the grid has 317 points, and the contraction factor of the loop is $q = 0.085$, so the loop converges fast from $\mu = 1$. The results (a measurement):

| $r = \lvert z \rvert$ | 0 | 0.2 | 0.4 | 0.6 | 0.8 |
|---|---|---|---|---|---|
| true $\gamma$ | 1.2 | 1.1765 | 1.0899 | 1 | 1 |
| $R = 2$ | 1.0933 | 1.0863 | 1.0675 | 1.0427 | 1.0185 |
| $R = 3$ | 1.1765 | 1.1490 | 1.0856 | 1.0242 | 0.9906 |

At $z = 0$ there is a closed form: for a real radial transform, $\mu(0, k)$ depends only on $|k|$, and $\gamma_R(0) = \exp(-\frac{1}{\pi}\int_0^R \mathbf{t}^{\exp}(s)/s\, ds)$ (a theorem, proved in the correctness section). It gives 1.0957 for $R = 2$ and 1.1765 for $R = 3$, which the grid matches to 4 digits. As $R$ grows, the closed form gives 1.2327 at $R = 4$, 1.2460 at $R = 5$, 1.2285 at $R = 6$ and 1.1994 at $R = 8$. The small cutoffs smooth the peak, and the larger ones overshoot a little and come back (a measurement on noise-free data).

## Correctness

Three statements are theorems. First, for a radial conductivity the series in line L2 is exactly $\mathbf{t}^{\exp}$: expand $e^{ikz}$ on the circle in powers of $e^{i\varphi}$, apply the eigenvalues, and integrate against $e^{i \bar k \bar z}$; only the matching modes survive. Second, at $z = 0$ with a real radial $\mathbf{t}$, the truncated equation has the solution $\mu(0, k) = m(|k|)$ with $m(r) = \exp(-\frac{1}{2\pi}\int_r^R t(s)/s\, ds)$; the proof is that the mean of $k'/(k - k')$ over a circle $|k'| = s$ is 0 for $s < |k|$ and $-1$ for $s > |k|$. Third, the loop L6 to L8 is a contraction in the sup norm when $q = \max_k \sum_{k' \ne k} |w_{k'}|/|k - k'| < 1$, so it has one fixed point and converges to it with the rate $q$, even though the map is only real-linear. For the continuous equation, $R \sup_{|k| \le R} |\mathbf{t}(k)|/|k| < 2\pi$ is enough. In the example $q = 0.085$ at $R = 3$. The full proofs are in the correctness file.

What is not a theorem: that $\gamma_R$ is close to $\gamma$. Nachman's theorem says that with the exact $\mathbf{t}$ and no cutoff, $\mu(z, 0)^2 = \gamma(z)$ for conductivities with two derivatives in $L^p$, $p > 1$. Knudsen, Lassas, Mueller and Siltanen (2009) proved that a cutoff $R$ chosen from the noise level makes the method with the exact $\mathbf{t}$ a regularization strategy: the result tends to $\gamma$ as the noise tends to 0. The approximation $\mathbf{t}^{\exp}$ agrees with $\mathbf{t}$ for small $|k|$ and differs for large $|k|$. Its use is a heuristic, supported by measurements such as the table above.

## Complexity

In the real-RAM model, let $m$ be the number of grid points with $|k| \le R$, so $m \approx \pi R^2/h^2$, let $c$ be the number of boundary modes, $n^2$ the number of points $z$, and $K$ the number of iterations for one point. Line L2 costs $O(m c)$ for radial data and $O(m c^2)$ for a full matrix. One iteration of line L7 costs $O(m^2)$ with the direct sum, as in the code, so one point costs $O(K m^2)$ and all points $O(n^2 K m^2)$. The Cauchy matrix takes $O(m^2)$ memory. The sum in line L7 is a discrete convolution with the kernel $1/k$, so on a periodic grid it costs $O(m \log m)$ with the [fast Fourier transform](/fast-fourier-transform/); practical codes do this and solve the real-linear system with [GMRES](/gmres/) on the real and imaginary parts. $K$ is the number of iterations to reach the tolerance; by the contraction theorem it is at most $\log(1/\varepsilon)/\log(1/q)$ up to a constant when $q < 1$, but $q$ is not known in advance.

## Properties

- **Direct in the conductivity.** There is no forward solver and no outer iteration over $\gamma$. The only iteration is the linear solve for each $z$. This is a property of the method.
- **Parallel over the points.** Each $z$ is a separate linear problem with the same $\mathbf{t}^{\exp}$.
- **Regularized by the cutoff.** The radius $R$ is the only regularization parameter. It is a nonlinear low-pass filter, because the cutoff acts on $\mathbf{t}$, not on $\gamma$.
- **Smooth output.** With a cutoff, the result is smooth, and sharp edges come out blurred.
- **Exact for the background.** For $\gamma = 1$, $\mathbf{t}^{\exp} = 0$ and the result is exactly 1 at every point, for every $R$.
- **Two dimensions only.** The method uses the complex structure of the plane. Related methods in 3D use the special solutions of Sylvester and Uhlmann; they work differently and are still a research subject.

## Variants and improvements

- **The full scattering transform.** Compute $\psi(\cdot, k)$ on the boundary from Nachman's boundary integral equation, then $\mathbf{t}$. This is the form with a convergence proof; it costs a boundary solve for each $k$.
- **Nonlinear low-pass filtering with a noise-based $R$.** Knudsen, Lassas, Mueller and Siltanen choose $R$ as a function of the noise level and prove that this is a regularization strategy. In practice $R$ is often chosen by looking at where $\mathbf{t}^{\exp}$ starts to blow up, which is a heuristic.
- **Other domains and electrodes.** Real data come from a few electrodes on a domain that is not a disk. Then $\Lambda_\gamma$ is known only on electrode patterns, and the domain is mapped to a disk or treated by a boundary correction. See Chapter 15 of Mueller and Siltanen.
- **Complex conductivities and partial data.** There are D-bar methods for admittivities $\sigma + i\omega\varepsilon$ and for data on part of the boundary. They need different scattering transforms.
- **Linearized forms.** Replacing $\mu$ by 1 in the integral gives a one-step reconstruction that is linear in $\mathbf{t}^{\exp}$, in the spirit of Calderon's linearization. It is faster; that it is less accurate for high contrast is a heuristic expectation, because it drops the nonlinear part.

## When to use it

Use the D-bar method for absolute imaging of a planar conductivity, when you want a direct method without a forward solver and with one clear regularization parameter. It is fast for many points and gives a good starting image for iterative methods such as the [Gauss-Newton algorithm](/gauss-newton-algorithm/) with [Tikhonov regularization](/tikhonov-regularization/). For 3D bodies, or when a detailed electrode model is needed, an iterative method with a finite element forward solver is the usual choice.

## Pitfalls

- **A large cutoff with noise.** The weights $|k|^{2n}/(n!)^2$ amplify noise in $\lambda_n$ very fast. For the conductivity of the example with peak 1.5 instead of 1.2, Gaussian noise of standard deviation 0.003 on each $\lambda_n$ changes $\gamma_R(0)$ by 0.01 at $R = 2$ and by more than 1 at $R = 5$ (a measurement, seed 3). Choose $R$ from the noise level.
- **A large cutoff without noise.** $\mathbf{t}^{\exp}$ is not $\mathbf{t}$. For two layers, $\gamma = 2$ for $r < 0.5$ and $\gamma = 1$ outside, the center value is 1.776 at $R = 2$, 2.610 at $R = 3$ and 3.074 at $R = 4$, against the true value 2 (a measurement on exact data). High contrast and jumps make $\mathbf{t}^{\exp}$ wrong at large $|k|$ first.
- **The point $k = 0$.** The factor $1/\bar k$ is singular there. Use $\mathbf{t}^{\exp}(k)/\bar k \to 0$ and give $k = 0$ the weight 0, or shift the grid so that 0 is not a cell center and interpolate.
- **Forgetting the conjugate.** The equation has $\overline{\mu}$, so it is not a complex-linear system. A complex solver applied to $\mu$ directly gives wrong results; split into real and imaginary parts.
- **A conductivity that is not 1 at the boundary.** The theory assumes $\gamma = 1$ near $\partial\Omega$. If the boundary value is $\gamma_0 \ne 1$, divide the data by $\gamma_0$ first. Even a tail of size $10^{-4}$ at the boundary makes $\lambda_n - n$ grow about linearly with $n$ (a first-order estimate), and this spoils $\mathbf{t}^{\exp}$ for large $|k|$.
- **No convergence check.** The fixed-point loop converges only when the map is a contraction or close to it. Check the change, cap the iterations, and stop with an error, as the code does.

## Implementations

The Python code takes the DN eigenvalues $\lambda_1, \lambda_2, \dots$ of a radial conductivity, a list of points $z$, the cutoff $R$ and the grid spacing $h$. It stores the full Cauchy matrix, so it is meant for grids of a few hundred points. It also has two helpers for test data: the closed-form eigenvalues of a two-layer conductivity, and a solver for any radial $\gamma(r)$ that integrates the Riccati equation $dw/ds = n^2 \gamma - w^2/\gamma$ for $w = r\gamma U'/U$ in $s = \log r$ with the [classical Runge-Kutta method](/classical-runge-kutta-4/). The tests check the eigenvalues $13/11$ and $98/47$ of the two-layer case and the agreement of the two solvers, the series for $\mathbf{t}^{\exp}$ against a direct quadrature of the boundary integral, the first-order Cauchy transform of $e^{-|k|^2}$ against $(1 - e^{-|z|^2})/z$, the exact result for $\gamma = 1$, the residual of the fixed point and the closed form at $z = 0$, the rotation symmetry and the accuracy on the smooth example, and the growth of the noise with $R$.

## History

Calderon posed the problem in 1980. Nachman (1996) proved uniqueness in the plane for conductivities with two derivatives, with a constructive proof: the conductivity comes from the solution of a d-bar equation in the complex parameter $k$. Siltanen, Mueller and Isaacson (2000) implemented this proof as an algorithm and introduced the approximation $\mathbf{t}^{\exp}$. Mueller and Siltanen (2003) studied the method on noisy data and used the cutoff as the regularization. Knudsen, Lassas, Mueller and Siltanen (2009) proved that the cutoff, chosen from the noise level, gives a regularization strategy. The method has since been used on data from real EIT devices.

## References
