"""insert

Revision ID: 034481c5a10a
Revises: 3ca8387855d3
Create Date: 2023-11-15 04:00:38.132926

"""
import uuid

from alembic import op
import sqlalchemy as sa
from datetime import datetime

from core import Base


# revision identifiers, used by Alembic.
revision = '034481c5a10a'
down_revision = '3ca8387855d3'
branch_labels = None
depends_on = None

def get_uuid():
    return str(uuid.uuid4())

def upgrade() -> None:
    test_user_id = get_uuid()
    password = "$2y$10$nhZM2l64rtV1ngfoZ49Ogu4mUP6Kkajt/Ts1paqxrfofiQ5PtLnk6"
    
    op.bulk_insert(
        Base.metadata.tables['users'],
        [
            {
                'id': test_user_id,
                'email': "test@mail.ru",
                'password': password,
                'first_name': "Test",
                'last_name': "Test",
                'father_name': "Test",
                'phone_number': "+7-707-000-00-00"
            }
        ]
    )
    
    psychology_genre_id = get_uuid()
    roman_genre_id = get_uuid()
    fantasy_genre_id = get_uuid()
    horror_genre_id = get_uuid()
    
    op.bulk_insert(
        Base.metadata.tables['genres'],
        [
            {
                'id': psychology_genre_id,
                'name': 'Психология'
            },
            {
                'id': roman_genre_id,
                'name': 'Роман'
            },
            {
                'id': fantasy_genre_id,
                'name': 'Фэнтези'
            },
            {
                'id': horror_genre_id,
                'name': 'Ужасы'
            },
            {
                'id': get_uuid(),
                'name': 'Драма'
            },
            {
                'id': get_uuid(),
                'name': 'Наука'
            },
            {
                'id': get_uuid(),
                'name': 'Биография'
            },
            {
                'id': get_uuid(),
                'name': 'Приключения'
            },
            {
                'id': get_uuid(),
                'name': 'Криминал'
            },
            {
                'id': get_uuid(),
                'name': 'Исторический'
            },
            {
                'id': get_uuid(),
                'name': 'Религия'
            }
        ]
    )
    
    napoleon_hill_author_id = get_uuid()
    robert_kiyosaki_author_id = get_uuid()
    anna_todd_author_id = get_uuid()
    james_dashner_author_id = get_uuid()
    
    op.bulk_insert(
        Base.metadata.tables['authors'],
        [
            {
                'id': napoleon_hill_author_id,
                'name': 'Наполеон Хилл'
            },
            {
                'id': robert_kiyosaki_author_id,
                'name': 'Роберт Кийосаки'
            },
            {
                'id': anna_todd_author_id,
                'name': 'Анна Тодд'
            },
            {
                'id': james_dashner_author_id,
                'name': 'Джеймс Дашнер'
            },
            {
                'id': get_uuid(),
                'name': 'Уильям Шекспир'
            },
            {
                'id': get_uuid(),
                'name': 'Альберт Эйнштейн'
            },
            {
                'id': get_uuid(),
                'name': 'Леонид Леонов'
            },
            {
                'id': get_uuid(),
                'name': 'Агата Кристи'
            },
            {
                'id': get_uuid(),
                'name': 'Джейн Остин'
            },
            {
                'id': get_uuid(),
                'name': 'Фёдор Достоевский'
            },
            {
                'id': get_uuid(),
                'name': 'Марк Твен'
            },
            {
                'id': get_uuid(),
                'name': 'Жюль Верн'
            }
        ]
    )
    
    op.bulk_insert(
        Base.metadata.tables['books'],
        [
            {
                'id': get_uuid(),
                'name': 'Думай и богатей',
                'author_id': napoleon_hill_author_id,
                'genre_id': psychology_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            },
            {
                'id': get_uuid(),
                'name': 'Богатый папа, бедный папа',
                'author_id': robert_kiyosaki_author_id,
                'genre_id': psychology_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            },
            {
                'id': get_uuid(),
                'name': 'После',
                'author_id': anna_todd_author_id,
                'genre_id': roman_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            },
            {
                'id': get_uuid(),
                'name': 'Лабиринт',
                'author_id': james_dashner_author_id,
                'genre_id': fantasy_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            },
            {
                'id': get_uuid(),
                'name': 'Испытание огнем',
                'author_id': james_dashner_author_id,
                'genre_id': fantasy_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            }, {
                'id': get_uuid(),
                'name': 'Лекарство от смерти',
                'author_id': james_dashner_author_id,
                'genre_id': fantasy_genre_id,
                'publisher_id': test_user_id,
                'year': 2019,
                'image_link': 'https://book24.kz/upload/iblock/7a5/7a54b6b34d9d7a46741ad7b8f2fc9836.jpg',
            }
        ]
    )


def downgrade() -> None:
    pass
