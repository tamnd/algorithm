---
tag: JWNAWS
kind: problem
slug: optimal-superposition
name: Optimal superposition of point sets
aliases:
- Least-RMSD superposition
- Rigid-body superposition
area: biology/structure-prediction
level: core
summary: Given two lists of matched 3D points, find the rotation and translation that move the first onto the second with the least RMSD; reflections are not allowed.
prereqs: [rmsd, vector-rotation]
see_also: [kabsch-algorithm, quaternion-superposition, singular-value-decomposition, symmetric-eigenproblem, structure-alignment, tm-score, gdt-ts, least-squares-problem]
sources:
  - paper: doi:10.1107/S0567739476001873
    title: Wolfgang Kabsch, A solution for the best rotation to relate two sets of vectors, Acta Crystallographica A32(5), 1976, 922-923
    locator: the statement of the problem and its solution
  - paper: doi:10.1107/S0567739478001680
    title: Wolfgang Kabsch, A discussion of the solution for the best rotation to relate two sets of vectors, Acta Crystallographica A34(5), 1978, 827-828
    locator: the case of a negative determinant and the exclusion of reflections
  - paper: doi:10.1364/JOSAA.4.000629
    title: Berthold K. P. Horn, Closed-form solution of absolute orientation using unit quaternions, Journal of the Optical Society of America A 4(4), 1987, 629-642
    locator: the proof that the optimal translation matches the centroids, and the quaternion solution for the rotation and the scale
  - paper: doi:10.1109/34.88573
    title: Shinji Umeyama, Least-squares estimation of transformation parameters between two point patterns, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(4), 1991, 376-380
    locator: the solution in any dimension, with the sign correction and the optimal scale
  - paper: doi:10.1109/TPAMI.1987.4767965
    title: K. S. Arun, T. S. Huang and S. D. Blostein, Least-squares fitting of two 3-D point sets, IEEE Transactions on Pattern Analysis and Machine Intelligence PAMI-9(5), 1987, 698-700
    locator: the SVD solution and the case where it gives a reflection
  - paper: doi:10.1007/BF02289451
    title: Peter H. Schönemann, A generalized solution of the orthogonal Procrustes problem, Psychometrika 31(1), 1966, 1-10
    locator: the orthogonal Procrustes problem, where reflections are allowed
---

The optimal superposition problem asks for the rigid motion that best fits one list of points onto a second list with the same number of points, where the $i$-th point of one list is matched to the $i$-th point of the other. Best means least [RMSD](/rmsd/). The motion is a rotation and a translation; a reflection is not allowed. The problem is the inner step of almost every comparison of protein structures. It has an exact solution in $\Theta(N)$ time for $N$ pairs, by the [Kabsch algorithm](/kabsch-algorithm/) or the [quaternion method](/quaternion-superposition/), and the best translation always moves the centroid of the first list onto the centroid of the second.

## In plain words

You have two copies of the same object, and you know which point of one copy belongs to which point of the other. You may pick up the first copy, turn it in any way and put it down anywhere. You may not turn it inside out, as a mirror would. The goal is to put it down so that the partner points are as close as possible, measured by the average of the squared gaps.

The answer comes in two parts. The place is easy: put the center of the first copy on the center of the second copy. The turn is the real question, and it has an exact answer that a small matrix computation gives. No trial and error is needed.

## Definition

**Model.** The points are in $\mathbb{R}^3$, with coordinates in Å. For proteins they are usually the $C_\alpha$ atoms of the matched residues, or all heavy atoms of matched residues. The arithmetic is exact real arithmetic in the [real RAM](/real-ram/), with square roots.

**Input.** $X = (x_1, \ldots, x_N)$ and $Y = (y_1, \ldots, y_N)$ with $x_i, y_i \in \mathbb{R}^3$ and $N \ge 1$.

**Output.** A rotation $R \in SO(3) = \{R \in \mathbb{R}^{3 \times 3} : R^{\mathsf T} R = I,\ \det R = +1\}$ and a translation $t \in \mathbb{R}^3$ that minimize

$$E(R, t) = \sum_{i=1}^{N} |R x_i + t - y_i|^2 .$$

The least RMSD is $\sqrt{E(R, t)/N}$. The condition $\det R = +1$ excludes reflections, which have $\det R = -1$. Without it the problem is the orthogonal Procrustes problem, and its answer for proteins can be the mirror image, a molecule with the other handedness.

**The best translation matches the centroids.** Let $\bar x = \frac1N \sum x_i$ and $\bar y = \frac1N \sum y_i$, and $a_i = x_i - \bar x$, $b_i = y_i - \bar y$. For each fixed $R$, the unique best $t$ is $t = \bar y - R \bar x$.

*Proof.* Let $c = R\bar x + t - \bar y$. Then $R x_i + t - y_i = (R a_i - b_i) + c$, and

$$E(R, t) = \sum_i |R a_i - b_i|^2 + 2\, c \cdot \sum_i (R a_i - b_i) + N |c|^2 .$$

The middle sum is $R \sum_i a_i - \sum_i b_i = 0$, because the centered points sum to 0. So $E(R, t) = \sum_i |R a_i - b_i|^2 + N|c|^2$. The first term does not depend on $t$, and the second is 0 exactly when $c = 0$, that is $t = \bar y - R\bar x$. $\square$

**What is left for the rotation.** Since $R$ keeps lengths, $|R a_i - b_i|^2 = |a_i|^2 + |b_i|^2 - 2 b_i^{\mathsf T} R a_i$, so

$$\min_t E(R, t) = G_A + G_B - 2 \operatorname{tr}(R H), \qquad G_A = \sum_i |a_i|^2,\ G_B = \sum_i |b_i|^2,\ H = \sum_i a_i b_i^{\mathsf T}.$$

The problem is therefore to maximize the linear function $\operatorname{tr}(RH)$ over $SO(3)$. The answer depends on the data only through the $3 \times 3$ matrix $H$ and the two numbers $G_A$, $G_B$.

## Variants

- **Weights.** Minimize $\sum w_i |R x_i + t - y_i|^2$ with $w_i > 0$. The best $t$ matches the weighted centroids, and $H = \sum w_i a_i b_i^{\mathsf T}$.
- **Reflections allowed.** Minimize over all orthogonal $R$. This is the orthogonal Procrustes problem of Schönemann (1966). The answer is $V U^{\mathsf T}$ for the SVD $H = U S V^{\mathsf T}$.
- **Scale.** Minimize over $c R x_i + t$ with $c > 0$. Umeyama (1991) and Horn (1987) give the closed form; the best $c$ is $\operatorname{tr}(RH)/G_A$ at the best $R$.
- **Other dimensions.** The same problem in $\mathbb{R}^d$ has the same solution with $\operatorname{diag}(1, \ldots, 1, d)$, by Umeyama (1991).
- **Many structures.** Fit $K$ structures to a common mean. A standard heuristic alternates between fitting each structure to the mean and recomputing the mean.
- **Unknown correspondence.** If the matching is not given, the problem becomes [structure alignment](/structure-alignment/), which is much harder.
- **Other objectives.** [GDT-TS](/gdt-ts/) and the [TM-score](/tm-score/) maximize the number or a weighted count of points within a cutoff, not the sum of squares. These objectives have no closed form, and the tools use heuristic searches.

## Examples

Let $x = (0,0,0), (2,0,0), (0,3,0), (0,0,4)$, with centroid $\bar x = (0.5, 0.75, 1)$ and $G_A = 21.75$.

**A rotated copy.** Let $y_i = R_z x_i + (1, 2, 3)$, with $R_z$ the turn by $90°$ about the $z$ axis. Then $\bar y = (0.25, 2.5, 4)$ and the best motion is $R = R_z$, $t = \bar y - R_z \bar x = (1, 2, 3)$, with $E = 0$.

**A mirror image.** Let $y_i$ be $x_i$ with $z$ changed to $-z$. The best orthogonal matrix is the mirror $\operatorname{diag}(1, 1, -1)$, with $E = 0$, but it is not a rotation. The best rotation has $\operatorname{tr}(RH) = 18.5372$, so $E = 43.5 - 2 \cdot 18.5372 = 6.4256$ and the least RMSD is $\sqrt{6.4256/4} = 1.2674$ Å. The [Kabsch algorithm](/kabsch-algorithm/) page computes it step by step.

**One point.** For $N = 1$, each rotation is optimal, with $t = y_1 - R x_1$ and $E = 0$.

**Points on a line.** If all $x_i$ lie on one line, each turn about that line leaves $E$ unchanged, so the optimal $R$ is not unique.

## Known algorithms

| algorithm | method | time | notes |
|---|---|---|---|
| [Kabsch algorithm](/kabsch-algorithm/) | SVD of $H$, sign fix $\operatorname{diag}(1, 1, d)$ | $\Theta(N)$ | Kabsch 1976 and 1978; also Arun, Huang and Blostein 1987 |
| [Quaternion method](/quaternion-superposition/) | top eigenvector of a $4 \times 4$ symmetric matrix | $\Theta(N)$ | Horn 1987, Kearsley 1989; proper by construction |
| QCP | Newton's method on the characteristic polynomial of the $4 \times 4$ matrix | $\Theta(N)$ | Theobald 2005; fastest when only the RMSD is needed |
| Umeyama's method | SVD with sign fix and scale | $\Theta(N)$ | any dimension |

All four are exact. The $N$-dependent work is the same in each, the sums that give $\bar x$, $\bar y$, $G_A$, $G_B$ and $H$; they differ in the constant-size step that follows.

## Bounds

The worst case time is $\Theta(N)$. The upper bound comes from the algorithms above. The lower bound holds because each coordinate can change the answer: if an algorithm does not read some $y_i$, an adversary can move that point and change the least RMSD. The extra space is $\Theta(1)$, since the five sums can be accumulated in one pass.

## Reductions

- **To a $3 \times 3$ SVD.** The rotation step is $\max_{R \in SO(3)} \operatorname{tr}(RH)$, and its value is $s_1 + s_2 + \operatorname{sign}(\det H)\, s_3$ for the [singular values](/singular-value-decomposition/) $s_1 \ge s_2 \ge s_3$ of $H$.
- **To a $4 \times 4$ symmetric eigenproblem.** With $R$ written as a unit quaternion $q$, $\operatorname{tr}(RH) = q^{\mathsf T} N q$ for a symmetric $N$ built from $H$, and the maximum is its top [eigenvalue](/eigenvalue/).
- **As a subroutine.** Structure alignment methods such as TM-align, the final step of [combinatorial extension](/combinatorial-extension/), and point-cloud registration in vision alternate between a correspondence step and an optimal superposition step.

## Applications

- **Model quality.** The RMSD between a predicted model and the native structure, after the best fit, is a standard measure, next to [GDT-TS](/gdt-ts/) and the [TM-score](/tm-score/).
- **Simulations.** Molecular dynamics frames are fitted to a reference to remove the overall motion, and the RMSD of the fitted frames tracks how the structure changes.
- **Structure comparison.** Aligners such as [DALI](/dali/) and [CE](/combinatorial-extension/) report the RMSD of the aligned residues after the best fit.
- **Crystallography.** Kabsch published the problem and its solution in Acta Crystallographica, for the comparison of crystal structures.

## References
