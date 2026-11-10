---
title: The two-stacks queue keeps its invariant and returns the aggregate of the window
proves: [correctness]
status: full
---

Let $(M, \otimes, 1)$ be a monoid: $\otimes$ is associative and $1 \otimes x = x \otimes 1 = x$ for all $x \in M$. For a sequence $u_1, \ldots, u_k$ of elements of $M$ write $\Pi(u_1, \ldots, u_k) = u_1 \otimes \cdots \otimes u_k$, with $\Pi() = 1$. By associativity this value does not depend on the bracketing, and $\Pi(u_1, \ldots, u_k) = \Pi(u_1, \ldots, u_j) \otimes \Pi(u_{j+1}, \ldots, u_k)$ for every $0 \le j \le k$.

**State.** Let the window hold $v_1, \ldots, v_n$ from the oldest to the newest. The structure is correct in a state when there is an $f$ with $0 \le f \le n$ such that:

1. $F$ holds, from the top down, the pairs $(v_1, a_1), \ldots, (v_f, a_f)$, and $a_i = \Pi(v_i, \ldots, v_f)$ for $1 \le i \le f$;
2. $B$ holds, from the bottom up, $v_{f+1}, \ldots, v_n$;
3. $a_B = \Pi(v_{f+1}, \ldots, v_n)$.

**Lemma 1.** The empty structure is correct, and each of INSERT, EVICT and QUERY maps a correct state to a correct state for the new window.

*Proof.* The empty structure has $F$ and $B$ empty and $a_B = 1$, which is the state with $n = f = 0$.

QUERY changes nothing.

INSERT$(v)$. The new window is $v_1, \ldots, v_n, v_{n+1}$ with $v_{n+1} = v$. Keep the same $f$. Line L1 puts $v_{n+1}$ on top of $B$, so condition 2 holds for the new window. Line L2 sets $a_B$ to $\Pi(v_{f+1}, \ldots, v_n) \otimes v_{n+1} = \Pi(v_{f+1}, \ldots, v_{n+1})$, which is condition 3. $F$ does not change, and condition 1 refers only to $v_1, \ldots, v_f$, so it still holds.

EVICT, precondition $n \ge 1$. The new window is $v_2, \ldots, v_n$.

*Case $f \ge 1$.* Line L3 finds $F$ not empty and line L10 pops $(v_1, a_1)$ and returns $v_1$, the oldest item. Rename the window as $v'_j = v_{j+1}$ for $1 \le j \le n - 1$ and set $f' = f - 1$. $F$ now holds, from the top down, $(v_2, a_2), \ldots, (v_f, a_f)$, and $a_{i} = \Pi(v_i, \ldots, v_f) = \Pi(v'_{i-1}, \ldots, v'_{f'})$, which is condition 1 for the new window. $B$ and $a_B$ do not change, and $v_{f+1}, \ldots, v_n = v'_{f'+1}, \ldots, v'_{n-1}$, so conditions 2 and 3 hold.

*Case $f = 0$.* Then $B$ holds $v_1, \ldots, v_n$ with $n \ge 1$. The loop of lines L5 to L8 runs while $B$ is not empty. We claim: after $k$ iterations, for $0 \le k \le n$, $B$ holds $v_1, \ldots, v_{n-k}$ from the bottom up, $F$ holds from the top down $(v_{n-k+1}, a_{n-k+1}), \ldots, (v_n, a_n)$ with $a_i = \Pi(v_i, \ldots, v_n)$, and $a = \Pi(v_{n-k+1}, \ldots, v_n)$. For $k = 0$ line L4 gives $a = 1 = \Pi()$, and both claims about the stacks hold. Assume the claim after $k < n$ iterations. Line L6 pops the top of $B$, which is $v_{n-k}$. Line L7 sets $a$ to $v_{n-k} \otimes \Pi(v_{n-k+1}, \ldots, v_n) = \Pi(v_{n-k}, \ldots, v_n)$. Line L8 pushes $(v_{n-k}, a)$ on top of $F$. So the claim holds after $k + 1$ iterations. Each iteration removes one item of $B$, so the loop stops after exactly $n$ iterations, with $B$ empty and $F$ holding $(v_1, a_1), \ldots, (v_n, a_n)$ from the top down, $a_i = \Pi(v_i, \ldots, v_n)$. Line L9 sets $a_B = 1$. This is a correct state with $f = n$. Line L10 then pops $(v_1, a_1)$ and returns $v_1$, and the case $f \ge 1$ above shows that the result is correct for the new window. $\square$

**Theorem.** In every reachable state, EVICT returns the oldest item of the window, and QUERY returns $\Pi(v_1, \ldots, v_n)$.

*Proof.* By Lemma 1 and induction on the number of operations, every reachable state is correct. The proof of the lemma shows that EVICT returns $v_1$. For QUERY, line L11 sets $a_F = a_1 = \Pi(v_1, \ldots, v_f)$ when $f \ge 1$, and $a_F = 1 = \Pi()$ when $f = 0$. Line L12 returns $a_F \otimes a_B = \Pi(v_1, \ldots, v_f) \otimes \Pi(v_{f+1}, \ldots, v_n) = \Pi(v_1, \ldots, v_n)$ by associativity. Neither step uses commutativity or an inverse. $\blacksquare$
