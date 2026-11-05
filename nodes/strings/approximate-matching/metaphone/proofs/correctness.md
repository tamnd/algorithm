---
title: METAPHONE computes the code that the rule table defines
proves: [correctness]
status: full
---

The specification is the rule table of the page. Let $s$ be the letters of the input in upper case (line L1). Indices are 0-based. The *prepared word* $w$ comes from $s$ in two steps: (P2) remove each letter that is equal to the letter just before it in $s$, unless the letter is C; (P3) if the result starts with KN, GN, PN, AE or WR, remove its first letter. The code of the word is the concatenation, for $i = 0, 1, \ldots, |w| - 1$, of the output of the first rule in the table for the letter $w[i]$ whose context condition holds at position $i$ of $w$. Each context condition reads only $w$, never the output.

**Lemma 1.** After line L3, the program holds the prepared word $w$.

*Proof.* Line L2 scans $s$ from left to right and appends $c = s[t]$ unless the list is non-empty, its last element equals $c$, and $c \ne \mathrm{C}$. We show by induction on $t$ that, after the step for $s[t]$, the list is the result of P2 on $s[0 \ldots t]$, and its last element equals $s[t]$. For $t = 0$, the list is $[s[0]]$. For $t \ge 1$: if $s[t] = s[t-1]$ and $s[t] \ne \mathrm{C}$, P2 removes $s[t]$, and the last element of the list is $s[t-1] = s[t]$ by the induction hypothesis, so line L2 does not append it. Otherwise P2 keeps $s[t]$. If $s[t] \ne s[t-1]$, then the last element $s[t-1]$ differs from $s[t]$ and line L2 appends $s[t]$. If $s[t] = \mathrm{C}$, line L2 appends it in any case. In both cases the last element is now $s[t]$. Line L3 is step P3 word for word. $\square$

**Lemma 2.** For each $i$, the step of line L4 for position $i$ appends the output of the first rule of the table for $w[i]$ whose condition holds at $i$.

*Proof.* The table has a group of rules for each letter, and the rules of one letter are disjoint from those of another letter, so only the group of $w[i]$ matters. Line L5 handles the vowels: the rule "first letter" outputs the vowel at $i = 0$, and the next rule outputs nothing. For a consonant, the branch of the program for $w[i]$ tests the conditions of its group in the order of the table, and it takes the first test that holds. We check each group where a condition is not a direct transcription. For G, the program tests "H follows, and H is neither the last letter nor followed by a vowel", which is the first condition, then "N is the last letter after G, or the rest of the word is NED", then "D before and E, I or Y after", then "E, I or Y after", then the default K. For H, the program tests "C, G, P, S or T before, or W before at position 1", then "a vowel before and no vowel after", then the default H. For W, it tests "position 0 and H after", then "a vowel after", then the default, which outputs nothing. For C, the case "H after" outputs K when S is before and X otherwise, which is the order "S before and H after" then "H after" of the table. The other groups have one or two conditions, and the program tests them in the order of the table. The helper `at` returns the empty string outside $w$, so a test on a letter before position 0 or after position $|w| - 1$ is false, as the table means. $\square$

**Theorem.** METAPHONE returns the code of its input.

*Proof.* By Lemma 1, the loop of line L4 runs over the prepared word $w$. By Lemma 2, each step appends the output of the rule of the table for that position. The steps run for $i = 0, 1, \ldots, |w| - 1$ in order, and no step changes $w$, so line L8 returns the concatenation that defines the code. $\blacksquare$

Each step reads at most three letters after $i$ and one before it, so the time is linear in the length of the input.
