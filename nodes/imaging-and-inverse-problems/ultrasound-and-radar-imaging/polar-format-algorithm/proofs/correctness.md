---
title: Under the plane-wave model the dechirped data are the scene's 2D Fourier transform on a polar raster, so exact regridding and an inverse DFT recover the scene
proves: [correctness]
status: full
---

We prove four facts about the polar format algorithm as written on the main page (lines L1 to L4). Theorems 1 to 3 are exact under the plane-wave approximation and with exact interpolation in L1 and L2. Theorem 4 is an exact expansion of the range without the plane-wave approximation and shows which term the algorithm ignores; its effect on a given image is a measurement, reported on the main page.

**Setting.** Pulse $m$ is sent from $a_m = -R_c(\sin\theta_m, \cos\theta_m)$. A point target of amplitude $a$ at $p = (x, y)$ has the relative range $\Delta R_m = |a_m - p| - R_c$. After dechirp against the scene center, sample $n$ of pulse $m$ is $a\, e^{-i u_n \Delta R_m}$ with $u_n = 4\pi f_n / c$, and the data of several targets add. The Fourier sign is $e^{-i 2\pi f t}$. Write $\hat\sigma(k_x, k_y) = \sum a\, e^{-i (k_x x + k_y y)}$ over the targets. The Cartesian grid has the rows $k_{y,i} = k_{y,0} + i\, \Delta k_y$ for $0 \le i < N$ and the columns $k_{x,j} = k_{x,0} + j\, \Delta k_x$ for $0 \le j < M$, all inside the polar sector, and the pixels are $y_q = (q - N/2)\, 2\pi/(N \Delta k_y)$ and $x_r = (r - M/2)\, 2\pi/(M \Delta k_x)$.

**Theorem 1 (linearity).** The output of L1 to L4 is linear in the data.

*Proof.* L1 and L2 are weighted sums with weights fixed by the geometry, L3 is an inverse DFT and a fixed permutation, and L4 is a product with fixed numbers. $\square$

**Theorem 2 (polar samples of the Fourier transform).** Under the plane-wave approximation $\Delta R_m = x \sin\theta_m + y \cos\theta_m$, the data are $d[m][n] = \hat\sigma(u_n \sin\theta_m, u_n \cos\theta_m)$, the transform of the scene at radius $u_n$ and angle $\theta_m$ from the $k_y$ axis.

*Proof.* For one target, $u_n \Delta R_m = (u_n \sin\theta_m) x + (u_n \cos\theta_m) y$, so $a\, e^{-i u_n \Delta R_m} = a\, e^{-i (k_x x + k_y y)}$ at $(k_x, k_y) = u_n(\sin\theta_m, \cos\theta_m)$. Sum over the targets. $\square$

This is the Fourier slice theorem for this geometry: each pulse is a band of the radial line of $\hat\sigma$ at its own angle.

**Theorem 3 (regridding and focus).** Assume Theorem 2 and that L1 and L2 return the exact values of the functions they interpolate. Then $G[i][j] = \hat\sigma(k_{x,j}, k_{y,i})$, and the image of L4 at the pixel $(x_r, y_q)$ is
$$\sum a\, D_N\big(\Delta k_y (y_q - y)\big)\, D_M\big(\Delta k_x (x_r - x)\big), \qquad D_L(t) = \sum_{l} e^{i l t},$$
where $l$ runs over the $L$ integers from $-L/2$ to $L/2 - 1$, up to a phase factor of modulus one that is 1 when $(x, y)$ is a pixel. In particular a target at a pixel gives exactly $N M a$ there.

*Proof.* The point of the radial line at angle $\theta_m$ with $k_y = k_{y,i}$ has radius $k_{y,i}/\cos\theta_m$, so L1 gives $R[m][i] = \hat\sigma(k_{y,i} \tan\theta_m, k_{y,i})$. For a fixed row these are values of the smooth function $k_x \mapsto \hat\sigma(k_x, k_{y,i})$ at the points $k_x = k_{y,i}\tan\theta_m$, the angle $\theta = \operatorname{atan2}(k_x, k_{y,i})$ is a one-to-one parameter of the row, and L2 reads the row at the angle of $k_{x,j}$, which gives $\hat\sigma(k_{x,j}, k_{y,i})$. For one target, $G[i][j] = a\, e^{-i (k_{x,0} x + k_{y,0} y)}\, e^{-i (j \Delta k_x x + i \Delta k_y y)}$. The inverse DFT of L3 divides by $N M$ and multiplies by $e^{+i 2\pi (i q' / N + j r' / M)}$, and the fftshift sets $q' = q - N/2$ and $r' = r - M/2$, so $2\pi i q'/N = i\, \Delta k_y\, y_q$ and $2\pi j r'/M = j\, \Delta k_x\, x_r$. The sum over $i$ and $j$ is a product of two geometric sums, $\sum_i e^{i\, i \Delta k_y (y_q - y)}$ and $\sum_j e^{i\, j \Delta k_x (x_r - x)}$; shifting the index to center it gives $D_N$ and $D_M$ times a phase of modulus one that is 1 when $y = y_q$ and $x = x_r$. L4 multiplies by $N M$ and by $e^{i (k_{y,0} y_q + k_{x,0} x_r)}$; when $(x, y) = (x_r, y_q)$ this cancels $e^{-i (k_{x,0} x + k_{y,0} y)}$, and $D_N(0) D_M(0) = N M$. By Theorem 1 the targets add. $\square$

**Theorem 4 (the term that the algorithm ignores).** Without the plane-wave approximation, with $s = x \sin\theta + y \cos\theta$ and $t = x \cos\theta - y \sin\theta$,
$$\Delta R = \sqrt{(R_c + s)^2 + t^2} - R_c = s + \frac{t^2}{2 R_c} + O\Big(\frac{|p|^3}{R_c^2}\Big).$$

*Proof.* $|a_m - p|^2 = R_c^2 + 2 R_c s + |p|^2$, and $|p|^2 = s^2 + t^2$ because $(\sin\theta, \cos\theta)$ and $(\cos\theta, -\sin\theta)$ are orthonormal, so $|a_m - p| = \sqrt{(R_c + s)^2 + t^2}$. Expand $\sqrt{(R_c + s)^2 + t^2} = (R_c + s)\sqrt{1 + t^2/(R_c + s)^2} = R_c + s + t^2/(2(R_c + s)) + O(t^4/R_c^3)$, and $t^2/(2(R_c + s)) = t^2/(2R_c) + O(|p|^3/R_c^2)$. $\square$

The term $t^2/(2R_c)$ adds the phase $-u_n t^2/(2R_c)$, which Theorem 2 leaves out. At $\theta = 0$ it is $x^2/(2R_c)$, a range offset for every pulse; its change with $\theta$ is to first order $-x y\, \theta / R_c$, a cross-range offset of about $x y / R_c$. Both are shifts, so the first effect of a large scene at short range is a geometric distortion; the parts of the term that are quadratic in $\theta$ or vary with $u_n$ blur the image, which matters only at still shorter range. Neither is corrected by L1 to L4.

**Cost.** L1 and L2 each do $M N$ interpolations of $K$ taps, L3 is a 2D FFT of $O(M N \log(M N))$ operations and L4 is $O(M N)$. The total is $O(M N (\log(M N) + K))$ in the real-RAM model, with $O(M N)$ extra space.
