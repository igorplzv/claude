from graphviz import Digraph

def create_production_flowchart():
    # Создаем новый граф
    dot = Digraph(comment='Производственный процесс титанового эндопротеза')
    
    # Настройка параметров графа для PDF
    dot.attr(rankdir='TB', bgcolor='white')
    # Установка размера страницы для PDF (A4 landscape)
    dot.attr(size='11.7,8.3!') # размеры в дюймах
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', fontsize='10')
    
    colors = {
        'control': '#FFE6E6',
        'prep': '#E6F3FF',
        'production': '#E6FFE6',
        'treatment': '#F2E6FF',
        'finish': '#FFF2E6'
    }
    
    nodes = [
        ('in_control_1', 'Входной контроль платформ\n(Оп. 003)\nКонтроль: геометрические размеры, плоскостность, шероховатость', colors['control']),
        
        ('in_control_2', 'Входной контроль порошка\n(Оп. 005)\nКонтроль: гранулометрический состав, насыпная плотность,\nхимический состав, влажность', colors['control']),
        
        ('prep_model', 'Подготовка файла модели\n(Оп. 010)\nКонтроль: целостность модели, поддержки,\nориентация, стратегия печати', colors['prep']),
        
        ('production', 'Аддитивное производство\n(Оп. 015)\nКонтроль: уровень O₂, температура платформы,\nпараметры лазера, качество слоя', colors['production']),
        
        ('powder_sieving', 'Просев порошка\nКонтроль: гранулометрический состав,\nотсутствие посторонних включений', colors['prep']),
        
        ('cutting', 'Электроэрозионная отрезка\n(Оп. 017)\nКонтроль: качество реза, перпендикулярность,\nотсутствие дефектов', colors['treatment']),
        
        ('manual_processing', 'Слесарная обработка\n(Оп. 019)\nУдаление поддержек,\nчерновая подготовка поверхности', colors['treatment']),
        
        ('heat_treatment', 'Термическая обработка\n(Оп. 020)\nКонтроль: температура, вакуум,\nвремя выдержки, скорость охлаждения', colors['treatment']),
        
        ('hip_stem', 'Горячее изостатическое прессование\n(Оп. 022)\nДля ножки протеза\nКонтроль: температура, давление, время', colors['treatment']),
        
        ('hip_cup', 'Вакуумный отжиг\n(Оп. 022)\nДля чашки протеза\nКонтроль: температура, вакуум, время', colors['treatment']),
        
        ('machining', 'Механическая обработка\n(Оп. 025)\nКонтроль: точность размеров,\nкачество поверхности, отклонения формы', colors['treatment']),
        
        ('mid_control', 'Промежуточный контроль\n(Оп. 027)\nКонтроль: геометрические параметры,\nкачество обработки', colors['control']),
        
        ('finishing', 'Финишная обработка\n(Оп. 030)\nКонтроль: шероховатость, отсутствие дефектов,\nравномерность обработки', colors['finish']),
        
        ('final_control', 'Контроль\n(Оп. 035)\nКонтроль: геометрия, шероховатость,\nмеханические свойства, структура', colors['control']),
        
        ('cleaning', 'Очистка и подготовка\n(Оп. 040)\nКонтроль: чистота поверхности,\nкачество очистки и сушки', colors['finish']),
        
        ('sterilization', 'Стерилизация\n(Оп. 045)\nКонтроль: параметры стерилизации,\nстерильность', colors['finish']),
        
        ('packing', 'Упаковка\n(Оп. 050)\nКонтроль: целостность упаковки,\nмаркировка, комплектность', colors['finish'])
    ]
    
    # Добавление узлов в граф
    for node_id, label, color in nodes:
        dot.node(node_id, label, fillcolor=color)
    
    # Добавление связей между узлами
    edges = [
        ('in_control_1', 'in_control_2'),
        ('in_control_2', 'prep_model'),
        ('prep_model', 'production'),
        ('production', 'cutting'),
        # Связь для просева порошка
        ('production', 'powder_sieving'),
        ('powder_sieving', 'in_control_2'),
        # Основной поток с измененной последовательностью
        ('cutting', 'manual_processing'),
        ('manual_processing', 'heat_treatment'),
        ('heat_treatment', 'hip_stem'),
        ('heat_treatment', 'hip_cup'),
        ('hip_stem', 'machining'),
        ('hip_cup', 'machining'),
        ('machining', 'mid_control'),
        ('mid_control', 'finishing'),
        ('finishing', 'final_control'),
        ('final_control', 'cleaning'),
        ('cleaning', 'sterilization'),
        ('sterilization', 'packing')
    ]
    
    # Добавление связей в граф
    for edge in edges:
        dot.edge(edge[0], edge[1])
    
    # Сохранение графа в PDF
    dot.render('production_flowchart', format='pdf', cleanup=True)

if __name__ == '__main__':
    create_production_flowchart()