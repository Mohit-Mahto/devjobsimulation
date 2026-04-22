const API_URL = 'https://devjob-backend.onrender.com/api';

document.addEventListener('DOMContentLoaded', () => {
    // Check if we are on the login page
    const loginForm = document.getElementById('loginForm');
    const authSwitch = document.getElementById('authSwitch');
    
    if (loginForm) {
        let isLogin = true;
        const formTitle = document.getElementById('formTitle');
        const submitBtn = document.getElementById('submitBtn');

        authSwitch.addEventListener('click', () => {
            isLogin = !isLogin;
            formTitle.innerText = isLogin ? 'Login to your account' : 'Create an account';
            submitBtn.innerText = isLogin ? 'Login' : 'Register';
            authSwitch.innerHTML = isLogin ? 'Don\'t have an account? <span>Register</span>' : 'Already have an account? <span>Login</span>';
        });

        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            const endpoint = isLogin ? '/auth/login' : '/auth/register';
            
            try {
                const response = await fetch(`${API_URL}${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();

                if (response.ok) {
                    localStorage.setItem('token', data.token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    window.location.href = 'index.html';
                } else {
                    alert(data.error || 'An error occurred');
                }
            } catch (err) {
                console.error(err);
                alert('Server connection failed');
            }
        });
    }

    // Protect routes
    const isAuthPage = window.location.pathname.includes('login.html');
    const token = localStorage.getItem('token');

    if (!token && !isAuthPage) {
        window.location.href = 'login.html';
    } else if (token && isAuthPage) {
        window.location.href = 'index.html';
    }

    // Logout logic
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = 'login.html';
        });
    }
});
