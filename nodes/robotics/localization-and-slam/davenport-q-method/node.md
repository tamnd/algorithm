---
tag: 98191D
kind: algorithm
slug: davenport-q-method
name: Davenport's q-method
aliases:
- q-method
area: robotics/localization-and-slam
level: advanced
summary: Solves Wahba's problem as the eigenvector of the largest eigenvalue of a 4x4 symmetric matrix built from the observations.
solves: [wahba-problem]
model: real-ram
complexity:
  vars: {n: the number of vector pairs}
  time: {worst: O(n)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1968
  people: [Paul B. Davenport]
  note: Davenport wrote Wahba's loss as a quadratic form in the attitude quaternion, which turns the constrained minimization into an eigenvalue problem for a symmetric 4 by 4 matrix.
prereqs: [wahba-problem, unit-quaternion-rotation, symmetric-eigenproblem]
see_also: [quest-algorithm, triad-method, quaternion-superposition, kabsch-algorithm, jacobi-eigenvalue-algorithm, attitude-estimation, shepperd-method, lagrange-multiplier]
sources:
  - book: isbn:9781493908011
    title: "F. Landis Markley and John L. Crassidis, Fundamentals of Spacecraft Attitude Determination and Control, Springer, 2014"
    locator: "Chapter 5 (static attitude determination), the sections on Wahba's problem and Davenport's q-method"
  - paper: doi:10.1007/BF03546284
    title: "F. Landis Markley and Daniele Mortari, Quaternion attitude estimation using vector observations, Journal of the Astronautical Sciences 48(2-3), 2000, pages 359 to 380"
    locator: "the derivation of the q-method and its comparison with QUEST, the SVD method and other solutions"
  - paper: "Paul B. Davenport, A vector approach to the algebra of rotations with applications, NASA Technical Note D-4696, 1968"
    locator: "the report as a whole, which develops the quaternion algebra of rotations that the q-method uses"
  - paper: doi:10.1137/1007077
    title: "Grace Wahba, A least squares estimate of satellite attitude, SIAM Review 7(3), 1965, page 409"
    locator: "the problem that the q-method solves"
---

Davenport's q-method solves [Wahba's problem](/wahba-problem/) exactly. It writes the attitude as a unit quaternion $q$, shows that the Wahba loss is a constant minus the quadratic form $q^T K q$ for a symmetric $4 \times 4$ matrix $K$ built from the data, and so reduces the constrained least-squares problem to one [symmetric eigenproblem](/symmetric-eigenproblem/): the optimal quaternion is the eigenvector of the largest eigenvalue of $K$. The method is optimal for any number of weighted vector pairs and never returns a reflection. [QUEST](/quest-algorithm/) computes the same eigenvector faster, without a full eigensolver. [Quaternion superposition](/quaternion-superposition/), which fits two point sets in structural biology and vision, uses the same matrix construction under another name; this page covers the attitude form with directions, weights and the loss.

## In plain words

You have several directions measured on a vehicle and the same directions from a map, and you want the rotation that fits them best. Searching over all rotations directly is awkward, because a rotation is a constrained object. The q-method uses a trick. It describes the rotation by four numbers whose squares add up to one, and it packs all the measurements into a small table of four rows and four columns. The quality of the fit for any rotation is then a simple product of the four numbers with that table. A standard tool from linear algebra finds the four numbers that make this product largest. Those four numbers give the best rotation, and the leftover gives how bad the best fit still is.

## The problem

Given unit vectors $b_i$ (body frame) and $r_i$ (reference frame) and weights $a_i > 0$ for $i = 1, \ldots, n$, find the rotation $A \in SO(3)$ that minimizes $L(A) = \tfrac{1}{2} \sum_i a_i |b_i - A r_i|^2$. The output is the Hamilton quaternion $q = (q_0, q_1, q_2, q_3)$, scalar first, of $R_{sb} = A^T$, as on the [unit quaternion rotation](/unit-quaternion-rotation/) page, together with the minimum loss.

## The algorithm

```pseudo id=main
Q-METHOD(b_{1..n}, r_{1..n}, a_{1..n})     ▷ returns q of R_sb = A^T and the loss
L1  B ← Σ_i a_i b_i r_i^T ;  λ_0 ← Σ_i a_i
L2  σ ← tr B ;  S ← B + B^T ;  z ← (B_23 - B_32, B_31 - B_13, B_12 - B_21)
L3  K ← [[σ, z^T], [z, S - σ I]]                   ▷ symmetric 4 × 4, tr K = 0
L4  (λ_1..λ_4, q^(1)..q^(4)) ← eigenpairs of K       ▷ Jacobi sweeps
L5  j ← index of the largest λ_j
L6  q ← q^(j), negated if q_0 < 0
L7  return q, λ_0 - λ_j
```

Line L1 forms the attitude profile matrix; all data enter only through $B$ and $\lambda_0$. The vector $z$ of line L2 equals $\sum_i a_i \, b_i \times r_i$. Line L4 uses the cyclic [Jacobi eigenvalue algorithm](/jacobi-eigenvalue-algorithm/), which is accurate for small symmetric matrices; any symmetric eigensolver works. The sign choice of line L6 does not change the rotation, since $q$ and $-q$ give the same rotation. The attitude matrix is $A = R(q)^T$.

## Example

Use the data of the [Wahba's problem](/wahba-problem/) page: $r_1 = e_1$, $r_2 = e_2$, $a_1 = a_2 = 1$, $b_1 = (0, 0, 1)$ and $b_2 = (0.999391, 0, -0.034899)$, which is the true $b_2 = (1, 0, 0)$ tilted by $2$ degrees toward $b_1$.

- Line L1: $B = b_1 e_1^T + b_2 e_2^T$ has rows $(0, 0.999391, 0)$, $(0, 0, 0)$, $(1, -0.034899, 0)$, and $\lambda_0 = 2$.
- Line L2: $\sigma = 0$, $z = (0.034899, 1, 0.999391)$.
- Line L3:
$$K = \begin{pmatrix} 0 & 0.034899 & 1 & 0.999391 \\ 0.034899 & 0 & 0.999391 & 1 \\ 1 & 0.999391 & 0 & -0.034899 \\ 0.999391 & 1 & -0.034899 & 0 \end{pmatrix}.$$
- Line L4: the eigenvalues are $-1.9996954$, $-0.0349048$, $0.0349048$ and $1.9996954$; they sum to $0 = \operatorname{tr} K$.
- Lines L5 to L7: $q = (0.504344, 0.504344, 0.495618, 0.495618)$, and the loss is $2 - 1.9996954 = 3.0461 \times 10^{-4}$.

The true attitude has $q = (\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2})$, the rotation by $120$ degrees about $(1, 1, 1) / \sqrt{3}$. The estimate misses $b_1$ and $b_2$ by $1$ degree each. Its loss is half that of the [TRIAD method](/triad-method/), which matches $b_1$ exactly and misses $b_2$ by $2$ degrees.

With three exact axes, $b_1 = (0, 0, 1)$, $b_2 = (1, 0, 0)$, $b_3 = (0, 1, 0)$ for $r_k = e_k$, the matrix is $K = J - I$ with $J$ the all-ones matrix. Its eigenvalues are $3$ once and $-1$ three times, the top eigenvector is $(\tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2}, \tfrac{1}{2})$, and the loss is $3 - 3 = 0$.

## Correctness

For unit vectors the loss is $L(A) = \lambda_0 - \operatorname{tr}(A B^T)$. Writing $A$ by a unit quaternion, a direct expansion gives $\operatorname{tr}(A B^T) = q^T K q$. Every rotation has a unit quaternion, so minimizing $L$ over rotations is maximizing the Rayleigh quotient of $K$ over unit vectors, and by the spectral theorem the maximum is $\lambda_{\max}$, reached at its eigenvectors. So the q-method returns an optimal attitude with loss $\lambda_0 - \lambda_{\max}$, and the answer is unique when $\lambda_{\max}$ is simple. This is a theorem for unit vectors and positive weights; [the correctness proof](proofs/correctness.md) gives every step.

## Complexity

In the [real RAM](/real-ram/) model, line L1 costs $9 n$ multiply-adds and lines L2 and L3 cost $O(1)$. Line L4 works on a fixed $4 \times 4$ matrix. Each Jacobi sweep costs a fixed number of operations, and the code caps the sweeps at 50, so line L4 is $O(1)$; the cyclic Jacobi method converges quadratically in its last sweeps. The total is $O(n)$ time and $O(1)$ extra memory beyond the input. The constant is large next to that of TRIAD: a full $4 \times 4$ eigensolver does many more operations than a few cross products, and QUEST removes most of them.

## Properties

- **Optimal (theorem).** The output minimizes the Wahba loss over $SO(3)$.
- **Never a reflection.** Every unit quaternion gives a proper rotation, so no sign fix is needed, unlike the SVD method.
- **Any number of vectors.** Works for $n \ge 2$ non-parallel vectors with any positive weights; with exact data it recovers the true attitude.
- **Gives the loss for free.** $\lambda_0 - \lambda_{\max}$ is the minimum loss, a check of how well the data agree.
- **Uniqueness test.** If the two largest eigenvalues are equal, the data do not fix the attitude. The gap $\lambda_{\max} - \lambda_3$ measures how well it is fixed.
- **Traceless.** $\operatorname{tr} K = 0$, a cheap check of the construction.

## Variants and improvements

- **[QUEST](/quest-algorithm/).** Finds $\lambda_{\max}$ by Newton's method on the characteristic polynomial of $K$, starting from $\lambda_0$, and the eigenvector in closed form. Same answer, less work.
- **SVD method.** Maximizes $\operatorname{tr}(A B^T)$ with the SVD of $B$ (Markley, 1988). The [Kabsch algorithm](/kabsch-algorithm/) is the same idea for point sets.
- **Quaternion superposition.** The same matrix for two point sets with weights, used in structural biology; see [quaternion superposition](/quaternion-superposition/).
- **[Power iteration](/power-iteration/).** Since only the top eigenvector is needed, one can iterate on $K + c I$ with $c \ge \lambda_0$, so that all eigenvalues are nonnegative; every eigenvalue of $K$ lies in $[-\lambda_0, \lambda_0]$. It converges at the rate of the ratio of the two largest shifted eigenvalues, which can be slow (heuristic).

## When to use it

Use the q-method when you need the optimal attitude from any number of weighted directions and a robust symmetric eigensolver is available, which is the case on any modern computer. It is the reference against which faster methods are tested. When the cost of an eigensolver matters, or when the attitude is computed thousands of times a second, use QUEST. When there are exactly two directions and one is far better than the other, [TRIAD](/triad-method/) is simpler.

## Pitfalls

- **Convention of $z$.** With $A = R_{bs}$ and $q$ the quaternion of $R_{sb}$, $z = \sum a_i b_i \times r_i$. Other books use the quaternion of $A$ itself, which flips the sign of $z$ or of the vector part. Test the code on exact data.
- **Unnormalized input.** The identity $L = \lambda_0 - \operatorname{tr}(A B^T)$ needs unit vectors. With other lengths the optimal rotation is still the top eigenvector, but $\lambda_0 - \lambda_{\max}$ is no longer the loss.
- **Degenerate data.** With all $b_i$ parallel, $\lambda_{\max}$ is a double eigenvalue and any vector in its eigenspace is returned. The answer is then arbitrary in the rotation about that direction.
- **Quaternion sign.** $q$ and $-q$ are the same rotation. Fix a sign, for example $q_0 \ge 0$, before comparing with another estimate.

## Implementations

## History

Wahba posed the problem in 1965. The eigenvector solution is credited to Paul Davenport, and the method carries his name. Shuster and Oh (1981) designed QUEST to get the same answer without a full eigensolver. Markley and Mortari (2000) surveyed the q-method and its faster relatives. The same quaternion matrix was found independently for point-set registration, which is why it appears as [quaternion superposition](/quaternion-superposition/) in other fields.

## References
