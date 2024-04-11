import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from skimage.feature import hog
import joblib


class PretrainedFacialRecognitionModel:
    def __init__(self, model_file):
        self.model = joblib.load(model_file)

    def predict(self, image1_data, image2_data):
        preprocessed_image1 = self.preprocess_image(image1_data)
        preprocessed_image2 = self.preprocess_image(image2_data)

        features1 = self.extract_features(preprocessed_image1)
        features2 = self.extract_features(preprocessed_image2)

        combined_features = self.combine_features(features1, features2)

        confidence = self.model.predict_proba(combined_features.reshape(1, -1))[:, 1][0]
        return confidence

    def preprocess_image(self, image_data):
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(image, (100, 100))  # Assuming dimension setting

        blurred_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
        equalized_image = cv2.equalizeHist(blurred_image)
        return equalized_image

    def extract_features(self, image):
        hog_features = hog(image, orientations=9, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), transform_sqrt=True, block_norm="L2-Hys")

        pca = PCA(n_components=50)  # Assuming 50 principal components
        pca_features = pca.fit_transform(hog_features.reshape(1, -1))
        return pca_features

    def combine_features(self, features1, features2):
        combined_features = np.concatenate((features1, features2), axis=1)
        return combined_features


class EnhancedPretrainedFacialRecognitionModel(BaseEstimator, TransformerMixin):
    def __init__(self, model_file):
        self.rf_model = RandomForestClassifier(n_estimators=100)
        self.gb_model = GradientBoostingClassifier(n_estimators=100)
        self.lr_model = LogisticRegression()

    def fit(self, X, y):
        self.rf_model.fit(X, y)
        self.gb_model.fit(X, y)
        self.lr_model.fit(X, y)
        return self

    def predict_proba(self, X):
        rf_proba = self.rf_model.predict_proba(X)
        gb_proba = self.gb_model.predict_proba(X)
        lr_proba = self.lr_model.predict_proba(X)
        return (rf_proba + gb_proba + lr_proba) / 3.0


pretrained_model = PretrainedFacialRecognitionModel('keras_model.h5')
enhanced_model = EnhancedPretrainedFacialRecognitionModel('keras_model.h5')
