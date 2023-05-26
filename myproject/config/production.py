# 서버 환경을 담당
# 데이터베이스 설정은 유지

from config.default import *

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = b'\x18o\x7f`\xe6\x8b\\\xbfD\xd1\xa8\xdd\x85:\xeeh'