---
title: The ground SLG evaluator terminates and gives each tabled atom its well-founded value
proves: [correctness, termination]
status: full
---

Chen and Warren (1996) proved that SLG resolution is sound and complete for the well-founded semantics of programs with finite ground instances. This file proves the same for the small evaluator of the page and its Python file, which works on a finite ground normal program $P$ and one query atom $q$. The line numbers refer to the pseudocode on the page.

## Notation

Let $(T^*, F^*)$ be the well-founded model of $P$: the least fixpoint of the operator $W_P(T, F) = (T_P(T, F), \mathrm{GUS}(T, F))$ of Van Gelder, Ross and Schlipf, where $T_P(T, F)$ is the set of heads of the rules whose body is true in $(T, F)$ and $\mathrm{GUS}$ is the greatest unfounded set. A set $X$ is unfounded with respect to $(T, F)$ if each rule with its head in $X$ has (i) a body literal that is false in $(T, F)$, or (ii) a positive body atom in $X$. The operator is monotone, so $(T^*, F^*) \le I$ for every $I$ with $W_P(I) \le I$.

A table is *true* once it has an answer with an empty delay, *false* once it is complete and has no answers, and *undefined* if it is complete and has conditional answers. A node $(h \leftarrow G \mid D)$ belongs to a rule of $h$; at line L4 it is taken from the work list, and each step gives it at most one successor: the same rule with one literal fewer in $G$.

## Termination

Each rule of a tabled atom starts one chain of nodes (line L30), and each node has at most one successor, which it gets at once (lines L8, L9, L13, L14) or after a wait in exactly one list, from which it leaves at most once (line L34 for a consumer, line L20 or L28 for a negative waiter, or never). So the number of nodes is at most the number of rules plus the number of body literals, $s$. Each answer comes from the last node of a chain, so there are at most as many answers as rules. SIMPLIFY stops because each change deletes a literal or an answer or makes a table true. Each pass of the main loop that does not stop either moves at least one waiting node to the work list (line L20) or completes at least one table (line L22). So there are at most $2s$ passes, and the evaluation stops.

## Soundness of true and false

We show by induction over the sequence of events that every table that becomes true is in $T^*$ and every table that becomes false is in $F^*$. The induction uses one invariant:

**(N)** For each node $(h \leftarrow G \mid D)$ and each answer $(h \mid D)$, there is a rule of $P$ with head $h$ whose body consists of the literals of $G$, the literals of $D$, and literals that were true by the table statuses when they were removed.

It holds for the first node of each chain. Each step either removes a literal that is true at that time (line L8: $b$ true; line L13: $b$ false, so $\mathit{not}\ b$ true; SIMPLIFY and line L31: true literals), or moves a literal from $G$ to $D$ (lines L9, L14, L20, L28). Statuses never go back: a true table stays true, and a false table is complete and gets no new answer, because no node of a complete table is left (see the last section).

*True.* A table becomes true when an answer has an empty delay. By (N) and the induction hypothesis, the body of its rule is true in $(T^*, F^*)$, so the head is in $T_P(T^*, F^*) = T^*$.

*False.* Tables become false only while a component $C$ is completed, at line L22 (the tables of $C$ with no answers) and at line L26 (the deleted atoms). Let $Y$ be the set of atoms of $C$ that have no answers after one of these events, together with the atoms deleted at that event. We show that $Y$ is unfounded with respect to $(T^*, F^*)$, so $Y \subseteq F^*$. Take $a \in Y$ and a rule $r$ of $a$. The chain of $r$ ended in one of these ways.

- It was dropped because a literal was false: $\mathit{not}\ b$ with $b$ true (line L12, or line L31 or SIMPLIFY), or $b$ with $b$ false. By induction, this literal of $r$ is false in $(T^*, F^*)$: case (i).
- It waits as a consumer of $b$, which has had no answer since then. If $b$ was complete earlier, it is false, and case (i) holds. Otherwise $b$ is incomplete when $C$ is chosen; since $C$ is a sink of the call graph on the incomplete tables, $b \in C$, and $b$ has no answers, so $b \in Y$: case (ii).
- It waits negatively. This is not possible: $C$ is completed only when no node of a table of $C$ waits on a table of $C$, and a wait on a table outside $C$ ended when that table was completed.
- It gave an answer that is still present when the atom is deleted at line L26. Then $a \notin S$, so the delay of the answer has a positive literal $b$ with $b \in C \setminus S$. The table $b$ is not true, because SIMPLIFY at line L24 removed the true literals, so $b$ has no answers or is itself deleted: $b \in Y$, and $b$ is in the body of $r$ by (N): case (ii).
- It gave an answer whose delay equals that of an answer already present. The same argument applies to that delay, which by (N) is also part of the body of $r$.

The head of $r$ is not true, since $a \in Y$. So every rule of $a$ satisfies (i) or (ii).

## Completeness

Let $V$ be the final statuses. At the end every table is complete. Let $I' = (T', F')$, where $T'$ is the set of true tables together with the atoms of $T^*$ that have no table, and $F'$ the set of false tables together with the atoms of $F^*$ that have no table. By soundness, $I' \le (T^*, F^*)$. We show that $W_P(I') \le I'$; then $(T^*, F^*) \le I'$, so the two are equal, and each undefined table is neither in $T^*$ nor in $F^*$.

*Final answers.* After $C$ is completed, each delay of an answer of $C$ mentions only tables of $C$ or of components completed before. These tables have no nodes left and do not change again, by induction on the order of completion, so the answers of $C$ do not change either. By the last SIMPLIFY, the literals of the final delays are all on undefined tables.

*$T_P(I') \subseteq T'$.* Let $r$ be a rule of $a$ whose body is true in $I'$. If $a$ has no table, the body is true in $(T^*, F^*)$, since $I' \le (T^*, F^*)$, so $a \in T^*$. Otherwise follow the chain of $r$. Each literal it reaches is called, so it is on a table, and it is true in $V$. A positive literal $b$ on a true table either continues the chain at once (line L8 or L9) or waits until the first answer of $b$, which comes because $b$ ends true (line L34). A negative literal $\mathit{not}\ b$ with $b$ false continues the chain at line L13 or L14, or waits until line L20 or L28 moves it on. So the chain gives an answer $(a \mid D)$ in which every literal ends true, unless $a$ is already true. Such an answer is never deleted: SIMPLIFY deletes only answers with a false literal, and line L26 does not delete it either. To see this, order the atoms of $C$ that end true by the time at which they become true. At an iteration of lines L23 to L27, the first of them that is not yet true has an answer whose positive delayed atoms of $C$ became true before it, so there are none left after line L24, and the atom is in $S$; by induction on the order, every later one is in $S$ too. The answer $(a \mid D)$ has only such atoms as positive delayed atoms of $C$, so $a \in S$. In the end all literals of $D$ are removed, and $a$ is true.

*$\mathrm{GUS}(I') \subseteq F'$.* Let $X$ be unfounded with respect to $I'$. Since $I' \le (T^*, F^*)$, $X$ is also unfounded with respect to $(T^*, F^*)$, so $X \subseteq F^*$. The atoms of $X$ without a table are then in $F'$, and no atom of $X$ is a true table. Suppose that some atoms of $X$ are undefined tables, and let $C$ be the first completed component that contains one of them. Take such an atom $a \in X \cap C$ and a final answer $(a \mid D)$, from a rule $r$. By (N), the body of $r$ is $D$ plus literals true in $I'$. The literals of $D$ are on undefined tables, so no literal of $r$ is false in $I'$, and the positive literals outside $D$ are in $T'$, which is disjoint from $X$. As $X$ is unfounded, $D$ contains a positive literal $b \in X$. The table $b$ is undefined, and it is in $C$ or in a component completed before $C$; by the choice of $C$, $b \in C$. So every final answer of every atom of $X \cap C$ has a positive delayed atom in $X \cap C$. The last iteration of lines L23 to L27 for $C$ deleted nothing, so $S$ contained every atom of $C$ with an answer, including the atoms of $X \cap C$. But the least fixpoint $S$ never adds a first atom of $X \cap C$, because each of its answers needs another atom of $X \cap C$ to be in $S$ already. This is a contradiction, so every atom of $X$ with a table is false.

## Why answer completion is needed

Without lines L23 to L27, a positive loop through delayed literals can keep an atom undefined when it is false. Take $a \leftarrow \mathit{not}\ b$, $b \leftarrow c, b$, $c \leftarrow \mathit{not}\ a$, $c \leftarrow c, \mathit{not}\ c$ and the query $a$. All three tables end up in one component, with the negative waits of $a$ on $b$ and of $c$ on $a$ and then of $c$ on $c$. Delaying gives the answers $a \mid \{\mathit{not}\ b\}$, $c \mid \{\mathit{not}\ a\}$ and $c \mid \{c, \mathit{not}\ c\}$. At completion, $b$ has no answers and is false, so $a$ becomes true and the answer $c \mid \{\mathit{not}\ a\}$ is deleted. The answer $c \mid \{c, \mathit{not}\ c\}$ has no false literal, so SIMPLIFY keeps it, but in the well-founded model $c$ is false: $\{c\}$ is unfounded. Answer completion finds that $c \notin S$ and deletes it.

## What the tests check

For every atom of every random program, the tests run the evaluator with that atom as the query and compare every tabled atom with the well-founded model. The well-founded model is computed from the definition with unfounded sets (programs with at most 6 atoms) and with the alternating fixpoint written with the plain functions of `lp.py` (programs with at most 12 atoms). They also check that only atoms reachable from the query are tabled, that a shuffle of the rules and of the body literals does not change the result, and the examples of the page.
