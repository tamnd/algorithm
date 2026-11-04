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
  - paper: doi:10.1007/BFb0028575
    title: Torben Hagerup, Sorting and searching on the word RAM, STACS 1998, Lecture Notes in Computer Science 1373
    locator: pp. 366 to 398 (the definition of the model, its instruction sets, and a survey of results)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (the RAM model and the word size c lg n)
  - paper: "Michael L. Fredman and Dan E. Willard, Surpassing the information theoretic bound with fusion trees, Journal of Computer and System Sciences 47(3) (1993)"
    locator: the fusion tree, the sorting bound, and the constant-time most significant bit
  - paper: "Michael L. Fredman and Dan E. Willard, Trans-dichotomous algorithms for minimum spanning trees and shortest paths, Journal of Computer and System Sciences 48(3) (1994)"
    locator: the introduction, where the term trans-dichotomous is defined
  - paper: "Yijie Han and Mikkel Thorup, Integer sorting in O(n sqrt(log log n)) expected time and linear space, 43rd Annual Symposium on Foundations of Computer Science (FOCS 2002)"
    locator: abstract (the main result)
  - paper: "Yijie Han, Deterministic sorting in O(n log log n) time and linear space, Journal of Algorithms 50(1) (2004)"
    locator: abstract (the main result)
  - paper: "Peter van Emde Boas, Preserving order in a forest in less than logarithmic time and linear space, Information Processing Letters 6(3) (1977)"
    locator: the O(log log U) priority queue
  - paper: "Dan E. Willard, Log-logarithmic worst-case range queries are possible in space Theta(N), Information Processing Letters 17(2) (1983)"
    locator: the y-fast trie
  - paper: "Paul Beame and Faith E. Fich, Optimal bounds for the predecessor problem and related problems, Journal of Computer and System Sciences 65(1) (2002)"
    locator: abstract (matching upper and lower bounds for static predecessor search with polynomial space)
  - paper: "Martin Dietzfelbinger, Torben Hagerup, Jyrki Katajainen and Martti Penttonen, A reliable randomized algorithm for the closest-pair problem, Journal of Algorithms 25(1) (1997)"
    locator: the multiply-shift hash family and its collision bound
  - paper: "Arne Andersson, Torben Hagerup, Stefan Nilsson and Rajeev Raman, Sorting in linear time?, Journal of Computer and System Sciences 57(1) (1998)"
    locator: abstract (signature sort, and the AC0 instruction set)
  - paper: "Michael L. Fredman, Janos Komlos and Endre Szemeredi, Storing a sparse table with O(1) worst case access time, Journal of the ACM 31(3) (1984)"
    locator: abstract (the main result)
  - paper: doi:10.1109/SWAT.1974.20
    title: Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974)
    locator: pp. 13 to 23
---

The word RAM is a [random access machine](/random-access-machine/) whose memory cells hold words of $w$ bits, where each operation on one or two words costs one step. It is the [unit-cost model](/unit-cost-model/) with a bound on the size of a number. The usual assumption is $w \ge \lg n$, so that a word can hold the index of any input item. This is the model behind almost every running time on this site that does not name another model.

## The machine

**Memory.** The memory is an array of cells $M[0], M[1], M[2], \ldots$. Each cell holds a word: an integer in the range $0$ to $2^w - 1$, which the machine can also treat as a bit string of length $w$. A word can be used as an address, so the machine reads and writes $M[M[i]]$ (indirect addressing). The program is fixed and is not stored in the memory. It has a constant number of registers of $w$ bits.

**Input.** An input of size $n$ is $n$ words in $M[0]$ to $M[n-1]$. When an item is longer than one word (a long string or a big integer), the input size counts words, not items.

**Instructions.** Each of these costs one step:

- addition and subtraction modulo $2^w$, and in most definitions multiplication modulo $2^w$ and integer division with remainder;
- comparison of two words, and a conditional jump;
- the bitwise operations AND, OR, XOR and NOT;
- left and right shifts by any number of bits from $0$ to $w$;
- a read or a write of the cell whose address is in a register.

Definitions differ in the exact list (Hagerup 1998 compares them). Some leave out multiplication and division, because neither is in [AC0](/ac0/): no circuit family of constant depth and polynomial size computes them. The *AC$^0$ RAM* of Andersson, Hagerup, Nilsson and Raman (1998) allows only instructions in AC$^0$, which include addition, comparison, the bitwise operations and shifts. A result on the word RAM should say which instructions it uses.

**The word size.** The model has two parameters, $n$ and $w$. The condition $w \ge \lg n$ is needed: with fewer bits, a word cannot hold the address of each input item. A run that uses cells up to address $S - 1$ needs $w \ge \lg S$, so a polynomial space needs $w = \Omega(\log n)$ with a larger constant. CLRS takes $w = c \lg n$ for a constant $c \ge 1$, which fixes $w = \Theta(\log n)$ and keeps the machine from doing too much work in one step. Fredman and Willard call an algorithm *trans-dichotomous* if its bound holds for every $w \ge \lg n$, because it bridges the size of the problem and the size of the machine (see [transdichotomous model](/transdichotomous-model/)). The algorithm cannot choose $w$: it runs on the $w$ of the machine that it is given. A bound on integer data is often a function of both $n$ and $w$, and some results hold only for a range of $w$, such as signature sort below.

## What it counts

The time of a run is the number of instructions that it executes. Each instruction costs 1, whatever the values of its words. The space is the largest address in use, plus one, in words, so a space of $s$ words is $s w$ bits. The space can be much larger than the number of cells in use when the program uses its memory sparsely. Hashing is the usual way to close the gap. Bounds are worst-case unless they say expected (over the random bits of the algorithm) or amortized.

**Why the bound on $w$ matters.** With no bound on the size of a number, unit cost gives too much power. Start with $x = 2$ and square it $k$ times. After $k$ steps $x = 2^{2^k}$, a number with $2^k + 1$ bits. Hartmanis and Simon (1974) showed that a RAM with unit-cost multiplication and bitwise operations on unbounded integers decides in polynomial time exactly the languages in [PSPACE](/pspace/) (see the [unit-cost model](/unit-cost-model/)). On the word RAM each number has at most $w$ bits, and the analysis states how the bound depends on $w$. With $w = O(\log n)$, each instruction is a constant number of operations on $O(\log n)$ bits.

**Word-level parallelism.** One instruction acts on all $w$ bits at once, so an algorithm can pack several small fields into one word and process them together. The number of 1-bits of a word (its [population count](/population-count/)) takes $\lg w$ rounds when $w$ is a power of 2. Round $r$ adds pairs of neighbouring fields of $2^{r-1}$ bits, with one mask, one shift and one addition, and gives fields of $2^r$ bits. Example with $w = 8$ and $x = 10110111$ (six 1-bits): the first round with mask $01010101$ gives $01\,10\,01\,10$ (the counts 1, 2, 1, 2), the second with mask $00110011$ gives $0011\,0011$ (3 and 3), and the third with mask $00001111$ gives $00000110$, which is 6. For $w = 64$ this is 6 rounds, whatever the number of 1-bits. [Fusion trees](/fusion-tree/) and the fast integer sorts are built from tricks of this kind (see [bit parallelism](/bit-parallelism/)).

**Hashing.** Multiplication modulo $2^w$ gives fast hash functions. The multiply-shift family of Dietzfelbinger, Hagerup, Katajainen and Penttonen (1997) maps a $w$-bit key $x$ to $\ell$ bits by

$$h_a(x) = \left\lfloor \frac{a x \bmod 2^w}{2^{w-\ell}} \right\rfloor,$$

for a random odd $a$ with $0 < a < 2^w$. It costs one multiplication and one shift. For two distinct keys the probability of a collision is at most $2/2^\ell$. Example with $w = 8$, $\ell = 3$, $a = 181$ and $x = 77$: $a x = 13937$, $13937 \bmod 256 = 113$, and $\lfloor 113 / 32 \rfloor = 3$. See [multiply-shift hashing](/multiply-shift-hashing/).

## Relation to other models

- **Unit-cost and logarithmic-cost RAM.** The word RAM with $w = \Theta(\log n)$ is the unit-cost RAM with a bound on the size of numbers. A run of $t$ steps on it costs $O(t \log n)$ in the [logarithmic-cost model](/logarithmic-cost-model/), because each instruction touches a constant number of words of $O(\log n)$ bits. So a polynomial bound on such a word RAM gives a polynomial bound on a [Turing machine](/turing-machine/) (see [RAM and Turing machine equivalence](/ram-turing-equivalence/)).
- **Comparison model.** In the [comparison model](/comparison-model/) an algorithm learns about the keys only by comparing two of them. A comparison algorithm runs on the word RAM with the same number of steps, up to a constant factor. The word RAM can also use the bits of the keys, as [radix sort](/radix-sort/) does, so the [comparison sort lower bound](/comparison-sort-lower-bound/) of $\Omega(n \log n)$ does not hold on it.
- **Pointer machine.** A [pointer machine](/pointer-machine/) follows and creates pointers but does no arithmetic on addresses. The word RAM can compute an address, so it can index an array and use a hash table.
- **Cell-probe model.** The [cell-probe model](/cell-probe-model/) also has cells of $w$ bits, but it counts only the cells that a run reads or writes, and computation is free. Each word RAM algorithm gives a cell-probe algorithm with no more probes than steps, so a lower bound in the cell-probe model is a lower bound on the word RAM.
- **Real RAM.** The [real RAM](/real-ram/) of computational geometry holds exact real numbers, with unit-cost arithmetic and no bitwise operations or floor function. It is not a word RAM, and results do not move between the two models without care.
- **Parallel models.** A word of $w$ bits with bitwise operations is a small parallel machine with $w$ processors that work in lockstep on one bit each. The [PRAM](/pram-model/) is the model with many full processors.

## Known results in the model

Here $n$ is the number of items, each item is one word, and $w \ge \lg n$.

- **Sorting integers.** [Radix sort](/radix-sort/) with digits of $\lceil \lg n \rceil$ bits sorts $n$ words in $O(n \lceil w / \lg n \rceil)$ time, which is $O(n)$ when $w = O(\log n)$. For example, $n = 2^{20}$ keys of $w = 64$ bits need $\lceil 64/20 \rceil = 4$ passes of [counting sort](/counting-sort/), each in $O(n + 2^{20})$ time. For every $w$, Fredman and Willard (1993) sort in $O(n \log n / \log \log n)$ time with fusion trees, which beats the comparison bound. Han (2004) sorts deterministically in $O(n \log \log n)$ time and linear space, and Han and Thorup (2002) sort in $O(n \sqrt{\log \log n})$ expected time and linear space. Signature sort (Andersson, Hagerup, Nilsson and Raman 1998) sorts in $O(n)$ expected time when $w \ge (\lg n)^{2+\varepsilon}$ for a constant $\varepsilon > 0$. Whether $n$ words can be sorted in $O(n)$ time for every $w$ is open. See [integer sorting](/integer-sorting/).
- **Predecessor search.** For a set of $n$ keys from $\{0, \ldots, 2^w - 1\}$, the structure of van Emde Boas (1977) answers a predecessor query in $O(\log w)$ time with $O(2^w)$ words of space. The y-fast trie of Willard (1983) answers a query in $O(\log w)$ time with $O(n)$ words, with the help of hashing; the time is worst case for a static set with [perfect hashing](/perfect-hashing/), and expected amortized when the set changes. The [fusion tree](/fusion-tree/) answers a query in $O(\log n / \log w)$ time with $O(n)$ words. The better of the two gives $O(\min(\log w, \log n / \log w))$, which is $O(\sqrt{\log n})$ for every $w$: the two terms have product $\log n$, so the smaller one is at most $\sqrt{\log n}$. Beame and Fich (2002) improved the static bound to $O(\min(\log w / \log \log w, \sqrt{\log n / \log \log n}))$ with polynomial space, and proved that this is optimal for deterministic structures with polynomial space, in the [cell-probe model](/cell-probe-model/). See the [predecessor problem](/predecessor-problem/) and the [predecessor lower bound](/predecessor-lower-bound/).
- **Dictionaries.** A [hash table](/hash-table/) with a hash function such as multiply-shift supports search, insert and delete in $O(1)$ expected time per operation and $O(n)$ words of space. For a static set, the perfect hashing of Fredman, Komlós and Szemerédi (1984) gives $O(1)$ worst-case search with $O(n)$ words (see [FKS perfect hashing](/fks-perfect-hashing/)).
- **Bit operations.** The population count takes $O(\log w)$ steps with the instructions above. The position of the highest 1-bit takes $O(\log w)$ steps by binary search with shifts, and Fredman and Willard (1993) found it in $O(1)$ steps with multiplication. Many processors have one instruction for each of these (see [leading zero count](/leading-zero-count/)).

### Pitfalls

- **"Linear-time radix sort" without a word size.** Radix sort takes $O(n)$ time only when $w = O(\log n)$. For $w = 64$ and $n = 1000$ it needs $\lceil 64/10 \rceil = 7$ passes with digits of 10 bits, and for keys of $w = n$ bits it is no better than comparison sorting.
- **Unbounded words.** A word RAM with $w$ much larger than $\log n$ is close to the unit-cost RAM with no bound, and a bound that needs such a $w$ must say so. A trans-dichotomous bound holds for every $w \ge \lg n$; a bound such as that of signature sort holds only for large $w$.
- **Multiplication is not always free.** Multiplication and division are not in AC$^0$, and some results are stated for the AC$^0$ RAM without them. Check the instruction set before you combine two results.
- **Expected versus worst case.** Hash tables give $O(1)$ expected time, not worst case, and the bound holds over the random choice of the hash function, not over random inputs.
- **Space as the largest address.** An algorithm that writes to a few cells at large addresses uses a large space in this model. Hashing the addresses reduces the space to the number of cells in use, at the cost of randomization.
- **Big integers.** A key of many words is not one word. An operation on two keys of $k$ words each costs $\Theta(k)$ steps or more, so a bound in items must be converted to a bound in words.

## References
