---
title: The matcher returns exactly the matches of the six patterns, with the longest lists
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A sentence is a sequence $a_0, \ldots, a_{n-1}$ of items, each a noun phrase (NP) or a word, and words are compared in lowercase. CONJ is the set $\{\text{and}, \text{or}\}$. The proof is about the patterns as they are written. Whether a match is a true hyponym pair is a heuristic question, answered by measurement.

**The specification.** A right list at $q$ is a sequence of items $a_q \ldots a_r$ of the form NP ("," NP)$^*$ [[","] CONJ NP]. The longest right list at $q$ is the right list at $q$ with the largest $r$, and $R(q)$ is the set of positions of its NPs, or $\emptyset$ if $a_q$ is not an NP. A left list ending at $p$ is a sequence $a_l \ldots a_{p-1}$ of the form NP ("," NP)$^*$ [","], and $L(p)$ is the set of NP positions of the one with the smallest $l$, or $\emptyset$ if there is none. The hypernym before $p$ is $h(p) = p - 1$ if $a_{p-1}$ is an NP, $p - 2$ if $a_{p-1}$ is "," and $a_{p-2}$ is an NP, and undefined otherwise. A position $p$ triggers:

- pattern 1 if $a_p a_{p+1}$ = "such as" and $h(p)$ is defined, with the matches $(x, h(p), 1)$ for $x \in R(p + 2)$;
- pattern 2 if $a_p$ = "such", $a_{p+1}$ is an NP and $a_{p+2}$ = "as", with the matches $(x, p + 1, 2)$ for $x \in R(p + 3)$;
- pattern 5 or 6 if $a_p$ is "including" or "especially" and $h(p)$ is defined, with the matches $(x, h(p), 5 \text{ or } 6)$ for $x \in R(p + 1)$;
- pattern 3 or 4 if $a_p$ is "or" or "and", $a_{p+1}$ = "other" and $a_{p+2}$ is an NP, with the matches $(x, p + 2, 3 \text{ or } 4)$ for $x \in L(p)$.

**Lemma 1.** The function RIGHT-LIST($q$) stops and returns $R(q)$.

*Proof.* If $a_q$ is not an NP, there is no right list at $q$ and the function returns the empty list. Otherwise, call a right list at $q$ open if it has no CONJ, and closed if it ends with CONJ NP. Let $a_q \ldots a_{j-1}$ be an open right list. The items that can follow it in a longer right list are ", NP" (a longer open list), "CONJ NP" (a closed list) or ", CONJ NP" (a closed list). These three cases are disjoint: the first and the third both start with ",", but the item after the comma is an NP in the first and a word in the third, and the second starts with a word in CONJ, which is not ",". A closed list cannot be extended. So the right lists at $q$ form one chain $\ell_0 \subset \ell_1 \subset \cdots$, each a prefix of the next, where $\ell_0 = a_q$ and $\ell_{i+1}$ is the unique one-step extension of $\ell_i$. The loop keeps the invariant that $a_q \ldots a_{j-1}$ is the open list $\ell_i$ and that $out$ holds its NP positions. Each test of the loop checks one of the three cases. In the first case it moves to $\ell_{i+1}$ and adds its new NP. In the second and third cases it adds the last NP of the closed list $\ell_{i+1}$ and returns. If no case applies, $\ell_i$ has no extension and is the longest. Each round of the loop increases $j$ by 2 or returns, and $j \le n + 1$ at the start of every round, so the loop stops. In all cases it returns the NP positions of the last list of the chain, which is the longest. $\square$

**Lemma 2.** The function LEFT-LIST($p$) stops and returns $L(p)$.

*Proof.* Read the items from $p - 1$ toward 0. A left list ending at $p$ is an optional "," at $p - 1$, then an NP, then zero or more pairs "," NP read to the left. Whether the optional comma is present is decided by $a_{p-1}$, since an NP is not ",". After that, the same argument as in Lemma 1 applies in the reverse direction with one extension case, ", NP": the left lists form one chain, and the loop follows it one pair at a time until $a_{j-1}$ is not "," or $a_{j-2}$ is not an NP. It returns the positions of the longest one, in left to right order. The index $j$ decreases by 2 each round and stays at least 0, so the loop stops. $\square$

**Claim.** HEARST returns, in the order of $p$ and then of the list, exactly the matches of the specification, and it stops.

*Proof.* Each position $p$ triggers at most one pattern. Patterns 1 and 2 both start with "such", but $a_{p+1}$ is the word "as" for pattern 1 and an NP for pattern 2. Patterns 5 and 6 start with "including" or "especially", and patterns 3 and 4 with "and" or "or", which are different words from "such" and from each other. Line L3 tests the condition of pattern 1 and, with the function NP-BEFORE, which returns $h(p)$ by its definition, the existence of $h(p)$. Line L4 tests pattern 2, line L5 patterns 5 and 6 with $h(p)$, and line L6 patterns 3 and 4. When the test of a line holds, it adds one triple per position of RIGHT-LIST or LEFT-LIST, which are $R$ and $L$ by Lemmas 1 and 2. So the loop of line L2 adds, for each $p$ in increasing order, exactly the matches that $p$ triggers. The loop has $n$ rounds, each of which stops by the lemmas, and line L7 returns the list. $\blacksquare$
