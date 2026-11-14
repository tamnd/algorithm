---
title: Transfinite interpolation reproduces the four boundary sides exactly and reproduces bilinear data
proves: [correctness, termination]
status: full
---

**Claim.** Let $B_0, \ldots, B_M$, $T_0, \ldots, T_M$, $L_0, \ldots, L_N$ and $R_0, \ldots, R_N$ be points of $\mathbb{R}^d$ with $M, N \ge 1$ and with common corners

$$B_0 = L_0 = P_{00}, \quad B_M = R_0 = P_{10}, \quad T_0 = L_N = P_{01}, \quad T_M = R_N = P_{11},$$

and let $0 = u_0 < u_1 < \cdots < u_M = 1$ and $0 = v_0 < \cdots < v_N = 1$. Let $x_{ij}$ be the output of TFI. Then:

1. $x_{i0} = B_i$, $x_{iN} = T_i$, $x_{0j} = L_j$ and $x_{Mj} = R_j$ for all $i$ and $j$;
2. if there is a map $F(u, v) = a + b\,u + c\,v + e\,uv$ with $a, b, c, e \in \mathbb{R}^d$ such that the side points are $B_i = F(u_i, 0)$, $T_i = F(u_i, 1)$, $L_j = F(0, v_j)$ and $R_j = F(1, v_j)$, then $x_{ij} = F(u_i, v_j)$ for all $i, j$;
3. with int or Fraction input, the computed values are exactly these values, and CHECK returns true exactly when every cell has four positive corner Jacobians.

TFI stops after $(M + 1)(N + 1)$ iterations of its inner loop, and CHECK after $4MN$ orientation tests.

**Notation.** Lines L5 to L8 compute

$$x_{ij} = U_{ij} + V_{ij} - C_{ij}, \qquad U_{ij} = (1 - u_i) L_j + u_i R_j, \quad V_{ij} = (1 - v_j) B_i + v_j T_i,$$
$$C_{ij} = (1 - v_j)\big((1 - u_i) P_{00} + u_i P_{10}\big) + v_j \big((1 - u_i) P_{01} + u_i P_{11}\big).$$

**Step 1 (the bottom side).** Take $j = 0$, so $v_0 = 0$. Then $V_{i0} = B_i$, $U_{i0} = (1 - u_i) L_0 + u_i R_0 = (1 - u_i) P_{00} + u_i P_{10}$ by the corner conditions, and $C_{i0} = (1 - u_i) P_{00} + u_i P_{10}$. So $U_{i0} - C_{i0} = 0$ and $x_{i0} = B_i$.

**Step 2 (the top side).** Take $j = N$, so $v_N = 1$. Then $V_{iN} = T_i$, $U_{iN} = (1 - u_i) L_N + u_i R_N = (1 - u_i) P_{01} + u_i P_{11}$, and $C_{iN} = (1 - u_i) P_{01} + u_i P_{11}$. So $x_{iN} = T_i$.

**Step 3 (the left and right sides).** Take $i = 0$, so $u_0 = 0$. Then $U_{0j} = L_j$, $V_{0j} = (1 - v_j) B_0 + v_j T_0 = (1 - v_j) P_{00} + v_j P_{01}$, and $C_{0j} = (1 - v_j) P_{00} + v_j P_{01}$. So $x_{0j} = L_j$. For $i = M$, $u_M = 1$ gives $U_{Mj} = R_j$ and $V_{Mj} = C_{Mj} = (1 - v_j) P_{10} + v_j P_{11}$, so $x_{Mj} = R_j$. This proves part 1. The corner conditions are used in each step: without them, $U - C$ or $V - C$ is not zero on the side, and the side is not reproduced.

**Step 4 (the projector form).** Part 1 is a case of a general fact about projectors, which also gives part 2. For a function $G$ on the unit square, let

$$(P_u G)(u, v) = (1 - u)\, G(0, v) + u\, G(1, v), \qquad (P_v G)(u, v) = (1 - v)\, G(u, 0) + v\, G(u, 1).$$

Both are linear, and both are idempotent: $P_u G$ is linear in $u$ with the values $G(0, v)$ and $G(1, v)$ at $u = 0$ and $u = 1$, so $P_u P_u G = P_u G$. They commute, because $P_u P_v G$ and $P_v P_u G$ are both the bilinear function with the values $G(0,0)$, $G(1,0)$, $G(0,1)$, $G(1,1)$ at the corners. The Boolean sum is

$$P_u \oplus P_v = P_u + P_v - P_u P_v, \qquad I - P_u \oplus P_v = (I - P_u)(I - P_v).$$

For any $G$ with the given values on the boundary of the square, $(P_u \oplus P_v) G$ at $(u_i, v_j)$ is $x_{ij}$, because $P_u G$ uses only $G(0, \cdot)$ and $G(1, \cdot)$, $P_v G$ uses only $G(\cdot, 0)$ and $G(\cdot, 1)$, and $P_u P_v G$ uses only the corners. Now $(I - P_u) H$ is zero on $u = 0$ and $u = 1$ for every $H$, and $(I - P_v) H$ is zero on $v = 0$ and $v = 1$. Since the projectors commute, $(I - P_u)(I - P_v) G = (I - P_v)(I - P_u) G$ is zero on all four sides, which is part 1 again.

**Step 5 (bilinear data).** Let $F = a + b u + c v + e uv$. For fixed $v$ it is linear in $u$, so $P_u F = F$. Then $P_u P_v F = P_v P_u F = P_v F$, and $(P_u \oplus P_v) F = F + P_v F - P_v F = F$. The side points of part 2 are the values of $F$ on the boundary, so by Step 4, $x_{ij} = ((P_u \oplus P_v) F)(u_i, v_j) = F(u_i, v_j)$. This proves part 2. The same argument shows that any $F$ that is linear in $u$ alone, or in $v$ alone, is reproduced.

**Step 6 (exactness and CHECK).** Lines L5 to L8 use only additions, subtractions and multiplications of the input values with $u_i$, $v_j$ and $1 - u_i$, $1 - v_j$. With int or Fraction values, each of these operations is exact, so the computed $x_{ij}$ are the values of Steps 1 to 5 and the equalities of part 1 hold as exact equalities. CHECK computes the four values ORIENT2D$(q_{k-1}, q_k, q_{k+1})$ for each cell with corners $q_0 = x_{ij}$, $q_1 = x_{i+1,j}$, $q_2 = x_{i+1,j+1}$, $q_3 = x_{i,j+1}$. The value at $q_k$ equals $\det(q_{k+1} - q_k,\ q_{k-1} - q_k)$, because ORIENT2D does not change under a cyclic shift of its arguments, and this is the Jacobian determinant of the bilinear map of the cell from the unit square at that corner. For example, at $q_1$ the two vectors are the $v$ edge $q_2 - q_1$ and the reversed $u$ edge $q_0 - q_1$, and $\det(x_v, -x_u) = \det(x_u, x_v)$. The values are exact, so CHECK returns true exactly when all $4MN$ values are positive. This proves part 3.

**Step 7 (termination).** The loops of L3 and L4 run over the finite ranges $0..M$ and $0..N$, and each iteration does a fixed number of operations on $d$ coordinates. The loop of L10 runs over $MN$ cells with four tests each. So both procedures stop. $\blacksquare$

**What the claim does not say.** The claim does not say that the grid is valid. TFI is a linear formula in the boundary data, and nothing in it keeps the interior map one to one. The test file has a hook-shaped side of a simple domain whose TFI grid has four cells that fail CHECK, two of them with all four corner values negative. Validity has to be checked after the grid is made, and an [elliptic grid](/elliptic-grid-generation/) is the usual repair.
