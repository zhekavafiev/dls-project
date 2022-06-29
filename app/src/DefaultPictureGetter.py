class DefaultPictureGetter:
    def get(self, text):
        if (text == 'Ван гог'):
            file_name_style = "./default_stiles/van_gog.jpg"
        if (text == 'Пикассо'):
            file_name_style = "./default_stiles/pikasso.jpeg"
        if (text == 'Космос'):
            file_name_style = "./default_stiles/kosmos.jpg"
        if (text == 'Мазки'):
            file_name_style = "./default_stiles/mazki.jpg"
        if (text == 'Лава'):
            file_name_style = "./default_stiles/lava.jpg"
        if (text == 'Лёд'):
            file_name_style = "./default_stiles/led.jpg"
        return file_name_style