---
title: PORTER-STEM applies the rules of Porter (1980) exactly, and its output is never longer than its input
proves: [correctness]
status: full
---

Let $w = w_1 w_2 \cdots w_n$ be a word of lower case letters. The rules of the paper are fixed: for each step $s$ in the order 1a, 1b, 1c, 2, 3, 4, 5a, 5b there is a list of rules $(C)\ S_1 \to S_2$, and step 1b has a second part that runs only if its rule for "ed" or "ing" was applied. The paper says that in each step only one rule is obeyed, the one with the longest $S_1$ that ends the word, and that it is obeyed only if its condition $C$ holds for the stem, the word without $S_1$. We show that PORTER-STEM computes exactly this.

**The type of a letter.** By the definition of the paper, letter $i$ of a string $x$ is a consonant if it is not a, e, i, o or u, and it is not a y that follows a consonant. Write $c_x(i)$ for "letter $i$ of $x$ is a consonant".

**Lemma 1.** CONSONANT-FLAGS returns $c_x(1), \ldots, c_x(|x|)$, and if $v$ is a prefix of $x$ then $c_v(i) = c_x(i)$ for $i \le |v|$.

*Proof.* The definition gives $c_x(i)$ from letter $i$ and, for a y, from $c_x(i-1)$; a y at position 1 follows no letter and is a consonant. The code computes the flags from left to right by exactly these cases, so by induction on $i$ each flag is right. The flag $c_x(i)$ depends only on letters $1, \ldots, i$, which are the same in $v$ and in $x$, so the second claim follows by the same induction. $\square$

So a condition on the stem $v$ can be evaluated on $v$ alone: the stem has the same consonants and vowels as the first $|v|$ letters of the word.

**Lemma 2.** For every string $v$, MEASURE$(v)$ (lines L13 to L15) returns the number $m$ in the form $v = [C](VC)^m[V]$.

*Proof.* Cut the flag sequence of $v$ into maximal runs of equal flags. The runs alternate between consonant runs (C) and vowel runs (V), so the sequence of runs is $[C](VC)^m[V]$ for exactly one $m$: $m$ is the number of V runs that are followed by a C run. Line L14 counts the positions $i$ where letter $i$ is a vowel and letter $i+1$ is a consonant. Such a position is the last letter of a V run whose next run is a C run, and each V run followed by a C run has exactly one last letter. So the count is $m$. $\square$

**Lemma 3.** The helpers decide the conditions of the paper on a stem $v$: HAS-VOWEL decides \*v\*, ENDS-DOUBLE-CONSONANT decides \*d, and ENDS-CVC decides \*o.

*Proof.* \*v\* says that some letter of $v$ is a vowel, which is "not every flag is a consonant". \*d says that $v$ ends with a double consonant: the last two letters are equal and both are consonants, which is what ENDS-DOUBLE-CONSONANT tests with the flags of Lemma 1. Porter's C code tests only the flag of the last letter. The two readings differ only for a final yy whose last y is a consonant: a y is a consonant only after a vowel, so the y before it is then a vowel, and by the definition the stem does not end with a double consonant. \*o says that the last three letters are consonant, vowel, consonant and the last letter is not w, x or y, which is what ENDS-CVC tests, with Lemma 1 for the flags. The tests \*S, \*T and \*L compare the last letter. $\square$

**Lemma 4.** In each step, line L2 finds the rule of the paper's longest match, or line L3 finds that no rule matches.

*Proof.* In each table no two rules have the same $S_1$; the two rules of step 5a with $S_1$ = "e" are written as one rule whose condition is (m > 1) or (m = 1 and not \*o), which holds exactly when one of the two rules of the paper applies. For each length there is at most one suffix of $w$ of that length, so among the rules whose $S_1$ ends $w$ the longest is unique. Line L2 scans all rules and keeps a matching rule when its $S_1$ is strictly longer than the one kept, so at the end it holds that unique rule, or none. $\square$

**Lemma 5.** Lines L4 to L7 do what the paper says once the rule $(C)\ S_1 \to S_2$ is chosen.

*Proof.* Line L4 forms the stem $v$, the word without $S_1$. By Lemmas 1 to 3, line L5 evaluates $C$ on $v$ as the paper defines it. If $C$ fails, the paper obeys no rule in this step, and the code returns $w$ unchanged; it does not try a rule with a shorter $S_1$. If $C$ holds, line L6 replaces $S_1$ by $S_2$.

Line L7 runs the second part of step 1b exactly when the paper does: when the second or third rule of step 1b, for "ed" or "ing", was applied. TIDY-1B is that second part. Its rules at → ate, bl → ble, iz → ize have no condition and the longest $S_1$, so they win when they match (line L9). The other two rules have an empty $S_1$ and act on the whole word. They cannot both hold: \*d needs the last two letters to be consonants, and \*o needs the second last to be a vowel. Line L10 is the rule (\*d and not (\*L or \*S or \*Z)) → single letter, and line L11 is the rule (m = 1 and \*o) → E. If none holds, line L12 leaves the word. $\square$

**Lemma 6.** The rule of step 5b in the code, $S_1$ = "l" with the condition "MEASURE$(v) > 1$ and $v$ ends with l", has the same effect as the paper's rule (m > 1 and \*d and \*L) → single letter.

*Proof.* The paper's rule tests the whole word $w$ and removes its last letter. The word $w$ ends with l and has \*d and \*L exactly when it ends with "ll", which is when the code's stem $v$, $w$ without its last l, ends with l (an l is always a consonant). For such a word, removing the last l does not change the measure: the last two letters are consonants, so the last position is not the end of a V run, and the vowel-consonant positions of Lemma 2 are the same in $w$ and in $v$. So the two conditions agree, and both rules remove the last letter. $\square$

**Theorem.** For every word $w$ of lower case letters, PORTER-STEM$(w)$ returns the result of applying the steps 1a, 1b, 1c, 2, 3, 4, 5a and 5b of the paper to $w$ in this order, with the rule of the longest match in each step. With the definitive option, the step 2 table is the one of the definitive version and words of one or two letters are returned unchanged. The call ends after $O(n)$ work, and its output has at most $n$ letters.

*Proof.* Line L1 runs the eight steps once each, in the order of the paper, and each step passes its output to the next. By Lemmas 4, 5 and 6 each step returns exactly the word that the paper's step gives on its input. The definitive option only changes the step 2 table and adds the test of length at the start, which is what that version specifies.

Each step scans a fixed number of rules with suffixes of at most 7 letters, and the condition and TIDY-1B make a fixed number of scans of the stem, so each step costs $O(n)$ and the call costs $O(n)$. In every rule $|S_2| \le |S_1|$, so a step does not make the word longer. TIDY-1B adds at most one letter, and it runs only after "ed" or "ing" was removed, so the word of step 1b is still shorter than its input. By induction over the steps, the output has at most $n$ letters. $\blacksquare$
