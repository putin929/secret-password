#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор безопасных паролей
Создает настраиваемые пароли с различными параметрами безопасности
"""

import random
import string
import secrets

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, 
                         use_symbols=True, exclude_ambiguous=False):
        """
        Генерирует пароль с заданными параметрами
        
        Args:
            length (int): Длина пароля
            use_uppercase (bool): Использовать заглавные буквы
            use_digits (bool): Использовать цифры
            use_symbols (bool): Использовать символы
            exclude_ambiguous (bool): Исключить двусмысленные символы (0, O, l, 1)
        
        Returns:
            str: Сгенерированный пароль
        """
        characters = self.lowercase
        
        if use_uppercase:
            characters += self.uppercase
        if use_digits:
            characters += self.digits
        if use_symbols:
            characters += self.symbols
            
        if exclude_ambiguous:
            ambiguous = "0Ol1"
            characters = ''.join(char for char in characters if char not in ambiguous)
        
        # Используем secrets для криптографической безопасности
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return password
    
    def generate_memorable_password(self, num_words=4):
        """
        Генерирует запоминающийся пароль из слов
        
        Args:
            num_words (int): Количество слов в пароле
            
        Returns:
            str: Пароль из слов
        """
        words = [
            "apple", "banana", "cherry", "dragon", "eagle", "forest", "guitar", "house",
            "island", "jungle", "kitchen", "lion", "mountain", "ocean", "piano", "queen",
            "river", "sunset", "tiger", "universe", "village", "window", "yellow", "zebra"
        ]
        
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        # Делаем первую букву каждого слова заглавной и добавляем цифры
        password_words = [word.capitalize() for word in selected_words]
        password = ''.join(password_words) + str(secrets.randbelow(100))
        
        return password
    
    def check_password_strength(self, password):
        """
        Оценивает силу пароля
        
        Args:
            password (str): Пароль для проверки
            
        Returns:
            dict: Результат анализа пароля
        """
        score = 0
        feedback = []
        
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Пароль должен содержать минимум 8 символов")
            
        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Добавьте строчные буквы")
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Добавьте заглавные буквы")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Добавьте цифры")
            
        if any(c in self.symbols for c in password):
            score += 1
        else:
            feedback.append("Добавьте специальные символы")
            
        if len(password) >= 12:
            score += 1
            
        strength_levels = {
            0: "Очень слабый",
            1: "Слабый", 
            2: "Средний",
            3: "Хороший",
            4: "Сильный",
            5: "Очень сильный",
            6: "Отличный"
        }
        
        return {
            "score": score,
            "strength": strength_levels[score],
            "feedback": feedback
        }

def main():
    generator = PasswordGenerator()
    
    print("=== ГЕНЕРАТОР ПАРОЛЕЙ ===\n")
    
    while True:
        print("1. Сгенерировать обычный пароль")
        print("2. Сгенерировать запоминающийся пароль")
        print("3. Проверить силу пароля")
        print("4. Выход")
        
        choice = input("\nВыберите опцию (1-4): ")
        
        if choice == "1":
            try:
                length = int(input("Длина пароля (по умолчанию 12): ") or "12")
                use_uppercase = input("Использовать заглавные буквы? (y/n): ").lower() != 'n'
                use_digits = input("Использовать цифры? (y/n): ").lower() != 'n'
                use_symbols = input("Использовать символы? (y/n): ").lower() != 'n'
                exclude_ambiguous = input("Исключить двусмысленные символы? (y/n): ").lower() == 'y'
                
                password = generator.generate_password(
                    length, use_uppercase, use_digits, use_symbols, exclude_ambiguous
                )
                print(f"\nСгенерированный пароль: {password}")
                
                # Автоматическая проверка силы
                strength = generator.check_password_strength(password)
                print(f"Сила пароля: {strength['strength']} ({strength['score']}/6)")
                
            except ValueError:
                print("Ошибка: введите корректное число")
                
        elif choice == "2":
            try:
                num_words = int(input("Количество слов (по умолчанию 4): ") or "4")
                password = generator.generate_memorable_password(num_words)
                print(f"\nЗапоминающийся пароль: {password}")
                
                strength = generator.check_password_strength(password)
                print(f"Сила пароля: {strength['strength']} ({strength['score']}/6)")
                
            except ValueError:
                print("Ошибка: введите корректное число")
                
        elif choice == "3":
            password = input("Введите пароль для проверки: ")
            if password:
                result = generator.check_password_strength(password)
                print(f"\nСила пароля: {result['strength']} ({result['score']}/6)")
                if result['feedback']:
                    print("Рекомендации:")
                    for tip in result['feedback']:
                        print(f"  • {tip}")
            else:
                print("Пароль не может быть пустым")
                
        elif choice == "4":
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
