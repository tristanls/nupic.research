# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
Temporal Pooler mixin that enables detailed monitoring of history.
"""

from collections import defaultdict
import numpy
from nupic.research.monitor_mixin.metric import Metric
from nupic.research.monitor_mixin.monitor_mixin_base import MonitorMixinBase
from nupic.research.monitor_mixin.trace import (
  IndicesTrace, CountsTrace, StringsTrace,  BoolsTrace)


class SpatialPoolerMonitorMixin(MonitorMixinBase):
  """
  Mixin for SpatialPooler that stores a detailed history, for inspection and
  debugging.
  """

  def __init__(self, *args, **kwargs):
    super(SpatialPoolerMonitorMixin, self).__init__(*args, **kwargs)
    self._mmTraces["dutyCycles"] = CountsTrace(self, "duty cycles")
    self._mmTraces["dutyCycles"].data = numpy.zeros(self._numColumns, dtype='uint32')


  def mmGetTraceActiveCells(self):
    """
    @return (Trace) Trace of active cells
    """
    return self._mmTraces["activeColumns"]

  def mmGetTraceActiveDutyCycles(self):
    """
    @return (Trace) Counts of duty cycles
    """
    return self._mmTraces["dutyCycles"]

  def mmGetTraceConnectionCounts(self):
    """
    @return (Trace) Counts of duty cycles
    """
    return self._mmTraces["totalConnected"]


  def mmGetMetricFromTrace(self, trace):
    """
    Convenience method to compute a metric over an indices trace

    @param (IndicesTrace) Trace of indices

    @return (Metric) Metric over trace excluding resets
    """
    return Metric.createFromTrace(trace.makeCountsTrace())

  # ==============================
  # Overrides
  # ==============================

  def compute(self, inputVector, learn, activeArray, *args, **kwargs):

    super(SpatialPoolerMonitorMixin, self).compute(\
        inputVector, learn, activeArray, *args,**kwargs)

    # extract indices of active columns
    activeColumns = numpy.nonzero(activeArray)

    # total number of connections
    connectedCounts = numpy.zeros(self._numColumns, dtype='uint32')
    self.getConnectedCounts(connectedCounts)
    totalConnection = numpy.sum(connectedCounts)

    self._mmTraces["activeColumns"].data.append(activeColumns)
    self._mmTraces["dutyCycles"].data[activeColumns] += 1
    self._mmTraces["totalConnected"].data.append(totalConnection)

  def mmGetDefaultTraces(self, verbosity=1):
    traces = [
      self.mmGetTraceActiveCells(),
    ]

    if verbosity == 1:
      traces = [trace.makeCountsTrace() for trace in traces]

    return traces


  def mmGetDefaultMetrics(self, verbosity=1):
    metrics = ([Metric.createFromTrace(trace)
                for trace in self.mmGetDefaultTraces()[:-1]])

    return metrics


  def mmClearHistory(self):
    super(SpatialPoolerMonitorMixin, self).mmClearHistory()

    self._mmTraces["activeColumns"] = IndicesTrace(self, "active columns")
    self._mmTraces["dutyCycles"] = CountsTrace(self, "duty cycles")
    self._mmTraces["dutyCycles"].data = numpy.zeros(self._numColumns, dtype='uint32')
    self._mmTraces["totalConnected"] = IndicesTrace(self, "total number of connection")