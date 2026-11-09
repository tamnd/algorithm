---
title: The simplex method returns a correct answer and stops under Bland's rule
proves: [correctness, termination]
status: full
---

**Statement.** Let $A \in \mathbb{Q}^{m \times n}$ have rank $m$, and let $B$ be a feasible basis of $\{x : Ax = b,\ x \ge 0\}$. Run SIMPLEX$(A, b, c, B)$.

1. If it returns OPTIMAL$(x, y)$, then $x$ is feasible, $A^\top y \le c$, and $c^\top x = b^\top y$. So $x$ is an optimal solution of $\min\{c^\top x : Ax = b,\ x \ge 0\}$.
2. If it returns UNBOUNDED, then the returned $x$ is feasible and the returned direction $w$ has $w \ge 0$, $Aw = 0$ and $c^\top w < 0$. So the program has no optimal solution.
3. If a basis never repeats, the run stops after at most $\binom{n}{m}$ pivots. With Bland's rule on lines L4 and L7, a basis never repeats.

**Setup.** For a basis $B$, write $N$ for the other indices, $x(B)$ for the basic solution ($x_B = A_B^{-1} b$, $x_N = 0$), $y = A_B^{-\top} c_B$ and $r = c - A^\top y$. Then $r_B = c_B - A_B^\top y = 0$.

**Step 1 (each pivot keeps a feasible basis).** Assume that $B$ is a feasible basis at line L1, and that the run reaches line L8 with $q \in N$, $r_q < 0$, $d = A_B^{-1} A_q$ and a row $p$ from line L7. For $t \ge 0$ let $x(t)$ have $x_q(t) = t$, $x_B(t) = x_B - t d$, and $0$ on $N \setminus \{q\}$. Then $A x(t) = A_B x_B - t A_B d + t A_q = b$. Row $i$ with $d_i \le 0$ has $x_{B(i)}(t) \ge x_{B(i)} \ge 0$. Row $i$ with $d_i > 0$ has $x_{B(i)}(t) \ge 0$ if and only if $t \le x_{B(i)}/d_i$. So $\theta = x_{B(p)}/d_p$, the least such ratio, gives $x(\theta) \ge 0$, with $x_{B(p)}(\theta) = 0$.

The new list $B' = B$ with $B(p)$ replaced by $q$ is a basis: $A_q = A_B d$ with $d_p \ne 0$, so $A_q$ is not in the span of the columns $A_{B(i)}$, $i \ne p$, and the $m$ columns of $B'$ are independent. The point $x(\theta)$ is $0$ outside $B'$ and solves $Ax = b$, so it is the basic solution of $B'$, and it is feasible.

**Step 2 (the objective never rises).** $c^\top x(t) = c_B^\top x_B - t\, c_B^\top d + t c_q = c^\top x(B) + t (c_q - y^\top A_q) = c^\top x(B) + t\, r_q$, since $c_B^\top d = c_B^\top A_B^{-1} A_q = y^\top A_q$. With $r_q < 0$ and $\theta \ge 0$, the value at the new basis is $c^\top x(B) + \theta r_q \le c^\top x(B)$. It is strictly smaller if and only if $\theta > 0$.

**Step 3 (claim 1).** Line L3 returns only when $r \ge 0$, that is $A^\top y \le c$. Also $b^\top y = (A_B x_B)^\top y = x_B^\top A_B^\top y = x_B^\top c_B = c^\top x$. For each feasible $x'$, $c^\top x' \ge (A^\top y)^\top x' = y^\top A x' = b^\top y = c^\top x$, where the inequality uses $x' \ge 0$ and $c - A^\top y \ge 0$. So $x$ is optimal.

**Step 4 (claim 2).** Line L6 returns when $d \le 0$. Let $w_q = 1$, $w_B = -d$, and $w = 0$ elsewhere. Then $w \ge 0$, $Aw = A_q - A_B d = 0$, and $c^\top w = c_q - c_B^\top d = r_q < 0$. For each $t \ge 0$ the point $x(B) + t w$ is feasible, with value $c^\top x(B) + t r_q$, which goes to $-\infty$. So no feasible point is optimal.

**Step 5 (claim 3, the count).** By Step 1 each basis of the run is a feasible basis, that is a set of $m$ of the $n$ column indices. There are at most $\binom{n}{m}$ such sets. If no set repeats, the run makes at most $\binom{n}{m} - 1$ pivots and then stops at line L3 or line L6.

**Step 6 (claim 3, Bland's rule).** Bland's rule takes the least $q$ with $r_q < 0$ on line L4, and on line L7 the least index $B(p)$ among the rows that tie for the least ratio. By Step 2 the value never rises, and it falls at each pivot with $\theta > 0$. So a repeated basis needs a sequence of pivots with $\theta = 0$ that starts and ends at the same basis. All bases of such a cycle have the same basic solution $\bar x$, since a step with $\theta = 0$ does not move the point.

Assume a cycle exists. Call an index *fickle* if it enters or leaves the basis during the cycle; each fickle index both enters and leaves. Let $t$ be the largest fickle index. Let $B$ be a basis of the cycle at which $t$ leaves, with entering index $q$ and column $d = A_B^{-1} A_q$. Let $B^*$ be a basis of the cycle at which $t$ enters, with reduced costs $r^*$. At $B^*$, Bland's rule chose $t$, so $r^*_t < 0$, and $r^*_j \ge 0$ for each $j < t$.

Define $w$ by $w_q = 1$, $w_B = -d$, and $0$ elsewhere. Then $Aw = 0$, so $r^{*\top} w = c^\top w - y^{*\top} A w = c^\top w = r_q < 0$, where $r_q < 0$ because $q$ entered at $B$. Write $r^{*\top} w = r^*_q + \sum_{i} r^*_{B(i)} (-d_i)$.

- $q$ is fickle and $q \ne t$ (it enters while $t$ leaves), so $q < t$. If $q$ is basic at $B^*$, then $r^*_q = 0$. If not, then $r^*_q \ge 0$, because $q < t$ and $t$ was the least index with a negative reduced cost at $B^*$. So $r^*_q \ge 0$.
- Since the sum is negative, some $i$ has $r^*_{B(i)} d_i > 0$. Let $s = B(i)$. Then $r^*_s \ne 0$, so $s$ is not basic at $B^*$. But $s$ is basic at $B$, so $s$ is fickle and $s \le t$.
- If $s = t$: $s = B(p)$ and $d_p > 0$, so $r^*_t d_p < 0$, not $> 0$. So $s < t$, hence $r^*_s \ge 0$ by the rule at $B^*$, and with $r^*_s \ne 0$ we get $r^*_s > 0$, so $d_i > 0$.
- The index $s$ is fickle and nonbasic at $B^*$, and all bases of the cycle have the same point $\bar x$, so $\bar x_s = 0$. At $B$ the basic variable $x_s = 0$ and $d_i > 0$, so row $i$ ties for the least ratio $0$ on line L7. Bland's rule then picks the least index among the tied rows, and $s < t$, so $t$ would not leave at $B$.

This contradicts the choice of $B$. So no cycle exists under Bland's rule, and by Step 5 the run stops. $\blacksquare$

**Remark.** The proof of Step 6 is Bland's 1977 argument as given by Chvátal (Chapter 3) and by Bertsimas and Tsitsiklis (Section 3.4). Without Bland's rule the count of Step 5 does not apply: on Beale's example Dantzig's rule repeats its first basis after 6 pivots with $\theta = 0$.
