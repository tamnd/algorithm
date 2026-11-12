---
tag: YXR4DQ
kind: definition
slug: rmsd
name: Root-mean-square deviation (RMSD)
aliases:
- Root-mean-square deviation
- Least RMSD
area: biology/structure-prediction
level: intro
summary: The square root of the mean squared distance between matched atoms of two structures, in Å, usually taken after the best rigid superposition.
prereqs: [euclidean-distance]
see_also: [optimal-superposition, kabsch-algorithm, quaternion-superposition, tm-score, gdt-ts, structure-alignment]
sources:
  - paper: doi:10.1107/S0567739476001873
    title: Wolfgang Kabsch, A solution for the best rotation to relate two sets of vectors, Acta Crystallographica A32(5), 1976, 922-923
    locator: the weighted sum of squared deviations that the best rotation minimizes
  - paper: doi:10.1110/ps.690101
    title: Oliviero Carugo and Sándor Pongor, A normalized root-mean-square distance for comparing protein three-dimensional structures, Protein Science 10(7), 2001, 1470-1473
    locator: the dependence of RMSD on the protein length and the normalized value RMSD100
  - paper: doi:10.1007/978-1-61779-588-6_10
    title: Irina Kufareva and Ruben Abagyan, Methods of protein structure comparison, in Homology Modeling, Methods in Molecular Biology, Humana Press, 2012, 231-257
    locator: the discussion of RMSD, its dependence on the superposition, and its sensitivity to outliers
  - paper: doi:10.1002/jcc.20110
    title: Evangelos A. Coutsias, Chaok Seok and Ken A. Dill, Using quaternions to calculate RMSD, Journal of Computational Chemistry 25(15), 2004, 1849-1857
    locator: the definition of the least RMSD over rotations and translations
---

The root-mean-square deviation (RMSD) of two structures with matched atoms is the square root of the mean of the squared distances between the matched atoms. In structural biology it is measured in ångström (Å) and usually means the least RMSD: the value after the second structure has been moved by the best rotation and translation, the [optimal superposition](/optimal-superposition/). An RMSD near 0 Å means the two structures are almost the same. The value depends on which atoms are matched and on the superposition, and it is not normalized for the size of the protein.

## Definition

**Model.** A structure is a list of points in $\mathbb{R}^3$, one for each atom, with coordinates in Å. Most protein comparisons use one point per residue, the $C_\alpha$ atom; a full-atom RMSD uses all heavy atoms. A correspondence pairs the point $x_i$ of one structure with the point $y_i$ of the other, for $i = 1, \ldots, N$.

**RMSD for a fixed position.** For two lists $X = (x_1, \ldots, x_N)$ and $Y = (y_1, \ldots, y_N)$ with $N \ge 1$,

$$\operatorname{RMSD}(X, Y) = \sqrt{\frac{1}{N} \sum_{i=1}^{N} |x_i - y_i|^2},$$

where $|x_i - y_i|$ is the [Euclidean distance](/euclidean-distance/). This is the Euclidean distance between $X$ and $Y$ as vectors of $\mathbb{R}^{3N}$, divided by $\sqrt N$.

**Least RMSD.** The least RMSD minimizes over the proper rigid motions, the rotations $R \in SO(3)$ and the translations $t \in \mathbb{R}^3$:

$$\operatorname{RMSD}_{\min}(X, Y) = \min_{R \in SO(3),\ t \in \mathbb{R}^3} \sqrt{\frac{1}{N} \sum_{i=1}^{N} |R x_i + t - y_i|^2}.$$

Reflections are not allowed, because a mirror image of a protein has the other handedness and is a different molecule. The [Kabsch algorithm](/kabsch-algorithm/) and the [quaternion method](/quaternion-superposition/) compute the minimum exactly in $\Theta(N)$ time.

**Weighted RMSD.** With weights $w_i > 0$, replace $\frac{1}{N}\sum$ with $\sum w_i |\cdot|^2 / \sum w_i$, for example to weigh atoms by mass.

## Examples and non-examples

Take $x = (0,0,0), (2,0,0), (0,3,0), (0,0,4)$ and $y = (1,2,3), (1,4,3), (-2,2,3), (1,2,7)$, which is $x$ turned by $90°$ about the $z$ axis and moved by $(1,2,3)$.

| comparison | RMSD |
|---|---|
| as given, no motion | $\sqrt{68/4} = 4.1231$ Å |
| centroids matched, no rotation | $\sqrt{19.5/4} = 2.2079$ Å |
| least RMSD, best rotation and translation | $0$ Å |
| least RMSD with $y_2$ and $y_3$ matched the wrong way | $1.4245$ Å |
| least RMSD to the mirror image of $x$ | $1.2674$ Å |

The first three rows show that the number depends on the superposition: the shape is the same in each row. The fourth row shows that it depends on the correspondence: the same two point sets, matched in another way, no longer fit. The last row is the cost of the ban on reflections.

**One bad atom.** Move only $y_4$ by 10 Å. The least RMSD goes from 0 to $3.4352$ Å, because the squares give large deviations a large weight, and the best fit spreads the error over all atoms.

**Size.** Let one of $N$ atoms be 5 Å off and all others exact, with no motion. The RMSD is $5/\sqrt N$: 1.58 Å for $N = 10$, 0.5 Å for $N = 100$ and 0.16 Å for $N = 1000$. The same local error looks smaller in a larger protein. On the other side, two unrelated large proteins have a larger RMSD than two unrelated small ones, so a raw value has no fixed meaning across lengths.

**Non-examples.**

- Two structures of different lengths have no RMSD until a correspondence is fixed. Finding one is the [structure alignment](/structure-alignment/) problem.
- The RMSD over a set of atoms that an aligner selected because they fit well is not comparable with the RMSD over all atoms. An aligner can lower the RMSD by dropping atoms.
- An RMSD after a fit that allows reflections, as in plain orthogonal Procrustes, is not the least RMSD defined here.

## Related definitions

- **A metric on shapes.** For a fixed correspondence, $\operatorname{RMSD}_{\min}$ is symmetric, is 0 exactly when one structure is a proper rigid motion of the other, and obeys the triangle inequality, because the rigid motions act on $\mathbb{R}^{3N}$ by isometries. So it is a metric on the classes of structures up to rigid motion.
- **[TM-score](/tm-score/)** and **[GDT-TS](/gdt-ts/)** count the residues within a distance cutoff instead of averaging squares. They depend less on a few bad regions and on the length.
- **RMSD100.** Carugo and Pongor (2001) divide the RMSD by $1 + \ln\sqrt{N/100}$, which scales it to the value expected for a protein of 100 residues.
- **dRMSD.** The distance RMSD compares the internal distance matrices, $\sqrt{\frac{2}{N(N-1)}\sum_{i<j}(|x_i - x_j| - |y_i - y_j|)^2}$. It needs no superposition, and it does not tell a structure from its mirror image.

## References
