import pandas as pd
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from services import feature_map_ds3


def train_model():
    df = pd.read_csv('./dataset.csv')

    features = [
        'is_positive',
        'xbc_having_div',
        'xbc_withdrawals',
        'xbc_regular',
        'ratio_txncnt_outflow_inflow'
    ]
    features_df = df[features]

    X = features_df.iloc[:, 1:].values  # create an np.array of independent variables
    y = features_df.iloc[:, 0].values  # create an np.array of dependent variables


    imputer = Imputer(missing_values='NaN', strategy='mean',  axis=0)
    imputer.fit(X[:,:])
    X[:, :] = imputer.transform(X[:,:])
                  
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    rf_class = RandomForestClassifier(n_estimators=50)
    rf_class.fit(X_train, y_train)
    return rf_class

rf = train_model()


def get_address_risk_score(address):
    features = [
        'xbc_having_div',
        'xbc_withdrawals',
        'xbc_regular',
        'ratio_txncnt_outflow_inflow'
    ]

    feature_df = feature_map_ds3([address])
    feature_df = feature_df[features]
    X = feature_df.iloc[:, :].values  # create an np.array of independent variables

    p_X = int(rf.predict_proba(X)[0][1] * 100)
    return p_X if p_X != 0 else 1
