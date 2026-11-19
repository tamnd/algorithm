---
tag: CTEH7D
kind: algorithm
slug: token-passing
name: Token passing
aliases:
- token passing model
area: natural-language-and-speech/speech-recognition
level: core
summary: Young's view of Viterbi decoding over a network of HMMs, where tokens holding scores and word histories move along arcs each frame.
model: word-ram
complexity:
  vars: {n: the number of frames, s: the number of HMM states in all word arcs, a: the number of word arcs}
  time: {worst: "O(n (s + a))"}
  space: {extra: "O(s + n a)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1989
  people: [Steve J. Young, N. H. Russell, J. H. S. Thornton]
  note: Young, Russell and Thornton described connected word recognition at Cambridge in 1989 as tokens passed around a transition network, which made the one-pass algorithm easy to extend to several alternatives and to syntax networks, and it became the decoder model of HTK.
prereqs: [viterbi-algorithm, hidden-markov-model, pronunciation-lexicon]
see_also: [time-synchronous-beam-search, stack-decoding, word-lattice, hclg-decoding-graph, beam-search, forced-alignment, n-gram-language-model, automatic-speech-recognition]
sources:
  - url: https://www.semanticscholar.org/paper/c10d5841e923bd607cc3b396fbf5bc4bd776878c
    title: Steve J. Young, N. H. Russell and J. H. S. Thornton, Token passing, a simple conceptual model for connected speech recognition systems, technical report CUED/F-INFENG/TR38, Cambridge University Engineering Department, 1989
    locator: the abstract (connected word recognition as passing tokens around a transition network, and its extension to several alternatives and syntax constraints)
  - paper: doi:10.1109/79.790984
    title: Hermann Ney and Stefan Ortmanns, Dynamic programming search for continuous speech recognition, IEEE Signal Processing Magazine 16(5), 1999, pages 64 to 83
    locator: the section on time-synchronous beam search, which computes the same scores
---

Token passing is a way to describe and build the Viterbi search of a connected speech recognizer, due to Young, Russell and Thornton 1989. The recognizer is a network: grammar nodes joined by word arcs, and each word arc is a copy of the HMM of the word. A token is a score with a link to the word history. At each frame every HMM state takes the best token offered by its predecessors and adds its emission score. When a token leaves a word, the decoder writes a word link record, and the token moves to the next grammar node. With no pruning it finds the best path, the same one as [time-synchronous Viterbi beam search](/time-synchronous-beam-search/): the two are the same search, written as messages on a network or as a list of active hypotheses.

## In plain words

Think of the recognizer as a map of rooms. Each word is a row of rooms, one for each sound, and the grammar says which word rows follow which. Each frame, every room holds at most one token, a slip that says how good the best way into this room is and which words that way went through.

At the next frame, each token is copied to the rooms it can reach, and each copy adds the cost of the move and how well the new room fits the sound. A room that gets several copies keeps the best. When a token leaves the last room of a word, you write down the word, and the token carries a pointer to that note. At the end, the best token at an end room points back to all its words.

## The problem

The input is a word network, a lexicon, and $n$ frames of acoustic scores. The network has grammar nodes, which do not emit, a start node, final nodes with a log score, and word arcs $(src, dst, w, g)$, where $g$ is a log grammar or language model score. A word arc is a left-to-right HMM for the phones of $w$. The task is the path through the network and through the HMM states that maximizes

$$\log p_{ac} + \lambda \log p_{lm} + |W| \log ip,$$

where $\log p_{ac}$ is the sum of the emission and transition log scores, $\log p_{lm}$ the sum of the $g$ of the arcs and the final score, $\lambda$ the language model weight and $ip$ the word insertion penalty. $\lambda$ and $ip$ are tuned heuristics.

In the code each phone is one state with a self loop of log probability $\ell$ and a forward move of log probability $f$, and the exit from a word is a forward move too. A bigram is the network with one node per previous word.

## The algorithm

```pseudo id=main
TOKEN-PASSING(N, e, n)
L1  node(start) ← (0, no link); all other tokens are empty
L2  for t ← 0 to n - 1 do
L3      for each word arc a and state j: tok(a, j) ← best of tok(a, j) + ℓ, tok(a, j - 1) + f, and, for j = 0, node(src(a)) + λ g(a) + log ip; then add e_t(j)
L4      PRUNE: drop the tokens with a score below best - beam
L5      clear the node tokens
L6      for each arc a with a token in its last state: s ← tok + f; write a link (w(a), t, s, link of tok); node(dst(a)) ← the better of node(dst(a)) and (s, new link)
L7  return the best node(q) + λ final(q) over final q, and follow its links back
```

Line L3 is the step inside the HMMs, line L6 the step between words. A grammar node keeps only the best token that reaches it at each frame. This is the Viterbi recombination, and it is right because everything after the node depends only on the node.

## Example

The network has a start node and a final node, joined by two word arcs: $AB = (a, b)$ and $CD = (c, d)$, with $g = 0$ and a final score of 0. Take $\lambda = 1$, $\log ip = 0$ and $\ell = f = \ln 0.5 \approx -0.693$. The emission scores are $e_0 = (a{:}{-1}, c{:}{-2})$ and $e_1 = (b{:}{-5}, d{:}{-1})$, and $-9$ for every other phone.

| frame | $a$ | $b$ | $c$ | $d$ | word links |
|---|---|---|---|---|---|
| 0 | $-1$ | none | $-2$ | none | none |
| 1 | $-10.693$ | $-6.693$ | $-11.693$ | $-3.693$ | $AB$ at $-7.386$, $CD$ at $-4.386$ |

At frame 1 the final node gets two offers and keeps $CD$ at $-4.386$. This is the same table of scores as in the example of time-synchronous beam search, entry by entry: the two searches differ only in how they are written down.

With a beam of 0.5, line L4 drops the token in $c$ at frame 0, and the search returns $AB$ at $-7.386$, which is worse than the best path by 3. A beam of 1.0 keeps it and finds $CD$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By induction on $t$, the token of state $j$ of arc $a$ at frame $t$ holds the best score of any partial path that is in that state at that frame, and the token of a node holds the best score of any partial path that has just left a word into it. A partial path in a state came from the same state, from the state before it, or from the source node of the arc, and the score it adds depends only on where it came from, so the best partial path extends one of the three best tokens. At the last frame, the best final node token, plus its final score, is the best full path.

For a bigram network, every path is a word sequence with a segmentation, and its score is the one that time-synchronous beam search gives it: token passing adds the language model score when a word starts and beam search adds it when the word ends, but the sum is the same. With no pruning both return the maximum of the same function, so they find the same best path. With a beam, both can miss it, and they need not miss in the same way, since the language model score enters the beam at different times.

## Complexity

Let $n$ be the number of frames, $s$ the number of HMM states in all word arcs and $a$ the number of word arcs. At each frame, line L3 looks at each state once, with at most three offers, and line L6 looks at each arc once. That is $O(s + a)$ per frame and $O(n (s + a))$ in all, without pruning. With pruning, only the states that hold a token cost time.

The extra space is $O(s)$ for the tokens of one frame and $O(n a)$ for the word link records, since each frame writes at most one record per arc that ends a word.

## Properties

- **Exact without pruning.** It computes the Viterbi path of the whole network.
- **Same search as beam search.** With the same network and no pruning, it returns the same best path as [time-synchronous Viterbi beam search](/time-synchronous-beam-search/).
- **Online.** Each frame is read once, in order.
- **Local.** Each state needs only its own token and the tokens of its predecessors, so the network can be any graph: a fixed grammar, a loop of words, or a bigram.
- **History in the token.** The word link records hold the word history, so the HMM states do not need back pointers per frame.

## Variants and improvements

- **N-best tokens.** Keep the best few tokens per state, with different word histories, to output several hypotheses or a [word lattice](/word-lattice/). This was one of the extensions in Young, Russell and Thornton 1989.
- **Pruning.** A global beam, a narrower beam at word ends, and a limit on the number of active models.
- **Context-dependent models.** Make the word arcs from [triphone models](/triphone-model/), with cross-word context on the arcs between words.
- **Precompiled networks.** A WFST decoder runs the same token passing over an [HCLG decoding graph](/hclg-decoding-graph/), where the arcs carry HMM states instead of whole words.
- **Forced alignment.** With a network that is one chain of words, token passing becomes [forced alignment](/forced-alignment/).

## When to use it

Use it to build a decoder for any network of HMMs, from a small command grammar to a bigram over a large vocabulary, especially when the network is fixed and you want simple code. It is the model behind the HTK recognizer. For large vocabularies with long language model histories, a prefix tree with tree copies or a precompiled graph keeps the network smaller.

## Pitfalls

- **Wrong network for the language model.** Recombination at a node is right only if the future depends only on the node. A single node for all word ends with a bigram applied later would merge tokens with different futures.
- **Lost alternatives.** Keeping one token per state gives only the best path. A lattice needs several tokens per state.
- **Tokens in loops of null nodes.** If the network has arcs between grammar nodes with no HMM, tokens must be passed through them in an order with no cycle in one frame.
- **Search errors from pruning.** As in the example, a narrow beam can drop the right word at the first frame.

## Implementations

The Python code runs token passing over a network of word arcs with one-state phones, a beam and word link records, and builds the network of a bigram. The tests compare the best score with exhaustive search over all arc paths of at most 5 words and all their segmentations on random networks with cycles, check the bigram network, check that the example fails with a beam of 0.5 and works with 1.0, check that pruning never gives a better score, and check that the links hold a history with a repeated word.

## History

Vintsyuk, then Bridle, Brown and Chamberlain, and Ney, had described one-pass dynamic programming for connected words before 1989. Young, Russell and Thornton wrote it in 1989 as a simple model: tokens passed around a transition network. The model made it easy to add several alternatives per state and syntax networks, and it became the decoder design of the HTK toolkit. Later WFST decoders, such as the one in Kaldi, still describe their Viterbi beam search as passing tokens over a graph.

## References
