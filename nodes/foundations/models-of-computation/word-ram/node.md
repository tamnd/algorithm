---
tag: DM95RK
kind: model
slug: word-ram
name: Word RAM
aliases:
- word RAM model
- w-bit RAM
area: foundations/models-of-computation
level: core
summary: A RAM whose memory cells hold words of w bits, with w at least lg n, where arithmetic, comparison, bitwise and shift operations on words cost one step each.
prereqs: [random-access-machine, unit-cost-model]
see_also: [transdichotomous-model, logarithmic-cost-model, cell-probe-model, pointer-machine, real-ram, integer-sorting, predecessor-problem, bit-parallelism]
sources:
  - url: "https://en.wikipedia.org/wiki/Word_RAM"
    locator: article Word RAM
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (the RAM model and the word size c lg n)
  - paper: "Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47 (1993)"
    locator: the model and the transdichotomous assumption, and the sorting bound
  - paper: "Michael L. Fredman and Dan E. Willard, Trans-dichotomous algorithms for minimum spanning trees and shortest paths, Journal of Computer and System Sciences 48 (1994)"
    locator: the introduction, where the term transdichotomous is defined
  - paper: "Yijie Han and Mikkel Thorup, Integer sorting in O(n sqrt(log log n)) expected time and linear space, FOCS 2002"
    locator: abstract (the main result)
  - paper: "Torben Hagerup, Sorting and searching on the word RAM, STACS 1998, Lecture Notes in Computer Science 1373"
    locator: the definition of the model and the survey of results
  - paper: "Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50 (2004)"
    locator: abstract (the main result)
  - paper: "Peter van Emde Boas, Preserving order in a forest in less than logarithmic time and linear space, Information Processing Letters 6 (1977)"
    locator: the O(log log U) priority queue
  - paper: "Dan E. Willard, Log-logarithmic worst-case range queries are possible in space Theta(N), Information Processing Letters 17 (1983)"
    locator: the y-fast trie
  - paper: "Martin Dietzfelbinger, Torben Hagerup, Jyrki Katajainen and Martti Penttonen, A reliable randomized algorithm for the closest-pair problem, Journal of Algorithms 25 (1997)"
    locator: the multiply-shift hash family
  - paper: "Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57 (1998)"
    locator: abstract (signature sort)
  - paper: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31 (1984)"
    locator: abstract (the main result)
  - paper: "Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974)"
    locator: abstract (the main result)
---

The word RAM is a [random access machine](/random-access-machine/) whose memory cells hold words of $w$ bits, where each operation on one or two words costs one step. It is the [unit-cost model](/unit-cost-model/) with a bound on the size of a number. The usual assumption is $w \ge \lg n$, so that a word can hold the index of any input item. This is the model behind almost every running time on this site that does not name another model.

## The machine

**Memory.** The memory is an array of cells $M[0], M[1], M[2], \ldots$. Each cell holds a word: an integer in the range $0$ to $2^w - 1$, or a bit string of length $w$. A word can be used as an address, so the machine reads and writes $M[M[i]]$ (indirect addressing). The program is fixed and is not stored in the memory.

**Input.** An input of size $n$ is $n$ words in $M[0]$ to $M[n-1]$. When the items are larger than one word (long strings, big integers), the input size counts words, not items.

**Instructions.** Each of these costs one step:

- arithmetic modulo $2^w$: addition, subtraction and multiplication, and on some definitions integer division with remainder;
- comparison of two words, and a conditional jump;
- the bitwise operations AND, OR, XOR and NOT;
- shifts left and right by any number of bits from $0$ to $w$;
- reading and writing a cell whose address is in a word.

Definitions differ in the exact list. Some leave out multiplication and division. The AC$^0$ RAM allows only operations that a constant-depth circuit of polynomial size computes, and these include addition, comparison, the bitwise operations and shifts, but not multiplication (see [AC0](/ac0/)). A result on the word RAM should say which instructions it uses.

**The word size.** The model has two parameters, $n$ and $w$. The assumption $w \ge \lg n$ is needed: with fewer bits, a word cannot hold an address of the input, and the machine cannot use indirect addressing on it. The working memory must be addressable too: a run that uses $S$ cells needs $w \ge \lg S$. This is one reason CLRS takes $w = c \lg n$ with a constant $c \ge 1$, so that a polynomial number of cells can be addressed. Fredman and Willard (1990, in a journal in 1994) call a bound that holds for every $w \ge \lg n$ *transdichotomous*, because it bridges the size of the problem and the size of the machine (see [transdichotomous model](/transdichotomous-model/)). The algorithm cannot choose $w$: a bound must hold for the $w$ of the machine it is given. CLRS takes $w = c \lg n$ for a constant $c \ge 1$, which fixes $w = \Theta(\log n)$. Many results on integer data state their bounds as functions of both $n$ and $w$.

## What it counts

The cost of a run is the number of instructions it executes. Each instruction costs 1, whatever the values of its words are. The space is the largest address in use, plus one, in words. This can be much larger than the number of cells in use when the memory is used sparsely, and hashing is the usual way to close the gap. A space of $s$ words is $s w$ bits.

**Why the bound on $w$ matters.** With no bound on the size of a number, unit cost gives too much power. Start with $x = 2$ and square it $k$ times: after $k$ steps $x = 2^{2^k}$, a number with $2^k + 1$ bits. Hartmanis and Simon (1974) showed that a RAM with unit-cost multiplication and bitwise operations on unbounded integers solves in polynomial time exactly the problems in [PSPACE](/pspace/). The word RAM avoids this, because each number has at most $w$ bits, and a run of $t$ steps can touch at most $O(t)$ cells, each with $w$ bits. Also, a bound must hold for every $w \ge \lg n$, including $w = \lg n$, so an algorithm cannot depend on very large words. Results that relate the word RAM to [Turing machines](/turing-machine/) also assume $w = O(\log n)$.

**Word-level parallelism.** One instruction acts on all $w$ bits at once. So an algorithm can pack several small values into one word and process them together. For example, the number of 1-bits of a word (its [population count](/population-count/)) takes $\lg w$ rounds of mask, shift and add: each round adds neighbouring fields in parallel and doubles the field width. For $w = 64$ this is $6$ rounds, independent of the number of 1-bits. [Fusion trees](/fusion-tree/) and the fast integer sorts are built from tricks of this kind (see [bit parallelism](/bit-parallelism/)).

**Hashing.** Multiplication modulo $2^w$ gives fast hash functions. The multiply-shift family of Dietzfelbinger, Hagerup, Katajainen and Penttonen maps a $w$-bit key $x$ to $\ell$ bits by
$$h_a(x) = \left\lfloor \frac{a x \bmod 2^w}{2^{w-\ell}} \right\rfloor,$$
for a random odd $a$ with $0 < a < 2^w$. It costs one multiplication and one shift. For two distinct keys the probability of a collision is at most $2/2^\ell$. For example, with $w = 8$, $\ell = 3$, $a = 181$ and $x = 77$: $a x = 13937$, $13937 \bmod 256 = 113$, and $113 \gg 5 = 3$. See [multiply-shift hashing](/multiply-shift-hashing/).

## Relation to other models

- **Unit-cost and logarithmic-cost RAM.** The word RAM with $w = \Theta(\log n)$ is the unit-cost RAM with a bound on the size of numbers. A run of $t$ steps on it costs $O(t \log n)$ in the [logarithmic-cost model](/logarithmic-cost-model/), because each word has $O(\log n)$ bits. So a polynomial bound on the word RAM gives a polynomial bound on a [Turing machine](/turing-machine/), see [RAM and Turing machine equivalence](/ram-turing-equivalence/).
- **Comparison model.** In the [comparison model](/comparison-model/) an algorithm learns about the keys only by comparing two of them. A comparison algorithm runs on the word RAM with the same cost. The word RAM can also use the bits of the keys, as in [radix sort](/radix-sort/), so the comparison lower bound of $\Omega(n \log n)$ for sorting does not hold on it.
- **Pointer machine.** A [pointer machine](/pointer-machine/) follows and creates pointers but does no arithmetic on addresses. The word RAM can compute an address, so it can index an array and use a hash table.
- **Cell-probe model.** The [cell-probe model](/cell-probe-model/) also has cells of $w$ bits, but it counts only the cells that a run reads or writes, and computation is free. Each word RAM algorithm gives a cell-probe algorithm with no more probes, so a lower bound in the cell-probe model is a lower bound on the word RAM.
- **Real RAM.** The [real RAM](/real-ram/) of computational geometry holds exact real numbers in its cells, with unit-cost arithmetic and no bitwise operations. It is not a word RAM, and results do not move between the two models without care.

## Known results in the model

Here $n$ is the number of items, each item is one word, and $w \ge \lg n$.

- **Sorting integers.** [Radix sort](/radix-sort/) with digits of $\lg n$ bits sorts $n$ words in $O(n \lceil w / \lg n \rceil)$ time, which is $O(n)$ when $w = O(\log n)$. For example, $n = 2^{20}$ keys of $w = 64$ bits need $\lceil 64/20 \rceil = 4$ passes of [counting sort](/counting-sort/), each in $O(n + 2^{20})$ time. For any $w$, Fredman and Willard (1993) sort in $O(n \log n / \log \log n)$ time with fusion trees, which beats the comparison bound. Han (2004) sorts deterministically in $O(n \log \log n)$ time and linear space, and Han and Thorup (2002) sort in $O(n \sqrt{\log \log n})$ expected time and linear space. Signature sort (Andersson, Hagerup, Nilsson and Raman, 1998) sorts in $O(n)$ expected time when $w \ge (\lg n)^{2+\varepsilon}$ for a constant $\varepsilon > 0$, and radix sort covers $w = O(\log n)$. Whether $n$ words can be sorted in $O(n)$ time for every $w$, in particular for $w$ between these two ranges, is open. See [integer sorting](/integer-sorting/).
- **Predecessor search.** For a set of $n$ keys from $\{0, \ldots, 2^w - 1\}$, the van Emde Boas structure (1977) answers a predecessor query in $O(\log w)$ time with $O(2^w)$ words of space. The y-fast trie of Willard (1983) uses hashing to answer queries in $O(\log w)$ time with $O(n)$ words. The time is worst case for a static set with perfect hashing, and expected amortized when the set changes. The [fusion tree](/fusion-tree/) answers a query in $O(\log n / \log w)$ time with $O(n)$ words. Taking the better of the y-fast trie and the fusion tree gives $O(\min(\log w, \log n / \log w))$ expected time with $O(n)$ words, which is $O(\sqrt{\log n})$ for every $w$, because the minimum of two numbers whose product is $\log n$ is at most $\sqrt{\log n}$. See [predecessor problem](/predecessor-problem/) and the [predecessor lower bound](/predecessor-lower-bound/).
- **Dictionaries.** A [hash table](/hash-table/) with a hash function such as multiply-shift supports search, insert and delete in $O(1)$ expected time per operation and $O(n)$ words of space. For a static set, the perfect hashing of Fredman, Komlós and Szemerédi (1984) gives $O(1)$ worst-case search with $O(n)$ words.
- **Bit operations.** The number of 1-bits of a word takes $O(\log w)$ steps with the instructions above. The position of the highest 1-bit takes $O(\log w)$ steps by binary search with shifts, and Fredman and Willard showed how to find it in $O(1)$ steps with multiplication. Many processors have one instruction for each of these, see [leading zero count](/leading-zero-count/).

## References
