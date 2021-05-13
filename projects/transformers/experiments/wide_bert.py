# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2021, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

from copy import deepcopy

from .bertitos import tiny_bert_100k
from .sparse_bertitos import tiny_bert_sparse_100k
from .trifecta import (
    KDLRRangeTestTrainer,
    small_bert_trifecta_100k,
    tiny_bert_trifecta_100k,
)

"""
These experiments to widen the BERT model and see the effect on eval/loss after
pre-training. Widening is simply done by setting adjusting the `hidden_size` and
`intermediate` size by some factor. As well, the sparsity is adjusted as best as
possible to keep the same number of on-params between the models.
"""


lr_range_test_args = dict(
    max_steps=100,
    trainer_class=KDLRRangeTestTrainer,

    trainer_mixin_args=dict(
        # LR Range Test
        min_lr=0.0001,
        max_lr=0.05,
        test_mode="linear",

        # KD
        teacher_model_names_or_paths=[
            "/mnt/efs/results/pretrained-models/transformers-local/bert_1mi",
        ],
    ),
    overwrite_output_dir=True,
    do_eval=True,
)


# ---------
# Tiny BERT
# ---------


# Bert with layers of 25 percent wider
tiny_bert_125_percent_wide_args = dict(
    hidden_size=160,
    intermediate_size=640,
    sparsity=0.843,
    sparsify_all_embeddings=False,
)

# Bert with layers of 12.5 percent wider
tiny_bert_150_percent_wide_args = dict(
    hidden_size=192,
    intermediate_size=768,
    sparsity=0.872,
    sparsify_all_embeddings=False,
)

# Bert with layers of 12.5 percent wider
tiny_bert_200_percent_wide_args = dict(
    hidden_size=256,
    intermediate_size=1024,
    sparsity=0.9083,
    sparsify_all_embeddings=False,
)

# Bert with layers of 12.5 percent wider
tiny_bert_487_percent_wide_args = dict(
    hidden_size=624,
    intermediate_size=2496,
    sparsify_all_embeddings=False,
)


# Dense Tiny BERT with hidden and intermediate sizes 1.25x bigger.
tiny_bert_125_perc_wide_100k = deepcopy(tiny_bert_100k)
tiny_bert_125_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_125_percent_wide_args,
)

# Sparse Tiny BERT with hidden and intermediate sizes 1.25x bigger.
tiny_bert_sparse_125_perc_wide_100k = deepcopy(tiny_bert_sparse_100k)
tiny_bert_sparse_125_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_125_percent_wide_args,
)

# Sparse Tiny BERT with hidden and intermediate sizes 1.25x bigger.
# Trained with RigL + KD + OneCycle LR (Trifecta)
tiny_bert_trifecta_125_perc_wide_100k = deepcopy(tiny_bert_trifecta_100k)
tiny_bert_trifecta_125_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_125_percent_wide_args,
)

# Sparse Tiny BERT with hidden and intermediate sizes 1.5x bigger.
# Trained with RigL + KD + OneCycle LR (Trifecta)
tiny_bert_trifecta_150_perc_wide_100k = deepcopy(tiny_bert_trifecta_100k)
tiny_bert_trifecta_150_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_150_percent_wide_args,
)

# Sparse Tiny BERT with hidden and intermediate sizes 2.0x bigger.
# Trained with RigL + KD + OneCycle LR (Trifecta)
tiny_bert_trifecta_200_perc_wide_100k = deepcopy(tiny_bert_trifecta_100k)
tiny_bert_trifecta_200_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_200_percent_wide_args,
)

# Sparse Tiny BERT with hidden and intermediate sizes 4.87x bigger.
# This is the same size in terms of parameters as Small BERT.
# Trained with RigL + KD + OneCycle LR (Trifecta)
tiny_bert_trifecta_487_perc_wide_100k = deepcopy(tiny_bert_trifecta_100k)
tiny_bert_trifecta_487_perc_wide_100k["config_kwargs"].update(
    **tiny_bert_487_percent_wide_args,
    sparsity=0.97,  # this sparsity mimics dense Tiny BERT 1.0x Wide
)
tiny_bert_trifecta_487_perc_wide_100k.update(
    # Using batch_size of 16 instead of 128 since we're training on 8 GPUs.
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
)

# This experiment is like the one of the same name above, but it's meant to be
# compared to Small BERT. Thus, it uses the same number of attention heads and
# a comparable number of on-params. As well, the lr is tuned given the slightly
# greater number of params.
# tiny_bert_trifecta_487_perc_wide_100k = deepcopy(tiny_bert_trifecta_100k)
# tiny_bert_trifecta_487_perc_wide_100k["config_kwargs"].update(
#     **tiny_bert_487_percent_wide_args,
#     # This better mimics Small BERT's architecture. Tiny BERT usually just has 2.
#     attention_heads=8,
#     # This mimics Small BERT 1.0x Wide at 96.95% sparse
#     sparsity=0.972,
# )
# tiny_bert_trifecta_487_perc_wide_100k["trainer_mixin_args"].update(
#     # This max_lr is determined by the test below:
#     # `tiny_bert_trifecta_487_perc_wide_lr_range_test`
#     max_lr=0.011,
#     pct_start=0.1,
# )
# tiny_bert_trifecta_487_perc_wide_100k.update(
#     # Using batch_size of 16 instead of 128 since we're training on 8 GPUs.
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
# )

# This helps decide the max_lr for `tiny_bert_trifecta_487_perc_wide_100k` above.
tiny_bert_trifecta_487_perc_wide_lr_range_test = deepcopy(tiny_bert_trifecta_487_perc_wide_100k)  # noqa E501
tiny_bert_trifecta_487_perc_wide_lr_range_test.update(
    **lr_range_test_args,
)


# This is a control for Tiny BERT 4.87x Wide
# This Small BERT has the same number of on-params and total params.
small_bert_97_percent_trifecta_100k = deepcopy(small_bert_trifecta_100k)
small_bert_97_percent_trifecta_100k["config_kwargs"].update(
    sparsity=0.9695,
    sparsify_all_embeddings=False,
)
small_bert_97_percent_trifecta_100k["trainer_mixin_args"].update(
    max_lr=0.012,
)


# This helps decide the max_lr for `small_bert_97_percent_trifecta_100k` above.
small_bert_97_percent_trifecta_lr_range_test = deepcopy(small_bert_97_percent_trifecta_100k)  # noqa E501
small_bert_97_percent_trifecta_lr_range_test.update(
    **lr_range_test_args,
)


CONFIGS = dict(

    # Tiny BERT
    tiny_bert_125_perc_wide_100k=tiny_bert_125_perc_wide_100k,
    tiny_bert_sparse_125_perc_wide_100k=tiny_bert_sparse_125_perc_wide_100k,
    tiny_bert_trifecta_125_perc_wide_100k=tiny_bert_trifecta_125_perc_wide_100k,
    tiny_bert_trifecta_150_perc_wide_100k=tiny_bert_trifecta_150_perc_wide_100k,
    tiny_bert_trifecta_200_perc_wide_100k=tiny_bert_trifecta_200_perc_wide_100k,
    tiny_bert_trifecta_487_perc_wide_100k=tiny_bert_trifecta_487_perc_wide_100k,
    tiny_bert_trifecta_487_perc_wide_lr_range_test=tiny_bert_trifecta_487_perc_wide_lr_range_test,  # noqa E501

    # Controls for Tiny BERT
    small_bert_97_percent_trifecta_100k=small_bert_97_percent_trifecta_100k,
    small_bert_97_percent_trifecta_lr_range_test=small_bert_97_percent_trifecta_lr_range_test,  # noqa E501
)
