---
tag: 2HK8NC
kind: technique
slug: optimal-parsing
name: Optimal parsing
aliases:
- shortest-path parsing
area: compression-and-coding/dictionary-compression
level: advanced
summary: Find the cheapest way to cut a text into dictionary phrases, as a shortest path over the text positions solved by dynamic programming.
prereqs: [greedy-parsing, dag-shortest-paths, trie]
see_also: [optimal-lz-parsing, lazy-matching, static-dictionary-compression, lzw, lz78, text-segmentation, dp-on-dag]
sources:
  - paper: doi:10.1137/120869511
    title: Paolo Ferragina, Igor Nitto and Rossano Venturini, On the bit-complexity of Lempel-Ziv compression, SIAM Journal on Computing 42(4), 1521-1541, 2013
    locator: "Section 1 (the shortest path view of parsing, credited to Schuegraf and Heaps 1974, and the known results: greedy is optimal for suffix-complete dictionaries and flexible parsing for prefix-complete dictionaries)"
  - paper: "Ernst J. Schuegraf and H. S. Heaps, A comparison of algorithms for data base compression by use of fragments as language elements, Information Storage and Retrieval 10(9-10), 309-319, 1974"
    locator: the parse of a text into fragments of a fixed set as a shortest path problem
  - paper: doi:10.1145/945394.945404
    title: Yossi Matias, Nasir Rajpoot and S. Cenk Sahinalp, The effect of flexible parsing for dynamic dictionary-based data compression, ACM Journal of Experimental Algorithmics 6, 2001
    locator: the flexible parsing rule, and LZW-FP, which builds the same dictionary as LZW and changes only the parse
  - paper: "Martin Cohn and Roger Khazan, Parsing with prefix and suffix dictionaries, Proceedings of the Data Compression Conference (DCC 1996), 180-189"
    locator: optimal parsing with prefix-closed and suffix-closed dictionaries
---

Optimal parsing cuts a text into phrases of a dictionary so that the total cost of the phrases is as small as possible. The cost may be the number of phrases or the number of output bits. The parses of $t[0 \ldots n-1]$ are the paths from node $0$ to node $n$ in a directed acyclic graph on the positions, so the cheapest parse is a shortest path, and a dynamic program over the positions from right to left finds it. This page covers the technique for any dictionary, mainly static ones; [optimal LZ parsing](/optimal-lz-parsing/) is the special problem where the dictionary is the earlier text of an LZ77 encoder and the cost depends on the copy distance.

## In plain words

You have a list of allowed pieces, each with a price, and you want to build a text from pieces at the lowest total price. Taking the longest piece at each step is not always cheapest: a long piece can leave you at a place where only bad pieces fit.

The fix is to work backward. Start at the end of the text, where the price of the rest is zero. Then step back one letter at a time. At each place, try every allowed piece that starts there, and add its price to the best price already known for the place where it ends. Keep the cheapest choice. When you reach the start, you know the best total price, and you follow the kept choices forward to read the pieces.

## When it applies

**Setting.** The input is a string $t = t[0 \ldots n-1]$ over an alphabet $\Sigma$ of size $\sigma$, and a dictionary $D$ of strings with a cost $c(w) \ge 0$ for each $w \in D$. A *parse* of $t$ is a sequence $w_1, \ldots, w_k$ of members of $D$ with $w_1 w_2 \cdots w_k = t$. Its cost is $c(w_1) + \cdots + c(w_k)$. The model is the worst case: no probability model, only the given text and costs. With $c \equiv 1$ the cost is the number of phrases.

**The graph.** Make one node for each position $0, 1, \ldots, n$, and an edge $i \to i + |w|$ of weight $c(w)$ for each $w \in D$ that occurs at position $i$ of $t$. Every edge goes forward, so the graph is a [directed acyclic graph](/directed-acyclic-graph/), and the parses of $t$ are exactly its paths from $0$ to $n$. Schuegraf and Heaps (1974) set up parsing as this shortest path problem.

**The recurrence.** Let $C[i]$ be the least cost of a parse of the suffix $t[i \ldots n-1]$. Then $C[n] = 0$ and

$$C[i] = \min \{\, c(w) + C[i + |w|] : w \in D \text{ occurs at } i \,\},$$

with $C[i] = \infty$ when no phrase fits. The proof is the [principle of optimality](/principle-of-optimality/): the first phrase of an optimal parse of $t[i \ldots]$ is some $w$, and the rest must be an optimal parse of $t[i+|w| \ldots]$, or a cheaper rest would give a cheaper parse. Conversely each term of the minimum is the cost of a parse. The positions from $n$ down to $0$ are a topological order, so each $C[i + |w|]$ is known when $C[i]$ is computed.

The technique needs three things: the cost of a phrase must not depend on the earlier phrases, the dictionary must not depend on the parse, and the encoder must be able to list all phrases that occur at a position. When the dictionary changes with the parse, as in [LZ78](/lz78/) and [LZW](/lzw/), the graph is not fixed and the recurrence does not apply as it is.

## The template

```pseudo id=main
OPTIMAL-PARSE(t)
L1  C[n] ← 0
L2  for i ← n − 1 downto 0 do
L3      C[i] ← ∞
L4      for each phrase w ∈ D that occurs at position i do      ▷ hole: list the phrases, e.g. by a trie walk
L5          if c(w) + C[i + |w|] < C[i] then                     ▷ hole: the cost c
L6              C[i] ← c(w) + C[i + |w|]; next[i] ← i + |w|
L7  i ← 0; while i < n do emit t[i .. next[i] − 1]; i ← next[i]
L8  return C[0]
```

The holes are the phrase lister in line L4 and the cost in line L5. For a static dictionary stored in a [trie](/trie/), line L4 walks the trie along $t[i \ldots]$ and reports each node that marks a member. If the longest member has length $L$, the walk costs $O(L)$, and the whole parse takes $O(nL)$ time and $O(n)$ extra space beyond the trie. For the dictionary of all substrings of the earlier text (LZ77) the graph has $\Theta(n^2)$ edges in the worst case, and [optimal LZ parsing](/optimal-lz-parsing/) shows which edges can be dropped.

### Flexible parsing

For a dictionary that is *prefix-closed* (each prefix of a member is a member) and contains each single symbol, a one-pass rule without the table $C$ is optimal in phrase count. Let $L(j)$ be the length of the longest member at position $j$. Flexible parsing, at position $i$, takes the phrase $t[i \ldots e-1]$ with $i < e \le i + L(i)$ that maximizes $e + L(e)$, so that the next phrase reaches as far as possible. Greedy, in contrast, maximizes $e$.

**Claim.** For such a dictionary, flexible parsing uses the minimum number of phrases.

**Proof.** Because $D$ is prefix-closed, the phrases at $j$ end exactly at $j+1, \ldots, j+L(j)$. Let $R_0 = 0$ and $R_{k+1} = \max_{j \le R_k} (j + L(j))$. By induction, the positions that some parse can reach in at most $k$ phrases are exactly $0, \ldots, R_k$: a position $p$ with $R_k < p \le R_{k+1}$ is reached in one phrase from the $j \le R_k$ that gives the maximum. So the least number of phrases is the least $k$ with $R_k \ge n$. Let $f_k$ be the position of flexible parsing after $k$ phrases. We show $f_k \le R_k$ and $f_k + L(f_k) = R_{k+1}$. For $k = 0$ both hold. For the step, flexible parsing picks $f_{k+1}$ in the range $(f_k, R_{k+1}]$, so $f_{k+1} \le R_{k+1}$. Every $j \le f_k$ has $j + L(j) \le R_{k+1}$ since $f_k \le R_k$, while $e = R_{k+1}$ in the range gives $e + L(e) > R_{k+1}$. So the maximum of $j + L(j)$ over $j \le R_{k+1}$ is reached inside the range, and $f_{k+1} + L(f_{k+1}) = R_{k+2}$. Thus flexible parsing ends with the first $k$ such that $R_k \ge n$. $\square$

## Classic examples

- **Static dictionaries.** [Static dictionary compression](/static-dictionary-compression/) with a fixed phrase list, for example common words or digrams, is the original use: the parse with the fewest phrases, or the fewest bits when phrases have codes of different lengths.
- **LZ77 with a bit cost.** [Optimal LZ parsing](/optimal-lz-parsing/) runs the same recurrence with copies as edges and the length of the codes of the length and the distance as the cost. LZMA and the `btopt` and `btultra` strategies of [Zstandard](/zstandard/) use parsers of this kind.
- **LZW with flexible parsing.** LZW-FP of Matias, Rajpoot and Sahinalp builds the same dictionary as [LZW](/lzw/) but cuts the text with the flexible rule, which needs fewer phrases on many inputs.
- **Word segmentation.** [Text segmentation](/text-segmentation/) into dictionary words with a score per word is the same shortest path computation.

### Worked examples

The tests in `impl/python` check each value below.

| Dictionary $D$ and costs | Text | Greedy | Flexible | Optimal |
|---|---|---|---|---|
| $\{a, b, c, d, ab, bc, bcd\}$, cost 1 each | `abcd` | `ab`, `c`, `d` (3) | `a`, `bcd` (2) | 2 |
| $\{a, b, ab, ba, bab\}$, cost 1 each | `abab` | `ab`, `ab` (2) | not prefix-closed | `a`, `bab` (2) |
| $a$ and $b$ cost 2, $ab$ costs 5 | `ab` | `ab` (cost 5) | `ab` (cost 5) | `a`, `b` (cost 4) |

For `abcd` the table is $C[4] = 0$, $C[3] = 1$ (`d`), $C[2] = 2$ (`c` then `d`), $C[1] = 1$ (`bcd`), and $C[0] = \min(1 + C[1], 1 + C[2]) = 2$ with the first phrase `a`. Flexible parsing at position 0 compares $e = 1$, which reaches $1 + L(1) = 4$, with $e = 2$, which reaches $2 + L(2) = 3$, and takes `a`. The tests also compare the dynamic program with the minimum over all parses on random dictionaries and costs, and flexible parsing with the optimum on random prefix-closed dictionaries.

## Variations

- **Left to right.** The same recurrence can run forward, with $C[i]$ the cost of the best parse of $t[0 \ldots i-1]$. An encoder that works on a stream uses this form and fixes the parse up to a point once all paths pass through it.
- **Unit costs.** With $c \equiv 1$, a breadth-first search from node $0$ suffices, and flexible parsing does it in one pass for prefix-closed dictionaries.
- **Costs that depend on the parse.** Real entropy coders set the code lengths from the statistics of the parse itself. Encoders then run the parse, update the cost estimates, and parse again. The result is a good parse, not a proven optimum.
- **Dynamic dictionaries.** For LZ78 and LZW, the dictionary at each step depends on the earlier phrases. Flexible parsing keeps the dictionary of the greedy LZW and changes only the cut, which keeps the decoder simple.
- **Suffix-closed dictionaries.** When every suffix of a member is a member, plain greedy is already optimal in phrase count; see [greedy parsing](/greedy-parsing/).

## Pitfalls

- **Greedy is not optimal for a general static dictionary.** The first worked example shows a gap of one phrase; longer texts give larger gaps.
- **Flexible parsing needs prefix closure.** Without it, the ends $j+1, \ldots, j+L(j)$ are not all phrase ends, and the proof fails. The tests find random dictionaries where flexible parsing uses more phrases than the optimum.
- **No parse may exist.** If $D$ misses a symbol of $t$, then $C[0] = \infty$. Greedy can also get stuck where a parse exists, for example $D = \{aa, aaa\}$ and `aaaa`.
- **Do not mix the LZ77 problem with this one.** For LZ77 the dictionary at position $i$ is the set of substrings that occur before $i$, there can be $\Theta(n^2)$ edges, and a copy has many distances with different costs. Listing all phrases as in line L4 is then too slow; see [optimal LZ parsing](/optimal-lz-parsing/).
- **Recursion depth.** A top-down memoized version recurses $n$ levels deep. Use the loop from right to left.

## Exercises

1. Show that for a suffix-closed dictionary that contains each single symbol, $C[i]$ with unit costs is non-increasing in $i$, that is $C[i] \ge C[i+1]$, and use it to prove again that greedy is optimal in phrase count.
2. Give a prefix-closed dictionary and a text on which flexible parsing is optimal in phrase count but not in total cost for some costs.

## References
