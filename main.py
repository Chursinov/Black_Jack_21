from tkinter import *  # Модуль GUI
from PIL import ImageTk  # Модуль для связи GUI и изображений
from PIL import Image as Img  # Модуль для  изображений
from random import shuffle  # Модуль рандом


class Main:
    # Инициализация класса.
    def __init__(self):
        self.ma1n = Tk()  # Создание окна
        self.ma1n.title('Black Jack [21]')  # Название программы
        self.ma1n.iconbitmap('favicon.ico')  # Добавляем иконку
        self.ma1n.geometry('258x421')  # Определяем размер окна
        self.ma1n.resizable(False, False)  # Окно нельзя расширять по осям Х и У
        self.ma1n.attributes('-topmost', True)  # Окно при запуске уходит на передний план
        self.cards = []  # Определяем список для карт
        self.load_images(self.cards)  # Вызываем метод загрузки фотографий
        self.deck = list(self.cards)  # Определяем колоду карт
        shuffle(self.deck)  # Перемешиваем колоду карт
        self.dealer_score = 0  # Обозначаем очки дилера
        self.player_score = 0  # Обозначаем очки игрока
        self.dealer_hand = []  # Обозначаем "руку" дилера
        self.player_hand = []  # Обозначаем "руку" игрока

        self.background_image = ImageTk.PhotoImage(Img.open('Background.png'))  # Определяем текстуру фона окна
        self.deal_image = ImageTk.PhotoImage(Img.open('Deal.png'))  # Текстура кнопки "начать"
        self.hit_image = ImageTk.PhotoImage(Img.open('Hit.png'))  # Текстура кнопки "взять"
        self.stand_image = ImageTk.PhotoImage(Img.open('Stand.png'))  # Текстура кнопки "оставить"
        self.background_label = Label(self.ma1n, image=self.background_image)   # Определяем фон окна
        self.status_label = Label(self.ma1n, font=('Minecraft', 10), bg='#f2ca3f', fg='#FFFFFF')  # Создаём Label, где будет отображаться статус игры (победа/проигрыш)
        self.dealer_score_label = IntVar()  # Переменная Integer типа для очков дилера
        self.dealer_label = Label(self.ma1n, textvariable=self.dealer_score_label, bg='#3b3a38', fg='#FFFFFF', font=('Minecraft', 10))  # Label для очков дилера
        self.dealer_card_frame = Frame(self.ma1n, bg='#7a3b5a')  # Рамка для карт дилера
        self.player_score_label = IntVar()  # Переменная Integer типа для очков игрока
        self.player_label = Label(self.ma1n, textvariable=self.player_score_label, bg='#3b3a38', fg='#FFFFFF', font=('Minecraft', 10))  # Label для очков игрока
        self.player_card_frame = Frame(self.ma1n, bg='#552e41')  # Рамка для карт игрока
        self.button_deal = Button(self.ma1n, image=self.deal_image, relief=FLAT, border='0', command=self.deal, bg='#552e41', activebackground='#552e41')  # Кнопка "Начать"
        self.button_hit = Button(self.ma1n, image=self.hit_image, relief=FLAT, border='0', command=self.hit, bg='#552e41', activebackground='#552e41')  # Кнопка "Взять"
        self.button_stand = Button(self.ma1n, image=self.stand_image, relief=FLAT, border='0', command=self.stand, bg='#552e41', activebackground='#552e41')  # Кнопка "Оставить"
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Выставляем в окне Label с фоном
        self.dealer_label.place(x=115, y=89, width=30, height=12)  # Выставляем счётчик очков дилера
        self.dealer_card_frame.place(x=73, y=121)  # Выставляем рамку с картами дилера
        self.player_label.place(x=115, y=225, width=30, height=12)  # Выставляем счётчик очков игрока
        self.player_card_frame.place(x=73, y=255)  # Выставляем рамку с картами игрока
        self.button_deal.place(x=90, y=309)  # Выставляем кнопку "Начать игру"

        self.ma1n.mainloop()  # Запуск главного окна

    # Загрузка фотографий.
    @staticmethod
    def load_images(card_images):
        suits = ['heart', 'club', 'diamond', 'spade']  # Масти карт (4шт)
        face_cards = ['J', 'Q', 'K']  # Карты выше 10 ("валет", "дама", "король")

        for i in suits:  # Для каждой карты в колоде
            for j in range(1, 11):  # Проход по картам с цифрами
                card_images.append((j, ImageTk.PhotoImage(Img.open(f'cards/{str(j)}_{i}.png'))))  # Открывается карта и добавляется в список
            for card in face_cards:  # Проход по картам с буквами
                card_images.append((10, ImageTk.PhotoImage(Img.open(f'cards/{str(card)}_{i}.png'))))  # Открывается карта и добавляется в список

    # Вывод фотографий в игре.
    def deal_card(self, frame):
        next_card = self.deck.pop(0)  # Карта достаётся из колоды и удаляется оттуда. (0 - карту взяли с верха колоды)
        self.deck.append(next_card)  # В колоду добавляется эта выпавшая карта
        if frame == self.dealer_card_frame:
            frame.config(bg='#824564')
            Label(frame, image=next_card[1], relief='flat', bg='#824564').pack(side=LEFT)  # Label с картой добавляется в рамку
        else:
            frame.config(bg='#552e41')
            Label(frame, image=next_card[1], relief='flat', bg='#552e41').pack(side=LEFT)  # Label с картой добавляется в рамку
        return next_card  # Результат программы - кортеж с весом карты и картинкой карты

    # Подсчёт карт в 'руке'.
    @staticmethod  # Метод - статический, так как не использует переменные или методы класса, и не ссылается на класс
    def score_hand(hand):
        score = 0
        ace = False
        for next_card in hand:
            card_value = next_card[0]
            if card_value == 1 and not ace:
                ace = True
                card_value = 11
            score += card_value
            if score > 21 and ace:
                score -= 10
                ace = False
        return score

    # Начало игры.
    def deal(self):
        self.status_label.place_forget()  # Прячем Label со статусом (поражение/победа)
        self.button_hit.place(x=26, y=309)  # Ставим кнопку "Взять" на координаты
        self.button_stand.place(x=155, y=309)  # Ставим кнопку "Оставить" на координаты
        self.button_deal.place_forget()  # Прячем кнопку "Начать игру"
        self.dealer_card_frame.destroy()  # Удаляем рамку с картами дилера
        self.dealer_card_frame = Frame(self.ma1n)  # Создаём рамку с картами дилера
        self.dealer_card_frame.place(x=73, y=121)  # Ставим рамку с картами дилера
        self.player_card_frame.destroy()  # Удаляем рамку с картами игрока
        self.player_card_frame = Frame(self.ma1n)  # Создаём рамку с картами игрока
        self.player_card_frame.place(x=73, y=255)  # Ставим рамку с картами игрока
        self.status_label['text'] = ''  # Стираем текст из Label со статусом игры
        self.dealer_hand = []  # Опустошаем колоду дилера
        self.player_hand = []  # Опустошаем колоду игрока
        self.player_hand.append(self.deal_card(self.player_card_frame))  # Добавляем в колоду игрока случайную карту
        self.player_score = self.score_hand(self.player_hand)  # Обновляем очки для игрока
        self.player_score_label.set(self.player_score)  # Обновляем Label, показывающий очки игрока
        if self.player_score > 21:  # Условие для перебора карт
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'YOU BUSTED'
        self.dealer_hand.append(self.deal_card(self.dealer_card_frame))  # Добавляем в колоду дилера случайную карту
        self.dealer_score = self.score_hand(self.dealer_hand)   # Обновляем очки для дилера
        self.dealer_score_label.set(self.dealer_score)  # Обновляем Label, показывающий очки игрока
        self.player_hand.append(self.deal_card(self.player_card_frame))  # Добавляем в колоду дилера случайную карту
        self.player_score = self.score_hand(self.player_hand)  # Обновляем очки для дилера
        self.player_score_label.set(self.player_score)  # Обновляем Label, показывающий очки игрока
        if self.player_score > 21:  # Условие для перебора карт
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'YOU BUSTED'
        if self.player_score == 21:  # Условие для Блекджека (если в сумме карты дают 21)
            self.stand()

    # Кнопка 'Взять'.
    def hit(self):
        self.player_hand.append(self.deal_card(self.player_card_frame))  # Добавляем в колоду дилера случайную карту
        self.player_score = self.score_hand(self.player_hand)  # Обновляем очки для игрока
        self.player_score_label.set(self.player_score)  # Обновляем Label, показывающий очки игрока
        if self.player_score > 21:  # Условие для перебора карт
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'YOU BUSTED'
            self.button_hit.place_forget()
            self.button_stand.place_forget()
            self.button_deal.place(x=90, y=309)
        if self.player_score == 21:  # Условие для Блекджека (если в сумме карты дают 21)
            self.stand()

    # Кнопка 'Пас'.
    def stand(self):
        self.dealer_score = self.score_hand(self.dealer_hand)
        while 0 < self.dealer_score < 17:  # Дилер берёт карты, в сумме до 17и
            self.dealer_hand.append(self.deal_card(self.dealer_card_frame))  # Добавляем в колоду дилера случайную карту
            self.dealer_score = self.score_hand(self.dealer_hand)  # Обновляем очки для дилера
            self.dealer_score_label.set(self.dealer_score)  # Обновляем Label, показывающий очки дилера
        self.player_score = self.score_hand(self.player_hand)  # Обновляем очки для игрока
        if self.player_score > 21:  # Условие для перебора
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'YOU BUSTED'
        elif self.dealer_score > 21 or self.dealer_score < self.player_score:  # Условие для победы
            self.status_label.place(x=36, y=180, width=187, height=30)
            if self.player_score == 21:  # Дополнительное условие для Блекджека (если в сумме карты дают 21)
                self.status_label['text'] = 'TWENTY ONE!'
            else:
                self.status_label['text'] = 'DEALER BUSTS!'
        elif self.dealer_score > self.player_score:  # Условие для Блекджека (если в сумме карты дают 21)
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'DEALER WINS!'
            print('lol')
        else:  # Иначе условие для ничьей
            self.status_label.place(x=36, y=180, width=187, height=30)
            self.status_label['text'] = 'PUSH!'
        self.button_hit.place_forget()  # Прячем кнопку "Взять"
        self.button_stand.place_forget()  # Прячем кнопку "Оставить"
        self.button_deal.place(x=90, y=309)  # Показываем кнопку "Начать игру"


# Старт игры.
if __name__ == '__main__':
    _new_window = Main()  # Создаём переменную и присваиваем ей класс
