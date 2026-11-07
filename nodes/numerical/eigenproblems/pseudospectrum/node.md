---
tag: 6RE7YY
kind: concept
slug: pseudospectrum
name: Pseudospectrum
aliases:
- ε-pseudospectrum
- pseudospectra
- epsilon-pseudospectrum
area: numerical/eigenproblems
level: research
summary: The set of z where ‖(A − zI)⁻¹‖ exceeds 1/ε, a robust view of spectra for nonnormal matrices.
prereqs: [nonsymmetric-eigenproblem, singular-value-decomposition, matrix-norms]
see_also: [condition-number, schur-decomposition, power-iteration, backward-error-analysis, similarity-transformation, spectral-theorem, weyls-inequality, qr-algorithm]
sources:
  - book: isbn:9780691119465
    title: Lloyd N. Trefethen and Mark Embree, Spectra and Pseudospectra, The Behavior of Nonnormal Matrices and Operators, Princeton University Press, 2005
    locator: Chapter 2 (the equivalent definitions, Theorem 2.1, and basic properties), Part IV (transient effects and the Kreiss matrix theorem), Part IX (computation of pseudospectra)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 7.9, Pseudospectra
  - paper: "Lloyd N. Trefethen, Computation of pseudospectra, Acta Numerica 8, 1999"
    title: Computation of pseudospectra
    locator: Acta Numerica 8 (1999), pp. 247 to 295
  - paper: "Lloyd N. Trefethen, Pseudospectra of linear operators, SIAM Review 39(3), 1997"
    title: Pseudospectra of linear operators
    locator: SIAM Rev. 39(3) (1997), pp. 383 to 406
  - paper: "Lloyd N. Trefethen, Anne E. Trefethen, Satish C. Reddy and Tobin A. Driscoll, Hydrodynamic stability without eigenvalues, Science 261, 1993"
    title: Hydrodynamic stability without eigenvalues
    locator: Science 261 (1993), pp. 578 to 584
  - paper: "Randall J. LeVeque and Lloyd N. Trefethen, On the resolvent condition in the Kreiss matrix theorem, BIT 24, 1984"
    title: On the resolvent condition in the Kreiss matrix theorem
    locator: BIT 24 (1984), pp. 584 to 591
  - paper: "James V. Burke, Adrian S. Lewis and Michael L. Overton, Robust stability and a criss-cross algorithm for pseudospectra, IMA Journal of Numerical Analysis 23, 2003"
    title: Robust stability and a criss-cross algorithm for pseudospectra
    locator: IMA J. Numer. Anal. 23 (2003), pp. 359 to 375
---

The $\varepsilon$-pseudospectrum of a square matrix $A$ is the set of complex numbers $z$ at which the resolvent $(zI - A)^{-1}$ has norm larger than $1/\varepsilon$. Equivalently, it is the set of numbers that are eigenvalues of some perturbed matrix $A + E$ with $\|E\| < \varepsilon$. For a normal matrix it is just the union of discs of radius $\varepsilon$ around the eigenvalues. For a nonnormal matrix it can be far larger: points far from every eigenvalue may be eigenvalues of a matrix within rounding distance of $A$. Pseudospectra explain what the eigenvalues alone cannot, such as the transient growth of $\|A^k\|$ and $\|e^{tA}\|$ when all eigenvalues indicate decay, the sensitivity of computed eigenvalues to rounding, and the convergence of iterative methods for nonnormal matrices.

## In plain words

The special values of a table of numbers can be very touchy. For some tables, nudging the entries by a hair moves those values a long way. The pseudospectrum answers a practical question: if every entry may be off by a tiny amount, where could the special values end up? It is a region in the plane drawn around the special values. For well-behaved tables the region is just a small circle around each value. For touchy tables it spreads into large blobs. Those blobs predict real effects: a process that should die out may first grow a lot, and a computer may report values far from the true ones, because both depend on the whole region, not on the few points at its centre.

## The idea

**Notation.** $A$ is a complex $n \times n$ matrix with eigenvalues $\lambda_1, \dots, \lambda_n$ (in no particular order on this page, since they may be complex), $\sigma(A)$ is the set of eigenvalues, and $\|\cdot\|$ is the 2-norm. $R(z) = (zI - A)^{-1}$ is the resolvent, defined for $z \notin \sigma(A)$, with the convention $\|R(z)\| = \infty$ on $\sigma(A)$. $\sigma_{\min}$ is the smallest singular value, $\Delta_r$ the open disc of radius $r$ about $0$, and $u$ the unit roundoff.

**Three equal definitions.** For $\varepsilon > 0$ the following sets are equal (Trefethen and Embree, Theorem 2.1):

$$\Lambda_\varepsilon(A) = \{ z : \|(zI - A)^{-1}\| > 1/\varepsilon \} = \{ z : z \in \sigma(A + E) \text{ for some } \|E\| < \varepsilon \} = \{ z : \|(A - zI) v\| < \varepsilon \text{ for some unit } v \}.$$

The first says the resolvent is large. The second says $z$ is an eigenvalue of a nearby matrix. The third says $z$ is an approximate eigenvalue with residual below $\varepsilon$, which is exactly what a backward stable eigensolver delivers. In the 2-norm, $\|R(z)\| = 1/\sigma_{\min}(zI - A)$, so $\Lambda_\varepsilon(A) = \{ z : \sigma_{\min}(zI - A) < \varepsilon \}$. The proof of the equivalences: if $\|(A - zI) v\| = s < \varepsilon$ for a unit $v$, then $E = -(A - zI) v v^*$ has $\|E\| = s$ and $(A + E - zI) v = 0$; conversely an eigenvector $v$ of $A + E$ gives $\|(A - zI) v\| = \|E v\| < \varepsilon$; and $\min_{\|v\| = 1} \|(A - zI) v\| = \sigma_{\min}(A - zI)$.

**Basic properties.** Each $\Lambda_\varepsilon(A)$ is a bounded open set containing $\sigma(A)$, the sets grow with $\varepsilon$, and their intersection over all $\varepsilon > 0$ is $\sigma(A)$. Every connected component of $\Lambda_\varepsilon(A)$ contains an eigenvalue, so there are at most $n$ components. Pseudospectra are invariant under unitary similarity, $\Lambda_\varepsilon(U^* A U) = \Lambda_\varepsilon(A)$, so they can be computed from the [Schur form](/schur-decomposition/). They shift and scale with $A$: $\Lambda_\varepsilon(\alpha A + \beta I) = \alpha \Lambda_{\varepsilon/|\alpha|}(A) + \beta$.

**Normal and nonnormal.** Always $\sigma(A) + \Delta_\varepsilon \subseteq \Lambda_\varepsilon(A)$, because $\|R(z)\| \ge 1/\operatorname{dist}(z, \sigma(A))$. If $A$ is normal, $\|R(z)\| = 1/\operatorname{dist}(z, \sigma(A))$ exactly and equality holds. If $A = V \Lambda V^{-1}$ is diagonalizable, the Bauer-Fike argument gives $\Lambda_\varepsilon(A) \subseteq \sigma(A) + \Delta_{\varepsilon \kappa(V)}$ with $\kappa(V) = \|V\| \|V^{-1}\|$. Asymptotically, near a simple eigenvalue $\lambda_j$ with right and left unit eigenvectors $x_j$ and $y_j$, $\Lambda_\varepsilon(A)$ is close to the disc of radius $\varepsilon / |y_j^* x_j|$ as $\varepsilon \to 0$: the eigenvalue [condition number](/condition-number/) $1/|y_j^* x_j|$ is the local magnification. For a Jordan block of size $m$, the radius grows like $\varepsilon^{1/m}$, which is much larger than $\varepsilon$ for small $\varepsilon$.

**Rounding errors.** A backward stable eigensolver such as the [QR algorithm](/qr-algorithm/) returns the exact eigenvalues of $A + E$ with $\|E\| = O(u \|A\|)$. So the computed eigenvalues lie in $\Lambda_{c u \|A\|}(A)$ for a modest $c$, and anywhere in it: when that set is large, the computed eigenvalues can be far from the true ones, and no stable algorithm can do better ([backward error analysis](/backward-error-analysis/)).

**Transient behaviour.** Eigenvalues determine the behaviour of $\|A^k\|$ and $\|e^{tA}\|$ only as $k, t \to \infty$. Pseudospectra bound the transient. With the $\varepsilon$-pseudospectral radius $\rho_\varepsilon(A) = \sup \{ |z| : z \in \Lambda_\varepsilon(A) \}$,

$$\sup_{k \ge 0} \|A^k\| \ge \frac{\rho_\varepsilon(A) - 1}{\varepsilon} \quad \text{for every } \varepsilon > 0,$$

which follows from the Laplace transform identity $R(z) = \sum_k A^k / z^{k+1}$ for $|z| > \rho(A)$. The supremum over $\varepsilon$ of the right side is the Kreiss constant $K(A) = \sup_{|z| > 1} (|z| - 1) \|R(z)\|$, and the Kreiss matrix theorem states $K(A) \le \sup_k \|A^k\| \le e \, n \, K(A)$ (Kreiss 1962 proved a bound of this form with a much larger factor; LeVeque and Trefethen 1984 proved $2en$, and Spijker 1991 $en$). The continuous analogue uses the $\varepsilon$-pseudospectral abscissa $\alpha_\varepsilon(A) = \sup \{ \operatorname{Re} z : z \in \Lambda_\varepsilon(A) \}$ and bounds $\sup_t \|e^{tA}\| \ge \alpha_\varepsilon(A)/\varepsilon$.

**Computation.** The standard method evaluates $\sigma_{\min}(zI - A)$ on a grid of points $z$ and draws contour lines at the wanted levels $\varepsilon$. Done naively, each point costs $O(n^3)$. Reducing $A$ once to triangular Schur form $T$ ($O(n^3)$, by the [QR algorithm](/qr-algorithm/)) lets each point use inverse Lanczos iteration on $(zI - T)^* (zI - T)$ with triangular solves, $O(n^2)$ per point (Trefethen 1999); the EigTool package of Wright implements this. Special quantities have faster algorithms: the pseudospectral abscissa and radius by criss-cross searches with Hamiltonian eigenproblems (Burke, Lewis and Overton 2003; Mengi and Overton 2005), and the distance to instability $\min_{\operatorname{Re} z = 0} \sigma_{\min}(zI - A)$ by Byers' bisection (1988).

## Examples

**A nonnormal $2 \times 2$ matrix.** Let

$$A = \begin{pmatrix} 1 & 100 \\ 0 & 2 \end{pmatrix}, \qquad \sigma(A) = \{1, 2\}.$$

At $z = 1.5$, halfway between the eigenvalues, $A - zI = \begin{pmatrix} -0.5 & 100 \\ 0 & 0.5 \end{pmatrix}$ has $|\det| = 0.25$ and largest singular value $100.0025$, so $\sigma_{\min} = 0.0024999$. Thus $1.5 \in \Lambda_\varepsilon(A)$ for every $\varepsilon > 0.0025$: a perturbation of norm $0.0025$ makes $1.5$ an eigenvalue, although $1.5$ is at distance $0.5$ from the spectrum. The point $1.5 + 2i$, at distance $2.06$, has $\sigma_{\min} = 0.0425$; the points $0$ and $3$, at distance $1$, have $\sigma_{\min} = 0.0200$. The eigenvalue condition numbers are both $\sqrt{1 + 100^2} = 100.005$, and the eigenvector matrix has $\kappa(V) = 200.005$. For a normal matrix with the same eigenvalues, the $0.0025$-pseudospectrum would be two discs of radius $0.0025$.

**Jordan blocks.** For the nilpotent Jordan block $J_m$ (ones on the superdiagonal) the pseudospectra are discs about $0$, and $\sigma_{\min}(zI - J_m) \approx |z|^m$ for small $|z|$: for $m = 4$ the values at $|z| = 0.1, 0.3, 0.5$ are $9.90 \times 10^{-5}$, $7.37 \times 10^{-3}$, $4.74 \times 10^{-2}$, and for $m = 8$ at $|z| = 0.1$ it is $1.0 \times 10^{-8}$. So a perturbation of size $10^{-8}$ can move the eigenvalue $0$ of $J_8$ a distance $0.1$, and one of size $u \approx 10^{-16}$ a distance about $0.01$.

**Transient growth.** Let $B = \begin{pmatrix} 0.9 & 1 \\ 0 & 0.9 \end{pmatrix}$. Its spectral radius is $0.9$, so $B^k \to 0$, but $\|B^k\|$ rises to $3.9126$ at $k = 9$ before decaying ($\|B\| = 1.5296$, $\|B^{20}\| = 2.707$, $\|B^{40}\| = 0.657$). Its pseudospectra are discs about $0.9$ of radius $\sqrt{\varepsilon (1 + \varepsilon)}$, so $\rho_\varepsilon(B) = 0.9 + \sqrt{\varepsilon(1 + \varepsilon)}$. At $\varepsilon = 1/24$ this is $0.9 + 5/24$, and the bound gives $\sup_k \|B^k\| \ge (5/24 - 0.1)/(1/24) = 2.6$, which is also the Kreiss constant $K(B)$. The theorem brackets the true peak, $2.6 \le 3.9126 \le e \cdot 2 \cdot 2.6 = 14.1$; the eigenvalues alone predict no growth at all. These numbers were computed by a script with closed-form singular values of $2 \times 2$ matrices and Jacobi's method for $J_m$.

## Where it is used

- **Fluid dynamics.** Linearized Navier-Stokes operators for shear flows have all eigenvalues in the stable half plane at Reynolds numbers where experiments show transition to turbulence; their pseudospectra protrude far into the unstable half plane and explain transient amplification by factors of thousands (Trefethen, Trefethen, Reddy and Driscoll 1993).
- **Stability of numerical methods for ODEs and PDEs.** The Kreiss matrix theorem and the Lax-Richtmyer theory use resolvent conditions rather than eigenvalues to decide whether a discretization is stable; pseudospectra show why the eigenvalue condition fails for nonnormal discretizations of convection.
- **Accuracy of computed eigenvalues.** The size of $\Lambda_{u\|A\|}(A)$ is the honest error bar on eigenvalues computed by any backward stable method for the [nonsymmetric eigenproblem](/nonsymmetric-eigenproblem/).
- **Iterative methods.** GMRES and other Krylov methods for nonnormal matrices converge at rates governed by pseudospectra, not by eigenvalues alone, and [power iteration](/power-iteration/) on a nonnormal matrix can stagnate long before its asymptotic rate takes over.
- **Robust control.** The distance to instability and the pseudospectral abscissa are robustness margins: how large a perturbation turns a stable system unstable.
- **Markov chains and card shuffling.** Cutoff phenomena, where a chain stays far from equilibrium and then mixes suddenly, show up as transient behaviour that pseudospectra describe (Jonsson and Trefethen 1998).

## References
