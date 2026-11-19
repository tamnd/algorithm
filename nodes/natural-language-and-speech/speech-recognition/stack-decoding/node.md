---
tag: A0NEW4
kind: algorithm
slug: stack-decoding
name: Stack decoding
aliases:
- A* stack decoder
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Best-first search over partial word sequences ordered by score plus an estimate of the rest, extending the top of a priority queue.
model: word-ram
complexity:
  vars: {n: the number of frames, V: the vocabulary size, L: the largest number of phones in a word}
  time: {worst: "O(V^2 n^2 log(V n) + V n^2 L)"}
  space: {extra: "O(V^2 n^2)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1969
  people: [Frederick Jelinek, Lalit Bahl, Robert Mercer, Douglas B. Paul]
  note: Jelinek gave the stack algorithm for sequential decoding of codes in 1969, the IBM group used it for continuous speech recognition, and Paul described an optimal A* version of the stack decoder in 1990.
prereqs: [a-star-search, priority-queue, hidden-markov-model, n-gram-language-model]
see_also: [a-star-optimality, time-synchronous-beam-search, token-passing, phrase-based-stack-decoding, beam-stack-search, word-lattice, viterbi-algorithm, k-shortest-paths]
sources:
  - paper: doi:10.1147/rd.136.0675
    title: Frederick Jelinek, Fast sequential decoding algorithm using a stack, IBM Journal of Research and Development 13(6), 1969, pages 675 to 685
    locator: the stack algorithm for sequential decoding
  - paper: doi:10.1109/TPAMI.1983.4767370
    title: Lalit R. Bahl, Frederick Jelinek and Robert L. Mercer, A maximum likelihood approach to continuous speech recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence 5(2), 1983, pages 179 to 190
    locator: the discussion of decoding by stack search
  - url: https://aclanthology.org/H90-1041/
    title: Douglas B. Paul, Algorithms for an optimal A* search and linearizing the search in the stack decoder, Speech and Natural Language Workshop, Hidden Valley, 1990
    locator: the abstract and the stack decoder loop (pop the best theory, stop at the end of the sentence, extend by a short list of candidate words)
---

A stack decoder recognizes speech by a best-first search over partial sentences. Each entry of its "stack", which is a [priority queue](/priority-queue/), is a word sequence that explains the first $t$ frames, with its score. The decoder pops the entry whose score plus an estimate of the score of the remaining frames is largest, extends it by every possible next word, and pushes the results. It stops when it pops a complete sentence. If the estimate is an upper bound on the true rest, as in [A* search](/a-star-search/), the first complete sentence popped is the best one. Unlike [time-synchronous beam search](/time-synchronous-beam-search/), the search is not ordered by time: an entry that covers few frames can be extended before one that covers many.

## In plain words

Keep a list of half-finished guesses at the sentence. Each guess says which words explain the speech up to some point, and how well. To compare a short guess with a long one, add to each a hopeful estimate of how well the rest of the speech could go.

Always take the guess that looks best with its estimate, and try every next word on it. When the best-looking guess is a whole sentence, stop. If the estimate is never too low, nothing you skipped could have beaten it.

## The problem

The input is $n$ frames of acoustic scores $e_t$, a lexicon, and a bigram language model. As on the page for time-synchronous beam search, each phone is one HMM state with a self loop of log probability $\ell$ and a forward move of log probability $f$, also used for the word exit. The task is the word sequence $W$ and segmentation that maximize

$$\log p_{ac} + \lambda \log p_{lm}(W) + |W| \log ip,$$

with the start $\langle s \rangle$ and the end $\langle /s \rangle$ in $p_{lm}$. $\lambda$ and $ip$ are tuned heuristics.

A partial hypothesis $(w_1 \cdots w_k, t)$ covers the frames $0, \ldots, t - 1$, and its score $g$ is the best score of these words in these frames. The estimate $h(t)$ of the rest must satisfy, for A*, $g + h(t) \ge$ the score of every complete sentence that extends the hypothesis. The code uses

$$h(t) = \sum_{u = t}^{n - 1} \max_{\text{phone}} e_u(\text{phone}) + (n - t) \max(0, \log ip),$$

which is such a bound when the transitions and language model terms are log probabilities, so at most 0.

## The algorithm

```pseudo id=main
STACK-DECODE(lexicon, lm, e, n, h)
L1  push (words = (), t = 0, g = 0) with priority h(0)
L2  while the stack is not empty do
L3      pop the entry with the largest priority
L4      if it is complete then return it
L5      if (last word, t) is closed then skip it; otherwise close it
L6      for each word w and each end t' > t: g' ← g + seg(w, t, t') + λ log p(w | last) + log ip
L7          if t' = n then push it as complete with priority g' + λ log p(⟨/s⟩ | w)
L8          else push (words + w, t', g') with priority g' + h(t')
L9      if the stack holds more than max_stack entries then drop the worst
L10 return failure
```

$\mathrm{seg}(w, t, t')$ is the best score of $w$ in the frames $t, \ldots, t' - 1$, from a Viterbi pass through the phones of $w$. One pass from $t$ gives it for every $t'$, and the code keeps it in a table per $(w, t)$. The closed set of line L5 is a recombination: with a bigram, two hypotheses with the same last word and the same $t$ have the same future, so only the first one popped needs to be extended.

## Example

The lexicon has $x = (a)$, $y = (b)$ and $z = (c, d)$, all language model scores are 0, $\lambda = 1$, $\log ip = 0$, and $\ell = f = \ln 0.5 \approx -0.693$. There are two frames: $e_0 = (a{:}\,0, c{:}{-1})$ and $e_1 = (d{:}{-1})$, and every other emission is $-9$. Then $h(2) = 0$, $h(1) = -1$ and $h(0) = -1$.

| pop | entry | pushed (priority) |
|---|---|---|
| 1 | $()$ at $t = 0$, priority $-1$ | $x$ at $t = 1$ ($-0.693 - 1 = -1.693$), $z$ complete ($-3.386$), $x$ complete ($-10.386$), $y$ at $t = 1$ ($-10.693$), $y$ complete ($-19.386$) |
| 2 | $x$ at $t = 1$, priority $-1.693$ | $x\,x$ complete ($-10.386$), $x\,y$ complete ($-10.386$) |
| 3 | $z$ complete, $-3.386$ | stop |

The prefix $x$ looks best after the first expansion, because its first frame is perfect and the estimate of its second frame is optimistic. Its extensions are poor, so the complete $z$, with $-2 + 2 \ln 0.5 \approx -3.386$, rises to the top and is returned. It is the best sentence.

With a stack of size 1, line L9 keeps only $x$ after the first pop and drops $z$. The search then returns $x\,x$ with $-9 + 2 \ln 0.5 \approx -10.386$. A limited stack, like a narrow beam, can lose the best path.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The estimate is admissible: each frame can add at most its best emission, transitions and language model terms add at most 0, and at most $n - t$ more words fit. It is also consistent: extending by one word never raises $g + h$. So the priorities of the entries that are pushed never exceed the priority of the entry that was popped, and a complete entry has its true score as priority. When a complete entry is popped, every prefix of the best sentence on the stack has a priority at least as large as the best score, so the popped score is the best one.

The tests check this against exhaustive search over all sequences of at most 5 words and all their segmentations. They also check two failures: a stack of size 1 on the example, and an estimate far below the true rest, $h(t) = -100 (n - t)$, which makes every complete sentence look better than any partial one and returns a one-word sentence that is about 3.9 worse than the best.

## Complexity

Let $n$ be the number of frames, $V$ the vocabulary size and $L$ the largest number of phones in a word. With the closed set there are at most $V (n + 1) + 1$ expansions, each pushes at most $V n$ entries, and each push or pop costs $O(\log (V n))$ on a heap of at most $V^2 n^2$ entries. The segment scores take $O(n L)$ per $(w, t)$, for $V n$ pairs. This gives the worst case $O(V^2 n^2 \log (V n) + V n^2 L)$ time and $O(V^2 n^2)$ space, with back pointers in the entries. The code copies the word sequence into each entry for clarity, which adds a factor of $n$ to the space.

In practice the search pops far fewer entries, and how many depends on how tight $h$ is. A loose $h$ makes the search close to breadth-first; a tight one goes almost straight to the answer. Without recombination, the stack decoder searches a tree of word sequences, which is exponential in the number of words, as Paul 1990 points out.

## Properties

- **Exact with an admissible estimate and no stack limit.** It then returns the best sentence. With a limit, or an estimate that can be too low, it is not exact.
- **Not time-synchronous.** Entries cover different numbers of frames. This makes long-span language models easy, since each entry holds its full word history, but makes it hard to compare entries without a good estimate.
- **Not online.** The estimate $h(t)$ uses the frames after $t$, so the decoder needs the whole utterance, or a bound on its future frames.
- **Whole words at a time.** Each step adds a whole word with its best segmentation, so the acoustic match of a word runs once per start frame.

## Variants and improvements

- **Fast match.** Real stack decoders do not try every word. A cheap acoustic and language model match gives a short list of candidates for each entry, as in Paul 1990.
- **Normalizing by time.** Instead of an estimate of the rest, compare entries by score minus the best score up to their end frame, or by score per frame. These are not admissible, but they work in practice.
- **A stack per end frame.** Keep one stack for each $t$ and extend the best entries of each in order of $t$. This becomes a time-ordered search, close to [beam stack search](/beam-stack-search/).
- **N-best output.** Do not stop at the first complete entry, and do not close keys. The next complete entries popped are then the next best sentences, in order, when the estimate is admissible and consistent. The closed set of line L5 would drop the second-best history of each key.
- **Machine translation.** The same idea, with one stack per number of source words covered, is [phrase-based stack decoding](/phrase-based-stack-decoding/).

## When to use it

Use it when the language model has a long history that a time-synchronous search would have to copy into many tree copies, or when you want the exact best sentence for a small task with an admissible estimate. Use it also to produce N-best lists. For large vocabularies with real-time limits, time-synchronous beam search or a WFST decoder is the usual choice, because its cost per frame is easy to control.

## Pitfalls

- **A loose estimate.** If $h$ is a poor bound, the decoder extends many short entries before any long one, and the stack grows fast.
- **An estimate that is too low.** Short entries then look worse than long ones, and the decoder returns the first complete sentence it reaches, as in the test.
- **Stack limits.** A size limit is needed in practice, and it makes the search inexact, as in the example.
- **Scores of different lengths.** Without an estimate of the rest, a short entry has a better log score than a long one only because it covers fewer frames. Comparing raw scores is wrong.
- **Positive scores.** The bound assumes that transitions and language model terms are at most 0. A positive insertion bonus or scaled scores must enter $h$, as $\max(0, \log ip)$ does in the code.

## Implementations

The Python code runs A* over (words, end frame) with a heap, a closed set on (last word, end frame), a table of word segment scores per (word, start frame), an optional stack limit, and an optional custom estimate. The tests compare it with exhaustive search over all sequences of at most 5 words and their segmentations on random tasks, check the word segment scores and the bound, check that a stack of size 1 returns $x\,x$ on the example, and check that an estimate below the true rest returns a worse one-word sentence.

## History

Jelinek 1969 gave the stack algorithm for the sequential decoding of convolutional codes. The IBM speech group applied it to continuous speech recognition, and Bahl, Jelinek and Mercer 1983 describe stack decoding as part of their statistical approach. Paul 1990 described a version that is an optimal A* search, which is guaranteed to find the most likely sentence, and a second algorithm that linearizes the search at the cost of approximating some path likelihoods. Time-synchronous beam search later became the more common decoder for large vocabularies, but the stack decoder idea lives on in phrase-based machine translation and in N-best search.

## References
