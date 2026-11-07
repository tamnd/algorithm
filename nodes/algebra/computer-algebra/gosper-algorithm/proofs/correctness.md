---
title: Gosper's algorithm finds a hypergeometric antidifference exactly when one exists
proves: [correctness, termination]
status: full
---

Let $K$ be a field of characteristic 0 (the implementation uses $K = \mathbb{Q}$), and let $t$ be a hypergeometric term with ratio $r(n) = t(n+1)/t(n) = \mathrm{num}(n)/\mathrm{den}(n)$, where $\mathrm{num}, \mathrm{den} \in K[n]$ are nonzero. A *hypergeometric antidifference* of $t$ is a hypergeometric term $z$ with $z(n+1) - z(n) = t(n)$.

**Lemma 1 (reduction to a rational equation).** $t$ has a hypergeometric antidifference if and only if there is a rational function $y \in K(n)$ with

$$r(n)\, y(n+1) - y(n) = 1. \tag{1}$$

If $y$ solves (1), then $z = y t$ is an antidifference.

*Proof.* If $y$ solves (1) and $z = y t$, then $z(n+1) - z(n) = y(n+1) r(n) t(n) - y(n) t(n) = t(n)$, and $z$ is hypergeometric because $z(n+1)/z(n) = r(n) y(n+1)/y(n)$ is rational. Conversely, let $z$ be a hypergeometric antidifference with ratio $\rho = z(n+1)/z(n) \in K(n)$. Then $t = z(\rho - 1)$, and $\rho \ne 1$ since $t \ne 0$. So $y = z/t = 1/(\rho - 1)$ is rational, and $y t = z$ gives (1). $\square$

**Lemma 2 (the Gosper form).** Lines L1 to L4 terminate, and afterwards

$$r(n) = \frac{a(n)}{b(n)} \cdot \frac{c(n+1)}{c(n)}, \qquad \gcd(a(n), b(n+h)) = 1 \text{ for every integer } h \ge 0. \tag{2}$$

*Proof.* After line L1, $a/b = r$ and $c = 1$, so (2) holds in its first part. Suppose an update at line L4 is made with $g = \gcd(a(n), b(n+h))$, so $g(n) \mid a(n)$ and $g(n-h) \mid b(n)$. Let $C(n) = \prod_{i=1}^{h} g(n-i)$. Then $C(n+1)/C(n) = g(n)/g(n-h)$ by telescoping the product, so

$$\frac{a(n)}{b(n)} = \frac{a(n)/g(n)}{b(n)/g(n-h)} \cdot \frac{C(n+1)}{C(n)},$$

and replacing $a$, $b$, $c$ by $a/g$, $b/g(n-h)$, $c\,C$ keeps the first part of (2). Each update lowers $\deg a$ by $\deg g \ge 1$, so there are at most $\deg \mathrm{num}$ updates, and the loops stop.

For the coprimality, note that $a$ and $b$ are only ever divided, so their roots are among the roots of $\mathrm{num}$ and $\mathrm{den}$ (in an algebraic closure). If $\gcd(a(n), b(n+h)) \ne 1$ for some integer $h \ge 0$, there is a root $\alpha$ of $a$ with $b(\alpha + h) = 0$, so $h = \beta - \alpha$ for a root $\beta$ of $b$, and $h \le |\alpha| + |\beta| \le H$ by Fujiwara's bound, which is what `root_bound` computes. So only $h \le H$ can fail. The loop of line L2 visits each such $h$, and the inner loop at line L3 runs until $\gcd(a(n), b(n+h)) = 1$. Later updates divide $a$ and $b$ further, which cannot create a common factor of $a(n)$ and $b(n + h')$ for an $h'$ already visited. $\square$

**Lemma 3 (the polynomial equation).** With $a, b, c$ as in (2) and $B(n) = b(n-1)$, a rational $y$ solves (1) if and only if $y = B(n)\,x(n)/c(n)$ for a *polynomial* $x$ with

$$a(n)\, x(n+1) - B(n)\, x(n) = c(n). \tag{3}$$

*Proof.* Put $x = c\,y/B$, a rational function. Substituting $y = B x / c$ and $r = (a/b)(c(n+1)/c(n))$ into (1):

$$\frac{a(n)}{b(n)} \frac{c(n+1)}{c(n)} \cdot \frac{b(n)\, x(n+1)}{c(n+1)} - \frac{b(n-1)\, x(n)}{c(n)} = 1,$$

which after multiplying by $c(n)$ is (3). So (1) and (3) are equivalent; it remains to show that a rational solution $x$ of (3) is a polynomial.

Write $x = f/g$ in lowest terms with $g$ monic, and suppose $\deg g \ge 1$. Multiplying (3) by $g(n) g(n+1)$ gives

$$a(n) f(n+1) g(n) - B(n) f(n) g(n+1) = c(n) g(n) g(n+1).$$

Hence $g(n+1)$ divides $a(n) f(n+1) g(n)$, and since $\gcd(f(n+1), g(n+1)) = 1$, $g(n+1) \mid a(n) g(n)$. In the same way $g(n) \mid B(n) g(n+1)$.

Let $S$ be the finite set of roots of $g$ in an algebraic closure. Choose $\gamma \in S$ and $m \ge 0$ such that $\gamma, \gamma + 1, \ldots, \gamma + m \in S$, $\gamma - 1 \notin S$ and $\gamma + m + 1 \notin S$; this exists because $S$ is finite and nonempty. The point $n = \gamma - 1$ is a root of $g(n+1)$ but not of $g(n)$, so by $g(n+1) \mid a(n) g(n)$ it is a root of $a$: $a(\gamma - 1) = 0$. The point $n = \gamma + m$ is a root of $g(n)$ but not of $g(n+1)$, so by $g(n) \mid B(n) g(n+1)$ it is a root of $B$: $b(\gamma + m - 1) = 0$. Then $a(n)$ and $b(n + m)$ have the common root $n = \gamma - 1$, which contradicts (2) with $h = m \ge 0$. So $g = 1$ and $x$ is a polynomial. $\square$

**Lemma 4 (degree bound).** Every polynomial solution $x$ of (3) has degree at most $D$, the value computed at line L5.

*Proof.* Since $c \ne 0$, $x \ne 0$; let $e = \deg x$ and $x = x_e n^e + \cdots$ with $x_e \ne 0$. Write $d_1 = \deg a$, $d_2 = \deg B$, $\lambda_a = \operatorname{LC}(a)$ and $\lambda_B = \operatorname{LC}(B)$. Note $x(n+1) = x_e n^e + (e x_e + x_{e-1}) n^{e-1} + \cdots$.

- If $d_1 \ne d_2$, the left side of (3) has degree exactly $\max(d_1, d_2) + e$, with leading coefficient $\lambda_a x_e$ or $-\lambda_B x_e$. So $e = \deg c - \max(d_1, d_2)$.
- If $d_1 = d_2 = d$ and $\lambda_a \ne \lambda_B$, the coefficient of $n^{d + e}$ is $(\lambda_a - \lambda_B) x_e \ne 0$, so $e = \deg c - d$.
- If $d_1 = d_2 = d$ and $\lambda_a = \lambda_B = \lambda$, the coefficient of $n^{d+e}$ cancels. Let $\alpha$ and $\beta$ be the coefficients of $n^{d-1}$ in $a$ and $B$ (0 if $d = 0$). The coefficient of $n^{d + e - 1}$ is $\lambda (e x_e + x_{e-1}) + \alpha x_e - \lambda x_{e-1} - \beta x_e = x_e (\lambda e + \alpha - \beta)$. If $e \ne (\beta - \alpha)/\lambda$, this is nonzero, so $d + e - 1 = \deg c$ and $e = \deg c - d + 1$. Otherwise $e = (\beta - \alpha)/\lambda$, which is then a nonnegative integer.

In each case $e \le D$, as computed by `degree_bound`. $\square$

**Theorem.** GOSPER$(\mathrm{num}, \mathrm{den})$ terminates. It returns a rational $y$ that solves (1) if such a $y$ exists, and returns None otherwise. In the first case $z = y t$ is a hypergeometric antidifference of $t$; in the second, $t$ has none.

*Proof.* Termination: Lemma 2 for lines L1 to L4, and the rest is straight-line code with one linear system. By Lemma 2 the form (2) holds at line L5. If $D < 0$, Lemma 4 shows that (3) has no polynomial solution, and line L6 returns None. Otherwise line L7 sets up (3) as a linear system for the coefficients $x_0, \ldots, x_D$, which by Lemma 4 contains every polynomial solution; line L8 returns None exactly when there is none. By Lemma 3, (1) has a rational solution exactly when (3) has a polynomial one, and line L9 returns $y = B x / c$, reduced, which solves (1). Lemma 1 turns both answers into the statements about antidifferences. $\blacksquare$
