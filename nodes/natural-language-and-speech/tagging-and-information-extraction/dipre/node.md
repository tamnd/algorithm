---
tag: RKXK3C
kind: algorithm
slug: dipre
name: DIPRE
aliases:
- dual iterative pattern relation expansion
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: Brin's bootstrapping that alternates between finding text patterns around seed pairs and finding new pairs that match the patterns.
solves: [relation-extraction]
model: word-ram
complexity:
  vars: {n: the total number of characters of the pages, r: the number of known pairs, p: the number of patterns, c: the largest length of a middle or of a matched field, o: the number of occurrences}
  time: {worst: "O(n c (r + p c))"}
  space: {extra: "O(n + o)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1998
  people: [Sergey Brin]
  note: "Brin presented DIPRE at the WebDB workshop of 1998 and ran it on 24 million web pages, starting from 5 books."
prereqs: [relation-extraction, string-matching]
see_also: [distant-supervision, hearst-patterns, yarowsky-algorithm, named-entity-recognition, regular-expression, aho-corasick, knuth-morris-pratt]
sources:
  - paper: doi:10.1007/10704656_11
    title: "Sergey Brin, Extracting patterns and relations from the World Wide Web, WebDB 1998, Lecture Notes in Computer Science 1590, Springer, 1999, pages 172 to 183"
    locator: "the definitions of occurrences and patterns, the pattern generation with specificity and url splitting, and the experiment on author and title pairs"
  - paper: "Eugene Agichtein and Luis Gravano, Snowball: extracting relations from large plain-text collections, ACM Digital Libraries 2000"
    title: Agichtein and Gravano 2000
    locator: the confidence of patterns and of tuples and the use of named entity tags
---

DIPRE (Dual Iterative Pattern Relation Expansion) finds pairs that stand in one relation, such as (author, title) for books, in a large set of web pages, starting from a handful of examples. Brin (1998) built it on a duality: if you know many pairs, you can find the patterns in which they are written, and if you know good patterns, you can find many pairs. So the algorithm goes back and forth. It looks up the known pairs in the pages and keeps the text around them, turns groups of similar contexts into patterns, and uses the patterns to read new pairs off the pages. It is a heuristic for [relation extraction](/relation-extraction/) with almost no labeled data. Its main risk is drift: one bad pattern brings in bad pairs, and these bring in more bad patterns.

## In plain words

Start with five books you know, each an author and a title. Search the web for pages where an author and title of yours appear close together, and note the text just before, between and after them, and the web address. When several of these places look the same, for example the title in bold, then the word "by", then the author, and all on the same site, make a pattern from what they share. Use the pattern to read every other author and title written the same way on that site. Add the new books to your list and start again. A pattern is kept only if it is specific enough, so that a very short shared context, which would match almost anything, is not used.

## The problem

Input: a set of pages, each a url and a text; a few seed pairs of the relation; a context length $m$ (Brin used 10 characters); and a threshold $t$. Output: a set of pairs of the relation. There is no labeled data beyond the seeds, and no guarantee: a pair is accepted when some accepted pattern finds it.

An occurrence of a pair is a place where both strings appear in a page with at most $c$ characters between them. It records seven things: the author, the title, the order (whether the author comes first), the url, the $m$ characters before the first string (the prefix), the text between the two (the middle) and the $m$ characters after the second (the suffix). A pattern has five parts: the order, a url prefix, a prefix, a middle and a suffix. A page whose url starts with the url prefix matches the pattern where its text holds the prefix, then a field, then the middle, then a field, then the suffix; the two fields are read as the author and the title in the given order.

The specificity of a pattern is the product of the lengths of its middle, url prefix, prefix and suffix. It measures how hard the pattern is to match by chance. A pattern built from $n$ occurrences is accepted when $n > 1$ and specificity times $n$ is above $t$.

## The algorithm

```pseudo id=main
DIPRE(pages, seeds, m, t)
L1  R ← seeds
L2  repeat
L3      O ← all occurrences of the pairs of R in the pages, with order, url, prefix, middle and suffix
L4      group O by (order, middle)
L5      for each group G: urlprefix ← longest common prefix of the urls, prefix ← longest common suffix of the prefixes, suffix ← longest common prefix of the suffixes
L6          if |G| > 1 and specificity · |G| > t then accept the pattern (order, urlprefix, prefix, middle, suffix)
L7          else if the urls of G differ then split G by the next character of the urls after urlprefix, and go to L5 for each part
L8      R ← R ∪ all pairs matched by the accepted patterns
L9  until R does not grow (or after a fixed number of rounds)
L10 return R
```

Line L7 is how Brin rescues a group whose shared context is too short: a smaller group from one site or one directory has a longer url prefix and often a longer shared prefix and suffix, so its pattern may pass the test. The code adds one guard of its own: a field is 1 to $c$ characters with no '<', '>' or line break.

## Example

The test file uses five small pages. Two lists on www.books.com/sf/ write one book per line as `<li><b>Title</b> by Author.`, and list2 also has the line `<li><b>Contents</b> by chapter.` before its closing `</ul>`. Two pages on www.reads.net/a/ write `<p>Author: <i>Title</i></p>`. A blog page says "I read Dune by Frank Herbert and then Foundation by Isaac Asimov." The seeds are (Isaac Asimov, Foundation) and (Frank Herbert, Dune), with $m = 10$ and $t = 100$. Below, `\n` is a line break.

Round 1 finds 5 occurrences. The two on the books.com lists share the middle `</b> by ` and give the url prefix `http://www.books.com/sf/list` (28 characters), the prefix `\n<li><b>` (8) and the suffix `.\n<li><b>` (9). The specificity is $8 \cdot 28 \cdot 8 \cdot 9 = 16128$, and $16128 \cdot 2 > 100$, so the pattern is accepted. The two blog occurrences share the middle ` by `, but their suffixes ` and then ` and `.\n` have no common prefix, so the specificity is 0 and the group is rejected; both are on one url, so it cannot be split. Herbert on reads.net is alone in its group. The pattern finds (Dan Simmons, Hyperion) but not the last book of a list, because its suffix asks for another `<li><b>` line after the book.

Round 2 has 7 occurrences: Simmons now also appears on reads.net next to Herbert, so the reads.net format gives a second pattern, and the two patterns add (William Gibson, Neuromancer), (Ursula K. Le Guin, The Dispossessed) and (Iain Banks, Excession). Round 3 has 11 occurrences. Gibson is the last line of list1, so the books.com suffix shrinks to `.\n<`, and the more general pattern now also matches the last line of list2: it adds the false pair (chapter, Contents). Round 4 adds nothing and the loop stops with 7 pairs, one of them wrong. With $t = 30000$ instead, the false pair never appears, but the run also stops with only Hyperion beside the seeds: a higher threshold trades recall for precision.

## Correctness

DIPRE is a heuristic, so no theorem says that its pairs are true. The proof in [proofs/correctness.md](proofs/correctness.md) shows what can be shown: the longest common prefix of a list is the one of its smallest and largest strings; the pattern step ends, because each split makes strictly smaller groups; each accepted pattern has $n > 1$ and specificity times $n > t$; an accepted pattern matches every occurrence it was built from, so a known pair is never lost; and the loop ends, because the set of pairs only grows and there are finitely many substrings. The test file checks the matcher against a search over all ways to cut a text into prefix, field, middle, field and suffix.

## Complexity

Let $n$ be the total length of the pages, $r$ the number of known pairs, $p$ the number of patterns and $c$ the bound on the middle and on a field. Count each string comparison and field check as one step, and list the positions of a string in a page with a linear-time [string matching](/string-matching/) method such as [Knuth-Morris-Pratt](/knuth-morris-pratt/). For each pair, each position of the first string is followed by at most $c$ candidate positions of the second, so finding occurrences costs $O(n c r)$. For each pattern, each position of its prefix has at most $c$ positions of the middle and $c$ of the suffix, so matching costs $O(n c^2 p)$. Grouping and the common prefixes cost the total length of the occurrences. So one round costs $O(n c (r + p c))$, the bound given above, and the space is $O(n + o)$ for the pages and the $o$ occurrences. Brin ran the occurrence search over 24 million pages; at that size the search over the text, done with an index, is the main cost.

## Properties

- Heuristic: precision depends on the pages and on $t$. Brin reports (a measurement) that 19 of 20 books sampled from his final list were real books.
- Weakly supervised: only the seeds are given. The patterns come from the data.
- Monotone: pairs are never removed, so an error stays and can spread. This is the drift that the example shows.
- Site-specific patterns: the url prefix limits a pattern to one site or directory, which is why patterns from web lists can be long and exact.

Brin's run on 24 million pages (a measurement): from 5 seed books, the first round found 199 occurrences, 3 patterns and 4047 pairs; the second found 3972 occurrences, 105 patterns and 9369 pairs; the final round found 9938 occurrences and 346 patterns, for 15257 books. Brin reports that he removed by hand 242 occurrences that involved a false title, "Conclusion".

## Variants and improvements

- Snowball (Agichtein and Gravano 2000) works on plain text with named entity tags, so a pattern requires an organization and a location in the right slots. It represents contexts as term vectors, clusters them, and gives each pattern a confidence from the share of its matches that agree with known pairs; a new pair is kept only if its confidence from all the patterns that found it is high enough.
- [Hearst patterns](/hearst-patterns/) are hand-written lexical patterns such as "X such as Y" for the is-a relation; DIPRE learns such patterns from seeds instead.
- The [Yarowsky algorithm](/yarowsky-algorithm/) uses the same bootstrapping idea for word senses: rules label examples and labeled examples make new rules.
- [Distant supervision](/distant-supervision/) also needs no hand-labeled sentences, but takes many pairs from a knowledge base at once and trains a classifier, instead of growing a small seed set.

## When to use it

Use DIPRE, or one of its descendants, when you want a large set of pairs of one relation from many semi-structured pages, you can name a few examples, and you can check a sample of the output by hand. It works best on lists and tables made by templates. For relations written in free prose, Snowball-style methods with entity tags, distant supervision or a trained classifier work better.

## Pitfalls

- Drift: one general pattern can bring in a whole class of wrong pairs, which then make new patterns. Check samples after each round, and keep $t$ high.
- Too long contexts: the suffix or prefix can capture parts of the next line, so a pattern misses the last item of a list, as in the example. More rounds usually fix this, but they also make patterns more general.
- Name variants: "I. Asimov" and "Isaac Asimov" count as different pairs. Normalize the strings before counting.
- Duplicate pages: mirrors of one page make one context look common. Remove duplicates before grouping.
- Many-to-many relations: an author has many books, so the pairs give no simple consistency test; Snowball's confidence works best when one side determines the other, as for an organization and its headquarters.

## Implementations

## History

Hearst (1992) had shown that a few lexical patterns find many is-a pairs in text. Brin (1998) turned the idea around: let the data find the patterns from a few pairs, and use the web as the text. The name stresses the duality of patterns and relations. Snowball (Agichtein and Gravano 2000) extended the idea to plain text with entity tags and confidence scores, and later open information extraction systems and distant supervision grew from the same aim of extraction with little labeled data.

## References
