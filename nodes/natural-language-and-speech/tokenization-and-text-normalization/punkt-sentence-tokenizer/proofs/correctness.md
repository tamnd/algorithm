---
title: Punkt applies the decision rules of Kiss and Strunk, and its statistics behave as stated
proves: [correctness, termination]
status: full
---

Punkt is a classifier, not an exact algorithm: its decisions can be wrong on real text, and its thresholds come from experiments. What can be proved is that the procedure computes the decision rules that Kiss and Strunk (2006) state, and that the statistics it uses have the properties that the rules rely on. Let the tokens be $t_1, \dots, t_N$ with types $w(t_i)$. Let $C(w)$ be the number of tokens of type $w$, $C(w, \bullet)$ the number of them with a final single period, $C(w, \neg\bullet) = C(w) - C(w, \bullet)$, and $C(\bullet)$ the number of tokens with a final single period. Logarithms are natural. Write $\ell(k, n, x) = k \ln x + (n - k) \ln (1 - x)$, with $0 \ln 0 = 0$.

**Lemma 1 (the type statistic).** For a type $w$ with $k = C(w, \bullet)$ and $m = C(w, \neg\bullet)$, line L3 computes $-2 \ln (P_0 / P_A)$, where $P_0$ and $P_A$ are the binomial probabilities of $k$ periods in $k + m$ trials with $p = C(\bullet)/N$ and with $0.99$. If $m = 0$ and $p < 0.99$, the value is $2k \ln(0.99/p) > 0$.

*Proof.* Both binomial probabilities have the factor $\binom{k+m}{k}$, which cancels in the ratio, so $-2\ln(P_0/P_A) = -2(\ell(k, k+m, p) - \ell(k, k+m, 0.99))$, which is the code. With $m = 0$ the terms in $1 - x$ vanish and the value is $-2(k \ln p - k \ln 0.99) = 2k \ln (0.99/p)$, which is positive when $p < 0.99$. $\square$

So a type that always has a period gets a positive score that grows linearly with $k$. With the factors $e^{-\mathrm{len}(w)}$ and $(\text{periods} + 1)$ and no penalty, it is classified as an abbreviation as soon as $k \ge 0.3\, e^{\mathrm{len}(w)} / (2(\text{periods} + 1)\ln(0.99/p))$. This is why a word that ends every sentence it occurs in, such as "late" in a small repetitive text, becomes an abbreviation once it is seen often enough.

**Lemma 2 (the collocation statistic).** Let $0 < c_1 < N$, $p = c_2/N$, $p_1 = c_{12}/c_1$ and $p_2 = (c_2 - c_{12})/(N - c_1)$. Then Dunning's $\log\lambda = 2(\ell(c_{12}, c_1, p_1) + \ell(c_2 - c_{12}, N - c_1, p_2) - \ell(c_{12}, c_1, p) - \ell(c_2 - c_{12}, N - c_1, p))$ is at least 0, and it is 0 exactly when $p_1 = p_2$.

*Proof.* For fixed $k$ and $n$, the function $x \mapsto \ell(k, n, x)$ on $[0, 1]$ has its unique maximum at $x = k/n$, because it is strictly concave where it is finite. So $\ell(c_{12}, c_1, p_1) \ge \ell(c_{12}, c_1, p)$ and $\ell(c_2 - c_{12}, N - c_1, p_2) \ge \ell(c_2 - c_{12}, N - c_1, p)$, with equality exactly when $p_1 = p$ and $p_2 = p$. Since $p = (c_1 p_1 + (N - c_1) p_2)/N$ is a weighted mean of $p_1$ and $p_2$ with positive weights, $p_1 = p = p_2$ holds exactly when $p_1 = p_2$. $\square$

**Lemma 3 (the one-sided test).** Under the hypotheses of Lemma 2, $c_{12}/c_1 > c_2/N$ holds exactly when $p_1 > p_2$.

*Proof.* The left side is $p_1$ and the right side is $p$, the weighted mean of $p_1$ and $p_2$ with positive weights. A number is larger than a strict mean of itself and another number exactly when it is larger than the other number. $\square$

By Lemmas 2 and 3, the test in `is_collocation` accepts a pair only if $w_2$ follows $w_1$ more often than it follows other tokens, and the evidence is strong. Without the one-sided test, a very frequent $w_2$ that follows $w_1$ less often than expected would also get a large $\log\lambda$, which is the case of "ist" in Table 1 of the paper.

**Lemma 4 (the statistics of line L6).** After line L6, the case flags of a type $w$ record exactly the cases (first letter upper or lower case) and positions (sentence start or inside a sentence) of the tokens of type $w$ whose position the first pass decides. A token is at a sentence start if it is $t_1$ or if $t_{i-1}$ is a first-pass boundary that is not an initial or a number, and inside a sentence if $t_{i-1}$ has no final period, ellipsis, question mark or exclamation mark. All other tokens are skipped.

*Proof.* The loop in `_statistics` visits every token once. It skips $t_i$ exactly when $t_{i-1}$ is an ellipsis, or has a final period and is not a first-pass boundary, or is an initial or a number with a final period. Otherwise it sets the start bit if $t_{i-1}$ is a first-pass boundary and the inside bit if not; a token with a final ? or ! is always a first-pass boundary. The bits are combined with a bitwise or, so they record which cases occurred and not how often. $\square$

**Theorem.** The procedure stops, and the flag `ends[i]` is true exactly in these cases.

1. $i = N$, or $t_i$ ends in a question mark or an exclamation mark.
2. $t_i$ has a final single period, is not an initial or a number, and its type is not an abbreviation.
3. $t_i$ is an ellipsis, or has a final period and an abbreviation type and is not an initial, and the orthographic heuristic says yes for $t_{i+1}$, or $t_{i+1}$ is capitalized and its type is a frequent sentence starter.
4. $t_i$ is an initial or a number with a final period, it is a first-pass boundary, and none of the three rules of lines L11 and L13 applies: a collocation with $t_{i+1}$ whose type is not a frequent starter, an orthographic "no" for $t_{i+1}$, or, for an initial, an undecided orthographic heuristic with a capitalized $t_{i+1}$ whose type is never seen in lower case in a decided position.

*Proof.* Termination: every loop runs over the tokens, the types or the pairs a fixed number of times. For correctness, the flags start as the first pass of line L5, which is true exactly for a final ? or !, and for a final single period whose type is not an abbreviation. Line L15 sets the last flag. The loop of lines L7 to L14 changes `ends[i]` only for $i < N$ and $t_i$ with a final period or an ellipsis, and the three branches are disjoint. A token of case 2 enters neither branch: it is not an ellipsis, its type is not an abbreviation, and it is not an initial or a number, so it keeps its first-pass value true. A token of case 3 enters the branch of line L8, which sets the flag to the stated condition, by Lemma 4 for the orthographic heuristic and by Lemmas 2 and 3 for the starters. An initial or a number enters the branch of line L10 (an initial is excluded from line L8 even if its type is an abbreviation). That branch only sets flags to false, so the flag is true exactly when the first pass made it true and no rule of lines L11 and L13 applies. Every other token has neither a final period nor an ellipsis, or has a ? or !, and keeps its first-pass value. $\blacksquare$

**Remark.** A number or an initial is never changed from "no boundary" to "boundary", as in the paper: a single letter that is not an abbreviation is expected to occur often without a period, so the type stage already treats it as an ordinary word. The theorem says nothing about the accuracy on real text. Kiss and Strunk report error rates between 0.35% and 2.12% on eleven corpora; that is a measurement.
