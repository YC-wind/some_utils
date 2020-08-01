import os
import re
import time
import json
import traceback
import stat
import paramiko
import shutil

HOST = "host"
USER = "user"
PASSWORD = "password"
PORT = "port"
__PATH__ = os.getcwd()
ORIGIN_PATH = "path"


class SftpServer(object):
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sftp = paramiko.SSHClient()
        self.sftp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__connect()

    def __connect(self):
        try:
            self.sftp.connect(hostname=self.host, port=self.port, username=self.username, password=self.password)
        except:
            self.sftp.connect(hostname=self.host, port=self.port, username=self.username, password=self.password,
                              look_for_keys=False, allow_agent=False)

    def close(self):
        self.sftp.close()

    def put_file(self, local_path, remote_path):
        '''
        利用sftp服务上传文件
        :param local_path:
        :param remote_path:
        :return:
        '''
        if not os.path.exists(local_path):
            print(f"{local_path} not exits!")
            return False
        sftp_client = self.sftp.open_sftp()
        filename = os.path.basename(local_path)
        print('正在上传：{} 到 {}'.format(filename, remote_path))
        try:
            sftp_client.put(local_path, remote_path, callback=self.__callback_function)  # 上传文件要传完整路径
        except:
            traceback.print_exc()
            pass
        finally:
            sftp_client.close()

    def __upload_dir(self, sftp_client, local_path, remote_path):
        for file in os.listdir(local_path):
            # 资源路径
            filepath = os.path.join(local_path, file)

            # 判断资源文件类型
            if os.path.isfile(filepath):
                # 1.文件
                sftp_client.put(filepath, os.path.join(remote_path, file), callback=self.__callback_function)
                # self.put_file(filepath, os.path.join(remote_path, file))
            elif os.path.isdir(filepath):

                # 2.目录
                try:
                    # filepath 修改为 os.path.join(remote_path, file)
                    sftp_client.chdir(os.path.join(remote_path, file))
                except Exception as e:
                    print(e)
                    # remote_path
                    sftp_client.mkdir(os.path.join(remote_path, file))
                    sftp_client.chdir(os.path.join(remote_path, file))
                self.__upload_dir(sftp_client, filepath, os.path.join(remote_path, file))
            ### 重置数据
            # 返回上一层目录
            sftp_client.chdir('..')

    def put_dir(self, local_path, remote_path):
        '''
        利用sftp服务上传文件夹
        :param local_path:
        :param remote_path:
        :return:
        '''
        if not os.path.exists(local_path):
            print(f"{local_path} not exits!")
            return False
        sftp_client = self.sftp.open_sftp()
        try:
            sftp_client.mkdir(remote_path)
        except:
            pass
        try:
            self.__upload_dir(sftp_client, local_path, remote_path)
        except:
            traceback.print_exc()
            pass
        finally:
            sftp_client.close()

    def get_file(self, remote_path, local_path):
        '''
        利用sftp服务下载文件
        :param remote_path:
        :param local_path:
        :return:
        '''
        sftp_client = self.sftp.open_sftp()
        try:
            sftp_client.get(remote_path, local_path)
        except:
            traceback.print_exc()
            os.remove(local_path)
            pass
        finally:
            sftp_client.close()

    def get_dir(self, remote_path, local_path):
        '''
        下载远程文件夹
        :param remote_path:
        :param local_path:
        :return:
        '''
        sftp_client = self.sftp.open_sftp()
        try:
            self.__download_dir(sftp_client, remote_path, local_path)
        except:
            traceback.print_exc()
            print(local_path)
            shutil.rmtree(local_path)
            pass
        finally:
            sftp_client.close()

    def __download_dir(self, sftp_client, remote_path, local_path):
        os.makedirs(local_path, exist_ok=True)
        # try:
        dir_items = sftp_client.listdir_attr(remote_path)
        # except:
        #     _ = f"{remote_path} not exit"
        #     print(_)
        #     return
        for item in dir_items:
            remote_child_path = os.path.join(remote_path, item.filename)
            local_child_path = os.path.join(local_path, item.filename)
            if stat.S_ISDIR(item.st_mode):
                self.__download_dir(sftp_client, remote_child_path, local_child_path)
            else:
                sftp_client.get(remote_child_path, local_child_path)

    def __callback_function(self, current_size, size):
        '''
        put的回调函数
        :param current_size: 当前上传大小
        :param size: 总大小
        :return:
        '''
        if current_size == size:
            print('File uploaded successfully!')

    def make_dir(self, remote_path):
        '''
        利用sftp服务上传文件夹
        :param remote_path:
        :return:
        '''
        sftp_client = self.sftp.open_sftp()
        try:
            print(remote_path)
            sftp_client.mkdir(remote_path)
        except:
            traceback.print_exc()
            pass
        finally:
            sftp_client.close()

    def del_file(self, remote_path):
        '''
        删除远程目录文件
        :param remote_path:
        :return:
        '''
        sftp_client = self.sftp.open_sftp()
        try:
            print(remote_path)
            sftp_client.remove(remote_path)
        except:
            traceback.print_exc()
            pass
        finally:
            sftp_client.close()

    def del_dir(self, remote_path):
        '''
        删除远程目录文件夹，递归删除
        :param remote_path:
        :return:
        '''
        sftp_client = self.sftp.open_sftp()
        try:
            print(remote_path)
            self.__delete_dir(sftp_client, remote_path)
        except:
            traceback.print_exc()
            pass
        finally:
            sftp_client.close()

    def __delete_dir(self, sftp_client, remote_path):
        files = sftp_client.listdir_attr(path=remote_path)
        for f in files:
            remote_child_path = os.path.join(remote_path, f.filename)
            if stat.S_ISDIR(f.st_mode):
                self.__delete_dir(sftp_client, remote_child_path)
            else:
                sftp_client.remove(remote_child_path)
        sftp_client.rmdir(remote_path)


if __name__ == "__main__":
    sftp = SftpServer(HOST, USER, PASSWORD, PORT)
    try:
        sftp.make_dir(f"{ORIGIN_PATH}/")
    except Exception as e:
        traceback.print_exc()
        print(repr(e))
        pass

    sftp.make_dir(f"{ORIGIN_PATH}/test")

    os.chdir(__PATH__)

    sftp.put_file(f'files/demo.xmind',
                  f"./{ORIGIN_PATH}/demo.xmind")

    sftp.put_dir(f'files',
                 f"./{ORIGIN_PATH}/files")

    sftp.get_file(f"./{ORIGIN_PATH}/demo.xmind",
                  f"demo.xmind")

    sftp.get_dir(f"./{ORIGIN_PATH}/files",
                 f"./{ORIGIN_PATH}/files2")

    # 测试 重复删除 文件夹
    sftp.del_dir(f"./{ORIGIN_PATH}/files")
    # 测试 重复删除 文件
    sftp.del_file(f"./{ORIGIN_PATH}/demo.xmind")
    #
    sftp.close()
