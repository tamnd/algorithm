---
tag: BQJJ13
kind: problem
slug: loop-modeling
name: Loop modeling
aliases:
- Protein loop prediction
- Loop closure
area: biology/structure-prediction
level: advanced
summary: Build the backbone of a protein segment between two fixed anchor residues, so that the chain closes with ideal geometry and the loop is native-like. CCD and KIC solve the closure.
prereqs: [dihedral-angle, comparative-modeling]
see_also: [modeller, fragment-assembly, rosetta, ramachandran-plot, side-chain-packing, energy-function, protein-structure-prediction, gradient-descent]
sources:
  - paper: doi:10.1110/ps.0242703
    title: Adrian A. Canutescu and Roland L. Dunbrack Jr., Cyclic coordinate descent, a robotics algorithm for protein loop closure, Protein Science 12(5), 2003, 963-972
    locator: the CCD step, the closed form of the best rotation about one bond for the three atoms of the moving end
  - paper: doi:10.1002/jcc.10416
    title: Evangelos A. Coutsias, Chaok Seok, Matthew P. Jacobson and Ken A. Dill, A kinematic view of loop closure, Journal of Computational Chemistry 25(4), 2004, 510-528
    locator: the analytic closure of a chain with six free dihedral angles, through a polynomial of degree 16
  - paper: doi:10.1038/nmeth0809-551
    title: Daniel J. Mandell, Evangelos A. Coutsias and Tanja Kortemme, Sub-angstrom accuracy in protein loop reconstruction by robotics-inspired conformational sampling, Nature Methods 6(8), 2009, 551-552
    locator: kinematic closure (KIC) as a move for sampling loops in Rosetta
  - paper: doi:10.1110/ps.9.9.1753
    title: Andras Fiser, Richard Kinh Gian Do and Andrej Sali, Modeling of loops in protein structures, Protein Science 9(9), 2000, 1753-1773
    locator: loop modeling by optimization of a statistical potential, and the fall of accuracy with loop length
---

Loop modeling is the problem of building the backbone, and often the side chains, of a segment of a protein between two residues whose positions are fixed. It comes up in [comparative modeling](/comparative-modeling/), where insertions and deletions of the alignment leave gaps that the template cannot fill, and in design and docking, where a flexible loop must be rebuilt. The problem has two parts. The *closure* part is geometric: choose the dihedral angles of the loop so that the chain leaves the first anchor and arrives exactly at the second, with ideal bond lengths and angles. The *selection* part is physical: among the closed loops, find the one that is closest to the true structure, usually the one with the lowest energy.

## In plain words

Imagine a bicycle chain with both ends nailed to a board. The links can turn at their joints, but each link has a fixed length. Many shapes of the chain still connect the two nails, and we must find the right one.

In a protein, the loop is a short piece of backbone between two parts whose shape we already know. Each residue of the loop has two joints that can turn. We must set the joints so that the end of the loop meets the fixed part at the right place and at the right angle. Then, among all shapes that fit, we pick the one that fits best with the rest of the protein. The longer the loop, the more shapes there are, and the harder the choice.

## Definition

**Model.** The backbone is the chain of atoms N, $C_\alpha$, C of each residue. Bond lengths and bond angles are fixed at ideal values, and the peptide bond is planar and trans ($\omega = 180°$). The free variables are the [dihedral angles](/dihedral-angle/) $\phi_k$ (about N-$C_\alpha$) and $\psi_k$ (about $C_\alpha$-C) of the loop residues.

**Input.** A protein structure with residues $1, \ldots, i$ and $j, \ldots, n$ fixed, and the sequence of the loop residues $i + 1, \ldots, j - 1$.

**Closure.** Find dihedral angles of the loop such that the chain built from the fixed residue $i$ places the atoms N, $C_\alpha$, C of residue $j$ exactly on their fixed positions. Equivalently, the rigid frame of residue $j$ must match: three position constraints and three orientation constraints, six equations in all.

**Selection.** Among the closed loops, find one that minimizes an [energy function](/energy-function/) of the loop in the context of the fixed protein, or one close to the true loop. The quality is measured by the [RMSD](/rmsd/) of the loop backbone to the experimental structure, after the superposition of the fixed part.

## Variants

- **Closure only.** Given a loop that does not close, for example from a fragment database or from random angles, change it as little as possible so that it closes.
- **Loop prediction.** Find the native loop. Here closure is a constraint and the score decides.
- **Loop sampling.** Produce an ensemble of closed loops, for example for flexible docking or for the many states of a mobile loop.
- **Full-atom loops.** Include the side chains of the loop, which turns the selection into a joint problem with [side-chain packing](/side-chain-packing/).

## Examples

**A CCD trace in the plane.** Take a planar chain of three links of length 1, with the joints $P_0 = (0, 0)$, $P_1 = (1, 0)$, $P_2 = (2, 0)$ and the end $M = (3, 0)$. $P_0$ is fixed, and the target is $F = (1, 2)$, at distance $\sqrt{8} \approx 2.83$ from $M$. One CCD step at a joint $P$ turns everything after $P$ so that $M$ points from $P$ toward $F$, which is the best rotation about $P$ for one end point. Visit the joints from the end, $P_2$, $P_1$, $P_0$, and repeat:

| step | joint | rotation | new end $M$ | $\lvert M - F \rvert$ |
|---|---|---|---|---|
| 1 | $P_2$ | $+116.57°$ | $(1.553, 0.894)$ | 1.236 |
| 2 | $P_1$ | $+31.72°$ | $(1.000, 1.051)$ | 0.949 |
| 3 | $P_0$ | $+17.00°$ | $(0.649, 1.298)$ | 0.785 |
| 4 | $P_2$ | $-42.49°$ | $(1.074, 1.884)$ | 0.138 |
| 6 | $P_0$ | $+1.27°$ | $(0.955, 1.910)$ | 0.101 |

After the third sweep the error is $0.037$, after the fourth $0.014$, after the fifth $0.0057$ and after the sixth $0.0023$. The first steps make large gains and the later ones small gains, which is typical for CCD: fast at the start, slow near the end. Each step leaves the length of every link unchanged, so the chain stays valid at all times.

**Counting the degrees of freedom.** Closure fixes six numbers (the frame of residue $j$). A loop of $k$ residues has $2k$ free dihedral angles. A loop of three residues has six, so closure is a square system with a finite number of solutions in general, up to 16 (Coutsias et al. 2004). Longer loops have $2k - 6$ more angles than equations, so the closed loops form a family of dimension $2k - 6$, and the selection must search it.

**A non-example.** Consecutive $C_\alpha$ atoms are $3.8$ Å apart. If an alignment puts a loop of 3 residues between two anchors whose $C_\alpha$ atoms are 20 Å apart, no loop can close, because the chain from $C_\alpha$ of residue $i$ to $C_\alpha$ of residue $j = i + 4$ spans at most $4 \times 3.8 = 15.2$ Å. Such a gap points to an error in the alignment, not to a hard loop.

## Known algorithms

- **Database search.** Search a library of known structures for segments of the right length whose ends fit the anchor geometry, then rank them. This works for short loops, where the library covers the space.
- **Cyclic coordinate descent (CCD)** (Canutescu and Dunbrack 2003). Visit the rotatable bonds in turn and rotate the rest of the chain about each bond by the angle that brings the three atoms of the moving end closest to their targets. For a bond with axis $\hat n$ through a point $O$, moving atoms $M_l$ and targets $F_l$, let $r_l$ be the part of $M_l - O$ at right angles to the axis and $f_l = F_l - O$. Rotating by $\theta$ changes $\sum_l |F_l - M_l|^2$ by $-2(a \cos\theta + b \sin\theta)$ up to a constant, with $a = \sum_l f_l \cdot r_l$ and $b = \sum_l f_l \cdot (\hat n \times r_l)$, so the best angle is $\theta^* = \operatorname{atan2}(b, a)$. Each step costs $O(k)$ for a loop of $k$ residues. The implementation of this page uses this rule.
- **Kinematic closure (KIC)** (Coutsias et al. 2004). Pick six dihedral angles, set the others, and solve the closure equations for the six exactly, as the real roots of a polynomial of degree 16. Mandell, Coutsias and Kortemme (2009) used KIC as a sampling move in [Rosetta](/rosetta/) and rebuilt many loops of their benchmark to sub-angstrom accuracy.
- **Restraint optimization.** [MODELLER](/modeller/) builds loops by optimizing a statistical potential of the loop with conjugate gradients and molecular dynamics (Fiser, Do and Sali 2000).
- **Fragment insertion.** Rosetta and similar programs insert short fragments from known structures ([fragment assembly](/fragment-assembly/)) and close the chain with CCD or KIC after each move.

## Bounds

- **Closure is a square system for six angles.** With exactly six free dihedral angles, the closure equations reduce to one polynomial of degree 16 in one variable, so there are at most 16 solutions, and they can all be found by a polynomial root finder (Coutsias et al. 2004).
- **CCD never moves the end away.** The angle $\theta = 0$ is one candidate of each step, so the best angle is at least as good, and the deviation of the moving end never grows. There is no guarantee that it reaches zero: a CCD run can stall at a local minimum of the deviation, and the test of the implementation contains such a start.
- **No useful worst-case bound on selection.** The number of closed loops grows exponentially with the length of the loop, and the scores are approximate. Fiser, Do and Sali (2000) report that the accuracy of the predicted loops falls as the loops get longer. These are measured trends, not proved bounds.

## Reductions

- **To inverse kinematics.** Closure is the inverse kinematics problem of a serial robot arm with revolute joints, where the end effector must reach a given pose. CCD and KIC both come from robotics.
- **To nonlinear least squares.** Closure with more than six angles is the minimization of the deviation of the end, a nonlinear least squares problem in the dihedral angles. CCD is coordinate descent on it, which makes each one-dimensional step exact.
- **From comparative modeling.** Each insertion or deletion of a target-template alignment becomes one loop problem with fixed anchors.

## Applications

- **Comparative models.** Insertions and deletions of the alignment are rebuilt as loops, often the least accurate parts of the model.
- **Antibody modeling.** The third hypervariable loop of the heavy chain varies a lot in length and shape, and loop modeling is the main step of modeling it.
- **Design.** Designed proteins need loops that connect the secondary structure elements, and sampling closed loops is part of the design of new backbones.
- **Refinement of experimental models.** Missing or poorly resolved loops in crystal structures and cryo-EM maps are rebuilt by loop modeling.

## References
