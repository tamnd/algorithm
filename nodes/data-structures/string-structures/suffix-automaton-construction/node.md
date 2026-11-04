---
tag: 4BJQ6A
kind: problem
slug: suffix-automaton-construction
name: Suffix automaton construction
area: data-structures/string-structures
level: advanced
summary: Build the suffix automaton of a string in linear time.
prereqs: [suffix-automaton, deterministic-finite-automaton]
see_also: [blumer-algorithm, suffix-automaton, suffix-tree, suffix-trie, dfa-minimization, distinct-substrings-counting, weiner-algorithm, myhill-nerode-theorem]
sources:
  - paper: Anselm Blumer, Janet Blumer, David Haussler, Andrzej Ehrenfeucht, Mu-Tian Chen and Joel Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985, doi:10.1016/0304-3975(85)90157-4
    locator: pages 31 to 55, the end-set classes, the bounds of 2n − 1 states and 3n − 4 edges, and the online linear construction
  - paper: Maxime Crochemore, Transducers and repetitions, Theoretical Computer Science 45(1), 1986, doi:10.1016/0304-3975(86)90041-1
    locator: pages 63 to 86, the suffix automaton as a minimal automaton, its construction, and its use for repetitions
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings
    locator: Chapter 5, suffix and factor automata, their sizes and constructions
---

Suffix automaton construction asks for the minimal deterministic automaton that accepts the suffixes of a text $t$ of length $n$, together with the suffix links and the lengths that make it useful as an index. The automaton has at most $2n - 1$ states and $3n - 4$ transitions, so it can be built in time linear in $n$ for a fixed alphabet, and the online algorithm of [Blumer et al.](/blumer-algorithm/) does so. This page states the problem, its variants and its bounds; the structure and its queries are on the page of the [suffix automaton](/suffix-automaton/).

## In plain words

Take all the endings of a word and build a machine that reads letters and says yes exactly when the letters read form one of those endings. Among all such machines, take the one with the fewest states. Reading any piece of the word from the start state never gets stuck, so the same machine also tells whether a string occurs in the word.

The [suffix trie](/suffix-trie/) is such a machine, but it can have about $n^2/2$ states. The smallest machine merges the states that behave the same way from then on, and it always has fewer than $2n$ states. The problem is to build this small machine directly, without building the big one first.

## Definition

**Input.** A text $t = t_1 \cdots t_n$ over an alphabet $\Sigma$.

**Output.** The minimal deterministic automaton $\mathcal{A}(t)$ with language $\{t_{i} \cdots t_n : 1 \le i \le n + 1\}$, the suffixes of $t$ including the empty one, given as:

- its states, one for each class of substrings with the same set $endpos(w)$ of end positions, plus the initial state;
- its transitions $\delta(v, a)$;
- its accepting states, the classes of the suffixes of $t$;
- for each state $v$, the length $len(v)$ of its longest string and the suffix link $link(v)$, the state of the longest suffix of that string in another class.

The last item is not part of the automaton itself, but every known construction computes it and most applications need it. By the [Myhill-Nerode theorem](/myhill-nerode-theorem/), two strings lead to the same state of the minimal automaton exactly when they have the same set of right extensions into suffixes, and for substrings of $t$ this is the same as having the same end set.

## Variants

- **Online construction.** The symbols arrive one at a time, and after each one the automaton of the prefix read so far must be available. The Blumer et al. algorithm is online.
- **Factor automaton.** The minimal automaton of the substrings (the factors) of $t$, with all states accepting. It has at most as many states as the suffix automaton, and sometimes fewer, since two substrings are equivalent as soon as their first occurrences end at the same place.
- **Compact DAWG.** The automaton with chains of states that have one transition merged into edges labeled by strings, the analog of the suffix tree for the suffix automaton.
- **Several texts.** The automaton of the suffixes of every text of a set, also called the generalized suffix automaton, used to compare documents.
- **Integer alphabets.** The symbols are integers in $\{1, \ldots, n^{O(1)}\}$, and the goal is linear time independent of the alphabet size, as for suffix arrays and suffix trees.

## Examples

For banana, the automaton has 10 states and 11 transitions, while the suffix trie has 16 nodes, one per distinct substring plus the root:

| state | strings | end set | len | link |
|---|---|---|---|---|
| 0 | ε | all | 0 | none |
| 1 | b | {1} | 1 | 0 |
| 2 | ba | {2} | 2 | 5 |
| 3 | ban | {3} | 3 | 7 |
| 4 | bana | {4} | 4 | 9 |
| 5 | a | {2, 4, 6} | 1 | 0 |
| 6 | nan, anan, banan | {5} | 5 | 7 |
| 7 | n, an | {3, 5} | 2 | 0 |
| 8 | nana, anana, banana | {6} | 6 | 9 |
| 9 | na, ana | {4, 6} | 3 | 5 |

The transitions are $0 \to_b 1$, $0 \to_a 5$, $0 \to_n 7$, $1 \to_a 2$, $2 \to_n 3$, $3 \to_a 4$, $4 \to_n 6$, $5 \to_n 7$, $6 \to_a 8$, $7 \to_a 9$ and $9 \to_n 6$. The accepting states are 8, 9, 5 and 0, the link path from the state of the whole text: they hold the suffixes banana, anana, nana; ana, na; a; and ε. The factor automaton of banana has 7 states.

For $t = ab^{n-1}$ the automaton has $2n - 1$ states, and for $t = ab^{n-2}c$ it has $3n - 4$ transitions, so the bounds below are tight.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| suffix trie, then [DFA minimization](/dfa-minimization/) | $\Theta(n^2)$ for the trie in the worst case | simple, but the trie can be quadratic |
| [Blumer et al.](/blumer-algorithm/) (1985) | $O(n \log \sigma)$, or $O(n)$ for a fixed alphabet | online, left to right, with state cloning |
| Crochemore (1986) | $O(n \log \sigma)$ | the same automaton seen as the minimal automaton of the suffixes, with an online construction |
| from the suffix tree of the reversed text | linear after the suffix tree | the suffix link tree of the automaton is the suffix tree of the reversed text with a node for each suffix, so its nodes are the states; the transitions are then added |

Here $\sigma$ is the number of distinct symbols. The $\log \sigma$ factor is the cost of a transition lookup in a balanced search tree; with arrays indexed by symbols the time is $O(n)$ and the space $O(n \sigma)$, and with hashing the time is $O(n)$ expected. For integer alphabets, linear-time constructions go through the suffix tree of the reversed text, which can be built in linear time with [Farach's algorithm](/farach-algorithm/).

## Bounds

- **Size.** For $n \ge 2$ the automaton has at most $2n - 1$ states, and for $n \ge 3$ at most $3n - 4$ transitions (Blumer et al.). So the output has size $\Theta(n)$ and every construction takes $\Omega(n)$ time.
- **Comparison lower bound.** If symbols can only be compared, the construction takes $\Omega(n \log n)$ comparisons for unbounded alphabets: the initial state has $n$ transitions exactly when the $n$ symbols are distinct, and element distinctness needs $\Omega(n \log n)$ comparisons.
- **Per symbol.** The online algorithm can spend $\Theta(n)$ time on one symbol, so the linear bound is amortized; the bound on a single step is not constant.

## Reductions

- **Suffix tree of the reversed text.** The states and suffix links of $\mathcal{A}(t)$ form the suffix tree of the reversed text, with an explicit node for every suffix of it: a state is a node, and its strings are read backward along the edge to it. So building one gives the other in linear time for a fixed alphabet, and building the automaton is no harder than building a [suffix tree](/suffix-tree/) of the reversed text plus adding the transitions. Appending a symbol to $t$ prepends it to the reversed text, which is the step of [Weiner's algorithm](/weiner-algorithm/).
- **Minimization.** $\mathcal{A}(t)$ is the minimized suffix trie. The trie can be quadratic, so this reduction is only practical for short texts, but it gives a simple correctness check.

## Applications

- **Substring tests.** A string $w$ is a substring of $t$ if and only if the transitions on its symbols exist from the initial state, in $O(\lvert w \rvert)$ steps.
- **Counting distinct substrings.** The number of distinct nonempty substrings is $\sum_{v \ne 0} (len(v) - len(link(v)))$; see [distinct substrings counting](/distinct-substrings-counting/). For banana it is 15.
- **Longest common substring.** Running a second string through the automaton of the first, following links on failure, finds the [longest common substring](/longest-common-substring/) in linear time.
- **Occurrence counts.** The size of the end set of each state, summed up the link tree, gives the number of occurrences of each substring.
- **Pattern matching and repetitions.** Crochemore used the automaton for string matching and for finding repetitions in texts.

## References
