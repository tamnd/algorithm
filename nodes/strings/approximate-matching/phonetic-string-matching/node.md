---
tag: XFBS7P
kind: problem
slug: phonetic-string-matching
name: Phonetic string matching
aliases:
- sound-alike matching
area: strings/approximate-matching
level: intro
summary: Match strings by how they sound rather than how they are spelled.
prereqs: [hash-function]
see_also: [soundex, metaphone, edit-distance, jaro-winkler-distance, approximate-dictionary-lookup, approximate-string-matching, equivalence-relation]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Chapter 6, the introduction to searching (Soundex as a search on a transformed key)
  - paper: "Justin Zobel and Philip Dart, Phonetic string matching: lessons from information retrieval, Proceedings of the 19th ACM SIGIR Conference, 1996, 166-172"
    locator: the comparison of phonetic codes and edit distances on a large set of names, and the Editex distance
  - paper: "Lawrence Philips, Hanging on the Metaphone, Computer Language 7(12), December 1990"
    locator: the Metaphone rules for English spelling
  - paper: doi:10.1145/146370.146380
    title: Karen Kukich, Techniques for automatically correcting words in text, ACM Computing Surveys 24(4), 1992
    locator: pages 377 to 439 (phonetic keys and similarity keys for the correction of isolated words)
---

Phonetic string matching is the problem of finding the strings that sound like a query string, even when they are spelt differently. The usual method maps each string to a phonetic key, such as a [Soundex](/soundex/) or a [Metaphone](/metaphone/) code, and calls two strings a match when their keys are equal. A second method compares strings with a distance whose costs depend on how letters sound. The main use is the search of names in records, where one name has many spellings.

## In plain words

A clerk hears a name on the phone and types it. The same person was typed differently in an old record. A search for the exact spelling fails, even though the two names sound the same.

Phonetic matching fixes this with a rule that turns each name into a short sound label. Letters that sound alike get the same symbol, and silent letters are dropped. Two names with the same label count as a match.

The labels are stored next to the names. A search computes the label of the query and returns all names with that label. This is fast, but labels are rough: some names that sound alike get different labels, and some unrelated names share a label.

## Definition

Let $\Sigma$ be an [alphabet](/alphabet/) of letters, and let $\varphi : \Sigma^* \to K$ be a phonetic key function into a set $K$ of codes. Two strings $x$ and $y$ match when $\varphi(x) = \varphi(y)$. This relation is an [equivalence relation](/equivalence-relation/), because it is equality of keys.

The search problem: given a list $D = (x_0, \ldots, x_{N-1})$ of strings and a query $q$, report the 0-based indices $\{\, t : \varphi(x_t) = \varphi(q) \,\}$.

The goal of a key function is a property that has no exact definition: $\varphi(x) = \varphi(y)$ should hold when the two strings are pronounced alike by speakers of the language, and should fail otherwise. So a key function is judged by its precision (the share of the reported strings that are true matches) and its recall (the share of the true matches that it reports) on a test set.

## Variants

- **Key-based matching.** One key for each string, as above. Examples are [Soundex](/soundex/), NYSIIS and [Metaphone](/metaphone/).
- **Several keys.** Double Metaphone gives each word a primary and an alternate key, and two words match when one key of each agrees.
- **Phonetic distance.** Instead of keys, use a distance whose substitution cost is small for letters of the same sound group. Zobel and Dart define Editex, an [edit distance](/edit-distance/) of this kind. Then the problem is a ranking or a threshold search.
- **Pronunciation first.** Convert each string to phonemes with a pronunciation dictionary or a set of rules, then compare the phoneme strings with an edit distance.
- **Mixed search.** Use a key to collect candidates, then rank them by an edit distance or the [Jaro-Winkler distance](/jaro-winkler-distance/).

## Examples

| names | Soundex | Metaphone | sound alike? |
|---|---|---|---|
| Robert, Rupert | R163, R163 | RBRT, RPRT | no, but Soundex matches them |
| Catherine, Kathryn | C365, K365 | K0RN, K0RN | yes, Metaphone matches |
| Smith, Smyth | S530, S530 | SM0, SM0 | yes, both match |
| Philips, Filips | P412, F412 | FLPS, FLPS | yes, Metaphone matches |
| Knight, Night | K523, N230 | NT, NT | yes, Metaphone matches |
| Jon, John, Jean, Gene | J500, J500, J500, G500 | JN for each | partly |
| Thompson, Tomson | T512, T525 | 0MPSN, TMSN | yes, neither matches |
| Leigh, Lee | L200, L000 | LK, L | yes, neither matches |

The table shows both kinds of error. A false match: Soundex puts Robert and Rupert together, and Metaphone puts Jean and Gene with John. A missed match: Thompson and Tomson, and Leigh and Lee, sound alike but get different keys in both codes.

## Known algorithms

| method | idea | cost of a key |
|---|---|---|
| [Soundex](/soundex/) | first letter and three digits for six consonant groups | $\Theta(L)$ |
| NYSIIS | rules on groups of letters, made for American names | $\Theta(L)$ |
| [Metaphone](/metaphone/) | context rules for English spelling | $\Theta(L)$ |
| Double Metaphone | two keys, rules for names of many origins | $\Theta(L)$ |
| Editex | edit distance with costs by sound groups | $\Theta(L_1 L_2)$ for a pair |

Here $L$ is the length of a string. With the keys of $D$ stored in a hash table, a query costs the time of one key plus the number of strings with that key, in expectation. A distance-based method compares the query with each candidate, or uses a structure for [approximate dictionary lookup](/approximate-dictionary-lookup/).

## Bounds

A key function reads each letter, so a key costs $\Omega(L)$ time in the worst case, and the methods above reach $O(L)$. A search with stored keys and a hash table takes $O(L + r)$ expected time for a query with $r$ matches. There is no lower bound on the error rate, because the true relation "sounds alike" has no formal definition. Equality of keys is transitive. So if three names $a$, $b$ and $c$ exist where $a$ sounds like $b$ and $b$ sounds like $c$, but $a$ does not sound like $c$, each key function errs on one of the three pairs.

## Reductions

- **To exact search.** Key-based matching is exact search on the keys: build a [hash table](/hash-function/) or a sorted list of keys, then look up the key of the query.
- **To approximate dictionary lookup.** A phonetic distance turns the problem into [approximate dictionary lookup](/approximate-dictionary-lookup/) under that distance.
- **To edit distance on phonemes.** With a pronunciation step, the problem becomes [edit distance](/edit-distance/) on phoneme strings.

## Applications

- **Genealogy and archives.** Census and immigration records were indexed by Soundex, so that a searcher finds a family under all its spellings.
- **Record linkage.** Systems that link records of the same person across databases compare names by phonetic keys and string distances.
- **Spelling suggestions.** A spelling checker can suggest words with the same phonetic key as a misspelt word.
- **Search of names.** Phone directories, police records and customer databases search names by sound.

## References
