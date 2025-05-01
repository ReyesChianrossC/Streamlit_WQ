def run_prediction_model(prediction_gap_weeks, title_suffix=""):
    water_cols = [
        'surface_temperature', 'middle_temperature', 'bottom_temperature',
        'ph', 'ammonia', 'nitrate', 'phosphate',
        'dissolved_oxygen', 'sulfide', 'carbon_dioxide'
    ]
    water_external_cols = water_cols + ['site', 'weather_condition', 'wind_direction', 'air_temperature']
    
    # Prepare DataFrames
    pd_waterparam_only = df_act2.select(*water_cols + ['site']).toPandas()
    pd_waterparam_external = df_act2.select(*water_external_cols).toPandas()
    
    # Encode categorical variables
    for col in ['site', 'weather_condition', 'wind_direction']:
        if col in pd_waterparam_external.columns:
            le = LabelEncoder()
            pd_waterparam_external[col] = le.fit_transform(pd_waterparam_external[col].astype(str))
    
    # Handle missing values
    pd_waterparam_only[water_cols] = pd_waterparam_only[water_cols].astype(float).fillna(pd_waterparam_only[water_cols].mean())
    pd_waterparam_external[water_cols + ['air_temperature']] = \
        pd_waterparam_external[water_cols + ['air_temperature']].astype(float).fillna(
            pd_waterparam_external[water_cols + ['air_temperature']].mean())
    
    # Normalize data
    scaler_only = MinMaxScaler()
    np_waterparam_only_scaled = scaler_only.fit_transform(pd_waterparam_only[water_cols])
    
    scaler_external = MinMaxScaler()
    np_waterparam_external_scaled = scaler_external.fit_transform(pd_waterparam_external[water_cols + ['air_temperature', 'site', 'weather_condition', 'wind_direction']])
    
    # Create sliding window predictions
    window_size = 1  # Predict for each time step
    step_size = 1    # Step size for sliding window
    X_list_only, Y_list_only, sites_list = [], [], []
    X_list_ext, Y_list_ext = [], []
    
    for start in range(0, len(np_waterparam_only_scaled) - prediction_gap_weeks - window_size + 1, step_size):
        end = start + window_size
        X_window_only = np_waterparam_only_scaled[start:end]
        Y_window_only = np_waterparam_only_scaled[end + prediction_gap_weeks - 1:end + prediction_gap_weeks]
        site_window = pd_waterparam_only['site'].values[start:end]
        
        X_window_ext = np_waterparam_external_scaled[start:end]
        Y_window_ext = np_waterparam_only_scaled[end + prediction_gap_weeks - 1:end + prediction_gap_weeks]
        
        if X_window_only.shape[0] == window_size and Y_window_only.shape[0] == 1:
            X_list_only.append(X_window_only)
            Y_list_only.append(Y_window_only)
            sites_list.append(site_window[0])  # Take the site at the start of the window
            X_list_ext.append(X_window_ext)
            Y_list_ext.append(Y_window_ext)
    
    X_waterparam_only = np.array(X_list_only)
    Y_waterparam_only = np.array(Y_list_only).squeeze(1)
    sites = np.array(sites_list)
    X_waterparam_external = np.array(X_list_ext)
    Y_waterparam_external = np.array(Y_list_ext).squeeze(1)
    
    # Debug shapes
    print(f"Prediction gap: {prediction_gap_weeks}")
    print(f"X_waterparam_only shape: {X_waterparam_only.shape}")
    print(f"Y_waterparam_only shape: {Y_waterparam_only.shape}")
    print(f"X_waterparam_external shape: {X_waterparam_external.shape}")
    print(f"Y_waterparam_external shape: {Y_waterparam_external.shape}")
    print(f"Sites length: {len(sites)}")
    
    # Reshape for models
    X_cnn_only = X_waterparam_only.reshape(X_waterparam_only.shape[0], X_waterparam_only.shape[1], 1)
    X_lstm_only = X_waterparam_only.reshape(X_waterparam_only.shape[0], 1, X_waterparam_only.shape[1])
    X_cnnlstm_only = X_waterparam_only.reshape(X_waterparam_only.shape[0], 1, X_waterparam_only.shape[1], 1)
    
    X_cnn_ext = X_waterparam_external.reshape(X_waterparam_external.shape[0], X_waterparam_external.shape[1], 1)
    X_lstm_ext = X_waterparam_external.reshape(X_waterparam_external.shape[0], 1, X_waterparam_external.shape[1])
    X_cnnlstm_ext = X_waterparam_external.reshape(X_waterparam_external.shape[0], 1, X_waterparam_external.shape[1], 1)
    
    # Train models and collect predictions
    models = {}
    site_predictions = []
    for name, train_func, X_train, Y_train in [
        ('CNN - Water Only', train_cnn, X_cnn_only, Y_waterparam_only),
        ('LSTM - Water Only', train_lstm, X_lstm_only, Y_waterparam_only),
        ('CNN-LSTM - Water Only', train_cnn_lstm, X_cnnlstm_only, Y_waterparam_only),
        ('CNN - Water + External', train_cnn, X_cnn_ext, Y_waterparam_only),
        ('LSTM - Water + External', train_lstm, X_lstm_ext, Y_waterparam_only),
        ('CNN-LSTM - Water + External', train_cnn_lstm, X_cnnlstm_ext, Y_waterparam_only),
    ]:
        print(f"Training {name}...")
        print(f"X_train shape: {X_train.shape}")
        print(f"Y_train shape: {Y_train.shape}")
        
        model, _ = train_func(X_train, Y_train)
        y_pred = model.predict(X_train, verbose=0)
        print(f"y_pred shape for {name}: {y_pred.shape}")
        
        # Check prediction variance
        pred_std = np.std(y_pred, axis=0)
        print(f"Prediction std for {name}: {pred_std}")
        if np.all(pred_std < 1e-5):
            print(f"Warning: Predictions for {name} have very low variance. Model may not be learning effectively.")
        
        if y_pred.shape[1] != len(water_cols):
            raise ValueError(f"Prediction output for {name} has {y_pred.shape[1]} columns, expected {len(water_cols)}")
        
        if y_pred.shape[0] != len(sites):
            raise ValueError(f"Prediction output for {name} has {y_pred.shape[0]} rows, expected {len(sites)}")
        
        models[name] = (Y_train, y_pred)
        
        # Store site-specific predictions
        pred_df = pd.DataFrame(y_pred, columns=[f"pred_{col}" for col in water_cols])
        pred_df['site'] = sites
        pred_df['model'] = name
        pred_df['horizon'] = title_suffix
        site_predictions.append(pred_df)
    
    # Compute metrics
    summary = []
    for model_name, (y_true, y_pred) in models.items():
        mae = np.mean(np.abs(y_true - y_pred))
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        summary.append([model_name, mae, mse, rmse, r2])
    
    metrics_df = pd.DataFrame(summary, columns=['Model', 'Final MAE', 'Final MSE', 'Final RMSE', 'R2 Score'])
    
    # Combine site-specific predictions
    site_predictions_df = pd.concat(site_predictions, ignore_index=True)
    return metrics_df, site_predictions_df
