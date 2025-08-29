#!/usr/bin/env python3
"""
Setup script for transSATSolver - Transformer-based SAT Solver

This setup script allows the project to be installed as a Python package,
enabling imports from the src/ directory and providing entry points for
main training and evaluation scripts.
"""

from setuptools import setup, find_packages
import os

def read_requirements():
    """Read requirements from requirements.txt"""
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

def read_readme():
    """Read long description from README.md"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

setup(
    name="transSATSolver",
    version="0.1.0",
    description="Transformer models (GPT2/LLaMA) for SAT problem solving",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="SAT Research Team",
    python_requires=">=3.11",
    
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    
    # Dependencies
    install_requires=read_requirements(),
    
    # Entry points for command-line usage
    entry_points={
        'console_scripts': [
            'transSAT-train=core.train:main',
            'transSAT-eval=core.evaluator:main',
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    
    # Additional metadata
    keywords="transformer, sat, satisfiability, machine-learning, pytorch",
    project_urls={
        "Source": "https://github.com/your-org/transSATSolver",
        "Bug Reports": "https://github.com/your-org/transSATSolver/issues",
    },
)