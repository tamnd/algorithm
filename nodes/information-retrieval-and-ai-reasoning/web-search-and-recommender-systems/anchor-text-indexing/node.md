---
tag: FR75WB
kind: technique
slug: anchor-text-indexing
name: Anchor text indexing
aliases:
- anchor text as document description
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Indexes the text of links that point to a page as part of that page, since it often describes the page better than the page itself.
prereqs: [inverted-index, tf-idf, web-crawling]
see_also: [bm25, posting-list, pagerank, hits-algorithm, link-spam, trustrank, focused-crawling, near-duplicate-document-detection]
sources:
  - paper: "Sergey Brin and Lawrence Page, The anatomy of a large-scale hypertextual Web search engine, Computer Networks and ISDN Systems 30(1-7), 107-117, 1998 (Proceedings of the Seventh International World Wide Web Conference)"
    locator: Section 2.2 (anchor text is associated with the page the link points to, because it often describes the page better and because it exists for pages that cannot be indexed, such as images and pages not yet crawled)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 21, Section 21.1.1 (anchor text and the web graph, with the example of a home page that does not contain the words people use for it, and the weighting of anchor terms)
  - paper: "Nick Craswell, David Hawking and Stephen Robertson, Effective site finding using link anchor information, Proceedings of the 24th Annual International ACM SIGIR Conference (SIGIR 2001)"
    locator: the experiments on finding the home page of a site, in which a ranking on anchor text did much better than a ranking on the content of the pages
  - paper: "Nadav Eiron and Kevin S. McCurley, Analysis of anchor text for web search, Proceedings of the 26th Annual International ACM SIGIR Conference (SIGIR 2003)"
    locator: the comparison of anchor text with queries and with titles, and the effect of anchor text on retrieval in an intranet
  - paper: "Stephen Robertson, Hugo Zaragoza and Michael Taylor, Simple BM25 extension to multiple weighted fields, Proceedings of the 13th ACM International Conference on Information and Knowledge Management (CIKM 2004)"
    locator: the combination of fields such as title, body and anchor text by weighting the term frequencies before the saturation of BM25
---

Anchor text indexing adds to each web page the text of the links that point to it, and indexes that text as a part of the page, usually in its own field. The anchor text of a link is the clickable text between the tags of the link, such as "IBM" in a link to the IBM home page. Many authors describe a page in the words that searchers use, while the page itself may not contain those words: a company home page may show only a logo and a menu. Brin and Page made anchor text a core part of Google in 1998, and it remains one of the strongest single signals for queries that look for a named site.

## In plain words

When people link to a page, they usually write a few words that say what the page is. Those words are a short description of the page, written by someone else, and often in the same words a searcher would type. A search engine can collect all the link texts that point to a page and treat them as extra text of that page. Then a page can be found by words that do not appear on it at all. It even works for pages the engine could not read, such as pictures or pages it has not fetched yet. The engine must be careful, because people can write misleading link text on purpose, and because many links say nothing, such as "click here".

## When it applies

Use anchor text when the documents link to each other and the links carry text written by many authors, as on the web, in intranets and in wikis. It helps most for navigational queries, where the user wants one known page, such as the home page of a company. It helps less in collections with few links, with links made by one author, or with links that are only menus. It also needs a crawl or a link database large enough to have many links to each important page.

## The template

1. **Extract.** While parsing each fetched page $u$, for each link from $u$ to a URL $v$, record the triple $(v, a, u)$, where $a$ is the anchor text, often with a few words around the link. Normalize $v$ as in the [crawler](/web-crawling/), and follow redirects to the final URL.
2. **Group by target.** Sort or shuffle the triples by $v$, as in [inverted index construction](/inverted-index/), so that all anchors of a page come together. Pages that were never fetched still get a record, so they can be found by their anchors.
3. **Filter and weigh.** Drop or reduce the weight of links inside the same site, which are mostly navigation. Drop empty and generic anchors, such as "click here" and "home". Count repeated anchors from one site once, or with a cap. Give anchors from trusted or important source pages more weight, for example by their [PageRank](/pagerank/) or [TrustRank](/trustrank/).
4. **Index a field.** Store the remaining anchor terms of $v$ in an anchor field, with a term frequency that counts the anchors that contain the term. Build its [posting lists](/posting-list/) like those of the body.
5. **Combine at query time.** Score each field and combine the scores, or, as in BM25F, add the weighted term frequencies of the fields before the saturation of [BM25](/bm25/), so that a term that appears in both the body and many anchors does not count twice in full.

## Classic examples

**A home page without its own name in words.** Let the page T at ibm.com have the body text "welcome to ibm products services support". The links to T are:

| source | anchor text | kept |
|---|---|---|
| a.org | IBM | yes |
| b.org | IBM | yes |
| c.org | Big Blue | yes |
| d.org | IBM homepage | yes |
| ibm.com | home | no, same site |
| e.org | click here | no, generic |

The anchor field of T then has the term counts ibm 3, big 1, blue 1, homepage 1. The query "big blue" matches nothing in the body of T, but it matches the anchor field. Three of the four kept anchors, all from outside sites, call the page "IBM", a strong sign that T is the page for that name.

**The World Wide Web Worm and Google.** Oliver McBryan's World Wide Web Worm of 1994 indexed the titles and anchor texts of pages. Brin and Page associated the anchor text with the target page in Google, for two reasons that they state: anchors often describe a page better than the page itself, and anchors exist for documents that a text engine cannot index, such as images, programs and pages that have not been crawled.

**Site finding.** Craswell, Hawking and Robertson ran experiments on queries that ask for the home page of a site. A ranking that used only the anchor text found the right page far more often than a ranking on the page content.

**Anchors look like queries.** Eiron and McCurley found that anchor text is short and close to queries in length and in the kind of words it uses, which helps explain why it works so well as a description.

## Variations

- **Text around the link.** Add a window of words before and after the anchor, which helps when the anchor is a generic word or an image. The window adds noise, so give it less weight.
- **Anchor text for images.** The alt text of an image inside a link, and the anchors that point to an image, describe the image for image search.
- **Weights by the number of sites.** Count how many distinct sites use a term in links to a page, not how many links, to blunt repeated links from one site.
- **Anchor text in ranking features.** Learning-to-rank systems use separate features for the match with the anchor field, the number of distinct anchors and the number of linking sites.
- **Focused crawling.** A [focused crawler](/focused-crawling/) can score an unfetched URL by its anchor text before it fetches the page.
- **Hubs and authorities.** Variants of [HITS](/hits-algorithm/) weigh each link by how well its anchor text matches the query.

## Pitfalls

- **Spam.** Anchor text is easy to fake: a [link farm](/link-spam/) can point thousands of links with a chosen phrase at a page. Weigh anchors by the trust of their sources and count each site once.
- **Google bombs.** Many people acting together can make a page rank first for a phrase that it does not contain, only by linking to it with that phrase. The page may not even agree with the phrase.
- **Navigation links.** Menus repeat the same anchors, such as "home" and "next", on every page of a site, and they can flood the anchor field. Treat links inside a site apart from links between sites.
- **Duplicates.** Mirrors and copied pages repeat the same links. Remove [near duplicates](/near-duplicate-document-detection/) before counting anchors.
- **Redirects and URL forms.** Links to http://x.org, http://www.x.org/ and http://x.org/index.html usually point to the same page. Without normalization, the anchors split over several URLs.
- **Stale anchors.** Anchors can describe what a page used to be, after the page changed or the domain got a new owner.

## Exercises

1. In the example above, a sixth outside site links to T with the anchor "IBM research". Give the new term counts of the anchor field, and say which counts change if the rule counts each term once per site and c.org adds a second link with the anchor "Big Blue".
2. Explain why anchor text helps a page that the crawler has not fetched yet, and what the search engine can show for such a page in its result list.
3. A page gets 500 links with the anchor "cheap flights" from 500 pages of one host. Describe two filters of the template that limit their effect, and what each one leaves.
4. Show by a small example that adding the anchor field score to the body score can rank a page with a term in both fields higher than BM25F does, and explain which ranking you prefer for a navigational query.

## References
