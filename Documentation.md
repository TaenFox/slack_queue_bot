# Бот-очередь для Slack

[Оригинальная документация](https://juicy-watchmaker-5f2.notion.site/Slack-f1be6135f1994c8d8f30799d56f6f6ef)

# Предисловие

Приветствую вас на странице, посвящённой проектной документации на небольшого бота для мессенджера Slack. Данная документация не предназначена для коммерческих целей и преследует цели профессиональной практики для IT специалистов.

Ниже описан минимально жизнеспособный продукт. Может показаться, что в нём отсутствуют какие-либо функциональности, но всё, что хочется сделать сверх описанного может послужить дополнительной практикой.

Для реализации бэкэнда приложения нет ограничений на выбор языка программирования.

Обратную связь можно оставить в форме по **[ссылке](https://forms.gle/CkZ3TbCSnzzhRk5X6)**

Спасибо за внимание,
[Павел Мокеев](https://www.linkedin.com/in/taenfox/)

# Описание

Бот предназначен для визуализации очереди между участниками общения в мессенджере Slack. По запросу пользователя инициируется создание очереди по тематике, определённой пользователем. После этого, участники общения вступают в очередь, выходят из неё, осуществляют ротацию - по порядку или вне порядка - посредством кнопок, прикреплённых в сообщении

Бот не имеет собственного хранилища информации и оперирует данными, которые собираются внутри сообщений-очередей

При взаимодействии пользователей с очередью в сообщении публикуется новое с актуализированными данными, а старое удаляется. В новом сообщении пользователь, который идёт следующим по порядку очереди получает новое уведомление.

<aside>
📌 Примеры:

- Ведущий дейли команды разработки
- Дежурство внутри команды
</aside>

<aside>
🧭 [**Ссылка на тестовое пространство Slack**](https://join.slack.com/t/taenfoxspace/shared_invite/zt-1o0rp8oya-xBoXQb~D8XKJeo_wvMGzxA)

</aside>

# Настройка приложения и используемые API

Для полноценного функционирования бота необходимо выполнить следующие условия:

- Создано приложение в каталоге Slack ([ссылка](https://api.slack.com/apps?new_app=1)). Для создания нужно указать пространство для установки - можно войти в тестовое пространство по ссылке выше.
- Написан backend для этого приложения на любом языке программирования (или с помощью других средств), который может обрабатывать входящие HTTP запросы и отправлять свои

Обработка различных действий приложения в пространстве требует предоставления соответствующих доступов, а также настройки самого приложения в каталоге. После этого приложение можно будет устанавливать в другие пространства Slack

## Настройка приложения

### Разрешения

В разделе **OAuth & Permissions** найти пункт ****************Scopes****************. Выдаём доступы в категории **Bot Token Scopes**. Для работы приложения потребуется выдать разрешение `chat:write`

После выдачи разрешения в разделе ****OAuth Tokens for Your Workspace**** по нажатию кнопки устанавливаем приложение в тестовое пространство Slack. После установки заполнено поле **Bot User OAuth Token** - это ключ для работы бота. Он используется для отправки запросов API

<aside>
🧭 **Полезные ссылки**

[Understanding OAuth scopes for Bots](https://api.slack.com/tutorials/understanding-oauth-scopes-bot)

</aside>

### Создание команды

В разделе нажать ****Slash Commands**** кнопку **Create New Command**. В возникшем диалоговом окне необходимо заполнить короткое название и URL для отправки HTTP запроса, когда команда запущена

<aside>
🧭 **Полезные ссылки**

[Enabling interactivity with Slash Commands](https://api.slack.com/interactivity/slash-commands)

</aside>

### Дополнительные функции

В разделе ****Interactivity & Shortcuts**** включена функция ****Interactivity****. После этого становится доступна подробная настройка. Здесь необходимо заполнить URL, на который при нажатии кнопок в сообщениях бота будут отправляться запросы.

## Работа с API Slack

<aside>
🧭 [**Схема взаимодействия пользователя, бота и Slack**](https://www.plantuml.com/plantuml/png/XLEzRXD14ExtAKPke_00557UWPRcOX_YXF55lWsYS84J88gmG49K54GHDT8bPCCbJfPN-EQD-6Ot72R1GdBXdPtlvvkTssvyCVLxpyVELtvS2axq3GAkqOhE4V43vsXnWqu_2A8U8kWh11OxiTyP6rfqx8-i1LpgNFTPPJlnGY1hxcarAkL9NVkT-gKhXhwUobvJJgLeP81ZGfUw854ai2Kys7dWTcci6bQxnSHBCow6prB_8_ltz-LExM-fwAt3aaGN26OQOU2IqkPMfdWe-8neyNXz_l-GBg48fmQnNt3AcnQdYFHvHJpEB36BCIb6N0hhlOA-SqJsyhAnGPQJLKc4x26I-iWu-jcj6D65lhyNvEEwsIFqjcMzx_KlPvOtjtxBV4rEbmXhtRfHoKUjNXI-pEOomKhYOpsWzf9uQkjR0_s3v_4ahmpt80-omus-HgJrwmnBspIRpToafbOndDPDu_2DnkCzFWJZ2iBAWINKVK6aVYJfuPyzCprXHn-IHsS-VgPNZ7famvVRqRKF19y8uvu4VB-Bj5Y6mKMcOM5EdZlxhGl9DfA5Avjx2Xs8DHggfILtvMGa5ZGbtkQ9d-al)

![https://juicy-watchmaker-5f2.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F0efa775a-7ef4-4a66-bcd9-da7eac9b04e7%2FXLEzRXD14ExtAKPke_00557UWPRcOX_YXF55lWsYS84J88gmG49K54GHDT8bPCCbJfPN-EQD-6Ot72R1GdBXdPtlvvkTssvyCVLxpyVELtvS2axq3GAkqOhE4V43vsXnWqu_2A8U8kWh11OxiTyP6rfqx8-i1LpgNFTPPJlnGY1hxcarAkL9NVkT-gKhXhwUobvJJgLeP81ZGfUw854ai2.png?id=17a87372-b6da-46e0-969b-f1b2a55bea24&table=block&spaceId=110dd269-5623-4f5c-949c-8c2b90418a3f&width=2000&userId=&cache=v2](%D0%91%D0%BE%D1%82-%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D1%8C%20%D0%B4%D0%BB%D1%8F%20Slack%20f1be6135f1994c8d8f30799d56f6f6ef/XLEzRXD14ExtAKPke_00557UWPRcOX_YXF55lWsYS84J88gmG49K54GHDT8bPCCbJfPN-EQD-6Ot72R1GdBXdPtlvvkTssvyCVLxpyVELtvS2axq3GAkqOhE4V43vsXnWqu_2A8U8kWh11OxiTyP6rfqx8-i1LpgNFTPPJlnGY1hxcarAkL9NVkT-gKhXhwUobvJJgLeP81ZGfUw854ai2.png)

****Примечание: удаление сообщения через контекстное меню доступно для администраторов пространства****

- PlantUML
    
    ```
    @startuml
    title Схема создания очереди и взаимодействия с ней
    hide footbox
    actor user as "Пользователь"
    participant slack as "Slack"
    participant bot as "Приложение"
    user -> slack: Команда создания очереди
    slack ->bot: Обработка встроеной команды
    bot -> slack ++: Создание сообщения с очередью
    user -> slack: Взаимодействие
    slack -> bot: Обработка взаимодействия
    bot->slack: Удаление сообщения
    deactivate slack
    bot->slack ++: Публикация сообщения\nс новой информацией
    |||
    note across
    Это сообщение не будет окончательно удалено 
    с помощью бота. Для его удаления можно 
    использовать контекстное меню Slack
    end note
    |||
    @enduml
    ```
    
</aside>

### API отправки и удаления сообщений

Отправка и удаление сообщений выполняется двумя соответствующими методами:

- **[chat.postMessage](https://api.slack.com/methods/chat.postMessage)** - отправка сообщений
- **[chat.delete](https://api.slack.com/methods/chat.delete)** - удаление сообщений

На страницах документации на вкладке ************Tester************ можно поэкспериментировать в работе с этими методами

### API обработки взаимодействий с сообщениями

При взаимодействии с сообщением очереди - нажатием кнопок или выбора элемента из списка - Slack отправляет на указанный в настройках URL HTTP-запрос, который содержит информацию о сообщении, с которым произошло взаимодействие, и саму суть взаимодействия

Бот должен уметь обрабатывать входящие HTTP запросы и на основе полученных данных реализовывать свою логику.

<aside>
🧭 **Полезные ссылки**

[Reference: block_actions payloads](https://api.slack.com/reference/interaction-payloads/block-actions)

</aside>

# Макет сообщения-очереди

- Payload сообщения
    
    ```json
    {
    	"blocks": [
    		{
    			"type": "header",
    			"text": {
    				"type": "plain_text",
    				"text": "Название очереди",
    				"emoji": true
    			}
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "mrkdwn",
    				"text": "*Сейчас: @Афанасьев*"
    			},
    			"accessory": {
    				"type": "button",
    				"text": {
    					"type": "plain_text",
    					"text": "Следующий",
    					"emoji": true
    				},
    				"action_id": "next-order"
    			}
    		},
    		{
    			"type": "section",
    			"text": {
    				"type": "plain_text",
    				"text": "- Иванов\n- Петров\n- Сидоров",
    				"emoji": true
    			}
    		},
    		{
    			"type": "actions",
    			"elements": [
    				{
    					"type": "static_select",
    					"placeholder": {
    						"type": "plain_text",
    						"text": "Идёт без очереди",
    						"emoji": true
    					},
    					"options": [
    						{
    							"text": {
    								"type": "plain_text",
    								"text": "Иванов",
    								"emoji": true
    							},
    							"value": "U313567"
    						},
    						{
    							"text": {
    								"type": "plain_text",
    								"text": "Петров",
    								"emoji": true
    							},
    							"value": "U325567"
    						},
    						{
    							"text": {
    								"type": "plain_text",
    								"text": "Сидоров",
    								"emoji": true
    							},
    							"value": "U389567"
    						}
    					],
    					"action_id": "out-of-order"
    				}
    			]
    		},
    		{
    			"type": "divider"
    		},
    		{
    			"type": "actions",
    			"elements": [
    				{
    					"type": "button",
    					"text": {
    						"type": "plain_text",
    						"text": "Занять",
    						"emoji": true
    					},
    					"action_id": "enter-order"
    				},
    				{
    					"type": "button",
    					"text": {
    						"type": "plain_text",
    						"text": "Покинуть",
    						"emoji": true
    					},
    					"action_id": "exit-order"
    				}
    			]
    		}
    	]
    }
    ```
    

<aside>
📌 **[Конструктор сообщения](https://app.slack.com/block-kit-builder/T04LPFEE890#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%9D%D0%B0%D0%B7%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D0%B8%22,%22emoji%22:true%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22mrkdwn%22,%22text%22:%22*%D0%A1%D0%B5%D0%B9%D1%87%D0%B0%D1%81:%20@%D0%90%D1%84%D0%B0%D0%BD%D0%B0%D1%81%D1%8C%D0%B5%D0%B2*%22%7D,%22accessory%22:%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%A1%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B8%D0%B9%22,%22emoji%22:true%7D,%22action_id%22:%22next-order%22%7D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22-%20%D0%98%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%5Cn-%20%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%5Cn-%20%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%22,%22emoji%22:true%7D%7D,%7B%22type%22:%22actions%22,%22elements%22:%5B%7B%22type%22:%22static_select%22,%22placeholder%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%98%D0%B4%D1%91%D1%82%20%D0%B1%D0%B5%D0%B7%20%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D0%B8%22,%22emoji%22:true%7D,%22options%22:%5B%7B%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%98%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2%22,%22emoji%22:true%7D,%22value%22:%22U313567%22%7D,%7B%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%9F%D0%B5%D1%82%D1%80%D0%BE%D0%B2%22,%22emoji%22:true%7D,%22value%22:%22U325567%22%7D,%7B%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%A1%D0%B8%D0%B4%D0%BE%D1%80%D0%BE%D0%B2%22,%22emoji%22:true%7D,%22value%22:%22U389567%22%7D%5D,%22action_id%22:%22out-of-order%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22actions%22,%22elements%22:%5B%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%97%D0%B0%D0%BD%D1%8F%D1%82%D1%8C%22,%22emoji%22:true%7D,%22action_id%22:%22enter-order%22%7D,%7B%22type%22:%22button%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22%D0%9F%D0%BE%D0%BA%D0%B8%D0%BD%D1%83%D1%82%D1%8C%22,%22emoji%22:true%7D,%22action_id%22:%22exit-order%22%7D%5D%7D%5D%7D)**

[**Интерактивный прототип](https://www.figma.com/proto/yQcpRtYwX1qZm87TiVNwZZ/%D0%91%D0%BE%D1%82-%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D1%8C-%D0%B4%D0%BB%D1%8F-Slack?node-id=1%3A2&scaling=min-zoom&page-id=0%3A1&starting-point-node-id=1%3A2) - тут можно посмотреть как работает очередь**

</aside>

![https://juicy-watchmaker-5f2.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F6a877c16-c8f5-4055-8e10-a13162105657%2FUntitled.png?id=d43cb46a-eb20-4013-a680-f9d70f0d8b96&table=block&spaceId=110dd269-5623-4f5c-949c-8c2b90418a3f&width=2000&userId=&cache=v2](%D0%91%D0%BE%D1%82-%D0%BE%D1%87%D0%B5%D1%80%D0%B5%D0%B4%D1%8C%20%D0%B4%D0%BB%D1%8F%20Slack%20f1be6135f1994c8d8f30799d56f6f6ef/Untitled.png)

Сообщение построено из различных блоков, каждый из которых выполняет свою функцию

## Название очереди

```json
{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Название очереди",
				"emoji": true
			}
		}
```

Тип блока: Header

Назначение: Заголовок очереди, помогает понять её предмет

Действие: нет

## Верх очереди

```json
{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Сейчас: @Афанасьев*"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Следующий",
					"emoji": true
				},
				"value": "next",
				"action_id": "next-order"
			}
		}
```

Тип блока: section

Назначение: Показывает пользователя, который находится наверху очереди (чья очередь) в формате “Сейчас: `{{Имя Фамилия пользователя}}`”. Пользователь, указанный в этом блоке получает уведомление. Также блок содержит кнопку, предназначенную для передачи очереди следующему пользователю.

### Действие

- Кнопка “Следующий” - при нажатии на неё:
    - пользователь, который находится наверху очереди, перемещается в её низ
    - публикуется новое сообщение, содержащее актуальное состояние и порядок очереди
    - удаляется сообщение, в котором была нажата кнопка

<aside>
📌 Пример Action, отправляемого в бота

- JSON
    
    ```json
    
    {
    	"type": "button",
    	"block_id": "oQIg",
    	"action_id": "next-order",
    	"text": {
    		"type": "plain_text",
    		"text": "Следующий",
    		"emoji": true
    	},
    	"action_ts": "1674843970.794411"
    }
    ```
    
</aside>

## Порядок очереди

```json
{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "- Иванов\n- Петров\n- Сидоров",
				"emoji": true
			}
		}
```

Тип блока: section

Назначение: Отображает текущий порядок в очереди. Представляет из себя обычный текст, в каждой строке которого указан пользователь, следующий за тем, который находится выше в очереди. Для переноса строки используется комбинация символов `\n`. Для проявления креатива можно использовать эмодзи вместо символа в начале строки списка

Действие: нет

## Смена порядка

```json
{
			"type": "actions",
			"elements": [
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Идёт без очереди",
						"emoji": true
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "Иванов",
								"emoji": true
							},
							"value": "U313567"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Петров",
								"emoji": true
							},
							"value": "U325567"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Сидоров",
								"emoji": true
							},
							"value": "U389567"
						}
					],
					"action_id": "out-of-order"
				}
			]
		}
```

Тип блока: actions

Назначение: Содержит список пользователей (список элементов, содержащих атрибуты пользователей). При выборе элемента из списка выбранный пользователь перемещается на верх очереди. Важные детали:

- плейсхолдер списка содержит текст “Идёт без очереди”
- каждый элемент списка состоит из полей `text` - описание текстового представления элемента; и `value` - ID пользователя Slack

### Действие

- При выборе элемента из списка:
    - пользователь, которому соответствует пункт списка, перемещается на верх очереди
    - публикуется новое сообщение, содержащее актуальное состояние и порядок очереди
    - удаляется сообщение, в котором была нажата кнопка

<aside>
📌 Пример Action, отправляемого в бота

- JSON
    
    ```json
    {
    	"type": "static_select",
    	"block_id": "kMx",
    	"action_id": "out-of-order",
    	"selected_option": {
    		"text": {
    			"type": "plain_text",
    			"text": "Петров",
    			"emoji": true
    		},
    		"value": "U325567"
    	},
    	"placeholder": {
    		"type": "plain_text",
    		"text": "Идёт без очереди",
    		"emoji": true
    	},
    	"action_ts": "1674845076.509561"
    }
    ```
    
</aside>

## Вход/выход очереди

```json
{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Занять",
						"emoji": true
					},
					"action_id": "enter-order"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Покинуть",
						"emoji": true
					},
					"action_id": "exit-order"
				}
			]
		}
```

Тип блока: actions

Назначение: Содержит две кнопки для управления собственной позицией в очереди:

- Кнопка “Занять” - пользователь помещается в низ очереди
- Кнопка “Покинуть” - пользователь удаляется из списка очереди

### Действие

- При нажатии кнопки “Занять”
    - пользователь, который нажал кнопку:
        - Если отсутствует в списке - помещается в низ очереди
        - Если присутствует - порядок не меняется
    - публикуется новое сообщение, содержащее актуальное состояние и порядок очереди
    - удаляется сообщение, в котором была нажата кнопка
    
    <aside>
    📌 Пример Action, отправляемого в бота
    
    - JSON
        
        ```json
        {
        			"type": "button",
        			"block_id": "VYGuI",
        			"action_id": "enter-order",
        			"text": {
        				"type": "plain_text",
        				"text": "Занять",
        				"emoji": true
        			},
        			"action_ts": "1674845767.001190"
        		}
        ```
        
    </aside>
    
- При нажатии кнопки “Покинуть”
    - пользователь, который нажал кнопку:
        - Если присутствует в списке - удаляется из очереди
        - Если отсутствует - порядок не меняется
    - публикуется новое сообщение, содержащее актуальное состояние и порядок очереди
    - удаляется сообщение, в котором была нажата кнопка
    
    <aside>
    📌 Пример Action, отправляемого в бота
    
    - JSON
        
        ```json
        {
        			"type": "button",
        			"block_id": "VYGuI",
        			"action_id": "exit-order",
        			"text": {
        				"type": "plain_text",
        				"text": "Покинуть",
        				"emoji": true
        			},
        			"action_ts": "1674845837.380499"
        		}
        ```
        
    </aside>