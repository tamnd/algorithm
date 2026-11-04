---
tag: 3GZVCW
kind: definition
slug: sublinear-time
name: Sublinear time
aliases:
- o(n) time
area: foundations/asymptotic-analysis
level: intro
summary: Running time that is asymptotically smaller than n, so the algorithm cannot read the whole input.
prereqs: [asymptotic-notation, time-complexity, input-size]
see_also: [logarithmic-time, polylogarithmic-time, constant-time, linear-time, binary-search, query-complexity, hoeffding-inequality, adversary-argument]
sources:
  - paper: "Ronitt Rubinfeld and Asaf Shapira, Sublinear time algorithms, SIAM Journal on Discrete Mathematics 25(4) (2011)"
    locator: the survey
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 2.4
  - book: "Oded Goldreich, Introduction to Property Testing, Cambridge University Press (2017)"
    locator: Chapter 1
  - paper: "Bernard Chazelle, Ronitt Rubinfeld and Luca Trevisan, Approximating the minimum spanning tree weight in sublinear time, SIAM Journal on Computing 34(6) (2005)"
    locator: the main theorem
  - book: isbn:9781107154889
    title: Mitzenmacher and Upfal, Probability and Computing, second edition
    locator: Chapter 4 (Hoeffding bound)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3 (the exercise on binary search) and Appendix C (probability)
---

An algorithm runs in sublinear time when its worst-case [time](/time-complexity/) is $o(n)$ for an input of size $n$, so for each constant $c > 0$ it uses fewer than $cn$ steps when $n$ is large. Such an algorithm cannot read the whole input. It needs random access to the input. For many problems it is exact only when the input has a promise (for example, that an array is sorted), or else it uses randomization and gives an approximate answer, or else the input is a data structure built in advance and the sublinear bound is the time of one query. The class contains [constant time](/constant-time/), [logarithmic time](/logarithmic-time/) and [polylogarithmic time](/polylogarithmic-time/), and also the times $\sqrt{n}$ and $n / \log n$.

## Definition

**Model.** The input is a string $x = x_1 x_2 \dots x_n$ of $n$ symbols that is stored in a read-only array. The machine is a [random-access machine](/random-access-machine/) that knows $n$, and a *query* reads $x_i$ for an index $i$ that the machine chooses. A query costs one step, and each other basic operation costs one step. A model that reads the input on a tape from left to right is not suitable: a head that moves one cell in each step sees only the first $t$ cells in $t$ steps, so an algorithm of that kind is blind to most of the input.

**Definition.** Let $T(n)$ be the worst-case number of steps of an algorithm on inputs of size $n$. The algorithm runs in *sublinear time* when $T(n) = o(n)$:

$$\forall c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ T(n) < c\,n.$$

For a randomized algorithm, $T(n)$ is the maximum over the inputs of size $n$ and over the random choices. A bound on the expected time uses the expectation in place of the maximum over the random choices; such a bound is always labelled as expected. The definition says nothing about the correctness of the output: the algorithm may be exact, or it may be allowed an error, as in the examples below.

**Query bound.** Every query costs a step, so $T(n)$ is at least the number of queries. A sublinear algorithm makes $o(n)$ queries on every input, and a lower bound on the number of queries is a lower bound on the time.

## Examples and non-examples

### Exact algorithms with a promise

- **Binary search** in a sorted array of $n$ keys makes at most $\lfloor \lg n \rfloor + 1$ comparisons, for $n \ge 1$. For $n = 10^6$ this is 20. The promise is that the array is sorted. The time is $O(\log n)$, so it is sublinear. A comparison-based search needs $\lceil \lg(n+1) \rceil$ comparisons in the worst case, because the decision tree is in effect binary (an outcome "equal" ends the search) and it needs $n + 1$ leaves, one for each gap where an absent key can fall. This number is equal to $\lfloor \lg n \rfloor + 1$. See [binary search](/binary-search/) and [logarithmic time](/logarithmic-time/). The same search on a linked list needs $\Theta(n)$ steps, because a list has no random access.
- **A hash table** or a balanced search tree answers a query in $O(1)$ expected or $O(\log n)$ time, once the structure exists. The building of the structure reads the whole input. The sublinear time is the time of one query, after the preprocessing.
- **A single element.** Reading the first item of an array, or checking if the array is empty, takes $\Theta(1)$ time.

### Randomization and approximation

- **Estimate a fraction.** Let $x \in \{0,1\}^n$ have $p n$ ones, for an unknown $p$. Pick $m$ indices uniformly and independently, with replacement, and let $\hat p$ be the fraction of ones among the $x_i$ read. By the [Hoeffding inequality](/hoeffding-inequality/), $\Pr[\,|\hat p - p| \ge \varepsilon\,] \le 2 e^{-2 m \varepsilon^2}$. So for $m \ge \ln(2/\delta) / (2\varepsilon^2)$ samples, the error is less than $\varepsilon$ with probability at least $1 - \delta$. For $\varepsilon = 0.05$ and $\delta = 0.01$ this is $m = 1060$, for each $n$. The time is $O(\log(1/\delta)/\varepsilon^2)$, which does not depend on $n$, so it is $O(1)$ for fixed $\varepsilon$ and $\delta$. The answer is approximate and may be wrong with probability $\delta$.
- **Test for the all-zero array (property testing).** A tester has to accept the array $0^n$ and to reject each array that is $\varepsilon$-far from it, which means that at least $\varepsilon n$ entries are 1. Between these two cases it may answer in any way. Query $m$ uniform indices, and reject if one of the entries is 1. This never rejects $0^n$. If the array is $\varepsilon$-far, the probability that all $m$ queries see a 0 is at most $(1 - \varepsilon)^m \le e^{-\varepsilon m}$, which is at most $\delta$ for $m \ge \ln(1/\delta)/\varepsilon$. For $\varepsilon = 0.01$ and $\delta = 0.01$ this is $m = 461$ queries, for each $n$. The task is a relaxation of the OR function, and the next subsection shows that the exact OR needs $n$ queries. *Property testing* is the study of such tasks, for properties of strings, graphs and functions.
- **A graph estimate.** The weight of a [minimum spanning tree](/minimum-spanning-tree/) of a connected graph can be approximated, for small integer edge weights and a graph of bounded average degree, in time that does not depend on the number of vertices (Chazelle, Rubinfeld and Trevisan, 2005).

### Non-examples

- [Linear search](/linear-search/) takes $\Theta(n)$ steps in the worst case.
- A loop that adds the $n$ entries of an array reads each of them, so it takes $\Theta(n)$ steps.
- An algorithm with time $n/2$ is not sublinear. It is $\Theta(n)$, and for $c = 1/2$ the bound $T(n) < cn$ fails.
- The trial division of an integer $N$ takes about $\sqrt{N}$ steps. This is sublinear in the *value* $N$, but the input size is the number of bits $b \approx \lg N$, and $\sqrt N \approx 2^{b/2}$ is exponential in $b$. Sublinear time is a property of the time as a function of the input size. See [input size](/input-size/).

### Why an exact deterministic algorithm often needs the whole input

*Claim 1.* Let $\mathrm{OR}(x) = 1$ if some $x_i = 1$, else 0. A deterministic algorithm that computes $\mathrm{OR}$ exactly on each $x \in \{0,1\}^n$ makes at least $n$ queries on some input. So its worst-case time is at least $n$, and it is not sublinear.

*Proof.* Suppose that it makes fewer than $n$ queries on each input. Run it on $x = 0^n$. It makes a set $S$ of queries, with $|S| < n$, so there is an index $i \notin S$. Let $y$ be $x$ with the bit $i$ set to 1. The strings $x$ and $y$ differ only at the index $i$. We show by induction on the step number that the runs on $x$ and on $y$ are in the same state after each step. The runs start in the same state. In a step that is not a query, the next state depends on the state only. In a query step, both runs query the same index $j$, because the state is the same and the algorithm is deterministic. This index is in $S$, so $j \ne i$, and the answers $x_j$ and $y_j$ are equal. So the states stay equal, the runs stop at the same step, and the outputs are equal. But $\mathrm{OR}(x) = 0$ and $\mathrm{OR}(y) = 1$, so it is wrong on one of them. $\square$

The same proof works for each function that has an input $x$ such that a change of any single entry of $x$ changes the answer. Two more cases are the AND function, with the input $1^n$, and the check of sortedness for $n \ge 2$ on the input $1, 2, \dots, n$, where the entry $i$ that is not read can be changed to $n + 1$ (if $i < n$) or to $0$ (if $i = n$), and this makes the array unsorted. This is the technique of the [adversary argument](/adversary-argument/). It shows that the promise in the examples above (a sorted array) cannot be checked in sublinear time. The OR bound shows that a search without the promise needs $n$ queries, because the search for the key 1 in an array of 0 and 1 is the OR function.

*Claim 2.* Randomization with a small error does not remove the need. Let a randomized algorithm make at most $t$ queries on each input and each random string, and let it output $\mathrm{OR}(x)$ with probability at least $2/3$ on each $x$. Then $t \ge n/3$.

*Proof.* Let $x = 0^n$. Let $r$ be the random string, with probability space $R$. For each index $i$, let $q_i = \Pr_r[\text{the run on } (x, r) \text{ queries } i]$. Each run queries at most $t$ indices, so $\sum_i q_i \le t$ and there is an index $i$ with $q_i \le t/n$. Let $y$ be $x$ with the bit $i$ set to 1. If the run on $(x, r)$ does not query $i$, the run on $(y, r)$ is identical (the same argument as for Claim 1, for the fixed $r$), so it has the same output. The algorithm outputs 0 on $(x, r)$ with probability at least $2/3$, so it outputs 0 on $(y, r)$ with probability at least $2/3 - t/n$. On $y$ the algorithm must output 1 with probability at least $2/3$, so it outputs 0 with probability at most $1/3$. Hence $2/3 - t/n \le 1/3$, which gives $t \ge n/3$. $\square$

The all-zero tester above does not contradict this. It does not decide the OR: it decides a *promise problem*, in which the inputs that have at least 1 and fewer than $\varepsilon n$ ones are excluded. The query bound of randomized algorithms is the subject of [randomized query complexity](/randomized-query-complexity/).

## Related definitions

- [Constant time](/constant-time/), [logarithmic time](/logarithmic-time/) and [polylogarithmic time](/polylogarithmic-time/) are sublinear. Each time $O(n^{1-\varepsilon})$ for a constant $\varepsilon > 0$ is sublinear. Time $n/\log n$ is sublinear and is not of this form.
- [Linear time](/linear-time/) is the next class, $O(n)$. An algorithm that reads all of the input takes $\Omega(n)$ time, so linear time is the smallest bound that allows it.
- [Query complexity](/query-complexity/) counts the queries to the input in place of the steps, and it is the usual tool for lower bounds in this area.
- The word *sublinear* is also used for space, as in the space of streaming algorithms. This page is about time.

## References
