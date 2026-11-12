---
title: Schorr-Waite marking marks exactly the reachable cells and restores every pointer
proves: [correctness, termination]
status: full
---

**Setting.** The heap has binary cells. Each cell $c$ has the fields $c.\mathit{left}$ and $c.\mathit{right}$ (a cell or nil), a mark bit and a flag bit. A *state* is the content of all fields, marks and flags, together with the values of the variables $t$ and $p$, taken at the test of line L2. One *iteration* is one pass of the loop: an advance (lines L3 to L5), a swing (lines L7 and L8), a retreat (lines L9 and L10), or the return at line L6.

For a set $M$ of marked cells and a value $x$ (a cell or nil), let $U(x, M)$ be the set of cells $z$ such that there is a path $x = v_0, v_1, \ldots, v_k = z$ with $k \ge 0$, each $v_{i+1}$ a field of $v_i$, and every $v_i \notin M$. So $U(x, M)$ is empty when $x$ is nil or $x \in M$. Fields here are the original fields of the heap, the ones it holds before the call. Write $\ell(x)$ and $r(x)$ for the original left and right field of a cell $x$.

**Lemma 1 (splitting a search).** Let $x \notin M$, let $M_1 = M \cup \{x\}$, $M_2 = M_1 \cup U(\ell(x), M_1)$ and $M_3 = M_2 \cup U(r(x), M_2)$. Then $M \cup U(x, M) = M_3$.

*Proof.* ($\supseteq$) The cell $x$ is in $U(x, M)$ by the path of length 0. A path from $\ell(x)$ that avoids $M_1$ avoids $M$, so putting $x$ in front of it gives a path from $x$ that avoids $M$; so $U(\ell(x), M_1) \subseteq U(x, M)$. In the same way, since $M_2 \supseteq M$, $U(r(x), M_2) \subseteq U(x, M)$.

($\subseteq$) Take $z \in U(x, M)$ and a shortest path $x = v_0, \ldots, v_k = z$ that avoids $M$. Because it is shortest, $v_i \ne x$ for $i \ge 1$. If $k = 0$, $z = x \in M_1$. Otherwise $v_1$ is $\ell(x)$ or $r(x)$, and the path $v_1, \ldots, v_k$ avoids $M_1$. If $v_1 = \ell(x)$, then $z \in U(\ell(x), M_1)$. If $v_1 = r(x)$ and the path $v_1, \ldots, v_k$ avoids $M_2$, then $z \in U(r(x), M_2)$. Otherwise some $v_j$ lies in $M_2 \setminus M_1 = U(\ell(x), M_1)$. Join a path from $\ell(x)$ to $v_j$ that avoids $M_1$ with the path $v_j, \ldots, v_k$, which also avoids $M_1$. The result is a path from $\ell(x)$ to $z$ that avoids $M_1$, so $z \in U(\ell(x), M_1)$. $\square$

**Lemma 2 (the visit lemma).** Let $S$ be a state with $t = x$ and $p = y$, where $y$ is nil or a marked cell, in which every cell holds its original fields, except that the cells on the current path back to the root hold reversed fields, and none of those cells is in $U(x, M)$, where $M$ is the set of marked cells of $S$. Then the run from $S$ reaches, after exactly $3\,|U(x, M)|$ iterations and without returning, a state $S'$ with:

- $t = x$ and $p = y$;
- every field of every cell equal to its value in $S$;
- the set of marked cells equal to $M \cup U(x, M)$;
- the flag of every cell outside $U(x, M)$ equal to its value in $S$.

*Proof.* By strong induction on the number $u$ of unmarked cells in $S$.

*Case 1: $x$ is nil or marked.* Then $U(x, M)$ is empty, and $S' = S$ after 0 iterations satisfies all four points. This covers $u = 0$.

*Case 2: $x$ is an unmarked cell.* The cell $x$ is unmarked, so it is not on the path back to the root, whose cells are all marked; so $x$ holds its original fields $\ell(x)$ and $r(x)$. The run goes in five parts.

1. The test of line L3 holds. Lines L4 and L5 mark $x$, set its flag to 0, set $x.\mathit{left} \leftarrow y$, $p \leftarrow x$ and $t \leftarrow \ell(x)$. One iteration. Now the marked set is $M_1 = M \cup \{x\}$, and the path back to the root has $x$ added on top.
2. The new state has $t = \ell(x)$ and $p = x$, a marked cell, and $u - 1$ unmarked cells. Its reversed cells are the old ones and $x$, all marked, so none of them is in $U(\ell(x), M_1)$. By the induction hypothesis, after $3\,|U(\ell(x), M_1)|$ iterations the run reaches a state with $t = \ell(x)$, $p = x$, all fields as after part 1 (so $x.\mathit{left} = y$ and $x.\mathit{right} = r(x)$), marked set $M_2 = M_1 \cup U(\ell(x), M_1)$, and the flag of $x$ still 0, because $x \in M_1$ is outside $U(\ell(x), M_1)$.
3. Now $t = \ell(x)$ is nil or marked: if it was unmarked in $M_1$, it is in $U(\ell(x), M_1) \subseteq M_2$. So the test of line L3 fails. The test of line L6 fails because $p = x$. The flag of $x$ is 0, so lines L7 and L8 run: $q = r(x)$, $x.\mathit{right} \leftarrow y$, $x.\mathit{left} \leftarrow \ell(x)$, flag of $x \leftarrow 1$, $t \leftarrow r(x)$. One iteration. The left field of $x$ is now restored, and its right field holds the path back.
4. The state has $t = r(x)$, $p = x$ marked, and at most $u - 1$ unmarked cells. By the induction hypothesis, after $3\,|U(r(x), M_2)|$ iterations the run reaches a state with $t = r(x)$, $p = x$, all fields as after part 3, marked set $M_3 = M_2 \cup U(r(x), M_2)$, and the flag of $x$ still 1.
5. As in part 3, $t$ is nil or marked, and $p = x$. The flag of $x$ is 1, so lines L9 and L10 run: $q = y$, $x.\mathit{right} \leftarrow r(x)$, $t \leftarrow x$, $p \leftarrow y$. One iteration.

After part 5, $t = x$ and $p = y$. The fields of $x$ are $\ell(x)$ and $r(x)$, as in $S$, and every other field is as in $S$, because parts 2 and 4 restore them and parts 1, 3 and 5 write only the fields of $x$. By Lemma 1 the marked set is $M_3 = M \cup U(x, M)$. The flags written are the flag of $x$ and, inside parts 2 and 4, flags of cells in $U(\ell(x), M_1) \cup U(r(x), M_2) \subseteq U(x, M)$, so the flags outside $U(x, M)$ are unchanged. The number of iterations is $3 + 3|U(\ell(x), M_1)| + 3|U(r(x), M_2)|$. The three sets $\{x\}$, $U(\ell(x), M_1)$ and $U(r(x), M_2)$ are pairwise disjoint (the second avoids $M_1 \ni x$, the third avoids $M_2$, which holds the first two), and their union is $U(x, M)$ by Lemma 1. So the count is $3\,|U(x, M)|$. $\square$

**Theorem.** Let the heap hold its original fields, let $M$ be its set of marked cells, and call SW-MARK$(\mathit{root})$. The call returns after exactly $3\,|U(\mathit{root}, M)| + 1$ iterations. On return, every field of every cell equals its original value, and the marked set is $M \cup U(\mathit{root}, M)$. In particular, if no cell is marked at the start, the call marks exactly the cells reachable from the root.

*Proof.* Line L1 gives the state $t = \mathit{root}$, $p = $ nil, with no reversed fields. Lemma 2 applies with $y = $ nil, and the run reaches $t = \mathit{root}$, $p = $ nil, all fields restored, after $3\,|U(\mathit{root}, M)|$ iterations. Then $t$ is nil or marked, so the test of line L3 fails, and line L6 returns. That is one more iteration. $\square$

**Corollary (many roots).** Calls for the roots $r_1, \ldots, r_m$ in turn, from a heap with no marks, leave marked exactly the set $R$ of cells reachable from some root, restore every field, and take $3|R| + m$ iterations in total.

*Proof.* Let $M_0 = \emptyset$ and $M_i = M_{i-1} \cup U(r_i, M_{i-1})$. By the theorem, call $i$ turns $M_{i-1}$ into $M_i$ and takes $3|M_i \setminus M_{i-1}| + 1$ iterations; the sum telescopes to $3|M_m| + m$. Each $M_i$ holds only reachable cells. Conversely, take $z$ reachable from $r_i$ by a path $r_i = v_0, \ldots, v_k = z$. If the path avoids $M_{i-1}$, then $z \in U(r_i, M_{i-1}) \subseteq M_i$. Otherwise let $v_j$ be its last cell in $M_{i-1}$; then $v_j \in M_h \setminus M_{h-1}$ for some $h < i$, so $v_j \in U(r_h, M_{h-1})$. If $j = k$, $z = v_j \in M_m$. Otherwise the cells $v_{j+1}, \ldots, v_k$ avoid $M_{i-1} \supseteq M_{h-1}$, and $v_j$ is not in $M_{h-1}$, so the path from $r_h$ to $v_j$ followed by $v_{j+1}, \ldots, v_k$ avoids $M_{h-1}$, and $z \in U(r_h, M_{h-1}) \subseteq M_m$. So $M_m = R$. $\blacksquare$

**Remark.** The proof uses only the original fields $\ell$ and $r$ and the fact that the reversed cells are marked. This is the reason the induction works: a cell on the path back is marked, so no search below it can enter it and read a reversed field. Mechanized proofs of the same algorithm exist in Hoare logic (Bornat 2000) and in Isabelle/HOL (Mehta and Nipkow 2003).
