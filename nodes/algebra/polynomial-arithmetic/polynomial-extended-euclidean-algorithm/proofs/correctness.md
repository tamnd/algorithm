---
title: The extended Euclidean algorithm returns the gcd and small Bézout coefficients
proves: [correctness]
status: full
---

Let $F$ be a field and $f, g \in F[x]$. We number the values of the loop as in the page: $r_0 = f$, $r_1 = g$, $s_0 = 1$, $s_1 = 0$, $t_0 = 0$, $t_1 = 1$, and the pass of line L4 for $i = 1, 2, \ldots$ computes $r_{i-1} = q_i r_i + r_{i+1}$ with $\deg r_{i+1} < \deg r_i$, $s_{i+1} = s_{i-1} - q_i s_i$ and $t_{i+1} = t_{i-1} - q_i t_i$. The loop stops after the pass with $r_{\ell+1} = 0$, and then the variables $(r_0, s_0, t_0)$ of the algorithm hold $(r_\ell, s_\ell, t_\ell)$.

**Invariant.** $s_i f + t_i g = r_i$ for every $i$ that the algorithm computes.

*Proof.* For $i = 0$ and $i = 1$ this is $1 \cdot f + 0 \cdot g = f$ and $0 \cdot f + 1 \cdot g = g$. If it holds for $i - 1$ and $i$, then

$$s_{i+1} f + t_{i+1} g = (s_{i-1} f + t_{i-1} g) - q_i (s_i f + t_i g) = r_{i-1} - q_i r_i = r_{i+1}. \qquad \square$$

**The gcd.** The values $r_i$ are those of the [Euclidean algorithm](/polynomial-euclidean-algorithm/), so by its proof the loop stops, and $r_\ell$ is a gcd of $f$ and $g$ when $(f, g) \ne (0, 0)$. If $f = g = 0$, the loop does not run, line L5 returns $(0, 1, 0)$, and $1 \cdot 0 + 0 \cdot 0 = 0 = \gcd(0, 0)$. Otherwise $r_\ell \ne 0$, $u = \operatorname{lc}(r_\ell)^{-1}$, and multiplying the invariant for $i = \ell$ by $u$ gives $(u s_\ell) f + (u t_\ell) g = u r_\ell$, the monic gcd $h$.

**Degree formulas.** Assume $m = \deg f \ge n = \deg g \ge 0$, and write $n_i = \deg r_i$, so $n_0 = m \ge n_1 = n > n_2 > \cdots > n_\ell \ge 0$ and $\deg q_i = n_{i-1} - n_i$ for $1 \le i \le \ell$ (rule 3 of [degree of a polynomial](/polynomial-degree/)). We show, for $2 \le i \le \ell + 1$,

$$\deg s_i = n_1 - n_{i-1}, \qquad \deg t_i = n_0 - n_{i-1}.$$

For $i = 2$: $s_2 = 1 - q_1 \cdot 0 = 1$, of degree $0 = n_1 - n_1$, and $t_2 = 0 - q_1 \cdot 1 = -q_1$, of degree $n_0 - n_1$.

For $i = 3$: $s_3 = 0 - q_2 \cdot 1$, of degree $n_1 - n_2$, and $t_3 = 1 - q_2 t_2$. Here $\deg(q_2 t_2) = (n_1 - n_2) + (n_0 - n_1) = n_0 - n_2 \ge 1 > 0 = \deg 1$, so $\deg t_3 = n_0 - n_2$.

For $4 \le i + 1 \le \ell + 1$, assume the formulas for $i - 1$ and $i$, with $i \ge 3$. Then

$$\deg(q_i s_i) = (n_{i-1} - n_i) + (n_1 - n_{i-1}) = n_1 - n_i > n_1 - n_{i-2} = \deg s_{i-1},$$

because $n_i < n_{i-2}$. By rule 1 of degree, $\deg s_{i+1} = \deg(s_{i-1} - q_i s_i) = n_1 - n_i$. In the same way $\deg(q_i t_i) = n_0 - n_i > n_0 - n_{i-2} = \deg t_{i-1}$, so $\deg t_{i+1} = n_0 - n_i$. $\square$

**Degree bounds of the output.** Assume $f, g \ne 0$ and that $h$ is neither the monic $f$ nor the monic $g$. If $m < n$, the first pass gives $q_1 = 0$, $r_2 = f$, $s_2 = 1$, $t_2 = 0$, so from then on the algorithm runs as XGCD$(g, f)$ with the roles of $s$ and $t$ exchanged; so it suffices to treat $m \ge n$. Then $g \nmid f$, since otherwise $h$ would be the monic $g$; so $r_2 \ne 0$ and $\ell \ge 2$. The formulas with $i = \ell$ give

$$\deg s = \deg s_\ell = n_1 - n_{\ell-1} < n_1 - n_\ell = \deg g - \deg h, \qquad \deg t = \deg t_\ell = n_0 - n_{\ell-1} < n_0 - n_\ell = \deg f - \deg h,$$

since $n_{\ell-1} > n_\ell = \deg h$. Scaling by $u$ does not change degrees. $\blacksquare$
