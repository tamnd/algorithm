---
title: IO-LINEARIZE finds the relative degree when it exists, reports when it does not, and the feedback gives the linear error equation
proves: [correctness, termination]
status: full
---

The system is $\dot x = f(x) + g(x) u$, $y = h(x)$, with $x \in U$, an open subset of $\mathbb{R}^n$, and $f$, $g$, $h$ of class $C^\infty$ on $U$. For a function $\varphi$ and a vector field $X$, $L_X \varphi = \frac{\partial \varphi}{\partial x} X$. The bracket is $[f, g] = \frac{\partial g}{\partial x} f - \frac{\partial f}{\partial x} g$, and $\mathrm{ad}_f^0 g = g$, $\mathrm{ad}_f^{j+1} g = [f, \mathrm{ad}_f^j g]$.

The system has relative degree $r$ at $x_0$ if $L_g L_f^k h(x) = 0$ for all $x$ in a neighborhood of $x_0$ and all $k < r - 1$, and $L_g L_f^{r-1} h(x_0) \neq 0$.

The test at line L8 asks whether $a = L_g \varphi$ vanishes on a neighborhood of $x_0$. In the implementation $f$, $g$ and $h$ are polynomials with rational coefficients, and the test is "$a$ is the zero polynomial". Lemma 1 shows that the two tests agree for polynomials.

## Lemma 1: a polynomial that vanishes on an open set is zero

Let $p$ be a polynomial in $n$ variables that is zero on an open ball around $x_0$. Write $q(z) = p(x_0 + z)$. This is a polynomial in $z$, and its coefficient of $z^\alpha$ is $\partial^\alpha p(x_0) / \alpha!$. All partial derivatives of $p$ at $x_0$ are zero, because $p$ is zero on a neighborhood of $x_0$. So $q$ is the zero polynomial, and so is $p(x) = q(x - x_0)$. $\square$

## Lemma 2: the bracket identity

For a $C^2$ function $\varphi$ and $C^1$ fields $f$, $g$: $L_{[f,g]} \varphi = L_f L_g \varphi - L_g L_f \varphi$.

*Proof.* By the product rule,

$$L_f L_g \varphi = \sum_{i,k} \frac{\partial^2 \varphi}{\partial x_i \partial x_k} g_k f_i + \sum_{i,k} \frac{\partial \varphi}{\partial x_k} \frac{\partial g_k}{\partial x_i} f_i.$$

Swap $f$ and $g$ and subtract. The second derivatives of $\varphi$ are symmetric, so the first sums cancel. What remains is $\sum_k \frac{\partial \varphi}{\partial x_k} \left( \frac{\partial g}{\partial x} f - \frac{\partial f}{\partial x} g \right)_k = L_{[f,g]} \varphi$. $\square$

## Lemma 3: the anti-triangular identity

Let $V$ be an open set on which $L_g L_f^k h = 0$ for $k = 0, \dots, r - 2$. Then on $V$, for all $i, j \ge 0$ with $i + j \le r - 1$,

$$L_{\mathrm{ad}_f^j g} L_f^i h = \begin{cases} 0 & \text{if } i + j \le r - 2, \\ (-1)^j L_g L_f^{r-1} h & \text{if } i + j = r - 1. \end{cases}$$

*Proof.* Induction on $j$. For $j = 0$ the claim is the hypothesis when $i \le r - 2$, and it is trivial when $i = r - 1$. Suppose that it holds for $j$, and let $i + j + 1 \le r - 1$. Lemma 2 with $X = \mathrm{ad}_f^j g$ and $\varphi = L_f^i h$ gives

$$L_{\mathrm{ad}_f^{j+1} g} L_f^i h = L_f \left( L_{\mathrm{ad}_f^j g} L_f^i h \right) - L_{\mathrm{ad}_f^j g} L_f^{i+1} h.$$

In the first term $i + j \le r - 2$, so the function in the brackets is zero on the open set $V$, and its derivative along $f$ is zero on $V$ too. In the second term the index sum is $i + j + 1$. If $i + j + 1 \le r - 2$, the term is zero by the induction hypothesis. If $i + j + 1 = r - 1$, the term is $(-1)^j L_g L_f^{r-1} h$, and with the minus sign in front the result is $(-1)^{j+1} L_g L_f^{r-1} h$. $\square$

## Lemma 4: a relative degree is at most $n$

If the system has relative degree $r$ at $x_0$, then $r \le n$, and the row vectors $dh(x_0), dL_f h(x_0), \dots, dL_f^{r-1} h(x_0)$ are linearly independent.

*Proof.* Let $V$ be the neighborhood in the definition and $a_0 = L_g L_f^{r-1} h(x_0) \neq 0$. Let $R$ be the $r \times n$ matrix with rows $dL_f^i h(x_0)$ and $S$ the $n \times r$ matrix with columns $\mathrm{ad}_f^j g(x_0)$, for $i, j = 0, \dots, r - 1$. The entry $(i, j)$ of $R S$ is $L_{\mathrm{ad}_f^j g} L_f^i h(x_0)$. By Lemma 3 it is zero when $i + j \le r - 2$ and $(-1)^j a_0$ when $i + j = r - 1$. So $R S$ is zero above the anti-diagonal and has nonzero entries on it, and $\det(R S) = \pm a_0^r \neq 0$. Then $r = \operatorname{rank}(R S) \le \operatorname{rank} R \le \min(r, n)$. So $\operatorname{rank} R = r$ and $r \le n$. $\square$

## Termination

The loop at line L2 runs at most $n$ times. Each pass computes two Lie derivatives, one evaluation at $x_0$ and one zero test. For polynomials with rational coefficients each of these is a finite computation. So IO-LINEARIZE stops after at most $n$ passes.

## Correctness of the three outcomes

Invariant: at the start of the pass with index $k$, $\varphi = L_f^k h$, the list $\xi$ holds $h, L_f h, \dots, L_f^{k-1} h$, and $L_g L_f^j h$ vanishes on a neighborhood of $x_0$ for every $j < k$. It holds for $k = 0$ by line L1. A pass that does not return reaches line L9 only when the test at line L8 says that $a = L_g L_f^k h$ vanishes near $x_0$, and line L9 sets $\varphi = L_f^{k+1} h$, so the invariant holds for $k + 1$. For polynomials, "vanishes near $x_0$" and "is the zero polynomial" are the same by Lemma 1, and finitely many neighborhoods have an open intersection.

*Return at line L7.* Here $L_g L_f^j h$ vanishes near $x_0$ for $j < k$ and $L_g L_f^k h(x_0) \neq 0$. This is the definition with $r = k + 1$. The returned $\xi$ is $(h, \dots, L_f^{r-1} h)$, $a = L_g L_f^{r-1} h$ and $b = L_f^r h$.

*Return at line L8.* Here $L_g L_f^j h$ vanishes near $x_0$ for $j < k$, $L_g L_f^k h(x_0) = 0$, and $L_g L_f^k h$ does not vanish on any neighborhood of $x_0$. Suppose that the relative degree $r$ exists at $x_0$. If $r - 1 < k$, then $L_g L_f^{r-1} h(x_0) = 0$, which is false. If $r - 1 = k$, the same value is $L_g L_f^k h(x_0) = 0$, which is false. If $r - 1 > k$, the definition makes $L_g L_f^k h$ zero on a neighborhood of $x_0$, which is false. So no relative degree exists at $x_0$, and UNDEFINED is the correct answer.

*Return at line L10.* All $n$ passes ended at line L9, so $L_g L_f^k h$ vanishes on a neighborhood $W$ of $x_0$ for $k = 0, \dots, n - 1$. Suppose that the system has a relative degree $r$ at some point $p \in W$. Then $L_g L_f^{r-1} h(p) \neq 0$, so $r - 1 \ge n$, which contradicts Lemma 4. So no point near $x_0$ has a relative degree. In the polynomial case $W$ is all of $\mathbb{R}^n$. NO INPUT EFFECT is the correct answer.

## The closed loop

Let IO-LINEARIZE return $r$, $\xi$, $a$, $b$, and let $V$ be an open neighborhood of $x_0$ on which $L_g L_f^k h = 0$ for $k < r - 1$ and $a(x) \neq 0$. Let $y_d$ be $r$ times continuously differentiable. Line L11 applies

$$u = \frac{v - b(x)}{a(x)}, \qquad v = y_d^{(r)}(t) - \sum_{i=0}^{r-1} c_i \left( L_f^i h(x) - y_d^{(i)}(t) \right).$$

On $V$ the closed-loop field is continuous in $t$ and $C^1$ in $x$, so it is locally Lipschitz in $x$, and the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) gives one solution $x(t)$ for as long as it stays in $V$.

Along this solution, for $i \le r - 2$,

$$\frac{d}{dt} L_f^i h(x) = L_f^{i+1} h(x) + L_g L_f^i h(x)\, u = L_f^{i+1} h(x),$$

so by induction $y^{(i)} = L_f^i h(x)$ for $i = 0, \dots, r - 1$. One more derivative gives $y^{(r)} = L_f^r h(x) + L_g L_f^{r-1} h(x)\, u = b(x) + a(x) u = v$. Let $e = y - y_d$. Then $e^{(i)} = L_f^i h(x) - y_d^{(i)}$ for $i < r$, and

$$e^{(r)} = y^{(r)} - y_d^{(r)} = v - y_d^{(r)} = -\sum_{i=0}^{r-1} c_i e^{(i)}.$$

So the error obeys $e^{(r)} + c_{r-1} e^{(r-1)} + \dots + c_0 e = 0$ while the state stays in $V$. Its characteristic polynomial is $s^r + c_{r-1} s^{r-1} + \dots + c_0$, and if this polynomial is Hurwitz, $e$ and its first $r - 1$ derivatives go to zero exponentially. This says nothing about the other $n - r$ state coordinates. They must be checked separately, with the zero dynamics. $\blacksquare$
