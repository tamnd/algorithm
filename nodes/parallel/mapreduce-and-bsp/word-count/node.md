---
tag: 9P6PN4
kind: problem
slug: word-count
name: Word count
aliases:
- word frequency count
- histogram of words
area: parallel/mapreduce-and-bsp
level: intro
summary: Count occurrences of every word in a large text corpus; the canonical MapReduce example.
prereqs: [mapreduce-model, frequency-counter]
see_also: [combiner, shuffle-phase, data-skew, group-by-aggregation, parallel-histogram, frequent-items-problem, inverted-index, element-distinctness]
sources:
  - paper: "Jeffrey Dean and Sanjay Ghemawat, MapReduce: simplified data processing on large clusters, 6th Symposium on Operating Systems Design and Implementation (OSDI), 2004"
    locator: Section 2.1 (the word count example), Section 4.3 (combiner function, with the remark that word frequencies follow a Zipf distribution) and Appendix A (the full word count program)
  - book: isbn:9781608453429
    title: Jimmy Lin and Chris Dyer, Data-Intensive Text Processing with MapReduce, Morgan and Claypool, 2010
    locator: Section 2.2 (word count as the first example) and Section 3.1.1 (combiners and in-mapper combining)
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.2 (MapReduce, with word count as the running example and 2.2.4 Combiners)
---

Word count is the problem of computing, for every distinct word of a text corpus, the number of times it occurs. On one machine it is a [frequency counter](/frequency-counter/) with a hash table. In the [MapReduce model](/mapreduce-model/) it is the standard first example: the map function emits the pair (word, 1) for each word, and the reduce function adds up the ones. Its costs show the two main effects of the model: a [combiner](/combiner/) cuts the communication, and the very uneven frequencies of words make some reducers much busier than others.

## In plain words

You have more text than one computer can read in a reasonable time, and you want a table that says how often each word appears. Give each computer a piece of the text. Each computer writes down "word, 1" for every word it reads. The system then collects the notes so that all notes for the same word arrive at the same computer, which adds them up. This sends one note for every word in the text. A better plan lets each computer first add up its own notes, so that it sends one note for each distinct word in its piece. A few words, such as "the", are far more common than the rest, so the computer that owns "the" gets much more work unless the notes are added up early.

## Definition

**Input.** A multiset of documents. Each document is a sequence of tokens (words) over an alphabet. Let $N$ be the total number of tokens, $V$ the number of distinct words, and $c(w)$ the number of occurrences of word $w$, so $\sum_w c(w) = N$.

**Output.** The set of pairs $\{(w, c(w)) : c(w) \ge 1\}$, in any order.

**Cost model.** The [MapReduce model](/mapreduce-model/) with $M$ map tasks (split $i$ has $N_i$ tokens and $D_i$ distinct words) and $R$ reduce tasks. The costs are the rounds, the communication (pairs and bytes sent in the shuffle), and the largest reducer input $L$. On one machine, the cost is time in the word RAM, with a hash of a word in $O(1)$ expected time.

## Variants

- **Plain MapReduce word count.** Map emits $(w, 1)$ for each token, reduce emits $(w, \sum \text{values})$.
- **With a combiner.** The reduce function also runs on the map side, which is correct because integer addition is associative and commutative, see [combiner](/combiner/).
- **In-mapper combining** (Lin and Dyer, Section 3.1.1). Each map task keeps a hash table of counts over its whole split and emits one pair per distinct word when the split ends. It sends the same pairs as one combiner pass, but the map task needs memory for $D_i$ counters.
- **Counting $n$-grams or word pairs.** The key is a tuple of words. The number of distinct keys grows fast, so the combiner helps less. Lin and Dyer (Section 3.2) compare the "pairs" and "stripes" designs for co-occurrence counts.
- **Approximate and top-$k$ counts.** When only the frequent words matter, a [count-min sketch](/count-min-sketch/) or a [Misra-Gries summary](/misra-gries-summary/) per map task uses memory that does not depend on $V$, and the summaries merge in the reduce. See the [frequent items problem](/frequent-items-problem/).

## Examples

**A small corpus.** The documents "a rose is a rose", "is a rose" and "a b" have $N = 10$ and $V = 4$. The output is (a, 4), (rose, 3), (is, 2), (b, 1). With $M = 2$ splits (the first document, then the other two), plain word count sends 10 pairs. With a combiner, split 0 sends (a, 2), (is, 1), (rose, 2) and split 1 sends (a, 2), (b, 1), (is, 1), (rose, 1), so 7 pairs in total, which is $D_0 + D_1 = 3 + 4$.

**A Zipf corpus.** Take a vocabulary of $V = 1000$ words $w_1, \dots, w_{1000}$, where $w_i$ has probability $p_i = 1/(i \, H_{1000})$ and $H_{1000} \approx 7.485$ is the [harmonic number](/harmonic-series/). Draw $N = 20{,}000$ tokens in 20 documents, and run with $M = 10$ map tasks of 2,000 tokens each and $R = 8$ reduce tasks. Each word is written as "w" and its index, so a pair (w17, 1) has 4 bytes.

| | without combiner | with combiner |
|---|---|---|
| pairs sent | 20,000 | 4,971 |
| bytes sent | 78,600 | 24,108 |
| largest reducer input (pairs) | 4,499 | 658 |
| average reducer input (pairs) | 2,500 | 621.4 |

The most frequent word $w_1$ occurs 2,688 times (its expected count is $N p_1 \approx 2{,}672$), so without a combiner its reduce task gets at least 2,688 pairs. With a combiner, $w_1$ sends one pair from each map task, so 10 pairs. The predicted number of pairs with a combiner (formula below) is $10 \times 499.44 = 4{,}994.4$.

## Known algorithms

| Algorithm | Model | Cost |
|---|---|---|
| hash table count ([frequency counter](/frequency-counter/)) | one machine | $O(N)$ expected time, $O(V)$ space |
| sort the tokens, count runs | one machine, comparisons | $O(N \log N)$ comparisons |
| plain MapReduce | 1 round | $N$ pairs sent, $L \ge \max_w c(w)$ |
| MapReduce with a combiner | 1 round | $\sum_i D_i$ pairs sent, at most $M$ pairs per key |
| in-mapper combining | 1 round | $\sum_i D_i$ pairs sent, $O(D_i)$ memory per map task |
| [parallel histogram](/parallel-histogram/) for a small fixed vocabulary | shared memory, $p$ processors | private tables of $V$ counters merged by a tree: $O(N/p + V \log p)$ time, $O(pV)$ space |

**The communication, derived.** Without a combiner, each token $w$ becomes one message $(w, 1)$, so the shuffle carries exactly $N$ pairs and $\sum_w c(w)\,(|w| + 1)$ bytes in the encoding of the example, where $|w|$ is the length of $w$ in bytes. The replication rate is 1. With one combiner pass per map task, map task $i$ sends one pair for each distinct word of its split, so the shuffle carries $\sum_{i=1}^{M} D_i$ pairs. Each $D_i$ is at least 1 when $N_i \ge 1$ and at most $\min(N_i, V)$, and every word with $c(w) \ge 1$ is in some split, so

$$V \le \sum_{i=1}^{M} D_i \le \min(N, M V).$$

When the tokens are drawn independently with probabilities $p_w$ and each split has $N/M$ tokens, word $w$ is in a given split with probability $1 - (1 - p_w)^{N/M}$. By linearity of expectation,

$$\mathbb{E}\Big[\sum_i D_i\Big] = M \sum_{w} \Big(1 - (1 - p_w)^{N/M}\Big).$$

A word with $p_w N/M \gg 1$ adds about $M$ pairs instead of $c(w) \approx p_w N$, and a rare word with $p_w N/M \ll 1$ adds about $c(w)$ pairs. So a combiner saves the most on the frequent words, which are the ones that cause skew.

## Bounds

- **One machine, lower bound.** [Element distinctness](/element-distinctness/) reduces to word count in $O(N)$ time: count, then check whether some count exceeds 1. So in the algebraic computation tree model, word count needs $\Omega(N \log N)$ time (Ben-Or's bound for element distinctness). With hashing in the word RAM, $O(N)$ expected time is possible, and reading the input already takes $\Omega(N)$.
- **MapReduce, communication.** In one round, the reduce task that outputs $(w, c(w))$ must receive at least one pair for $w$, so every one-round algorithm sends at least $V$ pairs. A combiner reaches $\sum_i D_i$, which equals $V$ when each word occurs in only one split.
- **MapReduce, largest reducer input.** Without a combiner, the reduce task of the most frequent word receives $L \ge \max_w c(w)$ pairs. With a combiner, each key group has at most $M$ values, so $L \le M \cdot K$, where $K$ is the largest number of distinct words that the [partitioner](/partitioner/) gives to one reduce task.
- **Zipf skew.** Under a Zipf law with exponent 1 over $V$ words, $\max_w c(w) \approx N/H_V$ with $H_V \approx \ln V + 0.577$. The average reducer input is $N/R$, so without a combiner the slowest reduce task does about $R/H_V$ times the average work, or more. For $V = 1000$ and $R = 100$ that is about $13.4$ times the average. Dean and Ghemawat (Section 4.3) give this reason for the combiner. See [data skew](/data-skew/).

## Reductions

- Word count is a group-by-count, the special case of [group-by aggregation](/group-by-aggregation/) where the aggregate is the count. Every MapReduce aggregation with an associative and commutative operator has the same plan and the same costs.
- Word count reduces to sorting: sort the tokens and count the runs of equal words. In MapReduce, this is what the [shuffle phase](/shuffle-phase/) does inside each reduce task.
- Element distinctness reduces to word count, as in the bound above.
- The [inverted index](/inverted-index/) is word count with the document identifiers kept instead of only counted.

## Applications

- Term frequencies for search ranking and text statistics, and the first pass of building an [inverted index](/inverted-index/).
- Counts of $n$-grams for language models, and counts of word pairs for co-occurrence statistics.
- Any histogram over a large set of keys: counts of URLs in web logs, of query strings, or of items in sales records.
- A test job for MapReduce systems: it uses every phase, and its output is easy to check against a count on one machine.

## References
