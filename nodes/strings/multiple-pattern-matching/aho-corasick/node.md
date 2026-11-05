---
tag: P3M1B3
kind: algorithm
slug: aho-corasick
name: Aho-Corasick algorithm
aliases:
- Aho-Corasick automaton matching
- Aho-Corasick string matching
area: strings/multiple-pattern-matching
level: core
summary: Builds a trie of the patterns with failure links and scans the text once, reporting all occurrences of all patterns in O(n + m + z) time.
solves: [multiple-string-matching, dictionary-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the total length of the patterns, z: the number of occurrences reported, σ: the alphabet size}
  time: {worst: O((n + m) log σ + z), expected: O(n + m + z)}
  space: {extra: O(m)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1975
  people: [Alfred V. Aho, Margaret J. Corasick]
  note: Published in Communications of the ACM in June 1975 as an aid to bibliographic search at Bell Laboratories.
prereqs: [trie, failure-link, knuth-morris-pratt, multiple-string-matching]
see_also: [dictionary-suffix-link, output-sensitive-matching, dictionary-matching, commentz-walter, wu-manber, karp-rabin-multiple-patterns, string-matching-automaton, two-dimensional-dictionary-matching]
sources:
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: Algorithm 1 (the pattern matching machine), Algorithms 2 and 3 (the goto and failure functions), Algorithm 4 (the deterministic automaton), and the example with he, she, his, hers
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4, Exact matching with a set of patterns (3.4.3 failure functions, 3.4.5 linear preprocessing, 3.4.6 output links)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (the prefix-based approach and the experimental map)
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 2, Pattern matching automata (the dictionary automaton and its implementation with failure links)
---

The Aho-Corasick algorithm solves [multiple string matching](/multiple-string-matching/): given a set of patterns of total length $m$ and a text of length $n$, it reports every occurrence of every pattern. It builds a [trie](/trie/) of the patterns, adds a [failure link](/failure-link/) and a [dictionary suffix link](/dictionary-suffix-link/) to each node, and then reads the text once from left to right. The time is $O(n + m + z)$ for $z$ occurrences when the trie moves cost $O(1)$, which is [output-sensitive](/output-sensitive-matching/) and optimal. It generalizes the failure function of [Knuth-Morris-Pratt](/knuth-morris-pratt/) from one pattern to a set, and it is the method of `fgrep`-style tools, virus scanners and intrusion detection systems.

## In plain words

Put all the words in one tree of letters, so that words that start the same share a branch. Each spot in the tree stands for the start of some word.

Read the text one letter at a time and walk down the tree. When the next letter has no branch, do not go back in the text. Jump to the spot for the longest end of what you have read that is still the start of some word, and try the letter again. Each spot keeps this jump target, worked out once before the search.

After each letter, the spot you are at may be a whole word, and some shorter ends of it may be whole words too. A second link from each spot leads straight to the next spot that is a whole word, so listing the matches costs only as much as the matches themselves.

## The problem

The input is a text $T = T[0 \ldots n-1]$ and a list of patterns $P_0, \ldots, P_{k-1}$ over an alphabet $\Sigma$, with total length $m = \sum_j |P_j|$. The output is the set of pairs $(s, j)$ such that $T[s \ldots s + |P_j| - 1] = P_j$. Indices are 0-based. Occurrences may overlap, one occurrence may lie inside another, and a pattern that appears twice in the list is reported once for each index. An empty pattern occurs at each $s$ from $0$ to $n$. This is the [multiple string matching](/multiple-string-matching/) problem, and the preprocessed form is [dictionary matching](/dictionary-matching/).

**Alphabet model.** The algorithm only tests characters for equality and uses them as keys of a map from a character to a child. The map is an array of size $\sigma$ for an integer alphabet, a balanced search tree for an ordered alphabet, or a hash table.

## The algorithm

Each node $v$ of the trie spells a string $\mathrm{str}(v)$, a prefix of some pattern; the root spells the empty string. $\mathrm{goto}(v, a)$ is the child of $v$ along the character $a$, if it exists. The algorithm stores three things for each node:

- $\mathrm{fail}[v]$: the node of the longest proper suffix of $\mathrm{str}(v)$ that is also a node;
- $\mathrm{dict}[v]$: the node of the longest proper suffix of $\mathrm{str}(v)$ that is a whole pattern, or nil;
- $\mathrm{out}[v]$: the indices $j$ with $P_j = \mathrm{str}(v)$, often empty.

```pseudo id=main
AHO-CORASICK(T, P_0, …, P_{k−1})
L1  for j ← 0 to k − 1 do                              ▷ build the trie
L2      walk down from the root along P_j, creating the missing children
L3      append j to out[v], where v is the last node of the walk
L4  for each child u of the root do fail[u] ← root, ENQUEUE(Q, u)
L5  while Q is not empty do                            ▷ breadth-first order
L6      v ← DEQUEUE(Q)
L7      if out[fail[v]] ≠ ∅ then dict[v] ← fail[v] else dict[v] ← dict[fail[v]]
L8      for each child u = goto(v, a) do
L9          f ← fail[v]
L10         while f ≠ root and goto(f, a) is undefined do
L11             f ← fail[f]
L12         if goto(f, a) is defined then fail[u] ← goto(f, a) else fail[u] ← root
L13         ENQUEUE(Q, u)
L14 v ← root, REPORT(v, 0)                             ▷ search
L15 for i ← 0 to n − 1 do
L16     while v ≠ root and goto(v, T[i]) is undefined do v ← fail[v]
L17     if goto(v, T[i]) is defined then v ← goto(v, T[i]) else v ← root
L18     REPORT(v, i + 1)

REPORT(v, e)                                           ▷ e is the end position
L19 if out[v] ≠ ∅ then w ← v else w ← dict[v]
L20 while w ≠ nil do
L21     for each j in out[w] do output (e − |P_j|, j)
L22     w ← dict[w]
```

The root has $\mathrm{dict}[\mathrm{root}] = \mathrm{nil}$, because the empty string has no proper suffix. Lines L1 to L3 build the trie in $O(m)$ map operations. Lines L4 to L13 set the links in breadth-first order, so a node is handled after all nodes of smaller depth. The failure link of a child $u = \mathrm{goto}(v, a)$ is found as in the [prefix function](/prefix-function/): try to extend the longest proper suffix of $\mathrm{str}(v)$ by $a$, then the next shorter one, and so on down to the root. Line L7 uses the fact that the patterns among the proper suffixes of $\mathrm{str}(v)$ are $\mathrm{str}(\mathrm{fail}[v])$, if it is a pattern, and the patterns among the proper suffixes of that string.

The search keeps $v$ at the node of the longest suffix of the text read so far that is a node of the trie. Line L16 falls back along failure links until the next character can extend the match, and line L17 takes the step. REPORT then lists all patterns that end at position $e$: they are exactly the patterns that are suffixes of $\mathrm{str}(v)$, and the dictionary links visit them from the longest to the shortest. Line L14 reports at $e = 0$, which matters only for an empty pattern.

## Example

The patterns of the original paper are $P_0$ = he, $P_1$ = she, $P_2$ = his, $P_3$ = hers. The trie has 10 nodes, named here by their strings.

| node | h | he | s | sh | she | hi | his | her | hers |
|---|---|---|---|---|---|---|---|---|---|
| fail | root | root | root | h | he | root | s | root | s |
| dict | nil | nil | nil | nil | he | nil | nil | nil | nil |
| out | | 0 | | | 1 | | 2 | | 3 |

For example, the proper suffixes of she are he, e and the empty string; he is the longest that is a node, so $\mathrm{fail}[\text{she}] = \text{he}$, and he is a pattern, so $\mathrm{dict}[\text{she}] = \text{he}$. The node his falls back to s, which is a node but not a pattern, so $\mathrm{dict}[\text{his}]$ is nil.

Search the text ushers ($n = 6$).

| $i$ | $T[i]$ | failure steps at L16 | $v$ after L17 | output at $e = i + 1$ |
|---|---|---|---|---|
| 0 | u | none | root | |
| 1 | s | none | s | |
| 2 | h | none | sh | |
| 3 | e | none | she | (1, 1) she, then (2, 0) he |
| 4 | r | she to he | her | |
| 5 | s | none | hers | (2, 3) hers |

At $i = 3$, REPORT starts at she, a pattern, and follows its dictionary link to he. At $i = 4$, she has no child r, so the search falls back to he, which has one. The text is read once, with one failure step in all, and the output is the three occurrences she at 1, he at 2 and hers at 2, the last two overlapping.

## Correctness

Let $N$ be the set of strings of the nodes, that is, the prefixes of the patterns. Three facts carry the proof. First, $\mathrm{fail}[u]$ is the node of the longest proper suffix of $\mathrm{str}(u)$ in $N$, and the chain $\mathrm{fail}[u], \mathrm{fail}[\mathrm{fail}[u]], \ldots, \mathrm{root}$ lists all proper suffixes of $\mathrm{str}(u)$ in $N$, longest first. Second, the chain from $\mathrm{dict}[v]$ lists all proper suffixes of $\mathrm{str}(v)$ that are patterns, longest first. Third, the search keeps this [loop invariant](/loop-invariant/): after line L17 for position $i$, $\mathrm{str}(v)$ is the longest suffix of $T[0 \ldots i]$ in $N$. An occurrence of $P_j$ that ends at $e$ makes $P_j$ a suffix of $T[0 \ldots e-1]$ that lies in $N$, so it is a suffix of $\mathrm{str}(v)$ and REPORT$(v, e)$ outputs it exactly once. The full proof is below.

## Complexity

Count the map operations $\mathrm{goto}(\cdot, \cdot)$ first; each one costs $O(1)$ with an array or with a hash table (expected), and $O(\log \sigma)$ with a balanced search tree.

- **Trie.** Lines L1 to L3 do one map operation for each pattern character, $m$ in all. The trie has at most $m + 1$ nodes.
- **Failure links, $O(m)$ steps.** Fix one pattern $P_j$ and the nodes $u_1, \ldots, u_\ell$ on its path, with $\ell = |P_j|$ and $u_t$ at depth $t$. When $u_{t+1}$ is handled, $f$ starts at $\mathrm{fail}[u_t]$, each pass of line L11 makes the depth of $f$ smaller by at least 1, and line L12 adds at most 1. So the passes for $u_{t+1}$ are at most $d_t + 1 - d_{t+1}$, where $d_t$ is the depth of $\mathrm{fail}[u_t]$. The sum over $t$ telescopes to at most $\ell$. Each node lies on the path of some pattern, so the total over all nodes is at most $\sum_j |P_j| = m$.
- **Search, at most $2n$ moves.** Use the depth of $v$ as a [potential](/potential-method/). Line L17 adds at most 1, $n$ times. Each failure step of line L16 lowers the depth by at least 1, and the depth never goes below 0. So there are at most $n$ failure steps and at most $2n$ map operations at lines L16 and L17.
- **Reporting, $O(n + z)$.** In REPORT, each node $w$ that the loop of line L20 visits has $\mathrm{out}[w] \ne \emptyset$, so each pass outputs at least one pair. The work is $O(1 + \text{the pairs output})$ for each of the $n + 1$ calls.

The total is $O(n + m + z)$ map operations. So the time is $O(n + m + z)$ with arrays (plus $O(m\sigma)$ to set up the arrays) or with hashing (expected), and $O((n + m)\log \sigma + z)$ in the worst case with balanced trees. The extra space is $O(m)$ for the trie and its links, plus $O(m\sigma)$ with arrays. Any algorithm must read the text and the patterns and write the output, so $\Omega(n + m + z)$ is a lower bound and the bound is optimal. The number $z$ can be as large as $(n + 1)k$: with the patterns a, aa, aaa and the text $a^n$, each pattern occurs at almost every position.

## Properties

- **Online.** The output for end position $e$ depends only on $T[0 \ldots e-1]$, and each text character is read once. The algorithm works on a stream.
- **One pass, no backtracking in the text.** The text pointer only moves forward. The delay for one character is not bounded by a constant, because line L16 can fall back many times, but it is at most the length of the longest pattern.
- **Output-sensitive.** The search time is $O(n + z)$ after preprocessing, whatever the number of patterns. See [output-sensitive matching](/output-sensitive-matching/).
- **Deterministic.** The algorithm makes no random choices. With hash maps for the children, only the time bound is an expectation, and it is taken over the hash function.

## Variants and improvements

- **The full automaton.** Replace the failure links by a transition $\delta(v, a)$ for every node and character: $\delta(v, a) = \mathrm{goto}(v, a)$ if it exists, else $\delta(\mathrm{fail}[v], a)$, and $\delta(\mathrm{root}, a) = \mathrm{root}$. This is Algorithm 4 of the original paper. Each text character then costs exactly one step, at the price of $\Theta(m\sigma)$ space. It is the [string-matching automaton](/string-matching-automaton/) of a set of patterns.
- **Output lists instead of dictionary links.** The original paper merges the output set of $\mathrm{fail}[v]$ into the output set of $v$. This is simpler, but for distinct patterns the stored sets can have total size $\Theta(m^{3/2})$: a node has at most $\sqrt{2m}$ pattern suffixes, because their lengths are distinct and sum to at most $m$, and the patterns $a, a^2, \ldots, a^L$ together with $L$ patterns $c_i a^L$ that start with distinct characters $c_i$ reach this order. The dictionary links keep the space at $O(m)$.
- **Compact representations.** Double-array tries and bit-parallel nodes cut the memory of large dictionaries. See [double-array trie](/double-array-trie/).
- **Skipping text.** For long patterns and a large alphabet, [Commentz-Walter](/commentz-walter/), [Set Horspool](/set-horspool/) and [Wu-Manber](/wu-manber/) read the text from right to left in a window and skip characters, which is faster on average but not in the worst case.
- **Dynamic dictionaries.** Insertion and deletion of patterns between searches is the problem of [dynamic dictionary matching](/dynamic-dictionary-matching/).
- **Two dimensions.** The [Bird-Baker](/bird-baker/) algorithm runs Aho-Corasick on the rows of a two-dimensional text.

## When to use it

Use Aho-Corasick when the set of patterns is large or when the worst case matters: its search time does not depend on the number of patterns, and an adversary cannot slow it down. It is the standard choice for virus signatures, intrusion detection and the search for a dictionary of words in a stream. For a few long patterns over a large alphabet, the skipping algorithms ([Wu-Manber](/wu-manber/), [Set Horspool](/set-horspool/)) read fewer characters on average. For patterns of one length, [Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/) is short to write. For one pattern, use [Knuth-Morris-Pratt](/knuth-morris-pratt/) or a Boyer-Moore algorithm.

## Pitfalls

- **Reporting only the current node.** Code that outputs only $\mathrm{out}[v]$ at line L19 misses each pattern that is a proper suffix of $\mathrm{str}(v)$: with the patterns she and he, the text she reports only she. Lines L19 to L22 must follow the dictionary links.
- **Following failure links to report.** Walking the whole failure chain at each position, instead of the dictionary chain, gives correct output but $\Theta(n \cdot L)$ time for the longest pattern length $L$, for example on the patterns $a^{L-1}b$ and b and the text $a^n$, where no node on the chain is a pattern until the end.
- **Depth-first link construction.** Line L12 needs $\mathrm{fail}$ of all shallower nodes. Setting the links in depth-first order of the trie reads links that are not set yet. Use breadth-first order (lines L4 to L6).
- **A child of the root failing to itself.** For a node $u$ of depth 1, $\mathrm{goto}(\mathrm{root}, a) = u$, so the rule of line L12 would set $\mathrm{fail}[u] = u$. Line L4 sets these links to the root first.
- **The empty pattern and duplicates.** An empty pattern makes the root a pattern node; it then occurs at each of the $n + 1$ positions, including position $n$ (line L14 handles position 0). A pattern listed twice has two indices in one node; store a list, not a single index.

## Implementations

## History

Alfred Aho and Margaret Corasick published the algorithm in 1975 in the Communications of the ACM. They built it to speed up a library bibliographic search program at Bell Laboratories that looked for many keywords at once. The paper defines the goto, failure and output functions, proves the linear bound, and shows how to turn the machine into a deterministic finite automaton. The failure function extends the one of Knuth, Morris and Pratt, whose journal paper appeared in 1977 but circulated as a technical report before. Aho's `fgrep` program for Unix used this method.

## References
