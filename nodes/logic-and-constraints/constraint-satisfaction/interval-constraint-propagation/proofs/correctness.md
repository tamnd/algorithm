---
title: Interval constraint propagation with HC4 removes no solution and stops
proves: [correctness]
status: full
---

We use the pseudocode of the page (lines L1 to L16). A *solution* is a real point $p \in B$ with $\ell_c \le f_c(p) \le u_c$ for every constraint $c$. For a node $k$ of the tree of $f_c$, $\text{val}_k(p)$ is the real value of the subexpression at node $k$ when the variables take the values of $p$.

## Lemma 1: outward rounding gives enclosures

Let $r$ be a real number and $v$ the floating-point number that round-to-nearest gives for $r$. If $v$ is finite, then $\text{pred}(v) \le r \le \text{succ}(v)$, where pred and succ are the neighbouring floating-point numbers. If $v = +\infty$, then $r$ is larger than the largest finite float $M$. If $v = -\infty$, then $r < -M$.

*Proof.* If $r < \text{pred}(v)$, then $\text{pred}(v)$ lies between $r$ and $v$, so it is nearer to $r$ than $v$ is, a contradiction. The case $r > \text{succ}(v)$ is the same. Round to nearest gives $+\infty$ only for $r > M$. $\square$

So the implementation's rule, which moves each inexact lower end to $\text{pred}(v)$ (or to $M$ after overflow to $+\infty$) and each inexact upper end to $\text{succ}(v)$ (or to $-M$), gives a lower bound and an upper bound of the real result. A result is treated as exact only when the operands and the result are integers of size less than $2^{53}$. Rounding is monotone and $2^{53}$ is a float, so the real result is then also an integer of size at most $2^{53}$, which is a float, and round-to-nearest returns it unchanged.

## Lemma 2: the interval operations are enclosures

For intervals $A$ and $B$ and an operation $\circ \in \{+, -, \times\}$, the computed interval $A \circ B$ contains $a \circ b$ for all $a \in A$, $b \in B$. The computed $A^2$ contains $a^2$ for all $a \in A$. If $0 \notin B$, the computed $A / B$ contains $a / b$ for all $a \in A$, $b \in B$.

*Proof.* With real arithmetic, the exact range of $a + b$ is $[\underline A + \underline B, \overline A + \overline B]$, of $a - b$ is $[\underline A - \overline B, \overline A - \underline B]$, and of $a \times b$ and $a / b$ (for $0 \notin B$) is the interval between the smallest and the largest product or quotient of ends, since these functions are monotone in each argument on each sign region. The range of $a^2$ is as computed by cases on the sign of $A$. The computed lower end is a lower bound of the exact lower end by Lemma 1, and in the same way for the upper end. When an end is infinite, the computed end is the limit, with $0 \cdot \infty$ taken as 0, which is a bound because the end itself is not a real value. When $A$ is unbounded in the division, the computed result is $(-\infty, \infty)$, which contains everything. $\square$

## Lemma 3: one revise removes no solution

Let $p$ be a solution with $p \in B$. If HC4-REVISE$(c, B)$ returns a box $B'$, then $p \in B'$. If it returns $\emptyset$, there is no such $p$.

*Proof.* We show the invariant: $\text{val}_k(p) \in J_k$ for every node $k$, at every moment after node $k$ gets its value at line L1.

*Line L1.* For a variable leaf, $J_k = B(x)$ and $p_x \in B(x)$. For a constant, $J_k$ is the constant. For an operation node, the children satisfy the invariant, and Lemma 2 gives $\text{val}_k(p) \in J_k$. The post-order makes sure that the children are done first.

*Line L2.* $\text{val}_{\text{root}}(p) = f_c(p) \in [\ell_c, u_c]$ since $p$ is a solution, and it is in $J_{\text{root}}$, so it is in the intersection.

*Line L5.* Let $k$ be a node with value $z = \text{val}_k(p) \in J_k$, and children with values $a$ and $b$ that are in $J_a$ and $J_b$.

- For $z = a + b$: $a = z - b \in J_k - J_b$ by Lemma 2, so $a$ stays in $J_a \cap (J_k - J_b)$. Then $b = z - a \in J_k - J_a$ with the new $J_a$, which still contains $a$.
- For $z = a - b$: $a = z + b$ and $b = a - z$, in the same way.
- For $z = a \times b$: if $0 \notin J_b$, then $b \neq 0$ and $a = z / b \in J_k / J_b$. If $0 \in J_b$, the code does not change $J_a$. The same holds with $a$ and $b$ swapped.
- For $z = a^2$: $z \ge 0$, so $z \in J_k \cap [0, \infty)$. Then $|a| = \sqrt z \in [r_0, r_1]$, where $r_0$ and $r_1$ are the computed square roots of the ends with outward rounding (Lemma 1, and $\sqrt{\ }$ is monotone). So $a \in [r_0, r_1]$ or $a \in [-r_1, -r_0]$, and $a$ is in the hull of the two intersections with $J_a$.

In each case the new interval of each child contains its value at $p$.

*Lines L3 and L6.* By the invariant, $J_k$ holds a real number whenever such a $p$ exists, so an empty interval means that no solution lies in $B$.

*Line L7.* Each node is reached in reverse post-order after its parent, so $J_k$ is final when the leaf is visited. $p_x \in B(x)$ and $p_x = \text{val}_k(p) \in J_k$, so $p_x$ stays in $B(x)$. If the meet is empty, no solution lies in $B$. $\square$

## Theorem 1: soundness of ICP

Every solution in the input box is in the box that ICP returns. If ICP returns $\emptyset$, the input box has no solution.

*Proof.* Let $p$ be a solution in the input box. By induction on the number of iterations of the loop at L10, $p \in B$: it holds at L8, and each iteration replaces $B$ by the result of HC4-REVISE at L15, which contains $p$ by Lemma 3. If L13 returns $\emptyset$, Lemma 3 says no solution lies in the current box, which contains all solutions of the input box, so there are none. $\square$

## Theorem 2: termination

ICP stops after finitely many iterations.

*Proof.* Each iteration removes one constraint from $Q$. A constraint enters $Q$ at L14 only when a domain $B(x)$ shrinks with $B'(x) \subseteq B(x)$ and either its width goes from infinite to finite, or its width $w'$ is less than $(1 - \rho) w$ for the old width $w$. Since $B'(x) \subseteq B(x)$ always, widths never grow. The first case happens at most once for each variable. In the second case, a zero width can never shrink again, and a nonzero width of an interval with float ends is at least the smallest positive float $w_{\min}$. So the second case happens at most $\lceil \ln(w_0 / w_{\min}) / (-\ln(1 - \rho)) \rceil$ times for each variable, where $w_0$ is its first finite width. Each such event adds at most the number of constraints on $x$ to $Q$. So only finitely many constraints ever enter $Q$, and the loop stops. $\square$

## Remark: what the output is not

The returned box need not be the hull of the solutions. On $[-1, 1]^2$ with $x + y = 0$ and $x - y = 0$, the forward pass of each constraint gives $[-2, 2]$, the root becomes $[0, 0]$, and each projection gives $[-1, 1]$ again, so nothing changes, although the only solution is $(0, 0)$. Theorem 1 is the full guarantee: no solution is lost.
