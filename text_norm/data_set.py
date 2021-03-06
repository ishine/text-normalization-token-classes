import numpy as np


class DataSet(object):

    def __init__(self, data, labels, keys):
        if len(data) != len(labels):
            raise ValueError

        self._data = np.array(data)
        self._labels = np.array(labels)
        self._keys = np.array(keys)

        self._epoch = 0
        self._offset = 0

    @property
    def data(self):
        return self._data

    @property
    def labels(self):
        return self._labels

    @property
    def keys(self):
        return self._keys

    @property
    def epoch(self):
        return self._epoch

    def next_batch(self, batch_size, shuffle=False):
        # check the data is not empty
        if not len(self._data):
            return []

        # new epoch, shuffle the data
        if not self._offset:
            self._epoch += 1
            if shuffle:
                self._shuffle_data()

        # get a batch
        data_batch = self._data[self._offset:self._offset + batch_size]
        labels_batch = self._labels[self._offset:self._offset + batch_size]
        keys_batch = self._keys[self._offset:self._offset + batch_size]

        # update an offset
        self._offset += batch_size

        # start new epoch
        if len(data_batch) < batch_size:
            self._offset = 0
            rest_data, rest_labels, rest_keys = self.next_batch(batch_size - len(data_batch))
            data_batch = np.concatenate([data_batch, rest_data])
            labels_batch = np.concatenate([labels_batch, rest_labels])
            keys_batch = np.concatenate([keys_batch, rest_keys])

        return data_batch, labels_batch, keys_batch

    def _shuffle_data(self):
        perm = np.arange(len(self._data))
        np.random.shuffle(perm)
        self._data = self._data[perm]
        self._labels = self._labels[perm]
        self._keys = self._keys[perm]
