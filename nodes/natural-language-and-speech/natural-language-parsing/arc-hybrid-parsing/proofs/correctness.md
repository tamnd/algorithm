---
title: The arc-hybrid system is sound and complete for projective trees, and every run ends after 2n transitions
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. A configuration is $(\sigma, \beta, A)$ with $\sigma = [v_0, \ldots, v_k]$ from bottom to top and buffer $[b, \ldots, n]$, a suffix of the sentence. For a word $v$, $Y_A(v)$ is the set of words below $v$ in $A$, $v$ included. When the buffer is empty, put $b = n + 1$ and $Y_A(b) = \emptyset$.

**Lemma 1 (invariant).** Every configuration reached from the initial one satisfies:

- (a) $v_0 = 0$, and no arc enters 0;
- (b) a word has a head in $A$ exactly when it has been shifted and popped; in particular, no stack word and no buffer word has a head;
- (c) $A$ has no cycle;
- (d) $Y_A(v_0), \ldots, Y_A(v_k), Y_A(b)$ are consecutive intervals in this order, and their union is $\{0, \ldots, b\}$ (or $\{0, \ldots, n\}$ when the buffer is empty); the buffer words after $b$ have no dependents in $A$;
- (e) for each arc $h \to d$ in $A$, every word strictly between $h$ and $d$ is in $Y_A(h)$.

*Proof.* At the start $\sigma = [0]$, $A = \emptyset$, $b = 1$, and all hold. SHIFT pushes $b$, whose interval is already next in line, and the new front $b + 1$ has $Y_A(b + 1) = \{b + 1\}$ by the last part of (d). LEFT-ARC adds $b \to s_0$ with $s_0 \ne 0$ and pops $s_0$, which had no head by (b). No cycle closes, because $b$ has no head, so no path of heads leads from $b$ to $s_0$. The intervals of $s_0$ and $b$ are neighbours, so $Y_A(b)$ becomes their union, an interval, and every word strictly between $s_0$ and $b$ lies in it, which gives (e). RIGHT-ARC adds $s_1 \to s_0$ and pops $s_0$; $s_0$ had no head, no cycle closes because $s_1$ is not below $s_0$ (their intervals are disjoint), the two top intervals merge, and (e) holds for the new arc in the same way. Older arcs keep (e) because partial yields only grow. $\square$

**Theorem 2 (soundness and termination).** Every run ends after exactly $2n$ transitions in a terminal configuration whose arcs form a projective tree rooted at 0.

*Proof.* *No dead end.* If the configuration is not terminal, either the buffer is not empty and SHIFT is legal, or the buffer is empty and the stack has two or more words, and RIGHT-ARC is legal. *Count.* The quantity $2|\beta| + |\sigma|$ is $2n + 1$ at the start and 1 at the end, and every transition lowers it by exactly one: SHIFT moves a word from the buffer to the stack, LEFT-ARC and RIGHT-ARC pop one word. So there are exactly $2n$ transitions. *Tree.* At the end, $\sigma = [0]$ and the buffer is empty, so by (b) every word has a head, exactly one since a word gets its head only when it is popped, and by (c) there is no cycle; following heads from any word ends at 0. *Projective.* By (e), the head of every arc dominates every word strictly between its ends. $\square$

**Theorem 3 (completeness).** For every projective tree $G$ there is a run that ends with $A = G$.

*Proof.* For a word $v$ with gold left dependents $l_1 < \cdots < l_a$ and right dependents $r_1 < \cdots < r_m$, let

$$\mathrm{SEQ}(v) = \mathrm{SEQ}(l_1) \cdots \mathrm{SEQ}(l_a) \; \text{LEFT-ARC}^{a} \; \text{SHIFT} \; \mathrm{SEQ}(r_1) \, \text{RIGHT-ARC} \cdots \mathrm{SEQ}(r_m) \, \text{RIGHT-ARC}.$$

Since $G$ is projective, the yield $Y(v)$ is an interval, split into the consecutive intervals $Y(l_1), \ldots, Y(l_a), \{v\}, Y(r_1), \ldots, Y(r_m)$.

*Claim.* If the buffer front is $\min Y(v)$ and the stack is $\sigma$, then $\mathrm{SEQ}(v)$ is legal and ends with the stack $\sigma \mid v$, the buffer front $\max Y(v) + 1$, and exactly the arcs of $G$ inside $Y(v)$ added. By induction on $|Y(v)|$: the calls $\mathrm{SEQ}(l_i)$ leave $\sigma \mid l_1 \mid \cdots \mid l_a$ with the front at $v$. Each LEFT-ARC then attaches the stack top to the front $v$: first $l_a$, then $l_{a - 1}$, down to $l_1$; they are not 0, so the moves are legal. SHIFT pushes $v$. Each $\mathrm{SEQ}(r_j)$ leaves $r_j$ above $v$, and RIGHT-ARC attaches $r_j$ to $v$ and pops it.

For the whole tree, with root children $c_1 < \cdots < c_m$, all to the right of 0, run $\mathrm{SEQ}(c_1)$, RIGHT-ARC, ..., $\mathrm{SEQ}(c_m)$, RIGHT-ARC. Each block leaves $[0, c_j]$ and then adds $0 \to c_j$. The yields cover $1, \ldots, n$ in order, so the run ends in $([0], [\,], G)$. With one root child, the only RIGHT-ARC from 0 is the last move, when the buffer is empty, so the single-root rule allows it. $\square$

**The static oracle.** The sequence of Theorem 3 is the one that the static oracle produces: it makes an arc as soon as the stack top is complete and its gold head is the buffer front or the word below it, and shifts otherwise. The tests check that the oracle rebuilds every projective tree with $n \le 5$ in $2n$ moves and fails on every non-projective tree, and that the set of trees built by all complete sequences for $n \le 5$ is exactly the set of projective trees.

**The dynamic oracle.** The exactness of the cost formulas on the main page is due to Goldberg and Nivre (2013), through arc decomposition. Here it is checked by search: for every projective gold tree with $n \le 4$ and 12 sampled gold trees with $n = 5$, and for every reachable configuration, the tests compute the true cost of each move, the least loss reachable after it minus the least loss reachable before it, and compare it with the formula.
