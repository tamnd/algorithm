---
title: SSAPRE keeps the outcome, inserts only at down-safe points, and never adds an evaluation on a path
proves: [correctness]
status: full
---

**Setting.** The program has const, copy and op instructions only. After line L1, every block is reachable from the entry block, the entry block has no predecessor, and no edge goes from a block with two successors to a block with two predecessors. We also assume that every block can reach a `ret`. A *path* is a sequence of blocks along edges, and a *complete path* starts at the entry and ends at a block with `ret`. We count *positions* on a path, because a path can visit a block more than once.

Fix one expression $e = a \mathbin{op} b$. The steps for different expressions do not share anything, so this is no loss. A *kill* is an instruction that defines $a$ or $b$. A real occurrence is an instruction `x = e`. It reads $a$ and $b$ before it defines $x$, so `a = a + b` is a real occurrence followed by a kill.

Line L2 gives each variable its versions in minimal SSA form: the variable has a φ at each block of the iterated dominance frontier of the blocks that define it, the entry counted. We use the standard property of SSA form.

**(V)** If the version of $a$ at a point $q$ is $d$, then the definition $d$ dominates $q$, and on every path from the entry to $q$ the last definition of $a$ is $d$. A φ counts as a definition at the top of its block.

Line L4 puts a Φ for $e$ at each block of $\Phi\text{-blocks} = \mathrm{DF}^+(\text{blocks with a real occurrence}) \cup \{\text{blocks with a φ for } a \text{ or } b\}$. Both parts are closed under the dominance frontier, so $\mathrm{DF}(Y) \subseteq \Phi\text{-blocks}$ for each block $Y$ that has a real occurrence or a Φ. The φ blocks of $a$ are closed because a φ is a definition of $a$ too.

A block in a dominance frontier has two or more predecessors. Since the critical edges are split, each predecessor of a Φ block has exactly one successor.

## 1. The rename walk

Line L5 walks the dominator tree in preorder. At a Φ block it pushes the Φ, and at each real occurrence it pushes the occurrence. When it leaves a block, it pops what the block and its subtree pushed. Each stack entry carries the versions of $a$ and $b$ at its own point. An occurrence whose versions equal those of the top of the stack gets the version of the top, and we call the top its *definition*. A Φ operand from a predecessor $p$ is the top at the end of $p$ if the versions match, and ⊥ if not. The operand *has a real use* if that top is a real occurrence.

**Lemma 1.** If an occurrence or a Φ operand at point $q$ has the definition $D$, then $D$ dominates $q$, and on every path from the entry to $q$ there is no kill after the last position of $D$.

*Proof.* The stack holds only entries of blocks on the dominator tree path from the entry to the current block, and entries before $q$ in the current block. So $D$ dominates $q$. Assume a path from the entry to $q$ has a definition of $a$ after the last position of $D$. Let $d$ be the version of $a$ at $q$. By (V) the last definition of $a$ before $q$ is $d$, so $d$ is after the last $D$, and the part of the path from that $d$ to $q$ does not pass $D$. Any path from the entry to $d$, followed by that part, is a path to $q$. It passes $D$, so the path to $d$ passes $D$, and $D$ dominates $d$. But $D$ sees the same version $d$ of $a$, so by (V) $d$ dominates $D$. Two different points cannot dominate each other, and $d$ before $D$ in one block is not possible either, because then the part from $d$ to $q$ would pass $D$. The same holds for $b$. $\square$

**Lemma 2.** Let $C$ be a block with no Φ and let $p$ be a predecessor of $C$. When the walk enters $C$, the top of the stack and the versions of $a$ and $b$ are the same as at the end of $p$.

*Proof.* $C$ has no φ for $a$ or $b$, so by (V) their versions at the top of $C$ are the versions at the end of each predecessor. The walk enters $C$ with the stack it had after it finished the block $\mathrm{idom}(C)$. The immediate dominator of $C$ dominates $p$. Let $Y$ be a block on the dominator tree path strictly below $\mathrm{idom}(C)$ down to $p$. Then $Y$ dominates $p$ and does not strictly dominate $C$, so $C \in \mathrm{DF}(Y)$. If $Y$ had a real occurrence or a Φ, $C$ would be a Φ block. So the stack at the end of $p$ has nothing above what $\mathrm{idom}(C)$ left. $\square$

**Corollary 3.** Let a path go from a point $q$ to a point $r$ and pass no real occurrence and no top of a Φ block, other than possibly the one at $q$. Then the walk sees the same top of the stack at $q$ and at $r$. The versions are also the same if the path has no kill.

*Proof.* Inside a block the walk pushes only at real occurrences. Between blocks, apply Lemma 2. $\square$

## 2. Down-safety

A point is *down-safe* if every path from it reaches a real occurrence before a kill or the end of a `ret` block.

**Lemma 4.** If a Φ $F$ is still down-safe after line L6, then the top of its block is down-safe.

*Proof.* We show the other direction: if a path $\pi$ from the top of the block of $F$ reaches a kill or a `ret` before a real occurrence, then $F$ is marked. We use induction on the length of $\pi$. Look at the first event on $\pi$ of these kinds: the walk reaches a real occurrence, the end of a `ret` block, or the end of a predecessor of a Φ block. Up to this event, Corollary 3 says that the top is $F$.

- If $\pi$ has a kill before the event, the versions now differ from those of $F$. At a real occurrence with a different version, L5 marks the top $F$. At the end of a predecessor of a Φ block, the operand is ⊥ and L5 marks $F$. At a `ret`, L5 marks $F$.
- If $\pi$ has no kill before the event, the event is not a real occurrence, because $\pi$ has none before its kill or `ret`. If it is a `ret`, L5 marks $F$. If it is the end of a predecessor of a Φ block $G$, then the operand of $G$ is $F$ with no real use. The rest of $\pi$ from the top of $G$ is shorter and still bad, so by induction $G$ is marked. Then line L6 marks $F$ through this operand. $\square$

## 3. Insertions are safe

**Lemma 5.** If line L10 marks an operand of a Φ $f$ for insertion, then $f$ is down-safe.

*Proof.* $f$ is will-be-avail, so it is can-be-avail. If the operand is ⊥ and $f$ is not down-safe, line L7 would reset $f$. So let the operand come from a Φ $g$ with no real use, with $g$ not will-be-avail, and assume $f$ is not down-safe. By L6, $g$ is not down-safe. If $g$ were not can-be-avail, the reset of $g$ in L7 would reach $f$. So $g$ is can-be-avail and later.

Let $S$ be the set of Φs that are not down-safe, can-be-avail and later. $g \in S$. Take $h \in S$. It has no ⊥ operand (L7), and no operand with a real use (L8). Each operand comes from a Φ $h'$. $h'$ is later, or L8 would reset $h$. $h'$ is can-be-avail, or L7 would reset $h$. $h'$ is not down-safe, by L6. So $h' \in S$.

Take a path from the entry to the block of $g$. The operand of $g$ from the predecessor on this path comes from some $h' \in S$, whose block dominates that predecessor by Lemma 1. So the path visits the block of $h'$ at an earlier position. Repeat with $h'$. The positions decrease forever on a finite path, which is not possible. So $f$ is down-safe. $\square$

**Theorem A (safety).** Each `t = e` that line L11 inserts is at a down-safe point.

*Proof.* The insertion is at the end of a predecessor $p$ of the block of $f$, just before the terminator. $p$ has one successor, the block of $f$, and a terminator does not kill. The top of the block of $f$ is down-safe by Lemmas 5 and 4. $\square$

## 4. The outcome does not change

Line L11 keeps one plain name $t$ for $e$, and writes it only with `t = e`. Say $t$ is *good* at a position of a run if the run executed `t = e` at an earlier position and no kill after it. Then $t$ holds the value of $e$ for the current $a$ and $b$.

**Lemma 6.** In every run of the new program, $t$ is good at each reload and at the top of the block of each will-be-avail Φ.

*Proof.* Strong induction on the position in the run. The entry block has no Φ.

- A reload $R$ has a definition $D$, and by Lemma 1 there is no kill from the last $D$ to $R$. If $D$ is a real occurrence that computes, L10 marked it to save, so the run executed `t = e` there. If $D$ is a reload, or a will-be-avail Φ, $t$ is good at the last $D$ by induction. In each case it stays good up to $R$.
- At the top of the block of a will-be-avail $f$, entered from $p$: if the operand is marked for insertion, `t = e` ran at the end of $p$. Otherwise it is not ⊥. If it has a real use, its definition saves or reloads, and if not, it comes from a will-be-avail Φ. Lemma 1 and the induction finish the proof as before. $\square$

**Theorem B.** On every input, the new program returns the same value as the original, or traps if the original traps.

*Proof.* Run both programs side by side. They take the same branches as long as the old names hold the same values. A kept instruction does the same thing. A reload gives $x$ the value of $e$ by Lemma 6, which is what the original computes, and a reload cannot trap. A save computes $e$ and copies it. An inserted `t = e` writes only $t$.

If the original returns, every real occurrence on its run evaluates $e$ without a trap. An inserted evaluation is at a down-safe point (Theorem A), so the original later evaluates $e$ on the same operand values, and the inserted one does not trap either. If the original traps at an instruction that the new program keeps or saves, the new program traps there too, unless it trapped earlier. If it traps at a real occurrence that the new program reloads, then $t$ is good there, so the new program already evaluated $e$ on the same operand values and trapped. An earlier trap of the new program is at an inserted or saved evaluation of $e$, and by down-safety or by the same values the original also traps. $\square$

## 5. No path gets more evaluations

**Lemma 7.** Let $F$ be a Φ that is will-be-avail and down-safe after L6, and let a path go from the top of its block to a real occurrence $R$ with no real occurrence and no kill before $R$. Then each Φ $G$ on the path is will-be-avail, the operand of $G$ on the path is not marked for insertion, and $R$ is a reload.

*Proof.* Let $G_0 = F, G_1, \dots, G_k$ be the Φs at the tops of the blocks on the path, in order. By Corollary 3 the operand of $G_{i+1}$ on the path comes from $G_i$ with no real use, and the definition of $R$ is $G_k$. If $G_i$ is down-safe, then $G_{i+1}$ is down-safe, or L6 would mark $G_i$ through this operand. A down-safe Φ is never reset by L7. $G_i$ is not later, so the reset of $G_i$ in L8 reached $G_{i+1}$. So each $G_i$ is will-be-avail, each operand on the path comes from a will-be-avail Φ and is not marked for insertion, and $R$ reloads from $G_k$. $\square$

**Theorem C.** On every complete path, the new program evaluates $e$ at most as often as the original.

*Proof.* The new program evaluates $e$ at a computing occurrence, which the original also evaluates, and at insertions. Send each insertion at the end of $p$, for the Φ $f$, to the first real occurrence $R$ after it on the path. $R$ exists and the part before it has no kill, because the point is down-safe (Theorem A). $f$ is down-safe by Lemma 5, so by Lemma 7, $R$ is a reload, and it is not a computing occurrence. Two insertions cannot go to the same $R$: the later one would be on an operand of a Φ on the path between the earlier one and $R$, and Lemma 7 says that such an operand is not marked. So the map is one to one into the occurrences that the new program reloads. $\square$

**Computational optimality.** Kennedy, Chan, Liu, Lo, Tu and Chow prove that the result is also computationally optimal: no safe placement evaluates $e$ fewer times on any path. We do not repeat that proof here. The tests compare the count on every path of random acyclic programs with busy code motion, which is computationally optimal, and the counts are equal.
