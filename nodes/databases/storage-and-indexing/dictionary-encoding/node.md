---
tag: 4407VK
kind: technique
slug: dictionary-encoding
name: Dictionary encoding
aliases:
- order-preserving dictionary encoding
- domain encoding
area: databases/storage-and-indexing
level: core
summary: "Replace each value of a column by a small integer code from a dictionary of its distinct values. If the dictionary is sorted, the codes keep the order and range filters run on codes."
prereqs: [decomposition-storage-model, bit-packing]
see_also: [dictionary-based-compression, late-materialization, frame-of-reference-encoding, bit-packing, run-length-encoding, decomposition-storage-model, front-coding, zone-map]
sources:
  - paper: "Daniel Abadi, Samuel Madden and Miguel Ferreira, Integrating compression and execution in column-oriented database systems, Proceedings of the 2006 ACM SIGMOD International Conference on Management of Data, 2006, 671 to 682"
    title: Integrating compression and execution in column-oriented database systems
    locator: the dictionary scheme among the compression methods of C-Store, and the operators that work on the codes
  - paper: "Daniel Abadi, Peter Boncz, Stavros Harizopoulos, Stratos Idreos and Samuel Madden, The design and implementation of modern column-oriented database systems, Foundations and Trends in Databases 5(3), 2013, 197 to 280"
    title: The design and implementation of modern column-oriented database systems
    locator: the section on compression in column stores and the section on operating directly on compressed data
  - paper: "Carsten Binnig, Stefan Hildenbrand and Franz Faerber, Dictionary-based order-preserving string compression for main memory column stores, Proceedings of the 2009 ACM SIGMOD International Conference on Management of Data, 2009"
    title: Dictionary-based order-preserving string compression for main memory column stores
    locator: order-preserving dictionaries that accept new values without a full re-encoding
---

Dictionary encoding is the most common compression scheme of column stores, tables kept as in the [decomposition storage model](/decomposition-storage-model/). It lists the distinct values of a column once, in a *dictionary* $D$, and stores the column as a list of small integer *codes*, each the index of a value in $D$, packed in $w$ bits each by [bit packing](/bit-packing/). A column of a million city names with a thousand distinct cities becomes a dictionary of a thousand names and a million 10-bit codes. It is the column form of [dictionary-based compression](/dictionary-based-compression/): the dictionary has whole values, not substrings of a text, and every code has the same width, so the code of row $i$ is at bit $i w$. A scan can evaluate a predicate on the codes without decoding them, which is why the scheme fits [late materialization](/late-materialization/). If $D$ is sorted, the dictionary is *order-preserving*: $a < b$ exactly when $\mathrm{code}(a) < \mathrm{code}(b)$, and a range predicate on values becomes a range of codes. If $D$ is in order of arrival, only equality is preserved.

## In plain words

Think of a long list of city names, one per row, where the same few cities appear again and again. Instead of writing "Paris" a thousand times, write a short list of the cities once, number them, and keep only the numbers in the long list. Numbers are short, so the list becomes much smaller.

To find the rows with Paris, look up the number of Paris once and then search the list of numbers. You never need to read a name again.

If the short list is in alphabetical order, the numbers are in alphabetical order too. Then "cities before Paris" is just "numbers smaller than the number of Paris". If the short list is in the order the cities first came in, the numbers say nothing about order, and you must check each city of the short list by name.

## When it applies

- The column has few distinct values compared with its number of rows, for example countries, status flags, product categories or dates. The scheme pays when $N w$ bits plus the dictionary is much less than the plain column.
- The values are wide, such as strings, so that a code of a few bits replaces many bytes and a comparison of codes replaces a comparison of strings.
- The queries filter, group or join on the column. Equality, grouping and joins need only equal codes for equal values, which every dictionary gives. Range predicates and sorting need an order-preserving dictionary.
- The column is mostly read, or written in batches. A new value either goes at the end of an unordered dictionary or forces a new code assignment in an ordered one.

## The template

The column has values $a_0, \ldots, a_{N-1}$, each NULL or a value of one ordered type. A predicate $\theta$ is one of $=, \ne, <, \le, >, \ge$ with a constant $v$; a comparison with NULL is never true.

```pseudo id=main
ENCODE(a, ordered)
L1  D ← the distinct non-null values of a, sorted if ordered, else in order of first appearance
L2  code(D[x]) ← x + 1 for x ← 0 to |D| - 1, and code(NULL) ← 0
L3  w ← the number of bits of |D|, at least 1
L4  for i ← 0 to N - 1 do write code(a[i]) in the w bits at bit i·w
L5  CODE(i): read the w bits at bit i·w
L6  DECODE(i): c ← CODE(i); if c = 0 then return NULL else return D[c - 1]

SELECT(θ, v)
L7  if the dictionary is ordered and θ is not ≠ then
L8      [s, e) ← the codes of the values x with x θ v, from two binary searches of v in D
L9      return the positions i with s ≤ CODE(i) < e
L10 S ← the empty set
L11 for x ← 0 to |D| - 1 do if D[x] θ v then add x + 1 to S
L12 return the positions i with CODE(i) in S
```

Code 0 is kept for NULL, so a NULL never falls in a code range or in $S$, and the codes go from 0 to $|D|$, which fit in $w$ bits. The binary searches of line L8 find $\ell$, the number of entries less than $v$, and $h$, the number of entries at most $v$; then $<$ gives codes $[1, \ell + 1)$, $\le$ gives $[1, h + 1)$, $=$ gives $[\ell + 1, h + 1)$, $>$ gives $[h + 1, |D| + 1)$ and $\ge$ gives $[\ell + 1, |D| + 1)$. The constant need not be in the dictionary.

**Why it works.** Codes are distinct for distinct values and the $w$-bit fields do not overlap, so DECODE returns the value that was encoded. In a sorted dictionary, $D$ is strictly increasing, so the values that satisfy a range predicate are a contiguous run of $D$, and their codes are an interval. In an unordered dictionary, line L11 tests each value of $D$ directly, so $S$ holds exactly the codes of the values that pass. In both cases a row passes if and only if its code is chosen, and no value is decoded. The proof file has the details.

**Cost.** The column takes $\lceil N w / 8 \rceil$ bytes for the codes plus the dictionary, where $w = \lceil \log_2 (|D| + 1) \rceil$. A selection with an ordered dictionary makes $O(\log d)$ comparisons of values, where $d = |D|$, and then $N$ comparisons of integers. With an unordered dictionary it makes $d$ comparisons of values and $N$ tests of membership in $S$, which are one bit read each if $S$ is a bitmap. Both are $O(N + d)$, but only $O(\log d)$ or $d$ of the steps compare the original values, which may be long strings.

**Example.** Take the column (Paris, Berlin, Paris, Rome, Berlin, Paris, NULL, Athens), with $N = 8$.

| position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| value | Paris | Berlin | Paris | Rome | Berlin | Paris | NULL | Athens |
| ordered code | 3 | 2 | 3 | 4 | 2 | 3 | 0 | 1 |
| unordered code | 1 | 2 | 1 | 3 | 2 | 1 | 0 | 4 |

The ordered dictionary is (Athens, Berlin, Paris, Rome); the unordered one is (Paris, Berlin, Rome, Athens). There are 4 values, so $w = 3$ and the 8 codes take 24 bits, 3 bytes. For "city < Paris", the ordered dictionary has $\ell = 2$ entries less than Paris, so the code range is $[1, 3)$ and the scan returns positions 1, 4 and 7. For "city >= Oslo", Oslo is not in the dictionary, $\ell = 2$, and the code range is $[3, 5)$, the codes of Paris and Rome. The unordered dictionary must compare Paris with all 4 entries, finds that Berlin and Athens pass, and scans for the code set $\{2, 4\}$; it returns the same positions 1, 4 and 7. Note that in the unordered codes Athens has the largest code, 4, so "code < code(Paris)" would give the wrong answer.

## Classic examples

- **C-Store.** Abadi, Madden and Ferreira (2006) put dictionary encoding among the schemes of C-Store and run selections and aggregations directly on the codes. An equality predicate becomes an integer comparison, and a group-by groups on codes and decodes only one value per group.
- **Column-store surveys.** Abadi, Boncz, Harizopoulos, Idreos and Madden (2013) describe dictionary encoding as a basic scheme of modern column stores, together with [run-length encoding](/run-length-encoding/) and [frame of reference encoding](/frame-of-reference-encoding/), and discuss operating on compressed data.
- **Columnar file formats.** Parquet and ORC write a dictionary page per column chunk and store the codes with bit packing and run-length encoding, falling back to plain values when the dictionary grows too large.
- **Joins and grouping.** If two columns share one dictionary, a join on them is a join on codes. A group-by on an encoded column can use the code as an index into an array of $|D| + 1$ aggregates, with no [hash table](/hash-table/).

## Variations

- **Order-preserving or not.** A sorted dictionary allows range predicates, sorting and min and max on codes, but a new value in the middle of the order forces a re-encoding of the column or a code with gaps. An unordered dictionary appends new values at the end, so it is cheap to update, but only equality, grouping and joins work on the codes.
- **Order-preserving with updates.** Binnig, Hildenbrand and Faerber (2009) keep the order for string dictionaries that grow, by leaving gaps between codes and by indexing the dictionary for both encoding and decoding.
- **Compressed dictionaries.** A sorted dictionary of strings can itself be stored with [front coding](/front-coding/), since neighbor entries share prefixes.
- **Local or global dictionaries.** A dictionary per block keeps $|D|$ and $w$ small and lets a [zone map](/zone-map/) skip blocks, but codes of different blocks cannot be compared. A global dictionary allows joins on codes across the whole table.
- **Codes of variable length.** Giving frequent values shorter codes, as [Huffman coding](/huffman-coding/) does, saves more space but loses the fixed width, so the code of row $i$ can no longer be found without decoding the rows before it.

## Pitfalls

- **Range predicates on unordered codes.** Comparing codes of an unordered dictionary with $<$ gives wrong results, as in the example. The plan must know whether the dictionary is ordered.
- **High cardinality.** If almost every value is distinct, the dictionary is as large as the column, and the codes add $N w$ bits. Check $|D|$ against $N$ before choosing the scheme, and fall back to plain storage.
- **Growing code width.** When $|D|$ passes a power of two, $w$ grows by one bit and every code must be rewritten. Reserve a width, or start a new block with a new dictionary.
- **NULL handling.** NULL needs a code of its own, or a separate null bitmap. If NULL gets an ordinary code, a range of codes can include it by mistake.
- **Collation.** An ordered dictionary of strings is sorted by one collation. A query with another collation, or with case-insensitive comparison, cannot use the code order.

## Exercises

1. A column has $N = 10^7$ rows and 3,000 distinct strings of 12 bytes on average. Compute the size of the plain column and of the dictionary-encoded column, with the dictionary.
2. Show how to evaluate "v BETWEEN x AND y" on an ordered dictionary with two binary searches, and how to evaluate "v LIKE 'Ber%'" as a code range.
3. An unordered dictionary receives values in arbitrary order. Give an algorithm that turns it into an ordered dictionary and rewrites the codes, and give its cost in terms of $N$ and $d$.
4. Prove that a group-by on an encoded column with an array of $|D| + 1$ counters gives the same groups as a group-by on the values, with NULL as one group.

## References
