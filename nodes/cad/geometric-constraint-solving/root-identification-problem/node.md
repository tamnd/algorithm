---
tag: JDQ34Y
kind: problem
slug: root-identification-problem
name: Root identification problem
aliases:
- chirality problem
- solution selection problem
area: cad/geometric-constraint-solving
level: advanced
summary: A well-constrained sketch has exponentially many solutions, and the solver must pick the one the user meant, usually by keeping orientations of the draft.
prereqs: [constructive-constraint-solving, well-constrained-system]
see_also: [geometric-constraint-problem, fudos-hoffmann-reduction, orientation-test, circle-circle-intersection, kabsch-algorithm, simulation-of-simplicity, partition-problem, dr-plan]
sources:
  - paper: doi:10.1145/248210.248223
    title: Ioannis Fudos and Christoph M. Hoffmann, A graph-constructive approach to solving systems of geometric constraints, ACM Transactions on Graphics 16(2), 179 to 216, 1997
    locator: Section 2.2, multiple solutions and root identification, with the orientation rules and the statement that the selection of a root by extra constraints is hard
  - paper: "William Bouma, Ioannis Fudos, Christoph M. Hoffmann, Jiazhen Cai and Robert Paige, Geometric constraint solver, Computer-Aided Design 27(6), 1995"
    locator: the selection of the intended solution from the sketch, and the statement that one simple extra requirement makes the selection NP-complete (general locator)
  - paper: "Caroline Essert-Villard, Pascal Schreck and Jean-François Dufourd, Sketch-based pruning of a solution space within a formal geometric constraint solver, Artificial Intelligence 124(1), 139 to 159, 2000"
    locator: the tree of solutions of a construction plan and its pruning by the sketch (general locator)
  - paper: "Robert Joan-Arinyo, María Victoria Luzón and Antoni Soto-Riera, Genetic algorithms for root multiselection in constructive geometric constraint solving, Computers and Graphics 27(1), 51 to 60, 2003"
    locator: the search over the choices of a construction plan with a genetic algorithm, and the experiments (general locator)
  - paper: "James B. Saxe, Embeddability of weighted graphs in k-space is strongly NP-hard, Proceedings of the 17th Allerton Conference on Communication, Control and Computing, 480 to 489, 1979"
    locator: the reduction from PARTITION to distances on a line
  - book: isbn:9781498738910
    title: Meera Sitharam, Audrey St. John and Jessica Sidman (editors), Handbook of Geometric Constraint Systems Principles, Chapman and Hall/CRC, 2018
    locator: the chapters on the solution of decomposed systems and the choice among their solutions (general locator)
---

A [well-constrained](/well-constrained-system/) sketch has a finite number of solutions, but the number is not one. A [constructive solver](/constructive-constraint-solving/) builds the shape with $n - 2$ ruler and compass steps for $n$ points, and each step places a point on one of the two intersections of two circles, so the system can have $2^{n-2}$ shapes that satisfy every constraint. The equations cannot tell which one the user meant. The root identification problem is to select that one. The usual answer keeps the orientation of each construction triangle as it is in the draft, which is exact and fast when the draft branch is real. When the user changes a value so much that this branch has no real solution, no rule is known that is both fast and proved to give the shape the user expects.

## In plain words

You draw a rough shape and give it exact dimensions. The program builds the exact shape one triangle at a time. Each triangle can open to the left or to the right, and both choices satisfy your dimensions. With many triangles there are very many shapes, and most of them look nothing like your drawing: parts fold over, cross each other or turn into their mirror image.

The program must give you the shape you meant. The simple rule is to copy, for each triangle, the side it opens to in your drawing. That rule gives one shape and is easy to compute. But after a large change of a dimension, that shape can stop existing, and then the program must guess which other shape is nearest to what you want.

## Definition

**Input.** A [well-constrained system](/well-constrained-system/) of $n$ points in the plane with distance constraints, its values, and a *construction plan*: a list of $n - 2$ merges, where merge $k$ places a point $r_k$ from two points $p_k, q_k$ that are already placed, as the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) or [Owen's decomposition](/owen-triconnected-decomposition/) finds it. Often there is also a draft $\hat x : V \to \mathbb{R}^2$, the sketch that the user drew.

**The choices.** For a placement $x$, the sign of merge $k$ is
$$ \sigma_k(x) = \operatorname{sign} \det\big(x(q_k) - x(p_k),\ x(r_k) - x(p_k)\big), $$
the result of the [orientation test](/orientation-test/) on the merge triangle. A real solution in which no merge triangle is flat has a *sign vector* $\sigma(x) \in \{+1, -1\}^{n-2}$, and each sign vector gives at most one solution up to proper rigid motion. So the solutions are the leaves of a binary tree of depth $n - 2$, and a leaf is missing when one of its circle pairs does not meet.

**Output.** One real solution, the one the user meant. This is not a mathematical property of the system, so the problem has several formal versions.

- **Given signs.** Given $\sigma \in \{+1, -1\}^{n-2}$, return the solution with $\sigma(x) = \sigma$, or report that it has no real solution.
- **Draft signs.** The same with $\sigma = \sigma(\hat x)$, the signs of the draft.
- **Nearest solution.** Among the real solutions, return one that keeps the most signs of the draft, or one that is nearest to the draft after the best proper rigid motion.
- **Extra conditions.** Return a solution that also meets conditions outside the system: one more distance, a sign of a triangle that is not in the plan, or an inequality, or report that none does.

**The variant on this page.** Points and distances in the plane, with a triangle-decomposable system and its plan, up to proper rigid motion. Angles and incidences of lines add choices of the same kind, such as the side of a line on which a point lies.

**Exact signs.** The draft sign is the [orientation test](/orientation-test/) on three draft points. For nearly collinear points the determinant is a small difference of large products, and in floating point [catastrophic cancellation](/catastrophic-cancellation/) can give the wrong sign. The solver then builds the mirror triangle and the user sees a part fold over. Take the sign exactly: with integer or rational coordinates in exact arithmetic, or with a filtered predicate in the style of [Shewchuk](/shewchuk-expansion-sum/), as in [exact geometric computation](/exact-geometric-computation/).

**Degenerate drafts and flat triangles.** A draft with three collinear points of a merge gives the sign 0, and the draft does not say which side the user meant. The solver can use a fixed rule, such as a symbolic perturbation by [simulation of simplicity](/simulation-of-simplicity/), which always picks the same side, or it can ask the user. On the side of the new values, the test whether a merge triangle with squared sides $a^2, b^2, c^2$ exists is the sign of $16 A^2 = 2(a^2 b^2 + b^2 c^2 + c^2 a^2) - a^4 - b^4 - c^4$, which is exact when the squared lengths are rational. The value 0 is a flat triangle: its two roots coincide, and a small change of a value can make them real and distinct or complex.

## Variants

- **Chirality.** A solution and its mirror image have opposite sign vectors. The two are congruent, but a proper motion cannot map one to the other, so a CAD system counts them as two shapes and must keep the hand of the draft. Up to all rigid motions, mirror images included, a triangle-decomposable system has at most $2^{n-3}$ solutions.
- **Decomposed systems that are not triangle-decomposable.** A [DR-plan](/dr-plan/) solves each rigid part with its own method, and each part has its own finite set of solutions. The choice is then a choice of one solution per part, and the parts that are solved by numerical methods have no sign vector to copy.
- **Assemblies.** In [assembly constraint solving](/assembly-constraint-solving/) a mate of two faces can be aligned or opposed, and a rotation about an axis can have two solutions. These are root choices of the same kind in three dimensions.
- **Tracking an edit.** The user changes one value from $c$ to $c'$, and the intended solution is the one that the old solution moves to when the value changes continuously. This version is well defined only while no merge triangle becomes flat on the way.
- **All roots.** Some systems show the user all the real solutions, or let the user flip one merge at a time. The number of leaves makes a full list possible only for small sketches.

## Examples

**The draft signs give the draft.** Take the six points of the example in the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/): the constraints $01, 02, 12, 34, 35, 45, 03, 04, 15$, and the draft $(0, 0)$, $(6, 0)$, $(3, -4)$, $(-1, 5)$, $(3, 6)$, $(7, 4)$ for the points 0 to 5. The plan has four merges, with the triangles $(p, q, r) = (0, 4, 3)$, $(3, 4, 5)$, $(0, 5, 1)$ and $(0, 1, 2)$. On the integer draft the four determinants are exactly $21$, $-12$, $-24$ and $-24$, so the draft signs are $(+, -, -, -)$. With the lengths measured on the draft, these signs give the draft back, moved by a proper motion. Of the $2^4 = 16$ sign vectors, 8 give real solutions.

**A change that kills the draft branch.** Now the user changes $\lvert 15 \rvert$ from $\sqrt{17} \approx 4.12$ to $15$ and keeps the other values. Merges 1 and 2 do not use the bar $15$, so with the draft signs the points $0, 3, 4, 5$ form the draft shape, and merge 3 needs a triangle with the squared sides $\lvert 50 \rvert^2 = 65$, $\lvert 01 \rvert^2 = 36$ and $\lvert 15 \rvert^2 = 225$. Here $\sqrt{65} < 15 - 6$, since $65 < 81$, and the exact test $16 A^2 = 2(65 \cdot 36 + 36 \cdot 225 + 225 \cdot 65) - 65^2 - 36^2 - 225^2 = -6016 < 0$ shows that the triangle does not exist. So the draft signs give no real solution.

If merge 1 or merge 2 flips, the points 0 and 5 fall on opposite sides of the line 34, and the measured side becomes $\lvert 50 \rvert^2 = 2113/17 \approx 124.3$. This lies between $81$ and $(15 + 6)^2 = 441$, so merge 3 works. The 8 sign vectors in which exactly one of merges 1 and 2 flips are now the real ones, and the 8 others, the draft signs among them, fail. Every real solution changes at least one sign of the draft.

**Two rules that do not agree.** Two real solutions change only one sign: $(+, +, -, -)$, which flips merge 2, and $(-, -, -, -)$, which flips merge 1. They are different shapes, so the rule "keep the most draft signs" has a tie. Measure each solution by the sum of squared distances to the draft after the best proper rigid motion, as the [Kabsch algorithm](/kabsch-algorithm/) computes it. The first one has about $74.8$ and the second about $125.6$, but $(+, +, -, +)$, which changes two signs, has about $78.9$. So the rule of fewest sign changes and the rule of least distance rank the solutions in different orders, and neither rule is the user's intent.

**Tracking fails too.** If $\lvert 15 \rvert$ grows continuously from $\sqrt{17}$, the draft branch exists until $\lvert 15 \rvert = 6 + \sqrt{65} \approx 14.06$. There the triangle $0, 5, 1$ is flat, with 0 on the segment from 1 to 5, and after that the two roots of merge 3 are complex. A continuous path from the old solution to a real solution for the value $15$ does not exist, so the tracking version has no answer either, and the solver must ask the user or choose by a rule.

## Known algorithms

- **Follow the given signs.** The construction phase of the [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) runs the plan once and, at each merge, takes the [circle-circle intersection](/circle-circle-intersection/) on the side that the sign asks for. It is proved to return the solution with that sign vector, or to stop at the first merge whose circles do not meet. Its cost is linear in the size of the plan, with one square root per merge.
- **Copy the draft.** The same with the signs of the draft, the rule of Bouma, Fudos and Hoffmann. For lines and angles, the rules also keep the side of a point with respect to a line and the direction in which an angle turns. It is proved to give the draft back when the values are those of the draft and no merge triangle of the draft is flat. When the draft branch is real after an edit, it returns that branch; when it is not, the rule gives no answer.
- **Browse and prune the tree.** Essert-Villard, Schreck and Dufourd walk the tree of $2^{n-2}$ leaves and cut the branches whose shapes do not look like the sketch, then let the user browse what is left. The walk is exponential in the worst case, and the quality of the pruning is only measured.
- **Search over sign vectors.** Joan-Arinyo, Luzón and Soto-Riera search the sign vectors with a [genetic algorithm](/genetic-algorithm/), with a fitness that measures the extra conditions or the likeness to the draft. Later papers by Luzón and her coauthors use other evolutionary methods. These methods give no guarantee to find a solution that exists.
- **Newton's method from the draft.** [Variational geometry](/variational-geometry/) does not choose a branch at all: [Newton's method](/newton-method-for-systems/) converges to the solution in whose basin the draft lies, which is often but not always the intended one.
- **Continuation.** [Homotopy continuation](/homotopy-continuation/) from the old values to the new ones follows the old solution, and is proved to stay on its branch while no merge triangle becomes flat. At a flat triangle it stops, as in the example.

## Bounds

**Proved.**

- **The number of roots.** A triangle-decomposable system of $n$ points has at most $2^{n-2}$ solutions up to proper motion in which no two shared points of a merge coincide, one per sign vector. A strip of triangles reaches $2^{n-2}$ real solutions for generic lengths, as the page on the [geometric constraint problem](/geometric-constraint-problem/) shows. For a general [Laman graph](/laman-theorem/) the bound is $\binom{2n-4}{n-2}$ complex solutions, by Borcea and Streinu.
- **Given signs are easy.** For a given sign vector, the solution is unique up to proper motion and is computed in linear time from the plan, as above. So the versions "given signs" and "draft signs" are solved exactly.
- **Branches change only at flat triangles.** While the values move along a path on which every merge triangle has positive area, the two roots of each circle pair move continuously and stay apart, so each solution moves continuously and keeps its sign vector. A solution can change its branch only when a merge triangle becomes flat, where two roots meet.
- **Extra conditions are hard on a line.** On a line, place the points of a path one by one with $x_{i+1} = x_i \pm a_i$. Each point has two choices, as in a merge. The question whether some choice also meets the extra condition $x_k = x_0$ is the [partition problem](/partition-problem/) for $a_0, \ldots, a_{k-1}$, which is NP-complete. This is Saxe's reduction.
- **Extra conditions are hard in the plane.** Bouma, Fudos and Hoffmann state that one simple requirement added to the choice of signs makes the selection NP-complete, and Fudos and Hoffmann (1997, Section 2.2) cite the result of Fudos for the selection of a root by extra constraints. The exact form of the added requirement is in those sources.

**What is only measured.** No theorem defines the solution that the user meant, so no algorithm is proved to find it. That the draft signs give the intended shape for small edits, that the shapes the pruning keeps are the ones users want, and how often the evolutionary searches find a good solution, all come from experience with CAD systems and from the test sets in the papers. Whether the nearest-solution versions are NP-hard, for the rule of fewest sign changes or for the rule of least distance, is not settled by the sources on this page.

## Reductions

- **From [partition](/partition-problem/).** The path on a line with the extra condition $x_k = x_0$ is a partition instance, as above, so the version with extra conditions is NP-hard already in one dimension.
- **To a search over $\{+1, -1\}^{n-2}$.** Each version is a search over sign vectors with a test per vector that costs one run of the plan. The extra-condition version is a [constraint satisfaction problem](/constraint-satisfaction-problem/) with one Boolean variable per merge, and the nearest-solution versions are optimization problems over the same set.
- **To polynomial systems with sign conditions.** The intended solution is a real point of the constraint equations at which given determinants have given signs. This is a question in the existential theory of the reals, which the methods of [cylindrical algebraic decomposition](/cylindrical-algebraic-decomposition/) decide for small systems.

## Applications

- **Parametric sketches.** Each time a user edits a dimension, the sketcher must keep the shape from flipping into a branch that the user did not ask for.
- **Assemblies.** The choice between an aligned and an opposed mate, and between two positions of a part on a circle, is root identification in space.
- **Linkages and robots.** The assembly modes of a linkage, such as the solutions of the [forward kinematics of the Stewart-Gough platform](/stewart-gough-forward-kinematics/), are roots of the same kind, and the controller must stay on the branch in which the machine was built.
- **Molecules.** Chirality in chemistry is the same choice: a molecule and its mirror image satisfy the same distances, and only one of them is the molecule that was measured.

## References
