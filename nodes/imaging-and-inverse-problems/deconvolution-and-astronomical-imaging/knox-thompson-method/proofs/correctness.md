---
title: "The Knox-Thompson recursion returns the object phase wherever the cross-spectrum transfer function is positive, and the sample phases converge to it"
proves: [correctness]
status: full
---

**Setting.** The grid is $n \times n$ and periodic, $N = n^2$, and frequencies $u = (u_1, u_2)$ are signed, with arithmetic mod $n$. The object $o$ is real and nonnegative with $\sum o > 0$, and $O(u) = |O(u)| e^{i\varphi(u)}$ is its DFT. The pupil $P$ is a real function on the grid. For a real phase screen $\psi$, the PSF is $s_\psi = |\mathcal F(P e^{i\psi})|^2$ and the transfer function is $T_\psi = \mathcal F(s_\psi) / \mathcal F(s_\psi)(0)$. The screens $\psi_1, \dots, \psi_F$ are independent with a common law $\mu$, and frame $f$ has $I_f = O\, T_{\psi_f}$.

For $e \in \{e_1, e_2\}$ define the sample and expected cross spectra and the transfer function

$$C^F_e(u) = \frac1F \sum_{f=1}^F I_f(u)\, \overline{I_f(u + e)}, \qquad H_e(u) = \mathbb E\big[T_\psi(u)\, \overline{T_\psi(u + e)}\big], \qquad C_e(u) = O(u)\, \overline{O(u + e)}\, H_e(u).$$

Let $U = \{u : |u| \le R\}$, ordered by $|u_1| + |u_2|$ as in line L3. A *step* is a pair $(p, u)$ with $p, u \in U$, $u - p = \pm e$ and $|p_1| + |p_2| = |u_1| + |u_2| - 1$; these are the pairs that line L6 uses.

**Claim 1 (the cross spectrum factors).** $C^F_e(u) = O(u)\, \overline{O(u + e)}\; \frac1F \sum_f T_{\psi_f}(u)\, \overline{T_{\psi_f}(u + e)}$, and $\mathbb E[C^F_e(u)] = C_e(u)$.

*Proof.* $I_f(u)\, \overline{I_f(u + e)} = O(u) T_f(u)\, \overline{O(u + e)}\, \overline{T_f(u + e)}$, and $O$ does not depend on $f$. Take the mean over $f$, then the expectation; $T$ is bounded by Claim 2, so the expectation exists. $\square$

**Claim 2 (the transfer function of one frame).** $T_\psi(0) = 1$, $|T_\psi(u)| \le 1$, and $T_\psi(-u) = \overline{T_\psi(u)}$. For the screen $-\psi$, $T_{-\psi} = \overline{T_\psi}$.

*Proof.* $s_\psi \ge 0$ and $s_\psi \ne 0$ when $P \ne 0$, so $\mathcal F(s_\psi)(0) = \sum s_\psi > 0$, and $|\mathcal F(s_\psi)(u)| \le \sum s_\psi$. Since $s_\psi$ is real, $\mathcal F(s_\psi)(-u) = \overline{\mathcal F(s_\psi)(u)}$. For the last part, $P$ is real, so $P e^{-i\psi} = \overline{P e^{i\psi}}$, and $\mathcal F(\bar g)(x) = \overline{\mathcal F(g)(-x)}$. Hence $s_{-\psi}(x) = s_\psi(-x)$, and $\mathcal F(s_{-\psi})(u) = \mathcal F(s_\psi)(-u) = \overline{\mathcal F(s_\psi)(u)}$. The scale $\sum s$ is the same for both. $\square$

**Claim 3 (a symmetric law gives a real transfer function).** If $\psi$ and $-\psi$ have the same law $\mu$, then $H_e(u)$ is real for every $u$. If the screens come in pairs $\psi, -\psi$, then the sample transfer function $\frac1F \sum_f T_{\psi_f}(u)\, \overline{T_{\psi_f}(u + e)}$ is real for every $F$.

*Proof.* By Claim 2, $T_{-\psi}(u)\, \overline{T_{-\psi}(u + e)} = \overline{T_\psi(u)\, \overline{T_\psi(u + e)}}$. Under a symmetric law the left side has the same expectation as the product for $\psi$, so $H_e(u) = \overline{H_e(u)}$. For a pair, the two terms are conjugates, and their sum is real. $\square$

A Gaussian screen with zero mean, such as filtered white noise, has a symmetric law.

**Claim 4 (the recursion is exact on positive data).** Suppose the cross spectra used by the recursion are $\hat C_e(u) = O(u)\, \overline{O(u + e)}\, h_e(u)$ with $h_e(u)$ real, and $h_e(p) > 0$ for every step $(p, p + e)$ and $h_e(u) > 0$ for every step $(p, u)$ with $u = p - e$. Suppose also that $O(u) \ne 0$ on $U$. Then lines L2 to L8 return $\varphi(u)$ for every $u \in U$, mod $2\pi$.

*Proof.* By induction in the order of line L3. $\varphi(0) = 0$ is correct because $O(0) = \sum o > 0$. Take $u \ne 0$ and assume $\varphi(p)$ is correct for all $p$ before $u$. Every $u \in U$, $u \neq 0$, has at least one step $(p, u)$: move one unit toward the origin along a nonzero coordinate; this lowers $|u_1| + |u_2|$ by one and does not raise $|u|$, so $p \in U$. For a step with $u = p + e$, the term is

$$e^{i\varphi(p)}\, \overline{\hat C_e(p)} = e^{i\varphi(p)}\, |O(p)|\, e^{-i\varphi(p)}\, |O(u)|\, e^{i\varphi(u)}\, h_e(p) = |O(p)|\,|O(u)|\, h_e(p)\; e^{i\varphi(u)} .$$

For a step with $u = p - e$, so $p = u + e$, the term is

$$e^{i\varphi(p)}\, \hat C_e(u) = e^{i\varphi(p)}\, |O(u)|\, e^{i\varphi(u)}\, |O(p)|\, e^{-i\varphi(p)}\, h_e(u) = |O(u)|\,|O(p)|\, h_e(u)\; e^{i\varphi(u)} .$$

Every term is $e^{i\varphi(u)}$ times a positive number, and there is at least one term, so $z = c\, e^{i\varphi(u)}$ with $c > 0$, and line L7 returns $\varphi(u)$. $\square$

With antithetic pairs, Claim 3 makes $h_e$ the real sample transfer function, so Claim 4 applies as soon as it is positive on the steps. With one pair it can be negative at some frequencies, and then the phase there and after it on the path can be off by $\pi$.

**Claim 5 (convergence in the number of frames).** Suppose the law of $\psi$ is symmetric, $H_e > 0$ on the steps as in Claim 4, and $O \ne 0$ on $U$. Then, with probability 1, the phases returned from $C^F_e$ converge to $\varphi$ on $U$ as $F \to \infty$.

*Proof.* The terms $T_{\psi_f}(u)\, \overline{T_{\psi_f}(u + e)}$ are independent, have the same law and are bounded by 1 (Claim 2). By the strong law of large numbers their mean converges to $H_e(u)$ with probability 1, for each of the finitely many $u$ and $e$, so $C^F_e \to C_e$ by Claim 1. By Claims 3 and 4, the recursion applied to $C_e$ returns $\varphi$, and in the proof of Claim 4 every $z$ is nonzero. The recursion is continuous at such data: each $z$ is a continuous function of the cross spectra and of the earlier phases through $e^{i\varphi(p)}$, and $\arg$ is continuous at a nonzero $z$ (as a map to the circle). By induction in the order of line L3, every returned phase converges to $\varphi(u)$ mod $2\pi$. $\square$

**Remark (what is assumed).** Claim 5 assumes $H_e > 0$ on the steps. Claim 3 gives only that $H_e$ is real. Positivity is a property of the turbulence and of the offset: $H_e(0) = \mathbb E[\overline{T(e)}]$ is the long-exposure transfer function at $e$, and $H_e$ is small when the offset is larger than a seeing cell in the frequency plane. The proof does not cover the sign of $H_e$ in general.
