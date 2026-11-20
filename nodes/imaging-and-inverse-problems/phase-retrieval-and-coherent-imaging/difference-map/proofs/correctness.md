---
title: Fixed points of the difference map give solutions, and HIO is a special case
proves: [correctness]
status: full
---

The setting is that of the algorithm. Images have $N$ pixels. $M$ is the set of images whose DFT has magnitude $A$, and $P_M$ (the magnitude step) maps each image to a nearest point of $M$. $C$ is the object constraint set (zero off the support $S$, and, with nonnegativity, real and nonnegative on $S$), and $P_S$ maps each image to its nearest point of $C$. A *solution* is an image in $C \cap M$. The parameters are real numbers $\beta \ne 0$, $\gamma_S$ and $\gamma_M$. Arithmetic is exact.

With

$$f_S(x) = (1 + \gamma_S) P_S(x) - \gamma_S x, \qquad f_M(x) = (1 + \gamma_M) P_M(x) - \gamma_M x,$$

the difference map is $D(x) = x + \beta\,[P_S(f_M(x)) - P_M(f_S(x))]$, as in lines L3 to L5, and the read-out of line L6 is $P_M(f_S(x))$.

Two facts about the projections are used. (a) $P_S(x) \in C$ and $P_M(x) \in M$ for every $x$, by construction. (b) $P_S(c) = c$ for $c \in C$ and $P_M(m) = m$ for $m \in M$: a point of a set is its own nearest point (for $P_M$, line L4 maps $G_u$ to $A_u G_u / |G_u| = G_u$ when $|G_u| = A_u > 0$, and $0$ to $A_u = 0$).

**Theorem 1 (fixed points give solutions).** If $D(x) = x$, then $P_S(f_M(x)) = P_M(f_S(x))$, and this image is a solution.

*Proof.* $D(x) = x$ means $\beta\,[P_S(f_M(x)) - P_M(f_S(x))] = 0$, and $\beta \ne 0$, so the two images are equal; call the image $z$. By (a), $z = P_S(f_M(x)) \in C$ and $z = P_M(f_S(x)) \in M$. So $z \in C \cap M$. $\square$

This is why the read-out is not $x$ itself: a fixed point $x$ need not be in either set, but the two projected estimates agree there and give a solution. Away from a fixed point, $\|D(x) - x\| / |\beta| = \|P_S(f_M(x)) - P_M(f_S(x))\|$ measures how far the two estimates are apart, which is the gap the implementation reports.

**Theorem 2 (solutions are fixed points).** If $z \in C \cap M$, then $D(z) = z$ and the read-out at $z$ is $z$, for all values of the parameters.

*Proof.* By (b), $P_S(z) = z$ and $P_M(z) = z$. So $f_S(z) = (1 + \gamma_S) z - \gamma_S z = z$ and in the same way $f_M(z) = z$. Then $P_S(f_M(z)) = z$ and $P_M(f_S(z)) = z$, so $D(z) = z + \beta(z - z) = z$, and the read-out is $z$. $\square$

**Theorem 3 (HIO is a special case).** Take a support constraint without nonnegativity, so that $P_S$ (keep the values on $S$, set zero off $S$) is linear. Take $\gamma_S = -1$ and $\gamma_M = 1/\beta$. Then for every $x$, with $p = P_M(x)$,

$$D(x)(r) = p(r) \text{ for } r \in S, \qquad D(x)(r) = x(r) - \beta\,p(r) \text{ for } r \notin S,$$

which is the hybrid input-output step with feedback $\beta$. With $\beta = 1$ (so $\gamma_S = -1$ and $\gamma_M = 1$, Elser's choice $\gamma_S = -1/\beta$, $\gamma_M = 1/\beta$ at $\beta = 1$), it is the Douglas-Rachford step $x + P_S(2p - x) - p$.

*Proof.* With $\gamma_S = -1$, $f_S(x) = 0 \cdot P_S(x) + x = x$, so $P_M(f_S(x)) = p$. With $\gamma_M = 1/\beta$, $f_M(x) = (1 + 1/\beta)\,p - x/\beta$. $P_S$ is linear, so

$$D(x) = x + \beta\Bigl[(1 + \tfrac{1}{\beta}) P_S(p) - \tfrac{1}{\beta} P_S(x) - p\Bigr] = x + (\beta + 1) P_S(p) - P_S(x) - \beta p .$$

On $S$, $P_S$ is the identity, and this is $x + (\beta + 1) p - x - \beta p = p$. Off $S$, $P_S$ gives zero, and this is $x - \beta p$. For $\beta = 1$ the formula is $x + 2P_S(p) - P_S(x) - p = x + P_S(2p - x) - p$ by linearity. $\square$

**What is not claimed.** $M$ is not convex, and no theorem says that the difference map reaches a fixed point. The gap is not monotone in general; the test file does not check a monotone quantity. Elser's choice $\gamma_S = -1/\beta$, $\gamma_M = 1/\beta$ comes from a local analysis near a fixed point, and the value of $\beta$ is tuned. With nonnegativity, $P_S$ is not linear and Theorem 3 does not hold as stated.
