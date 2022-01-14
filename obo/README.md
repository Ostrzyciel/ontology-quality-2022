## Ontologies
The following OBO Foundry ontologies were used in the investigation: AEO, AGRO, APOLLO-SV, BFO, BTO, CARO, CHEBI, CL, DOID, DRON, EHDAA2, ENVO, FOBI, FoodOn, GAZ, GO, HP, IAO, MP, NCBITaxon, OBI, PATO, PCO, PECO, PO, RO, SYMP, Uberon, UO, XCO. They are **not** included here, due to their excessive size. You can find them on https://obofoundry.org/

We downloaded almost all the ontologies used in the investigation on 4th January 2022, with the exception of FOBI, which failed to load. Instead, we used [this older version](https://github.com/pcastellanoescuder/FoodBiomarkerOntology/blob/28c837225944b7bf922517f1865f8eb2ffca043c/fobi.owl).

Most ontologies are available in the RDF/XML format, but some need to be converted to it first. CARO is in OWL/XML and FOBI is in the OWL functional syntax format.

### Loading ontologies
In the experiments, the scripts expect 31 namespaces to be created in a triple store instance. Of them, 30 correspond to single ontologies, with names like `obo-<ontology>` where `<ontology>` is the ontology's abbreviation in lowercase. The full list of all these abbreviations can be found in the `ontos.txt` file. The last namespace with the name `obo-ontos` should contain all ontologies loaded together. Caution: this results in a KB with ~40 million triples.

Given that some ontologies in this collection contain invalid URIs, you may encounter loading issues with some of the more restrictive triple stores. We did not have any such issues with Blazegraph.

## Experiments

The following subsections explain how to reproduce the OBO-related experiments presented in the paper.

### 1: rarely used properties

- Run `props.rq` against `obo-ontos` namespace. The results are saved in `results/props.json`.
- *Optional:* `props_analysis.ipynb` demonstrates the long tail-like distribution of property counts.
- The results of the query were then manually reviewed, and the results were saved to `results/props_review.yaml`.
- `props_issues.ipynb` summarizes the issues and identifies the source ontology of all issue occurrences.

### 2: property value type mismatch

- `otypes_get.ipynb` in cells 1–6 queries the ontologies for all properties and their value types. The results are saved in `results/otypes.json`.
- The results were then manually reviewed and compared to ontology documentation, OWL standard, etc. The initial set of suspected properties was saved by the reviewer in `results/otypes_review.yaml`.
- `otypes_get.ipynb` in cells 7–8 loads the initial review results and joins it with the previously obtained table. The result is saved in `results/otypes_invalid.json`.
- This was then used to construct SPARQL queries that counted the exact number of issues per property. The queries can be found in the `sparql_otype` directory. Note that queries for some properties are missing, for cases where we could not decide which is the preferred/correct form. The results of running each query against the `obo-ontos` namespace can be found in `results/otypes_invalid`.
- `otypes_analysis.ipynb` runs the issue counting queries and summarizes the results.

### 3: inconsistent cross-ontology references

- The results in this experiment were very large, thus they were compressed. Please, uncompress the `results.tar.gz` file first.
- `xrefs_skos.rq` retrieves all cross-ontology references made using SKOS properties. They are saved to `results/xrefs_skos.json`
- `xrefs_oboInOwl.rq` is the general query used to retrieve the set of all oboInOwl cross-ontology references. As the result set is very large (~4 million triples), it is advisable to execute this query using the LIMIT and OFFSET clauses. The results are saved to `results/xrefs_altId.json` for `oboInOwl:hasAlternativeId`. For `oboInOwl:hasDbXref` the results are in `results/xrefs_dbxref_*.json` files.
- `xrefs_bnodes.rq` retrieves only blank node-valued cross-references. The OPTIONAL clause is meant to find any additional properties attached to these blank nodes. However, there are none.
- `data/ontologies.yml` contains the OBO Foundry registry, while `data/bioregisty.yml` is the Bioregistry. Both files have their sources and licenses listed in a comment at the beginning of the file.
- `xrefs.ipynb` analyzes the cross-references and saves the problematic triples to `results/xrefs_unknown_id.json` and `xrefs_uri.json`.
- `get_per_ont.ipynb` determines the source ontology of the problematic references.







