from core.correlation_analysis_factory import AnalysisStrategy
from sklearn.decomposition import PCA


class PCAAnalysis(AnalysisStrategy):
    def analyze(self, data, features, targets):
        pca = PCA(n_components=min(len(features), 3))
        principal_components = pca.fit_transform(data[features].dropna())
        explained_variance = pca.explained_variance_ratio_

        loadings = pca.components_

        return {
            "principal_components": principal_components,
            "explained_variance": explained_variance,
            "loadings": loadings,
            "features": features
        }
