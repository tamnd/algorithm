---
tag: M9M4MB
kind: concept
slug: dihedral-angle
name: Dihedral (torsion) angle
aliases:
- Phi and psi angles
- Torsion angle
area: biology/structure-prediction
level: intro
summary: The angle of rotation about the middle bond of four atoms in a chain. The backbone of a protein has three per residue (phi, psi, omega), and omega is near 180 degrees.
prereqs: [cross-product, dot-product]
see_also: [ramachandran-plot, protein-secondary-structure, rotamer, rmsd, protein-structure-prediction, point-and-vector]
sources:
  - paper: doi:10.1021/bi00820a001
    title: IUPAC-IUB Commission on Biochemical Nomenclature, Abbreviations and symbols for the description of the conformation of polypeptide chains, tentative rules (1969), Biochemistry 9(18), 1970, pages 3471 to 3479
    locator: the definition of the torsion angle, its sign, the zero at the cis position, and the names phi, psi, omega and chi for the backbone and side chain angles
  - book: isbn:9780815323051
    title: Carl Branden and John Tooze, Introduction to Protein Structure, second edition, Garland, 1999
    locator: Chapter 1 (the planar peptide unit and the phi and psi angles of the backbone)
  - paper: "Jerod Parsons, J. Bradley Holmes, J. Maurice Rojas, Jerry Tsai and Charlie E. M. Strauss, Practical conversion from torsion space to Cartesian space for in silico protein synthesis, Journal of Computational Chemistry 26(10), 2005, pages 1063 to 1068"
    title: Parsons et al. 2005, the natural extension reference frame (NeRF)
    locator: the placement of a fourth atom from a bond length, a bond angle and a torsion angle
---

A dihedral angle, or torsion angle, of four points $p_0, p_1, p_2, p_3$ is the angle between the plane through $p_0, p_1, p_2$ and the plane through $p_1, p_2, p_3$, with a sign that says which way the rotation about the middle bond $p_1 p_2$ goes. In a protein the backbone of each residue has three of them: $\phi$, $\psi$ and $\omega$. Bond lengths and bond angles in a protein are nearly fixed, so the dihedral angles are the real degrees of freedom of the chain, and a list of them describes the backbone shape. The angle is computed from the [cross products](/cross-product/) of the bond vectors with one call of atan2.

## In plain words

Hold a pen in each hand and join the two pens with a short rod between your fists. Look along the rod. The two pens point in some directions across your view, and the angle between them as you see it is the dihedral angle. Turning one fist about the rod changes the angle, and nothing else changes: the rod keeps its length and each pen keeps its angle to the rod.

A protein backbone is a long chain of such joints. The lengths and the bend at each joint barely change, but the chain can turn about most of its bonds. So the shape of the backbone is mostly a list of turn angles. Two of these turns for each amino acid are free; the third sits in a stiff flat group and is almost always the same.

## The idea

### Definition

Let $p_0, p_1, p_2, p_3$ be points in space such that neither $p_0, p_1, p_2$ nor $p_1, p_2, p_3$ lie on one line. Put

$$b_1 = p_1 - p_0, \quad b_2 = p_2 - p_1, \quad b_3 = p_3 - p_2, \qquad n_1 = b_1 \times b_2, \quad n_2 = b_2 \times b_3.$$

The vectors $n_1$ and $n_2$ are normal to the two planes. The dihedral angle is

$$\theta = \operatorname{atan2}\big(\lVert b_2 \rVert \, b_1 \cdot n_2, \; n_1 \cdot n_2\big),$$

in the range $(-180°, 180°]$. The second argument is $\lVert n_1 \rVert \lVert n_2 \rVert \cos\theta$. The first is $\lVert n_1 \rVert \lVert n_2 \rVert \sin\theta$, because $(n_1 \times n_2) \cdot b_2 = \lVert b_2 \rVert^2 \, b_1 \cdot n_2$ by the vector triple product. The common factor $\lVert n_1 \rVert \lVert n_2 \rVert$ is positive, so atan2 returns $\theta$ itself. A formula with $\arccos$ of the normalized dot product gives only $\lvert \theta \rvert$, and it loses precision near $0°$ and $180°$; atan2 has neither problem.

### Sign and zero

The IUPAC-IUB rules of 1970 fix the convention. Look along the middle bond from $p_1$ to $p_2$. The angle is positive when the near bond $p_1 p_0$ must turn clockwise to cover the far bond $p_2 p_3$, and negative when it must turn counterclockwise. The angle is $0°$ when $p_0$ and $p_3$ are on the same side (cis, or eclipsed), and $180°$ when they are on opposite sides (trans). The same angle comes out when the four points are given in the reverse order. A mirror image changes the sign, so the sign carries the handedness of the chain.

### The backbone angles

The backbone of residue $i$ is the atoms $N_i$, $C_{\alpha,i}$ and $C_i$. Its three dihedral angles are

- $\phi_i$: the angle $C_{i-1}, N_i, C_{\alpha,i}, C_i$, a rotation about the bond N to $C_\alpha$;
- $\psi_i$: the angle $N_i, C_{\alpha,i}, C_i, N_{i+1}$, a rotation about the bond $C_\alpha$ to C;
- $\omega_i$: the angle $C_{\alpha,i}, C_i, N_{i+1}, C_{\alpha,i+1}$, a rotation about the peptide bond.

The first residue has no $\phi$, and the last has no $\psi$ and no $\omega$. The peptide bond C to N has partial double bond character, so the six atoms around it lie in one plane and $\omega$ is near $180°$ (trans) for almost all peptide bonds. The cis form, $\omega$ near $0°$, is rare, and most cis bonds come before a proline. So each residue has two free backbone angles, $\phi$ and $\psi$. Side chains have their own dihedral angles $\chi_1, \chi_2, \ldots$, and their preferred values define the [rotamers](/rotamer/).

### From angles back to atoms

The inverse map builds a chain from its internal coordinates. Given three placed atoms $a, b, c$, a bond length $L$, a bond angle $\beta$ at $c$ and a dihedral $\tau$, the natural extension reference frame (NeRF) puts the next atom at

$$d = c + L\big(-\cos\beta \, \hat{e}_1 + \sin\beta \cos\tau \, \hat{e}_2 + \sin\beta \sin\tau \, \hat{e}_3\big),$$

with $\hat{e}_1$ the unit vector from $b$ to $c$, $\hat{e}_3$ the unit normal of the plane $a, b, c$ in the direction of $(b - a) \times \hat{e}_1$, and $\hat{e}_2 = \hat{e}_3 \times \hat{e}_1$. One call costs $O(1)$, so a chain of $n$ residues is built in $O(n)$ time. Measuring all $3n$ angles of a chain also takes $O(n)$ time. Errors add up along the chain: a small error in one angle moves every atom after it, and the movement grows with the distance from the joint.

## Examples

**Four points in a known position.** Take $p_0 = (0, 1, 0)$, $p_1 = (0, 0, 0)$, $p_2 = (1, 0, 0)$ and $p_3 = (1, 0.5, 0.866)$, so that $p_3$ is $p_0$ turned by $60°$ about the $x$ axis. Then $b_1 = (0, -1, 0)$, $b_2 = (1, 0, 0)$ and $b_3 = (0, 0.5, 0.866)$. The normals are $n_1 = (0, 0, 1)$ and $n_2 = (0, -0.866, 0.5)$. So $\lVert b_2 \rVert \, b_1 \cdot n_2 = 0.866$ and $n_1 \cdot n_2 = 0.5$, and $\operatorname{atan2}(0.866, 0.5) = 60°$. Seen along the $x$ axis, $p_0$ points along $+y$ and $p_3$ is turned toward $+z$, which is clockwise for a viewer who looks along $+x$. With $p_3 = (1, 0.5, -0.866)$ the angle is $-60°$.

**A real backbone.** The table gives the first atoms of a chain built with $\phi = -57°$, $\psi = -47°$ and $\omega = 180°$, with bond lengths N to $C_\alpha$ 1.458 Å, $C_\alpha$ to C 1.525 Å and C to N 1.329 Å and bond angles 111.2°, 116.2° and 121.7°. The coordinates are in Å, rounded to three places.

| atom | x | y | z |
|---|---|---|---|
| $N_1$ | 0.000 | 0.000 | 0.000 |
| $C_{\alpha,1}$ | 1.458 | 0.000 | 0.000 |
| $C_1$ | 2.009 | 1.422 | 0.000 |
| $N_2$ | 1.463 | 2.263 | -0.872 |
| $C_{\alpha,2}$ | 1.899 | 3.650 | -0.974 |
| $C_2$ | 1.768 | 4.370 | 0.364 |

For $\phi_2$ the four atoms are $C_1, N_2, C_{\alpha,2}, C_2$. The formula gives $\lVert b_2 \rVert \, b_1 \cdot n_2 = -2.864$ and $n_1 \cdot n_2 = 1.859$, so $\phi_2 = \operatorname{atan2}(-2.864, 1.859) = -57.0°$. The same rounded coordinates give $\psi_1 = -47.0°$ (atoms $N_1, C_{\alpha,1}, C_1, N_2$) and $\omega_1 = -179.98°$ (atoms $C_{\alpha,1}, C_1, N_2, C_{\alpha,2}$), which is trans: $-179.98°$ and $180°$ differ by only $0.02°$.

**Degenerate input.** If $p_0, p_1, p_2$ lie on one line, then $n_1 = 0$, both arguments of atan2 are 0, and the angle is not defined. A program must reject this case, not return 0.

## Where it is used

- **Describing and checking backbones.** The pair $(\phi, \psi)$ of each residue is a point on the [Ramachandran plot](/ramachandran-plot/), and the regions of the plot match the [secondary structure](/protein-secondary-structure/) states. Validation tools flag residues whose pair is in a forbidden region.
- **Structure prediction and design.** Many methods of [protein structure prediction](/protein-structure-prediction/) and [fragment assembly](/fragment-assembly/) move in torsion space: they change $\phi$ and $\psi$ and rebuild the atoms with NeRF, so bond lengths and angles stay ideal. Side chain packing chooses $\chi$ angles from rotamer libraries.
- **Comparing structures.** Angle lists do not change under rotation and translation, so they compare two backbones without a superposition. They are local, though: a small change in many angles can move the far end a long way, so [RMSD](/rmsd/) after superposition is used for global comparison.
- **Force fields.** Torsion terms in an [energy function](/energy-function/) are periodic functions of dihedral angles.

Angles are periodic, so $-179°$ and $179°$ are $2°$ apart. Means and differences must be taken on the circle, for example by averaging the unit vectors $(\cos\theta, \sin\theta)$, not the raw numbers.

## References
