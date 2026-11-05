---
title: Thompson's construction accepts exactly the language of the expression, with at most 2m states
proves: [correctness]
status: full
---

**Statement.** Let $r$ be a regular expression of size $m$ and let $N$ be the output of THOMPSON on the postfix form of $r$. Then $L(N) = L(r)$, $N$ has at most $2m$ states and $4m$ moves, and each state has at most two outgoing moves.

**Setup.** Each token of the postfix form is a node $t$ of the syntax tree of $r$, and the step that handles $t$ pushes one fragment $(s_t, f_t)$. Let $V(t)$ be the set of states created while the tokens of the subtree of $t$ were handled. The tokens of a subtree form a contiguous block of the postfix form that ends with $t$, so $V(t)$ is the disjoint union of the sets of the children of $t$ and the states created at $t$ itself. We say that a move *exists at time $T$* when it was added at or before step $T$; moves are never removed. A path *reads* $w$ when the symbols on its moves, in order, spell $w$.

**Lemma 1.** At the moment the fragment of $t$ is pushed: (a) every move that leaves a state of $V(t)$ ends in $V(t)$; (b) $f_t$ has no outgoing move; (c) $s_t$ has no incoming move.

*Proof.* By induction on the syntax tree. For a leaf, lines L4 to L6 create $s, f$ with at most the move $s \to f$, and no other move touches them. For a union, by the induction hypothesis the children satisfy (a) to (c) when they are pushed. Between the push of a child and the step of $t$, the only steps are those of tokens of the other child, which create new states and add moves only out of new states and out of exits of fragments of that other subtree; these touch no state of the first child, whose sets are disjoint. At line L10 the moves added leave $s$ (to $s_1, s_2 \in V(t)$) and leave $f_1, f_2$ (to $f \in V(t)$). So (a) holds, $f$ is new so (b) holds, and $s$ is new and gets no incoming move, so (c) holds. A star is the same, with the moves of line L15 all inside $V(t)$. For a concatenation, line L12 adds only $f_1 \to s_2$, inside $V(t)$; $f_t = f_2$ had no outgoing move and gets none; $s_t = s_1$ had no incoming move and gets none. $\square$

**Lemma 2.** After the fragment of $t$ is pushed, no state of $V(t) \setminus \{f_t\}$ gains an outgoing move.

*Proof.* A later step adds moves out of new states, which are not in $V(t)$, and out of the exits $f_u$ of fragments $u$ that it pops. Let $u$ be such a fragment with $f_u \in V(t)$. The sets of a parse tree are nested or disjoint, and $u$ is pushed after $t$, so $V(t) \subseteq V(u)$, and $t$ lies in the subtree of $u$. The exit $f_u$ is a state created at $u$, unless $u$ is a concatenation, in which case $f_u$ is the exit of its right child. Following right children of concatenations down from $u$, we reach a node whose exit was created at that node. The state $f_u$ lies in $V(t)$ only if $t$ is on this chain, and then $f_t = f_u$. $\square$

**Lemma 3.** At any time after the fragment of $t$ is pushed, let $P$ be a path that starts at $s_t$, ends at $f_t$, and visits $f_t$ only at its end. Then every state of $P$ is in $V(t)$ and every move of $P$ existed when the fragment was pushed.

*Proof.* Every move of $P$ leaves a state other than $f_t$. By induction along $P$: the first state $s_t$ is in $V(t)$; if the current state $q \ne f_t$ is in $V(t)$, then by Lemma 2 its outgoing moves all existed at the push, and by Lemma 1(a) they end in $V(t)$. $\square$

Call a path as in Lemma 3 a *clean path of $t$*. Since moves are never removed, the clean paths of $t$ are the same at every time after the push.

**Lemma 4.** For every node $t$ and string $w$, a clean path of $t$ reads $w$ if and only if $w \in L(t)$.

*Proof.* By induction on the syntax tree.

1. *Leaves.* The fragment of $a$ has only $s \xrightarrow{a} f$, so the only clean path reads $a$. The fragment of $\varepsilon$ has only $s \xrightarrow{\varepsilon} f$, which reads $\varepsilon$. The fragment of $\emptyset$ has no move, and $s \ne f$, so it has no clean path.
2. *Union $t = t_1 \mid t_2$.* A clean path $P$ starts with $s \to s_1$ or $s \to s_2$, say $s \to s_1$, since $s$ has no other move. From $s_1$, as long as $P$ has not reached $f_1$, Lemmas 2 and 1(a) for $t_1$ keep it in $V(t_1)$. It must reach $f_1$, because the only move into $f$ comes from $f_1$ or $f_2$, and $f_2 \notin V(t_1)$. The only move out of $f_1$ is $f_1 \to f$. So $P = s \to Q \to f$ where $Q$ is a clean path of $t_1$. By the induction hypothesis $Q$ reads a string of $L(t_1)$, so $P$ reads a string of $L(t)$. Conversely, a clean path of $t_1$ reading $w \in L(t_1)$, with the moves $s \to s_1$ and $f_1 \to f$ added, is a clean path of $t$ that reads $w$; the same holds for $t_2$.
3. *Concatenation $t = t_1 t_2$.* A clean path from $s_1$ stays in $V(t_1)$ until it reaches $f_1$, by the argument of case 2, and it must reach $f_1$, because $f_2 \notin V(t_1)$. The first visit to $f_1$ ends a clean path $Q_1$ of $t_1$. The only move out of $f_1$ is $f_1 \to s_2$, and the rest of the path is a path from $s_2$ to $f_2$ that visits $f_2$ only at its end, that is, a clean path $Q_2$ of $t_2$. It cannot return to $V(t_1)$, since by Lemma 1(c) $s_1$ has no incoming moves and the other states of $V(t_1)$ are entered only from $V(t_1)$. So $P$ reads $xy$ with $x \in L(t_1)$ and $y \in L(t_2)$. Conversely, two such clean paths joined by $f_1 \to s_2$ form a clean path of $t$.
4. *Star $t = t_1^*$.* A clean path either is the single move $s \to f$, which reads $\varepsilon \in L(t)$, or starts with $s \to s_1$. In the second case, cut the path at each visit to $f_1$. Each piece from $s_1$ to the next visit of $f_1$ is a clean path of $t_1$ by the argument of case 2, and after each visit the path takes $f_1 \to s_1$ and starts a new piece, or takes $f_1 \to f$ and ends. So $P$ reads $x_1 x_2 \cdots x_k$ with $k \ge 1$ and each $x_i \in L(t_1)$, which is in $L(t_1)^k \subseteq L(t)$. Conversely, $\varepsilon$ is read by $s \to f$, and for $k \ge 1$ and $x_i \in L(t_1)$, the clean paths of $t_1$ for the $x_i$, joined by $f_1 \to s_1$ and framed by $s \to s_1$ and $f_1 \to f$, form a clean path of $t$. $\square$

**Theorem.** $L(N) = L(r)$.

*Proof.* Line L16 returns the fragment of the root $t = r$, with start $s_r$ and the one accepting state $f_r$, which has no outgoing move by Lemma 1(b). A string $w$ is in $L(N)$ if and only if some path from $s_r$ to $f_r$ reads $w$. Such a path ends at its first visit to $f_r$, because $f_r$ has no outgoing move, so it is a clean path of $r$. By Lemma 4 this holds if and only if $w \in L(r)$. $\square$

**Size.** Lines L4, L9 and L14 create two states for each leaf, union and star, and line L12 creates none, so $|Q| \le 2m$. A leaf adds at most one move, a union four, a concatenation one and a star four, so there are at most $4m$ moves. An entry created at line L9 or L14 gets exactly two moves at its creation; an entry created at line L4 gets at most one. An exit gets outgoing moves only when a fragment with that exit is popped. After the pop, the new fragment's exit is a new state (lines L10 and L15) or $f_2$ (line L12, when the popped exit was $f_1$), so the popped exit is never again the exit of a fragment on the stack. Hence each exit gets moves once, one or two of them, and every state has at most two outgoing moves. $\blacksquare$
