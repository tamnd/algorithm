---
title: TFM is linear in the data, focuses a point scatterer to a unique maximum of height M^2, and can use half of a reciprocal matrix
proves: [correctness]
status: full
---

We prove four facts about TFM as written on the main page (lines L1 to L11). The facts hold for the pulse-echo model of the page: point scatterers, no spreading loss, no directivity and a constant speed of sound $c$. They are theorems about that model, not about a real specimen.

**Setting.** The elements are $e_i = (x_i, 0)$, $i = 1, \ldots, M$, with distinct $x_i$. For a pixel $p = (x, z)$ with $z > 0$, line L2 computes $d_i(p) = |p - e_i|/c$. The data $D_{ij}$ is a complex baseband trace sampled at $t_k = t_0 + k/f_s$. SAMPLE (lines L8 to L10) returns $\tilde r_{ij}(t) = \tilde b_{ij}(t) e^{i 2\pi f_0 t}$, where $\tilde b_{ij}$ is the linear interpolation of the samples of $D_{ij}$, and $0$ outside the recorded window. TFM returns $I(p) = |S(p)|$ with $S(p) = \sum_{i,j} \tilde r_{ij}(d_i(p) + d_j(p))$.

**Theorem 1 (linearity and the adjoint).** $S$ is a linear map from the data to the complex image. The map $S^*$ that adds $\overline{e^{i 2\pi f_0 t}}\, v$ with the weights $1 - \varphi$ and $\varphi$ to the two samples that SAMPLE read for the pixel value $v$ is its adjoint: $\langle S D, V \rangle = \langle D, S^* V \rangle$ for all data $D$ and images $V$.

*Proof.* For a fixed pixel and pair, SAMPLE at time $t$ returns $((1 - \varphi) D_{ij}[k] + \varphi D_{ij}[k+1]) e^{i 2\pi f_0 t}$, or $0$, where $k$ and $\varphi$ depend only on $t$. This is a linear form $\ell(D) = \sum_q w_q D_{ij}[q]$ with fixed complex weights $w_q$. A sum of linear forms is linear. For one form, $\overline{\ell(D)}\, v = \sum_q \overline{D_{ij}[q]}\, \overline{w_q}\, v$, so the adjoint puts $\overline{w_q}\, v$ on sample $q$, which is what tfm_adjoint does. Summing over pairs and pixels gives the identity. $\square$

**Theorem 2 (a point scatterer).** Let the data be exact samples of one point scatterer $a$ at $p_0 = (x_0, z_0)$, $z_0 > 0$: $b_{ij}(t) = a\, g(t - \tau_{ij}) e^{-i 2\pi f_0 \tau_{ij}}$ with $\tau_{ij} = d_i(p_0) + d_j(p_0)$, a real envelope $g$ with $|g(s)| < g(0)$ for $s \ne 0$, and assume SAMPLE reads $b_{ij}$ without interpolation error inside the window. Then:

1. $S(p) = a \sum_{i,j} g(\Delta_{ij}) e^{i 2\pi f_0 \Delta_{ij}}$ with $\Delta_{ij} = d_i(p) + d_j(p) - \tau_{ij}$;
2. $I(p_0) = |a|\, g(0)\, M^2$;
3. $I(p) \le |a|\, g(0)\, M^2$ for every pixel $p$, and for $M \ge 2$ equality holds only at $p = p_0$.

*Proof.* Part 1: the analytic value at $t = d_i(p) + d_j(p)$ is $a\, g(t - \tau_{ij}) e^{-i 2\pi f_0 \tau_{ij}} e^{i 2\pi f_0 t} = a\, g(\Delta_{ij}) e^{i 2\pi f_0 \Delta_{ij}}$. Part 2: at $p = p_0$ every $\Delta_{ij}$ is $0$, so the $M^2$ terms all equal $a\, g(0)$. Part 3: by the triangle inequality $|S(p)| \le |a| \sum_{i,j} |g(\Delta_{ij})| \le |a|\, g(0)\, M^2$. Equality needs $|g(\Delta_{ij})| = g(0)$ for every pair, so $\Delta_{ij} = 0$ for all $i, j$. The diagonal pairs give $d_i(p) = d_i(p_0)$, that is $|p - e_i| = |p_0 - e_i|$ for every $i$. Take two elements with $x_1 \ne x_2$. Subtracting the squared equations $(x - x_i)^2 + z^2 = (x_0 - x_i)^2 + z_0^2$ for $i = 1, 2$ gives $2(x_2 - x_1)(x - x_0) = 0$, so $x = x_0$, and then $z^2 = z_0^2$ with $z, z_0 > 0$ gives $z = z_0$. $\square$

The Gaussian envelope of the code satisfies the hypothesis on $g$. In the tests the interpolation error is not zero, so the measured peak is $254.67$ for $M^2 = 256$; the test allows 1 percent.

**Theorem 3 (reciprocity).** If $D_{ij} = D_{ji}$ for all $i, j$, then $S(p) = \sum_i \tilde r_{ii}(2 d_i(p)) + 2 \sum_{i < j} \tilde r_{ij}(d_i(p) + d_j(p))$, which is what tfm_half computes with $M(M+1)/2$ reads in place of $M^2$.

*Proof.* The time $d_i(p) + d_j(p)$ is symmetric in $i$ and $j$, and so is the trace by hypothesis. The terms of the pairs $(i, j)$ and $(j, i)$ are therefore equal, and the full sum splits into the diagonal and twice the strict upper triangle. $\square$

Linear acoustics with a reciprocal medium gives $D_{ij} = D_{ji}$ up to noise; the simulator of the code has it exactly.

**Theorem 4 (cost).** TFM reads $M^2$ samples per pixel, so an $n \times n$ grid costs $\Theta(M^2 n^2)$ calls of SAMPLE, each $O(1)$, plus $O(M n^2)$ for the times of line L2. The extra space is $O(M)$ per pixel, besides the data of size $M^2 T$ and the image.

*Proof.* Lines L4 to L6 run $M^2$ times per pixel, and SAMPLE does a fixed number of operations. Line L2 computes $M$ square roots per pixel. $\square$

**Remark on the interpolation.** Linear interpolation of the baseband envelope has error at most $h^2 \max |b''| / 8$ with $h = 1/f_s$, and the phase factor is exact. Interpolating the RF signal itself would need $f_s$ several times $f_0$ for the same error, because the RF signal oscillates at $f_0$. This is why the code works on IQ data.
