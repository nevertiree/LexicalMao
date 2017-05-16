# -*- coding:gb2312 -*-

import os

import thulac


def data_clean(raw_line):
    return raw_line.strip().replace(" ", "")


# �������
def split_article(volume_path, volume_name, result_dir_path):
    file_index = 1
    with open(volume_path + volume_name, 'r') as raw_f:
        # ���ļ�
        new_file = []
        # ѭ������
        while 1:
            # ȥ���ո�
            line = raw_f.readline()
            # ����Ƿǿ��оͲ���
            if line:
                # �����---����ֹ �� д���ļ���
                if "---------------" in line or "��������������" in line:
                    print(new_file[0])
                    with open(result_dir_path + "%s-%s.txt" % (volume_name, str(file_index)), 'w') as new_f:
                        for _ in new_file:
                            if _.replace(" ", "") != "":
                                new_f.write(_)
                    new_file = []
                    file_index += 1
                else:
                    # ���û�оʹ洢
                    if line.replace(" ", "") != "":
                        new_file.append(line)
            else:
                break


def split_word(article_path, article_name, result_dir_path):
    print("Trans Lexical txt-%s" % article_name)
    thu = thulac.thulac(seg_only=True, filt=True)
    thu.cut_f(article_path + article_name, result_dir_path + article_name)


def clean_article(article_dir, n_article_dir):
    article_list = list(os.walk(article_dir))[0][2]
    for article in article_list:
        # ���ı�
        print("Read txt-%s" % article)
        with open(article_dir + article, "r") as rf:
            raw_data = rf.readlines()

        # ��ϴ�ı�
        print("Clean txt-%s" % article)
        clean_data = [data_clean(line) for line in raw_data]

        # д����ϴ����
        print("Write Clean Data txt-%s" % article)
        with open(n_article_dir + article, "w") as wf:
            for item in clean_data:
                wf.write(item)

#     # �ִ�
#     print("Trans Lexical txt-%s" % index)
#     thu.cut_f("mao\\%s-clean.txt" % index, "mao\\%s-out.txt" % index)


if __name__ == '__main__':
    # ��һ�����Ϊ���ɸ�����
    raw_volume_dir = "mao\\raw_volume\\"
    raw_article_dir = "mao\\raw_article\\"
    clean_article_dir = "mao\\clean_article\\"
    new_article_dir = "mao\\new_article\\"

    raw_volume_list = list(os.walk(raw_volume_dir))[0][2]
    raw_article_list = list(os.walk(raw_article_dir))[0][2]
    clean_article_list = list(os.walk(clean_article_dir))[0][2]

    # for volume in raw_volume_list:
    #     split_article(raw_volume_dir, volume_name=volume, result_dir_path=raw_article_dir)

    # clean_article(raw_article_dir, clean_article_dir)

    # �ִ�
    for a in clean_article_list:
        split_word(clean_article_dir, article_name=a, result_dir_path=new_article_dir)
