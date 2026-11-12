---
title: iSLIP returns a matching, is maximal after enough iterations, and desynchronizes its grant pointers within N - 1 slots under saturation
proves: [correctness]
status: full
---

We use the pseudocode of the page, with ports numbered $0, \ldots, N-1$ and all pointer arithmetic modulo $N$.

**Lemma 1 (a matching).** In each slot, the matched pairs form a matching, and each pair $(i, j)$ has $req[i][j] = 1$.

*Proof.* An output grants only an unmatched input that requested it (line L4), and an input accepts only a grant that it received (line L6). In one iteration each output grants at most one input and each input accepts at most one output, and matched ports take no part in later iterations of the slot (line L2 skips them). By induction on the iterations, no port is in two pairs. $\square$

**Lemma 2 (maximality).** If an iteration starts with a request $(i, j)$ between an unmatched input and an unmatched output, the iteration adds at least one pair. So with $N$ iterations the matching of the slot is maximal.

*Proof.* Output $j$ gets the request of input $i$, so it grants some input $i'$. Input $i'$ has a grant, so it accepts one. Each iteration that starts with an open request therefore adds a pair, and there can be at most $N$ pairs. If an iteration starts with no open request, the matching is maximal, and it stays so. $\square$

**Theorem (desynchronization under saturation).** Assume every input has a cell for every output in every slot. Then, from any grant and accept pointers and for any number of iterations, after at most $N - 1$ slots the grant pointers $g[0], \ldots, g[N-1]$ are pairwise distinct. From then on they stay distinct and every slot is a perfect matching. The bound $N - 1$ is reached when all grant pointers start equal.

*Proof.* Only the first iteration of a slot changes pointers (line L8), so we look only at it. In the first iteration all ports are unmatched and all requests are present, so output $j$ grants input $g[j]$. Let $s_v$ be the number of outputs whose grant pointer is $v$. Input $v$ gets $s_v$ grants. If $s_v \ge 1$ it accepts exactly one of them, and that output moves its pointer to $v + 1$ (line L10). The other $s_v - 1$ outputs keep the pointer $v$. So after the slot

$$s'_v = \max(s_v - 1, 0) + [s_{v-1} \ge 1]. \tag{1}$$

Call $v$ *empty* when $s_v = 0$. We want no empty position, which is the statement that the $N$ pointers are distinct, since $\sum_v s_v = N$.

*Step 1.* If $v$ is empty after a slot, then $v - 1$ was empty before it. This is the second term of (1).

*Step 2.* Assume some position $x$ is empty after slot $T = N - 1$. By Step 1, applied $T$ times, the position $y_k = x - (T - k)$ is empty after $k$ slots, for $k = 0, 1, \ldots, T$. Measure positions relative to this moving empty point: let $m_k(r)$ be the number of outputs with pointer $y_k + r$ after $k$ slots, for $r = 0, \ldots, N-1$. Then $m_k(0) = 0$. Since $y_{k+1} = y_k + 1$, an output whose pointer moves by one keeps its relative position, and an output whose pointer stays drops by one. From each occupied relative position exactly one output moves. So, for $0 \le k < T$,

$$m_{k+1}(r) = [m_k(r) \ge 1] + \max(m_k(r+1) - 1, 0) \quad (r \le N - 2), \qquad m_{k+1}(N-1) = [m_k(N-1) \ge 1],$$

where the last equation uses $m_k(0) = 0$: no output stays behind at the empty point.

*Step 3.* By induction on $j$, for $0 \le j \le T$, each $r \ge N - j$ has $m_j(r) \le 1$. For $j = 0$ there is no such $r$. If it holds for $j$, then for $r \ge N - j - 1$ with $r \le N - 2$ we have $r + 1 \ge N - j$, so $m_j(r+1) \le 1$, the second term is 0, and $m_{j+1}(r) \le 1$. For $r = N - 1$ the last equation gives $m_{j+1}(N-1) \le 1$.

*Step 4.* Since $m_{k+1}(0) = 0$ for $k < T$, the equation for $r = 0$ gives $\max(m_k(1) - 1, 0) = 0$, so $m_k(1) \le 1$ for $k \le T - 1$. Take $k = T - 1 = N - 2$. By Step 3, $m_k(r) \le 1$ for $r \ge 2$; also $m_k(1) \le 1$ and $m_k(0) = 0$. So $\sum_r m_k(r) \le N - 1$. But the sum is the number of outputs, $N$. This contradiction shows that no position is empty after $N - 1$ slots.

*Stability.* If all $s_v = 1$, then (1) gives $s'_v = 0 + 1 = 1$. Each input gets exactly one grant and accepts it, so the first iteration already gives a perfect matching, and the pointers all move by one and stay distinct.

*Tightness.* If all pointers start at the same value $v$, then $s_v = N$, and (1) shows that after $k$ slots the positions $v, \ldots, v + k$ are occupied, with $s_v = N - k$, and all other positions are empty. The last empty position disappears after exactly $N - 1$ slots. $\blacksquare$

**Remark (RRM).** Under the same saturation, RRM moves the grant pointer of every output past the granted input whether or not it is accepted. All outputs with pointer $v$ grant input $v$ and all move to $v + 1$. So equal pointers stay equal forever, and with all pointers equal each slot matches exactly one pair: the throughput is $1/N$ per port, which is $1/2$ for $N = 2$.
