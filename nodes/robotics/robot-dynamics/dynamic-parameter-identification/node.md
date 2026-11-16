---
tag: 51Y1TE
kind: problem
slug: dynamic-parameter-identification
name: Dynamic parameter identification
aliases:
- robot inertial parameter estimation
area: robotics/robot-dynamics
level: advanced
summary: Estimate the identifiable inertial and friction parameters of a robot from measured joint motions and torques, usually by least squares on the base parameters along an exciting trajectory.
prereqs: [least-squares-problem, base-inertial-parameters]
see_also: [linearity-in-dynamic-parameters, weighted-least-squares, maximum-likelihood-estimation, condition-number, semidefinite-programming, slotine-li-adaptive-control, computed-torque-control, kinematic-calibration]
sources:
  - paper: doi:10.1177/027836498600500306
    title: Christopher G. Atkeson, Chae H. An and John M. Hollerbach, Estimation of inertial parameters of manipulator loads and links, The International Journal of Robotics Research 5(3), 1986
    locator: pages 101 to 119
  - paper: doi:10.1109/70.56655
    title: Maxime Gautier and Wisama Khalil, Direct calculation of minimum set of inertial parameters of serial robots, IEEE Transactions on Robotics and Automation 6(3), 1990
    locator: pages 368 to 373
  - paper: doi:10.1177/027836499201100408
    title: Maxime Gautier and Wisama Khalil, Exciting trajectories for the identification of base inertial parameters of robots, The International Journal of Robotics Research 11(4), 1992
    locator: pages 362 to 375
  - paper: doi:10.1109/70.631234
    title: Jan Swevers, Chris Ganseman, Dilek Bilgin Tükel, Joris De Schutter and Hendrik Van Brussel, Optimal robot excitation and identification, IEEE Transactions on Robotics and Automation 13(5), 1997
    locator: pages 730 to 740
  - paper: doi:10.1109/LRA.2017.2729659
    title: "Patrick M. Wensing, Sangbae Kim and Jean-Jacques E. Slotine, Linear matrix inequalities for physically consistent inertial parameter identification: a statistical perspective on the mass distribution, IEEE Robotics and Automation Letters 3(1), 2018"
    locator: pages 60 to 67
  - book: isbn:9783319325507
    title: Bruno Siciliano and Oussama Khatib (editors), Springer Handbook of Robotics, second edition, Springer, 2016
    locator: "Chapter 6, Model Identification, by John Hollerbach, Wisama Khalil and Maxime Gautier, pages 113 to 138"
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Chapter 7, Section 7.4 (dynamic parameter identification)
---

Dynamic parameter identification is the problem of finding the inertial parameters of a robot, and usually its joint friction parameters, from measurements of its motion and its joint torques. Because the dynamics are linear in these parameters, the problem is a linear [least squares problem](/least-squares-problem/) once the motion is known. Only the [base inertial parameters](/base-inertial-parameters/) can be found, and only if the robot moves along a trajectory that excites every one of them.

## In plain words

The data sheet of a robot rarely gives the mass and the shape of the mass of each link with enough accuracy for good control, and a tool or a load changes them. So we let the robot move, record where its joints are and how hard each motor pushes, and ask which masses and inertias explain the record best. Each instant gives a few equations, and a long record gives many more equations than unknowns, so we take the best fit. Two things can spoil the answer. Some properties of the links never change the motor effort, so no record can show them; we drop those and keep only the combinations that matter. And a gentle or repetitive motion shows some combinations so weakly that noise hides them; the motion must be rich enough to show each one clearly.

## Definition

**Input.** The kinematic model of the robot, a choice of base parameters with the regressor $Y_B(q, \dot q, \ddot q)$ of size $n \times r$ (see [linearity in the dynamic parameters](/linearity-in-dynamic-parameters/)), and $K$ samples $(q_k, \dot q_k, \ddot q_k, \tau_k)$ of joint positions, velocities, accelerations and torques. In practice $\dot q_k$ and $\ddot q_k$ come from filtered numerical derivatives of the measured positions, and $\tau_k$ from motor currents and the motor torque constants.

**Model.** $\tau_k = Y_B(q_k, \dot q_k, \ddot q_k)\, \pi_B + e_k$ with an error $e_k$. With joint friction, the vector $\pi_B$ also holds, for example, a viscous coefficient and a Coulomb friction level per joint, whose columns are $\dot q_j$ and $\mathrm{sign}(\dot q_j)$.

**Output.** An estimate $\hat\pi_B \in \mathbb{R}^r$. The ordinary least squares estimate minimizes $\| T - W \pi_B \|^2$, with the stacked observation matrix $W$ ($Kn \times r$) and the stacked torques $T$:
$$\hat\pi_B = \arg\min_{\pi_B} \sum_{k=1}^K \| \tau_k - Y_B(q_k, \dot q_k, \ddot q_k)\, \pi_B \|^2 .$$
It is unique if and only if $W$ has full column rank $r$.

## Variants

- **Weighted least squares.** Joints have different noise levels, so each row is divided by an estimate of the standard deviation of its joint; see [weighted least squares](/weighted-least-squares/).
- **Maximum likelihood.** Swevers et al. (1997) used a periodic excitation, averaged the measurements over the periods to estimate the noise, and computed a [maximum likelihood estimate](/maximum-likelihood-estimation/).
- **Physical consistency.** Add the condition that $\pi_B$ comes from links with positive masses and valid inertia matrices. Wensing, Kim and Slotine (2018) wrote this condition as a [linear matrix inequality](/linear-matrix-inequality/) on the pseudo-inertia matrix of each link, so the estimation becomes a [semidefinite program](/semidefinite-programming/).
- **Load identification.** Only the ten parameters of the payload are unknown, measured with a wrist force sensor or from the joint torques (Atkeson, An and Hollerbach 1986).
- **Excitation design.** Choose the trajectory before the experiment so that $W$ is well conditioned; see below.
- **Floating base.** For a legged robot, the six base rows of the [floating-base dynamics](/floating-base-dynamics/) give equations in the parameters with the contact forces in place of the joint torques.
- **Online estimation.** Estimate the parameters while the robot runs, as in [Slotine-Li adaptive control](/slotine-li-adaptive-control/), where the estimate is updated to reduce the tracking error.

## Examples

A pendulum with one joint has the model $\tau = I \ddot q + g\, c \sin q + f \dot q$, where $q$ is measured from the hanging position, $I$ is the inertia about the joint, $c$ the mass times the distance of the center of mass from the axis, and $f$ the viscous friction coefficient. So $Y_B = (\ddot q,\ g \sin q,\ \dot q)$ and $\pi_B = (I, c, f)$. Take the true values $(0.5$ kg m$^2$, $1$ kg m, $0.1$ N m s$)$, 200 samples every 0.05 s, and Gaussian torque noise with a standard deviation of 0.05 N m (random seed 5).

| Trajectory | Condition number of $W$ | Estimate $(I, c, f)$ |
|---|---|---|
| $q = 0.1 \sin 2t$ | 6807 | $(-0.405,\ 0.630,\ 0.098)$ |
| $q = 0.8 \sin t + 0.4 \sin 3t$ | 5.58 | $(0.502,\ 1.000,\ 0.100)$ |

The first trajectory is small and has one frequency. Then $\sin q \approx q = -\ddot q / 4$, so the first two columns of $W$ are almost parallel, and the data fix only the combination $I - g c / 4$: the estimate gives $-0.405 - 9.81 \times 0.630 / 4 = -1.950$, and the true value is $0.5 - 9.81 / 4 = -1.9525$. The inertia estimate is negative, which no physical pendulum has. The second trajectory has a large amplitude and two frequencies, and it gives all three parameters to about 0.5 percent.

## Known algorithms

- **Least squares by QR.** Solve the stacked problem with a [QR decomposition](/qr-decomposition/) of $W$, or with the [SVD](/singular-value-decomposition/) when $W$ is close to rank deficient. The normal equations square the condition number. Cost: $O(K n r^2)$ for $K$ samples.
- **Regressor by recursion.** Each row block $Y_B(q_k, \dot q_k, \ddot q_k)$ can be computed with a modified [recursive Newton-Euler algorithm](/recursive-newton-euler-algorithm/), followed by the column reduction of the base parameters.
- **Exciting trajectories.** Gautier and Khalil (1992) computed trajectories that minimize a criterion based on the condition number of $W$. Swevers et al. (1997) used finite Fourier series for the joint motions, which are periodic and band limited, and optimized their coefficients.
- **Semidefinite programming.** For the physically consistent variant, an interior point method solves the least squares problem under the LMI constraints (Wensing, Kim and Slotine 2018).

## Bounds

- **Identifiability (theorem).** The parameters $\pi_B$ are determined by noise-free data if and only if $W$ has full column rank. The standard parameters $\pi$ are never all determined when the regressor has a rank deficit; see [base inertial parameters](/base-inertial-parameters/).
- **Statistical accuracy (theorem).** If the errors $e_k$ are independent with zero mean and covariance $\sigma^2 I$, the least squares estimate is unbiased with covariance $\sigma^2 (W^T W)^{-1}$, and by the Gauss-Markov theorem no other linear unbiased estimate has a smaller covariance. With Gaussian errors this is also the Cramér-Rao bound.
- **Effect of conditioning.** The relative error of $\hat\pi_B$ is bounded by the [condition number](/condition-number/) of $W$ times the relative size of the noise, to first order. This is why excitation design minimizes the condition number.
- **Errors in the regressor.** The accelerations in $W$ are noisy too, so the least squares estimate has a bias; filtering the data and the use of many samples make it small in practice.

## Reductions

- To the linear [least squares problem](/least-squares-problem/), after the reduction to base parameters.
- To a [semidefinite program](/semidefinite-programming/), when physical consistency is required.
- The same structure as [kinematic calibration](/kinematic-calibration/), where geometric parameters are found from pose measurements and only identifiable combinations of the errors can be found.

## Applications

- Feedforward and model-based control, such as [computed-torque control](/computed-torque-control/), which needs the inertial parameters to cancel the dynamics.
- Collision detection, which compares the measured torques with the torques of the model.
- Identification of a payload before the robot moves it fast.
- Simulation models of an existing robot.

## References
