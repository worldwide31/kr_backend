from decimal import Decimal

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import Company, CompanyRole, InventoryItem, OrderItem, Product, SupplyItem, Warehouse


MUSIC_PRODUCTS = [
    ("GTR-AC-001", "Акустическая гитара Yamaha F310 Natural", "Гитары акустические", "шт", "12800.00", "18990.00", 4, 18),
    ("GTR-AC-002", "Акустическая гитара Fender CD-60S Black", "Гитары акустические", "шт", "18600.00", "27990.00", 3, 12),
    ("GTR-CL-001", "Классическая гитара Martinez C-91C", "Гитары классические", "шт", "7200.00", "10990.00", 5, 22),
    ("GTR-EL-001", "Электрогитара Squier Sonic Stratocaster", "Электрогитары", "шт", "16900.00", "25990.00", 3, 10),
    ("GTR-EL-002", "Электрогитара Ibanez GRX40 Sunburst", "Электрогитары", "шт", "21400.00", "31990.00", 2, 8),
    ("GTR-BS-001", "Бас-гитара Squier Affinity Jazz Bass", "Бас-гитары", "шт", "26800.00", "39990.00", 2, 7),
    ("AMP-GT-001", "Гитарный комбоусилитель Boss Katana-50 MkII", "Гитарные усилители", "шт", "27900.00", "41990.00", 2, 6),
    ("AMP-GT-002", "Гитарный комбоусилитель Marshall MG15G", "Гитарные усилители", "шт", "10400.00", "15990.00", 3, 14),
    ("AMP-BS-001", "Басовый комбоусилитель Fender Rumble 40", "Басовые усилители", "шт", "20500.00", "30990.00", 2, 8),
    ("FX-001", "Педаль эффектов Boss DS-1 Distortion", "Гитарные эффекты", "шт", "5200.00", "7990.00", 8, 28),
    ("FX-002", "Педаль эффектов Electro-Harmonix Big Muff Pi", "Гитарные эффекты", "шт", "7600.00", "11990.00", 5, 16),
    ("STR-EL-010", "Струны Ernie Ball Regular Slinky 10-46", "Струны", "компл", "520.00", "890.00", 40, 160),
    ("STR-AC-011", "Струны D'Addario EJ16 Phosphor Bronze", "Струны", "компл", "650.00", "1090.00", 35, 140),
    ("STR-BS-045", "Струны D'Addario EXL165 Bass 45-105", "Струны", "компл", "2100.00", "3290.00", 12, 44),
    ("KEY-SYN-001", "Синтезатор Yamaha PSR-E373", "Клавишные инструменты", "шт", "19600.00", "29990.00", 2, 9),
    ("KEY-DP-001", "Цифровое пианино Casio CDP-S110", "Цифровые пианино", "шт", "31900.00", "47990.00", 2, 6),
    ("KEY-MID-001", "MIDI-клавиатура Arturia MiniLab 3", "MIDI-клавиатуры", "шт", "8900.00", "13990.00", 4, 18),
    ("KEY-MID-002", "MIDI-клавиатура Akai MPK Mini MK3", "MIDI-клавиатуры", "шт", "7800.00", "11990.00", 5, 22),
    ("DRM-AC-001", "Акустическая ударная установка Pearl Roadshow", "Ударные установки", "компл", "43800.00", "64990.00", 1, 4),
    ("DRM-EL-001", "Электронная ударная установка Roland TD-02K", "Электронные барабаны", "компл", "38600.00", "57990.00", 1, 5),
    ("DRM-CYM-001", "Комплект тарелок Zildjian Planet Z", "Тарелки", "компл", "13800.00", "20990.00", 2, 7),
    ("DRM-STK-001", "Барабанные палочки Vic Firth 5A", "Барабанные аксессуары", "пара", "420.00", "690.00", 45, 180),
    ("MIC-DYN-001", "Динамический микрофон Shure SM58", "Микрофоны", "шт", "7900.00", "11990.00", 6, 24),
    ("MIC-CND-001", "Конденсаторный микрофон Audio-Technica AT2020", "Микрофоны", "шт", "9600.00", "14990.00", 4, 15),
    ("MIC-USB-001", "USB-микрофон Fifine K669B", "USB-микрофоны", "шт", "3100.00", "4990.00", 8, 32),
    ("AUD-IF-001", "Аудиоинтерфейс Focusrite Scarlett Solo 4th Gen", "Аудиоинтерфейсы", "шт", "11800.00", "17990.00", 5, 18),
    ("AUD-IF-002", "Аудиоинтерфейс Behringer UMC204HD", "Аудиоинтерфейсы", "шт", "7200.00", "10990.00", 5, 20),
    ("MON-ST-001", "Студийные мониторы JBL 305P MkII, пара", "Студийные мониторы", "пара", "27800.00", "41990.00", 2, 8),
    ("MON-ST-002", "Студийные мониторы KRK Rokit 5 G4, пара", "Студийные мониторы", "пара", "32600.00", "48990.00", 2, 6),
    ("HPH-001", "Студийные наушники Audio-Technica ATH-M40x", "Наушники", "шт", "7200.00", "10990.00", 6, 26),
    ("HPH-002", "Студийные наушники Beyerdynamic DT 770 Pro 80 Ohm", "Наушники", "шт", "11800.00", "17990.00", 4, 16),
    ("MIX-AN-001", "Аналоговый микшер Yamaha MG10XU", "Микшерные пульты", "шт", "18400.00", "27990.00", 2, 7),
    ("MIX-DJ-001", "DJ-контроллер Pioneer DDJ-FLX4", "DJ-оборудование", "шт", "27800.00", "41990.00", 2, 6),
    ("SND-PA-001", "Активная акустическая система JBL EON710", "Концертный звук", "шт", "34200.00", "51990.00", 2, 5),
    ("SND-PA-002", "Сабвуфер Alto Professional TS12S", "Концертный звук", "шт", "42800.00", "63990.00", 1, 3),
    ("WND-SAX-001", "Альт-саксофон Yamaha YAS-280", "Духовые инструменты", "шт", "87200.00", "129990.00", 1, 3),
    ("WND-FLT-001", "Флейта Yamaha YFL-212", "Духовые инструменты", "шт", "38600.00", "57990.00", 1, 4),
    ("WND-HRM-001", "Губная гармоника Hohner Special 20 C", "Духовые инструменты", "шт", "2600.00", "4190.00", 10, 36),
    ("ORC-VLN-001", "Скрипка Stentor Student I 4/4", "Смычковые инструменты", "шт", "9600.00", "14990.00", 3, 10),
    ("ORC-CLL-001", "Виолончель Gewa Allegro VC1 4/4", "Смычковые инструменты", "шт", "51800.00", "77990.00", 1, 3),
    ("ACC-STN-001", "Гитарная стойка Hercules GS414B", "Стойки и держатели", "шт", "2600.00", "3990.00", 12, 40),
    ("ACC-STN-002", "Микрофонная стойка OnStage MS7701B", "Стойки и держатели", "шт", "2100.00", "3290.00", 15, 55),
    ("ACC-CBL-001", "Инструментальный кабель Kirlin 3 м", "Кабели", "шт", "620.00", "990.00", 50, 190),
    ("ACC-CBL-002", "Микрофонный кабель XLR Bespeco 5 м", "Кабели", "шт", "760.00", "1290.00", 45, 170),
    ("ACC-PDL-001", "Педалборд RockBoard DUO 2.1", "Гитарные аксессуары", "шт", "5200.00", "7990.00", 4, 14),
    ("ACC-TUN-001", "Тюнер-клипса Korg Pitchclip 2", "Тюнеры и метрономы", "шт", "980.00", "1590.00", 20, 75),
    ("ACC-MET-001", "Метроном Boss DB-30", "Тюнеры и метрономы", "шт", "2400.00", "3690.00", 10, 32),
    ("LGT-001", "LED PAR прожектор INVOLIGHT LEDPAR74", "Световое оборудование", "шт", "4300.00", "6990.00", 8, 24),
    ("LGT-002", "DMX-контроллер Chauvet Obey 40", "Световое оборудование", "шт", "7900.00", "11990.00", 3, 9),
    ("REC-001", "Портативный рекордер Zoom H1n", "Рекордеры", "шт", "7800.00", "11990.00", 5, 18),
]

LEGACY_DEMO_SKUS = ["DRY-100", "BOX-240"]


def get_or_create_company(db: Session, inn: str, defaults: dict) -> Company:
    company = db.scalar(select(Company).where(Company.inn == inn))
    if company:
        return company
    company = Company(inn=inn, **defaults)
    db.add(company)
    db.flush()
    return company


def get_or_create_warehouse(db: Session) -> Warehouse:
    warehouse = db.scalar(select(Warehouse).where(Warehouse.name == "Склад музыкального магазина"))
    if warehouse:
        return warehouse
    warehouse = Warehouse(
        name="Склад музыкального магазина",
        city="Москва",
        address="МКАД 42 км, логистический терминал 7",
        manager="Мария Белова",
    )
    db.add(warehouse)
    db.flush()
    return warehouse


def upsert_music_product(db: Session, warehouse: Warehouse, row: tuple[str, str, str, str, str, str, int, int]) -> None:
    sku, name, category, unit, purchase_price, sale_price, min_stock, quantity = row
    product = db.scalar(select(Product).where(Product.sku == sku))
    if not product:
        product = Product(
            sku=sku,
            name=name,
            category=category,
            unit=unit,
            purchase_price=Decimal(purchase_price),
            sale_price=Decimal(sale_price),
            min_stock=min_stock,
        )
        db.add(product)
        db.flush()
    inventory = db.scalar(
        select(InventoryItem).where(
            InventoryItem.product_id == product.id,
            InventoryItem.warehouse_id == warehouse.id,
        )
    )
    if not inventory:
        db.add(InventoryItem(product_id=product.id, warehouse_id=warehouse.id, quantity=quantity, reserved=0))
    elif inventory.quantity < quantity:
        inventory.quantity = quantity


def seed_demo_data(db: Session) -> None:
    referenced_order_ids = select(OrderItem.product_id).where(OrderItem.product_id == Product.id)
    referenced_supply_ids = select(SupplyItem.product_id).where(SupplyItem.product_id == Product.id)
    legacy_ids = list(
        db.scalars(
            select(Product.id)
            .where(Product.sku.in_(LEGACY_DEMO_SKUS))
            .where(~referenced_order_ids.exists())
            .where(~referenced_supply_ids.exists())
        )
    )
    if legacy_ids:
        db.execute(delete(InventoryItem).where(InventoryItem.product_id.in_(legacy_ids)))
        db.execute(delete(Product).where(Product.id.in_(legacy_ids)))

    get_or_create_company(
        db,
        "7701234567",
        {
            "name": "ООО Музыкальная Лавка",
            "role": CompanyRole.customer,
            "contact_name": "Анна Волкова",
            "email": "orders@music-lavka.ru",
            "phone": "+7 495 100-20-30",
            "address": "Москва, Ленинградский проспект, 15",
        },
    )
    get_or_create_company(
        db,
        "7809876543",
        {
            "name": "АО МузДистрибуция",
            "role": CompanyRole.supplier,
            "contact_name": "Игорь Соловьев",
            "email": "logistics@muzdist.ru",
            "phone": "+7 812 300-40-50",
            "address": "Санкт-Петербург, Обводный канал, 44",
        },
    )
    warehouse = get_or_create_warehouse(db)
    for row in MUSIC_PRODUCTS:
        upsert_music_product(db, warehouse, row)
    db.commit()
