---
title: Backprojection is linear and focuses a point target to a unique maximum equal to the number of pulses times its amplitude
proves: [correctness]
status: full
---

We prove three facts about time-domain backprojection as written on the main page (lines L1 to L6), for the stop-and-go model: point targets, known antenna positions $a_p$, $p = 1, \ldots, P$, and no antenna pattern or range loss in the data. Theorems 1 and 2 are exact for the sum $I(q)$ with exact interpolation; the error of the interpolation in L1 and L4 is a measurement, given on the main page.

**Setting.** Pulse $p$ is a complex baseband signal $d_p(t)$, sampled at $t_0 + j/f_s$. Lines L1 to L4 return an approximation $\tilde d_p(t)$ of $d_p(t)$ at $t = 2R_p(q)/c$ with $R_p(q) = |a_p - q|$, or skip the pulse when $t$ is outside the record. Let $A(q)$ be the set of pulses that are not skipped. The algorithm returns $I(q) = \sum_{p \in A(q)} \tilde d_p(2R_p(q)/c)\, e^{+i 4\pi f_0 R_p(q)/c}$. The Fourier sign is $e^{-i 2\pi f t}$.

**Theorem 1 (linearity).** $I$ is linear in the data.

*Proof.* The set $A(q)$, the read time and the phase factor depend only on the geometry. L1 is a DFT, a zero padding and an inverse DFT, which is linear, and L4 is a weighted sum of two samples with weights fixed by the geometry. A sum over pulses of linear maps is linear. $\square$

**Theorem 2 (a point target).** Let the data be one target of amplitude $\alpha$ at $q_0$, $d_p(t) = \alpha\, g(t - 2R_p(q_0)/c)\, e^{-i 4\pi f_0 R_p(q_0)/c}$, with a real pulse $g$ such that $|g(s)| < g(0)$ for $s \ne 0$, and assume exact interpolation, $\tilde d_p = d_p$. With $\Delta_p(q) = 2(R_p(q) - R_p(q_0))/c$:

1. $I(q) = \alpha \sum_{p \in A(q)} g(\Delta_p(q))\, e^{i 2\pi f_0 \Delta_p(q)}$;
2. $I(q_0) = |A(q_0)|\, \alpha\, g(0)$, which is $P \alpha\, g(0)$ when no pulse is skipped;
3. $|I(q)| \le |A(q)|\, |\alpha|\, g(0)$ for every $q$, and equality needs $R_p(q) = R_p(q_0)$ for every $p \in A(q)$.

*Proof.* At $t = 2R_p(q)/c$, $d_p(t) = \alpha\, g(\Delta_p)\, e^{-i 4\pi f_0 R_p(q_0)/c}$, and the factor $e^{+i 4\pi f_0 R_p(q)/c}$ turns the phase into $2\pi f_0 \cdot 2(R_p(q) - R_p(q_0))/c = 2\pi f_0 \Delta_p$. This is part 1. At $q_0$ every $\Delta_p$ is 0, which gives part 2. By the triangle inequality $|I(q)| \le |\alpha| \sum_{p \in A(q)} |g(\Delta_p)| \le |A(q)|\, |\alpha|\, g(0)$, and the second step is an equality only if $\Delta_p = 0$ for every $p \in A(q)$. $\square$

**Theorem 3 (uniqueness for a straight track).** Let the antenna move on the line $\{(s, 0, h)\}$ and let the pixels lie in the ground plane $z = 0$ on one side of the track, $y > 0$. If $A(q)$ contains two pulses at different $s$, then $R_p(q) = R_p(q_0)$ for those two pulses implies $q = q_0$. So by Theorem 2 the maximum of $|I|$ over such pixels with $A(q) = A(q_0)$ is reached only at $q_0$.

*Proof.* Write $q = (x, y, 0)$ and $q_0 = (x_0, y_0, 0)$. The equations $(s_k - x)^2 + y^2 + h^2 = (s_k - x_0)^2 + y_0^2 + h^2$ for $k = 1, 2$ subtract to $2(s_2 - s_1)(x - x_0) = 0$, so $x = x_0$ because $s_1 \ne s_2$. Then $y^2 = y_0^2$, and $y = y_0$ because both are positive. $\square$

For a target at a pixel and $P = 64$ pulses the test measures 63.78; the loss of 0.3% comes from the linear interpolation in L4 on the pulse upsampled by 8. For a general flight path, part 3 of Theorem 2 still holds, and the maximum is unique wherever the ranges from the positions in $A(q)$ fix the ground point.

**Cost.** L1 costs $O(F N \log(F N))$ per pulse with an FFT, and L2 to L5 cost $O(1)$ per pixel and pulse. An $n \times n$ image costs $O(P (n^2 + F N \log(F N)))$ in the real-RAM model, with $O(n^2 + F N)$ extra space.
