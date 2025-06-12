import time
import re
import sys
import random

def main():
    # Баннер Google Maps из символов
    banner = r"""
   _____       _           _   _____          _        
  / ____|     | |         | | |  __ \        | |       
 | |  __  ___ | | ___ __ _| | | |__) |___  __| |_ __   
 | | |_ |/ _ \| |/ / '__| | | |  _  // _ \/ _` | '_ \  
 | |__| | (_) |   <| |  | |_| | | \ \  __/ (_| | |_) | 
  \_____|\___/|_|\_\_|   \___/|_|  \_\___|\__,_| .__/  
                                               | |     
                                               |_|     
  """
    print(banner)
    print("\nПродолжить по Enter...")
    input()
    
    # Проверка аргументов командной строки
    args = " ".join(sys.argv[1:])
    if not args:
        print("Использование: -q <кол-во телефонов> -r <маршрут> [-dtp <координаты ДТП>] [-block <координаты перекрытия>]")
        print("Пример: -q 100 -r от 59.700671,30.784673 до 59.708113,30.783986 -dtp 59.7045,30.7850 -block 59.7058,30.7842")
        return
    
    # Парсинг аргументов
    dtp_coords = None
    block_coords = None
    try:
        phones = int(re.search(r'-q\s+(\d+)', args).group(1))
        route_match = re.search(r'-r\s+от\s+([\d.]+),([\d.]+)\s+до\s+([\d.]+),([\d.]+)', args)
        start_lat, start_lon = route_match.group(1), route_match.group(2)
        end_lat, end_lon = route_match.group(3), route_match.group(4)
        
        # Проверка наличия координат ДТП
        dtp_match = re.search(r'-dtp\s+([\d.]+),([\d.]+)', args)
        if dtp_match:
            dtp_coords = (dtp_match.group(1), dtp_match.group(2))
            
        # Проверка наличия координат перекрытия
        block_match = re.search(r'-block\s+([\d.]+),([\d.]+)', args)
        if block_match:
            block_coords = (block_match.group(1), block_match.group(2))
            
    except (AttributeError, ValueError):
        print("Ошибка в формате аргументов!")
        print("Правильный формат: -q <число> -r от <lat>,<lon> до <lat>,<lon>")
        print("Дополнительно: -dtp <lat>,<lon> -block <lat>,<lon>")
        return
    
    # Выбор навигаторов
    nav_options = {
        1: {"name": "Google Maps", "icon": "🟢", "delay": 0.2},
        2: {"name": "Яндекс.Карты", "icon": "🔵", "delay": 0.3},
        3: {"name": "2ГИС", "icon": "🟠", "delay": 0.25},
        4: {"name": "Все навигаторы", "icon": "🌀", "delay": 0.1}
    }
    
    print("\nВыберите навигаторы (через запятую):")
    for key, option in nav_options.items():
        print(f"[{key}] {option['icon']} {option['name']}")
    
    try:
        choices = list(map(int, input("> ").split(',')))
        selected_navs = []
        
        if 4 in choices:
            # Выбраны все навигаторы
            selected_navs = [nav_options[1], nav_options[2], nav_options[3]]
        else:
            for choice in choices:
                if choice in [1, 2, 3]:
                    selected_navs.append(nav_options[choice])
        
        if not selected_navs:
            print("Ошибка выбора! Используются все навигаторы по умолчанию")
            selected_navs = [nav_options[1], nav_options[2], nav_options[3]]
    
    except ValueError:
        print("Ошибка ввода! Используются все навигаторы по умолчанию")
        selected_navs = [nav_options[1], nav_options[2], nav_options[3]]
    
    # Распределение телефонов по навигаторам
    nav_phones = {nav['name']: 0 for nav in selected_navs}
    for i in range(phones):
        nav = random.choice(selected_navs)
        nav_phones[nav['name']] += 1
    
    # Эмуляция создания пробки
    print(f"\n🚗 Запуск {phones} телефонов...")
    print(f"📍 Маршрут: от ({start_lat}, {start_lon}) до ({end_lat}, {end_lon})")
    
    if dtp_coords:
        print(f"🚨 ДТП создано в точке ({dtp_coords[0]}, {dtp_coords[1]})")
        
    if block_coords:
        print(f"🚧 Перекрытие дороги в точке ({block_coords[0]}, {block_coords[1]})")
    
    print("🛑 Начинаем создавать пробку")
    print(f"📱 Распределение по навигаторам:")
    
    for nav in selected_navs:
        count = nav_phones[nav['name']]
        print(f"   {nav['icon']} {nav['name']}: {count} телефонов")
    
    completed = 0
    traffic_events = []
    
    # Эмуляция событий на дороге
    for i in range(phones):
        # Случайное создание событий при достижении 30% и 70% прогресса
        percent = (i+1) / phones * 100
        if percent > 30 and random.random() < 0.1 and not traffic_events:
            traffic_events.append("🚥 Замедление движения")
            print(f"\n🚥 На маршруте обнаружено замедление движения!")
            
        if percent > 50 and random.random() < 0.1 and len(traffic_events) < 2:
            traffic_events.append("🚦 Перегруженность на развязке")
            print(f"\n🚦 На развязке образовалась перегруженность!")
    
    completed = 0
    for nav in selected_navs:
        count = nav_phones[nav['name']]
        for i in range(count):
            completed += 1
            percent = completed / phones * 100
            delay = nav['delay'] * random.uniform(0.8, 1.2)
            
            # Добавляем дополнительную задержку при создании событий
            if dtp_coords and percent > 40 and random.random() < 0.3:
                delay *= 2
            if block_coords and percent > 60 and random.random() < 0.4:
                delay *= 1.8
                
            print(f"{nav['icon']} Телефон {completed}/{phones} "
                  f"({nav['name']}) строит маршрут... "
                  f"[{'█' * int(percent//5)}{'░' * (20 - int(percent//5))}] {percent:.1f}%", 
                  end='\r')
            time.sleep(delay)
    
    # Расчет интенсивности пробки
    intensity = phones * 10
    if dtp_coords:
        intensity += phones * 5
    if block_coords:
        intensity += phones * 7
    if dtp_coords and block_coords:
        intensity += phones * 15
    
    print("\n" + "✅ Пробка успешно создана!".center(50))
    print(f"🔥 Интенсивность трафика выросла на {int(intensity)}%".center(50))
    
    # Отчет о событиях
    print("\n📊 Отчет о дорожной ситуации:")
    if dtp_coords:
        print(f"  🚨 ДТП в точке ({dtp_coords[0]}, {dtp_coords[1]}) - пробка +{phones * 5}%")
    if block_coords:
        print(f"  🚧 Перекрытие в точке ({block_coords[0]}, {block_coords[1]}) - пробка +{phones * 7}%")
    if dtp_coords and block_coords:
        print(f"  ⚠️ Комбинированный эффект ДТП + перекрытие - пробка +{phones * 15}%")
    
    print("\n🚦 Прочие события:")
    if traffic_events:
        for event in traffic_events:
            print(f"  {event}")
    else:
        print("  ⛟ Дорожная ситуация в норме")
    
    print("\nСтатистика по навигаторам:")
    for nav in selected_navs:
        count = nav_phones[nav['name']]
        print(f"   {nav['icon']} {nav['name']}: {count} запросов")

if __name__ == "__main__":
    main()
