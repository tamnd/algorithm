---
title: The corotational force is the exact gradient of the corotated energy, and the warped stiffness is exact only at a rotated rest shape
proves: [correctness]
status: full
---

We use the notation of the page.
An element has $d + 1$ nodes in $d$ dimensions ($d = 2$ for triangles, $d = 3$ for tetrahedra).
$D_m$ and $D_s$ hold the rest and current edge vectors as columns, $F = D_s D_m^{-1}$, and $V_0$ is the rest area or volume.
For matrices, $A : B = \operatorname{tr}(A^T B)$ and $|A|_F^2 = A : A$.
We assume $\det F > 0$.
Then $F$ has a unique polar decomposition $F = R S$ with $R \in SO(d)$ and $S$ symmetric positive definite, and $R$ and $S$ are smooth functions of $F$.

The linear energy density is $\Psi_{lin}(F) = \mu|\varepsilon|_F^2 + \frac{\lambda}{2}(\operatorname{tr}\varepsilon)^2$ with $\varepsilon = \frac12(F + F^T) - I$.
Its stress is $P_{lin}(F) = 2\mu\varepsilon + \lambda(\operatorname{tr}\varepsilon) I$.
The corotated energy density is $\Psi_{cr}(F) = \mu|F - R|_F^2 + \frac{\lambda}{2}\operatorname{tr}(S - I)^2$, where $S = R^T F$.

## Step 1: the linear force of an element is $-K_e (y - X)$

The linear element force at the node positions $y$ is $f_{lin}(y) = -V_0 P_{lin}(F(y)) D_m^{-T}$ for the nodes $1, \dots, d$, and minus their sum for node 0.
$F(y)$ is affine in $y$ with $F(X) = I$, and $P_{lin}$ is affine in $F$ with $P_{lin}(I) = 0$.
So $f_{lin}$ is a linear function of the displacement $y - X$.
A linear map is fixed by its values on the unit vectors.
Line L7 uses the matrix $K_e$ whose column $k$ is $-f_{lin}(X + e_k)$, so $f_{lin}(y) = -K_e (y - X)$ for every $y$. $\square$

## Step 2: lines L5 to L8 compute $-V_0 P_{cr} D_m^{-T}$

Line L6 sets $y_a = R^T x_a$.
The edge matrix of $y$ is $R^T D_s$, so $F(y) = R^T F = S$.
$S$ is symmetric, so $\varepsilon(S) = S - I$ and $P_{lin}(S) = 2\mu(S - I) + \lambda\operatorname{tr}(S - I) I$.
By Step 1, line L7 gives $g = f_{lin}(y) = -V_0 P_{lin}(S) D_m^{-T}$ on the nodes $1, \dots, d$, and minus their sum on node 0.
Line L8 multiplies each nodal vector by $R$, which commutes with the sum, so the force on the nodes $1, \dots, d$ is $-V_0 R P_{lin}(S) D_m^{-T}$.
Now $R P_{lin}(S) = 2\mu(RS - R) + \lambda\operatorname{tr}(S - I) R = 2\mu(F - R) + \lambda\operatorname{tr}(S - I) R$.
Call this matrix $P_{cr}$. $\square$

## Step 3: $P_{cr} = \partial\Psi_{cr} / \partial F$

Expand $|F - R|_F^2 = |F|_F^2 - 2\operatorname{tr}(R^T F) + d$, because $R^T R = I$.
So $\Psi_{cr} = \mu(|F|_F^2 - 2\operatorname{tr} S + d) + \frac{\lambda}{2}(\operatorname{tr} S - d)^2$, and it is enough to show $d(\operatorname{tr} S) = R : dF$.

Differentiate $\operatorname{tr} S = \operatorname{tr}(R^T F)$: $d(\operatorname{tr} S) = \operatorname{tr}(dR^T F) + \operatorname{tr}(R^T dF)$.
$R(t)$ stays in $SO(d)$, so $dR = R W$ with $W$ skew symmetric.
Then $\operatorname{tr}(dR^T F) = \operatorname{tr}(W^T R^T R S) = -\operatorname{tr}(W S) = 0$, because the trace of a product of a skew symmetric and a symmetric matrix is 0.
So $d(\operatorname{tr} S) = R : dF$, and

$$d\Psi_{cr} = 2\mu F : dF - 2\mu R : dF + \lambda\operatorname{tr}(S - I)\, R : dF = P_{cr} : dF. \qquad \square$$

## Step 4: the force is the negative gradient of the energy

The element energy is $V_0\Psi_{cr}(F)$, and $F = D_s D_m^{-1}$ with $D_s$ linear in the nodes.
Moving node $a \ge 1$ by $\delta$ changes $D_s$ by $\delta e_a^T$, so $dF = \delta e_a^T D_m^{-1}$ and $d(V_0\Psi_{cr}) = V_0 P_{cr} : \delta e_a^T D_m^{-1} = \delta^T (V_0 P_{cr} D_m^{-T}) e_a$.
So the gradient for node $a$ is column $a$ of $V_0 P_{cr} D_m^{-T}$.
Moving node 0 by $\delta$ is the same as moving all the other nodes by $-\delta$ and then translating the element, which does not change $F$, so its gradient is minus the sum of the others.
With Step 2, the force of lines L2 to L8 on every node is minus the gradient of $V_0\Psi_{cr}$.
Summing over elements, the loop of lines L2 to L8 gives $-\nabla E_{cr}$ for $E_{cr} = \sum_e V_0\Psi_{cr}(F_e)$. $\square$

## Step 5: rest, rigid motions, net force and torque

If $x = Q X + t$ with $Q \in SO(d)$, then $D_s = Q D_m$ and $F = Q$, so $R = Q$, $S = I$ and $P_{cr} = 0$: no force.
For any rotation $Q$, $QF = (QR) S$ is the polar decomposition of $QF$, so $\Psi_{cr}(QF) = \Psi_{cr}(F)$.
In each element the nodal forces sum to 0 by construction, so the total force is 0.
The torque of one element is the skew part of $\sum_a (x_a - x_0) f_a^T$, and this sum is $-V_0 D_s D_m^{-1} P_{cr}^T = -V_0 F P_{cr}^T$.
Here $F P_{cr}^T = 2\mu(F F^T - F R^T) + \lambda\operatorname{tr}(S - I) F R^T$ and $F R^T = R S R^T$, so it is symmetric and the torque is 0. $\square$

## Step 6: the warped stiffness

The warped stiffness $R K_e R^T$ of line L9 maps a change $dx$ to the force change $-V_0\, dP_w\, D_m^{-T}$ with $dP_w = R\,(2\mu\operatorname{sym}(R^T dF) + \lambda\operatorname{tr}(R^T dF) I)$, by Step 1 applied to $R^T dx$.
The exact change is $dP_{cr} = 2\mu(dF - dR) + \lambda (R : dF) R + \lambda\operatorname{tr}(S - I)\, dR$.
Write $dR = RW$ and $dF = dR\, S + R\, dS$ with $dS$ symmetric.
Then $2 R\operatorname{sym}(R^T dF) = dF + R\, dF^T R = R(WS + dS) + R(-SW + dS)$, and $\operatorname{tr}(R^T dF) = R : dF$.
Subtracting,

$$dP_{cr} - dP_w = R\,\bigl(\mu\,(W(S - I) + (S - I)W) + \lambda\operatorname{tr}(S - I)\, W\bigr).$$

At a rotated rest shape $S = I$, so the difference is 0 and the warped stiffness is the exact Hessian there.
In 2D every skew $W$ is $\omega J$ with $J = \bigl(\begin{smallmatrix}0 & -1\\ 1 & 0\end{smallmatrix}\bigr)$, and $JE + EJ = (\operatorname{tr}E) J$ for a symmetric $E$, so the difference is $(\mu + \lambda)\operatorname{tr}(S - I)\, dR$.
It is not 0 when the element is stretched with $\operatorname{tr}(S - I) \ne 0$ and the change $dx$ turns the element.
So the stiffness of lines L9 and L10 is exact at rest and only approximate elsewhere. $\blacksquare$
