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
summary: The function that gives the memory an algorithm uses on inputs of size n, in the worst case and in a stated model, usually in words and with the recursion stack included.
prereqs: [input-size, asymptotic-notation, time-complexity]
see_also: [in-place-algorithm, word-ram, recursion, logspace, pspace, savitch-theorem, merge-sort, quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (merge sort and its extra array) and Chapter 7 (quicksort, the chapter problem on stack depth)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.2 (Algorithm Q, the stack of at most lg N entries) and Section 5.2.3 (heapsort)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Chapter 8, Space Complexity (the work tape, PSPACE, L and NL)
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 4, Space complexity (configurations and the bound of time by space)
---

The space complexity of an algorithm is the function $S$ that maps each [input size](/input-size/) $n$ to the amount of memory that the algorithm uses on inputs of size $n$, in a stated model of computation. As for [time complexity](/time-complexity/), the definition must name the case and say what it counts. The usual choice is the worst case, counted in machine words, without the input and the output, and with the [recursion](/recursion/) stack included.

## Definition

**The model.** Use the [word RAM](/word-ram/): memory is an array of cells, and each cell holds one word of $w$ bits, with $w \ge \lceil \lg n \rceil$ so that an index into the input fits in one word. Many texts write that a word has $\Theta(\log n)$ bits. The input occupies $n$ cells, one item in each, and the output has cells of its own.

**The count of one run.** For an algorithm $A$ and an input $x$, let $s_A(x)$ be the number of distinct cells, other than the cells of the input and of the output, that $A$ reads or writes during its run on $x$. These cells hold the variables, the buffers, the heap memory and the frames of the call stack.

**Auxiliary space.** The worst-case auxiliary space (also called extra space or working space) is

$$S(n) = \max_{x \in I_n} s_A(x),$$

where $I_n$ is the set of inputs of size $n$. When a page of this reference gives the space of an algorithm, it means this function. The **total space** adds the cells of the input and the output, so it is $S(n) + \Theta(n)$ for an input of $n$ items. Auxiliary space is the useful measure for an algorithm that reads all of an array, because the total space of each such algorithm is at least $n$ and so tells nothing.

**Conventions.** A cell that is allocated but never touched is not counted by $s_A$. In practice an allocated array of $k$ words counts as $k$ words, and the two counts agree for an algorithm that initializes what it allocates. A cell that is used, freed, and used again counts once, so $S$ measures the peak use, not the sum of all allocations. An algorithm is [in place](/in-place-algorithm/) when $S(n) = O(1)$ words. Some authors also call an algorithm in place when $S(n) = O(\log n)$ words, for example for a recursion stack.

**Words and bits.** Space in bits is at most $w$ times the space in words. With $w = \Theta(\log n)$, an array of $n$ indices takes $\Theta(n)$ words and $\Theta(n \log n)$ bits, while $n$ one-bit marks packed into words take $n$ bits and $\lceil n/w \rceil$ words.

### The recursion stack counts

Each active call of a recursive function holds a frame: its parameters, its local variables and its return address. A frame of a function with a constant number of variables takes $O(1)$ words. So the stack takes $\Theta(d)$ words, where $d$ is the largest number of calls that are active at the same time. A recursive algorithm that holds no other memory has auxiliary space $\Theta(d)$.

### Space and time

Let each step of the machine touch at most $c$ cells, for a constant $c$. A run of $t$ steps then touches at most $ct$ distinct cells, so $S(n) \le c \, T(n)$, where $T$ is the worst-case time. The space is at most a constant times the time. The converse fails: an $n$-bit [binary counter](/binary-counter-increment/) that counts from 0 to $2^n - 1$ uses $n$ bits and makes $2^n - 1$ increments.

In the other direction, the time is at most exponential in the space. Take a [Turing machine](/turing-machine/) with a read-only input tape and work tapes that use $S(n) \ge \log n$ cells, and that halts on every input. A configuration is the state, the head positions and the contents of the work tapes, so there are at most $2^{O(S(n))}$ of them. A halting run never repeats a configuration, because a deterministic machine that repeats one loops for ever. So the time is at most $2^{O(S(n))}$ (Arora and Barak, Chapter 4). On the Turing machine one counts the work tapes only. This makes classes below linear space possible, such as [logarithmic space](/logspace/). [Polynomial space](/pspace/) is the class of problems with $S(n) = n^{O(1)}$, and [Savitch's theorem](/savitch-theorem/) shows that nondeterminism adds at most a square to the space.

## Examples and non-examples

Each entry gives the auxiliary space in words.

- **[Linear search](/linear-search/), [selection sort](/selection-sort/), [insertion sort](/insertion-sort/).** A few indices and one temporary key. The space is $\Theta(1)$.
- **[Heapsort](/heapsort/).** The heap is built inside the input array, and an iterative sift-down needs two indices and one temporary key. The space is $O(1)$, so heapsort is in place in the strict sense.
- **[Merge sort](/merge-sort/).** The merge writes into a second array. A version with one buffer of $n$ items has $\Theta(n)$ auxiliary space. The version on the page of merge sort copies only the left half before each merge, so its buffer needs at most $\lceil n/2 \rceil$ items. The recursion has depth $\lceil \lg n \rceil$, so at most $\lceil \lg n \rceil + 1$ frames are active. The total is $\Theta(n)$, and the stack is of lower order.
- **[Quicksort](/quicksort/), smaller side first.** After a partition, the algorithm calls itself on the smaller side and continues with the larger side in a loop. It makes a call only on a range of at least 2 items. The partition puts the pivot in its final place and leaves it out of both ranges. Then at most $\lfloor \lg n \rfloor$ frames are active, for $n \ge 2$. *Proof.* Number the active calls by depth, with depth 0 for the first call. Let $s_d$ be the size of the range when the active call at depth $d$ starts. While this call runs, it works on a range of $r \le s_d$ items. A partition of this range leaves two ranges with $r - 1$ items in total, so the smaller one, which goes to the call at depth $d + 1$, has at most $(r - 1)/2 < s_d / 2$ items. So $s_{d+1} < s_d/2$ and $s_d \le n/2^d$. A call needs $s_d \ge 2$, so $2^{d+1} \le n$ and $d \le \lg n - 1$. The number of frames is at most $d + 1 \le \lg n$, and it is an integer. $\square$ Knuth's Algorithm Q (Volume 3, Section 5.2.2) uses the same rule with an explicit stack.
- **Quicksort, both sides by recursion.** With the last item as pivot, a sorted array of $n$ items leaves the right side empty at each step, so the calls nest $n - 1$ deep. For $n = 1000$ this is 999 active frames. The smaller-side rule on the same input has 1 frame, because the smaller side is always empty and the loop does all the work. So the plain version has $\Theta(n)$ space in the worst case.
- **[Binary search](/binary-search/).** The loop version uses $O(1)$ words. The recursive version holds up to $\lfloor \lg n \rfloor + 1$ frames, so $\Theta(\log n)$ words, unless the compiler turns the tail call into a jump.
- **[Breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/).** A search of a [graph](/graph/) with $n$ vertices and $m$ edges needs a mark for each vertex and a queue or stack of at most $n$ vertices, when it marks each vertex as it pushes it. Then the auxiliary space is $\Theta(n)$. An iterative depth-first search that pushes every neighbor without a test of the mark can hold $\Theta(m)$ entries.
- **Naive recursive [Fibonacci](/fibonacci-numbers/).** $\mathrm{fib}(n) = \mathrm{fib}(n-1) + \mathrm{fib}(n-2)$ nests calls $n$ deep, through $\mathrm{fib}(n), \mathrm{fib}(n-1), \ldots, \mathrm{fib}(1)$, so it holds $n$ frames and its space is $\Theta(n)$. Its time is exponential in $n$, so space can be far smaller than time.
- **Non-example: a bound that omits the stack.** "Recursive quicksort uses $O(1)$ extra space" is wrong once the stack counts: the smaller-side version uses $\Theta(\log n)$ words in the worst case, and the plain version $\Theta(n)$. A bound that omits the stack is a bound on the heap memory only, and it must say so.
- **Non-example: the sum of allocations.** A routine that allocates an array of $k$ words in each of $n$ rounds, and frees it at the end of the round, has auxiliary space $O(k)$, not $nk$.

### Pitfalls

- **Counting the input.** The total space of a sort is always at least $n$. Compare algorithms by auxiliary space.
- **Forgetting the stack.** Recursion uses memory even when the code allocates nothing. Bound the largest number of active calls.
- **Words against bits.** $O(n)$ words is $O(n \log n)$ bits. Bounds in complexity theory usually count bits, and bounds for algorithms usually count words.
- **"In place" with two meanings.** Say whether you mean $O(1)$ or $O(\log n)$ extra words.
- **Small space does not mean small time.** $S(n) \le c\,T(n)$ holds, but the binary counter shows that a small space allows a huge time.

## Related definitions

- [Time complexity](/time-complexity/) counts steps. Many algorithms trade one resource for the other.
- [In-place algorithm](/in-place-algorithm/): auxiliary space $O(1)$, or $O(\log n)$ in the weaker use.
- [Word RAM](/word-ram/): the model in which space is counted in words of $\Theta(\log n)$ bits.
- [Logarithmic space](/logspace/) and [polynomial space](/pspace/): the classes of problems defined by bounds on the work space of a Turing machine.
- [Input size](/input-size/): the argument of $S$.

## References
