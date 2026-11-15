---
title: Backward chaining with a loop check and memo tables decides the least model
proves: [correctness]
status: full
---

Let $P$ be a finite set of propositional definite rules $a \leftarrow b_1, \ldots, b_m$ (a fact has $m = 0$) and let $M$ be its least model. We use the procedure of the page: PROVE$(a)$ works with a goal stack $S$, a set *proved* and a set *failed*, and returns a pair $(\mathit{ok}, \mathit{low})$. The *depth* of an atom on $S$ is its position, counted from $0$ at the bottom.

## Proof trees

A *proof tree* for $a$ is a finite tree whose root carries $a$, in which a node with atom $x$ has children $y_1, \ldots, y_m$ for some rule $x \leftarrow y_1, \ldots, y_m$ of $P$. An atom $a$ is in $M$ exactly when it has a proof tree; this is the usual reading of $M = \bigcup_k T_P^k(\emptyset)$ by induction on $k$. For a set $X$ of atoms, $a$ is *$X$-provable* when it has a proof tree in which no node carries an atom of $X$. So $a \in M$ exactly when $a$ is $\emptyset$-provable, and an atom of $X$ is never $X$-provable.

**Lemma 1.** If $a$ is $X$-provable, then $a$ has a proof tree that avoids $X$ and in which no atom occurs twice on one path from the root.

*Proof.* Take an $X$-avoiding proof tree of least size. If an atom $x$ occurs at a node $u$ and again at a node $v$ below $u$, replace the subtree at $u$ by the subtree at $v$. The result is a smaller $X$-avoiding proof tree, a contradiction. $\square$

## Invariant

**Lemma 2.** At every moment, *proved* $\subseteq M$ and *failed* $\cap\, M = \emptyset$. Each call PROVE$(a)$ that returns $(\mathit{true}, \infty)$ has $a \in M$. Each call that returns $(\mathit{false}, l)$ has the property that $a$ is not $X$-provable for $X = \{ x \in S : \mathrm{depth}(x) \ge l \}$, where $S$ is the stack at the time of the call.

*Proof.* By induction on the number of calls that have returned. Take a call PROVE$(a)$ with stack $S$, $|S| = k$, and assume the claim for all calls that returned before it.

- Line L3: $a \in$ *proved* $\subseteq M$.
- Line L4: $a \in$ *failed*, so $a \notin M$, so $a$ is not $X$-provable for any $X$.
- Line L5: $a \in S$ at depth $d$, the result is $(\mathit{false}, d)$, and $a \in X$, so $a$ is not $X$-provable.
- Line L11: the rule $a \leftarrow b_1, \ldots, b_m$ had all inner calls return true, so each $b_j \in M$ by the induction hypothesis, and $a \in M$. Adding $a$ to *proved* keeps the invariant.
- Lines L12 to L14: every rule $a \leftarrow b_1, \ldots, b_m$ of $a$ had an inner call PROVE$(b_j)$ that returned $(\mathit{false}, c)$ with $c \ge \mathit{low}$. That call ran with the stack $S$ plus $a$ on top, at depth $k$. By the induction hypothesis $b_j$ is not $X_j$-provable, where $X_j$ is the set of atoms of $S \cup \{a\}$ at depth at least $c$.

  Let $l$ be the value that the call returns: $l = \infty$ when $\mathit{low} \ge k$ (line L13) and $l = \mathit{low}$ otherwise (line L14). Let $X$ be the set of atoms of $S$ at depth at least $l$. In both cases $X_j \subseteq X \cup \{a\}$: if $\mathit{low} \ge k$, then $c \ge k$ and $X_j \subseteq \{a\}$; if $\mathit{low} < k$, then $c \ge \mathit{low} = l$ and $X_j$ holds only atoms of $S$ at depth at least $l$, and maybe $a$.

  Assume that $a$ is $X$-provable. By Lemma 1 it has an $X$-avoiding proof tree in which $a$ does not occur below the root. The root uses some rule $a \leftarrow b_1, \ldots, b_m$, and the subtree of each $b_j$ avoids $X \cup \{a\} \supseteq X_j$. So the failed $b_j$ of that rule is $X_j$-provable, a contradiction. So $a$ is not $X$-provable.

  When $\mathit{low} \ge k$, $X = \emptyset$, so $a \notin M$, and line L13 keeps the invariant when it adds $a$ to *failed*. $\square$

## Termination

**Lemma 3.** Every call stops, and the stack never holds more than $n$ atoms, where $n$ is the number of atoms of $P$.

*Proof.* Line L6 pushes $a$ only after line L5 found that $a$ is not on $S$, so the atoms on $S$ are distinct and the recursion depth is at most $n + 1$. Each call makes at most one inner call for each body atom of each rule of $a$. So the tree of calls is finite. $\square$

## Theorem

BACKWARD-CHAIN$(P, g)$ stops, and it returns *true* exactly when $g \in M$. This holds also when the memo tables are kept from earlier goals.

*Proof.* The run stops by Lemma 3. The top call runs with the empty stack. If it returns true, $g \in M$ by Lemma 2. If it returns $(\mathit{false}, l)$, then $g$ is not $X$-provable for $X = \emptyset$, so $g \notin M$. Lemma 2 does not depend on the content of the memo tables at the start, only on the invariant, which holds for the empty tables and is kept by every call. $\blacksquare$

## Why a failure under a loop is not stored

If line L14 stored $a$ as failed, the invariant would break. In the program $g \leftarrow q$, $g \leftarrow s$, $q \leftarrow g$, $s$, the call PROVE$(q)$ inside PROVE$(g)$ meets $g$ on the stack and fails with $\mathit{low} = 0 < 1$. But $q \in M$, because $g \in M$ through $s$. The procedure stores nothing for $q$, and a later query for $q$ succeeds.
