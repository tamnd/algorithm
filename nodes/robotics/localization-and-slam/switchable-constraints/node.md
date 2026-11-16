---
tag: CZESV3
kind: technique
slug: switchable-constraints
name: Switchable constraints
aliases:
- switch variables for robust SLAM
area: robotics/localization-and-slam
level: research
summary: Gives each loop closure a switch variable that the optimizer can turn off, so false loop closures stop distorting the map.
prereqs: [pose-graph-optimization, nonlinear-least-squares]
see_also: [loop-closure-detection, m-estimator, ransac, se-sync, pose-graph, isam2, gauss-newton-algorithm, graphslam]
sources:
  - paper: doi:10.1109/IROS.2012.6385590
    title: "Niko Sünderhauf and Peter Protzel, Switchable constraints for robust pose graph SLAM, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2012, pages 1879 to 1884"
    locator: "the switch variable on each loop closure, the switch function, the switch prior, and the experiments with added false loop closures"
  - paper: "Niko Sünderhauf and Peter Protzel, Towards a robust back-end for pose graph SLAM, IEEE International Conference on Robotics and Automation, 2012, pages 1254 to 1261"
    locator: "the first form of the switchable constraints in a factor graph"
  - paper: doi:10.1109/TRO.2016.2624754
    title: "Cesar Cadena, Luca Carlone, Henry Carrillo, Yasir Latif, Davide Scaramuzza, Jose Neira, Ian Reid and John J. Leonard, Past, present, and future of simultaneous localization and mapping: toward the robust-perception age, IEEE Transactions on Robotics 32(6), 2016, pages 1309 to 1332"
    locator: "the discussion of robust back ends against wrong data association"
---

Switchable constraints make the back end of a SLAM system robust to wrong loop closures. A [loop closure detector](/loop-closure-detection/) sometimes says that two places are the same when they are not. One such edge in a [pose graph](/pose-graph/) can bend the whole map, because least squares gives a large error a large weight. Sünderhauf and Protzel give each loop closure edge a new variable $s_{ij}$, the switch. The error of the edge is multiplied by $\psi(s_{ij})$, a function with values in $[0, 1]$, and a prior term pulls each switch toward 1, the value "on". The optimizer then decides, together with the poses, how much to trust each loop closure. A wrong edge with a large error costs less when its switch goes toward 0 and the prior is paid instead. It is a heuristic. It does not guarantee that wrong edges are switched off or that right edges stay on, and the joint problem has more local minima than the original one.

## In plain words

Each loop closure gets a dimmer. The solver can turn a dimmer down when that loop closure does not fit with the rest of the map, but each turn costs a small fixed price. A correct loop closure fits, so turning it down saves nothing, and it stays on. A wrong loop closure pulls hard against all the other measurements. Turning it down saves more than the price, so the solver turns it down and the map comes back into shape. The dimmers are found together with the poses by the same solver, so no separate step is needed to find the bad measurements.

## When it applies

- The problem is [pose graph optimization](/pose-graph-optimization/) or a factor graph problem with a least squares cost, solved by [Gauss-Newton](/gauss-newton-algorithm/) or a similar local method.
- Some edges are doubtful, usually loop closures from appearance, and other edges are reliable, usually odometry.
- The wrong edges are a minority, and the reliable edges together give a good first guess.
- There is no time to check each loop closure separately, or the check needs the whole graph.

## The template

Let $O$ be the odometry edges and $L$ the loop closure edges, with errors $e_{ij}(X)$ and information matrices $\Omega_{ij}$. Add one scalar switch $s_{ij}$ for each loop closure and minimize jointly

$$\sum_{(i,j) \in O} e_{ij}^\top \Omega_{ij} e_{ij} + \sum_{(i,j) \in L} \psi(s_{ij})^2\, e_{ij}^\top \Omega_{ij} e_{ij} + \sum_{(i,j) \in L} \lambda\, (1 - s_{ij})^2.$$

1. Choose the switch function $\psi$: a sigmoid, or the linear function $\psi(s) = s$ with $s$ held in $[0, 1]$.
2. Choose the prior weight $\lambda$, the inverse variance of the switch prior. A small $\lambda$ makes switches cheap to turn off; a large one makes the method close to plain least squares.
3. Start every switch at 1 and the poses at the usual first guess, for example the odometry chain.
4. Run the same nonlinear least squares solver on poses and switches together. The new variables are scalars, and each one touches only its own edge, so the sparsity of the problem stays almost the same.
5. Read the final switches. A value near 0 marks a loop closure that the solver rejected.

**The implied robust cost.** With the linear switch, the switch of one edge with squared Mahalanobis error $r^2$ can be eliminated by hand. The term $s^2 r^2 + \lambda (1 - s)^2$ is least at $s = \lambda / (\lambda + r^2)$, and its value there is
$$\rho(r^2) = \frac{\lambda\, r^2}{\lambda + r^2}.$$
This is bounded by $\lambda$ for any error, so one wrong edge can add at most $\lambda$ to the cost. So switchable constraints with a linear switch act like a redescending [M-estimator](/m-estimator/) of the Geman-McClure type on each loop closure.

## Classic examples

**One pose and two loop closures.** Pose $x_0 = 0$ is fixed. Odometry says $x_1 = 1$. Loop closure $a$ says $x_1 = 1.2$, and it is correct. Loop closure $b$ says $x_1 = 4$, and it is wrong. All weights are 1, the switches are linear, and $\lambda = 1$.

- Plain least squares gives $x_1 = (1 + 1.2 + 4) / 3 = 2.067$. The wrong edge moves the pose by almost 1.
- With switches, alternate between the best $x_1$ for fixed switches, $x_1 = (1 + 1.2\,s_a^2 + 4\,s_b^2) / (1 + s_a^2 + s_b^2)$, and the best switches for fixed $x_1$, $s = 1 / (1 + r^2)$. From $x_1 = 2.067$, the switches become $s_a = 0.571$ and $s_b = 0.211$, then $x_1 = 1.145$, then $s_a = 0.997$ and $s_b = 0.109$, then $x_1 = 1.117$. The process ends at $x_1 = 1.116$, $s_a = 0.993$ and $s_b = 0.107$, with the cost 0.913.

The wrong edge is mostly switched off, but not fully. The result 1.116 is close to, but not equal to, 1.1, the least squares answer without the wrong edge.

**Pose graphs with added false loop closures.** Sünderhauf and Protzel added many random false loop closures to standard pose graph data sets and showed that the switchable formulation still recovered the map in their experiments. These are measured results on those data sets, not a guarantee.

## Variations

- **Dynamic covariance scaling.** Agarwal and colleagues eliminated the switch in closed form and applied the result as a scale on the information matrix of each loop closure. This gives the same kind of bounded cost without extra variables.
- **Max-mixtures.** Olson and Agarwal model each doubtful edge by a mixture of a narrow and a wide Gaussian, and take the most likely component in each step.
- **Consistency checks.** RRR of Latif, Cadena and Neira, and pairwise consistency maximization, group loop closures that agree with each other and reject the rest before or during the optimization. Such checks can use [RANSAC](/ransac/)-like ideas.
- **Robust kernels.** Huber, Cauchy and other [M-estimators](/m-estimator/) on loop closures work in a similar way, with a fixed kernel in place of a switch.
- **Certifiable robust methods.** Later work combines outlier models with relaxations like those of [SE-Sync](/se-sync/), at a higher cost.

## Pitfalls

- **A poor first guess.** The joint problem is more nonconvex than the original. If odometry drift is large, a correct loop closure can also have a large error at the start, and its switch goes off. The map then keeps the drift.
- **The prior weight.** With $\lambda$ too large, wrong edges stay on. With $\lambda$ too small, correct edges with a large error, which are the most useful ones, are switched off.
- **Many consistent wrong edges.** Several wrong loop closures that agree with each other, for example from a repeated corridor, can win against the odometry. Switches cannot tell them from correct edges.
- **Partial switches.** A switch that ends between 0 and 1 still pulls the map a little. Inspect the final switch values, and remove clearly rejected edges if the bias matters.
- **Odometry is trusted.** The method assumes that the edges without switches are correct. A wrong odometry edge is not handled.

## Exercises

1. Show that $\min_s s^2 r^2 + \lambda (1 - s)^2$ is attained at $s = \lambda / (\lambda + r^2)$, and that the minimum value is $\lambda r^2 / (\lambda + r^2)$.
2. In the example with one pose, find the value of $x_1$ if the switches are fixed at $s_a = 1$ and $s_b = 0$. Explain why the result of the switched problem differs from it.
3. Give a one-dimensional example with a first guess for which the alternating method switches off the correct loop closure.
4. Explain why adding one scalar variable per loop closure keeps the information matrix sparse, and what new nonzero entries appear.

## References
