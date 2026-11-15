---
title: AWZ finds the coarsest congruence, and congruent values are equal
proves: [correctness]
status: full
---

**Setting.** $S$ is a strict SSA program in the toy IR with only phis and op instructions: every operand is a constant, a parameter or a name whose definition dominates the use, and the use of a phi operand for predecessor $P$ is at the end of $P$. The SSA builder of the implementation gives such a program, because it folds copies and constants into the operands and reads 0 where no definition reaches. A *point* is a position between two instructions; a definition $d$ *dominates* a point $p$ if every path from the entry to $p$ runs through $d$ before it reaches $p$. The phis of a block run as one group when the block is entered, so the first point of a block is after its phis.

The value graph $G$ has a node for each parameter, each SSA name and each constant. Its label is ("param", $p$), ("op", $\mathit{op}$), ("phi", $B$) or ("const", $k$). The children of an op are its two operands, and the children of a phi in block $B$ are its operands in the order of the predecessors of $B$. A *congruence* is an equivalence relation $R$ on the nodes such that $u \mathrel{R} v$ implies that $u$ and $v$ have the same label and the same number of children, and $\mathrm{ch}_j(u) \mathrel{R} \mathrm{ch}_j(v)$ for every position $j$. A partition is a congruence if the relation "same class" is one.

## 1. The coarsest congruence exists

Let $R^*$ be the transitive closure of the union of all congruences. The identity is a congruence, so $R^*$ is reflexive, and it is symmetric and transitive. If $u \mathrel{R^*} v$, there is a chain $u = w_0, w_1, \ldots, w_m = v$ in which each step is in some congruence. Each step keeps the label and the number of children and relates the $j$-th children, so the chain of $j$-th children shows $\mathrm{ch}_j(u) \mathrel{R^*} \mathrm{ch}_j(v)$. So $R^*$ is a congruence, and every congruence refines it. It is the coarsest congruence.

## 2. The partition step finds it

The partition step keeps a partition $\pi$ and a worklist $W$ of classes. For a set $C$ and a position $j$, write $\mathrm{pre}_j(C)$ for the nodes whose $j$-th child is in $C$. Say that $\pi$ is *stable* for $C$ if every class $D$ of $\pi$ is inside $\mathrm{pre}_j(C)$ or disjoint from it, for every $j$.

Two facts hold because each node has at most one $j$-th child.

(F1) If $\pi$ is stable for $S_1$ and for $S_2 \subseteq S_1$, then it is stable for $S_1 \setminus S_2$, since $\mathrm{pre}_j(S_1 \setminus S_2) = \mathrm{pre}_j(S_1) \setminus \mathrm{pre}_j(S_2)$.

(F2) If $\pi$ is stable for $S$, every refinement of $\pi$ is stable for $S$.

**Invariant (I1).** Every congruence refines $\pi$. At the start $\pi$ is the partition by label and number of children, and every congruence refines it. A split of a class $D$ by $X = \mathrm{pre}_j(C)$, where $C$ is a union of classes of $\pi$, separates $u \in D \cap X$ from $v \in D \setminus X$. Nodes of $D$ have the same number of children, so $v$ has a $j$-th child, and it is outside $C$, while the $j$-th child of $u$ is in $C$. If a congruence $R$ had $u \mathrel{R} v$, then $\mathrm{ch}_j(u) \mathrel{R} \mathrm{ch}_j(v)$, and by (I1) the two children would be in one class of $\pi$, so both in $C$ or both outside it. This is false, so no congruence relates $u$ and $v$, and (I1) holds after the split.

**Invariant (I2).** For every class $C$ of $\pi$, either $C \in W$, or there is a set $U$ that is a union of classes in $W$ (possibly empty) such that $\pi$ is stable for $C \cup U$.

At the start every class is in $W$. Look at the two steps of the loop.

- *A split.* A class $D$ splits into a larger part, which keeps the name $D$, and a smaller part $D'$, which goes into $W$. If $D \in W$, both parts are in $W$. If $\pi$ was stable for $D \cup U$, it is now stable for $D \cup (D' \cup U)$ by (F2), and $D' \cup U$ is a union of classes in $W$. For any other class $E$ with a set $U \ni D$, $U$ is still a union of classes in $W$ after the split, because both parts are in $W$. Stability for a fixed set survives the split by (F2).
- *Taking $C$ out of $W$.* The step keeps $S$, the members of $C$ at that time, and splits every class by $\mathrm{pre}_j(S)$ for every $j$. After that, $\pi$ is stable for $S$. The classes inside $S$ are the class that keeps the name $C$, which is not in $W$, and the parts split off from it, which are in $W$. So $C$ satisfies (I2) with $U = S \setminus C$. Another class $E$ with a set $U$ that contains $S$ is stable for $E \cup U$ and for $S$, so by (F1) it is stable for $E \cup (U \setminus S)$, and $U \setminus S$ is a union of classes in $W$.

**End.** Each split adds a class, and there are at most $N$ classes for $N$ nodes, so there are at most $N - 1$ splits and at most $2N - 1$ classes ever enter $W$. When $W$ is empty, (I2) says that $\pi$ is stable for each of its classes. Then two nodes $u, v$ in one class have their $j$-th children in the same class for every $j$: if $\mathrm{ch}_j(u) \in C$, the class of $u$ meets $\mathrm{pre}_j(C)$, so it lies inside it. The classes also refine the labels, so $\pi$ is a congruence. By (I1) every congruence refines it. So $\pi$ is the coarsest congruence $R^*$.

**Cost.** Taking $C$ out of $W$ costs $O(|C|)$ plus the edges that enter $C$. Splitting a class $D$ by a part $P$ of size $|D \cap X|$ costs $O(|P|)$: if $P$ is at most half of $D$, the code moves $P$ out, and otherwise it builds $D \setminus P$, which is smaller than $P$. Fix a node $m$. Classes only shrink. A class that contains $m$ enters $W$ once at the start, and later only as a smaller part, which has at most half the size of the class of $m$ before the split. So at most $1 + \log_2 N$ classes that contain $m$ ever enter $W$, and $m$ and the edges into $m$ are scanned at most that often. The total is $O((N + E) \log N)$ for $E$ edges.

## 3. Congruent names hold equal values

Fix a run of $S$. For a name $x$ and a time $t$, let $\mathrm{val}_t(x)$ be the value that the latest execution of the definition of $x$ before $t$ wrote, and let $p_t$ be the point of the run at time $t$. A constant $k$ has the value $k$ at all times.

**Lemma.** If the definition of $c$ dominates the definition of $y$, and the definition of $y$ dominates $p_t$, then the latest execution of $c$ before $t$ came before the latest execution of $y$ before $t$.

*Proof.* Both have run, because their definitions dominate $p_t$. Suppose the latest $c$ came after the latest $y$. Dominance is antisymmetric and the two definitions differ, so $y$ does not dominate $c$, and there is a path from the entry to the definition of $c$ that avoids the definition of $y$. Continue it with the part of the run from the latest $c$ to $p_t$, which has no execution of $y$. This path reaches $p_t$ without the definition of $y$, which contradicts the dominance. $\square$

So when the definition of $y$ dominates $p_t$, the latest instance of $y$ was computed from the current values of its operands.

**Theorem.** Let $R$ be any congruence of $G$. At every time $t$ of the run, if $x \mathrel{R} y$ and the definitions of $x$ and $y$ both dominate $p_t$, then $\mathrm{val}_t(x) = \mathrm{val}_t(y)$.

*Proof.* By induction on $t$. At the start only the parameters are defined, and a parameter is congruent only to itself, because its label is unique. A step moves from $p_t$ to $p_{t+1}$ in one of two ways.

*An op $x = a \mathbin{op} b$ runs.* A definition other than $x$ that dominates $p_{t+1}$ also dominates $p_t$, because $p_t$ is the only point before $p_{t+1}$. So pairs that do not contain $x$ keep their values and the claim holds for them by induction. Now take $y \ne x$ with $x \mathrel{R} y$ whose definition dominates $p_{t+1}$. Then $y = c \mathbin{op} d$ with $a \mathrel{R} c$ and $b \mathrel{R} d$. First, $c \ne x$: otherwise the definition of $x$ dominates the definition of $y$, and the definition of $y$ dominates the point just before $x$, so by antisymmetry they are equal, which they are not. In the same way $d \ne x$. By the lemma, the latest $y$ computed $\mathrm{val}_t(c) \mathbin{op} \mathrm{val}_t(d)$ without a trap. The definitions of $c$ and $d$ dominate the definition of $y$, which dominates $p_t$, and the definitions of $a$ and $b$ dominate $p_t$ by strictness. By induction at $p_t$, $\mathrm{val}_t(a) = \mathrm{val}_t(c)$ and $\mathrm{val}_t(b) = \mathrm{val}_t(d)$, where a constant operand has its own value and is congruent only to the same constant. So $x$ computes the same operation on the same values. It does not trap, and it writes $\mathrm{val}_t(y)$.

*The run enters block $B$ from $P$ and runs the phis of $B$.* A definition that dominates the first point of $B$ and is not a phi of $B$ is in a block that strictly dominates $B$. That block dominates $P$, so the definition dominates $p_t$, the end of $P$, and old pairs keep their values. A phi of $B$ is congruent only to phis of $B$, because the label names the block. If $x$ and $y$ are phis of $B$ with $x \mathrel{R} y$, their operands $a_P$ and $c_P$ for $P$ are the children at the same position, so $a_P \mathrel{R} c_P$. Their definitions dominate the end of $P$ by strictness. By induction $\mathrm{val}_t(a_P) = \mathrm{val}_t(c_P)$, and both phis write this value. $\square$

The proof of the op case shows more: when $y$ is about to run and a congruent $x$ dominates it, the latest $x$ was computed from operands equal to those of $y$ without a trap. So $y$ does not trap either, and it would write $\mathrm{val}_t(x)$.

## 4. The elimination keeps every outcome

The elimination walks the dominator tree and keeps, for each class, the first definition it meets on the current branch of the tree. A definition $y$ whose class already has a representative $x$ in scope becomes `y = x`. The definition of $x$ dominates the definition of $y$: it is in a block that dominates the block of $y$, or earlier in the same block, or, when $y$ is a phi, it is a phi of the same block, since only phis of the block share its label. A representative is always a definition that was kept.

Run $S$ and the new program $S'$ on the same input, step by step. Both programs have the same blocks, terminators and number of instructions, so we show that they hold the same environment at every point. Assume it up to $p_t$.

- A kept instruction runs the same way in both.
- A replaced op $y$: by the remark after the theorem, $y$ in $S$ does not trap and writes $\mathrm{val}_t(x)$, and the copy in $S'$ writes the same value.
- A replaced phi $y$ of $B$ becomes a copy after the phis of $B$. In $S$, $y$ and $x$ are congruent phis of $B$, so by the theorem they get the same value on entry to $B$. In $S'$, $x$ is kept and gets that value, and the copy writes it into $y$ before any other instruction of $B$ reads $y$. A phi of $B$ that reads $y$ reads it at the end of a predecessor, where both programs agree by induction.

So the two runs return the same value, trap at the same step, or run out of fuel at the same step. The SSA builder keeps the outcome of the original program (by the usual argument for [SSA construction](/cytron-ssa-construction/), with copies folded), so the whole transformation does. Each op of $S'$ is an op of $S$ at the same place, so every run executes at most as many operations as before.
