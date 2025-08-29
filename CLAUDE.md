# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository implements transformer models (GPT2/LLaMA) for SAT (Boolean Satisfiability) problem solving. The project trains models to classify CNF formulas as SAT or UNSAT using execution traces from DPLL/CDCL solvers.

## Environment Setup

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate HF_SAT
```

Alternative pip installation:
```bash
pip install -r requirements.txt
```

## Dataset Preparation

Each dataset in `data/datasets/` contains a `prepare.py` script:
```bash
cd data/datasets/SAT_6_10_Random_State_Large
python prepare.py
```

## Training

Training uses a nanoGPT-inspired configuration system with Python config files in `configs/`:

Basic training:
```bash
python src/core/train.py --model_name llama-70M --train_file path/to/train.txt
```

With custom config:
```bash
python src/core/train.py configs/train_sat_11_15_marginal_large.py --epochs=12
```

Debug configuration parsing:
```bash
python src/utils/configurator.py
```

## Evaluation

Single model evaluation:
```bash
python src/core/evaluator.py --dataset=[Dataset Path] --model_dir=[Model Directory] --num_samples=[Number of Test Samples]
```

Batch evaluation:
```bash
# Linux
./scripts/folder_eval.sh ./results/models/6_10_random_ ./data/datasets/SAT_var_eval > results.txt

# Windows  
python src/models/parat/folder_eval.py results/models/sat-llama ./data/datasets/Large_500k_SAT_11_15_marginal_large results.txt
```

## Architecture

### Core Components

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

### PARAT Module (`src/models/parat/`)

Custom transformer implementation with parameter-efficient training components:
- **model.py**: Custom attention mechanisms and GLU activations
- **compiler.py**: Model compilation utilities
- **sops.py**: Sum-of-products operations for logical reasoning

### Configuration System

Training parameters are defined in Python files under `configs/`. Key parameters:
- `epochs`, `batch_size`, `block_size`: Training hyperparameters
- `n_layer`, `n_embd`, `n_head`: Model architecture
- `dataset`: Path to training dataset
- `out_dir`: Model checkpoint directory
- `model`: Architecture type ("gpt2" or "llama")
- `state_trace`: Include solver state traces in training data

## Data Format

SAT problems are stored as text with format:
```
[CNF formula] [SEPARATOR] [execution trace] [SAT/UNSAT]
```

The custom tokenizer handles logical operators and solver-specific tokens.

## Testing

Run solver tests:
```bash
cd sat_solver
python -m pytest tests/
```

Verify trace generation:
```bash
cd sat_solver  
python trace_verify.py
```
- 我是mac系统，conda环境为HF_SAT，安装python库时尽量使用mamba。