---
tag: PC7C1B
kind: technique
slug: standard-form-dyad-synthesis
name: Standard form dyad synthesis
aliases:
- complex number dyad synthesis
- Erdman-Sandor dyad method
area: cad/mechanism-and-assembly-design
level: advanced
summary: Writes each side of a linkage as a dyad of two complex vectors and solves the loop equations for the given positions, linear for up to three positions.
prereqs: [vector-loop-closure, motion-generation]
see_also: [burmester-theory, path-generation, function-generation, kinematic-synthesis, four-bar-linkage, cramers-rule, gaussian-elimination, transmission-angle]
sources:
  - book: isbn:0130408727
    title: Arthur G. Erdman, George N. Sandor and Sridhar Kota, Mechanism Design, Analysis and Synthesis, Volume 1, 4th edition, Prentice Hall, 2001
    locator: Chapter 8, Introduction to Kinematic Synthesis, Graphical and Linear Analytical Methods (the standard form of the dyad, the table of free choices, and three-position synthesis by Cramer's rule)
  - book: isbn:9781260113310
    title: Robert L. Norton, Design of Machinery, 6th edition, McGraw-Hill, 2019
    locator: Chapter 5 (two- and three-position motion generation by analytical synthesis with the W and Z dyads, and path generation with prescribed timing)
  - book: doi:10.1007/978-1-4419-7892-9
    title: J. Michael McCarthy and Gim Song Soh, Geometric Design of Linkages, 2nd edition, Springer, 2011
    locator: Chapter 5 (pp. 93 to 123), algebraic synthesis of planar chains
  - book: "Richard S. Hartenberg and Jacques Denavit, Kinematic Synthesis of Linkages, McGraw-Hill, New York, 1964"
    locator: the chapters on the complex number method for finitely separated positions (general locator)
---

Standard form dyad synthesis designs a planar linkage one side at a time. Each side is a dyad: a grounded link $W$ and a vector $Z$ from its moving pivot to the precision point, both written as complex numbers. If the link turns by $\beta_j$ and the coupler by $\alpha_j$ between position 1 and position $j$, the loop closure gives the standard form $W(e^{i\beta_j} - 1) + Z(e^{i\alpha_j} - 1) = \delta_j$, with $\delta_j = P_j - P_1$. For two or three positions the designer picks the free rotations and the standard form is a linear system for $W$ and $Z$; for four and five positions it leads to [Burmester theory](/burmester-theory/).

## In plain words

A four-bar is two arms joined by a middle piece. Each arm is fixed to the ground at one end and turns about that pivot. The middle piece carries the point or the part that must move.

This method looks at one arm and the line from its end to the moving point. It writes both as arrows, with a length and a direction. When the linkage moves to a new position, each arrow turns by some angle, and the arrows must still end at the new point. That gives one equation per new position.

If you choose how far the arm turns, the equations become simple and you can solve them exactly by hand. You then repeat the work for the other arm and join the two arms with the middle piece.

## When it applies

- The task is [motion generation](/motion-generation/), [path generation](/path-generation/) with prescribed timing, or [function generation](/function-generation/), for a planar linkage made of dyads (four-bars, slider-cranks, and the loops of six-bars).
- The number of positions is two or three, so that the system is linear after the free choices. With four or five positions the same equations are still the right model, but they are nonlinear.
- The rotations that the task does not give are free choices of the designer. In motion generation the coupler rotations $\alpha_j$ are given and the link rotations $\beta_j$ are free; in path generation with timing the $\beta_j$ of the input are given and the $\alpha_j$ are free.

## The template

The input is the three precision points $P_1, P_2, P_3$, the coupler rotations $\alpha_2, \alpha_3$, and the link rotations $\beta_2, \beta_3$, of which some are free choices.

```pseudo id=main
STANDARD-FORM-DYAD(P1, P2, P3, α2, α3, β2, β3)
L1  for j ∈ {2, 3}:  Bj ← e^{iβj} − 1;  Aj ← e^{iαj} − 1;  δj ← Pj − P1
L2  D ← B2·A3 − B3·A2
L3  if D = 0 then return "singular: change the free choices"
L4  W ← (δ2·A3 − δ3·A2)/D
L5  Z ← (B2·δ3 − B3·δ2)/D
L6  G ← P1 − W − Z
L7  return the fixed pivot G, the link W and the vector Z
```

Line L1 forms the coefficients. Lines L2, L4 and L5 are [Cramer's rule](/cramers-rule/) for the $2 \times 2$ complex system of the standard form, and L3 rejects the singular case. Line L6 places the fixed pivot so that the dyad ends at $P_1$ in position 1. The moving pivot in position $j$ is $G + W e^{i\beta_j}$, and $|W|$ is the length of the grounded link. Run the template twice, with two different sets of free choices but the same $\alpha_j$, to get two dyads. They share the coupler, so together they are a four-bar with ground $G_A G_B$, links $|W_A|$ and $|W_B|$, and coupler $|Z_A - Z_B|$.

### Derivation from the loop closure

Put the fixed pivot at $G$. In position 1 the dyad reaches the precision point by the link and then the coupler-side vector:

$$G + W + Z = P_1.$$

In position $j$ the grounded link has turned about $G$ by $\beta_j$, which multiplies its vector by $e^{i\beta_j}$, and the coupler has turned by $\alpha_j$, which multiplies every vector fixed in the coupler by $e^{i\alpha_j}$. The lengths stay the same because the links are rigid. So

$$G + W e^{i\beta_j} + Z e^{i\alpha_j} = P_j.$$

Subtract the equation of position 1. The unknown pivot $G$ cancels, and

$$W(e^{i\beta_j} - 1) + Z(e^{i\alpha_j} - 1) = P_j - P_1 = \delta_j.$$

This is the standard form. It is the [vector loop closure](/vector-loop-closure/) of the loop formed by the dyad in position 1, the dyad in position $j$, and the displacement $\delta_j$. Conversely, if $W$ and $Z$ satisfy the standard form for each $j$, then $G = P_1 - W - Z$ gives a dyad that reaches every $P_j$ with the coupler at the rotation $\alpha_j$, because adding the equation of position 1 back gives the equation of position $j$. $\blacksquare$

### The count of free choices

The unknowns of one dyad for $n$ positions are $W$ and $Z$ (four reals) and the $n - 1$ unknown rotations, one per position after the first (the $\beta_j$ in motion generation). Each position after the first gives one complex equation, so two real equations. The number of free real choices is

$$4 + (n - 1) - 2(n - 1) = 5 - n,$$

which is 3, 2, 1, 0 for $n = 2, 3, 4, 5$. For two positions the designer picks $\beta_2$ and $Z$ and solves one complex equation for $W$. For three positions the designer picks $\beta_2$ and $\beta_3$, and the template solves for $W$ and $Z$.

### When the system is singular

The system has the matrix $\begin{pmatrix} B_2 & A_2 \\ B_3 & A_3 \end{pmatrix}$ and determinant $D = B_2A_3 - B_3A_2$. It has a unique solution exactly when $D \ne 0$. With $e^{i\theta} - 1 = 2i\sin(\theta/2)\,e^{i\theta/2}$,

$$D = -4\left(\sin\tfrac{\beta_2}{2}\sin\tfrac{\alpha_3}{2}\,e^{i(\beta_2 + \alpha_3)/2} - \sin\tfrac{\beta_3}{2}\sin\tfrac{\alpha_2}{2}\,e^{i(\beta_3 + \alpha_2)/2}\right),$$

so $D = 0$ exactly when the rows $(B_2, A_2)$ and $(B_3, A_3)$ are proportional over the complex numbers. Cases that occur in practice:

- **The link turns with the coupler**, $\beta_2 = \alpha_2$ and $\beta_3 = \alpha_3$. Then $W$ and $Z$ enter only as $W + Z$, and the dyad is one rigid body turning about $G$. It exists only if the three positions are rotations about one point.
- **The link does not turn**, $\beta_2 = \beta_3 = 0$. Then $B_2 = B_3 = 0$ and $W$ drops out.
- **The coupler does not turn**, $\alpha_2 = \alpha_3 = 0$, a pure translation. Then $Z$ drops out, and the task needs a parallelogram or other special linkage.
- **Positions 2 and 3 have the same rotations**, $\beta_2 = \beta_3$ and $\alpha_2 = \alpha_3$.

When $D = 0$ the system has no solution unless $\delta_3$ is the same multiple of $\delta_2$, and then it has a one-parameter family. A $D$ close to zero gives very long links. The tests check that the template returns no dyad in each case above.

### Cost

One three-position dyad is a fixed number of complex operations. With exact data (rotations that are rational points $((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ of the unit circle and rational points $P_j$), every step is exact in rational arithmetic, which the tests use.

## Classic examples

**Recovering a known four-bar.** Take the four-bar with $O_2 = (0, 0)$, $O_4 = (9, 0)$, $a = 15$, $b = 5$, $c = 13$ and the midpoint $P$ of the coupler, at its three exact positions from the [kinematic synthesis](/kinematic-synthesis/) page: $P_1 = (72/5, 97/10)$, $P_2 = (23/2, 12)$, $P_3 = (2, 27/2)$. The coupler turns by $\alpha_2 = -16.26°$ and $\alpha_3 = -53.13°$, with

$$e^{i\alpha_2} = \tfrac{24}{25} - \tfrac{7}{25}i, \qquad e^{i\alpha_3} = \tfrac{3}{5} - \tfrac{4}{5}i.$$

With the input rotations $e^{i\beta_2} = \tfrac{24}{25} + \tfrac{7}{25}i$ and $e^{i\beta_3} = \tfrac{3}{5} + \tfrac{4}{5}i$ ($16.26°$ and $53.13°$), the template returns, in exact rational arithmetic,

$$G = 0, \qquad W = 12 + 9i, \qquad Z = \tfrac{12}{5} + \tfrac{7}{10}i,$$

which is the input link $O_2A$ and the half coupler from $A$ to $P$. With the output rotations $e^{i\beta_2} = \tfrac{63}{65} + \tfrac{16}{65}i$ and $e^{i\beta_3} = \tfrac{33}{65} + \tfrac{56}{65}i$ ($14.25°$ and $59.49°$) it returns $G = 9$, $W = \tfrac{39}{5} + \tfrac{52}{5}i$, $Z = -\tfrac{12}{5} - \tfrac{7}{10}i$, the output link $O_4B$ and the half coupler from $B$ to $P$.

**A new dyad by a free choice.** Keep the same positions and pick $\beta_2 = 10°$, $\beta_3 = 60°$. In floating point, the template gives $G = (16.9106, 2.2282)$, $W = (3.5547, 11.4201)$ with $|W| = 11.9606$, and $Z = (-6.0653, -3.9483)$. The dyad reaches the three points with errors below $4 \cdot 10^{-15}$. Joined with the output dyad above, it gives a four-bar with ground $8.2184$, links $11.9606$ and $13$, and coupler $4.8976$, a Grashof linkage whose shortest link is the coupler. Driving the new link through $0°$, $10°$, $60°$ in 3000 steps moves the linkage through the three positions on one branch. The [transmission angle](/transmission-angle/) at the three positions is $168.4°$, $137.9°$ and $55.8°$, so position 1 is close to a toggle and the design would be rejected. The free choices must be searched with this check, which is what design programs do.

**Two positions.** For two positions the designer chooses $\beta_2$ and $Z$. Then $W = (\delta_2 - Z(e^{i\alpha_2} - 1))/(e^{i\beta_2} - 1)$, one complex division. The [motion generation](/motion-generation/) page has a two-position example worked with the perpendicular bisector, which is the graphical form of the same equation.

**Path generation with prescribed timing.** For [path generation](/path-generation/) with timing the $\beta_j$ of the input dyad are data and the $\alpha_j$ are free. For three points the designer picks $\alpha_2$, $\alpha_3$ and the same template applies with the roles of the choices exchanged. The output dyad then uses the same $\alpha_j$ and its own free $\beta_j$.

**Function generation.** For [function generation](/function-generation/) with three precision points, put the precision point at the moving pivot of the output link in the frame of the input link (a kinematic inversion). The relative rotations play the role of $\alpha_j$ and $\beta_j$, and the template gives the coupler and the output link.

## Variations

- **Four positions.** A third equation $W B_4 + Z A_4 = \delta_4$ must be consistent with the first two. The condition is that the $3 \times 3$ complex determinant of the rows $(B_j, A_j, \delta_j)$ vanishes, one complex equation in $\beta_2, \beta_3, \beta_4$. One real choice remains, and the solutions trace the circle-point and center-point curves of [Burmester theory](/burmester-theory/).
- **Five positions.** Two such determinants must vanish, and the solutions are the at most four Burmester dyads.
- **Prescribed fixed pivot.** If the designer fixes $G$ and not the rotations, the equations are nonlinear in the $\beta_j$. Write $W = M_1 - G$ with $M_1$ unknown and use the inverse motion; for three positions this is again a center-of-circle construction.
- **Slider dyads.** A prismatic joint replaces $W e^{i\beta_j}$ by $W + s_j u$ with a fixed direction $u$ and unknown slides $s_j$, which gives the slider-crank form of the same method.
- **Six-bars.** Each loop of a Watt or Stephenson chain is written as dyads, and the method is applied loop by loop.

## Pitfalls

- **Wrong sign of the rotations.** All rotations are measured counterclockwise from position 1. A $\beta_j$ taken from the wrong end of the link or in the wrong sense gives a dyad that fits other positions.
- **Singular or near singular choices.** The cases listed above, and any choice with $|D|$ small, give no dyad or very long links. Check $|D|$ before you accept the result.
- **Each dyad is checked alone.** The template proves only that each dyad reaches each position. The four-bar made of two dyads can still have a branch defect, an order defect, or a poor transmission angle, as in the second example. Simulate the four-bar through the positions.
- **Free choices are not neutral.** The two free values for three positions move the fixed pivot over the plane. Pick them by a search with the side conditions, not by habit.
- **Floating point and exact data.** With rotations given in degrees the computed $e^{i\beta}$ are rounded, and the residuals are of order $10^{-15}$ times the size of the dyad. With rational points of the unit circle the method is exact.

## Exercises

1. Show that for three positions the fixed pivot $G$ found by the template is the center of the circle through the three positions $G + W e^{i\beta_j}$ of the moving pivot. Why is this the graphical method of the [motion generation](/motion-generation/) page?
2. In the first example, choose $\beta_2 = -16.26°$ and $\beta_3 = -53.13°$. Show that $D = 0$, and explain the result with the first singular case.
3. Prove that $D = 0$ when $\beta_2 = \beta_3$ and $\alpha_2 = \alpha_3$, and that the system then has a solution only if $\delta_2 = \delta_3$.
4. Write the condition for four positions as a $3 \times 3$ determinant, and count its real equations and unknowns.
5. Derive the standard form of a dyad whose grounded joint is prismatic, and solve it for three positions.

## References
