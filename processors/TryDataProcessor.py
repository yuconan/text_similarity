import logging
import os
import csv

logger = logging.getLogger(__name__)


class TryDataProcessor:

    def get_train_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {}".format(os.path.join(data_dir, "train.csv")))
        return self._read_csv(os.path.join(data_dir, "train.csv"))

    def get_dev_examples(self, data_dir):
        """See base class."""
        return []

    def get_test_examples(self, data_dir):
        """See base class."""
        return []

    def get_augment_examples(self, data_dir):
        """See base class."""
        logger.info("LOOKING AT {}".format(os.path.join(data_dir, "augment.csv")))
        return self._read_csv(os.path.join(data_dir, "augment.csv"))

    def get_all_examples(self, data_dir):
        """See base class."""
        train = self.get_train_examples(data_dir)
        dev = self.get_dev_examples(data_dir)
        test = self.get_test_examples(data_dir)
        return train, dev, test

    def get_labels(self):
        """See base class."""
        return ["0", "1"]

    @classmethod
    def _read_csv(cls, input_file):
        """
        :param input_file:
        :return: list [ sentences1,sentences2,label, category]
                if not sentences2, set None. the others same.
        """
        data_list = []
        with open(input_file, "r", encoding="utf-8-sig") as f:
            tsv_list = list(csv.reader(f))
            for line in tsv_list[1:]:
                data_list.append([line[0], line[1], line[2], line[3]])
        return data_list


# if __name__ == "__main__":
#     print(TryDataProcessor._read_csv(input_file='../try_data/train.csv'))