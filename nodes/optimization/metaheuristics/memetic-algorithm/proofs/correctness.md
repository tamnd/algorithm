---
title: The memetic algorithm keeps only 2-opt optimal tours, its sorted lengths never increase and its number of distinct tours never falls, and a variant with random restarts reaches the optimum with probability 1
proves: [correctness]
status: full
---

We use the pseudocode of the page on a symmetric instance with $n \ge 4$ cities. A tour is stored as a sequence of the $n$ cities, and two sequences are the same tour if one is a rotation or a reversal of the other. Let $\varepsilon \ge 0$ be the tolerance of 2-opt: a move is applied only if it changes the length by less than $-\varepsilon$. Let $P_s$ be the population after step $s$, with $P_0$ from line L1.

**Claim 1 (valid tours).** Every element of every $P_s$ is a permutation of the cities.

*Proof.* Let $a$ and $b$ be permutations and $i \le j$. OX copies the $j - i + 1$ cities $a_i, \ldots, a_j$, which are distinct. The other cities, in the order of $b$, are exactly the cities not among them, $n - (j - i + 1)$ in number, and they fill the $n - (j - i + 1)$ other positions once each. So the child is a permutation. A swap of two positions and the reversal of a segment, which is a 2-opt move, only reorder the entries. Line L1 starts from random permutations. By induction on $s$, every tour is a permutation. $\square$

**Claim 2 (2-opt stops, and its result is 2-opt optimal).** For every start tour, 2-opt stops after finitely many moves, and the result has no move that changes its length by less than $-\varepsilon$.

*Proof.* Each applied move lowers the length strictly. So no tour occurs twice during one run of 2-opt, and since there are at most $n!$ sequences, at most $n! - 1$ moves are applied. The loop stops only after a full pass in which no move qualifies. That is the definition of 2-opt optimal with tolerance $\varepsilon$. $\square$

**Claim 3 (local optimality).** Every tour in every $P_s$ is 2-opt optimal.

*Proof.* Every tour of $P_0$ is the output of 2-opt. In step $s$, the only tour that can enter is the output $c$ of line L6, which is 2-opt optimal by Claim 2. $\square$

**Claim 4 (monotone population).** Let $\ell_{(1)}(s) \le \cdots \le \ell_{(N)}(s)$ be the sorted lengths of the tours in $P_s$. Then $\ell_{(r)}(s) \le \ell_{(r)}(s - 1)$ for every $r$ and $s$. In particular the best length never increases, and line L9 returns a tour whose length is the smallest seen in any population.

*Proof.* If line L8 does nothing, $P_s = P_{s-1}$. Otherwise it removes one tour of length $\ell_{(N)}(s - 1)$ and adds a tour of length $L(c) < \ell_{(N)}(s - 1)$. Let $A$ be the multiset of lengths after the removal, and write its sorted values as $\ell_{(1)}(s-1), \ldots, \ell_{(N-1)}(s-1)$. Inserting $L(c)$ into $A$ gives a sorted list whose $r$-th value is at most $\ell_{(r)}(s - 1)$: for $r \le N - 1$, the $r$-th smallest of $A \cup \{L(c)\}$ is at most the $r$-th smallest of $A$, and for $r = N$, the largest of $A \cup \{L(c)\}$ is $\max(\ell_{(N-1)}(s - 1), L(c)) \le \ell_{(N)}(s - 1)$. $\square$

**Claim 5 (diversity).** The number of distinct tours in $P_s$ never decreases.

*Proof.* If line L8 replaces $w$ by $c$, then $c$ is not in $P_{s-1}$. If $w$ occurs more than once in $P_{s-1}$, the set of distinct tours gains $c$ and loses nothing, so the count grows by one. If $w$ occurs once, the set loses $w$ and gains $c$, so the count stays the same. $\square$

**Claim 6 (convergence of a variant).** Change line L5 so that, with probability $p_r > 0$ and independently of the past, $c$ is replaced by a uniform random permutation. Then the probability that no tour of $P_s$ has length $L^*$ is at most $(1 - 2p_r/(n-1)!)^s$, and it tends to 0.

*Proof.* Fix an optimal tour $t^*$. It is written by $2n$ sequences: $n$ rotations in each of 2 directions. So a uniform random permutation is $t^*$ with probability $2n/n! = 2/(n-1)!$, and the step does this with probability at least $2 p_r / (n-1)!$, whatever the past. No 2-opt move shortens $t^*$, since $t^*$ is optimal, so line L6 returns $t^*$. Now suppose that $P_{s-1}$ has no tour of length $L^*$. Then $t^*$ is not in $P_{s-1}$, and $L(t^*) = L^* < L(w)$, so line L8 adds it. By Claim 4, once a tour of length $L^*$ is in $P$, the best length stays $L^*$. Let $B_s$ be the event that $P_0, \ldots, P_s$ have no tour of length $L^*$. Then $P(B_s \mid B_{s-1}) \le 1 - 2p_r/(n-1)!$, and the chain rule gives the bound. $\square$

**Remark.** Without the change of Claim 6, the algorithm of the page can fail to reach the optimum for any number of steps. For example, if all $N$ tours of $P_0$ are the same tour $t$, then OX of two copies of $t$ gives $t$ again, so every child is $t$ or $t$ with two cities swapped, followed by 2-opt. If no such child is shorter than $t$, the population never changes. The bound of Claim 6 is useless as a time bound for all but tiny $n$. $\blacksquare$
