---
title: Correctness of Sreedhar's out-of-SSA translation
proves: [correctness]
status: full
---

We prove that the translation in `impl/python/sreedhar_cssa_translation.py` is correct. There are two parts. First, renaming the phi congruence classes of a program in conventional SSA form keeps its meaning. Second, Methods I and III add copies that keep the meaning and make the program conventional. Together they show that `sreedhar_out_of_ssa` returns a program without phi-functions that follows the same blocks and gives the same result as its input on every run.

## Setting

The input $P$ is in strict SSA form. Each name has one definition: a parameter is defined at the top of the entry $r$, a phi target at the *phi point* of its block (just after all phi-functions), and any other name at its instruction. The phi-functions of a block $b$ have one operand for each predecessor. On the edge $(p, b)$, all of them read their operand for $p$ at the *end* of $p$, and then all of them write their targets at the phi point of $b$.

A name $x$ is *live* at a point $q$ if some path from $q$ reaches a use of $x$ without passing the definition of $x$. The operand of a phi-function for the predecessor $p$ is used at the end of $p$. Two names $u \ne w$ *interfere* if $u$ is live just after the definition of $w$, or $w$ just after the definition of $u$. Note that a dead definition still interferes with the names live at it, because it writes its variable.

The *phi congruence classes* are the classes of the smallest equivalence relation in which each phi target is related to each of its name operands. $P$ is *conventional* if no two names in one class interfere and every phi operand is a name.

**Fact 0.** If $x$ is live at a point $q$ of a run of a strict program, then the definition of $x$ ran before $q$, and $x$ has been live at every point since its last run.

*Proof.* Take a path from $q$ to a use of $x$ that avoids the definition. Joined to the run up to $q$, it is a path from $r$ to the use. The definition dominates the use, so it lies on the run up to $q$. From its last run to $q$, the run followed by the same path reaches the use without the definition, so $x$ is live at each point between. $\square$

## Part 1: renaming a conventional program

`rename_classes` maps every name $x$ to a representative $\mathrm{rep}(x)$ of its class: the smallest parameter in the class if there is one, otherwise the smallest name. Names in no class keep their names. It deletes the phi-functions and the copies that become `y = y`. Call the result $Q$.

**Theorem 1.** If $P$ is conventional, then on every input $Q$ follows the same sequence of blocks as $P$, and it returns the same value, traps at the same instruction, or runs forever when $P$ does.

*Proof.* We show by induction over the steps of the two runs that they are in the same block and that this invariant holds:

(I) for every name $x$ live at the current point of $P$, the variable $\mathrm{rep}(x)$ in $Q$ holds the value of $x$ in $P$.

*Start.* Only parameters are live at the top of $r$, by Fact 0. Let $x$ be a live parameter. Every other parameter $y$ is defined at the same point, and $x$ is live just after it, so $x$ and $y$ interfere. As $P$ is conventional, $y$ is not in the class of $x$, so $\mathrm{rep}(x) = x$. $Q$ binds $x$ to the same argument.

*An instruction* $d = f(a, b)$. Its operands are live just before it, so by (I) $Q$ reads the same values, and computes the same value or traps in the same way. $Q$ writes $\mathrm{rep}(d)$. Let $x \ne d$ be live just after the instruction. If $\mathrm{rep}(x) = \mathrm{rep}(d)$, then $x$ and $d$ are in one class, and $x$ is live just after the definition of $d$, so they interfere; that is impossible. So the write clobbers no live name, and (I) holds after the step. A copy $d = s$ with $\mathrm{rep}(d) = \mathrm{rep}(s)$ is deleted in $Q$; then $\mathrm{rep}(d)$ already holds the value of $s$, which is the value of $d$.

*A terminator.* Its operand is live just before it, so by (I) both runs take the same branch or return the same value.

*An edge* $(p, b)$. Let $x_1, \ldots, x_m$ be the phi targets of $b$, and $a_i$ the operand of $x_i$ for $p$. In $P$, each $x_i$ gets the value that $a_i$ has at the end of $p$. $Q$ does nothing on the edge. Let $y$ be live at the phi point of $b$. If $y$ is a target $x_i$, then $\mathrm{rep}(x_i) = \mathrm{rep}(a_i)$, as they are in one class, and $a_i$ is live at the end of $p$, so by (I) that variable holds the right value. If $y$ is not a target, then $y$ is live on entry to $b$ and so at the end of $p$, its value does not change on the edge, and by (I) $\mathrm{rep}(y)$ holds it already. A dead target needs no value. As $Q$ writes no variable on the edge, (I) holds at the phi point.

So the invariant holds at every step, and the runs agree. $\square$

## Part 2: the copies

`to_cssa` handles the phi-functions one at a time. For the $k$-th phi-function of block $L_0$, with target $x_0$ and operand $x_i$ from predecessor $L_i$, a copy on the target replaces $x_0$ by a new name $x_0'$ in the phi-function and puts `x0 = x0'` after the phi-functions of $L_0$ and after the copies already there. A copy on the operand $x_i$ puts `xi' = xi` (or `xi' = k` for a constant) at the end of $L_i$, before its terminator, and makes $x_i'$ the operand. Then the classes of all resources of the phi-function are merged (line L16).

**Lemma 2 (meaning).** Each copy keeps the program in strict SSA form and keeps its meaning.

*Proof.* The new name $x_i'$ is defined at the end of $L_i$ and read there by the phi-function, with no definition of $x_i$ in between, so the phi-function gets the same value. The new name $x_0'$ gets the value $x_0$ used to get, and `x0 = x0'` passes it on before any instruction of $L_0$ that came from $P$. Every use of $x_0$ was dominated by the phi point of $L_0$, so it comes after this copy or in a block dominated by $L_0$; the program stays strict. Each new name has one definition. $\square$

**Lemma 3 (old names).** Adding a copy never makes two old names interfere that did not interfere before.

*Proof.* The copy `xi' = xi` at the end of $L_i$ moves the use of $x_i$ from the end of $L_i$ to just before the terminator. Live ranges of old names can only shrink, and no old name gets a new definition. The copy `x0 = x0'` moves the definition of $x_0$ from the phi point to a later point of $L_0$, with only copies to new names or to other targets in between. The old names live just after the new definition of $x_0$ are the old names that were live just after the phi point, other than $x_0$. So $x_0$ interferes with no new old name, and its own live range only shrinks. $\square$

**Lemma 4 (new names).** At the moment it is added:

- the new name $x_i'$ of an operand from $L_i$ interferes exactly with the names live just before the terminator of $L_i$, that is $\mathrm{LiveOut}(L_i)$ plus the operand of the terminator;
- the new name $x_0'$ of a target interferes only with names that are live just after the phi-functions of $L_0$, are phi targets of $L_0$, or are targets of the copies already placed after them.

Later, a new name can interfere only with a name defined later between its definition and its last use, and that is again a copy at the end of $L_i$ or after the phi-functions of $L_0$. Lemma 4 for that later copy covers the pair.

*Proof.* $x_i'$ is live from its definition to the end of $L_i$, where only the terminator follows. $x_0'$ is live from the phi point to its copy; the definitions in between are the other phi targets and the earlier copies. $\square$

These sets are exactly the sets `near[i]` in `_choose`: $\mathrm{LIVE}(i)$ in the pseudocode.

**Invariant J.** After each phi-function is handled, no two names in one class of the union-find interfere.

**Theorem 5.** Invariant J holds for Method I and for Method III.

*Proof.* Before the first phi-function every class is a single name. Assume J before the $k$-th phi-function. By Lemma 3 the copies add no interference between old names, so the classes not touched by the merge stay free of interference; the new names are only in the merged class $M$. It remains to show that $M$ has no interfering pair.

*Method I.* Every resource is copied, so $M = \{x_0', x_1', \ldots, x_n'\}$. Two operand names $x_i'$ and $x_j'$ live only at the ends of two different predecessors. $x_0'$ dies at the top of $L_0$ and every $x_i'$ is born at the end of a block, after that point when $L_i = L_0$. So no two of them are live at the same point, and none interferes with another.

*Method III.* Let $C$ be the set of copied resources when line L14 ends. $M$ is the union of the classes of the resources not in $C$ and the new names of the resources in $C$. Take two names in $M$.

1. Both in the class of one resource $j \notin C$: no interference, by J and Lemma 3.
2. In the classes of two resources $j, l \notin C$ that are different: if the classes interfered before the copies, line L6 saw the pair. Then lines L8 and L9 copy at least one of them, or the pair is deferred at line L10. For a deferred pair, line L12 copies the first of the two in its order if neither is copied yet. Either way $j$ or $l$ is in $C$, which is false. So the classes did not interfere before, and by Lemma 3 they do not interfere now.
3. The new name of $i \in C$ and a name $w$ in the class of $j \notin C$: by Lemma 4, they interfere only if $w \in \mathrm{LIVE}(i)$. But then lines L13 and L14 put $j$ into $C$, which is false.
4. The new names of $i, i' \in C$: they do not interfere, as for Method I.

So $M$ has no interfering pair, and J holds after the merge. $\square$

Each phi-function is handled once, and later steps change only their own phi-function. So at the end the classes of the union-find hold the phi congruence classes of the result, and every constant operand has been replaced by a copy. By Theorem 5, the result of `to_cssa` is conventional.

## The whole translation

**Theorem 6.** For a strict SSA program $P$ and either method, `sreedhar_out_of_ssa(P)` returns a program with no phi-functions that follows the same blocks as $P$ on every input and returns the same value, traps at the same point, or runs forever when $P$ does.

*Proof.* By Lemma 2 the program after `to_cssa` has the meaning of $P$ and is strict. By Theorem 5 it is conventional. By Theorem 1, `rename_classes` keeps its meaning. $\square$

**Corollary 7.** If $P$ is conventional and has no constant phi operands, Method III adds no copies.

*Proof.* Each class built during the run is part of a phi congruence class of $P$, by induction, so no two classes that line L6 compares ever interfere. No resource is copied at lines L4 to L12, so $C$ is empty and line L14 adds nothing. $\square$

## Counting

Method I adds one copy per phi operand and one per phi-function. Method III copies a subset of the same resources, so it never adds more. The tests compare both counts on random programs, and check the result with a brute-force interference test that follows paths.

## Running time

The implementation computes liveness and the interference graph again for each phi-function. Liveness by round-robin iteration takes $O(n \cdot (I + V))$ set operations per pass for $n$ blocks, $I$ instructions and $V$ names, and the interference graph has $O(V^2)$ edges. Sreedhar et al. update both in place as copies are added, which is what makes the method practical on large procedures.
