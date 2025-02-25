from core.factories.analysis_factory import AnalysisFactory
from persistence.DataCacheHandler import DataCacheHandler

data_handler = DataCacheHandler('../../queries/dag_to_issues_prs_future_avg.sql',
                                '../../persistence/files/dag_to_quality.parquet')

data = data_handler.load_from_parquet()
print("Data loaded successfully!")
print(data.head())

# Fill NaN values with 0 for correlation analysis
data.fillna(0, inplace=True)

# Define features (graph properties) and targets (quality metrics)
features = [
    'commitCount',
    'max_commit_depth',
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

strategy_name = "pca"
analysis_strategy = AnalysisFactory.get_analysis(strategy_name)

correlation_results = analysis_strategy.analyze(data=data, features=features, targets=None)
print(correlation_results)

#analysis_strategy.generic_visualization(data=data, features=features, targets=targets)

analysis_strategy.visualize_pca(correlation_results)
