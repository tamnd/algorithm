---
tag: GEZP6T
kind: theorem
slug: youla-parametrization
name: Youla-Kucera parametrization
aliases:
- Youla parametrization
- Q-parametrization
area: control/robust-and-adaptive-control
level: advanced
summary: All controllers that internally stabilize a plant are given by one formula in a free parameter Q in RH-infinity. Every closed loop map is affine in Q.
prereqs: [coprime-factorization, feedback-control-loop, transfer-function-matrix]
see_also: [h-infinity-control-problem, dgkf-h-infinity-synthesis, internal-model-control, h2-optimal-control, sensitivity-function, complementary-sensitivity-function, linear-fractional-transformation, nu-gap-metric]
sources:
  - paper: doi:10.1109/TAC.1976.1101139
    title: Dante C. Youla, Joseph J. Bongiorno and Hamid A. Jabr, Modern Wiener-Hopf design of optimal controllers, Part I, The single-input-output case, IEEE Transactions on Automatic Control 21(1), 3-13, 1976
    locator: the description of all stabilizing controllers for a single-input single-output plant and its use in Wiener-Hopf design
  - paper: doi:10.1109/TAC.1976.1101223
    title: Dante C. Youla, Hamid A. Jabr and Joseph J. Bongiorno, Modern Wiener-Hopf design of optimal controllers, Part II, The multivariable case, IEEE Transactions on Automatic Control 21(3), 319-338, 1976
    locator: the parametrization of all stabilizing controllers for a multivariable plant with matrix fraction descriptions
  - paper: doi:10.1016/S1474-6670(17)67787-5
    title: Vladimir Kučera, Stability of discrete linear feedback systems, IFAC Proceedings Volumes 8(1), 573-578, 1975
    locator: the parametrization of all stabilizing controllers of a discrete-time plant by polynomial equations
  - paper: doi:10.1109/TAC.1981.1102603
    title: George Zames, Feedback and optimal sensitivity, model reference transformations, multiplicative seminorms, and approximate inverses, IEEE Transactions on Automatic Control 26(2), 301-320, 1981
    locator: the weighted sensitivity problem, posed through the parametrization of the sensitivity of a stable plant
  - paper: doi:10.1016/0167-6911(88)90055-2
    title: Keith Glover and John C. Doyle, State-space formulae for all stabilizing controllers that satisfy an H-infinity norm bound and relations to risk sensitivity, Systems and Control Letters 11(3), 167-172, 1988
    locator: the parametrization of all controllers that meet an H-infinity norm bound
  - book: isbn:9780134565675
    title: Kemin Zhou, John C. Doyle and Keith Glover, Robust and Optimal Control, Prentice Hall, 1996
    locator: Chapter 5 (internal stability and coprime factorization over RH-infinity) and Chapter 12 (parametrization of all stabilizing controllers)
---

The Youla-Kucera parametrization describes the set of all controllers that internally stabilize a given linear plant. Write the plant as a ratio of stable transfer functions, $P = N M^{-1}$, with factors that satisfy a Bezout identity (a [coprime factorization](/coprime-factorization/)). Then every stabilizing controller has the form $C = (Y + M Q)(X - N Q)^{-1}$ for exactly one proper stable parameter $Q$, and every proper stable $Q$ that keeps $C$ proper gives a stabilizing controller. The four closed loop maps of the [feedback loop](/feedback-control-loop/) are affine in $Q$. So a search over stabilizing controllers, which is a nonconvex set, becomes a search over the vector space of stable transfer functions, and any convex specification on the closed loop maps stays convex. Youla, Jabr and Bongiorno (1976) and Kučera (1975) found the result independently. It is the start of the H2 and [H-infinity](/h-infinity-control-problem/) design methods of the 1980s.

## Statement

Notation. $RH_\infty$ is the set of proper real rational transfer functions with all poles in the open left half plane. A square matrix over $RH_\infty$ is a unit if its inverse is also in $RH_\infty$. The loop has negative feedback, as everywhere in this area: the plant $P$ and the controller $C$ are proper real rational matrices, $e = r - y$, $u = C e + d$ and $y = P u$. The loop is well posed if $I + P(\infty) C(\infty)$ is invertible. It is internally stable if it is well posed and the four maps from $(r, d)$ to $(e, u)$ are in $RH_\infty$:

$$\begin{bmatrix} (I + P C)^{-1} & -(I + P C)^{-1} P \\ C (I + P C)^{-1} & (I + C P)^{-1} \end{bmatrix}.$$

**Theorem (Youla, Jabr and Bongiorno 1976; Kučera 1975).** Let $P$ be a proper real rational $p \times m$ matrix with a doubly coprime factorization over $RH_\infty$: $P = N M^{-1} = \tilde M^{-1} \tilde N$, with $M, N, \tilde M, \tilde N, X, Y, \tilde X, \tilde Y$ in $RH_\infty$ and

$$\begin{bmatrix} \tilde X & \tilde Y \\ -\tilde N & \tilde M \end{bmatrix} \begin{bmatrix} M & -Y \\ N & X \end{bmatrix} = \begin{bmatrix} I & 0 \\ 0 & I \end{bmatrix}.$$

Then a proper real rational $C$ internally stabilizes $P$ if and only if

$$C = (Y + M Q)(X - N Q)^{-1} = (\tilde X - Q \tilde N)^{-1}(\tilde Y + Q \tilde M)$$

for some $Q \in RH_\infty^{m \times p}$ with $\det(X(\infty) - N(\infty) Q(\infty)) \ne 0$. The map from $Q$ to $C$ is one to one. For this $C$,

$$(I + P C)^{-1} = (X - N Q)\tilde M, \qquad P C (I + P C)^{-1} = N(\tilde Y + Q \tilde M), \qquad C (I + P C)^{-1} = M(\tilde Y + Q \tilde M),$$

and $(I + P C)^{-1} P = (X - N Q)\tilde N$. Each map is affine in $Q$.

**Stable plant.** If $P \in RH_\infty$, take $N = \tilde N = P$, $M = \tilde M = I$, $X = \tilde X = I$ and $Y = \tilde Y = 0$. The theorem then says: $C$ stabilizes $P$ if and only if $C = Q(I - P Q)^{-1}$ with $Q \in RH_\infty$ and $I - P(\infty) Q(\infty)$ invertible, and then $(I + P C)^{-1} = I - P Q$ and $P C (I + P C)^{-1} = P Q$.

A doubly coprime factorization exists for every proper real rational $P$; state-space formulas come from a stabilizable and detectable realization (see [coprime factorization](/coprime-factorization/)). That page uses the loop $u = K y$ with the identity $X M - Y N = I$. Its form is the one here with $K = -C$, $Y$ replaced by $-Y$ and $Q$ replaced by $-Q$.

## In plain words

A controller can make an unstable plant behave well, but most controllers you try will fail. The set of the good ones has a strange shape, so it is hard to search. The theorem gives a map that turns this set into a simple one. Pick any stable transfer function $Q$. Put it into a fixed formula built from the plant. The result is a controller that stabilizes the plant. Every stabilizing controller comes out of the formula for exactly one $Q$. Also, the closed loop responses depend on $Q$ in a linear way, plus a constant. So if you want a small tracking error or a small noise gain, you search over stable $Q$, and the problem is often convex.

## Proof

The proof is given for a single-input single-output plant, where all factors commute. The multivariable proof follows the same steps with the doubly coprime identity in place of the scalar Bezout identity (Zhou, Doyle and Glover 1996, chapter 12). In the scalar case the identity says $X M + Y N = 1$, with $\tilde X = X$, $\tilde Y = Y$, $\tilde M = M$ and $\tilde N = N$.

**Step 1: a test for internal stability.** Let $C = U/V$ with $U, V \in RH_\infty$ coprime: $R V + W U = 1$ for some $R, W \in RH_\infty$. Every proper rational $C$ has such a factorization. Put $\Delta = M V + N U$. Then

$$\frac{1}{1 + P C} = \frac{M V}{\Delta}, \quad \frac{P}{1 + P C} = \frac{N V}{\Delta}, \quad \frac{C}{1 + P C} = \frac{M U}{\Delta}, \quad \frac{P C}{1 + P C} = \frac{N U}{\Delta},$$

because $1 + P C = 1 + (N U)/(M V) = \Delta/(M V)$. *Claim: the loop is internally stable if and only if $\Delta$ is a unit of $RH_\infty$.* If $1/\Delta \in RH_\infty$, the four maps are products of elements of $RH_\infty$. Conversely, let the four maps be in $RH_\infty$. Multiply the two Bezout identities:

$$\frac{1}{\Delta} = \frac{(X M + Y N)(R V + W U)}{\Delta} = X R \frac{M V}{\Delta} + X W \frac{M U}{\Delta} + Y R \frac{N V}{\Delta} + Y W \frac{N U}{\Delta},$$

which is in $RH_\infty$. Well-posedness is part of this: $1/\Delta$ is proper.

**Step 2: every Q gives a stabilizing controller.** Let $Q \in RH_\infty$ with $X(\infty) - N(\infty) Q(\infty) \ne 0$. Put $U = Y + M Q$ and $V = X - N Q$. Then

$$M V + N U = M X - M N Q + N Y + N M Q = M X + N Y = 1.$$

This identity also shows that $U$ and $V$ are coprime, with the coefficients $M$ and $N$. $V$ is not zero at infinity, so $C = U/V$ is proper. By Step 1 with $\Delta = 1$, the loop is internally stable, and the four maps are $M V$, $N V$, $M U$ and $N U$: these are the formulas in the statement.

**Step 3: every stabilizing controller comes from some Q.** Let $C$ stabilize $P$, and write $C = U/V$ coprime. By Step 1, $\Delta = M V + N U$ is a unit. Put $U' = U/\Delta$ and $V' = V/\Delta$. They are in $RH_\infty$, $C = U'/V'$ and $M V' + N U' = 1$. Define $Q = X U' - Y V' \in RH_\infty$. Use $M X = 1 - N Y$:

$$Y + M Q = Y + M X U' - M Y V' = Y + U' - Y(N U' + M V') = U',$$

and in the same way, with $N Y = 1 - M X$, $X - N Q = X - N X U' + N Y V' = X + V' - X(N U' + M V') = V'$. So $C = (Y + M Q)/(X - N Q)$. Also $V' = 1/(M + N C)$ and $M + N C$ is proper, so $V'(\infty) = X(\infty) - N(\infty) Q(\infty) \ne 0$.

**Step 4: the map is one to one.** If $C = (Y + M Q)/(X - N Q)$, then the pair $(U, V) = (Y + M Q, X - N Q)$ has $M V + N U = 1$ by Step 2, and $U = C V$. So $(M + N C) V = 1$ and $V = 1/(M + N C)$ is fixed by $C$. Then $Q = (X - V)/N$ on the set where $N \ne 0$, and $N$ is not the zero function unless $P = 0$. If $P = 0$, take $N = 0$, $M = X = 1$ and $Y = 0$; then $C = Q$. In both cases $Q$ is fixed by $C$. $\square$

## Consequences

**Example.** $P = 1/(s - 1)$. Take $N = 1/(s + 1)$, $M = (s - 1)/(s + 1)$, $X = 1$ and $Y = 2$, so that $X M + Y N = (s - 1 + 2)/(s + 1) = 1$. For a constant $Q = q$:

$$C = \frac{2 + q\,\frac{s - 1}{s + 1}}{1 - \frac{q}{s + 1}} = \frac{(2 + q) s + 2 - q}{s + 1 - q}.$$

The closed loop polynomial is $(s - 1)(s + 1 - q) + (2 + q) s + 2 - q = s^2 + 2 s + 1$ for every $q$. So $q = 0$ gives the static gain $C = 2$, $q = 1$ gives the PI controller $C = 3 + 1/s$, and $q = -1$ gives $C = (s + 3)/(s + 2)$. Each places both closed loop poles at $-1$, which are the poles of the factors and of $Q$. The sensitivity is $S = \frac{s - 1}{s + 1} \cdot \frac{s + 1 - q}{s + 1}$; it is 0 at the unstable pole $s = 1$ for every $q$. With $q = 1$, $S(0) = 0$, so the PI controller has zero steady state error for a step reference.

- **Affine closed loop.** With $T_1 = X \tilde M$, $T_2 = N$, $T_3 = \tilde M$ (scalar case), the sensitivity is $T_1 - T_2 Q T_3$. A weighted H-infinity problem $\min_C \|W S\|_\infty$ over stabilizing $C$ becomes the model matching problem $\min_{Q \in RH_\infty} \|W(T_1 - T_2 Q T_3)\|_\infty$, which is convex in $Q$ (Zames 1981). The same holds for the [H2 norm](/h2-optimal-control/) and for time domain bounds on step responses.
- **Internal model control.** For a stable plant, $C = Q/(1 - P Q)$ is the [internal model control](/internal-model-control/) structure: the controller runs a copy of the plant model in parallel with $Q$. The parameter $Q$ is the map from $r$ to $u$, and $P Q$ is the complementary sensitivity.
- **Interpolation conditions.** For a scalar plant, $S = M(X - N Q)$ vanishes at every unstable pole of $P$ (a zero of $M$), and $T = N(Y + M Q)$ vanishes at every unstable zero of $P$. These constraints hold for every stabilizing controller, and they cause the classical limits of performance, such as the [Bode sensitivity integral](/bode-sensitivity-integral/).
- **All suboptimal H-infinity controllers.** The set of controllers that meet an H-infinity bound is again an LFT in a free parameter, now with $\|Q\|_\infty < \gamma$ (Glover and Doyle 1988; see the [two-Riccati page](/dgkf-h-infinity-synthesis/)).
- **Rule of thumb.** In numerical design, $Q$ is often restricted to a finite expansion $\sum_k q_k \phi_k$ in fixed stable filters $\phi_k$, which gives a finite dimensional convex problem. This gives an upper bound on the true optimum, and the order of the controller grows with the number of filters.

## Tightness

- **Q must be stable.** For $P = 1/(s - 1)$ with the factors of the example in Consequences, $Q = 1/(s - 2)$ gives $S = M(X - N Q) = \frac{s - 1}{s + 1}\bigl(1 - \frac{1}{(s + 1)(s - 2)}\bigr)$, which has a pole at $s = 2$. The controller is proper, but the loop is not internally stable.
- **The properness condition cannot be dropped.** For the stable static plant $P = 1$ the formula is $C = Q/(1 - Q)$. The constant $Q = 1$ is in $RH_\infty$, but it gives $X(\infty) - N(\infty) Q(\infty) = 0$, and no proper controller results.
- **Coprimeness cannot be dropped.** The factors $N = (s - 1)/(s + 1)^2$ and $M = (s - 1)^2/(s + 1)^2$ also give $P = 1/(s - 1)$, but they are not coprime, and no $X, Y$ satisfy the Bezout identity. With these factors the formula cannot be set up.
- **Internal stability, not only the map from r to y.** The controller $C = (s - 1)/s$ cancels the unstable pole: $P C = 1/s$, and $P C/(1 + P C) = 1/(s + 1)$ is in $RH_\infty$. But $P/(1 + P C) = s/((s - 1)(s + 1))$ has a pole at $s = 1$. This $C$ is not in the parametrized set, as the theorem says.

## History

Youla, Jabr and Bongiorno published the parametrization in 1976, in a two part paper on Wiener-Hopf design of optimal controllers, first for single-input single-output plants and then for multivariable plants. Kučera gave the same result for discrete-time plants with polynomial equations in 1975, and his name is often added for this reason. Zames (1981) used the parametrization for a stable plant to pose the H-infinity sensitivity problem, and the coprime factorization approach of the 1980s gave the form over $RH_\infty$ used here (Zhou, Doyle and Glover 1996, chapter 12). The state-space solutions of the H2 and H-infinity problems later gave the controllers directly, but the parametrization remains the basis of convex controller design.

## References
