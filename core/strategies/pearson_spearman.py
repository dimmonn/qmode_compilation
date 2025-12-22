from core.correlation_analysis_factory import AnalysisStrategy
from scipy.stats import pearsonr, spearmanr
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


class PearsonSpearmanCorrelation(AnalysisStrategy):
    def analyze(self, data, features, targets):
        correlation_results = {}
        for target in targets:
            correlation_results[target] = {}
            for feature in features:
                valid_data = data[[feature, target]].dropna()
                if valid_data.empty:
                    continue
                pearson_corr, pearson_p = pearsonr(valid_data[feature], valid_data[target])
                spearman_corr, spearman_p = spearmanr(valid_data[feature], valid_data[target])

                print(f"Feature: {feature}, Target: {target}")
                print(f"  Pearson Correlation: {pearson_corr:.4f}, P-value: {pearson_p:.4e}")
                print(f"  Spearman Correlation: {spearman_corr:.4f}, P-value: {spearman_p:.4e}")
                print("")

                correlation_results[target][feature] = {
                    'pearson_corr': pearson_corr,
                    'pearson_p': pearson_p,
                    'spearman_corr': spearman_corr,
                    'spearman_p': spearman_p
                }
        return correlation_results

    def generic_visualization(self, data, features, targets):
        for target in targets:
            for feature in features:
                plt.figure(figsize=(8, 5))
                sns.regplot(x=data[feature], y=data[target], scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
                plt.xlabel(feature)
                plt.ylabel(target)
                plt.title(f'Impact of {feature} on {target}')
                plt.tight_layout()
                plt.show()

    def _scatterplot_matrix(self, data, features, targets):
        for target in targets:
            for feature in features:
                plt.figure(figsize=(8, 5))
                sns.scatterplot(x=data[feature], y=data[target], alpha=0.5)
                sns.regplot(x=data[feature], y=data[target], scatter=False, color='red', ci=None)
                plt.xlabel(feature)
                plt.ylabel(target)
                plt.title(f'{feature} vs {target}')
                plt.tight_layout()
                plt.show()
