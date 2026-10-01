# Job Description Mapping: Google Data Specialist (R00336594)

**Source reviewed:** Accenture, Google Data Specialist, Job No. R00336594.  
**Review date:** 2026-09-30.  
**Source:** https://www.accenture.com/us-en/careers/jobdetails?id=R00336594_en&title=Google+Data+Specialist

This mapping describes what the portfolio repository demonstrates. It does **not** claim that billing-gated services were executed, that the project was client work, or that portfolio evidence substitutes for employment experience.

## 1. Hands-On Technical Delivery

| Job responsibility | Repository evidence | Status |
|---|---|---|
| Build data pipelines / ETL / ELT | Seeded Python generator; BigQuery batch load; staging and semantic-layer SQL | **Demonstrated** |
| BigQuery data modeling | Raw → staging → semantic views; warehouse, inventory, and shipment structures | **Demonstrated** |
| Performance tuning / query optimization | Dry-run byte checks, column pruning, clustering benchmark | **Demonstrated** |
| Batch ingestion | Local CSV generation and BigQuery batch load; optional GCS batch path | **Demonstrated / billing-gated alternative** |
| Streaming ingestion | Pub/Sub micro-batch pattern documented in notebook | **Design only; billing-gated** |
| Dataflow / Dataproc | Production architecture paths documented | **Design only; not executed** |
| Looker / Looker Studio | Final two-source semantic layer, implementation guide, and static reference build | **Demonstrated / live report external** |

## 2. Agentic AI & ML Solution Development

| Job responsibility | Repository evidence | Status |
|---|---|---|
| ML model development | BigQuery ML logistic-regression delay classifier | **Demonstrated** |
| Model testing / validation | ROC AUC evaluation, majority-class baseline, promotion gate | **Demonstrated** |
| MLOps processes | `ml_model_metrics` history and promotion decision documented in notebook | **Demonstrated** |
| Vertex AI / Gemini | Billing-gated experiment paths for AI generation, embeddings, and related workflows | **Design only; not executed** |
| Embeddings / RAG experimentation | Billing-gated notebook section documents the experiment path | **Design only; not executed** |
| Documentation / model card | Model card and validation narrative included in notebook | **Demonstrated** |

## 3. Requirements Gathering & Delivery Traceability

| Job responsibility | Repository evidence | Status |
|---|---|---|
| Translate requirements into technical tasks | Requirements traceability and delivery log in notebook | **Demonstrated as a self-directed simulation** |
| Communicate progress / blockers / assumptions | Notebook status notes, validation log, environment boundaries, and project disclaimer | **Demonstrated as documentation** |
| Client workshops / actual client collaboration | No real client engagement is claimed | **Not claimed** |

## 4. Data Governance, Quality & Security

| Job responsibility | Repository evidence | Status |
|---|---|---|
| Metadata management | BigQuery table/column descriptions and labels | **Demonstrated** |
| Data quality | 15-check `dq_check_results` suite | **Demonstrated** |
| Lineage | `INFORMATION_SCHEMA` lineage queries and source-to-view documentation | **Demonstrated** |
| IAM / least privilege | Access review and least-privilege design | **Demonstrated as design / review** |
| Validation / monitoring | DQ results, reconciliation checks, statistical diagnostics, ML evaluation | **Demonstrated** |
| Dataplex | Dataplex data-quality path documented | **Design only; not executed** |

## 5. Continuous Learning & Team Support

| Job responsibility | Repository evidence | Status |
|---|---|---|
| Reusable components | Parameterized synthetic generator, SQL scripts, DQ suite, ML workflow, dashboard specification | **Demonstrated** |
| Documentation / internal accelerators | README, executive summary, validation log, dashboard guide, JD mapping, reference build | **Demonstrated** |
| GCP / AI release awareness | Notebook release-note references and explicit billing-gated syntax revalidation note | **Demonstrated as process** |
| Modern engineering practices | GitHub-ready repository structure, deterministic validation, disclaimers, reproducibility and QA | **Demonstrated** |

## 6. Qualification / bonus-skill evidence represented by this project

| Job requirement / bonus area | Portfolio evidence | Boundary |
|---|---|---|
| SQL | GoogleSQL transformation, DQ, ML, and analytical queries | Project evidence only |
| Python | Synthetic generation, validation, statistical analysis | Project evidence only |
| Data modeling / pipelines | BigQuery raw → staging → semantic architecture | Project evidence only |
| GCP | BigQuery execution plus documented GCP architecture paths | Do not represent billing-gated services as executed |
| Looker / Looker Studio | Final Control Tower specification and reference build | Live report remains external |
| AI/ML | BigQuery ML and gated Gemini/embedding/RAG experiment design | Gated AI services not executed |
| Git / repository practices | Structured GitHub transfer package with documentation and scripts | Repository artifact |

## Evidence legend

- **Demonstrated:** implemented in the repository and/or represented in the supplied validation record.
- **Design only / billing-gated:** code or architecture is provided, but execution is intentionally not claimed in the no-billing environment.
- **Not claimed:** the repository deliberately avoids representing unsupported real-world experience.
