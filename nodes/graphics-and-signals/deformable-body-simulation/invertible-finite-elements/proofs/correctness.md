---
title: The signed SVD is valid, the diagonal stress is well defined and rotation equivariant, and the forces are the negative gradient of the energy where the model is not extended
proves: [correctness]
status: full
---

We use the notation of the page, in 2D.
$\operatorname{rot}(t)$ is the rotation by the angle $t$, and $Z = \operatorname{diag}(1, -1)$.
For matrices, $A : B = \operatorname{tr}(A^T B)$.
An element has the rest edge matrix $D_m$ with $\det D_m > 0$, $F = D_s D_m^{-1}$, $V_0 = \det D_m / 2$ and $B_m = -V_0 D_m^{-T}$.

## Step 1: line L4 gives a signed SVD

Write $F = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$ and set $e = (a + d)/2$, $g = (a - d)/2$, $h = (c + b)/2$ and $k = (c - b)/2$.
Then

$$F = \begin{pmatrix} e & -k \\ k & e \end{pmatrix} + \begin{pmatrix} g & h \\ h & -g \end{pmatrix} = q\operatorname{rot}(a_2) + r\operatorname{rot}(a_1) Z,$$

with $q = \sqrt{e^2 + k^2}$, $a_2 = \operatorname{atan2}(k, e)$, $r = \sqrt{g^2 + h^2}$ and $a_1 = \operatorname{atan2}(h, g)$.
Put $\varphi = (a_2 + a_1)/2$, $\theta = (a_2 - a_1)/2$, $\sigma_1 = q + r$ and $\sigma_2 = q - r$.
Since $\operatorname{diag}(\sigma_1, \sigma_2) = qI + rZ$ and $Z\operatorname{rot}(\theta) = \operatorname{rot}(-\theta) Z$,

$$\operatorname{rot}(\varphi)\operatorname{diag}(\sigma_1, \sigma_2)\operatorname{rot}(\theta) = q\operatorname{rot}(\varphi + \theta) + r\operatorname{rot}(\varphi - \theta) Z = F.$$

So $F = U\hat F V^T$ with $U = \operatorname{rot}(\varphi)$, $V = \operatorname{rot}(-\theta)$ and $\hat F = \operatorname{diag}(\sigma_1, \sigma_2)$, and $\det U = \det V = +1$.
As $q, r \ge 0$, $\sigma_1 \ge |\sigma_2|$.
Also $\det F = \sigma_1\sigma_2 = q^2 - r^2$, so $\sigma_2 < 0$ exactly when $\det F < 0$, and then $\sigma_2$ is the entry of smallest magnitude. $\square$

## Step 2: the stress of lines L5 to L7 does not depend on the choice of the SVD when $q > 0$

Let $F = U'\hat F' V'^T$ be any factorization with rotations $U' = \operatorname{rot}(\varphi')$, $V' = \operatorname{rot}(-\theta')$ and $\hat F' = \operatorname{diag}(\sigma_1', \sigma_2')$, $\sigma_1' \ge |\sigma_2'|$.
By the identity of Step 1 it equals $q'\operatorname{rot}(\varphi' + \theta') + r'\operatorname{rot}(\varphi' - \theta') Z$ with $q' = (\sigma_1' + \sigma_2')/2 \ge 0$ and $r' = (\sigma_1' - \sigma_2')/2 \ge 0$.
A matrix of the form $\left(\begin{smallmatrix} e & -k \\ k & e \end{smallmatrix}\right)$ plus one of the form $\left(\begin{smallmatrix} g & h \\ h & -g \end{smallmatrix}\right)$ fixes both parts, because the two sets of matrices are complementary subspaces of the 2 by 2 matrices.
So $q' = q$ and $r' = r$, that is $\hat F' = \hat F$.

Now let $q > 0$, and let $\hat P$ be a map of $(\sigma_1, \sigma_2)$ to a diagonal matrix that is symmetric in its two arguments.
If $r > 0$, then $\varphi' + \theta' = a_2$ and $\varphi' - \theta' = a_1$ modulo $2\pi$, so $\varphi' = \varphi + \pi j$ and $\theta' = \theta + \pi l$ with $j \equiv l \pmod 2$.
So $U' = sU$ and $V' = sV$ with the same sign $s = \pm 1$, and $U'\hat P V'^T = U\hat P V^T$.
If $r = 0$, then $\hat F = qI$, $\hat P = pI$ for one number $p$ by the symmetry, and $U'\hat P V'^T = p\,U'V'^T = p\operatorname{rot}(a_2) = U\hat P V^T$.
So $P = U\hat P(\hat F)V^T$ is a function of $F$ alone on the set $q > 0$. $\square$

The set $q = 0$ is the set of the matrices $rR'Z$ with a rotation $R'$, where $\sigma_1 = -\sigma_2$.
There $U V^T$ is not fixed by $F$, and the stress of the models below is not well defined.
It is a set of measure zero, which this proof leaves out.

## Step 3: rest, rotation equivariance and isotropy

At a rotation $F = Q$ we have $e^2 + k^2 = 1$ and $g = h = 0$, so $\hat F = I$, and both models give $\hat P(I) = 0$: no stress.
For rotations $Q$ and $Q'$, $Q F Q'$ has the signed SVD $(QU)\hat F (Q'^T V)^T$, and $q(QFQ') = q(F)$ by Step 2.
By Step 2, $P(QFQ') = Q U\hat P V^T Q' = Q P(F) Q'$.
This holds for every $F$ with $q > 0$, inverted or not. $\square$

## Step 4: the extension below $c$ is $C^1$, and it is finite for every $F$

Line L5 sets $\tilde\sigma_i = \max(\sigma_i, c)$ with $c > 0$, and line L6 sets $\hat P^{ext}(\sigma) = \hat P(\tilde\sigma) + J(\tilde\sigma)(\sigma - \tilde\sigma)$, where $J$ is the Jacobian of $\hat P$.
The model is only evaluated at $\tilde\sigma_i \ge c > 0$, so $\hat P^{ext}$ is finite for every $\sigma$, including $\sigma_2 \le 0$.
Where both $\sigma_i \ge c$, $\tilde\sigma = \sigma$ and $\hat P^{ext} = \hat P$.

Let $\sigma_i < c$ and $\sigma_j \ge c$.
Then $\tilde\sigma_i = c$ is constant, so $\partial\hat P^{ext}/\partial\sigma_i = J(\tilde\sigma) e_i$.
For $j$, $\tilde\sigma_j = \sigma_j$, and $\partial\hat P^{ext}/\partial\sigma_j = J(\tilde\sigma) e_j + (\partial J/\partial\sigma_j)(\tilde\sigma)(\sigma - \tilde\sigma)$.
As $\sigma_i \to c$ the value tends to $\hat P(\sigma)$ and both derivatives tend to $J(\sigma)e_i$ and $J(\sigma)e_j$, the derivatives of $\hat P$ from the other side.
The same holds when both entries are below $c$.
So $\hat P^{ext}$ and its first derivatives are continuous, given that $\hat P$ is $C^2$ on $\sigma_1, \sigma_2 > 0$, as the neo-Hookean $\hat P$ is.
For the corotated model, $\hat P$ is affine in $\sigma$, so $\hat P^{ext} = \hat P$ for every $c$. $\square$

## Step 5: the two models agree with their usual stresses

**Neo-Hookean.** For $\det F > 0$ the usual stress is $P = \mu(F - F^{-T}) + \lambda\log J\, F^{-T}$ with $J = \det F = \sigma_1\sigma_2$.
With $F = U\hat F V^T$, $F^{-T} = U\hat F^{-1}V^T$, so $P = U\bigl(\mu(\hat F - \hat F^{-1}) + \lambda\log J\,\hat F^{-1}\bigr)V^T$.
The diagonal entries are $\mu\sigma_i - \mu/\sigma_i + \lambda\log J/\sigma_i$, the $\hat P$ of the page.
So where both $\sigma_i \ge c$, line L7 gives the usual neo-Hookean stress.

**Corotated.** Let $R = UV^T$, a rotation, and $S = V\hat F V^T$, symmetric, so $F = RS$.
For $\det F > 0$ this is the polar decomposition.
Then $|F - R|_F^2 = |\hat F - I|_F^2$ and $\operatorname{tr}(S - I) = \sigma_1 + \sigma_2 - 2$, so the energy $\Psi_{cr}(F) = \mu|F - R|_F^2 + \frac{\lambda}{2}\operatorname{tr}(S - I)^2$ is $\hat\Psi(\sigma) = \mu\sum_i(\sigma_i - 1)^2 + \frac{\lambda}{2}(\sigma_1 + \sigma_2 - 2)^2$.
In 2D, $\sigma_1 + \sigma_2 = 2q$ and $R = \operatorname{rot}(a_2)$, so

$$\Psi_{cr}(F) = \mu\bigl(|F|_F^2 - 4q + 2\bigr) + 2\lambda(q - 1)^2,$$

a smooth function of $F$ on the whole set $q > 0$, which contains inverted and flat elements.
From $q^2 = e^2 + k^2$, $dq = \cos a_2\, de + \sin a_2\, dk$, and $R : dF = \cos a_2 (da + dd) + \sin a_2 (dc - db) = 2\,dq$.
So

$$d\Psi_{cr} = 2\mu F : dF - 2\mu R : dF + \lambda(2q - 2)\, R : dF = \bigl(2\mu(F - R) + \lambda\operatorname{tr}(S - I) R\bigr) : dF.$$

This gradient is $U\bigl(2\mu(\hat F - I) + \lambda\operatorname{tr}(\hat F - I) I\bigr)V^T$, which is what line L7 gives with the corotated $\hat P$. $\square$

## Step 6: lines L8 and L9 give the negative gradient of the energy

Let $P = \partial\Psi/\partial F$ at $F$.
Moving node $a \ge 1$ by $\delta$ changes $D_s$ by $\delta e_a^T$, so $dF = \delta e_a^T D_m^{-1}$ and $d(V_0\Psi) = V_0 P : \delta e_a^T D_m^{-1} = \delta^T(V_0 P D_m^{-T}) e_a$.
So the gradient for node $a$ is column $a$ of $V_0 P D_m^{-T} = -P B_m$, and line L8 sets $G = P B_m$, the negative gradient.
Moving node 0 by $\delta$ is the same as moving the other nodes by $-\delta$ and then translating, which does not change $F$, so its force is minus the sum of the others, as in line L9.
Summing over the elements, lines L1 to L9 return $-\nabla E$ for $E = \sum_e V_0\Psi(F_e)$.

With Step 5 this holds for the corotated model at every configuration with $q > 0$ in each element, inverted or not, and for the neo-Hookean model when both $\sigma_i \ge c$ in each element.
Below $c$ the extended neo-Hookean stress is not the gradient of any function of $\sigma$: $\partial\hat P^{ext}_1/\partial\sigma_2 = \lambda/(\sigma_1 c)$, but for $\sigma_2 < c \le \sigma_1$, $\partial\hat P^{ext}_2/\partial\sigma_1 = \lambda/(\sigma_1 c) - \lambda(\sigma_2 - c)/(\sigma_1 c^2)$, and the two differ.
So in that region the force is a finite, $C^1$ and rotation equivariant force, but not a conservative one. $\square$

## Step 7: zero net force and zero net torque

In each element the forces of line L9 sum to 0 by construction.
The torque of the element is the skew part of $\sum_{a \ge 1} (x_a - x_0) f_a^T = D_s G^T = D_s B_m^T P^T = -V_0 D_s D_m^{-1} P^T = -V_0 F P^T$.
With $F = U\hat F V^T$ and $P = U\hat P V^T$, $F P^T = U\hat F\hat P U^T$, which is symmetric because $\hat F$ and $\hat P$ are diagonal.
So the torque is 0 for every diagonal $\hat P$, including the extension below $c$. $\blacksquare$
