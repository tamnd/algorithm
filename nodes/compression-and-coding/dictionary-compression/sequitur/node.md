---
tag: ZP2YY9
kind: algorithm
slug: sequitur
name: Sequitur
aliases:
- SEQUITUR
- Nevill-Manning-Witten algorithm
area: compression-and-coding/dictionary-compression
level: advanced
summary: Online grammar inference that enforces digram uniqueness and rule utility, a heuristic for the smallest grammar.
model: word-ram
complexity:
  vars: {n: the input length}
  time: {expected: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1997
  people: [Craig G. Nevill-Manning, Ian H. Witten]
  note: Published in the Journal of Artificial Intelligence Research and in The Computer Journal in 1997, with the proof of linear time.
prereqs: [grammar-based-compression, hash-table, doubly-linked-list]
see_also: [straight-line-program-grammar, smallest-grammar-problem, re-pair, byte-pair-encoding, lz78, smallest-grammar-np-hardness, context-free-grammar, compressed-indexing]
sources:
  - paper: doi:10.1613/jair.374
    title: Craig G. Nevill-Manning and Ian H. Witten, Identifying hierarchical structure in sequences, a linear-time algorithm, Journal of Artificial Intelligence Research 7, 1997, pages 67 to 82
    locator: the two constraints (digram uniqueness and rule utility), the algorithm with its digram index, and the proof that it runs in linear time
  - paper: doi:10.1093/comjnl/40.2_and_3.103
    title: Craig G. Nevill-Manning and Ian H. Witten, Compression and explanation using hierarchical grammars, The Computer Journal 40(2/3), 1997, pages 103 to 116
    locator: Sequitur as a compressor and as a tool to show structure in text, music and DNA
  - paper: doi:10.1109/TIT.2005.850116
    title: Moses Charikar, Eric Lehman, Ding Liu, Rina Panigrahy, Manoj Prabhakaran, Amit Sahai and abhi shelat, The smallest grammar problem, IEEE Transactions on Information Theory 51(7), 2005
    locator: Section III (the remark that the lower bound for Sequential extends to Sequitur) and Section VI-C (Sequential, Theorem 7, the lower bound Omega(n^(1/3)))
---

Sequitur is an on-line [grammar-based compression](/grammar-based-compression/) algorithm. It reads a string one symbol at a time and keeps a [straight-line program](/straight-line-program-grammar/) for the prefix read so far, with two invariants: no pair of adjacent symbols (a *digram*) appears twice in the grammar, and each rule is used at least twice. Each new symbol can break an invariant, and a short chain of local repairs restores both. With a [hash table](/hash-table/) of digrams and [doubly linked lists](/doubly-linked-list/) for the rules, the total time is linear in expectation. Like [Re-Pair](/re-pair/), it is a heuristic for the [smallest grammar problem](/smallest-grammar-problem/).

## In plain words

Read a text letter by letter and keep a set of rules that can rebuild it. Each time two neighbouring letters appear a second time somewhere in the rules, give them a name: write a new rule "name means these two", and put the name in both places. If a rule with exactly these two letters already exists, use its name instead of making a new one.

The second rule says that a name must be used at least twice. If a name is used only once, it does not save anything, so put its letters back where the name was and delete it. Each new letter needs only a few such fixes, and at the end the rules rebuild the whole text.

## The problem

The input is a string $w = w_1 \cdots w_n$, given one symbol at a time. After each symbol $w_t$, the output is a grammar $G$ with start rule $S$ whose expansion is $w_1 \cdots w_t$. The size $|G|$ is the total length of the right-hand sides. Sequitur does not promise the smallest size. It promises two properties of $G$ after each symbol:

- **digram uniqueness:** no digram has two occurrences in the right-hand sides that do not overlap (in aaa the two copies of aa overlap, so aaa is allowed);
- **rule utility:** each rule other than $S$ is used at least twice.

## The algorithm

```pseudo id=main
APPEND(c)                                   ▷ called once for each input symbol c
L1  link a new node that holds c at the end of the start rule S
L2  REPAIR()
REPAIR()
L3  while some new digram is not checked or some rule has one use do
L4      if a rule r has exactly one use then
L5          put the right-hand side of r in place of that use, delete r
L6      else take a new digram x; m ← an occurrence of it that does not overlap x
L7          if m exists then MATCH(x, m)
MATCH(x, m)
L8  if m or x is the whole right-hand side of a rule R then replace the other one by R
L9  else make a new rule R whose right-hand side is a copy of the digram
L10     replace m and x by R
```

Each rule is a circular doubly linked list with a guard node, so a digram can be cut out and a nonterminal linked in with $O(1)$ pointer changes. A hash table maps each digram to the nodes where it starts. Each time a link between two symbols is made, its left node goes on a work list of new digrams, and the link is added to the hash table. Line L6 takes a node from that list and looks up the digram. When several stored occurrences qualify, it prefers one that is a whole rule, so that line L8 reuses the rule and does not make a copy of it.

Line L8 covers the case where the digram is already the whole right-hand side of a rule $R \to ab$: the other occurrence becomes $R$. If $x$ is the whole rule, the code checks $x$ again afterwards, because a third occurrence may still wait on the list. Lines L9 and L10 make a new rule and replace both occurrences. Each replacement removes one use of each symbol in the digram, so a rule can drop to one use; line L4 sees this before any other work and line L5 puts the rule back in place. Each replacement and each expansion makes new digrams, which go on the list, so one input symbol can start a short chain of repairs.

## Example

Take $w$ = abcdbcabcd. The first five symbols contain no repeated digram, so $S$ = abcdb.

| symbol | event | grammar after the repairs |
|---|---|---|
| a b c d b | no repeat | $S \to$ abcdb |
| c (6th) | bc occurs twice: lines L9 and L10 make $R_1 \to$ bc | $S \to a R_1 d R_1$, $R_1 \to$ bc |
| a, b (7th, 8th) | no repeat | $S \to a R_1 d R_1 ab$ |
| c (9th) | bc occurs in $S$ and is the whole rule $R_1$: line L8 | $S \to a R_1 d R_1 a R_1$ |
| | $a R_1$ now occurs twice: lines L9 and L10 make $R_2 \to a R_1$ | $S \to R_2 d R_1 R_2$, $R_2 \to a R_1$ |
| d (10th) | $R_2 d$ occurs twice: lines L9 and L10 make $R_3 \to R_2 d$ | $S \to R_3 R_1 R_3$ |
| | $R_2$ has one use left, in $R_3$: line L5 expands it | $R_3 \to a R_1 d$ |

The final grammar is $S \to R_3 R_1 R_3$, $R_1 \to$ bc, $R_3 \to a R_1 d$, with size $3 + 2 + 3 = 8$. Rule $R_3$ has length 3: rule utility lets rules grow longer than 2.

**Runs.** On aaa the grammar is $S \to$ aaa, because the two copies of aa overlap. On aaaa the two copies at positions 1 and 3 do not overlap, and Sequitur makes $S \to R_1 R_1$, $R_1 \to$ aa.

## Correctness

Each change of the grammar keeps the expansion of each rule: a replacement puts a nonterminal in place of the digram it stands for, and an expansion puts the right-hand side in place of the nonterminal. So $S$ always expands to the prefix read so far. Rule utility holds at the end of a call because each rule whose use count falls to 1 goes on a list that line L4 handles first. Digram uniqueness holds because each new link is checked by line L6 after it is made, and the last check of each surviving digram found no other occurrence. The full proof is in [the correctness proof](proofs/correctness.md). It assumes that line L8 never meets two occurrences that are both whole rules; the paper does not treat this case, the code raises an error if it happens, and the tests never meet it.

## Complexity

Count the changes of the grammar over $n$ symbols. Line L1 adds 1 to $|G|$. A replacement in line L8 lowers $|G|$ by 1. Lines L9 and L10 keep $|G|$ the same and add a rule. An expansion in line L5 lowers $|G|$ by 1 and removes a rule. Since $|G| \ge 0$, there are at most $n$ replacements in line L8 and expansions together. Each rule has length at least 2, which bounds the number of new rules by $n$. So the total number of changes is at most $2n$, and each makes $O(1)$ new links and $O(1)$ work list entries.

- The time is $O(n)$ expected, because each step does $O(1)$ hash table operations. The search of line L6 looks at the stored occurrences of one digram; between two repairs only a few new occurrences of a digram can exist, and on all inputs of the tests this list never held more than 4 nodes. Nevill-Manning and Witten prove the linear bound.
- The time for one symbol is not $O(1)$ in the worst case, since one symbol can start a chain of repairs. The bound is amortized over the input.
- The space is $O(n)$: the grammar, the hash table and the work lists each hold $O(n)$ items. In practice this is several machine words per symbol of the grammar.

## Properties

- **On-line.** After each symbol the grammar is complete for the prefix read so far. This is the main difference from [Re-Pair](/re-pair/), which needs the whole input.
- **Rules of any length.** Rules start with length 2 and can grow when line L5 expands a rule inside another one, as $R_3 \to a R_1 d$ in the example.
- **Deterministic.** The output depends only on the input and on the fixed order of the work lists.
- **No deep recursion.** The repairs run from two work lists, not from recursive calls, and the expansion of the grammar uses an explicit stack.
- **Approximation ratio.** Charikar et al. (2005) prove a lower bound $\Omega(n^{1/3})$ on the approximation ratio of the closely related algorithm Sequential of Kieffer and Yang, and state that it extends to Sequitur. They give no upper bound for Sequitur itself.

## Variants and improvements

- **Sequential.** Kieffer and Yang proposed an algorithm in the same spirit that appends, at each step, the longest prefix of the remaining input that is the expansion of an existing rule. Its grammars are *irreducible*, and Charikar et al. bound its ratio by $O((n / \log n)^{3/4})$.
- **Encoding.** For compression, the grammar must be written as bits, for example with [arithmetic coding](/arithmetic-coding/) of the symbols of the rules. Nevill-Manning and Witten give such an encoding; this page builds only the grammar.
- **Other units.** The same method works on words, lines or any other tokens instead of characters.
- **Off-line methods.** [Re-Pair](/re-pair/) and [byte-pair encoding](/byte-pair-encoding/) choose the most frequent pair over the whole input, which often gives smaller grammars when the whole input is available.

## When to use it

Use Sequitur when the input arrives as a stream and a grammar must be ready after each symbol, or when the goal is to show the repeated structure of a sequence, for example phrases in text, motifs in DNA or themes in music, which is how Nevill-Manning and Witten used it. Do not use it when the whole input is available and a small grammar matters most; Re-Pair then usually does better. For general file compression, an LZ77 compressor is faster and simpler.

## Pitfalls

- **Counting overlapping digrams.** In aaa the two copies of aa overlap. If line L6 accepts an overlapping occurrence, Sequitur tries to replace both and breaks the string. The test must reject a node $m$ that is $x$, the node before $x$, or the node after $x$.
- **A stale hash table.** Each change of a link must first remove the old digram from the hash table. If a removed digram stays in the table, line L6 can match a digram that no longer exists.
- **Not tracking the use counts.** Each time a replacement removes a use of a rule, the code must test whether one use is left and, if so, put the rule on the list of line L4. If it does not, a rule with one use stays in the grammar, rule utility fails, and the grammar is larger than it needs to be.
- **Making a duplicate rule.** If line L6 does not prefer an occurrence that is a whole rule, lines L9 and L10 make a second rule with the same right-hand side, and digram uniqueness fails.
- **Forgetting a third occurrence.** When $x$ is the whole rule in line L8, only $m$ is replaced. Another occurrence of the digram can still exist, so $x$ must be checked again.
- **Recursion.** A direct version calls the digram check from inside each replacement, which is a recursion as deep as the chain of repairs. On long inputs this can overflow the call stack; use work lists, as the code here does for line L3.

## Implementations

## History

Craig Nevill-Manning and Ian Witten developed Sequitur at the University of Waikato and published it in 1997, in the Journal of Artificial Intelligence Research, with the proof of linear time, and in The Computer Journal, as a compressor and as a tool to show hierarchical structure. Kieffer and Yang gave a related algorithm with irreducible grammars at about the same time. Charikar et al. (2005) studied Sequitur and these algorithms as approximation algorithms for the smallest grammar problem.

## References
