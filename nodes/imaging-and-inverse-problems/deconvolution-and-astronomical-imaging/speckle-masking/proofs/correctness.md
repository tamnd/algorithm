---
title: "The speckle masking recursion returns the object phase up to a linear term wherever the bispectrum transfer function is positive, and the sample phases converge to it"
proves: [correctness]
status: full
---

**Setting.** The grid is $n \times n$ and periodic, $N = n^2$, and frequencies $u = (u_1, u_2)$ are signed, with arithmetic mod $n$. The object $o$ is real and nonnegative with $\sum o > 0$, and $O(u) = |O(u)| e^{i\varphi(u)}$ is its DFT. The pupil $P$ is a real function on the grid. For a real phase screen $\psi$, the PSF is $s_\psi = |\mathcal F(P e^{i\psi})|^2$ and the transfer function is $T_\psi = \mathcal F(s_\psi) / \mathcal F(s_\psi)(0)$. The screens $\psi_1, \dots, \psi_F$ are independent with a common law $\mu$, and frame $f$ has $I_f = O\, T_{\psi_f}$.

For $e \in \{e_1, e_2\}$ define the sample bispectrum, the transfer function and the expected bispectrum

$$B^F_e(u) = \frac1F \sum_{f=1}^F I_f(u)\, I_f(e)\, \overline{I_f(u + e)}, \qquad S_e(u) = \mathbb E\big[T_\psi(u)\, T_\psi(e)\, \overline{T_\psi(u + e)}\big], \qquad B_e(u) = O(u)\, O(e)\, \overline{O(u + e)}\, S_e(u).$$

Let $U = \{u : |u| \le R\}$ with $R \ge 1$, ordered by $|u_1| + |u_2|$ as in line L3. A *step* is a pair $(p, u)$ with $p, u \in U$, $u - p = \pm e$ and $|p_1| + |p_2| = |u_1| + |u_2| - 1$; these are the pairs that line L6 uses. For the values $\tau_1, \tau_2$ of line L2, let $c = (\tau_1 - \varphi(e_1), \tau_2 - \varphi(e_2))$ and $\varphi'(u) = \varphi(u) + c \cdot u$. Then $\varphi'(0) = 0$, $\varphi'(e_1) = \tau_1$ and $\varphi'(e_2) = \tau_2$.

**Claim 1 (the bispectrum factors).** $B^F_e(u) = O(u)\, O(e)\, \overline{O(u + e)}\; \frac1F \sum_f T_{\psi_f}(u)\, T_{\psi_f}(e)\, \overline{T_{\psi_f}(u + e)}$, and $\mathbb E[B^F_e(u)] = B_e(u)$.

*Proof.* Each of the three factors of $I_f$ is $O$ times $T_{\psi_f}$ at the same frequency, and $O$ does not depend on $f$. Take the mean over $f$, then the expectation; $T$ is bounded by Claim 2, so the expectation exists. $\square$

**Claim 2 (the transfer function of one frame).** $T_\psi(0) = 1$, $|T_\psi(u)| \le 1$, and for the screen $-\psi$, $T_{-\psi} = \overline{T_\psi}$.

*Proof.* $s_\psi \ge 0$ and $s_\psi \ne 0$ when $P \ne 0$, so $\mathcal F(s_\psi)(0) = \sum s_\psi > 0$ and $|\mathcal F(s_\psi)(u)| \le \sum s_\psi$. $P$ is real, so $P e^{-i\psi} = \overline{P e^{i\psi}}$, and $\mathcal F(\bar g)(x) = \overline{\mathcal F(g)(-x)}$. Hence $s_{-\psi}(x) = s_\psi(-x)$, and since $s_\psi$ is real, $\mathcal F(s_{-\psi})(u) = \mathcal F(s_\psi)(-u) = \overline{\mathcal F(s_\psi)(u)}$. The scale $\sum s$ is the same for both screens. $\square$

**Claim 3 (a symmetric law gives a real transfer function).** If $\psi$ and $-\psi$ have the same law $\mu$, then $S_e(u)$ is real for every $u$. If the screens come in pairs $\psi, -\psi$, then the sample transfer function $\frac1F \sum_f T_{\psi_f}(u)\, T_{\psi_f}(e)\, \overline{T_{\psi_f}(u + e)}$ is real for every $F$.

*Proof.* By Claim 2, the triple product for $-\psi$ is the conjugate of the triple product for $\psi$. Under a symmetric law both have the same expectation, so $S_e(u) = \overline{S_e(u)}$. For a pair, the two terms are conjugates, and their sum is real. $\square$

A Gaussian screen with zero mean, such as filtered white noise, has a symmetric law.

**Claim 4 (image motion and linear phase terms).** If frame $f$ is moved by $t_f \in \mathbb Z^2$, so that $I_f(u)$ becomes $I_f(u)\, e^{-2\pi i\, u \cdot t_f / n}$, then $B^F_e$ does not change. For every real vector $c$, $\varphi'(u) + \varphi'(e) - \varphi'(u + e) = \varphi(u) + \varphi(e) - \varphi(u + e)$.

*Proof.* The three factors of the frame bispectrum get $e^{-2\pi i\, u \cdot t_f / n}$, $e^{-2\pi i\, e \cdot t_f / n}$ and $e^{+2\pi i\, (u + e) \cdot t_f / n}$, and the product of the three is 1. For the second part, $c \cdot u + c \cdot e - c \cdot (u + e) = 0$. $\square$

So no bispectrum, sample or expected, can tell $\varphi$ from $\varphi'$. The recursion returns $\varphi'$, which is the object phase up to the linear term $c \cdot u$, a shift of the reconstructed image.

**Claim 5 (the recursion is exact on positive data).** Suppose the bispectra used by the recursion are $\hat B_e(u) = O(u)\, O(e)\, \overline{O(u + e)}\, h_e(u)$ with $h_e(u)$ real, and $h_e(p) > 0$ for every step $(p, p + e)$ and $h_e(u) > 0$ for every step $(p, u)$ with $u = p - e$. Suppose also that $O \ne 0$ on $U$. Then lines L2 to L8 return $\varphi'(u)$ for every $u \in U$, mod $2\pi$.

*Proof.* By Claim 4, $\hat B_e(u) = |O(u)|\,|O(e)|\,|O(u + e)|\, h_e(u)\; e^{i(\varphi'(u) + \varphi'(e) - \varphi'(u + e))}$. Line L2 sets $0 = \varphi'(0)$, $\tau_1 = \varphi'(e_1)$ and $\tau_2 = \varphi'(e_2)$. Now use induction in the order of line L3, and assume that $\varphi'(p)$ is correct for every $p$ before $u$. Every $u \in U$ with $u \ne 0$ has at least one step $(p, u)$: move one unit toward the origin along a nonzero coordinate; this lowers $|u_1| + |u_2|$ by one and does not raise $|u|$, so $p \in U$, and $p$ comes before $u$. Write $K$ for positive numbers. For a step with $u = p + e$, the term of line L6 is

$$e^{i(\varphi'(p) + \varphi'(e))}\, \overline{\hat B_e(p)} = K\, e^{i(\varphi'(p) + \varphi'(e) - \varphi'(p) - \varphi'(e) + \varphi'(u))} = K\, e^{i\varphi'(u)} .$$

For a step with $u = p - e$, so $p = u + e$, the term is

$$e^{i(\varphi'(p) - \varphi'(e))}\, \hat B_e(u) = K\, e^{i(\varphi'(p) - \varphi'(e) + \varphi'(u) + \varphi'(e) - \varphi'(p))} = K\, e^{i\varphi'(u)} .$$

Every term is $e^{i\varphi'(u)}$ times a positive number, and there is at least one term, so $z = K\, e^{i\varphi'(u)}$ and line L7 returns $\varphi'(u)$. $\square$

With antithetic pairs, Claim 3 makes $h_e$ the real sample transfer function, so Claim 5 applies as soon as it is positive on the steps. With one pair it can be negative at some frequencies, and then the phase there and after it on the path can be off by $\pi$.

**Claim 6 (convergence in the number of frames).** Suppose the law of $\psi$ is symmetric, $S_e > 0$ on the steps as in Claim 5, and $O \ne 0$ on $U$. Then, with probability 1, the phases returned from $B^F_e$ converge to $\varphi'$ on $U$ as $F \to \infty$.

*Proof.* The triple products $T_{\psi_f}(u)\, T_{\psi_f}(e)\, \overline{T_{\psi_f}(u + e)}$ are independent, have the same law and are bounded by 1 (Claim 2). By the strong law of large numbers their mean converges to $S_e(u)$ with probability 1, for each of the finitely many $u$ and $e$, so $B^F_e \to B_e$ by Claim 1. By Claims 3 and 5, the recursion applied to $B_e$ returns $\varphi'$, and in the proof of Claim 5 every $z$ is nonzero. Each $z$ is a continuous function of the bispectra and of the earlier phases through $e^{i\varphi'(p)}$, and $\arg$ is continuous at a nonzero $z$ (as a map to the circle). By induction in the order of line L3, every returned phase converges to $\varphi'(u)$ mod $2\pi$. By Claim 4 the same holds when the frames move. $\square$

**Remark (what is assumed).** Claim 6 assumes $S_e > 0$ on the steps. Claim 3 gives only that $S_e$ is real. At $u = 0$ the value is $S_e(0) = \mathbb E[|T_\psi(e)|^2] \ge 0$, the transfer function of speckle interferometry, and it is positive unless $T_\psi(e) = 0$ almost surely. At other $u$, positivity is a property of the turbulence, and the proof does not cover the sign of $S_e$ in general.
