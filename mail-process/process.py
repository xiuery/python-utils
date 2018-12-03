# coding=utf-8

import os
import uuid
import email
from utils.Logger import logger
from imapclient import IMAPClient


IMAP_CONFIG = {
    "host": '',
    "username": '',
    "password": '',
    'port': 993
}

MAIL_PATH = {
    "destination": "已发送邮件",
}


class Process(object):
    # 邮件附件的存储路径
    path = 'files'

    def __init__(self):  # 初始化数据
        self.logger = logger
        self.imap = IMAPClient(IMAP_CONFIG['host'], port=IMAP_CONFIG['port'], ssl=True)

    def start(self):
        """启动程序"""
        try:
            self.logger.info('start process')
            self.login(IMAP_CONFIG['username'], IMAP_CONFIG['password'])
            # 选择文件目录
            self.select_folder(MAIL_PATH['destination'], True)
            # 获取mail并解析
            self.get_mail()
        except Exception as e:
            self.logger.exception(e)
        finally:
            self.logout()

    def login(self, username, password):
        """连接邮件服务器，登录认证"""
        self.imap.login(username=username, password=password)

    def logout(self):
        """邮件退出"""
        self.imap.logout()

    def get_all_folders(self):
        folders = self.imap.list_folders()

        for folder in folders:
            self.logger.info(folder)

        return folders

    def select_folder(self, folder, readonly=True):
        """选择邮件文件夹"""
        self.imap.select_folder(folder, readonly)

    def parse_header(self, m):
        """解析header"""
        headers = dict()

        for k, v in m.items():
            if k in headers:
                if isinstance(headers[k], list):
                    headers[k].append(self.make_header(v))
                else:
                    headers[k] = [headers[k]]
                    headers[k].append(self.make_header(v))
            else:
                headers[k] = self.make_header(v)

        return headers

    @staticmethod
    def decode_header(header):
        """header 解码"""
        return email.header.decode_header(header)

    def make_header(self, header):
        """make header"""
        return email.header.make_header(self.decode_header(header)).__str__()

    @staticmethod
    def mk_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)

        return path

    def get_attache(self, m, path):
        """邮件附件下载"""
        path = self.mk_dir(path)
        filename = path + m.get_filename()

        with open(filename, 'wb') as f:
            f.write(m.get_payload(decode=True))

        return filename

    def save_content_html(self, path, filename, content):
        path = self.mk_dir(path)

        with open(path + filename, 'wb') as f:
            f.write(content)

    def parse_body(self, m):
        """解析邮件信息"""
        body = {
            'attache': list(),
            'headers': dict(),
            'content': list()
        }

        # 一个邮件生成一个uuid
        uuid_x = str(uuid.uuid1())
        path = '/'.join([self.path, uuid_x]) + '/'

        for mw in m.walk():
            filename = mw.get_filename()
            if filename:
                body['attache'].append(self.get_attache(mw, path))
            else:
                body['headers'].update(self.parse_header(mw))

                # 邮件正文
                content = mw.get_payload(decode=True)
                if not content:
                    continue

                # 获取编码
                content_type = body['headers']['Content-Type']
                encoding = content_type.split('"')[1]

                # html保存为文件
                if content_type.split(';')[0] == 'text/html':
                    self.save_content_html(path, uuid_x + '.html', content)
                    body['content'].append(path + uuid_x + '.html')
                else:
                    body['content'].append(content.decode(encoding=encoding))

        return body

    def move_mail(self, mid, folder):
        """移动mail到指定目录"""
        self.imap.move(mid, folder)

    def get_mail(self):
        """获取目标文件夹内所有的邮件"""
        result = list()

        # 测试所有的folder
        # return self.get_all_folders()

        # mails = self.imap.fetch(self.imap.search([u'TEXT', u'MSO for testing']), ['BODY.PEEK[]'])
        mails = self.imap.fetch(self.imap.search(), ['BODY.PEEK[]'])

        for mid, message in mails.items():
            m = email.message_from_string(message[b'BODY[]'].decode())
            result.append(self.parse_body(m))

        return result


if __name__ == '__main__':
    process = Process()
    process.start()
