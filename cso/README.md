## Ontology

We used the Computer Science Ontology 3.3, you can download it from [here](https://cso.kmi.open.ac.uk/downloads). The CSO data model (upper ontology) can be found [here](https://cso.kmi.open.ac.uk/schema/cso). As the upper ontology is not versioned, we include its copy here, in the `cso_upper.ttl` file.

## Experiments

The following subsections explain how to reproduce the CSO-related experiments presented in the paper.

The experiments should be performed independently, always on a fresh copy of CSO.

### 1: synonym structure transformation

- Load the CSO in the triple store.
- Execute the SPARQL queries in order. This will yield a graph where topic clusters are grouped into a single entity.

### 2: externally inconsistent references

- Load the CSO in the triple store.
- `all_dbpedia_uris.rq` retrieves a list of all unique URIs in DBpedia that are referenced from within CSO. The results are saved to `results/all_dbpedia_uris.txt`
- Next, you will need to download the wikilinks subset of DBpedia. You can find it [here](https://databus.dbpedia.org/dbpedia/generic/wikilinks/). We used the English 2021.09.01 version ([direct link](https://databus.dbpedia.org/dbpedia/generic/wikilinks/2021.09.01/wikilinks_lang=en.ttl.bz2)). The file is ~1.7 GB when compressed.
- While decompressing the archive, filter out only those lines that are useful to us, i.e., are referenced from CSO. On Linux, you could use a command like: ``bzip2 -dc wikilinks.ttl.bz2 | grep -F "`cat all_dbpedia_uris.txt`" > cs_wikilinks.ttl``. The resulting Turtle file should be no bigger than 200 MB.
- Insert the obtained DBpedia wikilinks subset into the triple store.
- To ease querying later, `add_dbp_cso_tag.rq`. inserts a temporary property for DBpedia URIs that are referenced from the CSO.
- `count_mutual_links.rq` retrieves connections between DBpedia entities referenced from CSO. The results are saved in `results/mutual_links.json`.
- `links_cc.ipynb` performs network analysis on the retrieved results and saves a collection of suspects to `results/final_suspects.json`.
- `item_compare/app.py` is a very simple Dash app meant to speed up the review process. It saves the progress automatically to `results/review_results.json` and remembers where you left off, so if you want to play with it, you will need to move that results file somewhere.
- `summary.ipynb` summarizes the review results.

### 3: missing references to corresponding KBs

- Load the CSO in the triple store.
- `missing_wd.rq` identifies CSO topics where either a Wikidata or a DBpedia reference is missing. The results are saved to `results/missing_refs.tsv`.
- `missing_wd_unique.rq` retrieves a list of unique DBpedia URIs for which there are missing Wikidata references. The result is pasted into `get_missing_wd_links.rq` (the VALUES clause).
- Run `get_missing_wd_links.rq` on the public DBpedia endpoint. This will yield the missing Wikidata references, which are saved to `results/dbpedia_result.csv`.
- `make_ttl.ipynb` transforms the results and generates a Turtle patch, which is saved to `results/suggestion.ttl`.

### 4: logically invalid alignments

- Load the CSO in the triple store.
- `sameas_pairs.rq` retrieves all triples with the `owl:sameAs` property. The result is saved to `results/sameAs_pairs.tsv`.
- `sameas_clusters.ipynb` reads this information and infers the additional `owl:sameAs` relations, using its  reflexive, symmetrical, and transitive characteristics. The resulting additional triples are saved to `results/sameAs_inferred.ttl`.
- Insert `results/sameAs_inferred.ttl` into the triple store.
- `logic_violation.rq` looks for pairs of topics that are marked as identical, but are not connected using the `cso:relatedEquivalent` or `cso:preferentialEquivalent` properties. The results are saved to `results/results_violation.csv`.
- `stats.ipynb` summarizes the results and writes the list of unique pairs exhibiting the issue to `results/unique_pairs.tsv`.

### 5: intra-cluster alignment inconsistencies

- Load the CSO in the triple store.
- `related_eq_pairs.rq` finds CSO topic clusters. The result is saved to `results/related_eq.tsv`.
- `all_dbpedia_refs.rq` retrieves all references to DBpedia. The result is saved to `results/dbpedia_refs.tsv`.
- `consistency.ipynb` performs the consistency checks and exports the results. `results/missing_references.json` indicates which references are missing and `results/more_than_one_reference.json` lists topic clusters with more than one unique DBpedia reference.
- For the former (missing references) `make_ttl.ipynb` generates a Turtle patch file. The result is saved to `results/suggestion.ttl`.

We acknowledge that this experiment only concerns DBpedia entities and applying the provided patch will introduce inconsistencies similar to those observed in experiment 3. Additional work would be required to extend the patch to all corresponding knowledge bases.

### 6: term conflation

- Load the CSO in the triple store.
- `get_clusters.tsv` retrieves all `cso:*Equivalent` triples with the corresponding labels. The results are saved to `results/clusters.tsv`.
- `encodings.ipynb` encodes the labels and saves the encodings to `temp/topics.pkl.bz2`.
    - The Pickle files are **not** included in this repository due to size and security concerns.
- `cluster_sim.ipynb` rearranges the data and computes the similarity matrices between topics in clusters. The results are saved to `temp/cluster_data.pkl.bz2` and `temp/clusters.pkl.bz2`.
- `suspected_clusters.ipynb` computes similarity statistics and establishes the set of clusters that are suspected to be inconsistent. The result is saved in `results/final_suspects.csv`.
- `prepare_for_experts.ipynb` takes this data, shuffles it, and outputs in a form suitable for sharing with reviewers (`to_review` directory).
- The files in the `to_review` directory were then imported into Excel and given to reviewers for them to fill out. Their answers can be found in the `review_results` directory.
- `summarize_reviews.ipynb` calculates reviewer's scores distributions and agreement metrics. Additionally, a summary of all reviews is written to `results/cluster_reviews.csv`.

### Summary

- Load the CSO in the triple store.
- `all_topics.rq` retrieves a list of all CSO topics. The result is saved to `results/all_topics.tsv`.
- `summary.ipynb` aggregates the issues observed in all experiments and summarizes them.
