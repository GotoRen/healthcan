####################################
### Created by K18039-後藤 廉
### Created by K18100-棟安 舞
####################################
### 内容：ユニットテスト
### ファイル：test_healthcan.py
####################################

# ユニットテスト
import unittest
import copy
from unittest import mock
# 親クラス(healthcan.py)の読み込み
from model.healthcan import healthcan
# 現在日時の取得
import datetime
import pytz
# 算術演算ライブラリ
import decimal
from _pydecimal import Decimal
# プロジェクトの読み込み
# from model.project_healthcan import project
from model.project import project



class test_healthcan(unittest.TestCase):


    # DB 作成テスト
    # 正しい値を持ったインスタンスを作成しデータベースに登録する
    def setUp(self):
        self.hc = healthcan()
        now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        # idはAUTO_INCREMENT
        self.hc.attr["user_id"] = 2
        self.hc.attr["name"] = "愛工太郎"
        self.hc.attr["date"] = '{0:%Y-%m-%d}'.format(now.date())
        self.hc.attr["time"] = '{0:%H:%M:%S}'.format(now.time())
        self.hc.attr["height"] = Decimal(175.0)
        self.hc.attr["weight"] = Decimal(68.0)
        self.hc.attr["bmi"] = Decimal(22.2)          # 身長175.0cm, 体重68.0kg　におけるBMI：22.2
        self.hc.attr["pro_weight"] = Decimal(67.38)  # 身長175.0cm, 体重68.0kg　における適正体重：67.38kg
        self.hc.attr["diff_weight"] = Decimal(0.63)  # 身長175.0cm, 体重68.0kg　における差体重：0.63kg

        # project.nameを書き換えておくことでテスト用のDBを利用する
        patcher = mock.patch('model.project_healthcan.project.name', return_value="test_healthcan")
        self.mock_name = patcher.start()
        self.addCleanup(patcher.stop)
        healthcan.migrate()
        self.hc.save()


    # テストが終わるたびにテスト用DBをクリア
    def tearDown(self):
        healthcan.db_cleaner
        

    # No.1
    def test_db_is_working(self):
        hc = healthcan.find(self.hc.attr["id"])
        # findで帰ってきているのがidならDBに保存されている
        self.assertTrue(type(hc) is healthcan)
        # 最初のデータなのでidは1になる
        self.assertTrue(hc.attr["id"] == 1)


    # No.2
    # attrが正しい値を持っている
    def test_is_valid(self):
        self.assertTrue(self.hc.is_valid())


    # No.3
    # attrが間違った値を持っているかをチェックする関数のテスト
    def test_is_valid_with_invalid_attrs(self):
        
        # id must be None or a int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = None
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["id"] = 1
        self.assertTrue(hc_wrong.is_valid())
        
        # user_id must be a int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["user_id"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # name must be a string 
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["name"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # date must be not None and string and int
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["date"] = 1
        self.assertTrue(hc_wrong.is_valid())

        # time must be not None
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = "1"
        self.assertTrue(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["time"] = 1
        self.assertTrue(hc_wrong.is_valid())
        
        # height must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["height"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["height"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["height"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["weight"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["weight"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["weight"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # bmi must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["bmi"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["bmi"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["bmi"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # pro_weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["pro_weight"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["pro_weight"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["pro_weight"] = 1
        self.assertFalse(hc_wrong.is_valid())

        # diff_weight must be a Desimal
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["diff_weight"] = None
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["diff_weight"] = "1"
        self.assertFalse(hc_wrong.is_valid())
        hc_wrong = copy.deepcopy(self.hc)
        hc_wrong.attr["diff_weight"] = 1
        self.assertFalse(hc_wrong.is_valid())


    # No.4
    # default値を持ったhealthcanインスタンスを生成する
    # Controlerで入力フォームを作るのにも利用する
    def test_build(self):
        hc = healthcan.build()
        self.assertTrue(type(hc) is healthcan)


##############################################
# これ以降にユニットテストを追加してください（後藤）


    # No.5
    def test__index(self):
        self.assertEqual(len(healthcan._index(2)), 1)
        self.assertEqual(healthcan._index(2)[0], 1)



if __name__ == '__main__':
    # unittestを実行
    unittest.main()
