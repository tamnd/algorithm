---
title: Allen's propagation keeps every solution and ends with a closed network
proves: [correctness, termination]
status: full
---

The network holds a label $R_{ab}$ for each ordered pair of distinct intervals, a set of Allen's 13 base relations, with $R_{ba} = R_{ab}^{\smile}$ at all times, because lines L4, L10 and L13 write a label and its converse together. A *solution* is an assignment of real intervals that satisfies every constraint added so far. The network is *closed* when $R_{ac} \subseteq R_{ab} \circ R_{bc}$ for all distinct $a, b, c$. Two facts about the table are used:

- **(T1) converse rule.** $(r \circ s)^{\smile} = s^{\smile} \circ r^{\smile}$.
- **(T2) soundness.** If $x \mathrel{r} y$ and $y \mathrel{s} z$ for intervals $x, y, z$, then $x \mathrel{(r \circ s)} z$. This holds because the table is the exact set of base relations between $x$ and $z$ over all configurations of three intervals.

Both are checked by the tests of this page over the whole table.

**Claim.** Suppose the network is closed and every solution of the earlier constraints satisfies all labels. Then ADD$(i, j, S)$ returns OK or CONTRADICTION after at most $1 + 12 \binom{n}{2}$ pops. On OK, the network is closed and its solutions are exactly the solutions of the earlier constraints together with $i \mathrel{S} j$. On CONTRADICTION, there is no such solution.

**Lemma 1 (no solution is lost).** Every solution of the constraints added so far, including $i \mathrel{S} j$, satisfies every label at every step.

*Proof.* Line L1 intersects $R_{ij}$ with $S$, and a solution of the new constraint satisfies both. Lines L8 and L11 intersect a label with a composition of two labels. By (T2), a solution that satisfies those two labels also satisfies the composition. By induction on the steps, no solution is removed. $\square$

So if a label becomes empty at line L2, L9 or L12, there is no solution, and CONTRADICTION is correct.

**Lemma 2 (queue invariant).** While the loop runs, every *violated triple* $(a, b, c)$, one with $R_{ac} \not\subseteq R_{ab} \circ R_{bc}$, has $\{a, b\}$ or $\{b, c\}$ in the queue.

*Proof.* Before ADD, the network is closed. Line L4 shrinks only the label of $\{i, j\}$. A smaller $R_{ac}$ cannot break $R_{ac} \subseteq R_{ab} \circ R_{bc}$, so every new violated triple has $\{i, j\}$ as $\{a, b\}$ or $\{b, c\}$, and $\{i, j\}$ is in the queue.

When line L6 pops $\{p, q\}$, the triples that rely on it are those with $\{p, q\}$ as one of the two composed pairs. For a third interval $k$ there are four: $(p, q, k)$, $(k, p, q)$, $(q, p, k)$ and $(k, q, p)$. Line L8 makes $(p, q, k)$ hold and line L11 makes $(k, p, q)$ hold. By (T1), $(q, p, k)$ is the converse of $(k, p, q)$ and $(k, q, p)$ is the converse of $(p, q, k)$, so they hold too. Later steps can break one of these triples only by shrinking one of its composed labels other than $R_{pq}$, which the loop never changes while it handles $\{p, q\}$; every such shrink, at line L10 or L13, pushes that pair. Every other triple that a shrink can break has the shrunk pair as a composed pair, and that pair is pushed. So the invariant holds after each step. $\square$

**Proof of the claim.** When the queue is empty, Lemma 2 says no triple is violated, so the network is closed. By Lemma 1 every solution of all constraints satisfies all labels, and the labels hold every constraint (the earlier ones by assumption and $S$ by line L1), so a solution of the labels is a solution of the constraints. For the count: a pair enters the queue only when its label shrinks (lines L4, L10 and L13), and a label of at most 13 base relations that stays non-empty shrinks at most 12 times over the whole life of the network. $\blacksquare$

**Termination and cost.** Over any sequence of $a$ calls of ADD on a network of $n$ intervals, the number of pops is at most $12 \binom{n}{2}$ in total, and each pop does $2(n - 2)$ revisions of constant cost, because the table has fixed size. A call that changes nothing stops at line L3. The total is $O(n^3 + a)$, and a single call takes $O(n^3)$ time in the worst case.

**What the claim does not say.** A closed network can have no solution; the tests of this page contain one with 4 intervals. Closure decides consistency only for some subclasses, such as the ORD-Horn relations (Nebel and Bürckert 1995).
