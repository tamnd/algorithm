---
title: Redelmeier's algorithm counts each fixed polyomino exactly once
proves: [correctness]
status: full
---

We use the notation of the page. Let $\Omega$ be the allowed region, $o = (0, 0)$ the origin, and for a set $X$ of cells let $\Gamma(X)$ be the set of cells of $\Omega \setminus X$ that share an edge with a cell of $X$. A set of cells is *connected* when its cells are connected through shared edges. A *target* is a connected set $Q \subseteq \Omega$ with $o \in Q$ and $|Q| \le n$.

**Lemma 1 (translates).** For each $k \ge 1$, the map from fixed polyominoes with $k$ cells to targets of size $k$, which sends a polyomino to its translate whose first cell in the order (row, then column) is $o$, is a bijection.

*Proof.* Translation keeps the order of cells, so every polyomino has exactly one translate whose first cell is $o$. All cells of that translate come after $o$ in the order, so they lie in $\Omega$, and the translate is a target. Conversely a target $Q$ contains $o$, and every cell of $Q$ lies in $\Omega$ and so comes after $o$ or is $o$, so $o$ is its first cell and $Q$ is the image of its own class. $\square$

For a call of EXTEND$(U)$ with occupied set $P$ and reached set $R$, call the cells of $F = R \setminus (P \cup U)$ *forbidden*.

**Invariant (I).** At each call EXTEND$(U)$ with $P \ne \emptyset$: $P$ is connected, $o \in P \subseteq \Omega$, $R = P \cup \Gamma(P)$, and $U \subseteq \Gamma(P)$. At the first call, $P = \emptyset$, $R = U = \{o\}$.

**Lemma 2.** Assume (I) at a call EXTEND$(U)$. Then the call increments count$[|Q|]$ once for each connected set $Q \subseteq \Omega$ with $P \subsetneq Q$, $|Q| \le n$, $Q \cap F = \emptyset$, and, when $P = \emptyset$, $o \in Q$; it increments nothing else; and it returns with $P$ and $R$ as at the call.

*Proof.* By induction on $n - |P|$, and inside a call on the iterations of the loop. Let $c_1, \ldots, c_k$ be the cells of $U$ in the order in which line L4 removes them. Call a set $Q$ as in the claim a *goal* of the call.

*Every goal contains a cell of $U$.* If $P = \emptyset$, a goal contains $o$ and $U = \{o\}$. If $P \ne \emptyset$, a goal $Q$ is connected and strictly larger than $P$, so some cell of $Q \setminus P$ shares an edge with $P$, and it lies in $\Omega$, so it is in $\Gamma(P) \subseteq R$. It is not in $P$ and not forbidden, so it is in $U$.

So the goals split into $k$ disjoint classes: class $t$ is the set of goals whose first cell among $c_1, \ldots, c_k$ is $c_t$.

*Iteration $t$.* Lines L4 and L5 make $P' = P \cup \{c_t\}$ and count $P'$ once. $P'$ is a goal of class $t$: it is connected, since $c_t$ is $o$ or shares an edge with $P$; it lies in $\Omega$; it has no forbidden cell; and $|P'| \le n$ because the call at level $|P|$ happens only when $|P| < n$. If $|P'| = n$, the class has no other goal, since goals have at most $n$ cells, and the iteration ends by line L11. Otherwise, line L7 takes $N = \Gamma(\{c_t\}) \setminus R$, and line L8 makes $R' = R \cup N$. Since $\Gamma(P') = (\Gamma(P) \setminus \{c_t\}) \cup (\Gamma(\{c_t\}) \setminus P)$, and the cells of $\Gamma(\{c_t\}) \setminus P$ outside $R$ are exactly $N$, we get $R' = P' \cup \Gamma(P')$. The untried set of the inner call is $U' = \{c_{t+1}, \ldots, c_k\} \cup N \subseteq \Gamma(P')$. So (I) holds at the inner call. Its forbidden set is

$$F' = R' \setminus (P' \cup U') = F \cup \{c_1, \ldots, c_{t-1}\},$$

because $R' \setminus P'$ consists of $F$, the cells $c_1, \ldots, c_k$ other than $c_t$, and $N$, and $U'$ removes exactly $c_{t+1}, \ldots, c_k$ and $N$. By the induction hypothesis, the inner call counts once each connected $Q \subseteq \Omega$ with $P' \subsetneq Q$, $|Q| \le n$ and $Q \cap F' = \emptyset$. These are exactly the goals of class $t$ other than $P'$: a goal of class $t$ contains $P'$, avoids $F$, and avoids $c_1, \ldots, c_{t-1}$ by the choice of $t$; and conversely such a $Q$ is a goal whose first cell among the $c_j$ is $c_t$. Line L10 removes $N$ from $R$, and line L11 removes $c_t$ from $P$, so the state is as at the start of the iteration, except that $c_t$ has left $U$.

So iteration $t$ counts class $t$ exactly once. The classes are disjoint and cover all goals, so the call counts each goal once. After the last iteration $P$ and $R$ are as at the call. $\square$

**Theorem.** After REDELMEIER$(n)$, count$[k] = a(k)$ for $k = 1, \ldots, n$.

*Proof.* At the first call $P = \emptyset$ and $F = R \setminus U = \emptyset$, so by Lemma 2 the run counts each connected $Q \subseteq \Omega$ with $o \in Q$ and $|Q| \le n$ exactly once, in count$[|Q|]$. These are the targets, and by Lemma 1 the targets of size $k$ are in bijection with the fixed polyominoes with $k$ cells. $\blacksquare$

**Termination.** Each inner call has a larger $P$, the depth is at most $n$, and each loop removes a cell from a finite set at each iteration.
