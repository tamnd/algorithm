---
title: The chunk pass gives a diff3 parse, and the merge keeps the change of a side that alone changed the file
proves: [correctness]
status: full
---

We use the pseudocode of the page, with indices from 0. The inputs are the base $O$, the versions $A$ and $B$, and two matchings: $M_A$, a set of pairs $(x, y)$ with $O[x] = A[y]$, and $M_B$, a set of pairs $(x, z)$ with $O[x] = B[z]$, each strictly increasing in both coordinates. Since $M_A$ is increasing, a line $x$ of $O$ has at most one partner $a(x)$ in $A$, and in the same way at most one partner $b(x)$ in $B$. A *triple* is $(x, a(x), b(x))$ for a line $x$ of $O$ that is matched in both. A stable chunk with starts $(o, p, q)$ and length $k \ge 1$ is one where $(o + t, p + t, q + t)$ is a triple for each $t < k$.

Khanna, Kunal and Pierce call a list of chunks a *diff3 parse* if the chunks cut $A$, $O$ and $B$ into consecutive pieces, (I) every triple lies in some stable chunk, at the same offset in its three pieces, and (II) each stable chunk is as large as possible.

**Lemma 1 (invariant).** At line L2, the chunks emitted so far cut $A[0 \ldots l_A - 1]$, $O[0 \ldots l_O - 1]$ and $B[0 \ldots l_B - 1]$ into consecutive pieces, and every triple $(x, y, z)$ has one of two forms: $x < l_O$ and the triple lies in an emitted stable chunk, or $x \ge l_O$, $y \ge l_A$ and $z \ge l_B$.

*Proof.* At line L1 nothing is emitted and $l_O = l_A = l_B = 0$, so every triple has the second form. Assume the invariant at line L2.

*A stable chunk.* Lines L2 and L5 find the largest $k = i - 1 \ge 1$ such that $(l_O + t, l_A + t, l_B + t)$ is a triple for each $t < k$, and emit these lines as a stable chunk. A triple with $l_O \le x < l_O + k$ is the one of the line $x$, because each line has at most one partner on each side, so it lies in this chunk. A triple with $x \ge l_O + k$ comes after the triple of $l_O + k - 1$ in both increasing matchings, so $y \ge l_A + k$ and $z \ge l_B + k$. The new values of $l_O$, $l_A$, $l_B$ are these sums, so the invariant holds.

*An unstable chunk.* If $i = 1$, line L3 takes the least line $x \ge l_O$ of $O$ that is matched in both. Its triple has the second form, so $a(x) \ge l_A$ and $b(x) \ge l_B$, and line L4 emits the pieces $A[l_A \ldots a(x) - 1]$, $O[l_O \ldots x - 1]$ and $B[l_B \ldots b(x) - 1]$, which follow the earlier pieces. No triple has its first index in $[l_O, x)$, by the choice of $x$, and the triples at $x$ and after keep the second form for the new values $x$, $a(x)$, $b(x)$. So the invariant holds. $\square$

**Lemma 2 (progress).** Each round of the loop emits a nonempty chunk and increases $l_O + l_A + l_B$. So the loop ends.

*Proof.* A stable chunk has $k \ge 1$ lines in each piece. For an unstable chunk, all three pieces are empty only if $x = l_O$, $a(x) = l_A$ and $b(x) = l_B$, but then $(l_O, l_A, l_B)$ is a triple, and line L2 would have found $i > 1$. The sum is at most $|A| + |O| + |B|$. $\square$

**Theorem 1 (a diff3 parse).** The chunks returned by the parse form a diff3 parse of $A$, $O$ and $B$ with respect to $M_A$ and $M_B$.

*Proof.* The loop stops at line L3 when no line $x \ge l_O$ is matched in both. Line L6 then emits the rest of the three files as one chunk if it is not empty, so by Lemma 1 the chunks cut the three files into consecutive pieces. When the loop stops, no triple has the second form of Lemma 1, so every triple lies in a stable chunk, at the same offset in its three pieces: this is (I).

For (II), take a stable chunk with starts $(o, p, q)$ and length $k$. It cannot grow at the end: line L2 stopped because $(o + k, p + k, q + k)$ is not a triple, so a chunk that follows starts with an unstable chunk or nothing. It cannot grow at the start either. If it is the first chunk, then $o = p = q = 0$. Otherwise the chunk before it is unstable, because a stable chunk is never followed by another one, and it was made at line L4 with the least line $x = o \ge l_O$ that is matched in both. If $(o - 1, p - 1, q - 1)$ were a triple, then $o - 1 < l_O$ by the choice of $x$, so $o = l_O \ge 1$. An unstable chunk ends at a triple, so the next round emits a stable chunk; so the chunk before this unstable chunk is stable, and the triple of $l_O - 1$ is its last one, $(l_O - 1, l_A - 1, l_B - 1)$. Then $p = l_A$ and $q = l_B$, and the unstable chunk would be empty, against Lemma 2. $\square$

**Classes.** Each unstable chunk gets one class from its three pieces $(A_i, O_i, B_i)$: changed in $A$ if $O_i = B_i \ne A_i$, changed in $B$ if $O_i = A_i \ne B_i$, falsely conflicting if $A_i = B_i \ne O_i$, and truly conflicting if all three differ. The code adds one more class, unchanged, for $A_i = O_i = B_i$. This class is empty when $M_A$ and $M_B$ are maximum: the pairs of $M_A$ that start in $O_i$ end in $A_i$, because the chunk borders are triples, so the part of $M_A$ in the chunk is a maximum matching of $O_i$ and $A_i = O_i$, and so it is the identity. The same holds for $M_B$, so the first line of the chunk would start a triple at the start of the three pieces, and the chunk would be stable.

**Theorem 2 (the merge rule).** The merge takes the stable chunks, $A_i$ for a chunk that is changed in $A$, falsely conflicting or unchanged, and $B_i$ for a chunk that is changed in $B$; it marks the truly conflicting chunks. As a result:

1. If $A = O$ and $M_A$ is a maximum matching, the merge is $B$, with no conflict, for any $M_B$.
2. If $B = O$ and $M_B$ is a maximum matching, the merge is $A$, with no conflict, for any $M_A$.
3. If $A = B$ and $M_A = M_B$, the merge is $A$, with no conflict.

*Proof.* The first sentence is lines L7 and L8. For part 1, a maximum matching of $O$ with itself has $|O|$ increasing pairs, so it is the identity. Then $l_A = l_O$ at each round: a stable chunk adds the same length to both, and an unstable chunk sets $l_A = a(x) = x = l_O$. So $A_i = O_i$ in every chunk, and each chunk is stable, unchanged or changed in $B$. In each case the merge takes a piece equal to $B_i$, and by Theorem 1 the pieces $B_i$, in order, make $B$. Part 2 is the same with the two sides swapped. For part 3, $M_A = M_B$ gives $a(x) = b(x)$ for each $x$, so $l_A = l_B$ at each round and $A_i = B_i$ in every chunk. Each chunk is then stable, unchanged or falsely conflicting, and the merge takes $A_i$. $\square$

**Output triples.** The function for the outputs $(A', O', B')$ of the paper writes $(A_i, A_i, A_i)$ for a chunk that is changed in $A$, $(B_i, B_i, B_i)$ for a chunk that is changed in $B$, and $(A_i, O_i, B_i)$ for the other chunks, which is the definition of the output of a chunk.

**Cost.** By Lemma 2 there are at most $|A| + |O| + |B|$ rounds. Line L2 tests $i$ triples and the round moves $l_O$ by $i - 1$. Line L3 scans the lines $l_O$ to $x$ and the round moves $l_O$ to $x$, so each line of $O$ is scanned at most twice over all rounds. With hash sets for the matchings, each test takes expected $O(1)$ time, and the copies of the pieces take $O(|A| + |O| + |B|)$ in total. So the chunk pass is expected linear. The two matchings of the shared helper cost $O(|O| \, |A| + |O| \, |B|)$.
