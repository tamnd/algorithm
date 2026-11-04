---
tag: 1H3ZJ5
kind: definition
slug: time-complexity
name: Time complexity
aliases:
- running time
- time bound
area: foundations/asymptotic-analysis
level: intro
summary: The function T(n) that gives the worst-case, best-case or average number of steps of an algorithm on inputs of size n, in a stated model of computation.
prereqs: [input-size, asymptotic-notation]
see_also: [worst-case-analysis, order-of-growth, best-case-analysis, average-case-analysis, word-ram, space-complexity]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Chapter 2
  - paper: "F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8 (1965)"
    locator: the lower bound for palindromes by crossing sequences
---

The time complexity of an algorithm is the function $T$ that maps each input size $n$ to the number of steps that the algorithm takes on inputs of size $n$, counted in a stated model of computation. Because many inputs have the same size, the definition must say which input it uses: the worst, the best or the average one. The result is a function of $n$, and you describe its growth with [asymptotic notation](/asymptotic-notation/).

## Definition

Fix a model of computation, a way to measure the [size of an input](/input-size/), and a set $I_n$ of the inputs of size $n$. The usual model is the [random-access machine](/random-access-machine/) with [unit cost](/unit-cost-model/): each basic operation (an arithmetic operation on a word, a comparison, a read or a write of one memory cell, a jump) costs one step. Unit cost is fair when each word has $\Theta(\log n)$ bits: at least $\lg n$, so that a word holds an index into the input, and not much more. The [word RAM](/word-ram/) makes this precise. When the numbers can grow without a bound, use the [logarithmic cost model](/logarithmic-cost-model/), where an operation costs the number of bits of its operands.

For an algorithm $A$ and an input $x$, let $t_A(x) \in \mathbb{N} \cup \{\infty\}$ be the number of steps that $A$ takes on $x$, with $t_A(x) = \infty$ when $A$ does not stop on $x$. Then, for each $n \in \mathbb{N}$ with $I_n \ne \emptyset$:

- The **worst-case time** is $T_{\max}(n) = \sup_{x \in I_n} t_A(x)$. When $I_n$ is finite, this is a maximum.
- The **best-case time** is $T_{\min}(n) = \min_{x \in I_n} t_A(x)$.
- The **average-case time** is $T_{\mathrm{avg}}(n) = \sum_{x \in I_n} \Pr[x] \cdot t_A(x)$, for a stated probability distribution on $I_n$. For sorting, the usual choice makes each of the $n!$ relative orders of distinct keys equally likely.

When a page says "the time complexity" with no other word, it means $T_{\max}$. When $A$ stops on each input, each $T$ is a function from the sizes $n$ with $I_n \ne \emptyset$ to the non-negative reals, so you can write $T(n) = O(g(n))$, $T(n) = \Omega(g(n))$ or $T(n) = \Theta(g(n))$. These three statements are about the function $T$ for one fixed case. They are not the same as the three cases. The sentence "the best-case time of [insertion sort](/insertion-sort/) is $O(n^2)$" is correct, and it uses $O$ with the best case.

The exact value of $T(n)$ depends on the model, the language and the machine. The class of $T$ under $\Theta$ depends much less on them: a change of the constant cost per operation changes $T$ by a constant factor only. A change of the model can change more than a constant. A [single-tape Turing machine](/turing-machine/) needs $\Omega(n^2)$ steps to decide if a string is a palindrome, but a RAM does it in $O(n)$ steps. This is why bounds in this reference use asymptotic notation, and why they always name the model.

Two other costs use the same notation. An [amortized](/amortized-cost/) bound is a bound on the average cost of an operation over a worst-case sequence. An expected bound is an average over the random choices of the algorithm, not over the inputs. Neither is a case of the definition above.

For each $n$, $T_{\min}(n) \le T_{\mathrm{avg}}(n) \le T_{\max}(n)$. An upper bound on $T_{\max}$ bounds each input of size $n$, but a lower bound on $T_{\max}$ only says that some input is slow.

## Examples and non-examples

- Linear search in an array of $n \ge 1$ items, with the cost of one comparison as one step: $T_{\min}(n) = 1$, $T_{\max}(n) = n$, and $T_{\mathrm{avg}}(n) = (n+1)/2$ when the key is in the array at a uniform random place. So $T_{\max}(n) = \Theta(n)$ and $T_{\min}(n) = \Theta(1)$. See [worst-case analysis](/worst-case-analysis/) for the count.
- Insertion sort, counted in key comparisons: $T_{\min}(n) = n - 1$ and $T_{\max}(n) = n(n-1)/2$ for $n \ge 1$. The minimum occurs on the sorted array and the maximum on the reverse-sorted array. For 8 items they are 7 and 28 comparisons.
- Not a function of $n$ alone: "the algorithm takes 3 seconds". This is one measurement on one machine and one input. It is not a time complexity.
- Not a time complexity: "the algorithm runs fast on most inputs". With no case and no model, the statement does not define a function.
- Non-example of a finite time: a loop that runs until a value is found, on an input where the value never occurs, has $t_A(x) = \infty$. Then $T_{\max}(n) = \infty$, and no $O$ bound holds. An algorithm must stop on each input of $I_n$ to have a finite worst-case time.
- A trap with the size: [trial division](/trial-division/) tests if $N$ is prime with about $\sqrt{N}$ divisions. This looks small, but the input size is the number of bits $b = \lceil \lg(N+1) \rceil$, and $\sqrt{N}$ is about $2^{b/2}$. The time is exponential in $b$. A bound that is polynomial in the value of a number but not in its length is [pseudo-polynomial](/pseudo-polynomial-time/).

## Related definitions

- [Worst-case analysis](/worst-case-analysis/) studies $T_{\max}$. [Best-case analysis](/best-case-analysis/) studies $T_{\min}$. [Average-case analysis](/average-case-analysis/) studies $T_{\mathrm{avg}}$.
- [Order of growth](/order-of-growth/) is the class of $T$ that remains when you drop the constant factors and the lower terms.
- [Space complexity](/space-complexity/) is the same idea for the number of memory cells.
- The [comparison model](/comparison-model/) is a model where the cost counts only the comparisons between items.
- [Input size](/input-size/) fixes what $n$ means. For a graph, the time is often a function of two numbers, the count of vertices and the count of edges. See [multivariate asymptotic notation](/multivariate-asymptotic-notation/).

## References
