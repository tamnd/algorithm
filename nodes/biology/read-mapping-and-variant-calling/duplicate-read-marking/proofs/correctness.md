---
title: Duplicate marking returns exactly the duplicates of the definition
proves: [correctness]
status: full
---

Positions are 1-based, as in SAM. The input is a list of templates $T_0, \ldots, T_{N-1}$. A template is a *pair* (two mapped reads) or a *fragment* (one mapped read). Each read $r$ has a library, a chromosome, a leftmost mapped position, a CIGAR string, a strand and a list of base qualities.

## Definitions

**Unclipped 5' end.** For a forward read, the 5' end is the leftmost base. Its unclipped position is $\mathrm{pos} - \ell$, where $\ell$ is the total length of the soft and hard clips (S and H) at the start of the CIGAR string. For a reverse read, the 5' end is the rightmost base. Its unclipped position is $\mathrm{pos} + \mathrm{span} - 1 + \rho$, where span is the total length of the CIGAR operations that consume the reference (M, D, N, = and X) and $\rho$ is the total length of the clips at the end of the CIGAR string. In both cases this is where the 5' end of the read would lie if the clipped bases were aligned without gaps next to the aligned ones.

**End key.** $\kappa(r) = (\text{library}, \text{chromosome}, \text{unclipped 5' position}, \text{strand})$.

**Score and rank.** The score of a read is the sum of its base qualities that are at least 15, capped at 16383. The score $s_i$ of template $T_i$ is the sum over its reads. The rank of $T_i$ is the pair $(s_i, -i)$, compared in lexicographic order. Two different templates never have the same rank, so every non-empty set of templates has exactly one template of largest rank.

**Duplicates.** For a pair $T_i$ with reads $r, r'$, let $E_i$ be the multiset $\{\kappa(r), \kappa(r')\}$. Let $F$ be the set of all end keys of all pairs.

- A pair $T_i$ is a duplicate if there is a pair $T_j$, $j \ne i$, with $E_j = E_i$ and a larger rank.
- A fragment $T_i$ with read $r$ is a duplicate if $\kappa(r) \in F$, or if there is a fragment $T_j$, $j \ne i$, with read $r'$ such that $\kappa(r') = \kappa(r)$ and a larger rank.

This is the rule of Picard MarkDuplicates, without optical duplicates. In words: in each set of pairs with the same two ends, all but the best are duplicates; a fragment is a duplicate of any pair with an end at its place; among the fragments with the same end and no pair there, all but the best are duplicates.

## Proof

**Lemma 1.** The function `unclipped_five_prime` returns the unclipped 5' position of the definition.

*Proof.* For a forward read, the first loop adds up the lengths of the leading operations while they are S or H and stops at the first other operation, which is $\ell$. For a reverse read, the sum of the lengths of the operations in M, D, N, = and X is the span, and the second loop adds the lengths of the trailing S and H operations, which is $\rho$. The function returns the two formulas. $\square$

**Lemma 2.** After the loop of lines L2 to L4, the dictionary `pairs` maps each multiset $E$ that occurs to the list of the pairs $T_i$ with $E_i = E$. The dictionary `frags` maps each end key $\kappa$ that occurs to the list of the fragments whose read has end key $\kappa$. The set `pair_ends` is $F$.

*Proof.* Line L3 sends each pair to the key made by sorting its two end keys. Two multisets of two elements are equal exactly when their sorted tuples are equal, so the pairs with the same key are exactly those with the same $E_i$, whatever the order of the two mates in the template. Line L4 sends each fragment to its end key. Each template is visited once, so each list holds each matching template exactly once. Each pair adds both of its end keys to `pair_ends`, and nothing else is added. $\square$

**Lemma 3.** `_best` returns the template of largest rank in a group.

*Proof.* It takes the maximum of the group under the key $(s_i, -i)$, which is the rank. The maximum is unique, because the second component differs for different templates. $\square$

**Theorem.** `mark_duplicates` returns exactly the set of duplicates of the definition.

*Proof.* Take a pair $T_i$. By Lemma 2 its group in `pairs` is the set of pairs $T_j$ with $E_j = E_i$, and $T_i$ is in it. Line L6 marks every member of the group except the one of largest rank (Lemma 3). So $T_i$ is marked exactly when some other pair with $E_j = E_i$ has a larger rank, which is the definition. Pairs are not touched by the fragment loop.

Take a fragment $T_i$ with read $r$. By Lemma 2 its group in `frags` is the set of fragments with end key $\kappa(r)$. If $\kappa(r) \in F$, line L8 marks the whole group, $T_i$ included, which agrees with the first clause of the definition. Otherwise line L9 marks all members of the group but the one of largest rank, and $T_i$ is marked exactly when another fragment with the same end key has a larger rank, which is the second clause. Fragments are not touched by the pair loop. $\square$

**Independence of the input order of the mates.** The result does not depend on which read of a pair comes first, by the sorting in line L3. It depends on the order of the templates only through the tie rule $-i$: if two templates have the same score and the same key, the one that comes first is kept. Picard breaks such ties in its own way, so in a tie the code can keep a different template than Picard, but it marks the same number of templates.

## Cost

Let $B$ be the total number of bases and CIGAR operations of all reads. Computing all the scores and end keys costs $O(B)$. With hash tables, the grouping of lines L2 to L4 costs $O(N)$ expected time, and lines L5 to L9 touch each template a constant number of times, so the expected time is $O(N + B)$ and the extra space is $O(N)$. Picard sorts the read ends instead of hashing them, which costs $O(N \log N)$ comparisons and lets it spill to disk when the ends do not fit in memory.
