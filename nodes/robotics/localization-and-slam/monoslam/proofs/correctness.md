---
title: The filter steps of the planar MonoSLAM core are the EKF steps they claim to be
proves: [correctness]
status: full
---

**Setting.** This proof is about the toy core in `impl/python/monoslam.py`, not about the full system of Davison, Reid, Molton and Stasse (2007). The world is a plane. The state is the camera $c = (x, y, \theta, v_x, v_y, \omega)$ and the map points $p_1, \dots, p_m$, two numbers each, with a mean $\mu$ and a covariance $\Sigma$ of size $n = 6 + 2m$. A point at $(a, b)$ in the camera frame, with $a > 0$, gives the pixel $u = F b / a$, read with Gaussian noise of variance $r$.

**Claim.** (1) The prediction of line L1 computes $F \Sigma F^\top + G Q G^\top$ for the constant velocity model, and changes only the camera rows and columns. (2) Lines L3 to L5 are an EKF update with one scalar reading, and the gate of line L4 accepts a reading that follows the model with probability 0.99. (3) The depth samples of line L6 hold the posterior of the depth on a grid of 100 values, under the stated independence approximation. (4) The augmentation in `add_point` is the first-order covariance of the joint state with the new point. (5) The deletion of line L8 is an exact marginalization. (6) One frame costs $O(k m^2)$ time with $k$ readings and needs $O(m^2)$ memory. None of this makes the filter exact or consistent: the projection is not linear, so the EKF is a local approximation (see the end).

## (1) The prediction

The model of each frame of length $\Delta t$ is the one of Davison et al. for each coordinate: an unknown velocity change $V \sim N(0, q)$ enters at the start of the frame, then the camera moves with the new velocity. For the $x$ coordinate, $x' = x + (v_x + V) \Delta t$ and $v_x' = v_x + V$, and the same for $y$ and for $\theta$ with $\omega$. With $q = (\sigma_a \Delta t)^2$ for the linear velocities and $q = (\sigma_\alpha \Delta t)^2$ for the angular one, a random acceleration of standard deviation $\sigma_a$ over the frame gives this velocity change. The map points do not move.

The model is linear: $\mu' = F \mu$ and $s' = F s + G w$, where $F$ is the identity with $F_{0,3} = F_{1,4} = F_{2,5} = \Delta t$, and $G w$ adds $V \Delta t$ to the position and $V$ to the velocity. So the new mean is $F \mu$, which is what the code computes, and the new covariance is $F \Sigma F^\top + G Q G^\top$. For one pair (position $i$, velocity $j$) with noise $q$, $G Q G^\top$ has the entries $q \Delta t^2$ at $(i, i)$, $q \Delta t$ at $(i, j)$ and $(j, i)$ and $q$ at $(j, j)$, which are the four additions in the code.

$F$ differs from the identity only in the camera rows, so $F \Sigma$ changes only the camera rows of $\Sigma$, and $(F \Sigma) F^\top$ changes only its camera columns. The code does these two steps in place: first the six camera rows, then the six camera entries of each row. The map block $\Sigma_{mm}$ is not touched, and the cross block becomes $F_c \Sigma_{cm}$, where $F_c$ is the $6 \times 6$ camera part. The test `test_prediction_moves_only_the_camera` compares the result with the dense product on a full random covariance.

## (2) The update of one point and the gate

For the point $p_i$ at index $k$, the predicted pixel is $\hat u = h(\mu)$, with $h(c, p_i) = F b / a$, and the code linearizes at the current mean: $h(s) \approx \hat u + H (s - \mu)$, where $H$ has nonzero entries only at the camera pose $(x, y, \theta)$ and at $p_i$.

The derivatives are the chain rule. With $(\delta_x, \delta_y) = p_i - (x, y)$, $a = \cos\theta\, \delta_x + \sin\theta\, \delta_y$ and $b = -\sin\theta\, \delta_x + \cos\theta\, \delta_y$, we have $\partial u / \partial a = -F b / a^2$ and $\partial u / \partial b = F / a$. Next $\partial a / \partial p_i = (\cos\theta, \sin\theta)$ and $\partial b / \partial p_i = (-\sin\theta, \cos\theta)$, the derivatives by $(x, y)$ are the negatives of these, and $\partial a / \partial \theta = b$, $\partial b / \partial \theta = -a$. These are the formulas of `project_jac`; the test compares them with central differences.

The innovation is $\nu = u - \hat u$ and its variance is $S = H \Sigma H^\top + r$, a number. The Kalman gain is $K = \Sigma H^\top / S$. The update $\mu \leftarrow \mu + K \nu$ and $\Sigma \leftarrow \Sigma - K (H \Sigma) = \Sigma - \Sigma H^\top H \Sigma / S$ is the EKF update. The code forms $\Sigma H^\top$ once, from the five nonzero entries of $H$, and then subtracts the outer product $K (\Sigma H^\top)^\top$; this is the same matrix, because $H \Sigma = (\Sigma H^\top)^\top$ for a symmetric $\Sigma$. The result stays symmetric.

The code updates with one point at a time, and it computes $H$ again at the new mean before the next point. For a linear model with independent reading noises, a sequence of scalar updates gives exactly the joint update with all the readings: the posterior after both readings is the same Gaussian whatever the order, since each update multiplies the density by one Gaussian factor. For the nonlinear model the two differ to second order, and the sequential form uses the newer linearization point.

The gate. If the model holds, $\nu \sim N(0, S)$, so $\nu^2 / S$ follows the chi-square distribution with one degree of freedom, and $P(\nu^2 / S > 6.635) = 0.01$. Line L4 accepts the reading only if $\nu^2 / S \le 6.635$, the value `CHI2[(1, 0.99)]`. The width of the gate in pixels is $\sqrt{6.635\, S}$; this is the planar form of the search ellipse.

## (3) The depth samples

A new point starts as a ray from the camera position $o$ at the angle $\phi$ of its first reading, and its depth $d$ is unknown. The code keeps the values $d_j = 0.5 + 4.5 (j + 0.5) / 100$ for $j = 0, \dots, 99$, which are uniform on $[0.5, 5]$ m, with the log weights $\ell_j = 0$, a uniform prior on the grid.

When a later frame reads the point at $u$, each sample gives the point $o + d_j (\cos\phi, \sin\phi)$, the pixel $\hat u_j$ and the variance $s_j = H_j \Sigma_{cc} H_j^\top + r$, where $H_j$ holds the derivatives by the camera pose. The code adds $\log N(u; \hat u_j, s_j)$, up to a constant that is the same for all $j$, to $\ell_j$. By Bayes' rule on the finite set $\{d_j\}$, $p(d_j \mid u_{1:t}) \propto p(d_j) \prod_\tau p(u_\tau \mid d_j)$, so the normalized weights $w_j \propto \exp(\ell_j)$ are the posterior, if the readings of different frames are independent given $d$. That is an approximation: the readings also depend on the camera poses, whose errors are correlated from frame to frame. Samples behind the camera get the weight zero.

`stats` returns the mean $\bar d = \sum_j w_j d_j$ and the variance $\sum_j w_j (d_j - \bar d)^2$ of this discrete posterior. It subtracts the largest $\ell_j$ before the exponential, which changes no normalized weight and avoids an underflow of all the weights.

The example of the page. For $n$ equal weights on points with spacing $h$, the variance is $h^2 (n^2 - 1) / 12$. At the start $h = 0.045$ and $n = 100$, so the standard deviation is $0.045 \sqrt{9999 / 12} = 1.299$ m, the mean is 2.75 m, and the ratio is 0.472. The page uses the continuous value $4.5 / \sqrt{12} = 1.30$ m. If only the 22 samples in $[1.5, 2.5]$ keep their weight, from 1.5125 m to 2.4575 m, the mean is 1.985 m and the standard deviation is $0.045 \sqrt{483 / 12} = 0.285$ m, a ratio of 0.144, below the threshold 0.3. The test `test_depth_samples_page_example` checks these numbers.

## (4) The new map point

When the ratio drops below 0.3, the code puts the point into the filter with the function $g(x, y, \theta, u, d) = (x, y) + d (\cos\beta, \sin\beta)$, where $\beta = \theta + \operatorname{atan}(u / F)$ is the bearing of the present reading and $d$ is the distance from the present camera position to the ray point at the mean depth. The inputs $u$ and $d$ are treated as independent of the state, with the variances $r$ and $\sigma_d^2$ (the variance of the depth samples).

Let $J_c$, $J_u$ and $J_d$ be the derivatives of $g$ by the camera pose, by $u$ and by $d$. To first order $p - g(\mu, u, d) = J_c (c - \mu_c) + J_u \epsilon_u + J_d \epsilon_d$, with the three terms independent. So the covariance of $p$ with any state entry $s_j$ is $J_c \Sigma_{c, j}$, and the covariance of $p$ with itself is $J_c \Sigma_{cc} J_c^\top + J_u r J_u^\top + J_d \sigma_d^2 J_d^\top$. These are the two new rows and columns that `add_point` appends. The derivatives are $J_c = [[1, 0, -d \sin\beta], [0, 1, d \cos\beta]]$, $J_d = (\cos\beta, \sin\beta)$ and $J_u = d (-\sin\beta, \cos\beta) \cdot F / (F^2 + u^2)$, since $\operatorname{d} \operatorname{atan}(u / F) / \operatorname{d}u = F / (F^2 + u^2)$. The test `test_add_point_covariance` compares all of this with central differences of $g$.

Two approximations remain, and they make the new point more certain than it should be. The depth was estimated with the help of the camera estimate, so it is not independent of the state. And $\sigma_d^2$ is the spread along the first ray, used here along the present one.

## (5) Deleting a point

Line L8 deletes a point that was in view in at least 10 frames and was not found in more than half of them. The code removes its two entries from $\mu$ and its two rows and columns from $\Sigma$. For a Gaussian, the marginal of the other variables has the mean and the covariance with these entries removed, so the deletion is exact marginalization and the rest of the filter is unchanged. The test `test_delete_points_that_fail` checks that the arrays stay consistent.

## (6) Cost

Let $n = 6 + 2m$. The prediction changes 6 rows of length $n$ and 6 entries in each of $n$ rows, with at most two terms per entry, so it costs $O(m)$. Each scalar update computes $\Sigma H^\top$ from five columns, $O(n)$, and subtracts an outer product, $O(n^2)$. Line L3 costs $O(1)$ per point. So $k$ readings cost $O(k m^2)$, and the frame loop over the $m$ points adds $O(m)$. Each ray costs $O(100)$ per frame, and the number of rays is at most the target. The augmentation is $O(m)$ for the new rows plus the appends, and a deletion is $O(m^2)$ at most, which happens at most once per point. The covariance needs $O(m^2)$ memory. This is the bound of the page.

## What is not proved

The EKF linearizes $u = F b / a$ at the mean. The posterior is Gaussian only if the model is linear, so for this model the filter is an approximation, and its error depends on how far the mean is from the true state compared with the curvature of the projection. The filter can become overconfident, as nonlinear [EKF SLAM](/ekf-slam/) can. The test `test_simulation_measurement` is a measurement of this toy, not a proof: on three seeds the camera moves 1.5 m to the side, the known points leave the view, and the final camera error stays below 5 cm, while the prediction alone ends more than 0.5 m off.
