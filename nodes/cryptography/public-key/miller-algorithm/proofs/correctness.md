---
title: Miller's loop returns f_(r,P)(Q), and the shortcuts for k = 2 give the reduced Tate pairing
proves: [correctness]
status: full
---

Let $E$ be an elliptic curve over a field $K$ of characteristic not 2 or 3, given by $y^2 = x^3 + ax + b$, with point at infinity $\mathcal{O}$. We use the standard facts on divisors (Washington, Chapter 11): a nonzero rational function $h$ on $E$ has a divisor $\mathrm{div}(h)$; $\mathrm{div}(h_1 h_2) = \mathrm{div}(h_1) + \mathrm{div}(h_2)$; and $\mathrm{div}(h) = 0$ only for constant $h$.

**Lemma 1 (lines).** For points $T, U \ne \mathcal{O}$, let $\ell_{T,U}$ be the line through $T$ and $U$ (the tangent if $T = U$), and for $V \ne \mathcal{O}$ let $v_V = x - x_V$; set $v_{\mathcal{O}} = 1$. Then
$$\mathrm{div}(\ell_{T,U}) = (T) + (U) + (-(T+U)) - 3(\mathcal{O}), \qquad \mathrm{div}(v_V) = (V) + (-V) - 2(\mathcal{O}).$$
If $T + U = \mathcal{O}$, $\ell_{T,U} = v_T$ and the first formula reads $(T) + (-T) + (\mathcal{O}) - 3(\mathcal{O})$, which agrees with the second.

*Proof.* A non-vertical line $y = \lambda x + c$ meets $E$ in three points counted with multiplicity, which by the definition of the group law are $T$, $U$ and $-(T + U)$, and $y$ has a pole of order 3 at $\mathcal{O}$. A vertical line $x = x_V$ meets $E$ in $V$ and $-V$, and $x$ has a pole of order 2 at $\mathcal{O}$. $\square$

**Lemma 2 (Miller's recurrence).** For $j \ge 1$ let $f_{j,P}$ be a function with divisor $D_j = j(P) - ([j]P) - (j-1)(\mathcal{O})$. Then for $i, j \ge 1$,
$$f_{i+j,P} = c \cdot f_{i,P} \, f_{j,P} \, \frac{\ell_{[i]P,[j]P}}{v_{[i+j]P}}$$
for a nonzero constant $c$, and $f_{1,P}$ may be taken to be 1.

*Proof.* $D_1 = (P) - (P) - 0 = 0$, so $f_{1,P}$ is a constant. By Lemma 1, $\mathrm{div}(\ell_{[i]P,[j]P}/v_{[i+j]P}) = ([i]P) + ([j]P) - ([i+j]P) - (\mathcal{O})$, also when $[i+j]P = \mathcal{O}$. Adding $D_i + D_j$ gives $(i+j)(P) - ([i+j]P) - (i + j - 1)(\mathcal{O}) = D_{i+j}$. Two functions with the same divisor differ by a constant factor. $\square$

Each $f_{j,P}$ is defined only up to a constant. Below, $f_{j,P}$ means the function that the recurrence builds with $c = 1$ and $f_{1,P} = 1$; this is Miller's normalization.

**Theorem 1 (the loop).** Let $r = (r_t \ldots r_0)_2$ with $r_t = 1$ and let $Q$ be a point that is not a zero or a pole of any line or vertical used in the loop (for example, $Q \notin \langle P \rangle$ when $P$ has order $r$, since all those zeros and poles are multiples of $P$ or $\mathcal{O}$). Then MILLER$(P, Q, r)$ returns $f_{r,P}(Q)$.

*Proof.* For $s = t, t-1, \ldots, 0$ let $m_s = (r_t \ldots r_s)_2$. We show that after the bits down to $r_s$ are processed, $T = [m_s]P$ and $f = f_{m_s,P}(Q)$. At the start, $m_t = 1$, $T = P$ and $f = 1 = f_{1,P}(Q)$ (line L1). Assume the claim for $m_{s+1} = m$. Line L3 multiplies $f^2$ by $\ell_{T,T}(Q)/v_{2T}(Q)$, which by Lemma 2 with $i = j = m$ gives $f_{2m,P}(Q)$, and line L4 sets $T = [2m]P$. If $r_s = 1$, line L6 applies Lemma 2 with $i = 2m$ and $j = 1$ and gives $f_{2m+1,P}(Q)$, and line L7 sets $T = [2m + 1]P$. In both cases the new values belong to $m_s = 2m + r_s$. All the values evaluated at $Q$ are finite and nonzero by the condition on $Q$, so each step is well defined. At the end, $m_0 = r$. $\blacksquare$

Since $[r]P = \mathcal{O}$, $D_r = r(P) - r(\mathcal{O})$, so $f_{r,P}$ is the function used in the Weil and Tate pairings.

**Lemma 3 (final exponentiation for $k = 2$).** Let $p \equiv 3 \pmod 4$, $\mathbb{F}_{p^2} = \mathbb{F}_p[i]$ with $i^2 = -1$, and let $r \mid p + 1$. For $f \in \mathbb{F}_{p^2}^*$, $f^{(p^2-1)/r} = (\bar{f}/f)^{(p+1)/r}$, where $\overline{a + bi} = a - bi$.

*Proof.* The Frobenius map $z \mapsto z^p$ is a field automorphism of $\mathbb{F}_{p^2}$ that fixes $\mathbb{F}_p$, and $i^p = i \cdot (i^2)^{(p-1)/2} = i \cdot (-1)^{(p-1)/2} = -i$ because $(p-1)/2$ is odd. So $f^p = \bar{f}$ and $f^{p-1} = \bar{f}/f$. Then $f^{(p^2-1)/r} = (f^{p-1})^{(p+1)/r}$. $\square$

**Lemma 4 (denominator elimination).** In the setting of Lemma 3, suppose that $P \in E(\mathbb{F}_p)$ and that $x_Q \in \mathbb{F}_p$. Then dropping all the divisions by $v_V(Q)$ in lines L3 and L6 does not change $f_{r,P}(Q)^{(p^2-1)/r}$.

*Proof.* Every $V$ in the loop is a multiple of $P$, so $x_V \in \mathbb{F}_p$, and $v_V(Q) = x_Q - x_V \in \mathbb{F}_p^*$. The loop without divisions returns $f_{r,P}(Q) \cdot w$, where $w$ is a product of such values and their powers, so $w \in \mathbb{F}_p^*$. Then $w^{p-1} = 1$ by Fermat's little theorem, and $p - 1$ divides $(p^2 - 1)/r = (p-1)(p+1)/r$, so $w^{(p^2-1)/r} = 1$. $\square$

For the curve $y^2 = x^3 + x$ with $Q = (-x, iy)$, $x_Q = -x \in \mathbb{F}_p$, so Lemma 4 applies. For $y^2 = x^3 + 1$ with $Q = (\zeta x, y)$ and $\zeta \notin \mathbb{F}_p$, it does not, and the code keeps the divisions there.

**Corollary.** REDUCED-TATE, computed by line L9, by Lemma 3, or by Lemmas 3 and 4 when they apply, returns the same element $f_{r,P}(Q)^{(p^2-1)/r}$ of $\mu_r$. That this value is bilinear and non-degenerate is a property of the Tate pairing, proved in Washington, Chapter 11, and is not repeated here.
