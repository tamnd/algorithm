---
title: Constrain and restrict agree with f on the care set, constrain is f composed with the closest-point map, and restrict keeps the support of f
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order, and the store holds reduced ordered BDDs. A node $u$ has a level $\mathrm{lev}(u)$, the index of the variable that it tests, and a sink has level $n + 1$. We identify a node with its function. For a variable $x_v$ with $v \le \mathrm{lev}(u)$, the cofactors $u_0, u_1$ are the children of $u$ if $\mathrm{lev}(u) = v$, and both equal $u$ if $\mathrm{lev}(u) > v$; in both cases $u_b = u|_{x_v = b}$, and $u_b$ does not depend on $x_1, \ldots, x_v$. MK$(v, l, h)$ returns the node of $\neg x_v \, l \vee x_v \, h$. We write $C(f, c)$ and $R(f, c)$ for the results of CONSTRAIN and RESTRICT. The computed tables only return results that an earlier call with the same arguments computed, so we can reason about the recursion without them.

**Lemma 0 (termination and preconditions).** For $c \ne 0$, both procedures terminate, and every recursive call has a nonzero second argument.

*Proof.* Let $\mu(f, c) = \mathrm{lev}(f) + \mathrm{lev}(c)$. At lines L4 to L6 the new arguments are cofactors by $v = \min(\mathrm{lev}(f), \mathrm{lev}(c))$, so one level grows and the other does not shrink, and $\mu$ grows. At line L8, $c_0 \vee c_1$ does not depend on $x_1, \ldots, x_{\mathrm{lev}(c)}$, so its level is larger than $\mathrm{lev}(c)$, and $\mu$ grows. Since $\mu \le 2n + 2$, the recursion ends. At line L4, $c_0 = 0$ and $c \ne 0$ give $c_1 \ne 0$; line L5 is symmetric; at line L6 both are nonzero; and at line L8, $c_0 \vee c_1 \ne 0$ because $c \ne 0$. $\square$

**Theorem 1 (agreement).** For $c \ne 0$ and every $x$ with $c(x) = 1$, $C(f, c)(x) = f(x)$ and $R(f, c)(x) = f(x)$.

*Proof.* By induction on $2n + 2 - \mu(f, c)$, using Lemma 0. Fix $x$ with $c(x) = 1$.

- *Line L1 or L7, first part.* The result is $f$.
- *Line L2 or L7, second part.* $f = c$, so $f(x) = c(x) = 1$, which is the result.
- *Line L4.* Here $c_0 = 0$, so $c(x) = 1$ forces $x_v = 1$. Then $c_1(x) = c(x) = 1$, and by induction the result $g$ satisfies $g(x) = f_1(x) = f(x)$, since $x_v = 1$.
- *Line L5.* The same with the roles of 0 and 1 exchanged.
- *Line L6.* The result is MK$(v, g_0, g_1)$ with $g_b = C(f_b, c_b)$ (or $R$). If $x_v = b$, its value at $x$ is $g_b(x)$, and $c_b(x) = c(x) = 1$, so by induction $g_b(x) = f_b(x) = f(x)$.
- *Line L8 (restrict only).* Here $v = \mathrm{lev}(c) < \mathrm{lev}(f)$, so $f$ does not depend on $x_v$. Let $c' = c_0 \vee c_1$. Then $c'(x) = c(x \text{ with } x_v = 0) \vee c(x \text{ with } x_v = 1) \ge c(x) = 1$, so by induction $R(f, c')(x) = f(x)$. $\square$

**The closest-point map.** For $c \ne 0$ and a point $x$, define $y = \pi_c(x)$ from the top: for $i = 1, \ldots, n$, let $y_i = x_i$ if some point $z$ with $c(z) = 1$ has $z_1 = y_1, \ldots, z_{i-1} = y_{i-1}$ and $z_i = x_i$, and let $y_i = 1 - x_i$ otherwise. By induction on $i$, some care point extends $y_1, \ldots, y_i$, so $c(y) = 1$.

**Lemma 2 ($\pi_c$ is the closest care point).** With $d(x, y) = \sum_i |x_i - y_i| \, 2^{n-i}$, $\pi_c(x)$ is the unique care point that minimizes $d(x, \cdot)$.

*Proof.* The value $d(x, y)$ is the binary number with the digits $|x_1 - y_1|, \ldots, |x_n - y_n|$, so comparing $d(x, y)$ and $d(x, y')$ is a lexicographic comparison of the digit strings, and distinct $y$ give distinct strings. Let $y'$ be a care point with $y' \ne \pi_c(x)$, and let $i$ be the first index where they differ. Both extend $y_1, \ldots, y_{i-1}$. If $y_i = x_i$, then $y'_i \ne x_i$, so the digit of $y'$ is 1 and the digit of $\pi_c(x)$ is 0. If $y_i \ne x_i$, then no care point extends $y_1, \ldots, y_{i-1}, x_i$, so $y'_i \ne x_i$ too, which contradicts $y'_i \ne y_i$. So $d(x, \pi_c(x)) < d(x, y')$. $\square$

**Theorem 2 (constrain is a composition).** For $c \ne 0$ and all $x$, $C(f, c)(x) = f(\pi_c(x))$.

*Proof.* We show a slightly more general claim, by the same induction as in Theorem 1. Call a pair $(f, c)$ *below* $k$ if neither $f$ nor $c$ depends on $x_1, \ldots, x_k$. For such a pair, $\pi_c(x)$ copies $x_1, \ldots, x_k$, because the condition in the definition does not depend on those coordinates. We claim that $C(f, c)(x) = f(\pi_c(x))$ for all $x$.

- *Line L1.* If $c = 1$, every point is a care point, so $\pi_c(x) = x$, and the result $f$ is right. If $f$ is a sink, both sides are that constant.
- *Line L2.* $f = c$, and $c(\pi_c(x)) = 1$, so $f(\pi_c(x)) = 1$.
- *Lines L4 to L6.* Let $v$ be the top variable, so $(f, c)$ is below $v - 1$. Since $f$ and $c$ do not depend on $x_1, \ldots, x_{v-1}$, $\pi_c$ copies these coordinates. At step $v$, $\pi_c$ keeps $x_v$ if $c_{x_v} \ne 0$, and flips it otherwise. For the steps after $v$, the condition only involves care points of $c$ with the chosen $y_v$, that is, points of $c_{y_v}$, so the rest of $\pi_c(x)$ equals the rest of $\pi_{c_{y_v}}(x)$. Hence $f(\pi_c(x)) = f_{y_v}(\pi_{c_{y_v}}(x))$, since $f_{y_v}$ is $f$ with $x_v = y_v$ and does not read $x_v$.
  - At line L4, $c_0 = 0$, so $y_v = 1$ for every $x$, and the result $C(f_1, c_1)(x) = f_1(\pi_{c_1}(x))$ by induction. This equals $f(\pi_c(x))$.
  - Line L5 is symmetric, with $y_v = 0$.
  - At line L6, both cofactors are nonzero, so $y_v = x_v$, and the value of MK$(v, C(f_0, c_0), C(f_1, c_1))$ at $x$ is $C(f_{x_v}, c_{x_v})(x) = f_{x_v}(\pi_{c_{x_v}}(x)) = f(\pi_c(x))$ by induction. $\square$

Theorem 2 gives Theorem 1 again for constrain, since $\pi_c(x) = x$ when $c(x) = 1$. It also gives the two algebraic properties of the page: for any operation $\circ$, $(f \circ g) \downarrow c = (f \downarrow c) \circ (g \downarrow c)$, since both sides are $(f \circ g) \circ \pi_c$ by canonicity; and the range of $(f_1 \downarrow c, \ldots, f_m \downarrow c)$ is the image of the care set under $(f_1, \ldots, f_m)$, since $\pi_c$ maps all points onto the care set and is the identity on it.

**Theorem 3 (restrict keeps the support).** Every variable that the BDD of $R(f, c)$ tests is also tested by the BDD of $f$.

*Proof.* By the same induction. The results of lines L7 are $f$ or the sink 1. Line L8 returns $R(f, c')$ with the same $f$. Under line L9, $v$ is the top variable of $f$, and the results are $R(f_b, c_b)$ or MK$(v, R(f_0, c_0), R(f_1, c_1))$. The children $f_0$ and $f_1$ of $f$ test only variables that $f$ tests, and MK only adds a node of $x_v$, which $f$ tests. In a reduced BDD the tested variables are exactly the variables that the function depends on, so the claim holds for the functions as well. $\blacksquare$

**Remark (cost).** For constrain, every call has arguments $(f', c')$ with $f'$ reachable from $f$ and $c'$ reachable from $c$, by line L3. With the computed table each such pair does real work once, so there are $O(|f| \cdot |c|)$ calls, and the result has at most $|f| \cdot |c|$ nodes. No bound of this kind holds for restrict, whose line L8 makes new care sets.
