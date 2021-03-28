# -*- coding:utf-8 -*-
import os
import logging
import smtplib
import datetime
import win32com.client as win32
from email.message import EmailMessage
from basepath import get_base_path
from controler.getenvconfig import get_email_config


logger = logging.getLogger(__name__)
# 实例化读取配置文件
config = get_email_config()
# 测试报告的附件
mail_path = os.path.join(get_base_path(), 'report', 'report.html')


class SendEmail:
    def __init__(self):
        self.sever = config.get('smtp_sever')
        self.mail_from = config.get('from_addr')
        self.mail_pw = config.get('password')
        self.mail_to = config.get('to_addr')
        self.subj = config.get('subject')

    def qq_email(self):

        # 创建SMTP连接
        conn = smtplib.SMTP_SSL(self.sever, 465)
        conn.set_debuglevel(1)
        conn.login(self.mail_from, self.mail_pw)

        # 创建邮件对象
        msg = EmailMessage()

        # 设置邮件内容
        with open(mail_path, 'r')as f:
            msg.set_content(f.read(), 'html', 'utf-8')

        msg['subject'] = self.subj
        msg['from'] = '接口测试<%s>' % self.mail_from
        msg['to'] = '罗楠163<%s>' % self.mail_to

        # 添加附件
        with open(mail_path, 'rb')as f:
            msg.add_attachment(f.read(), maintype='application',
                               subtype='html', filename='report.html')

        # 发送邮件
        try:
            conn.sendmail(self.mail_from, [self.mail_to], msg.as_string())
            logger.info("邮件发送成功")
        except smtplib.SMTPException:
            logger.info("Error: 无法发送邮件")

        # 推出链接
        conn.quit()


def outlook(mail_path, address, cc):
    """
    # outlook 发送邮件
    :param mail_path:
    :param address:
    :param cc:
    :return:
    """
    look = win32.Dispath("outlook.Application")
    mail = look.CreateItem(0)
    mail.To = address
    mail.Cc = cc
    current_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d')
    attachment_name = "report{}.html".format(current_date)

    mail.Subject = "自动化测试报告-{}".format(current_date)
    mail.Attachments.Add(mail_path, 1, 1, attachment_name)
    with open(mail_path, 'r', True,  encoding='utf-8') as f:
        html = f.read()

    mail.BodyFormat = 2    # 2: html
    mail.HTMLBody = html

    mail.Send()


if __name__ == '__main__':
    SendEmail().qq_email()
    print('测试邮件已发送，请查看邮件，谢谢')