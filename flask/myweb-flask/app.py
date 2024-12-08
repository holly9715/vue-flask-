from App import create_app
from App.utils import Autoencoder
app = create_app()
UPLOAD_FOLDER = 'public'  # 假设这是你的public目录
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if __name__ == '__main__':
    #FIXME
    app.run(debug=True)
