---
title: NFA simulation accepts exactly the strings of the NFA and stops in O(l(n + m)) steps
proves: [correctness, termination]
status: full
---

Let $N = (Q, \Sigma, \delta, q_0, F)$ be the input, with $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$, and let $w = a_1 \cdots a_\ell$. For $S \subseteq Q$, let $E(S)$ be the set of states $r$ such that there is a path $p_0, p_1, \ldots, p_k$ with $k \ge 0$, $p_0 \in S$, $p_k = r$ and $p_j \in \delta(p_{j-1}, \varepsilon)$ for $1 \le j \le k$.

A *run* of $N$ on $v = b_1 \cdots b_t$ is a sequence of moves that starts in $q_0$ and whose labels, in order, are $b_1, \ldots, b_t$ with any number of $\varepsilon$ labels before, between and after them. Let $R(v)$ be the set of the last states of the runs on $v$. By definition, $v \in L(N)$ if and only if $R(v) \cap F \ne \emptyset$.

**Lemma 1 (CLOSE).** On input $S$, CLOSE stops after at most $|Q|$ pops and returns $E(S)$.

*Proof.* A state is pushed on $K$ only at the moment it is added to $C$, at line L9 or line L12, and states are never removed from $C$. So each state is pushed at most once, there are at most $|Q|$ pops, and the loop stops.

$C \subseteq E(S)$: the claim holds after line L9, since $S \subseteq E(S)$ with paths of length 0. Line L12 adds $r$ only when $r \in \delta(q, \varepsilon)$ for some $q \in C$; a path from $S$ to $q$ followed by the move to $r$ is a path from $S$ to $r$.

$E(S) \subseteq C$: each state that enters $C$ also enters $K$, and the loop stops only when $K$ is empty, so each state of the final $C$ was popped at line L11, and line L12 then put all its $\varepsilon$-successors in $C$. So the final $C$ contains $S$ and is closed under $\varepsilon$-moves. Take $r \in E(S)$ with a path $p_0, \ldots, p_k = r$. By induction on $j$, $p_j \in C$: $p_0 \in S \subseteq C$, and $p_{j} \in \delta(p_{j-1}, \varepsilon)$ with $p_{j-1} \in C$ gives $p_j \in C$. $\square$

**Lemma 2 (one step).** For each $v \in \Sigma^*$ and $a \in \Sigma$, $R(va) = E\big(\bigcup_{q \in R(v)} \delta(q, a)\big)$.

*Proof.* ($\supseteq$) Let $r$ be in the right side. Then there are $q \in R(v)$, $p \in \delta(q, a)$ and a path of $\varepsilon$-moves from $p$ to $r$. A run on $v$ that ends in $q$, followed by the move $q \to p$ on $a$ and the path to $r$, is a run on $va$ that ends in $r$.

($\subseteq$) Let $r \in R(va)$, with a run on $va$ that ends in $r$. The run reads $a$ in exactly one move with a label in $\Sigma$ after it has read $v$; let this move go from $q$ to $p$, so $p \in \delta(q, a)$. The moves before it form a run on $v$ that ends in $q$, so $q \in R(v)$. The moves after it are $\varepsilon$-moves from $p$ to $r$, so $r \in E(\{p\})$. Hence $r$ is in the right side. $\square$

**Lemma 3 (invariant).** If the algorithm reaches the test of line L2 after $i$ passes of the loop, then $S = R(a_1 \cdots a_i)$.

*Proof.* By induction on $i$. For $i = 0$, line L1 sets $S = E(\{q_0\})$ by Lemma 1, and $R(\varepsilon) = E(\{q_0\})$, since a run on $\varepsilon$ uses only $\varepsilon$-moves. For the step, assume $S = R(v)$ with $v = a_1 \cdots a_{i-1}$ before pass $i$. Lines L3 to L5 make $T = \bigcup_{q \in S} \delta(q, a_i)$, and line L6 sets $S = E(T)$ by Lemma 1. By Lemma 2 this is $R(v a_i)$. If line L7 returns, the next test of line L2 is never reached, and the claim holds vacuously. $\square$

**Theorem.** NFA-SIMULATION$(N, w)$ stops and returns true if and only if $w \in L(N)$.

*Proof.* The loop at line L2 makes at most $\ell$ passes, and each call of CLOSE stops by Lemma 1, so the algorithm stops.

If it returns false at line L7 in pass $i$, then $R(a_1 \cdots a_i) = \emptyset$ by Lemma 3 and the computation of pass $i$. Each run on $w$ begins with a run on $a_1 \cdots a_i$: the part of it up to and including the move that reads $a_i$ is a run on $a_1 \cdots a_i$. That prefix would end in a state of $R(a_1 \cdots a_i)$, so there is no run on $w$, and $w \notin L(N)$.

Otherwise, after all $\ell$ passes, $S = R(w)$ by Lemma 3, and line L8 returns true if and only if $R(w) \cap F \ne \emptyset$, that is, if and only if $w \in L(N)$. $\blacksquare$

**Running time.** In one pass, lines L4 and L5 read each $a_i$-move of each state of $S$ once, at most $m$ moves, and $S$ has at most $n$ states. By Lemma 1, CLOSE pops at most $n$ states, and it reads the $\varepsilon$-moves of each popped state once, at most $m$ moves. With a boolean array for membership, each "add" and each test is $O(1)$. So a pass costs $O(n + m)$, and the $\ell$ passes cost $O(\ell (n + m))$. The space is the two sets, the stack and the array: $O(n)$.
