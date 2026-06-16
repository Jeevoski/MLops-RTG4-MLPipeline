# MLops-RTG4-MLPipeline

A machine learning operations (MLOps) pipeline for spam detection built with DVC (Data Version Control) and MLflow-like experiment tracking using DVCLive. This project demonstrates reproducible ML workflows with automated data ingestion, preprocessing, feature engineering, model training, and evaluation.

## 📋 Project Overview

This project implements an end-to-end ML pipeline for spam classification with:
- **Automated data workflows** using DVC
- **Reproducible pipelines** with parameterized stages
- **Experiment tracking** using DVCLive
- **Model versioning** with git-based version control
- **Remote storage support** for ML artifacts (S3, GCS, Azure Blob)

## 📁 Project Structure

```
MLops-RTG4-MLPipeline/
├── src/                          # Source code for pipeline stages
│   ├── data_ingestion.py         # Download and split data
│   ├── data_preprocessing.py     # Text normalization & encoding
│   ├── feature_engineering.py    # TF-IDF vectorization
│   ├── model_building.py         # Model training (RandomForest)
│   └── model_evaluation.py       # Model evaluation & metrics
├── data/                         # Data directories (managed by DVC)
│   ├── raw/                      # Raw data (train/test splits)
│   ├── interim/                  # Preprocessed data
│   └── processed/                # TF-IDF vectorized features
├── models/                       # Trained models (managed by DVC)
│   └── model.pkl                 # Trained RandomForest model
├── reports/                      # Reports and metrics
│   └── metrics.json              # Evaluation metrics
├── experiments/                  # Jupyter notebooks & sample data
│   ├── mynotebook.ipynb          # Exploratory analysis
│   └── spam.csv                  # Sample dataset
├── dvc.yaml                      # DVC pipeline definition
├── dvc.lock                      # Locked pipeline state & reproducibility
├── params.yaml                   # Hyperparameters & configuration
├── .gitignore                    # Git ignore rules
├── .dvc/                         # DVC configuration
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- DVC (`pip install dvc`)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jeevoski/MLops-RTG4-MLPipeline.git
   cd MLops-RTG4-MLPipeline
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize DVC:**
   ```bash
   dvc init
   ```

## 📊 Pipeline Stages

The ML pipeline consists of 5 automated stages defined in `dvc.yaml`:

### 1. **Data Ingestion** (`data_ingestion.py`)
- Downloads spam dataset from remote source or uses local copy
- Splits data into train/test sets (80/20 split by default)
- **Output:** `data/raw/train.csv`, `data/raw/test.csv`
- **Params:** `data_ingestion.test_size`

### 2. **Data Preprocessing** (`data_preprocessing.py`)
- Encodes target labels using LabelEncoder
- Removes duplicate rows
- Text normalization:
  - Tokenization using NLTK
  - Removes stopwords and punctuation
  - Porter stemming
- **Output:** `data/interim/train_processed.csv`, `data/interim/test_processed.csv`

### 3. **Feature Engineering** (`feature_engineering.py`)
- Applies TF-IDF vectorization
- Limits features to `max_features` (default: 35)
- **Output:** `data/processed/train_tfidf.csv`, `data/processed/test_tfidf.csv`
- **Params:** `feature_engineering.max_features`

### 4. **Model Building** (`model_building.py`)
- Trains RandomForest classifier
- **Output:** `models/model.pkl`
- **Params:** `model_building.n_estimators`, `model_building.random_state`

### 5. **Model Evaluation** (`model_evaluation.py`)
- Evaluates model on test set
- Computes: accuracy, precision, recall, AUC
- Logs metrics and parameters using DVCLive
- **Output:** `reports/metrics.json`
- **Integration:** DVCLive experiment tracking (when available)

## ⚙️ Configuration

Edit `params.yaml` to modify pipeline behavior:

```yaml
data_ingestion:
  test_size: 0.20              # Train/test split ratio

feature_engineering:
  max_features: 35             # Max TF-IDF features

model_building:
  n_estimators: 22             # RandomForest trees
  random_state: 2              # Reproducibility seed
```

## 🔄 Running the Pipeline

### Run the entire pipeline:
```bash
dvc repro
```

### Run a specific stage:
```bash
dvc repro -t data_ingestion    # Run only data ingestion
dvc repro -t model_building    # Run only model building
```

### View pipeline DAG:
```bash
dvc dag
```

### Check pipeline status:
```bash
dvc status
```

## 🧪 Experiment Tracking with DVCLive

DVCLive automatically tracks experiments and parameters:

```bash
# Run an experiment
dvc exp run

# View all experiments
dvc exp show

# Compare specific experiments
dvc exp compare <exp-id-1> <exp-id-id-2>

# Remove an experiment
dvc exp remove <exp-name>

# Apply/reproduce a previous experiment
dvc exp apply <exp-name>
```

## 📈 Metrics

Model evaluation metrics are saved to `reports/metrics.json`:
- **Accuracy:** Overall classification accuracy
- **Precision:** True positives / (True positives + False positives)
- **Recall:** True positives / (True positives + False negatives)
- **AUC:** Area under ROC curve

## 🌐 Remote Storage Setup (Optional)

To store ML artifacts in cloud storage (S3, Azure Blob, GCS):

### AWS S3 Example:
```bash
# 1. Install AWS CLI and DVC S3 support
pip install dvc[s3]
pip install awscli

# 2. Configure AWS credentials
aws configure

# 3. Add S3 remote to DVC
dvc remote add -d myremote s3://my-bucket/dvc-storage

# 4. Push artifacts to remote
dvc push

# 5. Pull artifacts from remote
dvc pull
```

## 📦 Dependencies

Key libraries used in this project:
- **pandas:** Data manipulation and analysis
- **scikit-learn:** Machine learning models and metrics
- **nltk:** Natural language processing (tokenization, stemming)
- **pyyaml:** YAML configuration file handling
- **dvc:** Data and model versioning
- **dvclive:** Experiment tracking

Full list in `requirements.txt`

## 🔧 Troubleshooting

**Issue:** `params.yaml` not found
- **Solution:** Ensure `params.yaml` is in the project root directory

**Issue:** NLTK tokenizer not found
- **Solution:** Run `python -c "import nltk; nltk.download('punkt_tab')"`

**Issue:** DVC lock conflicts
- **Solution:** Remove `.dvc/tmp/rwlock` and rerun `dvc repro`

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test with `dvc repro`
3. Commit your changes: `git add . && git commit -m "Add your message"`
4. Push to GitHub: `git push origin feature/your-feature`
5. Create a Pull Request

## 📝 Project Workflow

### Initial Setup (Once)
```bash
git clone <repo>
dvc init
pip install -r requirements.txt
```

### Daily Development
```bash
# Make changes to code/parameters
# Run pipeline
dvc repro

# Check results
dvc exp show

# Commit changes
git add .
git commit -m "Update pipeline"
git push
```

### Updating Remote Storage
```bash
dvc push              # Push new artifacts
dvc pull              # Pull latest artifacts
```

## 📚 Resources

- [DVC Documentation](https://dvc.org/doc)
- [DVCLive Documentation](https://dvc.org/doc/dvclive)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [NLTK Documentation](https://www.nltk.org/)

## 📄 License

This project is licensed under the MIT License - see `LICENSE` file for details.

## 👤 Author

**Jeevan** - MLOps Project

---

**Last Updated:** June 16, 2026

**DVC Version:** 3.67.1+

**Python Version:** 3.12+