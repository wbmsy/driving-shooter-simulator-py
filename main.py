import random

import pyxel


class CatchGame:
    def __init__(self):
        # 画面サイズ: 160 x 160 px
        pyxel.init(160, 160, title="Apple Catch!")

        # プレイヤーの初期設定 (x座標, y座標)
        self.player_x = 72
        self.player_y = 140
        self.player_width = 16
        self.player_height = 8

        # リンゴの初期設定
        self.apple_x = random.randint(0, 152)
        self.apple_y = 0
        self.apple_speed = 2

        # ゲームの状態
        self.score = 0
        self.game_over = False

        # ゲームスタート！
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.game_over:
            # ゲームオーバー時にスペースキーでリスタート
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.__init__()
            return

        # 1. プレイヤーの移動制限と操作
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(0, self.player_x - 3)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(160 - self.player_width, self.player_x + 3)

        # 2. リンゴの落下
        self.apple_y += self.apple_speed

        # 3. 当たり判定（プレイヤーとリンゴが重なったか？）
        # 簡単な矩形（ボックス）同士の当たり判定です
        if (
            self.player_x < self.apple_x + 8
            and self.player_x + self.player_width > self.apple_x
            and self.player_y < self.apple_y + 8
            and self.player_y + self.player_height > self.apple_y
        ):
            # キャッチ成功！
            self.score += 10
            # リンゴを上部に戻してスピードアップ
            self.apple_x = random.randint(0, 152)
            self.apple_y = 0
            self.apple_speed = min(8, self.apple_speed + 0.2)  # 徐々に速くなる
            # ピピッという高音（組み込みの効果音）を鳴らす
            pyxel.play(0, 0)

        # 4. 見逃し判定（地面に落ちたか？）
        if self.apple_y > 160:
            self.game_over = True

    def draw(self):
        # 画面を黒(0)でクリア
        pyxel.cls(0)

        if self.game_over:
            # ゲームオーバー画面
            pyxel.text(50, 60, "GAME OVER", 8)  # 赤色でテキスト
            pyxel.text(45, 80, f"SCORE: {self.score}", 7)
            pyxel.text(30, 100, "PRESS SPACE TO RESET", 10)
        else:
            # プレイ中画面

            # 地面を描画 (暗い緑の帯)
            pyxel.rect(0, 148, 160, 12, 3)

            # プレイヤーを描画 (緑色の四角)
            pyxel.rect(
                self.player_x, self.player_y, self.player_width, self.player_height, 11
            )

            # リンゴを描画 (赤い円)
            pyxel.circ(
                self.apple_x + 4, self.apple_y + 4, 4, 8
            )  # (中心x, 中心y, 半径, 色8=赤)
            # リンゴのヘタ (緑のドット)
            pyxel.pset(self.apple_x + 4, self.apple_y, 3)

            # スコアを描画
            pyxel.text(5, 5, f"SCORE: {self.score}", 7)  # 白色でスコア表示


# ゲームの起動
CatchGame()
