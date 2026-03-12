import logging

logging.basicConfig(level=logging.INFO, format='%(message)s',
                    handlers=[logging.FileHandler('game_.log', encoding='utf-8'),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

cost_matrix = [
    [6, 15, 20, 24],  
    [17, 7, 19, 28],    
    [23, 12, 9, 23],   
    [25, 18, 16, 15]    
]
strategies = ["А1 (10)", "А2 (15)", "А3 (20)", "А4 (25)"]
nature = ["П1 (10)", "П2 (15)", "П3 (20)", "П4 (25)"]

def print_header(title):
    logger.info(title)

def build_risk_matrix(matrix):
    logger.info("\nМатрица рисков:")
    b_j = [min(col) for col in zip(*matrix)]
    logger.info(f"min по столбцам: {b_j}")
    
    risk_matrix = []
    for i in range(len(matrix)):
        row = [matrix[i][j] - b_j[j] for j in range(len(matrix[0]))]
        risk_matrix.append(row)
        logger.info(f"{strategies[i]}: {row}")
    return risk_matrix

def wald_criterion(matrix):
    print_header("КРИТЕРИЙ ВАЛЬДА")
    values = [max(row) for row in matrix]
    for i, val in enumerate(values):
        logger.info(f"{strategies[i]}: max = {val}")
    
    min_val = min(values)
    idx = values.index(min_val)
    logger.info(f"Оптимальная стратегия: {strategies[idx]}, значение = {min_val}")
    return idx, min_val

def savage_criterion(risk_matrix):
    print_header("КРИТЕРИЙ СЭВИДЖА")
    values = [max(row) for row in risk_matrix]
    for i, val in enumerate(values):
        logger.info(f"{strategies[i]}: max риск = {val}")
    
    min_val = min(values)
    idx = values.index(min_val)
    logger.info(f"Оптимальная стратегия: {strategies[idx]}, значение = {min_val}")
    return idx, min_val

def hurwicz_criterion(matrix, p=0.5):
    print_header(f"КРИТЕРИЙ ГУРВИЦА (p = {p})")
    values = []
    for i in range(len(matrix)):
        min_val = min(matrix[i])
        max_val = max(matrix[i])
        h = p * min_val + (1-p) * max_val
        values.append(h)
        logger.info(f"{strategies[i]}: {p}*{min_val} + {1-p}*{max_val} = {h:.1f}")
    
    min_val = min(values)
    idx = values.index(min_val)
    logger.info(f"Оптимальная стратегия: {strategies[idx]}, значение = {min_val:.1f}")
    return idx, min_val

def save_report(results):
    with open('report.txt', 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ\n")
        f.write(f"Матрица затрат:\n")
        for i in range(len(strategies)):
            f.write(f"{strategies[i]}: {cost_matrix[i]}\n")
        f.write(f"Критерий Вальда:    {strategies[results['wald'][0]]}\n")
        f.write(f"Критерий Сэвиджа:   {strategies[results['savage'][0]]}\n")
        f.write(f"Критерий Гурвица:   {strategies[results['hurwicz'][0]]}\n")

def main():
    print_header("ПРИНЯТИЕ РЕШЕНИЙ В УСЛОВИЯХ НЕОПРЕДЕЛЕННОСТИ")
    
    logger.info("\nМатрица затрат:")
    for i in range(len(strategies)):
        logger.info(f"{strategies[i]}: {cost_matrix[i]}")
    
    risk_matrix = build_risk_matrix(cost_matrix)
    
    results = {
        'wald': wald_criterion(cost_matrix),
        'savage': savage_criterion(risk_matrix),
        'hurwicz': hurwicz_criterion(cost_matrix, 0.5)
    }
    
    print_header("ИТОГОВЫЕ РЕЗУЛЬТАТЫ")
    logger.info(f"Критерий Вальда:    {strategies[results['wald'][0]]}")
    logger.info(f"Критерий Сэвиджа:   {strategies[results['savage'][0]]}")
    logger.info(f"Критерий Гурвица:   {strategies[results['hurwicz'][0]]}")
    
    save_report(results)
    logger.info("\nОтчет сохранен в файл report.txt")

if __name__ == "__main__":
    main()