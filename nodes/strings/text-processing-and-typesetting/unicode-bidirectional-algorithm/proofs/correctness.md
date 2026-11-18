---
title: "BIDI computes the paragraph level, the resolved levels and the visual order that the rules of UAX 9 define"
proves: [correctness, termination]
status: full
---

**Setup.** Let $s = s[0] \cdots s[n-1]$ be one paragraph, shown as one line, and let $t[i]$ be the Bidi_Class of $s[i]$. UAX 9 defines the result by rules that are applied in a fixed order. Each claim below shows that one part of BIDI computes the result of its rules from the result of the rules before them. Together they show that BIDI returns the levels and the order of UAX 9.

**Claim 1 (BD9).** `matching_pdi` gives each isolate initiator its matching PDI as BD9 defines it, or none.

*Proof.* BD9 matches an isolate initiator with the first later PDI at which the number of PDIs equals the number of isolate initiators counted from the initiator on, or with nothing if the paragraph ends first. The function keeps a stack of the unmatched initiators. A PDI matches the initiator on top of the stack, which is the latest initiator whose count is still open. This is the usual matching of [balanced parentheses](/balanced-parentheses/) with initiators as opening and PDIs as closing symbols, and it gives the same pairs as the counter of BD9. A PDI that finds the stack empty matches nothing, and so does an initiator left on the stack at the end. $\square$

**Claim 2 (P2, P3 and line L2).** `first_strong(t, a, b, match)` returns 0 if the first character of class L, R or AL in $t[a \ldots b-1]$ that is not between an isolate initiator and its matching PDI is L, 1 if it is R or AL, and none if there is no such character.

*Proof.* The loop goes through the positions in order. At an isolate initiator, it jumps to the matching PDI, so it skips exactly the characters between them; if there is no matching PDI, P2 skips the rest of the paragraph, and the loop returns none. Otherwise it returns at the first strong character. $\square$

So line L2 sets $p$ by P2 and P3 in automatic mode, and FSI gets its direction by the same rules on the text up to its matching PDI, as X5c says.

**Claim 3 (X1 to X8, line L3).** `explicit_levels` gives each character the level and the type that rules X1 to X8 give it.

*Proof.* The function keeps the state of X1: the directional status stack, with entries of level, override status and isolate status, and the three counters of overflow isolates, overflow embeddings and valid isolates. Each branch of the loop is one rule, with the same tests and the same updates:

- X2 to X5: the new level is the least odd or even level above the level of the top entry. The entry is pushed when the level is at most max_depth = 125 and both overflow counters are zero. Otherwise the overflow embedding counter goes up if the overflow isolate counter is zero.
- X5a to X5c: the initiator gets the level of the top entry and the override of the top entry. Then the same test decides between a push with isolate status true, together with an increment of the valid isolate counter, and an increment of the overflow isolate counter.
- X6a (PDI): if the overflow isolate counter is positive, it goes down. Else, if the valid isolate counter is positive, the overflow embedding counter is reset, the entries without isolate status are popped, then the isolate entry is popped, and the valid isolate counter goes down. In all cases the PDI gets the level and the override of the new top entry.
- X7 (PDF): nothing if an isolate overflows, a decrement if an embedding overflows, and a pop if the top entry has no isolate status and is not the only entry.
- X6 for all other characters except B and BN: the level of the top entry, and the class L or R if the override status says so. X8 gives B the paragraph level. BN is removed by X9, so its level does not matter.

The stack never becomes empty, because the pop of X6a needs a valid isolate, whose entry lies above the entry of X1, and the pop of X7 needs at least two entries. $\square$

**Claim 4 (X9, X10, lines L4 and L5).** The lists of `isolating_run_sequences` are the isolating run sequences of BD13, and sos and eos are those of X10.

*Proof.* After the removal of the classes of X9, the level runs are the maximal runs of kept characters with equal levels, which is how the function builds them. BD13 starts a sequence with each level run that does not begin with a PDI matched to an initiator at the end of an earlier level run, and appends, while the last run ends with an initiator that has a matching PDI, the level run that begins with that PDI. The function follows these links, and it marks each run when it uses it, so each level run is in exactly one sequence, in the order of BD13. When the initiator at the end of a run has a matching PDI, X5a to X5c and X6a give the initiator and the PDI the same level and the text between them a higher level, or the same level if the isolate overflows; in the first case the PDI starts a level run, which is the run that is appended. For sos, X10 takes the higher of the level of the sequence and the level of the kept character before its first character, or $p$ if there is none. For eos, it takes the kept character after the last one, or $p$ if there is none or if the last character is an isolate initiator. Lines after L5 compute exactly these. $\square$

**Claim 5 (W1 to W7, line L6).** After line L6, each type in the sequence is the result of rules W1 to W7.

*Proof.* UAX 9 applies each W rule to all the types of the sequence, in order, before the next rule. The function has one pass per rule, in the order W1 to W7:

- W1 goes from left to right and reads the type before the mark after the previous step has changed it, so a run of marks takes the type before the run; at the start it uses sos, and after an isolate initiator or a PDI it uses ON.
- W2 keeps the last strong type of L, R and AL, starting with sos, and changes EN to AN when it is AL. W3 then changes every AL to R.
- W4 changes a single ES between two EN, and a single CS between two numbers of the same type. W5 changes each maximal run of ET that touches an EN. W6 changes the remaining ES, ET and CS to ON. W7 changes EN to L when the last strong type of L and R, or sos, is L.

Each pass reads the types left by the passes before it, as the rules require. $\square$

**Claim 6 (N0 to N2 and I1, I2, lines L7 to L9).** After line L9, the levels of the sequence are those of rules N0 to I2.

*Proof.* BD16 finds the pairs with a stack of 63 entries among the characters of type ON with a Bidi_Paired_Bracket_Type: an opening bracket is pushed, and a closing bracket pops the stack down to the nearest entry whose bracket matches it, after canonical decomposition, if there is one. If an opening bracket finds the stack full, BD16 returns an empty list. The function does exactly this, then sorts the pairs by the position of the opening bracket. N0 handles the pairs in this order, and each pair sees the types that the pairs before it have set. For a pair, with $e$ the embedding direction and EN and AN counted as R: if a strong type equal to $e$ is inside, the pair gets $e$. If only the opposite direction is inside, the pair gets the first strong direction before the opening bracket, or sos; this is the opposite direction if that is what the context has, and $e$ otherwise. If no strong type is inside, the pair is left alone. Then the characters that were NSM before W1 and directly follow a changed bracket get its type. N1 and N2 then go over each maximal run of the neutral and isolate types B, S, WS, ON, LRI, RLI, FSI and PDI. With EN and AN counted as R and sos and eos at the ends, the run takes the direction on both sides when they agree, and $e$ when they do not. Finally I1 and I2 raise the level by the table of the rules, from the final type of each character. $\square$

**Claim 7 (L1 and L2, lines L10 to L12).** Line L10 sets the levels of rule L1, and `visual_order` returns the order of rule L2.

*Proof.* L1 resets to $p$ the levels of S and B, of each maximal sequence of WS and isolate formatting characters before an S or a B, and of such a sequence at the end of the line, with the original classes. The backward loop keeps a flag that is true at the end of the line and after an S or a B, and false after any other kept character, so it resets exactly these characters. Removed characters are skipped, because they have no level. Line L12 is L2 itself: for each $v$ from the highest level down to the lowest odd level, it reverses each maximal run of the list whose levels are at least $v$. If no level is odd, the loop does nothing; in that case all levels are even, every run reversed at a level $v$ is also the run reversed at $v - 1$, and the two reversals cancel, so L2 also leaves the order unchanged. The list holds only the kept characters, so the removed characters are skipped, as in BidiCharacterTest.txt. $\square$

By Claims 2 to 7, BIDI returns the paragraph level, the levels after L1 and the visual order after L2 that UAX 9 defines.

**Termination.** Every loop runs over a finite list, and each `while` loop moves an index forward or backward by at least one step, or pops a stack that never becomes empty (Claim 3). Line L12 runs at most 126 times. So BIDI stops on every input.
