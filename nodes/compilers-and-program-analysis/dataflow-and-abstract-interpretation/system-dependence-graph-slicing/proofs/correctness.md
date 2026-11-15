---
title: Summary edges are exact, and the two passes find exactly the nodes on realizable paths to the criterion
proves: [correctness, termination, complexity]
status: full
---

**Setting.** The system and its graph are as on the page. Edges go from a parent to a child. The edge kinds are: *intraprocedural* (control and data edges inside one procedure, including entry to formal-in, entry to formal-out, call node to actual-in and actual-out, and `ret` statement to formal-out); *call* edges from a call node at site $c$ to the entry of the callee; *parameter-in* edges from actual-in $k$ at $c$ to formal-in $k$ of the callee; *parameter-out* edges from the formal-out of the callee to the actual-out at $c$; and *summary* edges. Each procedure has exactly one formal-out node, for its return value. The criterion is a virtual node $\gamma$ in procedure $P$, with an intraprocedural edge from each start node of line L1.

**Words of paths.** Give each call or parameter-in edge at site $c$ the symbol $(_c$, each parameter-out edge at $c$ the symbol $)_c$, and every other edge no symbol. The word of a path is the sequence of its symbols. Match brackets with a stack, from left to right: a close $)_c$ is *matched* if the top of the stack is $(_c$, which it pops; otherwise it is *unmatched* (if the stack is empty) or *mismatched*. Opens left on the stack at the end are unmatched. A path without summary edges is *realizable* if no close is mismatched and no unmatched close comes after an unmatched open. It is *same-level* if every bracket is matched. The text between a matched pair is balanced, so a path segment from a matched open to its close is same-level inside, and an unmatched close never lies strictly between the two edges of a matched pair.

The slice over realizable paths is the set of nodes $n$ with a realizable path from $n$ to $\gamma$. In the paths below, an edge into an entry node is always a call edge and an edge into a formal-in node from outside the procedure is always a parameter-in edge; the only intraprocedural parent of a formal-in or formal-out is the entry node of its procedure, plus the `ret` statements for the formal-out.

## 1. Path edges

SUMMARY-EDGES keeps a set $PE$ of *path edges* $(v, w)$. Every $w$ it handles is a formal-out node.

**Lemma 1 (soundness).** If $(v, w) \in PE$, then $v$ and $w$ are in the same procedure, $w$ is its formal-out, and there is a same-level path from $v$ to $w$. If $(a, o)$ is a summary edge at site $c$ for argument $k$, there is a same-level path from $a$ to $o$ through formal-in $k$ and the formal-out of the callee.

*Proof.* By induction on the order in which pairs and summary edges are added. Line L12 adds $(w, w)$, the empty path. Line L18 adds $(x, w)$ when $(v, w) \in PE$ and $x \to v$ is intraprocedural (no symbol, same procedure) or a summary edge already added (same-level by induction); prefix the edge or path to the path from $v$. Line L17 adds the summary edge $(a, o)$ when $(f_k, w_Q) \in PE$ for formal-in $f_k$ of the callee $Q$; the path $a \to f_k \leadsto w_Q \to o$ has the word $(_c \, u \, )_c$ with $u$ balanced, so it is same-level. Line L17 then adds $(a, x)$ for $(o, x) \in PE$; prefix that path with $a \leadsto o$. $\square$

**Lemma 2 (completeness).** Let $v$ be a node that is not an entry node, in procedure $Q$ with formal-out $w$. If a same-level path without summary edges runs from $v$ to $w$, then $(v, w)$ is added to $PE$.

*Proof.* By induction on the length of the path $\pi$. If it is $0$, $v = w$ and line L12 adds it. Otherwise let $v \to v'$ be the first edge. It is not a close, since a close at the start is unmatched.

*Case 1: $v \to v'$ is intraprocedural.* Then $v'$ is not an entry node (entries have only call parents) and not a formal-in (its only intraprocedural parent is the entry, and $v$ is not one). The rest of $\pi$ is shorter and same-level, so $(v', w) \in PE$ by induction. When it is taken from the work list, line L18 reads the edge $v \to v'$ and adds $(v, w)$.

*Case 2: $v \to v'$ is a parameter-in edge at site $c$*, so $v = a_k$ is actual-in $k$ at $c$ and $v' = f_k$ is formal-in $k$ of the callee $R$. Its match is a close $)_c$, a parameter-out edge $w_R \to o_c$ into the actual-out at $c$. The part from $f_k$ to $w_R$ is same-level and shorter, so $(f_k, w_R) \in PE$, and when it is taken from the work list, lines L15 to L17 add the summary edge $(a_k, o_c)$. The part from $o_c$ to $w$ is same-level and shorter, so $(o_c, w) \in PE$. If $(o_c, w)$ is in $PE$ when the summary edge is added, line L17 adds $(a_k, w)$. If not, $(o_c, w)$ is added later and taken from the work list later still; line L18 then reads the summary edge into $o_c$ and adds $(a_k, w)$.

*Case 3: $v \to v'$ is a call edge at site $c$*, so $v$ is the call node. As in case 2 the match is the edge into the actual-out $o_c$, and $(o_c, w) \in PE$ by induction. The edge $v \to o_c$ is an intraprocedural control edge, so line L18 adds $(v, w)$ when $(o_c, w)$ is taken from the work list. $\square$

**Theorem 1 (summary edges).** SUMMARY-EDGES adds the summary edge $(a_k, o_c)$ at site $c$ if and only if a same-level path runs from formal-in $k$ of the callee of $c$ to its formal-out.

*Proof.* Only line L17 adds summary edges, and it does so when $(f_k, w_R) \in PE$, which by Lemma 1 gives the path. Conversely, such a path gives $(f_k, w_R) \in PE$ by Lemma 2, and when the pair is taken from the work list, line L16 visits every call site of $R$, including $c$. $\square$

**Termination and cost.** Every pair in $PE$ has as second node the formal-out of the procedure of its first node, so $|PE| \le N$, the number of nodes. Each pair enters the work list once. Taking $(v, w)$ costs the number of parents of $v$, or, for a formal-in, the number of call sites of its procedure times the number of pairs $(o, x)$ in $PE$ with first node $o$, which is at most one. Each summary edge is added once. The total is $O(N + E)$, where $E$ counts all edges including summary edges. With several formal-outs per procedure (global variables, reference parameters), the same count gives $O(g (N + E))$ for at most $g$ formal-outs per procedure.

## 2. The two passes

Let $S_1$ be the set after the first loop (lines L1 to L5) and $S$ the set returned (line L11). The first loop starts from the parents of $\gamma$ and follows every edge but parameter-out edges, backward; the second starts from $S_1$ and follows every edge but call and parameter-in edges. Both loops add each node at most once and read each of its parent edges once, so they stop after $O(N + E)$ steps.

**Lemma 3.** $n \in S_1$ if and only if a path from $n$ to $\gamma$ uses only intraprocedural, summary, call and parameter-in edges. $n \in S$ if and only if a path from $n$ to some node of $S_1$ uses only intraprocedural, summary and parameter-out edges.

*Proof.* This is backward reachability under the stated edge kinds, as in the PDG slice. $\square$

**Lemma 4.** Replace each summary edge of a path by the same-level path that Theorem 1 gives for it. The result has the same first and last nodes, and its word is the old word with balanced words put in.

**Theorem 2.** $S$ is exactly the set of nodes $n$ with a realizable path from $n$ to $\gamma$.

*Proof.* ($\subseteq$) Let $n \in S_1$. Lemma 3 gives a path to $\gamma$ with intraprocedural, summary, call and parameter-in edges; after Lemma 4 its word has opens and balanced inserts only, so no close is mismatched and no close is unmatched. It is realizable. Let $n \in S \setminus S_1$. Lemma 3 gives a path to some $m \in S_1$ with intraprocedural, summary and parameter-out edges; after Lemma 4 its word has closes and balanced inserts only, so its opens are all matched. Join it to the path from $m$ to $\gamma$. Every bracket of the second part that was matched or unmatched in that part stays so, since the first part leaves the stack empty; the closes of the first part are matched or unmatched and come before every unmatched open. The joined path is realizable.

($\supseteq$) Let $\pi$ be a realizable path from $n$ to $\gamma$ without summary edges. If $\pi$ has an unmatched close, let $e$ be the last one, $\pi_1$ the part up to and including $e$, and $\pi_2$ the rest; otherwise $\pi_1$ is empty and $\pi_2 = \pi$. No matched pair has its open in $\pi_1$ and its close in $\pi_2$, since $e$ cannot lie inside a matched pair. So in $\pi_2$ the unmatched brackets are opens, and in $\pi_1$ they are closes.

Rewrite each maximal matched pair in $\pi_2$. The open is at some site $c$, and the matching close is the parameter-out edge $w_R \to o_c$ of the same site. If the open is a parameter-in edge $a_k \to f_k$, the part from $f_k$ to $w_R$ is same-level, so Theorem 1 gives the summary edge $a_k \to o_c$; put it in place of the pair and what lies between. If the open is a call edge from the call node $c$, put the control edge $c \to o_c$ in its place. The first node of $\pi_2$ is the first node of the new path, because no pair of $\pi_2$ starts before it. The new path uses only intraprocedural, summary, call and parameter-in edges, so by Lemma 3 its first node $m$ is in $S_1$. Rewrite $\pi_1$ the same way: the new path from $n$ to $m$ uses only intraprocedural, summary and parameter-out edges, so $n \in S$ by Lemma 3. If $\pi_1$ is empty, $n = m \in S_1 \subseteq S$. $\square$

**Remark (what the tests check).** For a system without recursion, clone each procedure once per calling context, the string of call sites from `main`. A call or parameter-in edge goes from a callee copy to the caller copy one site shorter, and a parameter-out edge goes from the caller copy into the copy one site longer. Every realizable path of the SDG that ends at $\gamma$ lifts to a path of this graph that ends at a copy of $\gamma$: walk it backward, push the site at each parameter-out edge, and pop at each call or parameter-in edge; an unmatched open walked backward needs a copy of $\gamma$ whose context ends with that site, and such a copy exists because every procedure is called from `main`. Every path of the expanded graph projects to a realizable path. So by Theorem 2 the slice equals backward reachability from all copies of $\gamma$ in the expanded graph, which the tests compute directly.

The slice is exact for realizable paths of the graph, not for runs. A realizable path need not be feasible, as in the intraprocedural case on the [program slicing](/program-slicing/) page, so the slice is not minimal in general.
