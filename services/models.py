import pandas as pd
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from joblib import dump, load

from services import feature_map


def get_address_risk_score(address):
    # df = pd.read_csv('./dataset.csv')
    features = [
        'is_positive',
        'life_days',
        'active_in_days_percentage',
        'active_out_days_percentage',
        'percentage_in_internal_volume',
        'percentage_out_txs_count',
        'ratio_stddev_out_amount',
        ]
    # features_df = df[features]

    # X = features_df.iloc[:, 1:].values  # create an np.array of independent variables
    # y = features_df.iloc[:, 0].values  # create an np.array of dependent variables


    # imputer = Imputer(missing_values='NaN', strategy='mean',  axis=0)
    # imputer.fit(X[:,:])
    # X[:, :] = imputer.transform(X[:,:])
                  
    # scaler = StandardScaler()
    # X = scaler.fit_transform(X)

    # X_train, X_test, y_train, y_test = train_test_split(X, y)

    # nb = GaussianNB()
    # nb.fit(X_train, y_train)
    nb = load('./model.joblib')

    feature_df = feature_map([address])
    feature_df = feature_df[features]
    X = feature_df.iloc[:, 1:].values  # create an np.array of independent variables
    p_X = int(nb.predict_proba(X)[0][1] * 100)
    return p_X if p_X else 1
