---
title: The GCD test is exact for one equation without bounds, and sound with bounds
proves: [correctness]
status: full
---

We use the setting of the page. A subscript pair is $f(\vec{i}) = a_0 + \sum_{l=1}^{k} a_l i_l$ for the source and $g(\vec{j}) = b_0 + \sum_{l=1}^{k} b_l j_l$ for the sink, with integer coefficients. The direction vector $\vec{\psi} \in \{<, =, >, *\}^k$ is optional; $E = \{l : \psi_l = {=}\}$ is the set of its "=" entries. The equation $f(\vec{i}) = g(\vec{j})$ is

$$\sum_{l=1}^{k} a_l i_l - \sum_{l=1}^{k} b_l j_l = c, \qquad c = b_0 - a_0. \tag{1}$$

We take $\gcd(0, 0) = 0$ and $\gcd(x, 0) = |x|$, and the gcd of a list is the gcd of its entries taken one at a time. This gives the same value in any order, and $\gcd(x, -y) = \gcd(x, y)$.

## Lemma 1 (Bezout for $n$ variables)

Let $\alpha_1, \dots, \alpha_n$ be integers and $G = \gcd(\alpha_1, \dots, \alpha_n)$. Then the set $I = \{\sum_v \alpha_v x_v : \vec{x} \in \mathbb{Z}^n\}$ is equal to $G\mathbb{Z} = \{G t : t \in \mathbb{Z}\}$. So the equation $\sum_v \alpha_v x_v = c$ has an integer solution if and only if $G$ divides $c$, where "$0$ divides $c$" means $c = 0$.

*Proof.* If all $\alpha_v$ are $0$, then $I = \{0\}$ and $G = 0$, so $I = G\mathbb{Z}$. Otherwise $I$ has a positive element (take $x_v = \pm 1$ for one nonzero $\alpha_v$ and $0$ elsewhere). Let $d$ be the smallest positive element of $I$. The set $I$ is closed under sums and under multiplication by integers.

- *Every element of $I$ is a multiple of $d$.* Take $y \in I$ and divide: $y = q d + r$ with $0 \le r < d$. Then $r = y - q d \in I$, and $r < d$, so $r$ is not positive. So $r = 0$.
- *$d = G$.* Each $\alpha_v$ is in $I$ (take the unit vector), so $d$ divides each $\alpha_v$, and therefore $d$ divides $G$. Also $G$ divides each $\alpha_v$, so $G$ divides each element $\sum_v \alpha_v x_v$ of $I$, and in particular $d$. Both are positive, so $d = G$.

So $I \subseteq G\mathbb{Z}$ by the first point, and $G\mathbb{Z} \subseteq I$ because $G = d \in I$ and $I$ is closed under integer multiples. $\square$

## Lemma 2 (the witness)

`ext_gcd(a, b)` returns $(g, x, y)$ with $a x + b y = g = \gcd(a, b)$, and `solve_linear(coefs, c)` returns an integer vector $\vec{x}$ with $\sum_v \alpha_v x_v = c$ when $G$ divides $c$, and `None` otherwise.

*Proof.* In `ext_gcd`, let $a^*$ and $b^*$ be the inputs. The loop keeps $a^* x_0 + b^* y_0 = a$ and $a^* x_1 + b^* y_1 = b$: at the start $(x_0, y_0, x_1, y_1) = (1, 0, 0, 1)$, and one step replaces $(a, b)$ with $(b, a - q b)$ and the coefficient pairs in the same way. It also keeps $\gcd(a, b)$, since a common divisor of $a$ and $b$ divides $a - qb$, and back. Python's `divmod` gives $|a - q b| < |b|$, so $|b|$ falls at each step and the loop ends with $b = 0$. Then $\gcd(a^*, b^*) = \gcd(a, 0) = |a|$, and the sign flip makes $g \ge 0$.

In `solve_linear`, after the step for index $v$ the vector satisfies $\sum_{u \le v} \alpha_u x_u = g$ with $g = \gcd(\alpha_1, \dots, \alpha_v)$ (the other entries are $0$). Before the first step this holds with $g = 0$ and $\vec{x} = \vec{0}$. A step computes $s g + t \alpha_v = h = \gcd(g, \alpha_v)$, multiplies the old vector by $s$, and sets $x_v = t$; the new sum is $s g + t \alpha_v = h$. At the end, $g = G$. If $G = 0$, all coefficients are $0$, and the zero vector solves the equation exactly when $c = 0$. If $G \ne 0$ and $G$ divides $c$, multiplying by $c / G$ gives a solution. If $G$ does not divide $c$, Lemma 1 says that there is none, and the function returns `None`. $\square$

## Theorem 1 (exactness of one subscript without bounds)

Let $G$ be the value of $g$ after lines L2 to L5 of `gcd_test_subscript`. Then the test answers "maybe" if and only if equation (1) has an integer solution $(\vec{i}, \vec{j})$ with $i_l = j_l$ for all $l \in E$, with no bounds and no other constraint.

*Proof.* Put $i_l = j_l = t_l$ for $l \in E$. Equation (1) with these equalities is the equation

$$\sum_{l \in E} (a_l - b_l)\, t_l + \sum_{l \notin E} \bigl(a_l i_l + (-b_l) j_l\bigr) = c$$

in the free integer variables $t_l$ ($l \in E$), and $i_l, j_l$ ($l \notin E$). Its solutions are exactly the solutions of (1) with the equalities. Lines L2 to L5 compute $G = \gcd\bigl(\{a_l - b_l : l \in E\} \cup \{a_l, b_l : l \notin E\}\bigr)$: line L4 adds $a_l - b_l$, line L5 adds $a_l$ and $b_l$, and $\gcd(\cdot, b_l) = \gcd(\cdot, -b_l)$. This is the gcd of the coefficients of the equation above. By Lemma 1 the equation has a solution if and only if $G$ divides $c$. Lines L6 to L8 return "maybe" in exactly this case: for $G = 0$ when $c = 0$, and for $G \ne 0$ when $c \bmod G = 0$. $\square$

## Theorem 2 (soundness)

If two references have a dependence, that is, integer vectors $\vec{i}$ and $\vec{j}$ in the loop bounds that make all $m$ subscript pairs equal and satisfy $i_l \,\psi_l\, j_l$ for each $l$, then `gcd_test` returns "maybe". Equivalently, the answer "independent" proves that there is no dependence with the direction vector $\vec{\psi}$.

*Proof.* Take such $\vec{i}$ and $\vec{j}$, and one subscript pair. The pair satisfies equation (1) of that subscript, and $i_l = j_l$ for $l \in E$ because $\psi_l$ is "=". It is therefore a solution of the relaxed system of Theorem 1, which drops the bounds and the entries $<$, $>$, $*$. By Theorem 1 the test of that subscript answers "maybe". This holds for every subscript, so the loop of lines L9 and L10 never returns, and line L11 returns "maybe". $\square$

## Why "<" and ">" are not used

The test could try to use $\psi_l = {<}$ by writing $j_l = i_l + \delta_l$ with $\delta_l \ge 1$. The terms of level $l$ become $(a_l - b_l) i_l - b_l \delta_l$, and $\gcd(a_l - b_l, b_l) = \gcd(a_l, b_l)$, since a common divisor of two of $a_l$, $b_l$, $a_l - b_l$ divides the third. So the gcd does not change, and the constraint $\delta_l \ge 1$ is an inequality, which Lemma 1 cannot see. The same holds for $>$. This is why the code treats $<$, $>$ and $*$ alike.

## What the test does not decide

Theorem 1 is the only exactness the test has. With bounds, with the entries $<$ and $>$, or with several subscripts, "maybe" can be wrong:

- $A[2i]$ against $A[3j + 2]$ with $1 \le i, j \le 3$: $\gcd(2, 3) = 1$ divides $2$, but the solutions $(1 + 3t, 2t)$ all leave the box.
- $A[i]$ against $A[j]$ with $\psi = (<)$: $\gcd(1, 1) = 1$ divides $0$, but $i = j$ is forced.
- $A[i][i]$ against $A[j][j + 1]$: each subscript alone has solutions, the two together have none.

In each case the answer "maybe" is still allowed by Theorem 2, which is the only promise the test makes with bounds.

## Cost

Each call of `gcd` on numbers of absolute value at most $C$ takes $O(\log C)$ division steps, and the running gcd never exceeds the largest coefficient. A subscript makes at most $2k$ calls, so the test of $m$ subscripts takes $O(m k \log C)$ arithmetic operations and $O(1)$ extra space. `solve_linear` takes $O(n^2 + n \log C)$ operations for $n$ variables, because it scales the vector once per variable.
