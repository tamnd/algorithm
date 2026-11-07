---
title: Correctness of Ferrari's method
proves: [correctness, termination]
status: full
---

We work in exact complex arithmetic, where $\sqrt{\cdot}$ returns some square root and CARDANO returns the three roots of a cubic with multiplicity (proved on the page [Cardano's formula](/cardano-formula/)).

**Lemma 1 (the shift).** Let $s = b/(4a)$, $C = c/a$, $D = d/a$, $E = e/a$, and $p, q, r$ as in line L2. Then $\frac{1}{a}(ax^4 + bx^3 + cx^2 + dx + e) = y^4 + py^2 + qy + r$ for $y = x + s$.

*Proof.* Put $x = y - s$ and $4s = b/a$. Then $(y - s)^4 = y^4 - 4sy^3 + 6s^2y^2 - 4s^3y + s^4$, $4s(y - s)^3 = 4sy^3 - 12s^2y^2 + 12s^3y - 4s^4$, $C(y - s)^2 = Cy^2 - 2Csy + Cs^2$ and $D(y - s) = Dy - Ds$. Adding these and $E$, the $y^3$ terms cancel, the $y^2$ coefficient is $C - 6s^2 = p$, the $y$ coefficient is $D - 2Cs + 8s^3 = q$ and the constant is $E - Ds + Cs^2 - 3s^4 = r$. $\square$

So $x$ is a root of the quartic with multiplicity $k$ if and only if $y = x + s$ is a root of the depressed quartic $Q(y) = y^4 + py^2 + qy + r$ with multiplicity $k$, and line L9 maps the roots back.

**Lemma 2 (the splitting).** Let $m \ne 0$ satisfy $R(m) = 8m^3 + 8pm^2 + (2p^2 - 8r)m - q^2 = 0$, let $\sigma^2 = 2m$, and let $A = \frac{p}{2} + m + \frac{q}{2\sigma}$, $B = \frac{p}{2} + m - \frac{q}{2\sigma}$. Then $Q(y) = (y^2 - \sigma y + A)(y^2 + \sigma y + B)$.

*Proof.* $\sigma \ne 0$ since $m \ne 0$. Expanding,

$$(y^2 - \sigma y + A)(y^2 + \sigma y + B) = y^4 + (A + B - \sigma^2)y^2 + \sigma(A - B)y + AB.$$

Here $A + B - \sigma^2 = p + 2m - 2m = p$ and $\sigma(A - B) = \sigma \cdot q/\sigma = q$. Also $AB = (\frac{p}{2} + m)^2 - \frac{q^2}{4\sigma^2} = (\frac{p}{2} + m)^2 - \frac{q^2}{8m}$. This equals $r$ if and only if $8m(m^2 + pm + \frac{p^2}{4}) - 8mr - q^2 = 0$, which is $R(m) = 0$. $\square$

**Lemma 3 (the zero case).** The roots of $R$ are all zero if and only if $p = q = r = 0$.

*Proof.* The roots of $R$ are all zero if and only if $R(m) = 8m^3$, that is $8p = 0$, $2p^2 - 8r = 0$ and $q^2 = 0$. $\square$

**Lemma 4 (QUAD).** For any complex $\beta, \gamma$, lines L10 and L11 return the two roots, with multiplicity, of $y^2 + \beta y + \gamma$.

*Proof.* The roots are $t_\pm = -(\beta \pm w)/2$ with $w^2 = \beta^2 - 4\gamma$, and $t_+ t_- = (\beta^2 - w^2)/4 = \gamma$. Line L10 takes $t \in \{t_+, t_-\}$ of larger modulus. If $t = 0$ then $t_+ = t_- = 0$, so the roots are $0, 0$, which L11 returns. Otherwise the other root is $\gamma/t$. $\square$

**Theorem.** For $a \ne 0$, FERRARI returns the four roots of $ax^4 + bx^3 + cx^2 + dx + e$, with multiplicity.

*Proof.* If line L5 returns, the chosen $m$ of largest modulus is $0$, so all roots of $R$ are $0$, and $p = q = r = 0$ by Lemma 3. Then $Q(y) = y^4$, and by Lemma 1 the quartic is $a(x + s)^4$ with the root $-s$ of multiplicity 4. Otherwise $m \ne 0$ is a root of $R$, by the correctness of CARDANO. By Lemma 2, $Q(y) = (y^2 - \sigma y + A)(y^2 + \sigma y + B)$, so the roots of $Q$ with multiplicity are the roots of the two factors together, which line L8 computes by Lemma 4. Line L9 maps them to the roots of the quartic by Lemma 1. $\square$

**Termination.** There is no loop. FERRARI runs lines L1 to L9 once, with one call of CARDANO (which has no loop either) and two calls of QUAD. So it ends after a fixed number of operations.

**Why the root of largest modulus.** Not needed for correctness, by Lemma 2 any nonzero root works. If the roots of $Q$ are $y_1, \ldots, y_4$, Lemma 2 shows $\sigma = y_1 + y_2$ for the pair that the first factor holds, so the three roots of $R$ are $(y_1 + y_2)^2/2$, $(y_1 + y_3)^2/2$ and $(y_1 + y_4)^2/2$ (recall $y_1 + \cdots + y_4 = 0$). Their product is $q^2/8$. The largest of them keeps $|\sigma|$ as large as possible, so the division by $\sigma$ at L7 does not magnify the rounding errors in $q$ and $m$. The pitfall on the page shows the error when a small root is taken. $\blacksquare$
