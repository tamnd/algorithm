---
title: The segment Viterbi recursion returns a parse of largest score
proves: [correctness]
status: full
---

Fix a GHMM with states $Q = \{1, \ldots, K\}$ and a sequence $x$ of length $n \ge 1$. All quantities are natural logarithms, with $-\infty$ for an impossible event: $s_q$ (start), $t_{pq}$ (transition), $e_q$ (end), $d_q(l)$ (length $l$ of a segment of $q$, with $d_q(l) = -\infty$ for $l > D_q$) and $f_q(a, b)$ (state $q$ emits $x[a, b)$). A *parse* is a list of segments $(q_1, b_0, b_1), (q_2, b_1, b_2), \ldots, (q_m, b_{m-1}, b_m)$ with $0 = b_0 < b_1 < \cdots < b_m = n$. Its score is

$$\sigma = s_{q_1} + \sum_{r=2}^{m} t_{q_{r-1} q_r} + \sum_{r=1}^{m} \big(d_{q_r}(b_r - b_{r-1}) + f_{q_r}(b_{r-1}, b_r)\big) + e_{q_m}.$$

A *partial parse* of $x[0, b)$ is the same object with $b_m = b$, and its score is the same sum without the end term $e_{q_m}$.

For $1 \le b \le n$ and $q \in Q$, let $\Gamma_b(q)$ be the largest score of a partial parse of $x[0, b)$ whose last segment has state $q$, or $-\infty$ if there is none. For $1 \le b < n$, let $\Delta_b(q) = \max_{p} (\Gamma_b(p) + t_{pq})$, the best score of a partial parse of $x[0, b)$ followed by a step into $q$.

**Lemma 1 (recursion).** For $1 \le b \le n$,

$$\Gamma_b(q) = \max_{1 \le l \le \min(D_q, b)} \big(E_{b - l}(q) + d_q(l) + f_q(b - l, b)\big), \quad E_0(q) = s_q, \quad E_c(q) = \Delta_c(q) \text{ for } c \ge 1.$$

*Proof.* Take a partial parse of $x[0, b)$ that ends with a segment $(q, b - l, b)$. If $l = b$, the parse is that one segment and its score is $s_q + d_q(l) + f_q(0, b)$. If $l < b$, removing the last segment leaves a partial parse of $x[0, b - l)$ that ends in some state $p$, and the score is the score of that shorter parse plus $t_{pq} + d_q(l) + f_q(b - l, b)$. The added terms depend only on $p$, $q$, $l$ and $b$, not on the earlier segments. So for fixed $l$ and $p$, the best choice of the shorter parse is one of score $\Gamma_{b - l}(p)$, and the best over $p$ gives $\Delta_{b - l}(q)$. Conversely, each value on the right side is the score of a partial parse built in this way. Lengths above $D_q$ have $d_q(l) = -\infty$ and can be left out. $\square$

**Lemma 2 (the tables).** When line L8 has run for position $b$, the code holds $\mathit{gamma}[b][q] = \Gamma_b(q)$ and $\mathit{delta}[b][q] = \Delta_b(q)$ for all $q$, and $\mathit{back}[b][q]$ is a length $l$ that reaches the maximum of Lemma 1, and $\mathit{delta\_arg}[b][q]$ a state $p$ that reaches the maximum in $\Delta_b(q)$.

*Proof.* By induction on $b$. The loop over $l$ in lines L4 to L7 reads $\mathit{delta}[b - l][q]$ only for $b - l < b$, which holds $\Delta_{b - l}(q)$ by the induction hypothesis, and reads $s_q$ when $b - l = 0$ (line L5). Skipping a term with an impossible entry changes no maximum. So lines L3 to L7 compute the maximum of Lemma 1, and keep a length that reaches it. Line L8 then computes $\Delta_b(q)$ from the finished row $\mathit{gamma}[b]$. $\square$

**Theorem.** If some parse has a finite score, the decoder returns a parse whose score $\max_q (\Gamma_n(q) + e_q)$ is the largest score of any parse. Otherwise it returns $-\infty$ and no parse.

*Proof.* Every parse is a partial parse of $x[0, n)$ plus the end term of its last state, so the largest parse score is $\max_q (\Gamma_n(q) + e_q)$, and line L9 picks a state $q$ that reaches it; if all values are $-\infty$, no parse is possible. Line L10 follows the stored choices: from $(b, q)$ it emits the segment $(q, b - l, b)$ with $l = \mathit{back}[b][q]$, and moves to $(b - l, p)$ with $p = \mathit{delta\_arg}[b - l][q]$. By induction on the number of steps, the segments emitted so far, read backward, are the tail of a partial parse whose score is $\Gamma_b(q)$ at the current pair: by Lemma 2 the chosen $l$ and $p$ satisfy $\Gamma_b(q) = \Gamma_{b - l}(p) + t_{pq} + d_q(l) + f_q(b - l, b)$ when $b - l > 0$, and $\Gamma_b(q) = s_q + d_q(b) + f_q(0, b)$ when $l = b$. Each step lowers $b$ by at least 1, so the loop ends at $b = 0$ with a full parse whose score is $\Gamma_n(q) + e_q$. Line L11 returns its segments in order. $\square$

**Running time.** For each $b$ and $q$, lines L4 to L7 try at most $D_q$ lengths, each with one call of $d_q$ and $f_q$. Line L8 costs $K^2$ per position. With $D = \max_q D_q$ and segment scores in $O(1)$ time (by prefix sums, as in the toy gene model), the total is $\Theta(n (K D + K^2))$ in the worst case, that is $O(n D)$ per state. The tables take $\Theta(n K)$ space, and the traceback takes $O(n)$ time.
