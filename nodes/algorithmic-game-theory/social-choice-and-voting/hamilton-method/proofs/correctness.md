---
title: Correctness and optimality of Hamilton's method
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_n \ge 0$ be integers with $P = \sum_i p_i > 0$, and let $h \ge 0$ be an integer. The quota of state $i$ is $q_i = h p_i / P$, so $\sum_i q_i = h$. Write $q_i = \lfloor q_i \rfloor + \phi_i$ with $0 \le \phi_i < 1$.

**Claim 1 (the integer form).** Line L2 sets $a_i = \lfloor q_i \rfloor$ and $r_i = P \phi_i$.

*Proof.* Division with remainder gives $h p_i = P \lfloor h p_i / P \rfloor + (h p_i \bmod P)$ with $0 \le h p_i \bmod P < P$. Divide by $P$.

So ordering the states by $r_i$ is the same as ordering them by $\phi_i$, and the method needs no fractions.

**Claim 2 (the number of extra seats).** The number $s$ of line L3 is $\sum_i \phi_i$, and $0 \le s < n$. Moreover $s$ is less than the number of states with $\phi_i > 0$, unless $s = 0$.

*Proof.* $s = h - \sum_i \lfloor q_i \rfloor = \sum_i (q_i - \lfloor q_i \rfloor) = \sum_i \phi_i$. Each $\phi_i$ is in $[0, 1)$, so the sum of the positive ones is less than their number.

**Claim 3 (output).** The method returns integers $a_i \ge 0$ with $\sum_i a_i = h$ and $\lfloor q_i \rfloor \le a_i \le \lceil q_i \rceil$ for every $i$ (the quota property).

*Proof.* Lines L5 and L6 add 1 to exactly $s$ of the $\lfloor q_i \rfloor$, so the sum is $\sum_i \lfloor q_i \rfloor + s = h$. Each state gets $\lfloor q_i \rfloor$ or $\lfloor q_i \rfloor + 1$. By Claim 2 and the order of line L4, a state that gets the extra seat has $r_i > 0$, so $q_i$ is not an integer and $\lfloor q_i \rfloor + 1 = \lceil q_i \rceil$.

**Claim 4 (least squares).** Among all integer vectors $b \ge 0$ with $\sum_i b_i = h$, the output $a$ minimizes $D(b) = \sum_i (b_i - q_i)^2$. If the remainders $r_i$ are distinct, it is the only minimizer.

*Proof.* Let $b$ be a minimizer and $d_i = b_i - q_i$, so $\sum_i d_i = 0$. Moving one seat from state $i$ to state $j$ changes $D$ by
$$(d_i - 1)^2 - d_i^2 + (d_j + 1)^2 - d_j^2 = 2 (d_j - d_i + 1).$$
Let $i$ have the largest $d_i$ and $j$ the smallest $d_j$, and suppose $d_i - d_j > 1$. Then $b_i \ge 1$: if $b_i = 0$, then $d_i = -q_i \le 0$, so every $d \le 0$ with sum 0, every $d = 0$, and there is no gap. So the move is allowed, and it lowers $D$, which is a contradiction. So a minimizer has $\max_i d_i - \min_i d_i \le 1$. Since the $d_i$ sum to 0, $\min_i d_i \le 0 \le \max_i d_i$, so every $d_i$ is in $[-1, 1]$. If some $d_i = -1$, then $\max_i d_i \le 0$, so every $d_i \le 0$ with sum 0, and every $d_i = 0$, a contradiction. In the same way no $d_i = 1$. So $|b_i - q_i| < 1$, that is, $b_i = \lfloor q_i \rfloor + x_i$ with $x_i \in \{0, 1\}$, $x_i = 0$ when $\phi_i = 0$, and $\sum_i x_i = s$.

For such a vector, $D(b) = \sum_i \phi_i^2 + \sum_{i : x_i = 1} \bigl((1 - \phi_i)^2 - \phi_i^2\bigr) = \sum_i \phi_i^2 + \sum_{i : x_i = 1} (1 - 2 \phi_i)$. This is smallest when the $s$ states with $x_i = 1$ are $s$ states with the largest $\phi_i$, which is the choice of lines L4 to L6. If the $\phi_i$ are distinct, this choice is unique.

The same argument works for $\sum_i |b_i - q_i|^t$ with any $t \ge 1$, since only the order of the $\phi_i$ matters.

**Claim 5 (the Alabama paradox).** The method is not house monotone: with $p = (3, 3, 1)$, it gives $(1, 1, 1)$ for $h = 3$ and $(2, 2, 0)$ for $h = 4$.

*Proof.* For $h = 3$ the quotas are $9/7, 9/7, 3/7$: the integer parts are $(1, 1, 0)$, $s = 1$, and the remainders $2/7, 2/7, 3/7$ give the seat to state 3. For $h = 4$ the quotas are $12/7, 12/7, 4/7$: the integer parts are $(1, 1, 0)$, $s = 2$, and the remainders $5/7, 5/7, 4/7$ give the two seats to states 1 and 2.
