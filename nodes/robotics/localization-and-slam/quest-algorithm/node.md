---
tag: Z02XZG
kind: algorithm
slug: quest-algorithm
name: QUEST algorithm
aliases:
- quaternion estimator
area: robotics/localization-and-slam
level: advanced
summary: Shuster's fast solution of Wahba's problem that finds the largest eigenvalue of Davenport's matrix by Newton iteration on its characteristic polynomial.
solves: [wahba-problem]
model: real-ram
complexity:
  vars: {n: the number of vector pairs, k: the number of Newton steps}
  time: {worst: O(n + k)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [Malcolm D. Shuster, S. D. Oh]
  note: Shuster and Oh found the largest eigenvalue of Davenport's matrix by Newton's method from the sum of the weights and the eigenvector in closed form, which made the optimal attitude cheap enough for the spacecraft computers of the time.
prereqs: [davenport-q-method, characteristic-polynomial, newton-raphson-method]
see_also: [wahba-problem, triad-method, attitude-estimation, quaternion-superposition, unit-quaternion-rotation, shepperd-method, eigenvalue-problem]
sources:
  - paper: doi:10.2514/3.19717
    title: "M. D. Shuster and S. D. Oh, Three-axis attitude determination from vector observations, Journal of Guidance and Control 4(1), 1981, pages 70 to 77"
    locator: "the QUEST algorithm: the characteristic equation, the Newton iteration from the sum of the weights, the closed-form eigenvector and the method of sequential rotations"
  - paper: doi:10.1007/BF03546284
    title: "F. Landis Markley and Daniele Mortari, Quaternion attitude estimation using vector observations, Journal of the Astronautical Sciences 48(2-3), 2000, pages 359 to 380"
    locator: "the sections on QUEST and on the speed and robustness of the solutions of Wahba's problem"
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 5 (static attitude determination), the section on QUEST"
---

QUEST, the quaternion estimator, computes the optimal attitude of [Wahba's problem](/wahba-problem/), the same answer as [Davenport's q-method](/davenport-q-method/), but without a general eigensolver. It finds the largest eigenvalue of Davenport's $4 \times 4$ matrix $K$ by [Newton's method](/newton-raphson-method/) on the [characteristic polynomial](/characteristic-polynomial/), starting from the sum of the weights, which is already very close. It then reads the eigenvector off a closed-form column of the adjugate of $\lambda I - K$. When the attitude is near a rotation by $\pi$, that column vanishes, and QUEST rotates the reference frame by $\pi$ about a coordinate axis and solves again. [Quaternion superposition](/quaternion-superposition/) in other fields solves the same eigenproblem; the Newton start at the sum of the weights is what makes QUEST fast for attitude data.

## In plain words

The q-method finds the best rotation by asking a general linear algebra tool for the largest special number of a four by four table, and its matching direction. That tool is slow for a small flight computer. QUEST notices two things. First, when the measurements fit well, that largest number is very close to the sum of the sensor weights, so a few steps of a classic root-finding method from that start finish the job. Second, once the number is known, the matching direction has a ready-made formula, with no search. The formula breaks down only for rotations close to a half turn. For those, QUEST turns the map frame by a half turn first, solves the easy case, and turns the answer back.

## The problem

As for the q-method: given unit vectors $b_i$ and $r_i$ with weights $a_i > 0$, find the rotation $A = R_{bs}$ that minimizes $\tfrac{1}{2} \sum_i a_i |b_i - A r_i|^2$, and return the Hamilton quaternion $q$ of $R_{sb} = A^T$ and the minimum loss. With $B = \sum_i a_i b_i r_i^T$, $\sigma = \operatorname{tr} B$, $S = B + B^T$ and $z = \sum_i a_i \, b_i \times r_i$, the answer is the top eigenvector of $K = \begin{pmatrix} \sigma & z^T \\ z & S - \sigma I \end{pmatrix}$, and the loss is $\lambda_0 - \lambda_{\max}$ with $\lambda_0 = \sum_i a_i$.

## The algorithm

Let $\kappa = \operatorname{tr} \operatorname{adj} S$ and $\Delta = \det S$. The characteristic polynomial of $K$ is

$$\psi(\lambda) = \lambda^4 - (a + b) \lambda^2 - c \lambda + (a b + c \sigma - d),$$

with $a = \sigma^2 - \kappa$, $b = \sigma^2 + z^T z$, $c = \Delta + z^T S z$ and $d = z^T S^2 z$. Let $P_k$ be the rotation by $\pi$ about the axis $e_k$, and $P_{\text{none}} = I$.

```pseudo id=main
QUEST(b_{1..n}, r_{1..n}, a_{1..n})        ▷ returns q of R_sb = A^T and the loss
L1  B ← Σ_i a_i b_i r_i^T ;  λ_0 ← Σ_i a_i
L2  compute σ, S, z, κ, Δ from B, then the coefficients of ψ
L3  λ ← λ_0
L4  repeat λ ← λ - ψ(λ) / ψ'(λ) until the step is ≤ tol · λ_0
L5  for k in (none, x, y, z) do  B_k ← B P_k ; recompute σ, S, z, κ, Δ from B_k
L6      α ← λ² - σ² + κ ;  β ← λ - σ ;  γ ← (λ + σ) α - Δ ;  x ← (α I + β S + S²) z
L7      if |(γ, x)| ≥ ½ |ψ'(λ)| then leave the loop
L8  q ← (0, e_k) ⊗ (γ, x) / |(γ, x)|, negated if q_0 < 0   ▷ (0, e_none) means 1
L9  return q, λ_0 - λ
```

Line L4 is Newton's method; the code uses $\text{tol} = 10^{-15}$ and at most 50 steps. In exact arithmetic every step from $\lambda_0$ is positive, so the code also stops, without moving, at the first step that is not positive: in floating point the last iterates can swing by one unit of roundoff around the root. Line L6 is the first column of $\operatorname{adj}(\lambda I - K)$, which at $\lambda_{\max}$ equals $\psi'(\lambda_{\max}) \, q_0 \, q$, so its norm is $|\psi'(\lambda)| \, |q_0|$. Line L7 accepts a frame in which $|q_0| \ge \tfrac{1}{2}$. Such a frame exists, because turning the reference vectors by $\pi$ about $e_k$ moves $|q_k|$ into the scalar place, and one of the four components of a unit quaternion has absolute value at least $\tfrac{1}{2}$. The polynomial $\psi$ and $\lambda_{\max}$ are the same in every frame. If no frame passes the test because of rounding, the code keeps the frame with the longest column.

## Example

Use the noisy data of the [q-method](/davenport-q-method/) page: $r_1 = e_1$, $r_2 = e_2$, unit weights, $b_1 = (0, 0, 1)$ and $b_2 = (0.999391, 0, -0.034899)$.

- Lines L1 and L2: $\sigma = 0$, $\lambda_0 = 2$, and $\psi(\lambda) = \lambda^4 - 4 \lambda^2 + 0.0048719$, with $c = 0$.
- Lines L3 and L4: the Newton iterates are $2$, $1.9996955063$, $1.9996953903128$, $1.9996953903127825$. Three steps reach the last digit, because $\lambda_0$ is only $3 \times 10^{-4}$ above $\lambda_{\max}$.
- Line L6 in the unrotated frame: $(\gamma, x) = (4.0667, 4.0667, 3.9963, 3.9963)$ and $\psi'(\lambda) = 15.9878$. The norm is $8.0633 \ge \tfrac{1}{2} \cdot 15.9878$, so line L7 accepts the frame.
- Line L8: $q = (0.504344, 0.504344, 0.495618, 0.495618)$, the same as the q-method, and line L9 returns the loss $3.0461 \times 10^{-4}$. The ratio $8.0633 / 15.9878 = 0.50434$ is $q_0$, as the formula says.

For a case that needs a rotated frame, let the true $R_{sb}$ be the rotation by $\pi$ about $e_3$, with the same two reference vectors and exact data. Its quaternion is $(0, 0, 0, 1)$, so $q_0 = 0$ and the unrotated column is zero up to rounding. The frames $x$ and $y$ also have a zero scalar part, since $q_1 = q_2 = 0$. The frame $z$ has $|q_0'| = |q_3| = 1$, passes the test, and line L8 returns $q = (0, 0, 0, 1)$.

## Correctness

Three facts make QUEST correct; each is a theorem when $\lambda_{\max}$ is a simple eigenvalue and the arithmetic is exact. First, $\psi$ is the characteristic polynomial of $K$, and $(\gamma, x)$ is the first column of $\operatorname{adj}(\lambda I - K)$, by the Cayley-Hamilton theorem for $S$ and a Schur complement. Second, $K$ is symmetric, so $\psi$ has only real roots and is increasing and convex to the right of $\lambda_{\max}$; since $\lambda_0 \ge \lambda_{\max}$, Newton's method from $\lambda_0$ decreases monotonically to $\lambda_{\max}$. Third, the adjugate at a simple eigenvalue is $\psi'(\lambda_{\max}) \, q q^T$, so the column is a multiple of $q$, and the frame rule keeps the multiple away from zero. The q-method proof then shows that $q$ is optimal. The full argument is in [the correctness proof](proofs/correctness.md).

## Complexity

In the [real RAM](/real-ram/) model, line L1 costs $O(n)$. Lines L2 to L8 work on fixed $3 \times 3$ and $4 \times 4$ objects: each Newton step evaluates a quartic and its derivative, and each frame costs a few $3 \times 3$ products. So the time is $O(n + k)$ for $k$ Newton steps, and the extra memory is $O(1)$. Measured over 1000 random problems of 2 to 6 vectors for each noise level, counting the last step that triggers the stop: $k \le 4$ at a noise of $0.01$ rad, $k \le 7$ at $0.05$ rad, and $k \le 10$ at $0.5$ rad. Newton converges quadratically at a simple root, so $k$ grows like the logarithm of the number of correct digits wanted.

## Properties

- **Optimal (theorem).** Same answer as the q-method, up to rounding.
- **Monotone Newton (theorem).** The iterates never go below $\lambda_{\max}$ and never increase, so no safeguard is needed.
- **Few steps (measurement).** With good data, $\lambda_0 - \lambda_{\max}$ is the small minimum loss, so the start is already close; the example needed 3 steps for full precision.
- **Robust near $\pi$.** The sequential rotations keep $|q_0| \ge \tfrac{1}{2}$ in the frame used, which bounds the loss of accuracy in line L8 by a factor of about 2.
- **Gives the loss.** $\lambda_0 - \lambda$ is the minimum loss.

## Variants and improvements

- **No Newton step (heuristic).** Using $\lambda = \lambda_0$ in line L6 skips line L4. The error this causes is small when the data fit well, since then $\lambda_0 - \lambda_{\max}$ is small, but it is not optimal.
- **Covariance.** With weights equal to inverse sensor variances, Shuster and Oh (1981) also give the covariance of the attitude error from the same quantities.
- **Other fast methods.** FOAM and ESOQ compute the same optimal attitude from other closed forms; Markley and Mortari (2000) compare their speed and robustness with QUEST.
- **Recursive use.** In [attitude estimation](/attitude-estimation/), QUEST can run at each step on new measurements, or its output can serve as the measurement of a filter.

## When to use it

Use QUEST when the optimal attitude from several vector observations must be computed fast and often, as on a star tracker or in a loop that runs at a high rate. Use the q-method with a full eigensolver when the data may be degenerate or when the second eigenvalue is also wanted, and [TRIAD](/triad-method/) when there are exactly two vectors and optimality does not matter.

## Pitfalls

- **Rotations near $\pi$.** Without the sequential rotations, the column of line L6 is the difference of large nearly equal terms, and the computed quaternion can point anywhere. The test of line L7 must use $\psi'(\lambda)$; a fixed threshold on the norm depends on the scale of the weights.
- **Double eigenvalue.** If $\lambda_{\max}$ is not simple, Newton converges slowly and the adjugate is zero in every frame. The data do not fix the attitude, and QUEST cannot tell which solution to return.
- **Stopping rule.** Stop on the size of the Newton step relative to $\lambda_0$, not on $|\psi(\lambda)|$, and also stop on a step that is not positive. Near a root, $\psi$ is computed with cancellation. A first version of the code used only $|\text{step}| \le 10^{-15} \lambda_0$; with a noise of $0.2$ rad it swung forever between two neighbors of the root and hit the step limit.
- **Conventions.** QUEST returns the quaternion of $R_{sb}$ with the conventions of the q-method page; a sign error in $z$ gives the inverse rotation.

## Implementations

## History

Shuster and Oh (1981) introduced QUEST in a paper on three-axis attitude determination that also analyzed the [TRIAD method](/triad-method/). Their goal was the optimal answer of Wahba's problem at a cost close to that of TRIAD, by replacing the general eigensolver of Davenport's q-method with a Newton iteration and a closed-form eigenvector. The method of sequential rotations, in the same paper, handles the attitudes near a rotation by $\pi$. Markley and Mortari (2000) later compared QUEST with the other fast solutions of Wahba's problem.

## References
