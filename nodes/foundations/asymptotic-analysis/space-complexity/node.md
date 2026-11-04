---
tag: RF1AVH
kind: definition
slug: space-complexity
name: Space complexity
aliases:
- memory complexity
- working space
area: foundations/asymptotic-analysis
level: intro
summary: The function giving the amount of memory an algorithm uses as a function of input size.
prereqs: [input-size, asymptotic-notation]
see_also: [time-complexity, in-place-algorithm, word-ram, recursion, logspace, pspace, merge-sort, quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 (Section 2.3, merge sort) and Chapter 7 (quicksort, stack depth)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2 (sorting by exchanging, stack size of quicksort) and Section 5.2.3 (heapsort)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8 (Space Complexity)
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 4 (Space complexity)
---

The space complexity of an algorithm is the function $S$ that maps each [input size](/input-size/) $n$ to the number of memory cells that the algorithm uses on inputs of size $n$, in a stated model of computation. As for [time complexity](/time-complexity/), the definition must name the case (worst, average) and say what is counted. The usual choice is the worst case, counted in machine words, with the space of the recursion stack included.

## Definition

Fix a model, here the [word RAM](/word-ram/): memory is an array of cells, and each cell holds one word of $w$ bits, with $w \ge \lceil \lg n \rceil$ so that an index into the input fits in one word. Many texts write that a word has $\Theta(\log n)$ bits. For an algorithm $A$ and an input $x$, let $s_A(x)$ be the number of distinct cells that $A$ reads or writes during its run on $x$. Then the worst-case space is
$$S(n) = \max_{x \in I_n} s_A(x),$$
where $I_n$ is the set of inputs of size $n$. A cell that is allocated but never accessed is not counted. This is a convention. In practice an allocated array of $k$ words counts as $k$ words. The two measures agree for an algorithm that initializes all that it allocates.

### Total and auxiliary space

Total space counts every cell that the run accesses, including the cells of the input. Auxiliary space (also called working space) counts only the cells outside the input and the output. The auxiliary space is the useful measure for an algorithm that reads an array of $n$ items, because the input already takes $n$ cells.

Most texts on algorithms use a second convention: the whole input always counts, so the total space is the size of the input plus the auxiliary space. This page counts accessed cells, as defined above. Under this rule a sublinear-time algorithm such as [binary search](/binary-search/) accesses only $O(\log n)$ cells of its input. An algorithm is [in place](/in-place-algorithm/) when its auxiliary space is $O(1)$ words. Some authors also call an algorithm in place when it uses $O(\log n)$ auxiliary words, for example for a recursion stack.

### The recursion stack counts

Each active call of a [recursive](/recursion/) function holds a frame: its parameters, its local variables and its return address. A frame of a function with a constant number of variables has $O(1)$ words. So the stack space is $O(d)$ words, where $d$ is the greatest number of active calls at one time. A recursive algorithm that holds no other memory has auxiliary space $\Theta(d)$. Space is counted in words. In bits it is at most $w$ times larger. With the usual $w = \Theta(\log n)$, an array of $n$ indices needs $\Theta(n)$ words and $\Theta(n \log n)$ bits. A mark array of $n$ bits needs only $n$ bits.

### Time and space

Let each step of the machine access at most $c$ cells, where $c$ is a constant. A run of $T$ steps then accesses at most $cT$ distinct cells. So $S(n) \le c \, T(n)$: the space is at most a constant times the time. This is why an algorithm that must touch each of $n$ cells has $T(n) \ge n/c$. The converse is false. An $n$-bit [binary counter](/binary-counter-increment/) that counts from $0$ to $2^n - 1$ uses $n$ bits and $2^n - 1$ increments. For a [Turing machine](/turing-machine/) that halts on each input, with a read-only input tape and $S(n) \ge \log n$ cells on the work tapes, the time is at most $2^{O(S(n))}$, because a configuration is described by $O(S(n))$ bits plus the head positions and the number of different configurations bounds the time (Arora and Barak, Chapter 4). On the Turing machine one counts the work tape only, which makes sublinear classes such as [logarithmic space](/logspace/) possible, and [polynomial space](/pspace/) is the class with $S(n) = n^{O(1)}$.

## Examples and non-examples

Each entry is the auxiliary space in words for a sort of $n$ items or for a search.

- **[Linear search](/linear-search/), [selection sort](/selection-sort/), [insertion sort](/insertion-sort/).** A few indices and one temporary key. The space is $\Theta(1)$.
- **[Heapsort](/heapsort/).** The heap is built inside the input array, and a sift-down loop needs a constant number of words (two indices and one temporary key). The auxiliary space is $O(1)$, so heapsort is in place in the strict sense.
- **[Merge sort](/merge-sort/).** The merge step writes into a second array. A version with an auxiliary array of $n$ items has $\Theta(n)$ auxiliary space, and a version that copies only the left half before each merge needs $\lceil n/2 \rceil$ items. The recursion has depth $\lceil \lg n \rceil$, so it holds $\lceil \lg n \rceil + 1$ frames. The total auxiliary space is $\Theta(n)$, and the stack is of lower order.
- **[Quicksort](/quicksort/), stack space.** After a partition, the algorithm calls itself on the smaller side and continues with the larger side in a loop. A call is made only on a range of at least 2 items. With this rule the stack never holds more than $\lfloor \lg n \rfloor$ frames, for $n \ge 2$. The partition must put the pivot in its final place and leave it out of both ranges. Proof: a call at depth $d$ (the first call has depth $0$) starts with a range of $s_d$ items. At any time its frame works on a range of $r \le s_d$ items. A partition of this range leaves two ranges with $r - 1$ items in total, so the child call gets at most $(r-1)/2 < s_d/2$ items, and $s_{d+1} \le s_d/2$. Since $s_0 \le n$, we get $s_d \le n/2^d$. A call has $s_d \ge 2$, so $2 \le n/2^d$ and $d \le \lg n - 1$. The number of frames is at most $d + 1 \le \lg n$, and it is an integer. A version that recurses on both sides, with the last item as pivot, holds about $n$ frames on a sorted array, so its space is $\Theta(n)$ in the worst case.
- **Binary search.** The loop version uses $O(1)$ words. The recursive version holds $O(\log n)$ frames, unless the compiler removes tail calls.
- **[Breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/).** A search of a [graph](/graph/) with $n$ vertices and $m$ edges needs a mark for each vertex and a queue or a stack of at most $n$ vertices, when each vertex is marked as it is pushed (or when the depth-first search is recursive). Then the auxiliary space is $\Theta(n)$. An iterative depth-first search that pushes every neighbor without a test of the mark can hold $\Theta(m)$ entries.
- **Naive recursive [Fibonacci](/fibonacci-numbers/).** The function $\mathrm{fib}(n) = \mathrm{fib}(n-1) + \mathrm{fib}(n-2)$ makes calls to depth $n$, so it holds $n$ frames, and its space is $\Theta(n)$. Its time is exponential. This shows that space can be much smaller than time.
- **Non-example: a bound that omits the stack.** The statement "recursive quicksort or recursive binary search uses $O(1)$ extra space" is wrong once the stack is counted. Quicksort that recurses on the smaller side uses $\Theta(\log n)$ words in the worst case. A bound that omits the stack is a bound on the heap memory only, and it should say so.
- **Non-example: cumulative allocation.** A routine that allocates a new array of $k$ words in each of $n$ loop rounds and frees it at the end of the round has peak space $O(k)$. The sum of all allocations is $nk$ words. Space is the peak use, not the sum.

## Related definitions

- [Time complexity](/time-complexity/) counts steps. Space and time are two separate costs, and many algorithms trade one for the other.
- [In-place algorithm](/in-place-algorithm/): auxiliary space $O(1)$, or $O(\log n)$ in the weaker use.
- [Word RAM](/word-ram/): the model with words of $\Theta(\log n)$ bits in which space is counted in words.
- [Logarithmic space](/logspace/) and [polynomial space](/pspace/): the complexity classes that bound the space of a Turing machine.
- [Input size](/input-size/): the argument of $S$.

## References
