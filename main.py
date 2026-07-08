import random

import pyxel

# 画面サイズとレーンのX座標（左・中央・右）
WIDTH = 120
HEIGHT = 160
LANES = [20, 60, 100]


class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(WIDTH, HEIGHT, title="Driving Shooter")
        self.reset_game()
        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # ゲームの初期状態
        self.player_lane = 1  # 0:左, 1:中央, 2:右
        self.bullets = []  # 弾のリスト
        self.enemies = []  # 敵車のリスト
        self.score = 0
        self.is_game_over = False

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.is_game_over:
            # ゲームオーバー時にRキーでリスタート
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # 1. プレイヤーの移動（3レーン）
        if pyxel.btnp(pyxel.KEY_LEFT) and self.player_lane > 0:
            self.player_lane -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.player_lane < 2:
            self.player_lane += 1

        # 2. 銃を撃つ
        if pyxel.btnp(pyxel.KEY_SPACE):
            player_x = LANES[self.player_lane]
            # 弾をプレイヤーの少し上に生成 [x座標, y座標]
            self.bullets.append([player_x, HEIGHT - 20])

        # 弾の移動処理
        for b in self.bullets[:]:
            b[1] -= 5  # 上に向かって進む
            if b[1] < 0:
                self.bullets.remove(b)

        # 3. 敵車が向かってくる（スポーンと移動）
        # 30フレームごとにランダムなレーンに敵を生成
        if pyxel.frame_count % 30 == 0:
            lane = random.randint(0, 2)
            self.enemies.append([LANES[lane], -10])

        # 敵車の移動処理
        for e in self.enemies[:]:
            e[1] += 2  # 下に向かって進む
            if e[1] > HEIGHT:
                self.enemies.remove(e)

        # 4. 当たり判定（衝突処理）
        # 弾と敵車の当たり判定
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                # X座標が同じレーンで、Y座標が近ければ命中
                if b[0] == e[0] and abs(b[1] - e[1]) < 10:
                    if b in self.bullets:
                        self.bullets.remove(b)
                    if e in self.enemies:
                        self.enemies.remove(e)
                    self.score += 100

        # プレイヤーと敵車の当たり判定
        player_x = LANES[self.player_lane]
        player_y = HEIGHT - 15
        for e in self.enemies:
            if player_x == e[0] and abs(player_y - e[1]) < 15:
                self.is_game_over = True

    def draw(self):
        # 画面を黒(0)でクリア
        pyxel.cls(0)

        if self.is_game_over:
            pyxel.text(35, HEIGHT // 2 - 10, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(30, HEIGHT // 2 + 10, "Press R to Restart", 7)
            return

        # レーンの境界線を引く（背景）
        pyxel.line(40, 0, 40, HEIGHT, 1)
        pyxel.line(80, 0, 80, HEIGHT, 1)

        # プレイヤーの描画（色5: 水色）
        player_x = LANES[self.player_lane]
        pyxel.rect(player_x - 4, HEIGHT - 20, 8, 12, 5)

        # 弾の描画（色10: 黄色）
        for b in self.bullets:
            pyxel.rect(b[0] - 1, b[1] - 4, 2, 4, 10)

        # 敵車の描画（色8: 赤）
        for e in self.enemies:
            pyxel.rect(e[0] - 4, e[1], 8, 12, 8)

        # スコアの表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)


# ゲームの実行
App()
