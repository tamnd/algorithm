---
title: The noisy channel corrector returns the exact argmax of P(w) P(x | w) over one-edit candidates
proves: [correctness]
status: full
---

Let $V$ be a finite vocabulary with counts $c(w) \ge 1$ and total $N = \sum_w c(w)$, so $P(w) = c(w)/N$. Let $\Sigma$ be the alphabet and $\#$ a boundary letter not in $\Sigma$. For a string $u$, write $u_j$ for its letter at position $j$ (from 0) and $u_{-1} = \#$. The error model has four tables and a count table $\mathrm{count}$ of letters and letter pairs. A **derivation** of $x$ from $w$ is one of these single edits, with its weight:

- deletion of $w_j$: $x = w_{<j} w_{>j}$, weight $\mathrm{del}[w_{j-1}, w_j] / \mathrm{count}[w_{j-1} w_j]$;
- insertion of $a$ before position $j$: $x = w_{<j}\, a\, w_{\ge j}$, weight $\mathrm{ins}[w_{j-1}, a] / \mathrm{count}[w_{j-1}]$;
- substitution of $w_j$ by $e \ne w_j$: weight $\mathrm{sub}[w_j, e] / \mathrm{count}[w_j]$;
- transposition of $w_j w_{j+1}$ with $w_j \ne w_{j+1}$: weight $\mathrm{trans}[w_j, w_{j+1}] / \mathrm{count}[w_j w_{j+1}]$.

A weight with a zero numerator or denominator is $0$. The channel is $P(x \mid w) = \sum$ of the weights of all derivations of $x$ from $w$, and $P(x \mid w) = 0$ when there is none. This is the one-edit channel of Kernighan, Church and Gale, with the sum over derivations that Jurafsky and Martin use for "acres".

**Lemma 1 (candidate generation).** For a string $x \notin V$, lines L2 to L10 compute the map $C$ with $C[w] = P(x \mid w)$ for every $w \in V$ with $P(x \mid w) > 0$, and with no other keys.

*Proof.* Lines L3 to L9 enumerate tuples, and each tuple names one string $w$ and one weight. We match these tuples one to one with the derivations of $x$ from strings $w$, with the same weight.

- A deletion of $w_j$ gives $x = w_{<j} w_{>j}$, so $x_{<j} = w_{<j}$, the letter before is $x_{j-1} = w_{j-1}$ (or $\#$ for $j = 0$), and $w = x_{<j}\, w_j\, x_{\ge j}$. This is the tuple $(i, a) = (j, w_j)$ of lines L3 and L4, with the weight $\mathrm{del}[x_{i-1}, a] / \mathrm{count}[x_{i-1} a]$. Conversely each tuple $(i, a)$ of line L4 is the deletion of position $i$ from $w = x_{<i}\, a\, x_{\ge i}$.
- An insertion of $a$ before position $j$ of $w$ gives $x_j = a$ and $x_{j-1} = w_{j-1}$, so $w = x$ without $x_j$. This is the tuple $i = j$ of line L6, and conversely.
- A substitution of $w_j$ by $e$ gives $x_j = e$, so $w$ is $x$ with $a = w_j \ne x_j$ at position $j$. This is the tuple $(j, a)$ of line L7, with the weight $\mathrm{sub}[a, x_j] / \mathrm{count}[a]$, and conversely.
- A transposition at $j$ gives $x_j = w_{j+1}$ and $x_{j+1} = w_j$ with $x_j \ne x_{j+1}$. This is the tuple $i = j$ of lines L8 and L9, with the weight $\mathrm{trans}[x_{i+1}, x_i] / \mathrm{count}[x_{i+1} x_i]$, and conversely.

Distinct derivations give distinct tuples, because the kind of edit, the position and the letter determine the tuple. So the sum of the weights that line L10 adds into $C[w]$ is the sum over all derivations of $x$ from $w$, which is $P(x \mid w)$. Line L10 keeps a key only if $w \in V$ and a positive weight was added. $\square$

**Theorem 2 (output).** For $x \notin V$, the procedure returns a word $w^\ast \in V$ that maximizes $P(w) P(x \mid w)$ over all of $V$, the smallest such word in string order, with the score $P(w^\ast) P(x \mid w^\ast)$; if every word has the score $0$, it returns no word. For $x \in V$ it returns $x$ unchanged.

*Proof.* Line L1 handles $x \in V$. Otherwise, by Lemma 1, the words outside $C$ have $P(x \mid w) = 0$ and score $0$, and the words in $C$ have the score $c(w)/N \cdot C[w] > 0$ of line L11. Line L12 scans the words of $C$ in string order and replaces the best word only on a strictly larger score, so it keeps the first word, that is the smallest, among those with the largest score. $\square$

**Lemma 3 (Bayes).** For a fixed $x$ with $P(x) > 0$, the argmax of $P(w \mid x)$ is the argmax of $P(w) P(x \mid w)$.

*Proof.* $P(w \mid x) = P(w) P(x \mid w) / P(x)$ by [Bayes' theorem](/bayes-theorem/), and $P(x)$ does not depend on $w$. $\square$

**Cost.** For $|x| = n$ and $|\Sigma| = \sigma$, lines L3 to L9 form at most $(n + 1)\sigma + n + n(\sigma - 1) + (n - 1) = O(n\sigma)$ strings of length at most $n + 1$. With a hash table for $V$ and for the tables, each string costs $O(n)$ expected time to build and look up, so a correction costs $O(n^2 \sigma)$ expected time and $O(n\sigma)$ extra space. The work does not depend on $|V|$.

The test file checks Theorem 2 against a forward enumeration from every word of the vocabulary, with exact rational weights, on the toy model of the page and on random models over a three-letter alphabet in which several derivations often lead to the same word.
