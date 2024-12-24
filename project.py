import os
import csv


class PriceMachine():

    def __init__(self):
        self.data = []

    def load_prices(self, file_path='.'):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт

            Допустимые названия для столбца с ценой:
                розница
                цена

            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        for filename in os.listdir(file_path):
            if 'price' in filename and filename.endswith('.csv'):
                with open(os.path.join(file_path, filename), newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)
                    product_index, price_index, weight_index = self._search_product_price_weight(headers)

                    if product_index is not None and price_index is not None and weight_index is not None:
                        for row in reader:
                            if row:
                                self.data.append({
                                    'name': row[product_index],
                                    'price': float(row[price_index]),
                                    'weight': float(row[weight_index]),
                                    'file': filename,
                                    'price_per_kg': float(row[price_index]) / float(row[weight_index])
                                })
        return self.data

    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        product_index = None
        price_index = None
        weight_index = None
        for i, header in enumerate(headers):
            if header.lower() in ['название', 'продукт', 'товар', 'наименование']:
                product_index = i
            elif header.lower() in ['цена', 'розница']:
                price_index = i
            elif header.lower() in ['вес', 'масса', 'фасовка']:
                weight_index = i

        return product_index, price_index, weight_index

    def export_to_html(self, fname='output.html'):
        sorted_positions = sorted(self.data, key=lambda x: x['price'])
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <style>td {padding-right: 20px;}</style>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for indx, position in enumerate(sorted_positions, start=1):
            result += f'<tr><td>{indx}</td><td>{position['name']}</td><td>{position['price']}</td><td>{
            position['weight']}</td><td>{position['file']}</td><td>{position['price_per_kg']:.2f}</td></tr>'
        result += '''
            </table>
        </body>
        </html>
        '''

        with open(fname, 'w', encoding='utf-8') as f:
            f.write(result)

    def find_text(self, text):
        found_position = []

        for item in self.data:
            if text.lower() in item['name'].lower():
                found_position.append(item)

        found_position.sort(key=lambda x: x['price_per_kg'])
        return found_position


if __name__ == '__main__':

    pm = PriceMachine()
    pm.load_prices()
    print('Данные загружены')
    print('Введите наименование позиции для поиска или "exit" для выхода')

    while True:
        req_from_user = input('Поиск: ')
        if req_from_user.lower() == 'exit':
            print('Работа программы завершена')
            break

        results = pm.find_text(req_from_user)

        if results:
            print(f"{'№':<3} {'Наименование':<40} {'Цена':<15} {'Вес (кг)':<14} {'Файл':<20} {'Цена за кг.':<10}")
            for idx, item in enumerate(results, start=1):
                print(f'{idx:<3} {item['name']:<40} {item['price']:<15} {item['weight']:<15}'
                      f'{item['file']:<20} {item['price_per_kg']:.2f}')
        else:
            print('Товары не найдены')

    pm.export_to_html()
    print('Все позиции выгружены в файл: "output.html"')
