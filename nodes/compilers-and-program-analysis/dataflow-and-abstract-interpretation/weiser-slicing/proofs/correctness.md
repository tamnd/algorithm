---
title: Weiser's algorithm stops after at most c + 1 rounds, finds the dependence slice, and its projection is a slice
proves: [correctness, termination]
status: full
---

**Setting.** $P$ is a toy IR program with instructions `x = k`, `x = y` and `x = a op b`, and terminators `jump`, `br` and `ret`. Every block reaches a `ret`. Statements, the successor relation $n \to m$ between statements, $DEF$, $REF$, the criterion $C = \langle p, V \rangle$, the sets $R$, $S$, $B$ and $INFL$ and the projection are as on the page. There are $c$ branches. Post-dominance is taken on the blocks with a virtual EXIT after every `ret`. For a block $\ell$ that ends in a branch, $d_\ell$ is its immediate post-dominator. For a set $X$ of statements, $\mathrm{blk}(X)$ is the set of their blocks.

Two standard facts about post-dominance are used. (PD1) If $a$ post-dominates $b$ and $b$ post-dominates $a$, then $a = b$: otherwise take a shortest path from $a$ to EXIT; it meets $b$ after $a$, and the rest of it, from $b$, meets $a$ again, which gives a shorter path from $a$ to EXIT. (PD2) The strict post-dominators of a block form a chain, and the immediate one is post-dominated by all the others (see [post-dominance](/post-dominance/)).

## 1. The equations and their least solution

For seeds $\sigma$ (a set of names at each statement), the equations are

$$R(n) = \sigma(n) \cup \bigcup_{n \to m} f_n(R(m)), \qquad f_n(X) = (X \setminus DEF(n)) \cup \begin{cases} REF(n) & \text{if } DEF(n) \cap X \ne \emptyset \\ \emptyset & \text{otherwise.} \end{cases}$$

**Lemma 1.** Each $f_n$ is monotone and distributive: $f_n(X \cup Y) = f_n(X) \cup f_n(Y)$ and $f_n(\emptyset) = \emptyset$. The function RELEVANT-SETS returns the least solution $R_\sigma$, and $\sigma \subseteq \sigma'$ (pointwise) implies $R_\sigma \subseteq R_{\sigma'}$.

*Proof.* $(X \cup Y) \setminus D = (X \setminus D) \cup (Y \setminus D)$, and $D \cap (X \cup Y) \ne \emptyset$ holds if and only if $D \cap X \ne \emptyset$ or $D \cap Y \ne \emptyset$; this gives distributivity, and monotonicity follows. The sets in the code only grow, inside the finite set of names, so the loop stops. Each name it adds is forced by an equation from values that are already below the least solution, so by induction on the number of additions the result is below the least solution. When the loop stops, every equation holds, because each change of $R(m)$ puts $m$ back on the worklist and so recomputes $f_n(R(m))$ for every predecessor $n$. A solution below the least solution is the least solution. For the last claim, the least solution for $\sigma'$ satisfies $R(n) \supseteq \sigma(n) \cup \bigcup f_n(R(m))$, and by the Knaster-Tarski theorem the least solution for $\sigma$ is below every such set. $\square$

By distributivity, the least solution for a union of seeds is the union of the least solutions for each seed, so the seeds of round $k$ give the same sets as Weiser's $R^0_C \cup \bigcup_{b \in B} R^0_{\langle b, REF(b) \rangle}$.

**Lemma 2 (paths).** Let $T$ be a set of statements and let $\sigma(u) = REF(u)$ for $u \in T$, with $\sigma(p) \supseteq V$ added. Define $R^\ast(n)$ as the set of $x$ such that some path $n = n_0 \to \cdots \to n_k$ ($k \ge 0$) has no definition of $x$ among $n_0, \ldots, n_{k-1}$ and either $n_k = p$ and $x \in V$, or $n_k \in T$ and $x \in REF(n_k)$. Then for every statement $n$ and successor $m$, $x \in R^\ast(m)$ and $x \notin DEF(n)$ imply $x \in R^\ast(n)$.

*Proof.* Put $n$ in front of the path for $x$ from $m$. $\square$

## 2. Termination

Number the rounds $k = 1, 2, \ldots$. Round $k$ uses $B_{k-1}$ (with $B_0 = \emptyset$), computes $R_k$ from the seeds $V$ at $p$ and $REF(b)$ at each $b \in B_{k-1}$, then $S_k = \{n : DEF(n) \cap R_k(m) \ne \emptyset \text{ for its successor } m\} \cup B_{k-1}$, then $B_k = \{b : INFL(b) \cap \mathrm{blk}(S_k \cup \{p\}) \ne \emptyset\}$, and it stops when $B_k = B_{k-1}$.

**Lemma 3.** $B_{k-1} \subseteq B_k$ for all $k$, and the algorithm stops after at most $c + 1$ rounds.

*Proof.* $B_0 = \emptyset \subseteq B_1$. If $B_{k-1} \subseteq B_k$, the seeds of round $k + 1$ contain those of round $k$, so $R_k \subseteq R_{k+1}$ by Lemma 1, then $S_k \subseteq S_{k+1}$, and $B_k \subseteq B_{k+1}$, since the test on $INFL$ is monotone in $S$. Each round that does not stop adds at least one branch to $B$, and there are $c$ branches, so at most $c$ rounds do not stop. $\square$

At the last round $B_k = B_{k-1}$. Write $R$, $S$ and $B$ for its values. Then:

- (F1) An instruction $n$ with successor $m$ is in $S$ if and only if $DEF(n) \cap R(m) \ne \emptyset$; then $REF(n) \subseteq R(n)$ by the equation.
- (F2) An instruction $n \notin S$ with successor $m$ has $DEF(n) \cap R(m) = \emptyset$, so $R(m) \subseteq R(n)$ and $n$ writes no name of $R(m)$.
- (F3) A terminator $n$ has $DEF(n) = \emptyset$, so $R(m) \subseteq R(n)$ for every successor $m$.
- (F4) A branch is in $S$ if and only if it is in $B$; then $REF(b) \subseteq R(b)$, since $REF(b)$ is a seed at $b$.
- (F5) A branch $b \notin B$ has no block of $\mathrm{blk}(S \cup \{p\})$ in $INFL(b)$.
- (F6) $V \subseteq R(p)$.

## 3. INFL is the transitive control dependence

For blocks, $y$ is *control dependent* on $x$, written $y \in CD(x)$, if some successor $s$ of $x$ is post-dominated by $y$ (with $y = s$ allowed) and $y$ does not strictly post-dominate $x$.

**Lemma 4.** For every block $\ell$ that ends in a branch, $INFL(\ell)$ is the transitive closure $CD^+(\ell)$.

*Proof.* Let $d = d_\ell$. First, (KF): $d$ strictly post-dominates every $y \in INFL(\ell)$. Indeed $y \ne d$, and for a path from $y$ to EXIT, put in front of it the path from $\ell$ to $y$ that avoids $d$ after $\ell$. The result is a path from $\ell$ to EXIT, so it meets $d$, and it can only meet $d$ in the part from $y$.

*A step.* Let $x \in \{\ell\} \cup INFL(\ell)$, let $z \in CD(x)$ by the successor $s$, and suppose that every path from $s$ to $z$ meets $d$ before $z$. Every path from $s$ to EXIT meets $z$, so it meets $d$ first. A path from $s$ to the first $d$ followed by any path from $d$ to EXIT is a path from $s$ to EXIT, and it has $z$ only after that $d$, so $z$ post-dominates $d$. Since $d$ post-dominates $x$ (for $x = \ell$ by definition, else by KF), $z$ post-dominates $x$. If $z = x$, then $x$ and $d$ post-dominate each other and $x = d$ by PD1, which is false ($d \ne \ell$ and KF). If $z \ne x$, then $z$ strictly post-dominates $x$, against $z \in CD(x)$. So some path from $s$ to $z$ avoids $d$ before $z$, and $z \ne d$, because $z = d$ would strictly post-dominate $x$. With the path from $\ell$ to $x$, this gives $z \in INFL(\ell)$.

Applied to $x = \ell$, the step gives $CD(\ell) \subseteq INFL(\ell)$, and applied to $x \in INFL(\ell)$ it gives $CD(x) \subseteq INFL(\ell)$. So $CD^+(\ell) \subseteq INFL(\ell)$.

*Converse.* Let $y \in INFL(\ell)$ by the path $\ell = s_0, s_1, \ldots, s_k = y$, $k \ge 1$, with $s_1, \ldots, s_k \ne d$. Induction on $k$. Let $j$ be the largest index in $0, \ldots, k - 1$ such that $y$ does not post-dominate $s_j$. If $j$ exists, then $y$ post-dominates $s_{j+1}$ and does not post-dominate $s_j$, so $y \in CD(s_j)$. For $j = 0$ this is $y \in CD(\ell)$, and for $j \ge 1$, $s_j \in INFL(\ell)$ by a shorter path, so $s_j \in CD^+(\ell)$ and $y \in CD^+(\ell)$. If $j$ does not exist, $y$ post-dominates $\ell$ and $s_1$. If $y = \ell$, then $y \in CD(\ell)$ by $s_1$. If $y \ne \ell$, then $y$ and $d$ both strictly post-dominate $\ell$, so $y$ post-dominates $d$ by PD2, and $d$ post-dominates $y$ by KF, so $y = d$ by PD1, which is false. $\square$

## 4. The result is the dependence slice

Let $K^\ast$ be the dependence slice of the page [program slicing](/program-slicing/): the least set of instructions and branches closed under its rules 1 to 3. In block terms, a statement is control dependent on the branch of block $x$ when its block is in $CD(x)$.

**Lemma 5.** $S = K^\ast$.

*Proof.* ($K^\ast \subseteq S$.) It is enough to show that $S$ satisfies the three rules. Rule 1: if $s$ defines $x \in V$ and a path from the successor $m$ of $s$ to $p$ has no definition of $x$, then by F6 and by F2, F3 and the equations along the path, $x \in R(m)$, so $s \in S$ by F1. Rule 2: if the block of $p$ is in $CD(x)$ for a branch $b$ ending $x$, it is in $INFL(b)$ by Lemma 4, so $b \in B \subseteq S$ by F5. Rule 3: let $t \in S$. If $t$ reads $x$ and $s$ defines $x$ with a path from the successor $m$ of $s$ to $t$ that has no definition of $x$ before $t$, then $x \in REF(t) \subseteq R(t)$ by F1 or F4, and as for rule 1, $x \in R(m)$, so $s \in S$. If the block of $t$ is in $CD(x)$ for the branch $b$ of $x$, then $b \in S$ as for rule 2.

($S \subseteq K^\ast$.) By induction on the rounds, $S_k \subseteq K^\ast$ and $B_k \subseteq K^\ast$. Suppose $B_{k-1} \subseteq K^\ast$. Take $T = K^\ast$ in Lemma 2. Then $R^\ast$ contains the seeds of round $k$ ($V$ at $p$ by a path of length 0, and $REF(b)$ at $b \in B_{k-1} \subseteq K^\ast$). Let $y \in DEF(n) \cap R^\ast(m)$ for a successor $m$ of $n$. The path for $y$ from $m$ ends at $p$ with $y \in V$, and then $n \in K^\ast$ by rule 1, or at some $u \in K^\ast$ that reads $y$, and then $u$ is data dependent on $n$ and $n \in K^\ast$ by rule 3. In both cases $REF(n) \subseteq R^\ast(n)$ by a path of length 0. With Lemma 2, $R^\ast$ satisfies $R^\ast(n) \supseteq \sigma(n) \cup \bigcup_m f_n(R^\ast(m))$, so $R_k \subseteq R^\ast$ by Lemma 1 (Knaster-Tarski). Hence every $n$ with $DEF(n) \cap R_k(m) \ne \emptyset$ is in $K^\ast$, by the same argument, and $S_k \subseteq K^\ast$. Last, a branch $b \in B_k$ has some $u \in S_k \cup \{p\}$ whose block is in $INFL(b) = CD^+(b)$ by Lemma 4. Follow the chain of control dependences from $b$ down to the block of $u$: each branch on it is in $K^\ast$ by rule 2 (when $u = p$ and the branch is the last one) or rule 3, going up the chain from $u$. So $b \in K^\ast$. $\square$

## 5. The projection is a slice

Let $Q$ be the projection: the instructions of $S$ stay, every jump stays, a branch in $B$ stays, a branch $b \notin B$ at the end of block $\ell$ becomes `jump` $d_\ell$ (or `ret 0` if $d_\ell$ is EXIT), and a `ret a` keeps $a$ only if $a \in R$ at that return. For a statement $n = (\ell, i)$ of $P$, let $\pi(n) = (\ell, j)$, where $j$ is the number of instructions of $S$ in $\ell$ before position $i$; it is the position in $Q$ of the first kept statement of $\ell$ at or after $n$. The point $p_Q$ of the page is $\pi(p)$.

We consider runs of $P$ that never read an undefined name. A configuration is a statement and an environment (a partial map from names to integers). Say $(n, \sigma) \sim (q, \tau)$ when $q = \pi(n)$ and, for every $x \in R(n)$, either both $\sigma(x)$ and $\tau(x)$ are undefined or both are defined and equal.

**Lemma 6 (one step).** Suppose $(n, \sigma) \sim (q, \tau)$.

1. If $n$ is an instruction not in $S$ and $P$ does not trap at $n$, then $P$ moves to $(m, \sigma')$, $Q$ does not move, and $(m, \sigma') \sim (q, \tau)$.
2. If $n$ is an instruction in $S$, then $P$ traps at $n$ if and only if $Q$ traps at $q$. Otherwise $P$ moves to $(m, \sigma')$, $Q$ moves to $(q', \tau')$, and $(m, \sigma') \sim (q', \tau')$.
3. If $n$ is a jump or a branch in $B$, both move to the start of the same block, with unchanged environments, and the relation holds there.
4. If $n$ is a `ret`, both runs end. If $Q$ kept the operand, both return the same value.

*Proof.* 1. $\pi(m) = \pi(n) = q$, because $n$ is not kept. By F2, $n$ writes no name of $R(m) \subseteq R(n)$, so $\sigma'$ and $\sigma$ agree on $R(m)$, and $\sigma$ agrees with $\tau$ there. 2. $Q$ runs the same instruction. By F1, $REF(n) \subseteq R(n)$, so the operands have the same values, and the two runs trap together or compute the same value $v$ for $x = DEF(n)$. Then $\pi(m) = q'$, and $R(m) \subseteq R(n) \cup \{x\}$ by the equation; $\sigma'$ and $\tau'$ agree on $R(n) \setminus \{x\}$ and both map $x$ to $v$. 3. By F4, $REF(b) \subseteq R(b)$, so the branch goes the same way in both. By F3, $R(m) \subseteq R(n)$ for the target $m$, whose position in $Q$ is $\pi(m)$. 4. If the operand $a$ is kept, $a \in R(n)$. $\square$

**Lemma 7 (a skipped branch).** Suppose $(n, \sigma) \sim (q, \tau)$, where $n$ is a branch $b \notin B$ at the end of block $\ell$, and let $d = d_\ell$. Then $Q$ makes one step: it jumps to the start of $d$ with $\tau$ unchanged, or returns 0 when $d$ is EXIT. From $n$ on, until $P$ first enters $d$, the run of $P$ makes no observation, and if it enters $d$, at that moment its configuration $((d, 0), \sigma'')$ satisfies $((d, 0), \sigma'') \sim (\pi((d, 0)), \tau)$. If $d \ne$ EXIT, $P$ cannot reach a `ret` before it enters $d$.

*Proof.* Until it enters $d$, $P$ visits only blocks of $INFL(\ell)$, by the definition of $INFL$. By F5, these blocks hold no statement of $S$ and not the point $p$, so $P$ makes no observation there, and every statement it runs there is an instruction not in $S$ or a terminator. By F2 and F3, along the run $n = n_0, n_1, \ldots, n_r = (d, 0)$ we get $R(n_0) \supseteq R(n_1) \supseteq \cdots \supseteq R(n_r)$, and no $n_j$ writes a name of $R(n_{j+1}) \supseteq R(n_r)$. So $\sigma''$ agrees with $\sigma$ on $R(n_r)$, and $\sigma$ agrees with $\tau$ on $R(n) \supseteq R(n_r)$. If $d \ne$ EXIT, a `ret` block in $INFL(\ell)$ would give a path from $\ell$ to EXIT that avoids $d$, which is impossible. $\square$

**Theorem.** For every input $I$ on which the run of $P$ reads no undefined name: if the run of $P$ reaches a `ret`, then the run of $Q$ reaches a `ret` and $\mathrm{obs}_Q(I, \langle p_Q, V \rangle) = \mathrm{obs}_P(I, \langle p, V \rangle)$. If the run of $P$ traps or does not end, $\mathrm{obs}_P$ is a prefix of $\mathrm{obs}_Q$.

*Proof.* At the start both runs are at the first statement of the entry block with the same environment, so the relation holds. Lemmas 6 and 7 cut the run of $P$ into pieces, each matched with zero or one step of $Q$, and keep the relation at the end of each piece. Each step of $Q$ is matched with at least one step of $P$.

Observations. $P$ observes when it is at $p$. The block $\ell_p$ of $p$ is never inside a skipped region (F5), so the visits of $P$ and $Q$ to $\ell_p$ match one to one. In a visit, $P$ passes $p$ exactly once unless it traps before $p$, and $Q$ arrives at $\pi(p)$ exactly once, before $P$ passes the instructions of $\ell_p$ at positions from its last kept statement before $p$ up to $p$, none of which is kept. At $P$'s observation, the relation holds with $Q$ at $\pi(p)$ and $Q$'s environment as it was when $Q$ arrived there, and $V \subseteq R(p)$ by F6, so both see the same tuple.

If $P$ reaches a `ret`, then by Lemma 6 (4) or Lemma 7 (when $P$ returns inside a skipped region with $d$ = EXIT, $Q$ returns at its `ret 0`), $Q$ returns at the matching moment, after no more steps than $P$, and neither run observes again. So the sequences are equal. If $P$ traps, it traps in a non-kept instruction (then $Q$ may go on and observe more) or in a kept one (then $Q$ traps at the same moment). If $P$ does not end, every observation of $P$ is matched by one of $Q$, in order. In both cases $\mathrm{obs}_P$ is a prefix of $\mathrm{obs}_Q$. $\square$

With Lemma 5, this proves the claim of the page [program slicing](/program-slicing/) that the dependence slice, used as the kept set, is a slice.
