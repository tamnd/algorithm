---
tag: P66TAN
kind: theorem
slug: feedback-linearizability-conditions
name: Conditions for feedback linearizability
aliases:
- Jakubczyk-Respondek conditions
- Hunt-Su-Meyer conditions
area: control/nonlinear-control
level: advanced
summary: "A single-input system is feedback linearizable near x0 if and only if g, ad_f g, ..., ad_f^(n-1) g are independent at x0 and the span of the first n - 1 of them is involutive."
prereqs: [feedback-linearization, lie-bracket, relative-degree]
see_also: [feedback-linearization, lie-bracket, relative-degree, input-output-linearization, differential-flatness, kalman-rank-condition, controllable-canonical-form, lie-algebra-rank-condition]
sources:
  - paper: "B. Jakubczyk and W. Respondek, On linearization of control systems, Bulletin de l'Académie Polonaise des Sciences, Série des Sciences Mathématiques 28, 517-522, 1980"
    title: On linearization of control systems
    locator: the necessary and sufficient conditions for linearization by state feedback and change of coordinates
  - paper: doi:10.1109/TAC.1983.1103137
    title: "L. R. Hunt, R. Su and G. Meyer, Global transformations of nonlinear systems, IEEE Transactions on Automatic Control 28(1), 24-31, 1983"
    locator: the same conditions found independently, and conditions for a transformation on a large region
  - book: isbn:9783540199168
    title: Alberto Isidori, Nonlinear Control Systems, third edition, Springer, 1995
    locator: Chapter 4 for the single-input case and Chapter 5 for several inputs; Chapter 1 for the theorem of Frobenius
  - book: isbn:9780130673893
    title: Hassan K. Khalil, Nonlinear Systems, third edition, Prentice Hall, 2002
    locator: Section 13.3, Full-State Linearization
  - paper: doi:10.1016/S1474-6670(17)66062-2
    title: "R. W. Brockett, Feedback invariants for nonlinear systems, Proceedings of the 7th IFAC World Congress, Helsinki, 1115-1120, 1978"
    locator: the first linearization by feedback, for one input and a constant gain on the new input
---

This theorem says when a nonlinear system can be made exactly linear by a change of coordinates and a state feedback, the operation of [feedback linearization](/feedback-linearization/). For one input the answer is a test with [Lie brackets](/lie-bracket/) of the drift $f$ and the input field $g$. The brackets $g, \mathrm{ad}_f g, \dots, \mathrm{ad}_f^{n-1} g$ must be linearly independent, which is the nonlinear form of the controllability matrix of the [Kalman rank condition](/kalman-rank-condition/). And the first $n - 1$ of them must span an involutive distribution, a condition that has no linear counterpart, because for linear systems it always holds. The test also says that the system is linearizable if and only if some output has [relative degree](/relative-degree/) $n$, and the proof constructs such an output by the theorem of Frobenius. Jakubczyk and Respondek (1980) and Hunt, Su and Meyer (1983) found the conditions independently.

## Statement

**Setting.** The system is $\dot x = f(x) + g(x) u$, with $x$ in an open set $U \subseteq \mathbb{R}^n$, one input $u$, and smooth ($C^\infty$) fields $f$ and $g$. Solutions exist and are unique by the [Picard-Lindelöf theorem](/picard-lindelof-theorem/). The bracket is $[f, g] = \frac{\partial g}{\partial x} f - \frac{\partial f}{\partial x} g$, and $\mathrm{ad}_f^0 g = g$, $\mathrm{ad}_f^{k} g = [f, \mathrm{ad}_f^{k-1} g]$. A distribution $D$ is involutive if the bracket of any two fields with values in $D$ has values in $D$.

**Definition.** The system is **feedback linearizable near $x_0$** if there are an open neighborhood $V$ of $x_0$, a diffeomorphism $z = T(x)$ from $V$ onto an open set, and smooth functions $\alpha$, $\beta$ on $V$ with $\beta(x) \neq 0$, such that in the coordinates $z$ the system with $u = \alpha(x) + \beta(x) v$ is $\dot z = A z + B v$ with $(A, B)$ controllable.

**Theorem.** The following are equivalent.

1. The system is feedback linearizable near $x_0$.
2. There is a smooth function $h$ near $x_0$ such that $\dot x = f + g u$, $y = h(x)$ has relative degree $n$ at $x_0$.
3. (i) The vectors $g(x_0), \mathrm{ad}_f g(x_0), \dots, \mathrm{ad}_f^{n-1} g(x_0)$ are linearly independent, and (ii) the distribution $D = \mathrm{span}\{g, \mathrm{ad}_f g, \dots, \mathrm{ad}_f^{n-2} g\}$ is involutive near $x_0$.

**Several inputs (stated without proof).** For $\dot x = f(x) + \sum_{i=1}^m g_i(x) u_i$, let $G_k = \mathrm{span}\{\mathrm{ad}_f^j g_i : 0 \le j \le k, 1 \le i \le m\}$. The system is feedback linearizable near $x_0$ if and only if each $G_k$ has constant dimension near $x_0$ for $k = 0, \dots, n - 1$, $G_{n-1}$ has dimension $n$, and each $G_k$ is involutive for $k = 0, \dots, n - 2$ (Isidori, Chapter 5; Jakubczyk and Respondek 1980).

## In plain words

Feedback can cancel any nonlinear term that sits where the input acts. The question is whether the coordinates can be changed so that every nonlinear term sits there. Two things are needed. First, the input must be able to push the state in every direction, using the input alone and the directions that come from combining the input with the free motion. Second, the directions that come before the last one must fit together as the slices of a family of surfaces, with no twist between them. When both hold, a function exists that is constant on those surfaces, and taking that function as the output gives a chain of integrators. When the second fails, no choice of coordinates or feedback removes all the nonlinear terms.

## Proof

The proof uses three facts. (F1) $L_{[X,Y]} \varphi = L_X L_Y \varphi - L_Y L_X \varphi$ for fields $X$, $Y$ and a function $\varphi$ (see the [Lie bracket](/lie-bracket/) page). (F2) The relative degree does not change under a change of coordinates or a feedback $u = \alpha + \beta v$ with $\beta \neq 0$, and if $r$ is the relative degree at $x_0$, then for $i + j \le r - 1$ near $x_0$, $L_{\mathrm{ad}_f^j g} L_f^i h$ is $0$ when $i + j \le r - 2$ and $(-1)^j L_g L_f^{r-1} h$ when $i + j = r - 1$ (see [relative degree](/relative-degree/); the induction is written out in the proof of [input-output linearization](/input-output-linearization/)). (F3) The theorem of Frobenius: a distribution of constant dimension $n - 1$ near $x_0$ that is involutive is, near $x_0$, the kernel of $dh$ for a smooth $h$ with $dh(x_0) \neq 0$.

*1 implies 2.* In the coordinates $z$, the linear system $\dot z = A z + B v$ is controllable, so $\tilde h(z) = w^T z$, with $w^T$ the last row of the inverse of $[B, AB, \dots, A^{n-1} B]$, has $w^T A^k B = 0$ for $k < n - 1$ and $w^T A^{n-1} B = 1$, so relative degree $n$. By (F2), $h = w^T T(x)$ has relative degree $n$ for the original system.

*2 implies 1.* Take $T(x) = (h, L_f h, \dots, L_f^{n-1} h)$. By (F2) with $r = n$, the $n \times n$ matrix with entries $dL_f^i h(x) \cdot \mathrm{ad}_f^j g(x)$ is zero above the anti-diagonal and has the nonzero entries $\pm L_g L_f^{n-1} h(x)$ on it near $x_0$. So the rows $dL_f^i h(x_0)$ are independent, and $T$ is a local diffeomorphism by the inverse function theorem. In the coordinates $z = T(x)$, $\dot z_i = z_{i+1}$ for $i < n$ and $\dot z_n = L_f^n h + L_g L_f^{n-1} h\, u$. The feedback $\alpha = -L_f^n h / L_g L_f^{n-1} h$, $\beta = 1 / L_g L_f^{n-1} h$ gives a chain of $n$ integrators, which is controllable.

*2 implies 3.* The same matrix is the product of the matrix with rows $dL_f^i h(x)$ and the matrix with columns $\mathrm{ad}_f^j g(x)$. It is nonsingular, so the columns are independent, which is (i), and by continuity they stay independent near $x_0$. By (F2) with $i = 0$, $dh \cdot \mathrm{ad}_f^j g = 0$ near $x_0$ for $j \le n - 2$. So $D \subseteq \ker dh$. Both have dimension $n - 1$ near $x_0$, since $dh \neq 0$, so $D = \ker dh$. For fields $X$, $Y$ in $D$, (F1) gives $L_{[X,Y]} h = L_X (L_Y h) - L_Y (L_X h) = 0$, so $[X, Y]$ is in $\ker dh = D$. So $D$ is involutive, which is (ii).

*3 implies 2.* By (i) and continuity, $D$ has constant dimension $n - 1$ near $x_0$. By (ii) and (F3), $D = \ker dh$ near $x_0$ for a smooth $h$ with $dh(x_0) \neq 0$. So $L_{\mathrm{ad}_f^j g} h = 0$ near $x_0$ for $j \le n - 2$. We show by induction on $i$ that $L_{\mathrm{ad}_f^j g} L_f^i h = 0$ near $x_0$ whenever $i + j \le n - 2$. The case $i = 0$ is the line above. By (F1) with $X = \mathrm{ad}_f^j g$,

$$L_{\mathrm{ad}_f^j g} L_f^{i+1} h = L_f \left( L_{\mathrm{ad}_f^j g} L_f^{i} h \right) - L_{\mathrm{ad}_f^{j+1} g} L_f^{i} h .$$

If $(i + 1) + j \le n - 2$, both terms on the right are zero by the induction hypothesis. With $j = 0$ this gives $L_g L_f^k h = 0$ near $x_0$ for $k \le n - 2$. The same formula with $i + 1 + j = n - 1$ has a zero first term, so $L_{\mathrm{ad}_f^j g} L_f^{i+1} h = -L_{\mathrm{ad}_f^{j+1} g} L_f^{i} h$, and repeating it gives $L_g L_f^{n-1} h = (-1)^{n-1} L_{\mathrm{ad}_f^{n-1} g} h$. At $x_0$ the covector $dh(x_0)$ is not zero and vanishes on the $(n - 1)$-dimensional space $D(x_0)$. By (i), $\mathrm{ad}_f^{n-1} g(x_0)$ is not in $D(x_0)$, so $dh(x_0) \cdot \mathrm{ad}_f^{n-1} g(x_0) \neq 0$. So $L_g L_f^{n-1} h(x_0) \neq 0$, and $h$ has relative degree $n$ at $x_0$. $\blacksquare$

## Consequences

- **Linear systems.** For $f = A x$ and $g = b$, $\mathrm{ad}_f^k g = (-1)^k A^k b$ are constant fields. Their brackets are zero, so $D$ is involutive, and (i) is the [Kalman rank condition](/kalman-rank-condition/). So every controllable single-input linear system is feedback linearizable, and the output $h$ of the proof gives the [controllable canonical form](/controllable-canonical-form/).
- **Systems in the plane.** For $n = 2$, $D = \mathrm{span}\{g\}$ is spanned by one field and is always involutive. So a planar system is feedback linearizable near $x_0$ if and only if $g(x_0)$ and $[f, g](x_0)$ are independent.
- **Construction.** The proof is constructive up to one step: $h$ solves the partial differential equations $L_{\mathrm{ad}_f^j g} h = 0$ for $j \le n - 2$. Then [feedback linearization](/feedback-linearization/) uses $T$, $\alpha$ and $\beta$ from the proof.
- **Flatness.** A single-input system is [differentially flat](/differential-flatness/) if and only if it satisfies these conditions (Charlet, Lévine and Marino 1989). For several inputs, flatness is strictly weaker.
- **Accessibility.** Condition (i) implies the [Lie algebra rank condition](/lie-algebra-rank-condition/) at $x_0$, so a linearizable system is locally accessible.

## Tightness

- **Involutivity cannot be dropped.** For $\dot x_1 = x_2 + x_3^2$, $\dot x_2 = x_3$, $\dot x_3 = u$, the fields are $g = (0, 0, 1)$, $\mathrm{ad}_f g = (-2 x_3, -1, 0)$ and $\mathrm{ad}_f^2 g = (1, 0, 0)$, independent at every point, so (i) holds everywhere. But $[g, \mathrm{ad}_f g] = (-2, 0, 0)$ is not in $\mathrm{span}\{g, \mathrm{ad}_f g\}$ at any point, so (ii) fails, and the system is not feedback linearizable near any point. Its Jacobian linearization at $0$ is a controllable chain of integrators. So a controllable linearization is not enough.
- **The rank condition cannot be dropped.** For $\dot x_1 = x_1$, $\dot x_2 = u$, $\mathrm{ad}_f g = 0$. The distribution $\mathrm{span}\{g\}$ is involutive, but (i) fails, and $x_1$ cannot be influenced at all.
- **The result is local.** In the system $\dot x_1 = a \sin x_2$, $\dot x_2 = -x_1^2 + u$, the conditions hold where $\cos x_2 \neq 0$, and the transformation $z = (x_1, a \sin x_2)$ works only on $|x_2| < \pi/2$. A global transformation needs extra conditions, which Hunt, Su and Meyer (1983) study.

## History

Brockett (1978) introduced linearization by feedback, for one input and a constant gain on the new input. Jakubczyk and Respondek (1980) gave the necessary and sufficient conditions for general feedback, and Hunt and Su found the same conditions independently; their paper with Meyer (1983) also treats transformations on large regions. Jakubczyk and Respondek also treated several inputs, and Isidori (1995, Chapter 5) gives the conditions for several inputs in the form above.

## References
