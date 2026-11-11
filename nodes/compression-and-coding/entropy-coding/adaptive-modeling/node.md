---
tag: XX6766
kind: concept
slug: adaptive-modeling
name: Adaptive probability modeling
aliases:
- adaptive model
area: compression-and-coding/entropy-coding
level: advanced
summary: Estimate the probability of each symbol from the symbols already coded and update after each one, so the decoder can do the same and no model is sent.
prereqs: [arithmetic-coding]
see_also: [context-modeling, prediction-by-partial-matching, context-tree-weighting, cabac, adaptive-huffman-coding, fenwick-tree, conjugate-prior, minimum-description-length]
sources:
  - paper: doi:10.1145/214762.214771
    title: Ian H. Witten, Radford M. Neal and John G. Cleary, Arithmetic coding for data compression, Communications of the ACM 30(6), 520-540, 1987
    locator: the adaptive model of the C program, with the limit Max_frequency and the halving of the counts
  - paper: doi:10.1109/TIT.1981.1056331
    title: Raphail E. Krichevsky and Victor K. Trofimov, The performance of universal encoding, IEEE Transactions on Information Theory 27(2), 199-207, 1981
    locator: the estimator that adds one half to each count, and its redundancy
  - paper: doi:10.1109/TCOM.1984.1096090
    title: John G. Cleary and Ian H. Witten, Data compression using adaptive coding and partial string matching, IEEE Transactions on Communications 32(4), 396-402, 1984
    locator: the escape mechanism and the methods A and B
  - paper: doi:10.1109/26.61469
    title: Alistair Moffat, Implementing the PPM data compression scheme, IEEE Transactions on Communications 38(11), 1917-1921, 1990
    locator: the escape method C
  - paper: "Paul G. Howard, The design and analysis of efficient lossless data compression systems, PhD thesis, Brown University, 1993"
    locator: the escape method D
  - paper: doi:10.1109/18.87000
    title: Ian H. Witten and Timothy C. Bell, The zero-frequency problem, estimating the probabilities of novel events in adaptive text compression, IEEE Transactions on Information Theory 37(4), 1085-1094, 1991
    locator: the comparison of escape methods, and the methods P and X
  - paper: doi:10.1109/18.382012
    title: Frans M. J. Willems, Yuri M. Shtarkov and Tjalling J. Tjalkens, The context-tree weighting method, basic properties, IEEE Transactions on Information Theory 41(3), 653-664, 1995
    locator: the bound of one half lg n plus 1 on the parameter redundancy of the KT estimator
---

An adaptive model is a probability model for an entropy coder that learns from the data as it codes. Before each symbol it gives the coder a distribution computed from the symbols already coded, usually from counts, and after the symbol it updates the counts. The decoder runs the same model on the symbols it has decoded, so it gets the same distribution at each step and no model has to be sent. With an [arithmetic coder](/arithmetic-coding/), the code length is within a few bits of $\sum_i \lg(1/p_i)$, the sum of the information of the symbols under the predictions. So the quality of an adaptive coder is the quality of its predictions, and the question is how fast a model can learn and what it costs to learn.

## In plain words

The coder does not know in advance which letters are common. It starts with a guess that all letters are equally likely and keeps a tally of what it has seen. Each time it codes a letter, it uses the current tally to decide how many bits the letter gets, then adds the letter to the tally.

The decoder keeps its own tally in the same way. Because it sees the same letters in the same order, its tally is always the same as the coder's, so the two never disagree.

Early on the guesses are poor and cost extra bits. As the tally grows, the guesses get close to the true rates. A letter that has never appeared needs special care, because a tally of zero would make it impossible to code.

## The idea

**Static, semi-static and adaptive.** A *static* model is fixed in advance, for example a table of English letter frequencies, and it is only as good as its match to the data. A *semi-static* model reads the data twice: it counts the symbols, sends the counts, and then codes with them. An *adaptive* model reads the data once and sends no model; it pays instead for its poor early predictions. The two costs are close. For the Laplace estimator below, the adaptive length of any sequence with symbol counts $c_1, \ldots, c_k$ is exactly
$$\lg \binom{n}{c_1, \ldots, c_k} + \lg \binom{n + k - 1}{k - 1},$$
the cost of the [multinomial](/multinomial-coefficient/) index of the sequence among those with the same counts plus the cost of the counts themselves. This is what a semi-static coder that sends the counts would pay, and it does not depend on the order of the symbols.

**Additive estimators.** The common rule after $n$ symbols, with $c_s$ copies of symbol $s$ in an alphabet of $k$, is
$$P(s) = \frac{c_s + \delta}{n + k\delta}.$$
With $\delta = 1$ it is the Laplace estimator, the rule of succession. With $\delta = \tfrac12$ it is the Krichevsky and Trofimov (KT) estimator. Both are [Bayesian](/bayesian-inference/) predictions: Laplace with a uniform prior on the parameters and KT with the Dirichlet prior of parameter $\tfrac12$ (for $k = 2$, the Beta($\tfrac12$, $\tfrac12$) prior), each a [conjugate prior](/conjugate-prior/) of the multinomial. The product of the predictions is the probability that the mixture over all memoryless sources gives the sequence. For a binary sequence with $a$ zeros and $b$ ones it is $a!\,b!/(n+1)!$ for Laplace and $\Gamma(a + \tfrac12)\Gamma(b + \tfrac12)/(\pi\, n!)$ for KT.

**The price of learning.** Compare the adaptive length with $\lg(1/P_{ML})$, the length under the best memoryless model for the whole sequence, chosen after seeing it (this is $n$ times the order-0 empirical [entropy](/shannon-entropy/)). The difference is the [regret](/regret/) of the estimator. For binary sequences of length $n$, the KT regret is at most $\tfrac12 \lg n + 1$ bits for every sequence, and the Laplace regret at most $\lg(n + 1)$. For an alphabet of $k$ symbols, KT pays about $\tfrac{k-1}{2} \lg n$ bits, half a $\lg n$ per free parameter. This is the order of the cost of describing the parameters to a precision of $1/\sqrt n$, as in [minimum description length](/minimum-description-length/), and no estimator can do much better on most sources. The KT bound is the one used in the proof of [context tree weighting](/context-tree-weighting/).

**The zero-frequency problem.** In a large alphabet, or in a context that has seen only a few symbols, most symbols have count 0. A model must still give each of them some probability, or it cannot code them. Methods that set aside an *escape* probability for "a symbol not seen yet" were developed for [PPM](/prediction-by-partial-matching/). With $n$ symbols seen, $q$ of them distinct, and $c$ copies of the symbol in question:

| method | seen symbol | escape | source |
|---|---|---|---|
| A | $c/(n+1)$ | $1/(n+1)$ | Cleary and Witten 1984 |
| B | $(c-1)/n$ | $q/n$ | Cleary and Witten 1984 |
| C | $c/(n+q)$ | $q/(n+q)$ | Moffat 1990 |
| D | $(2c-1)/(2n)$ | $q/(2n)$ | Howard 1993 |

Method B counts a symbol as seen only from its second occurrence. Methods C and D give the escape a weight that grows with the number of distinct symbols, which matches text better. After an escape, the coder codes the new symbol with another model, a shorter context in PPM or a uniform distribution. Witten and Bell (1991) compare these methods and propose others based on a Poisson model of new symbols.

**Halving and recency.** Real data changes along the way. A model that only adds counts gives the start of a file as much weight as the end, and its counts grow without limit. The usual fix, used in the coder of Witten, Neal and Cleary (1987), is to halve all counts, rounding up, whenever the total reaches a limit. This keeps the total within the precision of the coder and makes the model forget old data at a rate set by the limit and the increment. A binary model may instead keep a probability $p$ and update it as $p \leftarrow p + (b - p)/2^r$ after each bit $b$, an [exponential moving average](/exponential-moving-average/); this is the model of LZMA and of [context mixing](/context-mixing/) coders. The state machine of [CABAC](/cabac/) is a table form of the same rule.

**Data structures.** For a large alphabet the coder needs the cumulative count below each symbol. A [Fenwick tree](/fenwick-tree/) gives it and updates it in $O(\log k)$ time. Witten, Neal and Cleary instead keep the symbols sorted by count, so the frequent ones are found first.

## Examples

**KT and Laplace on 0010.** The KT estimator predicts the four bits with $\tfrac12$, $\tfrac{1.5}{2} = \tfrac34$, $\tfrac{0.5}{3} = \tfrac16$ and $\tfrac{2.5}{4} = \tfrac58$. The product is $\tfrac{5}{128}$, a length of 4.68 bits. Laplace predicts $\tfrac12$, $\tfrac23$, $\tfrac14$, $\tfrac35$ with product $\tfrac{1}{20} = \tfrac{3!\,1!}{5!}$, 4.32 bits. The best memoryless model, with $P(0) = \tfrac34$ chosen after the fact, gives $(\tfrac34)^3 \tfrac14 = \tfrac{27}{256}$, 3.25 bits. The regrets are 1.43 and 1.08 bits, under the bounds $\tfrac12 \lg 4 + 1 = 2$ and $\lg 5 \approx 2.32$. On short sequences Laplace can win; on long ones with a skewed distribution, KT wins, because Laplace gives too much to the rare symbol.

**Escapes after abracadabra.** The counts are a 5, b 2, r 2, c 1, d 1, so $n = 11$ and $q = 5$. The escape probability is $\tfrac{1}{12}$ under method A, $\tfrac{5}{11}$ under B, $\tfrac{5}{16}$ under C and $\tfrac{5}{22}$ under D, and the letter a gets $\tfrac{5}{12}$, $\tfrac{4}{11}$, $\tfrac{5}{16}$ and $\tfrac{9}{22}$.

**Halving on a source that changes.** The implementation codes 40000 bits in 20 blocks that switch between $P(1) = 0.05$ and $P(1) = 0.95$. Plain counts end near $P(1) = 0.5$ and need 40007 bits. Counts with an increment of 32 that are halved when the total reaches 1024 need 13020 bits, close to $40000 \cdot h(0.05) \approx 11460$ bits, the entropy of the blocks. On a source that does not change, the same halving costs about 2 percent more than plain counts.

## Where it is used

Almost every practical arithmetic or range coder uses an adaptive model: the coder of Witten, Neal and Cleary, the binary models of LZMA and [range coding](/range-coding/), and the contexts of [CABAC](/cabac/). [Context modeling](/context-modeling/) keeps one adaptive model per context, and [PPM](/prediction-by-partial-matching/) adds the escape methods above. [Context tree weighting](/context-tree-weighting/) uses the KT estimator at each node of its tree. [Adaptive Huffman coding](/adaptive-huffman-coding/) applies the same idea to a prefix code that it rebuilds as the counts change. In machine learning, the same estimators appear as additive smoothing of word counts in language models.

## References
