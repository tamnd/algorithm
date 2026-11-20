---
tag: 3QNB55
kind: algorithm
slug: hobbs-algorithm
name: Hobbs algorithm
aliases:
- Hobbs naive algorithm
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Resolve a pronoun by a fixed left-to-right, breadth-first walk of the parse trees of the current and earlier sentences, with agreement checks. A heuristic."
solves: [coreference-resolution]
model: word-ram
complexity:
  vars: {n: the number of nodes in the parse trees, h: the height of the tree of the current sentence}
  time: {worst: "O(n h)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1978
  people: [Jerry R. Hobbs]
  note: "Hobbs published the naive algorithm in Lingua in 1978, as a purely syntactic baseline next to a semantic method."
prereqs: [parse-tree, breadth-first-search, coreference-resolution]
see_also: [centering-theory, mention-pair-model, span-ranking-coreference, constituency-parsing, treebank, incremental-algorithm-referring-expressions]
sources:
  - paper: "Jerry R. Hobbs, Resolving pronoun references, Lingua 44(4), 1978, pages 311 to 338"
    title: Hobbs 1978
    locator: the naive algorithm on surface parse trees, and its evaluation by hand on pronouns from three texts
  - book: isbn:9780131873216
    title: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, 2nd edition, Prentice Hall, 2009"
    locator: "Chapter 21, Computational Discourse (the section on the Hobbs algorithm with its grammar fragment, the nine steps and a worked example)"
  - paper: "Shalom Lappin and Herbert J. Leass, An algorithm for pronominal anaphora resolution, Computational Linguistics 20(4), 1994, pages 535 to 561"
    title: Lappin and Leass 1994
    locator: the comparison of their salience-based method with the Hobbs algorithm on the same pronouns
  - paper: "Joel R. Tetreault, A corpus-based evaluation of centering and pronoun resolution, Computational Linguistics 27(4), 2001, pages 507 to 520"
    title: Tetreault 2001
    locator: the summary of the evaluation of Hobbs 1978, and a new evaluation of the Hobbs algorithm and centering methods on news and fiction text
---

The Hobbs algorithm finds the antecedent of a third person pronoun by walking the parse trees of the text in a fixed order and taking the first noun phrase that agrees with the pronoun in gender, number and person. It uses no meaning and no world knowledge, only the shape of the trees, so Hobbs called it the naive algorithm. It is a heuristic: the order of the walk encodes preferences for subjects, for nearby sentences and against antecedents inside the pronoun's own clause, and nothing guarantees that the first match is right. It solves only part of [coreference resolution](/coreference-resolution/): it handles pronouns and needs a parser, while the [mention-pair model](/mention-pair-model/) and the [span-ranking model](/span-ranking-coreference/) link all kinds of mentions. It remains a strong baseline for pronouns.

## In plain words

Start at the pronoun in its sentence tree. Climb up the tree, and at each level look at what lies to the left, row by row and left to right, as the reader would have met it. Skip noun phrases that are too close to the pronoun in its own clause, because "John likes him" cannot mean that John likes John. If nothing fits in the sentence, go back one sentence at a time and read each tree row by row, left to right. The first noun phrase with the right gender and number wins. Because the walk goes row by row, a subject is found before an object, and a near sentence before a far one.

## The problem

Input: the parse tree $T$ of the sentence that holds the pronoun, the parse trees $T_1, \ldots, T_q$ of the earlier sentences, the NP node $\pi$ of the pronoun, and agreement features (gender, number, person) on the NP nodes. The trees follow Hobbs's grammar fragment, as given by Jurafsky and Martin: S → NP VP; NP → (Det) Nominal (PP | Rel)* or pronoun; Det → determiner or NP 's; PP → preposition NP; Nominal → noun (PP)*; Rel → wh-word S; VP → verb NP (PP)*. The Nominal node is the N-bar of the original paper: the head noun with its modifiers, below the determiner. Output: an NP node that is the proposed antecedent, or none.

## The algorithm

```pseudo id=main
HOBBS(π, T, T_1 .. T_q)
L1  step 1: start at the NP node π that dominates the pronoun; go up the tree to the first NP or S node
L2  step 2: call that node X and the path from X down to π the path p
L3  step 3: walk all branches below X to the left of p, breadth first and left to right; propose each NP that has an NP or S node between it and X
L4  step 4: if X is the highest S node of the sentence, walk the trees of the earlier sentences, the most recent first, each breadth first and left to right, propose each NP, and stop
L5  step 5: from X, go up to the first NP or S node; call it X and the path to it p
L6  step 6: if X is an NP and p does not pass through the Nominal node that X directly dominates, propose X
L7  step 7: walk all branches below X to the left of p, breadth first and left to right; propose each NP
L8  step 8: if X is an S node, walk all branches below X to the right of p, breadth first and left to right, but do not go below any NP or S node; propose each NP
L9  step 9: go to step 4
L10 the answer is the first proposed NP that agrees with the pronoun in gender, number and person
```

The steps follow Jurafsky and Martin's statement of Hobbs (1978). A walk "below X to the left of p" passes through the path nodes but does not propose them, and it does not go below the node where the path ends; so each region of the tree is walked once. Hobbs also gave rules for reflexive pronouns and a semantic version with selectional constraints; the code and the steps above are the naive version.

Each step has a reason. Step 3 skips an NP that sits right next to the path in the smallest clause or NP around the pronoun: such an NP would be bound by the pronoun, which English allows only for reflexives. Step 6 does not propose an NP whose head part contains the pronoun, as "the Fords in his lot" for "his". Step 8 allows an antecedent to the right of the pronoun only in a higher clause and not inside a lower NP or S, which allows a few cases of cataphora.

## Example

Jurafsky and Martin use this text: "Bob opened up a new dealership last week. John took a look at the Fords in his lot. He ended up buying one."

Take "his" in the second sentence. Its NP is the determiner of "his lot".

1. Step 2: the first NP above the pronoun NP is "his lot". It is X, and the path goes through its Det node.
2. Step 3: there is nothing to the left of the path below "his lot".
3. Step 4: X is not the highest S. Step 5: climb through the PP "in his lot" and the Nominal "Fords in his lot" to the NP "the Fords in his lot", the new X.
4. Step 6: the path passes through the Nominal of this NP, so it is not proposed. "The Fords in his lot" cannot be what "his" refers to.
5. Step 7: below X to the left of the path there are only "the" and "Fords", no NP. Step 8: X is not an S.
6. Back to step 4, then step 5: climb through the PP "at the Fords in his lot" and the VP to the S of the second sentence.
7. Step 7: walk left of the path. The first row below S holds the NP "John" and the VP. "John" is proposed, it is masculine and singular like "his", and the algorithm returns it. A reader takes "his" to be Bob, whose dealership it is, so the algorithm errs here: its search prefers an NP of the same sentence and uses no knowledge of the world.

Now take "He" in the third sentence. It is the subject, so step 2 gives the S node, which is the highest S. Step 3 finds nothing to the left. Step 4 walks the second sentence breadth first: the first NP in the first row is "John", which agrees, so "He" is John. Jurafsky and Martin point out that the centering algorithm of Brennan, Friedman and Pollard picks Bob here instead (see [centering theory](/centering-theory/)); a reader picks John.

If the second sentence starts with "Mary" instead of "John", "his" no longer agrees with "Mary". The search proposes "Mary", then "a look" (neuter), and then it reaches step 4 at the top S and walks the first sentence, where the first NP is "Bob". For "John likes him" after "Bill arrived", the subject "John" is never proposed for "him", because step 3 needs an NP or S node between "John" and the S node, and there is none; the answer is "Bill". The test file checks all these cases.

## Correctness

The algorithm is a heuristic, so the proof in [proofs/correctness.md](proofs/correctness.md) shows only what the search does: each walk is breadth first and left to right over exactly the region of its step, the search ends after at most one pass per level of the tree plus one walk of each earlier tree, no node is proposed twice, the pronoun itself is never proposed, and the two filters of steps 3 and 6 hold. The test file compares the walk with an independent order (by depth, then by preorder position) on random trees.

## Complexity

Let $n$ be the number of nodes in the current and earlier trees and $h$ the height of the current tree. The regions of the walks are disjoint, so the walks visit each node at most once. Climbing from the pronoun to the root takes $O(h)$ steps over all passes. The test of step 3, which looks for an NP or S between a candidate and X, costs $O(h)$ per candidate in the code, so the total is $O(n h)$; carrying a flag down the walk makes it $O(n)$. In practice the search stops at the first agreeing NP, which is usually close. The parser that builds the trees costs far more than the search.

## Properties

- Heuristic: the search order encodes three preferences (antecedents to the left, closer sentences first, subjects before objects through the breadth-first order) and two syntactic filters. It does not optimize any score.
- Deterministic and syntax only: it needs parse trees and agreement features, and no training data.
- Measured accuracy (a measurement): Hobbs evaluated the naive algorithm by hand on 300 pronouns, 100 from each of three texts, and reported 88.3% correct, and 91.7% when selectional constraints were added; these are the figures as summarized by Tetreault (2001), and other summaries give rounded or different numbers. On a manual of computer documentation, Lappin and Leass (1994) found that their own salience-based method did better than the Hobbs algorithm on the same pronouns. Tetreault (2001) found 80.1% for the Hobbs algorithm on a set of fiction texts. Numbers from different texts and parsers are not comparable.
- Correct parses assumed: the original evaluation used hand-built trees. With parser output, errors in the tree become errors in the search.

## Variants and improvements

- Semantic constraints: Hobbs's own second method adds selectional checks, such as "the antecedent of it in it drove must be able to drive".
- Salience-based methods: Lappin and Leass (1994) give each candidate a weighted salience from its grammatical role, recency and parallelism, and pick the highest after filters.
- Centering: [centering theory](/centering-theory/) ranks the entities of the previous utterance by grammatical role and prefers the transition that keeps the same center; the algorithm of Brennan, Friedman and Pollard (1987) uses it for pronouns.
- Learned models: the Hobbs distance, the rank of a candidate in the Hobbs order, is a common feature of learned coreference models.

## When to use it

Use it as a baseline for pronoun resolution when you have constituency parses, or as a feature in a learned model. It needs no training data. For full coreference over all mention types, use a learned model such as the [span-ranking model](/span-ranking-coreference/).

## Pitfalls

- Trees without Nominal nodes: Penn Treebank trees have no N-bar level, so steps 3 and 6 need a convention for where the head part of an NP begins. Without one, step 6 proposes NPs that contain the pronoun.
- Agreement features are not given: gender and number must come from a lexicon or a model, and errors there are common for names and organizations.
- Pleonastic "it": in "it is raining" the pronoun has no antecedent, but the algorithm will propose one. Detect such pronouns first.
- Reflexives: "himself" needs its antecedent inside its clause, the opposite of step 3. Treat reflexives with a separate rule.
- Comparing accuracy: the original numbers come from hand-checked trees on three texts; they are not comparable with numbers on parsed news text.

## Implementations

## History

Hobbs (1978) proposed the naive algorithm as a baseline, to show how much a purely syntactic method could do, next to a semantic method of his own. Its high accuracy on his three texts made it the standard baseline that later pronoun resolution methods were measured against, including the centering method of Brennan, Friedman and Pollard (1987) and the salience method of Lappin and Leass (1994). It is still taught as the first pronoun resolution algorithm in textbooks such as Jurafsky and Martin.

## References
