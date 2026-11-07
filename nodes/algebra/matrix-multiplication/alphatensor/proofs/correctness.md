---
title: A won game of TensorGame is a correct bilinear algorithm
proves: [correctness, termination]
status: full
---

Let $K$ be the ring of the game: $\mathbb{Z}$, or $\mathbb{Z}/q\mathbb{Z}$ when a modulus $q$ is given. Tensors are arrays indexed by $[nm] \times [mp] \times [np]$ with entries in $K$. For arrays $u$, $v$, $w$ write $(u \otimes v \otimes w)_{abc} = u_a v_b w_c$.

## The invariant

Let $S_t$ be the residual after $t$ moves and $(u^{(r)}, v^{(r)}, w^{(r)})$ the $r$-th move. Then
$$T = S_t + \sum_{r=1}^{t} u^{(r)} \otimes v^{(r)} \otimes w^{(r)} \qquad \text{for every } t \text{ reached}.$$
At line L1, $S_0 = T$ and the sum is empty. Line L4 sets $S_{t+1} = S_t - u^{(t+1)} \otimes v^{(t+1)} \otimes w^{(t+1)}$ entrywise in $K$, and appends the move, so the right side is unchanged. The checks before L4 only reject moves with entries outside F or with wrong shapes; they do not change $S$.

## A won game

If the loop ends with $S_t = 0$, the invariant gives $T = \sum_{r=1}^{t} u^{(r)} \otimes v^{(r)} \otimes w^{(r)}$ in $K$. For $T = \langle n, m, p \rangle$, the entry of $T$ at $((i, j), (j', k), (i', k'))$ is $[j = j'][k = k'][i = i']$. Let $A$ be $n \times m$ and $B$ be $m \times p$ with entries in a ring $R$ that is a $K$-algebra (any ring when $K = \mathbb{Z}$; a ring of characteristic $q$ when $K = \mathbb{Z}/q\mathbb{Z}$). Define $M_r = \big(\sum_{i,j} u^{(r)}_{ij} a_{ij}\big)\big(\sum_{j,k} v^{(r)}_{jk} b_{jk}\big)$. By distributivity, keeping $a$ on the left,
$$\sum_r w^{(r)}_{ik} M_r = \sum_{i_1, j_1, j_2, k_2} \Big(\sum_r u^{(r)}_{i_1 j_1} v^{(r)}_{j_2 k_2} w^{(r)}_{ik}\Big) a_{i_1 j_1} b_{j_2 k_2} = \sum_{i_1, j_1, j_2, k_2} T_{(i_1, j_1), (j_2, k_2), (i, k)}\, a_{i_1 j_1} b_{j_2 k_2} = \sum_{j} a_{ij} b_{jk} = c_{ik}.$$
No commutativity of $R$ is used, so the same holds when the entries are blocks, and the recursive use in `multiply_with` is correct by block multiplication; zero padding does not change the top-left part of the product.

The policy does not appear in this argument. So a won game is correct whatever the policy, the network or the search did.

## The penalty

If the game ends with $S_t \ne 0$, the reward is $-t - \gamma(S_t)$ with $\gamma(S) = \sum_a \operatorname{rank}(S_{a,\cdot,\cdot})$, the ranks of the slices taken over $\mathbb{Q}$ or over $\mathbb{Z}/q\mathbb{Z}$ for prime $q$. This is an upper bound on the tensor rank of $S$: a slice of rank $\rho_a$ is a sum of $\rho_a$ products $g \otimes h$, and $e_a \otimes g \otimes h$ is a rank-one tensor, so $S = \sum_a e_a \otimes S_{a,\cdot,\cdot}$ is a sum of $\sum_a \rho_a$ rank-one tensors. Hence finishing the lost game by the slices would give a correct scheme of rank $t + \gamma(S_t)$, and the reward of the lost game is minus that rank.

## Termination

Each pass through the loop increases $t$ by one, and the loop condition requires $t < R_{\text{limit}}$, so there are at most $R_{\text{limit}}$ passes, each finite. The slice ranks are computed by Gaussian elimination, which is finite. The recursion in `multiply_with` stops because a scheme with $\max(n, m, p) \ge 2$ strictly shrinks at least one side that is larger than the cutoff at each level, and the base case is reached when a side is at most the cutoff.
