import os
import sys
import random
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:    (0, -5),
    pg.K_DOWN:  (0, +5),
    pg.K_LEFT:  (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRact or 爆弾Ract
    戻り値:判定結果タプル(横縦方向)
    画面内:True/画面外:False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横方向のはみ出しチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向のはみ出しチェック
        tate = False
    return yoko, tate


def game_over(screen: pg.Surface, bg_img: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示する関数
    """
    gameover = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)  # アルファ値を持つSurfaceを作成
    gameover.blit(bg_img, (0, 0))  # 背景画像を貼り付け
    gameover.fill((0, 0, 0, 128))  # 半透明の黒いフィルターを貼り付け
    screen.blit(gameover, (0, 0))

    # "Game Over"のテキストを表示
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = WIDTH // 2, HEIGHT // 2
    screen.blit(text, text_rect)
    
    # 泣いているこうかとんの画像を左右に2つ表示
    cry_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    
    # 左側のこうかとん
    cry_kk_rect_left = cry_kk_img.get_rect()
    cry_kk_rect_left.center = WIDTH // 2 - 200, text_rect.centery
    screen.blit(cry_kk_img, cry_kk_rect_left)

    # 右側のこうかとん
    cry_kk_rect_right = cry_kk_img.get_rect()
    cry_kk_rect_right.center = WIDTH // 2 + 200, text_rect.centery
    screen.blit(cry_kk_img, cry_kk_rect_right)

    pg.display.update() # 画面を更新
    pg.time.wait(5000) # 5秒間待機
    return # ゲーム終了



def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    戻り値:爆弾画像リスト, 爆弾半径リスト
    爆弾画像リスト:bb_imgs, 爆弾半径リスト:bb_rads
    """
    bb_imgs = []  # 爆弾画像リスト
    bb_accs = [a for a in range(1, 11)]  # 爆弾加速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r)) #空のsurface
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い爆弾を描く
        bb_imgs.append(bb_img)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #空のsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤い爆弾を描く
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明にする
    bb_rct = bb_img.get_rect()  # 爆弾ract
    bb_rct.centerx = random.randint(0, WIDTH)  #爆弾位置
    bb_rct.centery = random.randint(0, HEIGHT)  #爆弾位置
    vx, vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0

    #課題2


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            # 課題1
            game_over(screen, bg_img)
        

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
