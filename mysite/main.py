import os
import django
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from booking_app.models import (
    Country, UserProfile, City, Service, Hotel,
    HotelImage, Room, RoomImage, Booking, Review
)


def clear_data():
    """Очистка всех данных"""
    print("Очистка базы данных...")
    Review.objects.all().delete()
    Booking.objects.all().delete()
    RoomImage.objects.all().delete()
    Room.objects.all().delete()
    HotelImage.objects.all().delete()
    Hotel.objects.all().delete()
    Service.objects.all().delete()
    City.objects.all().delete()
    UserProfile.objects.all().delete()
    Country.objects.all().delete()
    print("База данных очищена")


def populate_countries():
    """Создание стран"""
    print("Создание стран...")

    countries_data = [
        {'en': 'Kyrgyzstan', 'ru': 'Кыргызстан'},
        {'en': 'Kazakhstan', 'ru': 'Казахстан'},
        {'en': 'Uzbekistan', 'ru': 'Узбекистан'},
        {'en': 'Turkey', 'ru': 'Турция'},
        {'en': 'United Arab Emirates', 'ru': 'ОАЭ'},
        {'en': 'Russia', 'ru': 'Россия'},
        {'en': 'Georgia', 'ru': 'Грузия'},
        {'en': 'Thailand', 'ru': 'Таиланд'},
        {'en': 'Italy', 'ru': 'Италия'},
        {'en': 'France', 'ru': 'Франция'}
    ]

    countries = []
    for country_data in countries_data:
        country = Country.objects.create(
            country_name_en=country_data['en'],
            country_name_ru=country_data['ru'],
            country_image=f'country_images/{country_data["en"].lower().replace(" ", "_")}.png'
        )
        countries.append(country)

    print(f"Создано {len(countries)} стран")
    return countries


def populate_cities(countries):
    """Создание городов"""
    print("Создание городов...")

    cities_data = {
        'Kyrgyzstan': [
            {'en': 'Bishkek', 'ru': 'Бишкек'},
            {'en': 'Osh', 'ru': 'Ош'},
            {'en': 'Issyk-Kul', 'ru': 'Иссык-Куль'},
            {'en': 'Karakol', 'ru': 'Каракол'}
        ],
        'Kazakhstan': [
            {'en': 'Almaty', 'ru': 'Алматы'},
            {'en': 'Astana', 'ru': 'Астана'},
            {'en': 'Shymkent', 'ru': 'Шымкент'}
        ],
        'Uzbekistan': [
            {'en': 'Tashkent', 'ru': 'Ташкент'},
            {'en': 'Samarkand', 'ru': 'Самарканд'},
            {'en': 'Bukhara', 'ru': 'Бухара'}
        ],
        'Turkey': [
            {'en': 'Istanbul', 'ru': 'Стамбул'},
            {'en': 'Antalya', 'ru': 'Анталья'},
            {'en': 'Ankara', 'ru': 'Анкара'}
        ],
        'United Arab Emirates': [
            {'en': 'Dubai', 'ru': 'Дубай'},
            {'en': 'Abu Dhabi', 'ru': 'Абу-Даби'}
        ],
        'Russia': [
            {'en': 'Moscow', 'ru': 'Москва'},
            {'en': 'Saint Petersburg', 'ru': 'Санкт-Петербург'}
        ],
        'Georgia': [
            {'en': 'Tbilisi', 'ru': 'Тбилиси'},
            {'en': 'Batumi', 'ru': 'Батуми'}
        ],
        'Thailand': [
            {'en': 'Bangkok', 'ru': 'Бангкок'},
            {'en': 'Phuket', 'ru': 'Пхукет'}
        ],
        'Italy': [
            {'en': 'Rome', 'ru': 'Рим'},
            {'en': 'Venice', 'ru': 'Венеция'}
        ],
        'France': [
            {'en': 'Paris', 'ru': 'Париж'},
            {'en': 'Nice', 'ru': 'Ницца'}
        ]
    }

    cities = []
    for country in countries:
        country_name_en = country.country_name_en
        if country_name_en in cities_data:
            for city_data in cities_data[country_name_en]:
                city = City.objects.create(
                    country=country,
                    city_name_en=city_data['en'],
                    city_name_ru=city_data['ru'],
                    city_image=f'city_images/{city_data["en"].lower()}.png'
                )
                cities.append(city)

    print(f"Создано {len(cities)} городов")
    return cities


def populate_services():
    """Создание услуг"""
    print("Создание услуг...")

    services_data = [
        {'en': 'Free WiFi', 'ru': 'Бесплатный WiFi'},
        {'en': 'Swimming Pool', 'ru': 'Бассейн'},
        {'en': 'Spa & Wellness', 'ru': 'Спа и велнес'},
        {'en': 'Restaurant', 'ru': 'Ресторан'},
        {'en': 'Free Parking', 'ru': 'Бесплатная парковка'},
        {'en': 'Fitness Center', 'ru': 'Фитнес-центр'},
        {'en': 'Conference Room', 'ru': 'Конференц-зал'},
        {'en': 'Airport Transfer', 'ru': 'Трансфер из аэропорта'},
        {'en': 'Room Service 24/7', 'ru': 'Обслуживание номеров 24/7'},
        {'en': 'Pet Friendly', 'ru': 'Можно с питомцами'}
    ]

    services = []
    for service_data in services_data:
        service = Service.objects.create(
            service_name_en=service_data['en'],
            service_name_ru=service_data['ru'],
            service_image=f'service_images/{service_data["en"].lower().replace(" ", "_")}.png'
        )
        services.append(service)

    print(f"Создано {len(services)} услуг")
    return services

def populate_users(countries):
    print("Создание пользователей...")

    clients_data = [
        {'first': 'John', 'last': 'Smith',  'username': 'johnsmith',    'age': 32, 'phone': '+996555111222'},
        {'first': 'Emma', 'last': 'Johnson','username': 'emmaj',        'age': 28, 'phone': '+996777222333'},
        {'first': 'Michael', 'last': 'Brown','username': 'mikebrown',   'age': 35, 'phone': '+996700333444'},
        {'first': 'Sophia', 'last': 'Davis','username': 'sophiad',      'age': 29, 'phone': '+996555444555'},
        {'first': 'Daniel', 'last': 'Wilson','username': 'danwilson',   'age': 41, 'phone': '+996770555666'},
    ]

    owners_data = [
        {'first': 'Alexander', 'last': 'Petrov','username': 'alexpetrov',    'age': 45, 'phone': '+996555666777'},
        {'first': 'Victoria', 'last': 'Ivanova','username': 'vickyivanov',   'age': 38, 'phone': '+996777777888'},
        {'first': 'Dmitry', 'last': 'Sokolov',  'username': 'dmitrysokolov', 'age': 42, 'phone': '+996700888999'},
        {'first': 'Elena', 'last': 'Kozlova',   'username': 'elenakozlova',  'age': 40, 'phone': '+996555999000'},
        {'first': 'Sergey', 'last': 'Morozov',  'username': 'sergeymorozov', 'age': 50, 'phone': '+996770000111'},
    ]

    clients = []
    owners = []

    for i, client_data in enumerate(clients_data, 1):
        client = UserProfile.objects.create(
            username=client_data['username'],
            email=f'client{i}@example.com',
            password=make_password('password123'),
            first_name=client_data['first'],
            last_name=client_data['last'],
            age=client_data['age'],
            phone_number=client_data['phone'],
            country=random.choice(countries),
            user_role='client',
            photo=f'user_images/client{i}.png'
        )
        clients.append(client)

    for i, owner_data in enumerate(owners_data, 1):
        owner = UserProfile.objects.create(
            username=owner_data['username'],
            email=f'owner{i}@example.com',
            password=make_password('password123'),
            first_name=owner_data['first'],
            last_name=owner_data['last'],
            age=owner_data['age'],
            phone_number=owner_data['phone'],
            country=random.choice(countries),
            user_role='owner',
            photo=f'user_images/owner{i}.png'
        )
        owners.append(owner)

    print(f"Создано {len(clients)} клиентов и {len(owners)} владельцев")

    return clients, owners


def populate_hotels(cities, services, owners):
    """Создание отелей"""
    print("Создание отелей...")

    hotels_data = [
        {
            'name_en': 'Grand Plaza Hotel',
            'name_ru': 'Гранд Плаза Отель',
            'street_en': '123 Main Street',
            'street_ru': 'Главная улица, 123',
            'desc_en': 'Luxury 5-star hotel in the heart of the city...',
            'desc_ru': 'Роскошный 5-звездочный отель в самом центре города...',
            'stars': 5,
            'postal': 720000
        },
        {
            'name_en': 'Royal Palace Resort',
            'name_ru': 'Роял Палас Резорт',
            'street_en': '456 Beach Avenue',
            'street_ru': 'Пляжная улица, 456',
            'desc_en': 'Beachfront resort with private beach access. All-inclusive service, water sports, kids club, and evening entertainment. Ideal for family vacations.',
            'desc_ru': 'Курортный отель на берегу с частным пляжем. Услуга все включено, водные виды спорта, детский клуб и вечерние развлечения. Идеален для семейного отдыха.',
            'stars': 5,
            'postal': 720001
        },
        {
            'name_en': 'City Comfort Inn',
            'name_ru': 'Сити Комфорт Инн',
            'street_en': '789 Central Boulevard',
            'street_ru': 'Центральный бульвар, 789',
            'desc_en': 'Modern 4-star hotel near major attractions. Comfortable rooms, business center, fitness gym, and complimentary breakfast. Great value for money.',
            'desc_ru': 'Современный 4-звездочный отель рядом с главными достопримечательностями. Комфортные номера, бизнес-центр, фитнес-зал и бесплатный завтрак. Отличное соотношение цены и качества.',
            'stars': 4,
            'postal': 720002
        },
        {
            'name_en': 'Mountain View Lodge',
            'name_ru': 'Маунтин Вью Лодж',
            'street_en': '321 Alpine Road',
            'street_ru': 'Альпийская дорога, 321',
            'desc_en': 'Cozy mountain resort with stunning views. Ski-in/ski-out access,'
                       ' fireplace lounges, and traditional cuisine. Perfect winter getaway destination.',
            'desc_ru': 'Уютный горный курорт с потрясающими видами. Прямой выход на склоны,'
                       ' лаунжи с камином и традиционная кухня. Идеальное место для зимнего отдыха.',
            'stars': 4,
            'postal': 720003
        },
        {
            'name_en': 'Business Tower Hotel',
            'name_ru': 'Бизнес Тауэр Отель',
            'street_en': '654 Corporate Drive',
            'street_ru': 'Корпоративная улица, 654',
            'desc_en': 'Premium business hotel with state-of-art facilities. Large conference halls, executive lounge,'
                       ' express check-in, and airport shuttle.',
            'desc_ru': 'Премиальный бизнес-отель с современным оборудованием. Большие конференц-залы, executive лаунж, '
                       'экспресс регистрация и трансфер в аэропорт.',
            'stars': 5,
            'postal': 720004
        },
        {
            'name_en': 'Seaside Paradise Hotel',
            'name_ru': 'Сисайд Парадайз Отель',
            'street_en': '987 Ocean Drive',
            'street_ru': 'Океанская улица, 987',
            'desc_en': 'Tropical paradise hotel with ocean views. Private villas, infinity pool, spa treatments, '
                       'and gourmet restaurants. Romantic couples retreat.',
            'desc_ru': 'Тропический райский отель с видом на океан. Частные виллы, инфинити бассейн,'
                       ' спа-процедуры и ресторан для гурманов. Романтический отдых для пар.',
            'stars': 5,
            'postal': 720005
        },
        {
            'name_en': 'Heritage Boutique Hotel',
            'name_ru': 'Херитаж Бутик Отель',
            'street_en': '147 Old Town Square',
            'street_ru': 'Площадь Старого Города, 147',
            'desc_en': 'Historic boutique hotel in restored building. Unique design rooms, rooftop terrace, '
                       'art gallery, and authentic local cuisine restaurant.',
            'desc_ru': 'Исторический бутик-отель в восстановленном здании. Уникальные дизайнерские номера,'
                       ' терраса на крыше, художественная галерея и ресторан местной кухни.',
            'stars': 4,
            'postal': 720006
        },
        {
            'name_en': 'Green Valley Resort',
            'name_ru': 'Грин Вэлли Резорт',
            'street_en': '258 Nature Trail',
            'street_ru': 'Природная тропа, 258',
            'desc_en': 'Eco-friendly resort surrounded by nature. Organic farm-to-table dining, '
                       'yoga pavilion, hiking trails, and wildlife tours.',
            'desc_ru': 'Экологичный курорт в окружении природы. Органическая ферма с рестораном,'
                       ' павильон для йоги, пешие маршруты и туры для наблюдения за дикой природой.',
            'stars': 4,
            'postal': 720007
        },
        {
            'name_en': 'Urban Style Hotel',
            'name_ru': 'Урбан Стайл Отель',
            'street_en': '369 Fashion Street',
            'street_ru': 'Модная улица, 369',
            'desc_en': 'Trendy hotel in shopping district. Modern minimalist design, rooftop bar,'
                       ' late-night room service, and walking distance to entertainment.',
            'desc_ru': 'Модный отель в торговом районе. Современный минималистичный дизайн, бар на крыше,'
                       ' круглосуточное обслуживание номеров и в шаговой доступности развлечения.',
            'stars': 4,
            'postal': 720008
        },
        {
            'name_en': 'Family Garden Hotel',
            'name_ru': 'Фэмили Гарден Отель',
            'street_en': '741 Park Lane',
            'street_ru': 'Парковая аллея, 741',
            'desc_en': 'Family-oriented hotel with spacious suites. Kids playground, family pool, '
                       'babysitting service, and children s menu. Safe and comfortable environment.',
            'desc_ru': 'Семейный отель с просторными номерами. Детская площадка, семейный бассейн, '
                       'услуги няни и детское меню. Безопасная и комфортная обстановка.',
            'stars': 3,
            'postal': 720009
        }
    ]

    hotels = []
    for i, hotel_data in enumerate(hotels_data):
        city = random.choice(cities)
        hotel = Hotel.objects.create(
            hotel_name_en=hotel_data['name_en'],
            hotel_name_ru=hotel_data['name_ru'],
            street_en=hotel_data['street_en'],
            street_ru=hotel_data['street_ru'],
            postal_code=hotel_data['postal'],
            city=city,
            country=city.country,
            hotel_stars=hotel_data['stars'],
            hotel_video=f'hotel_videos/hotel_{i + 1}.mp4',
            description_en=hotel_data['desc_en'],
            description_ru=hotel_data['desc_ru'],
            owner=random.choice(owners)
    )

    hotel_services = random.sample(services, random.randint(4, 8))
    hotel.service.set(hotel_services)

    hotels.append(hotel)

    for j in range(4):
        HotelImage.objects.create(
            hotel=hotel,
            image=f'hotel_images/hotel_{i + 1}_{j + 1}.png'
        )

    print(f"Создано {len(hotels)} отелей и {len(hotels) * 4} изображений")
    return hotels


def populate_rooms(hotels):
        print("Создание номеров...")

        room_types = ['стандарт', 'семейный', 'одноместный', 'люкс']
        room_statuses = ['занят', 'забронирован', 'свободен']

        room_descriptions = {
            'стандарт': {
                'en': 'Comfortable standard room with modern amenities. Queen-size bed, work desk, '
                      'flat-screen TV, mini-bar, and private bathroom with shower.',
                'ru': 'Комфортабельный стандартный номер с современными удобствами. Двуспальная кровать,'
                      ' рабочий стол, телевизор с плоским экраном, мини-бар и собственная ванная комната с душем.'
            },
            'семейный': {
                'en': 'Spacious family room with separate sleeping areas. Two double beds, sofa, kitchenette,'
                      ' dining table, and large bathroom. Perfect for families with children.',
                'ru': 'Просторный семейный номер с отдельными спальными зонами. Две двуспальные кровати, диван,'
                      ' мини-кухня, обеденный стол и большая ванная комната. Идеально для семей с детьми.'
            },
            'одноместный': {
                'en': 'Cozy single room ideal for solo travelers. Single bed, wardrobe, work area, free WiFi,'
                      ' and compact bathroom. Great value for business trips.',
                'ru': 'Уютный одноместный номер, идеальный для индивидуальных путешественников. Односпальная кровать, '
                      'гардероб, рабочая зона, бесплатный WiFi и компактная ванная. Отличный вариант для командировок.'
            },
            'люкс': {
                'en': 'Luxurious suite with premium furnishings. King-size bed, separate living room, dining area,'
                      ' luxury bathroom with jacuzzi, city/ocean view, and VIP amenities.',
                'ru': 'Роскошный люкс с премиальной мебелью. Королевская кровать, отдельная гостиная, обеденная зона, '
                      'роскошная ванная с джакузи, вид на город/океан и VIP-удобства.'
            }
        }

        # Базовые цены для разных типов номеров
        base_prices = {
            'стандарт': Decimal('5000'),
            'одноместный': Decimal('3500'),
            'семейный': Decimal('8000'),
            'люкс': Decimal('15000')
        }

        rooms = []
        for hotel in hotels:
            # Создаем 10 номеров для каждого отеля
            for room_num in range(1, 11):
                room_type = random.choice(room_types)

                # Цена зависит от типа номера и звездности отеля
                price = base_prices[room_type] * Decimal(str(hotel.hotel_stars or 3)) / Decimal('3')

                room = Room.objects.create(
                    hotel=hotel,
                    room_number=100 + room_num,
                    room_type=room_type,
                    room_status=random.choice(room_statuses),
                    price=price,
                    description_en=room_descriptions[room_type]['en'],
                    description_ru=room_descriptions[room_type]['ru']
                )
                rooms.append(room)

                # Создаем 3 изображения для каждого номера
            for j in range(3):
                RoomImage.objects.create(
                    room=room,
                    image=f'room_images/room_{room.id}_{j + 1}.png'
                )

        print(f"Создано {len(rooms)} номеров и {len(rooms) * 3} изображений")
        return rooms


def populate_bookings(clients, hotels, rooms):
    """Создание бронирований"""
    print("Создание бронирований...")

    bookings = []
    for i in range(10):
        client = random.choice(clients)
        room = random.choice(rooms)

        # Случайная дата заезда в пределах последних 60 дней или будущих 90 дней
        days_offset = random.randint(-60, 90)
        check_in = date.today() + timedelta(days=days_offset)

        # Длительность пребывания от 2 до 14 дней
        stay_duration = random.randint(2, 14)
        check_out = check_in + timedelta(days=stay_duration)

        booking = Booking.objects.create(
            user=client,
            hotel=room.hotel,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        bookings.append(booking)

    print(f"Создано {len(bookings)} бронирований")
    return bookings


def populate_reviews(clients, hotels):
    """Создание отзывов"""
    print("Создание отзывов...")

    reviews_data = [
        {
            'en': 'Excellent hotel! Amazing service, clean rooms, and friendly staff.'
                  ' The location is perfect and breakfast was delicious. Highly recommend!',
            'ru': 'Отличный отель! Потрясающий сервис, чистые номера и дружелюбный персонал. '
                  'Расположение идеальное, а завтрак был вкусным. Очень рекомендую!'
        },
        {
            'en': 'Great experience overall. Beautiful rooms with stunning views. '
                  'The spa was fantastic and the restaurant served excellent cuisine.',
            'ru': 'В целом отличный опыт. Красивые номера с потрясающим видом. '
                  'Спа был фантастическим, а ресторан подавал отличную кухню.'
        },
        {
            'en': 'Very comfortable stay. Staff went above and beyond to make our vacation special.'
                  ' Pool area was clean and well-maintained.',
            'ru': 'Очень комфортное пребывание. Персонал сделал все возможное,'
                  ' чтобы наш отпуск был особенным. Зона бассейна была чистой и ухоженной.'
        },
        {
            'en': 'Good hotel with nice amenities. Room was spacious and bed was comfortable. '
                  'WiFi could be faster but overall satisfied with the stay.',
            'ru': 'Хороший отель с приятными удобствами. Номер был просторным, кровать удобной.'
                  ' WiFi мог бы быть быстрее, но в целом доволен пребыванием.'
        },
        {
            'en': 'Perfect for family vacation! Kids loved the playground and pool. '
                  'Staff was very helpful with arranging activities. Will definitely come back.',
            'ru': 'Идеально для семейного отдыха! Дети любили площадку и бассейн. '
                  'Персонал был очень полезен в организации мероприятий. Обязательно вернемся.'
        },
        {
            'en': 'Wonderful boutique hotel with unique character. Attention to detail was impressive. '
                  'Breakfast selection was varied and tasty.',
            'ru': 'Замечательный бутик-отель с уникальным характером. Внимание к деталям было впечатляющим.'
                  ' Выбор завтрака был разнообразным и вкусным.'
        },
        {
            'en': 'Business trip perfection. Close to conference center, fast check-in, '
                  'and excellent business facilities. Room service was prompt.',
            'ru': 'Идеально для командировки. Близко к конференц-центру,'
                  ' быстрая регистрация и отличные бизнес-услуги. Обслуживание номеров было быстрым.'
        },
        {
            'en': 'Romantic getaway done right! Beautiful sunset views, private beach access, '
                  'and intimate dining options. Anniversary was memorable.',
            'ru': 'Романтический отдых получился отличным! Красивые виды заката,'
                  ' частный пляж и интимные варианты ужина. Годовщина была незабываемой.'
        },
        {
            'en': 'Clean, modern hotel in great location. Staff speaks multiple languages.'
                  ' Gym and pool were excellent. Value for money.',
            'ru': 'Чистый, современный отель в отличном месте. Персонал говорит на нескольких языках. '
                  'Тренажерный зал и бассейн были отличными. Соответствует цене.'
        },
        {
            'en': 'Peaceful mountain retreat. Fresh air, beautiful scenery, and cozy rooms.'
                  ' Hiking trails nearby. Perfect place to relax and unwind.',
            'ru': 'Спокойное горное убежище. Свежий воздух, красивые пейзажи и уютные номера. '
                  'Пешие тропы рядом. Идеальное место для отдыха и расслабления.'
        }
    ]

    reviews = []
    for i in range(10):
        # Генерируем случайную дату в прошлом
        random_date = datetime.now() - timedelta(days=random.randint(1, 365))

        # Создаем отзыв с created_date
        review = Review.objects.create(
            user=random.choice(clients),
            hotel=random.choice(hotels),
            stars=random.randint(4, 5),
            text_en=reviews_data[i]['en'],
            text_ru=reviews_data[i]['ru'],
            created_date=timezone.now()
        )
        reviews.append(review)

    print(f"Создано {len(reviews)} отзывов")
    return reviews


def main():
    """Главная функция"""
    print("=" * 80)
    print("НАЧАЛО ЗАПОЛНЕНИЯ БАЗЫ ДАННЫХ СИСТЕМЫ БРОНИРОВАНИЯ ОТЕЛЕЙ")
    print("=" * 80)

    # Очищаем базу данных
    clear_data()

    # Заполняем данные в правильном порядке
    countries = populate_countries()
    cities = populate_cities(countries)
    services = populate_services()
    clients, owners = populate_users(countries)
    hotels = populate_hotels(cities, services, owners)
    rooms = populate_rooms(hotels)
    bookings = populate_bookings(clients, hotels, rooms)
    reviews = populate_reviews(clients, hotels)

    print("=" * 80)
    print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА!")
    print("=" * 80)
    print(f"Всего создано:")
    print(f"  - Стран: {len(countries)}")
    print(f"  - Городов: {len(cities)}")
    print(f"  - Услуг: {len(services)}")
    print(f"  - Клиентов: {len(clients)}")
    print(f"  - Владельцев отелей: {len(owners)}")
    print(f"  - Отелей: {len(hotels)}")
    print(f"  - Изображений отелей: {len(hotels) * 4}")
    print(f"  - Номеров: {len(rooms)}")
    print(f"  - Изображений номеров: {len(rooms) * 3}")
    print(f"  - Бронирований: {len(bookings)}")
    print(f"  - Отзывов: {len(reviews)}")
    print(f"\nВсе данные на двух языках: English, Русский")
    print(f"Переведенные поля: country_name, city_name, service_name,")
    print(f"hotel_name, street, hotel description, room description, review text")
    print(f"UserProfile (first_name, last_name, username) - БЕЗ переводов")
    print("=" * 80)


if __name__ == '__main__':
    main()






