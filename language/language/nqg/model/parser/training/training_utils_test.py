# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
"""Tests for training_utils with different training strategies.

These tests also serve as a sort of integration test between
the generation of tf.Examples, input_utils, and training_utils.
"""

import os

from language.nqg.model.parser import nqg_model
from language.nqg.model.parser import test_utils
from language.nqg.model.parser.data import example_converter
from language.nqg.model.parser.training import input_utils
from language.nqg.model.parser.training import training_utils
from language.nqg.model.qcfg import qcfg_rule

import tensorflow as tf

from official.nlp import optimization


def _write_tf_examples(examples_filepath, config, num_examples=8):
  """Write examples as test data."""
  tokenizer = test_utils.MockTokenizer()
  rules = [
      qcfg_rule.rule_from_string("foo NT_1 ### foo NT_1"),
      qcfg_rule.rule_from_string("bar ### bar"),
      qcfg_rule.rule_from_string("foo bar ### foo bar"),
  ]

  converter = example_converter.ExampleConverter(rules, tokenizer, config)
  example = ("foo bar", "foo bar")

  writer = tf.io.TFRecordWriter(examples_filepath)
  for _ in range(num_examples):
    tf_example = converter.convert(example)
    writer.write(tf_example.SerializeToString())


def _run_model_with_strategy(strategy, config, bert_config, dataset_fn):
  dataset_iterator = iter(
      strategy.experimental_distribute_datasets_from_function(dataset_fn))
  batch_size = int(config["batch_size"] / strategy.num_replicas_in_sync)
  with strategy.scope():
    model = nqg_model.Model(
        batch_size, config, bert_config, training=True, verbose=False)
    optimizer = optimization.create_optimizer(config["learning_rate"],
                                              config["training_steps"],
                                              config["warmup_steps"])
    train_for_n_steps_fn = training_utils.get_train_for_n_steps_fn(
        strategy, optimizer, model)
    mean_loss = train_for_n_steps_fn(
        dataset_iterator,
        tf.convert_to_tensor(config["steps_per_iteration"], dtype=tf.int32))
    return mean_loss


def _run_model(config, bert_config, dataset_fn):
  batch_size = config["batch_size"]
  model = nqg_model.Model(
      batch_size, config, bert_config, training=True, verbose=False)
  optimizer = optimization.create_optimizer(config["learning_rate"],
                                            config["training_steps"],
                                            config["warmup_steps"])

  training_step = training_utils.get_training_step(optimizer, model)
  mean_loss = training_step(next(iter(dataset_fn(ctx=None))))
  return mean_loss


class TrainingUtilsTest(tf.test.TestCase):

  def setUp(self):
    super(TrainingUtilsTest, self).setUp()
    self.config = test_utils.get_test_config()
    self.bert_config = test_utils.get_test_bert_config()
    examples_filepath = os.path.join(self.get_temp_dir(), "examples.tfrecord")
    _write_tf_examples(examples_filepath, self.config)
    self.dataset_fn = input_utils.get_dataset_fn(examples_filepath, self.config)

  def test_model_no_strategy(self):
    mean_loss = _run_model(self.config, self.bert_config, self.dataset_fn)
    self.assertIsNotNone(mean_loss)

  def test_model_one_device(self):
    strategy = tf.distribute.OneDeviceStrategy(device="/cpu:0")
    mean_loss = _run_model_with_strategy(strategy, self.config,
                                         self.bert_config, self.dataset_fn)
    self.assertIsNotNone(mean_loss)

  def test_model_mirrored(self):
    strategy = tf.distribute.MirroredStrategy(devices=["/cpu:0", "/cpu:1"])
    mean_loss = _run_model_with_strategy(strategy, self.config,
                                         self.bert_config, self.dataset_fn)
    self.assertIsNotNone(mean_loss)


if __name__ == "__main__":
  tf.test.main()
