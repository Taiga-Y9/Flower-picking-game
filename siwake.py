import pygame as pg
import os

def main():

  # 初期化処理
  chip_s = 40  # マップチップの基本サイズ
  map_s = pg.Vector2(15, 15)  # マップの横・縦の配置数

  pg.init()
  pg.display.set_caption('花仕分けゲーム')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 15)
  frame = 0
  exit_flag = False
  exit_code = '000'
  image_path = "./img/maptile_tsuchi_02.png"
  background_image = pg.image.load(image_path).convert()
  kadan_image = pg.image.load("./img/maptile_sogen_02.png")

  # 背景画像を画面サイズに合わせる
  screen_width = chip_s * int(map_s.x)
  screen_height = chip_s * int(map_s.y)
  background_image = pg.transform.scale(
      background_image, (screen_width, screen_height))

  kadan_image = pg.transform.scale(kadan_image, (0, 0))

  # グリッド設定
  grid_c = '#bbbbbb'

  # 自キャラ移動関連
  cmd_move = -1  # 移動コマンドの管理変数
  m_vec = [
      pg.Vector2(0, -1),
      pg.Vector2(1, 0),
      pg.Vector2(0, 1),
      pg.Vector2(-1, 0)
  ]  # 移動コマンドに対応したXYの移動量

  # 自キャラの画像読込み
  reimu_p = pg.Vector2(6.4, 10)   # 自キャラ位置
  reimu_s = pg.Vector2(48, 64)  # 画面に出力する自キャラサイズ 48x64
  reimu_d = 2  # 自キャラの向き
  reimu_img_raw = pg.image.load('./img/reimu.png')
  reimu_img_arr = []
  for i in range(4):   # 上右下左の4方向
    reimu_img_arr.append([])
    for j in range(3):  # アニメーションパターンx3
      p = pg.Vector2(24 * j, 32 * i)  # 切り抜きの開始座標・左上
      tmp = reimu_img_raw.subsurface(pg.Rect(p, (24, 32)))  # 切り出し
      tmp = pg.transform.scale(tmp, reimu_s)  # 拡大
      reimu_img_arr[i].append(tmp)
    reimu_img_arr[i].append(reimu_img_arr[i][1])

  # ゲームループ
  while not exit_flag:
    screen.blit(background_image, (0, 0))
    screen.blit(kadan_image, (0, 0))

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT:  # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'

# キー状態の取得
    key = pg.key.get_pressed()
    cmd_move = -1
    cmd_move = 0 if key[pg.K_w] else cmd_move
    cmd_move = 1 if key[pg.K_d] else cmd_move
    cmd_move = 2 if key[pg.K_s] else cmd_move
    cmd_move = 3 if key[pg.K_a] else cmd_move

    # グリッド
    for x in range(0, disp_w, chip_s):  # 縦線
      pg.draw.line(screen, grid_c, (x, 0), (x, disp_h))
    for y in range(0, disp_h, chip_s):  # 横線
      pg.draw.line(screen, grid_c, (0, y), (disp_w, y))

    # 移動コマンドの処理
    speed_factor = 0.3  # 移動速度を調整する係数

    if cmd_move != -1:
      reimu_d = cmd_move  # キャラクタの向きを更新
      af_pos = reimu_p + m_vec[cmd_move] * \
          speed_factor  # 移動後の (仮) 座標をスピードファクターでスケーリング
      if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
        reimu_p += m_vec[cmd_move] * speed_factor  # ここで速度を掛けて実際に移動

    # 自キャラの描画 dp:描画基準点（imgの左上座標）
    dp = reimu_p * chip_s - pg.Vector2(0, 24)
    af = frame // 6 % 4  # 6フレーム毎にアニメーション
    screen.blit(reimu_img_arr[reimu_d][af], dp)

    # フレームカウンタの描画
    frame += 1
    frm_str = f'{frame:05}'
    screen.blit(font.render(frm_str, True, 'BLACK'), (10, 10))
    screen.blit(font.render(f'{reimu_p}', True, 'BLACK'), (10, 20))

    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')
