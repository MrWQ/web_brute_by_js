#!/usr/bin/python3
# -*- coding: utf-8 -*-
import execjs
import linecache
import multiprocessing as mp

js_data = """
 function encrypt(vword){
			  var key = CryptoJS.enc.Utf8.parse('abcdefgabcdefg12');
			  var iv = CryptoJS.enc.Utf8.parse('abcdefgabcdefg12');
			   
			   var srcs = CryptoJS.enc.Utf8.parse(vword);
			 //  console.log(iv);
			   var encrypted = CryptoJS.AES.encrypt(srcs, key, {
			      iv: iv,
			      mode: CryptoJS.mode.CBC,
			      padding: CryptoJS.pad.Pkcs7
			   });
			  
			  ss = encrypted.ciphertext.toString().toUpperCase();
			  return ss;
			   
			}
			
"""
######################################################################################
#######  加密部分 获取js加密方法
with open('aes.js', 'r', encoding='utf8') as js_file:
    js = js_file.read()
    js_func = execjs.compile(js + js_data)      #######1. 将js编译
    print('+ 测试js方法：' + js_func.call('encrypt', 'admin')) #测试，测试通过后修改2

# ###### 加密部分 调用js对明文加密
def encrypt_line(line):
    line = line.replace('\n', '')
    line = js_func.call('encrypt', line)  #######2. 加密，调用js方法
    return line

# 多进程加密，提高效率
def mp_job(input_lines):
    pool = mp.Pool()                                # 创建进程池，默认为cpu线程数
    results = pool.map(encrypt_line, input_lines)   # 自动给进程分配任务,并将执行结果保存为results列表
    return results


# 将文件编码改为utf-8
# 改变文件编码utf-8 防止gbk编码文件无法打开
def encodeFile(path):
    # 改变文件编码utf-8 防止gbk编码文件无法打开
    fp = open(path, 'rb')
    fps = fp.read()
    fp.close()
    try:
        fps = fps.decode('utf-8')
        print('当前文件编码为 utf-8,无需修改编码')
    except:
        fps = fps.decode('gbk')
        print('当前文件编码为 gbk,正在修改编码...')
    fps = fps.encode('utf-8')
    fp = open(path, 'wb')
    fp.write(fps)
    fp.close()
    print('当前文件编码为 utf-8')
######################################################################################


print('+ 创建进程：' + str(mp.current_process()))

if __name__ == '__main__':
    input_dict = '10W.dict.txt'  #######3. 明文字典路径
    output_dict = '10w1.txt'  #######4. 密文字典路径

    print('+ 明文路径： ' + input_dict)
    print('+ 密文路径： ' + output_dict)
    print('+ 加密中...')
    input_lines = linecache.getlines(input_dict)
    result_list = mp_job(input_lines)
    with open(output_dict, 'a') as f:
        for i in result_list:
            f.write(i + '\n')

