---
tag: ZN2NZT
kind: algorithm
slug: grid-beam-search
name: Grid beam search
aliases:
- lexically constrained decoding
area: natural-language-and-speech/text-generation-and-decoding
level: advanced
summary: Beam search with one beam per count of satisfied constraint tokens, so that the output must contain given words or phrases.
solves: [autoregressive-decoding]
model: word-ram
complexity:
  vars: {n: the most output tokens, k: the beam width of one cell, c: the total number of constraint tokens, m: the number of phrases, V: "the vocabulary size |V|", M: the cost of one call of the model}
  time: {worst: "O(n k (c + 1) (M + V + m))"}
  space: {extra: "O(n k (c + 1) + V)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Chris Hokamp, Qun Liu]
  note: Hokamp and Liu introduced the grid for interactive and domain specific translation at ACL 2017. Post and Vilar 2018 replaced it by one beam split among the counts.
prereqs: [beam-search, autoregressive-decoding]
see_also: [grammar-constrained-decoding, diverse-beam-search, machine-translation, encoder-decoder-model, aho-corasick, top-k-selection, inadequacy-of-the-mode, length-normalization]
sources:
  - paper: doi:10.18653/v1/P17-1141
    title: Chris Hokamp and Qun Liu, Lexically constrained decoding for sequence generation using grid beam search, ACL 2017, pages 1535 to 1546
    locator: "Algorithm 1 (the grid), and Section 3.3 (the cost in model calls, linear in the number of constraint tokens)"
  - paper: doi:10.18653/v1/N18-1119
    title: Matt Post and David Vilar, Fast lexically constrained decoding with dynamic beam allocation for neural machine translation, NAACL 2018, pages 1314 to 1324
    locator: the dynamic beam allocation that keeps one beam of fixed size and splits it among the counts of met constraints
---

Grid beam search finds a probable output of an autoregressive model that contains a given set of words or phrases, for example the required terms of a glossary in [machine translation](/machine-translation/). A plain [beam search](/beam-search/) cannot do this by filtering at the end, because hypotheses that hold the phrases usually fall out of the beam early: forcing a word in costs probability now, and pays off only later. Hokamp and Liu 2017 keep a separate beam for each count of constraint tokens covered so far. A hypothesis competes only with hypotheses that have covered as much as it has, and only the cell that has covered all $c$ constraint tokens may finish. The cost is $c + 1$ beams in place of one, so the number of model calls grows linearly with $c$. It is a heuristic: with a finite beam it can miss the best output that holds the phrases, and the page shows such a case.

## In plain words

You want the model to write a text that uses some given words. If you just add the words to a normal search, the texts that contain them lose to texts that skip them, because a forced word looks unlikely at the moment you add it. So grid beam search sorts the partial texts into bins by how many of the required words they already hold. Texts only compete inside their own bin. At each step a text can add a free word and stay in its bin, or add the next required word and move up one bin. Only texts in the top bin, which hold every required word, may stop.

## The problem

The model gives $\log p(w \mid y)$ for every prefix $y$ and every token $w$ of the vocabulary $V$, which contains "</s>". All logs are natural logs. The constraints are $m$ phrases $P_1, \ldots, P_m$, each a non-empty sequence of tokens without "</s>", with $c = |P_1| + \cdots + |P_m|$ tokens in all. An output $y$ of at most $n$ tokens, "</s>" included, holds the constraints if each phrase appears in $y$ as a contiguous block and the $m$ blocks take disjoint positions. The task is

$$y^* = \arg\max \{ \log p(y) : y \text{ holds } P_1, \ldots, P_m \}.$$

This is a search problem over an exponential set, and grid beam search is a heuristic for it. A phrase may contain the same token as the free text; the search then has two ways to produce the same output, and both compete.

## The algorithm

A hypothesis is a prefix with its score, the set of phrases it has covered, and, if it is inside a phrase, which phrase and how far. A hypothesis inside a phrase is open; the others are closed. The cell $\text{Grid}[c']$ at step $t$ holds the hypotheses of $t - 1$ tokens of which $c'$ are constraint tokens.

```pseudo id=main
GRID-BEAM-SEARCH(model, P_1 .. P_m, n, k)
L1  Grid[0] ← { empty prefix, score 0, nothing covered };  Grid[c'] ← ∅ for c' > 0;  best ← none
L2  for t ← 1 to n do
L3      for c' ← 0 to c, for each hypothesis h in Grid[c'] do
L4          ℓ ← model(h.prefix)                         ▷ one call per hypothesis
L5          if h is closed and c' = c then best ← the better of best and h + "</s>"
            if t = n then continue                         ▷ no room for a token before "</s>"
            if h is closed then
L6              generate: for each w ≠ "</s>", put h + w with score + ℓ[w] into Next[c']
L7              start: for each phrase i not covered, put h + P_i[1] into Next[c' + 1]
            else
L8              continue: put h + the next token of its phrase into Next[c' + 1]
L9      for each c': empty Next[c'] if c' < c - (n - 1 - t), else keep its k best;  Grid ← Next
L10 return best                                          ▷ none if no output held every phrase
```

Line L9 drops cells that cannot reach $c$ covered tokens with the tokens that remain before "</s>". The code numbers the steps as the pseudocode does and counts the model calls.

## Example

Take the model M1 of [greedy decoding](/greedy-decoding/): at the empty prefix $p(a) = 0.5$, $p(b) = 0.4$, $p(\text{</s>}) = 0.1$; after a, $0.4, 0.3, 0.3$; after b, $0.05, 0.05, 0.9$; after two tokens, "</s>" has probability 1. Without constraints the best output is b</s> (0.36). Require the phrase "a", so $c = 1$, with $n = 3$ and $k = 1$.

- Step 1. The empty prefix (call 1) generates a ($-0.693$) and b ($-0.916$) into cell 0, and starts the phrase with a ($-0.693$) into cell 1. Each cell keeps one: a in cell 0, and the constraint a in cell 1.
- Step 2. The free a (call 2) generates aa and ab into cell 0 and starts the phrase: aa ($-1.609$) into cell 1. The constraint a (call 3) is closed in cell $c$, so it finishes a</s> ($\log 0.15 = -1.897$); it also generates aa ($-1.609$) and ab ($-1.897$) into cell 1. Cell 0 can no longer reach $c$ in time, so line L9 empties it. Cell 1 holds aa twice, one copy from each route, and keeps the first.
- Step 3. aa (call 4) finishes aa</s> ($\log 0.2 = -1.609$), better than a</s>.

The result is aa</s> with probability 0.2, after 4 calls, which is the best output that contains a. With the phrase "b" the search returns b</s> (0.36).

A narrow grid can fail. On a random model with tokens a, b, c and "</s>" (seed 0 in the test), the phrase "b c", $n = 5$ and $k = 1$, grid beam search returns b c </s> with log probability $-5.020$, but the best output that holds the phrase is a c b c </s>, with $-2.745$. A grid with an unbounded beam finds it. On 40 random models with $k = 1$ the narrow grid misses the best output on some of them and not on all; the test checks both.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It proves four facts. Every output returned holds all the phrases (soundness), because only closed hypotheses in cell $c$ finish and a hypothesis reaches cell $c$ only by placing every token of every phrase at disjoint positions. Line L9 drops only hypotheses that can no longer finish. With $k$ at least the size of every cell, the search enumerates every pair of an output and a placement of the phrases in it, so it returns the best output that holds the phrases: it is then an exhaustive search. And the number of model calls is at most $n k (c + 1)$.

With a finite $k$ the search is a heuristic, as the seed 0 case shows. The test compares it with exhaustive search over all outputs that hold the phrases.

## Complexity

The grid has $c + 1$ cells of at most $k$ hypotheses, so each step makes at most $k (c + 1)$ model calls, and $n$ steps make at most $n k (c + 1)$, the $O(k t c)$ of Hokamp and Liu (Section 3.3) with $t = n$. A closed hypothesis produces at most $|V| + m$ candidates and an open one produces one. Selecting the $k$ best of a cell takes linear time with [top-k selection](/top-k-selection/), so the time is $O(n k (c + 1) (M + |V| + m))$ for a call cost $M$ in the word RAM; the code sorts each cell, for clarity. The grid at one step holds $O(k (c + 1))$ hypotheses, each with a prefix of $O(n)$ tokens.

The calls in one step are independent, so a GPU runs them in one batch of $k (c + 1)$ prefixes. With many constraints this batch is large, which is the reason for the fixed-size beam of Post and Vilar 2018.

## Properties

- **Sound** (a theorem). Every output it returns holds every phrase.
- **Exact with an unbounded beam** (a theorem), and a heuristic with a finite beam (the seed 0 case).
- **Linear in the constraints.** The model calls grow as $c + 1$, not with the number of subsets of phrases.
- **Order free.** The phrases can appear in any order in the output; the search does not need an alignment to the input.
- **No output.** If no output of at most $n$ tokens holds the phrases, or the beam lost all of them, it returns nothing.

## Variants and improvements

- **Dynamic beam allocation.** Post and Vilar 2018 keep one beam of size $k$ for all counts and divide its slots among the counts at each step. The cost no longer grows with $c$.
- **Disjunctive constraints.** Allow a set of alternative phrases, for example the inflected forms of a term, and count the constraint as met when any one of them appears.
- **Negative constraints.** Forbid phrases by masking the token that would complete them. A matcher such as [Aho-Corasick](/aho-corasick/) over the forbidden phrases tracks the partial matches of a prefix.
- **Grammars.** [Grammar-constrained decoding](/grammar-constrained-decoding/) masks the tokens that a grammar or an automaton does not allow at each step, which also handles structure such as JSON.
- **Training with constraints.** Some systems copy the constraints into the input and train the model to use them. That moves the work from the search to the model, without a guarantee that the phrases appear.

## When to use it

Use grid beam search when certain words must appear and you can afford $c + 1$ times the work of a beam search: terminology in translation, interactive translation where a user fixes a word, or keywords in a generated description. With many constraints, or on a tight latency budget, use dynamic beam allocation. If the constraint is a format and not a list of phrases, use grammar-constrained decoding.

## Pitfalls

- **A cell that empties.** With a small $k$, the cell $c$ may hold nothing at the end, and the search returns no output even if one exists. Increase $k$ or $n$, or fall back to the unconstrained output.
- **Phrases in odd places.** The grid forces the phrases in but does not ask where they fit best; the model may put a phrase at the end, or repeat it, which hurts fluency. Measure the quality and not only the coverage.
- **Tokenization.** Constraints are lists of tokens. Tokenize each phrase the way the model tokenizes text in context, because a subword tokenizer can split the same word differently at the start of a sentence and inside it.
- **Length bias.** Outputs in the top cell are longer than free outputs, and raw log probabilities prefer short outputs; compare finished outputs with [length normalization](/length-normalization/).

## Implementations

The code takes the log probabilities of the model as given, as a function of the prefix, and implements the grid search around them; it does not run or train a network.

## History

Hokamp and Liu presented grid beam search at ACL 2017, for interactive post-editing and domain adaptation of neural [encoder-decoder](/encoder-decoder-model/) translation. Its cost grows with the number of constraint tokens, and Post and Vilar 2018 removed that growth with dynamic beam allocation.

## References
