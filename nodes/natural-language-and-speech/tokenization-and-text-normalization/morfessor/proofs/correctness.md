---
title: The Morfessor search returns segmentations of the words, keeps the cost up to date, and never raises the cost, but it can stop at a local optimum
proves: [correctness, termination]
status: full
---

Notation. The corpus gives each word type $w$ a count $f_w \ge 1$. An analysis $A$ gives each word $w$ a list of morphs $A(w)$ whose concatenation is $w$. The morph counts are $c(m) = \sum_w f_w \cdot (\text{the number of times } m \text{ is in } A(w))$, the total is $C = \sum_m c(m)$, and the lexicon is the set of morphs with $c(m) > 0$. All logs are natural logs. With the maximum likelihood estimate $p(m) = c(m) / C$ of Creutz and Lagus, the two-part cost is

$$\mathrm{cost}(A) = \sum_{\text{tokens}} -\ln p(m) + K \sum_{m \in \text{lexicon}} |m| = C \ln C - \sum_m c(m) \ln c(m) + K \sum_{m \in \text{lexicon}} |m|,$$

since the morph $m$ is used $c(m)$ times and $\sum_m c(m) \ln (c(m) / C) = \sum_m c(m) \ln c(m) - C \ln C$. Here $K > 0$ is the cost of one character of the lexicon, in nats ($5 \ln 2$ for 5 bits).

**Lemma 1 (the counts).** After any sequence of calls ADD($m$, $d$) that keeps every count nonnegative, the model holds $C$, $S = \sum_m c(m) \ln c(m)$ and the total length of the lexicon, so COST returns the formula above for the current counts.

*Proof.* Each call changes one count from $c$ to $c + d$. It adds $d$ to $C$, replaces the term $c \ln c$ of $S$ by $(c + d) \ln (c + d)$ (with $0 \ln 0 = 0$), and adds or removes $|m|$ from the lexicon length exactly when the count leaves or reaches $0$. By induction on the number of calls, the three values match the counts. COST-WITH adds and then removes the same amounts, so it leaves the model as it found it. $\square$

**Theorem 1 (RESPLIT).** For a string $s$ and a count $f$, RESPLIT stops, returns a list of nonempty strings whose concatenation is $s$, and adds $f$ to the count of each returned morph, once per use.

*Proof.* By induction on $|s|$. If line R5 keeps $s$ whole, it adds $f$ to $c(s)$ and returns $[s]$. Otherwise there is a cut $0 < i < |s|$, and lines R6 and R7 call RESPLIT on $s[{:}i]$ and $s[i{:}]$, which are shorter, nonempty, and join to $s$. By the induction hypothesis each call stops, returns a list that joins to its part and adds $f$ for each morph it returns, so the joined list has the claimed properties. $\square$

**Theorem 2 (the cost never rises).** Each pass of lines M4 to M6 over one word keeps an analysis of the corpus whose model counts are the counts of the analysis, and the cost after the pass is at most the cost before it. So the costs of the trace never increase, and MORFESSOR stops after at most the given number of epochs.

*Proof.* Before the pass, the model counts are those of $A$ (at the start by line M1, and later by induction). Line M4 removes $f_w$ from each morph of $A(w)$, and line M5 adds $f_w$ for each morph of the new list (Theorem 1), so the counts are those of $A$ with $A(w)$ replaced by the new list, which joins to $w$. If the new cost is larger than the cost before, line M6 removes the new morphs and adds back the old ones, which restores the counts and the cost of $A$. In both cases the cost does not rise, by Lemma 1. Each epoch is a sequence of such passes, so its cost is at most the cost at its start. The loop runs at most max-epochs times. $\square$

**Theorem 3 (only a local optimum).** The result need not have the least cost over all analyses.

*Proof.* Take the corpus bb 11 times and bbbb 9 times. Start from the words whole. With $K = 5 \ln 2$ and either order of the two words (the test file runs both), RESPLIT compares each word whole with its splits while the other word is still in the lexicon, and the search ends with bb as bb and bbbb as bb + bb: one morph type of 2 characters, a data cost of $0$ (one morph has probability 1), and a cost of $2K$. The analysis with every word as single b's has one morph type of 1 character and a cost of $K < 2K$. The test file runs this case and checks the global optimum by brute force over all analyses. $\square$

The cost is a sum over the corpus, and the search changes one word at a time with a greedy recursive split, so the result depends on the order of the words and on the start. Theorem 2 makes the search a descent method; whether its result is a good segmentation is a matter of measurement.
