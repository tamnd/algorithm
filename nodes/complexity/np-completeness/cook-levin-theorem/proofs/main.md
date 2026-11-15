---
title: Proof of the Cook-Levin theorem
proves: [statement]
status: full
---

We prove that SAT is NP-complete under polynomial-time many-one (Karp) reductions. Membership is short; hardness is the tableau construction.

## Membership

A certificate for a CNF formula $\varphi$ with $n$ variables is an assignment $a \in \{0,1\}^n$, of length at most $|\varphi|$. The verifier evaluates each clause under $a$ and accepts if every clause has a true literal. On a multitape Turing machine this takes time polynomial in $|\varphi|$ (look up each literal's variable on a second tape). So $\mathrm{SAT} \in \mathsf{NP}$.

## The machine model

Let $L \in \mathsf{NP}$. By the verifier definition of NP there are a polynomial $p$ and a deterministic multitape Turing machine that, given $x$ and $y$ with $|y| = p(|x|)$, decides in polynomial time whether $y$ is a certificate for $x$. Pad the certificates to the exact length $p(n)$ as on the verifier page. By the multitape simulation theorem, a deterministic single-tape machine does the same check with at most a quadratic slowdown. So there are a polynomial $t$ and a deterministic single-tape machine $M = (Q, \Gamma, \delta, q_0, q_{\mathrm{acc}}, q_{\mathrm{rej}})$ with these properties:

1. The tape is infinite to the right, with cells $0, 1, 2, \ldots$. The input alphabet is $\{0, 1, \#\}$, and $\Gamma$ also contains the blank $\sqcup$. A move to the left from cell 0 leaves the head on cell 0.
2. For every $x$ of length $n$: $x \in L$ if and only if there is $y \in \{0,1\}^{p(n)}$ such that $M$, started in $q_0$ with the head on cell 0 and $x \# y$ on cells $0, \ldots, n + p(n)$, enters $q_{\mathrm{acc}}$ within $T = t(n)$ steps.
3. Once $M$ is in $q_{\mathrm{acc}}$ or $q_{\mathrm{rej}}$, it stays in that state, does not move and does not write. We call these the halting states.

We may take $t(n) \ge n + p(n) + 1$, and $T$ can be computed from $n$ in time polynomial in $n$. In $T$ steps the head starts at cell 0 and moves at most one cell per step, so it visits only cells $0, \ldots, T$. Write $\delta(q, a) = (q', b, d)$ with $d \in \{-1, 0, +1\}$ for $q$ not halting, and set $\delta(q, a) = (q, a, 0)$ for the halting states.

## The formula

Fix $x$ with $|x| = n$ and let $T = t(n)$. The formula $\varphi_x$ has these variables, for $0 \le s \le T$, $0 \le i \le T$, $q \in Q$ and $a \in \Gamma$:

- $Q_{s,q}$: at time $s$ the state is $q$;
- $H_{s,i}$: at time $s$ the head is on cell $i$;
- $S_{s,i,a}$: at time $s$ cell $i$ holds $a$.

For a set of variables $X$, let $\mathrm{EO}(X)$ be the clauses "exactly one of $X$ is true": the clause $\bigvee_{v \in X} v$ and the clauses $(\lnot u \lor \lnot v)$ for all pairs $u \ne v$ in $X$. The clauses of $\varphi_x$ are in six groups.

1. Well-formed configurations. For each $s$: $\mathrm{EO}(\{Q_{s,q} : q \in Q\})$, $\mathrm{EO}(\{H_{s,i} : 0 \le i \le T\})$, and for each $i$, $\mathrm{EO}(\{S_{s,i,a} : a \in \Gamma\})$.
2. Start. The unit clauses $Q_{0,q_0}$ and $H_{0,0}$; $S_{0,i,x_{i+1}}$ for $0 \le i < n$; $S_{0,n,\#}$; the clause $(S_{0,i,0} \lor S_{0,i,1})$ for $n < i \le n + p(n)$; and $S_{0,i,\sqcup}$ for $n + p(n) < i \le T$.
3. Moves. For each $s < T$, each cell $i$, each $q \in Q$ and each $a \in \Gamma$, let $\delta(q, a) = (q', b, d)$ and $j = \max(0, i + d)$. Write $P = (\lnot H_{s,i} \lor \lnot Q_{s,q} \lor \lnot S_{s,i,a})$. If $j \le T$, add the three clauses $P \lor Q_{s+1,q'}$, $P \lor S_{s+1,i,b}$ and $P \lor H_{s+1,j}$. If $j = T + 1$, add the clause $P$.
4. Frame. For each $s < T$, each $i$ and each $a$: $(H_{s,i} \lor \lnot S_{s,i,a} \lor S_{s+1,i,a})$.
5. Accept. The unit clause $Q_{T,q_{\mathrm{acc}}}$.

## Cost of the map

There are $(T+1)(|Q| + (T+1)(|\Gamma| + 1))$ variables, which is $O(T^2)$ since $M$ is fixed. Group 1 has $O(T|Q|^2 + T \cdot T^2 + T^2|\Gamma|^2) = O(T^3)$ clauses; the $O(T^3)$ term comes from the pairwise clauses of the head. Group 2 has $O(T)$ clauses, group 3 at most $3(T+1)^2|Q||\Gamma|$, group 4 at most $(T+1)^2|\Gamma|$, and group 5 one. Each clause has at most $T + 1$ literals, and each literal is a variable number of $O(\log T)$ bits. A machine writes the clauses with a few nested loops over $s$, $i$, $q$ and $a$ and a fixed table for $\delta$, so the map $x \mapsto \varphi_x$ runs in time polynomial in $T$, hence in $n$.

## If x is in L, then the formula is satisfiable

Let $y \in \{0,1\}^{p(n)}$ make $M$ accept $x \# y$ within $T$ steps. Run $M$ on $x \# y$ for exactly $T$ steps; by property 3 it stays in $q_{\mathrm{acc}}$ after it gets there. Set $Q_{s,q}$, $H_{s,i}$ and $S_{s,i,a}$ to true exactly when the configuration at time $s$ has state $q$, head on cell $i$, and $a$ on cell $i$. Each configuration has one state, one head position (in $0, \ldots, T$) and one symbol per cell, so group 1 holds. The start configuration holds $x \# y$ followed by blanks, and each cell of $y$ holds 0 or 1, so group 2 holds. In group 3, $P$ is false only when the head is on cell $i$ in state $q$ reading $a$ at time $s$; then the next configuration has state $q'$, symbol $b$ on cell $i$ and head on $j$, and $j \le T$ because the head is on cell at most $s + 1 \le T$ at time $s + 1$. So all clauses of group 3 hold, and the case $j = T + 1$ never has $P$ false. Group 4 holds because a step changes only the cell under the head. Group 5 holds because the state at time $T$ is $q_{\mathrm{acc}}$.

## If the formula is satisfiable, then x is in L

Let $\sigma$ be any satisfying assignment of $\varphi_x$. By group 1, for each $s$ exactly one $Q_{s,q}$, exactly one $H_{s,i}$ and, for each $i$, exactly one $S_{s,i,a}$ is true. So $\sigma$ defines for each $s$ a state $q_s$, a head position $h_s \in \{0, \ldots, T\}$ and a tape content $w_s(0) \cdots w_s(T)$. Let $y = w_0(n+1) \cdots w_0(n + p(n))$. By group 2, each symbol of $y$ is 0 or 1 (the clause $(S_{0,i,0} \lor S_{0,i,1})$ and group 1), and $(q_0, h_0, w_0)$ is the start configuration of $M$ on $x \# y$, restricted to cells $0, \ldots, T$.

Let $C_s$ be the configuration of $M$ on $x \# y$ after $s$ steps. We show by induction on $s$ that $(q_s, h_s, w_s)$ equals $C_s$ on cells $0, \ldots, T$, with the head of $C_s$ inside these cells. The case $s = 0$ is the previous paragraph. Assume it for $s < T$, and let $a = w_s(h_s)$ and $\delta(q_s, a) = (q', b, d)$, with $j = \max(0, h_s + d)$. In the clauses of group 3 for $(s, h_s, q_s, a)$, the part $P$ is false under $\sigma$. If $j = T + 1$, the clause $P$ is false, which is impossible; so $j \le T$. The three clauses then force $q_{s+1} = q'$, $w_{s+1}(h_s) = b$ and $h_{s+1} = j$, by the uniqueness of group 1. For a cell $i \ne h_s$, $H_{s,i}$ is false, so the frame clause for $(s, i, w_s(i))$ forces $S_{s+1,i,w_s(i)}$, and $w_{s+1}(i) = w_s(i)$. These are exactly the changes that one step of $M$ makes, so $(q_{s+1}, h_{s+1}, w_{s+1})$ equals $C_{s+1}$ on cells $0, \ldots, T$, with the head on cell $j \le T$.

For $s = T$, group 5 gives $q_T = q_{\mathrm{acc}}$. So $M$ is in $q_{\mathrm{acc}}$ after $T$ steps on $x \# y$. Since the only way into a halting state is a step of $M$, and halting states do not change, $M$ entered $q_{\mathrm{acc}}$ within $T$ steps. By property 2, $x \in L$.

## Conclusion

The map $x \mapsto \varphi_x$ is computable in polynomial time, and $x \in L \iff \varphi_x \in \mathrm{SAT}$. So $L \le_m^p \mathrm{SAT}$ for every $L \in \mathsf{NP}$, and SAT is in NP. Hence SAT is NP-complete under Karp reductions.

Two further facts follow from the proof. First, $\sigma \mapsto y$ and $y \mapsto \sigma$ are polynomial-time maps between satisfying assignments and certificates, so the reduction is a Levin reduction. Second, $M$ is deterministic, so every certificate $y$ has exactly one run and therefore exactly one satisfying assignment; the number of satisfying assignments of $\varphi_x$ equals the number of certificates of $x$, and the reduction is parsimonious. $\blacksquare$
