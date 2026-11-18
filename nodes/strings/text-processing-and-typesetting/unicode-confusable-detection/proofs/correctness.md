---
title: "SKELETON equals bidiSkeleton(LTR) on text that stays at level 0, and confusability is an equivalence relation"
proves: [correctness, termination]
status: full
---

**Setup.** Let $P(c)$ be the prototype of a code point $c$: the target of the line of $c$ in confusables.txt, or $c$ itself if $c$ has no line. Let $D$ be the set of code points with Default_Ignorable_Code_Point. UTS 39 section 4 defines $\mathrm{internalSkeleton}(X) = \mathrm{NFD}(P^*(\mathrm{NFD}(X) \setminus D))$, where $X \setminus D$ deletes the code points of $D$ and $P^*$ applies $P$ to each code point and concatenates the results.

**Claim 1.** INTERNAL-SKELETON($X$) returns internalSkeleton($X$).

*Proof.* Line L1 computes $\mathrm{NFD}(X)$. Line L2 deletes the code points of $D$ and keeps the order of the rest. Line L3 concatenates $P(c)$ over the remaining code points in order, which is $P^*$. Line L4 applies NFD. Each line is one step of the definition, in the same order. $\square$

**Claim 2.** Let $X$ have no code point of bidi class R, AL or AN and no explicit directional formatting character (LRE, RLE, LRO, RLO, PDF, LRI, RLI, FSI, PDI), and let every code point of class BN in $X$ be in $D$. Then bidiSkeleton(LTR, $X$) = internalSkeleton($X$).

*Proof.* bidiSkeleton(LTR, $X$) runs the bidirectional algorithm of UAX 9 with paragraph level 0 on $X$, reorders through rule L2, applies L3 and L4, and then takes internalSkeleton. We show that every character that the algorithm keeps gets level 0.

- With no explicit formatting characters, rules X1 to X8 give every character the paragraph embedding level 0, and the only isolating run sequence of each paragraph has sos = eos = L. Rule X9 removes the BN characters.
- The remaining classes are L, EN, ES, ET, CS, NSM, ON, B, S and WS. Rule W1 gives each NSM the class of the character before it, or sos = L at the start. W2 changes EN to AN only after AL, and there is no AL. W3 changes AL, of which there are none. W4 to W6 change ES, ET and CS next to EN into EN or into ON. W7 changes each EN to L, because the strong class before it is L or sos = L, since there is no R. After W7 the only strong class is L.
- Rule N0 (brackets) gives a pair the embedding direction L or the direction of the strong class inside, which is L. N1 gives a neutral run between two L the class L. N2 gives the other neutrals the embedding direction, which is L for level 0. So every character is L.
- I1 raises only R, AN and EN at even levels, and there are none. So all levels are 0. Rule L1 sets separators and trailing white space to the paragraph level 0.

With all levels 0, rule L2 reverses no run, because it only reverses runs at level 1 or higher. Rule L3 only moves marks in right-to-left runs, and L4 mirrors only characters at odd levels, so neither changes anything. The only possible difference is that X9 removed the BN characters. These are all in $D$, so step 2 of internalSkeleton removes them anyway. Hence the input to internalSkeleton in bidiSkeleton has the same code points in the same order as $X$ without its BN characters, and both sides give the same skeleton. $\square$

Lines L5 and L6 return INTERNAL-SKELETON($X$) exactly under the conditions of Claim 2, and raise an error otherwise. So SKELETON is skeleton($X$) = bidiSkeleton(LTR, $X$) wherever it returns.

**Claim 3.** The relation $X \cong Y$ of line L7 is an equivalence relation.

*Proof.* $X \cong Y$ holds when skeleton($X$) = skeleton($Y$). Equality of the values of one function is reflexive, symmetric and transitive. $\square$

**Claim 4.** CLASSIFY returns the kind of UTS 39.

*Proof.* If the skeletons differ, line L8 returns none. Otherwise, write ALL for the set of all scripts; it is the identity for intersection, and line L9 computes the resolved script sets $R_X$ and $R_Y$ as intersections with Common and Inherited read as ALL. Single-script confusables are confusables whose resolved script sets share a script, which is the test $R_X \cap R_Y \ne \emptyset$ of line L10. Otherwise they are mixed-script confusables. Among those, whole-script confusables are the ones where both strings are single-script, $R_X \ne \emptyset$ and $R_Y \ne \emptyset$, which is line L11. Line L12 returns the remaining case, mixed-script confusables where at least one string is mixed-script. $\square$

**Idempotence.** UTS 39 states that the data is idempotent. For the subset in the implementation, this can be checked line by line: every prototype is in NFD, contains no code point of $D$, and contains no code point that has a line of its own. A skeleton $S$ is in NFD and has no code point of $D$, so steps 1 and 2 leave it unchanged. Every code point of $S$ comes from a prototype or is a code point without a line, so step 3 leaves it unchanged, and step 4 too. Hence skeleton(skeleton($X$)) = skeleton($X$). A test checks this on random strings.

**Termination.** Each of the lines L1 to L7 makes one pass over a finite string, and NFD stops on every finite input. CLASSIFY calls these a fixed number of times.
