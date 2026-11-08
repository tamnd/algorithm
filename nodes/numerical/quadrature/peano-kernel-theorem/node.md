---
tag: 40PVBK
kind: theorem
slug: peano-kernel-theorem
name: Peano kernel theorem
aliases:
- Peano kernel
- Peano's theorem on quadrature remainders
- Peano kernel representation
area: numerical/quadrature
level: advanced
summary: Writes the quadrature error as an integral of a kernel against a derivative of f, giving sharp error bounds.
prereqs: [quadrature-error]
see_also: [quadrature-error, interpolatory-quadrature, newton-cotes-formulas, simpsons-rule, trapezoidal-rule, gauss-quadrature-theorem, degree-of-precision, euler-maclaurin-formula]
sources:
  - paper: "Giuseppe Peano, Resto nelle formule di quadratura espresso con un integrale definito, Atti della Reale Accademia dei Lincei, Rendiconti (5) 22, 1913, 562-569"
    locator: the representation of the remainder by a kernel
  - book: isbn:9780122063602
    title: Philip J. Davis and Philip Rabinowitz, Methods of Numerical Integration, second edition, Academic Press, 1984
    locator: Section 4.3, Truncation error (the Peano kernel and its use for error bounds of specific rules)
  - book: isbn:9780521295147
    title: M. J. D. Powell, Approximation Theory and Methods, Cambridge University Press, 1981
    locator: Chapter 22, The Peano kernel theorem
  - book: isbn:9780521007948
    title: Endre Süli and David F. Mayers, An Introduction to Numerical Analysis, Cambridge University Press, 2003
    locator: Chapter 7, Numerical integration I (the error of the Newton-Cotes rules)
  - paper: "Arthur Sard, Integral representations of remainders, Duke Mathematical Journal 15, 1948, 333-345"
    locator: the general form for functionals involving derivatives and several variables
---

## Statement

Let $w$ be integrable on $[a, b]$, let $x_1, \ldots, x_n \in [a, b]$ and let

$$E(f) = \int_a^b f(x)\, w(x)\,dx - \sum_{i=1}^n w_i f(x_i)$$

be the error functional of a [quadrature rule](/quadrature-rule/). Let $k \ge 0$ and suppose $E(p) = 0$ for every polynomial $p$ of degree at most $k$. Define the **Peano kernel**

$$K_k(t) = \frac{1}{k!}\, E_x\big[(x - t)_+^k\big], \qquad (x - t)_+^k = \begin{cases} (x - t)^k & x \ge t, \\ 0 & x < t, \end{cases}$$

where $E_x$ means that $E$ acts on the function of $x$ for fixed $t$ (for $k = 0$, $(x - t)_+^0$ is the step function equal to 1 for $x \ge t$). Then for every $f \in C^{k+1}[a, b]$,

$$E(f) = \int_a^b K_k(t)\, f^{(k+1)}(t)\,dt.$$

Moreover:

1. $K_k(t) = 0$ for $t$ outside $[a, b]$ (for $t > b$ trivially, for $t < a$ because $(x - t)^k$ is a polynomial of degree $k$ on $[a, b]$).
2. $|E(f)| \le \|K_k\|_{L^1} \|f^{(k+1)}\|_\infty$, and $\|K_k\|_{L^1} = \int_a^b |K_k(t)|\,dt$ is the smallest constant $c$ with $|E(f)| \le c \|f^{(k+1)}\|_\infty$ for all $f \in C^{k+1}[a, b]$.
3. If $K_k$ does not change sign on $[a, b]$, then for every $f \in C^{k+1}[a, b]$ there is $\xi \in [a, b]$ with

$$E(f) = \frac{E(x^{k+1})}{(k+1)!}\, f^{(k+1)}(\xi).$$

## In plain words

A quadrature rule makes no error on low-degree polynomials. Any smooth function is a low-degree polynomial plus a remainder that is built from its next derivative. So the error of the rule depends only on that derivative.

The theorem says exactly how: the error is a weighted average of the derivative, with a weight function called the kernel that belongs to the rule and not to the function. If the kernel never changes sign, the error is a fixed constant times the derivative at some point, which is the familiar form of error formulas such as Simpson's. If it does change sign, the total size of the kernel still gives the best possible bound.

## Proof

**Representation.** Let $f \in C^{k+1}[a, b]$. Taylor's theorem with the integral remainder, expanded at $a$, gives for $x \in [a, b]$

$$f(x) = p(x) + \frac{1}{k!} \int_a^x (x - t)^k f^{(k+1)}(t)\,dt = p(x) + \frac{1}{k!} \int_a^b (x - t)_+^k f^{(k+1)}(t)\,dt,$$

where $p$ is the Taylor polynomial of degree $k$ at $a$. Since $E(p) = 0$ and $E$ is linear,

$$E(f) = E_x\Big[\frac{1}{k!} \int_a^b (x - t)_+^k f^{(k+1)}(t)\,dt\Big].$$

$E$ has two parts. For the integral part, the function $(x, t) \mapsto w(x) (x - t)_+^k f^{(k+1)}(t)$ is measurable on $[a, b]^2$ and bounded in absolute value by $|w(x)| (b - a)^k \|f^{(k+1)}\|_\infty$, which is integrable, so Fubini's theorem lets us exchange the order:

$$\int_a^b w(x) \frac{1}{k!}\int_a^b (x - t)_+^k f^{(k+1)}(t)\,dt\,dx = \int_a^b f^{(k+1)}(t)\, \frac{1}{k!} \int_a^b w(x) (x - t)_+^k\,dx\,dt.$$

For the sum part, a finite sum of integrals is the integral of the sum: $\sum_i w_i \frac{1}{k!}\int_a^b (x_i - t)_+^k f^{(k+1)}(t)\,dt = \int_a^b f^{(k+1)}(t) \frac{1}{k!}\sum_i w_i (x_i - t)_+^k\,dt$. Subtracting, $E(f) = \int_a^b K_k(t) f^{(k+1)}(t)\,dt$.

**Item 1.** For $t > b$, $(x - t)_+^k = 0$ on $[a, b]$, so $K_k(t) = 0$. For $t < a$, $(x - t)_+^k = (x - t)^k$ on $[a, b]$, a polynomial of degree $k$ in $x$, so $K_k(t) = E(\,(x - t)^k)/k! = 0$.

**Item 2.** The bound is $|\int K_k f^{(k+1)}| \le \int |K_k| \cdot \|f^{(k+1)}\|_\infty$. For sharpness, $K_k$ is piecewise polynomial, so its sign function $\operatorname{sgn} K_k$ has finitely many jumps. Choose continuous $g_\varepsilon$ with $|g_\varepsilon| \le 1$ that agree with $\operatorname{sgn} K_k$ outside a set of measure $\varepsilon$. Let $f_\varepsilon$ be a $(k + 1)$-fold antiderivative of $g_\varepsilon$; it lies in $C^{k+1}[a, b]$ with $\|f_\varepsilon^{(k+1)}\|_\infty \le 1$, and $E(f_\varepsilon) = \int K_k g_\varepsilon \ge \int |K_k| - 2 \varepsilon \|K_k\|_\infty$. Letting $\varepsilon \to 0$ shows that no constant smaller than $\int |K_k|$ works.

**Item 3.** If $K_k \ge 0$ (or $\le 0$) on $[a, b]$, the mean value theorem for integrals, applied to the continuous $f^{(k+1)}$ and the one-signed $K_k$, gives $\xi$ with $E(f) = f^{(k+1)}(\xi) \int_a^b K_k$. Applying the representation to $f(x) = x^{k+1}$, whose derivative of order $k + 1$ is the constant $(k + 1)!$, gives $E(x^{k+1}) = (k+1)! \int_a^b K_k$. Substituting $\int K_k$ gives the formula. $\square$

## Consequences

**The classical error formulas.** For each rule below the kernel is computed directly from the definition, and item 3 gives the error.

| rule on the panel | $k$ | kernel $K_k(t)$ on the panel | sign | error |
|---|---|---|---|---|
| trapezoidal, $[0, h]$ | 1 | $-\tfrac12 t (h - t)$ | $\le 0$ | $-\frac{h^3}{12} f''(\xi)$ |
| midpoint, $[-\tfrac h2, \tfrac h2]$ | 1 | $\tfrac12 (\tfrac h2 - \lvert t \rvert)^2$ | $\ge 0$ | $\frac{h^3}{24} f''(\xi)$ |
| Simpson, $[-1, 1]$ | 3 | $-\tfrac{1}{72} (1 - \lvert t \rvert)^3 (1 + 3 \lvert t \rvert)$ | $\le 0$ | $-\frac{1}{90} f^{(4)}(\xi)$ |
| Simpson, $[-1, 1]$ | 2 | $-\tfrac16\, t\, (1 - \lvert t \rvert)^2$ | changes sign | $\lvert E \rvert \le \frac{1}{36} \max \lvert f''' \rvert$ |

For the trapezoidal rule with $k = 1$: $K_1(t) = \int_t^h (x - t)\,dx - \frac{h}{2}(h - t) = \frac{(h - t)^2}{2} - \frac{h (h - t)}{2} = -\frac{t (h - t)}{2}$, and $\int_0^h K_1 = -\frac{h^3}{12}$. For Simpson with $k = 3$: $\int_{-1}^{1} K_3 = -\frac{2}{72}\big(\frac14 + \frac{3}{20}\big) = -\frac{1}{90}$, which with $h = 1$ is the $-\frac{h^5}{90} f^{(4)}(\xi)$ of [Simpson's rule](/simpsons-rule/). The $k = 2$ kernel of Simpson's rule is odd, so the mean value form fails, but item 2 gives the bound $\frac{1}{36} \max|f'''|$ on $[-1, 1]$; scaled to a double panel of width $2h$ and summed, this is the bound $\frac{(b - a) h^3}{72} \max|f'''|$ for $f \in C^3$ only.

**A family of bounds for one rule.** A rule exact on degree $d$ has kernels $K_0, K_1, \ldots, K_d$, one for each smoothness class. For $f \in C^{r}$ with $r \le d + 1$, use $K_{r-1}$. The Peano theorem thus gives the error of a rule on functions of low smoothness, where the usual formula with $f^{(d+1)}$ does not apply.

**Other norms.** By Hölder's inequality, $|E(f)| \le \|K_k\|_{L^q} \|f^{(k+1)}\|_{L^p}$ for $1/p + 1/q = 1$. With $p = 2$ this is the starting point of the theory of optimal rules in Sobolev spaces (Sard, Nikolskii), and the [Koksma-Hlawka inequality](/koksma-hlawka-inequality/) is a cousin of the case $p = 1$, $k = 0$ in one dimension.

**One sign is the same as a mean value formula.** Conversely to item 3, suppose $E(f) = c\, f^{(k+1)}(\xi_f)$ for every $f \in C^{k+1}[a, b]$, with a constant $c$. If $K_k$ took both signs, it would be positive on some interval $J_+$ and negative on some interval $J_-$, since it is piecewise polynomial. Take continuous $g_\pm \ge 0$, not identically 0, supported in $J_\pm$, and $f_\pm$ with $f_\pm^{(k+1)} = g_\pm$. Then $E(f_+) = \int K_k g_+ > 0$ and $E(f_-) < 0$, but both equal $c$ times a nonnegative number, a contradiction. So the classical error formulas of the $n$-point [Gauss rules](/gauss-quadrature-theorem/), with $f^{(2n)}(\xi)$, and of the closed and open [Newton-Cotes rules](/newton-cotes-formulas/), with $f^{(d+1)}(\xi)$ (Steffensen's theorem), say exactly that their kernels of the highest order do not change sign.

**Composite rules.** The kernel of a composite rule is the sum of the panel kernels, each supported on its panel. If every panel kernel has the same sign, so does the sum, and the composite error is $c\,(b - a) h^{d+1} f^{(d+1)}(\xi)$.

## Tightness

- **The order $k$ cannot be raised.** If $E(x^{k+1}) \ne 0$, then no representation $E(f) = \int K f^{(k+2)}$ exists, since its right side would vanish for $f = x^{k+1}$.
- **The constant in item 2 is optimal**, by the proof. It is attained in the limit by functions whose derivative of order $k + 1$ is the sign of the kernel.
- **The sign condition in item 3 is needed.** For Simpson's rule with $k = 2$, $E(x^3) = 0$, so a formula $E(f) = \frac{E(x^3)}{3!} f'''(\xi)$ would give $E(f) = 0$ for all $f \in C^3$; but $E(x^4) = -\frac{4}{15} \ne 0$ on $[-1, 1]$. The kernel changes sign at $t = 0$, and only the bound of item 2 holds.
- **Smoothness.** The representation needs $f^{(k+1)}$ integrable; it extends to $f^{(k)}$ absolutely continuous. For $f$ with a jump in $f^{(k)}$, the representation fails and the rate of the rule drops.

## History

Giuseppe Peano introduced the kernel in a 1913 note to the Accademia dei Lincei, as a way to write the remainder of any quadrature formula as a definite integral. Before that, error terms such as those of the trapezoidal and Simpson rules were derived one rule at a time. Richard von Mises used the kernel in the 1930s to study quadrature errors systematically, and Arthur Sard (1948, and his 1963 book Linear Approximation) extended it to functionals that involve derivatives and to several variables, and used it to construct optimal rules.

## References
