---
title: The arc-standard system is sound and complete for projective trees, and every run ends after 2n transitions
proves: [correctness, termination]
status: full
---

The words are $1, \ldots, n$ and 0 is the root. A configuration is $(\sigma, \beta, A)$ as on the main page. Only SHIFT touches the buffer, and it takes the front, so $\beta = [b, b + 1, \ldots, n]$ for some $b$. Write the stack as $\sigma = [v_0, v_1, \ldots, v_k]$ from bottom to top, and for a word $v$ let its **partial yield** $Y_A(v)$ be the set of words below $v$ in the arcs $A$, $v$ included.

**Lemma 1 (invariant).** Every configuration reached from the initial one satisfies:

- (a) $v_0 = 0$, and 0 has no head in $A$;
- (b) each word has at most one head in $A$, and $A$ has no cycle;
- (c) a word has a head in $A$ exactly when it has been shifted and is no longer on the stack;
- (d) $Y_A(v_0), \ldots, Y_A(v_k)$ are consecutive intervals in this order, and their union is $\{0, 1, \ldots, b - 1\}$;
- (e) for each arc $h \to d$ in $A$, every word strictly between $h$ and $d$ is in $Y_A(h)$.

*Proof.* At the start $\sigma = [0]$, $A = \emptyset$ and $b = 1$, and all five hold. SHIFT pushes $b$ with $Y_A(b) = \{b\}$, the next interval, and adds no arc. LEFT-ARC adds $s_0 \to s_1$ for the top two words $s_1 = v_{k - 1} \ne 0$ and $s_0 = v_k$, and removes $s_1$. By (c), $s_1$ had no head, so (b) keeps one head per word, and (a) holds since $s_1 \ne 0$. No cycle closes: a cycle through the new arc would need $s_0 \in Y_A(s_1)$, but by (d) the two partial yields are disjoint. The new $Y_A(s_0)$ is $Y_A(s_1) \cup Y_A(s_0)$, the union of two neighbouring intervals, so (d) holds. Every word strictly between $s_1$ and $s_0$ is in that union, which gives (e) for the new arc; the older arcs keep (e) because partial yields only grow. (c) holds since $s_1$ left the stack with its head. RIGHT-ARC is the mirror image, with $s_1$ as the head and $s_0$ removed; here $s_1 = 0$ is allowed, and (a) still holds. $\square$

**Theorem 2 (soundness and termination).** Every run stops after exactly $2n$ transitions in a terminal configuration, and its arcs $A$ form a projective tree rooted at 0. Under the single-root rule, 0 has exactly one child.

*Proof.* *No dead end.* In a configuration that is not terminal, either the buffer is not empty and SHIFT is legal, or the buffer is empty and the stack has at least two words, and then RIGHT-ARC is legal, also under the single-root rule, whose condition asks only for an empty buffer when $s_1 = 0$.

*Count.* The quantity $2|\beta| + |\sigma|$ is $2n + 1$ at the start and 1 in a terminal configuration. SHIFT lowers $|\beta|$ by one and raises $|\sigma|$ by one; each arc transition lowers $|\sigma|$ by one. So each transition lowers the quantity by exactly one, and every run stops after exactly $2n$ transitions.

*Tree.* In a terminal configuration $\sigma = [0]$ and $\beta$ is empty, so by (c) every word has a head, by (b) exactly one and no cycle. Following heads from any word therefore reaches the only word without a head, which is 0 by (a).

*Projective.* For each arc $h \to d$, (e) says that $h$ dominates every word strictly between $h$ and $d$, which is the definition of a projective arc.

*Single root.* A RIGHT-ARC with $s_1 = 0$ requires $s_1 = v_0$, so the stack is $[0, s_0]$, and under the rule the buffer is empty. After it the configuration is terminal. So 0 gets at most one child, and it gets at least one, because some word of a tree on $\{0, \ldots, n\}$ has 0 as its head. $\square$

**Theorem 3 (completeness).** For every projective tree $G$ there is a sequence of legal transitions from the initial configuration to a terminal configuration with $A = G$. If 0 has one child in $G$, the sequence is legal under the single-root rule.

*Proof.* For a word $v$ with gold left dependents $l_1 < \cdots < l_a$ and right dependents $r_1 < \cdots < r_m$, define the sequence

$$\mathrm{SEQ}(v) = \mathrm{SEQ}(l_1) \cdots \mathrm{SEQ}(l_a) \; \text{SHIFT} \; \text{LEFT-ARC}^{a} \; \mathrm{SEQ}(r_1) \, \text{RIGHT-ARC} \cdots \mathrm{SEQ}(r_m) \, \text{RIGHT-ARC},$$

with the labels of $G$. Let $Y(v)$ be the yield of $v$ in $G$. Since $G$ is projective, $Y(v)$ is an interval, and it is split into the consecutive intervals $Y(l_1), \ldots, Y(l_a), \{v\}, Y(r_1), \ldots, Y(r_m)$, in this order.

*Claim.* If the buffer starts at $\min Y(v)$ and the stack is some $\sigma$, then $\mathrm{SEQ}(v)$ is legal, it ends with the stack $\sigma \mid v$, the buffer starting at $\max Y(v) + 1$, and the arcs of $G$ inside $Y(v)$ added, and nothing else changed. By induction on $|Y(v)|$: the calls $\mathrm{SEQ}(l_i)$ leave $\sigma \mid l_1 \mid \cdots \mid l_a$ with the buffer at $v$, because the yields follow each other. SHIFT pushes $v$. Each LEFT-ARC then attaches the word below $v$ to $v$: first $l_a$, then $l_{a - 1}$, down to $l_1$, and it is legal since these words are not 0. Then each $\mathrm{SEQ}(r_j)$ leaves $r_j$ on top of $v$ with the buffer at the start of the next yield, and RIGHT-ARC attaches $r_j$ to $v$ and removes it. In the end $v$ is on top of $\sigma$ with all arcs of $G$ in $Y(v)$. Every LEFT-ARC and RIGHT-ARC here has $s_1 \ne 0$, because the words of $Y(v)$ are not 0, so the single-root rule never blocks them.

For the whole tree, let $c_1 < \cdots < c_m$ be the children of 0. Run $\mathrm{SEQ}(c_1)$, RIGHT-ARC, ..., $\mathrm{SEQ}(c_m)$, RIGHT-ARC from the initial configuration. By the claim, each $\mathrm{SEQ}(c_j)$ leaves $[0, c_j]$ on the stack, and RIGHT-ARC adds $0 \to c_j$. The yields of the children cover $1, \ldots, n$ in order, so the run ends with $[0]$, an empty buffer and $A = G$. If $m = 1$, the only RIGHT-ARC with $s_1 = 0$ is the last transition, when the buffer is empty, so the rule allows it. $\square$

**The static oracle.** The sequence of Theorem 3 is the one that the static oracle of the main page produces: it does every LEFT-ARC as soon as the dependent and its head are the top two words, and every RIGHT-ARC as soon as the dependent is complete. The tests check that the oracle builds every projective tree with $n \le 5$, and random projective trees up to $n = 6$, and that it fails on every non-projective tree with $n \le 5$. They also check Theorems 2 and 3 by brute force, by building all complete transition sequences for $n \le 5$, with and without the single-root rule.
