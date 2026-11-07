---
title: ESTRIN returns f(x) with n additions, n + ceil(log2(n + 1)) - 1 multiplications and depth at most 2 ceil(log2(n + 1))
proves: [correctness]
status: full
---

Let $R$ be a commutative ring, $a = [a_0, \ldots, a_n]$ with $n \ge 0$, $f = \sum_{k=0}^{n} a_k x^k$, and fix the point $x \in R$. Write $\ell_k$ for the length of the list $c$ at the start of the $k$-th pass through line L3 (counting from $k = 0$), and $p_k$ for the value of $p$ then.

**Lemma 1 (one round).** Let $c = [c_0, \ldots, c_{\ell - 1}]$ with $\ell \ge 2$, let $p \in R$, and let $c'$ be the list built by lines L4 and L5. Then $\sum_{i} c'_i (p^2)^i = \sum_i c_i p^i$, and $c'$ has $\lceil \ell/2 \rceil$ entries.

*Proof.* For $0 \le i < \lfloor \ell/2 \rfloor$, $c'_i = c_{2i} + c_{2i+1} p$, and $c'_i (p^2)^i = c_{2i} p^{2i} + c_{2i+1} p^{2i+1}$. If $\ell$ is odd, the last entry is $c'_{(\ell-1)/2} = c_{\ell - 1}$, and $c_{\ell-1} (p^2)^{(\ell-1)/2} = c_{\ell - 1} p^{\ell - 1}$. Every index of $c$ appears in exactly one of these terms, so the sums agree. The count is $\lfloor \ell/2 \rfloor$, plus $1$ if $\ell$ is odd, which is $\lceil \ell/2 \rceil$. $\square$

**Theorem (correctness).** ESTRIN$(a, x)$ returns $f(x)$.

*Proof.* We show that at the start of each pass through line L3, $\sum_i c_i p^i = f(x)$. At the first pass, $c = a$ and $p = x$ by lines L1 and L2, so the sum is $f(x)$. If the loop body runs, then $c$ has $\ell \ge 2$ entries, and by Lemma 1 the new list $c'$ satisfies $\sum_i c'_i (p^2)^i = f(x)$. Line L6 sets $c \leftarrow c'$. If $c'$ has more than one entry, line L7 sets $p \leftarrow p^2$ and the invariant holds. If $c'$ has one entry, $p$ is not updated, but then $\sum_i c'_i q^i = c'_0$ for every $q$, so the invariant holds as well. The length goes from $\ell$ to $\lceil \ell/2 \rceil < \ell$ for $\ell \ge 2$, so the loop ends, with one entry $c_0 = \sum_i c_i p^i = f(x)$, which line L8 returns. For an empty list the implementation returns $0 = f(x)$. $\square$

**Theorem (cost).** For $n \ge 1$, let $L = \lceil \log_2(n + 1) \rceil$. ESTRIN uses exactly $n$ additions and $n + L - 1$ multiplications, and its depth, the longest chain of operations each of which uses the result of the one before, is at most $2L$.

*Proof.* *Rounds.* We have $\ell_0 = n + 1$ and $\ell_{k+1} = \lceil \ell_k / 2 \rceil$. By induction, $\ell_k = \lceil (n + 1)/2^k \rceil$, because $\lceil \lceil m/2^k \rceil / 2 \rceil = \lceil m / 2^{k+1} \rceil$ for positive integers $m$. So $\ell_k = 1$ exactly when $2^k \ge n + 1$, that is $k \ge L$, and the loop body runs $L$ times.

*Additions and multiplications in line L4.* A round on a list of length $\ell$ does $\lfloor \ell/2 \rfloor = \ell - \lceil \ell/2 \rceil$ additions and as many multiplications. Summed over the rounds this telescopes to $\ell_0 - \ell_L = (n + 1) - 1 = n$.

*Squarings.* Line L7 squares after each round except the last, where the new list has one entry: $L - 1$ squarings.

*Depth.* Let $\delta_k$ be the largest depth of an entry of $c$ at the start of round $k$, and let $\pi_k$ be the depth of $p_k$. Then $\delta_0 = 0$ and $\pi_0 = 0$, since the inputs have depth $0$. Line L7 gives $\pi_{k+1} = \pi_k + 1$, so $\pi_k = k$. Line L4 gives $\delta_{k+1} \le \max(\delta_k, \pi_k) + 2 = \max(\delta_k + 2, k + 2)$, since an entry $c_{2i} + c_{2i+1} p$ needs one multiplication after $c_{2i+1}$ and $p$ are known, and one addition after that. By induction, $\delta_k \le 2k$: it holds for $k = 0$, and $\delta_{k+1} \le \max(2k + 2, k + 2) = 2(k + 1)$. After $L$ rounds the depth of the result is at most $2L$. $\blacksquare$
