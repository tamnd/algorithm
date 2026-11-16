---
title: The moment formulas of CAMShift give the centroid, the principal axis and the spread of the probability mass, the size rule doubles a uniform target, and the loop stops
proves: [correctness]
status: full
---

Notation as on the page. $P(x) \ge 0$ is the probability image, the window $R$ is a finite set of pixels, and the moments are $M_{ij} = \sum_{(u, v) \in R} u^i v^j P(u, v)$. We assume $M_{00} > 0$; line L5 handles the other case.

## Claim 1: lines L4 and L6 compute the centroid, and a fixed point is a window centered on its own centroid

$(x_c, y_c) = (M_{10} / M_{00}, M_{01} / M_{00})$ is the mean of the pixel positions in $R$ weighted by $P$, which is the definition of the centroid of the mass $P$ restricted to $R$. Line L6 moves the window center there. If the window is centered at $(x_c, y_c)$ of its own pixels, the next centroid equals the center, so the move is 0 and line L7 stops. $\square$

## Claim 2: the orientation and the axis lengths are those of the covariance matrix

Let $a = M_{20} / M_{00} - x_c^2$, $b = 2 (M_{11} / M_{00} - x_c y_c)$ and $c = M_{02} / M_{00} - y_c^2$. Then

$$
\Sigma = \begin{pmatrix} a & b/2 \\ b/2 & c \end{pmatrix}
$$

is the covariance matrix of the position under the weights $P / M_{00}$, since for example $\sum P (u - x_c)^2 / M_{00} = M_{20} / M_{00} - x_c^2$. Let $\theta = \frac12 \operatorname{atan2}(b, a - c)$, $e = (\cos \theta, \sin \theta)$ and $f = (-\sin \theta, \cos \theta)$, and let $R_\theta$ be the rotation with columns $e$ and $f$. Write $a - c = \kappa \cos 2\theta$ and $b = \kappa \sin 2\theta$ with $\kappa = \sqrt{b^2 + (a - c)^2} \ge 0$; this is the definition of atan2. Using $\cos^2 \theta = (1 + \cos 2\theta)/2$, $\sin^2 \theta = (1 - \cos 2\theta)/2$ and $2 \sin \theta \cos \theta = \sin 2\theta$:

$$
e^{\mathsf T} \Sigma e = a \cos^2 \theta + b \sin \theta \cos \theta + c \sin^2 \theta = \tfrac{a + c}{2} + \tfrac{a - c}{2} \cos 2\theta + \tfrac{b}{2} \sin 2\theta = \tfrac{a + c + \kappa}{2},
$$

$$
f^{\mathsf T} \Sigma f = \tfrac{a + c}{2} - \tfrac{a - c}{2} \cos 2\theta - \tfrac{b}{2} \sin 2\theta = \tfrac{a + c - \kappa}{2},
$$

$$
e^{\mathsf T} \Sigma f = -\tfrac{a - c}{2} \sin 2\theta + \tfrac{b}{2} \cos 2\theta = -\tfrac{\kappa}{2} \cos 2\theta \sin 2\theta + \tfrac{\kappa}{2} \sin 2\theta \cos 2\theta = 0 .
$$

So $R_\theta^{\mathsf T} \Sigma R_\theta = \operatorname{diag}(\lambda_1, \lambda_2)$ with $\lambda_{1,2} = (a + c \pm \kappa)/2$: $e$ is an eigenvector for the larger eigenvalue, and the length and width of line L9 are $\sqrt{\lambda_1}$ and $\sqrt{\lambda_2}$, the standard deviations of the mass along its principal axes. The eigenvalues are nonnegative because $\Sigma$ is a covariance matrix. When $\kappa = 0$ the mass is isotropic, every direction is principal, and $\theta$ is arbitrary. $\square$

## Claim 3: a uniform ellipse gives its own angle and half its semi-axes

Take the continuous mass of constant density on the ellipse $E$ with center 0, semi-axes $A \ge B$ and major axis along $(\cos \varphi, \sin \varphi)$. In the coordinates $(s, t)$ of its axes, $E = \{ (s/A)^2 + (t/B)^2 \le 1 \}$. The substitution $s = A \rho \cos \alpha$, $t = B \rho \sin \alpha$ has Jacobian $A B \rho$, so

$$
\int_E s^2 = A^3 B \int_0^1 \rho^3 \, d\rho \int_0^{2\pi} \cos^2 \alpha \, d\alpha = \frac{\pi A^3 B}{4}, \qquad \int_E t^2 = \frac{\pi A B^3}{4}, \qquad \int_E s t = 0,
$$

and the area is $\pi A B$. The covariance in the axis coordinates is $\operatorname{diag}(A^2/4, B^2/4)$. By Claim 2 the computed angle is $\varphi$ (modulo $\pi$, when $A > B$), and the length and width are $A/2$ and $B/2$. On a pixel grid the sums approximate these integrals. $\square$

## Claim 4: the size rule makes the window about twice the target

If the window contains a uniform target of $n$ pixels, each with $P = 255$, and no other mass, then $M_{00} = 255 n$ and $s = 2 \sqrt{M_{00}/256} = 2 \sqrt{n} \sqrt{255/256}$. For a square target of side $\ell$, $n = \ell^2$ and $s$ is just below $2 \ell$; line L8 rounds it up to an odd integer, so the window side is at least $2 \ell \sqrt{255/256}$. A window of side about $2 \ell$ contains the whole target with a margin of $\ell / 2$ on each side, so a target that grows a little is still inside the next window, and the rule settles where the window is about twice the target. $\square$

## Claim 5: the procedure stops

The loop of lines L3 to L7 runs at most $k_{\max}$ times, and each iteration reads a finite window. $\square$

## What is not claimed

Bradski's paper states that mean shift converges. For a disc-shaped window the step is the mean shift step of a flat kernel, which climbs a density estimate with the Epanechnikov kernel, and the argument on the [mean shift tracking](/mean-shift-tracking/) page applies. For the rectangular window used here that argument does not apply directly, and with real centers and a pixel grid the window can stop one pixel short of the centroid of the whole target (see the example on the page). So termination comes from the cap, not from a convergence theorem. Nothing here says that the window covers the target: the back projection is a heuristic score of how target-like each color is.
