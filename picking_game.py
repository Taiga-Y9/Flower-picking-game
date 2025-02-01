import pygame as pg
import os
import random

def main():
  # 初期化処理
  score = 0
  chip_s = 40  # マップチップの基本サイズ
  map_s = pg.Vector2(15, 15)  # マップの横・縦の配置数
  flower_spawn_interval = 3500  # 花が生える間隔（ミリ秒）
  reduced_interval_factor = 0.9  # インターバルの減少倍率
  flower_life_duration = 10000  # 花の持続時間（ミリ秒）
  flower_spawn_timer = 0  # タイマー
  flower_spawn_time = flower_spawn_interval  # タイマーの初期値
  last_flower_spawn = pg.time.get_ticks()  # 最後の花の生成時刻
  flowers = []  # 生成された花のリスト
  flower_death_duration = 2000  # 花が枯れてからゲームを終了するまでの時間（ミリ秒）
  flower_end_time = None  # ゲーム終了までのタイマー
  speed_factor = 0.3  # 移動速度を調整する係数
  is_game_over = False  # ゲームオーバーかどうかのフラグ

  pg.init()
  pg.display.set_caption('花摘みゲーム')
  disp_w = int(chip_s * map_s.x)
  disp_h = int(chip_s * map_s.y)
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 30)
  frame = 0
  exit_flag = False
  exit_code = '000'
  screen_width = chip_s * int(map_s.x)
  screen_height = chip_s * int(map_s.y)

  kareki_image = pg.image.load("./img/ki_kareki.png")
  image_path = "./img/maptile_tsuchi_02.png"
  background_image = pg.image.load(image_path).convert()
  kadan_image = pg.image.load("./img/maptile_sogen_02.png")
  kadan_img_rect = kadan_image.get_rect(center=(disp_w // 2, disp_h // 2))
  background_image = pg.transform.scale(
      background_image, (screen_width, screen_height))
  kadan_image = pg.transform.scale(kadan_image, (chip_s * 5, chip_s * 5))
  kareki_image = pg.transform.scale(kareki_image, (chip_s, chip_s))

  # 花画像の読み込み
  flower_images = [
      pg.transform.scale(pg.image.load(
          './img/rose_red_02.png'), (chip_s, chip_s)),
      pg.transform.scale(pg.image.load(
          './img/cosmos_blue.png'), (chip_s, chip_s)),
  ]

  # 自キャラの初期設定
  reimu_p = pg.Vector2(6.4, 10)
  reimu_s = pg.Vector2(48, 64)
  reimu_d = 2
  reimu_img_raw = pg.image.load('./img/reimu.png')
  reimu_img_width, reimu_img_height = reimu_img_raw.get_size()
  assert reimu_img_width >= 72 and reimu_img_height >= 128, "画像サイズが不足しています。"
  reimu_img_arr = []
  for i in range(4):
    reimu_img_arr.append([])
    for j in range(3):
      p = pg.Vector2(24 * j, 32 * i)
      tmp = reimu_img_raw.subsurface(pg.Rect(p, (24, 32)))
      tmp = pg.transform.scale(tmp, reimu_s)
      reimu_img_arr[i].append(tmp)

      # 最小限のサイズ検証
    if len(reimu_img_arr[i]) < 2:
      reimu_img_arr[i].append(reimu_img_arr[i][0])  # フレームが足りない場合は最初のフレームで埋める
    else:
      reimu_img_arr[i].append(reimu_img_arr[i][1])  # フレームが2つある場合の動作

  def reset_game():
    nonlocal score, flower_spawn_time, last_flower_spawn, flowers, is_game_over, reimu_p, reimu_d
    score = 0
    flower_spawn_time = flower_spawn_interval  # リセット
    last_flower_spawn = pg.time.get_ticks()  # 現在の時間で更新
    flowers.clear()  # 花をクリア
    is_game_over = False  # ゲームオーバーフラグをリセット
    reimu_p = pg.Vector2(6.4, 10)  # 自キャラの初期位置に戻す
    reimu_d = 2  # 向きをリセット
  # ゲームループ
  while not exit_flag:
    # イベント処理
    for event in pg.event.get():
      if event.type == pg.QUIT:
        exit_flag = True
    current_time = pg.time.get_ticks()
    screen.blit(background_image, (0, 0))
    screen.blit(kadan_image, (200, 200))

    if is_game_over:
      # スコアとリスタートオプションを表示
      score_surface = font.render(f"score: {score}", True, 'BLACK')
      restart_surface = font.render("Press spacekey to restart.", True, 'BLACK')
      screen.blit(score_surface, (disp_w // 2 -
                  score_surface.get_width() // 2, disp_h // 2 - 20))
      screen.blit(restart_surface, (disp_w // 2 -
                  restart_surface.get_width() // 2, disp_h // 2 + 20))
      pg.display.update()
      # リスタート用のキーイベント処理
      for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
          reset_game()  # リセット
    else:

      # 花を生成するかどうか
      if current_time - last_flower_spawn > flower_spawn_time:
        print("花が生成された")
        flower_type = random.choice(flower_images)
        flower_pos = pg.Vector2(random.randint(
            0, map_s.x - 1), random.randint(0, map_s.y - 1)) * chip_s
        flowers.append(
            {'image': flower_type, 'pos': flower_pos, 'spawn_time': current_time, 'alive': True})
        last_flower_spawn = current_time

      # 花の描画と寿命の管理
      for flower in flowers[:]:
        if flower['alive']:
          # 花を生やす処理...
          screen.blit(flower['image'], flower['pos'])
          if current_time - flower['spawn_time'] > flower_life_duration:
            flower['alive'] = False  # 花が枯れる
            flower['death_time'] = current_time  # 枯れた時間を記録
            flower['image'] = kareki_image  # 枯れた花の画像に変更
        else:
          # 枯れた花を描画...
          screen.blit(flower['image'], flower['pos'])
          if current_time - flower['death_time'] > flower_death_duration:
            flowers.remove(flower)  # 2秒後に花を
          is_game_over = True

      if flower_end_time and current_time - flower_end_time > flower_death_duration:
        exit_flag = True
        exit_code = '002'  # ゲーム終了コード

      # 自キャラの描画
      dp = reimu_p * chip_s - pg.Vector2(0, 24)
      af = frame // 6 % 4
      screen.blit(reimu_img_arr[reimu_d][af], dp)

      # 自キャラが花に触れた時の処理
      for flower in flowers[:]:
        if pg.Rect(flower['pos'], (chip_s, chip_s)).colliderect(pg.Rect(dp, (reimu_s.x, reimu_s.y))):
          flowers.remove(flower)
          score += 10

      # フレーム更新
      # フレームカウンタの描画
      frame += 1
      frm_str = f'{frame:05}'
      # スコアの描画
      screen.blit(font.render(
          f"score:{score}", True, 'BLACK'), (10, 10))
      # 画面の更新と同期
      pg.display.update()
      clock.tick(30)  # FPSを30に設定

      # 花が設置される間隔の調整
      if current_time // 15000 > (last_flower_spawn // 15000):
        flower_spawn_time = int(flower_spawn_time * reduced_interval_factor)

      # システムイベントの検出
      for event in pg.event.get():
        if event.type == pg.QUIT:  # ウィンドウの[X]の押下
          exit_flag = True
          exit_code = '001'

      # キー状態の取得（自キャラの移動処理）
      key = pg.key.get_pressed()
      cmd_move = -1
      m_vec = [
          pg.Vector2(0, -1),
          pg.Vector2(1, 0),
          pg.Vector2(0, 1),
          pg.Vector2(-1, 0)
      ]
      key = pg.key.get_pressed()
      cmd_move = -1
      cmd_move = 0 if key[pg.K_w] else cmd_move
      cmd_move = 1 if key[pg.K_d] else cmd_move
      cmd_move = 2 if key[pg.K_s] else cmd_move
      cmd_move = 3 if key[pg.K_a] else cmd_move
      # speed_factorの調整
      if key[pg.K_f]:
        speed_factor += 0.01  # fキーで速度を上げる
      if key[pg.K_g] and speed_factor > 0.2:
        speed_factor -= 0.01  # gキーで速度を下げる
      # 自キャラの移動処理
      if cmd_move != -1:
        reimu_d = cmd_move  # キャラクタの向きを更新
        af_pos = reimu_p + m_vec[cmd_move] * speed_factor  # 移動後の (仮) 座標
        if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 1):
          reimu_p += m_vec[cmd_move] * speed_factor  # 実際に移動

  # ゲーム終了処理
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')
