---
title: The sign changes of the Routh array count the right half plane roots, in the regular case, with zero rows, and with one epsilon substitution when no root is on the axis
proves: [correctness, termination]
status: full
---

Let $p(s) = a_0 s^n + a_1 s^{n-1} + \dots + a_n$ be real with $a_0 \ne 0$ and $n \ge 1$. For a real polynomial $g$, $N(g)$ is the number of its roots in the open right half plane and $Z(g)$ the number on the imaginary axis, both counted with multiplicity. $[\,\cdot\,]$ is $1$ if the condition holds and $0$ otherwise. A polynomial is *even* if it has only even powers and *odd* if it has only odd powers; such a polynomial *has a parity*. For $g$ with a parity, $g(-s) = \pm g(s)$, so its roots are symmetric about the origin. The arithmetic is exact. The proof follows the continuity argument of Meinsma (1995).

## Rows as polynomials

Row $i$ of the array, with entries $r_{i,0}, r_{i,1}, \dots$, stands for the polynomial

$$R_i(s) = r_{i,0}\, s^{n-i} + r_{i,1}\, s^{n-i-2} + r_{i,2}\, s^{n-i-4} + \cdots ,$$

which has the parity of $n - i$. So $R_0$ and $R_1$ are the parts of $p$ with the parity of $n$ and of $n - 1$, and $p = R_0 + R_1$. Write $r_i = r_{i,0}$ and, when $r_i \ne 0$, $P_i = R_i + R_{i+1}$, a polynomial of degree $n - i$ whose two parts are $R_i$ and $R_{i+1}$ ($R_{n+1} = 0$).

**Lemma 0 (the cross product rule).** If $r_{i-1} \ne 0$ and $r_i \ne 0$, line L6 computes

$$R_{i+1} = R_{i-1} - \eta\, s\, R_i , \qquad \eta = r_{i-1} / r_i .$$

*Proof.* With $u = $ row $i - 1$ and $c = $ row $i$, the coefficient of $s^{n-i-1-2j}$ in $R_{i-1}$ is $u_{j+1}$, and in $s R_i$ it is $c_{j+1}$. The coefficient of $s^{n-i+1}$ is $u_0 - \eta c_0 = 0$. So $R_{i-1} - \eta s R_i = \sum_j (u_{j+1} - u_0 c_{j+1} / c_0)\, s^{n-i-1-2j}$, and $u_{j+1} - u_0 c_{j+1}/c_0 = (c_0 u_{j+1} - u_0 c_{j+1})/c_0$ is line L6. $\square$

## Two facts about roots

**Fact 1 (continuity of roots).** Let $g_t$ be real polynomials whose coefficients depend continuously on $t$ in an interval $J$, with constant degree $k$. If no $g_t$, $t \in J$, has a root on the imaginary axis, then $N(g_t)$ is constant on $J$. *Reason.* By Rouché's theorem, for $t$ near $t_0$ the roots of $g_t$ lie in small discs around the roots of $g_{t_0}$, each disc holding as many roots as the multiplicity of its center. Discs that do not meet the axis keep the count on each side, so $N(g_t)$ is locally constant, and $J$ is connected.

**Fact 2 (a root to infinity).** If moreover $J = [t_0, 1)$, $g_t \to g_1$ coefficientwise, the leading coefficient of $g_t$ tends to $0$, and $g_1$ has degree $k - 1$, then for $t$ close to $1$, $k - 1$ roots of $g_t$ lie in small discs around the roots of $g_1$ and the last root leaves every bounded set. *Reason.* Rouché's theorem on the discs around the roots of $g_1$ gives $k - 1$ roots in the discs; on a bounded set outside the discs $|g_t|$ is bounded away from $0$ for $t$ near $1$, because $g_t \to g_1$ uniformly there.

## Lemma 1: the imaginary axis

Let $F$ and $G$ be real polynomials of opposite parity. Then for real $\omega$, $F(i\omega) + G(i\omega) = 0$ if and only if $F(i\omega) = 0$ and $G(i\omega) = 0$.

*Proof.* An even real polynomial takes real values at $i\omega$, and an odd one takes purely imaginary values. So one of $F(i\omega)$, $G(i\omega)$ is the real part of the sum and the other is $i$ times its imaginary part. $\square$

Now let $F$ and $G$ have opposite parity, and let $D = \gcd(F, G)$. Since $F(-s) = \pm F(s)$ and $G(-s) = \pm G(s)$, $D(-s)$ is also a common divisor of the same degree, so $D(-s) = \pm D(s)$, and $D$ has a parity. Then $F/D$ and $G/D$ have parities, opposite to each other, and they are coprime. By Lemma 1, $F/D + G/D$ has no root on the axis. Hence:

**Corollary 1.** If $p = F + G$ with $F$, $G$ of opposite parity and $D = \gcd(F, G)$, then the roots of $p$ on the imaginary axis are exactly the roots of $D$ on the axis, with the same multiplicities. In particular $Z(p) = Z(D)$.

## Lemma 2: one step lowers the degree

Let $p = F + G$ have degree $m \ge 1$, where $F$ has the parity of $m$ and the leading coefficient $a_0 \ne 0$, and $G$ has the other parity and the coefficient $a_1 \ne 0$ at $s^{m-1}$. Let $\eta = a_0 / a_1$, $H = F - \eta s G$ and $q = G + H$. Then:

(a) $q$ has degree $m - 1$, its parts are $G$ (leading coefficient $a_1$) and $H$, and $\gcd(G, H) = \gcd(F, G)$;

(b) $Z(q) = Z(p)$, with the same roots on the axis;

(c) $N(p) = N(q) + [a_0 a_1 < 0]$.

*Proof.* (a) $s G$ has the parity of $m$ and the leading term $a_1 s^m$, so $H$ has the parity of $m$ and degree at most $m - 2$. A common divisor of $F$ and $G$ divides $H$, and a common divisor of $G$ and $H$ divides $F = H + \eta s G$.

(b) Corollary 1 for $p$ and for $q$, with the same $D$.

(c) Let $D = \gcd(F, G)$, $\tilde F = F/D$, $\tilde G = G/D$, and for $t \in [0, 1]$

$$p_t = F + G - t \eta s G = D \cdot \tilde p_t , \qquad \tilde p_t = (\tilde F - t \eta s \tilde G) + \tilde G .$$

Then $p_0 = p$ and $p_1 = q$. The polynomial $\tilde F - t\eta s \tilde G$ has the parity of $\tilde F$, and $\gcd(\tilde F - t\eta s\tilde G, \tilde G) = \gcd(\tilde F, \tilde G) = 1$. By Lemma 1, no $\tilde p_t$ has a root on the axis. The coefficient of $s^m$ in $p_t$ is $a_0 - t \eta a_1 = (1 - t) a_0$, which is nonzero for $t < 1$; the coefficient of $s^{m-1}$ is $a_1$ for every $t$, because $F$ and $s G$ contribute nothing to that power. So $\tilde p_t$ has constant degree $k = m - \deg D$ on $[0, 1)$, and $\tilde p_1 = q / D$ has degree $k - 1$.

By Fact 1, $N(\tilde p_t) = N(\tilde p_0)$ for $t \in [0, 1)$. By Fact 2, for $t$ near $1$, $k - 1$ roots of $\tilde p_t$ lie near the roots of $\tilde p_1$, which are off the axis, so they contribute $N(\tilde p_1)$; the last root $\rho(t)$ leaves every bounded set. The sum of all roots of $p_t$ is $-a_1 / ((1 - t) a_0)$. The roots of $D$ do not move and the other $k - 1$ roots of $\tilde p_t$ stay bounded, so $\rho(t) = -a_1 / ((1 - t) a_0) + O(1)$, whose real part tends to $+\infty$ if $a_0 a_1 < 0$ and to $-\infty$ if $a_0 a_1 > 0$. So $N(\tilde p_0) = N(\tilde p_1) + [a_0 a_1 < 0]$, and adding $N(D)$ on both sides gives (c). $\square$

By Lemma 0, when $r_i \ne 0$ and $r_{i+1} \ne 0$, Lemma 2 applied to $P_i$ (with $F = R_i$, $G = R_{i+1}$) gives $q = P_{i+1}$. So the array is the sequence $P_0 = p, P_1, P_2, \dots$ of Lemma 2.

## Theorem 1: the regular case

If no special case occurs, then $Z(p) = 0$ and $N(p) = V$, the number of sign changes in $r_0, \dots, r_n$.

*Proof.* All $r_i$ are nonzero. For $i = 0, \dots, n - 1$, Lemma 2 gives $N(P_i) = N(P_{i+1}) + [r_i r_{i+1} < 0]$ and $Z(P_i) = Z(P_{i+1})$. $P_n = r_n$ is a nonzero constant, with $N = Z = 0$. Adding up, $N(p) = \sum_i [r_i r_{i+1} < 0] = V$ and $Z(p) = 0$. $\blacksquare$

## Lemma 3: the derivative of an even or odd polynomial

Let $A$ be even or odd, of degree $d \ge 1$. Then $A + A'$ has degree $d$, its parts are $A$ and $A'$, $N(A + A') = N(A)$, and the roots of $A + A'$ on the axis are the multiple roots of $A$ on the axis, each with its multiplicity lowered by one.

*Proof.* $A'$ has the other parity and degree $d - 1$. Let $A_t = A + t A'$ for $t \in [0, 1]$; its degree is $d$ for every $t$. For $t > 0$, Lemma 1 says $A_t(i\omega) = 0$ if and only if $A(i\omega) = A'(i\omega) = 0$. Let $i\omega$ be a root of $A$ of multiplicity $\mu$ and write $A = (s - i\omega)^\mu h$ with $h(i\omega) \ne 0$. Then

$$A_t = (s - i\omega)^{\mu - 1} \bigl(t \mu h + (s - i\omega)(h + t h')\bigr) ,$$

and the bracket equals $t \mu h(i\omega) \ne 0$ at $s = i\omega$, so for $t > 0$ the multiplicity of $i\omega$ in $A_t$ is exactly $\mu - 1$. Let $E$ be the product of $(s - i\omega)^{\mu - 1}$ over the distinct roots $i\omega$ of $A$ on the axis. Conjugate roots have equal multiplicities, so $E$ is real. $E$ divides every $A_t$, and $B_t = A_t / E$ has no root on the axis for $t \in (0, 1]$, so by Fact 1 $N(B_t)$ is constant on $(0, 1]$.

As $t \to 0+$, $B_t \to B_0 = A / E$, which has the same degree, a simple root at each axis root $i\omega$ of $A$, and the roots of $A$ off the axis. Near a simple root $i\omega$ of $B_0$, the implicit function theorem gives a root $s(t) = i\omega + t\, s'(0) + O(t^2)$ of $B_t$ with $s'(0) = -\partial_t B_t / \partial_s B_0$ at $(0, i\omega)$. With $E = (s - i\omega)^{\mu-1} e$, $e(i\omega) \ne 0$, one finds $\partial_s B_0(i\omega) = h(i\omega)/e(i\omega)$ and $\partial_t B_t (i\omega) = (A'/E)(i\omega) = \mu h(i\omega)/e(i\omega)$. So $s'(0) = -\mu$, and $s(t)$ lies in the open left half plane for small $t > 0$. The roots of $B_0$ off the axis keep their side for small $t$. Hence $N(B_t) = N(B_0) = N(A)$ for small $t > 0$, and so for $t = 1$: $N(A + A') = N(E) + N(B_1) = 0 + N(A)$. $\square$

Since the roots of $A$ are symmetric about the origin, $A$ has as many roots in the left as in the right half plane, so $d = 2 N(A) + Z(A)$.

## Theorem 2: zero rows

Suppose zero rows occur and no zero first entry does. Let $A_1$ be the auxiliary polynomial of the first zero row. Then $N(p) = V$, the roots of $p$ on the imaginary axis are those of $A_1$ with multiplicity, and $p$ has $n - V - Z(A_1)$ roots in the open left half plane.

*Proof.* Every row, after lines L7 to L11, has a nonzero first entry: a regular row by assumption, and a replaced zero row because its first entry is $d$ times the nonzero first entry of the row above. So $c \ne 0$ in line L5 throughout.

Induction on the number $z$ of zero rows; $z = 0$ is Theorem 1. Let $z \ge 1$ and let row $k \ge 1$ be the first zero row, so $R_k = 0$ before the replacement and $P_{k-1} = R_{k-1} = A_1$, of degree $d = n - k + 1$. Lemma 2 for $i = 0, \dots, k - 2$ gives

$$N(p) = V(r_0, \dots, r_{k-1}) + N(A_1)$$

and the same roots on the axis for $p$ and $A_1$. (For $k = 1$, $p = A_1$.) After the replacement, row $k - 1$ holds the coefficients of $A_1$ and row $k$ those of $A_1'$, and every later row depends only on these two rows. So rows $k - 1, \dots, n$ are the array of $A_1 + A_1'$, whose parts are $A_1$ and $A_1'$; it has $z - 1$ zero rows and no zero first entry. By induction and Lemma 3, $V(r_{k-1}, \dots, r_n) = N(A_1 + A_1') = N(A_1)$. Adding the two counts, $V = N(p)$. The left half plane count is $n - N(p) - Z(p)$. $\blacksquare$

## Theorem 3: one zero first entry

Suppose exactly one $\varepsilon$ substitution occurs, in row $k$, no zero row occurs, and $p$ has no root on the imaginary axis. Then $N(p) = V$, with the signs taken as $\varepsilon \to 0+$.

*Proof.* Rows $0, \dots, k - 1$ have nonzero first entries, so Lemma 2 for $i = 0, \dots, k - 2$ gives $N(p) = V(r_0, \dots, r_{k-1}) + N(P_{k-1})$ and $Z(P_{k-1}) = Z(p) = 0$. Here $P_{k-1} = R_{k-1} + R_k$, where $R_k \ne 0$ has a zero coefficient at $s^{n-k}$. For real $\varepsilon$ let

$$P^\varepsilon = P_{k-1} + \varepsilon\, s^{n-k} ,$$

whose parts are $R_{k-1}$ and $R_k + \varepsilon s^{n-k}$. The rows $k - 1, \dots, n$ that the algorithm computes, with $\varepsilon$ as a symbol, are rational functions of $\varepsilon$, and every first entry $r_i(\varepsilon)$, $i \ge k$, is a nonzero rational function, since no further special case occurs. Only finitely many $\varepsilon$ make a numerator or a denominator of some entry vanish. For every other real $\varepsilon$, evaluating the entries at $\varepsilon$ gives the numerical array of $P^\varepsilon$, with the same operations and nonzero divisors, and that array is regular. A nonzero rational function has a constant sign on some interval $(0, \varepsilon_0)$, namely its sign as $\varepsilon \to 0+$. So for small $\varepsilon > 0$, Theorem 1 gives $N(P^\varepsilon) = V(r_{k-1}, r_k(\varepsilon), \dots, r_n(\varepsilon))$, which is the count of line L12 on rows $k - 1, \dots, n$.

As $\varepsilon \to 0$, $P^\varepsilon \to P_{k-1}$ with the constant degree $n - k + 1$ and leading coefficient $r_{k-1}$, and $P_{k-1}$ has no root on the axis. By Fact 1 (on a small interval around $0$, where no $P^\varepsilon$ has a root on the axis, by continuity), $N(P^\varepsilon) = N(P_{k-1})$ for small $\varepsilon$. Adding, $N(p) = V$. $\blacksquare$

**What is not proved.** If a second substitution occurs, the implementation uses the same $\varepsilon$, so the polynomial and the perturbation both depend on $\varepsilon$, and the argument above does not apply. The tests found no wrong count in that case for polynomials without roots near the axis. Combinations of $\varepsilon$ and zero rows are also not covered here.

**The hypothesis on the axis is needed.** $p(s) = s^5 + 3 s^3 + s^2 + 2 s + 1 = (s^2 + 1)(s^3 + 2 s + 1)$ has $a_1 = 0$, so the substitution happens in row 1. The signs as $\varepsilon \to 0+$ are $+, +, -, +, -, +$, so $V = 4$, but $N(p) = 2$: the roots are $\pm i$, $-0.4534$ and $0.2267 \pm 1.46771 i$. In the proof, $P^\varepsilon = p + \varepsilon s^4$ moves both axis roots into the right half plane.

## Theorem 4: the Hurwitz decision

`is_hurwitz(p)`, which is true exactly when no special case occurs and $V = 0$, is true if and only if every root of $p$ has a negative real part.

*Proof.* If no special case occurs and $V = 0$, Theorem 1 gives $N(p) = Z(p) = 0$. Conversely, let $p$ be Hurwitz. Then $p / a_0$ is a product of factors $s + \rho$ with $\rho > 0$ and $s^2 + 2\sigma s + \sigma^2 + \tau^2$ with $\sigma > 0$, so all coefficients of $p$ are nonzero and have the sign of $a_0$; in particular $a_0 a_1 > 0$. Lemma 2 applies to $P_0 = p$ and gives $N(P_1) = N(p) - 0 = 0$ and $Z(P_1) = Z(p) = 0$; $P_1$ has degree $n - 1$, so it is Hurwitz. By induction every $P_i$ is Hurwitz of degree $n - i$, so its first two coefficients $r_i$ and $r_{i+1}$ are nonzero and of the same sign. Hence no row is zero, no first entry is zero, and $V = 0$. $\blacksquare$

## Theorem 5: the Hurwitz determinants

Let $H$ be the $n \times n$ Hurwitz matrix of $p$, $H_{ij} = a_{2j - i}$ (with $a_k = 0$ for $k < 0$ or $k > n$), and $\Delta_k$ its leading principal minor of order $k$. In the regular case, $\Delta_k = r_1 r_2 \cdots r_k$ for $k = 1, \dots, n$.

*Proof.* Induction on $n$. Row $2l - 1$ of $H$ is $(0, \dots, 0, a_1, a_3, \dots)$ and row $2l$ is $(0, \dots, 0, a_0, a_2, \dots)$, both starting in column $l$. Subtract $\eta = a_0 / a_1$ times row $2l - 1$ from row $2l$, for each $l$. This adds multiples of earlier rows to later rows, so it does not change any leading principal minor. Row $2l$ becomes $(0, \dots, 0, 0, a_2 - \eta a_3, a_4 - \eta a_5, \dots)$, which is the row of $R_2$ starting in column $l + 1$. Now column 1 is $(a_1, 0, \dots, 0)^T$, and the matrix left after deleting row 1 and column 1 is the Hurwitz matrix of $P_1 = R_1 + R_2$, of degree $n - 1$, whose coefficients are $a_1, r_{2,0}, a_3, r_{2,1}, \dots$. So $\Delta_k(p) = a_1\, \Delta_{k-1}(P_1)$, with $\Delta_0 = 1$. The array of $P_1$ is rows $1, \dots, n$ of the array of $p$, so by induction $\Delta_{k-1}(P_1) = r_2 \cdots r_k$, and $a_1 = r_1$. $\blacksquare$

With $a_0 > 0$, a positive first column is thus the same as $\Delta_1, \dots, \Delta_n > 0$, which is Hurwitz's form of the criterion.

## Termination and cost

The loop in line L3 runs $n$ times. Row $i$ has $\lfloor (n - i)/2 \rfloor + 1$ entries, each computed once by line L6 with two multiplications, a subtraction and a division, and lines L7 to L11 cost $O(n)$ per row. So the algorithm stops after $O(n^2)$ arithmetic operations on the entries, which are numbers in the regular case and with zero rows, and rational functions of $\varepsilon$ after a substitution.
