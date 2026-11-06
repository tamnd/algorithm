---
tag: 3Y0Y57
kind: algorithm
slug: incremental-parsing
name: Incremental parsing
aliases:
- Wagner-Graham incremental parsing
- incremental reparsing
area: automata-and-parsing/context-free-parsing
level: research
summary: Re-parses only the changed regions of an edited input, reusing prior parse results.
solves: [incremental-reparsing]
model: word-ram
complexity:
  vars: {n: the length of the edited input, G: the grammar size (the sum over all productions of the right side length plus one), r: the number of item sets that are computed again}
  time: {worst: O(n^3 G), best: O(n G), edit: O((r + 1) n^2 G)}
  space: {extra: O(n^2 G)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1979
  people: [Carlo Ghezzi, Dino Mandrioli]
  note: Ghezzi and Mandrioli published an incremental LR parser in 1979, after earlier work by Lindstrom in 1970 and Celentano in 1978. In 1998 Wagner and Graham gave an incremental LR parser for many edits at once with optimal reuse of nodes.
prereqs: [earley-parser, parse-chart, context-free-language-recognition]
see_also: [incremental-reparsing, lr-parsing, glr-parsing, packrat-parsing, parse-tree, abstract-syntax-tree, parser-error-recovery, chart-parsing]
sources:
  - paper: doi:10.1145/357062.357066
    title: Carlo Ghezzi and Dino Mandrioli, Incremental parsing, ACM Transactions on Programming Languages and Systems 1(1) (1979)
    locator: pp. 58 to 70
  - paper: doi:10.1145/322203.322215
    title: Carlo Ghezzi and Dino Mandrioli, Augmenting parsers to support incrementality, Journal of the ACM 27(3) (1980)
    locator: pp. 564 to 579
  - paper: doi:10.1145/293677.293678
    title: Tim A. Wagner and Susan L. Graham, Efficient and flexible incremental parsing, ACM Transactions on Programming Languages and Systems 20(5) (1998)
    locator: pp. 980 to 1013
  - paper: doi:10.1145/800161.805153
    title: G. Lindstrom, The design of parsers for incremental language processors, Proceedings of the Second Annual ACM Symposium on Theory of Computing (1970)
    locator: pp. 81 to 91
  - paper: doi:10.1007/bf00265676
    title: A. Celentano, Incremental LR parsers, Acta Informatica 10(4) (1978)
    locator: the whole paper
  - paper: doi:10.1145/362007.362035
    title: Jay Earley, An efficient context-free parsing algorithm, Communications of the ACM 13(2) (1970)
    locator: pp. 94 to 102 (the item sets that this page reuses)
  - paper: doi:10.1145/3136014.3136022
    title: Patrick Dubroy and Alessandro Warth, Incremental packrat parsing, Proceedings of the 10th ACM SIGPLAN International Conference on Software Language Engineering (2017)
    locator: pp. 14 to 25
  - book: isbn:9780387202488
    title: Dick Grune and Ceriel J. H. Jacobs, Parsing Techniques, A Practical Guide, second edition, Springer, 2008
    locator: Section 9.10.4, Incremental Parsing; Section 18.2.8, Incremental Parsing (annotated bibliography), p. 629
---

Incremental parsing parses a string again after an edit, and reuses the work that it did for the old string. Program editors use it to keep a [parse tree](/parse-tree/) up to date after each keystroke, in time that depends on the edit and not on the size of the file. The method on this page keeps the [Earley](/earley-parser/) item sets: the sets before the edit stay, the sets after it are computed again until one of them agrees with the old chart, and the old sets after that point are reused with shifted positions. It works for every [context-free grammar](/context-free-grammar/), and it gives the same chart as a full parse.

## In plain words

A parser that reads from left to right writes down, at each position, what it knows about the text so far. When you change a few characters in the middle of a long file, everything that the parser wrote before the change is still true, because it did not look at the changed part. After the change, the parser starts again from the last good position and reads the new text. A short distance after the change, its notes often become the same as the old notes, moved by the difference in length. From that point on, it is as if the parser had never seen the change, so it can copy the rest of the old notes. The parser must only check that the matching notes do not depend on anything inside the changed part.

## The problem

We use the notation of the grammar pages: productions $A \to \alpha \mid \beta$, $\varepsilon$ for the empty string, $S$ the start symbol, $n$ the input length, and the grammar size $|G| = \sum_{A \to \alpha} (|\alpha| + 1)$.

The input is a context-free grammar $G = (V, \Sigma, P, S)$, any productions allowed, an old string $w = a_1 \cdots a_n$ with its Earley chart $E[0], \ldots, E[n]$, and an edit: positions $0 \le p \le q \le n$ and a string $v$ of length $t$ that replaces $a_{p+1} \cdots a_q$. The output is the new string $w' = a_1 \cdots a_p\, v\, a_{q+1} \cdots a_n$ of length $n' = n + \delta$, with $\delta = t - (q - p)$, and its Earley chart $E'[0], \ldots, E'[n']$. The chart answers the [membership question](/context-free-language-recognition/) for $w'$ and is the input to the next edit. This is the [incremental reparsing](/incremental-reparsing/) problem with the Earley chart as the stored parse.

## The algorithm

The [parse chart](/parse-chart/) of Earley's algorithm has one set $E[j]$ for each position $j$. An item $[A \to \alpha \bullet \beta,\ i] \in E[j]$ says that $\alpha$ derives $a_{i+1} \cdots a_j$ and that $A$ can start at position $i$; $i$ is the **origin** of the item. Two facts make reuse possible. First, $E[j]$ depends only on $a_1 \cdots a_j$, so the sets $E[0], \ldots, E[p]$ do not change. Second, $E[j]$ is computed from $E[j - 1]$, the symbol $a_j$ and the sets $E[i]$ at the origins $i$ of its items; nothing else.

Let $q' = p + t$, the end of $v$ in $w'$. An old position $i \ge q$ corresponds to the new position $i + \delta$, and an old position $i \le p$ with $i < q$ to itself. The **shift** $\sigma$ applies this map to the origin of each item. A new set $E'[k]$ with $k \ge q'$ is **anchored** when it equals $\sigma(E[k - \delta])$, and every origin $i$ of the old set lies before the edit, or is $k - \delta$ itself, or is an old position $i \ge q$ whose new set $E'[i + \delta]$ is anchored. Once a set is anchored, all later sets equal the shifted old sets, so the parser can stop.

```pseudo id=main
REPARSE(G, w, E, p, q, v)          ▷ E is the Earley chart of w; replace a_{p+1} … a_q by v
L1  w′ ← a_1 ⋯ a_p v a_{q+1} ⋯ a_n; n′ ← |w′|; δ ← |v| − (q − p); q′ ← p + |v|
L2  E′[0], …, E′[p] ← E[0], …, E[p]                        ▷ the prefix does not change
L3  for k ← p to n′ do
L4      if k > p then E′[k] ← EARLEY-SET(G, E′[0..k−1], scan of E′[k − 1] over a′_k, k)
L5      if k ≥ q′ then
L6          ANCH[k] ← every origin i of E[k − δ] has (i < q and i ≤ p) or (i ≥ q and (i = k − δ or ANCH[i + δ]))
L7          ANCH[k] ← ANCH[k] and E′[k] = σ(E[k − δ])         ▷ σ maps an origin i ≥ q to i + δ
L8          if ANCH[k] then
L9              for j ← k + 1 to n′ do E′[j] ← σ(E[j − δ])      ▷ reuse the old suffix
L10             return w′, E′
L11 return w′, E′

RECOGNIZE-AFTER-EDIT(G, w, E, p, q, v)
L12 (w′, E′) ← REPARSE(G, w, E, p, q, v); return true if some [S → α •, 0] ∈ E′[n′], else false
```

EARLEY-SET is one round of lines L5 to L12 of the [Earley parser](/earley-parser/): it starts from the items that scan $a'_k$ from $E'[k - 1]$, and closes them under prediction, completion and the nullable rule. For the sets at origins before $k$, it builds once an index of their items by the symbol after the dot. When $q > p$ and $v$ is empty, $q' = p$, and line L6 tests the unchanged set $E'[p]$ against the old set $E[q]$: a deletion can be anchored at once.

The test of line L6 is needed. Two charts can agree at position $k$ while an item there has an origin whose set has changed. That item will later complete and read the changed set. So equality at one position is not enough; the origins must be anchored too.

## Example

Take the grammar $E \to E + T \mid T$, $T \to ( E ) \mid a$ and $w = a + ( a ) + a$, so $n = 7$. The edit replaces the fourth symbol, the inner $a$, by $a + a$: $p = 3$, $q = 4$, $v = a + a$, $\delta = 2$ and $q' = 6$. The new string is $w' = a + ( a + a ) + a$, with $n' = 9$.

| New position $k$ | What happens | $E'[k]$ |
|---|---|---|
| 0 to 3 | copied from $E[0..3]$ (line L2) | $E'[3]$ holds $[T \to ( \bullet E ), 2]$ and the predictions at 3 |
| 4, 5 | computed (line L4), inside the edit | $E'[5] = \{[E \to E + \bullet T, 3], [T \to \bullet ( E ), 5], [T \to \bullet a, 5]\}$ |
| 6 | computed; $6 \ge q'$, so tested against $E[4]$ | $[E \to E + T \bullet, 3]$, $[E \to E \bullet + T, 3]$, $[T \to ( E \bullet ), 2]$, $[T \to a \bullet, 5]$ |
| 7 | computed; tested against $E[5]$, anchored | $[E \to E + T \bullet, 0]$, $[E \to E \bullet + T, 0]$, $[T \to ( E ) \bullet, 2]$ |
| 8, 9 | $\sigma(E[6])$ and $\sigma(E[7])$ (line L9) | $E'[9]$ holds $[E \to E + T \bullet, 0]$ |

At $k = 6$, the old set $E[4] = \{[E \to E \bullet + T, 3], [E \to T \bullet, 3], [T \to ( E \bullet ), 2], [T \to a \bullet, 3]\}$ has all its origins before the edit, but it is not equal to $E'[6]$: the new set has the item $[T \to a \bullet, 5]$, which starts inside $v$. At $k = 7$, after the closing parenthesis, the old set $E[5] = \{[E \to E + T \bullet, 0], [E \to E \bullet + T, 0], [T \to ( E ) \bullet, 2]\}$ has origins 0 and 2, both before the edit, and it equals $E'[7]$. So the set is anchored. Four sets are computed again ($r = 4$), and the last two are shifted copies. $E'[9]$ contains $[E \to E + T \bullet, 0]$, so $w'$ is accepted.

The test of line L6 matters in the grammar $S \to x A c \mid y A d$, $A \to a A \mid z$. Edit $w = x a a z c$ by replacing $x$ with $y$. The new set after $y a$ equals the old set after $x a$: both are $\{[A \to a \bullet A, 1], [A \to \bullet a A, 2], [A \to \bullet z, 2]\}$. But origin 1 points to the set after the first symbol, which holds $[S \to y \bullet A d, 0]$ instead of $[S \to x \bullet A c, 0]$. If the parser reused the old suffix here, it would accept $y a a z c$, which is not in the language. Line L6 rejects the anchor, the parser computes all sets, and $y a a z c$ is rejected.

## Correctness

**Claim.** REPARSE returns $w'$ and the Earley chart of $w'$. So line L12 returns true if and only if $S \Rightarrow^* w'$.

*Prefix and computed sets.* An Earley set $E[j]$ is the least set that contains the items scanned from $E[j - 1]$ and is closed under prediction and completion, where completion reads the sets at the origins. It depends only on $a_1 \cdots a_j$, so lines L2 and L4 build correct sets.

*Anchored sets propagate.* Call an old position good if it lies before the edit, or if it is at least $q$, its new set equals the shifted old set, and all earlier origins in its set are good. Line L6 and line L7 test exactly this. If $K$ is good, then the old $E[K + 1]$ and the new $E'[K + 1 + \delta]$ are built from the same seed by the same rules, and every completion reads sets at good origins, where the new set is the shift of the old one. A least-set argument in both directions gives $E'[K + 1 + \delta] = \sigma(E[K + 1])$, and the origins of $E[K + 1]$ are again good. By induction, every set that line L9 copies is correct. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $m$ be the position where line L8 stops, or $n'$, and let $r = m - p$ be the number of sets that line L4 computes.

- **Computed sets.** A set $E'[k]$ has at most $(k + 1) |G|$ items. Completion for a pair $(A, i)$ reads the items of $E'[i]$ that wait on $A$, through the index, and each item of $E'[i]$ waits on one symbol, so one set costs $O(\sum_{i \le k} |E'[i]|) = O(n^2 |G|)$. The $r$ computed sets cost $O(r n^2 |G|)$.
- **Tests.** Line L6 and line L7 take time linear in the two sets, $O(n |G|)$, at most $r + 1$ times.
- **Copies.** Lines L2 and L9 write $n' + 1 - r$ sets. In this simple form, line L9 copies each shifted set, which costs its size, at most $O(n^2 |G|)$ in total.
- **Total.** The time is $O((r + 1) n^2 |G|)$. If no set is anchored, $r$ can be $n$, and the time is $O(n^3 |G|)$, the same as a full Earley parse. If the sets have $O(|G|)$ items each and $r$ is small, the time is $O(n |G|)$, mostly for the copies. The space is the new chart, $O(n^2 |G|)$.

## Properties

- **Exact.** The result is the same chart that Earley's algorithm builds for $w'$ from scratch, so the answers, and the parse trees read from the chart, are the same.
- **General.** It works for every context-free grammar, including empty productions, unit productions, cycles, left recursion and ambiguity.
- **Safe stop.** The parser stops only at a set whose items and origins are tied to the old chart. A wrong guess costs time but never correctness.
- **Bounded by a full parse.** In the worst case, it computes every set after $p$, which is never more work than a full parse plus the tests.
- **Repeatable.** The output chart is the input to the next edit.

## Variants and improvements

- **State matching for LR parsers.** Ghezzi and Mandrioli used the same idea with an [LR parser](/lr-parsing/): the parser saves its stack at each position, restarts at the edit, and stops when its configuration matches a saved one at the corresponding old position. Their 1980 paper extends the idea to other parsing methods.
- **Reuse of subtrees.** Wagner and Graham parse the old parse tree as input, not only the tokens. Subtrees that the edit does not touch are shifted as single symbols, if the parse state allows it, so the parser does not even look at their tokens. Their parser handles many edits at once, in optimal time, and keeps as many old tree nodes as possible.
- **Lazy shifts.** If positions are stored as references to tokens, or as offsets in a balanced tree, the old suffix needs no copy, and line L9 costs much less than the size of the suffix.
- **Incremental packrat parsing.** A [packrat parser](/packrat-parsing/) stores results by position. Dubroy and Warth keep the memo entries that did not read into the edited region, with shifted positions.
- **Generalized LR.** An incremental [GLR parser](/glr-parsing/) reuses subtrees of a shared parse forest, so ambiguous grammars can be used in an editor.
- **Error recovery.** Editors see many inputs that are not yet correct. An incremental parser is often combined with [error recovery](/parser-error-recovery/), so that the unchanged parts of the tree survive while the user types.

## When to use it

Use incremental parsing when the same input is parsed again and again after small edits, as in a program editor, a language server or a structure editor. For a single parse, or after large edits, a full parse is simpler and just as fast. The chart method on this page suits general grammars and small or medium inputs, because the Earley chart takes $O(n^2 |G|)$ space. For programming languages with LR grammars, the subtree-reuse parsers of Wagner and Graham keep only the [parse tree](/parse-tree/) or the [abstract syntax tree](/abstract-syntax-tree/), and are the usual choice.

## Pitfalls

- **Matching one set is not enough.** Two charts can agree at a position and still differ in a set that an origin points to. Check the origins, as line L6 does; the example with $x A c$ and $y A d$ shows the wrong answer that the plain test gives.
- **The two meanings of position $p$ or $q$.** After an insertion ($p = q$), the old position $q$ maps to $q'$, not to $p$; after a deletion ($t = 0$), the old positions $p$ and $q$ both become $p$. A shift that sends origin $q$ to itself after an insertion does not follow the meaning of the old items, and it finds fewer anchors.
- **Lookahead.** A parser that reads $k$ symbols ahead used the symbols after a position to build its state. With lookahead, the sets just before the edit can also change, so the restart point must move back by the lookahead.
- **Stale semantic values.** Reused trees keep their attributes. Values that depend on the context of a node, such as the scope of a name, must be computed again even when the tree is reused.
- **Recursion depth.** Long inputs make long chains of sets and deep trees. Process the sets with loops, as the implementation does.

## Implementations

## History

Lindstrom studied parsers for incremental language processors in 1970, and Celentano described incremental LR parsers in 1978. Ghezzi and Mandrioli published an incremental LR parser in 1979 that restarts at the edit and stops when the parser state matches a saved one, and in 1980 they extended the idea to other parsers. Wagner and Graham showed in 1998 that earlier LR methods were inefficient, too restrictive, or in some cases wrong, and gave a simple parser for LR($k$) sentential forms that reuses subtrees, handles many edits in optimal time, and keeps the most old nodes. Dubroy and Warth gave an incremental packrat parser in 2017.

## References
