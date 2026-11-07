---
title: A candidate that divides both inputs is the gcd
proves: [correctness, termination]
status: full
---

Let $f, g \in \mathbb{Z}[x]$ be nonzero and primitive, as after line L1. Let $G = \gcd(f, g)$, primitive with a positive leading coefficient. Fix an integer $\xi \ge 2 \min(|f|_\infty, |g|_\infty) + 2$, and say $a \in \{f, g\}$ is the input with $|a|_\infty = \min(|f|_\infty, |g|_\infty)$. Every point used by the algorithm satisfies this bound: line L2 sets $\xi$ to it, and line L8 never makes $\xi$ smaller, because $\lfloor \xi \cdot 73794 / 27011 \rfloor \ge \xi$ for $\xi \ge 1$.

**Fact 1 (Cauchy bound).** If $p \in \mathbb{Z}[x]$ divides $a$ and $\alpha \in \mathbb{C}$ is a root of $p$, then $|\alpha| < 1 + |a|_\infty \le \xi / 2$.

*Proof.* $\alpha$ is a root of $a = \sum_{i=0}^{m} a_i x^i$ with $a_m \ne 0$. If $|\alpha| \le 1$ the claim holds since $|a|_\infty \ge 1$. Otherwise $a_m \alpha^m = -\sum_{i < m} a_i \alpha^i$ gives
$$|\alpha|^m \le |a_m| |\alpha|^m \le |a|_\infty \sum_{i < m} |\alpha|^i = |a|_\infty \frac{|\alpha|^m - 1}{|\alpha| - 1} < |a|_\infty \frac{|\alpha|^m}{|\alpha| - 1},$$
so $|\alpha| - 1 < |a|_\infty$. Finally $1 + |a|_\infty \le \xi / 2$ is the bound on $\xi$. $\square$

**Fact 2.** If $p \in \mathbb{Z}[x]$ divides $a$ and $\deg p = e \ge 1$, then $|p(\xi)| > (\xi / 2)^e \ge \xi / 2$. If $p$ divides $a$ and $p \ne 0$, then $p(\xi) \ne 0$.

*Proof.* Write $p = \operatorname{lc}(p) \prod_{j=1}^{e} (x - \alpha_j)$. By Fact 1, $|\xi - \alpha_j| \ge \xi - |\alpha_j| > \xi - \xi/2 = \xi/2$, and $|\operatorname{lc}(p)| \ge 1$. So $|p(\xi)| > (\xi/2)^e$, which is at least $\xi/2$ because $\xi / 2 \ge 1$. For $e = 0$, $p$ is a nonzero constant. $\square$

**Fact 3.** For $\gamma \ne 0$, $\tilde h = \operatorname{genpoly}(\gamma, \xi)$ is nonzero, satisfies $\tilde h(\xi) = \gamma$, and every coefficient lies in $(-\xi/2, \xi/2]$. Hence $|\operatorname{cont}(\tilde h)| \le \xi / 2$.

*Proof.* The expansion loop keeps $\gamma_{\text{orig}} = \sum_{j < i} h_j \xi^j + \gamma_i \xi^i$, where $\gamma_i$ is the value of $\gamma$ after $i$ steps, and it stops when $\gamma_i = 0$. It does stop: if $|\gamma_i| \ge 1$ then $|\gamma_{i+1}| \le (|\gamma_i| + \xi/2)/\xi < |\gamma_i|$, because $\xi \ge 2$. Each digit is chosen in $(-\xi/2, \xi/2]$. The content divides each nonzero coefficient, so it is at most $\xi/2$ in absolute value, and there is a nonzero coefficient since $\gamma \ne 0$. $\square$

**Theorem.** At any try, let $\gamma = \gcd(f(\xi), g(\xi))$, $\tilde h = \operatorname{genpoly}(\gamma, \xi)$ and $h = \operatorname{pp}(\tilde h)$. If $h$ divides $f$ and $g$ in $\mathbb{Z}[x]$, then $h = G$.

*Proof.* By Fact 2 with $p = a$, $a(\xi) \ne 0$, so $\gamma \ne 0$ and Fact 3 applies. Write $\tilde h = c\, h$ with $c = \pm \operatorname{cont}(\tilde h)$, so $0 < |c| \le \xi/2$.

Since $h$ is primitive and divides $f$ and $g$, it divides $G$ (in $\mathbb{Z}[x]$, a common divisor divides the gcd). Write $G = h k$ with $k \in \mathbb{Z}[x]$. Since $G$ divides $f$ and $g$, the integer $G(\xi)$ divides $f(\xi)$ and $g(\xi)$, hence divides $\gamma$: $\gamma = m\, G(\xi)$ for a nonzero integer $m$. Now
$$c\, h(\xi) = \tilde h(\xi) = \gamma = m\, G(\xi) = m\, h(\xi)\, k(\xi).$$
The polynomial $h$ divides $a$ and is nonzero, so $h(\xi) \ne 0$ by Fact 2, and therefore $c = m\, k(\xi)$. So $|k(\xi)| \le |c| \le \xi / 2$.

The polynomial $k$ divides $G$, which divides $a$. If $\deg k \ge 1$, Fact 2 gives $|k(\xi)| > \xi / 2$, a contradiction. So $k$ is a nonzero integer constant. Both $G$ and $h$ are primitive, so $k = \pm 1$, and both have positive leading coefficients, so $k = 1$ and $h = G$. $\blacksquare$

**Correctness of the output.** If line L7 returns, the theorem gives $h = \gcd(\operatorname{pp} f, \operatorname{pp} g)$, and by Gauss's lemma $c \cdot h = \gcd(f, g)$ for $c = \gcd(\operatorname{cont} f, \operatorname{cont} g)$. Otherwise the algorithm returns FAIL, which makes no claim.

**Termination.** Each try does finitely many integer operations: an evaluation, an integer gcd, a terminating expansion (Fact 3), and two trial divisions, each of which lowers the degree of the remainder at every step. The loop of line L3 runs at most $T$ times. $\blacksquare$
