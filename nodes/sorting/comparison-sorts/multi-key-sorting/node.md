---
tag: SX2GHX
kind: technique
slug: multi-key-sorting
name: Multi-key sorting
aliases:
- Items with multiple keys
area: sorting/comparison-sorts
level: intro
summary: Technique for ordering records by several fields in turn, using a stable sort or a comparator that breaks ties by successive keys.
prereqs: [stable-sort, lexicographic-order, comparator]
see_also: [radix-sort, stable-sort, lexicographic-order, comparator, merge-sort, timsort, multikey-quicksort, counting-sort]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.5, Applications (Comparators, Sorting with multiple keys, and Stability)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.3, Radix sort (sorting on the least significant digit first with a stable sort, and Lemma 8.3)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Chapter 5, Sorting (the introduction, on keys made of several parts), and Section 5.2.5, Sorting by distribution (least significant digit first)
  - paper: "Python Software Foundation, Sorting Techniques (the Sorting HOWTO), Python documentation"
    locator: the sections Sort Stability and Complex Sorts, and Key Functions
---

Multi-key sorting puts records in order by several fields: first by a primary key, then, among records with equal primary keys, by a secondary key, and so on. This is the [lexicographic order](/lexicographic-order/) on the tuple of keys. There are two standard ways. One sort with a [comparator](/comparator/) that compares the keys in turn and stops at the first difference works with any sorting algorithm. A sequence of [stable sorts](/stable-sort/), one per key, from the least important key to the most important, gives the same result and lets each pass use its own order. The second way, with counting sort as the stable pass, is [LSD radix sort](/radix-sort/).

## In plain words

A list of people must be sorted by city, and the people in the same city by age, and people of the same age by name. The city decides first. Only when two people live in the same city does the age matter, and only when the age is also the same does the name matter.

There are two ways to do this. You can compare two people by city first, and look at the age only on a tie, and at the name only on a second tie; one sort with this rule is enough. Or you can sort the list three times: first by name, then by age, then by city, each time with a sort that keeps the order of ties. The last sort decides the most, and the earlier sorts survive inside its ties.

## When it applies

- **The order of the records is defined by several fields,** with a fixed priority among them: last name then first name, date then time, department then salary.
- **Some fields are in reverse order.** For example, sort by score from high to low, and by name from A to Z among equal scores.
- **A stable sort is available,** such as [merge sort](/merge-sort/) or [Timsort](/timsort/), or a stable linear-time sort for small keys, such as [counting sort](/counting-sort/).
- **The user sorts a table by clicking columns.** Each click is a stable sort by one column, so the result of the earlier clicks survives inside the ties of the last one.

## The template

Let the keys be $k_1, \ldots, k_d$, with $k_1$ the most important. The goal is the order in which $x$ comes before $y$ when $(k_1(x), \ldots, k_d(x))$ is less than $(k_1(y), \ldots, k_d(y))$ in lexicographic order.

```pseudo id=main
COMPARE(x, y)                              ▷ less, equal or greater
L1  for i ← 1 to d do
L2      if kᵢ(x) < kᵢ(y) then return less
L3      if kᵢ(y) < kᵢ(x) then return greater
L4  return equal

MULTI-KEY-SORT(A)                          ▷ the method of passes
L5  for i ← d down to 1 do
L6      STABLE-SORT(A, by kᵢ)              ▷ hole: any stable sort
```

**One sort with a comparator.** Lines L1 to L4 compare the keys in priority order and stop at the first key that differs. Any correct sort that uses COMPARE puts the records in lexicographic order of their keys. The sort need not be stable, unless records with all keys equal must keep their order.

**Passes of stable sorts.** Lines L5 and L6 sort by the least important key first, and by $k_1$ last. The method needs each pass to be stable. The claim, by induction on the passes, is: after the passes for $k_d, k_{d-1}, \ldots, k_i$, the array is in lexicographic order of $(k_i, \ldots, k_d)$. After the pass for $k_d$ this is the plain order by $k_d$. The pass for $k_{i-1}$ sorts by $k_{i-1}$; records with different $k_{i-1}$ are now in the right order, and records with equal $k_{i-1}$ keep their previous order, which by the claim is the order of $(k_i, \ldots, k_d)$. So they are in the order of $(k_{i-1}, \ldots, k_d)$. CLRS proves the same claim for radix sort in Lemma 8.3.

**A key per field in another direction.** For a key that must go from high to low, reverse its test in COMPARE, or use a stable sort in reverse order for its pass. A stable sort in reverse order keeps equal items in input order; reversing the output of an ascending stable sort does not, because it also reverses the ties.

**Cost.** With a comparator, one sort makes $O(n \log n)$ comparisons, and each comparison looks at up to $d$ keys, so the time is $O(d\, n \log n)$ in the worst case, and much less when the first key usually decides. With passes, there are $d$ sorts, each $O(n \log n)$ with a comparison sort, or $O(n + K)$ with counting sort on keys in a range of $K$ values. The second form is LSD radix sort, with $O(d(n + K))$ time.

## Classic examples

**Records by three fields.** Sort (Eve, Sales, 31), (Bob, IT, 25), (Ann, Sales, 25), (Dan, IT, 31), (Cid, Sales, 25) by department, then age, then name.

| step | the order |
|---|---|
| a stable sort by name | Ann, Bob, Cid, Dan, Eve |
| then a stable sort by age | Ann 25, Bob 25, Cid 25, Dan 31, Eve 31 |
| then a stable sort by department | Bob IT 25, Dan IT 31, Ann Sales 25, Cid Sales 25, Eve Sales 31 |

One sort with COMPARE on (department, age, name) gives the same order. With an unstable sort for the last pass, the order of Ann and Cid inside (Sales, 25) could be lost.

- **Dates.** Sort dates by (year, month, day). As a comparator, compare the years first. As passes, sort by day, then by month, then by year, each pass by counting sort with at most 31, 12 and a few hundred values.
- **Strings.** Lexicographic order on strings is multi-key order with one key per character position. [Multikey quicksort](/multikey-quicksort/) and MSD radix sort sort from the first character; LSD radix sort sorts fixed-length strings from the last character.
- **Python.** Python's sort is stable, and its key may be a tuple, so `sorted(rows, key=lambda r: (r.dept, r.age, r.name))` is the comparator method. For mixed directions, the Sorting HOWTO sorts in passes: `rows.sort(key=name)` and then `rows.sort(key=score, reverse=True)`.
- **Java and C++.** Java's `Comparator.comparing(f).thenComparing(g)` builds COMPARE from the keys. In C++, `std::tie(x.a, x.b) < std::tie(y.a, y.b)` compares tuples in lexicographic order, and `std::stable_sort` gives the passes.
- **Spreadsheets.** A sort dialog with "sort by, then by" fields builds the comparator; clicking column headers one after another relies on a stable sort for the passes.

## Variations

- **Most significant key first.** Sort by $k_1$, then sort each group of equal $k_1$ by $k_2$, and so on. This is MSD radix sort. It needs no stability, but it needs to find the groups. It wins when $k_1$ splits the records into many small groups.
- **A combined key.** Map the tuple of keys to one key with the same order, for example $\text{year} \cdot 10^4 + \text{month} \cdot 100 + \text{day}$ for dates, or a string of fixed-width fields. Then one sort by the combined key is enough.
- **Decorate, sort, undecorate.** Compute the tuple of keys once per record, sort the pairs (tuple, record), and drop the tuples. This avoids computing costly keys in each comparison.
- **Partial keys.** In some orders, a later key matters only for some values of an earlier one, for example sort by type, and only items of one type by size. A comparator can express this; passes cannot without care.

## Pitfalls

- **Passes in the wrong order.** The most important key must be sorted last. Sorting by $k_1$ first and $k_2$ second gives the order of $(k_2, k_1)$.
- **An unstable pass.** One unstable pass can break the order that the earlier passes made. [Quicksort](/quicksort/), [heapsort](/heapsort/) and [selection sort](/selection-sort/) are not stable, and C's `qsort` and C++'s `std::sort` are not guaranteed to be.
- **Reversing a stable sort.** To sort one key from high to low, do not sort ascending and then reverse the array: this also reverses the ties. Use a descending comparator or a sort that is stable in descending order.
- **Negating keys.** The trick of sorting by $-k$ for a descending key fails for strings, and for integers it can overflow at the least value of a fixed-width type.
- **An inconsistent comparator.** COMPARE must be a total order. A comparator that breaks ties by a field in some cases and not in others, or that treats missing values differently on the two sides, can make a sort loop, crash or give a wrong order.
- **Floating-point keys.** A NaN key is neither less nor greater than any value, so it breaks the total order. Decide where NaN goes and test for it first.

## Exercises

1. Sort the records of the example by age from high to low, then by name, using passes of a stable sort. Which passes are needed, and in which order?
2. Prove that COMPARE defines a total order on the records when each key has a total order, with ties allowed as "equal".
3. Show by an example of three records that the method of passes fails if the last pass is a selection sort.
4. A table has $n = 10^6$ rows and $d = 3$ keys with $K = 100$ values each. Compare the cost of one comparison sort with COMPARE and of three passes of counting sort.
5. Show that sorting by $k_1$ and then sorting each group by $k_2$ (most significant first) gives the same result as the passes, and that it needs no stable sort.

## References
