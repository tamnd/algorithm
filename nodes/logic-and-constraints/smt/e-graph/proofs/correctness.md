---
title: The e-graph keeps the congruence closure of its merges
proves: [correctness, termination]
status: full
---

We use the notation of the page. An e-node $n$ of class $y$ is stored in $\mathit{nodes}[y]$ when it is made, and it keeps its identity when its class is joined with another. Its canonical form CANONICAL$(n)$ changes over time, because FIND changes. Let $T$ be the set of terms added so far, and let $\mathrm{CC}$ be the congruence closure on $T$ of the pairs passed to MERGE by the user. Each class represents a set of terms, and we identify a term of $T$ with the class that ADD returned for it.

**Fact 0.** A class id that is not canonical never becomes canonical again, because only line L10 changes $\mathit{uf}$, and it sets $\mathit{uf}[x]$ of a canonical $x$ to another id. So if two e-nodes have the same canonical form at some time, they have the same canonical form at all later times: their symbols are equal, and the ids of their arguments are in the same classes, which are never split.

## The invariants

- (E1) For each e-node $n$ of class $y$ and each argument $c_i$ of $n$, the entry $(n, y)$ is in $\mathit{parents}[\mathrm{FIND}(c_i)]$.
- (E2) For each e-node $n$ of class $y$, either $\mathrm{CANONICAL}(n)$ is a key of $\mathit{memo}$ with $\mathrm{FIND}(\mathit{memo}[\mathrm{CANONICAL}(n)]) = \mathrm{FIND}(y)$, or some entry $(n, y')$ with $\mathrm{FIND}(y') = \mathrm{FIND}(y)$ is on $\mathit{pending}$.
- (E3) If two terms of $T$ are in the same class, they are equal in $\mathrm{CC}$.

All three hold for the empty e-graph.

**ADD.** If line L2 finds the canonical form $m$ of the new e-node in $\mathit{memo}$, nothing changes. Otherwise line L3 makes a class $x$ that holds only the new e-node $n$. Line L4 adds $(n, x)$ to the parent list of each argument class. Line L1 made the arguments canonical, so this gives (E1) for $n$. Line L5 gives (E2) for $n$. Line L5 can overwrite no key, because $m$ was not a key. Other e-nodes keep their entries, so (E1) and (E2) hold. For (E3): the new class has one term if L3 runs. If L2 returns a class $x'$, the new term $t = f(t_1, \ldots, t_k)$ joins the class of a term $t' = f(t'_1, \ldots, t'_k)$ whose e-node has the same canonical form, so $t_i$ and $t'_i$ are in the same classes and are equal in $\mathrm{CC}$ by (E3), and then $t$ and $t'$ are equal in $\mathrm{CC}$ by congruence. A term in a class that $x'$ was joined with earlier is equal to $t'$ by (E3), so (E3) holds.

**MERGE.** A call either does nothing (line L8) or links the canonical class $x$ below $y$. Only the e-nodes with an argument whose FIND was $x$ change their canonical form. By (E1), each such e-node $n$ of class $z$ has its entry $(n, z)$ in $\mathit{parents}[x]$, and line L12 puts all of them on $\mathit{pending}$. So (E2) holds for them. For each other e-node, its canonical form is the same, and FIND of its class and of the table value is the same class or both moved to $y$, so (E2) holds. Line L13 moves the list of $x$ to $y$, and FIND of each id in class $x$ is now $y$, so (E1) holds. For (E3): a user merge adds a pair of $\mathrm{CC}$ by definition. A merge from line L18 joins the class of a pending e-node $n$ with the class of an e-node $n'$ whose canonical form is the key $m = \mathrm{CANONICAL}(n)$. The argument below shows that $n'$ exists, and then $n$ and $n'$ have the same symbol and arguments in the same classes, so the terms they stand for are equal in $\mathrm{CC}$ by (E3) and congruence.

**The table entry of a key.** We also keep (E4): for each key $m$ of $\mathit{memo}$ that is in canonical form now, the class $\mathrm{FIND}(\mathit{memo}[m])$ has an e-node whose canonical form is $m$. Line L5 and line L19 write $\mathit{memo}[m]$ only with the class of an e-node whose canonical form is $m$ at that time. By Fact 0, that e-node still has the canonical form $m$ later, as long as $m$ is canonical, and classes are never split. So (E4) holds, and the e-node $n'$ above exists.

**REBUILD.** One pass takes an entry $(n, y)$ from $\mathit{pending}$. Line L17 computes $m = \mathrm{CANONICAL}(n)$. If $m$ is a key whose class is not the class of $y$, line L18 joins them, which keeps (E1) to (E3) as shown for MERGE. Line L19 then sets $\mathit{memo}[m]$ to the class of $y$. Before the write, either $m$ was not a key, or its class is now the class of $y$, so no other e-node loses its table entry of (E2). After the write, (E2) holds for $n$ without the removed entry. So (E1) to (E4) hold after each pass.

## Termination

Each call of MERGE that does not stop at line L8 lowers the number of classes by one, so there are fewer such calls than classes. Each of them adds a finite number of entries to $\mathit{pending}$. Each pass of REBUILD removes one entry. So the loop of line L15 stops after a finite number of passes. $\square$

## The clean state

**Theorem.** When $\mathit{pending}$ is empty, two terms of $T$ are in the same class if and only if they are equal in $\mathrm{CC}$. A term $t$, in $T$ or not, is represented by the class LOOKUP$(t)$, and LOOKUP$(t)$ is nil exactly when no class represents $t$.

*Proof.* With $\mathit{pending}$ empty, (E2) says that each e-node $n$ has its canonical form in $\mathit{memo}$, with the class of $n$. So two e-nodes with the same canonical form are in the same class. The relation "same class" on $T$ is an equivalence relation. It contains the user merges, by line L10. It is a congruence: if $f(s_1, \ldots, s_k)$ and $f(t_1, \ldots, t_k)$ are in $T$ and each $s_i$ is in the class of $t_i$, the e-nodes of the two terms have the same canonical form, so they are in the same class. So it contains $\mathrm{CC}$, which is the least such congruence. By (E3) it is contained in $\mathrm{CC}$, so the two are equal.

For LOOKUP, use induction on $t = f(t_1, \ldots, t_k)$, with a constant as the case $k = 0$. Suppose the class $x$ represents $t$, by an e-node $f(c_1, \ldots, c_k)$ in $x$ with $t_i$ represented by $c_i$. By the induction hypothesis, LOOKUP$(t_i)$ returns $\mathrm{FIND}(c_i)$. So line L22 builds the canonical form of that e-node, which is a key of $\mathit{memo}$ with the class $x$ by (E2), and line L23 returns $x$. Each term is represented by at most one class, because two e-nodes with the same canonical form are in one class. If no class represents $t$, then either some $t_i$ is not represented, and LOOKUP$(t_i)$ is nil by the induction hypothesis, or the canonical e-node of line L22 is in no class. In the second case it is not a key of $\mathit{memo}$, because by (E4) a canonical key leads to a class with an e-node of that form. So LOOKUP returns nil. $\blacksquare$

## Extraction

Let the cost of each e-node be positive, and let $\mathrm{best}(x)$ be the least cost of a term represented by $x$. A term of cost $\mathrm{best}(x)$ exists, because the class has a term from its first ADD, and costs are positive integers. Take a best term and suppose that a class $z$ appears twice on a path from its root, at a subterm $u$ and at a proper subterm $u'$ of $u$. Replacing $u$ by $u'$ gives a term that the same class represents (the e-node of each ancestor stays the same), with a smaller cost. This is a contradiction, so a best term has depth at most $c$, the number of classes. After round $r$ of the loop, each class whose best term has depth at most $r$ has its best cost, by induction on $r$. So $c$ rounds are enough, and each value the loop stores is the cost of a term that the class represents. $\blacksquare$
