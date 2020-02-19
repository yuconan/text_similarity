import logging
from processors.TryDataProcessor import TryDataProcessor
from transformers import BertTokenizer
from models.bert import Bert

from k_fold import k_fold_cross_validation
from utils.augment import DataAugment
from utils.utils import *
from train_eval import *


class NewsConfig:

    def __init__(self):
        absdir = os.path.dirname(os.path.abspath(__file__))
        _pretrain_path = '/pretrain_models/bert-base-chinese'
        _config_file = 'config.json'
        _model_file = 'pytorch_model.bin'
        _tokenizer_file = 'vocab.txt'
        _data_path = '/try_data'

        self.models_name = 'base_bert'
        self.task = 'base_try_data'
        self.config_file = os.path.join(absdir + _pretrain_path, _config_file)
        self.model_name_or_path = os.path.join(absdir + _pretrain_path, _model_file)
        self.tokenizer_file = os.path.join(absdir + _pretrain_path, _tokenizer_file)
        self.data_dir = absdir + _data_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')              # 设备
        self.device_id = 3
        self.do_lower_case = True
        self.label_on_test_set = True
        self.requires_grad = True
        self.class_list = []
        self.num_labels = 2
        self.train_num_examples = 0
        self.dev_num_examples = 0
        self.test_num_examples = 0
        self.hidden_dropout_prob = 0.1
        self.hidden_size = 768
        self.require_improvement = 1000                                                         # 若超过1000batch效果还没提升，则提前结束训练
        self.num_train_epochs = 8                                                               # epoch数
        self.batch_size = 32                                                                     # mini-batch大小
        self.pad_size = 64                                                                      # 每句话处理成的长度
        self.learning_rate = 1e-5                                                               # 学习率
        self.weight_decay = 0.01                                                                # 权重衰减因子
        self.warmup_proportion = 0.1                                                            # Proportion of training to perform linear learning rate warmup for.
        self.k_fold = 5
        # logging
        self.is_logging2file = True
        self.logging_dir = absdir + '/logging' + '/' + self.task + '/' + self.models_name
        # save
        self.load_save_model = False
        self.save_path = absdir + '/model_saved' + '/' + self.task
        self.dev_split = 0.1
        self.test_split = 0.1
        self.seed = 369
        # 增强数据
        self.data_augment = True
        self.data_augment_args = 'themword'


def thucNews_task(config):

    if config.device.type == 'cuda':
        torch.cuda.set_device(config.device_id)

    random_seed(config.seed)

    tokenizer = BertTokenizer.from_pretrained(config.tokenizer_file,
                                              do_lower_case=config.do_lower_case)
    processor = TryDataProcessor()
    config.class_list = processor.get_labels()
    config.num_labels = len(config.class_list)

    total_examples = processor.get_train_examples(config.data_dir)
    # 划分训练集（做K折）和测试集
    train_examples, test_examples = train_test_split(config, total_examples)

    logging.info("self config %s", config_to_json_string(config))

    model = Bert(config)
    if config.load_save_model:
        model_load(config, model, device='cpu')

    dev_ev, predict = k_fold_cross_validation(
        config, train_examples, model, tokenizer,
        train_enhancement=DataAugment().dataAugment if config.data_augment else None,
        enhancement_arg=config.data_augment_args,
        test_examples=test_examples)


if __name__ == '__main__':

    config = NewsConfig()
    logging_filename = None
    if config.is_logging2file is True:
        file = time.strftime('%Y-%m-%d_%H-%M-%S') + '.log'
        logging_filename = os.path.join(config.logging_dir, file)
        if not os.path.exists(config.logging_dir):
            os.makedirs(config.logging_dir)

    logging.basicConfig(filename=logging_filename, format='%(levelname)s: %(message)s', level=logging.INFO)

    thucNews_task(config)

