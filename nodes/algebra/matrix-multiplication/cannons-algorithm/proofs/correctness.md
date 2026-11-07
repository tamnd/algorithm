---
title: Cannon's schedule computes AB, and its BSP cost
proves: [correctness, termination]
status: full
---

Let $R$ be a semiring (addition associative and commutative with a zero, multiplication associative and distributive on both sides); commutativity of the multiplication and subtraction are not used. Let $q \ge 1$. The matrix $A$ is split into $q \times q$ blocks $A_{ik}$ of size $s_1 \times s_2$, and $B$ into blocks $B_{kj}$ of size $s_2 \times s_3$, after padding with zeros so that $q$ divides each side. All indices of blocks and processors are taken modulo $q$, in $\{0, \ldots, q-1\}$.

## Padding

Let $A'$ and $B'$ be $A$ and $B$ with zero rows and columns added at the bottom and right. Then the top-left block of $A'B'$ of the size of $AB$ equals $AB$, because each added row of $A'$ or column of $B'$ is zero, and each added column of $A'$ meets an added row of $B'$, so it contributes only products with a zero factor. So it is enough to prove that the schedule computes $A'B'$; from now on $A$ and $B$ denote the padded matrices.

## The skew

Line L2 sends the $A$ block of $(i, j)$ to $(i, j - i)$. For fixed $i$ the map $j \mapsto j - i$ is a bijection of $\mathbb{Z}/q$, so each processor $(i, j')$ receives exactly one $A$ block, from $(i, j' + i)$, namely $A_{i, i + j'}$. In the same way line L2 sends the $B$ block of $(i, j)$ to $(i - j, j)$, a bijection of the column for fixed $j$, so $(i', j)$ receives $B_{i' + j, j}$. So after line L2, processor $(i, j)$ holds $A_{i, k}$ and $B_{k, j}$ with $k = i + j$.

## The loop

**Invariant.** At the start of the pass with index $t$ of line L3, for $0 \le t \le q - 1$, processor $(i, j)$ holds $A_{i, k_t}$ and $B_{k_t, j}$ with $k_t = i + j + t \pmod q$, and
$$C_{ij} = \sum_{u = 0}^{t - 1} A_{i,\, i + j + u}\, B_{i + j + u,\, j}.$$

*Initialization.* For $t = 0$ the sum is empty, which matches line L1, and the blocks are those of the skew.

*Maintenance.* Line L4 adds $A_{i, k_t} B_{k_t, j}$ to $C_{ij}$, which extends the sum to $u = t$. If $t < q - 1$, line L5 sends the $A$ block of every $(i, j)$ to $(i, j - 1)$ and the $B$ block to $(i - 1, j)$. These are bijections, so $(i, j)$ receives the $A$ block of $(i, j + 1)$, which is $A_{i,\, i + (j + 1) + t} = A_{i, k_{t+1}}$, and the $B$ block of $(i + 1, j)$, which is $B_{(i+1) + j + t,\, j} = B_{k_{t+1}, j}$. So the invariant holds at the start of pass $t + 1$.

*End.* After pass $t = q - 1$, $C_{ij} = \sum_{u=0}^{q-1} A_{i,\, i+j+u} B_{i+j+u,\, j}$. As $u$ runs over $\{0, \ldots, q - 1\}$, $i + j + u \bmod q$ runs over every residue exactly once, so, since addition is commutative and associative,
$$C_{ij} = \sum_{k=0}^{q-1} A_{ik} B_{kj},$$
which is block $(i, j)$ of $AB$ by block multiplication. In each product the $A$ block is on the left. $\square$

## Termination

The loop of line L3 has $q$ passes, each local product at line L4 is a finite sequential computation, and each exchange moves a finite number of blocks. So the schedule ends after the skew and $q$ passes.

## The BSP cost

Let $q$ divide the sides and $s_1 = n/q$, $s_2 = m/q$, $s_3 = p/q$.

- *Supersteps.* The skew is one superstep, and each of the $q$ passes is one (the work of L4, then the exchange of L5 if $t < q - 1$). So $S = q + 1$.
- *Work.* In each pass every processor does one product of an $s_1 \times s_2$ and an $s_2 \times s_3$ block, $s_1 s_2 s_3$ multiplications and as many additions. Over $q$ passes this is $q s_1 s_2 s_3 = nmp/q^2$ multiplications per processor, the same on every processor.
- *Communication.* In the skew, each processor sends at most one $A$ block and one $B$ block and, by the bijections above, receives at most one of each. So the skew is an $h$-relation with $h \le s_1 s_2 + s_2 s_3$, with equality when $q \ge 2$, because processor $(1, 1)$ then sends both of its blocks to other processors. Each exchange at line L5 with $q \ge 2$ moves every block to a different processor, so $h = s_1 s_2 + s_2 s_3$. There are $q - 1$ such exchanges. So
$$H = q(s_1 s_2 + s_2 s_3) = \frac{nm + mp}{q},$$
which is $2n^2/q = 2n^2/\sqrt P$ for square matrices. For $q = 1$ nothing moves and $H = 0$.

The BSP cost is $W + gH + LS = 2n^3/P + 2g\,n^2/\sqrt P + L(\sqrt P + 1)$ for $n \times n$ matrices and $P = q^2$ processors, counting both multiplications and additions in $W$.
