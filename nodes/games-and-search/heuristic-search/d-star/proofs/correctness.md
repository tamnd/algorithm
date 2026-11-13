---
title: When D* stops processing states, the robot state has its distance to the goal and the back pointers give a shortest path; each phase stops
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The map is a finite directed graph with no self-loops. Each arc $Y \to X$ has a cost $c(Y, X)$, which is positive or $\infty$, and $c(Y, X) = \infty$ when there is no arc. A *neighbour* of $X$ is a state with an arc to $X$ or from $X$. Write $\mathrm{dist}(X)$ for the distance from $X$ to the goal $G$ on the current map. We use $\infty + a = \infty$ and $\infty \le \infty$.

A *phase* is a maximal run of PROCESS-STATE calls with no MODIFY-COST between them: the loop of line L29, or one loop of line L34. We look at the state of the algorithm *between operations*, that is, before or after a whole call of INSERT, MODIFY-COST or PROCESS-STATE. During a call of PROCESS-STATE on $X$, we treat $X$ as CLOSED from line L3 on. $k_{min}$ is the least key on OPEN.

## Three invariants

**Invariant K (keys).** Every OPEN state $Y$ has $k(Y) \le h(Y)$.

*Proof.* Lines L21 to L24 set $h(Y) \leftarrow h_{new}$ and $k(Y)$ to $h_{new}$ or to a minimum that includes $h_{new}$. The only other change of $h$ is line L7, on the state that is being processed, which is not OPEN. $\square$

**Invariant R (relaxed arcs).** For every arc $Y \to X$ with $t(X) = $ CLOSED:

- (a) $t(Y) \ne$ NEW;
- (b) if $t(Y) = $ CLOSED then $h(Y) \le h(X) + c(Y, X)$, and if $t(Y) = $ OPEN then $k(Y) \le h(X) + c(Y, X)$.

**Invariant M (back pointers).** $h(G) = 0$ and $G$ has no back pointer. Every state $Y \ne G$ with $t(Y) \ne$ NEW has a back pointer $X = b(Y)$ with $t(X) \ne$ NEW, and

- if $t(X) = $ CLOSED then $h(Y) = h(X) + c(Y, X)$;
- if $t(X) = $ OPEN then $k(X) < h(Y)$ or $h(Y) = \infty$.

**Invariant A (no cycles).** Following back pointers from a state that is not NEW never repeats a state. With M, it ends at $G$.

*Proof of R, M and A.* At the start only $G$ is OPEN, with $h = k = 0$, so the three hold. We check each operation.

$G$ first. Line L6 needs $h(G) > h(Y) + c(G, Y) > 0$, the third test of line L10 needs $0 > h(X) + c$, and the second tests of lines L10 and L14 need $b(G) = X$. None holds, $G$ is never NEW again, and lines L17, L19 and L26 keep $h$. So $h(G) = 0$ for ever and $b(G)$ is never set.

*INSERT$(Z, h_{new})$.* Arcs into $Z$ are free of R, because $Z$ is OPEN after it. For an arc $Z \to X$ with $X$ CLOSED, R(a) says that $Z$ was not NEW. If $Z$ was CLOSED, R(b) gave $h_{old}(Z) \le h(X) + c(Z, X)$ and now $k(Z) = \min(h_{old}(Z), h_{new}) \le h_{old}(Z)$. If $Z$ was OPEN, the new $k(Z)$ is at most the old one. So R holds. For M, take a child $Y$ with $b(Y) = Z$. If $Z$ was CLOSED, M gave $h(Y) = h_{old}(Z) + c(Y, Z)$, so $k(Z) \le h_{old}(Z) < h(Y)$ or $h(Y) = \infty$. If $Z$ was OPEN, $k(Z)$ did not go up. INSERT changes no pointer.

*MODIFY-COST$(Y, X, c_{new})$.* Only the arc $Y \to X$ changes. If $X$ is CLOSED, line L26 makes it OPEN with $k(X) = h(X)$, so the arc is free of R. For M with $b(Y) = X$: before, $h(Y) = h(X) + c_{old}(Y, X) > h(X) = k(X)$ or $h(Y) = \infty$. If $X$ is OPEN, nothing about R or M changes. If $X$ is NEW, R does not apply and no state points to $X$.

*PROCESS-STATE on $X$ with $k_{old} = k(X)$.* Every other OPEN state has key at least $k_{old}$.

First, after lines L4 to L7, $h(X) \ge k_{old}$. Line L7 sets $h(X) = h(Q) + c(X, Q)$. If $Q$ is CLOSED, R(b) for the OPEN state $X$ gives $k_{old} \le h(Q) + c(X, Q)$. If $Q$ is OPEN, $h(Q) \ge k(Q) \ge k_{old}$ by K.

Arcs $Y \to X$ into $X$, if $X$ is CLOSED at the end. In the LOWER branch (line L8 true), each neighbour $Y$ either goes through line L11, and then $Y$ is OPEN with $k(Y) \le h(X) + c(Y, X)$, or fails all three tests of line L10. Then $Y$ is not NEW, and $h(Y) = h(X) + c(Y, X)$ if $b(Y) = X$ and $h(Y) \le h(X) + c(Y, X)$ if not. With K, R(b) holds for the arc. In the RAISE branch, line L15 is as line L11. If line L16 is true for some $Y$, line L17 makes $X$ OPEN and all arcs into $X$ are free of R. Otherwise each $Y$ that is not handled by line L15 has $h(Y) \le h(X) + c(Y, X)$ as before. The value $h(X)$ does not change after line L7, so the tests do not interfere.

Arcs $X \to Q$ out of $X$, with $Q$ CLOSED at the end. Then $Q$ was CLOSED at the start, so R(b) for the OPEN state $X$ gave $k_{old} \le h(Q) + c(X, Q)$, and $h(Q)$ has not changed. In the LOWER branch, $h(X) = k_{old}$, so $h(X) \le h(Q) + c(X, Q)$. In the RAISE branch, if $h(Q) \le k_{old}$ then lines L5 to L7 made $h(X) \le h(Q) + c(X, Q)$. If $h(Q) > k_{old}$ and $h(X) > h(Q) + c(X, Q)$, then:

- line L16 is false for $Q$, because $h(X) > h(Q) + c(X, Q)$ and $h(Q) > h(X) + c(Q, X)$ cannot both hold with positive costs;
- $b(X) \ne Q$, because $b(X) = Q$ with $Q$ CLOSED gives $h(X) = h(Q) + c(X, Q)$, by M at the start or by line L7;
- so line L14 or line L18 is true for $Q$, and $Q$ becomes OPEN.

If line L17 made $X$ OPEN, then $k(X) \le h(X)$ and the same bound holds. So R(b) holds for the arcs out of $X$.

R(a): every NEW neighbour of $X$ passes the first test of line L10 or line L14 and becomes OPEN. No other state becomes CLOSED.

M for the children of $X$. Each neighbour $Y$ with $b(Y) = X$ and $h(Y) \ne h(X) + c(Y, X)$ goes through line L11 or line L15 and gets equality. If line L17 makes $X$ OPEN, then $k(X) = h(X) < h(X) + c(Y, X) = h(Y)$ or $h(Y) = \infty$. A pointer set at line L11 or line L15 gives equality at that time. M for $X$ itself: line L7 sets $b(X) = Q$ and $h(X) = h(Q) + c(X, Q)$, which is equality if $Q$ is CLOSED. If $Q$ is OPEN, $k(Q) \le h(Q) < h(X)$. A later INSERT of $Q$ keeps M by the INSERT case.

A. Pointers change only at lines L7, L11 and L15.

- Line L15 sets $b(Y) = X$ only if $Y$ was NEW or $b(Y)$ was already $X$. A NEW state has no children, so no cycle can close.
- Line L11 with $Y$ not NEW and $b(Y) \ne X$ needs $h(Y) > h(X) + c(Y, X) > h(X) = k_{old}$. Here $h(X) = k_{old}$. By M at the start, $b(X)$ is CLOSED with a smaller value, because an OPEN target would have a key less than $h(X) = k_{old}$. From there the chain claim below applies, so the chain from $X$ has CLOSED states with values less than $h(X)$. So $Y$ is not on it, and no cycle closes.
- Line L7 sets $b(X) = Q$ with $h(Q) \le k_{old}$. Each state $W$ with $b(W) = X$ had $k_{old} = k(X) < h(W)$ by M, so the chain from $Q$, whose values are at most $h(Q) \le k_{old}$, does not reach $X$.

*The chain claim.* If $h(Y) \le k_{old}$, where $k_{old}$ is at most every key on OPEN, and $Y \ne X$ is not NEW, then the chain from $Y$ goes through CLOSED states with strictly smaller values $h$. Indeed if $b(Y)$ were OPEN, M would give a key less than $h(Y) \le k_{old}$; if $b(Y) = X$, M before the call gave $k_{old} = k(X) < h(Y)$. So $b(Y)$ is CLOSED, $h(b(Y)) = h(Y) - c(Y, b(Y)) < h(Y)$, and we repeat. $\square$

## Consequences

**Lemma 1 (the chain).** Let $Y$ be a state that is not NEW, with $h(Y) < \infty$ and $h(Y) \le k_{min}$, or with OPEN empty. Then the back pointer chain from $Y$ is a path from $Y$ to $G$ of cost exactly $h(Y)$ on the current map. In particular $h(Y) \ge \mathrm{dist}(Y)$.

*Proof.* The chain claim without $X$: each pointer goes to a CLOSED state, and $h$ drops by the cost of the arc. By A the chain ends at $G$, where $h = 0$. $\square$

**Lemma 2 (the lower bound).** Let $Y$ be a state with $\mathrm{dist}(Y) < k_{min}$, or with OPEN empty. Then every state on every shortest path from $Y$ is CLOSED, and $h(Y) \le \mathrm{dist}(Y)$.

*Proof.* Let $Y = P_0, P_1, \ldots, P_m = G$ be a shortest path. If all $P_i$ are CLOSED, R(b) gives $h(P_i) \le h(P_{i+1}) + c(P_i, P_{i+1})$, and the sum gives $h(Y) \le \mathrm{dist}(Y)$. Otherwise let $j$ be the largest index with $P_j$ not CLOSED. If $j = m$, then $G$ is OPEN with $k(G) \le h(G) = 0 \le \mathrm{dist}(Y) < k_{min}$, which is false. If $j < m$, then $P_{j+1}, \ldots, P_m$ are CLOSED, so by R(a) $P_j$ is OPEN, and by R(b)
$$ k(P_j) \le h(P_{j+1}) + c(P_j, P_{j+1}) \le \sum_{i \ge j} c(P_i, P_{i+1}) \le \mathrm{dist}(Y) < k_{min} , $$
which is false too. $\square$

**Theorem 3 (the stop rule).** When the loop of line L34 stops, $h(R) = \mathrm{dist}(R)$. If it is finite, the back pointers from $R$ give a shortest path of the map. The same holds when the loop of line L29 stops.

*Proof.* The loop of line L34 stops when OPEN is empty or $k_{min} \ge h(R)$. If $h(R) < \infty$, Lemma 1 gives a path of cost $h(R)$, so $h(R) \ge \mathrm{dist}(R)$. If $\mathrm{dist}(R) < h(R) \le k_{min}$, Lemma 2 gives $h(R) \le \mathrm{dist}(R)$, which is false. So $h(R) = \mathrm{dist}(R)$. If $h(R) = \infty$, then $k_{min} = \infty$ or OPEN is empty, and $\mathrm{dist}(R) < \infty$ would give $h(R) \le \mathrm{dist}(R) < \infty$ by Lemma 2. So $\mathrm{dist}(R) = \infty$.

For line L29: the first phase starts from the state where only $G$ is OPEN and no cost has changed. In it, every OPEN state has $k = h$ and no CLOSED state is put back on OPEN. A processed state $X$ has $k_{old} = h(X)$, so lines L4 to L7 do nothing and the LOWER branch runs. In it, the second test of line L10 would need $b(Y) = X$, so $X$ would have been processed before and put back, and the third test with $Y$ CLOSED would need $h(Y) > h(X) + c$, while $Y$ was processed earlier with $h(Y) \le h(X)$, because the keys do not go down (Lemma 4 below, whose proof does not use this part). So line L11 lowers $h$ of OPEN or NEW states only, and keeps $k = h$. When $R$ becomes CLOSED, it was processed with key $h(R)$, the least key, so $h(R) \le k_{min}$ from then on, and the argument above applies. $\square$

## Termination

**Lemma 4 (keys go up).** In a phase, the keys $k_{old}$ of the processed states do not go down, and a state processed twice in a phase has a strictly larger key the second time.

*Proof.* We show that each INSERT during the processing of $X$ at key $k_{old}$ gives a key at least $k_{old}$, and strictly larger if the state was CLOSED. Lines L11 and L15 use $h_{new} = h(X) + c(Y, X) > k_{old}$, because $h(X) \ge k_{old}$. If $Y$ was CLOSED, then $h(Y) > k_{old}$ too: in the second test of line L10 or line L14, M gave $k(X) < h(Y)$ or $h(Y) = \infty$, and in the third test, $h(Y) > h(X) + c(Y, X)$. Line L17 uses $h(X) > k_{old}$ in the RAISE branch, and line L19 needs $h(Y) > k_{old}$. An OPEN state keeps a key that is at least $k_{old}$. $X$ is CLOSED after it is processed, or put back by line L17 with a larger key. $\square$

**Lemma 5 (the values are discrete).** In a phase, every finite value of $h$, and so every finite key, is $v + c_1 + \cdots + c_r$, where $v$ is a finite value of $h$ at the start of the phase and $c_1, \ldots, c_r$ are costs of arcs of the current map. For each bound $B$, only finitely many such numbers are at most $B$.

*Proof.* The new values are made at lines L7, L11 and L15 as an old value plus one arc cost, and keys are values that $h$ had. Each finite cost is at least the least finite arc cost $c_{min} > 0$, so $r \le B / c_{min}$. $\square$

**Theorem 6 (each phase stops).** Every phase has finitely many PROCESS-STATE calls.

*Proof.* Assume that a phase has infinitely many. By Lemma 4 each pair (state, key) occurs at most once. So by Lemma 5 the keys cannot stay below a finite bound. A state processed with key $\infty$ is never put back, because a later key would be strictly larger. So the finite keys are not bounded. Let $D$ be the largest finite value of $\mathrm{dist}$, and let $T_0$ be the first processing with a finite key $k_{old} > D$. Write $S_{fin}$ for the states with $\mathrm{dist} < \infty$ and $S_\infty$ for the others. An arc from $S_\infty$ to $S_{fin}$ has cost $\infty$.

- At $T_0$, every state of $S_{fin}$ is CLOSED with $h = \mathrm{dist}$, by Lemmas 2 and 1. After $T_0$, none is put back: its key would be at most $h = \mathrm{dist} \le D < k_{old}$, against Lemma 4.
- After $T_0$, line L7 never runs on a state $X \in S_\infty$. It needs $h(Q) \le k_{old}$ and $h(X) > h(Q) + c(X, Q)$. The chain claim then gives a finite path from $Q$ to $G$, and the arc $X \to Q$ is finite, so $X \in S_{fin}$.
- After $T_0$, the LOWER branch runs only with $h(X) = \infty$. If $h(X) = k_{old}$ is finite, the chain claim gives a finite path from $X$, so $X \in S_{fin}$, which is not processed.
- So after $T_0$, a pointer changes only when a NEW state gets its first pointer. With $h(X) = \infty$ the third test of line L10 is false, and line L15 does not change an existing pointer.

Now let $d(Y)$ be the number of arcs on the chain from $Y$ to $G$, which is fixed after $T_0$ by A, and at most $n - 1$. Let $B_0$ be the largest finite value at $T_0$ and $c_{max}$ the largest finite arc cost. By induction over time, every finite value after $T_0$ satisfies $h(Y) \le B_0 + d(Y)\, c_{max}$. A new value is $h(X) + c(Y, X)$ with $X = b(Y)$ and $d(Y) = d(X) + 1$. So the finite keys after $T_0$ are at most $B_0 + n\, c_{max}$, a contradiction. $\square$

**Theorem 7 (the robot).** Assume that the true costs do not change, that the first map gives each arc a cost at most its true cost, and that the robot learns the true cost of each arc out of its position before it leaves the position. Then MAIN stops. Each move uses an arc of finite true cost. If MAIN reports that there is no known path, the goal cannot be reached in the true graph from the position of the robot. If the goal can be reached in the true graph from every state that can be reached from the start, for example when the true graph is undirected and the goal can be reached from the start, the robot reaches the goal.

*Proof.* Each arc changes its map cost at most once, when it is first sensed, so there are finitely many MODIFY-COST calls, and each phase stops by Theorem 6. After a phase, $h(R) = \mathrm{dist}(R)$ by Theorem 3. If it is finite, $b(R)$ is CLOSED with $h(b(R)) = h(R) - c(R, b(R)) < h(R) \le k_{min}$. So while no change is seen, the loop of line L34 does nothing, each move lowers $h(R)$ by a positive cost, and $h(R)$ stays the distance of the robot. After the last change the robot reaches $G$, or line L31 stops it. The map costs are at most the true costs, so the map distance is at most the true distance, and line L31 stops only when the true distance is $\infty$. The arc of each move has a finite map cost, which is its true cost, because the robot sensed it. Under the last assumption, the goal can be reached from every position of the robot, so line L31 never stops it. $\square$
