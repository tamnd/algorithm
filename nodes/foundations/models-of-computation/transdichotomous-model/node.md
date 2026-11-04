---
tag: QNR9NW
kind: concept
slug: transdichotomous-model
name: Transdichotomous model
aliases:
- transdichotomous assumption
area: foundations/models-of-computation
level: advanced
summary: Word RAM assumption that the word size is at least log n so that problem size fits in a word.
prereqs: [word-ram, unit-cost-model, asymptotic-notation]
see_also: [fusion-tree, integer-sorting, radix-sort, predecessor-problem, cell-probe-model, logarithmic-cost-model, real-ram, ac0]
sources:
  - url: "https://en.wikipedia.org/wiki/Transdichotomous_model"
    locator: article Transdichotomous model
  - paper: doi:10.1016/0022-0000(93)90040-4
    title: "Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47(3) (1993), 424 to 436"
    locator: the whole paper, pp. 424 to 436 (the fusion tree, the O(n log n / log log n) sort)
  - paper: doi:10.1016/S0022-0000(05)80064-9
    title: "Michael L. Fredman and Dan E. Willard, Trans-dichotomous algorithms for minimum spanning trees and shortest paths, Journal of Computer and System Sciences 48(3) (1994), 533 to 551"
    locator: the introduction (the model, and the term strongly trans-dichotomous)
  - paper: doi:10.1016/0020-0190(83)90075-3
    title: "Dan E. Willard, Log-logarithmic worst-case range queries are possible in space Theta(N), Information Processing Letters 17(2) (1983), 81 to 84"
    locator: the y-fast trie, pp. 81 to 84
  - paper: doi:10.1006/jcss.1998.1580
    title: "Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57(1) (1998), 74 to 93"
    locator: abstract (the O(n log log n) bound, and linear expected time for w at least (log n)^(2+epsilon))
  - paper: doi:10.1016/j.jalgor.2003.09.001
    title: "Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50(1) (2004), 96 to 105"
    locator: abstract (the main theorem), pp. 96 to 105
  - paper: doi:10.1109/SFCS.2002.1181890
    title: "Yijie Han and Mikkel Thorup, Integer sorting in O(n sqrt(log log n)) expected time and linear space, 43rd Annual IEEE Symposium on Foundations of Computer Science (FOCS 2002), 135 to 144"
    locator: abstract (the main theorem), pp. 135 to 144
  - paper: doi:10.1006/jcss.2002.1822
    title: "Paul Beame and Faith E. Fich, Optimal bounds for the predecessor problem and related problems, Journal of Computer and System Sciences 65(1) (2002), 38 to 72"
    locator: abstract and the introduction (the upper bound, and the two cell-probe lower bounds as functions of the universe size and of n)
  - paper: doi:10.1016/S0304-3975(98)00172-8
    title: "Arne Andersson, Peter Bro Miltersen and Mikkel Thorup, Fusion trees can be implemented with AC0 instructions only, Theoretical Computer Science 215(1-2) (1999), 337 to 344"
    locator: abstract and the introduction
  - paper: doi:10.1007/BFb0028575
    title: "Torben Hagerup, Sorting and searching on the word RAM, STACS 98, Lecture Notes in Computer Science 1373 (1998), 366 to 398"
    locator: the definition of the word RAM and the survey of sorting and searching, pp. 366 to 398
---

The transdichotomous model is the [word RAM](/word-ram/) with the assumption that the word size $w$ is at least $\lg n$, where $n$ is the size of the input, and with the rule that a bound must hold for every such $w$. The assumption lets one word hold the index of any item of the input, so that [unit-cost](/unit-cost-model/) array access is fair. Fredman and Willard named the model in 1990 and used it to design algorithms that beat the bounds of the [comparison model](/comparison-model/), such as the [fusion tree](/fusion-tree/).

## In plain words

A computer works on whole words, and a word has a fixed number of bits. A program must be able to point at each item of its input. For that, a word needs enough bits to write the position of any item. So the word cannot have fewer bits than the number needed to write the input size.

The transdichotomous model makes this rule part of the model. It also says how to state a result. The algorithm must work for every word size that is large enough, and the bound should not depend on the word size, or should say exactly how it depends on it. So the result holds on any computer whose words are big enough to address the input.

## The idea

**The assumption.** The model has two parameters: $n$, the number of input words, and $w$, the number of bits of a word. The assumption is $w \ge \lg n$. Some authors write $w \ge \lceil \lg (n+1) \rceil$ or $w = \Omega(\log n)$ instead. An array with $n$ cells has the addresses $0, \ldots, n-1$, and the largest of these needs $\lceil \lg n \rceil$ bits. So with $w \ge \lg n$ every address fits in one word. A counter that reaches the value $n$ itself needs $\lceil \lg (n+1) \rceil$ bits. When $n$ is a power of two and $w = \lg n$, this is one bit more than $w$: for $n = 2^{20}$ the value $n$ has 21 bits. This is why some authors assume $w \ge \lceil \lg (n+1) \rceil$, and why loop counters are usually allowed a constant number of words. The other rules of the machine are those of the [word RAM](/word-ram/), which this page does not repeat.

**The form of a bound.** A running time bound $T(n, w)$ is *transdichotomous* when it is proved for all $n \ge 1$ and all $w \ge \lg n$. There are two readings.

- *Strong form.* The bound does not depend on $w$. It is a function $T(n)$ that holds for every $w \ge \lg n$. Fredman and Willard (1994) call an algorithm *strongly trans-dichotomous* when its time and space do not depend on the word size.
- *Two-parameter form.* The bound is a function of both $n$ and $w$, and it holds for every $w \ge \lg n$.

In both forms, the algorithm cannot assume a particular $w$. A bound holds in particular when $w = \lg n$, so an algorithm cannot count on words much larger than an address. It also holds when $w$ is huge compared with $\lg n$, so an algorithm cannot count on keys that are short compared with the word.

**The name.** The name says that the model crosses the dichotomy between the size of the machine and the size of the problem: the word size is tied to the input size, and not fixed in advance. The term is in the title of the paper of Fredman and Willard on minimum spanning trees and shortest paths (FOCS 1990, journal version 1994). Their fusion tree paper (STOC 1990, journal version 1993) works under the same assumption.

**The instruction set matters.** A transdichotomous bound depends on the instructions of the machine as well as on $w$. Fusion trees as Fredman and Willard built them use multiplication, which is not an [AC0](/ac0/) operation. Andersson, Miltersen and Thorup (1999) showed that the same space and time bounds can be reached with AC0 instructions only, but some of these instructions are not standard ones such as addition, shifts and bitwise Boolean operations. So a bound on the word RAM must say which instructions it uses.

### Pitfalls

- **A fixed word size is not transdichotomous.** If $w$ is a constant such as 64, the machine can address only $2^{64}$ cells, and every bound for large $n$ is about a different machine.
- **Unbounded words at unit cost are not transdichotomous.** If a register holds an integer of any size at unit cost, the model is much stronger. Hartmanis and Simon showed that with unit-cost multiplication and bitwise operations on such registers, polynomial time equals polynomial space (see the [word RAM](/word-ram/)). The bound $w$ on the word size is what keeps the transdichotomous model realistic.
- **A two-parameter bound is not a strong-form bound.** [Radix sort](/radix-sort/) is linear when $w = O(\log n)$, but its time grows with $w$. Calling it a linear-time sort on the word RAM leaves out the condition on $w$.
- **Lower bounds need a model with cells of $w$ bits.** A comparison lower bound such as $\Omega(n \log n)$ for sorting does not hold here, because the algorithm can use the bits of the keys. Lower bounds for this model are proved in the [cell-probe model](/cell-probe-model/), which charges one step for each read of a cell of $w$ bits and nothing for computation.

## Examples

Each example is a result on the word RAM with $w \ge \lg n$.

**Fusion trees (two-parameter form).** A fusion tree stores $n$ keys of $w$ bits in $O(n)$ words and answers a predecessor query in $O(\log n / \log w)$ time (Fredman and Willard 1993). See [fusion tree](/fusion-tree/).

**Sorting (strong form).** Fredman and Willard (1993) sort $n$ words in $O(n \log n / \log \log n)$ time for every $w \ge \lg n$. This is below the bound $\Omega(n \log n)$ of the comparison model, which is the meaning of the title of their paper. Later bounds for every $w \ge \lg n$ are these.

| result | time | kind | space |
|---|---|---|---|
| Fredman and Willard 1993 | $O(n \log n / \log \log n)$ | deterministic | $O(n)$ |
| Han 2004 | $O(n \log \log n)$ | deterministic | $O(n)$ |
| Han and Thorup 2002 | $O(n \sqrt{\log \log n})$ | expected | $O(n)$ |

Before Han, Andersson, Hagerup, Nilsson and Raman (1998) sorted in $O(n \log \log n)$ time for every $w \ge \lg n$, and in $O(n)$ expected time when $w \ge (\log n)^{2 + \varepsilon}$ for a constant $\varepsilon > 0$. The second result is a two-parameter result: it is linear only for large words. Whether $n$ words can be sorted in $O(n)$ time for every $w \ge \lg n$ is an open problem. See [integer sorting](/integer-sorting/).

**Predecessor search (strong form from two parameters).** The y-fast trie of Willard (1983) stores a static set of $n$ keys from the universe $\{0, \ldots, 2^w - 1\}$ in $O(n)$ words and answers a predecessor query in $O(\log w)$ time in the worst case. The fusion tree answers it in $O(\log n / \log w)$ time. Take the better of the two for the given $w$. For positive numbers $a$ and $b$, $\min(a, b)^2 \le a b$, so $\min(a, b) \le \sqrt{ab}$. With $a = \lg w$ and $b = \lg n / \lg w$ the product is $\lg n$, so the query time is $O(\sqrt{\log n})$ for every $w$, a bound in $n$ alone. For $n = 2^{20}$ the two terms are these, and the minimum stays below $\sqrt{20} \approx 4.47$ in each row.

| $w$ | $\lg w$ | $\lg n / \lg w$ | minimum |
|---|---|---|---|
| 20 | 4.32 | 4.63 | 4.32 |
| 64 | 6 | 3.33 | 3.33 |
| 1024 | 10 | 2 | 2 |
| $2^{20}$ | 20 | 1 | 1 |

Beame and Fich (2002) improved and closed this. They give a static structure with polynomial space and query time

$$
O\left(\min\left\{ \frac{\log w}{\log \log w},\ \sqrt{\frac{\log n}{\log \log n}} \right\}\right),
$$

and they note that the transformations of Andersson and Thorup make it dynamic with $O(n)$ space. They also prove matching lower bounds in the cell-probe model, for structures with $n^{O(1)}$ cells of $w^{O(1)}$ bits. As a function of $n$ alone, no such structure does better than $\Omega(\sqrt{\log n / \log \log n})$ in the worst case. This holds for some choice of $w$ as a function of $n$, not for every $w$. When $w = \lg n$, for example, the first term $\log w / \log \log w$ is much smaller. See [predecessor problem](/predecessor-problem/).

**Radix sort (two-parameter form).** [Radix sort](/radix-sort/) with digits of $\lceil \lg n \rceil$ bits sorts $n$ words of $w$ bits in $O(n \lceil w / \lg n \rceil)$ time, one pass of [counting sort](/counting-sort/) for each digit. For $n = 2^{20}$ and $w = 64$ this is $\lceil 64 / 20 \rceil = 4$ passes, and for $w = 32$ it is $2$ passes. The bound is linear when $w = O(\log n)$, but it grows with $w$, so it is not a strong-form bound. Fredman and Willard (1994) use this example to explain the strong form.

**Non-examples.**

- A machine with a fixed word size, for example $w = 32$, is not transdichotomous. It can address at most $2^{32}$ cells. For an input with $n = 2^{40}$ items an address needs $40 > 32$ bits, and a loop counter over the items does not fit in a word.
- A bound that holds only for $w = \Theta(\log n)$ is a bound for one range of $w$, and not for every $w \ge \lg n$. It can be a good result, but it is not transdichotomous in the strong sense.

## Where it is used

- **Integer sorting and searching.** The word RAM results on [integer sorting](/integer-sorting/), on predecessor search and on dictionaries are stated in this way. The survey of Hagerup (1998) collects the results up to that year.
- **Graph algorithms.** Fredman and Willard (1994) give a linear-time [minimum spanning tree](/minimum-spanning-tree/) algorithm and an $O(m + n \log n / \log \log n)$ version of [Dijkstra's algorithm](/dijkstra/) for a graph with $n$ vertices and $m$ edges with integer weights. Both use a new priority queue, the atomic heap, that needs the transdichotomous assumption.
- **Lower bounds.** The [cell-probe model](/cell-probe-model/) has cells of $w$ bits too, and a lower bound there is a lower bound on the word RAM with any instruction set. The predecessor bounds of Beame and Fich are of this kind.
- **Contrast with bit costs.** In the [logarithmic-cost model](/logarithmic-cost-model/) the cost of an operation grows with the number of bits of its operands. The transdichotomous model charges one step for an operation on a word of any allowed size, and it limits the size by $w$ instead.
- **Contrast with exact reals.** The [real RAM](/real-ram/) of computational geometry stores exact reals at unit cost and has no word size. Its lower bounds come from algebraic trees, and they do not apply to the word RAM.

## References
