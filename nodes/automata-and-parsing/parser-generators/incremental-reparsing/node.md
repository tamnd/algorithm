---
tag: SPMN1S
kind: problem
slug: incremental-reparsing
name: Incremental reparsing
aliases:
- incremental parsing problem
area: automata-and-parsing/parser-generators
level: research
summary: Given a parse of a document and a local edit, compute the parse of the edited document in time proportional to the edit.
model: word-ram
prereqs: [parse-tree, lr-parsing, context-free-grammar]
see_also: [incremental-parsing, parser-error-recovery, context-free-language-recognition, packrat-parsing, valiant-algorithm, amortized-update-time, persistent-data-structure, parser-generator]
sources:
  - paper: doi:10.1145/357062.357066
    title: Carlo Ghezzi and Dino Mandrioli, Incremental parsing, ACM Transactions on Programming Languages and Systems 1(1) (1979)
    locator: pp. 58 to 70 (reparsing after a change by reusing the unaffected parts of an earlier deterministic parse)
  - paper: doi:10.1145/293677.293678
    title: Tim A. Wagner and Susan L. Graham, Efficient and flexible incremental parsing, ACM Transactions on Programming Languages and Systems 20(5) (1998)
    locator: pp. 980 to 1013 (incremental LR parsing with reuse of whole subtrees, the treatment of sequences, and the bound in terms of new terminals, modification sites and tree size)
  - paper: doi:10.1145/3136014.3136022
    title: Patrick Dubroy and Alessandro Warth, Incremental packrat parsing, Software Language Engineering (SLE 2017)
    locator: pp. 14 to 25 (keeping the memo table of a packrat parser across edits)
  - paper: doi:10.1145/256303.256309
    title: Gudmund Skovbjerg Frandsen, Peter Bro Miltersen and Sven Skyum, Dynamic word problems, Journal of the ACM 44(2) (1997)
    locator: pp. 257 to 271 (membership in a regular language under changes of single letters)
  - paper: doi:10.1016/S0022-0000(75)80046-8
    title: Leslie G. Valiant, General context-free recognition in less than cubic time, Journal of Computer and System Sciences 10(2) (1975)
    locator: pp. 308 to 315 (static recognition through Boolean matrix multiplication)
  - url: https://tree-sitter.github.io/tree-sitter/using-parsers/3-advanced-parsing.html
    title: Tree-sitter documentation, Advanced parsing
    locator: the section Editing (ts_tree_edit, and ts_parser_parse called with the old tree)
---

Incremental reparsing is the problem of keeping the parse of a document up to date while it is edited: given the old token sequence, its [parse tree](/parse-tree/) and an edit that replaces a few tokens, produce the parse tree of the new sequence, doing work that depends on the size of the edit and of the change in the tree rather than on the length of the document. It is what lets editors and language servers highlight, fold and analyse code on every keystroke. For deterministic grammars Wagner and Graham's incremental LR parser reaches $O(t + s \log N)$ time for $t$ new tokens and $s$ edit sites in a tree of $N$ nodes, but no method can beat the size of the change itself, which a single token can make linear.

## In plain words

A program editor parses the file once, then the user types a character. Parsing the whole file again works, but for a large file it is slow, and almost all of the tree is the same as before. Incremental reparsing asks for the new tree while reusing the untouched parts of the old one: the parser should start near the edit, reuse whole unchanged pieces when it meets them, and stop as soon as the rest of the old tree fits again. The difficulty is that a small edit can matter far away, as when a quote or a comment opener changes the meaning of everything after it, so the reuse has to be checked, not assumed.

## Definition

**Notation.** A grammar is $G = (V, \Sigma, P, S)$ with productions written $A \to \alpha \mid \beta$, the empty string $\varepsilon$, start symbol $S$, input length $n$ and size $|G| = \sum_{A \to \alpha \in P} (|\alpha| + 1)$.

**Input.** A fixed grammar $G$; a token sequence $w = a_1 \cdots a_n$ with a parse tree $T$ for it, plus whatever auxiliary data the method chose to keep from the previous run (parser states, memo tables, lookahead lengths); and an edit $(i, j, x)$, meaning that $a_{i+1} \cdots a_j$ is replaced by the token string $x$, giving $w' = a_1 \cdots a_i \, x \, a_{j+1} \cdots a_n$.

**Output.** A parse tree $T'$ of $w'$, or a report that $w' \notin L(G)$, together with the updated auxiliary data. When the grammar is ambiguous, $T'$ is whatever a fixed batch parser would produce, or a shared forest of all parses. The new tree may share subtrees with the old one.

**Cost.** The work is measured against the size of the edit, $|x| + (j - i)$, and the size of the change: the number of nodes of $T'$ that are not subtrees of $T$. An incremental method is good when its cost is close to that measure, ideally up to a logarithmic factor in $n$, and it must always give the same answer as reparsing from scratch.

## Variants

- **Recognition only.** Maintain only whether $w \in L(G)$ under edits: a dynamic membership problem, studied for regular languages and some context-free ones.
- **Tokens or characters.** Editors change characters, so a full solution also relexes incrementally: the scanner restarts near the edit and stops when its state and token boundaries agree with the old token stream again. The parser then sees an edit of tokens.
- **One edit or many.** Edits may be applied one at a time, or batched, with $s$ separate modification sites handled in one reparse.
- **Grammar class.** Deterministic grammars ([LR](/lr-parsing/), LL) admit a unique tree and table-driven methods; general grammars need generalized parsers and shared forests; parsing expression grammars use [packrat](/packrat-parsing/) memo tables.
- **Erroneous input.** Documents being edited are often not in $L(G)$. Practical systems combine incremental reparsing with [error recovery](/parser-error-recovery/), so that a tree exists for every state of the document and an error stays local.
- **Batch versus online.** In the online setting each edit must be answered before the next arrives; amortized bounds over a sequence of edits ([amortized update time](/amortized-update-time/)) are also of interest.

## Examples

**A list edited at different places.** A list of $n$ statements parsed with the left-recursive rule $L \to L \; ; \; s \mid s$ has a spine of $n$ nodes $L$, the $m$-th covering the first $m$ statements. Replacing statement $k$ by another statement changes every spine node that contains it, so the new tree has $n - k + 1$ new $L$ nodes even though only one token changed. A script counted 1000, 501 and 1 new spine nodes for $k = 1$, 500 and 1000 with $n = 1000$. If the same list is stored as a balanced tree, as Wagner and Graham do for sequences, the same edits create at most 11 new internal nodes: the path from the statement to the root.

**One token that changes everything.** For $S \to x \, X \mid y \, Y$, $X \to a \, X \mid \varepsilon$, $Y \to a \, Y \mid \varepsilon$ and the input $x \, a^m$, changing the first token to $y$ relabels every $X$ node as a $Y$ node: all $m + 2$ internal nodes of the tree are new (1002 of 1002 for $m = 1000$, by script). The same happens in real languages when a comment opener or an unmatched quote is typed at the top of a file: the following text changes from code to comment or string, first at the level of tokens and then of the tree.

**The usual case.** Changing an identifier inside one expression of a long program changes only the leaf and the nodes on its path to the root; every other subtree, and in particular every other statement, can be reused. With balanced sequences that path has logarithmic length.

## Known algorithms

- **Parse from scratch.** A deterministic LR(1) or LL(1) parser, or a packrat parser, takes $O(n)$ time per edit, and a general method such as the [Earley parser](/earley-parser/) or GLR takes up to cubic time. This is the baseline, and it is fast enough for small files.
- **Restart from saved states.** Ghezzi and Mandrioli (1979) kept information from the previous deterministic parse with the tree, so that the parser could resume near the edit and stop when its configuration matched the old parse again, reusing the parts on both sides.
- **Subtree reuse in LR parsing.** Wagner and Graham (1998) give an [incremental LR parser](/incremental-parsing/) whose input is a mix of new tokens and old subtrees: an old subtree is shifted whole when its nonterminal can be shifted in the current state and the edit cannot affect it, and is broken into its children otherwise. Sequences are stored as balanced trees, so that lists do not give the linear spines of the first example. They show a running time of $O(t + s \log N)$ for $t$ new terminals and $s$ modification sites in a tree of $N$ nodes, together with optimal reuse of subtrees, for LR(1) grammars.
- **Incremental packrat parsing.** Dubroy and Warth (2017) keep the memo table of a [packrat parser](/packrat-parsing/) across edits: entries whose examined range does not meet the edit are kept and shifted, and the others are discarded, so the next parse reuses most results.
- **Tools.** Tree-sitter, a parser generator library used by editors, documents a two-step interface: the tree is first adjusted to the edit with `ts_tree_edit`, and `ts_parser_parse` is then called again with the old tree, which produces a new tree that shares structure with the old one.

## Bounds

- **Output lower bound.** Any method that builds $T'$ explicitly must create every node of $T'$ that is not a subtree of $T$, so its cost is at least the size of the change, which is $\Theta(n)$ in the worst case even for a single changed token, as the second example shows. Incremental methods can only win when changes are local, which is the common case in editing.
- **Recognition for regular languages.** For membership in a fixed regular language under changes of single letters, Frandsen, Miltersen and Skyum (1997) give $O(\log n / \log \log n)$ time per change and show that this is optimal for some languages; so even the simplest grammars do not allow constant time per edit.
- **General context-free grammars.** An incremental recognizer with update time $u(n)$ gives a batch recognizer with time about $n \, u(n)$, by inserting the tokens one at a time. Batch recognition for general grammars is known to be possible in the time of [Boolean matrix multiplication](/boolean-matrix-multiplication/) ([Valiant's algorithm](/valiant-algorithm/)) and is not known to be possible in linear time, so no general method is known with update time polylogarithmic in $n$, and the deterministic and PEG classes are where incremental methods are fast.

## Reductions

- **From batch parsing.** As in the bounds, $n$ insertions at the end build the input from nothing, so batch parsing reduces to incremental reparsing with $n$ edits.
- **To batch parsing.** Conversely, reparsing from scratch solves every instance, with the batch cost per edit.
- **Through relexing.** Character edits reduce to token edits by incremental lexing, which is itself an instance of the problem for the regular grammar of the tokens.
- **To dynamic sequence problems.** For grammars whose parse is a composition of per-token transitions, such as recognition by a finite automaton, membership after an edit reduces to maintaining the product of a sequence of transition functions in a balanced tree, at $O(\log n)$ products per change.

## Applications

- **Editors and language servers.** Syntax highlighting, code folding, outline views and structural navigation are recomputed after every keystroke from an incrementally maintained tree.
- **Incremental compilation and analysis.** Name resolution, type checking and other analyses use the set of changed nodes to limit their own work.
- **Structure editors.** Editors that mix structured and textual editing reparse the text the user typed into an otherwise structured document.
- **Interactive environments.** Notebooks and read-eval-print loops reparse a growing input after each line.

## References
