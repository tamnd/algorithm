---
tag: 3MK9DJ
kind: problem
slug: wahba-problem
name: Wahba's problem
aliases:
- optimal attitude from vector observations
area: robotics/localization-and-slam
level: core
summary: "Find the rotation that best maps a set of reference unit vectors to their measured body frame directions in weighted least squares."
prereqs: [special-orthogonal-group, least-squares-problem]
see_also: [triad-method, davenport-q-method, quest-algorithm, attitude-estimation, kabsch-algorithm, quaternion-superposition, optimal-superposition, singular-value-decomposition]
sources:
  - paper: doi:10.1137/1007077
    title: "Grace Wahba, A least squares estimate of satellite attitude, SIAM Review 7(3), 1965, page 409"
    locator: "the problem statement (Problem 65-1)"
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 5 (static attitude determination methods)"
  - paper: doi:10.1007/BF03546284
    title: "F. Landis Markley and Daniele Mortari, Quaternion attitude estimation using vector observations, Journal of the Astronautical Sciences 48(2-3), 2000, pages 359 to 380"
    locator: "the survey of solutions of Wahba's problem: the q-method, QUEST, the SVD method and the faster methods"
  - paper: "F. Landis Markley, Attitude determination using vector observations and the singular value decomposition, Journal of the Astronautical Sciences 36(3), 1988, pages 245 to 258"
    locator: "the solution of Wahba's problem from the singular value decomposition of the attitude profile matrix"
---

Wahba's problem asks for the rotation that best explains a set of direction measurements. A spacecraft or a robot knows some directions in a reference frame, for example the direction to the Sun and the local magnetic field from a model, and it measures the same directions in its own body frame. The rotation from the reference frame to the body frame is its attitude. With noise, no rotation matches all pairs, so Wahba (1965) asked for the rotation with the least weighted sum of squared errors. The problem has an exact solution as an eigenvector of a $4 \times 4$ matrix ([Davenport's q-method](/davenport-q-method/)) or from a singular value decomposition, and a fast iterative one ([QUEST](/quest-algorithm/)). The rotation step of [optimal superposition](/optimal-superposition/) in structural biology is the same problem with vectors that are not unit: the [Kabsch algorithm](/kabsch-algorithm/) and [quaternion superposition](/quaternion-superposition/) solve it there, and this page links them rather than repeating them.

## In plain words

You stand in a field at night and see two known stars. You know where those stars are on a sky map, and you see where they are relative to your own head. From this you can work out which way you are facing. With perfect eyes, two stars are enough and the answer is exact. Real sensors are noisy, so the directions you see do not fit any single way of facing. Wahba's problem asks for the way of facing that fits all the seen directions best, with more trust given to the better sensors. "Best" means that the sum of the squared misses is as small as possible. The problem looks hard because a rotation is a constrained object, but it has a clean exact answer.

## Definition

**Data.** Unit vectors $r_1, \ldots, r_n$ in the reference frame, unit vectors $b_1, \ldots, b_n$ in the body frame, and weights $a_i > 0$. The model is $b_i = A r_i + \text{noise}$, where the attitude matrix $A$ is in the [special orthogonal group](/special-orthogonal-group/) $SO(3)$. In the notation of rigid-body motion, $A = R_{bs} = R_{sb}^T$.

**Task.** Find

$$A^\star = \arg\min_{A \in SO(3)} L(A), \qquad L(A) = \tfrac{1}{2} \sum_{i=1}^n a_i \, |b_i - A r_i|^2 .$$

**The gain form.** For unit vectors, $|b_i - A r_i|^2 = 2 - 2 b_i^T A r_i$. With $\lambda_0 = \sum_i a_i$ and the attitude profile matrix $B = \sum_i a_i b_i r_i^T$,

$$L(A) = \lambda_0 - \operatorname{tr}(A B^T),$$

so the problem is to maximize the linear function $\operatorname{tr}(A B^T)$ over $SO(3)$. All the data enter through the $3 \times 3$ matrix $B$. This identity holds exactly; it is the first step of every known solution.

**Constraint.** $A$ must be a rotation, not only an orthogonal matrix. Without the condition $\det A = 1$, the answer can be a reflection, which no rigid body can perform.

## Variants

- **Two vectors, one exact.** The [TRIAD method](/triad-method/) uses exactly two pairs and matches the first one exactly. It does not minimize $L$.
- **Non-unit vectors.** If the $b_i$ and $r_i$ have any lengths, the loss is still a constant minus $\operatorname{tr}(A B^T)$ with the same $B$, so every solution below still applies. This is the centered form of [optimal superposition](/optimal-superposition/).
- **Weights from noise.** Shuster and Oh (1981) chose $a_i$ as the inverse variance of a sensor noise that is small and symmetric about the true direction. Then $A^\star$ is a maximum likelihood estimate, and the inverse of the Hessian of $L$ at $A^\star$ is the covariance of the attitude error.
- **Dynamic.** When the body turns between measurements and a gyro is available, the static problem becomes a filtering problem; see [attitude estimation](/attitude-estimation/).

## Examples

**Exact data.** Let $r_1 = e_1$, $r_2 = e_2$ with $a_1 = a_2 = 1$, and let the true $R_{sb}$ be the rotation by $120$ degrees about $(1, 1, 1) / \sqrt{3}$, the matrix with rows $(0, 0, 1)$, $(1, 0, 0)$, $(0, 1, 0)$. Then $A = R_{sb}^T$ has rows $(0, 1, 0)$, $(0, 0, 1)$, $(1, 0, 0)$, so $b_1 = (0, 0, 1)$ and $b_2 = (1, 0, 0)$. Every method recovers this $A$, and the minimum loss is $0$.

**Two noisy vectors.** Keep $b_1 = (0, 0, 1)$ but tilt $b_2$ by $2$ degrees toward $b_1$: $b_2 = (\cos 2^\circ, 0, -\sin 2^\circ) = (0.999391, 0, -0.034899)$. Now the measured angle between the two directions is $88$ degrees, while the reference angle is $90$ degrees, so no rotation fits both. TRIAD with $b_1$ first fits $b_1$ exactly and misses $b_2$ by $2$ degrees, at loss $\tfrac{1}{2} (2 \sin 1^\circ)^2 = 6.0917 \times 10^{-4}$. The optimal rotation misses each vector by $1$ degree, at loss $(2 \sin 0.5^\circ)^2 = 3.0461 \times 10^{-4}$, half the loss of TRIAD. The [q-method page](/davenport-q-method/) computes this answer step by step.

**No unique answer.** If all $b_i$ are parallel, every rotation about that direction fits equally well, and the minimizer is a whole circle of rotations.

## Known algorithms

- **[TRIAD method](/triad-method/).** Two pairs only, closed form, $O(1)$. Exact for noise-free data, not optimal with noise.
- **[Davenport's q-method](/davenport-q-method/).** The optimal attitude is the unit quaternion that is the eigenvector of the largest eigenvalue of a symmetric $4 \times 4$ matrix $K$ built from $B$. $O(n)$ to build $B$, then one $4 \times 4$ symmetric eigenproblem.
- **[QUEST](/quest-algorithm/).** Finds the largest eigenvalue of $K$ by Newton's method on its characteristic polynomial, starting from $\lambda_0$, and the eigenvector from a closed-form adjugate column. $O(n)$ plus a few Newton steps.
- **SVD method.** With the [singular value decomposition](/singular-value-decomposition/) $B = U S V^T$, the optimum is $A^\star = U \operatorname{diag}(1, 1, \det U \det V) V^T$ (Markley, 1988). The [Kabsch algorithm](/kabsch-algorithm/) is the same formula for point sets.
- **Faster closed forms.** FOAM and ESOQ avoid the eigensolver with other closed forms; Markley and Mortari (2000) compare them with QUEST for speed and robustness.

## Bounds

- **Exact recovery (theorem).** If the data are exact, $b_i = A_0 r_i$, and at least two $r_i$ are not parallel, then $A^\star = A_0$ is the unique minimizer and $L(A^\star) = 0$. Proof: $L \ge 0$ and $L(A_0) = 0$, and a rotation that fixes two independent directions is the identity.
- **Range of the loss (theorem).** $0 \le L(A^\star) = \lambda_0 - \lambda_{\max} \le \lambda_0$, where $\lambda_{\max}$ is the largest eigenvalue of $K$; see the proof on the [q-method page](/davenport-q-method/).
- **Uniqueness (theorem).** The minimizer is unique if and only if $\lambda_{\max}$ is a simple eigenvalue of $K$. If $B$ has rank at most $1$, as when all $b_i$ are parallel, the minimizer is not unique.
- **Cost.** Any algorithm must read all $n$ pairs, so $\Omega(n)$ time. The q-method, QUEST and the SVD method reach $O(n)$, because after $B$ is formed the remaining work is on a matrix of fixed size.

## Reductions

- **To a linear objective.** Wahba's problem is equivalent to maximizing $\operatorname{tr}(A B^T)$ over $SO(3)$; only $B$ matters.
- **To a symmetric eigenproblem.** With $A$ written by a unit quaternion $q$, $\operatorname{tr}(A B^T) = q^T K q$, a quadratic form, so the problem becomes the [symmetric eigenproblem](/symmetric-eigenproblem/) for the largest eigenvalue of $K$. This is the q-method.
- **To an SVD.** Maximizing $\operatorname{tr}(A B^T)$ over rotations is solved by the SVD of $B$, with a sign fix that turns a reflection into a rotation.
- **From optimal superposition.** After both point sets are centered, the rotation of least RMSD solves Wahba's problem with $b_i$ and $r_i$ the centered points and all weights $1$. So the algorithms of one field solve the other.

## Applications

- Spacecraft attitude from star trackers, Sun sensors and magnetometers, where Wahba's problem was first posed.
- The attitude of a drone or a phone from gravity and the magnetic field when it is not accelerating, often as the measurement step inside a filter.
- Registration of point sets in computer vision and structural biology, by the reduction from superposition.

## References
