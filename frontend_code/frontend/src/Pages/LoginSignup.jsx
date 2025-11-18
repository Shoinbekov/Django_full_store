// LoginSignup.jsx (ОКОНЧАТЕЛЬНО ИСПРАВЛЕННЫЙ КОД)
import React, { useState } from "react";
import "./CSS/LoginSignup.css";
import axios from "axios";

// Настройка Axios для отправки куки во всех запросах
const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    withCredentials: true, // 🚨 ГЛАВНОЕ ИЗМЕНЕНИЕ: Включаем отправку куки
});

export const LoginSignup = () => {
    const [isLogin, setIsLogin] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            let res;

            if (isLogin) {
                // 🔐 ЛОГИН
                res = await api.post("login/", { username, password });
                
                // ✅ Успех: Сохраняем флаг логина
                localStorage.setItem('auth-token', 'logged_in'); 
                alert(res.data.message);
                // Перезагрузка для обновления контекста ShopContext и Navbar
                window.location.replace("/"); 

            } else {
                // 📝 РЕГИСТРАЦИЯ
                res = await api.post("register/", { username, email, password, password_confirm: password });
                
                alert(res.data.message || "Регистрация успешна! Войдите в систему.");
                setIsLogin(true); // Переключаем на Login после успешной регистрации
            }

            setUsername("");
            setEmail("");
            setPassword("");
            
        } catch (error) {
            console.error("Ошибка запроса:", error.response?.data || error.message);
            const errorMessage = error.response?.data?.error || 
                                 error.response?.data?.message || 
                                 JSON.stringify(error.response?.data) ||
                                 "Ошибка при входе или регистрации.";
            alert(`Ошибка: ${errorMessage}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        // ... (ваш JSX код без изменений)
        <div className="loginsignup">
            <div className="loginsignup-container">
                <h1>{isLogin ? "Login" : "Sign Up"}</h1>
                <form className="loginsignup-fields" onSubmit={handleSubmit}>
                    {/* ... (поля ввода) ... */}
                    <input
                        type="text"
                        placeholder="Your Name"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    {!isLogin && (
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    )}
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? "Please wait..." : "Continue"}
                    </button>
                </form>
                {/* ... (остальной текст и переключение) ... */}
                <p className="loginsignup-login">
                    {isLogin
                        ? "Don't have an account?"
                        : "Already have an account?"}{" "}
                    <span onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? "Sign up here" : "Login here"}
                    </span>
                </p>
                <div className="loginsignup-agree">
                    <input type="checkbox" />
                    <p>
                        By continuing, I agree to the terms of use & privacy policy.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default LoginSignup;