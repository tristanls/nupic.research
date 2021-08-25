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
#
# This work was built off the Greedy InfoMax codebase from Sindy Lowe:
# https://github.com/loeweX/Greedy_InfoMax
# The original Greedy InfoMax paper can be found here:
# https://arxiv.org/abs/1905.11786
# ----------------------------------------------------------------------

import torch.nn as nn
import torch.nn.functional as F
import nupic.research.frameworks.greedy_infomax.utils.data_utils as data_utils
from nupic.torch.modules import SparseWeights2d

# used to block gradients between layers
class GradientBlock(nn.Module):
    def __init__(self):
        super(GradientBlock, self).__init__()

    def forward(self, x):
       return x.detach()

# used to emit encodings at various points in the model's computation graph
class EmitEncoding(nn.Identity):
    def __init__(self):
        super(EmitEncoding, self).__init__()

    def encode(self, x, n_patches_x, n_patches_y):
        out = F.adaptive_avg_pool2d(x, 1)
        out = out.reshape(-1, n_patches_x, n_patches_y, out.shape[1])
        out = out.permute(0, 3, 1, 2).contiguous()
        return out

class PatchifyInputs(nn.Module):
    def __init__(self, patch_size=16, overlap=2):
        super(PatchifyInputs, self).__init__()
        self.patch_size = patch_size
        self.overlap = overlap

    def forward(self, x):
        x, n_patches_x, n_patches_y = data_utils.patchify_inputs(x)
        return x, n_patches_x, n_patches_y

class SparseConv2d(nn.Module):
    def __init__(self, in_channels: int,
        out_channels: int,
        kernel_size,
        stride = 1,
        padding = 0,
        dilation = 1,
        groups = 1,
        bias = True,
        padding_mode = 'zeros',
        sparse_weights_class = SparseWeights2d,
        sparsity=None,
        allow_extremes=False):
        super(SparseConv2d, self).__init__()
        self.conv2d = nn.Conv2d(in_channels,
                                out_channels,
                                kernel_size,
                                stride=stride,
                                padding=padding,
                                dilation=dilation,
                                groups=groups,
                                bias=bias,
                                padding_mode=padding_mode)
        self.conv2d = sparse_weights_class(self.conv2d,
                                      sparsity=sparsity,
                                      allow_extremes=allow_extremes)
    def forward(self, x):
        return self.conv2d(x)