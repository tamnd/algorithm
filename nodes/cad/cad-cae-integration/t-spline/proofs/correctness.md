---
title: T-spline blending functions are tensor B-splines on a full grid and combinations of them on any T-mesh
proves: [correctness]
status: full
---

We use the representation and the pseudocode of the page: a T-mesh in index space with lines $0..m$ and $0..n$, knot values $sv$ and $tv$, the four outer lines on each side complete, and the anchors $(i, j)$ with $2 \le i \le m - 2$ and $2 \le j \le n - 2$. $N[x_0, \ldots, x_4]$ is the cubic B-spline on the knots $x_0 \le \cdots \le x_4$, and $B_a = N[sv_a, \ldots, sv_{a+4}]$ and $B_b = N[tv_b, \ldots, tv_{b+4}]$ are the global B-splines.

**Lemma 1 (the rays are defined).** For each anchor, lines L2 to L4 find two lines in each direction.

*Proof.* For $i \le m - 2$ the ray to the right passes the columns $m - 1$ and $m$, which are complete, so each of them contains $(k, j)$ on a vertical edge. The same holds to the left with the columns 1 and 0, since $i \ge 2$, and for the rows. $\square$

**Lemma 2 (full grid).** If the T-mesh is the full grid, the anchors are all $(i, j)$ with $2 \le i \le m - 2$ and $2 \le j \le n - 2$, the local index vectors of $(i, j)$ are $(i - 2, \ldots, i + 2)$ and $(j - 2, \ldots, j + 2)$, and $T_{(i, j)} = B_{i-2}(s)\, B_{j-2}(t)$. So EVALUATE returns the tensor product NURBS surface with control points $P_{(i,j)}$ and weights $w_{(i,j)}$.

*Proof.* In the full grid every point $(k, j)$ lies on a vertical edge and on a horizontal edge, so every point is a vertex, and the first two columns to the right of $i$ that meet the ray are $i + 1$ and $i + 2$. The same holds in the other directions. Line L5 then returns the windows of five consecutive knots, which are the knots of $B_{i-2}$ and $B_{j-2}$. The number of anchors is $(m - 3)(n - 3)$, the number of tensor B-splines. Lines L6 to L10 compute the quotient of the two sums, which is the NURBS formula. $\square$

**Lemma 3 (one insertion).** Let $t_0 \le \cdots \le t_4$ with $t_0 < t_4$, let $u$ satisfy $t_0 \le u \le t_4$, and let $\tau_0 \le \cdots \le \tau_5$ be the sorted list of $t_0, \ldots, t_4, u$. Then

$$N[t_0, \ldots, t_4] = c_0\, N[\tau_0, \ldots, \tau_4] + c_1\, N[\tau_1, \ldots, \tau_5]$$

with $c_0 = 1$ if $u \ge t_3$ and $c_0 = (u - t_0)/(t_3 - t_0)$ otherwise, and $c_1 = 1$ if $u \le t_1$ and $c_1 = (t_4 - u)/(t_4 - t_1)$ otherwise.

*Proof.* Extend $t$ to a knot vector of any spline space that contains $N[t_0, \ldots, t_4]$ as one of its B-splines, with the coefficient 1 on it and 0 on the others. Boehm's rule for inserting $u$ gives the new coefficients $\alpha_k c_k + (1 - \alpha_k) c_{k-1}$, with $\alpha_k = (u - t_k)/(t_{k+3} - t_k)$ clamped to $[0, 1]$. Only two new coefficients involve the old coefficient 1: the one of the new B-spline that starts at $\tau_0 = t_0$, which is $\alpha = \min(1, (u - t_0)/(t_3 - t_0))$, and the one of the new B-spline that ends at $\tau_5 = t_4$, which is $1 - \alpha'$ with $\alpha' = \max(0, (u - t_1)/(t_4 - t_1))$, that is $\min(1, (t_4 - u)/(t_4 - t_1))$. All the other new coefficients are 0. Boehm's rule keeps the spline as a function, so the identity holds. $\square$

**Lemma 4 (column $A$ of $M$).** After line L12, $N[s_A] = \sum_a d_a B_a$ and $N[t_A] = \sum_b e_b B_b$, where each sum runs over the global B-splines whose index knots lie between the first and the last index of $s_A$ (and $t_A$). Hence, with the entries of line L13,

$$T_A(s, t) = \sum_{a, b} M[(a, b), A]\, B_a(s)\, B_b(t).$$

*Proof.* Line L12 inserts the missing index lines one at a time. Each insertion replaces one B-spline by two by Lemma 3, so the sum of the current pieces is always equal to $N[s_A]$. A piece is split by a line $x$ only if $x$ lies strictly between its first and last index lines and is not one of them, so after all lines $x$ in the range have been tried, each piece has five consecutive index lines: it is some $B_a$. The pieces with the same index lines are added. The same holds for $t$. The product of the two sums is $T_A$. $\square$

**Theorem (correctness).** EVALUATE returns $S(s, t) = \sum_A w_A P_A T_A / \sum_A w_A T_A$, where $T_A$ is the product of the cubic B-splines on the local knot vectors inferred by the ray rule. On a full grid this is the NURBS surface. On every T-mesh, $S$ is the NURBS surface on the global knot vectors with the homogeneous control points $Q_{(a, b)} = \sum_A M[(a, b), A]\, (w_A P_A, w_A)$. Each $T_A$ is nonnegative and is zero outside $[s_{A,0}, s_{A,4}] \times [t_{A,0}, t_{A,4}]$.

*Proof.* The rays are defined by Lemma 1. Line L8 computes $T_A$ from the knots of line L5, and lines L9 and L10 form the quotient, so EVALUATE returns $S$. The full grid case is Lemma 2. By Lemma 4,

$$\sum_A (w_A P_A, w_A)\, T_A = \sum_{a, b} \Big( \sum_A M[(a, b), A]\, (w_A P_A, w_A) \Big) B_a B_b = \sum_{a, b} Q_{(a, b)}\, B_a B_b,$$

and dividing the first three coordinates by the last gives the NURBS surface with those homogeneous points. A cubic B-spline is nonnegative and is zero outside its first and last knot, so the product $T_A$ has the stated sign and support. $\square$

**Remark (what is not claimed).** The theorem does not say that the $T_A$ are linearly independent or that they sum to 1. Linear independence holds if and only if $M$ has full column rank, by Theorem 1 of Li, Zheng, Sederberg, Hughes and Scott (2012), and it can fail. Partition of unity holds for analysis-suitable T-meshes with suitable boundary lines, a cited result. The tests check both for the example of the page, exactly, at sample points and by the rank of $M$. $\blacksquare$
