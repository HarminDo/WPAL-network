#!/usr/bin/env python

# --------------------------------------------------------------------
# This file is part of WMA Network.
#
# WMA Network is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WMA Network is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WMA Network.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------

import os.path as osp

import numpy as np
import scipy.io as sio


class RAPDataset:
	def __init__(self, db_path, par_set_id):
		self._db_path = db_path

		rap = sio.loadmat(osp.join(self._db_path,'RAP_annotation','RAP_annotation.mat'))['RAP_annotation']

		self._partition = rap[0][0][0]
		self.labels = rap[0][0][1]
		self.attr_ch = rap[0][0][2]
		self.attr_eng = rap[0][0][3]
		self.num_attrs = self.attr_eng.shape[0]
		self.position = rap[0][0][4]
		self._img_names = rap[0][0][5]
		self.attr_exp = rap[0][0][6]

		"""In our model, labels should be all between 0 and 1.
		Some labels are set to 2 in the RAP dataset, usually meaning the label is unknown or unsure.
		We change it to 0.5 as a more reasonable value expression.
		"""
		self.labels = np.array([[0.5 if x == 2 else x for x in line] for line in self.labels])

		self.set_partition_set_id(par_set_id)

	def evaluate_detections(self, attr, inds, output_dir):
		num = attr.shape[0]
		mA = (sum([(
						sum([attr[i][j] for j in xrange(num)])
						/ sum([self.labels[i][j] for j in xrange(num)])
						+ sum([(1 - attr[i][j]) for j in xrange(num)])
						/ sum([(1 - self.labels[i][j]) for j in xrange(num)])
				) for i in xrange(self.num_attrs)])) / (2 * num)

		return mA

	def set_partition_set_id(self, par_set_id):
		self.train_ind = self._partition[par_set_id][0][0][0][0][0] - 1
		self.test_ind = self._partition[par_set_id][0][0][0][1][0] - 1

	def get_img_path(self, img_id):
		return osp.join(self._db_path, 'RAP_dataset', self._img_names[img_id][0][0])

if __name__ == '__main__':
	db = RAPDataset('/home/ken.yu/datasets/rap', 0)
	print db._partition.shape
	print db._partition[0][0][0][0][1].shape
	print db._partition[1][0][0][0][1].shape
	print "Labels:", db.labels.shape
	print db.train_ind.shape
	print 'Max training index: ', max(db.train_ind)
	print db.get_img_path(0)
	print db.num_attrs