---
title: The composite midpoint rule has error (b - a) h^2 f''(ξ)/24
proves: [correctness]
status: full
---

Let $a < b$, $m \ge 1$, $h = (b - a)/m$ and $c_i = a + (i - \tfrac12) h$ for $i = 1, \ldots, m$. MIDPOINT$(f, a, b, m)$ returns, in exact arithmetic,

$$M_m(f) = h \sum_{i=1}^{m} f(c_i),$$

because the loop of lines L3 and L4 adds $f(c_1), \ldots, f(c_m)$ once each to $s = 0$ (line L2), and line L5 multiplies by $h$. Write $I(f) = \int_a^b f(x)\,dx$ and $E(f) = I(f) - M_m(f)$.

**Lemma 1 (one panel).** Let $f \in C^2[c - h/2, c + h/2]$. Then there is $\eta$ in this panel with

$$\int_{c - h/2}^{c + h/2} f(x)\,dx - h f(c) = \frac{h^3}{24} f''(\eta).$$

*Proof.* Define $g(x) = 2\big(f(x) - f(c) - f'(c)(x - c)\big)/(x - c)^2$ for $x \ne c$ and $g(c) = f''(c)$. By Taylor's theorem with the Lagrange remainder, for each $x \ne c$ there is $\zeta$ between $c$ and $x$ with $f(x) = f(c) + f'(c)(x - c) + \tfrac12 f''(\zeta)(x - c)^2$, so $g(x) = f''(\zeta)$. Hence every value of $g$ is a value of $f''$ on the panel. Also $g$ is continuous: it is continuous at $x \ne c$ as a quotient of continuous functions, and $g(x) \to f''(c)$ as $x \to c$ because $\zeta \to c$ and $f''$ is continuous. Now

$$\int_{c-h/2}^{c+h/2} \big(f(x) - f(c)\big)\,dx = f'(c) \int_{c-h/2}^{c+h/2} (x - c)\,dx + \frac12 \int_{c-h/2}^{c+h/2} g(x)\,(x - c)^2\,dx.$$

The first integral on the right is 0 by symmetry. In the second, $(x - c)^2 \ge 0$, so the mean value theorem for integrals gives $x^*$ in the panel with value $\tfrac12 g(x^*) \int (x - c)^2\,dx = \tfrac12 g(x^*) \cdot \frac{h^3}{12}$. With $g(x^*) = f''(\eta)$ this is $\frac{h^3}{24} f''(\eta)$. $\square$

**Theorem (composite error).** Let $f \in C^2[a, b]$. Then there is $\xi \in [a, b]$ with

$$E(f) = \frac{(b - a)\, h^2}{24} f''(\xi).$$

*Proof.* The panels $[c_i - h/2, c_i + h/2]$ for $i = 1, \ldots, m$ cover $[a, b]$ and overlap only at their ends. By Lemma 1, $E(f) = \frac{h^3}{24} \sum_{i=1}^m f''(\eta_i)$. The mean $\frac1m \sum_i f''(\eta_i)$ lies between the minimum and the maximum of $f''$ on $[a, b]$, so by the intermediate value theorem it equals $f''(\xi)$ for some $\xi \in [a, b]$. So $E(f) = \frac{h^3 m}{24} f''(\xi) = \frac{(b - a) h^2}{24} f''(\xi)$. $\square$

**Corollary (degree of exactness).** For $f$ of degree at most 1, $f'' = 0$ and $E(f) = 0$. For $f(x) = x^2$, $E(f) = (b - a) h^2/12 \ne 0$. So the degree of exactness is exactly 1.

**Corollary (bracketing).** If $f'' \ge 0$ on $[a, b]$, then $M_m(f) \le I(f) \le T_m(f)$, where $T_m$ is the trapezoidal rule with the same $m$. The left inequality is the theorem. The right one is the trapezoidal error formula $I - T_m = -\frac{(b - a) h^2}{12} f''(\xi')$. $\blacksquare$

**Termination and cost.** The loop runs exactly $m$ times and evaluates $f$ once per pass, so the algorithm makes $m$ evaluations, none of them at $a$ or $b$.
