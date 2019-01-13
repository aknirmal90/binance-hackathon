import pandas as pd
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from services import feature_map_ds3


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
              
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y)
rf_class = RandomForestClassifier(n_estimators=500)
rf_class.fit(X_train, y_train)


def get_address_risk_score(address):
    features = [
        'xbc_having_div',
        'xbc_withdrawals',
        'xbc_regular',
        'ratio_txncnt_outflow_inflow'
    ]

    feature_df = feature_map_ds3([address])
    feature_df = feature_df[features]
    
    X_ = feature_df.values
    X_ = scaler.transform(X_)  # create an np.array of independent variables

    p_X = int(rf_class.predict_proba(X_)[0][1] * 100)
    return p_X if p_X != 0 else 1
