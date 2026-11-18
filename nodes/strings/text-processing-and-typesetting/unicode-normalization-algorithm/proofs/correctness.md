---
title: The normalization procedure computes NFD, NFC, NFKD and NFKC as defined in the core specification
proves: [correctness, termination]
status: full
---

**Claim.** For every string $X$ of code points, NORMALIZE (lines L1 to L5) stops, and it returns toNFD$(X)$, toNFKD$(X)$, toNFC$(X)$ or toNFKC$(X)$ for the four forms. These are defined in section 3.11 of the core specification: NFD is the full canonical decomposition of each character (D68) followed by the Canonical Ordering Algorithm (D109), NFKD is the same with the full compatibility decomposition (D65), and NFC and NFKC apply the Canonical Composition Algorithm (D117) to the result of NFD and NFKD.

**Data facts.** The proof uses three properties of the Unicode Character Database. They are facts about the data, not consequences of the definitions. The tests do not prove them, but they compare the whole procedure with an independent implementation on every decomposable character of Unicode 3.2 and on random strings, so an error in one of them would show up there.

- (F1) The decomposition mappings form no cycle, so the full decomposition of every code point exists (D68 and D65 assume this). Its longest case under NFKD has 18 code points.
- (F2) Every primary composite (D114) has canonical combining class 0. This is why the non-starter decompositions are full composition exclusions.
- (F3) Let $L$ be a starter that the composition has produced and $C$ a character after it. A primary composite $P$ is canonically equivalent to $\langle L, C \rangle$ exactly when the canonical decomposition mapping of $P$ is the pair $(L, C)$, or $L$, $C$ are a Hangul $L, V$ or $LV, T$ pair. This is the pair table that UAX 15 describes and that the implementation builds from the two-part mappings of the characters that are not full composition exclusions.

**Lemma 1 (decomposition, lines L6 to L9).** FULL-DECOMPOSE$(c)$ returns the full canonical decomposition of $c$, or the full compatibility decomposition if the form is NFKD or NFKC.

*Proof.* By induction on the depth of the mapping graph, which is finite by (F1). A Hangul syllable gets the jamo of section 3.12.2 at line L6, and jamo do not decompose further. A code point without a mapping of the selected kind is its own full decomposition (line L8). Otherwise line L9 replaces each code point of the mapping by its full decomposition, which is the definition. For canonical decomposition, compatibility mappings (those with a tag such as <compat>) are skipped. For compatibility decomposition, both kinds are applied, as D65 requires. $\square$

So after line L2, $d$ is the concatenation of the full decompositions of the characters of $X$.

**Lemma 2 (ordering, lines L10 to L13).** CANONICAL-ORDER$(d)$ leaves the starters in place and stably sorts each maximal run of non-starters by canonical combining class. The result has no reorderable pair (D108), and it is the unique result of D109.

*Proof.* Line L12 swaps $d[j-1]$ and $d[j]$ only if $\mathrm{ccc}(d[j-1]) > \mathrm{ccc}(d[j]) > 0$, that is, only a reorderable pair. Both characters are non-starters, so a starter never moves and a mark never crosses a starter. Invariant of the loop of line L10: before step $i$, $d[0 \ldots i-1]$ has no reorderable pair, so each run of non-starters in it is sorted by ccc. Step $i$ moves $d[i]$ left while the character before it is a non-starter with a larger class, and stops at a starter, at a mark with a class at most $\mathrm{ccc}(d[i])$, or at the start. If $\mathrm{ccc}(d[i]) = 0$, nothing moves. This is one step of insertion sort inside the last run, so the invariant holds for $i + 1$. Marks with equal classes are never swapped, so the sort is stable.

Uniqueness: D109 swaps reorderable pairs until none remain. Every such swap keeps the positions of the starters and the relative order of two marks with equal classes. So in any final result, each run holds the same marks, in nondecreasing class order, with equal classes in their input order, and only one sequence has these properties. $\square$

After line L3, $d$ is therefore toNFD$(X)$ or toNFKD$(X)$, and line L5 returns it for the forms NFD and NFKD.

**Lemma 3 (composition, lines L14 to L22).** For a canonically ordered sequence $d$, COMPOSE$(d)$ returns the result of D117.

*Proof.* D117 visits the characters $C$ from left to right. For each one, it finds the last starter $S$ before $C$, and if $C$ is not blocked from $S$ and a primary composite $P$ is canonically equivalent to $\langle S, C \rangle$, it replaces $S$ by $P$ and deletes $C$. By D115, $C$ is blocked from $S$ when some character $B$ between them has $\mathrm{ccc}(B) = 0$ or $\mathrm{ccc}(B) \ge \mathrm{ccc}(C)$.

The procedure keeps the processed prefix in $out$. Invariant: $starter$ is the index in $out$ of the last starter, or $-1$ if there is none, and $last$ is the class of the last character after it in $out$, or $-1$ if there is no such character. Every character after $out[starter]$ is a non-starter, because each starter that is appended becomes the new $starter$ (line L20). These non-starters come from one run of the canonically ordered input, so their classes do not decrease, and the largest of them is $last$. So some character between $S$ and $C$ blocks $C$ exactly when $last \ne -1$ and $last \ge \mathrm{ccc}(C)$. Line L17 tests the opposite, so it allows composition exactly when D117 does. For a starter $C$ this means that $C$ must come right after $S$. By (F3), COMPOSE-PAIR finds $P$ when it exists. If it does (line L18), $P$ replaces $S$ and $C$ is dropped. By (F2), $P$ is a starter, so the invariant still holds, and $last$ does not change because $C$ is gone. If it does not, line L21 appends $C$ and lines L19 and L20 update the invariant. $\square$

**Proof of the claim.** By Lemmas 1 and 2, lines L1 to L3 compute toNFD$(X)$ or toNFKD$(X)$. For the forms NFC and NFKC, line L4 applies COMPOSE, which by Lemma 3 is D117. That is the definition of toNFC and toNFKC.

**Termination.** FULL-DECOMPOSE stops by (F1). Each step of CANONICAL-ORDER moves one mark left at most $i$ times, so the sort stops after $O(m^2)$ comparisons for $m = |d|$, and in fact after $O(\sum_r k_r^2)$ for runs of lengths $k_r$. COMPOSE runs its loop once per element of $d$. So NORMALIZE stops. $\blacksquare$
