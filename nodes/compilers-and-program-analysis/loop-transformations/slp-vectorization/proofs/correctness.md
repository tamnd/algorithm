---
title: SLP vectorization emits legal SIMD groups in an order that computes the same values
proves: [correctness]
status: full
---

A *location* is a scalar name or a memory cell. A statement reads some locations and writes one. Statements $s_a$ and $s_b$ with $a < b$ have a dependence $s_a \to s_b$ if they touch a common location and at least one of them writes it. We write $s \leadsto t$ if there is a path of dependences from $s$ to $t$. Two statements are independent if neither $s \leadsto t$ nor $t \leadsto s$. A group runs by reading all operands of all its lanes from the current state, and then writing all results.

**Lemma 1 (pairs).** Every pair $(s, t)$ in $P$ has $s$ and $t$ isomorphic and independent, and if they access memory, $t$ accesses the cell right after the cell of $s$. Every statement is the left element of at most one pair and the right element of at most one pair.

*Proof.* Lines L1, L4 and L5 add a pair only after CANPACK accepts it, and CANPACK checks exactly these facts against the current $P$. A pair is never removed. $\square$

By the second statement of Lemma 1, the pairs form disjoint simple paths and cycles in the graph whose edges are the pairs. Line L6 walks each path from its start, and each cycle from some member, and cuts it into pieces.

**Lemma 2 (groups).** Each group $g = (g_1, \dots, g_m)$ produced by line L6 has $2 \le m \le VL$, all members are pairwise isomorphic and pairwise independent, and if they access memory, $g_{k+1}$ accesses the cell after $g_k$ for each $k$.

*Proof.* Consecutive members form a pair of $P$, so by Lemma 1 they are isomorphic and, for memory, adjacent. Isomorphism is an equivalence relation (same kind and same array or operator), so all members are isomorphic. Line L6 adds a member to the current group only if it is independent of every member already in it and the group has fewer than $VL$ members; otherwise it starts a new group. So all members are pairwise independent and $m \le VL$. Groups of one member are dropped and run as scalar statements. $\square$

**Lemma 3 (schedule).** The loop of lines L7 to L10 ends. It emits every statement exactly once. For every dependence $s \to t$, the item of $s$ is emitted strictly before the item of $t$.

*Proof.* Let $f$ be the first statement, in text order, that is not yet emitted. Every predecessor $p$ of $f$ has $p < f$, so it is emitted. If $f$ is not in a group, its item $\{f\}$ is ready, and line L8 finds an item. So when no item is ready, $f$ is in a group, and line L10 removes that group. Every round either emits at least one statement or removes a group, so after at most $n$ emissions and $n$ removals the loop ends with all statements emitted. An emitted item is marked done as a whole, so no statement is emitted twice.

Take a dependence $s \to t$. If $s$ and $t$ were in one item, that item would be a group with $s \leadsto t$, against Lemma 2 (a split only makes smaller items). So they are in different items. Line L8 emits the item of $t$ only when every predecessor of every member is emitted, so $s$ is emitted earlier. $\square$

**Lemma 4 (one group is a sequence).** Running a group as one instruction gives the same state as running its members one by one in lane order.

*Proof.* The members are pairwise independent, so in particular no two of them have a dependence: no member reads a location that another member writes, and no two members write the same location. In the sequential run, each member reads only locations that no other member writes, so it reads the values of the state before the group, as the SIMD run does. The members write different locations, so the order of the writes does not matter. $\square$

**Theorem.** For every initial state, the emitted code computes the same final values of all locations as the block $B$.

*Proof.* By Lemma 4, the emitted code is the same as the sequential run of a permutation $\sigma$ of the statements of $B$ (the items in order, the lanes of each group in lane order). By Lemma 3, $\sigma$ keeps the order of every dependent pair. We show by induction along $B$ that each statement $t$ reads the same values in $\sigma$ as in $B$, and so writes the same value.

Take a location $\ell$ that $t$ reads. If no statement before $t$ in $B$ writes $\ell$, then no such statement exists before $t$ in $\sigma$ either: a writer $w$ of $\ell$ after $t$ in $B$ has the dependence $t \to w$, so it stays after $t$. So $t$ reads the initial value in both. Otherwise let $w$ be the last writer of $\ell$ before $t$ in $B$. The dependence $w \to t$ keeps $w$ before $t$ in $\sigma$. Any other writer $w'$ of $\ell$ before $t$ in $B$ comes before $w$ in $B$ and has the dependence $w' \to w$, so it stays before $w$. Any writer after $t$ in $B$ stays after $t$. So the last writer of $\ell$ before $t$ in $\sigma$ is $w$. By the induction hypothesis $w$ writes the same value in both runs, so $t$ reads the same value.

For the final state, the last writer of each location in $B$ stays after all other writers of that location, by the output dependences, and it writes the same value. Locations that no statement writes keep their initial values. $\square$

The proof uses none of the heuristic choices: which seeds line L1 tries first, which candidate lines L4 and L5 accept, or where line L6 starts a cycle. Those choices change only how many statements end up in groups.
