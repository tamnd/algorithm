---
title: Sinc quadrature is a truncated trapezoidal sum of the log-ratio transformed integrand, and its truncation error is exp(-sqrt(2 pi d alpha n))
proves: [correctness]
status: full
---

Let $a < b$ be finite, $L = b - a$, and let $f$ be continuous on $(a, b)$ with $\int_a^b |f| < \infty$. Write

$$\varphi(x) = \log\frac{x - a}{b - x}, \qquad \psi(t) = \varphi^{-1}(t) = \frac{a + b e^t}{1 + e^t}, \qquad g(t) = f(\psi(t))\,\psi'(t),$$

and let $(M, N, h)$ be the parameters of line L1: $M = n$, $N = \lceil \alpha n / \beta \rceil$, $h = \sqrt{2\pi d / (\alpha n)}$. Lines refer to the pseudocode SINC.

**Lemma 1 (the change of variables).** $\psi$ is an infinitely differentiable, strictly increasing bijection of $\mathbb{R}$ onto $(a, b)$ with

$$\psi'(t) = \frac{L e^t}{(1 + e^t)^2} = \frac{(\psi(t) - a)(b - \psi(t))}{L},$$

and $\int_a^b f(x)\,dx = \int_{-\infty}^{\infty} g(t)\,dt$, both integrals converging absolutely.

*Proof.* $\psi(t) - a = L e^t/(1 + e^t)$ and $b - \psi(t) = L/(1 + e^t)$, both positive, with product $L^2 e^t/(1 + e^t)^2 = L\,\psi'(t)$; so $\psi' > 0$, and $\psi(t) \to a$ as $t \to -\infty$ and $\to b$ as $t \to \infty$. The substitution rule holds on every compact subinterval of $(a, b)$; letting the ends tend to $a$ and $b$ and using monotone convergence on $|f|$ gives the claim. $\square$

**Lemma 2 (nodes and weights without cancellation).** For $t \le 0$ put $e = e^t \in (0, 1]$; then $\psi(t) - a = Le/(1+e)$, $b - \psi(t) = L/(1+e)$ and $\psi'(t) = Le/(1+e)^2$. For $t > 0$ put $e = e^{-t} \in (0, 1)$; then $\psi(t) - a = L/(1+e)$, $b - \psi(t) = Le/(1+e)$ and $\psi'(t) = Le/(1+e)^2$.

*Proof.* For $t > 0$ multiply numerator and denominator of the formulas in Lemma 1 by $e^{-t}$, and of $\psi'$ by $e^{-2t}$. $\square$

Line L3 evaluates exactly these expressions (with $x = a + (\psi - a)$ for $t \le 0$ and $x = b - (b - \psi)$ for $t > 0$), so in exact arithmetic $x_k = \psi(kh)$ and $w_k = h\,\psi'(kh)$, and line L4 adds $h\,g(kh)$. In floating point the formulas use only $\exp$ of a nonpositive argument, products, quotients and one sum $1 + e \in (1, 2]$, so the distances and the weight have relative errors of a few units in the last place for every $k$, even when the distance is far below the machine epsilon times $|a|$ or $|b|$. The returned value is therefore

$$Q = h \sum_{k = -M}^{N} g(kh).$$

**Theorem 1 (convergence of the truncated trapezoidal sum, proved).** Suppose $g \in C^1(\mathbb{R})$ with $\int_{\mathbb{R}} |g'| < \infty$. Then

$$\Big| Q - \int_a^b f \Big| \le h \int_{\mathbb{R}} |g'| + \int_{t < -Mh} \big(|g| + h|g'|\big) + \int_{t > Nh} \big(|g| + h|g'|\big).$$

*Proof.* Let $J_k = [kh, (k+1)h]$; these intervals tile $\mathbb{R}$. For each $k$, $\big|h\,g(kh) - \int_{J_k} g\big| \le \int_{J_k} |g(kh) - g(t)|\,dt \le h \int_{J_k} |g'|$, and so also $h\,|g(kh)| \le \int_{J_k} \big(|g| + h|g'|\big)$. Summing the first inequality over all $k \in \mathbb{Z}$ gives $\big|h \sum_{k \in \mathbb{Z}} g(kh) - \int_{\mathbb{R}} g\big| \le h \int_{\mathbb{R}} |g'|$. The terms omitted by line L2 are those with $k < -M$, whose $J_k$ lie in $(-\infty, -Mh]$, and those with $k > N$, whose $J_k$ lie in $[(N+1)h, \infty)$; summing the second inequality over them bounds the omitted part by the two tail integrals. Combine with Lemma 1. $\square$

**Theorem 2 (the truncation error, proved).** Suppose in addition that $|g(t)| \le C e^{\alpha t}$ for $t \le 0$ and $|g(t)| \le C e^{-\beta t}$ for $t \ge 0$. Equivalently, up to the constant, $|f(x)|\,(x - a)(b - x)/L \le C_1 (x - a)^\alpha$ near $a$ and $\le C_1 (b - x)^\beta$ near $b$, which holds for $f(x) = (x - a)^{\alpha - 1}(b - x)^{\beta - 1}$ times any bounded function. Then

$$\int_{t < -Mh} |g| + \int_{t > Nh} |g| \le C\Big(\frac{1}{\alpha} + \frac{1}{\beta}\Big) e^{-\sqrt{2\pi d \alpha n}} .$$

*Proof.* $\int_{-\infty}^{-Mh} C e^{\alpha t}\,dt = \frac{C}{\alpha} e^{-\alpha M h}$ and $\int_{Nh}^{\infty} C e^{-\beta t}\,dt = \frac{C}{\beta} e^{-\beta N h}$. By line L1, $\beta N \ge \alpha n = \alpha M$, so both exponents are at most $-\alpha n h = -\alpha n \sqrt{2\pi d/(\alpha n)} = -\sqrt{2\pi d \alpha n}$. $\square$

The equivalence of the two forms of the hypothesis follows from Lemma 1: for $t \le 0$, $\psi(t) - a = Le^t/(1 + e^t) \in [Le^t/2, Le^t]$, so a power $(x - a)^\alpha$ is a constant times $e^{\alpha t}$ up to a factor in $[2^{-\alpha}, 1]$, and similarly at $b$. The same argument with $g'$ in place of $g$ handles the $h|g'|$ tail terms whenever $g'$ obeys the same kind of bound.

**The discretization error (cited, not proved here).** Theorem 1 bounds the error of the full sum over $\mathbb{Z}$ only by $O(h)$. The fast rate needs analyticity. Let $D_d = \{z : |\arg\frac{z - a}{b - z}| < d\}$, $0 < d < \pi$, the eye-shaped region that $\varphi$ maps onto the strip $S_d = \{t : |\operatorname{Im} t| < d\}$. If $f$ is analytic in $D_d$ and $g = (f \circ \psi)\,\psi'$ is integrable along horizontal lines in $S_d$ with $\int |g(s + i y)|\,ds \le B$ for $|y| < d$, then

$$\Big| h \sum_{k \in \mathbb{Z}} g(kh) - \int_{\mathbb{R}} g \Big| \le \frac{2B}{e^{2\pi d / h} - 1}$$

(Stenger 1993, the sinc trapezoidal error theorem of Chapter 3; Trefethen and Weideman 2014, Theorem 5.1). With $h$ from line L1, $2\pi d / h = \sqrt{2\pi d \alpha n}$, the same exponent as in Theorem 2. This balance is how line L1 is derived: equating $2\pi d / h$ with $\alpha M h$ gives $h = \sqrt{2\pi d / (\alpha M)}$. Combining it with Theorem 2 gives Stenger's bound

$$\Big| Q - \int_a^b f \Big| \le C' \, e^{-\sqrt{2\pi d \alpha n}}$$

for $f$ in this class, with $C'$ depending on $f$, $d$, $\alpha$, $\beta$ but not on $n$ (Stenger 1981; Stenger 1993; Lund and Bowers 1992). If the true decay rate at $a$ is smaller than the $\alpha$ passed, Theorem 2 with the true rate $\alpha_0$ gives the tail $e^{-\alpha_0 n h}$, which is slower; if $f$ is analytic only in a thinner region $D_{d_0}$, $d_0 < d$, the discretization term becomes $e^{-2\pi d_0/h}$. Both are visible in the tests.

**Orientation and empty intervals.** For $a = b$ the implementation returns 0. For $b < a$ it returns minus the result on $[b, a]$, which is correct since $\int_a^b = -\int_b^a$; $\alpha$ and $\beta$ then describe the lower and upper end of $[b, a]$. Infinite end points are rejected: they need a different map, such as $\varphi(x) = \log x$ on $(0, \infty)$, which this implementation does not provide.

**Termination and cost.** Line L2 runs $M + N + 1 = n + \lceil \alpha n / \beta \rceil + 1$ times, each with one evaluation of $f$ and $O(1)$ other operations, so for $\alpha = \beta$ the cost is $2n + 1$ evaluations and the error is $O(e^{-\sqrt{2\pi d \alpha n}})$; reaching a tolerance $\tau$ takes $n \approx (\log \tau)^2 / (2\pi d \alpha)$. $\blacksquare$
