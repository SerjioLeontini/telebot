import telebot
import requests
import json
from telebot import types
from datetime import datetime

#Подключение к боту
bot = telebot.TeleBot('')

#Подключение к Яндексу
headers = {""}

# Кнопки снизу
markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
markup_new_or_not = types.ReplyKeyboardMarkup(resize_keyboard = True)
item1 = types.KeyboardButton("Сейчас🕑")
item2 = types.KeyboardButton("На день🌎")
item3 = types.KeyboardButton("На 5️⃣ дней")
item1_1 = types.KeyboardButton("В этом же🎲")
item2_1 = types.KeyboardButton("В другом🚫")
markup.add(item1, item2, item3)
markup_new_or_not.add(item1_1, item2_1)
reply_markup = types.ReplyKeyboardRemove()

#Сопутствующие сообщения
#Перевод
trans = {
	"clear" : "ясно",
	"partly-cloudy" : "малооблачно",
	"cloudy" : "облачно",
	"overcast" : "пасмурно",
	"drizzle" : "морось",
	"light-rain" : "легкий дождь",
	"rain" : "дождь",
	"moderate-rain" : "несильный дождь",
	"heavy-rain" : "сильный дождь",
	"continuous-heavy-rain" : "продолжительный сильный дождь",
	"showers" : "ливень",
	"wet-snow" : "дождь со снегом",
	"light-snow" : "легкий снег",
	"snow" : "снег",
	"snow-showers" : "снегопад",
	"hail" : "град",
	"thunderstorm" : "гроза",
	"thunderstorm-with-rain" : "гроза со снегом",
	"thunderstorm-with-hail" : "гроза с градом"
}

#Условие для эмодзи
emodzi = {
	"clear" : "☀",
	"partly-cloudy" : "🌤",
	"cloudy" : "🌥",
	"overcast" : "☁",
	"drizzle" : "🌂",
	"light-rain" : "☂",
	"rain" : "💧",
	"moderate-rain" : "☂",
	"heavy-rain" : "☔",
	"continuous-heavy-rain" : "💦",
	"showers" : "💦",
	"wet-snow" : "🌨",
	"light-snow" : "❄",
	"snow" : "❄",
	"snow-showers" : "☃",
	"hail" : "🌧",
	"thunderstorm" : "🌩",
	"thunderstorm-with-rain" : "⛈",
	"thunderstorm-with-hail" : "⛈"
}

#Ветер
wind_trans = {
	"nw" : "северо-западный",
	"n" : "северный",
	"ne" : "северо-восточный",
	"e" : "восточный",
	"se" : "юго-восточный",
	"s" : "южный",
	"sw" : "юго-западный",
	"w" : "западный",
	"c" : "отсутствует"
}

moon_trans = {
	"moon-code-0" : "Полнолуние🌕",
	"moon-code-1" : "Убывающая луна🌖",
	"moon-code-2" : "Убывающая луна🌖",
	"moon-code-3" : "Убывающая луна🌖",
	"moon-code-4" : "Последняя четверть луны🌗",
	"moon-code-5" : "Убывающая луна🌘",
	"moon-code-6" : "Убывающая луна🌘",
	"moon-code-7" : "Убывающая луна🌘",
	"moon-code-8" : "Новолуние🌑",
	"moon-code-9" : "Растущая луна🌒",
	"moon-code-10" : "Растущая луна🌒",
	"moon-code-11" : "Растущая луна🌒",
	"moon-code-12" : "Первая четверть луны🌓",
	"moon-code-13" : "Растущая луна🌔",
	"moon-code-14" : "Растущая луна🌔",
	"moon-code-15" : "Растущая луна🌔",
}

#Месяца
month = {
	1 : "января",
	2 : "февраля",
	3 : "марта",
	4 : "апреля",
	5 : "мая",
	6 : "июня",
	7 : "июля",
	8 : "августа",
	9 : "сентября",
	10 : "октября",
	11 : "ноября",
	12 : "декабря"
}

#Цифры
nums = {
	0: "0⃣",
	1: "1⃣",
	2: "2⃣",
	3: "3⃣",
	4: "4⃣",
	5: "5⃣",
	6: "6⃣",
	7: "7⃣",
	8: "8⃣",
	9: "9⃣"
}

#Стартовое сообщение
@bot.message_handler(commands=['start'])
def welcome(message):
	#Стикер
	sti = open('img/welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)

	#Сообщение
	hello = bot.send_message(message.chat.id, "Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, который поможет тебе узнать погоду в любой точке мира!\n В каком городе хотели бы узнать погоду?".format(message.from_user, bot.get_me()), 
		parse_mode='html', reply_markup = reply_markup)

#Сообщения
@bot.message_handler(content_types=['text'])
def city_of_weather(message):
	#Город
	global city
	city = message.text

	#Попытка найти погоду
	google_url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?key=AIzaSyBRIZSlQ0_HbNKMkHE-DqPV1VM5N8N0fO4&input='+str(city)+'&inputtype=textquery&language=RU&fields=geometry'
	global req
	req = requests.get(google_url)

	#Если нашел
	if json.loads(req.text)["status"] == "OK":
		#Далее
		period = bot.send_message(message.chat.id, "Выберите, на какой период🌝", reply_markup = markup)
		bot.register_next_step_handler(period, type_of_weather)
	#Если не нашел
	else:
		#Стикер
		sti = open('img/error.webp', 'rb')
		bot.send_sticker(message.chat.id, sti)
		#Далее
		error = bot.send_message(message.chat.id, "Я не нашел такого города😢 Попробуй еще раз!", reply_markup = reply_markup)
		bot.register_next_step_handler(error, city_of_weather)

		

#На какой период
def type_of_weather(message):
	if message.chat.type == 'private':
		if message.text == 'Сейчас🕑':
			#Задание города
			lat = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lat"]
			lng = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lng"]
			#Поиск значений
			yandex_url = 'https://api.weather.yandex.ru/v2/forecast?lat='+str(lat)+'&lon='+str(lng)+'&lang=ru_RU&hours=false&extra=false'
			ya_req = requests.get(yandex_url, headers=headers)
			inf = json.loads(ya_req.text)['fact'] #Фактические значения

			#Параметры
			temp_now = inf['temp']
			feels_temp_now = inf['feels_like']
			condition = inf['condition']
			wind = inf['wind_speed']
			wind_dir = inf['wind_dir']
			press = inf['pressure_mm']

			#Условие на температуру
			if feels_temp_now <= 0:
				itog = "Зимааааа❄️"
			elif feels_temp_now > 0 and feels_temp_now <= 10:
				itog = "Прохладно, однако🧥"
			elif feels_temp_now > 10 and feels_temp_now <= 16:
				itog = "Я бы накинул курточку🧣"
			elif feels_temp_now > 16 and feels_temp_now <= 22:
				itog = "Почти тепло⛅️"
			elif feels_temp_now > 22 and feels_temp_now <= 28:
				itog = "Уф, лето на дворе☀️"
			elif feels_temp_now > 28:
				itog = "Жарааааааа🔥"

			

			#Итоговое сообщение
			bot.send_message(message.chat.id, "В городе {0} {1}{8}.\nТемпература воздуха: {2} C°. Ощущается как {3} C°.🌡\nВетер {4} {5} м/с🌬\nДавление {6} мм.рт.ст🕰\n{7}".format(city, trans[condition], str(temp_now), str(feels_temp_now), wind_trans[wind_dir], str(wind), press, itog, emodzi[condition]), reply_markup = reply_markup)

			#Далее
			want_more = bot.send_message(message.chat.id, "Хотите узнать что-то еще? В этом же городе или в другом?😉", reply_markup = markup_new_or_not)
			bot.register_next_step_handler(want_more, new_or_not)

		elif message.text == 'На день🌎':
			#Задание города
			lat = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lat"]
			lng = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lng"]
			#Поиск значений
			yandex_url = 'https://api.weather.yandex.ru/v2/forecast?lat='+str(lat)+'&lon='+str(lng)+'&lang=ru_RU&hours=true&extra=false'
			ya_req = requests.get(yandex_url, headers=headers)
			inf = json.loads(ya_req.text)['forecasts'][0] #Сегодня
			
			#Параметры
			sunrise = inf["sunrise"]
			sunset = inf["sunset"]
			moon = inf["moon_text"]

			#Ночью
			night = inf["parts"]["night"]
			night_temp = night["temp_avg"]
			night_cond = night["condition"]
			night_wind = night["wind_speed"]
			night_wind_dir = night["wind_dir"]
			night_press = night["pressure_mm"]

			#Утром
			morning = inf["parts"]["morning"]
			morning_temp = morning["temp_avg"]
			morning_cond = morning["condition"]
			morning_wind = morning["wind_speed"]
			morning_wind_dir = morning["wind_dir"]
			morning_press = morning["pressure_mm"]

			#Днем
			day = inf["parts"]["day"]
			day_temp = day["temp_avg"]
			day_cond = day["condition"]
			day_wind = day["wind_speed"]
			day_wind_dir = day["wind_dir"]
			day_press = day["pressure_mm"]

			#Вечером
			evening = inf["parts"]["evening"]
			evening_temp = evening["temp_avg"]
			evening_cond = evening["condition"]
			evening_wind = evening["wind_speed"]
			evening_wind_dir = evening["wind_dir"]
			evening_press = evening["pressure_mm"]

			#Сообщение
			bot.send_message(message.chat.id, ("Сегодня в городе {0} восход в {1}, закат в {2}.🏠 {27}\n\n🌃Ночью {3}{4}.\nТемпература воздуха {5} C°.🌡 \nВетер {6} {7} м/с.🌬\nДавление {8} мм.рт.ст🕰"
				+ "\n\n🌄Утром {9}{10}.\nТемпература воздуха {11} C°.🌡  \nВетер {12} {13} м/с.🌬\nДавление {14} мм.рт.ст🕰"
				+ "\n\n🌞Днем {15}{16}.\nТемпература воздуха {17} C°.🌡  \nВетер {18} {19} м/с.🌬\nДавление {20} мм.рт.ст🕰"
				+ "\n\n🌇Вечером {21}{22}.\nТемпература воздуха {23} C°.🌡  \nВетер {24} {25} м/с.🌬\nДавление {26} мм.рт.ст🕰" + "\n\nОдевайтесь по погоде!🧣").format(city, sunrise, sunset, 
				trans[night_cond], emodzi[night_cond], night_temp, wind_trans[night_wind_dir], night_wind, night_press, 
				trans[morning_cond], emodzi[morning_cond], morning_temp, wind_trans[morning_wind_dir], morning_wind, morning_press, 
				trans[day_cond], emodzi[day_cond], day_temp, wind_trans[day_wind_dir], day_wind, day_press, 
				trans[evening_cond], emodzi[evening_cond], evening_temp, wind_trans[evening_wind_dir], evening_wind, evening_press, 
				moon_trans[moon]), reply_markup = reply_markup)

			#Далее
			want_more = bot.send_message(message.chat.id, "Хотите узнать что-то еще? В этом же городе или в другом?😉", reply_markup = markup_new_or_not)
			bot.register_next_step_handler(want_more, new_or_not)

		elif message.text == "На 5️⃣ дней":
			#Задание города
			lat = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lat"]
			lng = json.loads(req.text)["candidates"][0]["geometry"]["location"]["lng"]
			#Поиск значений
			yandex_url = 'https://api.weather.yandex.ru/v2/forecast?lat='+str(lat)+'&lon='+str(lng)+'&lang=ru_RU&hours=true&extra=false'
			ya_req = requests.get(yandex_url, headers=headers)
			inf = json.loads(ya_req.text)['forecasts']
			day1 = inf[1]
			day2 = inf[2]
			day3 = inf[3]
			day4 = inf[4]
			day5 = inf[5]

			#Day1
			day1_date = day1["date"].split('-')

			#Превращение числа даты в эмодзи
			if int(day1_date[2]) < 10:
				day1_day_em = nums[int(day1_date[2][1])]
			else:
				mod = int(day1_date[2]) % 10
				cel = int(day1_date[2]) // 10
				day1_day_em = nums[cel] + nums[mod]

			day1_date = day1_day_em + ' ' + month[int(day1_date[1])] + ' ' + str(day1_date[0])
			sunrise1 = day1["sunrise"]
			sunset1 = day1["sunset"]
			day1 = day1["parts"]["day_short"]
			day1_temp = day1["temp"]
			day1_feels_like = day1["feels_like"]
			day1_cond = day1["condition"]
			day1_wind = day1["wind_speed"]
			day1_wind_dir = day1["wind_dir"]
			day1_press = day1["pressure_mm"]

			#Day2
			day2_date = day2["date"].split('-')
			#Превращение числа даты в эмодзи
			if int(day2_date[2])  < 10:
				day2_day_em = nums[int(day2_date[2][1])]
			else:
				mod = int(day2_date[2]) % 10
				cel = int(day2_date[2]) // 10
				day2_day_em = nums[cel] + nums[mod]

			day2_date = day2_day_em + ' ' + month[int(day2_date[1])] + ' ' + str(day2_date[0])
			sunrise2 = day2["sunrise"]
			sunset2 = day2["sunset"]
			day2 = day2["parts"]["day_short"]
			day2_temp = day2["temp"]
			day2_feels_like = day2["feels_like"]
			day2_cond = day2["condition"]
			day2_wind = day2["wind_speed"]
			day2_wind_dir = day2["wind_dir"]
			day2_press = day2["pressure_mm"]

			#Day3
			day3_date = day3["date"].split('-')
			#Превращение числа даты в эмодзи
			if int(day3_date[2])  < 10:
				day3_day_em = nums[int(day3_date[2][1])]
			else:
				mod = int(day3_date[2]) % 10
				cel = int(day3_date[2]) // 10
				day3_day_em = nums[cel] + nums[mod]

			day3_date = day3_day_em + ' ' + month[int(day3_date[1])] + ' ' + str(day3_date[0])
			sunrise3 = day3["sunrise"]
			sunset3 = day3["sunset"]
			day3 = day3["parts"]["day_short"]
			day3_temp = day3["temp"]
			day3_feels_like = day3["feels_like"]
			day3_cond = day3["condition"]
			day3_wind = day3["wind_speed"]
			day3_wind_dir = day3["wind_dir"]
			day3_press = day3["pressure_mm"]

			#Day4
			day4_date = day4["date"].split('-')
			#Превращение числа даты в эмодзи
			if int(day4_date[2])  < 10:
				day4_day_em = nums[int(day4_date[2][1])]
			else:
				mod = int(day4_date[2]) % 10
				cel = int(day4_date[2]) // 10
				day4_day_em = nums[cel] + nums[mod]

			day4_date = day4_day_em + ' ' + month[int(day4_date[1])] + ' ' + str(day4_date[0])
			sunrise4 = day4["sunrise"]
			sunset4 = day4["sunset"]
			day4 = day4["parts"]["day_short"]
			day4_temp = day4["temp"]
			day4_feels_like = day4["feels_like"]
			day4_cond = day4["condition"]
			day4_wind = day4["wind_speed"]
			day4_wind_dir = day4["wind_dir"]
			day4_press = day4["pressure_mm"]

			#Day5
			day5_date = day5["date"].split('-')
			#Превращение числа даты в эмодзи
			if int(day5_date[2])  < 10:
				day5_day_em = nums[int(day5_date[2][1])]
			else:
				mod = int(day5_date[2]) % 10
				cel = int(day5_date[2]) // 10
				day5_day_em = nums[cel] + nums[mod]

			day5_date = day5_day_em + ' ' + month[int(day5_date[1])] + ' ' + str(day5_date[0])
			sunrise5 = day5["sunrise"]
			sunset5 = day5["sunset"]
			day5 = day5["parts"]["day_short"]
			day5_temp = day5["temp"]
			day5_feels_like = day5["feels_like"]
			day5_cond = day5["condition"]
			day5_wind = day5["wind_speed"]
			day5_wind_dir = day5["wind_dir"]
			day5_press = day5["pressure_mm"]

			#Сообщение
			bot.send_message(message.chat.id, ("🏠В городе {0}:\n\n{1} {2}{3} \nВосход в {4}, закат в {5}🌇\nТемпература воздуха {6} C°.🌡 \nВетер {7} {8} м/с.🌬\nДавление {9} мм.рт.ст🕰"
				+ "\n\n{10} {11}{12}.\nВосход в {13}, закат в {14}🌇\nТемпература воздуха {15} C°.🌡  \nВетер {16} {17} м/с.🌬\nДавление {18} мм.рт.ст🕰"
				+ "\n\n{19} {20}{21}.\nВосход в {22}, закат в {23}🌇\nТемпература воздуха {24} C°.🌡  \nВетер {25} {26} м/с.🌬\nДавление {27} мм.рт.ст🕰"
				+ "\n\n{28} {29}{30}.\nВосход в {31}, закат в {32}🌇\nТемпература воздуха {33} C°.🌡  \nВетер {34} {35} м/с.🌬\nДавление {36} мм.рт.ст🕰"
				+ "\n\n{37} {38}{39}.\nВосход в {40}, закат в {41}🌇\nТемпература воздуха {42} C°.🌡  \nВетер {43} {44} м/с.🌬\nДавление {45} мм.рт.ст🕰" + "\n\nНе болейте!😷").format(city, 
				day1_date, trans[day1_cond], emodzi[day1_cond], sunrise1, sunset1,  day1_temp, wind_trans[day1_wind_dir], day1_wind, day1_press,
				day2_date, trans[day2_cond], emodzi[day2_cond], sunrise2, sunset2,  day2_temp, wind_trans[day2_wind_dir], day2_wind, day2_press,
				day3_date, trans[day3_cond], emodzi[day3_cond], sunrise3, sunset3,  day3_temp, wind_trans[day3_wind_dir], day3_wind, day3_press,
				day4_date, trans[day4_cond], emodzi[day4_cond], sunrise4, sunset4,  day4_temp, wind_trans[day4_wind_dir], day4_wind, day4_press,
				day5_date, trans[day5_cond], emodzi[day5_cond], sunrise5, sunset5,  day5_temp, wind_trans[day5_wind_dir], day5_wind, day5_press), reply_markup = reply_markup)

			#Далее
			want_more = bot.send_message(message.chat.id, "Хотите узнать что-то еще? В этом же городе или в другом?😉", reply_markup = markup_new_or_not)
			bot.register_next_step_handler(want_more, new_or_not)

		else:
			i_dont_know = bot.send_message(message.chat.id, "Я не знаю, что ответить, используйте дополнительную клавиатуру😒")
			bot.register_next_step_handler(i_dont_know, type_of_weather)

#Сменить ли город?
def new_or_not(message):
	if message.chat.type == 'private':
		if message.text == 'В этом же🎲':
			#Далее
			period = bot.send_message(message.chat.id, "Выберите, на какой период🌝", reply_markup = markup)
			bot.register_next_step_handler(period, type_of_weather)

		elif message.text == 'В другом🚫':
			another_city = bot.send_message(message.chat.id, "Введите название города😁", reply_markup = reply_markup)
			bot.register_next_step_handler(another_city, city_of_weather)

		else:
			i_dont_know = bot.send_message(message.chat.id, "Я не знаю, что ответить, используйте дополнительную клавиатуру😒")
			bot.register_next_step_handler(i_dont_know, new_or_not)

bot.polling(none_stop=True)