---
title: Laderman's 23 products give the 3×3 matrix product
proves: [correctness, termination]
status: full
---

Let $R$ be a ring: an additive abelian group with an associative multiplication that distributes over addition on both sides. Commutativity is not used. Every product below is written with an entry of $A$ on the left and an entry of $B$ on the right, and the only rules used are distributivity, $x(-y) = -(xy) = (-x)y$, and the laws of the additive group. So every identity holds when the entries are blocks of matrices over $R$ of matching shapes.

## The nine identities

Write $c_{ik} = a_{i1}b_{1k} + a_{i2}b_{2k} + a_{i3}b_{3k}$ for the target, and $M_1, \ldots, M_{23}$ for the products of the table on the main page.

**Four groups.** By distributivity,
$$M_7 + M_8 = (-a_{11}+a_{31})\big((b_{11}-b_{13}+b_{23}) + (b_{13}-b_{23})\big) + a_{32}(b_{11}-b_{13}+b_{23}) = (-a_{11}+a_{31})b_{11} + a_{32}(b_{11}-b_{13}+b_{23}),$$
so with $M_6 = a_{11}b_{11}$,
$$G_1 := M_6+M_7+M_8 = a_{31}b_{11} + a_{32}b_{11} - a_{32}b_{13} + a_{32}b_{23}.$$
In the same way, splitting the left factor of $M_4$ as $(-a_{11}+a_{21}) + a_{22}$ and of $M_{16}$ and $M_{12}$ as $(-a_{13}+a_{23}) + a_{22}$ and $(-a_{13}+a_{33}) + a_{32}$,
$$\begin{aligned}
G_2 &:= M_{14}+M_{16}+M_{17} = a_{23}b_{31} + a_{22}b_{23} + a_{22}b_{31} - a_{22}b_{33}, \\
G_3 &:= M_{12}+M_{13}+M_{14} = a_{33}b_{31} + a_{32}b_{22} + a_{32}b_{31} - a_{32}b_{32}, \\
G_4 &:= M_2+M_4+M_6 = a_{21}b_{11} + a_{22}b_{11} - a_{22}b_{12} + a_{22}b_{22}.
\end{aligned}$$
For $G_4$: $M_2 + M_4 = (a_{11}-a_{21})\big((-b_{12}+b_{22}) - (b_{11}-b_{12}+b_{22})\big) + a_{22}(b_{11}-b_{12}+b_{22}) = -(a_{11}-a_{21})b_{11} + a_{22}(b_{11}-b_{12}+b_{22})$, and adding $M_6$ gives the line. $G_2$ and $G_3$ are the same computation with the indices renamed.

**Completed groups.** Expanding $M_9 = (a_{31}+a_{32})(-b_{11}+b_{13})$, $M_{18} = (a_{22}+a_{23})(-b_{31}+b_{33})$, $M_{15} = (a_{32}+a_{33})(-b_{31}+b_{32})$ and $M_5 = (a_{21}+a_{22})(-b_{11}+b_{12})$ and adding,
$$\begin{aligned}
H_1 &:= G_1 + M_9 = a_{31}b_{13} + a_{32}b_{23}, & H_2 &:= G_2 + M_{18} = a_{22}b_{23} + a_{23}b_{33}, \\
H_3 &:= G_3 + M_{15} = a_{32}b_{22} + a_{33}b_{32}, & H_4 &:= G_4 + M_5 = a_{21}b_{12} + a_{22}b_{22}.
\end{aligned}$$

**Entries with five products.** Using $M_{23} = a_{33}b_{33}$, $M_{21} = a_{21}b_{13}$, $M_{22} = a_{31}b_{12}$ and $M_{20} = a_{23}b_{32}$:
$$\begin{aligned}
c_{33} &= M_6+M_7+M_8+M_9+M_{23} = H_1 + a_{33}b_{33} = a_{31}b_{13}+a_{32}b_{23}+a_{33}b_{33}, \\
c_{23} &= M_{14}+M_{16}+M_{17}+M_{18}+M_{21} = H_2 + a_{21}b_{13}, \\
c_{32} &= M_{12}+M_{13}+M_{14}+M_{15}+M_{22} = H_3 + a_{31}b_{12}, \\
c_{22} &= M_2+M_4+M_5+M_6+M_{20} = H_4 + a_{23}b_{32}.
\end{aligned}$$
Each right side is the wanted $c_{ik}$.

**$c_{21}$ and $c_{31}$.** The long product is
$$M_3 = -a_{22}b_{11} + a_{22}b_{12} + a_{22}b_{21} - a_{22}b_{22} - a_{22}b_{23} - a_{22}b_{31} + a_{22}b_{33}.$$
The table gives $c_{21} = M_2+M_3+M_4+M_6+M_{14}+M_{16}+M_{17} = G_4 + M_3 + G_2$. In this sum the terms $a_{22}b_{11}$, $a_{22}b_{12}$, $a_{22}b_{22}$ from $G_4$ and $a_{22}b_{23}$, $a_{22}b_{31}$, $a_{22}b_{33}$ from $G_2$ cancel with the six matching terms of $M_3$, and what remains is $a_{21}b_{11} + a_{22}b_{21} + a_{23}b_{31}$. In the same way, with
$$M_{11} = -a_{32}b_{11} + a_{32}b_{13} + a_{32}b_{21} - a_{32}b_{22} - a_{32}b_{23} - a_{32}b_{31} + a_{32}b_{32},$$
$c_{31} = G_1 + M_{11} + G_3 = a_{31}b_{11} + a_{32}b_{21} + a_{33}b_{31}$.

**$c_{12}$ and $c_{13}$.** The table gives $c_{12} = M_1 + M_4 + M_5 + M_6 + M_{12} + M_{14} + M_{15} = H_4 - M_2 + H_3 - M_{13} + M_1$. Here
$$\begin{aligned}
-M_2 &= a_{11}b_{12} - a_{11}b_{22} - a_{21}b_{12} + a_{21}b_{22}, \\
-M_{13} &= -a_{13}b_{22} + a_{13}b_{32} + a_{33}b_{22} - a_{33}b_{32}, \\
M_1 &= a_{11}b_{22} + a_{12}b_{22} + a_{13}b_{22} - a_{21}b_{22} - a_{22}b_{22} - a_{32}b_{22} - a_{33}b_{22}.
\end{aligned}$$
Adding these to $H_4 + H_3 = a_{21}b_{12} + a_{22}b_{22} + a_{32}b_{22} + a_{33}b_{32}$, every monomial cancels except $a_{11}b_{12} + a_{12}b_{22} + a_{13}b_{32} = c_{12}$. In the same way $c_{13} = M_6+M_7+M_9+M_{10}+M_{14}+M_{16}+M_{18} = H_1 - M_8 + H_2 - M_{17} + M_{10}$, with
$$\begin{aligned}
-M_8 &= a_{11}b_{13} - a_{11}b_{23} - a_{31}b_{13} + a_{31}b_{23}, \\
-M_{17} &= -a_{13}b_{23} + a_{13}b_{33} + a_{23}b_{23} - a_{23}b_{33}, \\
M_{10} &= a_{11}b_{23} + a_{12}b_{23} + a_{13}b_{23} - a_{22}b_{23} - a_{23}b_{23} - a_{31}b_{23} - a_{32}b_{23},
\end{aligned}$$
and the sum with $H_1 + H_2 = a_{31}b_{13} + a_{32}b_{23} + a_{22}b_{23} + a_{23}b_{33}$ is $a_{11}b_{13} + a_{12}b_{23} + a_{13}b_{33} = c_{13}$.

**$c_{11}$.** $M_6 + M_{14} + M_{19} = a_{11}b_{11} + a_{13}b_{31} + a_{12}b_{21}$.

So all nine identities hold in every ring.

## The recursion

**Claim.** For all $n, m, p \ge 0$ and $n_0 \ge 1$, $\mathrm{LADERMAN}(A, B, n_0)$ returns $AB$ for $A \in R^{n \times m}$ and $B \in R^{m \times p}$.

*Proof by strong induction on $s = n + m + p$.* If $\min(n, m, p) \le n_0$, line L1 returns the classical product, which is $AB$.

Otherwise $n, m, p \ge 2$. If some side is not a multiple of $3$, line L2 pads $A$ to $A' = \begin{pmatrix} A & 0 \\ 0 & 0 \end{pmatrix}$ of size $n' \times m'$ and $B$ to $B' = \begin{pmatrix} B & 0 \\ 0 & 0 \end{pmatrix}$ of size $m' \times p'$, with each side rounded up to a multiple of $3$. Then the top-left $n \times p$ block of $A'B'$ is $AB + 0 \cdot 0 = AB$. The padded call has all sides multiples of $3$ and still has $\min(n', m', p') > n_0$, so it does not reach line L2 again. It reaches line L3, and its correctness is the case below, which only uses the induction hypothesis on calls with smaller side sums.

If all sides are multiples of $3$, line L3 splits $A$ and $B$ into $3 \times 3$ grids of blocks of sizes $h \times k$ and $k \times q$, with $h = n/3$, $k = m/3$, $q = p/3$. By block multiplication, the block $(i, k)$ of $AB$ is $\sum_j A_{ij} B_{jk}$. The factors at line L4 are $h \times k$ and $k \times q$, and $h + k + q \le \lceil n/3 \rceil + \lceil m/3 \rceil + \lceil p/3 \rceil < s$ for the original sides (each $\lceil x/3 \rceil < x$ for $x \ge 2$), so by the induction hypothesis each call returns the true block product $M_r$. Lines L5 and L6 then form the nine sums of the table. Block matrices of these shapes satisfy all the ring laws used in the first part (with $h \times k$ times $k \times q$ products), so the nine identities give $C_{ik} = \sum_j A_{ij} B_{jk}$, which is the block $(i, k)$ of $AB$. $\square$

## Termination

Each recursive call at line L4 has a smaller side sum than the call that made it, measured against the unpadded sides, and the padded call of line L2 goes to line L3 without padding again. So the side sum strictly decreases along every chain of calls, except for one padding step per level, and every chain ends at line L1. Since each side shrinks from $x$ to at most $\lceil x/3 \rceil$ per level, the depth is $O(\log \max(n, m, p))$.
