---
title: GRAPPA is exact when the coil maps have a finite k-space support that the kernel spans and the calibration data are rich enough
proves: [correctness]
status: full
---

The setting is that of the algorithm, in exact arithmetic and with $\lambda = 0$ (any exact solution of the normal equations of line L3). k-space is indexed by $\kappa = (\kappa_1, \kappa_2) \in \mathbb{Z}_n^2$, with the phase encoding index first and wrap-around in both indices. The scan keeps the rows $\kappa_1 \equiv 0 \pmod R$ and the ACS rows, a block of consecutive rows where every sample is known. For the offset $\delta \in \{1, \ldots, R-1\}$, the kernel has the source offsets $O_\delta = \{(-\delta + R t, d) : t \in T,\ |d| \le w\}$ for a fixed set $T$ of integers, and predicts

$$\hat x_a(\kappa) = \sum_{b=1}^{c} \sum_{o \in O_\delta} W_\delta[(b, o)][a]\; x_b(\kappa + o) \qquad \text{for } \kappa_1 \equiv \delta \pmod R.$$

**Model (H1).** The coil k-space is a convolution of the object k-space with a kernel of finite support: there are a finite set $H \subset \mathbb{Z}^2$ and numbers $h_b(e)$ with

$$x_b(\kappa) = \sum_{e \in H} h_b(e)\, X(\kappa - e) \quad \text{for all } \kappa \text{ and } b,$$

where $X$ is the k-space of the object. This holds when each map $s_b$ is a trigonometric polynomial whose image frequencies lie in $H$, because multiplication in the image is circular convolution in k-space. Real maps are smooth but not band-limited, so (H1) holds only approximately for them.

Let $U_\delta = \{o - e : o \in O_\delta \cup \{(0,0)\},\ e \in H\}$, the set of object samples, relative to $\kappa$, that the sources and the target depend on. Define the source matrix $S_\delta$ with a row for each source $(b, o)$ and a column for each $u \in U_\delta$, $S_\delta[(b,o)][u] = h_b(o - u)$ (zero when $o - u \notin H$), and the target matrix $T_\delta[a][u] = h_a(-u)$. By (H1), $x_b(\kappa + o) = \sum_u S_\delta[(b,o)][u]\, X(\kappa + u)$ and $x_a(\kappa) = \sum_u T_\delta[a][u]\, X(\kappa + u)$.

**Theorem.** Assume (H1). Fix $\delta$, and suppose:
1. (span) every row of $T_\delta$ lies in the row space of $S_\delta$;
2. (rich calibration) the matrix $P_\delta$ whose rows are the vectors $(X(\kappa + u))_{u \in U_\delta}$, for the target positions $\kappa$ used in the fit of line L2, has full column rank $|U_\delta|$.

Then the weights $W_\delta$ of line L3 satisfy $\hat x_a(\kappa) = x_a(\kappa)$ for every coil $a$ and every $\kappa$ with $\kappa_1 \equiv \delta \pmod R$. If this holds for every $\delta$, GRAPPA returns the full k-space of every coil. Every sample it reads was acquired.

*Proof.* Reading. For a target row $\kappa_1 \equiv \delta$, the source rows are $\kappa_1 - \delta + Rt \equiv 0 \pmod R$, which the scan keeps. In the fit, line L2 uses only target rows whose source rows lie inside the ACS block. So the method reads only acquired samples.

Existence. By the span assumption there is a matrix $W^\star$ with $\sum_{(b,o)} W^\star[(b,o)][a]\, S_\delta[(b,o)][u] = T_\delta[a][u]$ for all $a$ and $u$, that is, $S_\delta^{\mathsf T} W^\star = T_\delta^{\mathsf T}$.

Calibration. The rows of the calibration matrix of line L2 are the source vectors $(x_b(\kappa + o))_{(b,o)}$ for the fit positions $\kappa$, so the calibration matrix is $A = P_\delta S_\delta^{\mathsf T}$, and the right side is $B = P_\delta T_\delta^{\mathsf T}$. Then $A W^\star = B$, so the least squares problem $\min_W \lVert A W - B \rVert^2$ has the value 0, and every solution $W$ of the normal equations (with $\lambda = 0$) is a minimizer and satisfies $A W = B$. Hence $P_\delta (S_\delta^{\mathsf T} W - T_\delta^{\mathsf T}) = 0$. $P_\delta$ has full column rank, so $S_\delta^{\mathsf T} W = T_\delta^{\mathsf T}$: the fitted kernel is exact on the level of the object samples.

Prediction. For any $\kappa$ with $\kappa_1 \equiv \delta$,

$$\hat x_a(\kappa) = \sum_{(b,o)} W[(b,o)][a] \sum_u S_\delta[(b,o)][u]\, X(\kappa + u) = \sum_u T_\delta[a][u]\, X(\kappa + u) = x_a(\kappa).$$

Lines L4 to L8 apply this to every missing row, and the acquired rows are kept, so the output is the full k-space. $\square$

**Remarks.**
- The span assumption needs at least as many independent sources as the dimension of the span of the target rows. For the band maps of the tests ($H = \{0, 1\}^2$), $R = 2$, two source rows and three columns, $U$ has 16 elements and there are $4 \cdot 6 = 24$ sources. The tests find the error below $10^{-6}$, which is consistent with the span assumption for those maps; the rank is not proved here.
- The calibration assumption fails, for example, when the ACS block is too narrow for the kernel, or when the object k-space vanishes on a pattern inside the ACS block. Then the fit has several exact solutions, and some of them are wrong outside the ACS block.
- With $\lambda > 0$ the weights solve a Tikhonov problem; as $\lambda \to 0$ they tend to the solution of least norm of the normal equations, which is exact under the assumptions, so the theorem holds in the limit.
- For real coils, (H1) is an approximation, and GRAPPA is an approximate method. The size of the error is a measurement.
