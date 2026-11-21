---
title: Correctness of fan-beam filtered back-projection
proves: [correctness]
status: full
---

We use the conventions of the page. $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$. The Radon transform is $p(\theta, s) = \mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$, now for all $\theta \in \mathbb{R}$, so that $p(\theta + \pi, -s) = p(\theta, s)$. The source at the angle $\beta$ is $S(\beta) = D\,\omega^\perp(\beta)$. The ray with the fan angle $\gamma$ is the line $(\theta, s) = (\beta + \gamma, D\sin\gamma)$, and $g(\beta, \gamma) = p(\beta + \gamma, D\sin\gamma)$.

Throughout, $f \in C^2_c(\mathbb{R}^2)$ has its support in the disk $|x| \le r$ with $r < D$, and $x$ is a point with $|x| < D$. We write $\ell(\beta)$ and $\gamma'(\beta)$ for the distance from $S(\beta)$ to $x$ and the fan angle of the ray through $x$:
$$\ell\cos\gamma' = D - x\cdot\omega^\perp(\beta), \qquad \ell\sin\gamma' = x\cdot\omega(\beta).$$
The page calls $\ell$ by the name $L$.

The proof has five parts. Part 1 writes the parallel-beam inversion formula with a finite-part integral, which is an honest function integral. Part 2 is a lemma on how a finite part behaves under a change of the cut. Part 3 changes the variables from parallel to fan coordinates and proves the fan-beam formula for both detectors. Part 4 proves the short-scan formula with Parker's weights. Part 5 names the approximations of the discrete algorithm.

## Part 1. The ramp filter as a finite part

Let $h$ be the ramp filter, the distribution with the Fourier transform $|\sigma|$. For $q \in C^2_c(\mathbb{R})$ put
$$(h * q)(s) = -\frac{1}{2\pi^2}\int_0^\infty \frac{q(s + v) + q(s - v) - 2q(s)}{v^2}\,dv.$$
The integrand is bounded near $v = 0$, because $q(s + v) + q(s - v) - 2q(s) = O(v^2)$, and it is $O(v^{-2})$ at infinity. So the integral converges. For $q(s) = e^{2\pi i \sigma s}$ the numerator is $2e^{2\pi i\sigma s}(\cos(2\pi\sigma v) - 1)$, and $\int_0^\infty (\cos(cv) - 1)v^{-2}\,dv = -\pi|c|/2$. So the formula multiplies $e^{2\pi i\sigma s}$ by $|\sigma|$, and by Fourier inversion it is the ramp filter on $C^2_c$. The theorem of the page [filtered back-projection](/filtered-back-projection/) gives
$$f(x) = \int_0^\pi (h * p(\theta, \cdot))(x\cdot\omega(\theta))\,d\theta = \frac{1}{2}\int_0^{2\pi} (h * p(\theta, \cdot))(x\cdot\omega(\theta))\,d\theta. \tag{1}$$
The second form holds because $p(\theta + \pi, -s) = p(\theta, s)$ and $h * q$ commutes with the reflection $s \mapsto -s$.

For $\epsilon > 0$ the integral in the definition splits as
$$(h * q)(s) = -\frac{1}{2\pi^2}\lim_{\epsilon \to 0}\left(\int_{|s - u| > \epsilon} \frac{q(u)}{(s - u)^2}\,du - \frac{2q(s)}{\epsilon}\right), \tag{2}$$
since $\int_\epsilon^\infty 2q(s)v^{-2}\,dv = 2q(s)/\epsilon$. The error of the bracket against its limit is at most $\epsilon \sup|q''|$.

## Part 2. A lemma on the cut

**Lemma 1.** Let $\psi$ be a function on an interval $I$ with a Lipschitz derivative, with compact support in $I$, let $t_0$ be inside $I$, and let $c$ be a positive $C^2$ function on $I$. Then, as $\epsilon \to 0$,
$$\int_{\{t \in I \,:\, c(t)|t - t_0| > \epsilon\}} \frac{\psi(t)}{(t - t_0)^2}\,dt = \frac{2c(t_0)\psi(t_0)}{\epsilon} + \mathrm{FP}\!\int \frac{\psi(t)}{(t - t_0)^2}\,dt + O(\epsilon),$$
where $\mathrm{FP}\int \psi(t)(t - t_0)^{-2}\,dt = \int_0^\infty (\psi(t_0 + v) + \psi(t_0 - v) - 2\psi(t_0))v^{-2}\,dv$. The constant in $O(\epsilon)$ depends only on bounds for $\psi$, its Lipschitz constant, $1/c$ and the first two derivatives of $c$ near $t_0$.

*Proof.* For small $\epsilon$ the set where $c(t)|t - t_0| \le \epsilon$ near $t_0$ is an interval $[t_0 - e_-, t_0 + e_+]$, where $e_\pm\,c(t_0 \pm e_\pm) = \epsilon$. Put $c_0 = c(t_0)$ and $c_1 = c'(t_0)$. Taylor expansion gives $e_\pm = \epsilon/c_0 \mp c_1\epsilon^2/c_0^3 + O(\epsilon^3)$, so $e_+ + e_- = 2e + O(\epsilon^3)$ with $e = \epsilon/c_0$. The left side is
$$\int_{e_+}^\infty \frac{\psi(t_0 + v)}{v^2}\,dv + \int_{e_-}^\infty \frac{\psi(t_0 - v)}{v^2}\,dv = \int_e^\infty \frac{\psi(t_0 + v) + \psi(t_0 - v)}{v^2}\,dv - \int_e^{e_+} \frac{\psi(t_0 + v)}{v^2}\,dv - \int_e^{e_-} \frac{\psi(t_0 - v)}{v^2}\,dv.$$
The last two integrals are over intervals of length $O(\epsilon^2)$ where $v^{-2} = e^{-2}(1 + O(\epsilon))$ and $\psi = \psi(t_0) + O(\epsilon)$. Their sum is $\psi(t_0)(e_+ + e_- - 2e)/e^2 + O(\epsilon) = O(\epsilon)$. The first integral is $2\psi(t_0)/e$ plus $\int_e^\infty (\psi(t_0 + v) + \psi(t_0 - v) - 2\psi(t_0))v^{-2}\,dv$. The integrand of the last integral is bounded, so it differs from the full finite part by $O(e) = O(\epsilon)$. Since $2\psi(t_0)/e = 2c_0\psi(t_0)/\epsilon$, the lemma follows. $\square$

The point of the lemma is that a cut which is not symmetric to first order still gives the same finite part, and only the size of the singular term changes.

## Part 3. The fan-beam formula

Let $t$ be a detector coordinate: $t = \gamma$ for the equiangular detector, or $t = D\tan\gamma$ for the flat detector. In both cases $\gamma$ is a smooth increasing function of $t$ on the range of $t$, and the map
$$\Phi: (\beta, t) \mapsto (\theta, s) = (\beta + \gamma(t),\ D\sin\gamma(t))$$
from $[0, 2\pi) \times T$ to $[0, 2\pi) \times (-D, D)$, with $\theta$ taken modulo $2\pi$, is a bijection. Given $(\theta, s)$, the only solution is $\gamma = \arcsin(s/D)$ and $\beta = \theta - \gamma$. Its Jacobian is $J = D\cos\gamma\,\gamma'(t)$, where $\gamma'(t)$ is the derivative of $\gamma$ in $t$. The lines with $|s| \ge D$ miss the support of $f$, so they add nothing to (1).

**Lemma 2 (the distance to the ray).** $x\cdot\omega(\beta + \gamma) - D\sin\gamma = \ell\sin(\gamma' - \gamma)$.

*Proof.* Expand $\omega(\beta + \gamma) = \cos\gamma\,\omega(\beta) + \sin\gamma\,\omega^\perp(\beta)$. Then $x\cdot\omega(\beta + \gamma) - D\sin\gamma = \cos\gamma\,(x\cdot\omega(\beta)) - \sin\gamma\,(D - x\cdot\omega^\perp(\beta)) = \ell(\sin\gamma'\cos\gamma - \cos\gamma'\sin\gamma)$. $\square$

So $x\cdot\omega(\theta) - s = c(\beta, t)\,(t_x - t)$ with a positive smooth factor $c$, where $t_x = t_x(\beta)$ is the detector coordinate of the ray through $x$. For the equiangular detector, $t_x = \gamma'$ and $c = \ell\sin(\gamma' - \gamma)/(\gamma' - \gamma)$, with $c = \ell$ at $\gamma = \gamma'$. For the flat detector, $\sin(\gamma' - \gamma) = \cos\gamma'\cos\gamma\,(\tan\gamma' - \tan\gamma)$, and with $U = (D - x\cdot\omega^\perp(\beta))/D = \ell\cos\gamma'/D$ and $t_x = D\,x\cdot\omega(\beta)/(D - x\cdot\omega^\perp(\beta))$ this gives $c = DU/\sqrt{D^2 + t^2}$.

**Lemma 3 (the angle of the ray through $x$).** The direction $\theta_x(\beta) = \beta + \gamma'(\beta)$ of the ray through $x$ satisfies $\theta_x' = J/c$ at $t = t_x$, and $\theta_x' > 0$.

*Proof.* Put $\phi(\beta, t) = x\cdot\omega(\theta) - s$ with $(\theta, s) = \Phi(\beta, t)$, so $\phi = c\,(t_x - t)$. The map $(\beta, t) \mapsto (\theta, \phi)$ is $\Phi$ followed by $(\theta, s) \mapsto (\theta, x\cdot\omega(\theta) - s)$, whose Jacobian is $-1$. So its Jacobian is $-J$. On the curve $t = t_x(\beta)$ we have $\phi = 0$, $\partial_t\phi = -c$, and $\partial_\beta\phi + \partial_t\phi\,t_x' = 0$, so $\partial_\beta\phi = c\,t_x'$. Then $\det \partial(\theta, \phi)/\partial(\beta, t) = \partial_\beta\theta\,\partial_t\phi - \partial_t\theta\,\partial_\beta\phi = -c\,(\partial_\beta\theta + \partial_t\theta\,t_x') = -c\,\theta_x'$. Hence $J = c\,\theta_x'$. Both $J$ and $c$ are positive. $\square$

The lemma also has a direct meaning. The source moves with the speed $D$, and the part of its velocity normal to the ray is $D\cos\gamma'$. The ray turns about $x$ at the rate $D\cos\gamma'/\ell$, and this is $J/c$ for the equiangular detector.

**Theorem 1 (fan-beam inversion).** With the notation above, put $\psi(\beta, t) = g(\beta, \gamma(t))\,J(t)/c(\beta, t)^2$. Then
$$f(x) = \frac{1}{2}\int_0^{2\pi} (h * \psi(\beta, \cdot))(t_x(\beta))\,d\beta.$$
For the equiangular detector this is
$$f(x) = \int_0^{2\pi} \frac{1}{\ell^2}\int \kappa(\gamma' - \gamma)\,D\cos\gamma\,g(\beta, \gamma)\,d\gamma\,d\beta, \qquad \kappa(u) = \frac{1}{2}\left(\frac{u}{\sin u}\right)^2 h(u),$$
and for the flat detector it is
$$f(x) = \frac{1}{2}\int_0^{2\pi} \frac{1}{U^2}\int h(t_x - t)\,\frac{D}{\sqrt{D^2 + t^2}}\,g(\beta, t)\,dt\,d\beta.$$
Here the inner integrals mean the action of the distribution $h$, given by the finite part of Part 1, on a function with a Lipschitz derivative.

*Proof.* Put (2) into (1) and move the limit outside, which is allowed because the error in (2) is uniform in $\theta$:
$$f(x) = -\frac{1}{4\pi^2}\lim_{\epsilon \to 0}\left(\iint_{|x\cdot\omega - s| > \epsilon} \frac{p(\theta, s)}{(x\cdot\omega - s)^2}\,ds\,d\theta - \frac{2}{\epsilon}\int_0^{2\pi} p(\theta, x\cdot\omega(\theta))\,d\theta\right).$$
In the first integral the integrand is bounded on the domain, so the change of variables $\Phi$ is allowed. It gives
$$\int_0^{2\pi}\int_{c\,|t_x - t| > \epsilon} \frac{g(\beta, \gamma(t))\,J}{c^2\,(t_x - t)^2}\,dt\,d\beta = \int_0^{2\pi}\int_{c\,|t_x - t| > \epsilon} \frac{\psi(\beta, t)}{(t - t_x)^2}\,dt\,d\beta.$$
By Lemma 1, applied for each $\beta$ with bounds uniform in $\beta$, the inner integral is $2c\psi/\epsilon + \mathrm{FP}\int\psi\,(t - t_x)^{-2}\,dt + O(\epsilon)$ with $c\psi = gJ/c$ taken at $t = t_x$. In the second integral substitute $\theta = \theta_x(\beta)$. By Lemma 3 this map is increasing, it covers $[0, 2\pi)$ once modulo $2\pi$, and $d\theta = (J/c)\,d\beta$. Also $p(\theta_x, x\cdot\omega(\theta_x)) = g(\beta, \gamma(t_x))$, because both are the integral over the ray through $x$. So
$$\frac{2}{\epsilon}\int_0^{2\pi} p(\theta, x\cdot\omega(\theta))\,d\theta = \frac{2}{\epsilon}\int_0^{2\pi} \left.\frac{gJ}{c}\right|_{t = t_x}\,d\beta,$$
which cancels the singular term of Lemma 1. What remains is $f(x) = -\frac{1}{4\pi^2}\int_0^{2\pi}\mathrm{FP}\int\psi(\beta, t)(t - t_x)^{-2}\,dt\,d\beta$, and $-\frac{1}{2\pi^2}\mathrm{FP}$ is $h *$ by Part 1. This is the first formula.

For the equiangular detector, $J = D\cos\gamma$ and $1/c^2 = \ell^{-2}w(\gamma' - \gamma)$ with $w(u) = (u/\sin u)^2$, a smooth even function with $w(0) = 1$. So $\psi = \ell^{-2}w(\gamma' - \gamma)\,D\cos\gamma\,g$. Since $\ell$ does not depend on $\gamma$ and $w$ is smooth, $h * \psi$ at $\gamma'$ is $\ell^{-2}$ times the action of the distribution $w h$ on $D\cos\gamma\,g$, and $\frac{1}{2}wh = \kappa$. For the flat detector, $\gamma(t) = \arctan(t/D)$, so $J = D\cos\gamma \cdot D/(D^2 + t^2) = D^3/(D^2 + t^2)^{3/2}$ and $J/c^2 = D/(U^2\sqrt{D^2 + t^2})$. Here $U$ does not depend on $t$. $\square$

The second formula is the one that lines L4 and L5 of the algorithm compute. Line L4 forms $D\cos\gamma\,g$, line L5 applies the kernel $\kappa$, and line L8 divides by $\ell^2$, the squared distance from the source. The function `fan_beam_fbp_flat` computes the third formula with the kernel $h/2$.

## Part 4. Short scan with Parker's weights

The ray $(\beta, \gamma)$ and the ray $(\beta + \pi + 2\gamma, -\gamma)$ are the same line, because $(\beta + \pi + 2\gamma) + (-\gamma) = (\beta + \gamma) + \pi$ and $D\sin(-\gamma) = -D\sin\gamma$.

**Lemma 4 (weights).** Let $W(\theta, s)$ be a function with a Lipschitz derivative and $W(\theta, s) + W(\theta + \pi, -s) = 1$ on the support of $p$. Then $f(x) = \int_0^{2\pi} (h * (W p)(\theta, \cdot))(x\cdot\omega(\theta))\,d\theta$.

*Proof.* Split $[0, 2\pi)$ into $[0, \pi)$ and $[\pi, 2\pi)$ and substitute $\theta \mapsto \theta + \pi$ in the second part. Since $h$ is even, $(h * (Wp)(\theta + \pi, \cdot))(-x\cdot\omega(\theta)) = \int h(x\cdot\omega - s)\,W(\theta + \pi, -s)\,p(\theta, s)\,ds$. The two parts add to $\int_0^\pi (h * p(\theta, \cdot))(x\cdot\omega)\,d\theta$, which is $f(x)$ by (1). $\square$

**Lemma 5 (Parker's weights add to 1).** Let $0 < \delta < \pi/2$ and $|\gamma| < \delta$. Define $w(\beta, \gamma)$ for $\beta \in [0, \pi + 2\delta]$ by $\sin^2(\frac{\pi}{4}\frac{\beta}{\delta - \gamma})$ for $\beta < 2(\delta - \gamma)$, by 1 for $2(\delta - \gamma) \le \beta \le \pi - 2\gamma$, and by $\sin^2(\frac{\pi}{4}\frac{\pi + 2\delta - \beta}{\delta + \gamma})$ for $\beta > \pi - 2\gamma$, and put $w = 0$ for the other $\beta$ modulo $2\pi$. Then the weights of the two copies of each line add to 1.

*Proof.* There are three cases. If $\beta < 2(\delta - \gamma)$, the copy $\beta^* = \beta + \pi + 2\gamma$ lies in $(\pi + 2\gamma, \pi + 2\delta)$, which is the last region for the fan angle $-\gamma$. Its weight is $\sin^2(\frac{\pi}{4}\frac{2(\delta - \gamma) - \beta}{\delta - \gamma}) = \cos^2(\frac{\pi}{4}\frac{\beta}{\delta - \gamma})$, and the sum is 1. If $2(\delta - \gamma) \le \beta \le \pi - 2\gamma$, then $\beta + \pi + 2\gamma \ge \pi + 2\delta$ and $\beta - \pi + 2\gamma \le 0$, so the other copy is outside the scan or on its edge, where the weight is 0. If $\beta > \pi - 2\gamma$, the copy $\beta^* = \beta - \pi + 2\gamma$ lies in $(0, 2(\delta + \gamma)]$, the first region for $-\gamma$, and its argument and the argument of $w(\beta, \gamma)$ add to $\frac{\pi}{4}\cdot\frac{2\delta + 2\gamma}{\delta + \gamma} = \frac{\pi}{2}$. Again the sum is 1. $\square$

The weight is continuous with a continuous derivative in $\beta$. The derivative of $\sin^2(\frac{\pi}{4}u)$ at $u = 0$ and $u = 2$ is 0, which joins the pieces. If the support of $f$ lies in $|x| \le r$ with $D\sin\delta > r$, only fan angles with $|\gamma| \le \arcsin(r/D) < \delta$ carry data, and there the weight has a Lipschitz derivative in $(\beta, \gamma)$.

**Theorem 2 (short scan).** Under these conditions,
$$f(x) = \int_0^{\pi + 2\delta} \frac{1}{\ell^2}\int 2\kappa(\gamma' - \gamma)\,D\cos\gamma\,w(\beta, \gamma)\,g(\beta, \gamma)\,d\gamma\,d\beta.$$

*Proof.* Take $W$ as the Parker weight, written in parallel coordinates through $\Phi$. Lemma 5 gives the hypothesis of Lemma 4. Then repeat Part 3 with $Wp$ in place of $p$ and without the factor $\frac{1}{2}$ of (1). The weight is 0 for $\beta \notin [0, \pi + 2\delta]$. $\square$

This is the factor 2 that the function `_angles` returns for the short scan.

## Part 5. What the discrete algorithm approximates

Line L2 replaces $h$ by the ramp band-limited to $1/(2\alpha)$ and sampled at $m\alpha$, which gives the values $\kappa(m\alpha) = \frac{1}{2}(m\alpha/\sin m\alpha)^2 h_B(m\alpha)$: $1/(8\alpha^2)$ at $m = 0$, 0 at even $m$, and $-1/(2\pi^2\sin^2(m\alpha))$ at odd $m$. The values come from Lemma 2 of the filtered back-projection proof. Line L5 replaces the integral over $\gamma$ by the sum with step $\alpha$, line L8 reads the filtered projection at $\gamma'$ by linear interpolation, and line L9 replaces the integral over $\beta$ by the rectangle rule with step $2\pi/a$. For a full scan the integrand is periodic in $\beta$, so this is the trapezoidal rule. These are the only approximations. They are the same as in parallel-beam FBP, with one difference: the factor $(u/\sin u)^2$ makes the band limit in $\gamma$ only approximately a band limit in $s$, so Lemma 3 of the parallel proof (exact discrete filtering) does not carry over exactly. The page reports the error of these approximations as a measurement.
