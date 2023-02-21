import wx
import os
import time
import sqlite3

class RankCalc(wx.Frame):
    def __init__(self, parent, title):
        super(RankCalc, self).__init__(parent, title=title)

        self.val = True
        
        self.CreateDB()
        self.InitUI()

    def CreateDB(self):
        # if id nothing .db file
        if not os.path.exists('RankCalc.db'):
            # DBの作成
            self.conn = sqlite3.connect('RankCalc.db')
            c = self.conn.cursor()

            # 同盟名, 同盟戦力, 同盟撃破数, 同盟領土数, 関所数, 聖所数
            c.execute('CREATE TABLE IF NOT EXISTS Alliance_0 (alliance_name text, alliance_power int, alliance_kill int, alliance_territory int, pass int, shrine int)')
            c.execute('CREATE TABLE IF NOT EXISTS Alliance_1 (alliance_name text, alliance_power int, alliance_kill int, alliance_territory int, pass int, shrine int)')
            # 同盟名, 個人戦力
            c.execute('CREATE TABLE IF NOT EXISTS Member (alliance_name text, member_name text, member_power int)')

            # 初期データの挿入
            c.execute('INSERT INTO Alliance_0 VALUES ("同盟1", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_0 VALUES ("同盟2", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_0 VALUES ("同盟3", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_0 VALUES ("同盟4", 0, 0, 0, 0, 0)')

            c.execute('INSERT INTO Alliance_1 VALUES ("同盟1", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_1 VALUES ("同盟2", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_1 VALUES ("同盟3", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance_1 VALUES ("同盟4", 0, 0, 0, 0, 0)')

            # DBの保存
            self.conn.commit()

    def InitUI(self):
        # サイズ固定
        self.SetMaxSize((480, 330))
        self.SetMinSize((480, 330))
        # 4つの同盟のタブを作成
        self.nb = wx.Notebook(self)
        self.nb.AddPage(AlliancePanel(self.nb, '同盟1'), 'ベルモナ帝国')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟2'), 'うきょち同盟')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟3'), 'Reiyans同盟')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟4'), 'まいまい帝国')

        # タブが切り替わったときのイベント
        self.nb.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.TabChange)
        
        # ラジオボタンが押されたときのイベント
        for i in range(4):
            self.nb.GetPage(i).radio_mid.Bind(wx.EVT_RADIOBUTTON, self.UpdateAllRadio)
            self.nb.GetPage(i).radio_fin.Bind(wx.EVT_RADIOBUTTON, self.UpdateAllRadio)

    def TabChange(self, e):
        # スコアを更新
        for i in range(4):
            self.nb.GetPage(i).CalcScore()

    def UpdateAllRadio(self, e):
        # イベント取得
        event = e.GetEventObject()
        print(event.GetLabel())
        # ラジオボタンの更新
        for i in range(4):
            self.nb.GetPage(i).radio_mid.SetValue(not self.val)
            self.nb.GetPage(i).radio_fin.SetValue(self.val)


# 同盟ごとのパネル
class AlliancePanel(wx.Panel):
    def __init__(self, parent, alliance_name):
        super(AlliancePanel, self).__init__(parent)

        # 初期変数読み込み
        self.alliance_name = alliance_name
        self.table_list = ['alliance_0', 'alliance_1']

        # 初期実行関数
        self.InitUI()
        self.ConnectDB()

    def InitUI(self):
        # 同盟戦力(0以上、上限なし)
        self.alliance_power = wx.SpinCtrl(self, size=(100, -1), min=0, max=2147483647)
        # 同盟撃破数
        self.alliance_kill = wx.SpinCtrl(self, size=(100, -1), min=0, max=2147483647)
        # 同盟領土数
        self.alliance_territory = wx.SpinCtrl(self, size=(100, -1), min=0, max=2147483647)
        # 関所数
        self.pass_ = wx.SpinCtrl(self, size=(100, -1), min=0, max=100)
        # 聖所数
        self.shrine = wx.SpinCtrl(self, size=(100, -1), min=0, max=100)
        # スコア
        self.score = wx.TextCtrl(self, size=(100, -1))
        self.score.Disable()
        # 中間・最終のラジオボタン
        self.radio_mid = wx.RadioButton(self, label='中間', style=wx.RB_GROUP)
        self.radio_fin = wx.RadioButton(self, label='最終')


        # 個人戦力のスクロールバー付きリストボックス
        self.member_power = wx.ListBox(self, size=(280, 160), style=wx.LB_SINGLE | wx.LB_HSCROLL)
        # 追加テキストボックス
        self.member_power_name = wx.TextCtrl(self, size=(100, -1))
        self.member_power_val = wx.TextCtrl(self, size=(100, -1))
        # 追加ボタン
        self.member_power_add = wx.Button(self, label='追加')
        # 更新ボタン
        self.member_power_upd = wx.Button(self, label='更新')
        # 削除ボタン
        self.member_power_del = wx.Button(self, label='削除')
        

        # 同盟戦力のラベル
        alliance_power_label = wx.StaticText(self, label='同盟戦力')
        # 同盟撃破数のラベル
        alliance_kill_label = wx.StaticText(self, label='同盟撃破数')
        # 同盟領土数のラベル
        alliance_territory_label = wx.StaticText(self, label='同盟領土数')
        # 関所数のラベル
        pass_label = wx.StaticText(self, label='関所数')
        # 聖所数のラベル
        shrine_label = wx.StaticText(self, label='聖所数')
        # 個人戦力のラベル
        member_power_label = wx.StaticText(self, label='個人戦力')
        # 個人名のラベル
        member_power_name_label = wx.StaticText(self, label='名前')
        # 個人戦力のラベル
        member_power_val_label = wx.StaticText(self, label='戦力')
        # スコアのラベル
        score_label = wx.StaticText(self, label='スコア')


        # レイアウト
        # 左側のレイアウト
        vbox_left = wx.BoxSizer(wx.VERTICAL)
        vbox_left.Add(alliance_power_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.alliance_power, flag=wx.LEFT, border=10)
        vbox_left.Add(alliance_kill_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.alliance_kill, flag=wx.LEFT, border=10)
        vbox_left.Add(alliance_territory_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.alliance_territory, flag=wx.LEFT, border=10)
        vbox_left.Add(pass_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.pass_, flag=wx.LEFT, border=10)
        vbox_left.Add(shrine_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.shrine, flag=wx.LEFT, border=10)
        vbox_left.Add(score_label, flag=wx.LEFT, border=10)
        vbox_left.Add(self.score, flag=wx.LEFT, border=10)
        
        # ラジオボタンのレイアウト
        radio_box = wx.BoxSizer(wx.HORIZONTAL)
        radio_box.Add(self.radio_mid, flag=wx.LEFT, border=10)
        radio_box.Add(self.radio_fin, flag=wx.LEFT, border=10)

        # 左側のラベルにラジオボタンを付ける
        vbox_left.Add(radio_box, flag=wx.TOP, border=10)

        # 右側のレイアウト
        vbox_right = wx.BoxSizer(wx.VERTICAL)
        vbox_right.Add(member_power_label, flag=wx.LEFT, border=10)
        vbox_right.Add(self.member_power, flag=wx.LEFT, border=10)

        # 右側のラベルを付ける
        vbox_right_mod = wx.BoxSizer(wx.HORIZONTAL)
        vbox_right_mod.Add(member_power_name_label, flag=wx.LEFT, border=10)
        vbox_right_mod.Add(self.member_power_name, flag=wx.LEFT, border=10)

        vbox_right_mod.Add(member_power_val_label, flag=wx.LEFT, border=10)
        vbox_right_mod.Add(self.member_power_val, flag=wx.LEFT, border=10)

        # mod のレイアウトを追加
        vbox_right.Add(vbox_right_mod, flag=wx.TOP, border=10)

        # ボタンのレイアウト
        vbox_right_btn = wx.BoxSizer(wx.HORIZONTAL)
        vbox_right_btn.Add(self.member_power_add, flag=wx.LEFT, border=10)
        vbox_right_btn.Add(self.member_power_upd, flag=wx.LEFT, border=10)
        vbox_right_btn.Add(self.member_power_del, flag=wx.LEFT, border=10)

        # ボタンのレイアウトを追加
        vbox_right.Add(vbox_right_btn, flag=wx.TOP, border=10)

        # レイアウトのマージ
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(vbox_left, flag=wx.LEFT, border=10)
        hbox.Add(vbox_right, flag=wx.LEFT, border=10)
        self.SetSizer(hbox)


        # イベント(テキストボックス)
        self.alliance_power.Bind(wx.EVT_TEXT, self.UpdateAllianceTable)
        self.alliance_kill.Bind(wx.EVT_TEXT, self.UpdateAllianceTable)
        self.alliance_territory.Bind(wx.EVT_TEXT, self.UpdateAllianceTable)
        self.pass_.Bind(wx.EVT_TEXT, self.UpdateAllianceTable)
        self.shrine.Bind(wx.EVT_TEXT, self.UpdateAllianceTable)
        # イベント(ボタン)
        self.member_power_add.Bind(wx.EVT_BUTTON, self.EditMemberTable)
        self.member_power_upd.Bind(wx.EVT_BUTTON, self.EditMemberTable)
        self.member_power_del.Bind(wx.EVT_BUTTON, self.EditMemberTable)
        # イベント(ラジオボタン)
        self.radio_mid.Bind(wx.EVT_RADIOBUTTON, self.UpdateAllianceTable)
        self.radio_fin.Bind(wx.EVT_RADIOBUTTON, self.UpdateAllianceTable)

        # リストボックスのイベント
        self.member_power.Bind(wx.EVT_LISTBOX, self.SelectMemberTable)

    # UNIX 秒を取得     2023-02-24 18:00:00 前判定
    def CheckDate(self):
        if int(time.time()) > 1677229200:
            return False
        return True
    
    # ラジオボタンの判定
    def CheckRadio(self):
        if self.radio_mid.GetValue():
            return True
        return False
    
    # データベースの接続とデータの取得
    def ConnectDB(self):
        self.conn = sqlite3.connect('RankCalc.db')
        self.c = self.conn.cursor()
        try:
            # データの取得
            # 同盟データ(中間集計前)
            self.c.execute('SELECT * FROM alliance_0 WHERE alliance_name=?', (self.alliance_name,))
            _, alliance_power, alliance_kill, alliance_territory, pass_, shrine = self.c.fetchone()
            alliance_power_sum = alliance_power
            alliance_kill_sum = alliance_kill
            alliance_territory_sum = alliance_territory
            pass_sum = pass_
            shrine_sum = shrine

            # 中間集計以降のデータ
            self.c.execute('SELECT * FROM alliance_1 WHERE alliance_name=?', (self.alliance_name,))
            _, alliance_power, alliance_kill, alliance_territory, pass_, shrine = self.c.fetchone()
            alliance_power_sum += alliance_power
            alliance_kill_sum += alliance_kill
            alliance_territory_sum += alliance_territory
            pass_sum += pass_
            shrine_sum += shrine

            # 同盟データの表示
            self.alliance_power.SetValue(str(alliance_power_sum))
            self.alliance_kill.SetValue(str(alliance_kill_sum))
            self.alliance_territory.SetValue(str(alliance_territory_sum))
            self.pass_.SetValue(str(pass_sum))
            self.shrine.SetValue(str(shrine_sum))

            # スコア計算
            self.CalcScore()

            # メンバーデータの取得
            self.UpdateMemberPower()

        except Exception as e:
            print(e)

    # スコアの計算
    def CalcScore(self):
        total_score = 0
        score_list = [100, 80, 50, 30]
        

        for table in self.table_list:
            # 同盟戦力をランキングに変換
            self.c.execute('SELECT alliance_name, alliance_power FROM ' + table + ' ORDER BY alliance_power DESC')
            alliance_power_rank = 0
            for i, (alliance_name, alliance_power) in enumerate(self.c.fetchall()):
                if self.alliance_name == alliance_name:
                    alliance_power_rank = i
                    break

            # 同盟撃破数をランキングに変換
            self.c.execute('SELECT alliance_name, alliance_kill FROM ' + table + ' ORDER BY alliance_kill DESC')
            alliance_kill_rank = 0
            for i, (alliance_name, alliance_kill) in enumerate(self.c.fetchall()):
                if self.alliance_name == alliance_name:
                    alliance_kill_rank = i
                    break

            # 同盟領土数をランキングに変換
            self.c.execute('SELECT alliance_name, alliance_territory FROM ' + table + ' ORDER BY alliance_territory DESC')
            alliance_territory_rank = 0
            for i, (alliance_name, alliance_territory) in enumerate(self.c.fetchall()):
                if self.alliance_name == alliance_name:
                    alliance_territory_rank = i
                    break

            if self.CheckRadio() == False:
                # 関所 を取得
                self.c.execute('SELECT pass FROM ' + table + ' WHERE alliance_name=?', (self.alliance_name,))
                pass_score = self.c.fetchone()[0]
                # 聖所 を取得
                self.c.execute('SELECT shrine FROM ' + table + ' WHERE alliance_name=?', (self.alliance_name,))
                shrine_score = self.c.fetchone()[0]

                total_score += pass_score * 100
                total_score += shrine_score * 20

            # スコア計算(メンバー以外)
            total_score += score_list[alliance_power_rank]
            total_score += score_list[alliance_kill_rank]
            total_score += score_list[alliance_territory_rank]

            if self.CheckRadio():
                break

        # メンバー戦力のスコア計算
        member_power_sum = 0
        if self.CheckRadio() == False:
            # メンバー戦力から2000000以上を抽出
            member_power_score_list = [2000000, 3000000, 5000000, 10000000]
            self.c.execute('SELECT member_power FROM member WHERE member_power >= 2000000 AND alliance_name=?', (self.alliance_name,))
            member_power_list = self.c.fetchall()
            
            for member_power in member_power_list:
                if int(member_power[0]) >= member_power_score_list[3]:
                    member_power_sum += 100
                elif int(member_power[0]) >= member_power_score_list[2]:
                    member_power_sum += 50
                elif int(member_power[0]) >= member_power_score_list[1]:
                    member_power_sum += 30
                elif int(member_power[0]) >= member_power_score_list[0]:
                    member_power_sum += 20


        # スコア計算(メンバーのみ)
        total_score += member_power_sum

        RankCalc.SetRadio(self, self.CheckRadio())

        self.score.SetValue(str(total_score))

    # 同盟テーブルの更新
    def UpdateAllianceTable(self, e):
        if self.CheckDate():
            table = self.table_list[0]
        else:
            table = self.table_list[1]

        # 同盟戦力
        alliance_power = self.alliance_power.GetValue()
        # 同盟撃破数
        alliance_kill = self.alliance_kill.GetValue()
        # 同盟領土数
        alliance_territory = self.alliance_territory.GetValue()
        # 関所数
        pass_ = self.pass_.GetValue()
        # 聖所数
        shrine = self.shrine.GetValue()

        self.CalcScore()

        # 同盟名, 同盟戦力, 同盟撃破数, 同盟領土数, 関所数, 聖所数
        self.c.execute('UPDATE ' + table + ' SET alliance_power=?, alliance_kill=?, alliance_territory=?, pass=?, shrine=? WHERE alliance_name=?', (alliance_power, alliance_kill, alliance_territory, pass_, shrine, self.alliance_name))
        self.conn.commit()


    # メンバーテーブルの更新
    def EditMemberTable(self, e):
        # 個人名
        member_name = self.member_power_name.GetValue()
        # 個人戦力
        member_power = self.member_power_val.GetValue()
        # ボタン
        btn = e.GetEventObject().GetLabel()

        if member_name == '' or member_power == '':
            return

        # 重複チェック
        self.c.execute('SELECT * FROM member WHERE member_name=?', (member_name,))
        if self.c.fetchone() is not None:
            if btn == '追加' or btn == '更新':
                return

        if btn == '追加':
            # 同盟名, 個人名, 個人戦力
            self.c.execute('INSERT INTO member VALUES (?, ?, ?)', (self.alliance_name, member_name, member_power))
            self.conn.commit()
        elif btn == '更新':
            # 同盟名, 個人名, 個人戦力
            self.c.execute('UPDATE member SET member_power=? WHERE member_name=?', (member_power, member_name))
            self.conn.commit()
        elif btn == '削除':
            # 同盟名, 個人名
            self.c.execute('DELETE FROM member WHERE member_name=?', (member_name,))
            self.conn.commit()

        # リストボックスの更新
        self.UpdateMemberPower()

        # テキストボックスのクリア
        self.member_power_name.Clear()
        self.member_power_val.Clear()

    # リストボックスが選択された時の処理
    def SelectMemberTable(self, e):
        # 個人名
        member_name = self.member_power.GetStringSelection().split(':')[0]
        # 個人戦力
        member_power = self.member_power.GetStringSelection().split(':')[1]
        
        self.member_power_name.SetValue(member_name)
        self.member_power_val.SetValue(str(member_power))

    # リストボックスの更新
    def UpdateMemberPower(self):
        self.member_power.Clear()
        self.c.execute('SELECT member_name, member_power FROM member WHERE alliance_name=?', (self.alliance_name,))
        for row in self.c.fetchall():
            self.member_power.Append(str(row[0] + ':' + str(row[1])))


if __name__ == '__main__':
    app = wx.App()
    frame = RankCalc(None, title='同盟スコア計算')
    frame.Show()
    app.MainLoop()