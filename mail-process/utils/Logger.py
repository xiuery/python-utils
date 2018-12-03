# coding=utf-8
__author__ = 'xiuery.com'

import logging.handlers

# 初始化
# logging.basicConfig()

# 创建logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 写入日志文件
logfile = 'log/mail-process.log'
file_handle = logging.handlers.TimedRotatingFileHandler(logfile, 'D', 1, encoding='utf-8')
file_handle.setLevel(logging.INFO)

# 输出到控制台
stream_handle = logging.StreamHandler()
stream_handle.setLevel(logging.INFO)

# handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_handle.setFormatter(formatter)
stream_handle.setFormatter(formatter)

# logger添加到handler
logger.addHandler(file_handle)
logger.addHandler(stream_handle)
