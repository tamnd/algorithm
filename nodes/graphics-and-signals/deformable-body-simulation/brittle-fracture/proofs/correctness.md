---
title: The stress split, the separation tensor and the local remesh of O'Brien-Hodgins fracture have the properties the method needs
proves: [correctness]
status: full
---

We use the notation of the page, in 2D.
An element has the nodes $a_0, a_1, a_2$, the rest edge matrix $D_m$ with $\det D_m > 0$, $V_0 = \det D_m/2$ and $F = D_s D_m^{-1}$.
For a symmetric $2 \times 2$ matrix $\Sigma$, the nodal forces of $\Sigma$ are the columns $g_1, g_2$ of $G(\Sigma) = -V_0 F\Sigma D_m^{-T}$ on $a_1$ and $a_2$, and $g_0 = -g_1 - g_2$ on $a_0$.
$m(a) = aa^T/|a|$ for $a \ne 0$ and $m(0) = 0$.

## Step 1: the stress split of lines L2 and L3

Let $S = v_1 n_1 n_1^T + v_2 n_2 n_2^T$ with orthonormal eigenvectors.
Line L2 sets $S^+ = \sum_i \max(0, v_i)n_i n_i^T$ and $S^- = S - S^+ = \sum_i \min(0, v_i)n_i n_i^T$.
So $S^+$ has the eigenvalues $\max(0, v_i) \ge 0$ and $S^-$ the eigenvalues $\min(0, v_i) \le 0$, and $S^+S^- = \sum_i \max(0, v_i)\min(0, v_i)n_i n_i^T = 0$, because $n_i^T n_j = 0$ for $i \ne j$ and one of $\max(0, v_i)$ and $\min(0, v_i)$ is zero.
If $v_1 = v_2$, $S$ is a multiple of $I$ and the split does not depend on the choice of the eigenvectors.
$G(\Sigma)$ is linear in $\Sigma$, so $G(S^+) + G(S^-) = G(S)$ and $f^+ + f^- = f$, the rule of line L3. $\square$

## Step 2: the forces are the negative gradient of the energy

The energy of an element is $W = V_0\psi(F)$ with $\psi = \mu|E|_F^2 + \frac{\lambda}{2}\operatorname{tr}(E)^2$ and $E = (F^TF - I)/2$.
Then $d\psi = (2\mu E + \lambda\operatorname{tr}(E)I) : dE = S : dE$, and $dE = (dF^TF + F^TdF)/2$ with $S$ symmetric, so $d\psi = (FS) : dF$.
With $D_s = [x_{a_1} - x_{a_0},\ x_{a_2} - x_{a_0}]$, $dF = dD_s D_m^{-1}$, so $dW = V_0 (FSD_m^{-T}) : dD_s$.
The column $k$ of $dD_s$ is $dx_{a_k} - dx_{a_0}$, so $\partial W/\partial x_{a_k} = V_0(FSD_m^{-T})_{\cdot k} = -g_k$ for $k = 1, 2$ and $\partial W/\partial x_{a_0} = g_1 + g_2 = -g_0$.
Summing over the elements, the forces of line L3 are $-\nabla\sum_e W_e$. $\square$

## Step 3: the separation tensor is symmetric and rotation covariant

Each $m(a)$ is symmetric, so $\varsigma$ of line L4 is symmetric.
It is positive semidefinite: for any $y$, $y^Tm(a)y = (a \cdot y)^2/|a| \ge 0$.

Let all positions move by $x \mapsto Qx + t$ with a rotation $Q$.
Then $D_s \mapsto QD_s$ and $F \mapsto QF$.
$E$ and $S$ depend on $F^TF$ only, so they do not change, and neither do $S^+$ and $S^-$.
So $G(\Sigma) \mapsto QG(\Sigma)$ for $\Sigma = S, S^+$, and every force $f$, $f^+$ and $f^-$ is multiplied by $Q$, as are their sums.
Since $|Qa| = |a|$, $m(Qa) = Qaa^TQ^T/|a| = Qm(a)Q^T$.
Every term of line L4 has this form, so $\varsigma \mapsto Q\varsigma Q^T$.
This matrix has the same eigenvalues, and its eigenvectors are $Qn_i$. $\square$

## Step 4: a node of one element

If only one element meets the node, each sum in line L4 has one term: $\sum f^+ = f^+$ and $\sum m(f^+) = m(f^+)$, and the same for $f^-$.
So $\varsigma = \frac12(-m(f^+) + m(f^+) + m(f^-) - m(f^-)) = 0$, and line L6 never splits that node. $\square$

## Step 5: uniform states at an interior node

Let every element at an interior node $a$ have the same $F$, for example because $x = AX + t$ on the whole patch.
We first show that the forces on $a$ sum to zero.
By Step 2 the forces of an element are $-\nabla W$, and $W$ does not change under a cyclic relabeling of the nodes, which keeps $\det D_m > 0$; so for each element $e$ at $a$ we may call $a$ its node $a_0$.
Then the force on $a$ is $g_0 = -g_1 - g_2 = V_0FSD_m^{-T}\mathbf 1$ with $\mathbf 1 = (1, 1)^T$.
The vector $w = D_m^{-T}\mathbf 1$ satisfies $(X_{a_1} - X_a) \cdot w = (X_{a_2} - X_a) \cdot w = 1$, so it is normal to the edge opposite $a$, points from $a$ toward that edge, and has the length $1/h$ with the height $h$ of the element over that edge.
Since $V_0 = \frac12 h\ell$ with the length $\ell$ of the edge, $V_0w = \frac12\nu_e$, where $\nu_e$ is the normal of the opposite edge that points away from $a$, with the length $\ell$.
The edges opposite $a$ form the boundary of the patch of elements around the interior node $a$, a closed polygon, and the $\nu_e$ are its outward edge normals scaled by the edge lengths, so $\sum_e\nu_e = 0$.
So $\sum_e g_0 = \frac12FS\sum_e\nu_e = 0$.
The same holds for $S^+$ and $S^-$ in place of $S$, so $\sum f^+ = \sum f^- = 0$ at $a$.

If $S$ is negative definite, $S^+ = 0$, so all $f^+ = 0$ and line L4 gives $\varsigma = -\frac12\sum m(f^-)$, which is negative semidefinite by Step 3.
If $S$ is positive definite, $S^- = 0$ and $\varsigma = \frac12\sum m(f^+)$, which is positive semidefinite.
So a uniformly compressed patch never splits at an interior node, for any $\tau \ge 0$. $\square$

## Step 6: the local remesh keeps a valid mesh and the state

**The cut of an edge (line L8).**
Let the element $(v, a, b)$ be positively oriented, and let the new node $p$ have $X_p = (1 - s)X_a + sX_b$ and $x_p = (1 - s)x_a + sx_b$ with $0 < s < 1$.
The two new elements $(v, a, p)$ and $(v, p, b)$ have the signed rest areas $s$ and $1 - s$ times the area of $(v, a, b)$, so both are positive and their areas sum to the old one.
The map from rest to current positions is affine on $(v, a, b)$, with the gradient $F$.
The new node lies on this map, because it uses the same $s$ in both coordinates, so the map is affine with the same $F$ on both new elements.
So the energy density is the same, and the energy, being $V_0\psi(F)$ summed, does not change.
The neighbor $(b, a, w)$ across the edge is cut at the same $p$ into $(b, p, w)$ and $(p, a, w)$, with the same argument.
After the two cuts, the edge $ab$ is replaced by the edges $ap$ and $pb$, each in two elements, and the new edges $vp$ and $pw$ are each in two elements, so the mesh stays conforming.
If the edge $ab$ is on the boundary, only the first cut takes place, and $ap$ and $pb$ are boundary edges.

**The duplication (line L10).**
The copy $a'$ has the same rest position, position and velocity as $a$, and line L10 only renames $a$ to $a'$ in some elements.
So every element keeps its rest shape and its current shape, and the areas, the orientations and the energy do not change.
An element at $a$ has no other copy of $a$, so no element contains both $a$ and $a'$, and no edge gets a third element.

**Mass and momentum (line L11).**
The lumped mass of node $i$ is $m_i = \sum_{e \ni i}\rho V_{0,e}/3 = \int\rho\phi_i\,dX$, where $\phi_i$ is the piecewise linear hat function of $i$; this is the formula of line L11.
The total mass is $\rho$ times the total area, which does not change.
Let $v_h = \sum_i v_i\phi_i$ be the piecewise linear velocity field.
Since $\sum_i\phi_i = 1$, $\sum_i m_iv_i = \int\rho v_h\,dX$.
The cut of an edge gives $p$ the velocity $(1 - s)v_a + sv_b = v_h(X_p)$, so on the new elements the linear interpolation is again $v_h$, and the duplication does not change the velocity of any element.
So $v_h$ is the same field after lines L8 to L10, and the linear momentum $\sum_i m_iv_i$ is the same. $\blacksquare$
