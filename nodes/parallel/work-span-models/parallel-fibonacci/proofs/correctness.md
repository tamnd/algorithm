---
title: P-FIB returns the Fibonacci number, has no determinacy race, and has work 4F(n+1) - 3 and span 2n
proves: [correctness, complexity]
status: full
---

We use the pseudocode of the page and the strand model of CLRS. The Fibonacci numbers are $F_0 = 0$, $F_1 = 1$ and $F_k = F_{k-1} + F_{k-2}$ for $k \ge 2$. A call P-FIB$(k)$ with $k \le 1$ is one strand. A call with $k \ge 2$ is three strands: $A$ runs line L1 and the spawn of line L2, $B$ runs up to the call of line L3, and $C$ runs the sync of line L4 and line L5. Its DAG has the edges $A \to B$ (continuation), $A \to$ the first strand of P-FIB$(k-1)$ (spawn), $B \to$ the first strand of P-FIB$(k-2)$ (call), and the last strands of both calls $\to C$ (return). Each strand costs one unit.

**Lemma 1 (value).** For each $n \ge 0$, P-FIB$(n)$ returns $F_n$.

*Proof.* By strong induction on $n$. If $n \le 1$, line L1 returns $n = F_n$. Let $n \ge 2$, and assume the claim for all smaller arguments. Line L2 gives $x = F_{n-1}$ and line L3 gives $y = F_{n-2}$, by the hypothesis. The sync of line L4 waits for the spawned call, so $x$ holds its final value when line L5 reads it. Line L5 returns $F_{n-1} + F_{n-2} = F_n$. $\square$

**Lemma 2 (no determinacy race).** No two logically parallel strands of P-FIB$(n)$ access the same memory location while one of them writes it.

*Proof.* Each call has its own local variables $n$, $x$ and $y$, and the program has no other shared state. We use induction on $n$; a call with $n \le 1$ is one strand. In a call with $n \ge 2$, the only strands that run in parallel are those of the subtree of P-FIB$(n-1)$ on one side, and $B$ and the subtree of P-FIB$(n-2)$ on the other side. The two subtrees touch only the locals of their own calls, which are disjoint, and $B$ reads only $n$, which nothing writes after the call starts. The return value of the spawned call goes into $x$, which $B$ and the other subtree never touch. Only $C$ reads $x$ and $y$, after the sync of line L4. So two parallel strands never access a common location, and by the hypothesis no race exists inside a subtree. $\square$

**Lemma 3 (work).** The work is $W(n) = 4F_{n+1} - 3$ for all $n \ge 0$.

*Proof.* The work is the number of strands. It satisfies $W(0) = W(1) = 1$ and $W(n) = W(n-1) + W(n-2) + 3$ for $n \ge 2$, because a call with $n \ge 2$ has its own three strands plus the strands of its two calls. Check the formula: $4F_1 - 3 = 1$ and $4F_2 - 3 = 1$. For $n \ge 2$, if it holds for $n-1$ and $n-2$, then $W(n) = (4F_n - 3) + (4F_{n-1} - 3) + 3 = 4(F_n + F_{n-1}) - 3 = 4F_{n+1} - 3$. $\square$

**Lemma 4 (span).** The span is $S(0) = S(1) = 1$ and $S(n) = 2n$ for all $n \ge 2$.

*Proof.* Each path from the first strand $A$ to the last strand $C$ of a call with $n \ge 2$ goes through the spawned call or through $B$ and the called call. So the longest path has $S(n) = \max\big(1 + S(n-1) + 1,\ 1 + 1 + S(n-2) + 1\big) = \max\big(S(n-1) + 2,\ S(n-2) + 3\big)$ strands. Then $S(2) = \max(3, 4) = 4$ and $S(3) = \max(6, 4) = 6$. Let $n \ge 4$ and assume $S(k) = 2k$ for $2 \le k < n$. Then $S(n-1) + 2 = 2n$ and $S(n-2) + 3 = 2n - 1$, so $S(n) = 2n$. $\square$

**Theorem.** P-FIB$(n)$ is correct and race-free. Its work is $T_1(n) = 4F_{n+1} - 3 = \Theta(\varphi^n)$, its span is $T_\infty(n) = 2n = \Theta(n)$ for $n \ge 2$, and its parallelism is $\Theta(\varphi^n / n)$, where $\varphi = (1 + \sqrt 5)/2$.

*Proof.* Lemmas 1 to 4 give the exact values. Binet's formula $F_k = (\varphi^k - \psi^k)/\sqrt 5$ with $\psi = (1 - \sqrt 5)/2$ and $|\psi| < 1$ gives $F_{n+1} = \varphi^{n+1}/\sqrt 5 + O(1)$. So $4F_{n+1} - 3 = (4\varphi/\sqrt 5)\,\varphi^n + O(1) = \Theta(\varphi^n)$, and the parallelism $(4F_{n+1} - 3)/(2n)$ is $\Theta(\varphi^n/n)$. $\blacksquare$
