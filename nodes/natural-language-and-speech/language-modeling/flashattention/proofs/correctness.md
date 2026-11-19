---
title: FlashAttention returns softmax(Q K^T / sqrt(d_k) + B) V, takes no exponential of a positive number, and moves n (d_v + 2) + m (d_k + d_v) + T_c n (d_k + 2 d_v + 4) numbers between slow and fast memory
proves: [correctness]
status: full
---

We use the notation of the page. $Q$ is $n \times d_k$, $K$ is $m \times d_k$ and $V$ is $m \times d_v$. For a query row $r$ and a key $c$, write $s_{rc} = Q_r \cdot K_c / \sqrt{d_k}$ if key $c$ is visible to row $r$ and $s_{rc} = -\infty$ otherwise. Every row sees at least one key. The target is

$$O^\ast_r = \frac{\sum_c e^{s_{rc}} V_c}{\sum_c e^{s_{rc}}}.$$

The key blocks $\mathcal{K}_1, \ldots, \mathcal{K}_{T_c}$ partition $\{1, \ldots, m\}$ in order. Write $\mathcal{C}_J = \mathcal{K}_1 \cup \cdots \cup \mathcal{K}_J$, and for a row $r$ let $\mathcal{V}_J(r) = \{ c \in \mathcal{C}_J : s_{rc} > -\infty \}$. We use $e^{-\infty} = 0$.

**Invariant.** After the outer loop at line L2 has handled the blocks $\mathcal{K}_1, \ldots, \mathcal{K}_J$, for every row $r$:

1. if $\mathcal{V}_J(r) = \emptyset$, then $m_r = -\infty$, $\ell_r = 0$ and $O_r = 0$;
2. otherwise $m_r = \max_{c \in \mathcal{V}_J(r)} s_{rc}$, $\ell_r = \sum_{c \in \mathcal{C}_J} e^{s_{rc} - m_r}$, and $O_r = \frac{1}{\ell_r} \sum_{c \in \mathcal{C}_J} e^{s_{rc} - m_r} V_c$.

**Initialization ($J = 0$).** $\mathcal{C}_0$ is empty, and line L1 sets $m_r = -\infty$, $\ell_r = 0$ and $O_r = 0$, which is case 1.

**Maintenance.** Assume the invariant for $J - 1$ and look at block $\mathcal{K}_J$. The inner loop at line L3 visits every query block once, and the rows are updated independently, so fix a row $r$. Line L4 sets $S_{rc} = s_{rc}$ for $c \in \mathcal{K}_J$.

If no key of $\mathcal{K}_J$ is visible to $r$, line L5 skips the row. Then $\mathcal{V}_J(r) = \mathcal{V}_{J-1}(r)$, the new keys add $e^{-\infty} = 0$ to both sums, and the invariant for $J$ is the one for $J - 1$.

Otherwise line L6 computes $\tilde m = \max_{c \in \mathcal{K}_J} s_{rc}$, a finite number, $p_c = e^{s_{rc} - \tilde m}$ and $\tilde\ell = \sum_{c \in \mathcal{K}_J} p_c \ge 1$. Line L7 sets $m' = \max(m_r, \tilde m)$, which is finite and equals $\max_{c \in \mathcal{V}_J(r)} s_{rc}$ in both cases of the hypothesis (in case 1, $m_r = -\infty$ and $m' = \tilde m$). Let $a = e^{m_r - m'}$ and $b = e^{\tilde m - m'}$; both exponents are at most 0, so $0 \le a, b \le 1$. In case 1, $a = 0$. Line L8 gives

$$\ell' = a \ell_r + b \tilde\ell = \sum_{c \in \mathcal{C}_{J-1}} e^{s_{rc} - m_r} e^{m_r - m'} + \sum_{c \in \mathcal{K}_J} e^{s_{rc} - \tilde m} e^{\tilde m - m'} = \sum_{c \in \mathcal{C}_J} e^{s_{rc} - m'},$$

where in case 1 the first sum is 0 on both sides. In the same way, using $\ell_r O_r = \sum_{c \in \mathcal{C}_{J-1}} e^{s_{rc} - m_r} V_c$ from the hypothesis (and $0$ in case 1), line L9 gives

$$\ell' O_r^{\text{new}} = a \ell_r O_r + b \sum_{c \in \mathcal{K}_J} p_c V_c = \sum_{c \in \mathcal{C}_J} e^{s_{rc} - m'} V_c.$$

The division at line L9 is defined because $\ell' \ge b \tilde\ell$ and the term of the key that reaches $m'$ is $e^0 = 1$, so $\ell' \ge 1$. Line L10 stores $m'$ and $\ell'$, so the invariant holds for $J$ in case 2.

**Termination.** The loops are finite. After the last block, $\mathcal{C}_{T_c}$ is all keys and $\mathcal{V}_{T_c}(r)$ is not empty by the precondition, so case 2 holds:

$$O_r = \frac{\sum_c e^{s_{rc} - m_r} V_c}{\sum_c e^{s_{rc} - m_r}} = \frac{e^{-m_r} \sum_c e^{s_{rc}} V_c}{e^{-m_r} \sum_c e^{s_{rc}}} = O^\ast_r.$$

So line L11 returns the attention output. $\square$

**No overflow.** Every exponential the algorithm takes has the form $e^{x - y}$ with $y$ the maximum of a set containing $x$: $s_{rc} - \tilde m$ at line L6, and $m_r - m'$ and $\tilde m - m'$ at lines L8 and L9. So every exponential is in $[0, 1]$, and by the maintenance step $\ell_r \ge 1$ after the first update. In the floating-point model the algorithm therefore never overflows when the scores themselves are finite. $\square$

**Convex updates.** In case 2, line L9 writes $O_r^{\text{new}} = \lambda O_r + (1 - \lambda) \bar V$ with $\lambda = a \ell_r / \ell'$ and $\bar V = \sum_{c \in \mathcal{K}_J} p_c V_c / \tilde\ell$, a convex combination of the visible values of the block. Since $a \ell_r + b \tilde \ell = \ell'$, $\lambda \in [0, 1]$, so each coordinate of $O_r$ stays between the smallest and the largest coordinate of the visible values seen so far. $\square$

**Transfers.** Count the numbers read from or written to slow memory, as the code does. Line L1 writes $O$, $\ell$ and $m$: $n (d_v + 2)$. Over all iterations of line L2, each key and value row is read once: $m (d_k + d_v)$. For each of the $T_c$ key blocks, the inner loop reads every row of $Q$, $O$, $\ell$ and $m$ once, $n (d_k + d_v + 2)$, and line L10 writes every row of $O$, $\ell$ and $m$ once, $n (d_v + 2)$. The total is

$$n (d_v + 2) + m (d_k + d_v) + T_c\, n (d_k + 2 d_v + 4).$$

With $n = m = N$, $d_k = d_v = d$ and $B_c = \lceil M / 4d \rceil$, $T_c = \lceil N / B_c \rceil \le 4 N d / M + 1$, so the total is at most $N (3d + 2) + (4 N d / M + 1) N (3d + 4) = O(N^2 d^2 / M)$ for $d \le M \le N d$, since then $N d \le N^2 d^2 / M$. It is also at least $T_c N \cdot 3d \ge (N / B_c) \cdot 3 N d = \Omega(N^2 d^2 / M)$ when $B_c \le 2M / 4d$, which holds for $M \ge 4d$. $\blacksquare$
