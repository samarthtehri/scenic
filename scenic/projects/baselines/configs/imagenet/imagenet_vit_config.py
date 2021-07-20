# pylint: disable=line-too-long
r"""Default configs for ViT on ImageNet2012.

```

"""
# pylint: disable=line-too-long

import ml_collections

_IMAGENET_TRAIN_SIZE = 1281167


def get_config(runlocal=''):
  """Returns the ViT experiment configuration for ImageNet."""

  runlocal = bool(runlocal)

  config = ml_collections.ConfigDict()
  config.experiment_name = 'imagenet-vit'
  # dataset
  config.dataset_name = 'imagenet'
  config.data_dtype_str = 'float32'
  config.dataset_configs = ml_collections.ConfigDict()

  # model
  config.model_name = 'vit_multilabel_classification'
  config.model = ml_collections.ConfigDict()
  config.model.hidden_size = 768
  config.model.patches = ml_collections.ConfigDict()
  config.model.patches.grid = [14, 14]
  config.model.num_heads = 12
  config.model.mlp_dim = 3072
  config.model.num_layers = 12
  config.model.representation_size = 768
  config.model.classifier = 'token'
  config.model.attention_dropout_rate = 0.
  config.model.dropout_rate = 0.1
  config.model_dtype_str = 'float32'

  # training
  config.trainer_name = 'fewshot_trainer'
  config.optimizer = 'adam'
  config.optimizer_configs = ml_collections.ConfigDict()
  config.optimizer_configs.beta1 = 0.9
  config.optimizer_configs.beta2 = 0.999
  config.optimizer_configs.weight_decay = 0.3
  config.explicit_weight_decay = None  # No explicit weight decay
  config.l2_decay_factor = None
  config.max_grad_norm = 1.0
  config.label_smoothing = None
  config.num_training_epochs = 90
  config.log_eval_steps = 1000
  config.batch_size = 8 if runlocal else 4096
  config.rng_seed = 42
  config.init_head_bias = -10.0

  # learning rate
  steps_per_epoch = _IMAGENET_TRAIN_SIZE // config.batch_size
  total_steps = config.num_training_epochs * steps_per_epoch
  base_lr = 3e-3
  config.lr_configs = ml_collections.ConfigDict()
  config.lr_configs.learning_rate_schedule = 'compound'
  config.lr_configs.factors = 'constant*linear_warmup*linear_decay'
  config.lr_configs.total_steps = total_steps
  config.lr_configs.end_learning_rate = 1e-5
  config.lr_configs.warmup_steps = 10_000
  config.lr_configs.base_learning_rate = base_lr

  # logging
  config.write_summary = True  # write TB and/or XM summary
  config.write_xm_measurements = True  # write XM measurements
  config.xprof = True  # Profile using xprof
  config.checkpoint = True  # do checkpointing
  config.checkpoint_steps = 5000
  config.debug_train = False  # debug mode during training
  config.debug_eval = False  # debug mode during eval


  return config


def get_hyper(hyper):
  """Defines the hyper-parameters sweeps for doing grid search."""
  return hyper.product([])
