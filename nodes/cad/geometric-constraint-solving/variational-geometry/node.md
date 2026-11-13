---
tag: 7QY4S1
kind: concept
slug: variational-geometry
name: Variational geometry
aliases:
- variational design
area: cad/geometric-constraint-solving
level: core
summary: Light and Gossard's view of a design as a system of equations among its dimensions, so a change of one dimension is solved for the whole shape.
prereqs: [geometric-constraint-problem, newton-method-for-systems]
see_also: [feature-based-modeling, constructive-constraint-solving, local-propagation-solving, root-identification-problem, well-constrained-system, levenberg-marquardt, rank, homotopy-continuation]
sources:
  - paper: "Robert Light and David Gossard, Modification of geometric models through variational geometry, Computer-Aided Design 14(4), 209 to 214, 1982"
    locator: the model as characteristic points with dimension equations, the simultaneous solution by Newton-Raphson iteration, and the use of the Jacobian to find missing and redundant dimensions (general locator)
  - paper: "V. C. Lin, D. C. Gossard and R. A. Light, Variational geometry in computer-aided design, Computer Graphics (Proceedings of SIGGRAPH 81) 15(3), 171 to 177, 1981"
    locator: the first account of the method, with dimensions as constraint equations on the points of a part and their simultaneous solution (general locator)
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on numerical solution of constraint systems (general locator)
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: the survey of earlier approaches, with the numerical approach and its weak points against the graph-constructive one (general locator)
---

Variational geometry is the idea that the dimensions of a part are equations, and that the shape of the part is the solution of all these equations together. A change of one dimension does not move one point by a fixed rule. It changes one value in the system, and the solver finds the new shape that satisfies every dimension at the same time. Lin, Gossard and Light described the idea in 1981, and Light and Gossard gave the method in 1982: they wrote the part as a set of characteristic points, each dimension as an equation in their coordinates, and solved the whole system with [Newton's method](/newton-method-for-systems/) from the old shape. The same paper used the Jacobian of the system to find missing and redundant dimensions. Most commercial sketchers still have a numerical solver of this kind as a fallback for the parts of a sketch that the [graph-constructive](/constructive-constraint-solving/) methods cannot solve.

## In plain words

A drawing in a CAD program has numbers on it: this side is 50, that hole is 10 from the edge, these two lines meet at 90 degrees. In variational geometry, each number is a rule about the points of the drawing. When you change one number, the program does not just stretch one line. It looks for new positions of all the points that obey all the rules at once, and it starts from the old drawing so that the new one looks like the old one.

The program finds the answer by small steps. Each step looks at how far each rule is from being true and moves the points to fix all of them together. Near the answer, each step makes the error much smaller, so a few steps are enough.

## The idea

**The model.** The part has $n$ characteristic points, the corners and centers that fix its shape, with coordinates $x \in \mathbb{R}^N$. Each dimension or relation is an equation $f_k(x) = c_k$, as on the page on [geometric constraints](/geometric-constraint/). Some extra equations fix the part to the sheet, for example a fixed point and a fixed direction, so that the rigid motions are gone and the system $F(x) = 0$ has as many equations as unknowns.

**The solve.** Start from the current shape $x^{(0)}$ and repeat the Newton step
$$ J_F(x^{(t)})\, \delta = -F(x^{(t)}), \qquad x^{(t+1)} = x^{(t)} + \delta, $$
until the residual is small. The Jacobian $J_F$ is sparse, because each equation involves only the points of one dimension, so a sparse linear solver does each step. Near a regular solution, where $J_F$ is not singular, the error squares at each step. When the user changes one value $c_k$, the old shape is a good start, since the new solution is near the old one when the change is small.

**Analysis of the dimensioning.** The [rank](/rank/) of the Jacobian at the current shape tells the designer about the dimensions. If the rank is less than the number of unknowns because there are too few equations, some directions are free, and the null space of $J_F$ shows which points can still move: the part is under-dimensioned. If two rows are dependent, one dimension is redundant or in conflict with the others: the part is over-dimensioned. This is a numerical test at one shape. It is the same as the [well-constrained](/well-constrained-system/) condition at a regular point, and it can give a wrong answer at a special shape, such as three collinear points in a sketch that is well-constrained for other shapes.

**What the method does not do.** Newton's method finds one solution, the one whose basin of attraction holds the start. It gives no list of all solutions and no proof that a solution exists. When the start is far from the intended solution, the iteration can reach the mirror image or another branch, which is the [root identification problem](/root-identification-problem/), or it can diverge. When the start is a degenerate shape, $J_F$ is singular and the step is not defined. Damped methods such as [Levenberg-Marquardt](/levenberg-marquardt/) make the iteration more robust but do not change these limits. [Homotopy continuation](/homotopy-continuation/) can find all solutions, at a much higher cost.

## Examples

**One triangle, three dimensions.** Put $A$ at the origin and $B$ on the $x$-axis, so the unknowns are $x_B$, $x_C$ and $y_C$. The dimensions are $\lvert AB \rvert = 5$, $\lvert AC \rvert = 4$ and $\lvert BC \rvert = 3$:
$$ F(x) = \bigl(x_B^2 - 25,\; x_C^2 + y_C^2 - 16,\; (x_C - x_B)^2 + y_C^2 - 9\bigr). $$
Start from the drawn shape $B = (4.6, 0)$, $C = (3, 2)$. Newton's method gives these iterates; the last column is the largest $\lvert F_k \rvert$.

| step | $x_B$ | $x_C$ | $y_C$ | largest residual |
|---|---|---|---|---|
| 0 | 4.6 | 3.0 | 2.0 | 3.84 |
| 1 | 5.01739 | 3.20605 | 2.44093 | 0.239 |
| 2 | 5.00003 | 3.20000 | 2.40035 | $1.8 \times 10^{-3}$ |
| 3 | 5.00000 | 3.20000 | 2.40000 | $1.2 \times 10^{-7}$ |
| 4 | 5 | 3.2 | 2.4 | $6 \times 10^{-16}$ |

The exact solution is $C = (16/5, 12/5)$, and the number of correct digits about doubles at each step.

**A change of one dimension.** Now the designer changes $\lvert AB \rvert$ from 5 to 5.5. Newton's method starts from the old solution, with residual 5.25, and reaches $x_B = 5.5$, $x_C = 149/44 \approx 3.38636$, $y_C \approx 2.12898$ in 4 steps (residuals 0.276, $8.5 \times 10^{-4}$, $2.1 \times 10^{-8}$, $2 \times 10^{-17}$). Both other sides keep their lengths, and $C$ moves to keep them.

**A start on the wrong side.** From the start $B = (4.6, 0)$, $C = (3, -0.5)$, the iteration converges to $C = (3.2, -2.4)$, the mirror image. Both shapes satisfy all three dimensions; the draft chose the side.

**A degenerate start.** The determinant of the Jacobian here is $8 x_B^2 y_C$. From any start with $C$ on the line $AB$, so $y_C = 0$, the Newton step is not defined, and the method cannot choose between the two sides. The equations are fine; only the start is degenerate.

**Missing and redundant dimensions.** Drop $\lvert BC \rvert = 3$: the Jacobian has 2 rows and rank 2 on 3 unknowns, and its null space at the solution is the rotation of $C$ about $A$, so the designer sees that $C$ is free on a circle. Add an angle of 90 degrees at $C$ to the three lengths: the four rows have rank 3 at the solution, and the angle is redundant for these values (since $3^2 + 4^2 = 5^2$) and in conflict for other values.

## Where it is used

- **Parametric sketchers.** The numerical solver of a sketcher, used alone in early systems and as the fallback for parts that do not decompose in later ones. See [feature-based modeling](/feature-based-modeling/).
- **Graph-constructive solvers.** A [DR-plan](/dr-plan/) solves its small rigid parts one at a time, and a part that is not ruler-and-compass constructible is solved numerically in the variational way.
- **Assemblies.** Assembly mates are solved by Newton-type methods on the poses of the parts; see [assembly constraint solving](/assembly-constraint-solving/).
- **Dragging.** When the user drags a point of an under-constrained sketch, the solver moves the free directions as little as possible, which is a least-squares version of the same solve.

## References
