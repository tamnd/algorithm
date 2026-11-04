---
title: The banker's queue keeps its invariant and implements a persistent queue
proves: [correctness]
status: full
---

We use the pseudocode of the page. A stream denotes the finite sequence of the items of its cells; forcing a suspension does not change what it denotes, only whether its value is stored. For a list $R$, $\text{rev}(R)$ is its reverse, and $\cdot$ is concatenation of sequences. For a queue $Q = (\ell_f, F, \ell_r, R)$ let

$$ \text{seq}(Q) = F \cdot \text{rev}(R). $$

A tuple is *valid* if $\ell_f = |F|$, $\ell_r = |R|$ and $\ell_r \le \ell_f$.

**Lemma 1 (CHECK).** Let $(\ell_f, F, \ell_r, R)$ satisfy $\ell_f = |F|$, $\ell_r = |R|$ and $\ell_r \le \ell_f + 1$. Then CHECK returns a valid tuple $Q'$ with $\text{seq}(Q') = F \cdot \text{rev}(R)$.

*Proof.* If $\ell_r \le \ell_f$, line L8 returns the same tuple, which is then valid, and the sequence is the same. Otherwise $\ell_r = \ell_f + 1$, and line L9 returns $(\ell_f + \ell_r, F ⧺ \text{REVERSE}(R), 0, \langle\rangle)$. The lazy concatenation $F ⧺ G$ denotes $F \cdot G$ (by induction on $|F|$: if $F$ is empty its value is the value of $G$, and otherwise its first cell holds the first item of $F$ and its rest is the concatenation of the rest of $F$ with $G$). REVERSE$(R)$ denotes $\text{rev}(R)$. So the new front denotes $F \cdot \text{rev}(R)$, its length is $|F| + |R| = \ell_f + \ell_r$, the new rear is empty with length 0, and $0 \le \ell_f + \ell_r$. The tuple is valid, and its sequence is $F \cdot \text{rev}(R) \cdot \text{rev}(\langle\rangle) = F \cdot \text{rev}(R)$. $\square$

**Lemma 2 (operations).** Let $Q$ be valid with $\text{seq}(Q) = \langle x_1, \ldots, x_n \rangle$.

1. EMPTY returns a valid tuple with sequence $\langle\rangle$.
2. SNOC$(Q, x)$ returns a valid tuple with sequence $\langle x_1, \ldots, x_n, x \rangle$.
3. If $n = 0$, HEAD and TAIL report an error. If $n \ge 1$, HEAD$(Q)$ returns $x_1$, and TAIL$(Q)$ returns a valid tuple with sequence $\langle x_2, \ldots, x_n \rangle$.

*Proof.* (1) Line L1 returns $(0, \langle\rangle, 0, \langle\rangle)$, which is valid with the empty sequence.

(2) Line L3 calls CHECK on $(\ell_f, F, \ell_r + 1, \text{cons}(x, R))$. Here $|\text{cons}(x, R)| = \ell_r + 1$ and $\ell_r + 1 \le \ell_f + 1$, so Lemma 1 applies, and the result is valid with sequence $F \cdot \text{rev}(\text{cons}(x, R)) = F \cdot \text{rev}(R) \cdot \langle x \rangle = \langle x_1, \ldots, x_n, x \rangle$.

(3) Since $Q$ is valid, $n = \ell_f + \ell_r \le 2\ell_f$, so $\ell_f = 0$ if and only if $n = 0$. If $n = 0$, lines L4 and L6 report the error. If $n \ge 1$, then $\ell_f \ge 1$, so $F$ is non-empty and its first item is the first item of $F \cdot \text{rev}(R)$, which is $x_1$; line L5 returns it. In line L7 the rest $F'$ of $F$ has $|F'| = \ell_f - 1$ and $F = \langle x_1 \rangle \cdot F'$. The arguments of CHECK satisfy $\ell_r \le \ell_f = (\ell_f - 1) + 1$, so by Lemma 1 the result is valid with sequence $F' \cdot \text{rev}(R) = \langle x_2, \ldots, x_n \rangle$. $\square$

**Lemma 3 (no old version changes).** No operation changes the sequence of a tuple that existed before it.

*Proof.* The operations create new tuples, new list cells (line L3) and new suspensions (line L9). They never assign to a field of an existing tuple, cell or suspension. The only change to existing objects is the memoization of a forced suspension, which stores the value that the suspension denotes and so does not change the sequence of any stream. $\square$

**Theorem.** Every version that a program builds from EMPTY by SNOC and TAIL, applied to any earlier versions in any order, is valid, and HEAD, TAIL and SNOC act on each version as the persistent queue type specifies.

*Proof.* By induction on the number of operations performed. EMPTY gives a valid version by Lemma 2(1). Each later operation takes as argument a version that was valid when it was made, and by Lemma 3 it still has the same fields and sequence, so it is still valid. Lemma 2(2) and 2(3) then give the result of the operation and the validity of the new version. $\blacksquare$
