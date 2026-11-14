---
tag: Y5D7CB
kind: theorem
slug: burmester-theory
name: Burmester theory
aliases:
- center-point and circle-point curves
- Burmester points
area: cad/mechanism-and-assembly-design
level: advanced
summary: For four positions of a moving plane the pivots of all guiding cranks lie on two circular cubics, the center-point and circle-point curves; for five positions at most four cranks exist.
prereqs: [motion-generation, standard-form-dyad-synthesis]
see_also: [kinematic-synthesis, nine-point-path-synthesis, path-generation, optimization-based-linkage-synthesis, homotopy-continuation, grashof-condition, transmission-angle, four-bar-linkage]
sources:
  - book: "Ludwig Burmester, Lehrbuch der Kinematik, Erster Band, Die ebene Bewegung, Arthur Felix, Leipzig, 1888"
    locator: the theory of a plane moving through four and five given positions, the center-point and circle-point curves and the Burmester points (general locator)
  - paper: "O. Bottema, On the determination of the Burmester points for five positions of a moving plane, Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen, Series A, 67 (1964), 310 to 318; also Indagationes Mathematicae 26 (1964)"
    locator: exact wording of the title not confirmed against the original
  - book: isbn:0486663469
    title: O. Bottema and B. Roth, Theoretical Kinematics, North-Holland, 1979; Dover reprint, 1990
    locator: the chapter on plane kinematics, finitely separated positions and the center-point and circle-point curves (general locator)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 5 (pp. 93 to 123), algebraic synthesis of planar chains, the center-point curve for four positions and the Burmester points for five
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, four- and five-position motion generation with the standard form and the center-point and circle-point curves (chapter-level locator)
  - paper: "F. Freudenstein and G. N. Sandor, Synthesis of path-generating mechanisms by means of a programmed digital computer, Journal of Engineering for Industry (Transactions of the ASME, Series B), 81(2) (1959), 159 to 168"
---

Burmester theory describes every crank that can guide a moving plane through four or five given positions. A crank here is a dyad: a fixed pivot, the center point, joined by a link of fixed length to a moving pivot, the circle point, that rides on the moving plane. For four positions the center points of all such cranks fill a cubic curve, and their circle points fill a second cubic. For five positions only the points common to two of these curves are left, and there are at most four of them, the Burmester points. Two cranks make a [four-bar linkage](/four-bar-linkage/), so five positions allow at most six four-bars.

The problem itself, with the bookkeeping of positions and the checks that a synthesized linkage must pass, is on the [motion generation](/motion-generation/) page. The linear algebra for two and three positions is on the [standard form dyad synthesis](/standard-form-dyad-synthesis/) page. This page proves the curves and the count.

## Statement

A position of the moving plane is a rigid motion $D_j(x) = R_j x + d_j$, with $R_j$ the rotation by $\theta_j$ and $d_j \in \mathbb{R}^2$. A *dyad* for the positions $D_1, \dots, D_n$ is a point $c$ of the moving plane, the circle point, a point $m$ of the fixed plane, the center point, and a length $r$, with

$$|D_j c - m| = r \qquad (j = 1, \dots, n).$$

The *pole* $P_{jk}$ is the fixed point of the displacement $D_k D_j^{-1}$ from position $j$ to position $k$; it exists when $\theta_j \ne \theta_k$. The *circular points* are $I = (1 : i : 0)$ and $J = (1 : -i : 0)$ of the complex projective plane. A curve through both is called circular.

**Theorem (Burmester 1888).** Let the positions have pairwise different angles.

1. *Count.* A dyad has five real parameters and each position imposes one equation on them, so for $n$ positions in general the dyads form a family of dimension $5 - n$: three for two positions, two for three, one for four, a finite set for five and none for six or more.
2. *Four positions.* The center points of the dyads lie on the curve $\det M(m) = 0$, where $M(m)$ is a $3 \times 3$ matrix whose entries are affine in $m$. This curve has degree at most 3. Its cubic part is $-8|m|^2 \lambda(m)$ for a linear form $\lambda$, so when $\lambda \ne 0$ it is a circular cubic, the *center-point curve*. It passes through the six poles $P_{jk}$. The circle points, written in the moving plane, lie on the center-point curve of the inverse motions $D_j^{-1}$, a circular cubic called the *circle-point curve*.
3. *Five positions.* The center points are among the common points of the center-point curves $C_4$ of positions $1, 2, 3, 4$ and $C_5$ of positions $1, 2, 3, 5$. If $C_4$ and $C_5$ have no common component, then apart from $I$, $J$, $P_{12}$, $P_{13}$ and $P_{23}$ they meet in at most four points, the *Burmester points*, and exactly four counted with multiplicity when those five points are simple intersections. The number of real ones is 0, 2 or 4, and any two real dyads make a four-bar, so there are at most $\binom{4}{2} = 6$ four-bars.

The proof uses Bezout's theorem: two curves of degrees $p$ and $q$ in the complex projective plane with no common component meet in exactly $pq$ points counted with multiplicity. It is cited, not proved.

## In plain words

Pick a point on a moving plate and a fixed pin on the ground. A rod can join them only if the point stays at the same distance from the pin in every position the plate must take. Each position is one condition, and the point and pin together have five numbers to choose. So with four positions there is one degree of freedom left, and the possible pins trace a curve. With five positions nothing is left to choose, and only a few pins work.

The curve for four positions is a cubic, and it always passes through the poles, the pivots of the single turns that carry one position to another. For five positions, take two such curves, built from two groups of four positions. They meet in nine points, but five of those meetings are forced and useless, which leaves at most four useful pins.

## Proof

**Step 1, the count.** The unknowns are $c \in \mathbb{R}^2$, $m \in \mathbb{R}^2$ and $r$, five real numbers. Each position gives the single equation $|D_j c - m|^2 = r^2$. Since $r$ appears only through $r^2 = |D_1 c - m|^2$, it can be eliminated, which leaves the four unknowns $c, m$ and the $n - 1$ equations

$$f_j(c, m) = |D_j c - m|^2 - |D_1 c - m|^2 = 0 \qquad (j = 2, \dots, n).$$

For equations in general position the solution set has dimension $4 - (n - 1) = 5 - n$. The same number comes out of the standard form on the [standard form dyad synthesis](/standard-form-dyad-synthesis/) page, with $W$ and $Z$ as unknowns.

**Step 2, each equation is linear in $c$.** Since $R_j$ is a rotation, $|R_j c|^2 = |c|^2$, and

$$|D_j c - m|^2 = |c|^2 + 2 (R_j c) \cdot (d_j - m) + |d_j - m|^2.$$

The term $|c|^2$ cancels in $f_j$. Writing $(R_j c) \cdot v = c \cdot R_j^{\mathsf T} v$,

$$f_j(c, m) = c \cdot g_j(m) + h_j(m), \qquad g_j(m) = 2 R_j^{\mathsf T}(d_j - m) - 2 R_1^{\mathsf T}(d_1 - m), \qquad h_j(m) = |d_j - m|^2 - |d_1 - m|^2.$$

Both $g_j$ and $h_j = |d_j|^2 - |d_1|^2 - 2 m \cdot (d_j - d_1)$ are affine in $m$. So for a fixed $m$ the equations $f_j = 0$ are linear in $c$.

**Step 3, four positions give a cubic.** For $n = 4$ the three equations $f_2 = f_3 = f_4 = 0$ read $M(m) (c, 1)^{\mathsf T} = 0$, where row $j$ of the $3 \times 3$ matrix $M(m)$ is $(g_j(m)^{\mathsf T}, h_j(m))$. A solution $c$ exists only if $\det M(m) = 0$. Conversely, if $\det M(m) = 0$ and the $3 \times 2$ block of the $g_j$ has rank 2, the kernel of $M(m)$ is spanned by a vector with last entry not zero, and scaling it gives the unique $c$. Every entry of $M(m)$ is affine in $m$, so $\det M(m)$ is a polynomial of degree at most 3.

Its cubic part comes from the linear parts of the entries. A difference of two rotations has the form $R_j^{\mathsf T} - R_1^{\mathsf T} = a_j I_2 + b_j Q$, where $Q$ is the rotation by $90°$ and $a_j, b_j$ are real. So the linear part of $g_j(m)$ is $-2(a_j m + b_j Q m)$ and the linear part of $h_j(m)$ is $-2 e_j \cdot m$, with $e_j = d_j - d_1$. Put $N(m)$ for the $2 \times 2$ matrix with rows $m^{\mathsf T}$ and $(Qm)^{\mathsf T}$. Row $j$ of the linear part is $-2 (a_j, b_j, e_j \cdot m) \operatorname{diag}(N(m), 1)$, and $\det N(m) = m_x^2 + m_y^2 = |m|^2$. Hence

$$\text{cubic part of } \det M(m) = (-2)^3 \, |m|^2 \det \begin{pmatrix} a_2 & b_2 & e_2 \cdot m \\ a_3 & b_3 & e_3 \cdot m \\ a_4 & b_4 & e_4 \cdot m \end{pmatrix} = -8 |m|^2 \lambda(m),$$

with $\lambda$ linear in $m$. In homogeneous coordinates $(x : y : w)$ the points at infinity of the curve are the zeros of the cubic part with $w = 0$, and $x^2 + y^2 = 0$ at $I$ and $J$. So when $\lambda \ne 0$ the curve is a cubic through $I$ and $J$.

**Step 4, the poles lie on the curve.** The displacement $D_k D_j^{-1}$ is a rigid motion that fixes $P_{jk}$, so for every $c$

$$|D_k c - P_{jk}| = |D_k D_j^{-1}(D_j c) - D_k D_j^{-1}(P_{jk})| = |D_j c - P_{jk}|.$$

For $j = 1$ this says $f_k(c, P_{1k}) = 0$ for every $c$, so row $k$ of $M(P_{1k})$ is zero and the determinant vanishes. For $2 \le j < k$ it says $f_k(c, P_{jk}) - f_j(c, P_{jk}) = |D_k c - P_{jk}|^2 - |D_j c - P_{jk}|^2 = 0$ for every $c$, so rows $j$ and $k$ of $M(P_{jk})$ are equal and again the determinant vanishes. All six poles lie on the center-point curve.

**Step 5, the circle-point curve.** Each $D_j$ is an isometry, so $|D_j c - m| = |c - D_j^{-1} m|$. Read the other way, $c$ is a center point and $m$ a circle point for the positions $D_j^{-1}$ of the fixed plane seen from the moving plane. Steps 3 and 4 applied to the inverse motions show that the circle points lie on a circular cubic in the moving plane. It passes through the poles of the inverse motions, which are the points $x$ with $D_j x = D_k x$, the points of the moving plane that sit at $P_{jk}$ in positions $j$ and $k$.

**Step 6, five positions.** Let $M_4(m)$ have rows $f_2, f_3, f_4$ and $M_5(m)$ rows $f_2, f_3, f_5$, and let $C_4$ and $C_5$ be their zero curves, the center-point curves of positions $1, 2, 3, 4$ and $1, 2, 3, 5$. The center point of a dyad through all five positions lies on both. Five common points are forced and have nothing to do with positions 4 and 5:

- $I$ and $J$, by Step 3;
- $P_{12}$ and $P_{13}$, where the row of $f_2$ or of $f_3$ vanishes, and $P_{23}$, where those two rows are equal, by Step 4.

By Bezout's theorem, $C_4 \cap C_5$ has exactly $3 \cdot 3 = 9$ points counted with multiplicity when the cubics have no common component. The five forced points use up at least 5, so at most 4 remain, and exactly 4 when the forced points are simple. Conversely, let $m$ be a common point that is not forced and at which the rows $g_2(m), g_3(m)$ are independent. Then $f_2 = f_3 = 0$ has a unique solution $c$, and $\det M_4(m) = 0$ makes $f_4(c, m) = 0$ while $\det M_5(m) = 0$ makes $f_5(c, m) = 0$. So $c$ and $m$ form a dyad through all five positions.

Both determinants have real coefficients, so the non-real common points come in conjugate pairs. Of the four, counted with multiplicity, an even number are non-real, so 0, 2 or 4 are real. Two real dyads share the moving plane and make a four-bar with the moving plane as coupler; four dyads give $\binom{4}{2} = 6$ pairs. $\blacksquare$

## Consequences

**Four positions leave a curve to choose from.** A designer picks a center point on the center-point curve, reads off its circle point, and repeats for a second dyad. The one free parameter on each dyad is used to place pivots on the frame and to meet the conditions that the curves do not see: [Grashof type](/grashof-condition/), the order of the positions, a single branch, and a good [transmission angle](/transmission-angle/), as described on the [motion generation](/motion-generation/) page.

**Five positions leave a short list.** The four Burmester points give at most six four-bars, and these must be checked one by one. The example below shows that most of them can fail.

**Six positions are generally out of reach.** A sixth position adds a sixth equation to five unknowns, so a four-bar can only approximate it. This is the step to [optimization-based linkage synthesis](/optimization-based-linkage-synthesis/). Linkages with more links, such as the [six-bar linkages](/watt-and-stephenson-six-bar/), have more parameters and reach more positions.

**The computation is small.** Five positions lead to a polynomial system with four solutions. It is solved by elimination, by intersecting the two cubics, or by [homotopy continuation](/homotopy-continuation/). The harder count for path generation through nine points is on the [nine-point path synthesis](/nine-point-path-synthesis/) page.

**Example.** Take five positions of the coupler of the four-bar with ground pivots $O_2 = (0, 0)$ and $O_4 = (9, 0)$, input $a = 15$, coupler $b = 5$ and output $c = 13$, the reference linkage of the [kinematic synthesis](/kinematic-synthesis/) page. The moving frame has its origin at $A$ and its first axis along $AB$, so $A = D_j(0, 0)$ and $B = D_j(5, 0)$.

| position | input angle | $A$ | coupler angle $\theta_j$ |
| --- | --- | --- | --- |
| 1 | $30°$ | $(12.9904, 7.5000)$ | $29.71°$ |
| 2 | $45°$ | $(10.6066, 10.6066)$ | $7.03°$ |
| 3 | $60°$ | $(7.5000, 12.9904)$ | $-5.33°$ |
| 4 | $75°$ | $(3.8823, 14.4889)$ | $-17.38°$ |
| 5 | $90°$ | $(0, 15)$ | $-36.87°$ |

The equations $\det M_4(m) = \det M_5(m) = 0$ were solved by Newton's method in complex arithmetic from 3000 seeded random starts. It found seven finite common points. Three are the forced poles $P_{12} = (19.5433, 14.9961)$, $P_{13} = (18.9422, 18.9422)$ and $P_{23} = (20.0653, 26.1496)$. The other four are the Burmester points, and here all four are real:

| dyad | center point $m$ | circle point in position 1 | length $r$ |
| --- | --- | --- | --- |
| $K_1$ | $(0, 0)$ | $(12.9904, 7.5000)$ | $15$ |
| $K_2$ | $(9, 0)$ | $(17.3332, 9.9778)$ | $13$ |
| $K_3$ | $(11.3115, 19.9803)$ | $(11.9496, 17.7380)$ | $2.3313$ |
| $K_4$ | $(-4.7435, 7.1337)$ | $(8.3811, 8.7375)$ | $13.2222$ |

$K_1$ and $K_2$ are the input and output of the linkage that made the positions, as they must be. For each dyad the five distances $|D_j c - m|$ agree to within $2 \cdot 10^{-14}$. As Step 4 predicts, $P_{14}$, $P_{24}$ and $P_{34}$ lie on $C_4$ but not on $C_5$, and $P_{45}$ lies on neither.

The six four-bars were then driven through the motion, stepping the driving link in 6000 parts:

| four-bar | ground, links, coupler | moves through positions 1 to 5 in order |
| --- | --- | --- |
| $K_1 K_2$ | $9$; $15$, $13$; $5$ | yes, driven at $K_1$; transmission angle $20.4°$ to $149.5°$ |
| $K_1 K_4$ | $8.5668$; $15$, $13.2222$; $4.7725$ | yes, driven at $K_1$; transmission angle $26.2°$ to $158.0°$ |
| $K_2 K_4$ | $15.4846$; $13$, $13.2222$; $9.0377$ | only when driven at $K_4$; transmission angle $42.2°$ to $171.3°$ |
| $K_1 K_3$ | $22.9600$; $15$, $2.3313$; $10.2907$ | no |
| $K_2 K_3$ | $20.1135$; $13$, $2.3313$; $9.4447$ | no |
| $K_3 K_4$ | $20.5620$; $2.3313$, $13.2222$; $9.6821$ | no |

In the last three, the sign of the assembly changes between two positions whichever grounded link drives, so the coupler and the driven link become collinear on the way, or the positions are on different branches. Only the original and two new four-bars are usable, and all three have transmission angles far from $90°$ at the ends of the motion.

## Tightness

- **Four is reached.** The example has four real Burmester points. Real counts 0 and 2 also occur. For 40 sets of five random positions (seeds 0 to 39), Newton's method from 400 starts found all four points for 34 sets: 12 had no real point, 17 had two and 5 had four.
- **The five forced points cannot be dropped.** Bezout's bound of 9 for two cubics is never reached by dyads, because $I$, $J$, $P_{12}$, $P_{13}$ and $P_{23}$ lie on both curves for every choice of positions 4 and 5.
- **The hypothesis of no common component is needed.** If all five positions are translations, $R_j = I_2$, then $g_j(m) = 2(d_j - d_1)$ is constant and $\det M(m)$ has degree at most 1, so there is no cubic. If moreover the $d_j$ lie on a circle with center $q$, then for every $c$ the point $m = c + q$ gives $|D_j c - m| = |d_j - q|$, the same for all $j$. Every circle point has a center point, a two-parameter family of dyads, which is the motion of a parallelogram linkage.
- **Pairwise different angles are needed for the poles.** If $\theta_j = \theta_k$ the displacement from $j$ to $k$ is a translation, its pole is at infinity, and the curve need not pass through it in the affine plane.

## History

Ludwig Burmester set out the theory in his *Lehrbuch der Kinematik* of 1888. He named the center-point curve (Mittelpunktkurve) and the circle-point curve (Kreispunktkurve) and found the points for five positions by graphical construction from the poles, which is why they carry his name. In 1964 Oene Bottema gave a method to compute the Burmester points for five positions, and the theory takes its modern algebraic form in Bottema and Roth's *Theoretical Kinematics* of 1979. Freudenstein and Sandor's 1959 program on an IBM 650 for five-point path generation with prescribed crank rotations was an early use of the computer for finitely separated positions, and the complex-number standard form of Sandor and Erdman made the four- and five-position cases a routine part of textbooks.

## References
