from core.correlation_analysis_factory import AnalysisStrategy
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


class RandomForestAnalysis(AnalysisStrategy):
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)

    def analyze(self, data, features, targets):
        results = {}

        for target in targets:
            train_data = data[data['dataset_split'] == 'train']
            valid_data = data[data['dataset_split'] == 'validation']

            X_train = train_data[features]
            y_train = train_data[target]

            X_valid = valid_data[features]
            y_valid = valid_data[target]

            self.model.fit(X_train, y_train)

            y_pred = self.model.predict(X_valid)

            mse = mean_squared_error(y_valid, y_pred)
            r2 = r2_score(y_valid, y_pred)

            results[target] = {
                "model": self.model,
                "r2_score": r2,
                "mse": mse,
                "y_true": y_valid,
                "y_pred": y_pred,
                "feature_importances": self.model.feature_importances_,
            }
        return results

    def visualize_importance(self, results, features):
        for target, res in results.items():
            importances = res["feature_importances"]
            sorted_idx = np.argsort(importances)[::-1]
            sorted_features = np.array(features)[sorted_idx]
            sorted_importances = importances[sorted_idx]

            plt.figure(figsize=(8, 5))
            sns.barplot(x=sorted_importances, y=sorted_features, palette="viridis")
            plt.title(f"Feature Importances for predicting {target}")
            plt.xlabel("Importance")
            plt.ylabel("Feature")
            plt.tight_layout()
            plt.show()

    def visualize_prediction_fit(self, results):
        for target, res in results.items():
            plt.figure(figsize=(6, 5))
            sns.scatterplot(x=res["y_true"], y=res["y_pred"], alpha=0.6)
            plt.plot([res["y_true"].min(), res["y_true"].max()],
                     [res["y_true"].min(), res["y_true"].max()], 'r--')
            plt.xlabel("Actual")
            plt.ylabel("Predicted")
            plt.title(f"Actual vs Predicted: {target}")
            plt.tight_layout()
            plt.show()

    def visualize_residuals(self, results):
        for target, res in results.items():
            residuals = res["y_true"] - res["y_pred"]
            plt.figure(figsize=(6, 4))
            sns.histplot(residuals, bins=50, kde=True)
            plt.title(f"Residuals for {target}")
            plt.xlabel("Residual")
            plt.tight_layout()
            plt.show()
