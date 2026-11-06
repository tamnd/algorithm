---
tag: TTA91F
kind: theorem
slug: cfl-pumping-lemma
name: Pumping lemma for context-free languages
aliases:
- Bar-Hillel lemma
area: automata-and-parsing/context-free-parsing
level: core
summary: Every sufficiently long string in a context-free language splits into five parts that can be pumped.
prereqs: [context-free-language, parse-tree, chomsky-normal-form]
see_also: [pumping-lemma-for-regular-languages, cfl-closure-properties, parikh-theorem, cfg-finiteness-problem, cfg-emptiness-problem, inherent-ambiguity, linear-grammar, chomsky-normal-form-conversion]
sources:
  - paper: doi:10.1524/stuf.1961.14.14.143
    title: Yehoshua Bar-Hillel, Micha Perles and Eli Shamir, On formal properties of simple phrase structure grammars, Zeitschrift für Phonetik, Sprachwissenschaft und Kommunikationsforschung 14 (1961)
    locator: pp. 143 to 172
  - paper: doi:10.1007/BF01694004
    title: William Ogden, A helpful result for proving inherent ambiguity, Mathematical Systems Theory 2(3) (1968)
    locator: pp. 191 to 194
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 7.2, The Pumping Lemma for Context-Free Languages (7.2.1 The Size of Parse Trees, 7.2.2 Statement of the Pumping Lemma, 7.2.3 Applications of the Pumping Lemma for CFL's)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 2.3, Non-Context-Free Languages (the pumping lemma for context-free languages, with pumping length b^(|V|+1), and Example 2.36)
---

## Statement

**Notation.** A grammar is $G = (V, \Sigma, R, S)$ with productions $A \to \alpha \mid \beta$, $\varepsilon$ is the empty string, and $|G|$ is the sum of $1 + |\alpha|$ over the productions $A \to \alpha$. For a string $s$, $|s|$ is its length.

**Theorem (Bar-Hillel, Perles and Shamir).** For every [context-free language](/context-free-language/) $L$ there is an integer $p \ge 1$, a *pumping length*, such that every $s \in L$ with $|s| \ge p$ can be written as $s = u v x y z$ with

1. $|v y| \ge 1$,
2. $|v x y| \le p$, and
3. $u v^i x y^i z \in L$ for every $i \ge 0$.

If $L \setminus \{\varepsilon\} = L(G)$ for a grammar $G$ in [Chomsky normal form](/chomsky-normal-form/) with $k$ nonterminals, then $p = 2^k$ works.

The lemma is used in the contrapositive: if for every $p$ there is some $s \in L$ with $|s| \ge p$ such that every split with conditions 1 and 2 leaves the language for some $i$, then $L$ is not context-free.

## In plain words

A grammar in a simple form builds each string as a tree where every inner node has at most two children. A tree with a very long string at the bottom must be tall, and a tall path must use some rule symbol twice, since there are only a few.

Where the same symbol appears twice on a path, the part of the tree between the two copies can be cut out, or repeated as often as we like, and the tree stays valid. Cutting it out or repeating it removes or copies two pieces of the string, one on each side of the middle. These two pieces are what gets pumped.

So in a context-free language every long string has two nearby pieces that can be repeated together. Languages that need three counts to match, like equal numbers of a's, b's and c's, cannot have this.

## Proof

The full proof is in [the proof of the pumping lemma](proofs/main.md). It has two steps.

**Size of parse trees.** In a grammar in Chomsky normal form, a [parse tree](/parse-tree/) whose longest root-to-leaf path has $h$ edges has a yield of length at most $2^{h-1}$. This holds by induction on $h$: a tree of height 1 is $A \to a$, and a taller tree has a root $A \to B C$ with two subtrees of height at most $h - 1$.

**Pumping.** Let $s \in L$ with $|s| \ge p = 2^k$, so $s \ne \varepsilon$ and $s$ has a parse tree $T$ in $G$. Since $|s| > 2^{k-1}$, $T$ has a path of at least $k + 1$ edges, and its lowest $k + 1$ inner nodes are labelled by nonterminals. Two of them carry the same label $A$. Let $N_1$ be the upper one and $N_2$ the lower one, with yields $v x y$ and $x$, and let $s = u (v x y) z$. Then:

- the subtree at $N_1$ has height at most $k + 1$, because the path was chosen longest and $N_1$ is among its lowest $k + 1$ inner nodes, so $|v x y| \le 2^k = p$;
- $N_1$ uses a production $A \to B C$, and $N_2$ lies inside one of the two subtrees, so the other subtree, whose yield is nonempty in Chomsky normal form, is part of $v$ or $y$, and $|v y| \ge 1$;
- replacing the subtree at $N_1$ by the subtree at $N_2$ gives a tree for $u x z$, and replacing the subtree at $N_2$ by a copy of the subtree at $N_1$, $i - 1$ times, gives a tree for $u v^i x y^i z$. $\blacksquare$

For an arbitrary grammar, the same argument works with $p = b^{|V| + 1}$, where $b \ge 2$ bounds the length of the right sides, if $T$ is chosen with the fewest nodes: an empty $v y$ would let the subtree at $N_2$ replace the one at $N_1$ and give a smaller tree for $s$ (Sipser).

**Example of the construction.** Take the grammar $S \to A X \mid A B$, $X \to S B$, $A \to a$, $B \to b$ for $\{a^n b^n : n \ge 1\}$ and the string $aaabbb$. Its parse tree has the path $S, X, S, X, S, B$ to the last letter $b$ of the inner $ab$. Going up from the bottom, the first repeated label is $S$: the lower $S$ derives $ab$ and the upper $S$ derives $aabb$. So $u = a$, $v = a$, $x = ab$, $y = b$, $z = b$, and $u v^i x y^i z = a^{i+2} b^{i+2}$, which is in the language for every $i \ge 0$.

**Example: $\{a^n b^n c^n : n \ge 0\}$ is not context-free.** Suppose $p$ is a pumping length and take $s = a^p b^p c^p$. Since $|v x y| \le p$, the window $v x y$ touches at most two of the three blocks. If $v$ or $y$ contains two different letters, $u v^2 x y^2 z$ is not of the form $a^* b^* c^*$. Otherwise $v$ and $y$ each lie in one block, at least one is nonempty, and some block is untouched, so $u x z$ has unequal counts. A script checks that for $p = 1, \ldots, 6$ no split survives both $i = 0$ and $i = 2$.

**Example: $\{w w : w \in \{a, b\}^*\}$ is not context-free.** Take $s = a^p b^p a^p b^p$ and pump down to $u x z$, of length $4p - m$ with $m = |v y|$; it can be a square only if $m$ is even. A window of length at most $p$ lies inside the first half, inside the second half, or within the middle $b^p a^p$. If it lies in the first half, $u x z = t\, a^p b^p$ with $|t| = 2p - m$, so its first half is $t\, a^{m/2}$, ending with $a$, and its second half is $a^{p - m/2} b^p$, ending with $b$. The second half is symmetric. In the middle case $u x z = a^p b^j a^l b^p$ with $j + l = 2p - m$; a square $w w$ of this form would need $w$ to start with $a^p$ and end with $b^p$, so $|w| \ge 2p$, but $|w| = 2p - m/2$. A script confirms that no split survives $i = 0$ and $i = 2$ for $p \le 5$.

**Example: primes.** $\{a^q : q \text{ prime}\}$ is not context-free. Take a prime $q \ge p$ and $s = a^q = u v x y z$ with $m = |v y| \ge 1$. Then $u v^i x y^i z$ has length $q + (i - 1) m$, and for $i = q + 1$ this is $q (1 + m)$, a product of two factors at least 2.

## Consequences

- **Non-context-free languages.** The lemma shows that $\{a^n b^n c^n\}$, $\{w w\}$, $\{a^{n^2}\}$ and $\{a^q : q \text{ prime}\}$ are not context-free, and so it separates the context-free languages from the context-sensitive ones.
- **Closure fails.** From $\{a^n b^n c^n\}$ not being context-free it follows that the context-free languages are not closed under intersection or complement; see [closure properties](/cfl-closure-properties/).
- **Emptiness and finiteness by length.** $L$ is nonempty if and only if it contains a string of length less than $p$, since a shortest string of length at least $p$ could be pumped down. $L$ is infinite if and only if it contains a string $s$ with $p \le |s| < 2p$: such a string pumps up forever, and if $L$ is infinite, a shortest string of length at least $p$ cannot have length $2p$ or more, since pumping down removes at most $p$ letters. This gives simple but slow decision procedures; the [emptiness](/cfg-emptiness-problem/) and [finiteness](/cfg-finiteness-problem/) tests use the same idea on the grammar directly in linear time.
- **Ogden's lemma.** A stronger form lets one *mark* positions of $s$: if at least $p$ positions are marked, there is a split in which $v y$ contains a marked position and $v x y$ contains at most $p$ marked positions. The proof is the same, following a path that keeps the most marked leaves below it. Ogden used it to prove [inherent ambiguity](/inherent-ambiguity/), for example of $\{a^i b^j c^l : i = j \text{ or } j = l\}$.
- **Linear languages.** For a [linear grammar](/linear-grammar/), the repeated nonterminals can be taken near the root, which gives a split with $|u v y z| \le p$ instead of $|v x y| \le p$.

## Tightness

- **The pumping length.** The bound $2^k$ is close to the best possible in terms of the number $k$ of nonterminals. The grammar $A_0 \to a$, $A_{j+1} \to A_j A_j$ for $j < k - 1$, with start symbol $A_{k-1}$, is in Chomsky normal form with $k$ nonterminals and generates the single string $a^{2^{k-1}}$. A finite language has no pumpable string, since pumping up gives infinitely many strings, so its pumping length is $2^{k-1} + 1$.
- **The converse is false.** The language $L = \{a^i b^j c^l d^m : i = 0 \text{ or } j = l = m\}$ satisfies the lemma with $p = 1$: pump the first letter of the string, which changes only the number of $a$'s, or only the first block if $i = 0$. A script checks this for the 237 strings of $L$ of lengths 1 to 9 with $i = 0, \ldots, 4$. Yet $L$ is not context-free: its intersection with the regular language $a b^* c^* d^*$ is $\{a b^n c^n d^n\}$, and erasing the $a$ by a homomorphism gives $\{b^n c^n d^n\}$, so closure under these operations would make that language context-free. Ogden's lemma, with the $b$'s, $c$'s and $d$'s marked, also shows it directly.
- **One letter.** Over a one-letter alphabet the context-free languages are exactly the regular ones, by [Parikh's theorem](/parikh-theorem/), so there the lemma says no more than the [pumping lemma for regular languages](/pumping-lemma-for-regular-languages/).

## History

Bar-Hillel, Perles and Shamir proved the lemma in 1961, in the paper that also proved that context-free languages are closed under intersection with regular languages and that their emptiness and finiteness are decidable. Ogden published the marked version in 1968 to prove inherent ambiguity. The proof by Chomsky normal form and the bound $2^k$ is the presentation of Hopcroft, Motwani and Ullman.

## References
