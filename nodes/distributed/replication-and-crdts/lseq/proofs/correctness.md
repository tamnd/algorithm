---
title: LSEQ allocation returns a fresh position between its arguments, and replicas converge
proves: [correctness, invariant, termination]
status: full
---

**Setting.** As in the Logoot proof, a position is a finite list of triples $(d, s, c)$, compared in lexicographic order with a proper prefix first, and $\top$ is above every position. Here the digit at level $i$ lies in $[0, \mathrm{base}(i))$ with $\mathrm{base}(i) = 2^{4 + i + 1} \ge 2$. A position is *good* if it is not empty and its last digit is at least 1. Sites have distinct ids and increase their clock before each ALLOC. Operations are delivered once at every replica in a causal order.

**Claim 1 (the digit).** At a level $i$ where line L3 finds room, the digit $d$ of line L6 or line L7 satisfies $pd < d < qd$, $d \ge 1$ and $d < \mathrm{base}(i)$.

*Proof.* Line L4 gives $1 \le \mathit{step} \le qd - pd - 1$, and let $1 \le r \le \mathit{step}$. For boundary+, $d = pd + r$, so $pd < d \le qd - 1$. For boundary−, $d = qd - r$, so $qd > d \ge pd + 1$. In both cases $d \ge pd + 1 \ge 1$. Also $qd \le \mathrm{base}(i)$: either $qd = \mathrm{base}(i)$ by line L2, or $qd$ is the digit of $q[i]$, which is below $\mathrm{base}(i)$. So $d < \mathrm{base}(i)$. $\square$

**Claim 2 (ALLOC).** Let $p$ be the empty list or a good position, let $q$ be $\top$ or a good position, and let $p < q$. Then ALLOC$(p, q)$ stops and returns a good position $x$ with $p < x < q$, $|x| \le \max(|p|, |q|) + 1$, every digit at level $i$ below $\mathrm{base}(i)$, and the site and clock of the caller in its last triple.

*Proof.* The Logoot proof of the same claim uses only these facts about the digit chosen at the level with room: $pd < d < qd$, $d \ge 1$, and $d$ in range. Claim 1 gives them for both strategies. The rest of that proof is about lines L1 to L3 and the walk of line L8, which are the same here, except that the base of line L2 depends on the level. The proof uses only $\mathrm{base}(i) \ge 2$ at each level, which holds. So the invariants (a) to (c) of the Logoot proof hold at each round, lines L5 to L7 return a position strictly between $p$ and $q$, and the walk stops by round $\max(|p|, |q|)$. Copied triples come from $p$ or $q$, whose digits are in range at their levels, and a triple added by the walk has digit 0. $\square$

**Claim 3 (unique positions).** Two different inserts make different positions.

*Proof.* By Claim 2 the last triple holds the site and the fresh clock value of the insert. Site ids are distinct and clocks never repeat. $\square$

**Theorem 1 (convergence).** Two replicas that have run the same set of operations show the same list.

*Proof.* As in the Logoot proof: by Claim 3 an insert's position belongs to it alone, a delete comes after its insert in causal order, so a replica that has run a causally closed set $E$ holds exactly the pairs inserted in $E$ and not deleted in $E$. READ sorts them by position. The strategy map of a replica affects only which positions it makes, not where a received position goes. $\square$

**Theorem 2 (local intent and stable order).** A local INSERT$(i, v)$ makes $v$ the $i$-th element at its source, a local DELETE$(i)$ removes the $i$-th element, and the relative order of two elements never changes.

*Proof.* Every stored position is good, by Claim 2. The insert allocates between the positions of elements $i - 1$ and $i$, or the start and $\top$, so by Claim 2 its position lies between them. A delete removes the pair at index $i$. Positions never change. $\square$

**Termination.** By Claim 2, ALLOC runs at most $\max(|p|, |q|) + 1$ rounds. $\blacksquare$
