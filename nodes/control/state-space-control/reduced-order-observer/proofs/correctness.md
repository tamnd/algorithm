---
title: The reduced-order observer has the error T^(-1) [0; e] with e' = F e, and F gets the chosen characteristic polynomial
proves: [correctness]
status: full
---

Let $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$ and $C \in \mathbb{R}^{p \times n}$ with $\operatorname{rank} C = p < n$, and let $\alpha$ be a monic real polynomial of degree $n - p$.

## Lemma 1: the coordinates

Line L1 returns $T = [C; V]$ invertible, and in the coordinates $Tx = [y; w]$ the system is

$$\dot y = A_{11} y + A_{12} w + B_1 u, \qquad \dot w = A_{21} y + A_{22} w + B_2 u,$$

with the blocks of line L2.

*Proof.* The loop adds the unit row $e_i^T$ when it is independent of the rows already chosen. The unit rows span $\mathbb{R}^n$, so after the loop the chosen rows span $\mathbb{R}^n$; there are $n$ of them and they are independent, so $T$ is invertible. Let $\xi = Tx$. Then $\dot \xi = TAT^{-1}\xi + TBu$, and the first $p$ entries of $\xi$ are $Cx = y$. Splitting $TAT^{-1}$ and $TB$ after $p$ rows and columns gives the two equations. $\square$

## Lemma 2: the error equation

Let $L \in \mathbb{R}^{(n - p) \times p}$ be any matrix, and let $F, G, H$ be as in line L4. Let $z$ solve $\dot z = Fz + Gy + Hu$, and let $\hat x = T^{-1}[y; z + Ly]$. Then $\varepsilon = w - Ly - z$ satisfies $\dot \varepsilon = F\varepsilon$, and $x - \hat x = T^{-1}[0; \varepsilon]$.

*Proof.* Let $z^\ast = w - Ly$. By Lemma 1,

$$\dot z^\ast = A_{21} y + A_{22} w + B_2 u - L A_{11} y - L A_{12} w - L B_1 u = (A_{22} - L A_{12}) w + (A_{21} - L A_{11}) y + (B_2 - L B_1) u.$$

Substitute $w = z^\ast + Ly$:

$$\dot z^\ast = F z^\ast + (F L + A_{21} - L A_{11}) y + H u = F z^\ast + G y + H u.$$

Subtracting the equation of $z$ gives $\dot\varepsilon = F\varepsilon$. Finally $x = T^{-1}[y; w]$ and $\hat x = T^{-1}[y; z + Ly]$, so $x - \hat x = T^{-1}[0; w - Ly - z] = T^{-1}[0; \varepsilon]$. $\square$

In discrete time the same algebra with $y_{k+1}$ and $w_{k+1}$ in place of $\dot y$ and $\dot w$ gives $\varepsilon_{k+1} = F\varepsilon_k$. The derivative $\dot y$ never appears in the observer, because the term $-L\dot y$ in $\dot z^\ast$ was replaced by its value from the model.

## Lemma 3: observability is inherited

If $(C, A)$ is observable, then $(A_{12}, A_{22})$ is observable.

*Proof.* Observability does not change under a change of coordinates, so $(C T^{-1}, TAT^{-1}) = ([I, 0], \bar A)$ is observable. Suppose $(A_{12}, A_{22})$ is not observable. By the [Popov-Belevitch-Hautus test](/popov-belevitch-hautus-test/) there are $\lambda \in \mathbb{C}$ and $v \ne 0$ with $A_{22} v = \lambda v$ and $A_{12} v = 0$. Then $\xi = [0; v]$ satisfies

$$\bar A \xi = \begin{bmatrix} A_{12} v \\ A_{22} v \end{bmatrix} = \lambda \xi, \qquad [I, 0]\, \xi = 0,$$

so by the same test $([I, 0], \bar A)$ is not observable, a contradiction. $\square$

The converse also holds: if $([I, 0], \bar A)$ has an eigenvector $\xi = [\xi_1; \xi_2]$ with $[I, 0]\xi = 0$, then $\xi_1 = 0$, and $\bar A \xi = \lambda\xi$ gives $A_{12}\xi_2 = 0$ and $A_{22}\xi_2 = \lambda\xi_2$. So the two pairs are observable together, and the algorithm raises an error exactly when $(C, A)$ is not observable.

## Lemma 4: the eigenvalues of F

Line L3 returns $L$ with $\det(sI - (A_{22} - L A_{12})) = \alpha(s)$ whenever $(A_{12}, A_{22})$ is observable.

*Proof.* $(A_{22} - L A_{12})^T = A_{22}^T - A_{12}^T L^T$, and $(A_{22}^T, A_{12}^T)$ is controllable by duality. PLACE returns $K_d$ with $\det(sI - (A_{22}^T - A_{12}^T K_d)) = \alpha(s)$; this is proved on the [Luenberger observer](/luenberger-observer/) page (Heymann's lemma in the form of Hautus, then Ackermann's formula). With $L = K_d^T$, transposition does not change the determinant. $\square$

## Theorem

If $\operatorname{rank} C = p < n$ and $(C, A)$ is observable, the algorithm returns $F, G, H, L, T^{-1}$ with $\det(sI - F) = \alpha(s)$, and for every input and every initial value $z(0)$ the estimate error is $x(t) - \hat x(t) = T^{-1}[0; e^{Ft}\varepsilon(0)]$ (in discrete time $T^{-1}[0; F^k \varepsilon_0]$). If the roots of $\alpha$ are in the open left half plane (inside the unit circle), the error goes to 0. Otherwise the algorithm raises an error.

*Proof.* Lemmas 1 to 4. The checks for $\operatorname{rank} C = p$ and $p < n$ come before line L1. $\square$

## Remark

With $\alpha(z) = z^{n-p}$, the [Cayley-Hamilton theorem](/cayley-hamilton-theorem/) gives $F^{n-p} = 0$, so the estimate is exact from step $n - p$ on, for every input sequence. The tests check this in rational arithmetic.
