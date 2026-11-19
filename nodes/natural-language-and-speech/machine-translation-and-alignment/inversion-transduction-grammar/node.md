---
tag: 8BXTRR
kind: model
slug: inversion-transduction-grammar
name: Inversion transduction grammar
aliases:
- ITG
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Wu's synchronous grammar in binary normal form whose rules keep or invert the order of two children, biparsing a sentence pair in time cubic in each sentence length.
history:
  year: 1997
  people: [Dekai Wu]
  note: Wu (1997) defined inversion transduction grammars and their stochastic form, gave the normal form with straight and inverted binary rules, and used a dynamic program over pairs of spans to align and bracket parallel sentences. ITG constraints were later used to limit the reordering of phrase-based decoders and to restrict word aligners.
prereqs: [synchronous-context-free-grammar]
see_also: [permutation, word-alignment, probabilistic-cky, inside-outside-algorithm, chomsky-normal-form, lexicalized-reordering-model, hierarchical-phrase-based-translation, phrase-based-stack-decoding]
sources:
  - paper: "Dekai Wu, Stochastic inversion transduction grammars and bilingual parsing of parallel corpora, Computational Linguistics 23(3), 1997, pages 377 to 403"
    title: Wu 1997
    locator: the straight and inverted rules, the normal form, the stochastic model, the biparsing algorithm and the reorderings an ITG can express
  - paper: "Prosenjit Bose, Jonathan F. Buss and Anna Lubiw, Pattern matching for permutations, Information Processing Letters 65(5), 1998, pages 277 to 283"
    title: Bose, Buss and Lubiw 1998
    locator: separable permutations and their characterization as the permutations that avoid the patterns 2413 and 3142
---

An inversion transduction grammar (ITG) is a [synchronous context-free grammar](/synchronous-context-free-grammar/) whose rules have at most two children, and each binary rule either keeps the order of its children on the target side (a *straight* rule) or reverses it (an *inverted* rule). Wu (1997) showed that every ITG has a normal form like [Chomsky normal form](/chomsky-normal-form/), and that the best joint parse of a source sentence of $m$ words and a target sentence of $l$ words can be found in $O(m^3 l^3)$ time, which gives a [word alignment](/word-alignment/) and a bracketing of both sentences together. The reorderings an ITG can produce are exactly the separable permutations: all orders for up to three words, and 22 of the 24 orders of four words.

## The machine

**Direction and notation.** The source is $f = f_1 \ldots f_m$ and the target $e = e_1 \ldots e_l$. Spans are fencepost: $(s, t)$ covers $f_{s+1} \ldots f_t$ and $(u, v)$ covers $e_{u+1} \ldots e_v$. Probabilities are multiplied, or their natural logs added.

**Rules in normal form.** With nonterminals $X, Y, Z$, a source word $x$ and a target word $y$:

| rule | written | source side | target side |
|---|---|---|---|
| straight | $X \to [Y \; Z]$ | $Y \; Z$ | $Y \; Z$ |
| inverted | $X \to \langle Y \; Z \rangle$ | $Y \; Z$ | $Z \; Y$ |
| word pair | $X \to x / y$ | $x$ | $y$ |
| source word only | $X \to x / \varepsilon$ | $x$ | nothing |
| target word only | $X \to \varepsilon / y$ | nothing | $y$ |

A *stochastic* ITG gives each rule a probability, with the rules of each left side summing to 1. The *bracketing* ITG has one nonterminal $A$ and only the rules $A \to [A \, A]$, $A \to \langle A \, A \rangle$ and the word rules; it knows no syntax and only constrains which reorderings are possible.

**Reachable orders.** Consider one-to-one translations, where target word $k$ translates source word $\pi(k)$. A tree of straight and inverted nodes produces $\pi$ exactly when $\pi$ can be built by splitting the source into two adjacent blocks whose translations are also adjacent, in the same or the reverse order, and splitting each block again, down to single words. Such permutations are called separable.

**Example.** For four words, the target order 2 1 4 3 comes from $[\langle 1 \, 2 \rangle \, \langle 3 \, 4 \rangle]$: two inverted pairs side by side. The order 2 4 1 3 has no first split. Cutting the source after word 1 leaves the words 2, 3, 4 at the target positions 1, 4 and 2, which are not adjacent; cutting after word 2 puts the words 1 and 2 at the target positions 3 and 1; cutting after word 3 puts the words 1, 2 and 3 at the positions 3, 1 and 4. So no ITG derivation gives this order, and the same holds for 3 1 4 2. The orders 2 4 1 3 and 3 1 4 2 are the *inside-out* alignments, which occur in real data but rarely.

## What it counts

The model counts derivations, each with a probability, and the main computation is *biparsing*: the best (or the total) probability of a derivation that yields $f$ and $e$ together. Let $\beta(X, s, t, u, v)$ be the best probability that $X$ derives the source span $(s, t)$ and the target span $(u, v)$. Then

$$\beta(X, s, t, u, v) = \max \Big\{ \max_{X \to [Y Z],\, S,\, U} p \, \beta(Y, s, S, u, U) \, \beta(Z, S, t, U, v), \; \max_{X \to \langle Y Z \rangle,\, S,\, U} p \, \beta(Y, s, S, U, v) \, \beta(Z, S, t, u, U) \Big\},$$

with $s \le S \le t$ and $u \le U \le v$, the word rules as base cases, and the answer $\beta(S, 0, m, 0, l)$. In the straight case $Y$ takes the left parts of both spans; in the inverted case $Y$ takes the left source part and the right target part. There are $O(m^2 l^2 |N|)$ items, each with $O(m l)$ split pairs and $O(|N|^2)$ rules, so the time is $O(m^3 l^3 |N|^3)$ and the space $O(m^2 l^2 |N|)$ on the [word RAM](/word-ram/). For the bracketing ITG, $|N| = 1$ and the time is $O(m^3 l^3)$, which is $O(n^6)$ when both sentences have $n$ words. Replacing max by sum gives the inside probabilities, and with the outside probabilities the [inside-outside algorithm](/inside-outside-algorithm/) trains a stochastic ITG by expectation maximization.

For translation, the target is unknown. Parsing only the source with the source side of the grammar costs $O(m^3)$ times the grammar size, as in [CKY](/probabilistic-cky/); an n-gram language model on the target makes each item also hold the boundary words of its target string, which keeps decoding polynomial for a fixed vocabulary but much slower.

## Relation to other models

- **Synchronous CFG.** An ITG is an SCFG of rank 2 in normal form. Wu (1997) showed that an ITG with longer straight and inverted rules can be put in this normal form, and rank 3 SCFGs give no new translations, so the rank 2 SCFGs and the ITGs describe the same translations.
- **Hiero.** [Hierarchical phrase-based](/hierarchical-phrase-based-translation/) rules have up to two nonterminals, so Hiero is a rank 2 SCFG, but its rules carry whole phrases around the gaps and are learned from data instead of being binary word-level rules.
- **Phrase-based reordering.** In a [stack decoder](/phrase-based-stack-decoding/), the ITG constraint allows a phrase order only if it is separable. The [lexicalized reordering model](/lexicalized-reordering-model/) has the same two basic classes, monotone and swap, but only for neighbouring phrases.
- **Word alignment models.** The [IBM models](/ibm-model-1/) and the [HMM model](/hmm-alignment-model/) allow any alignment. A bracketing ITG restricts the alignment to separable structure, which excludes the inside-out patterns but also many bad alignments.
- **Monolingual parsing.** With an empty target side, the biparsing program becomes the CKY program for one sentence; the extra factors $l^3$ come from the second sentence.

## Known results in the model

- **Separable permutations (theorem).** The one-to-one orders an ITG produces are the separable permutations, which are the permutations that contain neither 2 4 1 3 nor 3 1 4 2 as a pattern (Bose, Buss and Lubiw 1998).
- **Their count (theorem).** For $n = 1, \ldots, 6$ words there are 1, 2, 6, 22, 90 and 394 separable permutations, the large Schröder numbers, out of $n! = 1, 2, 6, 24, 120, 720$. The large Schröder numbers grow like $c^n$ times a power of $n$ with $c = 3 + 2\sqrt 2 \approx 5.83$, while $n!$ grows faster than any $c^n$, so the fraction of all orders that an ITG can produce goes to 0 as $n$ grows.
- **Spurious ambiguity (theorem).** Different trees can give the same order. For three words there are 2 tree shapes, each with 4 labelings of its two inner nodes as straight or inverted, so 8 trees but only 6 orders: $[[1\,2]\,3]$ and $[1\,[2\,3]]$ both give 1 2 3. A normal form that prefers one branching direction for nodes of the same kind removes this ambiguity, which matters when counting or summing over derivations.
- **Biparsing in $O(m^3 l^3)$ (theorem).** By the program above. For general SCFGs of unbounded rank the problem is NP-hard (see the [SCFG page](/synchronous-context-free-grammar/)).
- **Coverage (measurement).** Studies of hand-aligned parallel text found that the separable orders cover most of the reordering for the language pairs studied, and that the inside-out patterns are real but rare.
- **Decoding constraint (measurement).** Zens and Ney (2003) compared the ITG constraint with other reordering constraints for word-based decoding and found that it covered the reordering in their data better than the IBM constraints.

## References
