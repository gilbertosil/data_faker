import random
import json
import pandas as pd
import numpy as np
from faker import Faker
from typing import List,Dict, Any
from datetime import datetime, timedelta, date

fake = Faker('pt_BR')

class SalesDataGenerator:
    def __init__(self):
        # Estados do Brasil
        self.states = {
            'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas',
            'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 
            'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão',
            'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
            'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco',
            'PI': 'Piauí', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
            'RS': 'Rio Grande do Sul', 'RO': 'Rondônia', 'RR': 'Roraima',
            'SC': 'Santa Catarina', 'SP': 'São Paulo', 'SE': 'Sergipe', 'TO': 'Tocantins'
        }

        # Categorias de Produto fixas
        self.categories = {
            'Eletrônicos': ['Smartphone', 'Notebook', 'TV', 'Tablet', 'Fones de Ouvido'],
            'Roupas': ['Camiseta', 'Calça Jeans', 'Vestido', 'Tênis', 'Casaco'],
            'Alimentos': ['Arroz', 'Feijão', 'Carne', 'Frutas', 'Legumes'],
            'Móveis': ['Sofá', 'Cama', 'Mesa', 'Cadeira', 'Armário'],
            'Automotivo': ['Pneu', 'Bateria', 'Óleo', 'Farol', 'Volante']
        }        

        self.payment_methods = [
            'Cartão de Crédito', 'Cartão de Débito', 'PIX', 
            'Boleto', 'Dinheiro', 'Transferência Bancária']

    def _get_region(self, state: str) -> str:
        """Obtem a regiao do Pais do Estado"""
        regions = {
            'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
            'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
            'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
            'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
            'Sul': ['PR', 'RS', 'SC']
        }
        
        for region, states in regions.items():
            if state in states:
                return region
        return 'Unknown'
    
    def _get_state_vat(self, state: str) -> float:
        """Obtem o percentual do imposto (simulacao de ICMS)"""
        vat_rates = {
            'SP': 0.18, 'RJ': 0.20, 'MG': 0.19, 'ES': 0.17,
            'PR': 0.18, 'RS': 0.19, 'SC': 0.17, 'DF': 0.18,
            'GO': 0.17, 'MT': 0.17, 'MS': 0.17, 'BA': 0.19,
            'CE': 0.18, 'PE': 0.19, 'PA': 0.17, 'AM': 0.18
        }
        return vat_rates.get(state, 0.18)
    
    def _get_regional_discount(self, state: str) -> float:
        """Obtem desconto baseado na regiao"""
        discounts = {
            'SP': 0.05, 'RJ': 0.04, 'MG': 0.03, 'PR': 0.04,
            'RS': 0.03, 'SC': 0.03, 'DF': 0.04, 'BA': 0.02
        }
        return discounts.get(state, 0.02)

    def generate_customer(self) -> Dict[str, Any]:
        """Gera os dados fakes de clientes brasileiros"""
        return {
            'customer_id': fake.uuid4()[:8],
            'name': fake.name(),
            'cpf': fake.cpf(),
            'email': fake.email(),
            'phone': fake.cellphone_number(),
            'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d'),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'state': fake.random_element(list(self.states.keys())),
            'zip_code': fake.postcode()
        }

    def generate_product(self) -> Dict[str, Any]:
        """Gera os dados fakes de produto"""
        category = random.choice(list(self.categories.keys()))
        product_name = random.choice(self.categories[category])
        
        return {
            'product_id': f"PROD{random.randint(1000, 9999)}",
            'product_name': product_name,
            'category': category,
            'subcategory': product_name,
            'brand': fake.company(),
            'price': round(random.uniform(50, 5000), 2),
            'cost': round(random.uniform(30, 4000), 2),
            'profit_margin': round(random.uniform(0.1, 0.5), 3)
        }

    def generate_sale(self, customer: Dict, product: Dict, date: datetime) -> Dict[str, Any]:
        """Gera um registro de venda"""
        quantity = random.randint(1, 5)
        unit_price = product['price']
        total_price = unit_price * quantity
        payment_method = random.choice(self.payment_methods)
        
        # Add regional variations based on state
        state = customer['state']
        state_vat = self._get_state_vat(state)
        discount = self._get_regional_discount(state)
        
        return {
            'sale_id': f"SALE{random.randint(100000, 999999)}",
            'sale_date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'customer_id': customer['customer_id'],
            'product_id': product['product_id'],
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'payment_method': payment_method,
            'state': state,
            'state_name': self.states[state],
            'region': self._get_region(state),
            'vat_rate': state_vat,
            'vat_amount': round(total_price * state_vat, 2),
            'discount': discount,
            'final_price': round(total_price * (1 - discount), 2),
            'profit': round((product['price'] - product['cost']) * quantity, 2),
            'shipping_cost': round(random.uniform(10, 50), 2),
            'delivery_days': random.randint(1, 10)
        }

    def generate_sales(self, num_records: int = 1000, 
                           start_date: str = '2026-01-01',
                           end_date: str = '2026-01-31') -> List[Dict[str, Any]]:
        """Gera uma lista de vendas"""
        
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        sales = []
        customers = [self.generate_customer() for _ in range(100)]
        products = [self.generate_product() for _ in range(50)]
        
        for _ in range(num_records):
            customer = random.choice(customers)
            product = random.choice(products)
            random_date = start + timedelta(
                days=random.randint(0, (end - start).days),
                hours=random.randint(8, 20),
                minutes=random.randint(0, 59)
            )
            
            sale = self.generate_sale(customer, product, random_date)
            sales.append(sale)
        
        return sales

    def generate_dataset(self, num_records: int = 5000):
        """Gera um dataset completo e salva os dados"""
        
        print("Gerandos dados de venda...")
        sales = self.generate_sales(num_records)        
        df_sales = pd.DataFrame(sales)
        
        # Gera os dados relacionados
        customers = [self.generate_customer() for _ in range(100)]
        products = [self.generate_product() for _ in range(50)]        
        
        # Gerar estatisticas resumidas
        summary = self.generate_summary_statistics(df_sales)        
        
        return df_sales, customers, products, summary
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Gera estatísticas resumidas"""
        
        summary = {
            'total_sales': len(df),
            'total_revenue': df['final_price'].sum(),
            'total_profit': df['profit'].sum(),
            'avg_sale_value': df['final_price'].mean(),
            'sales_by_state': df.groupby('state_name')['final_price'].sum().to_dict(),
            'sales_by_region': df.groupby('region')['final_price'].sum().to_dict(),
            'top_products': df.groupby('product_id')['quantity'].sum().nlargest(5).to_dict(),
            'payment_method_distribution': df['payment_method'].value_counts().to_dict(),
            'monthly_sales': df.groupby(pd.to_datetime(df['sale_date']).dt.to_period('M'))['final_price'].sum().to_dict()
        }        
            
        return summary


def generate_data():
    print("Inicio da Aplicação")
    generator = SalesDataGenerator()
    customer = generator.generate_customer()
    print(customer)
    product = generator.generate_product()
    print(product)
    sale = generator.generate_sale(customer,product, date.today())
    print(sale)
    sales = generator.generate_sales(500)
    print(sales)
    sales_data, customers, products, summary = generator.generate_dataset(2000)


if __name__ == "__main__":
    generate_data()