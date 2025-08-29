
# Transformer-based SAT Solver

This repository implements transformer models (GPT2/LLaMA) for SAT (Boolean Satisfiability) problem solving. The project trains models to classify CNF formulas as SAT or UNSAT using execution traces from DPLL/CDCL solvers.

---

## Environment Setup

To set up the environment, follow these steps:

1. Use the `environment.yml` file to install the necessary dependencies (PyTorch, Hugging Face libraries, etc.).
2. Run the following commands to create and activate the environment:

   ```bash
   conda env create -f environment.yml
   conda activate HF_SAT
   ```

---

## Datasets

Each dataset has its corresponding folder in the `data/datasets/` directory. These folders contain scripts for downloading and preparing the datasets.

To prepare a dataset, navigate to its directory and run `prepare.py`. For example:

   ```bash
   cd data/datasets/SAT_6_10_Random_State_Large
   python prepare.py
   ```

---

## Training

### Configuration

Training configurations are stored as Python files in the `configs/` directory. Each file contains custom training hyperparameters, including:

- **Dataset path**
- **Model save path** (with or without a timestamp)
- **Context size** for the model

To create a new training configuration, add a new Python file in `configs/` and define the necessary parameters. A list of commonly used configurable parameters can be found in the `### Parameters ###` section of `src/core/train.py`, including:

- `out_dir`: The base path to save the model. A timestamp is added by default to avoid overwriting; to disable this, set `append_timestamp=False`.
- `block_size`: The context size for the model.
- `dataset`: The training dataset, usually a directory in `data/datasets/`.
- `model`: Architecture type ("gpt2" or "llama")
- `state_trace`: Include solver state traces in training data

(This method is adapted from nanoGPT.)

### Running Training

To train a model using a basic configuration, use the following command:

   ```bash
   python src/core/train.py --model_name llama-70M --train_file path/to/train.txt
   ```

To use custom hyperparameters, specify them in the command:

   ```bash
   python src/core/train.py configs/[YOUR_TRAINING_CONFIG].py --epochs=12
   ```

If you encounter an `AssertionError`, check for issues like spaces instead of `=` in the parameter assignments. You can debug using `src/utils/configurator.py` to locate the error.

---

## Evaluation

The evaluation process focuses on measuring the model's accuracy in predicting SAT/UNSAT for CNF formulas.

To evaluate a model on a dataset, use:

   ```bash
   python src/core/evaluator.py --dataset=[Dataset Path] --model_dir=[Model Directory] --num_samples=[Number of Test Samples]
   ```

*Note*: Evaluation can be slower than training since token generation occurs incrementally and without batching. Typically, `num_samples` is set to 100 for initial evaluation.

### Batch Evaluation

For batch evaluation on multiple models, use the scripts in `scripts/`:

- **Linux**:

   ```bash
   ./scripts/folder_eval.sh ./results/models/6_10_random_ ./data/datasets/SAT_var_eval > results/6_10_random.txt
   ```

- **Windows**:

   ```bash
   python src/models/parat/folder_eval.py results/models/sat-llama ./data/datasets/Large_500k_SAT_11_15_marginal_large results.txt
   ```

---

## Project Architecture

### Directory Structure

```
transSATSolver/
├── src/                          # Source code
│   ├── core/                     # Core training and evaluation
│   │   ├── train.py             # Main training script
│   │   ├── trainer.py           # Custom HuggingFace trainer
│   │   └── evaluator.py         # Model evaluation
│   ├── dataset/                 # Data handling
│   │   └── sat_dataset.py       # Custom SAT dataset and tokenizer
│   ├── models/                  # Model implementations
│   │   ├── parat/               # PARAT transformer implementation
│   │   └── sat_solver/          # SAT solver implementations (DPLL/CDCL)
│   └── utils/                   # Utilities
│       ├── configurator.py      # Configuration system
│       └── utils.py             # General utilities
├── tests/                       # Unit tests
│   └── sat_solver/              # SAT solver tests
├── configs/                     # Training configurations
├── data/                        # Data directory
│   └── datasets/                # SAT problem datasets
├── scripts/                     # Batch processing scripts
├── results/                     # Training outputs
│   ├── models/                  # Saved model checkpoints
│   ├── logs/                    # Training logs
│   └── evaluations/             # Evaluation results
├── docs/                        # Documentation and research papers
├── setup.py                     # Project installation script
├── environment.yml              # Conda environment specification
└── requirements.txt             # Python package requirements
```

### Key Components

- **src/dataset/sat_dataset.py**: Custom tokenizer and dataset classes for SAT problem data
- **src/core/trainer.py**: Custom HuggingFace trainer for SAT-specific training
- **src/core/train.py**: Main training script with configurable parameters
- **src/core/evaluator.py**: Model evaluation with SAT/UNSAT classification metrics
- **src/utils/utils.py**: Utility functions including custom stopping criteria and model loading

### SAT Solver Module (`src/models/sat_solver/`)

- **generate_formula.py**: Random SAT formula generation
- **dpll.py/cdcl.py**: SAT solver implementations
- **trace_verify.py**: Execution trace validation
- Batch scripts for data generation: `batch_generate_data.sh`, `batch_solve_dpll.sh`

### Testing

Run all tests:
```bash
python -m pytest tests/
```

Run specific SAT solver tests:
```bash
python -m pytest tests/sat_solver/
```

Verify trace generation:
```bash
cd src/models/sat_solver  
python trace_verify.py
```

### Data Format

SAT problems are stored as text with format:
```
[CNF formula] [SEPARATOR] [execution trace] [SAT/UNSAT]
```

The custom tokenizer handles logical operators and solver-specific tokens.
