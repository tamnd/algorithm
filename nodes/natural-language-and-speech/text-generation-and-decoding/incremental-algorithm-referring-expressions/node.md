---
tag: NEB4RM
kind: algorithm
slug: incremental-algorithm-referring-expressions
name: Incremental algorithm for referring expressions
aliases:
- Dale-Reiter incremental algorithm
area: natural-language-and-speech/text-generation-and-decoding
level: core
summary: Build a description of a target object by adding attributes in a fixed preference order whenever they rule out some distractor.
model: word-ram
complexity:
  vars: {p: the number of attributes in the preference list, m: the number of distractors}
  time: {worst: "O(p m)"}
  space: {extra: "O(p + m)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1995
  people: [Robert Dale, Ehud Reiter]
  note: Dale and Reiter proposed the algorithm in Cognitive Science in 1995 as a fast interpretation of the Gricean maxims that is closer to what people do than a search for the shortest description.
prereqs: [set-cover]
see_also: [greedy-set-cover, np-hard, natural-language-generation-pipeline, greedy-algorithm, garey-johnson-compendium]
sources:
  - paper: doi:10.1207/s15516709cog1902_3
    title: Robert Dale and Ehud Reiter, Computational Interpretations of the Gricean Maxims in the Generation of Referring Expressions, Cognitive Science 19(2), 1995, pages 233 to 263
    locator: "Section 2.2 (the set cover correspondence), Figure 2 in Section 3.1 (the costs of four interpretations), Figure 6 in Section 4.3 (the algorithm), Section 4.4 (the example), Section 4.5 (the run time)"
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: the greedy set cover heuristic
---

The incremental algorithm builds a description that picks out one object, the referent, from the other objects in the context, the distractors. It goes through the attributes in a fixed preference order, such as type, colour and size. It adds an attribute with the value of the referent when that property rules out at least one distractor that is still left, and it stops as soon as no distractor is left. Robert Dale and Ehud Reiter published it in 1995. It is the referring expression step of the microplanner in the [natural language generation pipeline](/natural-language-generation-pipeline/). The description it returns is correct but need not be the shortest, and finding the shortest one is [NP-hard](/np-hard/).

## In plain words

You want to say which dog you mean. There are two dogs and a cat in the room. Your dog is small and black, the other dog is large and white, and the cat is small and black.

Say first what kind of thing it is: "dog" rules out the cat. Then try the next attribute on your list. If the list says colour next, "black" rules out the white dog, and you say "the black dog". If the list says size next, "small" rules out the large dog, and you say "the small dog".

The algorithm never goes back. Once a word is in, it stays, even when a later word makes it unnecessary. People speak like this too: they often say more than they need, and they do not first search all short descriptions.

## The problem

The input is a referent $r$, a set $C$ of distractors and a preference list $P$ of attributes. Each object has a value for some of the attributes. A property $\langle A, V \rangle$ is true of $r$ when $r$ has the value $V$ for $A$, and it rules out a distractor $x$ when $x$ is known to have a value for $A$ that is not $V$. A description is a set $L$ of properties true of $r$, and it distinguishes $r$ when every distractor is ruled out by some property in $L$. The task is to find a distinguishing description, or to report that none exists. A short description is better, but the algorithm does not try to minimize the length.

## The algorithm

```pseudo id=main
MAKE-REFERRING-EXPRESSION(r, C, P)
L1  L ← {}
L2  for each attribute A in P, in order
L3      V ← the value of A for r
L4      R ← {x in C : the known value of A for x is not V}
L5      if R ≠ {}
L6          add <A, V> to L
L7          C ← C - R
L8      if C = {}
L9          add <type, r.type> to L if L has no type pair
L10         return L
L11 return failure
```

This is Figure 6 of the paper in its flat form. In the paper, line L3 calls FindBestValue, which can climb a taxonomy of values, for example from "chihuahua" to "dog", and picks the basic level value unless a more specific value rules out more distractors. Line L4 is RulesOut: a distractor is removed only when the hearer is known to believe that it does not have the property. Line L9 adds the type even when it rules out nothing, so that the result can be said as a noun phrase, "the black one" becoming "the black dog".

## Example

This is the example of Section 4.4 of the paper. The referent is Object1, a small black dog. The distractors are Object2, a large white dog, and Object3, a small black cat.

| step | attribute | value | ruled out | left |
|---|---|---|---|---|
| start | | | | Object2, Object3 |
| 1 | type | dog | Object3 | Object2 |
| 2 | colour | black | Object2 | none |

With $P$ = (type, colour, size) the result is {type: dog, colour: black}, "the black dog". With $P$ = (type, size, colour), step 2 uses size, "small" rules out Object2, and the result is "the small dog".

The result need not be minimal. Take the referent as before, and the distractors a small white cat and a large black cat. With $P$ = (colour, size, type), "black" rules out the white cat and "small" rules out the large cat, so the list is empty after two attributes, and line L9 adds the type: "the small black dog". The single property "dog" rules out both cats, so "the dog" is enough.

## Correctness

These are theorems, proved in full in the proofs file.

- **Soundness.** If the algorithm returns $L$, then every property in $L$ is true of $r$, and $L$ rules out every distractor. The invariant is that $C$ holds exactly the distractors that no property of $L$ rules out.
- **Completeness for $P$.** The algorithm fails exactly when the properties of $r$ for all attributes in $P$ together do not distinguish $r$. Once an attribute rules out a distractor, that distractor is gone, and no step brings it back.
- **No redundancy when added.** Each attribute pair except the final type pair rules out, at the time it is added, some distractor that no earlier pair ruled out. A later pair can still make an earlier one unnecessary.
- **No constant factor.** For every $k \ge 2$ there is an input where one property is enough and the algorithm returns $k$.
- **Hardness of the shortest description.** Deciding whether a distinguishing description with at most $s$ properties exists is NP-complete, by a direct reduction from [set cover](/set-cover/): one attribute per set, one distractor per element, and the distractor of element $u$ differs from $r$ on attribute $j$ exactly when $u$ is in set $j$.

Dale and Reiter (Section 2.2) state that a distinguishing description is a set cover, and cite Garey and Johnson for its NP-hardness. They do not write out a reduction, so the proofs file gives one.

That the incremental algorithm gives natural descriptions is a heuristic claim, which the paper supports with results from psycholinguistics. The algorithm optimizes nothing: it follows a fixed order and never revises a choice.

## Complexity

The loop runs at most $p = |P|$ times. Line L4 checks each remaining distractor once, with a hash table lookup for the attribute value, and line L7 removes the ruled out ones. So the worst case is $O(p\,n_d)$ time for $n_d$ distractors, and $O(p + n_d)$ extra space for $L$ and $C$. Section 4.5 of the paper notes that the run time is linear in the number of distractors and does not depend on the number of attributes the referent has.

Figure 2 of the paper compares four interpretations of the maxims, with $n_a$ the properties true of the referent, $n_d$ the distractors and $n_l$ the attributes in the final description:

| interpretation | complexity | typical run time |
|---|---|---|
| Full Brevity (Dale 1989) | NP-hard | about $n_a^{n_l}$ |
| Greedy Heuristic (Dale 1989) | polynomial | about $n_a n_d n_l$ |
| Local Brevity (Reiter 1990) | polynomial | about $n_a n_d n_l$ |
| Incremental Algorithm | polynomial | about $n_d n_l$ |

The estimate $n_d n_l$ for the incremental algorithm assumes that few attributes of $P$ are tried without being added.

## Properties

- **Deterministic and order dependent.** The output depends only on the order $P$. Different orders give different descriptions, as in the example.
- **Not minimal.** The output can be longer than the shortest description, with no constant bound on the ratio. This is by design: the paper argues that people also add properties that are not needed.
- **Never backtracks.** A property, once added, stays. This makes the algorithm fast and simple to implement.
- **Fails only when it must.** If the attributes in $P$ can distinguish the referent at all, the algorithm finds a description.
- **The type is always there.** Line L9 adds the type pair, so a noun is available for the noun phrase.

## Variants and improvements

- **Full Brevity.** Search the descriptions by size and return the shortest. This is exact and NP-hard; on small inputs a search over subsets of attributes, in $O(2^{n_a} n_d n_a)$ time, is fast enough. The tests use it as the reference.
- **Greedy Heuristic.** Add the property that rules out the most remaining distractors. This is Johnson's [greedy set cover](/greedy-set-cover/) algorithm, so its result is at most $H(n_d) \le 1 + \ln n_d$ times the shortest, where $H$ is the harmonic number. The code includes it.
- **Local Brevity.** Reiter (1990) starts from a description and replaces or removes properties while the result gets shorter.
- **Value taxonomies.** The full algorithm of the paper picks the value of each attribute from a taxonomy, with the basic level value preferred.
- **Relations and sets.** Later work extends the algorithm to relations between objects ("the cup on the table"), to sets of referents, and to negated or vague properties.

## When to use it

Use the incremental algorithm in a rule based generator when you need short, natural descriptions of objects in a known domain, and a fixed preference order of attributes is easy to state, for example type before colour before size. It is fast and predictable. If the shortest description matters, for example on a small screen, and the number of attributes is small, search the subsets instead. If the description must also say how objects relate to each other, use an algorithm that handles relations.

## Pitfalls

- **Missing values.** Treat a distractor with no known value for an attribute as not ruled out. Treating a missing value as "different" gives a description that the hearer cannot use.
- **Stopping before the check.** The check of line L8 must run after every attribute, also when the attribute is skipped. Skipping the check after an attribute that the referent does not have can make the algorithm fail on an input it can solve.
- **Empty preference list.** With $P$ empty the loop never runs and the algorithm fails, even when there are no distractors. Put at least the type in $P$.
- **Expecting minimality.** Do not use the algorithm where the shortest description is required. Its output can be much longer than needed.
- **Order of output.** The order of the pairs in $L$ is the order of $P$, not the order of words in the phrase. The realizer must order the adjectives and the noun.

## Implementations

## History

Dale (1989) had generated referring expressions in the EPICURE system by searching for the shortest description, with a greedy heuristic to make the search fast. Reiter (1990) proposed the Local Brevity interpretation. In their 1995 paper, Dale and Reiter compared these interpretations of Grice's maxims with experiments in psycholinguistics, which show that people often include properties that are not needed. They concluded that a simple, fast algorithm that does not try to minimize the description is both more efficient and closer to human behavior. The algorithm was used in the IDAS system and became the standard baseline for the generation of referring expressions.

## References
