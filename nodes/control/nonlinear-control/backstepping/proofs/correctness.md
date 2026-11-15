---
title: Backstepping gives V' = -sum c_i z_i^2 along the closed loop, and the origin of a strict feedback system becomes globally asymptotically stable
proves: [correctness, termination]
status: full
---

The system is in strict feedback form:

$$\dot x_i = f_i(\bar x_i) + g_i(\bar x_i)\, x_{i+1} \quad (1 \le i \le n - 1), \qquad \dot x_n = f_n(\bar x_n) + g_n(\bar x_n)\, u,$$

where $\bar x_i = (x_1, \dots, x_i)$. The functions $f_i, g_i : \mathbb{R}^i \to \mathbb{R}$ are smooth ($C^\infty$), $f_i(0) = 0$, and $g_i(\bar x_i) \neq 0$ for every $\bar x_i$. The gains $c_1, \dots, c_n$ are positive. Put $\alpha_0 = 0$, $z_0 = 0$ and $g_0 = 0$, and for $i = 1, \dots, n$ define

$$z_i = x_i - \alpha_{i-1}(\bar x_{i-1}), \qquad D_i = \sum_{j=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_j} \bigl(f_j + g_j x_{j+1}\bigr), \qquad \alpha_i = \frac{-c_i z_i - g_{i-1} z_{i-1} - f_i + D_i}{g_i}.$$

These are lines L3, L4 and L5. The feedback is $u = \alpha_n(x)$ (line L6), and $V = \frac12 \sum_{i=1}^n z_i^2$.

## Termination

The algorithm defines $\alpha_1, \dots, \alpha_n$ once each. The implementation does this by a recursion on $i$ that stops at $i = 0$, so it ends after $n$ levels.

## Lemma 1: each alpha_i is smooth, depends only on the first i states, and is zero at zero

By induction on $i$. $\alpha_0 = 0$. Suppose the claim holds for $\alpha_{i-1}$. Then $z_i$ and $z_{i-1}$ are smooth functions of $\bar x_i$. $D_i$ uses the first partial derivatives of $\alpha_{i-1}$, which are smooth, and the terms $f_j + g_j x_{j+1}$ for $j \le i - 1$, which depend only on $\bar x_i$. $g_{i-1}$ and $f_i$ are smooth, and $g_i$ is smooth and never zero, so the quotient $\alpha_i$ is smooth on $\mathbb{R}^i$. At $x = 0$: $\alpha_{i-1}(0) = 0$ gives $z_i = z_{i-1} = 0$; $f_j(0) = 0$ gives $f_j + g_j x_{j+1} = 0$, so $D_i = 0$; and $f_i(0) = 0$. So $\alpha_i(0) = 0$. $\square$

## Lemma 2: the error dynamics

Along every solution of the closed loop, for $i = 1, \dots, n$,

$$\dot z_i = -c_i z_i - g_{i-1} z_{i-1} + g_i z_{i+1},$$

with the convention $g_n z_{n+1} = 0$.

*Proof.* By the chain rule, $\frac{d}{dt} \alpha_{i-1}(\bar x_{i-1}) = \sum_{j=1}^{i-1} \frac{\partial \alpha_{i-1}}{\partial x_j} \dot x_j$. For $j \le i - 1 \le n - 1$, $\dot x_j = f_j + g_j x_{j+1}$, so this sum is $D_i$. Hence $\dot z_i = \dot x_i - D_i$.

For $i \le n - 1$: $\dot x_i = f_i + g_i x_{i+1}$, and $x_{i+1} = z_{i+1} + \alpha_i$ by the definition of $z_{i+1}$. So

$$\dot z_i = f_i + g_i \alpha_i + g_i z_{i+1} - D_i = f_i + (-c_i z_i - g_{i-1} z_{i-1} - f_i + D_i) + g_i z_{i+1} - D_i = -c_i z_i - g_{i-1} z_{i-1} + g_i z_{i+1}.$$

For $i = n$: $\dot x_n = f_n + g_n u = f_n + g_n \alpha_n$, and the same computation without the term $g_n z_{n+1}$ gives $\dot z_n = -c_n z_n - g_{n-1} z_{n-1}$. $\square$

## Lemma 3: the derivative of V

Along the closed loop, $\dot V = -\sum_{i=1}^n c_i z_i^2$.

*Proof.* By Lemma 2,

$$\dot V = \sum_{i=1}^n z_i \dot z_i = -\sum_{i=1}^n c_i z_i^2 - \sum_{i=2}^{n} g_{i-1} z_{i-1} z_i + \sum_{i=1}^{n-1} g_i z_i z_{i+1}.$$

The term $i = 1$ of the first cross sum is absent because $g_0 = 0$. Shift the index of the second cross sum by one: $\sum_{i=1}^{n-1} g_i z_i z_{i+1} = \sum_{i=2}^{n} g_{i-1} z_{i-1} z_i$. The two cross sums cancel. $\square$

## Lemma 4: the change of coordinates

The map $\Phi : x \mapsto z$ is a smooth bijection of $\mathbb{R}^n$ with a smooth inverse, and $\Phi(0) = 0$.

*Proof.* $\Phi$ is smooth by Lemma 1. Given $z$, the equations $x_i = z_i + \alpha_{i-1}(\bar x_{i-1})$ for $i = 1, 2, \dots, n$ determine $x_1 = z_1$, then $x_2$, and so on, in a unique way. So $\Phi$ is a bijection, and the inverse is a composition of smooth maps. $\Phi(0) = 0$ by Lemma 1. $\square$

## Theorem: global asymptotic stability

With $u = \alpha_n(x)$, the origin of the closed loop is globally asymptotically stable, and $|z(t)| \le e^{-c\, t} |z(0)|$ with $c = \min_i c_i$.

*Proof.* The closed loop $\dot x = F(x)$ is smooth by Lemma 1, so it is locally Lipschitz and solutions are unique (Picard-Lindelöf). $V(x) = \frac12 |\Phi(x)|^2$ is smooth. It is positive definite, because $V(x) = 0$ only if $\Phi(x) = 0$, that is, $x = 0$ (Lemma 4). It is proper: the sublevel set $\{V \le r\}$ is the image of the compact ball $\{|z|^2 \le 2 r\}$ under the continuous map $\Phi^{-1}$, so it is compact. By Lemma 3, $\dot V \le -c |z|^2 = -2 c V$, which is negative for $x \neq 0$. Every solution stays in the compact set $\{V \le V(x(0))\}$, so it exists for all $t \ge 0$. Lyapunov's direct method gives global asymptotic stability. The comparison $\dot V \le -2 c V$ gives $V(t) \le e^{-2 c t} V(0)$, which is the bound on $|z(t)|$. $\square$

## Lemma 5: the dual numbers compute D_i exactly

Let $R$ be a commutative ring that contains the values of the state, and let $R[\varepsilon] = R[e]/(e^2)$ with a new symbol $\varepsilon$. A value $a + b \varepsilon$ is stored as a dual number with a tag that is larger than every tag inside $a$ and $b$. The operations of the class `Dual` are the ring operations of $R[\varepsilon]$: $(a + b\varepsilon) + (c + d\varepsilon) = (a + c) + (b + d)\varepsilon$, $(a + b\varepsilon)(c + d\varepsilon) = a c + (a d + b c)\varepsilon$, and $(a + b\varepsilon)/(c + d\varepsilon) = a/c + \frac{b c - a d}{c^2}\varepsilon$ when $c$ is invertible. The functions $\sin$, $\cos$ and $\exp$ use $h(a + b\varepsilon) = h(a) + h'(a)\, b\, \varepsilon$.

*Claim.* For every function $h$ built from these operations and a point $x$ and direction $v$ with entries in $R$, evaluating $h$ at $x + \varepsilon v$ gives $h(x) + (\nabla h(x) \cdot v)\, \varepsilon$.

*Proof.* By induction on the expression. Constants and coordinates are clear. For a sum, a product and a quotient, the rules above are the sum, product and quotient rules of differentiation. For $\sin$, $\cos$ and $\exp$, the rule is the chain rule. These identities hold in any commutative ring $R$, so they hold when $R$ itself contains dual numbers with smaller tags. $\square$

In the implementation, step $i$ evaluates $\alpha_{i-1}$ at $x + \varepsilon v$ with a new tag, where $v_j = f_j + g_j x_{j+1}$ for $j < i$. By the claim, the coefficient of $\varepsilon$ is $\nabla \alpha_{i-1} \cdot v = D_i$, and the part without $\varepsilon$ is $\alpha_{i-1}(x)$. Every tag made inside the evaluation of $\alpha_{i-1}$ is removed before it returns, so the result has no tag larger than the new one, and the split is unambiguous. The rest of step $i$ is line L5 as written. So the code returns $\alpha_n(x)$ and the errors $z_i$ exactly when the inputs are exact rationals and $f_i$, $g_i$ are rational functions, and up to floating point rounding otherwise. $\blacksquare$
