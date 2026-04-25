import webbrowser
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve


class LinksPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.animations = []  # Храним анимации
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)

        # Верхняя панель с кнопкой назад
        top_layout = QHBoxLayout()
        btn_back = QPushButton("← Назад в меню")
        btn_back.setFixedSize(150, 40)
        btn_back.clicked.connect(self.go_back)
        top_layout.addWidget(btn_back)
        top_layout.addStretch()

        # Заголовок
        title = QLabel("Полезные ссылки")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px 0px;")
        title.setAlignment(Qt.AlignCenter)

        # Кнопка Кибрарий
        btn_kibrary = QPushButton("Кибрарий")
        btn_kibrary.setFixedSize(350, 45)
        btn_kibrary.setCursor(Qt.PointingHandCursor)
        btn_kibrary.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: 1px solid #bbb;
                border-radius: 5px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        btn_kibrary.clicked.connect(self.toggle_kibrary)

        # Контейнер для контента (текст + кнопка ссылки)
        self.content_wrapper = QWidget()
        self.content_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        content_layout = QVBoxLayout(self.content_wrapper)
        content_layout.setContentsMargins(0, 5, 0, 0)
        content_layout.setSpacing(0)

        # Текст с информацией
        kibrary_text = QLabel()
        kibrary_text.setWordWrap(True)
        kibrary_text.setStyleSheet("""
            font-size: 14px; 
            background: #f5f5f5; 
            padding: 15px; 
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            line-height: 1.4;
        """)

        html_content = """
        <p><b>Кибрарий</b> — онлайн-библиотека знаний по кибербезопасности от «Сбера». 
        Ресурс создан, чтобы помочь пользователям узнать о киберугрозах, схемах мошенничества, 
        защитить свои сбережения и конфиденциальные данные от киберпреступников.</p>
        <p>В библиотеке собраны материалы по разным темам кибербезопасности.</p>
        """
        kibrary_text.setText(html_content)
        kibrary_text.setTextFormat(Qt.RichText)

        # Кнопка-ссылка для открытия сайта
        url_btn = QPushButton("🌐 Перейти на сайт Кибрария")
        url_btn.setCursor(Qt.PointingHandCursor)
        url_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 12px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                font-size: 13px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
        """)
        url_btn.clicked.connect(lambda: webbrowser.open("https://www.sberbank.ru/ru/person/kibrary"))

        content_layout.addWidget(kibrary_text)
        content_layout.addWidget(url_btn)

        # ВАЖНО: Сначала добавляем в основной layout, потом вычисляем высоту
        layout.addLayout(top_layout)
        layout.addWidget(title)
        layout.addWidget(btn_kibrary, alignment=Qt.AlignCenter)
        layout.addWidget(self.content_wrapper)
        layout.addStretch()

        # Вычисляем полную высоту до сокрытия
        self.content_wrapper.adjustSize()
        self.full_height = self.content_wrapper.sizeHint().height()

        # Скрываем контент (устанавливаем высоту 0)
        self.content_wrapper.setMinimumHeight(0)
        self.content_wrapper.setMaximumHeight(0)

        # Сохраняем ссылки для использования в toggle
        self.btn_kibrary = btn_kibrary
        self.is_open = False

    def toggle_kibrary(self):
        if not self.is_open:
            # Открываем
            self.animate_height(self.content_wrapper, self.full_height)
            self.is_open = True
            self.btn_kibrary.setStyleSheet("""
                QPushButton {
                    background-color: #4a90e2;
                    color: white;
                    border: 1px solid #357abd;
                    border-radius: 5px;
                    font-size: 13px;
                    font-weight: bold;
                }
            """)
        else:
            # Закрываем
            self.animate_height(self.content_wrapper, 0)
            self.is_open = False
            self.btn_kibrary.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #bbb;
                    border-radius: 5px;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
            """)

    def animate_height(self, widget, target_height):
        """Анимация изменения высоты виджета"""
        animation = QPropertyAnimation(widget, b"maximumHeight")
        animation.setDuration(250)
        animation.setStartValue(widget.height())
        animation.setEndValue(target_height)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start()

        # Сохраняем ссылку чтобы анимация не удалилась сборщиком мусора
        self.animations.append(animation)
        animation.finished.connect(lambda: self.animations.remove(animation))

    def go_back(self):
        if self.parent_window:
            self.parent_window.show_menu()