# qmodel_compilation

This repository contains the compiled analysis pipeline and results for a quantitative study on the relationship between commit graph structure, code churn, and software process outcomes, with a focus on issues, pull requests, and defect-introducing commits.

The implementation supports three research questions (RQ1–RQ3) and applies graph-based metrics, churn metrics, and statistical / machine-learning models to real-world GitHub projects (e.g., Ansible, Facebook).

---

## Research Questions

### RQ1 — Commit DAG vs. Issue Resolution

To what extent are structural properties of the commit DAG associated with issue-level outcomes?

This research question evaluates correlations between commit-graph metrics and issue resolution time using Pearson and Spearman correlation analysis.

Implemented in:
- `DagToIssuesPrPearsonRQ1`

---

### RQ2 — Commit DAG vs. Pull Request Characteristics

How do commit DAG characteristics relate to pull-request properties?

This research question analyzes correlations between commit-graph metrics and pull-request–level characteristics.

Implemented in:
- `DagToPrrPearsonRQ2`

---

### RQ3 — Defect-Side Explanation of Issue Resolution Time

To what extent can graph and churn metrics of bug-introducing commits explain issue resolution time?

This research question models issue resolution time as a function of graph-based and churn-based metrics extracted from SZZ-identified bug-introducing commits that belong to pull requests.

Implemented in:
- `IssueDefectRQ3Models`

---

## Data Model

### Unit of Analysis

- One row corresponds to one closed issue
- Only issues linked to SZZ-identified bug-introducing commits are included
- Only bug-introducing commits with `pr_id > 0` (i.e., belonging to a pull request) are used

---

### Target Variable

- `log_issue_resolution_hours`

The target is defined as:
log_issue_resolution_hours = log(1 + issue_resolution_hours)


The logarithmic transformation mitigates heavy-tailed distributions in issue resolution time.

---

## Features

All features describe properties of bug-introducing commits and are prefixed with `bic_`.

### Graph-Based Metrics

- `bic_num_commits`
- `bic_avg_depth_diff`
- `bic_max_depth_diff`
- `bic_avg_fp_distance`
- `bic_max_fp_distance`
- `bic_avg_upstream_heads`
- `bic_max_upstream_heads`
- `bic_avg_in_degree`
- `bic_avg_out_degree`
- `bic_avg_branches`
- `bic_avg_average_degree`
- `bic_avg_days_since_merge`
- `bic_max_days_since_merge`

---

### Churn Metrics

- `bic_total_additions`
- `bic_total_deletions`
- `bic_total_changes`
- `bic_avg_changes_per_file`
- `bic_max_changes_in_file`
- `bic_num_files_changed`
- `bic_change_density_per_file`
- `bic_avg_branch_commit_rate`

---

## Methods

### Correlation Analysis (RQ1, RQ2)

- Pearson correlation
- Spearman rank correlation (robustness check)
- Results visualized using correlation heatmaps

---

### Linear Regression (RQ3)

- Ordinary Least Squares (OLS)
- Features are standardized (z-score normalization)
- Intercept included
- Coefficients interpreted as standardized effects
- Statistical significance assessed using p-values

Outputs include:
- Regression coefficients
- Significance annotations
- Residual distributions
- Actual vs. predicted plots

---

### Random Forest Regression (RQ3)

- Non-linear regression baseline
- 80/20 train–validation split
- Metrics:
  - R² (explained variance)
  - Mean Squared Error (MSE)

Outputs include:
- Feature importance rankings
- Actual vs. predicted plots
- Residual histograms

---

## Partial Results (Illustrative)

- Commit graph depth metrics (e.g., `bic_max_depth_diff`) consistently show the strongest association with issue resolution time.
- Churn-related metrics exhibit moderate monotonic relationships, more visible under Spearman correlation.
- Linear regression and random forest models yield consistent rankings of influential features.
- Models explain a non-trivial but incomplete fraction of the variance in issue resolution time.

---

## Code Structure
```aiignore
 tree            
        
.
├── README.md
├── __init__.py
├── clients
│            ├── __init__.py
│            └── proven
│                ├── __init__.py
│                ├── bid_to_issues_pca.py
│                ├── bid_to_issues_pr_anova.py
│                ├── bid_to_issues_regression.py
│                ├── chorn_to_issues_pr_anova.py
│                ├── chorn_to_issues_pr_pca.py
│                ├── chorn_to_issues_pr_pearson.py
│                ├── dag_to_issues_pr_anova.py
│                ├── dag_to_issues_pr_pca.py
│                ├── dag_to_issues_pr_pearson.py
│                ├── dag_to_issues_regression_analysis.py
│                ├── lr
│                │            ├── RpbustAnalysis.py
│                │            └── lr_file_change_complexity_vs_issue_pr_time.py
│                ├── ps
│                │            ├── ps_dag_to_issues.py
│                │            ├── ps_dev_workload_vs_issues_time.py
│                │            ├── ps_dev_workload_vs_pr_time.py
│                │            ├── ps_developer_inactivity_to_issues_pr.py
│                │            └── ps_file_change_complexity_vs_issue_pr_time.py
│                ├── rf
│                │            ├── rf_developer_inactivity_to_issues_pr.py
│                │            ├── rf_file_change_complexity_vs_issue_pr_time.py
│                │            └── rf_ps_dag_to_issues.py
│                ├── rq1_issues
│                │            ├── issue_defect_graph_ci_metrics.py
│                │            └── issue_fix_graph_ci_metrics.py
│                ├── rq2_pr
│                │            ├── __init__.py
│                │            ├── pr_defect_graph_ci_metrics.py
│                │            └── pr_fix_graph_ci_metrics.py
│                └── rq3
│                    ├── __init__.py
│                    └── issue_RQ3_models.py
├── context
│            ├── LrContext.py
│            ├── PsContext.py
│            ├── __init__.py
│            └── rf_context.py
├── core
│            ├── __init__.py
│            ├── __pycache__
│            │            └── correlation_analysis_factory.cpython-311.pyc
│            ├── correlation_analysis_factory.py
│            ├── factories
│            │            ├── __init__.py
│            │            ├── __pycache__
│            │            │            └── analysis_factory.cpython-311.pyc
│            │            └── analysis_factory.py
│            └── strategies
│                ├── __init__.py
│                ├── __pycache__
│                │            ├── anova.cpython-311.pyc
│                │            ├── pca.cpython-311.pyc
│                │            └── pearson_spearman.cpython-311.pyc
│                ├── anova.py
│                ├── linear_regression.py
│                ├── pca.py
│                ├── pearson_spearman.py
│                └── random_forest.py
├── demo
│            └── build_demo.py
├── persistence
│            ├── DataCacheHandler.py
│            ├── __init__.py
│            ├── __pycache__
│            │            └── DataCacheHandler.cpython-311.pyc
│            └── files
│                ├── issue_defect_graph_ci_metrics_ansible.parquet
│                ├── issue_defect_graph_ci_metrics_facebook.parquet
│                ├── issue_rq3_defect_graph_churn_pr_commits_ansible.parquet
│                ├── issue_rq3_defect_graph_churn_pr_commits_facebook.parquet
│                ├── pull_defect_graph_ci_metrics_ansible.parquet
│                └── pull_defect_graph_ci_metrics_facebook.parquet
├── populate_name_owner.py
├── queries
│            ├── __init__.py
│            ├── bug_commits_to_issues.sql
│            ├── bug_commits_to_pr.sql
│            ├── bug_introduced_defects_to_issues.sql
│            ├── churn_to_issues_prs_future_avg.sql
│            ├── dag_to_issues_prs_future_avg.sql
│            ├── issue_defect_graph_ci_metrics.sql
│            ├── pull_defect_graph_ci_metrics.sql
│            └── sp
│                ├── dag_to_issues.sql
│                ├── dev_workload_vs_issues_time.sql
│                ├── dev_workload_vs_pr_time.sql
│                ├── developer_inactivity_to_issues_pr.sql
│                ├── file_change_complexity_vs_issue_pr_time.sql
│                ├── labels_to_issue.sql
│                └── labels_to_pr.sql
└── requirements.txt


```


---

## Notes on Metric Interpretation

Some metrics (e.g., `bic_avg_branches`) may be zero for a large fraction of observations due to branch deletion or merge policies in Git workflows. These metrics are retained for completeness but should be interpreted with caution.

Future work may redefine such metrics to better capture structural branching exposure, for example by counting distinct downstream splits observed by a commit.

---

## Reproducibility

- Analyses are deterministic where applicable (fixed random seeds)
- Results are reproducible given the same underlying dataset
- All visualization functions are included in the repository

---

## License

Specify license here.

