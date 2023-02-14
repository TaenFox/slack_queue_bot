# Бот-очередь для слака #
## Миссия проекта
Этот проект изначально задумывался как документация (см [Documentation.md](Documentation.md)) для практики - сначала себя как аналитика, а затем и всех желающих как разработчиков

Однако, я решил углубиться в практику более глубоко и сделал попытку объяснить ChatGPT какой код мне нужен. К сожалению, дословно весь текст он не понял - может потому что сложно понять взаимосвязи, а может это ограничения того, что описание выполнено на русском языке. Но меня это не остановило и вспомнив былую практику написания кода и приступил к детальному описанию функций и классов, которые я хочу увидеть. С этой задачей ИИ справился, а этого и моих знаний было достаточно, чтобы собрать отдельные блоки кода в целый проект.

Диалог с ботом представлен в файле [chatGPT.md](chatGPT.md)

## О проекте

Это бот для популярного мессенджера Slack, который генерирует сообщение-очередь с набором увеселительного контента внутри. Функциональность сообщения:

- Пользователь может занять очередь (в т.ч. несколько раз), нажав кнопку "Занять"
- Пользователь может покинуть очередь (столько раз сколько необходимо, начиная с верха очереди), нажав кнопку "Покинуть"
- Любой пользователь нажатием кнопки "Следующий" может "провернуть" очередь, переместив пользователя, который наверху очереди, в самый конец
- Любой пользователь может изменить порядок очереди, выбрав из выпадающего списка участников того, который будет помещён на верх очереди
- Администратор пространства или пользователь с соответствующими правами может удалить сообщение-очередь, используя диалоговое меню сообщения

Для разворачивания бота не требуется БД или права на хранение или изменение файлов на сервере, т.к. вся необходимая информация хранится в объекте сообщения, получаемом при взаимодействии с ним

## Благодарности
- Спасибо Владимиру Колосову за помощь с тестированием - без него я бы забросил это дело
- Спасибо [Богдану Марченко](https://www.linkedin.com/in/bogdan-m-39a4b6207/) за технический подсказки по Python
- Спасибо [Олегу Иванову](https://www.youtube.com/@MediaFizika) за генерацию картинок для антуража
- Спасибо [создателям ChatGPT](openai.com), без которого не случился бы этот проект