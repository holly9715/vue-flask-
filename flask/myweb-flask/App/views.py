from flask import Blueprint, jsonify, request,send_from_directory,make_response


from .models import *
from flask_jwt_extended import create_access_token
import os, base64
from datetime import datetime
from werkzeug.utils import secure_filename
from App.lpdr.lpdr import lp_img_preprocess, lp_refer, lp_postprocess, lp_generate_result
from App.ppocrv3.ppocrv3 import pp_img_preprocess, pp_refer, pp_postprocess, pp_generate_result
from flask import current_app

blue = Blueprint('user', __name__)


def get_table_columns(tablename='part_inventory'):
    # 获取所有模型（表）
    tables = db.metadata.tables
    # 遍历表并打印列名
    # print(tables)
    for table_name, table in tables.items():
        if table_name == tablename:
            # print(f"Table: {table_name}")
            columns = [column.name for column in table.columns]
            # print(f"Columns: {columns}")
            return columns


def formatFileSize(size):
    if (size < 1024):
        return '%d B'%size
    elif (size < 1024 * 1024):
        return '%d KB'%(size/1024)
    else:
        return '%d MB'%(size/1024/1024)

def formatDate(date):
    return datetime.fromtimestamp(date).strftime('%Y-%m-%d')

def list_directory(path):
    """ 递归列出目录中的所有文件和子目录 """
    items = []
    # now=datetime.now()
    # now=f" {now.year}-{now.month}-{now.day}"
    # print(os.listdir(path))
    # temp_list=sorted(os.listdir(path),key=lambda i : i['isDir'])
    temp_list=[]
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            items.append({
                'name': item,
                'isDir': True,
                'size': formatFileSize(os.path.getsize(full_path)) if not os.path.isdir(full_path) else None,
                'uploadTime': formatDate(os.path.getmtime(full_path)),
                'path': full_path,
                'children': list_directory(full_path)  # 递归调用
            })
        else:
            temp_list.append({
                'name': item,
                'size': formatFileSize(os.path.getsize(full_path)) if not os.path.isdir(full_path) else None,
                'uploadTime': formatDate(os.path.getmtime(full_path)),
                'path':full_path
            })
    items.extend(temp_list)
    return items



print(list_directory(r"public"))


@blue.route('/')
def test():
    response = make_response(send_from_directory(directory='../public', path='253.txt'))
    response.headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename('253.txt')
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@blue.route('/test/', methods=['GET'])
def index():
    print("内部函数",os.getcwd())
    return jsonify({
        'code': 0,
        'data': {
            'data': "flask + vue3 成功连通（跨域）！"
        }
    })


@blue.route('/users/login/', methods=['GET', 'POST'])
def user_login():
    vue_username = request.form.get('username')
    vue_password = request.form.get('password')

    u = User()
    flask_username = list(User.query.filter(User.username == vue_username))
    flask_password = list(User.query.filter(User.username == vue_username).filter(User.password == vue_password))

    res = 'vx.jpg'
    img_data = open(os.path.join('App/static/img/resource/others/', str(res)), "rb").read()
    img_data = base64.b64encode(img_data).decode('utf-8')

    if flask_username and flask_password:
        flask_username = flask_username[0].username
        access_token = flask_password[0].access_token
        flask_identity = flask_password[0].identity
        token = access_token
        res = jsonify({
            "success": True,
            "state": 1,
            "message": "登录成功",
            "content": {
                "access_token": token,
                "token_type": "string",
                "img_data": img_data,
                "username": flask_username,
                "identity": flask_identity
            }
        })
        return res
    else:
        res = jsonify({
            'success': False
        })
        return res

print(os.getcwd())
@blue.route('/users/register/', methods=['GET', 'POST'])
def user_register():
    vue_username = request.form.get('username')
    vue_password = request.form.get('password')

    u = User()
    flask_username = list(User.query.filter(User.username == vue_username))
    flask_password = list(User.query.filter(User.username == vue_username).filter(User.password == vue_password))
    if (flask_username):
        res = jsonify({
            'success': False
        })
        print('用户名已存在')
    else:
        if vue_username == 'admin-car':
            vue_identity = '超级管理员'
            u.identity = vue_identity
        else:
            vue_identity = '普通用户'
            u.identity = vue_identity

        u.username = vue_username
        u.password = vue_password
        token = create_access_token(identity=vue_username)
        u.access_token = token
        #加头像
        # res = 'vx.jpg'
        # img_data = open(os.path.join('App/static/img/resource/others/', str(res)), "rb").read()
        # img_data = base64.b64encode(img_data).decode('utf-8')

        try:
            db.session.add(u)
            db.session.commit()
            res = jsonify({
                "success": True,
                "state": 1,
                "message": "注册成功",
                "content": {
                    "access_token": token,
                    "token_type": "string",

                    "username": vue_username,
                    "identity": vue_identity
                }
            })
            print('注册')
            return res
        except Exception as e:
            print(e)
            print('数据库有问题')
            db.session.rollback()
            db.session.flush()
            res = jsonify({
                'success': False,
                'state': 0,
                'message': '注册失败',
                "content": {
                    "access_token": 'null',
                    "token_type": "null"
                }
            })
    return res


@blue.route('/users/logout/', methods=['POST'])
def user_logout():
    res = jsonify({
        'success': True,
        'state': 1,
        'message': '退出成功',
        "content": {
            "access_token": '不需要返回',
            "token_type": "不需要返回"
        }
    })
    return res


@blue.route('/users/getAll/', methods=['GET'])
def user_getAll():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arr = []
    for i in range(len(User.query.all())):
        temp = []
        user_id = User.query.all()[i].id
        temp.append(user_id)
        user_identity = User.query.all()[i].identity
        temp.append(user_identity)
        user_username = User.query.all()[i].username
        temp.append(user_username)
        user_password = User.query.all()[i].password
        temp.append(user_password)
        access_token = User.query.all()[i].access_token
        temp.append(access_token)
        arr.append(temp)

    res = []
    for i in range(len(arr)):
        tp = {
            'id': arr[i][0],
            'identity': arr[i][1],
            'username': arr[i][2],
            'password': arr[i][3],
            'token': arr[i][4]
        }
        res.append(tp)

    result = jsonify({
        'code': '000000',
        'data': res,
        'message': '处理成功',
        'time': now_time
    })
    return result


@blue.route('/users/delete/<string:id>', methods=['DELETE'])
def user_del(id):
    u = User.query.get(id)
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        db.session.delete(u)
        db.session.commit()
        result = jsonify({
            'code': '000000',
            'data': True,
            'message': '处理成功',
            'time': now_time
        })
        return result
    except:
        db.session.rollback()
        db.session.flush()
        result = jsonify({
            'code': '111111',
            'data': False,
            'message': '处理失败',
            'time': now_time
        })
        return result
from App.utils import *
from PIL import Image
import io
@blue.route('/users/car/upload/', methods=['GET', 'POST'])
def user_car_upload():
    file=request.files.get('file')
    filename = secure_filename(file.filename)
    print(file)
    image = Image.open(io.BytesIO(file.read()))
    isFault= detect_part(image)
    return jsonify({'isFault':isFault,'success':True}),200

#car
@blue.route('/users/upload/', methods=['GET', 'POST'])
def user_upload():
    rec_ = []
    if request.method == 'POST':
        file = request.files.get('file')
        if file is not None:
            filename = secure_filename(file.filename)
            print("filename", filename)
            data = request.form.get('data')
            img_path = 'App/static/img/resource/' + str(data) + '/' + filename
            file.save(img_path)
            infer_result = 'App/static/img/dest/' + str(data) + '/result_' + filename
            if data == 'lpdr':
                try:
                    img = open(img_path, 'rb').read()
                    pre_img, ratio_h, ratio_w, src_h, src_w = lp_img_preprocess(img)
                    prob = lp_refer(pre_img)
                    post_result = lp_postprocess(prob, ratio_h, ratio_w, src_h, src_w)
                    rec_res = lp_generate_result(img_path, post_result, infer_result)
                    for i in range(len(rec_res)):
                        rec_.append(rec_res[i][0])
                    img_data = open(infer_result, "rb").read()
                    img_data = base64.b64encode(img_data).decode('utf-8')
                    res = jsonify({
                        "success": True,
                        "state": 1,
                        "message": "推理成功",
                        "content": {
                            "img_data": img_data,
                            'rec_result': rec_
                        }
                    })
                    return res
                except:
                    res = jsonify({
                        "success": False,
                        "state": 0,
                        "message": "图片中有效目标为零",
                        "content": {
                            "img_data": 'null',
                        }
                    })
                    return res
            if data == 'ppocrv3':
                try:
                    img = open(img_path, 'rb').read()
                    pre_img, ratio_h, ratio_w, src_h, src_w = pp_img_preprocess(img)
                    prob = pp_refer(pre_img)
                    post_result = pp_postprocess(prob, ratio_h, ratio_w, src_h, src_w)
                    rec_res = pp_generate_result(img_path, post_result, infer_result)
                    for i in range(len(rec_res)):
                        rec_.append(rec_res[i][0])
                    img_data = open(infer_result, "rb").read()
                    img_data = base64.b64encode(img_data).decode('utf-8')
                    res = jsonify({
                        "success": True,
                        "state": 1,
                        "message": "推理成功",
                        "content": {
                            "img_data": img_data,
                            'rec_result': rec_
                        }
                    })
                    return res
                except:
                    res = jsonify({
                        "success": False,
                        "state": 0,
                        "message": "图片中有效目标为零",
                        "content": {
                            "img_data": 'null',
                        }
                    })
                    return res
            else:
                res = jsonify({
                    "success": True,
                    "state": 1,
                    "message": "图片中有效目标为零",
                    "content": {
                        "img_data": 'null',
                        'rec_result': "car"
                    }
                })
                return res
        else:
            res = jsonify({
                "success": False,
                "state": 0,
                "message": "后端接收不到图片",
                "content": {
                    "img_data": 'null',
                }
            })
            return res
    else:
        res = jsonify({
            "success": False,
            "state": 0,
            "message": "请求方法应为POST",
            "content": {
                "img_data": 'null',
            }
        })
        return res

@blue.route('/users/part_inventory/data/<id>', methods=["DELETE"])
def deleteStock(id):
    print('删除')
    p = PartInventory.query.get(int(id))
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        db.session.delete(p)
        db.session.commit()
        result = jsonify({
            'success':True,
            'data': True,
            'message': '处理成功',
            'time': now_time
        })
        print('suc')
        return result
    except Exception as e:
        print(e)
        print('处理失败')
        db.session.rollback()
        db.session.flush()
        result = jsonify({
            'success': False,
            'data': False,
            'message': '处理失败',
            'time': now_time
        })
        return result


@blue.route('/users/part_inventory/data', methods=['GET', 'POST'])
def fetch_invetory_data():
    if request.method=='GET':
        columns = get_table_columns()
        data = []
        d = PartInventory().query.all()
        data = [{'id': i.id
                    , '配件编号': i.配件编号
                    , '配件名': i.配件名
                    , '可用库存': i.可用库存
                    , '待检库存': i.待检库存
                    , '供应商': i.供应商
                    , '库存上限': i.库存上限
                    , '库存下限': i.库存下限
                    , '时间': i.时间
                 } for i in d]
        res = {'columns': columns, 'data': data}
        # print('jie')

        return jsonify(res)
    if request.method=='POST':
        data = request.form
        print(type(data))
        print(data)
        print("接收到的数据:")
        for key, value in data.items():
            print(f"{key}: {value}")
        stockform=PartInventory()
        # stockform.时间=request.form.get('时间')

        stockform.可用库存=request.form.get('可用库存')
        stockform.库存上限=request.form.get('库存上限')
        stockform.库存下限=request.form.get('库存下限')
        stockform.供应商="公司拟还"
        stockform.待检库存=request.form.get('待检库存')
        stockform.配件名=request.form.get('配件名')
        stockform.配件编号=request.form.get('配件编号')
        print(request.form.get('配件编号'))

        try:
            print(stockform.配件编号)
            db.session.add(stockform)
            db.session.commit()
            res = jsonify({
                'success': True,
            })

            return res

        except Exception as e:
            print(e)
            db.session.rollback()
            db.session.flush()
            res = jsonify({
                'success': False,
            })
            return res



# os.mkdir('zhende')
@blue.route('/users/share/upload', methods=['GET', 'POST'])
def upload():
    # upload_folder = current_app.config['UPLOAD_FOLDER']
    # print(request.files.path)
    # a=request
    # print(request.files.file)
    # print('laji')
    if request.method=="GET":

        fullpath=str(request.args.get('path'))
        print(fullpath)
        dirname=request.args.get('dirname')
        print(dirname)
        fullpath=os.path.join(fullpath,dirname)
        try:
            print(fullpath)
            os.mkdir(fullpath)
        except Exception as e:
            print(e)

        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        path=request.form['path']
        print(path)
        if 'file' not in request.files:

            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':

            return jsonify({'error': 'No selected file'}), 400
        #file = request.files.get('file')
        # if file is not None:
        if file:
            filename = file.filename
            full_path = os.path.join( path , filename)
            print(full_path)
            file.save(full_path)
            return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200


@blue.route('/users/share/download/<path:file_path>', methods=['GET'])
def download(file_path):
    # print('xia')
    # file_path = request.form.get('path')
    # print(file_path)
    if not os.path.isfile(file_path):
        return "File not found", 404
    temp=file_path.split('/')
    filename=str(temp[-1])
    dir='/'.join(temp[:-1])
    dir='../'+dir
    print(filename,dir)
    # print(os.getcwd())

    response = make_response(send_from_directory(directory=dir, path=filename))
    response.headers['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

import shutil

@blue.route('/users/share/delete', methods=['POST'])
def delete_file():
    # 获取文件名
    file_path = request.form.get('path')
    # print('shan')
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    # 删除文件
    try:
        print(file_path)
        if(os.path.isdir(file_path)):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
        return jsonify({'message': f'File deleted successfully'}) , 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 500
# os.getcwd()
@blue.route('/users/share/getfiles', methods=['GET'])
def get_files():
    directory_path = 'public'  # 修改为你的public目录路径
    files_and_dirs = list_directory(directory_path)
    return jsonify(files_and_dirs)

@blue.route('/users/getModel', methods=['GET','POST'])
def get_model():
    folder_path = 'model/global_model'
    file_name = [os.path.basename(f) for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]
    if request.method=='GET':

        print(file_name)
        return jsonify({'filename':file_name[0]}),200
    elif request.method=='POST':
        print('psot')
        # response = make_response()
        # response.headers['Content-Disposition'] = 'attachment; filename=' + 'x.pt'
        # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
        # response.headers['Pragma'] = 'no-cache'
        # response.headers['Expires'] = '0'
        return send_from_directory(directory='../model/global_model', path=file_name[0])


@blue.route('/users/fl/uploadModel', methods=['GET','POST'])
def uploadModel():
    # print('upload')
    file = request.files.get('file')
    filename = secure_filename(file.filename)
    # file = request.files['file']
    path='model/local_model/'+filename
    print(file)
    file.save(path)
    return jsonify({'message': 'File uploaded successfully'}), 200

