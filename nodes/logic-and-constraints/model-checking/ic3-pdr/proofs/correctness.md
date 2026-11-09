---
title: IC3 keeps its frame invariants, is sound, and terminates on finite systems
proves: [correctness]
status: full
---

We use the notation of the page. The state set $S$ is finite, $|S| \le 2^n$. We identify a formula over the state variables with the set of states that satisfy it. For $i \ge 1$, $F_i$ is a set of clauses, and as a state set it is the set of states that satisfy all of them. A cube $t$ is identified with the set of states that satisfy it. We write $\mathrm{post}(X)$ for the set of successors of the states in $X$, so $X \wedge T \Rightarrow Y'$ means $\mathrm{post}(X) \subseteq Y$.

The frame invariants, for the current value of $k$, are:

- (A) $I \subseteq F_i$ for $1 \le i \le k$;
- (B) $F_{i+1} \subseteq F_i$ as clause sets for $1 \le i < k$, so $F_i \subseteq F_{i+1}$ as state sets;
- (C) $\mathrm{post}(F_i) \subseteq F_{i+1}$ for $0 \le i < k$;
- (D) $F_i \subseteq P$ for $0 \le i < k$.

**Lemma 1.** After line L2 and after each later change of the frames, (A) to (D) hold.

*Proof.* After line L2, $k = 1$ and $F_1$ has no clauses. (A) and (C) hold since $F_1 = S$, (B) is empty, and (D) says $I \subseteq P$, which line L1 checked. There are three kinds of change.

*Line L16.* The clause $\neg g$ is added to $F_1, \ldots, F_i$, where $1 \le i \le k$, $g \subseteq t$ is a cube, $g \cap I = \emptyset$, and $\mathrm{post}(F_{i-1} \setminus g) \cap g = \emptyset$. For $i = 1$ this is the query of line L14 with $F_0 = I$, or the test in GENERALIZE. (A) holds, as $I \subseteq \neg g$. (B) holds, as the clause goes into a prefix $F_1, \ldots, F_i$ of the frames. (D) holds, as frames only shrink. For (C), only the frames $F_{j+1}$ with $j + 1 \le i$ get the new clause, so we must show $\mathrm{post}(F_j) \cap g = \emptyset$ for $0 \le j \le i - 1$, with $F_j$ the new frame. For $j = 0$: $I \subseteq F_{i-1}$ by (A) (or $F_0 = I$ when $i = 1$), and $I \cap g = \emptyset$, so $I \subseteq F_{i-1} \setminus g$. For $1 \le j \le i - 1$: the new $F_j$ is the old $F_j$ minus $g$, and the old $F_j \subseteq F_{i-1}$ by (B), so the new $F_j \subseteq F_{i-1} \setminus g$. In both cases $\mathrm{post}(F_j) \cap g \subseteq \mathrm{post}(F_{i-1} \setminus g) \cap g = \emptyset$. The other parts of (C) only gain constraints on the left side, which keeps them true.

*Line L9.* The clause $c \in F_i \setminus F_{i+1}$ is added to $F_{i+1}$ only if $\mathrm{post}(F_i) \subseteq c$. (A) holds, since $c \in F_i$ and $I \subseteq F_i$. (B) holds, since $c \in F_i$. (C) for index $i$ is exactly the test, and the other indices only gain constraints on the left. (D) holds as frames only shrink.

*Line L6.* The loop of line L4 ended, so $F_k \cap \neg P = \emptyset$, which is (D) for the old $k$. The new frame $F_{k+1} = S$ makes (C) for index $k$ trivial, and (A) and (B) for the new frame hold because it has no clauses. ∎

**Lemma 2 (BLOCK).** Each call BLOCK$(s, k)$ with $s \in F_k \setminus P$ and $s \notin I$ terminates. If it returns a path, the path is a counterexample. If it returns NONE, then afterwards $s \notin F_k$.

*Proof.* We show three facts about the stack $Q$, which hold whenever line L12 is reached: (i) the levels on $Q$, from bottom to top, are $k, k - 1, \ldots$, decreasing by one; (ii) the bottom state is $s$, and each state above it is a predecessor of the state below it under a recorded input; (iii) no state on $Q$ is in $I$, and each level is at least 1. They hold at the start. Line L19 pushes $u$ at level $i - 1$; line L18 has ruled out $i - 1 = 0$ and $u \in I$, and $u$ is a predecessor of $t$ by the model of line L14. Pops keep the facts. So when line L18 returns, the path $u, t, \ldots, s$ follows $T$, starts in $I$ (if $i - 1 = 0$, then $u \in F_0 = I$), and ends in $s \notin P$: a counterexample.

Now we show by induction on $j \ge 1$: once an obligation $(t, j)$ is on top of $Q$, the run either returns a counterexample before $(t, j)$ is popped, or pops $(t, j)$ after finitely many steps, and then $t \notin F_j$. Each visit of $(t, j)$ at line L14 either succeeds or finds a predecessor $u \in F_{j-1} \setminus t$. In the first case, line L16 adds $\neg g$ with $g \subseteq t$ to $F_j$, so the single state $t$ is not in $F_j$, and $(t, j)$ is popped. In the second case $j - 1 \ge 1$ (else line L18 returns), and $(u, j - 1)$ is pushed. By the induction hypothesis it is popped after finitely many steps with $u \notin F_{j-1}$, or a counterexample is returned. Frames only shrink, so each predecessor found for $(t, j)$ is a different state of the original $F_{j-1}$. Hence $(t, j)$ sees at most $|S|$ predecessors before the query of line L14 succeeds. For $j = 1$, the second case returns at once at line L18. Applying the claim to $(s, k)$ proves the lemma. ∎

In each call from line L5, $s \in F_k \setminus P$ by the query of line L4, and $s \notin I$ because $I \subseteq P$ by line L1. So Lemma 2 applies.

**Theorem 1 (soundness of HOLDS).** If line L10 returns HOLDS with $F_i$, then $F_i$ is an inductive invariant that implies $P$, so $P$ holds in every reachable state.

*Proof.* Here $1 \le i \le k - 1$ and $F_i = F_{i+1}$ as clause sets, so also as state sets. By (A), $I \subseteq F_i$. By (C), $\mathrm{post}(F_i) \subseteq F_{i+1} = F_i$. By (D), $F_i \subseteq P$, since $i < k$. By induction on the length of a path, every reachable state is in $F_i$, hence in $P$. ∎

**Theorem 2 (soundness of FAILS).** If IC3 returns FAILS, then $P$ is not an invariant.

*Proof.* At line L1 the initial state itself violates $P$. At line L5 the path is a counterexample by Lemma 2. ∎

**Lemma 3.** When line L10 is reached for index $i$ and $F_i \ne F_{i+1}$ as clause sets, then $F_i \subsetneq F_{i+1}$ as state sets.

*Proof.* By (B), $F_{i+1} \subseteq F_i$ as clause sets, so there is a clause $c \in F_i \setminus F_{i+1}$. Line L8 tried to push $c$ in this round and failed, so there was a state $a \in F_i$ with a successor $b \notin c$. Line L10 for index $i$ comes right after the loop of line L8 for index $i$, and that loop changes only $F_{i+1}$. So $a$ is still in $F_i$. By (C), $b \in F_{i+1}$, and $b \notin F_i$ because $b$ violates $c \in F_i$. With (B) this gives $F_i \subsetneq F_{i+1}$. ∎

**Theorem 3 (termination).** IC3 terminates. When it reaches line L10 with frame count $k$ and does not return, then $k \le |S|$.

*Proof.* Each run of the loop of line L4 that does not return removes $s$ from $F_k$ by Lemma 2, and $F_k$ only shrinks, so the loop runs at most $|S|$ times. The propagation loop is finite. If propagation finds no equal pair, Lemma 3 gives $F_1 \subsetneq F_2 \subsetneq \cdots \subsetneq F_k$ as state sets. Since $\emptyset \ne I \subseteq F_1$ and $F_k \subseteq S$, we get $k \le |S|$. So $k$ never exceeds $|S| + 1$ at line L3, and the outer loop ends. ∎

**Corollary (completeness).** For each finite system, IC3 returns HOLDS if $P$ is an invariant and FAILS otherwise. This follows from Theorems 1 to 3, since the algorithm stops only at lines L1, L5 and L10.
