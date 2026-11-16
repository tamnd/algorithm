---
tag: 25FNCG
kind: algorithm
slug: se3-exponential-map
name: "Exponential map of SE(3)"
aliases:
- exponential coordinates of rigid motion
area: robotics/rigid-body-motion
level: core
summary: "Turns a screw axis S and a distance theta into the rigid motion exp([S] theta) in closed form: Rodrigues' formula for the rotation and a matrix G(theta) for the translation."
model: real-ram
complexity:
  vars: {n: "the size of the matrix, fixed at n = 4"}
  time: {worst: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1984
  people: [Roger W. Brockett]
  note: Brockett wrote the kinematics of robot arms as products of exponentials of twists, which made this map a standard tool in robotics.
prereqs: [rigid-body-twist, rodrigues-rotation-formula, matrix-exponential]
see_also: [product-of-exponentials-formula, screw-motion, chasles-theorem, so3-logarithm-map, adjoint-map-se3, forward-kinematics, pose-graph-optimization, uncertainty-on-lie-groups]
sources:
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 3, Section 3.3.3 (exponential coordinates of rigid-body motions, the closed form of the exponential and the matrix logarithm of a rigid-body motion)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 2, Section 3.2 (exponential coordinates for rigid motion and twists); the book writes a twist with the linear part first
  - paper: doi:10.1007/BFb0031048
    title: Roger W. Brockett, Robotic manipulators and the product of exponentials formula, Mathematical Theory of Networks and Systems, Lecture Notes in Control and Information Sciences 58, Springer, 1984, 120-129
    locator: the whole paper (forward kinematics as a product of exponentials of twists)
  - paper: arxiv:1812.01537
    title: Joan Sola, Jeremie Deray and Dinesh Atchuthan, A micro Lie theory for state estimation in robotics, 2018
    locator: the exponential and logarithm maps of SE(3) in the examples of the paper
---

The exponential map of SE(3) takes a twist, a 6-vector that describes a velocity of a rigid body, and returns the rigid motion that the body makes when it keeps this velocity for one unit of time.
The result is a 4 by 4 [homogeneous transformation matrix](/homogeneous-transformation-matrix/) in the [special Euclidean group](/special-euclidean-group/) SE(3).
It is the [matrix exponential](/matrix-exponential/) of a $4 \times 4$ matrix of a special form, and that form gives a closed formula with one sine and one cosine, with no series and no general matrix routine.
The rotation part is [Rodrigues' formula](/rodrigues-rotation-formula/); the translation part needs one more matrix, $G(\theta)$.
Geometrically, every result is a [screw motion](/screw-motion/): a rotation about a fixed line and a translation along the same line.
The map is the building block of the [product of exponentials formula](/product-of-exponentials-formula/) for robot arms.

## In plain words

Think of a nut on a bolt.
When you turn the nut, it turns about the axis of the bolt, and it also moves along the axis.
The bolt axis, the amount of travel per turn, and the angle of the turn together fix where the nut ends up.
A twist holds the same three things as six numbers.
The exponential map takes these six numbers and gives the final position and orientation of the body, as a table of numbers that a computer can multiply.
When there is no turn, the body slides along a straight line, and the map is a plain shift.
When the angle is very small, the general formula would divide small numbers by small numbers, so a short series is used.

## The problem

We use the conventions of Lynch and Park.
A twist is $\mathcal{V} = (\omega, v) \in \mathbb{R}^6$, with the angular part first, and its matrix is

$$[\mathcal{V}] = \begin{pmatrix} [\omega] & v \\ 0 & 0 \end{pmatrix} \in \mathbb{R}^{4 \times 4},$$

where $[\omega]$ is the [skew-symmetric matrix](/skew-symmetric-matrix-of-a-vector/) of $\omega$.
A screw axis is a twist $S = (\omega, v)$ with $|\omega| = 1$, or with $\omega = 0$ and $|v| = 1$.
A [rigid-body twist](/rigid-body-twist/) is a screw axis times a speed, so we can write it as $S\dot\theta$.

Problem 1: given a screw axis $S$ and a number $\theta$, compute $T = e^{[S]\theta} \in SE(3)$.
For a revolute motion, $\theta$ is an angle in radians; for a prismatic motion ($\omega = 0$), it is a distance in meters.

Problem 2: given any vector of exponential coordinates $\xi = (w, u) \in \mathbb{R}^6$, compute $e^{[\xi]}$.
If $w \ne 0$, then $\xi = S\theta$ with $\theta = |w|$ and $S = \xi/\theta$.

The inverse problem, the logarithm, is: given $T \in SE(3)$, find $\xi$ with $e^{[\xi]} = T$.

## The algorithm

EXP-SCREW solves Problem 1.
EXP-COORDS solves Problem 2 and calls EXP-SCREW, unless the angle is below the threshold $\delta = 10^{-2}$.

```pseudo id=main
EXP-SCREW(S, θ)                              ▷ S = (ω, v) a screw axis
L1  (ω, v) ← S
L2  if ω = 0 then                             ▷ prismatic: |v| = 1
L3      return [[I, v θ], [0, 1]]              ▷ a translation by v θ
L4  K ← [ω]
L5  R ← I + sin θ · K + (1 - cos θ) · K²       ▷ Rodrigues' formula
L6  G ← I θ + (1 - cos θ) · K + (θ - sin θ) · K²
L7  p ← G v
L8  return [[R, p], [0, 1]]
```

```pseudo id=coords
EXP-COORDS(ξ)                                ▷ ξ = (w, u), any 6-vector
E1  (w, u) ← ξ
E2  θ ← |w|
E3  if θ ≥ δ then
E4      return EXP-SCREW(ξ / θ, θ)
E5  a ← 1 - θ²/6 + θ⁴/120 ; b ← 1/2 - θ²/24 + θ⁴/720 ; c ← 1/6 - θ²/120 + θ⁴/5040
E6  K ← [w]
E7  return [[I + a K + b K², (I + b K + c K²) u], [0, 1]]
```

Line L3 is the case of a pure translation.
Lines L5 and L6 come from the power series of $e^{[S]\theta}$, as the correctness section shows.
In EXP-COORDS, $a$, $b$ and $c$ are the Taylor polynomials of $\sin\theta/\theta$, $(1 - \cos\theta)/\theta^2$ and $(\theta - \sin\theta)/\theta^3$.
With these factors the result is the same matrix as in EXP-SCREW, but nothing is divided by $\theta$, so $\theta = 0$ is no special case.

The logarithm reverses the steps.
First take $w = \log R$ with the [logarithm map of SO(3)](/so3-logarithm-map/), and $\theta = |w|$.
Then $u = (I - \tfrac12 [w] + d\,[w]^2)\, p$ with $d = (1 - \tfrac{\theta}{2}\cot\tfrac{\theta}{2})/\theta^2$, and $d = 1/12 + \theta^2/720 + \theta^4/30240$ for small $\theta$.
This matrix is the inverse of the matrix $I + b[w] + c[w]^2$ in line E7.
In the form of Lynch and Park, with a unit $\hat\omega$, $G(\theta)^{-1} = \tfrac{1}{\theta} I - \tfrac12 [\hat\omega] + \big(\tfrac{1}{\theta} - \tfrac12\cot\tfrac{\theta}{2}\big)[\hat\omega]^2$, and $v = G(\theta)^{-1} p$.
If $R = I$, then $w = 0$ and the motion is a translation: $S = (0, p/|p|)$ and $\theta = |p|$.

## Example

Take the screw axis $S = (\omega, v)$ with $\omega = (0, 0, 1)$ and $v = (1, 0, 0)$, and $\theta = \pi/2$.

- Line L4: $K = [\omega]$, and $K^2 = \operatorname{diag}(-1, -1, 0)$.
- Line L5: with $\sin\theta = 1$ and $\cos\theta = 0$, $R = I + K + K^2 = R_z(\pi/2) = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$.
- Line L6: $G = \tfrac{\pi}{2} I + K + (\tfrac{\pi}{2} - 1) K^2$.
- Line L7: $\tfrac{\pi}{2} v = (\pi/2, 0, 0)$, $K v = \omega \times v = (0, 1, 0)$, and $K^2 v = (-1, 0, 0)$. So $p = (\pi/2 - (\pi/2 - 1),\ 1,\ 0) = (1, 1, 0)$.

So $T = e^{[S]\pi/2}$ turns the body by 90 degrees about the vertical and moves its origin to $(1, 1, 0)$ m.
The geometry explains this.
A screw axis with a unit $\omega$ and pitch $h$ through the point $q$ is $S = (\omega, -\omega \times q + h\omega)$.
Here $h = \omega \cdot v = 0$, and $-\omega \times q = (1, 0, 0)$ for $q = (0, 1, 0)$.
So the motion is a pure rotation by 90 degrees about the vertical line through $(0, 1, 0)$.
That rotation takes the origin, which is 1 m from the line in the $-y$ direction, to the point 1 m from the line in the $+x$ direction, which is $(1, 1, 0)$.

With a pitch of $h = 0.1$ m/rad about the same line, $S = (0, 0, 1, 1, 0, 0.1)$, and $\theta = \pi$, the implementation gives $R = R_z(\pi)$ and $p = (0, 2, 0.3141593)$.
The origin turns half way around the line to $(0, 2)$ and rises by $h\theta = 0.1\pi$.

A prismatic axis $S = (0, 0, 0, 0, 0, 1)$ with $\theta = 0.5$ m gives the translation $p = (0, 0, 0.5)$ and $R = I$.

The logarithm of the first $T$ returns $\xi = (0, 0, \pi/2, \pi/2, 0, 0) = S\theta$, the input.

## Correctness

By induction, $[S]^k = \begin{pmatrix} [\omega]^k & [\omega]^{k-1} v \\ 0 & 0 \end{pmatrix}$ for $k \ge 1$.
So the power series of $e^{[S]\theta}$ has the upper left block $e^{[\omega]\theta}$ and the upper right block $\big(\sum_{k \ge 1} \frac{\theta^k}{k!}[\omega]^{k-1}\big) v$.
If $\omega = 0$, only the term $k = 1$ is left, which gives line L3.
If $|\omega| = 1$, then $[\omega]^3 = -[\omega]$, so the powers of $[\omega]$ repeat with a sign.
Collecting the odd and the even powers gives the series of $\sin\theta$ and $1 - \cos\theta$ in the rotation block, which is line L5.
It gives the series of $1 - \cos\theta$ and $\theta - \sin\theta$ in $G$, which is line L6.
For EXP-COORDS, the three series alternate with decreasing terms when $\theta < 1$, so the truncation errors of line E5 are below $\theta^6/5040$, which is below $3 \cdot 10^{-16}$ for $\theta < 10^{-2}$.
The proof below gives all steps, and also proves that the matrix of the logarithm is the inverse of $G$.

## Complexity

The input has a fixed size, so the time and the space are $\Theta(1)$ in the [real RAM](/real-ram/).
EXP-SCREW computes one sine and one cosine, one $3 \times 3$ product $K^2$ (27 multiplications), two combinations of $I$, $K$ and $K^2$, and one product $G v$.
That is fewer than 150 floating-point operations.
The cost does not depend on $\theta$.

The product of exponentials formula for an arm with $n$ joints calls the map $n$ times and multiplies $n$ matrices of size $4 \times 4$, so forward kinematics costs $\Theta(n)$ operations.

## Properties

- **One parameter subgroups.** $e^{[S]\theta_1} e^{[S]\theta_2} = e^{[S](\theta_1 + \theta_2)}$, because $[S]\theta_1$ and $[S]\theta_2$ commute.
- **Derivative.** $\frac{d}{d\theta} e^{[S]\theta} = [S] e^{[S]\theta} = e^{[S]\theta} [S]$. So a body that moves along $e^{[S]\theta(t)}$ has the twist $S\dot\theta$, the same in the fixed frame and in the moving frame.
- **Surjective.** Every $T \in SE(3)$ is $e^{[\xi]}$ for some $\xi$; the logarithm above constructs one. This is the algebraic form of [Chasles' theorem](/chasles-theorem/).
- **Not injective.** Adding $2\pi$ to the angle of a revolute screw gives the same $T$, and at a rotation angle of $\pi$ there are two logarithms.
- **Change of frame.** $T e^{[S]\theta} T^{-1} = e^{[\mathrm{Ad}_T S]\theta}$, where $\mathrm{Ad}_T$ is the [adjoint map](/adjoint-map-se3/).
- **Not a group morphism.** In general $e^{[\xi_1]} e^{[\xi_2]} \ne e^{[\xi_1 + \xi_2]}$, because the two matrices do not commute.

## Variants and improvements

- **Two separate exponentials.** Some code computes $R = e^{[w]}$ and takes $p = u$ as the translation. That is a different map, the exponential of SO(3) times the translations, and it does not follow a screw motion. It is used in some filters; the two maps agree to first order only.
- **Dual quaternions.** A [dual quaternion](/dual-quaternion/) stores the same rigid motion in 8 numbers, and its exponential is the same screw motion.
- **The plane.** In SE(2), with $\xi = (\theta, u_x, u_y)$, the translation is $V u$ with $V = \frac{1}{\theta}\begin{pmatrix} \sin\theta & -(1 - \cos\theta) \\ 1 - \cos\theta & \sin\theta \end{pmatrix}$.
- **Jacobians.** Optimization on SE(3) needs the derivative of the exponential with respect to $\xi$, the left or right Jacobian. Sola, Deray and Atchuthan give the closed forms; see [uncertainty on Lie groups](/uncertainty-on-lie-groups/).

## When to use it

Use the exponential map to compute the [forward kinematics](/forward-kinematics/) of an arm with the product of exponentials formula, to integrate a constant twist over a time step exactly, and to apply a small correction $\xi$ to a pose in [pose graph optimization](/pose-graph-optimization/) or a filter on SE(3), with $T \leftarrow T e^{[\xi]}$.
Use the logarithm to measure the error between two poses as a 6-vector.
If you only need the composition of known poses, multiply the matrices directly with the [pose compounding operators](/pose-compounding-operators/).

## Pitfalls

- **The order of the twist.** Lynch and Park put the angular part first; Murray, Li and Sastry put the linear part first. A mix of the two gives wrong results without a warning.
- **v is not the velocity of the body origin.** In the twist $(\omega, v)$ in the fixed frame, $v$ is the velocity of the body point that is at the origin of the fixed frame. For a rotation about a line through $q$, $v = -\omega \times q$, not 0.
- **A screw that is not normalized.** EXP-SCREW needs $|\omega| = 1$. If you pass a twist $\xi$ with $|w| \ne 1$, use EXP-COORDS, which normalizes.
- **Small angles.** The closed form $(1 - \cos\theta)/\theta^2$ loses digits to cancellation when $\theta$ is small; use the series below a threshold.
The tests of the implementation check that the two branches agree to $10^{-13}$ at the threshold $10^{-2}$ (a measurement, not a proof).
- **Integrating the translation separately.** $e^{[\xi]}$ is not the translation $u$ followed by the rotation $e^{[w]}$; the translation of $e^{[\xi]}$ is $G u$, not $u$.

## Implementations

## History

The screw theory of rigid motion goes back to Mozzi (1763) and Chasles (1830).
Brockett (1984) used exponentials of twists to describe the kinematics of robot arms, the product of exponentials formula.
Murray, Li and Sastry (1994) and Lynch and Park (2017) give the closed form of the exponential and its inverse in their textbooks.
Lynch and Park note that, in the kinematics literature, exponential coordinates of rotation have also been called Euler-Rodrigues parameters.

## References
