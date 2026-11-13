---
title: Alpha-beta returns a value with the stated relation to the window, so the full window gives the negamax value
proves: [correctness, termination]
status: full
---

We use the pseudocode ALPHABETA of the page, in negamax form. The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/), and EVALUATE gives each terminal node its value for the side to move there. Let $N(n)$ be the [negamax](/negamax/) value: $N(t) = \text{EVALUATE}(t)$ at a terminal node and $N(n) = \max_c (-N(c))$ over the children $c$ of an inner node. The negamax page proves that $N(n)$ is the minimax value for the side to move at $n$. The *height* $h(n)$ is 0 at a terminal node and $1 + \max_c h(c)$ otherwise.

Values are real numbers or $\pm\infty$, compared in the usual order. A *window* is a pair $(\alpha, \beta)$ with $\alpha < \beta$. Line L2 sets $m \leftarrow -\infty$ in the fail-soft form and $m \leftarrow \alpha$ in the fail-hard form, which is the procedure F2 of Knuth and Moore.

**Theorem 1 (fail-hard and fail-soft bounds).** Let $\alpha < \beta$ and let $r = $ ALPHABETA$(n, \alpha, \beta)$ in either form. Then

1. if $N(n) \le \alpha$ then $r \le \alpha$,
2. if $\alpha < N(n) < \beta$ then $r = N(n)$,
3. if $N(n) \ge \beta$ then $r \ge \beta$.

In the fail-soft form, also

4. if $r \le \alpha$ then $N(n) \le r$,
5. if $r \ge \beta$ then $N(n) \ge r$.

The three cases of 1 to 3 cover all values of $N(n)$ and they give disjoint ranges of $r$, so the converse of each also holds: $r \le \alpha$ implies $N(n) \le \alpha$, $\alpha < r < \beta$ implies $r = N(n)$, and $r \ge \beta$ implies $N(n) \ge \beta$.

*Proof.* By induction on $h(n)$, for all windows at once. The call stops, because each call makes calls only on children, which have a smaller height.

If $h(n) = 0$, line L1 returns $r = N(n)$, and all five claims hold.

Let $h(n) > 0$ with children $c_1, \ldots, c_k$ in the order of line L3. Let $m_0$ be the value set by line L2 and $m_i$ the value of $m$ after the child $c_i$, so $m_i = \max(m_{i-1}, t_i)$ with $t_i = -$ALPHABETA$(c_i, -\beta, -a_i)$ and $a_i = \max(m_{i-1}, \alpha)$. Let $j$ be the index of the child at which line L6 returns, or $j = k$ when no cutoff happens; then $r = m_j$. Write $w_i = -N(c_i)$, the value of the move to $c_i$ for the side to move at $n$, so $N(n) = \max_i w_i$.

*Step 1: each $t_i$ bounds $w_i$ in the window $(a_i, \beta)$.* The call on $c_i$ has the window $(-\beta, -a_i)$. We have $a_i < \beta$, because $a_1 = \max(m_0, \alpha) = \alpha < \beta$ and, for $i > 1$, the loop went on after child $i-1$, so $m_{i-1} < \beta$. So the induction hypothesis applies to $c_i$. After the negation it says: if $w_i \ge \beta$ then $t_i \ge \beta$; if $a_i < w_i < \beta$ then $t_i = w_i$; if $w_i \le a_i$ then $t_i \le a_i$. The converses hold for the same reason as above. In the fail-soft form, also $t_i \ge \beta$ implies $w_i \ge t_i$, and $t_i \le a_i$ implies $w_i \le t_i$.

*Step 2: the invariant.* For $i \le j$ let $W_i = \max(w_1, \ldots, w_i)$, with $W_0 = -\infty$. We show by induction on $i$ that, while no cutoff has happened ($m_i < \beta$),
$$ \max(m_i, \alpha) = \max(W_i, \alpha). $$
For $i = 0$ both sides are $\alpha$. Let $i \ge 1$ with $m_i < \beta$. Then $t_i \le m_i < \beta$, so by Step 1 either $t_i = w_i$, or $t_i \le a_i$ and $w_i \le a_i$. In the first case $\max(m_i, \alpha) = \max(a_i, t_i) = \max(a_i, w_i)$. In the second case $\max(m_i, \alpha) = a_i = \max(a_i, w_i)$. In both cases $\max(a_i, w_i) = \max(m_{i-1}, \alpha, w_i) = \max(W_{i-1}, \alpha, w_i) = \max(W_i, \alpha)$ by the hypothesis for $i - 1$.

*Step 3: a cutoff.* Suppose line L6 returns at child $j$, so $r = m_j \ge \beta$ and $m_{j-1} < \beta$, which gives $r = t_j \ge \beta$. By Step 1, $w_j \ge \beta$, so $N(n) \ge w_j \ge \beta$. This is claim 3 for this case, and claim 1 and claim 2 do not apply. In the fail-soft form Step 1 gives $w_j \ge t_j = r$, so $N(n) \ge r$, which is claim 5. Claim 4 does not apply, because $r \ge \beta > \alpha$.

*Step 4: no cutoff.* Suppose the loop ends, so $r = m_k < \beta$ and, by Step 2, $\max(r, \alpha) = \max(N(n), \alpha)$. If $N(n) \ge \beta$ this gives $\max(r, \alpha) \ge \beta$, which is false, because $r < \beta$ and $\alpha < \beta$. So $N(n) < \beta$, and claims 3 and 5 do not apply. If $\alpha < N(n) < \beta$, then $\max(r, \alpha) = N(n) > \alpha$, so $r = N(n)$: claim 2. If $N(n) \le \alpha$, then $\max(r, \alpha) = \alpha$, so $r \le \alpha$: claim 1. For claim 4 in the fail-soft form, let $r \le \alpha$. Then $t_i \le m_k = r \le \alpha \le a_i$ for every $i$, so Step 1 gives $w_i \le t_i \le r$ for every $i$, and $N(n) = \max_i w_i \le r$. $\square$

**Corollary 2.** ALPHABETA$(n, -\infty, +\infty)$ returns $N(n)$ in both forms.

*Proof.* Claim 2 with $\alpha = -\infty$ and $\beta = +\infty$, for a finite value $N(n)$. If $N(n) = \pm\infty$, claims 1 and 3 give $r \le -\infty$ or $r \ge +\infty$, so again $r = N(n)$. $\blacksquare$

**Remark (the fail-hard result lies in the window at an inner node only when the leaves are clamped).** In the fail-hard form $m$ starts at $\alpha$, so the result of an inner node is at least $\alpha$. It can still be larger than $\beta$, because line L1 returns the leaf value without a clamp, and a leaf child can give $t > \beta$. Some texts also clamp the leaf values to $[\alpha, \beta]$; Theorem 1 holds for that form too, with the same proof, because a clamped leaf value satisfies claims 1 to 3.

**Lemma 3 (both forms make the same calls).** On the same tree and window, the two forms evaluate the same leaves in the same order.

*Proof.* By induction on the height. Let $m^s_i$ and $m^h_i$ be the values of $m$ in the two forms. If the calls on $c_1, \ldots, c_i$ are the same and each pair of results satisfies Theorem 1 in the same window, then $\max(m^h_i, \alpha) = \max(m^s_i, \alpha)$, because both are equal to $\max(W_i, \alpha)$ by Step 2 when no cutoff happened. So the next windows $(-\beta, -a_{i+1})$ are equal. A cutoff happens in one form if and only if $\max(m_i, \alpha) \ge \beta$, which is the same test in both, because $\alpha < \beta$. $\square$
