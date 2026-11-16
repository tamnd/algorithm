---
tag: SBVY23
kind: problem
slug: kinematic-calibration
name: Kinematic calibration
aliases:
- robot calibration
area: robotics/robot-kinematics
level: advanced
summary: Estimate the true link parameters of a robot from measured end effector poses, so that its forward kinematics model matches the real arm. It is a nonlinear least squares problem.
prereqs: [forward-kinematics, nonlinear-least-squares]
see_also: [nonlinear-least-squares, denavit-hartenberg-convention, product-of-exponentials-formula, levenberg-marquardt, gauss-newton-algorithm, dynamic-parameter-identification, observability, singular-value-decomposition]
sources:
  - paper: doi:10.1177/027836499601500604
    title: J. M. Hollerbach and C. W. Wampler, The calibration index and taxonomy for robot kinematic calibration methods, International Journal of Robotics Research 15(6), 1996
    locator: pages 573 to 591, the count of equations per pose and the classification of open loop and closed loop calibration methods
  - paper: doi:10.1109/CDC.1983.269783
    title: S. A. Hayati, Robot arm geometric link parameter estimation, Proceedings of the 22nd IEEE Conference on Decision and Control, 1983
    locator: pages 1477 to 1483, the failure of the DH parameters for nearly parallel joint axes, and an extra rotation for such joints
  - paper: doi:10.1002/rob.4620020406
    title: S. Hayati and M. Mirmirani, Improving the absolute positioning accuracy of robot manipulators, Journal of Robotic Systems 2(4), 1985
    locator: pages 397 to 413, the modified link model and its use for calibration
  - paper: doi:10.1109/70.149944
    title: H. Zhuang, Z. S. Roth and F. Hamano, A complete and parametrically continuous kinematic model for robot manipulators, IEEE Transactions on Robotics and Automation 8(4), 1992
    locator: pages 451 to 463, the CPC model
  - book: "L. J. Everett, M. Driels and B. W. Mooring, Kinematic modelling for robot calibration, Proceedings of the 1987 IEEE International Conference on Robotics and Automation, Raleigh"
    locator: the number of independent kinematic parameters, 4R + 2P + 6 (general locator)
  - book: isbn:9780471508649
    title: B. W. Mooring, Z. S. Roth and M. R. Driels, Fundamentals of Manipulator Calibration, Wiley, 1991
    locator: modeling, measurement, identification and compensation (general locator)
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.11, Kinematic Calibration
---

Kinematic calibration finds the true values of the geometric parameters of a robot: the link lengths, the twists and offsets between joint axes, the zero positions of the joints, and the frames of the base and the tool. The controller computes the pose of the tool with [forward kinematics](/forward-kinematics/), using the values from the drawings. Small errors in manufacture and assembly make the real pose differ from this prediction, often by a millimeter or more on an industrial arm, even though the arm returns to a taught pose much more precisely. Calibration moves the arm to many poses, measures the tool with an external sensor, and fits the parameters by [nonlinear least squares](/nonlinear-least-squares/). The main questions are which parameters the data can determine (identifiability), how to choose the poses, and which model of the arm to use.

## In plain words

A robot computes where its hand is from its joint angles and from the lengths of its parts. If a part is a little longer than the drawing says, the robot thinks its hand is in one place when it is really a little to the side.

To fix this, move the robot to many positions and measure where the hand really is, for example with a laser tracker. Then adjust the lengths and angles in the robot's model until its predictions match the measurements as closely as possible.

Some errors cannot be told apart. If the whole robot is turned a little on the floor, or its first joint reads a little off, every measurement changes in the same way. Then only the sum of the two errors can be found, and the model must keep only one of them.

## Definition

**Model.** A forward kinematics map $T(q;\, \phi) \in SE(3)$ of the joint values $q \in \mathbb{R}^n$ and the parameter vector $\phi \in \mathbb{R}^N$. The parameters can be the [Denavit-Hartenberg](/denavit-hartenberg-convention/) parameters plus joint offsets and the base and tool frames, or the joint screws and home pose of the [product of exponentials](/product-of-exponentials-formula/). The nominal value is $\phi_0$.

**Data.** $K$ joint vectors $q_1, \dots, q_K$ and the measurements $y_1, \dots, y_K$ of the tool at those joint values. A measurement can be a full pose ($m = 6$ numbers), a position ($m = 3$), or less.

**Problem.** Find

$$\hat\phi = \arg\min_{\phi} \sum_{k=1}^{K} \big\| y_k - h(q_k;\, \phi) \big\|^2 ,$$

where $h(q;\phi)$ is the part of $T(q;\phi)$ that the sensor measures. The norm can be weighted to put positions and angles on the same scale.

**Identification Jacobian.** Stack the derivatives $\partial h(q_k; \phi) / \partial \phi$ for all $k$ into the $Km \times N$ matrix $\Phi(\phi)$.

**Identifiability.** *If $\Phi(\phi^\ast)$ has full column rank $N$ at the true parameters $\phi^\ast$, then $\phi^\ast$ is locally identifiable: no other parameter vector near $\phi^\ast$ gives the same noise-free measurements.* Proof: the map $\phi \mapsto (h(q_k;\phi))_k$ has an injective derivative at $\phi^\ast$, so it is an immersion and is injective on a neighborhood of $\phi^\ast$. $\blacksquare$ If some column of $\Phi$ is a combination of others for every choice of poses, the parameter set is redundant and must be reduced. If the rank is low only for the chosen poses, more or better poses are needed. This is the same question as [observability](/observability/) in control.

**Complete and minimal models.** A model is *complete* if it can describe every real arm close to the nominal one, and *minimal* if no parameter is redundant. Everett, Driels and Mooring (1987) showed that a complete and minimal model of an arm with $R$ revolute and $P$ prismatic joints has

$$N = 4R + 2P + 6$$

independent parameters when the full pose of the tool is measured. For a 6R arm, $N = 30$. With position measurement only, the 3 parameters of the tool orientation do not affect the data, and 27 parameters remain.

## Variants

| variant | what is measured | notes |
|---|---|---|
| open loop, full pose | position and orientation of the tool | 6 equations per pose |
| open loop, position only | tool position, for example by a laser tracker | 3 equations per pose; the tool orientation is not identifiable |
| closed loop, self calibration | none outside; the tool is held on a point, a plane or a sphere | the constraint gives the equations; Hollerbach and Wampler (1996) count the equations each pose gives, their calibration index, to classify such methods |
| parallel robots | leg lengths and the measured platform pose | the residual can be written in the leg lengths, which needs only the closed form inverse kinematics |
| non-geometric errors | as above | joint compliance, gear errors and heat are outside the kinematic model; some methods add terms for them |

**The DH model near parallel axes.** For two nominally parallel joint axes, the DH offset $d_i$ is set by the common normal. A tilt of one axis by a small angle $\varepsilon$ moves the common normal far along the axis, so $d_i$ changes by an amount of order $1/\varepsilon$, and the model is not a continuous function of the real geometry. Hayati (1983) and Hayati and Mirmirani (1985) replace $d_i$ by a small rotation $\beta_i$ about the $y$ axis for such joints. The CPC model of Zhuang, Roth and Hamano (1992) is complete and parametrically continuous for all axis layouts. A product of exponentials model is also continuous in this sense, because a small change of a joint axis is a small change of its screw.

## Examples

**A planar 2R arm, worked by hand.** The nominal link lengths are $L_1 = L_2 = 1$ m and the true ones are $L_1 = 1.02$ m and $L_2 = 0.97$ m. The tip is

$$p(q) = L_1 (\cos q_1, \sin q_1) + L_2 (\cos(q_1 + q_2), \sin(q_1 + q_2)),$$

which is linear in $(L_1, L_2)$, so here the least squares problem is linear and one step of [Gauss-Newton](/gauss-newton-algorithm/) solves it.

- At $q = (0, 0)$ the measured tip is $(1.99, 0)$; the nominal model predicts $(2, 0)$. The rows of $\Phi$ are $(1, 1)$ and $(0, 0)$.
- At $q = (0, \pi/2)$ the measured tip is $(1.02, 0.97)$; the nominal model predicts $(1, 1)$. The rows are $(1, 0)$ and $(0, 1)$.

With both poses, $\Phi^\top \Phi = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and $\Phi^\top y = (1.99 + 1.02,\ 1.99 + 0.97) = (3.01, 2.96)$. Solving gives $L_1 = (2 \cdot 3.01 - 2.96)/3 = 1.02$ and $L_2 = (2 \cdot 2.96 - 3.01)/3 = 0.97$, the true values.

With the first pose only, $\Phi$ has rank 1: the data fix $L_1 + L_2 = 1.99$ and nothing else. A stretched arm cannot tell its two links apart, so the poses must be chosen with care.

**Two parameters that cannot be separated.** Add to the same arm a rotation $\beta$ of the base about the vertical axis and an offset $\delta_1$ of the zero of joint 1. The tip depends only on $q_1 + \beta + \delta_1$, so the columns of $\Phi$ for $\beta$ and $\delta_1$ are equal at every pose. No choice of poses makes them identifiable, and a minimal model keeps only their sum.

## Known algorithms

Costs are in the [real RAM](/real-ram/) model for $K$ poses, $n$ joints and $N = O(n)$ parameters.

| step | method | cost |
|---|---|---|
| residuals and $\Phi$ | forward kinematics and its derivative in the parameters, pose by pose | $O(K n^2)$ by a direct method, $O(K n)$ with prefix and suffix products |
| one iteration | [Gauss-Newton](/gauss-newton-algorithm/): form $\Phi^\top\Phi$ and solve, or use the [QR decomposition](/qr-decomposition/) of $\Phi$ | $O(K n^2 + n^3)$ |
| robust iteration | [Levenberg-Marquardt](/levenberg-marquardt/), with a damping term | the same per iteration |
| redundant parameters | find the dependent columns with the [singular value decomposition](/singular-value-decomposition/) or QR with pivoting, and remove them | $O(K n^2 + n^3)$ |
| pose selection | choose poses that make the smallest singular value, or the [condition number](/condition-number/), of $\Phi$ good | heuristic search |

Gauss-Newton converges locally, and quadratically when the residual at the solution is zero. The nominal parameters are usually a good start because the errors are small, but that is an observation about practice, not a theorem.

## Bounds

- **Number of measurements (counting).** The noise-free equations $h(q_k;\phi) = y_k$ can determine $N$ parameters only if $K m \ge N$. For a 6R arm this means at least 5 full poses ($5 \cdot 6 = 30$) or at least 9 positions ($9 \cdot 3 = 27$). In practice many more poses are used, to average the noise.
- **Number of parameters.** $4R + 2P + 6$ for a complete and minimal model with full pose data (Everett, Driels and Mooring 1987).
- **Accuracy of the estimate.** For the linearized problem with independent noise of variance $\sigma^2$ in each measured number, the least squares estimate has covariance $\sigma^2 (\Phi^\top \Phi)^{-1}$. So a small singular value of $\Phi$ means a large error in some combination of the parameters.

## Reductions

- **To nonlinear least squares.** The problem is an instance of [nonlinear least squares](/nonlinear-least-squares/) with a structured Jacobian, one block of rows per pose.
- **From dynamic identification.** [Dynamic parameter identification](/dynamic-parameter-identification/) estimates masses and inertias and is linear in its parameters, so one linear least squares solve suffices. Its counterpart of a minimal model is the set of [base inertial parameters](/base-inertial-parameters/). Kinematic calibration is nonlinear in its parameters, because they enter through sines, cosines and products of transforms.
- **To linear least squares, near the nominal model.** Linearize at $\phi_0$: $y_k - h(q_k;\phi_0) \approx \Phi_k(\phi_0)\, \Delta\phi$. One solve of this linear problem is one Gauss-Newton step, and for small errors one or two steps are often enough.

## Applications

Offline programming, where robot programs are generated from a CAD model and run without teaching each pose by hand, needs an arm whose absolute pose is accurate, not only repeatable. So do robots that are guided by external sensors, robots in machining and drilling, and robots replaced in a cell without reteaching. Calibration is also a step in the manufacture of many industrial arms, and the identified parameters are stored in the controller.

## References
