import wx
import os
import sqlite3

class RankCalc(wx.Frame):
    def __init__(self, parent, title):
        super(RankCalc, self).__init__(parent, title=title)
        
        self.CreateDB()
        self.InitUI()

    def CreateDB(self):
        # if id nothing .db file
        if not os.path.exists('RankCalc.db'):
            # DBの作成
            self.conn = sqlite3.connect('RankCalc.db')
            c = self.conn.cursor()

            # 同盟名, 同盟戦力, 同盟撃破数, 同盟領土数, 関所数, 聖所数
            c.execute('CREATE TABLE IF NOT EXISTS Alliance (alliance_name text, alliance_power int, alliance_kill int, alliance_territory int, pass int, shrine int)')
            # 同盟名, 個人戦力
            c.execute('CREATE TABLE IF NOT EXISTS Member (alliance_name text, member_name text, member_power int)')

            # 初期データの挿入
            c.execute('INSERT INTO Alliance VALUES ("同盟1", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance VALUES ("同盟2", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance VALUES ("同盟3", 0, 0, 0, 0, 0)')
            c.execute('INSERT INTO Alliance VALUES ("同盟4", 0, 0, 0, 0, 0)')

            # DBの保存
            self.conn.commit()

    def InitUI(self):
        # サイズ固定
        self.SetMaxSize((480, 330))
        self.SetMinSize((480, 330))
        # 4つの同盟のタブを作成
        self.nb = wx.Notebook(self)
        self.nb.AddPage(AlliancePanel(self.nb, '同盟1'), '同盟1')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟2'), '同盟2')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟3'), '同盟3')
        self.nb.AddPage(AlliancePanel(self.nb, '同盟4'), '同盟4')

class AlliancePanel(wx.Panel):
    def __init__(self, parent, alliance_name):
        super(AlliancePanel, self).__init__(parent)
        self.alliance_name = alliance_name
        self.InitUI()
        self.ConnectDB()

    def InitUI(self):
        # 同盟戦力
        self.alliance_power = wx.TextCtrl(self, size=(100, -1))
        # 同盟撃破数
        self.alliance_kill = wx.TextCtrl(self, size=(100, -1))
        # 同盟領土数
        self.alliance_territory = wx.TextCtrl(self, size=(100, -1))
        # 関所数
        self.pass_ = wx.TextCtrl(self, size=(100, -1))
        # 聖所数
        self.shrine = wx.TextCtrl(self, size=(100, -1))
        # スコア
        self.score = wx.TextCtrl(self, size=(100, -1))


        # 個人戦力のスクロールバー付きリストボックス
        self.member_power = wx.ListBox(self, size=(280, 160), style=wx.LB_SINGLE)
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

        # リストボックスのイベント
        self.member_power.Bind(wx.EVT_LISTBOX, self.SelectMemberTable)

    def ConnectDB(self):
        self.conn = sqlite3.connect('RankCalc.db')
        self.c = self.conn.cursor()
        try:
            # データの取得
            # 同盟データ
            self.c.execute('SELECT * FROM alliance WHERE alliance_name=?', (self.alliance_name,))
            _, alliance_power, alliance_kill, alliance_territory, pass_, shrine = self.c.fetchone()
            self.alliance_power.SetValue(str(alliance_power))
            self.alliance_kill.SetValue(str(alliance_kill))
            self.alliance_territory.SetValue(str(alliance_territory))
            self.pass_.SetValue(str(pass_))
            self.shrine.SetValue(str(shrine))

            # メンバーデータ
            self.c.execute('SELECT * FROM member WHERE alliance_name=?', (self.alliance_name,))
            for row in self.c.fetchall():
                self.member_power.Append(str(row[1]) + ':' + str(row[2]))

        except Exception as e:
            print(e)

    def UpdateAllianceTable(self, e):
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

        # 同盟名, 同盟戦力, 同盟撃破数, 同盟領土数, 関所数, 聖所数
        self.c.execute('UPDATE alliance SET alliance_power=?, alliance_kill=?, alliance_territory=?, pass=?, shrine=? WHERE alliance_name=?', (alliance_power, alliance_kill, alliance_territory, pass_, shrine, self.alliance_name))
        self.conn.commit()

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
        self.member_power.Clear()
        self.c.execute('SELECT member_name, member_power FROM member WHERE alliance_name=?', (self.alliance_name,))
        for member_data in self.c.fetchall():
            self.member_power.Append(str(member_data[0] + ':' + str(member_data[1])))

        # テキストボックスのクリア
        self.member_power_name.Clear()
        self.member_power_val.Clear()

    def SelectMemberTable(self, e):
        # 個人名
        member_name = self.member_power.GetStringSelection().split(':')[0]
        # 個人戦力
        member_power = self.member_power.GetStringSelection().split(':')[1]
        
        self.member_power_name.SetValue(member_name)
        self.member_power_val.SetValue(str(member_power))


if __name__ == '__main__':
    app = wx.App()
    frame = RankCalc(None, title='同盟スコア計算')
    frame.Show()
    app.MainLoop()