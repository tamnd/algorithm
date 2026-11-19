---
title: Composition with the epsilon filter computes the composed relation
proves: [correctness]
status: full
---

We use the notation of the page. The semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$ is commutative: $a \otimes b = b \otimes a$. The tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$ and the log semiring on costs are commutative.

A path $\pi$ of a transducer is a sequence of arcs, each arc starting where the previous one ends. Its input string $i(\pi)$ and output string $o(\pi)$ are the labels read along it with the $\varepsilon$ labels dropped. A successful path starts in the start state and ends in a final state. Its weight is $w(\pi) = w(e_1) \otimes \cdots \otimes w(e_k) \otimes \rho(\text{last state})$. The weight of a pair of strings is

$$T(x, y) = \bigoplus_{\pi \text{ successful},\ i(\pi) = x,\ o(\pi) = y} w(\pi),$$

and $T(x, y) = \bar 0$ when there is no such path. The composition is defined by $(T_1 \circ T_2)(x, z) = \bigoplus_y T_1(x, y) \otimes T_2(y, z)$. If the machines have cycles, we assume that these sums are defined, as in a $k$-closed semiring; for machines without cycles and for $\varepsilon$-free machines and a fixed $(x, z)$ all the sums are finite.

**Lemma 1 (the search builds the reachable part).** Call a triple $(q_1, q_2, f)$ reachable if a sequence of the moves of lines L5 to L8 leads to it from $(i_1, i_2, 0)$. The loop of lines L2 to L8 creates exactly the reachable triples, pops each of them once, and adds every move out of each of them exactly once.

*Proof.* Line L10 pushes a triple only when it is not yet in $Q$, so each triple is pushed and popped at most once. There are at most $3 s_1 s_2$ triples, so the loop stops. Every created triple is the target of a move from a created triple, or the start, so it is reachable. Conversely, take a reachable triple and a shortest sequence of moves to it. By induction on the length of that sequence, the triple before the last move was created and popped, and when it was popped, lines L5 to L8 made the last move, so line L10 created the triple. The arcs out of a triple are added only when that triple is popped, which happens once. $\square$

**Lemma 2 (one interleaving).** In the moves of lines L6 to L8, write $J$ for a joint move (both machines take an $\varepsilon$ arc, line L6), $A$ for a move of $T_1$ alone (line L7) and $B$ for a move of $T_2$ alone (line L8). From filter state 0, the sequences of such moves that the filter allows are exactly the words of $J^* (A^* \cup B^*)$. For any $p, r \ge 0$ exactly one of these words has $p$ moves of $T_1$ (counting $J$ and $A$) and $r$ moves of $T_2$ (counting $J$ and $B$).

*Proof.* Line L6 needs $f = 0$ and keeps $f = 0$. Line L7 needs $f \in \{0, 1\}$ and sets $f = 1$. Line L8 needs $f \in \{0, 2\}$ and sets $f = 2$. So from state 1 only $A$ is allowed, from state 2 only $B$, and from state 0 all three. A word that starts in state 0 is therefore a run of $J$, then either a run of $A$ or a run of $B$, and every such word is allowed. A word $J^j A^a$ or $J^j B^b$ with $p$ and $r$ moves of the two machines has $j + a = p$, $j + b = r$, and $a = 0$ or $b = 0$. So $j = \min(p, r)$, and $a$ and $b$ are fixed. $\square$

**Lemma 3 (paths and pairs of paths).** Let $T = T_1 \circ T_2$ be the output of COMPOSE. There is a bijection between the successful paths $\pi$ of $T$ and the pairs $(\pi_1, \pi_2)$ of successful paths of $T_1$ and $T_2$ with $o(\pi_1) = i(\pi_2)$. Under it, $i(\pi) = i(\pi_1)$, $o(\pi) = o(\pi_2)$ and $w(\pi) = w(\pi_1) \otimes w(\pi_2)$.

*Proof.* Projection. Each arc of $T$ was made from one arc of $T_1$, one arc of $T_2$, or one of each. Keeping the $T_1$ arcs of $\pi$ in order gives a path $\pi_1$ of $T_1$ from $i_1$, and keeping the $T_2$ arcs gives a path $\pi_2$ of $T_2$ from $i_2$. The last state of $\pi$ is final only if both components are final (line L4), so $\pi_1$ and $\pi_2$ are successful. A matched move (line L5) reads the same symbol $b \ne \varepsilon$ on the output of $T_1$ and the input of $T_2$, and the other moves read $\varepsilon$ on both of these sides, so $o(\pi_1) = i(\pi_2)$. The input labels of $\pi$ are those of $\pi_1$ and the output labels those of $\pi_2$. The weights of the arcs of $\pi$ are the weights of the arcs of $\pi_1$ and $\pi_2$, each used once, and the final weight is $\rho_1 \otimes \rho_2$. Since $\otimes$ is commutative and associative, $w(\pi) = w(\pi_1) \otimes w(\pi_2)$.

Construction. Let $o(\pi_1) = i(\pi_2) = y_1 \cdots y_m$. Cut $\pi_1$ into $A_0 e_1 A_1 \cdots e_m A_m$, where $e_k$ is the arc that writes $y_k$ and each $A_k$ is a run of arcs that write $\varepsilon$. Cut $\pi_2$ in the same way into $B_0 f_1 B_1 \cdots f_m B_m$, where $f_k$ reads $y_k$. Build $\pi$ segment by segment. The filter state is 0 at the start and after each matched move. For segment $k$, Lemma 2 gives exactly one allowed word of moves that takes the $|A_k|$ arcs of $A_k$ and the $|B_k|$ arcs of $B_k$; then the matched move takes $e_{k+1}$ and $f_{k+1}$ (line L5 allows it in every filter state). Every triple on the way is reachable, so by Lemma 1 all these arcs are in $T$, and the last triple is final by line L4.

The two maps are inverse to each other. Projection of the constructed path gives back $(\pi_1, \pi_2)$. In the other direction, a path $\pi$ of $T$ is determined by its projections: the matched moves of $\pi$ are fixed by the arcs $e_k, f_k$, and by Lemma 2 the moves between two matched moves are fixed by the lengths $|A_k|$ and $|B_k|$, since the filter state is 0 after each matched move. $\square$

**Theorem.** For all strings $x$ and $z$, $T(x, z) = (T_1 \circ T_2)(x, z)$.

*Proof.* By Lemma 3, and grouping the pairs by the middle string $y$,

$$T(x, z) = \bigoplus_{\pi} w(\pi) = \bigoplus_y \ \bigoplus_{\substack{i(\pi_1) = x,\ o(\pi_1) = y \\ i(\pi_2) = y,\ o(\pi_2) = z}} w(\pi_1) \otimes w(\pi_2) = \bigoplus_y T_1(x, y) \otimes T_2(y, z),$$

where the last step is distributivity of $\otimes$ over $\oplus$. $\square$

**Corollary (size without epsilons).** If neither machine has an $\varepsilon$ on the shared side, lines L6 to L8 never run, every triple has $f = 0$, and $T$ has at most $s_1 s_2$ states. Every arc of $T$ comes from line L5, from one pair $(e_1, e_2)$ of an arc of $T_1$ and an arc of $T_2$. The source of that arc is the triple of the sources of $e_1$ and $e_2$, which is popped once (Lemma 1), so each pair gives at most one arc and $T$ has at most $e_1 e_2$ arcs.

**Remark (no filter).** Without the filter, every word over $\{J, A, B\}$ is allowed, so the map of Lemma 3 is still onto but no longer one to one. Then $T(x, z)$ is a sum in which each term $w(\pi_1) \otimes w(\pi_2)$ appears one or more times. In an idempotent semiring such as the tropical one, $a \oplus a = a$, so the result is still right. In the log semiring it is not. With $T_1$ the single arc $a{:}\varepsilon/0$ and $T_2$ the single arc $\varepsilon{:}c/0$, there are three paths (A then B, B then A, and J), and the cost of $(a, c)$ becomes $-\log 3$ instead of $0$.
