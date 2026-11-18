---
title: A differential file answers every lookup as the flat relation does
proves: [correctness]
status: full
---

**Model.** The structure is a main file $M$ (a map from keys to records), a differential file $D$ (a map from keys to records or a delete marker $\bot$), a filter $F$ of $m$ bits with hash functions $h_1, \dots, h_k$, and an archive (a list of maps). The relation it represents is

$$R(M, D) = \{(x, r) : D(x) = r \ne \bot\} \cup \{(x, r) : M(x) = r,\ x \notin \mathrm{dom}(D)\}.$$

The abstract relation $S$ starts as $M_0$, put$(x, r)$ sets $S(x) = r$, and delete$(x)$ removes $x$ from $S$.

**Invariants.** After every operation:

1. (I1) $R(M, D) = S$.
2. (I2) For every key $x \in \mathrm{dom}(D)$, the bits $h_1(x), \dots, h_k(x)$ of $F$ are 1.
3. (I3) $M$ equals the last map in the archive.

**Lemma 1.** The invariants hold at the start and after each put, delete and reorganize.

*Proof.* At the start $D$ is empty, $F$ is all zeros, $M = M_0 = S$ and the archive holds a copy of $M_0$, so all three hold.

put$(x, r)$ sets $D(x) = r$ (line L4). For $x$ the new $R$ gives $r$, for every other key nothing changes, and $S$ changes the same way, so I1 holds. Line L5 sets the bits of $x$ and clears none, so I2 holds. $M$ and the archive do not change, so I3 holds. delete$(x)$ is the same with $D(x) = \bot$: the new $R$ has no record for $x$, as $S$.

reorganize sets $M' = R(M, D)$ (line L6), appends a copy of $M'$ to the archive and makes it the main file (line L7), and then empties $D$ and clears $F$ (line L8). Now $R(M', \emptyset) = M' = R(M, D) = S$, which is I1. I2 holds because $D$ is empty, and I3 by line L7. $\square$

**Lemma 2.** lookup$(x)$ returns $S(x)$, or absent if $x \notin \mathrm{dom}(S)$.

*Proof.* If $x \in \mathrm{dom}(D)$, then by I2 the test of line L1 is true, and line L2 returns $D(x)$, or absent when $D(x) = \bot$. That is $R(M, D)(x)$. If $x \notin \mathrm{dom}(D)$, then line L2 does not return, whatever the filter says, and line L3 returns $M(x)$ or absent, which again is $R(M, D)(x)$. By I1 this is $S(x)$. $\square$

**Lemma 3.** scan returns the records of $S$ in key order, and between two reorganizations $M$ does not change.

*Proof.* scan computes $R(M, D)$ in key order, which is $S$ by I1. Only line L7 assigns $M$. $\square$

**Recovery.** If $M$ is lost between two reorganizations, a copy of the last map in the archive restores it, by I3, and I1 holds again with the same $D$. $\square$

The filter enters only in Lemma 2, and only through I2. A false positive (line L1 true for a key not in $D$) changes the reads that a lookup makes, never its answer.
