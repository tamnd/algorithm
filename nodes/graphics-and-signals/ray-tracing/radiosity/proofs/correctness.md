---
title: The radiosity system is diagonally dominant, Jacobi, Gauss-Seidel and progressive refinement converge, and the sphere zones have exact form factors
proves: [correctness]
status: full
---

Let the patches $P_1, \dots, P_n$ have the areas $A_i > 0$, the reflectances $0 \le \rho_i < 1$ and the emissions $E_i \ge 0$. Let

$$K(x, y) = \frac{\cos\theta_x \cos\theta_y}{\pi |x - y|^2} V(x, y), \qquad F_{ij} = \frac{1}{A_i}\int_{P_i}\int_{P_j} K(x, y)\, dA(y)\, dA(x).$$

Let $M = \operatorname{diag}(\rho) F$, so the system is $B = E + MB$, and let $\rho_{\max} = \max_i \rho_i$.

**Lemma 1 (reciprocity and row sums).** $A_i F_{ij} = A_j F_{ji}$. If the patches cover all the surfaces of a closed scene, then $\sum_j F_{ij} = 1$ for each $i$. In every scene $\sum_j F_{ij} \le 1$.

*Proof.* $K(x, y) = K(y, x)$, so $A_i F_{ij} = \int_{P_i}\int_{P_j} K = \int_{P_j}\int_{P_i} K = A_j F_{ji}$. For a fixed $x$, the change of variables from $y$ to the direction $\omega$ from $x$ to $y$ gives $dA(y) \cos\theta_y / |x - y|^2 = d\omega$. Each direction of the hemisphere above $x$ meets at most one visible point, so $\sum_j \int_{P_j} K(x, y)\, dA(y) \le \frac{1}{\pi}\int_{H^2} \cos\theta\, d\omega = 1$, with equality when each direction meets a surface. Average over $x \in P_i$. $\square$

**Lemma 2 (diagonal dominance).** $I - M$ is strictly diagonally dominant by rows, with the margin at least $1 - \rho_i$ in row $i$. So it is nonsingular, and $B = E + MB$ has exactly one solution.

*Proof.* The diagonal entry is $1 - \rho_i F_{ii} \ge 1 - \rho_i > 0$. The off-diagonal entries of row $i$ have the absolute sum $\rho_i \sum_{j \ne i} F_{ij} \le \rho_i (1 - F_{ii})$ by Lemma 1. The diagonal minus this sum is at least $1 - \rho_i F_{ii} - \rho_i + \rho_i F_{ii} = 1 - \rho_i > 0$. A strictly diagonally dominant matrix is nonsingular: if $(I - M)v = 0$ with $v \ne 0$, take $i$ with $|v_i| = \|v\|_\infty$, and row $i$ gives $|1 - M_{ii}|\,|v_i| \le \sum_{j \ne i} |M_{ij}|\,|v_i|$, which is a contradiction. $\square$

**Lemma 3 (the Neumann series).** $\|M\|_\infty \le \rho_{\max} < 1$, so $B = \sum_{k \ge 0} M^k E$, and the term $M^k E$ is the radiosity carried by light after exactly $k$ reflections.

*Proof.* $M \ge 0$ and row $i$ sums to $\rho_i \sum_j F_{ij} \le \rho_i$. So the series converges in the norm $\|\cdot\|_\infty$, and its sum $S$ satisfies $S = E + MS$. By Lemma 2 this is the solution. The term $M^k E$ applies the transfer $k$ times to the emission. $\square$

**Theorem 1 (Jacobi).** The Jacobi iterates $B^{(k+1)} = E + M B^{(k)}$ satisfy $\|B^{(k)} - B\|_\infty \le \rho_{\max}^k \|B^{(0)} - B\|_\infty$.

*Proof.* Subtract $B = E + MB$: $e^{(k+1)} = M e^{(k)}$, and $\|M\|_\infty \le \rho_{\max}$ by Lemma 3. $\square$

**Theorem 2 (Gauss-Seidel).** The sweep of lines L5 to L7 satisfies $\|e^{\text{new}}\|_\infty \le \rho_{\max} \|e^{\text{old}}\|_\infty$.

*Proof.* Row $i$ of the sweep gives $e_i^{\text{new}} = \sum_{j < i} M_{ij} e_j^{\text{new}} + \sum_{j \ge i} M_{ij} e_j^{\text{old}}$. Suppose $|e_j^{\text{new}}| \le \rho_{\max} \|e^{\text{old}}\|_\infty$ for all $j < i$. These values are at most $\|e^{\text{old}}\|_\infty$, so $|e_i^{\text{new}}| \le \sum_j M_{ij} \|e^{\text{old}}\|_\infty \le \rho_{\max} \|e^{\text{old}}\|_\infty$. Induction on $i$ finishes the proof. $\square$

The stop test of line L8 uses the change $\delta$ of one sweep. Since $\|e^{(k)}\|_\infty \le \|B^{(k+1)} - B^{(k)}\|_\infty + \|e^{(k+1)}\|_\infty \le \delta + \rho_{\max}\|e^{(k)}\|_\infty$, the error at the stop is at most $\delta/(1 - \rho_{\max}) < \varepsilon/(1 - \rho_{\max})$.

**Theorem 3 (progressive refinement).** Let the unshot radiosities start at $\Delta B = E$ with $B = E$, and let each shot of patch $i$ add $\rho_j F_{ji} \Delta B_i$ to $B_j$ and to $\Delta B_j$ for every $j$, after it sets $\Delta B_i$ to 0. Then

1. the invariant $B = E + M(B - \Delta B)$ holds after each shot, and
2. if each shot picks a patch with the largest $A_i \Delta B_i$, the total unshot power $U = \sum_i A_i \Delta B_i$ satisfies $U' \le (1 - (1 - \rho_{\max})/n)\, U$.

So $\Delta B \to 0$, and $B$ converges to the solution.

*Proof.* (1) At the start, $B - \Delta B = 0$ and $B = E$. A shot of patch $i$ with the value $s = \Delta B_i$ changes $B_j$ and $\Delta B_j$ by the same amount for $j \ne i$, and changes $B_i - \Delta B_i$ by $+s$, since $\Delta B_i$ drops by $s$ before it gets the same addition as $B_i$. So $M(B - \Delta B)$ changes in row $j$ by $\rho_j F_{ji} s$, which is the change of $B_j$. The invariant is kept.

(2) The shot removes $A_i s$ from $U$ and adds $\sum_j A_j \rho_j F_{ji} s = \sum_j \rho_j A_i F_{ij} s \le \rho_{\max} A_i s$, by reciprocity and Lemma 1. So $U' \le U - (1 - \rho_{\max}) A_i s$. The patch has the largest of $n$ nonnegative terms, so $A_i s \ge U/n$.

With $\Delta B \ge 0$ and $A_i > 0$, $U \to 0$ gives $\Delta B \to 0$. The invariant can be written $(I - M)B = E - M\Delta B$, so $B = (I - M)^{-1}(E - M\Delta B)$ by Lemma 2, and $B \to (I - M)^{-1}E$. $\square$

The code uses $F_{ij} A_i / A_j$ for $F_{ji}$. If the computed form factors are not exactly reciprocal, the shots solve the system with these values, which differ from the computed $F_{ji}$ by the quadrature error.

**Lemma 4 (the sphere zones).** Inside a sphere of radius $R$, $K(x, y) = 1/(4\pi R^2)$ for all $x \ne y$ on the sphere. So the zone between the heights $z_j$ and $z_{j+1}$ has $F_{ij} = (z_{j+1} - z_j)/(2R)$ for every $i$, and $A_i = 2\pi R (z_{i+1} - z_i)$.

*Proof.* Let $c$ be the center. The triangle $c x y$ is isosceles with the sides $R$, $R$ and $d = |x - y|$. The inner normal at $x$ is $(c - x)/R$, and the angle between it and $y - x$ has the cosine $d/(2R)$. The same holds at $y$. So $K = (d/2R)^2/(\pi d^2) = 1/(4\pi R^2)$. Every point sees every other point on the inside of a sphere, so $V = 1$. Integrate over zone $j$ and average over zone $i$: $F_{ij} = A_j/(4\pi R^2)$. By Archimedes' hat-box theorem, $A_j = 2\pi R (z_{j+1} - z_j)$. $\square$

For the cuts $-1, 0, \frac12, 1$ of the unit sphere, $F_{ij} = (\frac12, \frac14, \frac14)$ in every row. Each row sums to 1, and $A_i F_{ij} = \pi \Delta z_i \Delta z_j$ is symmetric, as Lemma 1 requires. The tests check these identities in exact fractions, and check that the exact Gaussian elimination gives $(\frac{13}{9}, \frac49, \frac29)$, that Jacobi meets the bound of Theorem 1 in exact arithmetic, and that the three iterations reach the exact solution.
