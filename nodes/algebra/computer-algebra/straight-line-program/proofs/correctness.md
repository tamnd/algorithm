---
title: Correctness of evaluation, reverse-mode gradient, degree bound and zero test for straight-line programs
proves: [correctness]
status: full
---

**Setting.** $R$ is a commutative ring and $\gamma_1, \ldots, \gamma_L$ is a program in $n$ variables, as defined on the page. Its values $v_1, \ldots, v_L \in R[x_1, \ldots, x_n]$ are defined by $v_j = x_i$, $v_j = c$ or $v_j = v_a \circ v_b$, according to $\gamma_j$, and $f = v_L$ (with $f = 0$ if $L = 0$). For $\xi \in R^n$ let $\phi_\xi : R[x_1, \ldots, x_n] \to R$ be evaluation at $\xi$.

**Theorem.** (a) EVALUATE returns $f(\xi)$, and with reduction modulo $p$ it returns $f(\xi) \bmod p$. (b) GRADIENT returns $(\partial f / \partial x_1 (\xi), \ldots, \partial f / \partial x_n (\xi))$, where $\partial / \partial x_i$ is the formal derivative. (c) The propagated bound $\delta_j$ satisfies $\deg v_j \le \delta_j$, with $\delta_j = -1$ only if $v_j = 0$. (d) If $R = \mathbb{Z}/p\mathbb{Z}$ and $f \ne 0$ has total degree at most $D$, then $s$ independent uniform points all give $0$ with probability at most $(D / p)^s$; if $f = 0$, they all give $0$.

## Proof of (a)

By induction on $j$, the stored value is $\phi_\xi(v_j)$. For a load this is the definition. For $v_j = v_a \circ v_b$ with $a, b < j$, the stored value is $\phi_\xi(v_a) \circ \phi_\xi(v_b) = \phi_\xi(v_a \circ v_b)$, since $\phi_\xi$ is a ring homomorphism. The map $R \to R / pR$ is also a ring homomorphism, so reducing after each step gives the image of $\phi_\xi(v_j)$, by the same induction. $\square$

## Proof of (b)

Introduce new indeterminates $y_1, \ldots, y_L$. For $j = L, L - 1, \ldots, 0$ define $F_j \in R[x_1, \ldots, x_n, y_1, \ldots, y_j]$ by $F_L = y_L$ and
$$F_{j-1} = F_j \big|_{y_j \leftarrow e_j}, \qquad e_j = \begin{cases} x_i & \text{if } \gamma_j = x_i, \\ c & \text{if } \gamma_j = c, \\ y_a \circ y_b & \text{if } \gamma_j = v_a \circ v_b. \end{cases}$$
Substituting the values for the $y$'s shows that $F_j(x, v_1, \ldots, v_j) = f$ for every $j$, and $F_0 = f$. Write $\bar{\cdot}$ for evaluation at $x = \xi$, $y_k = v_k(\xi)$.

*Claim.* When the loop of G4 is about to handle index $j$, we have $w_k = \overline{\partial F_j / \partial y_k}$ for all $k \le j$, and $g_i = \overline{\partial F_j / \partial x_i}$ for all $i$.

For $j = L$: $F_L = y_L$, so $\partial F_L / \partial y_L = 1$ and all other derivatives are $0$, which matches G2 and G3.

Step from $j$ to $j - 1$. By the chain rule for formal derivatives (which holds over any commutative ring, because both sides are $R$-linear derivations that agree on monomials),
$$\frac{\partial F_{j-1}}{\partial u} = \Bigl(\frac{\partial F_j}{\partial u} + \frac{\partial F_j}{\partial y_j} \cdot \frac{\partial e_j}{\partial u}\Bigr)\Big|_{y_j \leftarrow e_j}$$
for every indeterminate $u$ other than $y_j$. After evaluation, the substitution $y_j \leftarrow e_j$ has no effect, because $\bar{e}_j = v_j(\xi)$ by (a). So the new value for $u$ is the old one plus $\bar{w}_j \cdot \overline{\partial e_j / \partial u}$, where $w_j$ is the current value at index $j$. Now $\partial e_j / \partial u$ is: $1$ for $u = x_i$ if $\gamma_j = x_i$ (step G5); $1$ for $u = y_a$ and $\pm 1$ for $u = y_b$ if $\gamma_j = v_a \pm v_b$ (step G6); $y_b$ for $u = y_a$ and $y_a$ for $u = y_b$ if $\gamma_j = v_a \times v_b$, with sum $2 y_a$ if $a = b$, and the code adds both terms (step G7); and $0$ in all other cases and for constants. These are exactly the updates of the loop body, so the claim holds for $j - 1$.

At the end ($j = 0$), $g_i = \overline{\partial F_0 / \partial x_i} = \partial f / \partial x_i (\xi)$. If $L = 0$, then $f = 0$ and G2 returns the zero vector, which is correct. $\square$

**Cost.** The forward pass is $L$ operations. In the backward pass each instruction costs at most two multiplications and two additions, so the total is at most $5L$ operations.

## Proof of (c)

By induction on $j$. Loads: $\deg x_i = 1$, $\deg c = 0$ for $c \ne 0$, and the bound $-1$ is used only for $c = 0$. For $v_a \pm v_b$: $\deg(v_a \pm v_b) \le \max(\deg v_a, \deg v_b) \le \max(\delta_a, \delta_b)$, and if the maximum is $-1$ then both are $0$, so the sum is $0$. For $v_a v_b$: $\deg(v_a v_b) \le \deg v_a + \deg v_b$ over any commutative ring (the product of the top parts may vanish, but no larger degree can appear), and the code sets $-1$ exactly when one factor has bound $-1$, in which case that factor is $0$ and so is the product. $\square$

## Proof of (d)

If $f = 0$ then $f(\xi) = 0$ for all $\xi$, so by (a) every point gives $0$. If $f \ne 0$ has total degree at most $D$, the Schwartz-Zippel lemma gives $\Pr[f(\xi) = 0] \le D / p$ for a uniform $\xi \in (\mathbb{Z}/p\mathbb{Z})^n$. The points are independent, so all $s$ give $0$ with probability at most $(D / p)^s$. By (c), the propagated bound $\delta_L$ can serve as $D$. $\blacksquare$
