---
title: Operator strength reduction keeps the outcome of every run
proves: [correctness]
status: full
---

**Setting.** $P$ is a program of the toy IR in strict SSA form, as the implementation checks: every name has one definition, phi-functions stand at the tops of blocks, every block is reachable, the entry block has no predecessor, no name is address-taken, and every use is dominated by its definition. For a phi operand from a predecessor $p$, the definition must dominate $p$. Integers are unbounded. We also assume that pointers never meet arithmetic: no name that an operation reads, and no name that flows into such a name through copies and phi-functions, ever holds a pointer. $P'$ is the program that `osr` returns.

**Claim.** For every input, the run of $P'$ visits the same blocks in the same order as the run of $P$, and it ends with the same return value or the same trap, or it runs forever exactly when the run of $P$ does.

We write $P_1$ for the program just before the deletion of line L7. It is $P$ with three changes: new instructions inserted by lines L21 and L28, each candidate $x = iv \mathbin{op} rc$ replaced by a copy $x = r$ at line L14, and some comparisons rewritten at line L6. We first show that $P_1$ behaves like $P$, then that the deletion keeps the behavior.

**Times and current values.** A run is a sequence of steps. The phi-functions at the top of a block form one step: they read all their operands at the end of the predecessor, then assign. Every other instruction is one step. The *current value* of a name at a step is the value that its most recent earlier execution assigned. A *point* is a place where a name is read: an instruction, a terminator, or the end of a predecessor block for a phi operand.

## Dominance in runs

**Lemma 1.** Let $D$ and $B$ be blocks with $D$ strictly dominating $B$, and let $B$ dominate a block $Q$. In a run, if $D$ is visited and $Q$ is visited later, then $B$ is visited after that visit of $D$ and no later than that visit of $Q$.

*Proof.* Every path from the entry to $D$ that passes $B$ passes $D$ before its first $B$, because $D$ dominates $B$. So the part of such a path up to its first $D$ does not contain $B$. Join this part to the run from the visit of $D$ to the visit of $Q$. If that part of the run did not visit $B$, the joined path would go from the entry to $Q$ without $B$, which is not possible. $\square$

Say that an instruction $I$ in block $B$ *comes before* a point $q$ in block $Q$ if $B$ strictly dominates $Q$, or if $B = Q$ and $I$ stands before $q$ in the block. The end of $B$ counts as a point after every instruction of $B$.

**Lemma 2 (freshness).** Let $I$ come before a point $q$, and let $J$ be an instruction that comes before $I$. In a run, if $J$ executes and the run later reaches $q$, then $I$ executes in between.

*Proof.* If $J$ and $I$ are in the same block, take the visit of that block in which $J$ executes. If $q$ is in the same visit, $I$ stands between $J$ and $q$. Otherwise the run leaves the visit through its terminator, so every instruction after $J$ in the block executes, $I$ included. If $J$ is in a block $D$ that strictly dominates the block $B$ of $I$, Lemma 1 gives a visit of $B$ after $J$ and no later than the visit of $q$. If that visit is the visit of $q$, $I$ stands before $q$ in it. Otherwise the run leaves it, so $I$ executes. $\square$

The usual consequence of strict SSA form follows from Lemma 2 with $J$ the first step of the run: every name is defined before it is read. The same holds for $P_1$ once we show it is in strict SSA form.

## Where the new instructions stand

Write $h$ for the header of an induction variable and $\mathrm{def}(y)$ for the block that defines $y$. A region constant $rc$ for $h$ is an integer, a parameter, or a name with $\mathrm{def}(rc)$ strictly dominating $h$. Line L9 accepts a component only if $h$ dominates all its members. A name that line L14 marks is defined where the candidate was, and the candidate reads an induction variable, so $h$ dominates its block too. The same holds for the names of line L21, which stand next to the definition of an induction variable.

**Lemma 3.** $P_1$ is in strict SSA form, and each new instruction comes before every point that reads its name.

*Proof.* *Names of line L28.* $r = o_1 \mathbin{op} o_2$ is appended to the block $d$ of the deeper of the two definitions. Both definitions dominate the point where Apply is called, so they lie on one chain of the dominator tree, and $d$ is well defined. The parameters count as defined before the entry, so $d$ is the entry if both operands are parameters or integers. Apply is called from three places.

1. For a phi operand from a predecessor $p$. The operand $o$ is defined in a block that dominates $p$. The region constant is defined in a block that strictly dominates $h$. If $p$ is not dominated by $h$, the phi is at $h$ itself, because every predecessor of a block other than $h$ that $h$ dominates is also dominated by $h$. A path from the entry to $p$ that avoids the definition of the region constant continues to $h$, so the definition dominates $p$. If $h$ dominates $p$, the definition dominates $p$ too, because it strictly dominates $h$. So $d$ dominates $p$, and the read at the end of $p$ comes after $r$.
2. For an operand of a copied operation, or for the new side of a comparison at line L6. Both operands are region constants for $h$, so $d$ strictly dominates $h$, and the reading point is in a block that $h$ dominates.
3. A lookup in the table at line L23 returns a name made in one of these two ways, and the new reading point again falls in one of the two cases.

*Names of line L21.* The copy $r$ of the definition of $iv$ is inserted right after it, or among the phi-functions right after it. Each operand of the copy is one of three things. It can be the result of Reduce for an operand $o$ of the definition, which stands right after the definition of $o$ and so comes before it. It can be a name of line L28, covered above. Or it can be an operand of the definition of $iv$ that is kept as it is, which strict SSA form of $P$ already covers. Every point that reads $r$ reads it instead of $iv$ or next to $iv$, so it comes after the definition of $iv$, and $r$ stands right after that definition.

*The copies of line L14* read $r$ at the place of the candidate, which reads $iv$. If the candidate is in the block of $iv$, it stands after $iv$ and so after $r$. $\square$

## The values of the new names

Every name made at lines L16 and L27 has a *meaning*. For a key $(op, o_1, o_2)$ in the table, the meaning of its name $r$ is $o_1 \mathbin{op} o_2$. The integers and operands that Apply returns at line L26 and in the simplifications $x \cdot 0 = 0$, $x \cdot 1 = x$, $x + 0 = x$ and $x - 0 = x$ satisfy the same identity on the spot.

**Lemma 4.** In every run of $P_1$, at every step that reads a new name $r$ with meaning $o_1 \mathbin{op} o_2$, the current value of $r$ equals the current value of $o_1$ combined by $op$ with the current value of $o_2$.

*Proof.* By strong induction on the step $\tau$ of the read. Let $\sigma < \tau$ be the step of the last execution of the definition of $r$ before $\tau$. It exists by Lemma 3.

*Names of line L28.* At $\sigma$ the instruction computed $r$ from the current values of $o_1$ and $o_2$. Their definitions come before $r$ and $r$ comes before the reading point. If one of them ran again between $\sigma$ and $\tau$, Lemma 2 would run $r$ again before $\tau$, against the choice of $\sigma$. So the operands have the same values at $\sigma$ and at $\tau$.

*Names of line L21.* Here $r$ has meaning $iv \mathbin{op} rc$ with $op$ one of $+$, $-$ and $\times$. Write $k$ for the value of $rc$. The definition of $iv$ runs in the step just before $\sigma$, or in the same step for a phi. It is a phi, a copy, or an add or subtract with one region constant, because line L9 accepts only these, line L14 makes copies, and line L21 copies such definitions. The definition of $iv$ is never changed after it is copied: a name with a header is never replaced at line L14, and line L6 changes only comparisons. We show that $r = iv \mathbin{op} k$ right after $\sigma$.

- $iv = \phi(\ldots, o_p, \ldots)$. The copy is $r = \phi(\ldots, e_p, \ldots)$ where $e_p$ is Reduce or Apply of $(op, o_p, rc)$. Coming from $p$, both read at the end of $p$, a step before $\tau$, so by induction $e_p = o_p \mathbin{op} k$ there, and $iv = o_p$.
- $iv = o$, a copy of an induction variable with the same header. Then $r = e$ with $e = \mathrm{Reduce}(op, o, rc)$, and by induction $e = o \mathbin{op} k$.
- $iv = a + b$ with $a$ in the component and $b$ a region constant, or the same with the sides swapped. The copy is $r = a' + b'$ with $a' = a \mathbin{op} k$ by induction. If $op$ is $\times$, then $b' = b \cdot k$ and $r = (a + b) k$. If $op$ is $+$ or $-$, then $b' = b$ and $r = (a \pm k) + b = (a + b) \pm k$.
- $iv = a - b$ with $a$ in the component and $b$ a region constant. The same identities give $(a - b) k$ and $(a - b) \pm k$.

Between $\sigma$ and $\tau$ the value of $iv$ does not change: its definition stands right before $r$ and cannot trap, so a new execution of it is followed by a new execution of $r$ in the same visit. The value of $rc$ does not change either: its definition comes before $r$, and Lemma 2 applies as for line L28. So at $\tau$ the identity still holds. $\square$

## The rewritten instructions

**Lemma 5.** In every run of $P_1$, every replaced candidate and every rewritten comparison computes the same value as the original instruction would compute at the same step.

*Proof.* A candidate $x = iv \mathbin{op} rc$ became $x = r$ with $r = \mathrm{Reduce}(op, iv, rc)$, and Lemma 4 gives $r = iv \mathbin{op} rc$ at that step.

A comparison $c = a \mathbin{cmp} b$ with an induction variable $a$ and a region constant $b$ is rewritten in rounds. One round uses a reduction $r = a \mathbin{op} k$ of $a$ and the name or value $b' = b \mathbin{op} k$ of Apply, and Lemma 4 holds for both at the step of the comparison. For $op$ equal to $+$ or $-$, $a \mathbin{cmp} b$ and $r \mathbin{cmp} b'$ agree for every $cmp$ in $<$, $\le$, $=$ and $\ne$, because adding the same integer to both sides keeps the order. For $op$ equal to $\times$, line L6 uses only an integer $k \ne 0$. For $k > 0$ the order is kept. For $k < 0$ it is reversed, so $a < b$ holds if and only if $b' < r$, the same for $\le$, and the sides are swapped. Equality and inequality do not depend on the sign. With $b$ on the left the argument is the same. Each round keeps the value, and $b'$ is again a region constant for $h$, so by induction on the rounds the final comparison computes the original value. $\square$

## The same behavior

**Lemma 6.** $P_1$ behaves like $P$ on every input.

*Proof.* Run both in lock-step. They have the same blocks and the same terminators. By induction on the steps, the original names have the same current values in both. In a block, $P_1$ executes the original instructions in the original order, some of them rewritten, and new instructions in between. A new instruction defines only a new name. It is a phi, a copy, or $+$, $-$ or $\times$ on integers, so it cannot trap: its operands are integers by the assumption on pointers, and every name it reads is defined by Lemma 3. A rewritten instruction computes the same value by Lemma 5. Every other instruction reads the same values. So the branches go the same way, the stores, calls and loads see the same values, and the same trap or return happens at the same visit. $\square$

**Lemma 7.** The deletion at line L7 keeps the behavior.

*Proof.* Line L7 marks every name that a terminator, a store, a call, a load, an `alloc` or an operation that may trap reads, and then every name that the definition of a marked name reads. It deletes only constants, copies, phi-functions and operations that cannot trap whose names are not marked. A kept instruction reads only marked names, so their definitions are kept. Run $P_1$ and $P'$ in lock-step. $P'$ executes the kept instructions in the same order, and by induction they compute the same values. The deleted ones cannot trap and write no memory. So the branches and the outcome are the same. $\square$

Lemmas 6 and 7 together prove the claim. The run of $P'$ visits the same blocks as the run of $P$, so it ends exactly when the run of $P$ ends.

**Integers that wrap.** The identities of Lemma 4 hold modulo $2^w$, so the rewrite of candidates is also correct for integers of $w$ bits that wrap. Lemma 5 for the order tests $<$ and $\le$ is not: with wrapping, neither adding $k$ nor multiplying by $k$ keeps the order. A compiler for such integers must prove that no value in the new comparison wraps before it replaces such a test. Tests for equality and inequality through $+$ and $-$ stay correct, and through $\times$ they need an odd $k$ or a proof that nothing wraps.
