
## Overview

This code is mainly inspired by [ShuaiW](https://github.com/ShuaiW/teach-machine-to-trade).

### Dependencies

Python 3.6
`pip install -r requirements.txt`

### Table of content

* `agent.py`: a Deep Q learning agent
* `envs.py`: a simple 3-stock trading environment
* `model.py`: a multi-layer perceptron as the function approximator
* `utils.py`: some utility functions
* `run.py`: train/test logic
* `requirement.txt`: all dependencies
* `data/`: the csv file of stock table and history close price of 19 stocks

### How to run

**To train a Deep Q agent**, run `python run.py --mode train`. There are other parameters and I encourage you look at the `run.py` script. After training, a trained model as well as the portfolio value history at episode end would be saved to disk.

**To test the model performance**, run `python run.py --mode test --weights <trained_model>`, where `<trained_model>` points to the local model weights file. Test data portfolio value history at episode end would be saved to disk.
