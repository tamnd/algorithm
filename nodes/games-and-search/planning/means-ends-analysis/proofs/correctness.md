---
title: Means-ends analysis is sound and terminates, its cost is bounded by the depth bound, and it is incomplete
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode MEANS-ENDS and SOLVE of the page, for a ground STRIPS task $(F, A, I, G)$ with $n = |F|$ and $m = |A|$, a depth bound $k \ge 0$ and any order of the differences. Write $s[o] = (s \setminus \mathit{del}(o)) \cup \mathit{add}(o)$, and for a sequence $\pi$ applicable from $s$ write $s[\pi]$ for its final state.

**Theorem 1 (soundness).** For every $d \ge 0$: if SOLVE($s$, $g$, $d$) returns $(s', \pi)$, then $\pi$ is applicable from $s$, $s[\pi] = s'$, and $g \subseteq s'$. So if MEANS-ENDS returns a plan, the plan is applicable from $I$ and ends in a state that contains $G$.

*Proof.* Induction on $d$. A return at line L5 gives $(s, \text{empty})$ with $g \subseteq s$, which satisfies the claim for every $d$; this is the only success for $d = 0$, by line L6. Let $d \ge 1$ and let the return be at line L16. By the hypothesis for $d - 1$ and line L9, $\pi_1$ is applicable from $s$, $s[\pi_1] = s_1$ and $\mathit{pre}(o) \subseteq s_1$. So $o$ is applicable in $s_1$, and $s_1[o] = s_2$ by line L12. By the hypothesis and line L13, $\pi_2$ is applicable from $s_2$, $s_2[\pi_2] = s_3$ and $g \subseteq s_3$. Hence $\pi_1 \cdot o \cdot \pi_2$ is applicable from $s$, ends in $s_3$, and $g \subseteq s_3$. The claim about MEANS-ENDS is the case $s = I$, $g = G$, $d = k$. $\square$

**Theorem 2 (termination and size).** SOLVE($s$, $g$, $d$) makes at most $(2 n m)^j$ calls at nesting level $j$, for $0 \le j \le d$, and stops. Every plan it returns has at most $2^d - 1$ actions.

*Proof.* A call with bound $d$ makes nested calls only with bound $d - 1$ (lines L9 and L13), and a call with bound 0 makes none (lines L5 and L6), so the calls form a tree of height at most $d$. One call loops over the pairs $(p, o)$ with $p \in g \setminus s$ and $o \in T[p]$, that is $o$ adds $p$. Each action $o$ appears in at most $|\mathit{add}(o)| \le n$ lists, so there are at most $n m$ pairs, and each pair makes at most two nested calls. Hence a call has at most $2 n m$ children, and level $j$ has at most $(2 n m)^j$ calls. A finite tree of calls, each with finite loops, finishes. For the size, let $L(d)$ be the largest length of a returned plan. A return at line L5 gives the empty plan, so $L(0) = 0$, and a return at line L16 gives $L(d) \le 2 L(d - 1) + 1$. So $L(d) \le 2^d - 1$. $\square$

**Lemma 3 (the table of results).** The implementation stores the result of each call under the key $(s, g, d)$ and returns it for a later call with the same key. This does not change the result.

*Proof.* The result of SOLVE depends only on $s$, $g$, $d$, the fixed table $T$ and the fixed order, since the procedure reads no other changing data. A key is stored only after its call has finished. A call with key $(s, g, d)$ never starts while another call with the same key is running, because all nested calls have a smaller bound. So a stored value is the finished result of the same computation. $\square$

**Theorem 4 (cost).** Without the table, MEANS-ENDS takes $O(n (2 n m)^k)$ time and $O(k (n + 2^k))$ space.

*Proof.* Line L1 takes $O(n m)$ time. A call at level $j < k$ costs $O(n)$ for line L5, and for each of its at most $n m$ pairs $O(n)$ for line L12 and $O(2^{k - j})$ to join the plans at line L16, by Theorem 2. A call at level $k$ costs $O(n)$. With Theorem 2 the total is at most
$$ \sum_{j < k} (2 n m)^j \cdot n m \cdot O(n + 2^{k - j}) + (2 n m)^k \cdot O(n). $$
For $n m \ge 2$, the part with $n$ is at most $n m \cdot n \cdot 2 (2 n m)^{k-1} = n (2 n m)^k$, and the part with $2^{k - j}$ is $n m \, 2^k \sum_{j < k} (n m)^j \le 2^{k+1} (n m)^k = 2 (2 n m)^k$. So the time is $O(n (2 n m)^k)$. The recursion is at most $k + 1$ calls deep, and each open call holds a state of $O(n)$ bits and a plan of at most $2^k$ actions, so the space is $O(k (n + 2^k))$. $\square$

## Incompleteness

The *small swap* task has the facts $aR1$, $aR2$, $aR3$, $bR1$, $bR2$, $bR3$, where $vRi$ says that register $Ri$ holds the value $v$, the initial state $I = \{aR1, bR2\}$, the goal $G = \{bR1, aR2\}$, and six actions.

| action | pre | add | del |
| --- | --- | --- | --- |
| saveA | $aR1$ | $aR3$ | |
| saveB | $bR2$ | $bR3$ | |
| o1 | $bR2$ | $bR1$ | $aR1$ |
| o1' | $bR3$ | $bR1$ | $aR1$ |
| o2 | $aR1$ | $aR2$ | $bR2$ |
| o2' | $aR3$ | $aR2$ | $bR2$ |

The sequence saveA, o1, o2' is a plan: it gives $\{aR1, bR2, aR3\}$, then $\{bR2, aR3, bR1\}$, then $\{aR3, bR1, aR2\}$.

**Lemma 5 (a lost value stays lost).** Let $s$ be a state with $aR1 \notin s$ and $aR3 \notin s$. Then every state reachable from $s$ contains $aR2$ only if $s$ does. The same holds with $a$, $R1$ and $aR2$ replaced by $b$, $R2$ and $bR1$.

*Proof.* No action adds $aR1$. The only action that adds $aR3$ is saveA, which needs $aR1$. So along any sequence from $s$, by induction, $aR1$ and $aR3$ stay false, and then o2 and o2', the only actions that add $aR2$, are never applicable. So $aR2$ is never added. For $b$: no action adds $bR2$, only saveB adds $bR3$ and it needs $bR2$, and only o1 and o1' add $bR1$, with the preconditions $bR2$ and $bR3$. $\square$

**Theorem 6 (incompleteness).** On the small swap task, MEANS-ENDS returns failure for every depth bound $k \ge 0$ and every order of the differences, although a plan of 3 actions exists.

*Proof.* For $k = 0$, SOLVE fails at line L6, since $G \not\subseteq I$. Let $k \ge 1$ and suppose SOLVE($I$, $G$, $k$) succeeds. As $G \not\subseteq I$, it returns at line L16 for a difference $p \in \{bR1, aR2\}$ and an operator $o$ that adds $p$, so $o$ is one of o1, o1', o2, o2'. The nested call of line L13 succeeds from $s_2 = s_1[o]$, so by Theorem 1 some plan leads from $s_2$ to a state that contains $G$. We show that this is false in each case.

- $o$ = o1. Its precondition $\{bR2\}$ holds in $I$, so the call of line L9 returns at line L5 with $s_1 = I$. Then $s_2 = \{bR1, bR2\}$ contains none of $aR1$, $aR3$, $aR2$, so by Lemma 5 no state reachable from $s_2$ contains $aR2$.
- $o$ = o1'. The call of line L9 is SOLVE($I$, $\{bR3\}$, $k - 1$). If $k - 1 = 0$, it fails. Otherwise its only difference is $bR3$, whose only operator is saveB. The precondition $\{bR2\}$ of saveB holds in $I$, so the nested call returns $(I, \text{empty})$, saveB gives $I \cup \{bR3\}$, which contains $\{bR3\}$, and the call returns $(I \cup \{bR3\}, \text{saveB})$; this is its first success, so it is the result. Then $s_1 = \{aR1, bR2, bR3\}$ and $s_2 = \{bR1, bR2, bR3\}$, which contains none of $aR1$, $aR3$, $aR2$. Lemma 5 applies again.
- $o$ = o2. As in the first case with the roles of $a$ and $b$ exchanged: $s_1 = I$ and $s_2 = \{aR1, aR2\}$ contains none of $bR2$, $bR3$, $bR1$.
- $o$ = o2'. As in the second case: $s_1 = \{aR1, bR2, aR3\}$ and $s_2 = \{aR1, aR3, aR2\}$ contains none of $bR2$, $bR3$, $bR1$.

Every case contradicts Lemma 5, so SOLVE($I$, $G$, $k$) fails. The argument did not use the order of the differences or of the operators. By Lemma 3 the implementation, with its table of results, fails too. $\square$

The proof shows where the method loses completeness. In the plan saveA, o1, o2', the first action is needed by o2', the operator for the second difference, but it must come before o1, the operator for the first one. SOLVE builds every plan as a plan for the preconditions of one operator, the operator, and a plan for the rest, and when the preconditions of o1 already hold, the first part is empty. No plan of that shape puts saveA before o1.
