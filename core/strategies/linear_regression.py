from core.correlation_analysis_factory import AnalysisStrategy
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class LinearRegressionAnalysis(AnalysisStrategy):
    def analyze(self, data, features, targets):
        regression_results = {}

        for target in targets:
            X = data[features].copy()
            y = data[target]

            X = sm.add_constant(X)
            model = sm.OLS(y, X, missing='drop').fit()

            summary_df = pd.DataFrame({
                'feature': model.params.index,
                'coefficient': model.params.values,
                'p_value': model.pvalues.values
            })

            regression_results[target] = summary_df

        return regression_results

    def visualize_regression(self, results, features, targets):
        for target in targets:
            df = results[target]
            df = df[df['feature'] != 'const']

            plt.figure(figsize=(10, 5))
            ax = sns.barplot(x='feature', y='coefficient', data=df, palette='coolwarm')

            # Annotate p-values
            for i, row in df.iterrows():
                significance = ''
                if row['p_value'] < 0.001:
                    significance = '***'
                elif row['p_value'] < 0.01:
                    significance = '**'
                elif row['p_value'] < 0.05:
                    significance = '*'

                ax.text(i, row['coefficient'], significance, ha='center', va='bottom')

            plt.title(f'Linear Regression Coefficients for {target}')
            plt.xticks(rotation=45)
            plt.axhline(0, color='gray', linestyle='--')
            plt.tight_layout()
            plt.show()


    def visualize_scatter(self, data, features, targets):
        import seaborn as sns
        import matplotlib.pyplot as plt

        for target in targets:
            for feature in features:
                plt.figure(figsize=(8, 5))
                sns.scatterplot(x=data[feature], y=data[target], alpha=0.5)
                sns.regplot(x=data[feature], y=data[target], scatter=False, color='red', ci=None)
                plt.xlabel(feature)
                plt.ylabel(target)
                plt.title(f'{feature} vs {target} (Linear Fit)')
                plt.tight_layout()
                plt.show()