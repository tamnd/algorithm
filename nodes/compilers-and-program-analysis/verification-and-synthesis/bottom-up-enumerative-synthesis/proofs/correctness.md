---
title: Bottom-up search with observational equivalence returns a smallest program
proves: [correctness]
status: full
---

**Setting.** A grammar has a finite set of sorts and a finite set of rules. A rule $r$ of arity $m \ge 0$ builds a program of sort $T$ from programs $P_1, \ldots, P_m$ of fixed sorts $T_1, \ldots, T_m$. The size of $r(P_1, \ldots, P_m)$ is $1 + \sum_i |P_i|$. The examples have inputs $i_1, \ldots, i_k$ and wanted outputs $o_1, \ldots, o_k$. The vector of a program $P$ is $\mathrm{vec}(P) = ([\![P]\!](i_1), \ldots, [\![P]\!](i_k))$. The semantics is *compositional*: for each rule $r$ there is a function $F_r$ with $\mathrm{vec}(r(P_1, \ldots, P_m)) = F_r(\mathrm{vec}(P_1), \ldots, \mathrm{vec}(P_m))$. This holds when each operator is a function of the values of its arguments on the same input, as for $+$, $-$, $\times$, $\le$ and ite. Line numbers refer to the pseudocode on the page.

At size $s$, line L3 builds $r(Q_1, \ldots, Q_m)$ for every rule $r$ and every tuple of kept programs of the right sorts with $1 + \sum_i |Q_i| = s$. Line L4 computes its vector by $F_r$ from the stored vectors of the parts. Line L5 drops it if a kept program of the same sort has the same vector. Otherwise line L6 keeps it and line L7 returns it if its sort is the start sort and its vector is $(o_1, \ldots, o_k)$. The parts of a program of size $s$ have sizes below $s$, so they were kept at earlier rounds.

## Lemma: every vector is kept at its least size

**Claim.** Assume that the search has finished round $s$ without a return. Then for every program $P$ of sort $T$ with $|P| \le s$ there is a kept program $Q$ of sort $T$ with $|Q| \le |P|$ and $\mathrm{vec}(Q) = \mathrm{vec}(P)$.

**Proof.** By induction on $|P|$. Let $P = r(P_1, \ldots, P_m)$. Each $P_i$ is smaller than $P$, so by induction there is a kept $Q_i$ of sort $T_i$ with $|Q_i| \le |P_i|$ and $\mathrm{vec}(Q_i) = \mathrm{vec}(P_i)$. (For a leaf, $m = 0$ and there is nothing to do.) Let $R = r(Q_1, \ldots, Q_m)$. Its size is $s' = 1 + \sum_i |Q_i| \le |P|$, so round $s'$ has finished, and line L3 built $R$ in that round from the kept $Q_i$. By compositionality, $\mathrm{vec}(R) = F_r(\mathrm{vec}(Q_1), \ldots) = F_r(\mathrm{vec}(P_1), \ldots) = \mathrm{vec}(P)$. If line L6 kept $R$, take $Q = R$. If line L5 dropped it, a program $Q$ of sort $T$ with the same vector was kept before, in round $s'$ or earlier, so $|Q| \le s' \le |P|$. $\square$

## Theorem

SYNTHESIZE(examples, maxsize) returns a program of the start sort that meets all examples and has the least size among all such programs, if one of size at most maxsize exists. It returns "none" exactly when no such program exists.

**Proof.** *Soundness.* Line L7 returns $P$ only if $\mathrm{vec}(P) = (o_1, \ldots, o_k)$, and the vector computed at line L4 is the true vector by compositionality, so $P$ meets every example.

*Least size.* Say line L7 returns $P$ in round $s$, and some program $R$ of the start sort with $|R| < s$ meets the examples. Round $|R|$ finished without a return. By the lemma there is a kept $Q$ of the start sort with $|Q| \le |R|$ and $\mathrm{vec}(Q) = (o_1, \ldots, o_k)$. When line L6 kept $Q$, line L7 returned it, in a round before $s$. This is a contradiction.

*Completeness.* Say a program $R$ with $|R| \le$ maxsize meets the examples, and the search returns nothing in rounds $1, \ldots, |R|$. The lemma after round $|R|$ gives a kept $Q$ with the wanted vector, and line L7 returned $Q$ when it was kept. This is a contradiction. So a return happens, and by the first two parts it is a smallest correct program. If no correct program of size at most maxsize exists, line L7 never fires and line L8 returns "none". $\square$

## Remarks

**No pruning.** Without line L5 the search keeps every program, so it builds all programs in order of size, and the first hit is again of least size. With and without pruning the answer has the same size, but it can be a different program of that size.

**Other cost models.** The proof uses only two facts about size: the cost of $r(P_1, \ldots, P_m)$ is larger than the cost of each $P_i$, and it does not grow when a part is replaced by a part of no larger cost. So the theorem holds for every cost of the form $w(r) + \sum_i c(P_i)$ with positive integer rule weights $w(r)$, with rounds over the cost values instead of the sizes.

**Where it fails.** If the semantics is not compositional, two programs with the same vector can behave differently inside a larger program, and pruning can drop the only part of the right answer. This happens with side effects, with a state that the vector does not record, and with recursion through the program being built, where the value of a call depends on the whole program and not on the vector of the part.
