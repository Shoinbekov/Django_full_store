import React, { createContext, useState, useEffect } from "react"
import all_product from "../Components/Assets/all_product";
import axios from "axios";

export const ShopContext = createContext(null);

// Настройка Axios для отправки куки
const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    withCredentials: true, // КРИТИЧНО для работы с сессиями Django
});

const getDefaultCart = () => {
    let cart = {};
    for (let index = 1; index <= all_product.length; index++) {
        cart[index] = 0;
    }
    return cart;
}

const ShopContextProvider = (props) => {
    const [cartItems, setCartItems] = useState(getDefaultCart());

    // 1. ПРИ ЗАГРУЗКЕ: Загружаем корзину с бэкенда
    useEffect(() => {
        if (localStorage.getItem('auth-token')) { 
            api.get('cart/')
            .then((response) => {
                const newCart = getDefaultCart();
                let totalItems = 0;

                response.data.forEach(item => {
                    newCart[item.product.id] = item.quantity;
                    totalItems += item.quantity;
                });
                
                setCartItems(newCart);
                console.log(`Корзина загружена, всего товаров: ${totalItems}`);
            })
            .catch((error) => {
                console.error("Ошибка при получении корзины:", error.response || error.message);
                // Если сессия истекла или 401/403, очищаем токен
                if (error.response && (error.response.status === 401 || error.response.status === 403)) {
                     localStorage.removeItem('auth-token');
                     window.location.replace("/login");
                }
            });
        }
    }, []);


    // 2. ФУНКЦИЯ ДОБАВЛЕНИЯ В КОРЗИНУ
    const addToCart = (itemId) => {
        if (!localStorage.getItem('auth-token')) {
             alert("Вы не залогинены. Пожалуйста, войдите, чтобы сохранить корзину!");
             window.location.replace("/login");
             return;
        }

        // Локальное обновление для скорости
        setCartItems((prev) => ({ ...prev, [itemId]: prev[itemId] + 1 }));

        // Используем action 'cart/add_item/'
        api.post('cart/add_item/', { product_id: itemId })
        .then(response => {
            console.log("Товар добавлен на бэкенде:", response.data);
        })
        .catch(error => {
            console.error("Ошибка API при добавлении в корзину:", error.response);
            // Откатываем локальное состояние при ошибке
            setCartItems((prev) => ({ ...prev, [itemId]: prev[itemId] - 1 }));
            alert("Не удалось добавить товар. Проверьте логин и наличие товара.");
        });
    }
    
    // 3. ФУНКЦИЯ УДАЛЕНИЯ ИЗ КОРЗИНЫ
    const removeFromCart = (itemId) => {
        if (!localStorage.getItem('auth-token')) return;

        const currentQuantity = cartItems[itemId] || 0;
        if (currentQuantity <= 0) return;

        // Локальное уменьшение количества
        setCartItems((prev) => ({ ...prev, [itemId]: prev[itemId] > 0 ? prev[itemId] - 1 : 0 }));

        // Используем action 'cart/remove_item/'
        api.post('cart/remove_item/', { product_id: itemId })
        .then(response => {
            console.log("Товар удален на бэкенде:", response.data);
        })
        .catch(error => {
            console.error("Ошибка API при удалении с бэкенда:", error.response);
            // Если ошибка, откатываем локальное состояние
            setCartItems((prev) => ({ ...prev, [itemId]: currentQuantity })); 
            alert("Не удалось удалить товар. Пожалуйста, попробуйте снова.");
        });
    }

    // 4. ФУНКЦИЯ ОФОРМЛЕНИЯ ЗАКАЗА 
    const createOrder = async () => {
        if (!localStorage.getItem('auth-token')) {
            alert("Пожалуйста, войдите, чтобы оформить заказ.");
            return;
        }
        
        if (getTotalCartItems() === 0) {
            alert("Ваша корзина пуста.");
            return;
        }

        try {
            const response = await api.post('orders/', { status: 'Processing' });
            
            alert(`Заказ #${response.data.id} успешно оформлен!`);
            setCartItems(getDefaultCart()); 
            return response.data;

        } catch (error) {
            console.error("Ошибка при оформлении заказа:", error.response);
            alert("Не удалось оформить заказ. Пожалуйста, попробуйте позже.");
            return null;
        }
    }
    
    const getTotalCartAmount = () => {
        let totalAmount = 0;
        for (const item in cartItems) {
            if (cartItems[item] > 0) {
                const itemInfo = all_product.find(
                    (product) => product.id === Number(item)
                );
                if (itemInfo) {
                    totalAmount += itemInfo.new_price * cartItems[item];
                }
            }
        }
        return totalAmount; 
    };

    const getTotalCartItems = () => {
        let totalItem = 0;
        for(const item in cartItems){
            if(cartItems[item]>0){
                totalItem+= cartItems[item];
            }
        }
        return totalItem;
    }

    const contextValue = {getTotalCartItems, getTotalCartAmount, all_product, cartItems, addToCart, removeFromCart, createOrder};
    
    return (
        <ShopContext.Provider value={contextValue}>
            {props.children}
        </ShopContext.Provider>
    )
}

export default ShopContextProvider;