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
  - paper: doi:10.1137/100791075
    title: Ronitt Rubinfeld and Asaf Shapira, Sublinear time algorithms, SIAM Journal on Discrete Mathematics 25(4), 1562 to 1588 (2011)
    locator: Section 1 (the model and the basic examples)
  - book: isbn:9781107194052
    title: Oded Goldreich, Introduction to Property Testing, Cambridge University Press (2017)
    locator: Chapter 1, The Main Themes
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.4, A Survey of Common Running Times (sublinear time)
  - paper: doi:10.1137/S0097539702403244
    title: Bernard Chazelle, Ronitt Rubinfeld and Luca Trevisan, Approximating the minimum spanning tree weight in sublinear time, SIAM Journal on Computing 34(6), 1370 to 1379 (2005)
    locator: the main theorem
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Chernoff and Hoeffding Bounds
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1, Searching an Ordered Table
---

An algorithm runs in sublinear time when its worst-case [time](/time-complexity/) is $o(n)$ for an [input size](/input-size/) $n$: for each constant $c > 0$ it uses fewer than $cn$ steps once $n$ is large. Such an algorithm cannot read the whole input, so it needs random access to the input, and it is exact only in special settings: the input carries a promise (for example, that an array is sorted), the input is a data structure built in advance, or the algorithm is randomized and the answer is approximate. The class contains [constant time](/constant-time/), [logarithmic time](/logarithmic-time/) and [polylogarithmic time](/polylogarithmic-time/), and also the times $\sqrt{n}$ and $n / \log n$.

## Definition

**Model.** The input is a string $x = x_1 x_2 \cdots x_n$ of $n$ symbols that is stored in a read-only array. The machine is a [random-access machine](/random-access-machine/) that knows $n$. A *query* reads $x_i$ for an index $i$ that the machine chooses, and costs one step, as does each other basic operation. A machine that reads its input on a tape from left to right is not suitable: in $t$ steps its head sees only the first $t + 1$ cells, so in $o(n)$ steps it never sees most of the input.

**Definition.** Let $T(n)$ be the worst-case number of steps of an algorithm on inputs of size $n$. The algorithm runs in *sublinear time* when $T(n) = o(n)$:

$$\forall c > 0 \ \exists n_0 \ \forall n \ge n_0 : \ T(n) < c\,n.$$

For a randomized algorithm, $T(n)$ is the maximum over the inputs of size $n$ and over the random choices. A bound on the expected time takes the expectation over the random choices in place of the maximum, and it must be labelled as expected. The definition says nothing about the correctness of the output: the algorithm may be exact, or it may be allowed an error, as in the examples below.

**Query bound.** Each query costs a step, so $T(n)$ is at least the number of queries. A sublinear algorithm makes $o(n)$ queries on every input, and a lower bound on the number of queries is a lower bound on the time. See [query complexity](/query-complexity/).

**The size is the size of the input as stored.** Whether a time is sublinear depends on what $n$ measures. A graph with $V$ vertices given by its adjacency matrix has an input of $V^2$ bits, so a time of $O(V)$ is sublinear in the input size. The same time is not sublinear for a graph given by adjacency lists of total size $\Theta(V + E)$ when $E = O(V)$. A time of $O(\sqrt N)$ on an integer $N$ is not sublinear in the input size $\lg N$ at all: it is exponential in it.

## Examples and non-examples

### Exact algorithms with a promise or a structure

- **Binary search.** In a sorted array of $n$ keys, binary search makes at most $\lfloor \lg n \rfloor + 1$ three-way comparisons, for $n \ge 1$, which is 20 for $n = 10^6$. The promise is that the array is sorted. A comparison-based search needs $\lceil \lg(n+1) \rceil = \lfloor \lg n \rfloor + 1$ comparisons in the worst case, because its decision tree is in effect binary (an outcome "equal" ends the search) and needs a leaf for each of the $n + 1$ gaps where an absent key can fall (Knuth, Section 6.2.1). See [binary search](/binary-search/).
- **A universal sink in an adjacency matrix.** A *universal sink* of a directed graph with $V$ vertices is a vertex with in-degree $V - 1$ and out-degree 0. Given the $V \times V$ adjacency matrix $M$, keep a candidate $c = 0$ and, for $j = 1, \ldots, V - 1$, set $c \leftarrow j$ when $M[c][j] = 1$. If $M[c][j] = 1$, then $c$ has an out-edge and is not a sink. If $M[c][j] = 0$, then $j$ lacks the in-edge from $c$ and is not a sink. So after the loop, every vertex other than $c$ is ruled out, and $2(V - 1)$ more queries check $c$. The total is at most $3(V - 1)$ queries: 2997 for $V = 1000$, against $10^6$ entries in the matrix. In the input size $n = V^2$ this is $O(\sqrt n)$ time.
- **Queries to a structure.** A hash table or a balanced search tree answers a query in expected $O(1)$ or worst-case $O(\log n)$ time once it exists. Building it reads the whole input. The sublinear time is the time of one query, after the preprocessing.

### Randomization and approximation

- **Estimate a fraction.** Let $x \in \{0,1\}^n$ have $pn$ ones, for an unknown $p$. Pick $m$ indices uniformly and independently, with replacement, and let $\hat p$ be the fraction of ones among the entries read. By the [Hoeffding inequality](/hoeffding-inequality/), $\Pr[\,|\hat p - p| \ge \varepsilon\,] \le 2 e^{-2 m \varepsilon^2}$. So for $m \ge \ln(2/\delta) / (2\varepsilon^2)$ the error is less than $\varepsilon$ with probability at least $1 - \delta$. For $\varepsilon = 0.05$ and $\delta = 0.01$ this is $m = 1060$, for each $n$. The time is $O(\log(1/\delta)/\varepsilon^2)$, which does not depend on $n$.
- **Test for the all-zero array.** A *tester* must accept the array $0^n$ and reject each array that is $\varepsilon$-far from it, which here means that at least $\varepsilon n$ entries are 1. On other inputs any answer is allowed. Query $m$ uniform indices, and reject if one of the entries is 1. This never rejects $0^n$. If the array is $\varepsilon$-far, all $m$ queries see a 0 with probability at most $(1 - \varepsilon)^m \le e^{-\varepsilon m}$, which is at most $\delta$ for $m \ge \ln(1/\delta)/\varepsilon$. For $\varepsilon = \delta = 0.01$ this is $m = 461$ queries, for each $n$. *Property testing* studies such tasks for properties of strings, graphs and functions (Goldreich, Chapter 1).
- **A graph estimate.** For a connected graph of average degree $d$ with integer edge weights from 1 to $w$, given by adjacency lists, the weight of a [minimum spanning tree](/minimum-spanning-tree/) can be approximated within a factor $1 + \varepsilon$ in time that depends on $d$, $w$ and $\varepsilon$ but not on the number of vertices (Chazelle, Rubinfeld and Trevisan, 2005).

### Non-examples

- [Linear search](/linear-search/) takes $\Theta(n)$ steps in the worst case.
- A loop that adds the $n$ entries of an array reads each of them, so it takes $\Theta(n)$ steps.
- An algorithm with time $n/2$ is not sublinear. It is $\Theta(n)$, and the bound $T(n) < cn$ fails for $c = 1/2$.
- Trial division of an integer $N$ takes about $\sqrt{N}$ divisions. This is sublinear in the *value* $N$, but the input size is the number of bits $\beta = \lfloor \lg N \rfloor + 1$, and $\sqrt N \ge 2^{(\beta - 1)/2}$ is exponential in $\beta$. This is the error behind [pseudo-polynomial time](/pseudo-polynomial-time/), in its most extreme form.

### Why an exact deterministic algorithm often needs the whole input

*Claim 1.* Let $\mathrm{OR}(x) = 1$ if some $x_i = 1$, else 0. A deterministic algorithm that computes $\mathrm{OR}$ exactly on each $x \in \{0,1\}^n$ makes at least $n$ queries on some input.

*Proof.* Suppose that it makes fewer than $n$ queries on each input. Run it on $x = 0^n$. It queries a set $S$ of indices with $|S| < n$, so there is an index $i \notin S$. Let $y$ be $x$ with the bit $i$ set to 1. We show by induction on the step number that the runs on $x$ and on $y$ are in the same state after each step. The runs start in the same state. In a step that is not a query, the next state depends only on the current state. In a query step, both runs query the same index $j$, because the state is the same and the algorithm is deterministic. This index is in $S$, so $j \ne i$, and $x_j = y_j$. So the states stay equal, the runs stop at the same step, and the outputs are equal. But $\mathrm{OR}(x) = 0$ and $\mathrm{OR}(y) = 1$, so the algorithm is wrong on one of them. $\square$

The same proof works for each function that has an input $x$ such that a change of any single entry of $x$ changes the answer. Two more cases are the AND function, with the input $1^n$, and the check of sortedness for $n \ge 2$ on the input $1, 2, \ldots, n$: an unread entry $i < n$ can be changed to $n + 1$, and an unread entry $i = n$ to 0, and either change makes the array unsorted. This is an [adversary argument](/adversary-argument/). It shows that the promise of binary search (a sorted array) cannot be checked in sublinear time, and that a search without the promise needs $n$ queries, because the search for the key 1 in an array of zeros and ones computes $\mathrm{OR}$.

*Claim 2.* Randomization with a small error does not remove the need. Let a randomized algorithm make at most $t$ queries on each input and each random string, and let it output $\mathrm{OR}(x)$ with probability at least $2/3$ on each $x$. Then $t \ge n/3$.

*Proof.* Let $x = 0^n$ and let $r$ be the random string. For each index $i$, let $q_i = \Pr_r[\text{the run on } (x, r) \text{ queries } i]$. Each run queries at most $t$ indices, so $\sum_i q_i \le t$, and some index $i$ has $q_i \le t/n$. Let $y$ be $x$ with the bit $i$ set to 1. For a fixed $r$ such that the run on $(x, r)$ does not query $i$, the run on $(y, r)$ is identical, by the argument of Claim 1, and has the same output. The algorithm outputs 0 on $x$ with probability at least $2/3$, so it outputs 0 on $y$ with probability at least $2/3 - t/n$. On $y$ it must output 1 with probability at least $2/3$, so it outputs 0 with probability at most $1/3$. Hence $2/3 - t/n \le 1/3$, which gives $t \ge n/3$. $\square$

The all-zero tester does not contradict Claim 2. It solves a *promise problem*: the inputs with at least one 1 and fewer than $\varepsilon n$ ones are excluded. See [randomized query complexity](/randomized-query-complexity/).

## Related definitions

- [Constant time](/constant-time/), [logarithmic time](/logarithmic-time/) and [polylogarithmic time](/polylogarithmic-time/) are sublinear. Each time $O(n^{1-\varepsilon})$ for a constant $\varepsilon > 0$ is sublinear. The time $n/\lg n$ is sublinear and is not of this form, since $(n/\lg n)/n^{1-\varepsilon} = n^{\varepsilon}/\lg n \to \infty$.
- [Linear time](/linear-time/), $O(n)$, is the next class. An algorithm that reads all of its input takes $\Omega(n)$ time, so linear time is the smallest bound that allows it.
- [Query complexity](/query-complexity/) counts the queries to the input in place of the steps, and it is the usual tool for lower bounds in this area.
- The word *sublinear* is also used for space, as in the space of streaming algorithms. This page is about time.

## References
