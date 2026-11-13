---
tag: ZFP8QP
kind: problem
slug: twenty-questions-problem
name: Twenty questions problem
aliases:
- Twenty questions game
area: games-and-search/puzzles
level: intro
summary: Find a hidden object among n with yes-or-no questions. ceil(log2 n) in the worst case; Huffman coding for the least expected number; Ulam's version allows lies.
prereqs: [binary-search, information-theoretic-bound]
see_also: [huffman-coding, shannon-entropy, optimal-binary-search-tree, hu-tucker-algorithm, search-decision-tree, kraft-inequality, counterfeit-coin-problem, mastermind-problem]
sources:
  - paper: doi:10.1109/JRPROC.1952.273898
    title: David A. Huffman, A method for the construction of minimum-redundancy codes, Proceedings of the IRE 40(9), 1952, 1098 to 1101
    locator: the whole paper (the merging construction of an optimal prefix code)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 5, Data Compression (the Kraft inequality, the entropy bounds on the expected code length, Huffman codes and their optimality)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, 2nd edition, Addison-Wesley, 1998
    locator: Section 6.2.2 (optimal binary search trees, and the Hu-Tucker algorithm for the alphabetic case)
  - paper: doi:10.1016/S0304-3975(01)00303-6
    title: Andrzej Pelc, Searching games with errors, fifty years of coping with liars, Theoretical Computer Science 270(1-2), 2002, 71 to 109
    locator: the whole survey (Rényi and Ulam games, the volume bound, the solutions for a fixed number of lies, and the other error models)
  - paper: "Andrzej Pelc, Solution of Ulam's problem on searching with a lie, Journal of Combinatorial Theory, Series A 44, 1987, 129 to 140"
    locator: the main theorem (the least number of questions for every n with one lie)
  - paper: "Alfréd Rényi, On a problem of information theory, MTA Mat. Kut. Int. Közl. 6B, 1961, 505 to 516"
    locator: the whole paper (search with answers that may be wrong)
  - book: "Stanislaw M. Ulam, Adventures of a Mathematician, Charles Scribner's Sons, 1976"
    locator: the passage that poses the game of twenty questions with lies (one or two lies, one million objects)
---

The twenty questions problem asks for a strategy that finds a hidden object among $n$ known objects with yes-or-no questions. If any question about the set of objects is allowed, $\lceil \log_2 n \rceil$ questions are necessary and enough in the worst case, by the [information-theoretic bound](/information-theoretic-bound/) and [binary search](/binary-search/), so 20 questions cover $2^{20} = 1\,048\,576$ objects. When the objects have known probabilities, [Huffman coding](/huffman-coding/) gives the least expected number of questions, which lies between the [Shannon entropy](/shannon-entropy/) $H$ and $H + 1$. In the version of Rényi (1961) and Ulam (1976) some answers may be lies, and with one lie a million objects need 25 questions (Pelc 1987).

## In plain words

One player thinks of something from a known list. The other player asks questions that have a yes or no answer, and wants to find the thing with as few questions as possible.

The best plan cuts the list of possible answers in half with each question. Then each question doubles the size of the list you can handle, and twenty questions are enough for about a million things.

If some things are much more likely than others, ask about the likely ones early, so that on average you need fewer questions. The best plan of this kind is the same as the best way to write the things as short codes of zeros and ones.

The game gets harder when the other player may lie a few times. Then you must ask extra questions to catch the lies.

## Definition

Let $X = \{1, \ldots, n\}$ be the objects and $x \in X$ the hidden one. A *question* is a subset $S \subseteq X$, with answer "yes" when $x \in S$. An *adaptive strategy* is a binary [decision tree](/search-decision-tree/) whose inner nodes hold questions and whose leaves name objects; it *solves* the game when every $x$ reaches a leaf that names $x$.

- **Worst case.** Minimize the depth of the tree.
- **Average case.** Given probabilities $p_1, \ldots, p_n$, minimize $\sum_i p_i d_i$, where $d_i$ is the depth of the leaf of object $i$.
- **Restricted questions.** Only questions of the form "is $x < t$?" for a fixed order of $X$ (comparison questions), or other families of sets.
- **Lies.** The answerer may give at most $e$ false answers, chosen adversarially (Ulam's game), or each answer is false with probability $\varepsilon$ independently (noisy search).

The answers along a path form a word of 0s and 1s, and the leaves of a tree form a [prefix code](/prefix-code/). So the average case asks for an optimal prefix code.

## Variants

- **Comparison questions.** The tree must also be an ordered tree, an *alphabetic tree*: the objects at its leaves read left to right in the given order. The optimal one is found by the dynamic program for [optimal binary search trees](/optimal-binary-search-tree/) in $O(n^3)$ time, or $O(n^2)$ with Knuth's speed-up, and by the [Hu-Tucker algorithm](/hu-tucker-algorithm/) or the [Garsia-Wachs algorithm](/garsia-wachs-algorithm/) in $O(n \log n)$.
- **Fixed questions in advance.** A non-adaptive strategy asks all questions at once; $\lceil \log_2 n \rceil$ questions still suffice without lies, by the binary digits of $x$.
- **A fixed number of lies.** Rényi and Ulam. The exact answer is known for $e = 1$ for all $n$ (Pelc 1987), and for $e = 2$ and $e = 3$ by later work surveyed in Pelc (2002).
- **Random errors.** Each answer is wrong with probability $\varepsilon < 1/2$. The number of questions needed then grows like $\log_2 n / C(\varepsilon)$, where $C$ is the capacity of the binary symmetric channel; see Pelc (2002).
- **Other answers.** A three-way answer, as in the [counterfeit coin problem](/counterfeit-coin-problem/), or a numeric score, as in the [Mastermind problem](/mastermind-problem/).

## Examples

**Worst case.** With $n = 1000$ objects, $\lceil \log_2 1000 \rceil = 10$ questions, since $2^9 = 512 < 1000 \le 1024 = 2^{10}$. With $n = 10^6$, 20 questions; with $n = 2^{20} + 1$, 21.

**Average case.** Let the probabilities be $\frac{1}{16}, \frac{1}{16}, \frac{2}{16}, \frac{4}{16}, \frac{8}{16}$. Huffman's method merges the two smallest weights again and again: $1 + 1 = 2$, $2 + 2 = 4$, $4 + 4 = 8$, $8 + 8 = 16$. The depths are $4, 4, 3, 2, 1$, and the expected number of questions is $(4 + 4 + 6 + 8 + 8)/16 = 30/16 = 1.875$. All probabilities are powers of $\frac{1}{2}$, so this equals the entropy exactly. Ask first "is it the most likely object?", and so on down.

**Comparison questions cost more.** If the same objects are in the order with probabilities $\frac{8}{16}, \frac{1}{16}, \frac{4}{16}, \frac{1}{16}, \frac{2}{16}$ and only questions "is it before position $t$?" are allowed, the best expected number is $32/16 = 2$, not $1.875$, since the likely objects are not next to each other.

**The lower bound for lies.** With at most one lie and $q$ questions, a solving strategy needs $n(q + 1) \le 2^q$. *Proof.* Fix a strategy and an object $x$. The answerer can answer all questions truthfully, or lie exactly at question $i$ for any $i = 1, \ldots, q$; these $q + 1$ answer words are all different, and all must end at leaves that name $x$. Leaves that name different objects are different, and the tree has at most $2^q$ leaves, so $n(q + 1) \le 2^q$. $\square$ Pelc (1987) showed that for even $n$ the least $q$ with $n(q + 1) \le 2^q$ is enough, and for odd $n$ the least $q$ with $n(q + 1) + (q - 1) \le 2^q$. For $n = 10^6$ this gives $q = 25$: $10^6 \cdot 26 \le 2^{25} = 33\,554\,432$ but $10^6 \cdot 25 > 2^{24}$. The first values, for $n = 1$ to 10, are $0, 3, 5, 5, 6, 6, 6, 6, 7, 7$.

## Known algorithms

- **Halving.** Keep the set of candidates and ask about any half of it: $\lceil \log_2 n \rceil$ questions, which is [binary search](/binary-search/) when the questions are comparisons.
- **Huffman coding.** Build the tree by merging the two least likely groups, in $O(n \log n)$ time with a heap; the tree is optimal for the expected number of questions (Huffman 1952). See [Huffman coding](/huffman-coding/) and [optimal prefix code](/optimal-prefix-code/).
- **Optimal alphabetic trees.** For comparison questions, the [optimal binary search tree](/optimal-binary-search-tree/) dynamic program with only leaf weights, or the Hu-Tucker and Garsia-Wachs algorithms.
- **Ulam's game.** With one lie, the state is a pair $(a, b)$: $a$ objects agree with every answer so far and $b$ objects agree with all answers but one. A question takes $a_1$ of the first kind and $b_1$ of the second; "yes" leads to $(a_1, a - a_1 + b_1)$ and "no" to $(a - a_1, a_1 + b - b_1)$. Good strategies keep the *volume* $a(q + 1) + b$ of the two answers nearly equal, and Pelc's strategies reach his bound. A search over these pairs finds the least number of questions for small $n$, and it agrees with Pelc's formula for every $n$ below 120.
- **Noisy search.** Repeat each comparison and take the majority, or use a Bayesian update of the probabilities of all objects and ask at the median; see Pelc (2002).

## Bounds

- **Worst case.** Exactly $\lceil \log_2 n \rceil$: each question at most halves the set of candidates in the worst case, and halving reaches this.
- **Average case.** $H \le L^* < H + 1$, where $L^*$ is the least expected number of questions and $H = -\sum_i p_i \log_2 p_i$ (Cover and Thomas, Chapter 5). The lower bound follows from the [Kraft inequality](/kraft-inequality/) for the depths of the leaves.
- **Comparison questions.** The optimal alphabetic tree costs less than $H + 2$, and at least the Huffman cost.
- **One lie.** Pelc's formula above, about $\log_2 n + \log_2 \log_2 n + O(1)$.

## Reductions

- **To prefix codes.** A question strategy is a binary prefix code for the objects and back; the expected number of questions is the expected code length. So the problem with arbitrary questions is source coding, and the problem with comparison questions is alphabetic coding.
- **From lies to error-correcting codes.** A non-adaptive strategy with $e$ lies is a binary code of length $q$ with $n$ words that corrects $e$ errors, and the volume bound is the Hamming bound for codes.

## Applications

- **Data compression.** Prefix codes, Huffman codes and arithmetic coding are strategies for this game in which the questions are the bits of the code.
- **Search and diagnosis.** Fault diagnosis, decision tables and expert systems ask the most informative test first, which is the greedy form of the same idea.
- **Searching with unreliable tests.** Ulam's game models search with faulty comparisons, and communication over a noisy channel in which the sender sees what the receiver got.

## References
