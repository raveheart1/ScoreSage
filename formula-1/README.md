# Formula 1 Predictive Modeling

## Overview
This project is designed to predict Formula 1 race outcomes for the Mexican Grand Prix using machine learning. The model is built using historical data from various practice, qualifying, and race sessions. The data is processed, and a Random Forest model is used for predictions.

## Directory Structure
```
formula-1/
├── data/
│   ├── drivers/
│   │   ├── hamilton/
│   │   │   └── grand-prix/
│   │   │       └── bahrain/
│   │   │           ├── position_data_Race.csv
│   │   │           ├── pit_data_Race.csv
│   │   │           └── ...
│   │   └── verstappen/
│   │       └── grand-prix/
│   │           └── bahrain/
│   │               ├── position_data_Race.csv
│   │               ├── pit_data_Race.csv
│   │               └── ...
├── models/
│   └── mexican_gp_predictor_model.pkl
├── scripts/
│   ├── train_model.py  # Main training script
│   ├── preprocess_data.py  # Data preprocessing utilities
│   └── predict.py  # Script for making predictions
├── requirements.txt
└── README.md  # Documentation
```

## Getting Started
1. **Install Dependencies**: Install the required packages by running:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Data**: Ensure that the necessary driver data is present in the `data/` directory. Data should include information like lap times, pit times, stint details, track and air temperatures, etc.

   - The script now dynamically loads all CSV files from the `data/drivers/` directory, so you only need to add new files in the appropriate folders.

3. **Train the Model**: Run the training script to train the predictive model:
   ```bash
   python scripts/train_model.py
   ```
   This will generate the `mexican_gp_predictor_model.pkl` file, which is saved in the `models/` directory.

4. **Make Predictions**: Use the `predict.py` script to make predictions. For example, to predict the outcome based on sample lap data:
   ```bash
   python scripts/predict.py
   ```

## Model Details
- **Algorithm**: Random Forest Classifier
- **Input Features**: The model dynamically selects numeric features that are common across all loaded datasets. Typical features include lap number, speed, pit duration, stint, track temperature, and air temperature.
- **Label**: Final position of the driver

## Data
The data used for training the model includes:
- **Practice, Qualifying, and Race data**: Data from various sessions, such as lap times, positions, pit stops, etc.
- **Drivers**: Historical performance data of multiple drivers like Hamilton, Verstappen, etc.

Ensure that the data is stored in the appropriate folders as described in the directory structure. The script will automatically load all CSV files within the `data/drivers/` directory.

## Requirements
The required Python packages are listed in `requirements.txt`:
- pandas
- numpy
- scikit-learn
- joblib
- requests
- urllib3<2.0
- fastf1

Install the dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
1. **Training the Model**: Use the `train_model.py` script to train the model on your data.
2. **Making Predictions**: Use the `predict.py` script to predict the race outcomes based on new input data.

## Future Work
- **Feature Engineering**: Add more features like weather conditions, tire changes, car setup, and race incidents to improve model accuracy.
- **Model Tuning**: Experiment with different machine learning models and hyperparameters for better prediction accuracy.
- **Summary-Level Dataset**: Consider creating a summary dataset that includes aggregated metrics for each driver per race, which could improve prediction accuracy.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
