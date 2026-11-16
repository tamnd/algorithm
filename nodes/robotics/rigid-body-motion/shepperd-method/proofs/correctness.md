---
title: SHEPPERD returns a unit quaternion of the input rotation
proves: [correctness]
status: full
---

We use the notation of the page.
A quaternion is $q = (w, x, y, z)$ in the Hamilton convention, scalar first, with $ij = k$.
For a unit quaternion $q$, the map $v \mapsto$ the vector part of $q\,(0, v)\,q^*$ is linear, and its matrix $R(q)$ is

$$R(q) = \begin{pmatrix} w^2 + x^2 - y^2 - z^2 & 2(xy - wz) & 2(xz + wy) \\ 2(xy + wz) & w^2 - x^2 + y^2 - z^2 & 2(yz - wx) \\ 2(xz - wy) & 2(yz + wx) & w^2 - x^2 - y^2 + z^2 \end{pmatrix}.$$

With $w^2 + x^2 + y^2 + z^2 = 1$, the diagonal entries become the form $1 - 2(y^2 + z^2)$ and so on that the page uses.
The proof is first in exact arithmetic, and the last section gives a first-order error bound in floating point.

## Every rotation has a unit quaternion

**Lemma 1.** For every $R \in SO(3)$ there is a unit quaternion $q$ with $R(q) = R$, and the unit quaternions with this property are exactly $q$ and $-q$.

*Proof.*
By Euler's rotation theorem, $R = e^{[\hat\omega]\theta}$ for a unit axis $\hat\omega$ and an angle $\theta \in [0, \pi]$.
Put $q = (\cos\frac\theta2, \sin\frac\theta2\,\hat\omega)$.
Expanding $R(q)$ with $c = \cos\frac\theta2$, $s = \sin\frac\theta2$ and the identities $c^2 - s^2 = \cos\theta$, $2cs = \sin\theta$ and $2s^2 = 1 - \cos\theta$ gives $R(q) = \cos\theta\, I + \sin\theta\,[\hat\omega] + (1 - \cos\theta)\hat\omega\hat\omega^{\mathsf T}$, which is Rodrigues' formula, so $R(q) = R$.
The entries of $R(q)$ are quadratic in $q$, so $R(-q) = R(q)$.
Conversely, suppose $R(p) = R(q)$ for unit $p$ and $q$.
Then $R(p^* q) = R(p)^{\mathsf T} R(q) = I$, because $R$ of a product is the product of the matrices and $R(p^*) = R(p)^{\mathsf T}$.
Write $p^* q = (a, b)$ with $b \in \mathbb{R}^3$.
From the diagonal of $R(a, b) = I$ and $a^2 + |b|^2 = 1$ we get $b_1^2 = b_2^2 = b_3^2$ and $1 - 2(b_2^2 + b_3^2) = 1$, so $b = 0$ and $a = \pm 1$.
Hence $q = \pm p$. $\square$

## The ten identities

**Lemma 2.** Let $q$ be a unit quaternion and $R = R(q)$, with $t = r_{11} + r_{22} + r_{33}$.
Then

$$4w^2 = 1 + t, \quad 4x^2 = 1 + 2r_{11} - t, \quad 4y^2 = 1 + 2r_{22} - t, \quad 4z^2 = 1 + 2r_{33} - t,$$

$$4wx = r_{32} - r_{23}, \quad 4wy = r_{13} - r_{31}, \quad 4wz = r_{21} - r_{12}, \quad 4xy = r_{21} + r_{12}, \quad 4xz = r_{13} + r_{31}, \quad 4yz = r_{32} + r_{23}.$$

*Proof.*
From the first form of $R(q)$, $t = 3w^2 - x^2 - y^2 - z^2 = 4w^2 - 1$.
Also $r_{11} = w^2 + x^2 - y^2 - z^2$, so $1 + 2r_{11} - t = (w^2 + x^2 + y^2 + z^2) + 2(w^2 + x^2 - y^2 - z^2) - (3w^2 - x^2 - y^2 - z^2) = 4x^2$.
The cases of $y$ and $z$ are the same with the indices moved.
The six product identities come from the sums and the differences of the symmetric pairs of entries: for example $r_{32} - r_{23} = 2(yz + wx) - 2(yz - wx) = 4wx$ and $r_{21} + r_{12} = 2(xy + wz) + 2(xy - wz) = 4xy$. $\square$

## Line L2 picks the largest square

**Lemma 3.** The index $k$ of line L2 is the index of a largest number among $w^2, x^2, y^2, z^2$, and this number is at least $1/4$.

*Proof.*
By Lemma 2, $4w^2 - 4x^2 = 2(t - r_{11})$, $4x^2 - 4y^2 = 2(r_{11} - r_{22})$, $4y^2 - 4z^2 = 2(r_{22} - r_{33})$, and in the same way $4w^2 - 4y^2 = 2(t - r_{22})$, $4w^2 - 4z^2 = 2(t - r_{33})$ and $4x^2 - 4z^2 = 2(r_{11} - r_{33})$.
So the map $(t, r_{11}, r_{22}, r_{33}) \mapsto (4w^2, 4x^2, 4y^2, 4z^2)$ keeps the order of every pair, and the largest entry of one list has the same index as the largest entry of the other.
The four squares sum to 1, so the largest is at least $1/4$. $\square$

## The branch returns plus or minus q

**Theorem.** For every $R \in SO(3)$, SHEPPERD returns a unit quaternion $p$ with $R(p) = R$ and $p_w \ge 0$.

*Proof.*
Let $q$ be a unit quaternion with $R(q) = R$ (Lemma 1), and let $k$ be the index of line L2.
Write $c_0, c_1, c_2, c_3$ for $w, x, y, z$.
Replace $q$ by $-q$ if needed so that $c_k > 0$; this is possible because $c_k^2 \ge 1/4$ by Lemma 3.
The branch of index $k$ computes $\sqrt{4c_k^2}/2 = |c_k| = c_k$ by the square identity of Lemma 2, and the radicand is at least 1, so the root is defined.
It then divides three product sums by $4c_k \ge 2$, and by the product identities of Lemma 2 each quotient is $4c_k c_j / (4c_k) = c_j$.
So the branch returns exactly $q$.
Line L15 replaces $q$ by $-q$ if $w < 0$.
In both cases the output $p$ is $\pm q$, so it has length 1, $R(p) = R(q) = R$, and $p_w \ge 0$. $\square$

**Uniqueness.** If the rotation angle is less than $\pi$, then $w = \cos\frac\theta2 > 0$, and by Lemma 1 only one of $\pm q$ has $w \ge 0$.
At the angle $\pi$, $w = 0$, and the output is the one of $\pm q$ whose component $k$ is positive.

## Floating point

Let the entries of the input have absolute errors at most $\varepsilon$, with $\varepsilon$ small, and ignore the rounding of the few operations of the method, which adds terms of the order of the unit roundoff $u$.
The selected square $S = 4c_k^2$ is a sum of four entries with coefficients $\pm 1$ (for example $1 + 2r_{11} - t = 1 + r_{11} - r_{22} - r_{33}$), so its error is at most $3\varepsilon$.
The derivative of $\sqrt S / 2$ is $1/(4\sqrt S) = 1/(8c_k)$, and $c_k \ge 1/2$, so the error of $c_k$ is at most $3\varepsilon/4$ to first order.
Each other component is $c_j = N/(4c_k)$, where the numerator $N$ has an error of at most $2\varepsilon$.
To first order,

$$|\delta c_j| \le \frac{|\delta N|}{4c_k} + \frac{|c_j|\,|\delta c_k|}{c_k} \le \frac{2\varepsilon}{2} + 2 \cdot \frac{3\varepsilon}{4} = \frac{5\varepsilon}{2}.$$

So every component has an error of at most $\frac52\varepsilon + O(u)$, for every rotation.

For comparison, the formula that always uses $k = 0$ has $\delta w \le 3\varepsilon/(8w)$ and $|\delta c_j| \approx |c_j|\,\delta w / w$, which is about $3\varepsilon/(8w^2)$ when $|c_j|$ is close to 1.
At the angle $\pi - d$, $w = \sin\frac d2 \approx d/2$, so the error grows like $3\varepsilon/(2d^2)$.
With $\varepsilon$ of the order of $u \approx 1.1 \cdot 10^{-16}$, this is the $u/d^2$ growth of the table on the page.
