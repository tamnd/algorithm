---
title: MOC solves each segment exactly for a flat source, conserves particles in every iteration, contracts by about the scattering ratio, and reduces to the exact slab flux for a long strip
proves: [correctness]
status: full
---

We assume exact arithmetic. The rectangle, the cells, the tracks and the lines L1 to L9 are those of the page. Every cell $i$ has the area $A_i$, $\Sigma_{t,i} > 0$ and $0 \le \Sigma_{s,i} \le c\,\Sigma_{t,i}$, and all faces are vacuum. A direction is a track direction $\alpha$ with the azimuthal weight $w_\alpha = \pi/n_a$ and a polar cosine $\mu_p$ with the weight $w_p$, where the $w_p$ sum to 2 and $\sin\theta_p = \sqrt{1 - \mu_p^2}$. The weights of all directions sum to $2n_a \cdot (\pi/n_a) \cdot 2 = 4\pi$. A track of the angle $\alpha$ carries the spacing $\delta_\alpha$, and it is cut into segments, one for each cell that it crosses, of the in-plane lengths $\ell$.

## One segment

**Lemma 1 (the segment solve is exact).** Let a segment of in-plane length $\ell$ lie in cell $i$, with the emission density $Q_i$ per steradian. Along the direction with the polar angle $\theta$, the transport equation is $\sin\theta\,d\psi/ds + \Sigma_t\psi = Q$ in the in-plane distance $s$. Its solution from the entering value $\psi_{\mathrm{in}}$ is
$$\psi(s) = \frac{Q}{\Sigma_t} + \left(\psi_{\mathrm{in}} - \frac{Q}{\Sigma_t}\right)e^{-\Sigma_ts/\sin\theta},$$
so line L6 gives the exact leaving value $\psi_{\mathrm{out}} = \psi(\ell)$, and the mean of $\psi$ over the segment is $\bar\psi = Q/\Sigma_t + (\psi_{\mathrm{in}} - \psi_{\mathrm{out}})/\tau$ with $\tau = \Sigma_t\ell/\sin\theta$.

*Proof.* A 3D path that makes the angle $\theta$ with the $z$ axis covers the in-plane distance $s$ over the path length $s/\sin\theta$, so the streaming term $\Omega\cdot\nabla\psi$ is $\sin\theta\,d\psi/ds$. The formula solves this linear equation with the initial value $\psi_{\mathrm{in}}$. Integrating it over $[0, \ell]$ gives $\ell\,\bar\psi = \ell Q/\Sigma_t + (\psi_{\mathrm{in}} - Q/\Sigma_t)(1 - e^{-\tau})\ell/\tau$, and $(\psi_{\mathrm{in}} - Q/\Sigma_t)(1 - e^{-\tau}) = \psi_{\mathrm{in}} - \psi_{\mathrm{out}}$. $\square$

In line L6, $\Delta\psi = (\psi - Q/\Sigma_t)(1 - e^{-\tau})$ is $\psi_{\mathrm{in}} - \psi_{\mathrm{out}}$, and $\psi \leftarrow \psi - \Delta\psi$ is $\psi_{\mathrm{out}}$. Since $0 < 1 - e^{-\tau} < 1$, $\psi_{\mathrm{out}}$ lies between $\psi_{\mathrm{in}}$ and $Q/\Sigma_t$.

**Lemma 2 (the segments are correct).** The cut points of a track are its entry and exit points and all its crossings with the inner grid lines. So each open interval between two cut points lies in one cell, the cell of its midpoint, and the segments of a track partition its chord.

*Proof.* A line meets each grid line at most once (or lies on it, which a track with $\sin\alpha > 0$ and offset at a midpoint does only with measure zero, and then the cut test treats it as not crossing). Between two consecutive cut points the track crosses no grid line, so it stays in one cell. $\square$

## The cell flux and the balance

Let $\Phi_i$ be the sum over the directions and the segments in cell $i$ of $w_\alpha w_p\delta_\alpha\ell\,\bar\psi$, which is the quadrature for $\int_{A_i}\int\psi\,d\Omega\,dA$: the tracks of each direction sample the cell with the spacing $\delta_\alpha$, and each segment contributes the area $\delta_\alpha\ell$. Let $a_i = \frac{1}{4\pi A_i}\sum w_\alpha w_p\delta_\alpha\ell$ be the ratio of the track area of cell $i$ to its true area, averaged over the directions.

**Lemma 3 (line L8).** Line L8 is
$$\phi_i = \frac{\Phi_i}{A_i} + (1 - a_i)\,\frac{4\pi Q_i}{\Sigma_{t,i}}.$$
So it is the quadrature average of the angular flux, with the track area replaced by the true area in the flat-source part. If $a_i = 1$, $\phi_i = \Phi_i/A_i$.

*Proof.* The tally of line L6 adds $w_\alpha w_p\delta_\alpha\sin\theta_p(\psi_{\mathrm{in}} - \psi_{\mathrm{out}})$ for each segment. By Lemma 1, $\sin\theta(\psi_{\mathrm{in}} - \psi_{\mathrm{out}}) = \sin\theta\,\tau(\bar\psi - Q/\Sigma_t) = \Sigma_t\ell(\bar\psi - Q/\Sigma_t)$. So the tally of cell $i$ is $\Sigma_{t,i}\Phi_i - Q_i\cdot 4\pi A_ia_i$, and line L8 gives $4\pi Q_i/\Sigma_{t,i} + \Phi_i/A_i - 4\pi a_iQ_i/\Sigma_{t,i}$. $\square$

**Theorem 4 (balance in every iteration).** Let $\phi$ be the old iterate, $Q_i = (\Sigma_{s,i}\phi_i + q_i)/(4\pi)$, and $\phi'$ the new iterate with the leakage $\Lambda$ of line L7. Then
$$\sum_i\left(\Sigma_{t,i}\phi'_i - \Sigma_{s,i}\phi_i - q_i\right)A_i + \Lambda = 0 .$$
At convergence ($\phi' = \phi$) this is the exact balance $\sum_i\Sigma_{a,i}\phi_iA_i + \Lambda = \sum_iq_iA_i$, for any track spacing and any quadrature.

*Proof.* By line L8, $(\Sigma_{t,i}\phi'_i - 4\pi Q_i)A_i$ is the tally of cell $i$. The sum of the tallies over all cells is the sum over all tracks and directions of $w_\alpha w_p\delta_\alpha\sin\theta_p$ times the sum of $\psi_{\mathrm{in}} - \psi_{\mathrm{out}}$ over the segments of the track. This telescopes to the value entering the domain, 0 for vacuum, minus the value leaving it. Line L7 adds $w_\alpha w_p\delta_\alpha\sin\theta_p$ times the leaving value into $\Lambda$, so the sum of the tallies is $-\Lambda$. Finally $4\pi Q_i = \Sigma_{s,i}\phi_i + q_i$. $\square$

The weight $w_\alpha w_p\delta_\alpha\sin\theta_p\,\psi$ of a leaving track is the quadrature of the outgoing current $\int\Omega\cdot n\,\psi\,d\Omega$ over the face: a track bundle of the width $\delta_\alpha$ crosses a face of the length $\delta_\alpha/|\cos\beta|$, where $\beta$ is the angle between the track and the normal, and $\Omega\cdot n = \sin\theta\cos\beta$.

## Convergence of the source iteration

**Theorem 5 (contraction).** Let $\varepsilon = \max_i\max(0, a_i - 1)$. Then the iteration of lines L3 to L8 is a contraction in the maximum norm with the factor at most $c(1 + 2\varepsilon)$. So for $c(1 + 2\varepsilon) < 1$ the iterates converge to the unique fixed point from every start.

*Proof.* The map $\phi \mapsto \phi'$ is affine, and its linear part sends an error $e$ to the result $e'$ of lines L4 to L8 with $q = 0$ and $Q_i = \Sigma_{s,i}e_i/(4\pi)$. Let $m = \max_i|Q_i|/\Sigma_{t,i} \le c\max_i|e_i|/(4\pi)$. Each track enters with 0, and by Lemma 1 each leaving value lies between the entering value and $Q/\Sigma_t$; by induction along the track, $|\psi| \le m$ on every segment, and so $|\bar\psi| \le m$ as a mean of $\psi$. By Lemma 3,
$$|e'_i| \le \frac{|\Phi_i|}{A_i} + |1 - a_i|\,4\pi m \le \left(a_i + |1 - a_i|\right)4\pi m,$$
since the weights in $\Phi_i/A_i$ sum to $4\pi a_i$. If $a_i \le 1$ the factor is 1, and otherwise it is $2a_i - 1 \le 1 + 2\varepsilon$. So $\max_i|e'_i| \le c(1 + 2\varepsilon)\max_i|e_i|$. The Banach fixed-point theorem gives the rest. $\square$

With a pure absorber ($c = 0$) the second iteration repeats the first, so line L9 stops after 2 iterations, as the tests check. In the tests the track areas of single angles differ from the true areas by at most $0.4$ percent, so $\varepsilon \le 0.004$.

## The long strip

**Theorem 6 (the slab limit).** Consider a purely absorbing slab $0 \le x \le L$, infinite in $y$ and $z$, with a uniform source $q$ and vacuum faces. Its exact scalar flux is
$$\phi(x) = \frac{q}{2\Sigma_t}\left(2 - E_2(\Sigma_tx) - E_2(\Sigma_t(L - x))\right), \qquad E_2(a) = \int_1^\infty\frac{e^{-at}}{t^2}\,dt .$$

*Proof.* With $Q = q/(4\pi)$ and no scattering, the flux along a direction with the cosine $\mu$ to the $x$ axis is the uncollided flux from the entering face: for $\mu > 0$, $\psi = (Q/\Sigma_t)(1 - e^{-\Sigma_tx/\mu})$, and for $\mu < 0$ the same with $L - x$ and $|\mu|$, by Lemma 1 along the straight path. Then $\phi = 2\pi\int_{-1}^1\psi\,d\mu$, and $\int_0^1 e^{-a/\mu}\,d\mu = E_2(a)$ by the substitution $t = 1/\mu$. $\square$

The cell averages follow from $\int E_2(\Sigma_tx)\,dx = -E_3(\Sigma_tx)/\Sigma_t$ and $E_3(a) = (e^{-a} - aE_2(a))/2$. For the rectangle of the tests, which is 20 mean free paths tall, every point of the middle row of cells is at least 8 mean free paths from the top and bottom faces, so the particles that these faces remove change the flux there by less than $e^{-8} q/\Sigma_t \approx 3.4 \times 10^{-4}$ (the uncollided flux along a path longer than 8 mean free paths). The remaining difference between MOC and Theorem 6 is the error of the angular quadrature and of the track spacing, which the page measures.
