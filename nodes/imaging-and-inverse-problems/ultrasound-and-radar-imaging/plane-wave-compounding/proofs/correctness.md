---
title: Coherent plane-wave compounding is linear, equals the sum of the single-angle images, and puts a maximum of height N M at a point scatterer
proves: [correctness]
status: full
---

We prove four facts about the algorithm on the main page (lines L1 to L9) for the pulse-echo model of the page: a linear array on $z = 0$, plane waves that are exact in the medium, point scatterers, constant speed of sound $c$, and no spreading loss or directivity.

**Setting.** Angle $a$ has the tilt $\alpha_a$, $a = 1, \ldots, N$. The wavefront of angle $a$ passes the origin at $t = 0$, so it reaches the point $p = (x, z)$ at $T_a(p) = (z \cos\alpha_a + x \sin\alpha_a)/c$ (line L5). The echo from $p$ reaches element $j$ at $e_j = (x_j, 0)$ after a further $|p - e_j|/c$ (line L2). SAMPLE returns the analytic value $\tilde r_{aj}(t)$ of trace $(a, j)$ with linear interpolation of the baseband samples, and $0$ outside the window. Let $J(p)$ be the set of elements that pass line L7. The complex image is $S(p) = \sum_a \sum_{j \in J(p)} \tilde r_{aj}(T_a(p) + |p - e_j|/c)$ and the output is $|S(p)|$.

**Lemma (the transmit time).** For a plane wave with the unit direction $n_a = (\sin\alpha_a, \cos\alpha_a)$ that passes the origin at time $0$, the time at which it reaches $p$ is $\langle n_a, p \rangle / c = T_a(p)$.

*Proof.* The wavefront at time $t$ is the line $\{p : \langle n_a, p \rangle = c t\}$, because it moves along $n_a$ at speed $c$ and contains the origin at $t = 0$. Solve for $t$. $\square$

With this origin of time, element $j$ fires at $x_j \sin\alpha_a / c$, which is negative for some elements; only the common time origin matters for the image. Adding the receive time gives the delay $\tau = (z \cos\alpha + x \sin\alpha + \sqrt{z^2 + (x - x_j)^2})/c$ of Montaldo et al. (2009).

**Theorem 1 (linearity and decomposition).** $S$ is linear in the data, its exact adjoint spreads each pixel value back with the conjugate weights of SAMPLE, and $S = \sum_a S_a$, where $S_a$ is the image of angle $a$ alone.

*Proof.* Each term is a linear form in one trace with weights that depend only on the geometry. The outer sum over $a$ in L4 adds the per-angle sums, and nothing in the inner loops depends on other angles. The adjoint of a sum of linear forms is the sum of their adjoints. $\square$

So coherent compounding is the same as forming one complex image per angle and adding them. The modulus must come after the sum; adding the moduli is incoherent compounding, a different method.

**Theorem 2 (a point scatterer).** Let the data be exact samples of one scatterer $a_0$ at $p_0 = (x_0, z_0)$, $z_0 > 0$: trace $(a, j)$ holds the echo with the delay $\tau_{aj} = T_a(p_0) + |p_0 - e_j|/c$ and a real envelope $g$ with $|g(s)| \le g(0)$, and SAMPLE reads it without interpolation error. Then

$$S(p) = a_0 \sum_a \sum_{j \in J(p)} g(\Delta_{aj})\, e^{i 2\pi f_0 \Delta_{aj}}, \qquad \Delta_{aj} = T_a(p) - T_a(p_0) + \frac{|p - e_j| - |p_0 - e_j|}{c},$$

$|S(p_0)| = |a_0|\, g(0)\, N\, |J(p_0)|$, and $|S(p)| \le |a_0|\, g(0)\, N\, |J(p)|$ for every $p$. Without an f-number, $|J(p)| = M$, so $p_0$ is a global maximum of the image with the value $N M |a_0| g(0)$.

*Proof.* At the read time $t = T_a(p) + |p - e_j|/c$ the analytic value is $a_0\, g(t - \tau_{aj}) e^{i 2\pi f_0 (t - \tau_{aj})}$, and $t - \tau_{aj} = \Delta_{aj}$. At $p_0$ every $\Delta_{aj}$ is $0$, so all $N |J(p_0)|$ terms equal $a_0 g(0)$. The bound is the triangle inequality with $|g| \le g(0)$. $\square$

We do not prove that the maximum is unique for every geometry. The tests check that the peak is at the scatterer on the grid, for the compounded image and for single tilted waves.

**Theorem 3 (the receive f-number).** With an f-number $F$, line L7 keeps the elements with $|x - x_j| \le z/(2F)$, an aperture of width $z/F$ centered under the pixel. For an array of pitch $d$ the number of elements in the sum is at most $\lfloor z/(F d) \rfloor + 1$, and the set grows with $z$.

*Proof.* The condition defines a closed interval of length $z/F$ that contains the interval for any smaller $z$. An interval of length $L$ holds at most $\lfloor L/d \rfloor + 1$ points of a grid with step $d$. $\square$

In the test, $F = 1.5$ at $z = 6$ mm gives a width of 4 mm and 14 of the 16 elements, and the peak is 14 up to the interpolation loss.

**Theorem 4 (cost).** Each pixel reads $N |J(p)| \le N M$ samples, so an $n \times n$ image costs $O(N M n^2)$ in the real-RAM model, with $O(M)$ extra space for the receive times of line L2. The acquisition needs $N$ firings, against $M$ for full matrix capture.

*Proof.* Lines L4 to L8 run $N |J(p)|$ times per pixel at $O(1)$ each, and L2 runs $M$ times per pixel. $\square$
