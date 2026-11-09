---
title: Dynamic backtracking is complete and uses polynomial space
proves: [correctness]
status: full
---

We use the pseudocode of the page. $\sigma$ is the current partial assignment, $P$ the list of assigned variables in the order they were assigned, and an elimination is a value $(x, b)$ with an explanation $E(x, b)$, a set of variables. For a set $S$ of variables, a solution $\tau$ *agrees with* $\sigma$ on $S$ if $\tau(z) = \sigma(z)$ for every $z \in S$. An elimination is *valid* if every variable of $E(x, b)$ is assigned and no solution agrees with $\sigma$ on $E(x, b)$ and gives $b$ to $x$.

We first treat the mode that stops at the first solution.

**Lemma 1 (invariant).** At the start of each iteration of line L2:

1. every stored elimination is valid;
2. the assigned variables satisfy every constraint between two of them;
3. at most one elimination is stored for each pair $(x, b)$, and no assigned variable has its current value eliminated.

*Proof.* At the start nothing is assigned or eliminated. Assume the invariant at the start of an iteration, and let $x$ be the variable of line L3.

*Line L4.* It eliminates $(x, b)$ with $E = \{y\}$ only if $b$ is not yet eliminated and $(\sigma(y), b)$ violates the constraint between $y$ and $x$. Then $y$ is assigned, and a solution that gives $\sigma(y)$ to $y$ cannot give $b$ to $x$. So the new elimination is valid, and part 3 holds since $x$ is unassigned.

*Lines L5 and L6.* The value given to $x$ is not eliminated. Every value that conflicts with a variable of $P$ was eliminated at line L4, unless it was already eliminated, so the new value conflicts with no assigned variable, and part 2 holds. No elimination changes. Part 3 holds because the value of $x$ is not eliminated.

*A dead end, lines L7 to L13.* Every value of $x$ is eliminated, with explanations that are subsets of $U$. All of them are valid. A solution that agrees with $\sigma$ on $U$ gives some value $b \in D(x)$ to $x$, and it also agrees with $\sigma$ on $E(x, b) \subseteq U$, which contradicts the validity of $(x, b)$. So no solution agrees with $\sigma$ on $U$.

If $U = \emptyset$, then no solution exists, and line L9 is right. Otherwise let $y$ be the variable of $U$ latest in $P$, and $v = \sigma(y)$. No solution agrees with $\sigma$ on $U \setminus \{y\}$ and gives $v$ to $y$. Line L11 unassigns $y$ and changes no other variable. Line L12 deletes every elimination whose explanation contains $y$. Every elimination that is left has an explanation of assigned variables with unchanged values, so it is still valid. Line L13 stores $(y, v)$ with $E = U \setminus \{y\}$. Its variables are assigned and unchanged, and we showed above that it is valid. There was no elimination of $(y, v)$ before, by part 3, since $y$ had the value $v$. Removing a variable keeps part 2. $\square$

**Theorem 1 (soundness).** If line L14 is reached, $\sigma$ is a solution.

*Proof.* All variables are assigned, and by part 2 of Lemma 1 every constraint holds. $\square$

**Lemma 2 (termination).** The loop ends.

*Proof.* For a stored elimination, let its *anchor* be the position in $P$ (counting from 1) of the variable of its explanation that comes last in $P$, or 0 if the explanation is empty. By part 1 of Lemma 1 all variables of an explanation are assigned, so the anchor is defined. Let $c_k$ be the number of eliminations with anchor $k$, and let $V = (c_0, c_1, \ldots, c_{|P|})$. Order these vectors lexicographically, with a proper prefix smaller than its extensions. We show that $V$ grows strictly in each iteration.

- Line L4 adds eliminations and deletes none. Their anchors are positions of variables in $P$. So each $c_k$ stays or grows.
- If line L6 runs, $P$ gets one more position at the end, with $c_{|P|} = 0$ for the new last position, since no explanation contains the new variable. Together with line L4, $V$ becomes an extension of a vector that is at least the old one, so $V$ is strictly larger.
- At a dead end, let $p \ge 1$ be the position of $y$ in $P$. An elimination deleted at line L12 contains $y$, so its anchor is at least $p$. Removing $y$ from $P$ moves the positions after $p$ down by one and does not change the positions before $p$. So $c_0, \ldots, c_{p-1}$ change only by line L13. The new elimination has the explanation $U \setminus \{y\}$, and all its variables come before $y$ in $P$, because $y$ is the last variable of $U$ in $P$. So its anchor is some $q < p$. Hence $c_0, \ldots, c_{q-1}$ do not change and $c_q$ grows by 1, and $V$ is strictly larger, whatever happens after position $q$. With line L4 earlier in the same iteration, which only made $V$ larger, the claim holds.

By part 3 of Lemma 1, there are at most $\sum_x |D(x)| \le n d$ eliminations, so each $c_k$ is at most $n d$, and $V$ has at most $n + 1$ entries. There are at most $(n + 2)(n d + 1)^{n+1}$ such vectors. A strictly increasing sequence of them is at most this long. $\square$

**Theorem 2 (completeness).** If the problem has a solution, dynamic backtracking returns one. If it returns failure, there is no solution.

*Proof.* By Lemma 2 the loop ends. It ends at line L9 or at line L14. At line L9, the proof of Lemma 1 shows that no solution exists. So if a solution exists, the loop ends at line L14, which returns a solution by Theorem 1. $\square$

**Theorem 3 (polynomial space).** At every time at most $n d$ eliminations are stored, each with an explanation of at most $n$ variables, so the space is $O(n^2 d)$ words besides the input.

*Proof.* Part 3 of Lemma 1 gives one elimination per pair $(x, b)$, and there are at most $n d$ such pairs. An explanation is a set of variables. The list $P$, the assignment and the positions take $O(n)$. $\square$

**All solutions.** In the all-solutions mode, when all variables are assigned, the search records $\sigma$ and then runs lines L10 to L13 with $U = P$. Replace "no solution" in the definition of a valid elimination by "no solution that is not yet recorded". The new elimination of $(y, \sigma(y))$ with the explanation $P \setminus \{y\}$ is valid in this sense: the only solution that agrees with $\sigma$ on every other variable and gives $\sigma(y)$ to $y$ is $\sigma$, which is recorded. The proofs of Lemma 1 and Lemma 2 go through without change (the anchor of the new elimination is the position before $y$, which is the last position of $P$). The loop ends at line L9, with no unrecorded solution left. So every solution is recorded, and each recorded assignment is a solution. The tests also check, by brute force, that no solution is recorded twice. $\blacksquare$
