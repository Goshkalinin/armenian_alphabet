import csv, telebot, os, requests
from PIL import Image, ImageFilter, ImageFont, ImageDraw
from random import randint, choice


def get_word():


    next_csv = open('Text/next_csv.txt', 'r', encoding='utf-8')
    next_csv_num = int(next_csv.read())


    words_csv = list(os.listdir("Text/AlphaCSV/"))
    words_csv = sorted(words_csv)
    csvs = len(words_csv)-1

    n = 0
    for i in words_csv:
        # print(i)
        # print(n)
        n += 1

    with open('Text/AlphaCSV/' + words_csv[next_csv_num], mode="r+", encoding='utf-8') as words_csv:
        words_list = list(csv.reader(words_csv, delimiter=','))
        random_word = words_list[randint(2,len(words_list)-1)]


    next_csv = open('Text/next_csv.txt', 'w', encoding='utf-8')
    if next_csv_num < csvs:
        next_csv.write(str(next_csv_num+1))
    else:
        next_csv.write(str(0))
    letter_description_list = []
    for i in words_list[1]:
        if len(i) > 0:
            letter_description_list.append(i)

    letter_description_list_num = randint(0, len(letter_description_list)-1)



    ru_letter = words_list[0][0]
    am_letter = words_list[0][1]+words_list[0][2]
    letter_name = words_list[0][3]
    letter_transcript = words_list[0][4]
    letter_description = words_list[1][letter_description_list_num]
    am_word = random_word[1]
    query = random_word[2]
    word = random_word[3]
    translit = random_word[4]

    return( ru_letter,
            am_letter,
            letter_name,
            letter_transcript,
            letter_description,
            am_word,
            query,
            word,
            translit

            )


def download_im(query):
    url = 'https://loremflickr.com/1000/1000/' + query
    link = requests.get(url, allow_redirects=True)
    real_path = link.url
    bober = "https://loremflickr.com/cache/resized/defaultImage.small_1000_1000_nofilter.jpg"
    if real_path != bober:
        open("RawPics/" + query + '.jpg', 'wb').write(link.content)
    else:
        link = requests.get('https://loremflickr.com/1000/1000/cat', allow_redirects=True)
        open("RawPics/" + query + '.jpg', 'wb').write(link.content)


def make_picture(   ru_letter,
                    am_letter,
                    letter_name,
                    letter_transcript,
                    letter_description,
                    am_word,
                    query,
                    word,
                    translit

                    ):

    def random_case(b):

        a = randint(0,1)
        if a == 0:
            return  b.lower()
        else:
            return b.upper()



    ru_font = ImageFont.truetype("Fonts/"+'micross.ttf', 60)

    word = random_case(word)
    translit = "[" + translit + "]"


    pic = query + ".jpg"
    original = Image.open("RawPics/" + pic)

    blurred = original.filter(ImageFilter.GaussianBlur(20))
    mask = Image.new("L", original.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((100, 150, 900, 900), fill=255)
    mask_blur = mask.filter(ImageFilter.GaussianBlur(20))

    final = Image.composite(original, blurred, mask_blur)
    draw = ImageDraw.Draw(final)
    draw.rectangle((0, 0, 1000, 120), fill=(0, 0, 0))  # upper block
    draw.rectangle((0, 880, 1000, 1000), fill=(0, 0, 0))  # bottom block

    final.putalpha(255)


    gradient_list = os.listdir('Gradients/')
    gradient = Image.open('Gradients/' + gradient_list[randint(0,4)]).rotate(360/choice([1, 2, 4, -2, -4])).resize((1000,1000))  # открываем картинку с градиентом
    alpha = Image.new('L', (1000,1000))
    draw = ImageDraw.Draw(alpha)

    draw.text((55,25),word, fill='white',font = ru_font)
    draw.text((955, 25),"    (" + ru_letter + ")     " +  letter_name + ": " + am_letter,fill='white', font = ru_font, anchor="ra")

    draw.text((55, 905), am_word,fill='white', font = ru_font)  # am word
    draw.text((955, 905), translit, fill='white', font = ru_font, anchor="ra")

    draw.line([(0, 120), (1000, 120)], fill ='white', width = 5)
    draw.line([(0, 880), (1000, 880)], fill ='white', width = 5)

    gradient.putalpha(alpha)  # нашлёпываем картинку с альфой на градиет
    blur = gradient.filter(ImageFilter.GaussianBlur(4))

    test = Image.alpha_composite(final, blur)
    draw = ImageDraw.Draw(test)

    draw.text((50,20),word, fill='white',font = ru_font)
    draw.text((950, 20),"    (" + ru_letter + ")     " + letter_name + ": " + am_letter, (255, 255, 255), font = ru_font, anchor="ra")

    draw.text((50, 900), am_word, (255, 255, 255), font = ru_font)  # am word
    draw.text((950, 900), translit, (255, 255, 255), font = ru_font, anchor="ra")

    final = Image.new("RGB", (1000,1000), (255, 255, 255))
    final.paste(test, mask=test.split()[3]) # 3 is the alpha channel

    final.save("FinalPics/" + pic, 'JPEG', quality=100)


def make_tg_post(photo, massage, audio):


    photo = open(photo, 'rb')

    bot_token = '5435386776:AAEHm6zODpgVKo65jI8CIQKL4o3yL80S9Fc'

    # channel_name = "-1001577133132" # Goshka test channel
    channel_name = "@armenianalphabet"

    bot = telebot.TeleBot(token = bot_token)

    try:
        audio = open(audio, 'rb')
        bot.send_audio(channel_name, audio, disable_notification = True)
        bot.send_photo(channel_name, photo, massage, parse_mode = "MARKDOWN", disable_notification = True )
    except:
        bot.send_photo(channel_name, photo, massage, parse_mode = "MARKDOWN", disable_notification = True )

def process():

    base =  get_word()
    ru_letter = base[0]
    am_letter = base[1]
    letter_name = base[2]
    letter_transcript = base[3]
    letter_description = base[4]
    am_word = base[5]
    query = base[6]
    word = base[7]
    translit = base[8]

    photo = "FinalPics/" + query + ".jpg"
    massage  = "*" + am_letter + " — " + letter_name + "*" + "\n" + letter_description
    print(am_letter)
    audio = "Audio/" + am_letter + ".mp3"

    download_im(query)
    make_picture(   ru_letter,
                    am_letter,
                    letter_name,
                    letter_transcript,
                    letter_description,
                    am_word,
                    query,
                    word,
                    translit

                    )



    make_tg_post(photo, massage, audio)

    print(ru_letter)

# for i in range(0, 44):
#     print(i)
#     process()


process()





