---
title: A Pratt parser accepts exactly the well-formed expressions and returns their unique valid tree
proves: [correctness, termination]
status: full
---

We use the pseudocode, the binding powers and the conditions (A) and (B) of the page. The tokens are $t_1 \cdots t_n$ and $t_{n+1} = \$$. Every infix and postfix operator has $\text{lbp} \ge 1$, every rbp is at least 0, and $\text{lbp}(t) = 0$ for every other token, including `)` and $\$$. A token is never both infix and postfix.

**Spines.** The *left spine* of a tree is the chain of nodes reached from its root by repeatedly going to the left operand of an infix or postfix node. The *right spine* is the chain reached by repeatedly going to the right operand of an infix or prefix node. A group $(\,e\,)$ or an operand ends both chains. In the conditions, the left spine of the right operand counts only nodes that take a left operand, and the right spine of the left operand counts only nodes that have a right operand, which by definition are the nodes of the spines.

Say that a call EXPR(ρ) *starts* at the value $p$ of pos when it is made and *stops at* $q$ if pos is $q$ when it returns.

## Termination and running time

Each call reads a token at line L4 and each round of the loop of line L9 reads a token at line L10, and pos only grows. So there are at most $n + 1$ calls and $n$ rounds in all, and PARSE stops after $O(n)$ steps.

## Lemma 1: the parser builds valid trees

**Lemma 1.** If EXPR(ρ) starts at $p$ and returns a tree $T$, stopping at $q$, then

1. $T$ is a tree of the grammar whose leaves are $t_p \cdots t_{q-1}$, and $T$ is valid;
2. every node on the left spine of $T$ has $\text{lbp} > \rho$;
3. $\text{lbp}(t_q) \le \rho$, and $\text{lbp}(t_q) \le \text{rbp}(X)$ for every node $X$ on the right spine of $T$.

*Proof.* By induction on the order of returns. Consider the tree left after lines L4 to L8. It is an operand (both spines empty), or a group whose inside is valid by induction (both spines end at the group), or a prefix node $u$ with operand $R$ returned by EXPR(rbp(u)) that stopped at the current position $m$. In the last case, part 2 of the induction gives condition (B) at $u$, and part 3 gives $\text{lbp}(t_m) \le \text{rbp}(X)$ for every $X$ on the right spine of $u$, which is $u$ followed by the right spine of $R$.

We show that each round of the loop keeps three facts, which hold before the first round by what we just said: left is valid with leaves $t_p \cdots t_{m-1}$; every node on its left spine has $\text{lbp} > \rho$; and $\text{lbp}(t_m) \le \text{rbp}(X)$ for every $X$ on its right spine. A round takes $o = t_m$ with $\text{lbp}(o) > \rho$.

- If $o$ is postfix, the new node satisfies (A) by the third fact, its left spine is $o$ followed by the old left spine, and its right spine is empty.
- If $o$ is infix, line L12 calls EXPR(rbp(o)), which returns $R$ and stops at some $m'$. The new node satisfies (A) by the third fact and (B) by part 2 for $R$. Its left spine is $o$ followed by the old left spine, all with $\text{lbp} > \rho$. Its right spine is $o$ followed by the right spine of $R$, and part 3 for $R$ gives $\text{lbp}(t_{m'}) \le \text{rbp}(o)$ and $\text{lbp}(t_{m'}) \le \text{rbp}(X)$ for $X$ on the right spine of $R$.

The loop ends at $q$ with $\text{lbp}(t_q) \le \rho$, and the three facts give parts 1, 2 and 3. $\square$

## Lemma 2: a valid tree is what the parser builds

**Lemma 2.** Let $T$ be a valid tree whose leaves are $t_p \cdots t_{q-1}$. Suppose every node on the left spine of $T$ has $\text{lbp} > \rho$, $\text{lbp}(t_q) \le \rho$, and $\text{lbp}(t_q) \le \text{rbp}(X)$ for every node $X$ on the right spine of $T$. Then a call EXPR(ρ) that starts at $p$ returns $T$ and stops at $q$.

*Proof.* By induction on the size of $T$. Write $T$ along its left spine: from the bottom, a node $N_0$ that is an operand, a group or a prefix node, then the nodes $o_1, \ldots, o_k$ of the left spine, from the bottom up, where an infix $o_s$ has the right operand $R_s$. The first leaf of $T$ is the first token of $N_0$, which is $t_p$, and the call reads it at line L4.

- If $N_0$ is an operand, line L5 makes the leaf.
- If $N_0 = (\,e\,)$, the tree $e$ is valid, its left spine has $\text{lbp} \ge 1 > 0$, and the token after it is `)`, with $\text{lbp} = 0 \le 0$ and $0 \le$ every rbp. By induction EXPR(0) returns $e$ and stops at the `)`, and line L6 reads it.
- If $N_0$ is a prefix node $u$ with operand $R$, condition (B) at $u$ says that the left spine of $R$ has $\text{lbp} > \text{rbp}(u)$. The token after $R$ is $o_1$ if $k \ge 1$, and $t_q$ if $k = 0$. In the first case condition (A) at $o_1$ bounds its lbp by the rbp of every node on the right spine of $N_0$, which is $u$ followed by the right spine of $R$; in the second case the hypothesis on $t_q$ gives the same bound, since then $N_0 = T$. By induction, line L7 gets $R$ from EXPR(rbp(u)).

Now the loop. Before round $s$, the token at pos is $o_s$, and it is on the left spine of $T$, so $\text{lbp}(o_s) > \rho$ and line L9 takes it. If $o_s$ is postfix, line L11 builds its node. If $o_s$ is infix, condition (B) at $o_s$ bounds the left spine of $R_s$ from below by $\text{rbp}(o_s)$. The token after $R_s$ is $o_{s+1}$, whose lbp is at most the rbp of every node on the right spine of its left operand, by (A); that spine is $o_s$ followed by the right spine of $R_s$. For $s = k$ the token after $R_k$ is $t_q$, and the right spine of $T$ is $o_k$ followed by the right spine of $R_k$, so the hypothesis gives the same bound. By induction, line L12 gets $R_s$. After round $k$ the token is $t_q$ with $\text{lbp}(t_q) \le \rho$, so the loop ends and the call returns $T$ at $q$. $\square$

## Lemma 3: the parser accepts every well-formed input

A well-formed sequence $E$ can be read from left to right in two states: in state *X* an operand is expected (a prefix operator, an operand or `(`), and in state *Y* an operand has just ended (next comes a postfix or infix operator, or the end of $E$). From the grammar, $E$ is a sequence $U^* P Q^* (O\, U^* P Q^*)^*$ with prefix operators $U$, primaries $P$ (an operand or $(\,E'\,)$ with $E'$ well formed), postfix operators $Q$ and infix operators $O$. Every tree yields such a sequence, and every such sequence has a tree, for example the one that groups all operators to the left.

**Lemma 3.** If EXPR(ρ) starts at a position in state X of a well-formed sequence at the current level of parentheses, it returns without error and stops at a position in state Y of that sequence.

*Proof.* By induction on the number of tokens the call reads. In state X, line L4 reads an operand, a `(` or a prefix operator. After an operand the state is Y. After `(`, the call EXPR(0) starts in state X of the inner sequence $E'$, and by induction it stops in state Y of $E'$ at a token with $\text{lbp} \le 0$, which is not an infix or postfix operator; in state Y the only other possibility is the end of $E'$, so the token is the `)` and line L6 reads it, reaching state Y. After a prefix operator the state is X again, and by induction the call of line L7 stops in state Y. In the loop, a token with $\text{lbp} > \rho \ge 0$ is infix or postfix. A postfix operator leads from Y to Y. An infix operator leads to X, and by induction the call of line L12 stops in Y. So the call stops in state Y. $\square$

## Conclusion

*Soundness.* If PARSE returns a tree $T$, then by Lemma 1, with $p = 1$ and line L2, $T$ is a valid tree of the grammar whose leaves are the whole input. So the input is well formed.

*Completeness.* If the input is well formed, then by Lemma 3 the call EXPR(0) at line L1 stops in state Y of the whole input, at a token with $\text{lbp} \le 0$. That token is not an infix or postfix operator, so it is the end of the input, and line L2 passes.

*Uniqueness.* Let $T$ be any valid tree of a well-formed input. Its left spine has $\text{lbp} \ge 1 > 0$, and the token after it is $\$$, with $\text{lbp}(\$) = 0 \le 0$ and $0 \le \text{rbp}(X)$ for every $X$. By Lemma 2 the call EXPR(0) of line L1 returns $T$. So every valid tree is the tree that PARSE returns, there is exactly one valid tree, and PARSE returns it.
