---
title: SAFT is linear in the data and focuses a point scatterer to a unique maximum equal to the number of positions in the sum
proves: [correctness]
status: full
---

We prove three facts about SAFT as written on the main page (lines L1 to L10), for the monostatic pulse-echo model: one transducer at the positions $q_k = (x_k, 0)$, $k = 1, \ldots, K$, point scatterers, constant speed of sound $c$, and no spreading loss or beam pattern in the data. These are theorems about that model.

**Setting.** Trace $k$ is a complex baseband signal sampled at $t_0 + q/f_s$. SAMPLE (lines L8 to L10) returns $\tilde r_k(t) = \tilde b_k(t) e^{i 2\pi f_0 t}$ with $\tilde b_k$ the linear interpolation of the samples, and $0$ outside the window. For a pixel $p = (x, z)$, $z > 0$, let $A(p)$ be the set of positions that pass line L4: all $k$ without a half angle, and the $k$ with $|x - x_k| \le z \tan\theta$ with a half angle $\theta$. SAFT returns $I(p) = |S(p)|$ with $S(p) = \sum_{k \in A(p)} \tilde r_k(2 |p - q_k| / c)$.

**Theorem 1 (linearity and the adjoint).** $S$ is linear in the traces. The map that adds $\overline{e^{i 2\pi f_0 t}}\, v$ with the weights $1 - \varphi$ and $\varphi$ to the two samples read for each $k \in A(p)$ is its exact adjoint.

*Proof.* The set $A(p)$ and the read time depend only on the geometry, not on the data. For fixed $p$ and $k$, SAMPLE is a linear form $\sum_q w_q b_k[q]$ with fixed weights, and its adjoint puts $\overline{w_q}\, v$ on sample $q$. Summing over $k \in A(p)$ and over pixels keeps both properties. $\square$

**Theorem 2 (a point scatterer).** Let the traces be exact samples of one scatterer $a$ at $p_0 = (x_0, z_0)$, $z_0 > 0$: $b_k(t) = a\, g(t - \tau_k) e^{-i 2\pi f_0 \tau_k}$ with $\tau_k = 2|p_0 - q_k|/c$, a real envelope with $|g(s)| < g(0)$ for $s \ne 0$, and no interpolation error. Then $S(p) = a \sum_{k \in A(p)} g(\Delta_k) e^{i 2\pi f_0 \Delta_k}$ with $\Delta_k = 2(|p - q_k| - |p_0 - q_k|)/c$, and:

1. $I(p_0) = |a|\, g(0)\, |A(p_0)|$;
2. $I(p) \le |a|\, g(0)\, |A(p)|$ for every $p$;
3. if $A(p)$ holds two positions with different $x_k$, equality in part 2 holds only at $p = p_0$.

*Proof.* At the read time $t = 2|p - q_k|/c$ the analytic value is $a\, g(t - \tau_k) e^{i 2\pi f_0 (t - \tau_k)}$, which gives the sum. At $p_0$ all $\Delta_k$ are $0$. The triangle inequality gives part 2. Equality needs $\Delta_k = 0$ for all $k \in A(p)$, that is $|p - q_k| = |p_0 - q_k|$. For two positions with $x_1 \ne x_2$, subtracting the two squared equations gives $2(x_2 - x_1)(x - x_0) = 0$, so $x = x_0$, and then $z = z_0$ because both are positive. $\square$

Without a half angle, $A(p)$ is all $K$ positions, so the peak is $K |a|\, g(0)$, the unique maximum. The test with $K = 21$ measures $20.886$, the loss coming from the interpolation.

**Theorem 3 (no grating lobe for a step of at most a quarter wavelength).** Consider a narrowband far-field point at the direction $u_0 = \sin\theta_0$ seen from the center of the scan and a pixel at the same range in the direction $u$. Under the far-field approximation $|p - q_k| \approx R - x_k u$, the terms of the sum have the phase $e^{-i 2\pi (2 d / \lambda) k (u - u_0)}$ for a step $d$ between positions. This is the beam pattern of a uniform linear array with the spacing $2d$ in units of the wavelength. By the grating lobe theorem of [delay-and-sum beamforming](/delay-and-sum-beamforming/) with $d$ replaced by $2d$, there is no grating lobe for any $u_0$ when $2d \le \lambda/2$, that is $d \le \lambda/4$, and for $u_0 = 0$ there is none when $2d < \lambda$.

*Proof.* With $|p - q_k| - |p_0 - q_k| \approx -x_k (u - u_0)$ and $x_k = k d$ plus a constant, $2\pi f_0 \Delta_k = -2\pi (2 d/\lambda) k (u - u_0)$ plus a constant phase, which is the steered array factor of a uniform line with spacing $2d$. $\square$

The factor 2 comes from the two-way path: moving the transducer by $d$ changes the path by up to $2d$.

**Cost.** Lines L3 to L6 run at most $K$ times per pixel, so an $n \times n$ image costs $O(K n^2)$ in the real-RAM model, and the extra space is $O(1)$ per pixel besides the $K T$ samples of data.
