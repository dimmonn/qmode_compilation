import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

from scipy.stats import pearsonr, spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

from persistence.DataCacheHandler import DataCacheHandler

data_handler = DataCacheHandler('../../queries/dag_to_issues_prs_future_avg.sql',
                                '../persistence/files/dag_to_quality.parquet')
data = None
try:
    data = data_handler.load_from_parquet()
    print("Data loaded successfully!")
    print(data.head())
except Exception as e:
    print(f"Error loading data: {e}")

# Fill NaN values with 0 for correlation analysis
data.fillna(0, inplace=True)

# Define features (graph properties) and targets (quality metrics)
features = ['max_commit_depth',
            'min_commit_depth',
            'avg_degree',
            'max_degree',
            'max_branches',
            'max_edges',
            'max_vertices',
            'max_files_changed'
            ]
targets = ['avg_issue_resolution_time_days', 'avg_pr_review_time_days', 'num_of_prs_opened_after_commit_date',
           'num_of_issues_opened_after_commit_date']

X = data[features]
y = data[targets]

# Add constant for intercept
X = sm.add_constant(X)

# Fit the regression model

# for target in targets:
#     y = data[target]  # Select one target at a time
#     model = sm.OLS(y, X).fit()
#     print(f"\nRegression results for: {target}")
#     print(model.summary())

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)
