---
title: Derivative-based matching decides membership
proves: [correctness, termination]
status: full
---

Write $\nu(x)$ for the NULLABLE bit of a node $x$, and $a^{-1}L = \{v : av \in L\}$ for the left quotient of a language $L$ by a symbol $a$. For a word $u$, $u^{-1}L = \{v : uv \in L\}$. Then $\varepsilon^{-1}L = L$, $(ua)^{-1}L = a^{-1}(u^{-1}L)$, and $u \in L$ if and only if $\varepsilon \in u^{-1}L$.

**Lemma 1 (constructors).** For all expressions $x, y, x_1, \ldots, x_j$: $L(\mathrm{CAT}(x, y)) = L(x) L(y)$, $L(\mathrm{ALT}(x_1, \ldots, x_j)) = L(x_1) \cup \cdots \cup L(x_j)$ and $L(\mathrm{STAR}(x)) = L(x)^*$. The bit $\nu$ stored with each node it returns is true if and only if $\varepsilon$ is in its language.

*Proof.* Each case of lines L10 to L12 uses a language identity. For CAT: $\emptyset L = L \emptyset = \emptyset$ and $\{\varepsilon\} L = L \{\varepsilon\} = L$. For ALT: union is associative, commutative and idempotent, so the union of the $L(x_i)$ equals the union of the languages of the members of the flattened set; $L(\emptyset) = \emptyset$ adds nothing; an empty union is $\emptyset$, and a union of one member is that member. For STAR: $\emptyset^* = \{\varepsilon\}^* = \{\varepsilon\}$, and $(L^*)^* = L^*$. When a new node is made, its bit is $\nu(x) \land \nu(y)$ for a concatenation, the disjunction of the members' bits for a union, and true for a star. By induction on the order in which nodes are made, each bit is correct: $\varepsilon \in L(x) L(y)$ if and only if $\varepsilon \in L(x)$ and $\varepsilon \in L(y)$; $\varepsilon$ is in a union if and only if it is in a member; and $\varepsilon \in L^*$ always. The base nodes $\emptyset$, $\varepsilon$ and the symbols have the bits false, true and false. Hash-consing returns an existing node only when the node is equal, with the same language and bit. $\square$

**Lemma 2 (derivative).** For every node $r$ and symbol $a$, $L(D(r, a)) = a^{-1} L(r)$.

*Proof.* By induction on the structure of $r$. Memoization returns a value computed earlier for the same pair, so it does not change the result.

- $r = \emptyset$: $a^{-1}\emptyset = \emptyset$. $r = \varepsilon$: no word $av$ equals $\varepsilon$, so $a^{-1}\{\varepsilon\} = \emptyset$. This is line L5.
- $r = b$, a symbol: $a^{-1}\{b\}$ is $\{\varepsilon\}$ if $b = a$ and $\emptyset$ otherwise. This is line L6.
- $r = s_1 \mid \cdots \mid s_j$: $a^{-1}(L_1 \cup \cdots \cup L_j) = a^{-1}L_1 \cup \cdots \cup a^{-1}L_j$. By induction and Lemma 1, line L7 returns an expression for this set.
- $r = st$: let $av \in L(s)L(t)$, so $av = xy$ with $x \in L(s)$ and $y \in L(t)$. If $x \ne \varepsilon$, then $x = ax'$ with $x' \in a^{-1}L(s)$, and $v = x'y \in (a^{-1}L(s)) L(t)$. If $x = \varepsilon$, then $\varepsilon \in L(s)$ and $v \in a^{-1}L(t)$. Conversely, both cases give $av \in L(s) L(t)$. So
$$a^{-1}(L(s)L(t)) = (a^{-1}L(s))\, L(t) \;\cup\; \big(a^{-1}L(t) \text{ if } \varepsilon \in L(s), \text{ else } \emptyset\big).$$
By Lemma 1, $\nu(s)$ tells which case applies, and line L8 returns an expression for this set, by induction and Lemma 1.
- $r = s^*$: let $av \in L(s)^*$. Then $av = x_1 \cdots x_l$ with $l \ge 1$ and each $x_i \in L(s)$; drop the empty factors, so that $x_1$ is not empty. Then $x_1 = ax'$ with $x' \in a^{-1}L(s)$, and $v = x' x_2 \cdots x_l \in (a^{-1}L(s)) L(s)^*$. Conversely, if $v = x' y$ with $ax' \in L(s)$ and $y \in L(s)^*$, then $av = (ax') y \in L(s)^*$. So $a^{-1}(L(s)^*) = (a^{-1}L(s))\, L(s)^*$, which is what line L9 returns, by induction and Lemma 1, since the node $r$ itself has language $L(s)^*$. $\square$

**Termination.** A call $D(r, a)$ evaluates `D` only on $(r, a)$ and on pairs $(z, a)$ for children $z$ of $r$. The children of a node were made before it, so they are strictly below it in the finite DAG of nodes reachable from $r$, and the evaluation is a postorder over this DAG, with each pair evaluated at most once by memoization. Each step makes finitely many calls of the constructors, each of which does finitely many set and table operations. So each call of `D` stops. The loop of lines L1 to L3 runs at most $n$ times. So DERIV-MATCH stops.

**Theorem.** DERIV-MATCH$(r_0, w)$ returns true if and only if $w \in L(r_0)$.

*Proof.* Let $r_i$ be the value of $r$ after $i$ rounds of the loop. By induction on $i$, $L(r_i) = (a_1 \cdots a_i)^{-1} L(r_0)$. For $i = 0$ this is $\varepsilon^{-1}L(r_0) = L(r_0)$. For $i \ge 1$, by Lemma 2,
$$L(r_i) = a_i^{-1} L(r_{i-1}) = a_i^{-1}\big((a_1 \cdots a_{i-1})^{-1} L(r_0)\big) = (a_1 \cdots a_i)^{-1} L(r_0).$$

If line L3 returns false in round $i$, then $r_i = \emptyset$ and $(a_1 \cdots a_i)^{-1}L(r_0) = \emptyset$. Every word $w$ with prefix $a_1 \cdots a_i$ has $w = a_1 \cdots a_i v$, and $w \in L(r_0)$ would put $v$ in this empty set. So $w \notin L(r_0)$, and false is correct.

Otherwise the loop ends with $r = r_n$, and line L4 returns $\nu(r_n)$. By Lemma 1, this is true if and only if $\varepsilon \in L(r_n) = w^{-1} L(r_0)$, which holds if and only if $w \in L(r_0)$. $\blacksquare$
