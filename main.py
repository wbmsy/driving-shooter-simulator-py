import random

import pyxel

# 画面サイズとレーンのX座標（左・中央・右）
WIDTH = 120
HEIGHT = 160
LANES = [20, 60, 100]

# プレイヤーの設定
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 12
PLAYER_Y = HEIGHT - 30

# 弾の設定
BULLET_HEIGHT = 4
MAX_BULLET_COUNT = 3

# 敵車の設定
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 12


class App:
    def __init__(self):
        # 画面の初期化
        pyxel.init(WIDTH, HEIGHT, title="Driving Shooter")
        pyxel.load("resource.pyxres")
        self.reset_game(0)
        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def reset_game(self, status):
        # ゲームの初期状態
        self.player_lane = 1  # 0:左, 1:中央, 2:右
        self.bullets = []  # 弾のリスト
        self.enemies = []  # 敵車のリスト
        self.explosion = []  # 爆発のリスト
        self.bullet_count = 0
        self.kills = 0
        self.enemy_speed_multiplier = 1.0
        self.game_time = 0
        self.game_status = status # 0:ホーム, 1:プレイ, 2:クリア, 3:ゲームオーバー

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.game_status == 0:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game(1)
            return

        if self.game_status == 2:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game(0)
            return

        if self.game_status == 3:
            # ゲームオーバー時にRキーでリスタート
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game(1)
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game(0)
            return

        # 1. プレイヤーの移動（3レーン）
        if pyxel.btnp(pyxel.KEY_LEFT) and self.player_lane > 0:
            self.player_lane -= 1
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.player_lane < 2:
            self.player_lane += 1

        # 2. 銃を撃つ
        if self.bullet_count > 0:
            if pyxel.btnp(pyxel.KEY_Z):
                self.bullet_count -= 1
                player_x = LANES[self.player_lane]
                # 弾をプレイヤーの少し上に生成 [x座標, y座標]
                self.bullets.append([player_x, PLAYER_Y - BULLET_HEIGHT])

        # 弾の移動処理
        for b in self.bullets[:]:
            b[1] -= 5  # 上に向かって進む
            if b[1] <= BULLET_HEIGHT * (-1):
                self.bullets.remove(b)

        # 弾の補充
        if pyxel.frame_count % 40 == 0:
            if self.bullet_count < MAX_BULLET_COUNT:
                self.bullet_count += 1

        # 3. 敵車が向かってくる（スポーンと移動）
        # 10フレームごとに80％の確率でランダムなレーンに敵を生成
        if random.random() >= 0.20:
            if pyxel.frame_count % 10 == 0:
                lane = random.randint(0, 2)
                type = random.randint(0, 3)
                self.enemies.append([LANES[lane], ENEMY_HEIGHT * (-1), type])

        # 敵車の移動処理
        for e in self.enemies[:]:
            e[1] += 2 * self.enemy_speed_multiplier  # 下に向かって進む
            if e[1] > HEIGHT:
                self.enemies.remove(e)

        # 敵車の速度を上げる
        if self.game_time % 10 == 0 and self.game_time != 0 and pyxel.frame_count % 30 == 0:
            self.enemy_speed_multiplier += 0.5

        # 4. 当たり判定（衝突処理）
        # 弾と敵車の当たり判定
        for b in self.bullets[:]:
            for e in self.enemies[:]:
                # X座標が同じレーンで、Y座標が近ければ命中
                if b[0] == e[0] and abs(b[1] - e[1]) < ENEMY_HEIGHT - 2:
                    self.explosion.append([e[0], e[1], 0])  # 爆発の座標を追加
                    # if b in self.bullets:
                    self.bullets.remove(b)
                    # if e in self.enemies:
                    self.enemies.remove(e)
                    self.kills += 1

        # 爆発の処理
        for exp in self.explosion[:]:
            exp[1] += 2 * self.enemy_speed_multiplier  # 爆発のY座標を下に移動
            exp[2] += 1
            if exp[2] > 5:  # 爆発のアニメーションが5フレームで終了
                self.explosion.remove(exp)  # 爆発を削除


        # プレイヤーと敵車の当たり判定
        player_x = LANES[self.player_lane]
        for e in self.enemies:
            if player_x == e[0] and abs(PLAYER_Y - e[1]) < ENEMY_HEIGHT:
                self.game_status = 3
                pyxel.play(0,0)

        # 経過時間の更新
        if pyxel.frame_count % 30 == 0:
            self.game_time += 1

        # ゴール条件
        if self.game_time == 60:
            self.game_status = 2

    def draw(self):
        # 画面を黒(0)でクリア
        pyxel.cls(0)

        if self.game_status == 0:
            pyxel.text(WIDTH // 2 - len("Press Space to Start") * 4 // 2, HEIGHT // 2, "Press Space to Start", 7)
            return

        if self.game_status == 2:
            pyxel.text(WIDTH // 2 - len("Press Space to Start") * 4 // 2, HEIGHT // 2, "Press Space to Start", 7)
            return

        if self.game_status == 3:
            pyxel.text(WIDTH // 2 - len("GAME OVER") * 4 // 2, HEIGHT // 2, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(WIDTH // 2 - len("Restart: R") * 4 // 2, HEIGHT // 2 + 15, "Restart: R", 7)
            pyxel.text(WIDTH // 2 - len("Home: Space") * 4 // 2, HEIGHT // 2 + 25, "Home: Space", 7)
            return

        # レーンの境界線を引く（背景）
        pyxel.line(40, 0, 40, HEIGHT, 1)
        pyxel.line(80, 0, 80, HEIGHT, 1)

        # プレイヤーの描画（色5: 水色）
        player_x = LANES[self.player_lane]
        # pyxel.rect(
        #     player_x - PLAYER_WIDTH / 2, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT, 5
        # )
        pyxel.blt(player_x - 7, PLAYER_Y, 0, 1, 17, 14, 13, colkey=0, scale=1)

        # 弾の描画（色10: 黄色）
        for b in self.bullets:
            # pyxel.rect(b[0] - BULLET_WIDTH / 2, b[1], BULLET_WIDTH, BULLET_HEIGHT, 10)
            pyxel.blt(b[0] - 3.75, b[1], 0, 0, 0, 8, 8, colkey=0, scale=0.8)

        # 敵車の描画（色8: 赤）
        for e in self.enemies:
            # pyxel.rect(e[0] - ENEMY_WIDTH / 2, e[1], ENEMY_WIDTH, ENEMY_HEIGHT, 8)
            match e[2]:
                case 0:
                    pyxel.blt(e[0] - 7.8, e[1], 0, 0, 32, 16, 16, colkey=13, scale=1.3)
                case 1:
                    pyxel.blt(e[0] - 7.8, e[1], 0, 16, 32, 16, 16, colkey=13, scale=1.2)
                case 2:
                    pyxel.blt(e[0] - 7.8, e[1], 0, 32, 32, 16, 16, colkey=13, scale=1.0)
                case 3:
                    pyxel.blt(e[0] - 7.8, e[1], 0, 48, 32, 16, 16, colkey=13, scale=0.9)

        # 爆発の描画（色9: オレンジ）
        for exp in self.explosion:
            pyxel.blt(exp[0] - 8, exp[1], 0, 16, 0, 16, 16, colkey=0, scale=1)

        # スコアの表示
        pyxel.text(5, 5, f"KILLS: {self.kills}", 7)
        pyxel.text(75, 5, f"BULLETS: {self.bullet_count}", 7)
        pyxel.text(75, 15, f"TIME: {self.game_time}", 7)
        pyxel.text(75, 25, f"SPEED: {self.enemy_speed_multiplier:.1f}", 7)


# ゲームの実行
App()
