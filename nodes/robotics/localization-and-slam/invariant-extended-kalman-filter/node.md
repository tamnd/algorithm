---
tag: 5ADY95
kind: algorithm
slug: invariant-extended-kalman-filter
name: Invariant extended Kalman filter
aliases:
- InEKF
area: robotics/localization-and-slam
level: research
summary: Barrau and Bonnabel's EKF on a matrix Lie group with an invariant error, whose propagation does not depend on the estimate for group-affine systems.
solves: [mobile-robot-localization, state-estimation]
model: real-ram
complexity:
  vars: {T: the number of time steps, k: the dimension of the group}
  time: {worst: O(T k^3)}
  space: {extra: O(k^2)}
properties: {deterministic: true, exact: false, online: true, recursive: true}
history:
  year: 2017
  people: [Axel Barrau, Silvère Bonnabel]
  note: Barrau and Bonnabel showed that for group-affine dynamics the invariant error follows an exactly linear law in the Lie algebra, and used it to prove local stability of the invariant EKF as an observer.
prereqs: [extended-kalman-filter, special-euclidean-group, uncertainty-on-lie-groups]
see_also: [error-state-kalman-filter, ekf-localization, nonlinear-complementary-filter, attitude-estimation, matrix-exponential, se3-exponential-map, ekf-slam, robot-pose]
sources:
  - paper: doi:10.1109/TAC.2016.2594085
    title: "Axel Barrau and Silvère Bonnabel, The invariant extended Kalman filter as a stable observer, IEEE Transactions on Automatic Control 62(4), 2017, pages 1797 to 1812"
    locator: "Theorem 2 (the log-linear property of the invariant error for group-affine systems), the definitions of the left and right invariant filters, and the stability results"
  - paper: "Axel Barrau and Silvère Bonnabel, The invariant extended Kalman filter as a stable observer, arXiv:1410.1465"
    locator: "Section 4 (the car example with odometry and position measurements)"
---

The invariant extended Kalman filter, or InEKF, is an [extended Kalman filter](/extended-kalman-filter/) whose state lives on a matrix Lie group, such as the planar poses $SE(2)$ or the [special Euclidean group](/special-euclidean-group/) $SE(3)$, and whose error is a group difference $\hat\chi^{-1} \chi$ or $\chi \hat\chi^{-1}$ rather than a vector difference. Barrau and Bonnabel (2017) showed that for a wide class of dynamics, which they call group affine, this error evolves by an exactly linear law in logarithmic coordinates, whatever the estimate is. The linearization in the propagation step is then exact for the noise-free part, and with a matching measurement the gain and covariance do not depend on the estimate at all. The usual EKF evaluates its Jacobians at the estimate, so a bad estimate gives bad Jacobians; the InEKF removes that loop. It is close to the [error-state Kalman filter](/error-state-kalman-filter/), which also keeps a nominal state and a small error, but the InEKF chooses the error so that the dynamics leave it invariant.

## In plain words

A robot that drives with odometry and gets position fixes from GPS is easy to model but hard to filter well, because heading and position are tied together by turning. A standard filter linearizes the motion around its current guess, so a wrong guess makes the filter wrong in a way that feeds on itself. This filter measures its error in the robot's own frame. With that choice, the way the error moves no longer depends on the guess, so the filter computes the same uncertainty and the same correction strength whether its guess is good or bad. In practice it recovers from large heading errors that make a standard filter diverge.

## The problem

The pose $\chi_k = (R_k, p_k) \in SE(2)$ moves as $\chi_{k+1} = \chi_k \exp(u_k)$, where $u_k = (\omega \delta t, v \delta t, 0)$ is the body twist over one step of a car and $\exp$ is the [matrix exponential](/matrix-exponential/) of $SE(2)$. Odometry reads $u_m = u + n$ with $n \sim (0, Q)$. A position sensor reads $Y = p + V$ with $V \sim (0, N)$. Estimate $\chi_k$ with a covariance, online. The filter writes the true pose as $\chi = \hat\chi \exp(\xi)$ and keeps the covariance $P$ of the error $\xi = (\xi_\theta, \xi_x, \xi_y)$. Here $e = \hat\chi^{-1} \chi$ is the inverse of the left-invariant error $\eta^L = \chi^{-1} \hat\chi$ of Barrau and Bonnabel (2017); the two carry the same information.

## The algorithm

Write $\operatorname{Ad}_\chi$ for the adjoint matrix with $\chi \exp(\xi) \chi^{-1} = \exp(\operatorname{Ad}_\chi \xi)$ and $H = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix}$.

```pseudo id=main
INEKF-STEP(χ̂, P, u_m, Q, Y, N)       ▷ one odometry increment and one position fix; returns (χ̂, P)
L1  χ̂ ← χ̂ exp(u_m)                                   ▷ propagate the estimate
L2  F ← Ad_{exp(-u_m)}
L3  P ← F P F^T + Q
L4  z ← first two entries of χ̂^{-1} (Y, 1)            ▷ innovation in the body frame, R̂^T (Y - p̂)
L5  N̂ ← R̂^T N R̂ ;  S ← H P H^T + N̂
L6  K ← P H^T S^{-1}
L7  χ̂ ← χ̂ exp(K z)                                    ▷ update on the group
L8  P ← (I - K H) P (I - K H)^T + K N̂ K^T             ▷ Joseph form
```

Lines L1 to L3 are the prediction. The matrix $F$ comes from the identity $\xi^+ = \operatorname{Ad}_{\exp(-u_m)} \xi$, which holds exactly for noise-free odometry. Line L4 moves the position fix into the frame of the estimate; for the true pose the result would be $(0, 0)$, so $z$ measures the error directly and its Jacobian is the constant $H$. Line L5 rotates the sensor noise into the same frame. When $N = s^2 I$, the rotation has no effect, so $S$, $K$ and $P$ are built only from $P_0$, $Q$, $N$ and the odometry. Line L7 applies the correction on the group, so $\hat\chi$ stays a valid pose.

## Example

The car drives at $1$ m/s and turns at $0.3 \sin(0.05 k)$ rad/s, with $\delta t = 0.1$ s and a position fix at every step. The data are exact, but the filter uses $Q = 0.01^2 I$ and $N = 0.1^2 I$. It starts with a heading error of $2.5$ rad ($143$ degrees) and a position error of $12.8$ m, with $P_0 = \operatorname{diag}(\pi^2, 100, 100)$.

| after correction | heading error (degrees) | position error (m) |
|---|---|---|
| 1 | 143.0 | 0.030 |
| 2 | 128.6 | |
| 5 | 36.2 | |
| 10 | 6.58 | 0.039 |
| 20 | 1.43 | |
| 50 | 0.029 | 0.0011 |

The first fix puts the position in the right place, and the heading follows as the car moves and the fixes reveal its direction. Two runs of the filter from different estimates, with the same fixes and odometry, produced the same $P$ and $K$ to $10^{-12}$. In a test with noisy data, the normalized estimation error squared averaged $2.76$ over 10 runs of 60 steps, close to the error dimension $3$, which a consistent filter should give. All numbers are measurements of the code.

## Correctness

The proof shows four facts for this model; the first is a theorem with no linearization at all, a case of Theorem 2 of Barrau and Bonnabel (2017).

1. With exact odometry, $\xi^+ = \operatorname{Ad}_{\exp(-u_m)} \xi$ for an error of any size and any $\hat\chi$.
2. The innovation satisfies $z = H \xi + \hat R^T V$ to first order, with constant $H$.
3. After line L7, the error is $(I - K H) \xi - K \hat R^T V$ to first order, so line L8 gives its covariance for any gain.
4. With $N = s^2 I$, the sequences $P_k$ and $K_k$ do not depend on the estimates.

[The correctness proof](proofs/correctness.md) has the derivations. Barrau and Bonnabel (2017) also prove that, under conditions on the noise matrices and the observability of the system, the InEKF is a locally stable observer around any trajectory; this page does not restate the conditions.

## Complexity

In the [real RAM](/real-ram/) model, with the group $SE(2)$ of dimension $k = 3$, each step costs $O(1)$: a few $3 \times 3$ products, one exponential and one $2 \times 2$ solve. Over $T$ steps the time is $O(T)$. For a group of dimension $k$ with measurements of size at most $k$, a step costs $O(k^3)$ and the memory is $O(k^2)$ for $P$, as for any Kalman filter.

## Properties

- **Log-linear error (theorem).** For group-affine dynamics, the noise-free error obeys a linear recursion in the Lie algebra exactly, not only to first order. A test propagated an error of size $\xi = (1, 2, -1.5)$ for 60 steps and matched the linear recursion to $10^{-9}$ (measurement).
- **Estimate-free gain (theorem, for this model).** With isotropic position noise, $P$ and $K$ do not depend on $\hat\chi$.
- **Consistency (measurement).** The NEES of $2.76$ against the dimension $3$, above.
- **Stays on the group.** The update multiplies by an exponential, so $\hat R$ stays a rotation.
- **Choice of error matters.** A left-invariant error suits measurements of the form $Y = \chi b + V$, such as the position fix here, where $b = (0, 0, 1)$. A right-invariant error $\hat\chi \chi^{-1}$ suits measurements of the form $Y = \chi^{-1} b + V$, such as a known landmark or direction seen from the body. With the other choice the Jacobian $H$ depends on the estimate again (heuristic summary of Barrau and Bonnabel, 2017).

## Variants and improvements

- **Other groups.** The same construction runs on $SE(3)$ for a 3D pose, and on a larger matrix group that holds attitude, velocity and position together for inertial navigation.
- **Attitude only.** On the rotation group $SO(3)$ with direction measurements, the invariant filter is close to the multiplicative filter of the [error-state Kalman filter](/error-state-kalman-filter/) page, which also uses a group error.
- **Biases.** Sensor biases do not fit the group structure. The usual remedy is to carry them as an extra vector state; the error then loses part of its invariance, and the exactness results hold only in part (heuristic).
- **SLAM.** Landmark positions can be added to the group, which gives an invariant form of [EKF SLAM](/ekf-slam/) (heuristic; this page does not cover it).

## When to use it

Use it when the state is a pose or another matrix Lie group element, the dynamics are group affine (rigid-body kinematics, odometry, inertial navigation with gravity), and the measurements are of the invariant form, for example position fixes, landmark bearings in the body frame or known directions. It is most useful when the initial heading is poor, where a standard EKF can diverge. When the system is not group affine, the gain still uses a group error, but the exactness results do not apply.

## Pitfalls

- **Left and right.** The error convention, the side of the exponential in the update and the form of $F$ must agree. Mixing a right update with a left error gives a filter that runs but is wrong.
- **Rotating the noise.** The measurement noise in the body frame is $\hat R^T N \hat R$. Using $N$ directly is correct only when $N$ is isotropic.
- **Noise Jacobian.** The odometry noise enters through a Jacobian close to $I$ for small steps. Using $Q$ directly, as in line L3, is the common first-order choice.
- **Not a global guarantee.** The stability results are local. In the example the filter recovered from $143$ degrees, but that is a measurement, not a theorem.

## Implementations

## History

Bonnabel, with Martin and Rouchon, worked on observers that keep the symmetries of the system in the 2000s, and this led to invariant versions of the extended Kalman filter. Barrau and Bonnabel (2017) gave the general group-affine framework, the log-linear property and stability proofs, and their car example with odometry and position fixes is the model on this page. Their filter has since been used for inertial navigation and for legged and wheeled robots.

## References
