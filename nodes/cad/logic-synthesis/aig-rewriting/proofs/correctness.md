---
title: Rewriting keeps the functions, makes no cycle and lowers the size by at least the gain
proves: [correctness]
status: full
---

We use the notation of the and-inverter graph page. $f_\ell$ is the function of a literal $\ell$ over the primary inputs. Before each node $v$ is handled, the graph is *clean*: every AND node is reached from an output, no two AND nodes have the same fanin pair, every node has fanins $2 \le a < b$ with $a \ne b \oplus 1$, the table maps each fanin pair to its node, and the fanout counts are exact. The first sweep at the start of the pass and line L12 after each change make the graph clean, and the dry runs of lines L3 to L8 do not change it.

Fix a node $v$, a cut $C$ of $v$ and the cone $Z$ of $v$ over $C$: the nodes on paths from $C$ to $v$, without $C$, so $v \in Z$. Let $M \subseteq Z$ be the maximum fanout-free cone, the nodes whose every fanout lies in $M$, together with $v$. Each library structure $S$ is a list of AND gates over the inputs $y_1, y_2, y_3$ and the constants.

**Lemma 1 (the structure has the function of v).** The literal $r$ built at line L10 satisfies $f_r = f_v$.

*Proof.* Let $t$ be the table of $v$ over the leaves $u_1, \ldots, u_k$ of $C$, so $f_v = t(f_{u_1}, \ldots, f_{u_k})$, since every path from an input to $v$ meets $C$. Line L4 gives $c$, a permutation $\pi$, a negation mask $\nu$ and an output phase $\omega$ with $t(x) = \omega \oplus c(y)$ where $y_j = x_{\pi(j)} \oplus \nu_j$. The structure $S$ computes $c$, which the test file checks on all 8 points. Line L10 feeds $y_j$ with the literal of $u_{\pi(j)}$, complemented if $\nu_j = 1$, and the constant 0 if $\pi(j) > k$, in which case $t$ and so $c$ do not depend on $y_j$. It complements the root if $\omega = 1$. The AND of the AIG page returns literals with the right functions, so $f_r = \omega \oplus c(\ldots) = t(f_{u_1}, \ldots, f_{u_k}) = f_v$. $\square$

**Lemma 2 (the replacement keeps the functions).** After line L11, every output has the same function as before.

*Proof.* Line L11 handles pairs $(o, r)$ with $f_r = f_o$, starting with $(v, r)$ by Lemma 1. It replaces each use of $o$, in an output or as a fanin of a node $p$, by $r$ with the same phase, which keeps the function of that output and of $p$. Then the fanins of $p$ are hashed again. If a trivial rule applies, $p$ has the function of the literal $s$ that the rule gives, and if the table holds a node $q$ with the same fanins, $f_p = f_q$. In both cases the pair $(p, s)$ or $(p, q)$ again has equal functions. A target that was itself replaced earlier is followed to its replacement, which has the same function. So every step keeps all functions, and the pass ends because each step deletes one node $o$ and only nodes that exist at the start of line L11 or are made at line L10 are ever handled. $\square$

**Lemma 3 (no cycle).** If the gain of the chosen structure is positive, then $r$ does not depend on $v$, and line L11 makes no cycle.

*Proof.* Call a value of the dry run of line L7 *real* if it is a literal of the graph, and *new* otherwise. Real values arise from the leaves, the constants, the trivial rules and table lookups. A real value that is not a leaf or a constant equals the result of a lookup at some gate of $S$, because a trivial rule returns one of its two inputs or a constant. We claim that if some lookup returns a node of $Z$, then the lookups of the dry run return every node of the cone of that node over $C$. Let a lookup return $w \in Z$ at gate $i$. The fanins of $w$ are the two values of gate $i$, so they are real, and each is either a leaf of $C$ or a node of $Z$, since every node on a path from $C$ to $w$ is in $Z$. A fanin in $Z$ is not a leaf or a constant, so it is the result of a lookup at an earlier gate, and the claim follows by induction on the gates.

A node of the graph depends on $v$ only if it is $v$ or lies above $v$. The leaves do not depend on $v$. Suppose the dry run returns $v$ at some lookup. Then by the claim it returns every node of the cone of $v$, which is $Z \supseteq M$, so it counts every node of $M$ as added and the gain $|M| - a$ is at most 0. So when the gain is positive, no lookup returns $v$. Then by induction on the gates, no real value depends on $v$: a lookup with fanins that do not depend on $v$ returns a node that is not $v$ and is not above $v$. Line L10 runs the same steps on the same table, with new nodes in place of the new values, so $r$ does not depend on $v$. Moving the fanouts of $v$ to $r$ therefore makes no cycle. A later step of line L11 replaces $p$ by a fanin of $p$, by a constant, or by a node $q$ with the same fanins as $p$, and none of these depends on $p$. $\square$

**Lemma 4 (the size).** Let $s$ be the number of AND nodes before the change and $s'$ the number after line L12. Then $s' \le s - (|M| - a)$.

*Proof.* After line L11, $v$ has no uses. Every node of $M$ other than $v$ has all its fanouts in $M$, so after the change it is reached from an output only through the nodes of $S$. By the argument of Lemma 3, a node of $M$ reached through $S$ is the result of a lookup at some gate of $S$ in the dry run, and the dry run counted it as added. So the reached nodes after line L12 are among the nodes outside $M$ that were there before, the nodes of $M$ counted by the dry run, and the nodes created at line L10. Line L10 makes at most one node for each gate of $S$ that the dry run counted as new, since a gate with only real values does the same lookup in both runs, and a gate counted as new adds at most one node. The merges of line L11 add no node. So $s' \le (s - |M|) + a$. $\square$

**Theorem.** One pass of REWRITE returns an AIG with the same output functions and no cycle, and each change lowers the number of AND nodes by at least its gain, which is positive. So the size never grows.

*Proof.* Lemmas 2 and 3 for each change, and Lemma 4 with the gain test of line L9. $\blacksquare$
