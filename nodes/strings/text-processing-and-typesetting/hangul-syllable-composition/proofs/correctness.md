---
title: Hangul syllable arithmetic decomposes, composes and names the 11,172 syllables correctly
proves: [correctness, termination]
status: full
---

**Claim.** (a) HANGUL-DECOMPOSE (lines L1 to L6) returns, for each precomposed Hangul syllable $s$, its full canonical decomposition as defined in section 3.12.2 of the core specification, and the map from syllables to jamo sequences is a bijection onto the sequences $L\,V$ and $L\,V\,T$ of modern jamo. (b) HANGUL-COMPOSE (lines L7 to L14) gives the same result as the canonical composition algorithm (D117) on any sequence in which no character other than the jamo and the syllables takes part in a composition with them. In particular, HANGUL-COMPOSE(HANGUL-DECOMPOSE$(s)$) $= s$. (c) Lines L15 and L16 give the character name of $s$. All three stop after a number of steps linear in the input length.

**Setup.** The constants are $S_B = \mathtt{AC00}$, $L_B = \mathtt{1100}$, $V_B = \mathtt{1161}$, $T_B = \mathtt{11A7}$, $L_C = 19$, $V_C = 21$, $T_C = 28$, $N_C = V_C T_C = 588$ and $S_C = L_C N_C = 11172$. A leading consonant is a code point $L_B + l$ with $0 \le l < 19$, a vowel is $V_B + v$ with $0 \le v < 21$, and a trailing consonant is $T_B + t$ with $1 \le t < 28$. The value $T_B$ itself is not a trailing consonant: $t = 0$ stands for "no trailing consonant".

**Lemma 1 (mixed radix).** The map $(l, v, t) \mapsto (l V_C + v) T_C + t$ is a bijection from $\{0 \ldots 18\} \times \{0 \ldots 20\} \times \{0 \ldots 27\}$ onto $\{0 \ldots 11171\}$, and its inverse is $l = x \operatorname{div} N_C$, $v = (x \bmod N_C) \operatorname{div} T_C$, $t = x \bmod T_C$.

*Proof.* This is the representation of $x$ in the mixed radix $(19, 21, 28)$. For $x = (l V_C + v) T_C + t$ with digits in range, $x \bmod T_C = t$ and $x \operatorname{div} T_C = l V_C + v$, which splits in the same way into $v$ and $l$, and $(x \bmod N_C) \operatorname{div} T_C = v$ because $x \bmod N_C = v T_C + t$. Both sets have $19 \cdot 21 \cdot 28 = 11172$ elements. $\square$

**Proof of (a).** Section 3.12.2 defines the decomposition of a syllable by these formulas: the syllable index is $s - S_B$, and the jamo are $L_B + l$, $V_B + v$, and $T_B + t$ if $t > 0$. Lines L1 to L4 compute $l$, $v$ and $t$ as in Lemma 1, and lines L5 and L6 return the jamo. The jamo have no decomposition mappings, so this decomposition is full. By Lemma 1, different syllables give different digit triples, and every $L\,V$ or $L\,V\,T$ comes from the syllable with index $(l V_C + v) T_C + t$. The standard gives the decomposition mapping in two parts, $LV$ to $L, V$ and $LVT$ to $LV, T$. Applied twice, the second form gives the same three jamo, because $LV = S_B + (l V_C + v) T_C$ has $t = 0$. $\square$

**Proof of (b).** Every jamo and every syllable has canonical combining class 0, so it is a starter. In D117, a character $C$ is blocked from a starter $S$ before it if any starter lies between them (D115). So a jamo or syllable can combine only with the character directly before it in the current result, and only if that character is a starter. The primary composites (D114) with a Hangul first part are exactly the two-part mappings of (a): $L + V \to LV$ and $LV + T \to LVT$. No syllable is excluded from composition.

HANGUL-COMPOSE keeps this invariant: after each step, its output is the result of D117 on the prefix read so far. Line L9 tests whether the last output character is a leading consonant and $c$ a vowel, and line L10 replaces it by $S_B + (l V_C + v) T_C$, the LV syllable of Lemma 1. Line L11 tests whether the last output character is an LV syllable (index divisible by $T_C$) and $c$ a trailing consonant, and line L12 adds $t$. Otherwise line L13 appends $c$, which is also what D117 does, since no primary composite exists for this pair and $c$ is a starter. After line L10, the new LV syllable is the last output character, so a following trailing consonant composes with it in the next step, as D117 requires. An LVT syllable has an index not divisible by $T_C$, so it takes no second trailing consonant, and $T_B$ fails the test of line L11.

For a syllable $s$ with digits $(l, v, t)$, the input $L_B + l$, $V_B + v$ gives $S_B + (l V_C + v) T_C$ at line L10, and a trailing $T_B + t$ adds $t$ at line L12. By Lemma 1 the result is $s$. $\square$

**Proof of (c).** Section 3.12.4 gives the name as "HANGUL SYLLABLE " followed by the Jamo_Short_Name values of $L$, $V$ and $T$, with the empty string for a missing $T$. Line L15 gets the jamo by (a), and line L16 concatenates their short names from Jamo.txt. The short name of U+110B is empty, so a syllable that starts with it has a name that starts with the vowel. $\square$

**Termination.** Lines L1 to L6 and L15 to L16 do a constant number of operations. HANGUL-COMPOSE runs its loop once per input code point, and each pass does $O(1)$ work. $\blacksquare$
