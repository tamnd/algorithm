---
title: The forces of the discrete elastic rod are the exact negative gradient of its energy, including the twist term through the holonomy
proves: [correctness]
status: full
---

We use the notation of the page.
The rod has the vertices $x_0, \dots, x_n$ and the edges $e^j = x_{j+1} - x_j$ with unit tangents $t^j$.
At an interior vertex $i$ the edges $a = e^{i-1}$ and $b = e^i$ meet, and we assume $a \cdot b > -|a||b|$, so the rod does not fold back.
$[w]$ is the skew matrix with $[w]y = w \times y$.
The energy is $E = E_s + E_b + E_t$ with

$$E_s = \sum_j \tfrac{k_s}{2}|\bar e^j|\Bigl(\tfrac{|e^j|}{|\bar e^j|} - 1\Bigr)^2, \qquad E_b = \sum_i \frac{\alpha|\kappa b_i|^2}{\bar l_i}, \qquad E_t = \frac{\beta\,\Delta\theta^2}{\bar L}.$$

## Step 1: the curvature binormal

$\kappa b = 2\,a \times b / (|a||b| + a \cdot b)$.
It is perpendicular to $a$ and $b$.
With the turning angle $\varphi$ between $a$ and $b$, $|a \times b| = |a||b|\sin\varphi$ and $a \cdot b = |a||b|\cos\varphi$, so $|\kappa b| = 2\sin\varphi / (1 + \cos\varphi) = 2\tan(\varphi/2)$. $\square$

## Step 2: lines L5 and L6 give $-\nabla(E_s + E_b)$

For one edge, $\partial E_s / \partial e = k_s(|e|/|\bar e| - 1)\,e/|e| = g$, and $e = x_{j+1} - x_j$, so the force is $+g$ on $x_j$ and $-g$ on $x_{j+1}$, as in line L5.

Write $\kappa b = N / D$ with $N = 2\,a \times b$ and $D = |a||b| + a \cdot b$.
Then $dN = 2\,da \times b + 2\,a \times db = -2[b]\,da + 2[a]\,db$ and $dD = (|b|\,a/|a| + b) \cdot da + (|a|\,b/|b| + a) \cdot db$.
By the quotient rule,

$$G_a = \frac{\partial\kappa b}{\partial a} = \frac{-2[b] - \kappa b\,(|b|\,a/|a| + b)^T}{D}, \qquad G_b = \frac{\partial\kappa b}{\partial b} = \frac{2[a] - \kappa b\,(|a|\,b/|b| + a)^T}{D}.$$

Since $a = x_i - x_{i-1}$ and $b = x_{i+1} - x_i$, $\partial\kappa b/\partial x_{i-1} = -G_a$, $\partial\kappa b/\partial x_i = G_a - G_b$ and $\partial\kappa b/\partial x_{i+1} = G_b$.
The term $\alpha|\kappa b|^2/\bar l$ has $\partial/\partial\kappa b = (2\alpha/\bar l)\kappa b$, so its gradient for vertex $k$ is $(2\alpha/\bar l)(\partial\kappa b/\partial x_k)^T\kappa b$.
Line L6 adds minus this to the three vertices. $\square$

## Step 3: parallel transport is the rotation of line L3

For unit $t_1$, $t_2$ with $c = t_1 \cdot t_2 > -1$ and $b = t_1 \times t_2 = \sin\varphi\, k$ for a unit axis $k$, Rodrigues' formula gives the rotation about $k$ by $\varphi$ as $I + \sin\varphi[k] + (1 - c)[k]^2$.
With $[k]^2 = kk^T - I$ and $(1 - c)/\sin^2\varphi = 1/(1 + c)$ this is $P = cI + [b] + bb^T/(1 + c)$, the formula of the code.
It maps $t_1$ to $t_2$ and fixes $b$.
$P$ is also the product $H_m H_{t_1}$ of the reflections $H_n = I - 2nn^T$ with $m = (t_1 + t_2)/|t_1 + t_2|$: $H_{t_1}$ maps $t_1$ to $-t_1$, $H_m$ maps $-t_1$ to $t_2$, both fix $b$, and the product of two reflections is the rotation about the line where their planes meet, by twice the angle between them, which is $\varphi$. $\square$

## Step 4: the variation of the twist (the holonomy)

Let the vertices move smoothly, with the first and the last edges fixed, and write $\delta$ for the derivative.
Let $u^j$ be the Bishop director of edge $j$ and $v^j = t^j \times u^j$, and let $\Psi_j = \delta u^j \cdot v^j$, the rate at which $u^j$ turns about $t^j$.
Since edge 0 is fixed, $u^0$ is fixed and $\Psi_0 = 0$.

From $u^j = P_j u^{j-1}$ and $v^j = P_j v^{j-1}$ (a rotation keeps the cross product),

$$\Psi_j = (\delta P_j\, u^{j-1}) \cdot (P_j v^{j-1}) + (P_j\,\delta u^{j-1}) \cdot (P_j v^{j-1}) = v^{j-1} \cdot (P_j^T \delta P_j)\, u^{j-1} + \Psi_{j-1}.$$

$P_j^T\delta P_j$ is skew, say $[\omega_j]$, and $v \cdot (\omega \times u) = \omega \cdot (u \times v) = \omega \cdot t^{j-1}$, so $\Psi_j - \Psi_{j-1} = t^{j-1} \cdot \omega_j$.

Now compute $t_1 \cdot \omega$ for $P = H_m H_{t_1}$ (Step 3, with $t_1 = t^{j-1}$ and $t_2 = t^j$).
For a unit $n$, $\delta H_n = -2(\delta n\, n^T + n\,\delta n^T)$ and $H_n \delta H_n = 2(n\,\delta n^T - \delta n\, n^T) = 2[\delta n \times n]$.
So $P^T\delta P = H_{t_1}(H_m \delta H_m)H_{t_1} + H_{t_1}\delta H_{t_1} = 2H_{t_1}[\delta m \times m]H_{t_1} + 2[\delta t_1 \times t_1]$.
For a reflection $H$, $H[w]H = -[Hw]$, so $\omega = -2H_{t_1}(\delta m \times m) + 2\,\delta t_1 \times t_1$, and

$$t_1 \cdot \omega = -2\,(H_{t_1}t_1) \cdot (\delta m \times m) = 2\,t_1 \cdot (\delta m \times m) = 2\,\delta m \cdot (m \times t_1).$$

With $s = |t_1 + t_2| = \sqrt{2 + 2c}$, $m \times t_1 = (t_2 \times t_1)/s$, and $\delta m = (I - mm^T)(\delta t_1 + \delta t_2)/s$, where the projection drops out because $m \times t_1 \perp m$.
So $t_1 \cdot \omega = (\delta t_1 + \delta t_2) \cdot (t_2 \times t_1)/(1 + c) = -\tfrac12\kappa b \cdot (\delta t_1 + \delta t_2)$, because $\kappa b = 2\,t_1 \times t_2/(1 + c)$ for unit tangents.
Summing from $\Psi_0 = 0$,

$$\Psi_{n-1} = -\tfrac12\sum_i \kappa b_i \cdot (\delta t^{i-1} + \delta t^i).$$

The last edge and $d_{end}$ are fixed, and $u^{n-1}$, $v^{n-1}$ turn together about $t^{n-1}$ at the rate $\Psi_{n-1}$.
Line L4 measures $\Delta\theta$ with $d_{end} = \cos\Delta\theta\, u^{n-1} + \sin\Delta\theta\, v^{n-1}$, so $\delta\Delta\theta = -\Psi_{n-1}$.
The unwrapping to the value nearest the previous one adds a constant multiple of $2\pi$, which does not change the derivative.

Finally, $\delta t = (I - tt^T)\,\delta e/|e|$ and $\kappa b_i \perp t^{i-1}, t^i$, so $\kappa b_i \cdot \delta t^{i-1} = \kappa b_i \cdot (\delta x_i - \delta x_{i-1})/|e^{i-1}|$ and $\kappa b_i \cdot \delta t^i = \kappa b_i \cdot (\delta x_{i+1} - \delta x_i)/|e^i|$.
With $h^-_i = \kappa b_i/(2|e^{i-1}|)$ and $h^+_i = -\kappa b_i/(2|e^i|)$, the interior vertex $i$ contributes $-h^-_i$ to $\partial\Delta\theta/\partial x_{i-1}$, $-h^+_i$ to $\partial\Delta\theta/\partial x_{i+1}$ and $h^-_i + h^+_i$ to $\partial\Delta\theta/\partial x_i$, and $\partial\Delta\theta/\partial x$ is the sum of these contributions over all interior vertices. $\square$

## Step 5: line L7 gives $-\nabla E_t$

$\partial E_t/\partial x = (2\beta\Delta\theta/\bar L)\,\partial\Delta\theta/\partial x$.
By Step 4 the force $-\partial E_t/\partial x$ adds $c\,h^-_i$ to $x_{i-1}$, $c\,h^+_i$ to $x_{i+1}$ and $-c(h^-_i + h^+_i)$ to $x_i$, with $c = 2\beta\Delta\theta/\bar L$, which is line L7.
The term holds for every motion of the vertices that are not in the two end edges, which is the setting of a rod clamped at both ends.
With Steps 2 and 5, lines L5 to L7 return $-\nabla E$. $\square$

## Step 6: the quasistatic twist energy

With the material angles $\theta^0, \dots, \theta^{n-1}$ of the edges measured from the Bishop frame and the end angles fixed by the clamps, the discrete twist energy is $\sum_i \beta m_i^2/\bar l_i$ with $m_i = \theta^i - \theta^{i-1}$ and $\sum_i m_i = \Delta\theta$.
By the Cauchy-Schwarz inequality, $\Delta\theta^2 = (\sum_i m_i)^2 \le (\sum_i m_i^2/\bar l_i)(\sum_i \bar l_i)$, with equality exactly when $m_i$ is proportional to $\bar l_i$.
So the minimum over the interior angles is $\beta\Delta\theta^2/\bar L$, the term $E_t$.
It depends on the centerline only through $\Delta\theta$, so Step 5 gives the gradient of the minimized energy. $\square$

## Step 7: rigid motions, net force and torque

All the terms use only lengths, dot products and cross products of edges, and $\Delta\theta$ is an angle between vectors that move with the rod.
Under $x \mapsto Qx + t$ with a rotation $Q$, applied also to $u^0$ and $d_{end}$, the transports satisfy $P(Qt_1, Qt_2) = QP(t_1, t_2)Q^T$, so the Bishop frame and $\Delta\theta$ are unchanged, and so is $E$.
$E$ does not change under a translation of all vertices, so its gradients sum to zero; it does not change under a small rotation $\delta x_k = w \times x_k$, so $\sum_k x_k \times \nabla_k E = 0$.
For a free rod (the terms of lines L5 and L6) the net force and the net torque are therefore zero.
A straight rod has $\kappa b_i = 0$ at every vertex, so lines L6 and L7 add nothing and a straight rod at its rest lengths feels no force, for every twist. $\blacksquare$
