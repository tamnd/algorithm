---
title: The composite Simpson rule has degree of exactness 3 and error -(b - a) h^4 f''''(ξ)/180
proves: [correctness]
status: full
---

Let $a < b$, let $m \ge 2$ be even, $h = (b - a)/m$ and $x_i = a + i h$. SIMPSON$(f, a, b, m)$ returns, in exact arithmetic,

$$S_m(f) = \frac{h}{3}\Big( f(x_0) + 4 \sum_{i \text{ odd}} f(x_i) + 2 \sum_{\substack{0 < i < m \\ i \text{ even}}} f(x_i) + f(x_m) \Big),$$

because line L2 adds the two end values with coefficient 1, the loop of lines L3 to L5 adds each inner value once with coefficient 4 (odd $i$) or 2 (even $i$), and line L6 multiplies by $h/3$. Write $I(f) = \int_a^b f(x)\,dx$ and $E(f) = I(f) - S_m(f)$.

**Step 1 (decomposition).** For $j = 1, \ldots, m/2$, the basic rule on the double panel $P_j = [x_{2j-2}, x_{2j}]$ with centre $c_j = x_{2j-1}$ is

$$S^{(j)}(f) = \frac{h}{3}\big( f(c_j - h) + 4 f(c_j) + f(c_j + h) \big).$$

Summing over $j$ gives $S_m(f)$: an odd node is the centre of one double panel (coefficient 4), an even inner node is the right end of one double panel and the left end of the next (coefficient $1 + 1 = 2$), and $x_0$, $x_m$ are ends of one double panel each (coefficient 1).

**Lemma 1 (exactness of the basic rule).** $S^{(j)}(p) = \int_{P_j} p$ for every polynomial $p$ of degree at most 3.

*Proof.* Put $t = x - c_j$, so the panel is $[-h, h]$. For $p = 1$: $\frac{h}{3}(1 + 4 + 1) = 2h = \int_{-h}^{h} 1$. For $p = t$ and $p = t^3$: both sides are 0, since the integrand is odd and the rule is symmetric. For $p = t^2$: $\frac{h}{3}(h^2 + 0 + h^2) = \frac{2h^3}{3} = \int_{-h}^{h} t^2\,dt$. Every cubic in $x$ is a cubic in $t$, so by linearity the rule is exact for all of them. $\square$

**Lemma 2 (one double panel).** Let $f \in C^4(P_j)$. Then there is $\eta \in P_j$ with

$$\int_{P_j} f - S^{(j)}(f) = -\frac{h^5}{90} f^{(4)}(\eta).$$

*Proof.* Let $c = c_j$ and let $q$ be the cubic Hermite interpolant with $q(c - h) = f(c - h)$, $q(c) = f(c)$, $q'(c) = f'(c)$ and $q(c + h) = f(c + h)$. It exists and is unique (four conditions, four coefficients; see [Hermite interpolation](/hermite-interpolation/)). The rule uses only the three values, which $q$ matches, so $S^{(j)}(f) = S^{(j)}(q) = \int_{P_j} q$ by Lemma 1. The Hermite error formula with [divided differences](/divided-differences/) gives

$$f(x) - q(x) = g(x)\,(x - c + h)(x - c)^2(x - c - h), \qquad g(x) = f[c - h, c, c, c + h, x].$$

For $f \in C^4$, $g$ is continuous on $P_j$, and each value $g(x)$ equals $f^{(4)}(\zeta)/24$ for some $\zeta \in P_j$ (the mean value theorem for divided differences with repeated points). The weight $(x - c + h)(x - c)^2(x - c - h) = (t^2 - h^2) t^2$ is at most 0 on the panel, so it does not change sign. The mean value theorem for integrals gives $x^* \in P_j$ with

$$\int_{P_j} (f - q) = g(x^*) \int_{-h}^{h} t^2 (t^2 - h^2)\,dt = g(x^*) \Big( \frac{2h^5}{5} - \frac{2h^5}{3} \Big) = -\frac{4 h^5}{15} g(x^*).$$

With $g(x^*) = f^{(4)}(\eta)/24$ this is $-\frac{h^5}{90} f^{(4)}(\eta)$. $\square$

**Theorem (composite error).** Let $f \in C^4[a, b]$. Then there is $\xi \in [a, b]$ with

$$E(f) = -\frac{(b - a)\, h^4}{180} f^{(4)}(\xi).$$

*Proof.* By Step 1 and Lemma 2, $E(f) = -\frac{h^5}{90} \sum_{j=1}^{m/2} f^{(4)}(\eta_j)$. The mean of the $m/2$ values $f^{(4)}(\eta_j)$ lies between the minimum and the maximum of the continuous $f^{(4)}$ on $[a, b]$, so it equals $f^{(4)}(\xi)$ for some $\xi$. Then $E(f) = -\frac{h^5}{90} \cdot \frac{m}{2} f^{(4)}(\xi) = -\frac{(b - a) h^4}{180} f^{(4)}(\xi)$. $\square$

**Corollary (degree of exactness).** For a cubic, $f^{(4)} = 0$ and $E(f) = 0$. For $f = x^4$, $f^{(4)} = 24$ and $E(f) = -\frac{2 (b - a) h^4}{15} \ne 0$. So the degree of exactness is exactly 3. $\blacksquare$

**Termination and cost.** The loop runs $m - 1$ times with one evaluation per pass, and line L2 makes two, so the algorithm makes exactly $m + 1$ evaluations.
