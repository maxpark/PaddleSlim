# Copyright (c) 2021  PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import yaml
import os
from paddleslim.auto_compression.strategy_config import *

__all__ = ['save_config', 'load_config']


def load_config(config):
    """Load configurations from yaml file into dict.
    Fields validation is skipped for loading some custom information.
    Args:
      config(str): The path of configuration file.
    Returns:
      dict: A dict storing configuration information.
    """
    if config is None:
        return None
    assert isinstance(
        config,
        str), f"config should be str but got type(config)={type(config)}"
    assert os.path.exists(config) and os.path.isfile(
        config), f"{config} not found or it is not a file."
    with open(config) as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
    return cfg


def extract_strategy_config(config):
    """Extract configuration items of strategies from file or dict.
    And fields validation is enable.
    Args:
      config(str, dict): The path of configuration file or a dict storing information about strategies.
    Returns:
      dict: The key is the name of strategy and the value is an instance of paddleslim.auto_compression.BaseStrategy.
    """
    if config is None:
        return None
    if isinstance(config, str):
        config = load_config(config)

    compress_config = {}
    if isinstance(config, dict):
        for key, value in config.items():
            if key in SUPPORTED_CONFIG:
                compress_config[key] = eval(key)(**value) if isinstance(
                    value, dict) else eval(key)()
    elif type(config) in [set, list, tuple]:
        for key in config:
            assert isinstance(key, str)
            if key in SUPPORTED_CONFIG:
                compress_config[key] = eval(key)()

    if len(compress_config) == 0:
        compress_config = None
    return compress_config


def extract_train_config(config):
    """Extract configuration items of training from file or dict.
    And fields validation is enable.
    Args:
      config(str, dict): The path of configuration file or a dict storing information about training.
    Returns:
      An instance of paddleslim.auto_compression.TrainConfig
    """
    if config is None:
        return None
    if isinstance(config, str):
        config = load_config(config)
    if isinstance(config, dict):
        for key, value in config.items():
            if key == TRAIN_CONFIG_NAME:
                return TrainConfig(
                    **value) if value is not None else TrainConfig()
    # return default training config when it is not set
    return TrainConfig()


def save_config(config, config_path):
    """
        convert dict config to yaml.
    """
    f = open(config_path, "w")
    yaml.dump(config, f)
    f.close()
