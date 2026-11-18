---
title: A semijoin program never changes the answer, OPT ends, and a tree query has a full reducer
proves: [correctness, termination]
status: full
---

We use the line numbers of the pseudocode on the page. The query is $Q = R_1 \bowtie \dots \bowtie R_r$ under bag semantics, after the local selections of line L1. Attributes with the same name are joined, and a NULL in a join attribute matches nothing. A semijoin $R_i \ltimes_A R_j$, for a set $A$ of attributes common to $R_i$ and $R_j$, ships the set of non-null values $R_j[A]$ and keeps the rows $t$ of $R_i$, with their counts, for which $t[A]$ is in that set. A program is a sequence of semijoins, followed by the move of every relation to the assembly site and the join there.

There are two separate claims. The answer is always right, for any program (Theorem 1); this is a theorem about data. The program that OPT picks is cheap only in the estimated cost model; this part is a heuristic, and the page shows that it is not optimal even for its own estimates.

**Rows that take part.** A row $t$ of $R_i$ *takes part* in $Q$ if some output tuple of $Q$ restricts to $t$ on the attributes of $R_i$. Write $R'_k$ for the current state of $R_k$ while a program runs.

**Theorem 1.** For every semijoin program, the join of the reduced relations equals $Q$, with the same count for every output tuple.

*Proof.* We show by induction over the program that each $R'_k$ is a sub-bag of $R_k$ (each row keeps its count or drops out) that still holds every row of $R_k$ that takes part in $Q$. At the start $R'_k = R_k$. Take a step $R_i \ltimes_A R_j$ and a row $t$ of $R'_i$ that takes part, through an output tuple $u$. Let $s$ be the restriction of $u$ to the attributes of $R_j$. Then $s$ is a row of $R_j$ that takes part, so $s$ is in $R'_j$ by the induction hypothesis. The attributes $A$ are join attributes, so $t[A] = u[A] = s[A]$, and this value has no NULL, because a NULL matches nothing. So $t[A]$ is among the shipped values and $t$ stays. The step only drops rows, so $R'_i$ stays a sub-bag of $R_i$.

At the end, every output tuple of $Q$ is built from rows that take part, and all of them are still present with their full counts, so the join of the $R'_k$ produces each output tuple of $Q$ at least as often as $Q$ does. It cannot produce more, because the $R'_k$ are sub-bags of the $R_k$ and the join is monotone in the counts. $\square$

The theorem does not need the profile or the estimates. A wrong estimate can make a program expensive, never wrong.

**The cost of a program on data.** A semijoin between relations at different sites costs $|R_j[A]| \cdot w(A)$, the number of distinct non-null values shipped times their width, and it costs 0 at one site. The move costs $|R'_k| \cdot \mathrm{width}(R_k)$ for each relation not at the assembly site. These are the definitions that the implementation uses, and the tests check them against a count made with the reference relational operators.

**Theorem 2 (termination).** The main loop of lines L3 to L5 runs at most $q$ times, where $q$ is the number of nonlocal candidate semijoins, and the pruning of line L7 replays the program at most $2q$ times.

*Proof.* The implementation uses each candidate at most once, so the main loop picks at most $q$ semijoins and then finds no candidate. In line L7, each test either removes a semijoin from the program or moves on to the next position, and both can happen at most $q$ times. $\square$

The rule "each candidate at most once" is a choice of this implementation. The paper states the loop as "while some nonlocal semijoin has benefit > cost". With the estimates of the paper, a semijoin on $A$ also lowers the estimate for the other attributes of $R_i$ through Yao's function, and adds a new edge to their lineage. In a cyclic query, such as the triangle $R(A, B)$, $S(B, C)$, $T(C, A)$, the three semijoins can then keep lowering one another's estimates, and the loop can go on with smaller and smaller gains. The bound removes this. On the example of the paper, no semijoin is picked twice, so the bound does not change the result.

**Theorem 3 (the greedy rule and pruning).** Each step of the main loop picks a candidate of the largest estimated profit, benefit minus cost, among the unused candidates, and only if that profit is positive. Each pruning step strictly lowers the estimated cost, with the assembly site fixed. So the cost of the returned plan is at most the cost before pruning.

*Proof.* Lines L3 and L4 take the maximum over all unused candidates of the current estimates, and the loop stops when the maximum is not positive. Line L7 removes a semijoin only when the replay without it costs strictly less, and it then uses that smaller cost as the new cost. $\square$

The example of the paper shows that the plan of the main loop is not optimal for the estimated cost: OPT returns a plan of cost 2080, and pruning finds a plan of cost 1880. So the greedy rule is a heuristic; no bound on how far it is from the best program is known to us.

**Full reducers.** A program *fully reduces* the query if it leaves in each $R_k$ exactly the rows that take part in $Q$. A join tree of the query is a tree on the relations such that, for every attribute $X$, the relations that hold $X$ form a connected subtree. A query is a tree query if it has a join tree.

**Theorem 4 (Bernstein and Chiu).** Root a join tree at a relation $R_0$. For each edge from a child $c$ to its parent $p$, let $A_c$ be the set of attributes common to $c$ and $p$. The program that first does $p \ltimes_{A_c} c$ for every child $c$, children before parents, and then $c \ltimes_{A_c} p$ for every child $c$, parents before children, fully reduces the query. It has $2(r - 1)$ semijoins.

*Proof.* By the property of a join tree, an attribute that occurs both inside the subtree $T_c$ of $c$ and outside it occurs in $c$ and in $p$, so it is in $A_c$.

*Upward pass.* We show that after it, each $R'_v$ holds exactly the rows of $R_v$ that take part in the join $Q_v$ of the relations of the subtree $T_v$. For a leaf this holds with nothing done. For an inner node $v$ with children $c_1, \dots, c_m$, the children are done first. A row $t$ of $R_v$ stays if, for each child $c$, some row $s_c$ of $R'_c$ agrees with $t$ on $A_c$; by induction $s_c$ extends to an output tuple $u_c$ of $Q_c$. Two different subtrees $T_{c}$ and $T_{c'}$ share only attributes of $v$, by the property above, and on those every $u_c$ agrees with $t$. So $t$ and all the $u_c$ fit together into one output tuple of $Q_v$. Conversely, a row of $R_v$ that takes part in $Q_v$ is never dropped, by the argument of Theorem 1 applied to $Q_v$.

*Downward pass.* After the upward pass the root holds exactly the rows that take part in $Q = Q_{R_0}$. Let $p$ be a parent that is already fully reduced, and $c$ a child. A row $t$ of $R'_c$ stays if some row $s$ of $R'_p$ agrees with it on $A_c$. The row $s$ takes part in $Q$ through an output tuple $u$, and $t$ takes part in $Q_c$ through an output tuple $u_c$. The only attributes that $T_c$ shares with the rest of the tree are in $A_c$, where $t$, $s$, $u$ and $u_c$ all agree. So $u_c$ on $T_c$ and $u$ on the rest fit together into an output tuple of $Q$ that holds $t$. A row that takes part in $Q$ is never dropped, by Theorem 1. By induction from the root down, every relation ends fully reduced. $\square$

The semijoins of Theorem 4 must use all of $A_c$, not one attribute of it. Theorem 4 also allows NULLs: a row with a NULL in an attribute of $A_c$ takes part in nothing and is dropped, while a NULL in an attribute that no other relation holds does no harm.

**Cyclic queries.** For the triangle $R(A, B) = \{(0, 0), (1, 1)\}$, $S(B, C) = \{(0, 0), (1, 1)\}$, $T(C, A) = \{(0, 1), (1, 0)\}$, each semijoin between two of the relations keeps every row, because each relation has both values $0$ and $1$ in each of its attributes. So no semijoin program changes the relations, while $Q$ is empty: no program fully reduces this instance. Bernstein and Goodman showed that a query has a full reducer for every database exactly when it is a tree query. The tests check Theorem 1 on random chain, star and triangle queries with NULLs and duplicates, Theorem 4 on random tree queries, and the triangle above.
