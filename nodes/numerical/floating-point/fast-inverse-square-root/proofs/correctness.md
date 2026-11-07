---
title: The fast inverse square root has relative error at most 0.0017525
proves: [correctness]
status: full
---

**Setting.** $x$ is a binary32 float with $2^{-125} \le x \le (2 - 2^{-23})2^{127}$. All floating-point operations are binary32 operations, correctly rounded to nearest, so each one satisfies the [standard model](/floating-point-model/) $\mathrm{fl}(a \mathbin{op} b) = (a \mathbin{op} b)(1 + \delta)$, $|\delta| \le u$, with $u = 2^{-24}$, when its exact result is in the normal range. $R = \texttt{0x5F3759DF}$. We write $y_0$ for the value of line L4, $y_1$ for the result, $\varepsilon_0 = y_0\sqrt{x} - 1$ and $\varepsilon_1 = y_1 \sqrt{x} - 1$.

**Theorem.** $-0.0017525 \le \varepsilon_1 \le 2 \times 10^{-7}$.

**Step 0 (the encoding).** A positive normal binary32 float $2^{E}(1 + k/2^{23})$, with $-126 \le E \le 127$ and $0 \le k < 2^{23}$, has the pattern $2^{23}(E + 127) + k$. Conversely each pattern in $[\texttt{0x00800000}, \texttt{0x7F7FFFFF}]$ is a positive normal float. Line L1 is exact: $x/2 \ge 2^{-126}$ is normal, and halving a normal float only lowers its exponent.

**Step 1 (scaling).** Let $i = \mathrm{BITS}(x)$. The domain gives $\texttt{0x01000000} \le i \le \texttt{0x7F7FFFFF}$, so $\texttt{0x00800000} \le \lfloor i/2 \rfloor \le \texttt{0x3FBFFFFF}$ and the pattern $g = R - \lfloor i/2 \rfloor$ of line L3 lies in $[\texttt{0x1F7759E0}, \texttt{0x5EB759DF}]$, so $y_0$ is a positive normal float. If $x$ and $4x$ are both in the domain, then $\mathrm{BITS}(4x) = i + 2^{24}$ by Step 0, so $\lfloor \mathrm{BITS}(4x)/2 \rfloor = \lfloor i/2 \rfloor + 2^{23}$ and the pattern of the guess for $4x$ is $g - 2^{23}$. Both patterns are normal, so by Step 0 the guess for $4x$ is $y_0/2$. Hence $\varepsilon_0(4x) = (y_0/2)\sqrt{4x} - 1 = \varepsilon_0(x)$. Each $x$ in the domain is $4^{j} x'$ for an integer $j$ and an $x' \in [1, 4)$, with all the intermediate values $4^{l} x'$ in the domain (the domain is a union of whole binades from $2^{-125}$ on). So the set of values of $\varepsilon_0$ on the domain is the set of its values on the floats of $[1, 4)$.

**Step 2 (the guess on [1, 4)).** Let $t_A = 7821791/2^{23}$ and $t_B = 3627487/2^{23}$; these are the fraction fields of $\texttt{0x3F7759DF}$ and $\texttt{0x3F3759DF}$, both of which have exponent field $126$. Let $\eta = (k/2 - \lfloor k/2 \rfloor)/2^{23} \in \{0, 2^{-24}\}$.

- *Piece A:* $x = 1 + m$, $m = k/2^{23}$, $0 \le k < 2^{23}$. Then $i = \texttt{0x3F800000} + k$ and $g = \texttt{0x3F7759DF} - \lfloor k/2 \rfloor$. Since $\lfloor k/2 \rfloor < 2^{22} < 7821791$, the exponent field stays $126$ and $y_0 = \tfrac12(1 + t_A - m/2 + \eta)$.
- *Piece B1:* $x = 2(1 + m)$, $m = k/2^{23}$, $0 \le k \le 7254975$. Then $g = \texttt{0x3F3759DF} - \lfloor k/2 \rfloor$ with $\lfloor k/2 \rfloor \le 3627487$, so $y_0 = \tfrac12(1 + t_B - m/2 + \eta)$.
- *Piece B2:* $x = 2(1 + m)$, $7254976 \le k < 2^{23}$. Now $\lfloor k/2 \rfloor > 3627487$, the subtraction borrows from the exponent field, which becomes $125$, and the fraction field is $2^{23} + 3627487 - \lfloor k/2 \rfloor$. So $y_0 = \tfrac14(2 + t_B - m/2 + \eta)$.

Drop $\eta$ and define, for real $m$ in the closed range of each piece,

$$g_A(m) = \tfrac12(1 + t_A - \tfrac{m}{2})\sqrt{1+m} - 1, \quad g_{B1}(m) = \tfrac12(1 + t_B - \tfrac{m}{2})\sqrt{2(1+m)} - 1, \quad g_{B2}(m) = \tfrac14(2 + t_B - \tfrac{m}{2})\sqrt{2(1+m)} - 1.$$

Then $\varepsilon_0 = g(m) + c\,\eta\sqrt{x}$ with $c = \tfrac12$ on pieces A and B1 and $c = \tfrac14$ on B2. Since $0 \le \eta \le 2^{-24}$ and $\sqrt{x} < 2$, we get $g(m) \le \varepsilon_0 \le g(m) + 6 \times 10^{-8}$.

Each $g$ has the form $L(m)\sqrt{m + 1}$ times a constant, minus 1, with $L$ linear, decreasing and positive on the range. Then $(L\sqrt{1+m})'' = 2L'(\sqrt{1+m})' + L(\sqrt{1+m})'' < 0$, so each $g$ is concave: its minimum over a closed interval is at an endpoint and its maximum is at the zero of $g'$ when that zero is inside. The derivative of $(a - m/2)\sqrt{1+m}$ is $(a - 1 - 3m/2)/(2\sqrt{1+m})$, which vanishes at $m = \tfrac23(a - 1)$. This gives the critical points $\tfrac23 t_A \approx 0.6216$, $\tfrac23 t_B \approx 0.2883$ and $\tfrac23(1 + t_B) \approx 0.9550$, each inside its piece. The values, rounded outward in the ninth decimal, are:

| piece | range of $m$ | at the left end | at the right end | at the critical point |
|---|---|---|---|---|
| A | $[0, 1]$ | $-0.033784926$ | $0.012881071$ | $0.032508610$ |
| B1 | $[0, 7254975/2^{23}]$ | $0.012881071$ | $-0.034375800$ | $0.033960196$ |
| B2 | $[7254976/2^{23}, 1]$ | $-0.034375769$ | $-0.033784926$ | $-0.033593969$ |

So $g \ge -0.0343758$ everywhere and $g \le 0.0339602$ everywhere, and with the $\eta$ term,

$$-0.0343758 \le \varepsilon_0 \le 0.0339603.$$

By Step 1 this holds on the whole domain.

**Step 3 (an exact Newton step).** Let $a = 1 + \varepsilon_0 = y_0\sqrt{x}$ and $z = (x/2) y_0^2 = a^2/2$. Then $a(1.5 - z) = a(3 - a^2)/2$, and with $a = 1 + \varepsilon_0$,

$$a(3 - a^2)/2 = \tfrac12(1 + \varepsilon_0)(2 - 2\varepsilon_0 - \varepsilon_0^2) = 1 - \tfrac32 \varepsilon_0^2 - \tfrac12 \varepsilon_0^3 = 1 - \tfrac12 \varepsilon_0^2(3 + \varepsilon_0).$$

Write $\bar\varepsilon_1 = -\tfrac12\varepsilon_0^2(3 + \varepsilon_0)$. For $\varepsilon_0 \in [-0.0343758, 0.0339603]$, $\bar\varepsilon_1 \le 0$, and $|\bar\varepsilon_1| = \tfrac12\varepsilon_0^2(3 + \varepsilon_0)$ is increasing in $|\varepsilon_0|$ on each side of $0$; its values at the two ends are $0.00175224$ and $0.00174954$. So $-0.0017523 \le \bar\varepsilon_1 \le 0$.

**Step 4 (the roundings of line L5).** All exact intermediate results are normal: $x/2$ is, $(x/2) y_0 = a\sqrt{x}/2$ lies in $[2^{-64}, 2^{64}]$, and the other values are near $\tfrac12$ or $1$, or near $y_0$. So the standard model gives

$$w = \mathrm{fl}(\mathrm{fl}(x_2 y_0) y_0) = z(1 + \theta), \quad |\theta| \le \gamma_2 = \frac{2u}{1 - 2u}, \qquad y_1 = y_0 (1.5 - w)(1 + \delta_3)(1 + \delta_4),$$

with $|\delta_3|, |\delta_4| \le u$ (Lemma 3.1 of Higham, as stated on the page of the [standard model](/floating-point-model/), gives the first bound). Multiply by $\sqrt{x}$:

$$1 + \varepsilon_1 = \bigl(a(1.5 - z) - a z \theta\bigr)(1 + \delta_3)(1 + \delta_4) = \bigl(1 + \bar\varepsilon_1 - a z\theta\bigr)(1 + \delta_3)(1 + \delta_4).$$

Here $0 < a \le 1.0339603$ and $0 < z = a^2/2 \le 0.534537$, so $|a z \theta| \le 0.55270 \cdot \gamma_2 \le 1.1055u$. With $A = 1 + \bar\varepsilon_1 - az\theta$, we have $1 - 0.0017523 - 1.1055u \le A \le 1 + 1.1055u$, and $(1 - u)^2 \le (1+\delta_3)(1+\delta_4) \le (1+u)^2$. Hence

$$1 + \varepsilon_1 \le (1 + 1.1055u)(1 + u)^2 \le 1 + 3.106u, \qquad 1 + \varepsilon_1 \ge (1 - 0.0017523 - 1.1055u)(1 - 2u) \ge 1 - 0.0017523 - 3.106u.$$

Since $u = 2^{-24} < 5.97 \times 10^{-8}$, $3.106u < 1.86 \times 10^{-7}$. So $-0.0017525 \le \varepsilon_1 \le 2 \times 10^{-7}$. $\blacksquare$

**Remark.** The bound is tight up to the rounding term: the float $x = 2(1 + 7254974/2^{23}) = 3.7297205924987793$ has $y_0 = 0.5$ exactly, $\varepsilon_0 = -0.0343758$ to 7 digits, and $\varepsilon_1 = -0.0017523$.
