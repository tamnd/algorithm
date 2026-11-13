---
title: The quantum Gauss sieve returns lattice vectors, ends its reductions, and keeps the list reduced when no search misses
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page. $\Lambda$ is the lattice spanned by the rows of $B$, a vector $w$ reduces $v$ if $2|\langle v, w \rangle| > \|w\|^2$, and $s = \operatorname{sign}\langle v, w \rangle$ is the sign used in the updates $v \leftarrow v - s w$ of line L4 and $w \leftarrow w - s v$ of line L6. SEARCH has $q = \lceil \log_2 |L| \rceil$ index qubits, and the indices $|L|, \dots, 2^q - 1$ are padding that is never marked. We say that a search misses if it returns $\perp$ while some entry of $L$ satisfies its predicate.

The proof shows what holds without any assumption: the output is a nonzero vector of $\Lambda$, every inner loop ends, every partner that SEARCH returns is a true partner, and the list is pairwise reduced when no search misses. It then bounds the cost of SEARCH and the probability of a miss. That the output is a shortest vector of $\Lambda$ is the heuristic claim of the classical sieve, and it is not proved here.

## Lemma 1: all vectors are lattice vectors

Every vector in $L$, in $S$ and in the variable $v$ is in $\Lambda$ at all times.

*Proof.* At line L1, $S$ holds the rows of $B$ and $L$ is empty. Line L3 takes $v$ from $S$ or samples it from $\Lambda$. Lines L4 and L6 replace a vector by the sum or the difference of two vectors of $\Lambda$, which is in $\Lambda$. Lines L6 and L7 only move vectors between $S$, $L$ and $v$. $\square$

## Lemma 2: a reduction makes the vector strictly shorter

If $w$ reduces $v$, then $\|v - s w\| < \|v\|$. If $2|\langle v, w \rangle| > \|v\|^2$, then $\|w - s v\| < \|w\|$.

*Proof.* $\|v - s w\|^2 = \|v\|^2 - 2 s \langle v, w \rangle + \|w\|^2 = \|v\|^2 - 2|\langle v, w \rangle| + \|w\|^2 < \|v\|^2$, by the condition $2|\langle v, w \rangle| > \|w\|^2$. The second claim is the first with the roles of $v$ and $w$ exchanged. $\square$

## Lemma 3: SEARCH is sound and ends

SEARCH returns $\perp$ or an index $i < |L|$ with $f(L[i])$ true, and it ends after fewer than $(C + 1)\sqrt{2^q} + 1$ queries.

*Proof.* Line L12 returns $i$ only after it checks $i < |L|$ and $f(L[i])$ classically, so a returned index is never wrong, whatever the quantum step measured. Each round adds $j + 1 \ge 1$ to the count of spent queries, with $j + 1 \le \lceil m \rceil < \sqrt{2^q} + 1$. Before the last round the count is below $C\sqrt{2^q}$, because line L10 lets the round start, so the total is below $C\sqrt{2^q} + \sqrt{2^q} + 1$. $\square$

## Lemma 4: the inner loops end

The loops of lines L4 and L6 end.

*Proof.* By Lemma 3 each call of SEARCH ends. In line L4, each round in which SEARCH returns an index replaces $v$ by a strictly shorter vector (Lemma 2), and $\|v\|^2$ is a nonnegative integer because $\Lambda \subseteq \mathbb{Z}^n$. So line L4 has at most $\|v\|^2$ such rounds before SEARCH returns $\perp$. In line L6, each round removes one entry from $L$, so there are at most $|L|$ rounds. $\square$

## Lemma 5: the list is pairwise reduced when no search misses

Suppose that no search misses up to some moment. Then at that moment every pair $u \ne w$ of entries of $L$ satisfies $2|\langle u, w \rangle| \le \min(\|u\|^2, \|w\|^2)$.

*Proof.* By induction on the number of executions of line L7, the only line that adds to $L$. The claim holds for the empty list, and line L6 only removes entries, which keeps it. When line L7 appends $v$, the loop of line L4 has just ended with $\perp$. With no miss, this means that no entry $w$ of $L$ satisfies $2|\langle v, w \rangle| > \|w\|^2$. The loop of line L6 has also ended with $\perp$, so after the removals no entry $w$ satisfies $2|\langle v, w \rangle| > \|v\|^2$. The vector $v$ is unchanged between these two tests, and $L$ only lost entries, so both inequalities hold for $v$ and every remaining $w$. With the induction hypothesis for the old pairs, the claim holds after line L7. $\square$

## Lemma 6: the success probability of one round

If $t \ge 1$ of the $2^q$ indices are marked and $\sin^2\theta = t / 2^q$ with $0 < \theta \le \pi/2$, then $j$ Grover iterations followed by a measurement give a marked index with probability $\sin^2((2j + 1)\theta)$, and the measured index is uniform among the marked indices given that it is marked.

*Proof.* Let $|g\rangle$ and $|b\rangle$ be the uniform superpositions over the marked and the unmarked indices. The start state is $|s\rangle = \sin\theta\, |g\rangle + \cos\theta\, |b\rangle$. The oracle is the reflection $I - 2|g\rangle\langle g|$, and the diffusion is the reflection $2|s\rangle\langle s| - I$. Both map the plane spanned by $|g\rangle$ and $|b\rangle$ to itself, and their product is a rotation of that plane by the angle $2\theta$, since the angle between $|s\rangle$ and $|b\rangle$ is $\theta$. After $j$ iterations the state is $\sin((2j + 1)\theta)\, |g\rangle + \cos((2j + 1)\theta)\, |b\rangle$. Measurement gives a marked index with probability $\sin^2((2j + 1)\theta)$, and since $|g\rangle$ has equal amplitudes on the marked indices, each of them is equally likely. $\square$

## Lemma 7: the cost of SEARCH and the probability of a miss

Let $|L| = N$ and suppose that $t \ge 1$ entries satisfy the predicate. Boyer, Brassard, Høyer and Tapp prove that, without the budget of line L10, the expected number of queries until line L12 returns is at most $K\sqrt{2^q / t}$ for a constant $K$ (their analysis covers $t \le \tfrac34 2^q$; for larger $t$ a round with $j = 0$ succeeds with probability above $3/4$). Then:

1. The expected number of queries of SEARCH is $O(\sqrt{N/t})$, since $2^q < 2N$.
2. The probability of a miss is at most $K/C$.

*Proof.* The first claim follows from the bound, because the budget only cuts runs short. For the second, a miss means that the run without the budget would have spent more than $C\sqrt{2^q}$ queries. By Markov's inequality this has probability at most $K\sqrt{2^q/t} / (C\sqrt{2^q}) \le K/C$. $\square$

## Theorem

QUANTUM-GAUSS-SIEVE returns a nonzero vector of $\Lambda$, every call of SEARCH and every inner loop ends, and if no search misses, the final list is pairwise reduced. Each search costs $O(\sqrt{N/t})$ queries in expectation when $t \ge 1$ partners exist, fewer than $(C + 1)\sqrt{2^q} + 1$ queries in all cases, and misses with probability at most $K/C$.

*Proof.* The output is the shortest entry of $L$, which is nonzero because line L5 never appends the zero vector, and it is in $\Lambda$ by Lemma 1. The inner loops end by Lemma 4, the list property is Lemma 5, and the costs are Lemmas 3 and 7. $\square$

**Remark.** The outer loop of line L2 ends after $c_{\max}$ collisions. That collisions keep coming, and that the shortest entry of the final list is a shortest vector of $\Lambda$, are the heuristic claims of the classical Gauss sieve; the implementation also caps the number of samples so that it always ends. A miss does not break Lemmas 1 to 4. It can only leave a pair in the list that is not reduced, and later searches can still remove it.
