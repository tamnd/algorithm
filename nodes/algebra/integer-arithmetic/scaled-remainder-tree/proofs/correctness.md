---
title: The scaled remainder tree returns every remainder exactly
proves: [correctness, termination]
status: full
---

Let $x \ge 0$ and $m_1, \ldots, m_k \ge 1$. In the product tree every internal node $v$ has two children and $Q_v$ is the product of the moduli at the leaves below it; let $d$ be its height. Write $\lambda(Q)$ for the binary length of $Q \ge 1$, so $2^{\lambda(Q) - 1} \le Q < 2^{\lambda(Q)}$. Let $G \ge 1$ with $2^G \ge d + 1$ and $p_v = \lambda(Q_v) + G$. For a real $z$ write $\{z\} = z - \lfloor z \rfloor \in [0, 1)$.

**Theorem.** SCALED-REMAINDERS terminates and returns $x \bmod m_i$ at the leaf of $m_i$, for every $i$.

**Termination.** The tree has $2k - 1$ nodes, line L3 runs once, line L5 once per node other than the root, and line L6 once per leaf; each is a finite computation on integers.

**1. Precisions decrease.** If $c$ is a child of $v$ with sibling $s$, then $Q_v = Q_c Q_s \ge Q_c$, so $\lambda(Q_c) \le \lambda(Q_v)$ and $p_c \le p_v$; the shift in line L5 is by a nonnegative amount.

**2. The error invariant.** Let $y_v = \{x / Q_v\}$. For every node $v$ there is a real $\delta_v$ with

$$y_v \equiv \frac{Y_v}{2^{p_v}} + \delta_v \pmod 1, \qquad 0 \le Q_v \delta_v < (\mathrm{depth}(v) + 1) \, 2^{-G} .$$

*Proof.* By induction on the depth. At the root, $x / P \equiv (x \bmod P)/P \pmod 1$, and line L3 sets $Y = \lfloor (x \bmod P) 2^{p} / P \rfloor$, so $\delta_{\text{root}} = (x \bmod P)/P - Y/2^{p} \in [0, 2^{-p})$, and $P \delta_{\text{root}} < P \, 2^{-\lambda(P) - G} < 2^{-G}$.

Let $c$ be a child of $v$ with sibling $s$. Since $x/Q_c = Q_s \cdot x/Q_v$ and $Q_s$ is an integer, $y_c \equiv Q_s y_v \pmod 1$, and by the hypothesis

$$y_c \equiv \frac{Q_s Y_v}{2^{p_v}} + Q_s \delta_v \pmod 1 .$$

Let $Z = (Q_s Y_v) \bmod 2^{p_v}$; then $Q_s Y_v / 2^{p_v} \equiv Z / 2^{p_v} \pmod 1$. Line L5 sets $Y_c = \lfloor Z / 2^{p_v - p_c} \rfloor$, so $Z / 2^{p_v} = Y_c / 2^{p_c} + \tau$ with $0 \le \tau < 2^{-p_c}$. Hence $y_c \equiv Y_c / 2^{p_c} + \delta_c$ with $\delta_c = \tau + Q_s \delta_v \ge 0$, and

$$Q_c \delta_c = Q_c \tau + Q_v \delta_v < Q_c 2^{-\lambda(Q_c) - G} + (\mathrm{depth}(v) + 1) 2^{-G} < (\mathrm{depth}(v) + 2) 2^{-G},$$

using $Q_c Q_s = Q_v$ and $Q_c < 2^{\lambda(Q_c)}$. Since $\mathrm{depth}(c) = \mathrm{depth}(v) + 1$, the invariant holds at $c$. $\square$

**3. The leaves.** Let a leaf have modulus $m$, value $Y$ and precision $p$, at depth at most $d$, and let $r = x \bmod m$. Then $y = \{x/m\} = r/m$, and by part 2, $r/m = Y/2^p + \delta + j$ for an integer $j$, with $0 \le m \delta < (d + 1) 2^{-G} \le 1$. Multiplying by $m$,

$$\frac{mY}{2^p} = r - mj - m\delta, \qquad 0 \le m \delta < 1 .$$

Since $r - mj$ is an integer, $\lceil mY / 2^p \rceil = r - mj$, and reducing modulo $m$ gives $r$, because $0 \le r < m$. So line L6 returns $x \bmod m$ at every leaf. $\blacksquare$
