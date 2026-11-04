---
title: Postfix evaluation returns the value of a postfix expression and rejects every other string
proves: [correctness, termination]
status: full
---

**Claim.** Let $s = s_1 \cdots s_m$ be a token string. If $s \in \mathcal{P}$, POSTFIX-EVAL returns $\operatorname{val}(s)$. If $s \notin \mathcal{P}$, it reports an error. In both cases it stops after at most $m$ rounds of the loop.

**Setup.** We use the definitions of the [reverse Polish notation](/reverse-polish-notation/) page: the weight $w$ of a token ($1$ for an operand, $1 - \operatorname{ar}(\omega)$ for an operator), the prefix sums $P_j = \sum_{i \le j} w(s_i)$ with $P_0 = 0$, and its theorem: $s \in \mathcal{P}$ exactly when $P_j \ge 1$ for $1 \le j \le m$ and $P_m = 1$, and each element of $\mathcal{P}$ splits by rule 2 in exactly one way, so $\operatorname{val}$ is well defined.

We prove this invariant for the loop of line L2. It holds before round $j + 1$, for $0 \le j \le m$, provided that rounds $1, \ldots, j$ reported no error:

> **(E)** $P_i \ge 1$ for $1 \le i \le j$. The prefix $s_1 \cdots s_j$ is a concatenation $F_1 \cdots F_p$ with $p = P_j$ and each $F_r \in \mathcal{P}$, and the stack holds $\operatorname{val}(F_1), \ldots, \operatorname{val}(F_p)$ from the bottom to the top. In particular $|S| = P_j$.

**Step 1: initialization.** Before round 1, $j = 0$, the prefix is empty, $p = 0 = P_0$, and the stack is empty. (E) holds.

**Step 2: maintenance.** Assume (E) for $j$, and consider round $j + 1$ with token $s_{j+1}$.

- *Operand.* Line L3 pushes $v = s_{j+1}$. Set $F_{p+1} = v$, which is in $\mathcal{P}$ by rule 1, with $\operatorname{val}(F_{p+1}) = v$. Now $p + 1 = P_j + 1 = P_{j+1} \ge 1$, and (E) holds for $j + 1$.
- *Operator $\omega$ of arity $k$ with $k \le p$.* Line L5 does not report an error, since $|S| = p \ge k$. Line L6 pops the top $k$ values, which are $\operatorname{val}(F_{p-k+1}), \ldots, \operatorname{val}(F_p)$: the first pop is the top, $\operatorname{val}(F_p)$, and it goes to $y[k]$, so $y[r] = \operatorname{val}(F_{p-k+r})$ for $r = 1, \ldots, k$. Let $G = F_{p-k+1} \cdots F_p\, \omega$. By rule 2, $G \in \mathcal{P}$, and by the definition of $\operatorname{val}$, $\operatorname{val}(G) = f_\omega(y[1], \ldots, y[k])$, which line L7 pushes. So the prefix $s_1 \cdots s_{j+1}$ is $F_1 \cdots F_{p-k}\, G$, a concatenation of $p - k + 1$ postfix expressions, and the stack holds their values in order. Since $P_{j+1} = P_j + 1 - k = p - k + 1 \ge 1$, (E) holds for $j + 1$.
- *Operator $\omega$ of arity $k$ with $k > p$.* Line L5 reports an error. In this case $P_{j+1} = p + 1 - k \le 0$, so the condition of the theorem fails at $j + 1$, and $s \notin \mathcal{P}$. The error is correct.

**Step 3: termination.** Each round increases $j$ by exactly 1, and the loop has $m$ rounds, so it stops after at most $m$ rounds, either at an error of line L5 or after round $m$. Lines L6 and L7 run a bounded number of steps for each round, $k$ pops and one push.

**Step 4: the result.** Suppose that no round reported an error. Then (E) holds for $j = m$: $P_i \ge 1$ for all $i$, and the stack holds $P_m$ values.

- If $P_m = 1$, then $s$ satisfies the condition of the theorem, so $s \in \mathcal{P}$. By (E), $s = F_1$ and the stack holds only $\operatorname{val}(F_1) = \operatorname{val}(s)$. Line L8 finds $|S| = 1$, and line L9 returns $\operatorname{val}(s)$.
- If $P_m \ne 1$, then $s \notin \mathcal{P}$ by the theorem, and line L8 finds $|S| = P_m \ne 1$ and reports an error.

Suppose now that a round $j + 1$ reported an error. By Step 2 this happens only in the third case, where $s \notin \mathcal{P}$.

So for $s \in \mathcal{P}$ no error occurs (each error case implies $s \notin \mathcal{P}$), and the algorithm returns $\operatorname{val}(s)$. For $s \notin \mathcal{P}$ it cannot return a value, because a return at line L9 needs no error in the loop and $P_m = 1$, which with (E) means $s \in \mathcal{P}$. So it reports an error. $\blacksquare$
