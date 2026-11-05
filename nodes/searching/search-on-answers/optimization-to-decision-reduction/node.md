---
tag: 8NXMP0
kind: concept
slug: optimization-to-decision-reduction
name: Optimization-to-decision reduction
aliases:
- decision version of an optimization problem
- search-by-decision reduction
area: searching/search-on-answers
level: intro
summary: Turn an optimization question into a sequence of feasibility questions asking whether a value k is achievable.
prereqs: [monotone-predicate, decision-problem]
see_also: [binary-search-on-answer, search-to-decision-reduction, parametric-search, binary-search-on-real-numbers, exponential-search, minimum-bottleneck-spanning-tree, turing-reduction]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 34, the overview at the start of the chapter (decision problems versus optimization problems)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: Chapter 5, NP-hardness (Turing reductions between the optimization and decision forms of the travelling salesman problem)
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 4.3.2, Finding Optimal Solutions
---

The optimization-to-decision reduction finds the optimal value of a minimization problem by asking only yes/no questions of the form "is there a solution of cost at most $t$?". The answers form a [monotone predicate](/monotone-predicate/) in $t$, so a [binary search](/binary-search/) over the possible values finds the optimum with a logarithmic number of questions. It is the reason why complexity theory can study [decision problems](/decision-problem/) in place of optimization problems, and it is the base of the [binary search on the answer](/binary-search-on-answer/) technique.

## In plain words

Some questions are hard to answer directly but easy to check. "What is the smallest truck that can carry these boxes in five trips?" is hard. "Can a truck of size twenty do it?" is easy: you load it and count the trips.

The checking question has a useful shape. If a truck of size twenty can do it, a bigger truck can do it too. So the answers are "no" for all the small sizes and "yes" for all the large ones. The smallest size is the place where "no" turns into "yes". You find that place as you find a word in a dictionary: ask about the middle size, keep the half that holds the change, and repeat. Each question halves the sizes that are left, so a few questions are enough.

## The idea

**The two problems.** Let $S$ be a set of feasible solutions and $f : S \to \mathbb{R}$ a cost. The optimization problem asks for $\mathrm{OPT} = \min_{s \in S} f(s)$ (assume the minimum exists). Its **decision version** is the family of questions

$$D(t):\quad \text{is there an } s \in S \text{ with } f(s) \le t\,?$$

For a maximization problem the question is "is there an $s$ with $f(s) \ge t$?", and everything below holds with the order reversed.

**The key fact.** $D(t)$ is true if and only if $\mathrm{OPT} \le t$. *Proof.* If $\mathrm{OPT} \le t$, an optimal $s^*$ has $f(s^*) = \mathrm{OPT} \le t$. If some $s$ has $f(s) \le t$, then $\mathrm{OPT} \le f(s) \le t$. $\square$ So $D$ is a monotone predicate in $t$, and $\mathrm{OPT}$ is its threshold: the smallest $t$ with $D(t)$ true.

**Integer costs.** Suppose $\mathrm{OPT}$ is an integer and $L \le \mathrm{OPT} \le U$ is known. A first-true binary search over $\{L, \ldots, U\}$ finds $\mathrm{OPT}$. Because $D(U)$ is known to be true, the search only needs to tell apart the $U - L + 1$ possible thresholds, and it uses at most $\lceil \lg(U - L + 1) \rceil$ calls of $D$. This is also the least number of calls that any method based only on $D$ can guarantee, since each call has two outcomes.

**Finite candidate sets.** Often $\mathrm{OPT}$ is known to lie in a finite set $C$ of candidates, such as the edge weights of a graph or the pairwise distances of points. Sort $C$ as $c_1 < c_2 < \cdots < c_N$ and search on the index: the predicate $i \mapsto D(c_i)$ is monotone, and $\lceil \lg N \rceil$ calls suffice when $D(c_N)$ is known to be true. When $C$ is too large to list, it can often be searched implicitly, as in [selection in a sorted matrix](/sorted-matrix-selection/) or [parametric search](/parametric-search/).

**Real costs.** When the optimum is a real number in $[L, U]$, a [bisection on real numbers](/binary-search-on-real-numbers/) finds it to within $\varepsilon$ with $\lceil \lg((U - L)/\varepsilon) \rceil$ calls. An exact value needs extra structure, for example the candidate set above or a bound on the denominators of rational answers.

**No known upper bound.** If only $L$ is known, [exponential search](/exponential-search/) tries $t = L, L + 1, L + 3, L + 7, \ldots$ until $D$ is true, and then searches the last gap. It uses about $2 \lg(\mathrm{OPT} - L + 1)$ calls.

**Total cost.** If one call of $D$ costs $T_D$, the reduction costs $O(T_D \log(U - L + 1))$. When the costs are integers with $b$ bits, $\log(U - L + 1) = O(b)$, which is polynomial in the input size. So a polynomial-time decision algorithm gives a polynomial-time algorithm for the optimal value. The converse is immediate: one optimization call answers $D(t)$ by comparing $\mathrm{OPT}$ with $t$. This is the sense in which the two forms are equivalent under [Turing reductions](/turing-reduction/), and it is why NP-completeness is stated for decision problems.

**The value is not the solution.** The search returns $\mathrm{OPT}$, not a solution $s^*$. Often the last successful call of $D$ builds a witness as a side effect, for example the greedy partition that showed a capacity to be enough. If $D$ only answers yes or no, a [search-to-decision reduction](/search-to-decision-reduction/) builds a solution by fixing its parts one at a time and asking $D(\mathrm{OPT})$ about the restricted instances.

## Examples

**A bottleneck spanning tree.** Take the graph on vertices $0$ to $4$ with weighted edges $(0,1,4)$, $(0,2,9)$, $(1,2,2)$, $(1,3,7)$, $(2,3,5)$, $(3,4,6)$ and $(2,4,11)$. The goal is a spanning tree whose largest edge weight is as small as possible, the [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/). The decision question $D(t)$ is "do the edges of weight at most $t$ connect the graph?", answered by one graph search. The optimum is one of the 7 edge weights $2, 4, 5, 6, 7, 9, 11$. A binary search on this sorted list asks $D(6)$ (yes), $D(4)$ (no) and $D(5)$ (no), and returns $6$. Three calls are enough because $\lceil \lg 7 \rceil = 3$.

**The travelling salesman problem.** With integer edge weights at most $W$ on $n$ vertices, the shortest tour has length in $\{0, \ldots, nW\}$. So $\lceil \lg(nW + 1) \rceil$ calls of the decision version "is there a tour of length at most $t$?" give the optimal length. This is the classic argument that the decision version, which is NP-complete, is as hard as the optimization version up to a polynomial factor.

**Shipping within a deadline.** Packages of weights $1, 2, \ldots, 10$ must leave in order within 5 days. The decision question "is capacity $c$ enough?" is answered by greedy loading in linear time, and the smallest enough capacity is 15. The page on [monotone predicates](/monotone-predicate/) gives the trace.

**A maximization.** For [maximin placement](/maximin-placement/) the question is "can $k$ points be placed with all gaps at least $d$?". It is true for small $d$ and false for large $d$, so the search looks for the last true value instead of the first.

## Where it is used

- **Complexity theory.** P, NP and NP-completeness are defined for decision problems. The reduction above shows that nothing is lost for optimization problems with polynomially many bits in the cost.
- **[Binary search on the answer](/binary-search-on-answer/).** The programming technique that applies the reduction when the decision question has a fast greedy or graph test: [linear partition](/minimax-partition/), [maximin placement](/maximin-placement/), the [k-th smallest pair distance](/kth-smallest-pair-distance/).
- **[Parametric search](/parametric-search/).** Megiddo's method finds an exact real optimum by running a decision algorithm at the unknown optimum and resolving each comparison with calls of $D$.
- **Ratio objectives.** The question "is there a solution with ratio at most $\lambda$?" turns into "is $\min_s (a(s) - \lambda b(s)) \le 0$?" for a ratio $a(s)/b(s)$ with $b > 0$, which is the base of [fractional programming](/fractional-programming/) and of [Dinkelbach's algorithm](/dinkelbach-algorithm/).
- **Approximation algorithms.** Many algorithms guess the optimum up to a factor of 2 by trying $t = 1, 2, 4, \ldots$ and run a test that either succeeds with cost at most $c \cdot t$ or proves $\mathrm{OPT} > t$. The test is then only approximately a decision procedure, but the same search works.

## References
