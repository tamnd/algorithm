---
tag: 635TD2
kind: algorithm
slug: language-model-watermarking
name: Green list watermark for language models
aliases:
- Kirchenbauer watermark
- LLM output watermarking
area: security-and-privacy/adversarial-machine-learning
level: research
summary: "Biases generation toward a pseudorandom green list of tokens seeded by the previous token, and detects the watermark by a z-test on green counts."
model: real-ram
complexity:
  vars: {T: the number of tokens, V: the vocabulary size, c: the cost of one call of the language model}
  time: {generate: O(T (c + V)), detect: O(T V)}
  space: {extra: O(V + T)}
properties: {deterministic: false, exact: false, online: true, recursive: false}
history:
  year: 2023
  people: [John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, Tom Goldstein]
  note: Kirchenbauer et al. (ICML 2023) proposed the green list watermark with a z-test detector that needs only the key, not the model; Christ, Gunn and Zamir (COLT 2024) gave watermarks that cannot be detected without the key.
prereqs: [language-model, z-test, pseudorandom-function]
see_also: [z-test, hoeffding-inequality, pseudorandom-function, random-oracle-model, language-model, temperature-sampling, shannon-entropy, message-authentication-code]
sources:
  - url: https://proceedings.mlr.press/v202/kirchenbauer23a.html
    title: John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers and Tom Goldstein, A watermark for large language models, ICML 2023, PMLR 202, pages 17061 to 17084
    locator: Algorithm 1 (hard red list) and Algorithm 2 (soft red list), the z-test with the threshold z = 4, the spike entropy and Theorem 4.2 on the expected green count, and the advice not to count repeated n-grams (arXiv:2301.10226)
  - url: https://arxiv.org/abs/2306.09194
    title: Miranda Christ, Sam Gunn and Or Zamir, Undetectable watermarks for language models, COLT 2024, PMLR 247, pages 1125 to 1139
    locator: the definition of an undetectable watermark and the construction from a pseudorandom function
  - paper: "Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58, 1963"
    locator: the tail bound for sums of independent bounded variables, and its extension to sampling without replacement
---

The green list watermark of Kirchenbauer et al. (2023) marks the text that a language model generates, so that a detector with a secret key can later tell, with a known false-positive rate, whether a text came from the marked model. Before each token is drawn, a hash of the key and the previous token splits the vocabulary into a green list of $\gamma |V|$ tokens and a red list of the others, and the logits of the green tokens get a bonus $\delta$. Plain text has about a fraction $\gamma$ of green tokens, and marked text has more. The detector counts the green tokens among $T$ scored tokens and computes the z-score $z = (|s|_G - \gamma T) / \sqrt{T \gamma (1 - \gamma)}$. It needs the key, but not the model and not the prompt.

**Threat model.** The watermark is a defense for provenance. The adversary wants to remove the mark from a marked text (so it is not detected) or to put the mark on a text that the model did not write (so it is wrongly detected). The adversary does not know the key but can read marked texts. The capability is to edit tokens of a text, by insertion, deletion or substitution. The guarantee against false accusation is a theorem; the robustness against edits is a bound for a given number of edits, and a heuristic for paraphrase.

## In plain words

Think of the vocabulary as a deck of cards. Before each word, a secret key and the previous word shuffle the deck, and a quarter of the cards are painted green. The model is gently pushed to pick a green word, but it can still pick any word.

A person who writes text without the key picks green words about a quarter of the time, by chance. Text from the marked model has many more green words. A checker with the key repaints the cards for each position, counts the green words and asks how surprising the count is. A count far above a quarter is strong evidence of the mark.

The mark is weak when the model has almost no choice, for example in a fixed phrase, because then the push changes nothing.

## The problem

Given a language model $p(\cdot \mid s_{<t})$ over a vocabulary $V$, generate text whose distribution is close to $p$, such that a detector with a key $k$ flags generated texts of enough length and enough entropy, and flags a text that does not depend on $k$ with probability at most a chosen small number. The detector sees only the tokens $s_0, s_1, \dots, s_T$, where $s_0$ is the last token of the prompt.

## The algorithm

```pseudo id=main
GENERATE(p, s_0, T, gamma, delta, k)
L1  for t ← 1 to T do
L2      z ← the logits of p for the next token after s_0, ..., s_{t-1}
L3      G ← GREEN-LIST(k, s_{t-1}, gamma)
L4      for each v ∈ G do z[v] ← z[v] + delta
L5      s_t ← a draw from softmax(z)
L6  return s_1, ..., s_T
GREEN-LIST(k, u, gamma)
L7  r ← a generator seeded with H(k, u)                 ▷ H is a keyed hash
L8  return ⌊gamma |V|⌋ tokens of V drawn by r without replacement
DETECT(s_0, ..., s_T, gamma, k, z*)
L9  count ← 0, scored ← 0, seen ← ∅
L10 for t ← 1 to T do
L11     if (s_{t-1}, s_t) ∈ seen then continue            ▷ score each pair once
L12     seen ← seen ∪ {(s_{t-1}, s_t)}, scored ← scored + 1
L13     if s_t ∈ GREEN-LIST(k, s_{t-1}, gamma) then count ← count + 1
L14 z ← (count - gamma' · scored) / sqrt(scored · gamma' (1 - gamma'))   ▷ gamma' = ⌊gamma |V|⌋ / |V|
L15 return (z, z > z*)
```

GENERATE is Algorithm 2 of the paper, the soft red list. Line L2 asks the model for its logits. Lines L3 and L4 raise the logits of the green tokens by $\delta$, which multiplies their probabilities by $e^\delta$ before the softmax normalizes them again. Line L5 draws the token as usual, so the model can still pick a red token when it is very sure of it. Lines L7 and L8 make the green list a function of the key and the previous token only, so the detector can rebuild it from the text.

DETECT does not call the model. Lines L11 and L12 skip a pair (previous token, token) that was already scored: a repeated pair has the same green status every time, so counting it again would add no evidence and would break the independence that the z-test needs. Line L14 is the one-proportion [z-test](/z-test/) against the green fraction $\gamma'$ of plain text.

## Example

Take a toy bigram model over $|V| = 64$ integer tokens, with logits drawn from $N(0, 1)$ by a fixed seed, $\gamma = 0.25$ (16 green tokens per context) and $\delta = 2$. After the token 0, the green mass of the model is $q = 0.179$. Line L4 raises it to $e^2 q / (e^2 q + 1 - q) = 0.617$.

A marked text of 12 tokens after $s_0 = 0$ has 11 green tokens. Plain text would have about 3, and line L14 gives $z = (11 - 3) / \sqrt{12 \cdot 0.25 \cdot 0.75} = 8 / 1.5 = 5.33$, above the threshold $z^* = 4$.

The table is a measurement on this toy model: 20 texts of $T = 200$ tokens for each $\delta$, all with the same key.

| $\delta$ | mean green fraction | mean $z$ | smallest $z$ |
|---|---|---|---|
| 0 (no mark) | 0.246 | -0.13 | -1.44 |
| 1 | 0.466 | 6.78 | 5.00 |
| 2 | 0.671 | 13.05 | 11.35 |
| 4 | 0.938 | 20.68 | 19.92 |

The z-score grows like $\sqrt T$ for a fixed green fraction: with half of the tokens green, $z = 2.66$ at $T = 25$, $4.08$ at $T = 50$, $5.77$ at $T = 100$ and $8.16$ at $T = 200$. So short texts cannot be flagged with confidence.

## Correctness

**Theorem (false positives).** Model $H$ as a random function, so the green lists of different previous tokens are independent, uniformly random sets of size $\lfloor \gamma |V| \rfloor$. Let the text $s_0, \dots, s_T$ not depend on the key. Then DETECT returns true with probability at most $e^{-2 z^{*2} \gamma' (1 - \gamma')}$ for every threshold $z^* > 0$.

**Lemma (the bonus helps).** If the green mass of the model at a step is $q$, the green mass after line L4 is $e^\delta q / (e^\delta q + 1 - q) \ge q$, with equality only for $q \in \{0, 1\}$.

**Lemma (edits).** Changing $m$ tokens of a text lowers the count of line L13 by at most $2m$.

The theorem is proved by grouping the scored pairs by the previous token. Within a group the scored tokens are distinct, so their green indicators are a sample without replacement from the vocabulary; across groups they are independent. Hoeffding showed that a sum of draws without replacement satisfies the same tail bound as independent draws, so $P(\mathrm{count} - \gamma' N \ge a) \le e^{-2a^2/N}$ for $N$ scored pairs; the choice $a = z^* \sqrt{N \gamma'(1 - \gamma')}$ gives the bound. For $\gamma = 0.25$ and $z^* = 4$ the bound is $e^{-6} = 0.0025$, a theorem. The paper gives $3 \times 10^{-5}$, the one-sided normal tail at 4, which is the right value for large $T$ by the [central limit theorem](/central-limit-theorem/) but not a finite-sample guarantee. The edit lemma holds because a token at position $p$ enters only the pairs at positions $p$ and $p + 1$. The full proof is in `proofs/correctness.md`.

The power of the test is a separate theorem of the paper (Theorem 4.2): if the average spike entropy $S(p, \zeta) = \sum_v p_v / (1 + \zeta p_v)$ of the steps is at least $S^*$, with $\zeta = (1 - \gamma)(e^\delta - 1) / (1 + (e^\delta - 1)\gamma)$, then the expected number of green tokens is at least $\gamma e^\delta T S^* / (1 + (e^\delta - 1)\gamma)$. Low entropy gives a weak mark.

## Complexity

- **Generation.** One call of the model per token, as without the mark, plus $O(|V|)$ for the hash, the green list and the bonus: $O(T(c + |V|))$. The green list of $\lfloor \gamma |V| \rfloor$ tokens costs $O(\gamma |V|)$ with a partial shuffle.
- **Detection.** $O(T |V|)$ time, or $O(T)$ hash calls if the test of line L13 asks the generator only whether $s_t$ is green. It needs no model and no GPU.
- **Space.** $O(|V| + T)$, for the logits, one green list and the set of seen pairs.

## Properties

- **Keyed detection.** Without the key, the green lists look random, so a reader cannot see the mark by counting. With the key, the test is a plain z-test.
- **Bounded false positives.** For a text that does not depend on the key, the false-positive rate is at most $e^{-2 z^{*2}\gamma'(1-\gamma')}$ (the theorem). This covers human text, under the model of $H$ as a random function.
- **Quality cost.** The mark changes the output distribution. A larger $\delta$ gives a stronger mark and a larger change, which can lower quality. It is not distortion-free.
- **Entropy dependence.** The mark is strong only where the model has a real choice. Code, lists and fixed phrases carry a weak mark (the lemma and Theorem 4.2).
- **Local robustness.** Each edit lowers the count by at most 2, so many edits are needed to remove the mark from a long text. Paraphrase by another model can still remove it, a heuristic limit found in later work.
- **Context width.** A green list seeded by only one previous token can be learned by an adversary who sees many marked texts and counts which pairs are frequent; a wider context makes this harder but makes edits hurt more.

## Variants and improvements

- **Hard red list.** Algorithm 1 of the paper forbids red tokens completely. The mark is stronger, but low-entropy text suffers, because the best token may be red.
- **Wider or private context.** The paper also seeds the green list with more than one previous token, and with a pseudorandom function of the key, to make the lists harder to learn.
- **Undetectable watermarks.** Christ, Gunn and Zamir (2024) use a [pseudorandom function](/pseudorandom-function/) to embed the mark so that, without the key, no efficient test can tell marked text from unmarked text; the output distribution is unchanged in that computational sense.
- **Distortion-free sampling.** Other schemes replace the bonus by a keyed choice of the random numbers of line L5, so each token has the model's own distribution, and detect by the correlation of the tokens with those numbers.
- **Unique scoring.** Lines L11 and L12 follow the later advice of the paper to not count repeated n-grams. Without them, a text that repeats a green pair many times gets a z-score far too high.

## When to use it

Use it when the provider of a model wants to detect its own output later, for example to label generated text or to filter it from future training data, and can keep a key secret. It needs control of the sampling step, so it does not apply to models that others run. Do not use it as proof of authorship of short or low-entropy texts, and do not treat a missing mark as proof that a human wrote a text, because edits and paraphrase can remove it.

## Pitfalls

- **Too short a text.** At line L14 the z-score grows like $\sqrt T$, so a text of 25 tokens with half of them green gives only $z = 2.66$. Set a minimum length before flagging.
- **Counting repeated pairs.** If lines L11 and L12 are removed, a repeated phrase is counted many times and can give a large $z$ for human text. Score each pair once.
- **Using $\gamma$ when $\gamma |V|$ is not a whole number.** Line L8 takes $\lfloor \gamma |V| \rfloor$ tokens, so line L14 must use $\gamma' = \lfloor \gamma |V| \rfloor / |V|$; otherwise the z-score is biased.
- **The normal tail as a guarantee.** The value $3 \times 10^{-5}$ at $z^* = 4$ is the normal approximation. For a guaranteed rate, use the Hoeffding bound or an exact binomial tail.
- **A weak hash at line L7.** If the green list depends on a public or guessable seed, anyone can detect or forge the mark. The key must be secret, and $H$ should be a keyed function such as a [message authentication code](/message-authentication-code/).
- **Testing many keys or many windows.** Each extra test raises the chance of a false alarm; the threshold must account for every test that is run.

## Implementations

The code of this page is an abstract model on synthetic data. The language model is a seeded table of bigram logits over 64 integer tokens, built with `mlkit.softmax`, and there is no real text and no real model. The tests check that the green lists have the right size and depend on the key, the z-score values, that marked texts of 200 tokens are flagged, that plain texts and a wrong key are not flagged, that the false-positive rate over 600 random keys stays under the Hoeffding bound, that repeated pairs are scored once, that the bonus never lowers the green mass, that peaked models carry a weaker mark, that the mean green mass meets the spike entropy bound of Theorem 4.2, and that 20 edits lower the count by at most 40.

## History

Watermarks for text existed before language models, for example by the choice of synonyms, but they changed the text after it was written. Kirchenbauer, Geiping, Wen, Katz, Miers and Goldstein posted the green list watermark in January 2023 (ICML 2023). Its main ideas were to change the sampling step, not the text, and to detect with a z-test that needs only the key. They proved the bound on the expected green count through the spike entropy, and measured the effect on quality and the robustness to edits on an open model. Christ, Gunn and Zamir (COLT 2024) gave a cryptographic definition of an undetectable watermark and a construction. Later work studied distortion-free schemes, robustness to paraphrase, and attacks that learn the green lists from many marked texts.

## References
