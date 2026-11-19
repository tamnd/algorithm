---
title: The neural transition parser returns a projective tree after 2n moves for any weights, its cache is exact, and its loss gradient is p minus the gold indicator
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. The parser runs the arc-standard system: SHIFT, LEFT-ARC$_l$ (needs $s_1 \ne 0$) and RIGHT-ARC$_l$ (under the single-root rule, from $s_1 = 0$ only with an empty buffer). The network gives a real number $z_t$ to every transition $t$; the parser takes a legal $t$ with the largest $z_t$.

**Theorem 1 (termination and output).** For every choice of weights, the parser stops after exactly $2n$ moves and returns a projective dependency tree rooted at 0. Under the single-root rule the root has exactly one child.

*Proof.* The parser picks only legal transitions, so its run is a run of the arc-standard system with some choice rule. In any non-terminal configuration some transition is legal: SHIFT if the buffer is not empty; otherwise the stack has at least two words, and RIGHT-ARC is legal, also under the single-root rule, since the buffer is empty. So the maximum in line L6 is over a non-empty set. By the soundness theorem of arc-standard parsing (see [the arc-standard proof](/arc-standard-parsing/)), every run of that system ends after exactly $2n$ transitions in a terminal configuration whose arcs form a projective tree, with one root child under the single-root rule. None of this depends on how the legal transition is chosen. $\square$

**Lemma 2 (the oracle).** For a projective gold tree $G$, the static oracle (LEFT-ARC if $h^\ast(s_1) = s_0$; RIGHT-ARC if $h^\ast(s_0) = s_1$ and $s_0$ has all its gold dependents; SHIFT otherwise) gives a legal sequence of $2n$ moves that builds $G$. For a non-projective tree it gets stuck.

*Proof.* We first build a run $R$ that produces $G$, and then show that the oracle chooses the next move of $R$ in every configuration of $R$.

*Construction.* For a word $v$ with gold left dependents $l_1 < \cdots < l_a$ and right dependents $r_1 < \cdots < r_m$, let

$$\mathrm{SEQ}(v) = \mathrm{SEQ}(l_1) \cdots \mathrm{SEQ}(l_a)\ \text{SHIFT}\ \text{LEFT-ARC}^{a}\ \mathrm{SEQ}(r_1)\ \text{RIGHT-ARC} \cdots \mathrm{SEQ}(r_m)\ \text{RIGHT-ARC}$$

where SHIFT pushes $v$ and the LEFT-ARC moves attach $l_a, \ldots, l_1$ to $v$ in turn. Since $G$ is projective, the yields of $l_1, \ldots, l_a, v, r_1, \ldots, r_m$ are consecutive intervals in this order. By induction on the size of the yield, if the buffer front is the first word of the yield of $v$, then $\mathrm{SEQ}(v)$ is legal, pushes $v$ on top of the old stack, moves the buffer front past the yield, and adds exactly the gold arcs inside the yield. The whole run is $\mathrm{SEQ}(c_1)$ RIGHT-ARC $\cdots$ $\mathrm{SEQ}(c_m)$ RIGHT-ARC for the root children $c_1 < \cdots < c_m$; it has one SHIFT and one arc per word, $2n$ moves.

In every configuration of $R$, the stack yields $Y_A(v_0), \ldots, Y_A(v_k)$ are consecutive intervals in stack order, as in every arc-standard run. So the word $s_1$ below the top lies to the left of $Y_A(s_0)$. In $R$, once $s_0$ has its left dependents, $Y_A(s_0)$ starts where the gold yield of $s_0$ starts, so $s_1$ is not in the gold yield of $s_0$.

*The oracle follows $R$.* Take a configuration of $R$ and look at the next move of $R$.

- If it is LEFT-ARC, it attaches $l_i$ to $v$ inside $\mathrm{SEQ}(v)$: $s_0 = v$, $s_1 = l_i \ne 0$ and $h^\ast(s_1) = s_0$. The oracle tests LEFT-ARC first and chooses it.
- If it is RIGHT-ARC, it attaches $r_j$ to $v$ (or a root child $c_j$ to 0): $s_0 = r_j$, $s_1 = v$, $h^\ast(s_0) = s_1$, and $s_0$ is complete, since $\mathrm{SEQ}(r_j)$ added all gold arcs inside its yield. The LEFT-ARC test fails, because $h^\ast(v) = r_j$ together with $h^\ast(r_j) = v$ would be a cycle. So the oracle chooses RIGHT-ARC.
- If it is SHIFT, then by the shape of $R$ the move before it ended one of three blocks: the start of the run or a RIGHT-ARC to the root, so the stack is $[0]$ and no arc move is legal; the end of some $\mathrm{SEQ}(u)$ with $u$ a left dependent of a word not yet pushed (each SHIFT of a word $v$ comes right after $\mathrm{SEQ}(l_a)$, or, when $a = 0$, right after what came before $\mathrm{SEQ}(v)$); or the SHIFT of $v$ with its LEFT-ARC block, or a RIGHT-ARC inside $\mathrm{SEQ}(v)$, with a right dependent $r_j$ still to come. In the second case $s_0 = u$, whose gold head is in the buffer, so the RIGHT-ARC test fails, and $h^\ast(s_1) = u$ would put $s_1$ in the yield of $u$, which lies to its right, so the LEFT-ARC test fails. In the third case $s_0 = v$ is not complete, so the RIGHT-ARC test fails, and $h^\ast(s_1) = v$ would put $s_1$ in the yield of $v$, so the LEFT-ARC test fails. In all three cases the oracle chooses SHIFT.

So the oracle produces $R$, which builds $G$ in $2n$ moves.

*Non-projective trees.* Every run ends with a projective tree by Theorem 1, and the oracle adds only gold arcs. So on a non-projective $G$ the oracle cannot finish with $A = G$; the code reports this as a failure. $\square$

**Lemma 3 (the cache).** Let $W_1 = [W_1^{(1)} \cdots W_1^{(48)}]$ be split into blocks of $d$ columns, one per feature, and let feature $k$ select the item $v_k$ with embedding $E^{(k)}_{:, v_k}$. Then

$$W_1 x + b_1 = b_1 + \sum_{k=1}^{48} W_1^{(k)} E^{(k)}_{:, v_k}.$$

*Proof.* $x$ is the column of the 48 embeddings stacked in order, so $W_1 x$ is the sum of the block products, by the rule for multiplying a matrix split into column blocks by a vector split into matching row blocks. The cube is applied after the sum, so storing the block products for each pair $(k, v)$ and adding them gives the same hidden layer. $\square$

**Lemma 4 (the gradient of the loss).** Let $S$ be the set of legal transitions, $p_t = e^{z_t} / \sum_{u \in S} e^{z_u}$ for $t \in S$, and $\ell = -\log p_{t^\ast}$ for a gold $t^\ast \in S$. Then $\partial \ell / \partial z_t = p_t - [t = t^\ast]$ for $t \in S$ and 0 for $t \notin S$, and $\partial \ell / \partial (W_2)_{tj} = (p_t - [t = t^\ast]) h_j$ for $t \in S$ and 0 otherwise.

*Proof.* $\ell = -z_{t^\ast} + \log \sum_{u \in S} e^{z_u}$. The derivative of the second term in $z_t$ is $e^{z_t} / \sum_{u \in S} e^{z_u} = p_t$ for $t \in S$ and 0 for $t \notin S$; the first term gives $-1$ for $t = t^\ast$. Since $z_t = \sum_j (W_2)_{tj} h_j$, the chain rule gives the second formula. $\square$

The tests check Theorem 1 on random sentences and weights, with and without the single-root rule; Lemma 2 on every tree with $n \le 5$; Lemma 3 on every configuration of the example; and Lemma 4 against central finite differences.
