---
tag: RFRPXP
kind: technique
slug: grammar-constrained-decoding
name: Grammar-constrained decoding
aliases:
- structured generation
- guided generation
area: natural-language-and-speech/text-generation-and-decoding
level: research
summary: "Mask at each step the tokens that cannot extend the output to a string of a given regular or context-free language, tracked by an automaton."
prereqs: [autoregressive-decoding, deterministic-finite-automaton, context-free-grammar]
see_also: [regular-expression, earley-parser, pushdown-automaton, lr-parsing, trie, grid-beam-search, rejection-sampling, nucleus-sampling]
sources:
  - url: https://arxiv.org/abs/2307.09702
    title: "Brandon T. Willard and Rémi Louf, Efficient guided generation for large language models, arXiv 2307.09702, 2023"
    locator: "the reformulation of guided generation as transitions of a finite-state machine, the index from each state of the machine to the tokens of the vocabulary that keep the output in the language, and the extension to context-free grammars with a parser"
  - paper: doi:10.18653/v1/2023.emnlp-main.674
    title: "Saibo Geng, Martin Josifoski, Maxime Peyrard and Robert West, Grammar-constrained decoding for structured NLP tasks without finetuning, EMNLP 2023, pages 10932 to 10952"
    locator: "the use of formal grammars, including grammars that depend on the input, to constrain the output of a language model for information extraction, entity disambiguation and constituency parsing"
  - url: https://arxiv.org/abs/2405.21047
    title: "Kanghee Park, Jiayu Wang, Taylor Berg-Kirkpatrick, Nadia Polikarpova and Loris D'Antoni, Grammar-aligned decoding, NeurIPS 2024"
    locator: "the observation that grammar-constrained decoding distorts the distribution of the model, the definition of grammar-aligned decoding as sampling from the model conditioned on the grammar, and the ASAp algorithm"
---

Grammar-constrained decoding makes a [language model](/language-model/) produce only strings of a given formal language, such as the strings that match a [regular expression](/regular-expression/), the valid JSON objects of a schema, or the programs of a [context-free grammar](/context-free-grammar/). It runs an automaton for the language beside the decoder. At each step of [autoregressive decoding](/autoregressive-decoding/) it sets the logit of every token to $-\infty$ if appending that token leaves no way to complete the output inside the language, and allows the end token only when the output is already in the language. Any decoder then runs on the masked logits: greedy, beam search or sampling. The output is then always in the language, if the language has a string of the allowed length. But the method does not sample from the model conditioned on the output being in the language. It renormalizes one token at a time, and Park et al. 2024 show that this can change the probabilities of the valid strings by a large factor.

## In plain words

Suppose a program needs the model to answer with a date, a number, or a JSON object, and nothing else. At each step, before the model picks the next piece of text, look at every piece it could pick and cross out the ones that would break the required format for good. The model then picks among the pieces that are left. The answer always has the right format. The catch is that the model may be pushed into a format it would rarely choose, and then must finish it in whatever way is still allowed, so the answers are not always the ones the model likes best among valid ones.

## When it applies

The output must belong to a language that a program can check one prefix at a time. For a regular language a [deterministic finite automaton](/deterministic-finite-automaton/) does this: a prefix is good when its state can still reach an accepting state. For a context-free language a [pushdown automaton](/pushdown-automaton/), an [LR parser](/lr-parsing/) or an [Earley parser](/earley-parser/) does it: a prefix is good when some string of the language starts with it. The decoder must give access to the logits, or at least accept a mask on the vocabulary, at every step. Use it for tool calls, JSON output, code in a fixed syntax, and labels from a fixed set. Do not expect it to make the content correct: it fixes the form only.

## The template

Let $A$ be a deterministic automaton for the language $L$ over characters, with start state $q_0$. A state is live if an accepting state can be reached from it. A token is a string of characters, so $\delta^*(q, t)$ runs $A$ over the characters of $t$.

```pseudo id=main
CONSTRAINED-DECODE(model, A, n)          ▷ n = the largest number of tokens
L1  q ← q_0;  y ← the empty sequence
L2  for i ← 1 to n do
L3      z ← the next-token logits of the model for y
L4      for each token t ≠ end: if δ*(q, t) is undefined or not live then z[t] ← −∞
L5      if q is not accepting then z[end] ← −∞
L6      t ← choose a token from z     ▷ greedy, sampling, top-k, nucleus, ...
L7      if t = end then return y
L8      y ← y · t;  q ← δ*(q, t)
L9  return y
```

Lines L4 and L5 do not depend on the model, only on $q$. Willard and Louf 2023 compute, once for each state $q$ of $A$, the set of tokens allowed at $q$ and the state after each of them. Decoding then needs one table lookup per step in place of a scan of the vocabulary with the automaton. The table costs time proportional to the number of states times the total length of the token strings, which is often done in a [trie](/trie/) of the vocabulary. For a context-free language the state includes a stack or a parse chart, which can grow without bound, so the allowed sets cannot all be precomputed. Parsers then combine a table for the regular part of the grammar (the tokens of its lexer) with a check of the parser stack at each step.

## Classic examples

**Integers without leading zeros.** The regular expression `0|[1-9][0-9]*` has three useful states: the start $s$, the state $z$ after "0" (accepting, and no digit may follow), and the state $d$ after a nonzero digit (accepting, digits may follow). Take the tokens "0", "7", "05", "70", "x" and end. At $s$ the allowed tokens are "0", "7" and "70"; "05" is crossed out because no digit may follow "0", "x" is crossed out, and end is crossed out because $s$ is not accepting. At $d$ all four digit tokens and end are allowed. At $z$ only end is allowed. A tokenizer splits the text into pieces that do not follow the grammar, which is why line L4 runs the automaton over all the characters of each token.

**The distortion.** Let $L = \{\text{aa}, \text{b}\}$ and let the model give the first token a with probability 0.9 and b with 0.1. After a it gives end with 0.99 and a with 0.01; after aa or b it gives end. The model gives the string aa probability $0.9 \times 0.01 = 0.009$ and b probability 0.1, so conditioned on $L$ it gives aa probability $0.009 / 0.109 = 0.083$ and b probability 0.917. Constrained sampling allows both a and b at the first step, since a can still become aa, and keeps their weights 0.9 and 0.1. After a, only a is allowed, and it gets probability 1. So constrained sampling returns aa with probability 0.9, more than ten times the conditioned value. The model has put almost all of its weight on the string "a", which is not in $L$, and the mask moves that weight to the only valid way to finish the prefix.

**Structured tasks.** Geng et al. 2023 wrote grammars for the outputs of information extraction, entity disambiguation and constituency parsing, some built from the input of each example, and used them to constrain a model that was not fine-tuned for these tasks.

## Variations

- **Regular languages with an index.** The approach of Willard and Louf, used in the Outlines library: a table from each automaton state to the allowed tokens. JSON schemas are often compiled to a regular expression first.
- **Context-free grammars with a parser.** An LR or Earley parser tracks the prefix and answers whether each token keeps it viable.
- **A fixed set of answers.** A [trie](/trie/) of the allowed answers is the automaton: each node allows only its child tokens.
- **Constraints on words, not form.** [Grid beam search](/grid-beam-search/) forces given words to appear, which is a different kind of constraint and is tracked by a count, not an automaton.
- **Grammar-aligned decoding.** Park et al. 2024 define the goal as sampling from the model conditioned on $L$, and give ASAp (adaptive sampling with approximate expected futures), which samples many times and uses the results to correct its estimate of the probability that each prefix can be completed in $L$, so that the samples move toward the conditioned distribution.
- **Rejection.** Sample without a mask and reject outputs outside $L$. This samples exactly from the conditioned distribution, as in [rejection sampling](/rejection-sampling/), but it can need very many samples when the model rarely writes valid strings.

## Pitfalls

- **The distribution changes.** Masking token by token is not conditioning on the whole string (the second example). For greedy use this is often acceptable; for sampling, and for scores that use the probabilities, it is not the model's distribution.
- **Tokenization.** The model learned one way to split each text into tokens. The mask can force a split it never saw, for example a quote mark and a word as two tokens where the model always used one, which can lower the quality. Prompts that end in the middle of a token have the same problem.
- **Dead ends with a length limit.** The automaton guarantees a completion in some number of steps, not within $n$. If the output must be short, the live test must also count the steps left.
- **End of text.** If line L5 is left out, the model can stop before the output is in the language; if the end token is never allowed in an accepting state, it can never stop.
- **Form, not content.** A valid JSON object can still hold wrong values. A strict format can also lower accuracy on the task by keeping the model from writing its reasoning first.

## Exercises

1. Build the automaton for `0|[1-9][0-9]*` and list the allowed tokens at each state for the tokens "0", "7", "05", "70", "x" and end.
2. Show that if $L$ is not empty and lines L4 and L5 never leave all tokens masked, the output of CONSTRAINED-DECODE without a length limit, when it stops, is in $L$.
3. In the distortion example, find model probabilities for which constrained sampling gives aa a probability 100 times its conditioned value.
4. Show that rejection sampling returns a string of $L$ with exactly the model's conditioned probability, and give its expected number of samples.
5. Explain why the allowed sets of a context-free language cannot all be precomputed, using the language of balanced parentheses.

## References
