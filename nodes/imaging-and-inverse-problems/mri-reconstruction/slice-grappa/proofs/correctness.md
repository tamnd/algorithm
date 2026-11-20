---
title: Slice-GRAPPA separates the slices exactly when the coil maps have a finite k-space support that the kernel spans
proves: [correctness]
status: full
---

The setting is that of the algorithm, in exact arithmetic and with $\lambda = 0$ (any exact solution of the normal equations of line L4). There are $S$ slices and $c$ coils. The k-space of coil $b$ of slice $z$ is $x_{z,b}(\kappa)$ on $\mathbb{Z}_n^2$, with the unitary DFT. The shifts $\Delta_z$ are integers. The CAIPI shift of line L1 multiplies row $\kappa_1$ by $e^{-2\pi i \kappa_1 \Delta_z / n}$, which is the k-space of the slice image moved by $\Delta_z$ rows, $f(i - \Delta_z, j)$. Write $\tilde x_{z,b}$ for the shifted k-space. The collapsed data are

$$y_b(\kappa) = \sum_{z=1}^{S} \tilde x_{z,b}(\kappa).$$

The kernel of slice $z$ uses the offsets $O$ of a $k_r \times k_c$ patch and predicts $\hat{\tilde x}_{z,a}(\kappa) = \sum_{b, o} W_z[(b,o)][a]\, y_b(\kappa + o)$. Line L8 undoes the shift.

**Model (H1).** For each slice $z$ there are a finite set $H \subset \mathbb{Z}^2$ and numbers $h_{z,b}(e)$ with $x_{z,b}(\kappa) = \sum_{e \in H} h_{z,b}(e)\, X_z(\kappa - e)$, where $X_z$ is the k-space of the object of slice $z$. This holds when the maps of every slice are trigonometric polynomials with image frequencies in $H$.

**Lemma 1.** Under (H1), the shifted k-space also satisfies (H1) with the same $H$: $\tilde x_{z,b}(\kappa) = \sum_{e \in H} \tilde h_{z,b}(e)\, \tilde X_z(\kappa - e)$, where $\tilde X_z$ is the k-space of the shifted object and $\tilde h_{z,b}(e) = e^{-2\pi i e_1 \Delta_z / n} h_{z,b}(e)$.

*Proof.* Multiply (H1) by $e^{-2\pi i \kappa_1 \Delta_z/n} = e^{-2\pi i (\kappa_1 - e_1)\Delta_z/n}\, e^{-2\pi i e_1 \Delta_z/n}$. The first factor turns $X_z(\kappa - e)$ into $\tilde X_z(\kappa - e)$, and the second goes into the coefficient. Both factors are periodic in $\kappa_1$ with period $n$ because $\Delta_z$ is an integer. $\square$

Let $U = \{o - e : o \in O \cup \{(0,0)\},\ e \in H\}$. The unknowns near $\kappa$ are the $S |U|$ numbers $\tilde X_{z'}(\kappa + u)$. By Lemma 1, each source $y_b(\kappa + o)$ is $\sum_{z', u} S[(b,o)][(z',u)]\, \tilde X_{z'}(\kappa + u)$ with $S[(b,o)][(z',u)] = \tilde h_{z',b}(o - u)$, and the target $\tilde x_{z,a}(\kappa)$ is $\sum_{z',u} T_z[a][(z',u)]\, \tilde X_{z'}(\kappa + u)$ with $T_z[a][(z',u)] = \tilde h_{z,a}(-u)$ if $z' = z$ and 0 otherwise.

**Theorem.** Assume (H1) and integer shifts. Fix a slice $z$, and suppose:
1. (span) every row of $T_z$ lies in the row space of $S$;
2. (rich calibration) the matrix $P$ whose rows are $(\tilde X_{z'}(\kappa + u))_{z', u}$, for the calibration positions $\kappa$ of line L3, has full column rank $S |U|$.

Then line L7 gives $\hat{\tilde x}_{z,a}(\kappa) = \tilde x_{z,a}(\kappa)$ for every coil $a$ and every $\kappa$, and line L8 returns $x_{z,a}$.

*Proof.* The calibration of lines L1 to L3 sums the shifted single-slice calibration data into a synthetic collapsed k-space, so its patches are $P S^{\mathsf T}$, and the targets of slice $z$ are $P T_z^{\mathsf T}$. The rest is the argument of the [GRAPPA proof](/grappa/): by the span assumption an exact $W^\star$ with $S^{\mathsf T} W^\star = T_z^{\mathsf T}$ exists, so the least squares fit has the value 0, every solution $W$ satisfies $P(S^{\mathsf T} W - T_z^{\mathsf T}) = 0$, and full column rank of $P$ gives $S^{\mathsf T} W = T_z^{\mathsf T}$. Applied to the collapsed data at any $\kappa$, the kernel then returns $\sum_{z',u} T_z[a][(z',u)]\, \tilde X_{z'}(\kappa + u) = \tilde x_{z,a}(\kappa)$. Line L8 multiplies by $e^{2\pi i \kappa_1 \Delta_z/n}$, which undoes the shift. $\square$

**Remarks.**
- The kernel must cancel the other slices exactly. The span assumption therefore needs more sources than for in-plane GRAPPA: for the band maps of the tests ($H = \{0,1\}^2$), a $3 \times 3$ kernel, two slices and four coils, there are 36 sources for $2 \cdot 16 = 32$ unknowns. The tests find the error below $10^{-3}$ with the small regularization of the code, which is consistent with the assumption; the rank is not proved here.
- The theorem does not need a CAIPI shift. The shift changes the conditioning of the fit and the noise of the result: with the shift, the aliased copies of the slices fall on different coil profiles. The gain is a measurement.
- With a non-integer shift, the phase ramp is not periodic on the grid, and Lemma 1 fails.
- For real coils, (H1) is an approximation, and the slice leakage is a measurement.
