---
title: The Hopcroft-Karp algorithm decides DFA equivalence
proves: [correctness, termination, complexity]
status: full
---

Let $M_i = (Q_i, \Sigma, \delta_i, q_i, F_i)$ for $i = 1, 2$ be complete DFAs with disjoint state sets, $n = |Q_1| + |Q_2|$ and $\sigma = |\Sigma|$. Let $Q = Q_1 \cup Q_2$, $F = F_1 \cup F_2$, and let $\delta : Q \times \Sigma \to Q$ be $\delta_1$ on $Q_1$ and $\delta_2$ on $Q_2$. Then $\delta^*$ on $Q_1$ is $\delta_1^*$ and on $Q_2$ is $\delta_2^*$. For $x \in Q$, "x accepts" means $x \in F$.

Call the pairs pushed by lines L2 and L9 the *pushed pairs*. Each has the form $(p, r)$ with $p \in Q_1$, $r \in Q_2$, and a string $w$.

## Part 1: termination and cost

Each call of UNION in lines L2 and L9 joins two different sets: in line L2 the sets of $q_1$ and $q_2$ are different singletons, and in line L9 line L8 has just checked that the sets differ. So each call reduces the number of sets by one. There are $n$ sets at the start, so there are at most $n - 1$ calls. Each pushed pair follows one call, so at most $n - 1$ pairs are pushed, and the loop of line L3, which pops one pair per pass, runs at most $n - 1$ times. Each pass makes at most $2\sigma$ FIND calls in line L8. With union by size and path halving, a sequence of $m$ operations on $n$ elements takes $O(m\,\alpha(n))$ time, so the total time is $O(\sigma n\,\alpha(n))$, and the space is $O(n)$.

## Part 2: a reported string is a counterexample

**Invariant (I1).** Every pushed pair $(p, r)$ with string $w$ has $p = \delta_1^*(q_1, w)$ and $r = \delta_2^*(q_2, w)$.

*Proof.* Line L2 pushes $(q_1, q_2)$ with $\varepsilon$. Line L9 pushes $(\delta_1(p, a), \delta_2(r, a))$ with $wa$, where $(p, r)$ with $w$ was pushed before; by (I1) for $(p, r)$ and the definition of $\delta^*$, $\delta_1(p, a) = \delta_1^*(q_1, wa)$ and $\delta_2(r, a) = \delta_2^*(q_2, wa)$. $\square$

If line L5 returns $w$ for the pair $(p, r)$, then exactly one of $p \in F_1$ and $r \in F_2$ holds, so by (I1) exactly one of $w \in L(M_1)$ and $w \in L(M_2)$ holds. The string has length at most $n - 2$, because each pushed pair's string is one symbol longer than the string of the pair it came from, and the at most $n - 1$ pushed pairs form a tree rooted at the first pair.

## Part 3: if no string is reported, the DFAs are equivalent

Suppose line L10 is reached, and let $\equiv$ be the final partition of $Q$, viewed as an equivalence relation. Let $E$ be the set of the pushed pairs, as unordered pairs of states.

**Claim 1.** $\equiv$ is the smallest equivalence relation that contains $E$.

*Proof.* Each UNION joins the sets of the two states of one pushed pair, and the partition changes only by UNION. By induction on the number of UNION calls, the partition is always the set of connected components of the graph on $Q$ with the edges $E$ pushed so far. The connected components of a graph are the classes of the smallest equivalence relation that contains its edges. $\square$

**Claim 2.** If $x \equiv y$, then $x$ accepts if and only if $y$ accepts.

*Proof.* Every pushed pair was popped, since the stack is empty at line L10, and it passed line L5, so its two states agree on acceptance. By Claim 1, $x \equiv y$ means that a path $x = z_0, z_1, \ldots, z_k = y$ exists with each $\{z_{j-1}, z_j\} \in E$. Acceptance is the same along each edge, so it is the same at $x$ and $y$. $\square$

**Claim 3.** If $x \equiv y$, then $\delta(x, a) \equiv \delta(y, a)$ for every $a \in \Sigma$.

*Proof.* First let $\{x, y\} = \{p, r\}$ be a pushed pair. When it was popped, line L8 compared the sets of $\delta(p, a)$ and $\delta(r, a)$. If they were different, line L9 merged them; if not, they were already in one set. Sets only grow by merging, so at the end $\delta(p, a) \equiv \delta(r, a)$. In general, take the path $z_0, \ldots, z_k$ of Claim 1 from $x$ to $y$. Each edge gives $\delta(z_{j-1}, a) \equiv \delta(z_j, a)$, and transitivity gives $\delta(x, a) \equiv \delta(y, a)$. $\square$

**Claim 4.** For every $w \in \Sigma^*$, $\delta_1^*(q_1, w) \equiv \delta_2^*(q_2, w)$.

*Proof.* By induction on $|w|$. For $w = \varepsilon$, $q_1 \equiv q_2$ by line L2. If $\delta_1^*(q_1, w) \equiv \delta_2^*(q_2, w)$, then Claim 3 with the symbol $a$ gives $\delta_1^*(q_1, wa) \equiv \delta_2^*(q_2, wa)$. $\square$

By Claims 4 and 2, for every $w$, $\delta_1^*(q_1, w) \in F_1$ if and only if $\delta_2^*(q_2, w) \in F_2$, that is, $L(M_1) = L(M_2)$.

## Conclusion

By Part 1 the algorithm stops after at most $n - 1$ passes in $O(\sigma n\,\alpha(n))$ time. If it returns "not equivalent" with $w$, Part 2 shows that $w$ is in exactly one of the two languages, so the DFAs are not equivalent. If it returns "equivalent", Part 3 shows that $L(M_1) = L(M_2)$. Since one of the two answers is always returned, the algorithm decides equivalence. $\blacksquare$
