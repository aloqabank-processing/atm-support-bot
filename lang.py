ru = {
    '1': 'Отправить номер телефона',
    '2': 'В этом боте вы можете оставлять свои жалобы по работе банкоматов, а также свои предложения по улучшению сервиса.',
    '3': 'Введите комментарий с жалобой',
    '4': 'Здравствуйте! Благодарим за обращение! Передали в отдел контроля качества, в ближайшее время предоставят Вам обратную связь! Нажмите кнопку "Далее" если хотите оставить еще одно обращение',
    '5': "Другое",
    '6': "Здравствуйте! Благодарим за обращение! Передали в отдел контроля качества, к сожалению сейчас нерабочие часы. С вами свяжутся в рабочее время. Мы работаем с понедельника по пятницу, с 9:00 до 18:00. Нажмите кнопку 'Далее' если хотите оставить еще одно обращение",
    '7': "🇷🇺Язык выбран",
    '8': "Сфотографируйте QR код на банкомате и отправте фотографию в этот чат. Так мы узнаем с каким именно банкоматом произошла проблема",
    '9': "Нет возможности отправить фото",
    '10': "QR код плохо виден на фото. Попробуйте сфоткать его поближе и по возможности обрезать лишние части фото",
    '11': "Банкомат захватил карту",
    '12': "Ввести ID банкомата вручную",
    '13': "Введите ID банкомата. Узнать вы его можете рядом с QR-кодом банкомата",
    '14': "Проблемы с выдачей наличных",
    '15': "Банкомата с таким идентификатором не существует. \n Сфотографируйте QR код и отправьте мне или попробуйте ввести ID банкомата заново",
    '16': "Далее", 
    '17': "Проблема с банкоматом",
    '18': "Перевыпуск карты",
    '19': "Мои заявки",
    '20': "Выберите категорию проблемы",
    '21': "Нам необходимо узнать с каким банкоматом произошла проблема. Для этого вам необходимо ниже выбрать метод определения банкомата",
    '22': "По локации",
    '23': "По QR-коду",
    '24': "Назад",
    '25': "Нажмите на кнопку ниже чтобы отправить локацию. По ней мы определим банкомат",
    '26': "Отправить локацию",
    '26': "Напишите свои \n ФИО: \n Номер карты: (пример - 986019******0011) \n МФО от куда: \n МФО куда:",
}

uz = {
    '1': 'Telefon raqamini yuboring',
    '2': "Ushbu botda siz bankomat ishi bo'yicha shikoyatlaringizni, shuningdek xizmatni yaxshilash bo'yicha takliflaringizni qoldirishingiz mumkin.",
    '3': "Shikoyat bilan sharhni kiriting",
    '4': "Salom! Murojaat qilganingiz uchun tashakkur! Sifat nazorati bo'limiga topshirildi, yaqin kelajakda ular sizga fikr-mulohazalarni taqdim etadilar!",
    '5': "Boshqalar",
    '6': "Salom! Murojaat qilganingiz uchun tashakkur! Sifat nazorati bo'limiga topshirildi, afsuski, endi ish vaqti yo'q. Ular ish vaqtida siz bilan bog'lanishadi. Biz dushanbadan jumagacha, soat 9:00 dan 18:00 gacha ishlaymiz.",
    '7': "🇺🇿Til tanlangan",
    '8': "Bankomatda QR kodini suratga oling va fotosuratni ushbu suhbatga yuboring. Shunday qilib, biz qaysi bankomatda muammo yuz berganini aniq bilib olamiz",
    '9': "Fotosuratni yuborish imkoniyati yo'q",
    '10': "QR kodi fotosuratda ko'rinmaydi. Uni yaqinroq suratga olishga harakat qiling va iloji bo'lsa, fotosuratning qo'shimcha qismlarini kesib oling",
    '11': "Bankomat kartani yutib yubordi",
    '12': "Seriya raqamini qo'lda kiriting",
    '13': "Bankomat ID kiriting. Siz uni bankomatning QR kodi yonida bilib olishingiz mumkin",
    '14': "Naqd pul berish bilan bog'liq muammolar",
    '15': "Bunday identifikatorga ega bankomat yo'q \n QR kodini suratga oling va menga yuboring yoki bankomat identifikatorini qayta kiritishga harakat qiling",
    '16': "Keyingi",
    '17': "Bankomat muammosi",
    '18': "Kartani qayta chiqarish",
    '19': "Mening arizalarim",
    '20': "Muammo toifasini tanlang",
    '21': "Qaysi bankomatda muammo borligini bilishimiz kerak. Buning uchun quyida bankomatni aniqlash usulini tanlashingiz kerak",
    '22': "Joylashuv bo'yicha",
    '23': "QR kodi bo'yicha",
    '24': "Orqaga",
    '25': "Quyidagi tugmani bosing joylashuvni yuborish uchun. Undan biz bankomatni aniqlaymiz",
    '26': "Joylashuvni yuboring",
    # for example:
    # 'key': 'value"
}


def get_language(call_data):
    if call_data == "Ru":
        return ru
    elif call_data == "Uz":
        return uz
    else:
        return None
