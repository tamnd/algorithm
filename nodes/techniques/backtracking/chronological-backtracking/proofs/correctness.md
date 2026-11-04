---
title: Chronological backtracking returns the first solution, or failure when there is none
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. For $0 \le k \le m$, let $C_k$ be the set of consistent assignments of $X_1, \ldots, X_k$ with $X_j \in D_j$ for each $j$. Order the tuples of $C_k$ lexicographically, using the given order of each domain. A solution is an element of $C_m$.

**Prefix closure.** If $(v_1, \ldots, v_k) \in C_k$ and $j < k$, then $(v_1, \ldots, v_j) \in C_j$. *Proof.* A constraint whose variables are all among $X_1, \ldots, X_j$ has all its variables among $X_1, \ldots, X_k$, so it is satisfied by $(v_1, \ldots, v_k)$, and it reads only the values $v_1, \ldots, v_j$. $\square$

**Check of line L3.** If $a = (v_1, \ldots, v_{i-1}) \in C_{i-1}$, then line L3 accepts $v$ if and only if $(v_1, \ldots, v_{i-1}, v) \in C_i$. *Proof.* A constraint on variables among $X_1, \ldots, X_i$ either does not involve $X_i$, and then it is satisfied because $a$ is consistent, or it involves $X_i$, and then line L3 checks it. $\square$

**Lemma.** Let $a = (v_1, \ldots, v_{i-1}) \in C_{i-1}$ with $1 \le i \le m + 1$. Then BT$(a, i)$ terminates. It returns the lexicographically first element of $C_m$ that extends $a$, if one exists, and failure otherwise. If it returns failure, then on return $a$ again assigns exactly $X_1, \ldots, X_{i-1}$ with the same values.

*Proof.* By induction on $m + 1 - i$.

*Base, $i = m + 1$.* Line L1 returns $a$, which is in $C_m$ and is the only element of $C_m$ that extends itself.

*Step, $i \le m$.* Assume the lemma for $i + 1$. Let $u_1, \ldots, u_r$ be the values of $D_i$ in order. We show by induction on $t$ that before the iteration for $u_t$, the assignment is $a$ and no element of $C_m$ extends $(a, u_s)$ for any $s < t$. This holds for $t = 1$. In the iteration for $u_t$:

- If line L3 rejects $u_t$, then $(a, u_t) \notin C_i$ by the check lemma. By prefix closure, no element of $C_m$ extends $(a, u_t)$. The assignment is not changed.
- If line L3 accepts $u_t$, then $(a, u_t) \in C_i$, line L4 makes the assignment $(a, u_t)$, and line L5 calls BT with $i + 1$. By the induction hypothesis the call terminates. If it returns a solution, that solution is the first element of $C_m$ that extends $(a, u_t)$, and line L6 returns it. If it returns failure, no element of $C_m$ extends $(a, u_t)$, the assignment is $(a, u_t)$ again, and line L7 restores $a$.

Each element of $C_m$ that extends $a$ has some value $u_t$ for $X_i$. The extensions with $X_i = u_s$ come before those with $X_i = u_t$ in lexicographic order when $s < t$. So when line L6 returns a solution for $u_t$, there is no extension with an earlier value, and the returned solution is the first extension of $a$. If the loop ends, no value gives an extension, so no element of $C_m$ extends $a$, and line L8 returns failure with the assignment equal to $a$. The loop has $r$ iterations, each of which terminates, so the call terminates. $\square$

**Theorem.** BT$(\emptyset, 1)$ terminates. It returns the lexicographically first solution if a solution exists, and failure otherwise.

*Proof.* The empty assignment is in $C_0$, and each element of $C_m$ extends it. Apply the lemma with $i = 1$. $\blacksquare$

**All solutions.** In the version that outputs $a$ at line L1 and never returns at line L6, the same induction, with "returns the first extension" replaced by "outputs every element of $C_m$ that extends $a$, once each, in lexicographic order", shows that the search outputs all solutions, once each, in lexicographic order.
